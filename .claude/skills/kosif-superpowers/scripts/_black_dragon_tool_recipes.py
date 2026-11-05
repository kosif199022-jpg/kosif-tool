#!/usr/bin/env python3
"""Known-answer recipes for tools that have no test file of their own (used by _black_dragon_tool.py).

Each recipe builds a small fixture inside the adapter's .work folder, runs the REAL tool on it, and
checks the answer it must give. A checker tool also gets a planted flaw and must catch it; a checker
that misses the flaw earns no receipt. Nothing here writes outside the .work folder: tools that
normally rewrite repository files run in their read-only --check mode, or with --out pointing into
the work folder.
"""
from __future__ import annotations
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

SCRIPTS = Path(__file__).resolve().parent
SKILL = SCRIPTS.parent
REPO = SKILL.parents[2]
PY = [sys.executable, "-B"]


@dataclass
class Ctx:
    tool: dict
    script: Path
    work: Path
    env: dict
    timeout: int
    task: str
    steps: list
    check: Callable


def run(c: Ctx, step: str, argv: list, cwd: Path = REPO) -> subprocess.CompletedProcess:
    done = subprocess.run([str(a) for a in argv], cwd=cwd, env=c.env, text=True, capture_output=True,
                          stdin=subprocess.DEVNULL, timeout=c.timeout, check=False)
    c.steps.append({"step": step, "command": [str(a) for a in argv], "exit_code": done.returncode,
                    "stdout_sha256": hashlib.sha256(done.stdout.encode()).hexdigest(),
                    "stdout_tail": done.stdout[-600:], "stderr_tail": done.stderr[-400:]})
    return done


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --------------------------------------------------------------------------- atlas-transfer
def atlas_transfer(c: Ctx) -> None:
    """Five verifier rows with a known fate each: kept, merged duplicate, missing fields, dropped, unknown domain."""
    good = {"verdict": "keep", "domain": "media", "name_en": "Probe then transcode", "name_ar": "افحص ثم حوّل",
            "how": "ffprobe the input, then encode", "what_en": "safe transcode", "what_ar": "تحويل آمن",
            "atlas_ids": ["1"], "examples": [{"id": "1", "plugin": "p", "skill": "s", "path": "skills/s"}]}
    rows = [good,
            dict(good, name_en="Probe, then transcode!", how="ffprobe the input first, then encode it", atlas_ids=["2"]),
            {"verdict": "keep", "domain": "media", "name_en": "No how", "name_ar": "x"},
            dict(good, verdict="drop", name_en="Copyleft method"),
            dict(good, domain="astrology", name_en="Unknown domain")]
    vdir = c.work / "verify"
    write(vdir / "batch.json", json.dumps({"results": rows}, ensure_ascii=False))
    done = run(c, "atlas_transfer report on 5 fixture verifier rows", PY + [c.script, "report", "--verify", vdir])
    c.check("report exits 0", done.returncode == 0, done.returncode)
    rep = json.loads(done.stdout or "{}")
    want = {"verdict:keep": 4, "verdict:drop": 1, "merged-duplicate": 1, "dropped:missing-fields": 1,
            "dropped:unknown-domain": 1, "records:total": 1, "records:atlas-media": 1}
    c.check("every row got its known fate", all(rep.get(k) == v for k, v in want.items()),
            {"want": want, "got": rep})
    out = c.work / "powers"
    out.mkdir()  # the tool writes into an existing folder (normally data/powers)
    done = run(c, "atlas_transfer build into the work folder", PY + [c.script, "build", "--verify", vdir, "--out", out])
    recs = json.loads((out / "atlas-media.json").read_text(encoding="utf-8")) if (out / "atlas-media.json").is_file() else []
    c.check("build writes one atlas-media record with the merged ids and the longer how",
            done.returncode == 0 and len(recs) == 1 and recs[0]["atlas"]["ids"] == ["1", "2"]
            and recs[0]["how"] == "ffprobe the input first, then encode it",
            recs[0] if recs else done.stderr[-200:])


# --------------------------------------------------------------------------- atlas-review-summary
def _audited(i, skill, scope, state):
    return {"id": str(i), "skill": skill, "scope": scope, "path": f"skills/{skill}", "source": "upstream/x",
            "license": "MIT", "source_audit": {"state": state, "sha256": "%064x" % i, "warnings": [],
                                               "classification": "plain_text"}}


def atlas_review_summary(c: Ctx) -> None:
    """Four audited files; only the inspected main-scope ffmpeg and pre-mortem rows may become method candidates."""
    cat = {k: 1 for k in ("total", "main", "copyleft", "unique_normalized_skill_names", "reused_names",
                          "records_in_reused_names", "duplicate_description_groups",
                          "records_in_duplicate_descriptions", "claimed_file_count_sum", "claimed_complete_folders")}
    review = {"schema": "kosif.atlas.stratified-review.v2", "mode": "audit",
              "atlas_index_sha256": {"main": "a", "copyleft": "b"}, "catalog": cat, "source_sample_plan_size": 4,
              "static_audit_counts": {"warning:none": 4, "inspected": 4},
              "audited_files": [_audited(1, "ffmpeg", "main", "text_inspected_not_executed"),
                                _audited(2, "pre-mortem", "main", "text_inspected_not_executed"),
                                _audited(3, "remotion", "copyleft", "text_inspected_not_executed"),
                                _audited(4, "5why-root-cause", "main", "missing"),
                                _audited(5, "ffmpeg", "main", "text_inspected_not_executed")]}
    src = write(c.work / "review.json", json.dumps(review))
    out = c.work / "summary.json"
    done = run(c, "summarise a 5-row fixture review", PY + [c.script, "--review", src, "--output", out])
    r = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {}
    methods = [m["method"] for m in r.get("method_candidates", [])]
    c.check("exactly the two eligible methods, in PICKS order, duplicate ffmpeg kept once",
            done.returncode == 0 and methods == ["premortem_with_kill_criteria", "media_transcode_probe_validation"],
            methods)
    c.check("every candidate is marked not executed and not runtime-verified",
            bool(methods) and all(not m["executed"] and not m["runtime_verified"] for m in r["method_candidates"]), None)
    bad = write(c.work / "review-v1.json", json.dumps(dict(review, schema="kosif.atlas.stratified-review.v1")))
    done = run(c, "refuse a review with the wrong schema", PY + [c.script, "--review", bad, "--output", c.work / "x.json"])
    c.check("wrong schema is refused (non-zero exit, no output)", done.returncode != 0 and not (c.work / "x.json").exists(),
            done.returncode)


# --------------------------------------------------------------------------- build-chapters
def build_chapters(c: Ctx) -> None:
    ref = SKILL / "references" / "powers"
    stem = "thinking-core" if (ref / "thinking-core.md").is_file() else None
    if stem is None:
        done = run(c, "list families", PY + [c.script, "--check", "-q"])
        c.check("a generated family chapter exists to compare", False, "references/powers/thinking-core.md missing")
        return
    fresh = c.work / "fresh"
    done = run(c, f"render {stem} into the work folder", PY + [c.script, "--family", stem, "--out", fresh, "-q"])
    same = (fresh / f"{stem}.md").is_file() and (fresh / f"{stem}.md").read_bytes() == (ref / f"{stem}.md").read_bytes()
    c.check(f"rendered {stem}.md is byte-identical to the committed chapter", done.returncode == 0 and same,
            {"exit": done.returncode})
    done = run(c, "--check on the repository chapters", PY + [c.script, "--check", "-q"])
    c.check("--check passes on the committed chapters", done.returncode == 0, done.returncode)
    bad = c.work / "planted"
    bad.mkdir()
    text = (ref / f"{stem}.md").read_text(encoding="utf-8")
    write(bad / f"{stem}.md", text.replace("\n", "\nplanted stale line\n", 3))
    done = run(c, "--check on a planted stale chapter", PY + [c.script, "--family", stem, "--out", bad, "--check", "-q"])
    c.check("--check catches the planted stale chapter (exit 1)", done.returncode == 1, done.returncode)


# --------------------------------------------------------------------------- relabel-proofs
def relabel_proofs(c: Ctx) -> None:
    done = run(c, "--check on data/powers", PY + [c.script, "--check"])
    c.check("--check: no record would change", done.returncode == 0 and "would change 0 record" in done.stdout,
            done.stdout[-200:])
    cases = {"https://example.org/x": "url", "owner-upload:clip.mp4": "archive", "session-20261101.md": "session",
             "style:kinetic-arabic": "style", "kosif-tool/tools/build.py": "repo",
             "kosif-tool/tools/no_such_file_here.py": "missing", "kosif-atlas/skills/x": "sibling", "ran it once": "receipt"}
    code = ("import json,sys; sys.path.insert(0, sys.argv[1]); import relabel_proofs as R; "
            "print(json.dumps({p: R.scope_of(p) for p in json.loads(sys.argv[2])}))")
    done = run(c, "scope_of on 8 known paths", [sys.executable, "-I", "-B", "-c", code, SCRIPTS, json.dumps(list(cases))])
    got = json.loads(done.stdout or "{}")
    c.check("each path gets its known proof scope (a missing repo file is 'missing')", got == cases,
            {"want": cases, "got": got})


# --------------------------------------------------------------------------- protocol-lint
def _release(folder: Path, broken: bool) -> Path:
    v = "9.9"
    write(folder / "USIP_PORTABLE_v9_9.md", f"# USIP v{v} compact\n\nRoutes to A1.\n"
          + ("Old copy: USIP_PORTABLE_v9_8.md\n" if broken else ""))
    write(folder / "USIP_PORTABLE_FULL_v9_9.md",
          f"# USIP v{v} full\n\n- [Intro](#intro)\n" + ("- [Gone](#gone)\n" if broken else "")
          + "\n## Intro\n\nالبطاقة المرجعية السريعة\n1. one\n2. two\n\n---\n")
    write(folder / "USIP_PASTE.md", f"USIP v{v}\nما ستفعله بالضبط\n1. a\n" + ("3. b\n" if broken else "2. b\n")
          + "قواعد لا تُكسر\n")
    write(folder / "README.md", f"# README v{v}\n\n| `USIP_PORTABLE_v9_9.md` | compact |\n"
          "| `USIP_PORTABLE_FULL_v9_9.md` | full |\n| `USIP_PASTE.md` | paste |\n")
    return folder


def protocol_lint(c: Ctx) -> None:
    good = _release(c.work / "release-good", broken=False)
    done = run(c, "lint a clean v9.9 fixture release", PY + [c.script, good, "--version", "9.9", "--json"])
    r = json.loads(done.stdout or "{}")
    c.check("clean release passes (exit 0, no fails)", done.returncode == 0 and r.get("pass") is True and not r.get("fails"),
            r.get("fails"))
    bad = _release(c.work / "release-bad", broken=True)
    done = run(c, "lint a release with three planted drifts", PY + [c.script, bad, "--version", "9.9", "--json"])
    r = json.loads(done.stdout or "{}")
    codes = sorted({f.split()[0] for f in r.get("fails", [])})
    c.check("planted drifts caught: stale link (S), dead contents entry (T), numbering 1,3 (C)",
            done.returncode == 1 and codes == ["C", "S", "T"], {"codes": codes, "fails": r.get("fails")})
    real = REPO / "docs" / "protocol"
    done = run(c, "lint the repository's v6.5 compact protocol file for size", PY + [c.script, real, "--version", "6.5", "--json"])
    r = json.loads(done.stdout or "{}")
    c.check("repository's v6.5 compact file is under the 40 KB paste limit (no Z fail)",
            r.get("files", {}).get("compact") == "USIP_PORTABLE_v6_5.md"
            and not any(f.startswith("Z ") for f in r.get("fails", [])), r.get("fails", [])[:6])


# --------------------------------------------------------------------------- probe-env
def probe_env(c: Ctx) -> None:
    done = run(c, "probe this machine offline", PY + [c.script, "--json", "--no-network"])
    d = json.loads(done.stdout or "{}")
    c.check("probe exits 0 with JSON", done.returncode == 0 and "bins" in d, done.returncode)
    v = "%d.%d.%d" % sys.version_info[:3]
    c.check("reported Python version matches this interpreter", d.get("python", {}).get("version") == v,
            {"want": v, "got": d.get("python", {}).get("version")})
    found = {b: bool((d.get("bins") or {}).get(b, {}).get("path")) for b in ("ffmpeg", "git", "node")}
    real = {b: bool(shutil.which(b)) for b in found}
    c.check("ffmpeg / git / node presence matches shutil.which", found == real, {"probe": found, "which": real})
    c.check("network checks were skipped as asked", (d.get("network") or {}).get("skipped") is True, d.get("network"))


# --------------------------------------------------------------------------- collect-links
def collect_links(c: Ctx) -> None:
    page = write(c.work / "page.html", '<html><body><a href="https://example.org/a">Alpha</a>'
                 '<a href="https://example.org/b">Beta</a><a href="https://other.test/c">Gamma</a>'
                 '<a href="mailto:x@example.org">mail</a></body></html>')
    url = page.resolve().as_uri()
    done = run(c, "collect links from a local page in real Chromium", ["node", c.script, url, "--json"])
    d = json.loads(done.stdout or "{}") if done.stdout.strip().startswith("{") else {}
    hrefs = [x["href"] for x in d.get("links", [])]
    want = ["https://example.org/a", "https://example.org/b", "https://other.test/c"]
    c.check("the three http(s) links come back in order (mailto dropped)", done.returncode == 0 and hrefs == want,
            {"got": hrefs, "stderr": done.stderr[-200:]})
    done = run(c, "same page with --filter beta", ["node", c.script, url, "--filter", "beta"])
    c.check("--filter keeps only the Beta link", done.returncode == 0 and done.stdout.split() == ["https://example.org/b"],
            done.stdout[-200:])


# --------------------------------------------------------------------------- render-text
def _ink(png: Path):
    from PIL import Image
    im = Image.open(png).convert("L")
    dark = sum(1 for p in im.getdata() if p < 128)
    return im.size, dark


def render_text(c: Ctx) -> None:
    spec = write(c.work / "spec.json", json.dumps({"width": 900, "height": 300, "background": "#ffffff", "items": [
        {"id": "ar", "text": "بسم الله الرحمن الرحيم", "size": 64, "color": "#000000", "direction": "rtl", "family": "serif"},
        {"id": "short", "text": "بسم", "size": 64, "color": "#000000", "direction": "rtl", "family": "serif"},
        {"id": "blank", "text": "x", "size": 64, "color": "#ffffff", "direction": "ltr", "family": "serif"}]},
        ensure_ascii=False))
    out = c.work / "renders"
    done = run(c, "render 3 text items through Chromium", ["node", c.script, spec, out])
    c.check("render exits 0", done.returncode == 0, done.stderr[-300:])
    meta = json.loads((out / "renders.json").read_text(encoding="utf-8")) if (out / "renders.json").is_file() else []
    w = {m["id"]: m["width"] for m in meta}
    c.check("the long Arabic line is wider than the one-word line", w.get("ar", 0) > 2 * w.get("short", 1e9), w)
    try:
        (_, ink_ar), (_, ink_blank) = _ink(out / "ar.png"), _ink(out / "blank.png")
    except (OSError, ImportError) as exc:
        c.check("PNG files readable", False, str(exc))
        return
    c.check("black text leaves ink; white-on-white leaves none", ink_ar > 500 and ink_blank == 0,
            {"ar_dark_px": ink_ar, "blank_dark_px": ink_blank})


# --------------------------------------------------------------------------- color-media
def color_media(c: Ctx) -> None:
    from PIL import Image, ImageDraw
    photo = c.work / "in.png"
    im = Image.new("RGB", (160, 200), (40, 90, 200))
    ImageDraw.Draw(im).ellipse((40, 50, 120, 150), fill=(220, 40, 30))
    im.save(photo)
    out = c.work / "oil"
    done = run(c, "paint a red disc on blue in oil", PY + [c.script, "draw", "--photo", photo, "--out", out,
                                                         "--medium", "oil", "--subject", "scene", "--seed", "4"])
    png = out / "painting.png"
    c.check("draw exits 0 and writes painting.png + receipt.json",
            done.returncode == 0 and png.is_file() and (out / "receipt.json").is_file(), done.stderr[-200:])
    if not png.is_file():
        return
    p = Image.open(png).convert("RGB")
    W, H = p.size
    def mean(box):
        px = list(p.crop(box).getdata())
        return tuple(round(sum(v[i] for v in px) / len(px)) for i in range(3))
    centre = mean((int(W * .4), int(H * .45), int(W * .6), int(H * .55)))
    corner = mean((0, 0, int(W * .15), int(H * .12)))
    c.check("centre of the painting is red (R > B + 60)", centre[0] > centre[2] + 60, centre)
    c.check("corner of the painting is blue (B > R + 60)", corner[2] > corner[0] + 60, corner)
    c.check("no photo pixel copied: painting differs from the photo",
            p.resize(im.size).tobytes() != im.tobytes(), None)


# --------------------------------------------------------------------------- repo-build
def repo_build(c: Ctx) -> None:
    done = run(c, "tools/build.py --check (writes nothing)", PY + [c.script, "--check"])
    c.check("every derived catalog file is up to date (exit 0)",
            done.returncode == 0 and "up to date" in done.stdout, done.stdout[-300:])


# --------------------------------------------------------------------------- starter-remotion
REMOTION_LINE = re.compile(r"^KosifFilm\s+(\d+)\s+(\d+)x(\d+)\s+(\d+)\b", re.M)


def starter_remotion(c: Ctx) -> None:
    """The Remotion starter, really bundled and rendered by Remotion in headless Chromium.

    Needs `npm ci` in starters/remotion (CI does it; node_modules is gitignored and never committed).
    Known answers: one composition KosifFilm at 30 fps, 1080x1920, 360 frames; frames 0 and 60 render
    to non-blank 1080x1920 PNGs that differ (it moves); tsc finds no type error; and a planted flaw,
    a composition id that does not exist, must be refused with no file written.
    """
    root = c.script if c.script.is_dir() else c.script.parent
    cli = root / "node_modules" / ".bin" / "remotion"
    c.check("starter's node_modules installed (npm ci in starters/remotion)", cli.is_file(), str(cli))
    if not cli.is_file():
        return
    from PIL import Image  # only needed once Remotion is installed
    done = run(c, "remotion compositions src/index.ts", [cli, "compositions", "src/index.ts"], cwd=root)
    m = REMOTION_LINE.search(done.stdout)
    got = tuple(int(x) for x in m.groups()) if m else None
    c.check("composition KosifFilm: 30 fps, 1080x1920, 360 frames", done.returncode == 0 and got == (30, 1080, 1920, 360),
            got or done.stderr[-200:])
    stills = {}
    for frame in (0, 60):
        png = c.work / f"still-{frame}.png"
        done = run(c, f"remotion still KosifFilm frame {frame}",
                   [cli, "still", "KosifFilm", png, f"--frame={frame}"], cwd=root)
        ok = done.returncode == 0 and png.is_file()
        info = None
        if ok:
            im = Image.open(png).convert("RGB")
            colors = im.getcolors(1 << 22) or []
            lo, hi = im.convert("L").getextrema()
            info = {"size": list(im.size), "colors": len(colors), "luma": [lo, hi]}
            stills[frame] = im.tobytes()
            ok = im.size == (1080, 1920) and len(colors) > 50 and hi - lo > 30
        c.check(f"frame {frame}: 1080x1920 PNG with real, non-blank pixels", ok, info or done.stderr[-200:])
    c.check("frames 0 and 60 differ (the film moves)", len(stills) == 2 and stills[0] != stills[60], None)
    tsc = root / "node_modules" / ".bin" / "tsc"
    done = run(c, "tsc --noEmit (npm run typecheck)", [tsc, "--noEmit"], cwd=root)
    c.check("typecheck passes", done.returncode == 0, done.stdout[-200:])
    bad = c.work / "no-such.png"
    done = run(c, "planted flaw: still of a composition that does not exist",
               [cli, "still", "NoSuchFilm", bad, "--frame=0"], cwd=root)
    c.check("planted flaw caught: unknown composition refused, no file written",
            done.returncode != 0 and not bad.exists(), done.returncode)


# --------------------------------------------------------------------------- repo-ashell-cinema
def ashell_cinema(c: Ctx) -> None:
    """The iPhone a-Shell app, run offline in dash with HOME inside the work folder: Photos SAFE on a planted
    H.264 clip must be a lossless stream copy; a planted MPEG-2 .ts must NOT be copied (it is re-encoded).
    Downloads are not exercised (they need the user's device and network)."""
    home = c.work / "home"
    dl = home / "Documents" / "Cinema_Downloads"
    dl.mkdir(parents=True, exist_ok=True)
    env = dict(c.env, HOME=str(home))
    ff = ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=3",
          "-f", "lavfi", "-i", "sine=frequency=440:duration=3", "-shortest"]
    run(c, "planted H.264 clip", ff + ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(dl / "clip.mp4")])
    run(c, "planted MPEG-2 transport stream", ff + ["-c:v", "mpeg2video", "-c:a", "mp2", "-f", "mpegts", str(dl / "old.ts")])

    def safe(name):
        done = subprocess.run(["dash", str(c.script), "--safe", name], cwd=dl, env=env, text=True, capture_output=True,
                              stdin=subprocess.DEVNULL, timeout=c.timeout, check=False)
        c.steps.append({"step": "c --safe " + name, "exit_code": done.returncode, "stdout_tail": done.stdout[-600:]})
        return done.stdout

    out_h264 = safe("clip.mp4")
    made = dl / "PhotosSafe_clip.mp4"
    c.check("H.264 source: lossless stream copy", "Method: lossless copy (h264)" in out_h264, out_h264[-300:])
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name", "-of", "csv=p=0", str(made)],
                           capture_output=True, text=True).stdout.split() if made.is_file() else []
    c.check("Photos-safe MP4 written with h264 + aac", made.is_file() and probe[:2] == ["h264", "aac"], probe)
    out_ts = safe("old.ts")
    c.check("MPEG-2 source is not passed off as a lossless copy", "Method: lossless copy" not in out_ts
            and "Photos-safe MP4 ready" in out_ts, out_ts[-300:])


RECIPES = {
    "repo-ashell-cinema": ashell_cinema,
    "atlas-transfer": atlas_transfer,
    "atlas-review-summary": atlas_review_summary,
    "build-chapters": build_chapters,
    "relabel-proofs": relabel_proofs,
    "protocol-lint": protocol_lint,
    "probe-env": probe_env,
    "collect-links": collect_links,
    "render-text": render_text,
    "color-media": color_media,
    "repo-build": repo_build,
    "starter-remotion": starter_remotion,
}
