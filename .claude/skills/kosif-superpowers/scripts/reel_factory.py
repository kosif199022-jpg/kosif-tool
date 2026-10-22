#!/usr/bin/env python3
"""Reel factory — a voice, its word timings and licensed shots → a verified 9:16 reel (thin wrapper, no new renderer).

  python3 reel_factory.py plan  --audio VOICE [--audio-rights RIGHTS] [--audio-rights-evidence URL|FILE]
                                (--words words.json [--allow-words-mismatch]
                                 | --transcribe [--model medium] [--language ar] [--local-only] [--retranscribe])
                                (--shots shots.json | --shots-manifest manifest.json --shot-ids ID[@IN],ID,...)
                                [--title "دعاء يوم الخميس"] [--handle @kosif] [--credit "الصوت: @x"] [--phrases texts.json]
                                [--style gold-night|rose-dusk|emerald|ivory[:TRANSITIONS[:FRAME]]|SEED] [--min-shot 0.5]
                                [--out DIR] [--allow-tracked]
  python3 reel_factory.py build ...the same options... [--draft]

Input checks come first and write nothing: the audio must be AAC or MP3 (it is muxed with -c copy, never re-encoded,
and verify_video.py accepts only those two in a delivery MP4), and build first checks ffmpeg, ffprobe, node,
tools/render_html.cjs and Playwright's Chromium, so a missing tool is exit 2 before any transcription or rendering.

Rights record (advisory, never blocking — the owner's decision of 22-10 replaced the council's blocking gate):
whatever is declared is written to OUT/rights.json before any heavy work: --audio-rights (one of media_sources.RIGHTS)
with --audio-rights-evidence (an https URL or an existing local file) for anything but `owned`, and each shot's rights,
licence_url and credit (shots from a stock_fetch.py manifest take their licence from the manifest). Gaps (nothing
declared, a non-owned audio without evidence, a shot without an https licence or a credit) are listed in the record
as `gaps`, its status is `incomplete`, and one RIGHTS_NOTE line goes to stderr; the plan and the build go on.

Words: kosif-words/1, {"words": [...]}, a bare word list or whisper segments. They must belong to --audio: a declared
source.sha256 that is not the audio's, or a last word ending more than 0.25 s after the audio, is an input error
unless --allow-words-mismatch (plan.json → words.check records the result). --transcribe runs montage_pro.py
transcribe into OUT/words.json after the gate (--allow-tracked is passed on; --retranscribe replaces a words.json that
is up to date or hand-made) and records the engine and its measured time. Word-timing accuracy is not measured here.

plan: OUT/plan.json — phrases (words.json phrases, else whisper segments, else pauses ≥ 0.35 s, ≤ 6 words), one shot
per phrase cut at each phrase start (cycled when there are fewer shots), xfade transitions centred on the cuts, and
duration = audio + 1.0 s. A phrase that starts less than --min-shot (default and minimum 0.5 s: the 0.4 s xfade plus
0.1 s of clean footage) after the previous cut, or before the end, stays on the current shot and is listed in
plan.json → cut_rule.merged. Per-shot lengths include each 0.4 s xfade overlap; the plate is padded with its last
frame, so it always has exactly duration × 30 frames (build.json records the count it measured).
build: plan → ffmpeg plate (crop 4:5, 960×1200, 30 fps, JPG frames in OUT/build/plate) → assets/reel_scene.html with
the scene data inlined + Aref Ruqaa / Reem Kufi (OFL) → node tools/render_html.cjs (9:16, 30 fps) → the original
audio muxed with -c copy (never re-encoded) → verify_video.py --source-audio → OUT/TEST_REPORT.md + OUT/build.json.
--draft renders a 540×960 check copy (same 9:16 checks, faster).

OUT defaults to <repo>/out/reels/<slug of the title> (git-ignored) in a checkout, whatever the current folder, else
./out/reels/<slug>. A path inside the skill folder is always refused (its files ship with the skill); one inside a
git work tree that is tracked, not git-ignored, or under jobs/ is refused unless --allow-tracked.
Exit codes: 0 ok · 2 usage/input error (missing tool, unreadable file, bad option, undeliverable audio codec, words
from another recording) · 4 the build or its verification failed (BUILD_FAILED / VERIFY_FAILED). Rights never block.
Python 3.8+ stdlib; build needs ffmpeg/ffprobe, node and Playwright's Chromium (tools/render_html.cjs).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REPO = SKILL.parents[2]  # <repo>/.claude/skills/kosif-superpowers
sys.path.insert(0, str(HERE))
from media_sources import RIGHTS  # noqa: E402  one list of accepted rights for the whole skill

TEMPLATE = SKILL / "assets" / "reel_scene.html"
FONT_DIR = SKILL / "proofs" / "_shared" / "fonts"
FONTS = {"ArefRuqaa-Bold.ttf": "ArefRuqaa-Bold.ttf", "ReemKufi[wght].ttf": "ReemKufi.ttf",
         "OFL-ArefRuqaa.txt": "OFL-ArefRuqaa.txt", "OFL-ReemKufi.txt": "OFL-ReemKufi.txt"}
VERIFY = HERE / "verify_video.py"
MONTAGE = HERE / "montage_pro.py"
PY = sys.executable or "python3"
W, H, FPS = 1080, 1920, 30
XFADE, TAIL, PAUSE, MAX_WORDS = 0.4, 1.0, 0.35, 6
MIN_SHOT = round(XFADE + 0.1, 3)  # shortest shot whose two xfades do not overlap (3 clean frames between them)
WORDS_SLACK = 0.25  # the last word may end this much after the audio (rounding, a trailing breath)
SAFE = {"top": 220, "bottom": 1500}  # platform UI covers the top ~220 px and the bottom ~420 px of 1920
LAYOUT = {"panel": [90, 352, 900, 1125], "radius": 34, "title_y": 292, "ornament_y": 322, "text_cy": 1180,
          "text_max_w": 820, "handle_y": 1398, "credit_y": 1446}
DATA_TOKEN = "/*KOSIF_SCENE_DATA*/null"
STOCK_RIGHTS = {"pexels": "stock-license", "mixkit": "stock-license"}  # stock_fetch.py sources
CREDIT_RIGHTS = ("stock-license", "cc-by", "cc-by-sa")
DELIVERY_CODECS = ("aac", "mp3")  # the only codecs verify_video.py accepts in a delivery MP4 (audio is never re-encoded)
# How tools/render_html.cjs finds Playwright (cwd, /opt/node-tools, $KOSIF_PLAYWRIGHT); exit 0 ok, 3 no browser, 4 none.
CHROMIUM_JS = ("const c=[()=>require.resolve('playwright',{paths:[process.cwd()]}),()=>'/opt/node-tools/node_modules/playwright',"
               "()=>process.env.KOSIF_PLAYWRIGHT];for(const f of c){let s;try{s=f()}catch(e){continue}if(!s)continue;"
               "try{const m=require(s);if(m&&m.chromium){process.exit(require('fs').existsSync(m.chromium.executablePath())?0:3)}}"
               "catch(e){}}process.exit(4)")
PLATE_FILTER = ("crop='if(gt(iw/ih,0.8),ih*0.8,iw)':'if(gt(iw/ih,0.8),ih,iw/0.8)',"
                "scale=960:1200,setsar=1,fps=30,format=yuv420p")

PALETTES = {
    "gold-night": {"bg0": "#14244a", "bg1": "#050a17", "lattice": "rgba(242,196,109,0.075)", "accent": "#f2c46d",
                   "title": "#f2c46d", "text": "#fbf3df", "speak": "#f2c46d", "scrim": "5,10,23", "sweep": "255,236,180"},
    "rose-dusk": {"bg0": "#4a1d3a", "bg1": "#14060f", "lattice": "rgba(244,170,150,0.08)", "accent": "#f0a98f",
                  "title": "#f6c1ae", "text": "#fff1ea", "speak": "#ffc7a8", "scrim": "20,6,15", "sweep": "255,214,196"},
    "emerald": {"bg0": "#0f4a3e", "bg1": "#031410", "lattice": "rgba(230,196,106,0.07)", "accent": "#e6c46a",
                "title": "#e6c46a", "text": "#f3f7ef", "speak": "#f5d77f", "scrim": "3,20,16", "sweep": "255,238,170"},
    "ivory": {"bg0": "#fbf6ea", "bg1": "#e4d8bb", "lattice": "rgba(140,100,40,0.10)", "accent": "#b8862f",
              "title": "#3b2a14", "text": "#fffaf0", "speak": "#f3c66b", "scrim": "24,16,6", "sweep": "255,240,200"},
}
TRANSITION_SETS = {  # xfade names present since ffmpeg 4.3
    "reveal": ["fade", "circleopen", "wipedown", "fadewhite", "smoothup"],
    "soft": ["fade", "smoothdown", "fadewhite", "fadeblack"],  # no "dissolve": it switches pixels at random and reads as noise after the JPG plate
    "glide": ["smoothleft", "smoothup", "smoothright", "fade"],
}
FRAMES = ("rounded", "arch", "square")
PRESETS = {"gold-night": ("gold-night", "reveal", "rounded"), "rose-dusk": ("rose-dusk", "soft", "arch"),
           "emerald": ("emerald", "glide", "arch"), "ivory": ("ivory", "soft", "square")}


class Fail(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code


# ------------------------------------------------------------------ helpers
def sh(cmd, timeout=600):
    try:
        r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, "", f"timed out after {timeout} s: {Path(str(cmd[0])).name}"
    return r.returncode, r.stdout, r.stderr


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jread(p: Path, what: str):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Fail(2, f"{what}: cannot read {p}: {type(exc).__name__}: {exc}") from None


OUT_ROOT = None  # set by run(): every file the factory writes must resolve under it (no symlink may lead elsewhere)


def inside_out(p: Path):
    """Why P may not be written, or None: it, or a folder on the way to it, is a symlink, or it resolves outside OUT."""
    if OUT_ROOT is None:
        return None
    p = Path(p)
    try:
        rel = p.absolute().relative_to(OUT_ROOT)
    except ValueError:
        return f"{p} is outside {OUT_ROOT}"
    walk = OUT_ROOT
    for part in rel.parts:
        walk = walk / part
        if walk.is_symlink():
            return f"{walk} is a symlink (nothing is written through links inside {OUT_ROOT})"
    return None


def refuse_symlinks(out: Path):
    """OUT is the factory's own folder: a symlink anywhere inside it (file or folder) is refused before any write,
    so no write — jsave/tsave, the plate JPGs, fonts, scene, render, mux or verify output — can land elsewhere."""
    if out.is_symlink():
        raise Fail(2, f"refused to use {out}: it is a symlink")
    if not out.is_dir():
        return
    for root, dirs, files in os.walk(out, followlinks=False):
        for name in dirs + files:
            q = Path(root) / name
            if q.is_symlink():
                raise Fail(2, f"refused to use {out}: {q} is a symlink (nothing is written through links inside the out folder)")


def tsave(p: Path, text: str):
    why = inside_out(p)
    if why:
        raise Fail(2, f"refused to write {p}: {why}")
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    except OSError as exc:
        raise Fail(2, f"cannot write {p}: {type(exc).__name__}: {exc}") from None


def jsave(p: Path, data):
    tsave(p, json.dumps(data, ensure_ascii=False, indent=1) + "\n")


def last_json(text: str) -> dict:
    """The JSON object a child tool printed on its last non-empty stdout line ({} when there is none)."""
    for line in reversed((text or "").strip().splitlines()):
        try:
            doc = json.loads(line)
        except ValueError:
            continue
        return doc if isinstance(doc, dict) else {}
    return {}


def tail(text: str, n: int = 3) -> str:
    return " | ".join((text or "").strip().splitlines()[-n:])[:600]


def is_https(url) -> bool:
    u = urlsplit(str(url or ""))
    return u.scheme == "https" and bool(u.hostname) and not u.username and not u.password


def slugify(title: str, fallback: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")[:48].strip("-")
    if re.search(r"[a-z]", s):
        return s
    return "reel-" + hashlib.sha256((title or fallback).encode("utf-8")).hexdigest()[:8]


def split_credit(text: str):
    """'الصوت: @x' → {'label': 'الصوت:', 'latin': '@x'}: the scene draws them as two runs so bidi keeps the order."""
    text = (text or "").strip()
    if not text:
        return None
    m = re.match(r"^(.*?)\s*([@A-Za-z0-9][\x20-\x7e]*)$", text)
    if m:
        return {"text": text, "label": m.group(1).strip(), "latin": m.group(2).strip()}
    return {"text": text, "label": text, "latin": ""}


# ------------------------------------------------------------------ output folder
def default_out(slug: str) -> Path:
    """<repo>/out/reels/<slug> when this script runs from a checkout (whatever the current folder), else
    ./out/reels/<slug>. A relative out/ under the skill folder would ship reels with the skill."""
    base = REPO if (REPO / ".git").exists() else Path.cwd()
    return base / "out" / "reels" / slug


def inside_skill(out: Path) -> bool:
    try:
        Path(out).resolve().relative_to(SKILL)
    except ValueError:
        return False
    return True


def out_problem(out: Path):
    """Why OUT must not receive generated files, or None. The skill folder is always refused (git-ignored or not:
    package_skill.py and the repo's no-media test cover it); otherwise only paths inside a git work tree are restricted."""
    out = out.resolve()
    if inside_skill(out):
        return f"{out} is inside the skill folder {SKILL} (its files ship with the skill; reels go under <repo>/out/…)"
    try:
        in_repo = out.relative_to(REPO).parts
    except ValueError:
        in_repo = None
    if in_repo and in_repo[0] == "jobs":
        return f"{out} is inside jobs/ (job folders are tracked sources; outputs go under out/)"
    # Without a usable git, this checkout still only accepts out/… (fail closed); other folders are not restricted.
    unchecked = f"{out} is inside this repository and git cannot check it (use out/…)" if in_repo is not None and in_repo[:1] != ("out",) else None
    anc = out
    while not anc.exists() and anc != anc.parent:
        anc = anc.parent
    if not shutil.which("git"):
        return unchecked
    rc, top, _ = sh(["git", "-C", anc if anc.is_dir() else anc.parent, "rev-parse", "--show-toplevel"], 30)
    if rc:
        return unchecked  # not inside a git work tree (or git refuses it)
    top = Path(top.strip()).resolve()
    try:
        rel = out.relative_to(top)
    except ValueError:
        return None
    if not rel.parts:
        return f"{out} is the repository root"
    if rel.parts[0] == "jobs":
        return f"{out} is inside jobs/ (job folders are tracked sources; outputs go under out/)"
    rc, files, _ = sh(["git", "--literal-pathspecs", "-C", top, "ls-files", "--", rel.as_posix()], 60)
    tracked = [f for f in files.splitlines() if f.strip()]
    if tracked:
        return f"{out} is tracked by git ({len(tracked)} file(s), e.g. {tracked[0]})"
    rc, _, _ = sh(["git", "-C", top, "check-ignore", "-q", rel.as_posix()], 30)
    if rc == 1:
        return f"{out} is inside the repository but not git-ignored (use out/…)"
    return None


# ------------------------------------------------------------------ shots and rights
def _resolve_file(name, base: Path) -> Path:
    p = Path(str(name)).expanduser()
    if p.is_absolute():
        return p
    return base / p if (base / p).exists() or not p.exists() else p.resolve()


def load_shots(a) -> list:
    """Shots as [{file, start, rights, licence_url, credit, id?, source?, page?, duration?}] (exit 2 on bad input)."""
    shots = []
    if a.shots:
        doc = jread(Path(a.shots), "--shots")
        rows = doc.get("shots") if isinstance(doc, dict) else doc
        if not isinstance(rows, list) or not rows:
            raise Fail(2, "--shots must be a non-empty JSON list of {file, start, rights, licence_url, credit}")
        base = Path(a.shots).resolve().parent
        for i, r in enumerate(rows, 1):
            if not isinstance(r, dict) or not r.get("file"):
                raise Fail(2, f"--shots entry {i} has no file")
            try:
                start = float(r.get("start") or 0.0)
            except (TypeError, ValueError):
                raise Fail(2, f"--shots entry {i}: start must be seconds") from None
            shots.append({"file": str(_resolve_file(r["file"], base)), "start": max(0.0, start), "rights": r.get("rights"),
                          "licence_url": r.get("licence_url") or r.get("license_url"), "credit": r.get("credit"),
                          "id": r.get("id"), "source": r.get("source"), "page": r.get("page")})
    else:
        if not a.shot_ids:
            raise Fail(2, "--shots-manifest needs --shot-ids id[@in],id,…")
        man = Path(a.shots_manifest)
        doc = jread(man, "--shots-manifest")
        if not isinstance(doc, list):
            raise Fail(2, "--shots-manifest must be a stock_fetch.py manifest (a JSON list)")
        by_id = {str(e.get("id")): e for e in doc if isinstance(e, dict) and e.get("id") is not None and not e.get("error")}
        for tok in [t.strip() for t in a.shot_ids.split(",") if t.strip()]:
            sid, _, at = tok.partition("@")
            e = by_id.get(sid)
            if e is None:
                raise Fail(2, f"--shot-ids: id {sid} is not in {man} (known: {', '.join(sorted(by_id)) or 'none'})")
            if not e.get("file"):
                raise Fail(2, f"--shot-ids: manifest entry {sid} has no downloaded file ({e.get('skipped') or 'not fetched'})")
            dur = e.get("duration")
            try:
                start = float(at) if at else (min(1.0, float(dur) / 4) if dur else 1.0)
            except ValueError:
                raise Fail(2, f"--shot-ids: in-point of {tok} must be seconds") from None
            src = str(e.get("source") or "").lower()
            shots.append({"file": str((man.resolve().parent / e["file"])), "start": max(0.0, start),
                          "rights": e.get("rights") or STOCK_RIGHTS.get(src),
                          "licence_url": e.get("licence_url") or e.get("license_url"),
                          "credit": e.get("credit") or (f"{src.capitalize()} #{sid}" + (f" — {e['page']}" if e.get("page") else "")),
                          "id": sid, "source": src or None, "page": e.get("page"), "licence": e.get("licence"),
                          "duration": dur})
    if not shots:
        raise Fail(2, "no shots given")
    for i, s in enumerate(shots, 1):
        if not Path(s["file"]).is_file():
            raise Fail(2, f"shot {i}: file not found: {s['file']}")
    return shots


def rights_record(a, shots: list):
    """Gaps (each names exactly what was not declared) and the rights record written to OUT/rights.json. Advisory only."""
    problems = []
    rights, ev = a.audio_rights, a.audio_rights_evidence
    accepted = ", ".join(RIGHTS)
    audio_rec = {"file": str(Path(a.audio).resolve()), "rights": rights}
    if not rights:
        problems.append(f"audio: rights not declared (--audio-rights, one of {accepted})")
    elif rights not in RIGHTS:
        problems.append(f"audio: --audio-rights '{rights}' is not one of {accepted}")
    elif rights != "owned":
        if not ev:
            problems.append(f"audio: '{rights}' audio needs --audio-rights-evidence (an https URL or an existing local file)")
        elif is_https(ev):
            audio_rec["evidence"] = {"url": ev}
        elif Path(ev).is_file():
            audio_rec["evidence"] = {"file": str(Path(ev).resolve()), "sha256": sha256(Path(ev))}
        else:
            problems.append(f"audio: --audio-rights-evidence '{ev}' is neither an https URL nor an existing file")
        if rights in ("cc-by", "cc-by-sa") and not a.credit:
            problems.append(f"audio: '{rights}' audio needs --credit (attribution)")
    if Path(a.audio).is_file():
        audio_rec["sha256"] = sha256(Path(a.audio))
    shot_recs = []
    for i, s in enumerate(shots, 1):
        name = f"shot {i} ({s.get('id') or Path(s['file']).name})"
        r, url, credit = s.get("rights"), s.get("licence_url"), s.get("credit")
        if not r:
            problems.append(f"{name}: rights missing (one of {accepted})")
        elif r not in RIGHTS:
            problems.append(f"{name}: rights '{r}' is not one of {accepted}")
        if not url:
            problems.append(f"{name}: licence_url missing (an https URL is required)")
        elif not is_https(url):
            problems.append(f"{name}: licence_url must be an https URL (got '{url}')")
        if r in CREDIT_RIGHTS and not str(credit or "").strip():
            problems.append(f"{name}: '{r}' needs a credit")
        shot_recs.append({k: s.get(k) for k in ("file", "id", "source", "page", "rights", "licence", "licence_url", "credit")
                          if s.get(k) is not None})
    rec = {"schema": "kosif-reel-rights/2", "status": "incomplete" if problems else "complete", "gaps": problems,
           "audio": audio_rec, "shots": shot_recs, "credit_line": a.credit or None,
           "note": "Rights are declared by the operator and recorded for completeness; gaps never block the build, "
                   "and this tool does not grant a licence."}
    return problems, rec


# ------------------------------------------------------------------ words and phrases
def _phrase(text: str, members, words):
    idx = sorted(set(members))
    if not idx:
        return None
    ws = [dict(words[k]) for k in idx]
    return {"text": text or " ".join(w["w"] for w in ws), "start": ws[0]["s"], "end": ws[-1]["e"], "words": ws}


def parse_words(doc, warning=None):
    """kosif-words/1, {"words": [...]}, a bare word list, or whisper segments (a list or {"segments": [...]})
    → (words, phrases|None, source).
    words: [{"w", "s", "e"[, "p"]}] sorted, ends clamped to the next start, 3 decimals; p = whisper's own word
    probability when the file has one. A declared phrase needs a [first, last] word index range or numeric start/end."""
    declared, groups = None, None
    if isinstance(doc, dict):
        raw, declared = doc.get("words") if "words" in doc else doc.get("segments"), doc.get("phrases")
    else:
        raw = doc
    if not isinstance(raw, list):
        raise Fail(2, "words: no words list (expected kosif-words/1, {\"words\": [...]} or a list)")
    if raw and all(isinstance(x, dict) and isinstance(x.get("words"), list) for x in raw):  # whisper segments
        flat, groups = [], []
        for seg in raw:
            idx = []
            for w in seg["words"]:
                idx.append(len(flat))
                flat.append(w)
            groups.append((str(seg.get("text") or "").strip(), idx))
        raw = flat
    rows = []
    for i, w in enumerate(raw):
        if not isinstance(w, dict):
            continue
        text = str(w.get("word", w.get("w", w.get("text", ""))) or "").strip()
        try:
            s, e = float(w.get("start", w.get("s"))), float(w.get("end", w.get("e")))
        except (TypeError, ValueError):
            continue
        if text and math.isfinite(s) and math.isfinite(e):
            rows.append((max(0.0, s), e, text, i, w.get("prob", w.get("probability"))))
    rows.sort(key=lambda r: (r[0], r[3]))
    words, pos = [], {}
    for k, (s, e, text, i, prob) in enumerate(rows):
        e = max(e, s)
        if k + 1 < len(rows):
            e = min(e, max(rows[k + 1][0], s))
        pos[i] = len(words)
        words.append({"w": text, "s": round(s, 3), "e": round(e, 3)})
        if isinstance(prob, (int, float)) and not isinstance(prob, bool) and math.isfinite(prob):
            words[-1]["p"] = round(float(prob), 3)
    if not words:
        raise Fail(2, "words: no timed words found" + (f" — transcribe said: {warning}" if warning else ""))
    phrases, source = None, None
    if groups is not None:
        phrases, source = [_phrase(t, [pos[i] for i in idx if i in pos], words) for t, idx in groups], "whisper segments"
    elif isinstance(declared, list) and declared:
        phrases, source = [], "words.json phrases"
        for n, ph in enumerate(declared, 1):
            if not isinstance(ph, dict):
                continue
            rng = ph.get("words")
            if isinstance(rng, list) and len(rng) == 2 and all(isinstance(v, int) and not isinstance(v, bool) for v in rng):
                members = [pos[i] for i in range(rng[0], rng[1] + 1) if i in pos]
            else:
                try:
                    s0, e0 = float(ph.get("start")), float(ph.get("end"))
                except (TypeError, ValueError):
                    raise Fail(2, f"words: phrase {n} has neither a [first, last] word index range nor numeric "
                                  f"start/end ({json.dumps(ph, ensure_ascii=False)[:120]})") from None
                members = [k for k, w in enumerate(words) if s0 - 1e-6 <= w["s"] < e0]
            phrases.append(_phrase(str(ph.get("text") or "").strip(), members, words))
    if phrases is not None:
        phrases = sorted([p for p in phrases if p], key=lambda p: p["start"]) or None
    return words, phrases, source


def group_by_pause(words, pause: float = PAUSE, max_words: int = MAX_WORDS):
    """New phrase at a silence ≥ pause seconds or after max_words words."""
    groups, cur = [], []
    for w in words:
        if cur and (w["s"] - cur[-1]["e"] >= pause - 1e-9 or len(cur) >= max_words):
            groups.append(cur)
            cur = []
        cur.append(w)
    if cur:
        groups.append(cur)
    return [{"text": " ".join(w["w"] for w in g), "start": g[0]["s"], "end": g[-1]["e"], "words": [dict(w) for w in g]}
            for g in groups]


def check_words(doc, words, audio_sha: str, audio_dur: float, slack: float = WORDS_SLACK):
    """Do these word timings belong to --audio? → (problems, record for plan.json). Checks the kosif-words/1
    source.sha256 when declared and that the last word ends inside the audio (+ slack), and counts what a file can
    show by itself. It does not measure timing accuracy: there is no reference alignment to compare with."""
    src = doc.get("source") if isinstance(doc, dict) and isinstance(doc.get("source"), dict) else {}
    declared = str(src.get("sha256") or "").strip().lower() or None
    first, last = words[0]["s"], max(w["e"] for w in words)
    probs = [w["p"] for w in words if "p" in w]
    rec = {"source_sha256": declared, "sha256_match": None if declared is None else declared == audio_sha,
           "audio_duration": audio_dur, "first_word_start": first, "last_word_end": last,
           "fits_audio": last <= audio_dur + slack, "words_starting_after_audio": sum(1 for w in words if w["s"] >= audio_dur),
           "zero_length_words": sum(1 for w in words if w["e"] <= w["s"]),
           "speech_span_ratio": round((last - first) / audio_dur, 3) if audio_dur > 0 else None,
           "mean_word_prob": round(sum(probs) / len(probs), 3) if probs else None,
           "words_prob_below_0_5": sum(1 for p in probs if p < 0.5) if probs else None,
           "timing_accuracy": "not measured (no reference alignment); these checks only tie the words to this audio"}
    problems = []
    if declared is not None and declared != audio_sha:
        problems.append(f"words.json source.sha256 {declared[:12]}… ({src.get('file') or 'no file name'}) is not the sha256 "
                        f"of --audio ({audio_sha[:12]}…): these timings were made from another file")
    if not rec["fits_audio"]:
        problems.append(f"the last word ends at {last} s but --audio lasts {audio_dur} s "
                        f"({rec['words_starting_after_audio']} word(s) start after it)")
    rec.update({"status": "mismatch" if problems else "ok", "problems": problems})
    return problems, rec


def display_words(ph, override=None):
    """[[token, start, end]] for the scene. Same token count as the timed words → exact times; an override text with a
    different count is spread over the phrase by character position and marked 'estimated'."""
    text = override if override is not None else ph["text"]
    toks, ws = text.split(), ph["words"]
    if len(toks) == len(ws):
        return [[t, w["s"], w["e"]] for t, w in zip(toks, ws)], "words"
    if override is None or not toks:
        return [[w["w"], w["s"], w["e"]] for w in ws], "words"
    span, total = ph["end"] - ph["start"], sum(len(t) for t in toks) + len(toks) - 1
    out, at = [], 0
    for t in toks:
        out.append([t, round(ph["start"] + span * at / total, 3), round(ph["start"] + span * (at + len(t)) / total, 3)])
        at += len(t) + 1
    return out, "estimated"


def load_phrase_texts(path) -> list:
    doc = jread(Path(path), "--phrases")
    rows = doc.get("phrases") if isinstance(doc, dict) else doc
    if not isinstance(rows, list) or not all(isinstance(t, str) and t.strip() for t in rows):
        raise Fail(2, "--phrases must be a JSON list of non-empty strings (one per phrase)")
    return [t.strip() for t in rows]


# ------------------------------------------------------------------ style
def resolve_style(spec) -> dict:
    """A named preset (optionally name:transitions:frame) or an integer seed → a deterministic parametric look."""
    spec = str(spec if spec is not None else "gold-night").strip() or "gold-night"
    seed, rot = None, 0
    if re.fullmatch(r"-?\d+", spec):
        seed = int(spec)
        for salt in range(64):  # a seed never lands on a preset's exact look: re-hash until the tuple differs
            h = hashlib.sha256(f"kosif-reel-style/{seed}/{salt}".encode()).digest()
            pal = sorted(PALETTES)[h[0] % len(PALETTES)]
            tr = sorted(TRANSITION_SETS)[h[1] % len(TRANSITION_SETS)]
            fr = FRAMES[h[2] % len(FRAMES)]
            rot = h[3] % len(TRANSITION_SETS[tr])
            if (pal, tr, fr) not in PRESETS.values() or rot:
                break
    else:
        parts = spec.split(":")
        if parts[0] not in PRESETS:
            raise Fail(2, f"--style '{spec}': unknown (presets: {', '.join(PRESETS)}; or an integer seed)")
        pal, tr, fr = PRESETS[parts[0]]
        if len(parts) > 1 and parts[1]:
            if parts[1] not in TRANSITION_SETS:
                raise Fail(2, f"--style: transitions '{parts[1]}' unknown ({', '.join(TRANSITION_SETS)})")
            tr = parts[1]
        if len(parts) > 2 and parts[2]:
            if parts[2] not in FRAMES:
                raise Fail(2, f"--style: frame '{parts[2]}' unknown ({', '.join(FRAMES)})")
            fr = parts[2]
    cyc = TRANSITION_SETS[tr]
    return {"input": spec, "seed": seed, "palette": pal, "colors": dict(PALETTES[pal]), "transitions": tr,
            "transition_cycle": cyc[rot:] + cyc[:rot], "frame": fr, "xfade": XFADE}


# ------------------------------------------------------------------ audio and plan math
def audio_info(path: Path) -> dict:
    """Duration (ffprobe; stdlib wave for .wav when ffprobe is absent) and codec of the first audio stream."""
    if shutil.which("ffprobe"):
        rc, out, err = sh(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                           "stream=codec_name:format=duration", "-of", "json", path], 120)
        try:
            d = json.loads(out)
            dur = float(d["format"]["duration"])
            codec = (d.get("streams") or [{}])[0].get("codec_name")
        except (ValueError, KeyError, TypeError):
            raise Fail(2, f"--audio: ffprobe cannot read {path}: {tail(err, 1)}") from None
        if not codec:
            raise Fail(2, f"--audio: no audio stream in {path}")
        return {"duration": round(dur, 3), "codec": codec, "probe": "ffprobe"}
    if path.suffix.lower() == ".wav":
        try:
            with wave.open(str(path), "rb") as wf:
                return {"duration": round(wf.getnframes() / float(wf.getframerate()), 3), "codec": "pcm", "probe": "wave"}
        except (wave.Error, EOFError, OSError) as exc:
            raise Fail(2, f"--audio: cannot read {path}: {exc}") from None
    raise Fail(2, "ffprobe not found (needed to measure the audio); install ffmpeg")


def shot_duration(path: str):
    if not shutil.which("ffprobe"):
        return None
    rc, out, _ = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path], 60)
    try:
        d = float(out.strip())
    except ValueError:
        return None
    return d if rc == 0 and math.isfinite(d) and d > 0 else None


def plan_cuts(phrase_starts, duration: float, shots: list, cycle: list, xfade: float = XFADE, min_shot: float = MIN_SHOT):
    """One shot per phrase, cut at each phrase start; a phrase closer than min_shot to the previous cut or to the end
    keeps the current shot and is listed in that cut's "merged". Each xfade is centred on its cut, so shot k lasts
    (next cut + x/2) − (cut − x/2); the first starts at 0 and the last covers the tail. Sum of lengths − overlaps =
    duration exactly."""
    bounds, owners, merged = [0.0], [0], [[]]
    for i, s in enumerate(phrase_starts[1:], 1):
        if s - bounds[-1] >= min_shot - 1e-9 and duration - s >= min_shot - 1e-9:
            bounds.append(round(s, 3))
            owners.append(i)
            merged.append([])
        else:
            merged[-1].append(i)
    n, half, used, cuts = len(bounds), xfade / 2, {}, []
    for k in range(n):
        a = bounds[k] - (half if k else 0.0)
        b = bounds[k + 1] + half if k + 1 < n else duration
        dur = round(b - a, 3)
        si = k % len(shots)
        shot = shots[si]
        start = shot["start"] + used.get(si, 0.0)  # a cycled shot continues where it left off
        sd = shot.get("duration")
        if sd and start + dur > sd:
            start = max(0.0, sd - dur) if sd >= dur else 0.0  # plate input also loops (-stream_loop) if still short
        used[si] = used.get(si, 0.0) + dur
        cuts.append({"index": k, "shot": si, "file": shot["file"], "in": round(start, 3), "dur": dur, "at": bounds[k],
                     "phrase": owners[k], "merged": merged[k], "transition": None if k == 0 else cycle[(k - 1) % len(cycle)],
                     "offset": None if k == 0 else round(bounds[k] - half, 3)})
    return cuts


def plate_length(cuts, xfade: float = XFADE) -> float:
    return round(sum(c["dur"] for c in cuts) - xfade * (len(cuts) - 1), 3)


def make_plan(a, shots, style, words_info, words, phrases, phrase_source, audio) -> dict:
    duration = round(audio["duration"] + TAIL, 3)
    texts = load_phrase_texts(a.phrases) if a.phrases else None
    if texts is not None and len(texts) != len(phrases):
        raise Fail(2, f"--phrases has {len(texts)} texts but the words give {len(phrases)} phrases ({phrase_source})")
    out_ph = []
    for i, ph in enumerate(phrases):
        disp, timing = display_words(ph, texts[i] if texts else None)
        out_ph.append({"text": texts[i] if texts else ph["text"], "start": ph["start"], "end": ph["end"], "words": disp,
                       "word_timing": timing, "big": i == len(phrases) - 1 and len(phrases) > 1 and len(disp) <= 3})
    for s in shots:
        if s.get("duration") is None:
            s["duration"] = shot_duration(s["file"])
        if s.get("duration") and s["start"] >= s["duration"]:
            raise Fail(2, f"shot {s.get('id') or Path(s['file']).name}: in-point {s['start']} s is past its end ({s['duration']} s)")
    min_shot = getattr(a, "min_shot", MIN_SHOT)
    cuts = plan_cuts([p["start"] for p in out_ph], duration, shots, style["transition_cycle"], XFADE, min_shot)
    merged = []
    for c in cuts:
        for i in c["merged"]:
            s = out_ph[i]["start"]
            why = (f"starts {round(duration - s, 3)} s before the end (< {min_shot} s)" if duration - s < min_shot - 1e-9
                   else f"starts {round(s - c['at'], 3)} s after the cut at {c['at']} s (< {min_shot} s)")
            merged.append({"phrase": i, "start": s, "text": out_ph[i]["text"], "shown_on_cut": c["index"], "reason": why})
    return {
        "schema": "kosif-reel-plan/1", "title": a.title, "handle": a.handle, "credit": split_credit(a.credit),
        "audio": {"path": str(Path(a.audio).resolve()), "file": Path(a.audio).name,
                  "sha256": audio.get("sha256") or sha256(Path(a.audio)),
                  "duration": audio["duration"], "codec": audio["codec"], "probe": audio["probe"]},
        "words": words_info, "word_count": len(words), "phrase_source": phrase_source, "phrases": out_ph,
        "shots": [{k: s.get(k) for k in ("file", "id", "start", "duration", "rights", "licence_url", "credit")} for s in shots],
        "cut_rule": {"rule": "one shot per phrase, cut at each phrase start", "min_shot": min_shot,
                     "phrases": len(out_ph), "cuts": len(cuts), "merged": merged},
        "cuts": cuts,
        "transitions": [{"at": c["at"], "offset": c["offset"], "duration": XFADE, "name": c["transition"]} for c in cuts[1:]],
        "xfade": XFADE, "fps": FPS, "size": [W, H], "duration": duration, "frames": int(round(duration * FPS)),
        "plate": {"size": [960, 1200], "length": plate_length(cuts), "frames": int(round(duration * FPS))},
        "style": style, "safe_zone": dict(SAFE), "layout": dict(LAYOUT),
    }


def scene_data(plan: dict, plate_frames: int) -> dict:
    ph = plan["phrases"]
    return {"W": W, "H": H, "fps": FPS, "duration": plan["duration"], "title": plan["title"] or "",
            "handle": plan["handle"] or "", "credit": plan["credit"], "palette": plan["style"]["colors"],
            "frame": plan["style"]["frame"], "layout": plan["layout"], "safe": plan["safe_zone"], "xfade": plan["xfade"],
            "cuts": [c["at"] for c in plan["cuts"][1:]],
            "phrases": [{"s": p["start"], "e": ph[i + 1]["start"] if i + 1 < len(ph) else plan["duration"], "big": p["big"],
                         "words": p["words"]} for i, p in enumerate(ph)],
            "plate": {"dir": "plate", "frames": plate_frames, "digits": 4}}


def inline_scene(template: str, data: dict) -> str:
    if template.count(DATA_TOKEN) != 1:
        raise Fail(4, f"BUILD_FAILED at scene: {TEMPLATE} must contain {DATA_TOKEN} exactly once")
    # Every "<" becomes \u003c (JSON reads it back unchanged), so no title, word, handle or credit can end the script
    # element or open a comment that swallows it ("</script>", "<!--<script>"); U+2028/2029 stay valid JS too.
    js = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return template.replace(DATA_TOKEN, "/*KOSIF_SCENE_DATA*/" + js)


def plate_cmd(cuts, frames: int, pattern: Path, xfade: float = XFADE) -> list:
    """ffmpeg argv for the plate: exactly `frames` JPGs. Each input reads 2 frames more than its share (the extra
    frames of a shot that fades out are dropped by xfade) and the chain ends with its last frame cloned, because
    rounding inside an xfade chain was measured to leave it one frame short of duration × fps."""
    cmd, slack = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y"], 2.0 / FPS
    for c in cuts:
        cmd += ["-stream_loop", "-1", "-ss", f"{c['in']:.3f}", "-t", f"{c['dur'] + slack:.3f}", "-i", c["file"]]
    parts = [f"[{i}:v]{PLATE_FILTER}[v{i}]" for i in range(len(cuts))]
    last = "v0"
    for k, c in enumerate(cuts[1:], 1):
        parts.append(f"[{last}][v{k}]xfade=transition={c['transition']}:duration={xfade:g}:offset={c['offset']:.3f}[x{k}]")
        last = f"x{k}"
    parts.append(f"[{last}]tpad=stop_mode=clone:stop_duration=0.5[plate]")
    return cmd + ["-filter_complex", ";".join(parts), "-map", "[plate]", "-an", "-frames:v", str(frames),
                  "-q:v", "3", str(pattern)]


# ------------------------------------------------------------------ build
def render_script() -> Path:
    env = os.environ.get("KOSIF_RENDER_HTML")
    return Path(env) if env else REPO / "tools" / "render_html.cjs"


def chromium_problem():
    """None when Playwright's Chromium can be found the way tools/render_html.cjs looks for it, else why not."""
    rc, _, err = sh(["node", "-e", CHROMIUM_JS], 60)
    if rc == 0:
        return None
    if rc == 3:
        return "Playwright is installed but its Chromium is not downloaded (run: npx playwright install chromium)"
    return ("Playwright's Chromium not found (tools/render_html.cjs looks in the current folder, /opt/node-tools and "
            "$KOSIF_PLAYWRIGHT; install: npm i playwright && npx playwright install chromium)"
            + (f" [node exit {rc}: {tail(err, 1)}]" if rc not in (4,) else ""))


def build_problem():
    """Why build cannot run on this machine, or None. Checked before the rights record, transcription or any render."""
    for tool in ("ffmpeg", "ffprobe", "node"):
        if not shutil.which(tool):
            return f"{tool} not found on PATH (build needs ffmpeg, ffprobe and node with Playwright's Chromium)"
    renderer = render_script()
    if not renderer.is_file():
        return f"renderer not found: {renderer} (set KOSIF_RENDER_HTML)"
    if os.environ.get("KOSIF_RENDER_HTML"):
        return None  # a custom renderer brings its own browser
    return chromium_problem()


def build(a, out: Path, plan: dict, rights: dict) -> dict:
    renderer = render_script()
    audio = Path(plan["audio"]["path"])
    bdir, steps = out / "build", []
    plate_dir = bdir / "plate"
    refuse_symlinks(out)  # again right before the build's own writes (plate, fonts, scene, render, mux, verify)
    plate_dir.mkdir(parents=True, exist_ok=True)
    for old in plate_dir.glob("*.jpg"):
        if not old.is_symlink():
            old.unlink()

    def run(step, cmd, timeout=1800, fatal=True):
        t0 = time.time()
        rc, so, se = sh(cmd, timeout)
        steps.append({"step": step, "cmd": [str(c) for c in cmd], "rc": rc, "seconds": round(time.time() - t0, 2),
                      **({"stderr_tail": tail(se)} if rc else {})})
        if rc and fatal:
            raise Fail(4, f"BUILD_FAILED at {step} (exit {rc}): {tail(se or so)}")
        return rc, so, se

    result = {"steps": steps}
    try:
        run("plate", plate_cmd(plan["cuts"], plan["frames"], plate_dir / "%04d.jpg"))
        n_plate = len(list(plate_dir.glob("*.jpg")))
        result.update({"plate_frames": n_plate, "plate_frames_target": plan["frames"]})
        if n_plate != plan["frames"]:
            raise Fail(4, f"BUILD_FAILED at plate: {n_plate} frames written, {plan['frames']} expected")
        fonts = bdir / "fonts"
        fonts.mkdir(exist_ok=True)
        for src, dst in FONTS.items():
            shutil.copyfile(FONT_DIR / src, fonts / dst)
        data = scene_data(plan, n_plate)
        jsave(bdir / "scene_data.json", data)
        scene = bdir / "scene.html"
        tsave(scene, inline_scene(TEMPLATE.read_text(encoding="utf-8"), data))
        noaudio, reel = bdir / "video_noaudio.mp4", out / "reel.mp4"
        cmd = ["node", renderer, "--in", scene, "--out", noaudio, "--aspect", "9:16", "--fps", FPS,
               "--duration", plan["duration"], "--offline"]
        if a.draft:
            cmd += ["--width", 540, "--height", 960]
        run("render", cmd, timeout=3600)
        run("mux", ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-i", noaudio, "-i", audio,
                    "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", "-movflags", "+faststart", reel])
        vjson = bdir / "verify.json"
        rc, so, se = run("verify", [PY, VERIFY, reel, "--aspect", "9:16", "--fps", FPS, "--duration", plan["duration"],
                                    "--source-audio", audio, "--json", vjson], timeout=1800, fatal=False)
        try:
            verify = json.loads(vjson.read_text(encoding="utf-8")) if vjson.is_file() and rc in (0, 1) else None
        except ValueError:
            verify = None
        result.update({"scene": str(scene), "video": str(reel),
                       "verify": {"exit": rc, "stdout": so.strip().splitlines(), "stderr": tail(se), "report": verify}})
        rc_cs, _, _ = run("contact_sheet", ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-i", reel,
                                            "-vf", f"fps={8 / plan['duration']:.4f},scale=270:-1,tile=4x2", "-frames:v", "1",
                                            bdir / "contact_sheet.png"], fatal=False)
        if rc_cs == 0:
            result["contact_sheet"] = str(bdir / "contact_sheet.png")
        result["audio_untouched"] = sha256(audio) == plan["audio"]["sha256"]
        result["video_sha256"] = sha256(reel)
    except OSError as exc:  # a missing font, a full disk: report it like any other failed step
        raise Fail(4, f"BUILD_FAILED: {type(exc).__name__}: {exc}") from None
    finally:
        write_reports(a, out, plan, rights, result)
    if result["verify"]["exit"] != 0:
        raise Fail(4, f"VERIFY_FAILED: verify_video.py exit {result['verify']['exit']}: "
                      + "; ".join(line for line in result["verify"]["stdout"] if line.startswith("[FAIL]"))
                      + (f" {result['verify']['stderr']}" if result["verify"]["stderr"] else ""))
    return result


def write_reports(a, out: Path, plan: dict, rights: dict, result: dict):
    verify = (result.get("verify") or {}).get("report") or {}
    inputs = {"audio": {"path": plan["audio"]["path"], "sha256": plan["audio"]["sha256"]},
              "words": plan["words"], "template": {"path": str(TEMPLATE), "sha256": sha256(TEMPLATE)},
              "shots": [{"file": s["file"], "sha256": sha256(Path(s["file"]))} for s in plan["shots"]]}
    ok = (result.get("verify") or {}).get("exit") == 0
    jsave(out / "build.json", {"schema": "kosif-reel-build/1", "status": "verified" if ok else "failed", "inputs": inputs,
                               "commands": result.get("steps", []), "results": {k: v for k, v in result.items() if k != "steps"},
                               "rights": {"status": rights["status"], "gaps": rights.get("gaps", []),
                                          "audio": rights["audio"].get("rights"),
                                          "shots": [s.get("rights") for s in rights["shots"]]},
                               "style": plan["style"]["input"], "duration": plan["duration"]})
    checks = verify.get("checks") or []
    lines = [f"# TEST_REPORT — {plan['title'] or 'reel'}", "",
             f"> reel_factory.py build · 9:16 · {W}x{H} · {FPS} fps · {plan['duration']} s · {plan['frames']} frames"
             + (" · DRAFT 540x960" if a.draft else ""), "",
             "Values below are measured by verify_video.py on the delivered file; rows marked *not measured* need a human look.", "",
             "## 1. Delivered file", "", "| Item | Value |", "|---|---|",
             f"| Path | `{result.get('video', '—')}` |",
             f"| SHA-256 | `{result.get('video_sha256', '—')}` |",
             f"| Editable source | `{result.get('scene', '—')}` (+ scene_data.json, plate/) |",
             f"| Contact sheet | `{result.get('contact_sheet', '—')}` |", "",
             "## 2. Checks (verify_video.py --source-audio)", "", "| Check | Measured | Result |", "|---|---|---|"]
    for c in checks:
        lines.append(f"| {c['check']} | {c['value']} | {c.get('status') or ('PASS' if c['pass'] else 'FAIL')} |")
    if not checks:
        lines.append(f"| verify_video.py | exit {(result.get('verify') or {}).get('exit', 'not run')} | FAIL |")
    plate_ok = result.get("plate_frames") is not None and result.get("plate_frames") == result.get("plate_frames_target")
    lines += [f"| Source audio file unchanged (SHA-256 before = after) | {result.get('audio_untouched')} | "
              f"{'PASS' if result.get('audio_untouched') else 'FAIL'} |",
              f"| Plate frames written = duration × fps | {result.get('plate_frames', '—')} / {result.get('plate_frames_target', plan['frames'])} | "
              f"{'PASS' if plate_ok else 'FAIL'} |",
              f"| Text inside the safe band y {SAFE['top']}–{SAFE['bottom']} | by layout: title {LAYOUT['title_y']}, captions "
              f"≈{LAYOUT['text_cy']}, handle {LAYOUT['handle_y']}, credit {LAYOUT['credit_y']} | by design, not measured from pixels |",
              "| Arabic shaping / legibility / contrast | see the contact sheet | *not measured* |", ""]
    w, chk = plan["words"], plan["words"].get("check") or {}
    eng, tr = w.get("engine") or {}, w.get("transcribe") or {}
    lines += ["## 3. Words and timing", "",
              f"- words: {w.get('source')} `{w.get('path')}` · {plan['word_count']} words · {len(plan['phrases'])} phrases "
              f"({plan['phrase_source']}) · {plan['cut_rule']['cuts']} cuts, {len(plan['cut_rule']['merged'])} phrase(s) kept on "
              f"the previous shot (min shot {plan['cut_rule']['min_shot']} s)"]
    if eng:
        lines.append(f"- engine: {eng.get('name')} {eng.get('version') or ''} · model {eng.get('model')} · language {eng.get('language')}")
    if tr:
        lines.append(f"- transcription: {tr.get('status')} · {tr.get('elapsed_s')} s measured by montage_pro.py · "
                     f"{tr.get('wall_s')} s wall time for the whole call (process start and model load included)"
                     + (f" · warning: {tr['warning']}" if tr.get("warning") else ""))
    lines += [f"- belongs to the audio: {chk.get('status')} — source sha256 "
              f"{'matches' if chk.get('sha256_match') else ('differs' if chk.get('sha256_match') is False else 'not declared')}, "
              f"last word ends {chk.get('last_word_end')} s of {chk.get('audio_duration')} s"
              + (" (overridden with --allow-words-mismatch)" if chk.get("overridden") else ""),
              "- word-timing accuracy: **not measured** (no reference alignment); captions follow these timings as they are", "",
              "## 4. Rights (recorded, not enforced)", "", f"- status: **{rights['status']}**",
              f"- audio: {rights['audio'].get('rights') or 'not declared'} — evidence: "
              f"{json.dumps(rights['audio'].get('evidence'), ensure_ascii=False) if rights['audio'].get('evidence') else ('owned' if rights['audio'].get('rights') == 'owned' else 'none')}"]
    lines += [f"- gap: {g}" for g in rights.get("gaps", [])]
    lines += [f"- shot {i}: {s.get('rights')} — {s.get('licence_url')} — {s.get('credit') or 'no credit'}"
              for i, s in enumerate(rights["shots"], 1)]
    lines += ["", "## 5. Commands", ""]
    lines += [f"- `{st['step']}` exit {st['rc']} in {st['seconds']} s" for st in result.get("steps", [])]
    lines += ["", "Full argv for every command: build.json → commands.", ""]
    tsave(out / "TEST_REPORT.md", "\n".join(lines))


# ------------------------------------------------------------------ CLI
def run(a) -> dict:
    audio = Path(a.audio)
    if not audio.is_file():
        raise Fail(2, f"--audio: file not found: {audio}")
    style = resolve_style(a.style)
    if a.phrases and not Path(a.phrases).is_file():
        raise Fail(2, f"--phrases: file not found: {a.phrases}")
    if a.words and not Path(a.words).is_file():
        raise Fail(2, f"--words: file not found: {a.words}")
    if a.retranscribe and not a.transcribe:
        raise Fail(2, "--retranscribe only applies with --transcribe")
    if not (math.isfinite(a.min_shot) and a.min_shot >= MIN_SHOT - 1e-9):
        raise Fail(2, f"--min-shot must be at least {MIN_SHOT} s (the {XFADE} s xfade + 0.1 s), got {a.min_shot}")
    if a.cmd == "build":  # missing tools are found before the gate, the transcription or any render
        why = build_problem()
        if why:
            raise Fail(2, why)
    slug = slugify(a.title, audio.name)
    out = Path(a.out) if a.out else default_out(slug)
    if inside_skill(out):
        raise Fail(2, f"--out refused: {out_problem(out)}; use {default_out(slug)} or a folder outside the skill")
    if out.exists() and not out.is_dir():
        raise Fail(2, f"--out {out} exists and is not a folder")
    if not a.allow_tracked:
        why = out_problem(out)
        if why:
            raise Fail(2, f"--out refused: {why}; pass --allow-tracked to override")
    refuse_symlinks(Path(a.out) if a.out else out)
    out = out.resolve()
    global OUT_ROOT
    OUT_ROOT = out
    info = audio_info(audio)
    if info["codec"] not in DELIVERY_CODECS:
        raise Fail(2, f"--audio codec {info['codec']} cannot be delivered untouched: the reel carries the audio with -c copy "
                      f"(never re-encoded) and verify_video.py accepts only AAC or MP3 in a delivery MP4. Supply AAC (.m4a) or "
                      f"MP3, e.g. one encode you choose: ffmpeg -i {audio.name} -c:a aac -b:a 192k voice.m4a")
    info["sha256"] = sha256(audio)
    shots = load_shots(a)
    problems, rights = rights_record(a, shots)
    jsave(out / "rights.json", rights)
    if problems:  # advisory: recorded and said once, never a stop
        print("RIGHTS_NOTE: " + "; ".join(problems) + f" (recorded in {out / 'rights.json'}; the build goes on)", file=sys.stderr)
    # ---- heavy work starts here (after the rights record)
    if a.transcribe:
        wpath = out / "words.json"
        cmd = [PY, MONTAGE, "transcribe", audio, "--out", wpath, "--model", a.model, "--language", a.language]
        cmd += [flag for flag, on in (("--local-only", a.local_only), ("--force", a.retranscribe),
                                      ("--allow-tracked", a.allow_tracked)) if on]
        t0 = time.time()
        rc, so, se = sh(cmd, 7200)
        wall = round(time.time() - t0, 3)
        if rc:
            msg = tail(se or so, 2).replace("pass --force", "pass --retranscribe")
            raise Fail(2, f"--transcribe failed (montage_pro.py exit {rc}): {msg}")
        rep = last_json(so)
        tr = {"status": rep.get("status"), "elapsed_s": rep.get("elapsed_s"), "wall_s": wall,
              "command": [str(c) for c in cmd]}
        tr.update({k: rep[k] for k in ("warning", "dropped_segments", "vad_filter") if rep.get(k) is not None})
        winfo = {"source": "transcribe", "path": str(wpath), "sha256": sha256(wpath), "model": a.model,
                 "language": a.language, "transcribe": tr}
    else:
        wpath = Path(a.words).resolve()
        winfo = {"source": "file", "path": str(wpath), "sha256": sha256(wpath)}
    doc = jread(wpath, "words")
    words, phrases, source = parse_words(doc, (winfo.get("transcribe") or {}).get("warning"))
    winfo["schema"] = doc.get("schema") if isinstance(doc, dict) else "list"
    if isinstance(doc, dict) and isinstance(doc.get("engine"), dict):
        winfo["engine"] = doc["engine"]
    bad, winfo["check"] = check_words(doc, words, info["sha256"], info["duration"])
    if bad and not a.allow_words_mismatch:
        raise Fail(2, "words do not match --audio: " + "; ".join(bad) + ". Use the timings of this recording (or "
                      "--transcribe), or pass --allow-words-mismatch if it really is the same recording")
    if bad:
        winfo["check"]["overridden"] = True
        print("warning: --allow-words-mismatch: " + "; ".join(bad), file=sys.stderr)
    if not phrases:
        phrases, source = group_by_pause(words), f"pauses ≥ {PAUSE} s (≤ {MAX_WORDS} words)"
    plan = make_plan(a, shots, style, winfo, words, phrases, source, info)
    jsave(out / "plan.json", plan)
    res = {"status": "planned", "out": str(out), "plan": str(out / "plan.json"), "rights": str(out / "rights.json"),
           "rights_status": rights["status"],
           "duration": plan["duration"], "phrases": len(plan["phrases"]), "cuts": len(plan["cuts"]),
           "merged_phrases": len(plan["cut_rule"]["merged"]), "words_check": winfo["check"]["status"],
           "plate_length": plan["plate"]["length"], "style": f"{style['palette']}/{style['transitions']}/{style['frame']}"}
    if a.cmd == "build":
        b = build(a, out, plan, rights)
        res.update({"status": "verified", "video": b["video"], "report": str(out / "TEST_REPORT.md"),
                    "build": str(out / "build.json"), "verify": b["verify"]["stdout"][-1] if b["verify"]["stdout"] else ""})
    return res


def parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--audio", required=True, help="the voice/audio file (kept untouched; muxed with -c copy)")
    common.add_argument("--audio-rights", help="recorded in OUT/rights.json (advisory); one of: " + ", ".join(RIGHTS))
    common.add_argument("--audio-rights-evidence", help="https URL or local file proving the audio rights (recorded; not needed for owned)")
    w = common.add_mutually_exclusive_group(required=True)
    w.add_argument("--words", help="words.json (kosif-words/1, {\"words\": [...]}, a bare list or whisper segments)")
    w.add_argument("--transcribe", action="store_true", help="run montage_pro.py transcribe → OUT/words.json")
    common.add_argument("--allow-words-mismatch", action="store_true",
                        help="--words: accept timings whose source.sha256 is not --audio's or that run past its end")
    common.add_argument("--model", default="medium", help="--transcribe: faster-whisper model (default medium)")
    common.add_argument("--language", default="ar", help="--transcribe: language (default ar)")
    common.add_argument("--local-only", action="store_true", help="--transcribe: never download the model")
    common.add_argument("--retranscribe", action="store_true",
                        help="--transcribe: replace OUT/words.json even when it is up to date or was not written by transcribe")
    s = common.add_mutually_exclusive_group(required=True)
    s.add_argument("--shots", help="shots.json: [{file, start, rights, licence_url, credit}]")
    s.add_argument("--shots-manifest", help="stock_fetch.py manifest.json (licence taken from it)")
    common.add_argument("--shot-ids", help="with --shots-manifest: id[@in-seconds],id,… in cut order")
    common.add_argument("--title", default="", help="title drawn above the panel")
    common.add_argument("--handle", default="@kosif", help="signature handle (default @kosif; empty to hide)")
    common.add_argument("--credit", default="", help="credit line, e.g. 'الصوت: @x' (drawn as two runs)")
    common.add_argument("--phrases", help="JSON list of phrase texts (e.g. with tashkeel), one per phrase; timing stays from words")
    common.add_argument("--style", default="gold-night", help="preset (" + ", ".join(PRESETS) + ")[:transitions[:frame]] or an integer seed")
    common.add_argument("--min-shot", type=float, default=MIN_SHOT,
                        help=f"seconds; a phrase starting sooner after the previous cut (or before the end) keeps the "
                             f"current shot (default and minimum {MIN_SHOT})")
    common.add_argument("--out", help="output folder (default <repo>/out/reels/<slug>)")
    common.add_argument("--allow-tracked", action="store_true",
                        help="allow an --out that is tracked, not ignored, or under jobs/ (also passed to --transcribe)")
    sub.add_parser("plan", parents=[common], help="rights record + plan.json (no rendering)")
    b = sub.add_parser("build", parents=[common], help="plan, plate, scene, render, mux, verify")
    b.add_argument("--draft", action="store_true", help="render 540x960 (9:16) for a quick check")
    return ap


def main(argv=None) -> int:
    a = parser().parse_args(argv)
    if a.cmd == "plan":
        a.draft = False
    try:
        res = run(a)
    except Fail as exc:
        print(str(exc), file=sys.stderr)
        return exc.code
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
