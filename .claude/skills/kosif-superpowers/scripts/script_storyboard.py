#!/usr/bin/env python3
"""KOSIF Script-to-Storyboard: turn a play or screenplay into a shot list, then into a timed animatic MP4.

    python3 scripts/script_storyboard.py parse  <script.txt|script.pdf> --out storyboard.json [--title T]
                                               [--first-page N --last-page M] [--episode-seconds 90]
    python3 scripts/script_storyboard.py blank  --out storyboard.json --title T --duration 15 --shots 3
    python3 scripts/script_storyboard.py render --storyboard storyboard.json --out film.mp4 [--audio voice.m4a]
                                               [--episode N] [--width 1080 --height 1920 --fps 30 --crf 17]
    python3 scripts/script_storyboard.py --self-test

`parse` reads Arabic or English scripts written the usual stage way: act headings (الفصل / الجزء / ACT),
scene headings (المشهد / SCENE / INT. / EXT. / داخلي / خارجي), dialogue lines "NAME: text" or
"NAME (direction): text", and everything else as stage directions. PDF input goes through `pdftotext`
(poppler). Bidi control marks and Arabic presentation forms are cleaned, wrapped PDF lines are re-joined,
and page numbers are dropped. Each scene gets an establishing wide shot, dialogue shots that change size
on a speaker change or an emotional cue, and a duration estimated from the word count (2.3 spoken words
per second, 3 read words per second for directions, clamped to 1.5..8 s). It also reports characters with
their line counts, spellings that look like the same name (for example ألبس / ألباس), the pacing per act,
and how the scenes group into short-form episodes under --episode-seconds.

`render` makes a deterministic animatic: each shot is its own image or video (`source`, relative to the
storyboard) cropped to fill the frame, or a flat colour card when no source is set. Shot lengths are cut
on exact frame boundaries so the timeline never drifts. With --audio the audio is the master: shot
durations are scaled to its length and the track is stream-copied when MP4 can hold it. Defaults follow
the KOSIF export standard (1080x1920, 30 fps, H.264 CRF 17, BT.709, +faststart; scripts/export_profile.py
when present). It never writes text onto frames and never invents footage.

Stdlib only; FFmpeg/ffprobe are needed for `render`, pdftotext for PDF input. Ported and extended from the
owner's KOSIF Cinematic Toolkit (storyboard + master-audio render).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

SCHEMA = "kosif.storyboard.v1"
HERE = Path(__file__).resolve().parent

try:  # the shared export standard, when this checkout has it
    sys.path.insert(0, str(HERE))
    import export_profile as _xp  # type: ignore
    WIDTH, HEIGHT, FPS, CRF = _xp.WIDTH, _xp.HEIGHT, _xp.FPS, _xp.CRF
except Exception:  # pragma: no cover - same numbers as playbooks/export-standard.md
    _xp = None
    WIDTH, HEIGHT, FPS, CRF = 1080, 1920, 30, 17

SPOKEN_WPS = 2.3      # spoken Arabic/English words per second
READ_WPS = 3.0        # stage directions play faster than speech
MIN_SHOT, MAX_SHOT = 1.5, 8.0
PALETTE = ["#122826", "#29392d", "#2a263b", "#513427", "#20334a", "#3f3632", "#2f2a1f", "#1f2f3a"]
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
MP4_COPY_AUDIO = ("aac", "mp3", "alac")

BIDI = dict.fromkeys(map(ord, "‎‏‪‫‬‭‮⁦⁧⁨⁩﻿"), None)
DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")
ACT_RE = re.compile(r"^(?:الفصل|الجزء|ACT|Act|act|PART|Part)\b\s*(.*)$")
SCENE_RE = re.compile(r"^(?:المشهد|مشهد|SCENE|Scene|scene|INT\.|EXT\.|INT/EXT\.|داخلي|خارجي)(?:\s|[.:\-–]|$)\s*(.*)$")
SPEAKER_RE = re.compile(r"^(?P<name>[^:：()\d][^:：()]{0,40}?)\s*(?:\((?P<dir>[^)]{1,120})\))?\s*[:：]\s*(?P<text>.*)$")
PAREN_RE = re.compile(r"\(([^)]{1,200})\)")
WORD_RE = re.compile(r"[\w؀-ۿ]+")
SENTENCE_END = tuple(".!?؟…:»\"')")
ORDINALS = [("اول", 1), ("الول", 1), ("ثاني", 2), ("ثالث", 3), ("رابع", 4), ("خامس", 5), ("سادس", 6), ("سابع", 7),
            ("ثامن", 8), ("تاسع", 9), ("عاشر", 10), ("one", 1), ("two", 2), ("three", 3), ("four", 4), ("five", 5)]
MOVE_WORDS = set("يركض تركض يجري تجري يدخل تدخل يخرج تخرج يسير تسير يدفع تدفع يقترب تقترب يندفع تندفع تنطلق ينطلق "
                 "runs enters exits walks rushes crosses moves pushes chases".split())
EMOTION_MARKS = ("!", "؟!", "?!")


# ---------------------------------------------------------------------------- text helpers
def clean_line(raw: str) -> str:
    s = unicodedata.normalize("NFKC", raw.translate(BIDI)).replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def norm_key(s: str) -> str:
    s = DIACRITICS.sub("", clean_line(s)).casefold()
    s = re.sub("[أإآٱ]", "ا", s).replace("ى", "ي").replace("ة", "ه")
    return re.sub(r"[^\w؀-ۿ]", "", s)


def words(s: str) -> int:
    return len(WORD_RE.findall(s or ""))


def ordinal(heading: str) -> int | None:
    m = re.search(r"\d+", heading)
    if m:
        return int(m.group())
    k = re.sub(r"ا+", "ا", norm_key(re.sub(r"^\S+\s*", "", clean_line(heading))))
    for stem, n in ORDINALS:
        if stem in k:
            return n
    return None


def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def looks_like_speaker(name: str) -> bool:
    n = name.strip()
    return bool(n) and len(n) <= 30 and 1 <= len(n.split()) <= 3 and not n.endswith(("،", ",", "."))


# ---------------------------------------------------------------------------- parsing
def read_script(path: Path, first: int | None = None, last: int | None = None) -> str:
    if path.suffix.lower() == ".pdf":
        if not shutil.which("pdftotext"):
            raise RuntimeError("pdftotext (poppler-utils) is needed to read PDF scripts; export the script as .txt instead")
        cmd = ["pdftotext", "-enc", "UTF-8"]
        if first:
            cmd += ["-f", str(first)]
        if last:
            cmd += ["-l", str(last)]
        p = subprocess.run(cmd + [str(path), "-"], capture_output=True, text=True)
        if p.returncode:
            raise RuntimeError("pdftotext failed: " + p.stderr[-400:])
        return p.stdout
    return path.read_text(encoding="utf-8-sig", errors="replace")


def blocks(text: str) -> list[dict]:
    """Lines -> typed blocks (act, scene, dialogue, action) with wrapped lines re-joined."""
    out: list[dict] = []
    for raw in text.replace("\f", "\n\n").splitlines():
        line = clean_line(raw)
        if not line:
            if out and out[-1]["type"] in ("action", "dialogue"):
                out[-1]["closed"] = True
            continue
        if re.fullmatch(r"[\d\s\-–—|]+", line):
            continue  # page numbers and rules
        m = ACT_RE.match(line)
        if m and len(line) <= 40:
            out.append({"type": "act", "heading": line})
            continue
        m = SCENE_RE.match(line)
        if m and len(line) <= 80:
            out.append({"type": "scene", "heading": line})
            continue
        m = SPEAKER_RE.match(line)
        if m and looks_like_speaker(m.group("name")):
            out.append({"type": "dialogue", "character": DIACRITICS.sub("", m.group("name")).strip(),
                        "direction": (m.group("dir") or "").strip(), "text": m.group("text").strip(), "closed": False})
            continue
        prev = out[-1] if out else None
        if prev and prev["type"] in ("action", "dialogue") and not prev.get("closed") \
                and not prev["text"].endswith(SENTENCE_END):
            prev["text"] = (prev["text"] + " " + line).strip()
            continue
        out.append({"type": "action", "text": line, "closed": False})
    return out


def shot_duration(text: str, wps: float, lo: float, hi: float) -> float:
    return round(min(hi, max(lo, words(text) / wps)), 3)


def plan(blist: list[dict], *, title: str, wps: float = SPOKEN_WPS, lo: float = MIN_SHOT, hi: float = MAX_SHOT) -> dict:
    acts: list[dict] = []
    scenes: list[dict] = []
    act = None
    scene = None

    def new_act(heading):
        nonlocal act
        n = ordinal(heading)
        if act is not None and n is not None and act["number"] == n:
            return  # the same act repeated above each scene
        act = {"id": f"A{len(acts) + 1}", "heading": heading, "number": n if n is not None else len(acts) + 1}
        acts.append(act)

    def new_scene(heading):
        nonlocal scene
        if act is None:
            new_act("Act 1")
        scene = {"id": f"S{len(scenes) + 1:03d}", "act": act["id"], "heading": heading, "setting": "",
                 "color": PALETTE[len(scenes) % len(PALETTE)], "characters": [], "shots": []}
        scenes.append(scene)

    last_speaker = None
    for b in blist:
        if b["type"] == "act":
            new_act(b["heading"])
            continue
        if b["type"] == "scene":
            new_scene(b["heading"])
            last_speaker = None
            continue
        if scene is None:
            new_scene("Scene 1")
        shots = scene["shots"]
        sid = f"{scene['id']}-{len(shots) + 1:02d}"
        if b["type"] == "action":
            text = b["text"]
            if not scene["setting"]:
                scene["setting"] = text[:200]
            moving = any(w in MOVE_WORDS for w in WORD_RE.findall(text.casefold()))
            if not shots:
                size, camera = "wide (establishing)", "slow push-in"
            elif words(text) <= 8:
                size, camera = "insert / close detail", "static"
            else:
                size, camera = "medium wide", "tracking" if moving else "slow pan"
            shots.append({"id": sid, "kind": "action", "character": "", "text": text, "direction": "",
                          "shot_size": size, "camera": camera, "duration": shot_duration(text, READ_WPS, lo, hi),
                          "color": scene["color"], "source": ""})
            last_speaker = None
            continue
        who = b["character"]
        text = b["text"]
        inline = PAREN_RE.findall(text)
        direction = "; ".join(x for x in [b["direction"], *inline] if x)
        spoken = PAREN_RE.sub(" ", text).strip()
        if not shots:
            shots.append({"id": sid, "kind": "action", "character": "", "text": scene["heading"], "direction": "",
                          "shot_size": "wide (establishing)", "camera": "slow push-in", "duration": lo,
                          "color": scene["color"], "source": ""})
            sid = f"{scene['id']}-{len(shots) + 1:02d}"
        emotional = bool(direction) or spoken.endswith(EMOTION_MARKS) or words(spoken) <= 3
        if who == last_speaker:
            size = "close-up" if emotional else "medium close-up"
        else:
            size = "close-up" if emotional else ("over-the-shoulder" if last_speaker else "medium")
        camera = "slow push-in" if words(spoken) > 25 else "static"
        shots.append({"id": sid, "kind": "dialogue", "character": who, "text": spoken, "direction": direction,
                      "shot_size": size, "camera": camera, "duration": shot_duration(spoken, wps, lo, hi),
                      "color": scene["color"], "source": ""})
        if who not in scene["characters"]:
            scene["characters"].append(who)
        last_speaker = who

    scenes = [s for s in scenes if s["shots"]]
    chars: dict[str, dict] = {}
    for s in scenes:
        for sh in s["shots"]:
            if sh["kind"] == "dialogue":
                c = chars.setdefault(sh["character"], {"name": sh["character"], "lines": 0, "words": 0, "first_scene": s["id"]})
                c["lines"] += 1
                c["words"] += words(sh["text"])
    characters = sorted(chars.values(), key=lambda c: (-c["lines"], c["name"]))
    aliases = []
    names = [c["name"] for c in characters]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ka, kb = norm_key(a), norm_key(b)
            if ka == kb or (min(len(ka), len(kb)) >= 4 and edit_distance(ka, kb) <= 1):
                aliases.append([a, b])
    total = round(sum(sh["duration"] for s in scenes for sh in s["shots"]), 3)
    return {"schema": SCHEMA, "project": "KOSIF", "title": title, "orientation": "9:16",
            "export": {"width": WIDTH, "height": HEIGHT, "fps": FPS, "crf": CRF},
            "acts": [a for a in acts if any(s["act"] == a["id"] for s in scenes)],
            "scenes": scenes, "characters": characters,
            "warnings": [f"possible same character spelled two ways: {a} / {b}" for a, b in aliases],
            "totals": {"acts": len({s['act'] for s in scenes}), "scenes": len(scenes),
                       "shots": sum(len(s["shots"]) for s in scenes),
                       "dialogue_shots": sum(1 for s in scenes for sh in s["shots"] if sh["kind"] == "dialogue"),
                       "seconds": total}}


def pacing(board: dict, episode_seconds: float | None) -> dict:
    scenes = board["scenes"]
    total = board["totals"]["seconds"] or 1
    per_act = {}
    for s in scenes:
        per_act.setdefault(s["act"], 0.0)
        per_act[s["act"]] += sum(sh["duration"] for sh in s["shots"])
    secs = {s["id"]: round(sum(sh["duration"] for sh in s["shots"]), 3) for s in scenes}
    report = {"seconds_per_act": {k: round(v, 3) for k, v in per_act.items()},
              "share_per_act": {k: round(v / total, 3) for k, v in per_act.items()},
              "longest_scene": max(secs, key=secs.get) if secs else None,
              "scenes_without_dialogue": [s["id"] for s in scenes if not s["characters"]]}
    if episode_seconds:
        # Cut at every scene start that would overflow, and inside a long scene at shot
        # boundaries, so no episode runs over the limit unless one single shot does.
        eps, cur, t = [], [], 0.0
        for s in scenes:
            scene_secs = secs[s["id"]]
            if cur and t + scene_secs > episode_seconds:
                eps.append(cur)
                cur, t = [], 0.0
            for sh in s["shots"]:
                if cur and t + sh["duration"] > episode_seconds:
                    eps.append(cur)
                    cur, t = [], 0.0
                cur.append((s["id"], sh["id"], sh["duration"]))
                t += sh["duration"]
        if cur:
            eps.append(cur)
        report["episodes"] = [{"episode": i + 1, "first_shot": e[0][1], "last_shot": e[-1][1],
                               "scenes": sorted({x[0] for x in e}), "shots": len(e),
                               "seconds": round(sum(x[2] for x in e), 3)} for i, e in enumerate(eps)]
        report["episode_limit_seconds"] = episode_seconds
        report["scenes_split_across_episodes"] = [k for k, v in secs.items() if v > episode_seconds]
    return report


def parse_cmd(src: Path, out: Path, title: str | None, first, last, episode_seconds, wps) -> dict:
    if not src.is_file():
        raise FileNotFoundError(str(src))
    text = read_script(src, first, last)
    board = plan(blocks(text), title=title or src.stem, wps=wps)
    if not board["scenes"]:
        raise ValueError("no scenes or lines found in the script")
    board["source"] = {"file": src.name, "sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
                       "pages": [first, last] if (first or last) else None}
    board["pacing"] = pacing(board, episode_seconds)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"file": str(out), **board["totals"], "characters": len(board["characters"]),
            "warnings": len(board["warnings"])}


def blank_cmd(out: Path, title: str, duration: float, shots: int) -> dict:
    if not 1 <= shots <= 100:
        raise ValueError("shots must be 1..100")
    if not (duration > 0 and math.isfinite(duration)):
        raise ValueError("duration must be positive")
    each = round(duration / shots, 3)
    sc = {"id": "S001", "act": "A1", "heading": "Scene 1", "setting": "", "color": PALETTE[0], "characters": [],
          "shots": [{"id": f"S001-{i + 1:02d}", "kind": "action", "character": "",
                     "text": f"Shot {i + 1}: describe framing, movement, subject and lighting", "direction": "",
                     "shot_size": "", "camera": "", "duration": each, "color": PALETTE[i % len(PALETTE)], "source": ""}
                    for i in range(shots)]}
    board = {"schema": SCHEMA, "project": "KOSIF", "title": title, "orientation": "9:16",
             "export": {"width": WIDTH, "height": HEIGHT, "fps": FPS, "crf": CRF},
             "acts": [{"id": "A1", "heading": "Act 1", "number": 1}], "scenes": [sc], "characters": [], "warnings": [],
             "totals": {"acts": 1, "scenes": 1, "shots": shots, "dialogue_shots": 0, "seconds": round(each * shots, 3)}}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"file": str(out), "shots": shots, "seconds": board["totals"]["seconds"]}


# ---------------------------------------------------------------------------- render
def flat_shots(board: dict) -> list[dict]:
    if isinstance(board.get("scenes"), list):
        return [sh for s in board["scenes"] for sh in s.get("shots", [])]
    return list(board.get("shots", []))  # the toolkit's older flat layout


def valid_color(raw) -> str:
    raw = str(raw or PALETTE[0])
    if not re.fullmatch(r"(0x|#)[0-9a-fA-F]{6}", raw):
        raise ValueError("shot colour must be #RRGGBB or 0xRRGGBB")
    return "0x" + raw[-6:]


def frame_plan(durations: list[float], fps: int) -> list[int]:
    """Frames per shot from cumulative boundaries, so rounding never drifts the timeline."""
    out, t = [], 0.0
    for d in durations:
        a, t = round(t * fps), t + d
        out.append(max(1, round(t * fps) - a))
    return out


def run(cmd: list) -> str:
    p = subprocess.run([str(x) for x in cmd], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError("ffmpeg failed: " + p.stderr[-1500:])
    return p.stdout


def media_seconds(path: Path) -> float:
    out = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    try:
        return float(out.strip())
    except ValueError:
        raise ValueError(f"cannot read the duration of {path}") from None


def audio_codec(path: Path) -> str | None:
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=codec_name",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return p.stdout.strip().splitlines()[0] if p.returncode == 0 and p.stdout.strip() else None


def video_args(crf: int, fps: int) -> list[str]:
    if _xp is not None:
        return _xp.video_args(crf=crf, fps=fps)
    return ["-c:v", "libx264", "-preset", "slow", "-crf", str(min(crf, CRF)), "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv", "-r", str(fps)]


def shot_source(board_path: Path, raw) -> Path | None:
    if not raw:
        return None
    p = Path(str(raw)).expanduser()
    if not p.is_absolute():
        p = board_path.parent / p
    if not p.is_file():
        raise FileNotFoundError("missing shot media: " + str(p))
    if p.suffix.lower() not in IMAGE_EXT | VIDEO_EXT:
        raise ValueError("unsupported shot media: " + str(p))
    return p.resolve()


def render_cmd(board_path: Path, out: Path, audio: Path | None, width: int, height: int, fps: int, crf: int,
               max_shots: int, keep_work: bool, episode: int | None = None) -> dict:
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("render needs ffmpeg and ffprobe on PATH")
    if width < 128 or height < 128 or width % 2 or height % 2 or not 1 <= fps <= 120 or not 0 <= crf <= 51:
        raise ValueError("width/height must be even and >=128, fps 1..120, crf 0..51")
    crf = min(crf, CRF)  # the export standard: quality only goes up
    board = json.loads(board_path.read_text(encoding="utf-8"))
    shots = flat_shots(board)
    if episode:
        eps = {e["episode"]: e for e in board.get("pacing", {}).get("episodes", [])}
        if episode not in eps:
            raise ValueError(f"episode {episode} is not in the storyboard (run parse with --episode-seconds)")
        ids = [s.get("id") for s in shots]
        e = eps[episode]
        if e["first_shot"] not in ids or e["last_shot"] not in ids:
            raise ValueError("the episode's shots are no longer in the storyboard; run parse again")
        shots = shots[ids.index(e["first_shot"]):ids.index(e["last_shot"]) + 1]
    if not shots:
        raise ValueError("the storyboard has no shots")
    if len(shots) > max_shots:
        raise ValueError(f"{len(shots)} shots is over --max-shots {max_shots}; render one episode at a time")
    durations = [float(s.get("duration", 0)) for s in shots]
    if any(not (d > 0 and math.isfinite(d)) for d in durations):
        raise ValueError("every shot needs a positive duration")
    master = None
    if audio:
        audio = audio.expanduser().resolve()
        if not audio.is_file():
            raise FileNotFoundError(str(audio))
        master = media_seconds(audio)
        if master <= 0:
            raise ValueError("the audio has no usable duration")
        k = master / sum(durations)
        durations = [d * k for d in durations]
    frames = frame_plan(durations, fps)
    sources = [shot_source(board_path, s.get("source")) for s in shots]
    out = out.expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    if audio and out.resolve() == audio:
        raise ValueError("the output would overwrite the audio")

    def produce(work: Path):
        parts = []
        fill = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1,fps={fps}"
        for i, (shot, n, src) in enumerate(zip(shots, frames, sources)):
            part = work / f"{i:04d}.mp4"
            cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
            if src is None:
                cmd += ["-f", "lavfi", "-i", f"color=c={valid_color(shot.get('color'))}:s={width}x{height}:r={fps}"]
                vf = "setsar=1,format=yuv420p"
            elif src.suffix.lower() in IMAGE_EXT:
                cmd += ["-loop", "1", "-framerate", str(fps), "-i", src]
                vf = fill + ",format=yuv420p"
            else:
                cmd += ["-stream_loop", "-1", "-i", src]
                vf = fill + ",format=yuv420p"
            cmd += ["-an", "-vf", vf, "-frames:v", str(n), *video_args(crf, fps), part]
            run(cmd)
            parts.append(part)
        listing = work / "timeline.ffconcat"
        listing.write_text("ffconcat version 1.0\n" + "".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
        silent = work / "timeline.mp4"
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-safe", "0", "-f", "concat", "-i", listing,
             "-c", "copy", silent])
        if audio:
            a_args = ["-c:a", "copy"] if audio_codec(audio) in MP4_COPY_AUDIO else ["-c:a", "aac", "-b:a", "320k", "-ar", "48000"]
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", silent, "-i", audio, "-map", "0:v:0",
                 "-map", "1:a:0", "-c:v", "copy", *a_args, "-movflags", "+faststart", out])
        else:
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", silent, "-c", "copy",
                 "-movflags", "+faststart", out])

    if keep_work:
        work = out.with_suffix(".work")
        work.mkdir(parents=True, exist_ok=True)
        produce(work)
    else:
        with tempfile.TemporaryDirectory(prefix="kosif-animatic-") as td:
            produce(Path(td))
    report = {"schema": "kosif.animatic-report.v1", "title": board.get("title"), "episode": episode, "output": str(out),
              "audio": str(audio) if audio else None, "master_audio_seconds": master,
              "shots": len(shots), "frames": sum(frames), "seconds": round(sum(frames) / fps, 3),
              "width": width, "height": height, "fps": fps, "crf": crf,
              "shot_frames": {s.get("id", str(i)): n for i, (s, n) in enumerate(zip(shots, frames))},
              "note": "Animatic for timing only: colour cards or the user's own media, no generated footage."}
    out.with_suffix(".report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"file": str(out), "report": str(out.with_suffix(".report.json")), "shots": len(shots),
            "seconds": report["seconds"]}


# ---------------------------------------------------------------------------- self-test
SAMPLE = """الفصل الأول
المشهد الأول
محطة قطار مزدحمة، يدفع ولدان عربتين محملتين بالحقائب وتتبعهما أمهما.
سامي: أبي... أبي... (يرددها عدة مرات)
الأب: توقف عن مضايقة أخيك.
سمير (بضجر): هل يمكن أن نمضي الآن؟
سامي: لا!
الفصل الأول
المشهد الثاني
رصيف يغطيه البخار.
سامى: هذا هو المكان.
"""


def self_test() -> int:
    board = plan(blocks(SAMPLE), title="t")
    assert board["totals"]["acts"] == 1, board["totals"]
    assert board["totals"]["scenes"] == 2
    s1 = board["scenes"][0]["shots"]
    assert s1[0]["shot_size"].startswith("wide") and s1[0]["kind"] == "action"
    assert s1[1]["character"] == "سامي" and "يرددها" in s1[1]["direction"]
    assert s1[3]["direction"] == "بضجر" and s1[3]["shot_size"] == "close-up"
    assert any("سامي" in w and "سامى" in w for w in board["warnings"]), board["warnings"]
    assert frame_plan([1 / 3] * 3, 30) == [10, 10, 10] and sum(frame_plan([0.33] * 10, 30)) == 99
    assert clean_line("‫الفصل‬  ﻻ") == "الفصل لا"
    assert ordinal("الفصل األول") == 1 and ordinal("الفصل الثاني") == 2
    print("self-test ok")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="KOSIF script -> storyboard -> animatic")
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("parse", help="play/screenplay text or PDF -> storyboard JSON")
    p.add_argument("script")
    p.add_argument("--out", required=True)
    p.add_argument("--title")
    p.add_argument("--first-page", type=int)
    p.add_argument("--last-page", type=int)
    p.add_argument("--episode-seconds", type=float, default=90.0)
    p.add_argument("--wps", type=float, default=SPOKEN_WPS, help="spoken words per second (default 2.3)")
    b = sub.add_parser("blank", help="empty storyboard template")
    b.add_argument("--out", required=True)
    b.add_argument("--title", default="KOSIF Film")
    b.add_argument("--duration", type=float, default=15)
    b.add_argument("--shots", type=int, default=3)
    r = sub.add_parser("render", help="storyboard -> timed animatic MP4")
    r.add_argument("--storyboard", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--audio")
    r.add_argument("--width", type=int, default=WIDTH)
    r.add_argument("--height", type=int, default=HEIGHT)
    r.add_argument("--fps", type=int, default=FPS)
    r.add_argument("--crf", type=int, default=CRF)
    r.add_argument("--max-shots", type=int, default=250)
    r.add_argument("--keep-work", action="store_true")
    r.add_argument("--episode", type=int, help="render only this episode from the parse report")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.cmd:
        ap.print_help()
        return 2
    try:
        if a.cmd == "parse":
            if a.wps <= 0:
                raise ValueError("--wps must be positive")
            res = parse_cmd(Path(a.script), Path(a.out), a.title, a.first_page, a.last_page, a.episode_seconds or None, a.wps)
        elif a.cmd == "blank":
            res = blank_cmd(Path(a.out), a.title, a.duration, a.shots)
        else:
            res = render_cmd(Path(a.storyboard), Path(a.out), Path(a.audio) if a.audio else None, a.width, a.height,
                             a.fps, a.crf, a.max_shots, a.keep_work, a.episode)
    except (ValueError, RuntimeError, FileNotFoundError, json.JSONDecodeError) as err:
        print(f"KOSIF ERROR: {err}", file=sys.stderr)
        return 1
    print(json.dumps(res, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
