#!/usr/bin/env python3
"""Montage Pro — فريق مهمة المونتاج والموشن والـ3D داخل KOSIF Superpowers.

Upload an audio or a video, get a team, a menu of strong options, and a real render.

  python3 montage_pro.py doctor                                  # tools present/missing for the team
  python3 montage_pro.py team                                    # the 13 roles, their scripts and gates
  python3 montage_pro.py intake MEDIA --job JOB                  # analyst: measure the file (ffprobe, loudness, energy cues, cuts)
  python3 montage_pro.py options JOB [--brief "..."]             # director: option menu for this material + stage plan
  python3 montage_pro.py acquire URL --job JOB --license "CC0 / owner / …" --source-page URL [--owner]
                                                                 # IDM-style desk: segmented resumable file download or stream grab + rights.json
  python3 montage_pro.py convert JOB                             # conformer: edit-ready mezzanine (CFR H.264/AAC 48k) + 540p proxies
  python3 montage_pro.py build JOB --option ID [--style …]       # editor/motion/render/QA: produce and verify the chosen option

Every output is verified with verify_video.py; results land in JOB/report.json. The user's master audio is never
modified (its SHA-256 is recorded and re-checked). Nothing is downloaded without a licence note.
Python 3.8+ stdlib; uses ffmpeg/ffprobe, node+Chromium (HTML scenes) and yt-dlp when present.
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
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
TEAM = SKILL / "data" / "montage_pro_team.json"
PY = sys.executable or "python3"
STREAM_HOSTS = ("youtube.com", "youtu.be", "vimeo.com", "x.com", "twitter.com", "tiktok.com", "instagram.com",
                "facebook.com", "dailymotion.com", "twitch.tv", "reddit.com", "streamable.com")
DIRECT_EXT = (".mp4", ".mov", ".webm", ".mkv", ".m4a", ".mp3", ".wav", ".aac", ".flac", ".ogg", ".png", ".jpg", ".jpeg",
              ".gif", ".zip", ".m4v", ".avi")


# ------------------------------------------------------------------ helpers
def sh(cmd, timeout=1800, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=timeout, **kw)
    return r.returncode, r.stdout, r.stderr


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def jload(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def jsave(p: Path, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def need(tool):
    if not shutil.which(tool):
        raise SystemExit(f"{tool} not found; run montage_pro.py doctor")


def report(job: Path, key: str, value):
    r = jload(job / "report.json", {}) or {}
    r[key] = value
    jsave(job / "report.json", r)


# ------------------------------------------------------------------ doctor / team
def doctor():
    tools = {"ffmpeg": "cut, encode, loudness, reframe, looks", "ffprobe": "measure media", "node": "HTML scene render",
             "yt-dlp": "stream grab (pip install yt-dlp)", "aria2c": "optional multi-connection downloads",
             "blender": "optional 3D", "chromium": "HTML scene render"}
    out = {k: {"present": bool(shutil.which(k)) or (k == "chromium" and bool(os.environ.get("PLAYWRIGHT_BROWSERS_PATH"))), "role": v}
           for k, v in tools.items()}
    py = {}
    for m in ("numpy", "cv2", "PIL", "faster_whisper", "librosa"):
        try:
            __import__(m)
            py[m] = True
        except Exception:  # noqa: BLE001
            py[m] = False
    return {"tools": out, "python": py,
            "ready_options": [o["id"] for o in OPTIONS if all(out.get(t, {}).get("present") for t in o["needs"])]}


def team():
    return json.loads(TEAM.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ intake
def probe(media: Path) -> dict:
    need("ffprobe")
    rc, out, err = sh(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(media)], 120)
    if rc:
        raise SystemExit("ffprobe failed: " + err[-300:])
    d = json.loads(out)
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video" and s.get("disposition", {}).get("attached_pic") != 1), None)
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
    fps = None
    if v and v.get("avg_frame_rate", "0/0") != "0/0":
        n, dd = v["avg_frame_rate"].split("/")
        fps = round(float(n) / float(dd), 3) if float(dd) else None
    return {"duration": round(float(d["format"].get("duration", 0)), 3), "size_bytes": int(d["format"].get("size", 0)),
            "container": d["format"].get("format_name"),
            "video": {"codec": v.get("codec_name"), "width": v.get("width"), "height": v.get("height"), "fps": fps} if v else None,
            "audio": {"codec": a.get("codec_name"), "sample_rate": int(a.get("sample_rate", 0)), "channels": a.get("channels")} if a else None}


def loudness(media: Path) -> dict:
    rc, out, err = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", str(media), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], 900)
    tail = err[err.rfind("Summary:"):] if "Summary:" in err else ""
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return {"integrated_lufs": float(i.group(1)) if i else None, "true_peak_dbfs": float(tp.group(1)) if tp else None}


def intake(media: Path, job: Path) -> dict:
    need("ffmpeg")
    media = media.resolve()
    if not media.is_file():
        raise SystemExit(f"no such file: {media}")
    job.mkdir(parents=True, exist_ok=True)
    info = probe(media)
    kind = "video" if info["video"] else ("audio" if info["audio"] else "unknown")
    res = {"source": str(media), "sha256": sha256(media), "kind": kind, "probe": info,
           "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if info["audio"]:
        wav = job / "work" / "master.wav"
        wav.parent.mkdir(parents=True, exist_ok=True)
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(media), "-vn", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(wav)], 900)
        res["loudness"] = loudness(media)
        cues = job / "work" / "cues.json"
        words = job / "words.json"
        cmd = [PY, str(HERE / "audio_cue_mapper.py"), str(wav), "--out", str(cues)]
        if words.exists():
            cmd[3:3] = ["--aligned-words", str(words)]
        rc, out, err = sh(cmd, 900)
        c = jload(cues, {}) or {}
        res["audio_cues"] = {"file": str(cues), "onset_candidates": len(c.get("onset_candidates_seconds") or []),
                             "aligned_words": len(c.get("words") or []), "ok": rc == 0}
        if not words.exists():
            res["words_hint"] = "no words.json: put WhisperX/faster-whisper aligned words at JOB/words.json for word-synced text"
    if kind == "video":
        cuts = job / "work" / "cuts.json"
        rc, out, err = sh([PY, str(HERE / "motion_reference_probe.py"), str(media), "--cuts", "--out", str(cuts)], 1800)
        c = jload(cuts, {}) or {}
        res["cuts"] = {"file": str(cuts), "count": len(c.get("cut_candidates_seconds") or []), "seconds": c.get("cut_candidates_seconds") or [], "ok": rc == 0}
        sheet = job / "work" / "contact.jpg"
        n = 12
        step = max(info["duration"] / n, 0.5)
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(media), "-vf", f"fps=1/{step:.3f},scale=320:-2,tile=4x3", "-frames:v", "1", str(sheet)], 600)
        res["contact_sheet"] = str(sheet) if sheet.exists() else None
    jsave(job / "intake.json", res)
    report(job, "intake", {"kind": kind, "duration": info["duration"], "sha256": res["sha256"]})
    return res


# ------------------------------------------------------------------ options
OPTIONS = [
    {"id": "kinetic-film", "for": ["audio", "video"], "ar": "فيلم موشن جرافيك على الصوت (كلمات متحركة ورسم ومشاهد)",
     "en": "Motion-graphics film on the audio (kinetic text, draw-on, camera)", "team": ["director", "analyst", "writer", "motion", "render", "qa"],
     "needs": ["ffmpeg", "node"], "runs": True, "styles": ["auto", "kinetic", "doodle", "cinematic"],
     "pipeline": "audio_cue_mapper → creative_reasoning_bridge → motion_director compile → render (master audio) → verify_video"},
    {"id": "visualizer", "for": ["audio", "video"], "ar": "مُصوِّر صوتي (موجة/طيف) بعنوان وخلفية متدرجة",
     "en": "Audio visualizer (wave/spectrum) with title", "team": ["analyst", "motion", "render", "qa"],
     "needs": ["ffmpeg"], "runs": True, "styles": ["wave", "spectrum", "circle"],
     "pipeline": "ffmpeg showwaves/showspectrum + gradient + drawtext → verify_video"},
    {"id": "reframe", "for": ["video"], "ar": "إعادة تأطير 9:16 بخلفية مموهة لكل المنصات",
     "en": "Vertical 9:16 reframe with blurred backdrop", "team": ["editor", "conformer", "render", "qa"],
     "needs": ["ffmpeg"], "runs": True, "styles": ["9:16", "1:1", "4:5"],
     "pipeline": "ffmpeg split → blurred cover + fitted foreground → verify_video"},
    {"id": "highlight-reel", "for": ["video"], "ar": "ريل مختصر من أقوى اللقطات (قطعات وطاقة الصوت)",
     "en": "Highlight reel from the strongest shots (cuts + audio energy)", "team": ["analyst", "editor", "render", "qa"],
     "needs": ["ffmpeg"], "runs": True, "styles": ["15", "30", "60"],
     "pipeline": "measured cuts + RMS energy → top segments → concat with short crossfades → verify_video"},
    {"id": "look", "for": ["video"], "ar": "لوك سينمائي: تلوين وتباين وحبيبات وتعتيم أطراف",
     "en": "Cinematic look: grade, contrast, grain, vignette", "team": ["colorist", "render", "qa"],
     "needs": ["ffmpeg"], "runs": True, "styles": ["teal-orange", "warm", "mono", "film"],
     "pipeline": "ffmpeg eq/colorbalance/curves/noise/vignette → verify_video + before/after frames"},
    {"id": "reference-remix", "for": ["video"], "ar": "مشروع Remotion يعيد إيقاع مونتاج الفيديو بلقطاتك",
     "en": "Remotion project that re-uses this video's edit rhythm with your clips", "team": ["analyst", "editor", "motion"],
     "needs": ["ffmpeg"], "runs": True, "styles": ["30"],
     "pipeline": "motion_reference_probe cuts + audio cues → reference_edit_engine → editable Remotion project (npm install to render)"},
    {"id": "broll-documentary", "for": ["audio", "video"], "ar": "مونتاج وثائقي بلقطات حقيقية مرخصة على الكلام",
     "en": "Documentary B-roll edit on narration (licensed real footage)", "team": ["acquirer", "conformer", "editor", "render", "qa"],
     "needs": ["ffmpeg"], "runs": False, "styles": [],
     "pipeline": "acquire (rights.json) → convert → cinematic_cut_planner (words.json + clips) → cinematic_broll_render → verify_video",
     "inputs": "words.json (aligned transcript) and ≥3 licensed clips in JOB/footage"},
    {"id": "character", "for": ["audio"], "ar": "شخصية مرسومة تتحرك وتشير على كلمات الصوت",
     "en": "Drawn character that gestures on spoken words", "team": ["illustrator", "motion", "render", "qa"],
     "needs": ["ffmpeg"], "runs": False, "styles": [],
     "pipeline": "character_fullbody.py render --scene … --words JOB/words.json → verify_video",
     "inputs": "words.json with real timings"},
    {"id": "3d-scene", "for": ["audio", "video"], "ar": "مشهد ثلاثي الأبعاد بحركة كاميرا",
     "en": "3D scene with camera move", "team": ["3d", "render", "qa"], "needs": ["ffmpeg"], "runs": False, "styles": [],
     "pipeline": "native_3d.py render (or blender_cinema.py when Blender is installed) → mux master audio → verify_video",
     "inputs": "a scene JSON (templates/native-3d-demo.json is a start)"},
]


def options(job: Path, brief: str = "") -> dict:
    it = jload(job / "intake.json")
    if not it:
        raise SystemExit("run intake first")
    doc = doctor()
    present = {k for k, v in doc["tools"].items() if v["present"]}
    menu = []
    for o in OPTIONS:
        if it["kind"] not in o["for"]:
            continue
        missing = [t for t in o["needs"] if t not in present]
        menu.append({**o, "missing": missing, "status": "ready" if (o["runs"] and not missing) else ("needs-inputs" if not missing else "install"),
                     "command": f"python3 scripts/montage_pro.py build {job} --option {o['id']}" + (f" --style {o['styles'][0]}" if o["styles"] else "")})
    plan = None
    try:
        rc, out, err = sh([PY, str(HERE / "capability_mindmap.py"), "task", brief or ("مونتاج وموشن جرافيك لملف " + it["kind"])], 120)
        plan = out.strip()
    except Exception:  # noqa: BLE001
        pass
    res = {"kind": it["kind"], "duration": it["probe"]["duration"], "menu": menu, "stage_plan": plan}
    jsave(job / "options.json", res)
    return res


# ------------------------------------------------------------------ acquire (IDM-style desk)
def acquire(url: str, job: Path, licence: str, source_page: str, owner: bool, parts: int = 6) -> dict:
    if not (licence or owner):
        raise SystemExit("refusing: give --license \"<licence of this exact asset>\" and --source-page, or --owner for your own media")
    u = urlsplit(url)
    if u.scheme not in ("http", "https"):
        raise SystemExit("only http(s) URLs")
    dest = job / "footage"
    dest.mkdir(parents=True, exist_ok=True)
    host = (u.hostname or "").lower()
    stream = any(host == h or host.endswith("." + h) for h in STREAM_HOSTS) or u.path.lower().endswith((".m3u8", ".mpd"))
    before = {p.name for p in dest.iterdir()}
    if stream:
        route = "stream-grab (yt-dlp/ffmpeg via fetch_video.py; HLS/DASH segments merged, edit-safe H.264/AAC)"
        rc, out, err = sh([PY, str(HERE / "fetch_video.py"), url, "-o", str(dest), "--quality", "1080"], 3600)
    else:
        name = Path(u.path).name or "download.bin"
        name = re.sub(r"[^\w.\-]+", "_", name)[:120]
        route = f"segmented resumable download ({parts} ranges, .part resume, sha256) via app_studio.py download"
        rc, out, err = sh([PY, str(HERE / "app_studio.py"), "download", url, "-o", str(dest / name), "--set", f"parts={parts}"], 3600)
    new = [p for p in dest.iterdir() if p.name not in before and p.is_file() and not p.name.endswith(".part")]
    rights = jload(job / "rights.json", []) or []
    for p in new:
        rights.append({"file": str(p.relative_to(job)), "url": url, "source_page": source_page or url, "licence": licence or "owner-supplied",
                       "owner": owner, "sha256": sha256(p), "bytes": p.stat().st_size, "route": route,
                       "acquired_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    jsave(job / "rights.json", rights)
    res = {"route": route, "exit": rc, "files": [str(p) for p in new], "stderr_tail": (err or "")[-400:]}
    report(job, "acquire:" + url[:80], {"exit": rc, "files": len(new)})
    return res


# ------------------------------------------------------------------ convert (mezzanine + proxies)
def convert(job: Path, fps: int = 30) -> dict:
    need("ffmpeg")
    src = job / "footage"
    mez, prox = job / "mezzanine", job / "proxies"
    mez.mkdir(parents=True, exist_ok=True)
    prox.mkdir(parents=True, exist_ok=True)
    done = []
    for p in sorted(src.glob("*")) if src.is_dir() else []:
        if not p.is_file() or p.suffix.lower() not in (".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi", ".gif"):
            continue
        m = mez / (p.stem + ".mp4")
        rc, _, err = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-vf", f"fps={fps},format=yuv420p,scale=trunc(iw/2)*2:trunc(ih/2)*2",
                         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
                         "-movflags", "+faststart", str(m)], 3600)
        if rc == 0:
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(m), "-vf", "scale=-2:540", "-c:v", "libx264", "-crf", "28", "-preset", "veryfast",
                "-c:a", "aac", "-b:a", "96k", str(prox / (p.stem + "_540p.mp4"))], 3600)
        done.append({"source": p.name, "mezzanine": m.name if rc == 0 else None, "ok": rc == 0, "err": err[-200:] if rc else ""})
    report(job, "convert", done)
    return {"converted": done, "fps": fps}


# ------------------------------------------------------------------ build
def verify(job: Path, out: Path, aspect=None, master=None) -> dict:
    cmd = [PY, str(HERE / "verify_video.py"), str(out), "--json", str(job / "work" / (out.stem + ".verify.json"))]
    if aspect:
        cmd += ["--aspect", aspect]
    if master:
        cmd += ["--audio", str(master)]
    rc, o, e = sh(cmd, 900)
    lines = [l for l in o.splitlines() if l.startswith("[")]
    return {"exit": rc, "checks": lines[-12:], "summary": (o.strip().splitlines() or [""])[-1]}


def master_audio(job: Path) -> Path:
    it = jload(job / "intake.json")
    if not it:
        raise SystemExit("run intake first")
    return Path(it["source"])


def deliver_mix(job: Path, out: Path) -> dict:
    """Sound designer: a separate -14 LUFS delivery copy; the master and the first render stay untouched."""
    dst = out.with_name(out.stem + "-deliver-14lufs.mp4")
    rc, so, se = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                     "-ar", "48000", "-c:a", "aac", "-b:a", "192k", str(dst)], 3600)
    if rc:
        return {"status": "failed", "stderr": se[-300:]}
    return {"output": str(dst), "verify": verify(job, dst)}


def build(job: Path, option: str, style: str = None, title: str = "", deliver: bool = False) -> dict:
    need("ffmpeg")
    it = jload(job / "intake.json")
    if not it:
        raise SystemExit("run intake first")
    src = Path(it["source"])
    if sha256(src) != it["sha256"]:
        raise SystemExit("the source changed since intake; run intake again")
    outd = job / "out"
    outd.mkdir(parents=True, exist_ok=True)
    work = job / "work"
    dur = it["probe"]["duration"]
    o = next((x for x in OPTIONS if x["id"] == option), None)
    if not o:
        raise SystemExit("unknown option; see montage_pro.py options JOB")
    if not o["runs"]:
        return {"option": option, "status": "needs-inputs", "pipeline": o["pipeline"], "inputs": o.get("inputs")}
    style = style or (o["styles"][0] if o["styles"] else None)
    out = outd / f"{option}-{(style or 'default').replace(':', 'x')}.mp4"
    ttl = (title or "").replace(":", r"\:").replace("'", "")
    font = next((str(p) for p in (SKILL.parents[2] / "fonts").rglob("*.ttf")), None) if (SKILL.parents[2] / "fonts").is_dir() else None
    draw = (f",drawtext=text='{ttl}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=h*0.12" + (f":fontfile='{font}'" if font else "")) if ttl else ""
    res = {"option": option, "style": style, "output": str(out)}
    if option == "kinetic-film":
        cues = work / "cues.json"
        scene, dec, html = work / "scene.json", work / "decisions.json", work / "film.html"
        st = style if style in ("kinetic", "doodle", "cinematic") else "auto"
        steps = [[PY, str(HERE / "creative_reasoning_bridge.py"), str(cues), "--style", st, "--out", str(scene), "--report", str(dec)],
                 [PY, str(HERE / "motion_director.py"), "compile", str(scene), "--out", str(html)],
                 [PY, str(HERE / "motion_director.py"), "render", str(html), "--out", str(out), "--audio", str(work / "master.wav")]]
        for c in steps:
            if c[-1] == str(out) and out.exists():
                out.unlink()
            rc, so, se = sh(c, 3600)
            if rc:
                return {**res, "status": "failed", "step": " ".join(Path(x).name for x in c[:3]), "stderr": (se or so)[-500:]}
        res["editable_source"] = str(html)
        res["verify"] = verify(job, out, master=work / "master.wav")
    elif option == "visualizer":
        w, h = 1080, 1920
        vis = {"wave": f"showwaves=s={w}x600:mode=cline:colors=0x8be9fd|0xff79c6:rate=30",
               "spectrum": f"showfreqs=s={w}x600:mode=bar:colors=0x8be9fd|0xff79c6:fscale=log",
               "circle": f"avectorscope=s=900x900:zoom=1.5:draw=line:rc=139:gc=233:bc=253"}[style if style in ("wave", "spectrum", "circle") else "wave"]
        fc = (f"color=c=0x0b1020:s={w}x{h}:d={dur:.3f},geq=r='11+40*Y/H':g='16+10*Y/H':b='32+60*Y/H',format=yuv420p[bg];"
              f"[0:a]{vis},format=rgba[v];[bg][v]overlay=(W-w)/2:(H-h)/2:shortest=1{draw},format=yuv420p[o]")
        rc, so, se = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-filter_complex", fc, "-map", "[o]", "-map", "0:a",
                         "-r", "30", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], 3600)
        if rc:
            return {**res, "status": "failed", "stderr": se[-500:]}
        res["verify"] = verify(job, out, aspect="9:16", master=work / "master.wav")
    elif option == "reframe":
        aw, ah = {"9:16": (1080, 1920), "1:1": (1080, 1080), "4:5": (1080, 1350)}.get(style, (1080, 1920))
        fc = (f"[0:v]split[a][b];[a]scale={aw}:{ah}:force_original_aspect_ratio=increase,crop={aw}:{ah},boxblur=30:2,eq=brightness=-0.08[bg];"
              f"[b]scale={aw}:{ah}:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2{draw},format=yuv420p[o]")
        rc, so, se = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-filter_complex", fc, "-map", "[o]", "-map", "0:a?",
                         "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "192k", str(out)], 3600)
        if rc:
            return {**res, "status": "failed", "stderr": se[-500:]}
        res["verify"] = verify(job, out, aspect=style or "9:16")
    elif option == "highlight-reel":
        target = float(style or 30)
        segs = highlight_segments(it, work, target)
        if not segs:
            return {**res, "status": "failed", "stderr": "no segments"}
        parts = []
        for k, (a, b) in enumerate(segs):
            p = work / f"seg{k:02d}.mp4"
            sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(src), "-vf", "fps=30,format=yuv420p",
                "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-ar", "48000", str(p)], 1800)
            parts.append(p)
        lst = work / "concat.txt"
        lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
        rc, so, se = sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)], 1800)
        if rc:
            return {**res, "status": "failed", "stderr": se[-500:]}
        res["segments"] = [[round(a, 2), round(b, 2)] for a, b in segs]
        res["verify"] = verify(job, out)
    elif option == "look":
        looks = {"teal-orange": "colorbalance=rs=-0.08:bs=0.10:rh=0.10:bh=-0.08,eq=contrast=1.08:saturation=1.1",
                 "warm": "colortemperature=temperature=5200,eq=contrast=1.05:saturation=1.05",
                 "mono": "hue=s=0,eq=contrast=1.15",
                 "film": "curves=preset=increase_contrast,eq=saturation=0.92"}
        vf = looks.get(style, looks["teal-orange"]) + ",noise=alls=6:allf=t,vignette=PI/5,format=yuv420p" + draw
        rc, so, se = sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", vf, "-c:v", "libx264", "-crf", "18", "-c:a", "copy", str(out)], 3600)
        if rc:
            return {**res, "status": "failed", "stderr": se[-500:]}
        mid = max(dur / 2, 0)
        for tag, f in (("before", str(src)), ("after", str(out))):
            sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{mid:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=540:-2", str(outd / f"look-{tag}.jpg")], 300)
        res["frames"] = [str(outd / "look-before.jpg"), str(outd / "look-after.jpg")]
        res["verify"] = verify(job, out)
    elif option == "reference-remix":
        proj = outd / "remotion-project"
        if proj.exists():
            shutil.rmtree(proj)
        rc, so, se = sh([PY, str(HERE / "reference_edit_engine.py"), "--probe", str(work / "cuts.json"), "--cues", str(work / "cues.json"),
                         "--fps", "30", "--out", str(proj)], 1800)
        res = {**res, "output": str(proj), "next": "cd remotion-project && npm install && npm run render (Remotion licence applies)"}
        if rc:
            return {**res, "status": "failed", "stderr": (se or so)[-500:]}
    if deliver and option != "reference-remix" and Path(res["output"]).exists():
        res["delivery_mix"] = deliver_mix(job, Path(res["output"]))
    master_now = sha256(src)
    res["master_unchanged"] = master_now == it["sha256"]
    res["status"] = "rendered" if (option == "reference-remix" or Path(res["output"]).exists()) else "failed"
    report(job, "build:" + option + ":" + str(style), {k: res[k] for k in ("status", "output", "master_unchanged")})
    return res


def highlight_segments(it, work: Path, target: float):
    dur = it["probe"]["duration"]
    cuts = jload(work / "cuts.json", {}) or {}
    marks = sorted({0.0, dur} | {float(c) for c in (cuts.get("cut_candidates_seconds") or []) if 0 < float(c) < dur})
    shots = [(a, b) for a, b in zip(marks, marks[1:]) if b - a >= 0.8]
    if len(shots) < 2:  # no cuts measured: split into even windows
        n = max(2, int(dur // 4))
        shots = [(dur * k / n, dur * (k + 1) / n) for k in range(n)]
    cues = jload(work / "cues.json", {}) or {}
    env = cues.get("energy_rms") or []
    win = float(cues.get("window_seconds") or 0.05)
    per = max(0.8, min(4.0, target / max(1, len(shots))))

    def energy(a, b):
        vals = env[int(a / win):max(int(a / win) + 1, int(b / win))]
        return sum(vals) / len(vals) if vals else 0.0
    ranked = sorted(shots, key=lambda s: -energy(*s))
    pick, total = [], 0.0
    for a, b in ranked:
        seg = (a, min(b, a + per))
        if total + (seg[1] - seg[0]) > target + 0.5:
            continue
        pick.append(seg)
        total += seg[1] - seg[0]
        if total >= target - 0.5:
            break
    return sorted(pick)


# ------------------------------------------------------------------ CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    sub.add_parser("team")
    i = sub.add_parser("intake"); i.add_argument("media", type=Path); i.add_argument("--job", type=Path, required=True)
    o = sub.add_parser("options"); o.add_argument("job", type=Path); o.add_argument("--brief", default="")
    a = sub.add_parser("acquire"); a.add_argument("url"); a.add_argument("--job", type=Path, required=True)
    a.add_argument("--license", default=""); a.add_argument("--source-page", default=""); a.add_argument("--owner", action="store_true")
    a.add_argument("--parts", type=int, default=6)
    c = sub.add_parser("convert"); c.add_argument("job", type=Path); c.add_argument("--fps", type=int, default=30)
    b = sub.add_parser("build"); b.add_argument("job", type=Path); b.add_argument("--option", required=True)
    b.add_argument("--style"); b.add_argument("--title", default="")
    b.add_argument("--deliver-mix", action="store_true", help="also write a -14 LUFS delivery copy (master untouched)")
    x = ap.parse_args(argv)
    if x.cmd == "doctor":
        r = doctor()
        for k, v in r["tools"].items():
            print(f"  {'✅' if v['present'] else '❌'} {k:<9} {v['role']}")
        print("  python: " + " ".join(f"{k}{'✅' if v else '❌'}" for k, v in r["python"].items()))
        print("  ready options: " + ", ".join(r["ready_options"]))
        return 0
    if x.cmd == "team":
        t = team()
        print(t["name"])
        for r in t["roles"]:
            print(f"  [{r['id']}] {r['ar']} — {r['en']}\n      {r['mission']}\n      tools: {', '.join(r['scripts'])} · gate: {r['gate']}")
        return 0
    if x.cmd == "intake":
        r = intake(x.media, x.job)
        print(json.dumps({k: r[k] for k in r if k not in ("source",)}, ensure_ascii=False, indent=1))
        return 0
    if x.cmd == "options":
        r = options(x.job, x.brief)
        print(f"{r['kind']} · {r['duration']} s — option menu:")
        for m in r["menu"]:
            badge = {"ready": "✅", "needs-inputs": "🧩", "install": "📦"}[m["status"]]
            print(f"  {badge} {m['id']:<18} {m['ar']} — {m['en']}\n      team: {', '.join(m['team'])} · {m['pipeline']}")
            print(f"      run: {m['command']}" + (f"  (needs: {m.get('inputs')})" if m["status"] == "needs-inputs" else "") + (f"  (missing: {', '.join(m['missing'])})" if m["missing"] else ""))
        if r["stage_plan"]:
            print("\nstage plan (mind map):\n" + r["stage_plan"])
        return 0
    if x.cmd == "acquire":
        print(json.dumps(acquire(x.url, x.job, x.license, x.source_page, x.owner, x.parts), ensure_ascii=False, indent=1))
        return 0
    if x.cmd == "convert":
        print(json.dumps(convert(x.job, x.fps), ensure_ascii=False, indent=1))
        return 0
    if x.cmd == "build":
        r = build(x.job, x.option, x.style, x.title, x.deliver_mix)
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0 if r.get("status") in ("rendered", "needs-inputs") else 1


if __name__ == "__main__":
    raise SystemExit(main())
