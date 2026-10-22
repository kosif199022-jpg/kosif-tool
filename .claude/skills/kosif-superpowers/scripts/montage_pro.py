#!/usr/bin/env python3
"""Montage Pro — فريق مهمة المونتاج والموشن والـ3D داخل KOSIF Superpowers.

Upload an audio or a video, get a team, a menu of strong options, and a real render.

  python3 montage_pro.py doctor                                  # tools present/missing for the team
  python3 montage_pro.py team                                    # the 13 roles, their scripts and gates
  python3 montage_pro.py intake MEDIA --job JOB [--transcribe]   # analyst: measure the file (ffprobe, loudness, energy cues, cuts)
                                                                 # --transcribe (opt-in, takes the transcribe options) writes
                                                                 # JOB/words.json after probing, before the cue mapper imports it
  python3 montage_pro.py transcribe MEDIA --job JOB [--model medium] [--language ar|auto] [--local-only] [--force] [--out PATH]
                                    [--no-vad] [--no-speech-threshold 0.6] [--allow-tracked]
                                                                 # transcriber: faster-whisper word timings → JOB/words.json (kosif-words/1);
                                                                 # Silero VAD + no_speech_prob drop silence/music guesses; times are on the
                                                                 # file timeline (audio start offset added); refuses jobs/, git-tracked or
                                                                 # unignored repo paths (use out/…) unless --allow-tracked
  python3 montage_pro.py options JOB [--brief "..."]             # director: option menu for this material + stage plan
  python3 montage_pro.py acquire URL --job JOB --license "CC0 / owner / …" --source-page URL [--owner]
                                                                 # IDM-style desk: segmented resumable file download, DASH/HLS manifest grab
                                                                 # (stream_grabber.py), or page grab (yt-dlp) + rights.json
  python3 montage_pro.py convert JOB                             # conformer: edit-ready mezzanine (CFR H.264/AAC 48k) + 540p proxies
  python3 montage_pro.py build JOB --option ID [--style …]       # editor/motion/render/QA: produce and verify the chosen option

Every output is verified with verify_video.py; results land in JOB/report.json. The user's master audio is never
modified (its SHA-256 is recorded and re-checked). Nothing is downloaded without a licence note.
Python 3.8+ stdlib; uses ffmpeg/ffprobe, node+Chromium (HTML scenes) and yt-dlp when present; transcribe also needs
faster-whisper (pip install faster-whisper, numpy comes with it), imported only by that command.
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


def intake(media: Path, job: Path, transcribe_opts: dict = None) -> dict:
    """Measure MEDIA into JOB. transcribe_opts (opt-in, e.g. {"model": "medium", "language": "ar"}) first writes
    JOB/words.json with `transcribe` so the cue mapper below imports the aligned words; None keeps the old intake."""
    need("ffmpeg")
    media = media.resolve()
    if not media.is_file():
        raise SystemExit(f"no such file: {media}")
    job.mkdir(parents=True, exist_ok=True)
    info = probe(media)
    kind = "video" if info["video"] else ("audio" if info["audio"] else "unknown")
    res = {"source": str(media), "sha256": sha256(media), "kind": kind, "probe": info,
           "measured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    if transcribe_opts is not None:
        res["transcribe"] = (transcribe_job(media, job, job / "words.json", **transcribe_opts) if info["audio"]
                             else {"ok": False, "error": "no audio stream to transcribe"})
    if info["audio"]:
        wav = job / "work" / "master.wav"
        wav.parent.mkdir(parents=True, exist_ok=True)
        # master.wav sits on the file timeline: when the audio stream starts late (a video whose sound begins after
        # frame 0) the lead-in is padded with silence, so words.json (file timeline) and the cue map line up.
        offset = (res.get("transcribe") or {}).get("audio_offset") or (media_timing(media)[1] if info["video"] else 0.0)
        pad = ["-af", f"adelay={int(round(offset * 1000))}:all=1"] if offset and offset > 0.0005 else []
        sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(media), "-vn", *pad, "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(wav)], 900)
        res["loudness"] = loudness(media)
        cues = job / "work" / "cues.json"
        words = job / "words.json"
        if cues.exists():  # the mapper opens its output exclusively; a stale map must not survive a re-intake
            cues.unlink()
        cmd = [PY, str(HERE / "audio_cue_mapper.py"), str(wav), "--out", str(cues)]
        if words.exists():
            cmd[3:3] = ["--aligned-words", str(words)]
        rc, out, err = sh(cmd, 900)
        c = jload(cues, {}) or {}
        res["audio_cues"] = {"file": str(cues), "onset_candidates": len(c.get("onset_candidates_seconds") or []),
                             "aligned_words": len(c.get("words") or []), "ok": rc == 0}
        if offset and offset > 0.0005:
            res["audio_cues"]["audio_offset"] = round(offset, 3)
        if transcribe_opts is not None and (res.get("transcribe") or {}).get("ok") and words.exists() and not res["audio_cues"]["aligned_words"]:
            res["warning"] = ("transcribed words were not imported into the cue map: " + (err or out).strip().splitlines()[-1]
                              if (err or out).strip() else "transcribed words were not imported into the cue map")
        if not words.exists():
            res["words_hint"] = ("no words.json: run montage_pro.py transcribe MEDIA --job JOB (or intake --transcribe), "
                                 "or put WhisperX/faster-whisper aligned words at JOB/words.json for word-synced text")
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


# ------------------------------------------------------------------ transcribe (word timings → words.json, schema kosif-words/1)
WORDS_SCHEMA = "kosif-words/1"
FAKE_ENV = "KOSIF_TRANSCRIBE_FAKE"  # test hook: a JSON file {"segments": [...], "language": "ar"} replaces the model
WRITERS = ("faster-whisper", "fake")  # engine names this command writes (the fake hook never passes for a real run)
NO_SPEECH_MAX = 0.6  # whisper's own no_speech_threshold: a segment above it is dropped as non-speech (silence/music)
REPO = SKILL.parents[2]


class TranscribeError(Exception):
    """A clean one-line transcription failure: the CLI prints it on stderr and exits 2."""


def _one_line(exc) -> str:
    return (type(exc).__name__ + ": " + (str(exc).strip().splitlines() or [""])[0])[:200]


def _field(o, key, default=None):
    return o.get(key, default) if isinstance(o, dict) else getattr(o, key, default)


def _num(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def _fw_version():
    """Installed faster-whisper version from package metadata (no import), or None."""
    try:
        from importlib.metadata import version
        return version("faster-whisper")
    except Exception:  # noqa: BLE001 - not installed or no metadata
        return None


def target_problem(path: Path):
    """Why transcribe must not write PATH, or None. Same rule as reel_factory.out_problem: generated transcripts
    belong under out/ (git-ignored), never inside jobs/, a file tracked by git or an unignored repository path."""
    p = Path(path).resolve()
    try:
        p.relative_to(SKILL)
        return f"{p} is inside the skill folder {SKILL} (its files ship with the skill; transcripts go under <repo>/out/…)"
    except ValueError:
        pass
    try:
        in_repo = p.relative_to(REPO).parts
    except ValueError:
        in_repo = None
    jobs = f"{p} is inside jobs/ (job folders are tracked sources; transcripts go under out/)"
    if in_repo and in_repo[0] == "jobs":
        return jobs
    unchecked = f"{p} is inside this repository and git cannot check it (use out/…)" if in_repo is not None and in_repo[:1] != ("out",) else None
    anc = p.parent
    while not anc.exists() and anc != anc.parent:
        anc = anc.parent
    if not shutil.which("git"):
        return unchecked
    try:
        rc, top, _ = sh(["git", "-C", str(anc), "rev-parse", "--show-toplevel"], 30)
        if rc:
            return unchecked  # not inside a git work tree
        top = Path(top.strip()).resolve()
        rel = p.relative_to(top)
        if rel.parts[:1] == ("jobs",):
            return jobs
        _, files, _ = sh(["git", "--literal-pathspecs", "-C", str(top), "ls-files", "--", rel.as_posix()], 60)
        if files.strip():
            return f"{p} is tracked by git"
        rc, _, _ = sh(["git", "-C", str(top), "check-ignore", "-q", rel.as_posix()], 30)
    except ValueError:
        return None
    except (OSError, subprocess.SubprocessError):
        return unchecked
    return f"{p} is inside a git repository but not git-ignored (use out/…)" if rc == 1 else None


def guard_targets(paths, allow_tracked: bool = False):
    """TranscribeError for the first PATH that target_problem refuses, unless allow_tracked."""
    for p in [] if allow_tracked else paths:
        why = target_problem(p)
        if why:
            raise TranscribeError(f"refusing to write {Path(p).name}: {why}; pass --allow-tracked to override")


def media_timing(media: Path):
    """(container duration, audio offset) in seconds via ffprobe. The offset is where the first audio sample sits on the
    file timeline (audio stream start_time minus the container start_time, e.g. 0.776 s for a video whose audio starts
    late); the decoded samples start there, so word times get it added. (None, 0.0) when ffprobe is missing or fails."""
    if not shutil.which("ffprobe"):
        return None, 0.0
    try:
        rc, out, _ = sh(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "format=duration,start_time:stream=start_time",
                         "-of", "json", str(media)], 120)
        d = json.loads(out) if rc == 0 else {}
    except (OSError, subprocess.SubprocessError, ValueError):
        return None, 0.0
    fmt, st = d.get("format") or {}, (d.get("streams") or [{}])[0]
    dur, a0, f0 = _num(fmt.get("duration")), _num(st.get("start_time")), _num(fmt.get("start_time"))
    off = max(0.0, a0 - (f0 or 0.0)) if a0 is not None else 0.0
    return (dur if dur and dur > 0 else None), off


def media_duration(media: Path):
    """Container duration in seconds via ffprobe, or None when ffprobe is missing or cannot read the file."""
    return media_timing(media)[0]


def decode_16k(media: Path, timeout: int = 3600):
    """ffmpeg → mono 16 kHz float32 through a pipe (no PyAV: avoids the av 19 + faster-whisper 1.2.1 metadata_errors TypeError).
    Sample 0 is the first audio sample, i.e. media_timing()'s offset on the file timeline."""
    try:
        import numpy as np  # lazy: only transcribe needs numpy
    except Exception as exc:  # noqa: BLE001 - a broken numpy raises more than ImportError
        raise TranscribeError(f"numpy cannot be imported: {_one_line(exc)} (pip install faster-whisper)") from None
    try:
        r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(media), "-vn", "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                           capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise TranscribeError(f"decoding {media.name} timed out after {timeout} s") from None
    except OSError as exc:
        raise TranscribeError(f"cannot run ffmpeg: {_one_line(exc)}") from None
    if r.returncode or len(r.stdout) < 4:
        tail = (r.stderr.decode("utf-8", "replace").strip().splitlines() or ["no audio stream"])[-1]
        raise TranscribeError(f"cannot decode {media.name}: {tail[:200]}")
    return np.frombuffer(r.stdout[:len(r.stdout) // 4 * 4], dtype=np.float32)


def tidy_words(segments, limit=None, offset=0.0):
    """Whisper segments → (words, phrases) for kosif-words/1. `offset` seconds are added to every time (file timeline).
    Words are stripped (empty ones dropped), kept in segment order (segments by their first word, words by start inside a
    segment, so a phrase is always one contiguous index range), timed in whole milliseconds (3 decimals), starts strictly
    increasing (a word that starts before the previous one moves 1 ms after it), each end clamped to the next start and to
    `limit` seconds, so every word keeps a positive length. One phrase per segment that kept words, with the inclusive word
    index range; its text is the segment text, or the kept words when any timed word was dropped (limit or bad times)."""
    groups = []
    for si, seg in enumerate(segments):
        rows, lost = [], False
        for w in _field(seg, "words") or []:
            text = str(_field(w, "word", "") or "").strip()
            s, e = _num(_field(w, "start")), _num(_field(w, "end"))
            if not text:
                continue
            if s is None or e is None:
                lost = True
                continue
            p = _field(w, "probability", _field(w, "prob"))
            rows.append([int(round(max(0.0, s + offset) * 1000)), int(round(max(0.0, e + offset) * 1000)), text, p])
        if rows:
            rows.sort(key=lambda r: (r[0], r[1]))
            groups.append((rows[0][0], si, rows, lost))
    groups.sort(key=lambda g: (g[0], g[1]))
    flat = [(r, gi) for gi, g in enumerate(groups) for r in g[2]]
    for k in range(1, len(flat)):
        flat[k][0][0] = max(flat[k][0][0], flat[k - 1][0][0] + 1)
    lim = None if limit is None else int(math.floor(limit * 1000 + 1e-6))
    if lim is not None:
        flat = [f for f in flat if f[0][0] < lim]  # past the end of the audio (starts increase, so this cuts a tail)
    words, members = [], {}
    for k, ((s, e, text, p), gi) in enumerate(flat):
        nxt = flat[k + 1][0][0] if k + 1 < len(flat) else lim
        e = max(e, s + 1) if nxt is None else min(max(e, s + 1), nxt)
        w = {"word": text, "start": round(s / 1000, 3), "end": round(e / 1000, 3)}
        if _num(p) is not None:
            w["prob"] = round(float(p), 3)
        words.append(w)
        members.setdefault(gi, []).append(k)
    phrases = []
    for gi, (_, si, rows, lost) in enumerate(groups):
        idx = members.get(gi)
        if not idx:
            continue
        a, b = idx[0], idx[-1]
        seg = segments[si]
        text = "" if lost or len(idx) < len(rows) else str(_field(seg, "text", "") or "").strip()
        ph = {"text": text or " ".join(words[i]["word"] for i in range(a, b + 1)), "start": words[a]["start"], "end": words[b]["end"],
              "words": [a, b]}
        for key in ("no_speech_prob", "avg_logprob"):  # whisper's own confidence, so a reader can tell speech from a guess
            v = _num(_field(seg, key))
            if v is not None:
                ph[key] = round(v, 3)
        phrases.append(ph)
    return words, phrases


def transcribe(media: Path, out: Path, model: str = "medium", language: str = "ar", local_only: bool = False,
               force: bool = False, vad: bool = True, no_speech_threshold: float = NO_SPEECH_MAX, allow_tracked: bool = False) -> dict:
    """Write word timings for MEDIA to OUT (kosif-words/1). Skips when OUT already holds the same source sha256, model,
    engine (name, version, vad, threshold) and language (unless "auto") unless force. Silero VAD (vad) keeps silence and
    music out of the model, and segments whose no_speech_prob exceeds no_speech_threshold are dropped (listed in
    dropped_segments and a warning), so Whisper's "subscribe to the channel" guesses never become captions. OUT must
    not be inside jobs/, tracked by git or an unignored repository path unless allow_tracked. The file holds no clock
    time, so a rerun on the same input is diffable."""
    t0 = time.time()
    media, out = Path(media), Path(out)
    if not media.is_file():
        raise TranscribeError(f"no such media file: {media}")
    guard_targets([out], allow_tracked)
    lang = None if language in (None, "", "auto") else language
    fake = os.environ.get(FAKE_ENV)
    name = "fake" if fake else "faster-whisper"
    thr = round(float(no_speech_threshold), 3)
    digest = sha256(media)
    old = jload(out)
    eng = old.get("engine") if isinstance(old, dict) else None
    ours = isinstance(eng, dict) and old.get("schema") == WORDS_SCHEMA and eng.get("name") in WRITERS
    placeholder = (isinstance(eng, dict) and eng.get("name") == "hand-timed example"
                   and not (old.get("source") or {}).get("sha256"))  # templates/words.example.json copied by a scaffold
    ours = ours or placeholder
    if out.exists() and not ours and not force:  # hand-made or another tool's timings are never overwritten silently
        raise TranscribeError(f"{out} exists and was not written by transcribe; pass --force to replace it or --out another path")
    installed = None if fake else _fw_version()
    if (not force and ours and (old.get("source") or {}).get("sha256") == digest and eng.get("name") == name
            and eng.get("model") == model and (lang is None or eng.get("language") == lang)
            and eng.get("vad_filter") is bool(vad) and eng.get("no_speech_threshold") == thr
            and (eng.get("version") == "fake" if fake else (eng.get("version") != "fake" and installed in (None, eng.get("version"))))):
        return {"status": "up to date", "file": str(out), "words": len(old.get("words") or []),
                "elapsed_s": round(time.time() - t0, 3)}
    decoded = None
    if fake:
        data = jload(Path(fake))
        if not isinstance(data, dict) or not isinstance(data.get("segments"), list):
            raise TranscribeError(f"{FAKE_ENV}={fake} must be a JSON file with segments[]")
        segments, detected, version = data["segments"], data.get("language"), "fake"
    else:
        try:
            import faster_whisper  # lazy: optional dependency
        except ImportError:
            raise TranscribeError("faster_whisper not installed: pip install faster-whisper") from None
        except Exception as exc:  # noqa: BLE001 - a broken install (missing ctranslate2 library, numpy ABI) raises OSError & co
            raise TranscribeError(f"faster_whisper cannot be imported: {_one_line(exc)} (pip install faster-whisper)") from None
        if not shutil.which("ffmpeg"):
            raise TranscribeError("ffmpeg not found; install ffmpeg (see montage_pro.py doctor)")
        audio = decode_16k(media)
        decoded = len(audio) / 16000.0
        try:
            wm = faster_whisper.WhisperModel(model, device="cpu", compute_type="int8", local_files_only=local_only)
        except Exception as exc:  # noqa: BLE001 - huggingface_hub/ctranslate2 raise many types
            if local_only and isinstance(exc, OSError):
                raise TranscribeError(f"model '{model}' is not cached locally (--local-only); run once without --local-only to download it") from None
            raise TranscribeError(f"cannot load model '{model}': {_one_line(exc)}") from None
        try:
            segs, info = wm.transcribe(audio, language=lang, word_timestamps=True, beam_size=5, vad_filter=bool(vad))
            segments = list(segs)
        except Exception as exc:  # noqa: BLE001
            raise TranscribeError(f"transcription failed: {_one_line(exc)}") from None
        detected = getattr(info, "language", None)
        version = installed or getattr(faster_whisper, "__version__", None) or "unknown"
    probed, offset = media_timing(media)
    kept, dropped = [], []
    for seg in segments:
        nsp = _num(_field(seg, "no_speech_prob"))
        if nsp is not None and nsp > thr:
            s, e = _num(_field(seg, "start")), _num(_field(seg, "end"))
            dropped.append({"text": str(_field(seg, "text", "") or "").strip(), "start": None if s is None else round(s + offset, 3),
                            "end": None if e is None else round(e + offset, 3), "no_speech_prob": round(nsp, 3)})
        else:
            kept.append(seg)
    known = [d for d in (probed, None if decoded is None else offset + decoded) if d]
    # 1 ms under the shortest measured end, so readers that check end <= decoded duration (audio_cue_mapper) accept the last word
    words, phrases = tidy_words(kept, (min(known) - 0.001) if known else None, offset)
    duration = probed or (offset + decoded if decoded else None) or (words[-1]["end"] if words else 0.0)
    source = {"file": media.name, "sha256": digest, "duration": round(duration, 3)}
    if round(offset, 3):
        source["audio_offset"] = round(offset, 3)
    doc = {"schema": WORDS_SCHEMA, "source": source,
           "engine": {"name": name, "version": version, "model": model, "compute_type": "int8",
                      "language": lang or detected, "device": "cpu", "beam_size": 5, "word_timestamps": True,
                      "vad_filter": bool(vad), "no_speech_threshold": thr},
           "words": words, "phrases": phrases}
    if dropped:
        doc["dropped_segments"] = dropped
    try:
        jsave(out, doc)
    except OSError as exc:
        raise TranscribeError(f"cannot write {out}: {_one_line(exc)}") from None
    res = {"status": "written", "file": str(out), "words": len(words), "phrases": len(phrases),
           "duration": source["duration"], "model": model, "language": doc["engine"]["language"], "engine": name,
           "engine_version": version, "vad_filter": bool(vad), "elapsed_s": round(time.time() - t0, 3)}
    if source.get("audio_offset"):
        res["audio_offset"] = source["audio_offset"]
    warn = []
    if dropped:
        res["dropped_segments"] = len(dropped)
        warn.append(f"dropped {len(dropped)} segment(s) with no_speech_prob > {thr} (likely silence/music, not speech): "
                    + " | ".join(d["text"][:40] for d in dropped)[:200])
    if not words:
        warn.append("no words recognised (silence, music or wrong --language?)")
    if warn:
        res["warning"] = "; ".join(warn)
    return res


def transcribe_job(media: Path, job: Path, out: Path = None, model: str = "medium", language: str = "ar",
                   local_only: bool = False, force: bool = False, vad: bool = True, no_speech_threshold: float = NO_SPEECH_MAX,
                   allow_tracked: bool = False) -> dict:
    """transcribe() for a job: never raises, records the result in JOB/report.json; ok=False carries the one-line error.
    JOB/report.json passes the same path guard as the words file."""
    try:
        guard_targets([job / "report.json"], allow_tracked)
        r = transcribe(media, out or job / "words.json", model, language, local_only, force, vad, no_speech_threshold, allow_tracked)
    except TranscribeError as exc:
        return {"ok": False, "error": str(exc)}
    rec = {k: r.get(k) for k in ("status", "file", "words", "model", "language", "elapsed_s")}
    report(job, "transcribe", {**rec, "warning": r["warning"]} if r.get("warning") else rec)
    return {"ok": True, **r}


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
    stream = any(host == h or host.endswith("." + h) for h in STREAM_HOSTS)
    before = {p.name for p in dest.iterdir()}
    manifest = u.path.lower().endswith((".m3u8", ".mpd"))
    if manifest:
        name = re.sub(r"[^\w.\-]+", "_", Path(u.path).stem)[:80] or "stream"
        route = "manifest grab (KOSIF stream_grabber: DASH/HLS segment list → parallel resumable segments → merge best video+audio; DRM refused)"
        rc, out, err = sh([PY, str(HERE / "stream_grabber.py"), "grab", url, "-o", str(dest / (name + ".mp4")), "--max-height", "1080",
                           "--work", str(job / "work" / ("grab-" + name))], 3600)
    elif stream:
        route = "page stream grab (yt-dlp/ffmpeg via fetch_video.py; edit-safe H.264/AAC)"
        rc, out, err = sh([PY, str(HERE / "fetch_video.py"), url, "-o", str(dest), "--quality", "1080"], 3600)
    else:
        name = Path(u.path).name or "download.bin"
        name = re.sub(r"[^\w.\-]+", "_", name)[:120]
        route = f"segmented resumable download ({parts} ranges, .part resume, sha256) via app_studio.py download"
        rc, out, err = sh([PY, str(HERE / "app_studio.py"), "download", url, "-o", str(dest / name), "--set", f"parts={parts}"], 3600)
    new = [p for p in dest.iterdir() if p.name not in before and p.is_file() and not p.name.endswith((".part", ".parts"))]
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
    i.add_argument("--transcribe", action="store_true", help="opt-in: also write JOB/words.json (see transcribe) before the cue mapper")
    tr = sub.add_parser("transcribe", help="faster-whisper word timings → words.json (kosif-words/1)")
    tr.add_argument("media", type=Path); tr.add_argument("--job", type=Path, help="job dir: writes JOB/words.json and JOB/report.json")
    tr.add_argument("--out", type=Path, help="words.json path (default JOB/words.json)")
    for q in (i, tr):  # transcription settings (intake uses them only with --transcribe)
        q.add_argument("--model", default="medium", help="faster-whisper model (default medium)")
        q.add_argument("--language", default="ar", help="language code, or auto to detect (default ar)")
        q.add_argument("--local-only", action="store_true", help="never download the model; fail if it is not cached")
        q.add_argument("--force", action="store_true", help="rewrite words.json even when up to date or not written by transcribe")
        q.add_argument("--no-vad", action="store_true", help="feed silence/music to the model too (default: Silero VAD skips them)")
        q.add_argument("--no-speech-threshold", type=float, default=NO_SPEECH_MAX,
                       help=f"drop segments whose no_speech_prob is above this (default {NO_SPEECH_MAX}; 1 keeps all)")
        q.add_argument("--allow-tracked", action="store_true", help="allow words.json/report.json inside jobs/, tracked by git or not git-ignored")
    o = sub.add_parser("options"); o.add_argument("job", type=Path); o.add_argument("--brief", default="")
    a = sub.add_parser("acquire"); a.add_argument("url"); a.add_argument("--job", type=Path, required=True)
    a.add_argument("--license", default=""); a.add_argument("--source-page", default=""); a.add_argument("--owner", action="store_true")
    a.add_argument("--parts", type=int, default=6)
    c = sub.add_parser("convert"); c.add_argument("job", type=Path); c.add_argument("--fps", type=int, default=30)
    b = sub.add_parser("build"); b.add_argument("job", type=Path); b.add_argument("--option", required=True)
    b.add_argument("--style"); b.add_argument("--title", default="")
    b.add_argument("--deliver-mix", action="store_true", help="also write a -14 LUFS delivery copy (master untouched)")
    x = ap.parse_args(argv)
    if x.cmd in ("intake", "transcribe") and not 0.0 <= x.no_speech_threshold <= 1.0:
        ap.error("--no-speech-threshold must be between 0 and 1")
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
        topts = None
        if x.transcribe:
            topts = {"model": x.model, "language": x.language, "local_only": x.local_only, "force": x.force, "vad": not x.no_vad,
                     "no_speech_threshold": x.no_speech_threshold, "allow_tracked": x.allow_tracked}
            try:  # fail before any intake work when the transcript could not be written there anyway
                guard_targets([x.job / "words.json", x.job / "report.json"], x.allow_tracked)
            except TranscribeError as exc:
                print("transcribe: " + str(exc), file=sys.stderr)
                return 2
        r = intake(x.media, x.job, topts)
        print(json.dumps({k: r[k] for k in r if k not in ("source",)}, ensure_ascii=False, indent=1))
        if topts is not None and not r["transcribe"]["ok"]:
            print("transcribe: " + r["transcribe"]["error"], file=sys.stderr)
            return 2
        if r.get("warning"):  # --transcribe wrote words that never reached the cue map: say it and fail
            print("intake: " + r["warning"], file=sys.stderr)
            return 1
        return 0
    if x.cmd == "transcribe":
        if not (x.job or x.out):
            ap.error("transcribe needs --job JOB or --out PATH")
        tkw = {"vad": not x.no_vad, "no_speech_threshold": x.no_speech_threshold, "allow_tracked": x.allow_tracked}
        if x.job:
            r = transcribe_job(x.media, x.job, x.out, x.model, x.language, x.local_only, x.force, **tkw)
            err = None if r.pop("ok") else r["error"]
        else:  # --out alone: no job, so no report.json is written anywhere
            try:
                r, err = transcribe(x.media, x.out, x.model, x.language, x.local_only, x.force, **tkw), None
            except TranscribeError as exc:
                err = str(exc)
        if err:
            print("transcribe: " + err, file=sys.stderr)
            return 2
        print(json.dumps(r, ensure_ascii=False))
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
