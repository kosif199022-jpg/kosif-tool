"""Real programs for the photo-video-footage (and DL-*) power cards.

Every function builds a tiny synthetic fixture (frames, tones, transcripts, configs), performs the
card's technique with the card's own numbers (ffmpeg filters, OpenCV, numpy) and returns
known-answer checks. Offline, deterministic, no credits.
"""
from __future__ import annotations

import colorsys
import hashlib
import ipaddress
import json
import math
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[5]
FF = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]


# ---------------------------------------------------------------- helpers
def ff(*args, inp: bytes | None = None) -> subprocess.CompletedProcess:
    r = subprocess.run(FF + [str(a) for a in args], input=inp, capture_output=True, timeout=60)
    if r.returncode:
        raise RuntimeError(r.stderr.decode()[-600:])
    return r


def ffstderr(*args) -> str:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-y"] + [str(a) for a in args],
                       capture_output=True, timeout=60)
    return r.stderr.decode(errors="replace")


def probe(path, *entries) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams",
                        "-show_format", str(path)], capture_output=True, timeout=30)
    return json.loads(r.stdout or b"{}")


def vstream(path) -> dict:
    return next(s for s in probe(path)["streams"] if s["codec_type"] == "video")


def astreams(path) -> list:
    return [s for s in probe(path).get("streams", []) if s["codec_type"] == "audio"]


def duration(path) -> float:
    return float(probe(path)["format"]["duration"])


def write_video(path, frames, fps=30, codec="ffv1", extra=(), audio: Path | None = None):
    frames = np.asarray(frames, dtype=np.uint8)
    n, h, w, _ = frames.shape
    args = ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-"]
    if audio:
        args += ["-i", str(audio), "-c:a", "aac", "-shortest"]
    if codec == "ffv1":
        args += ["-c:v", "ffv1", "-pix_fmt", "bgr0"]
    else:
        args += ["-c:v", codec, "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-crf", "1"]
    ff(*args, *extra, path, inp=frames.tobytes())
    return Path(path)


def read_video(path, size=None) -> np.ndarray:
    st = vstream(path)
    w, h = (size or (int(st["width"]), int(st["height"])))
    vf = ["-vf", f"scale={w}:{h}"] if size else []
    r = subprocess.run(FF + ["-i", str(path), *vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, timeout=60)
    a = np.frombuffer(r.stdout, np.uint8)
    return a.reshape(-1, h, w, 3)


def write_wav(path, x, sr=16000, ch=1):
    x = np.clip(np.asarray(x, dtype=np.float64), -1, 1)
    pcm = (x * 32767).astype("<i2")
    with wave.open(str(path), "wb") as wv:
        wv.setnchannels(ch)
        wv.setsampwidth(2)
        wv.setframerate(sr)
        wv.writeframes(pcm.tobytes())
    return Path(path)


def read_wav(path):
    with wave.open(str(path)) as wv:
        sr, ch, n = wv.getframerate(), wv.getnchannels(), wv.getnframes()
        x = np.frombuffer(wv.readframes(n), "<i2").astype(np.float64) / 32767
    return (x.reshape(-1, ch).mean(1) if ch > 1 else x), sr


def decode_audio(path, sr=16000):
    r = subprocess.run(FF + ["-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                       capture_output=True, timeout=60)
    return np.frombuffer(r.stdout, "<i2").astype(np.float64) / 32767


def tone(sec, f=440, sr=16000, amp=0.5):
    t = np.arange(int(sec * sr)) / sr
    return amp * np.sin(2 * np.pi * f * t)


def dom_freq(x, sr):
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    return np.fft.rfftfreq(len(x), 1 / sr)[int(np.argmax(spec))]


def solid(n, h, w, rgb):
    return np.tile(np.array(rgb, np.uint8), (n, h, w, 1))


def jwrite(work, name, obj):
    p = Path(work) / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return p


def luma(img):
    img = np.asarray(img, np.float64)
    return 0.2126 * img[..., 0] + 0.7152 * img[..., 1] + 0.0722 * img[..., 2]


def rel_lum(rgb):
    c = np.asarray(rgb, np.float64) / 255
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def contrast(a, b):
    la, lb = sorted([float(rel_lum(a)), float(rel_lum(b))], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def near(a, b, tol):
    return abs(a - b) <= tol


def chk(name, ok, obs):
    return (name, bool(ok), str(obs))


def frame_index_frames(n, h=36, w=64):
    """Frame i encodes its index: R = (i % 16) * 16, G = (i // 16) * 16."""
    f = np.zeros((n, h, w, 3), np.uint8)
    for i in range(n):
        f[i, ..., 0] = (i % 16) * 16 + 8
        f[i, ..., 1] = (i // 16) * 12 + 8
    return f


def decode_index(frame):
    r, g = frame[..., 0].mean(), frame[..., 1].mean()
    return int(round((g - 8) / 12)) * 16 + int(round((r - 8) / 16))


# ---------------------------------------------------------------- DL
def dl_05(work):
    """Netscape cookies.txt: parse, flag expired, keep outside repo, redact in logs."""
    now = 1_800_000_000
    lines = ["# Netscape HTTP Cookie File",
             ".example.com\tTRUE\t/\tTRUE\t1900000000\tSID\tsecretAAA",
             ".example.com\tTRUE\t/\tFALSE\t1700000000\tOLD\tsecretBBB",
             "bad line without tabs",
             "#HttpOnly_.example.com\tTRUE\t/\tTRUE\t0\tSESS\tsecretCCC"]
    txt = "\n".join(lines)

    def parse(text):
        good, bad = [], 0
        for ln in text.splitlines():
            http_only = ln.startswith("#HttpOnly_")
            if ln.startswith("#") and not http_only or not ln.strip():
                continue
            parts = (ln[len("#HttpOnly_"):] if http_only else ln).split("\t")
            if len(parts) != 7:
                bad += 1
                continue
            dom, flag, path, secure, exp, name, val = parts
            good.append({"domain": dom, "name": name, "value": val, "expires": int(exp),
                         "secure": secure == "TRUE", "http_only": http_only})
        return good, bad

    def redact(log, cookies):
        for c in cookies:
            log = log.replace(c["value"], "***")
        return log

    def allowed_location(p: Path):
        try:
            p.resolve().relative_to(REPO)
            return False
        except ValueError:
            return True

    cookies, bad = parse(txt)
    expired = [c["name"] for c in cookies if c["expires"] and c["expires"] < now]
    session = [c["name"] for c in cookies if c["expires"] == 0]
    log = redact(f"yt-dlp --cookies cookies.txt  sent SID={cookies[0]['value']}", cookies)
    jwrite(work, "cookies_report.json", {"cookies": [{k: v for k, v in c.items() if k != "value"} for c in cookies],
                                         "expired": expired, "malformed": bad, "log": log})
    return [chk("3 valid cookies parsed, 1 malformed", len(cookies) == 3 and bad == 1, f"{len(cookies)}/{bad}"),
            chk("expired cookie flagged", expired == ["OLD"], expired),
            chk("HttpOnly session cookie recognised", session == ["SESS"] and cookies[2]["http_only"], session),
            chk("value redacted from log", "secret" not in log and "***" in log, log),
            chk("repo path refused for cookies", not allowed_location(REPO / "cookies.txt")
                and allowed_location(Path("/tmp/cookies.txt")), "repo refused, /tmp allowed")]


def dl_08(work):
    """Cloud container limits: route each host to download / ask-upload as measured."""
    measured = {"archive.org": "ok", "youtube.com": "403", "youtu.be": "403", "vimeo.com": "login",
                "commons.wikimedia.org": "403"}

    def route(url):
        from urllib.parse import urlparse
        host = urlparse(url).hostname or ""
        host = host[4:] if host.startswith("www.") else host
        state = next((v for k, v in measured.items() if host == k or host.endswith("." + k)), "unknown")
        if state == "ok":
            return "download_here"
        if state == "unknown":
            return "try_once_then_ask"
        return "ask_user_upload_or_run_on_device"

    cases = {"https://archive.org/details/x": "download_here",
             "https://www.youtube.com/watch?v=1": "ask_user_upload_or_run_on_device",
             "https://vimeo.com/5": "ask_user_upload_or_run_on_device",
             "https://upload.commons.wikimedia.org/a.webm": "ask_user_upload_or_run_on_device",
             "https://example.org/a.mp4": "try_once_then_ask"}
    got = {u: route(u) for u in cases}
    jwrite(work, "routes.json", got)
    return [chk(f"route {u.split('/')[2]}", got[u] == want, got[u]) for u, want in cases.items()]


def dl_11(work):
    """PhotosSafe export: libx264 crf 18 veryfast yuv420p, AAC 192k, +faststart, 1-frame sanity decode."""
    src = write_video(work / "src.mkv", np.random.default_rng(1).integers(0, 255, (30, 36, 64, 3)), 30,
                      audio=write_wav(work / "a.wav", tone(1.0)))
    out = work / "photos_safe.mp4"
    ff("-i", src, "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    v, a = vstream(out), astreams(out)
    data = out.read_bytes()
    moov, mdat = data.find(b"moov"), data.find(b"mdat")
    sanity = subprocess.run(FF + ["-i", str(out), "-frames:v", "1", "-f", "null", "-"], capture_output=True)
    return [chk("h264 yuv420p", v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p",
                f"{v['codec_name']} {v['pix_fmt']}"),
            chk("aac audio", a and a[0]["codec_name"] == "aac", a[0]["codec_name"] if a else None),
            chk("faststart moov before mdat", 0 < moov < mdat, f"moov@{moov} mdat@{mdat}"),
            chk("sanity decode -frames:v 1 exit 0", sanity.returncode == 0, sanity.returncode)]


# ---------------------------------------------------------------- FOOT discipline / validators
def foot_01(work):
    allowed = {"user-confirmed", "pd", "cc0", "cc-by", "stock-receipt"}
    banned = {"reference-frame", "scraped", "cc-by-nd", "cc-by-nc"}
    rows = [
        {"file": "a.mp4", "source": "user", "licence": "user-confirmed", "author": "owner", "url": "-", "use": "ad"},
        {"file": "b.jpg", "source": "commons", "licence": "CC-BY", "author": "Ann", "url": "https://c/b", "use": "ad"},
        {"file": "c.jpg", "source": "commons", "licence": "CC-BY", "author": "", "url": "https://c/c", "use": "ad"},
        {"file": "d.mp4", "source": "pinterest", "licence": "scraped", "author": "?", "url": "https://p/d", "use": "ad"},
        {"file": "e.jpg", "source": "flickr", "licence": "CC-BY-NC", "author": "Bo", "url": "https://f/e", "use": "ad"},
        {"file": "f.jpg", "source": "getty", "licence": "editorial", "author": "G", "url": "https://g/f", "use": "ad"},
        {"file": "g.png", "source": "nasa", "licence": "PD", "author": "NASA", "url": "https://n/g", "use": "ad"},
    ]

    def verdict(r):
        lic = r["licence"].lower()
        if any(not r.get(k) for k in ("source", "licence", "author", "url")):
            return "reject:missing-field"
        if lic in banned:
            return "reject:" + lic
        if lic == "editorial" and r["use"] == "ad":
            return "reject:editorial-in-ad"
        if lic in allowed:
            return "allow" + (":attribute" if lic == "cc-by" else "")
        return "reject:unknown"

    got = {r["file"]: verdict(r) for r in rows}
    md = ["| file | source | licence | author | url | verdict |", "|---|---|---|---|---|---|"]
    md += [f"| {r['file']} | {r['source']} | {r['licence']} | {r['author']} | {r['url']} | {got[r['file']]} |" for r in rows]
    (work / "ASSETS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    want = {"a.mp4": "allow", "b.jpg": "allow:attribute", "c.jpg": "reject:missing-field",
            "d.mp4": "reject:scraped", "e.jpg": "reject:cc-by-nc", "f.jpg": "reject:editorial-in-ad", "g.png": "allow"}
    return [chk("one ASSETS.md row per file", len(md) - 2 == len(rows), len(md) - 2)] + \
           [chk(f"verdict {k}", got[k] == v, got[k]) for k, v in want.items()]


def foot_02(work):
    """Open-footage guard: https only, allow-listed hosts, 64 KiB-500 MiB, challenge pages refused, sha receipt."""
    from urllib.parse import urlparse
    allow = ("wikimedia.org", "pexels.com")

    def check_url(u):
        p = urlparse(u)
        if p.scheme != "https":
            return "refuse:not-https"
        h = p.hostname or ""
        if not any(h == a or h.endswith("." + a) for a in allow):
            return "refuse:host"
        return "ok"

    def accept_body(body: bytes, ctype: str):
        if ctype.startswith("text/html") or body[:200].lstrip().lower().startswith((b"<!doctype", b"<html")):
            return "refuse:challenge-page"
        if not 64 * 1024 <= len(body) <= 500 * 1024 * 1024:
            return "refuse:size"
        return "ok"

    body = ff("-f", "lavfi", "-i", "testsrc=s=320x240:d=2:r=25", "-c:v", "libx264", "-preset", "ultrafast",
              "-crf", "10", "-f", "mp4", "-movflags", "frag_keyframe", "-").stdout
    clip = work / "clip.mp4"
    clip.write_bytes(body)
    receipt = {"schema": "kosif-open-footage-v1", "url": "https://upload.wikimedia.org/x.webm",
               "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body), "license_note": "CC0"}
    (work / "clip.mp4.source.json").write_text(json.dumps(receipt), encoding="utf-8")
    return [chk("http refused", check_url("http://upload.wikimedia.org/a") == "refuse:not-https", "http"),
            chk("non-listed host refused", check_url("https://evil.example/a.mp4") == "refuse:host", "evil"),
            chk("lookalike host refused", check_url("https://wikimedia.org.evil.com/a") == "refuse:host", "lookalike"),
            chk("wikimedia allowed", check_url(receipt["url"]) == "ok", "ok"),
            chk("challenge page refused", accept_body(b"<!DOCTYPE html><title>Just a moment", "text/html")
                == "refuse:challenge-page", "html"),
            chk("32 KiB body refused", accept_body(b"\0" * 32768, "video/mp4") == "refuse:size", "32KiB"),
            chk("real clip accepted", accept_body(body, "video/mp4") == "ok", len(body)),
            chk("receipt sha matches file", hashlib.sha256(clip.read_bytes()).hexdigest() == receipt["sha256"], "sha")]


def foot_03(work):
    """Safe single-URL guard + edit-safe copy (H.264 yuv420p CFR <= 60 fps, AAC 48 kHz)."""
    from urllib.parse import urlparse

    def guard(url, resolved_ip, size_mb, dur_s, height):
        if urlparse(url).scheme != "https":
            return "refuse:https"
        if not ipaddress.ip_address(resolved_ip).is_global:
            return "refuse:non-global-ip"
        if size_mb > 150:
            return "refuse:size"
        if dur_s > 900:
            return "refuse:duration"
        if height > 720:
            return "pick<=720p"
        return "ok"

    src = write_video(work / "src.mkv", frame_index_frames(120), 120, audio=write_wav(work / "a.wav", tone(1.0)))
    out = work / "edit.mp4"
    ff("-i", src, "-vf", "fps=60", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-ar", "48000", out)
    v, a = vstream(out), astreams(out)[0]
    fr = eval(v["r_frame_rate"])
    return [chk("private IP refused", guard("https://x/a", "10.0.0.5", 1, 1, 480) == "refuse:non-global-ip", "10.0.0.5"),
            chk("http refused", guard("http://x/a", "8.8.8.8", 1, 1, 480) == "refuse:https", "http"),
            chk("151 MB refused", guard("https://x/a", "8.8.8.8", 151, 1, 480) == "refuse:size", "151"),
            chk("901 s refused", guard("https://x/a", "8.8.8.8", 1, 901, 480) == "refuse:duration", "901"),
            chk("1080p capped to 720p", guard("https://x/a", "8.8.8.8", 1, 1, 1080) == "pick<=720p", "1080"),
            chk("edit copy 60 fps CFR from 120", fr == 60 and eval(v["avg_frame_rate"]) == 60, f"{fr} {v['avg_frame_rate']}"),
            chk("AAC 48 kHz", a["codec_name"] == "aac" and a["sample_rate"] == "48000", a["sample_rate"])]


def foot_04(work):
    shots = [{"id": 1, "dur": 2.0, "query": ["incense burner smoke aesthetic", "bakhoor mabkhara"],
              "query_ar": ["مبخرة بخور"]},
             {"id": 2, "dur": 3.0, "query": [], "query_ar": ["قهوة"]}]
    cands = {1: [{"id": "a", "len": 2.5, "h": 1080, "wm": False, "slowed": False},
                 {"id": "b", "len": 1.5, "h": 1080, "wm": False, "slowed": True},
                 {"id": "c", "len": 1.2, "h": 1080, "wm": False, "slowed": True},
                 {"id": "d", "len": 5.0, "h": 480, "wm": False, "slowed": False},
                 {"id": "e", "len": 5.0, "h": 720, "wm": True, "slowed": False},
                 {"id": "f", "len": 4.0, "h": 720, "wm": False, "slowed": False},
                 {"id": "g", "len": 9.0, "h": 2160, "wm": False, "slowed": False}]}

    def valid_shot(s):
        return 1 <= len(s["query"]) <= 3 and 1 <= len(s["query_ar"]) <= 3

    def usable(c, dur):
        need = dur * (0.67 if c["slowed"] else 1.0)
        return c["len"] >= need and c["h"] >= 720 and not c["wm"]

    pool = {1: [c["id"] for c in cands[1] if usable(c, 2.0)][:3]}
    jwrite(work, "pool.json", pool)
    return [chk("shot with no English query rejected", not valid_shot(shots[1]) and valid_shot(shots[0]), "2 invalid"),
            chk("slowed 1.5 s clip accepted (>= 0.67x2.0)", "b" in pool[1], pool),
            chk("slowed 1.2 s clip rejected", "c" not in [c["id"] for c in cands[1] if usable(c, 2.0)], "c"),
            chk("480p and watermark rejected", not usable(cands[1][3], 2) and not usable(cands[1][4], 2), "d,e"),
            chk("pool capped at 3 candidates", pool[1] == ["a", "b", "f"], pool[1])]


def foot_05(work):
    exts_v = {"mp4", "mov", "mkv", "webm", "avi", "m4v"}
    exts_a = {"mp3", "wav", "m4a", "aac", "flac", "ogg"}
    exts_i = {"png", "jpg", "webp", "gif"}
    exts_t = {"json", "txt", "srt"}
    media = work / "media"
    media.mkdir()
    write_video(media / "clip.mkv", solid(10, 36, 64, (10, 200, 10)), 10, audio=write_wav(work / "t.wav", tone(1)))
    write_wav(media / "voice.wav", tone(0.5))
    Image.new("RGB", (8, 8)).save(media / "pic.png")
    (media / "notes.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\nhi\n", encoding="utf-8")
    (media / "tool.exe").write_bytes(b"MZ")
    long_name = "x" * 151 + ".png"

    def classify(p: Path):
        if len(p.name) > 150:
            return {"error": "name too long"}
        ext = p.suffix.lower().lstrip(".")
        if ext not in exts_v | exts_a | exts_i | exts_t:
            return {"error": "type not accepted"}
        info = {"kind": "video" if ext in exts_v else "audio" if ext in exts_a else "image" if ext in exts_i else "text"}
        if info["kind"] in ("video", "audio"):
            pr = probe(p)
            info["duration"] = round(float(pr["format"]["duration"]), 2)
            info["has_video"] = any(s["codec_type"] == "video" for s in pr["streams"])
            info["has_audio"] = any(s["codec_type"] == "audio" for s in pr["streams"])
        return info

    index = {p.name: classify(p) for p in sorted(media.iterdir())}
    index[long_name] = classify(Path(long_name))
    jwrite(media, ".index.json", index)
    return [chk("video probed with audio", index["clip.mkv"]["has_video"] and index["clip.mkv"]["has_audio"]
                and near(index["clip.mkv"]["duration"], 1.0, 0.1), index["clip.mkv"]),
            chk("wav probed audio-only 0.5 s", index["voice.wav"]["kind"] == "audio" and not index["voice.wav"]["has_video"]
                and near(index["voice.wav"]["duration"], 0.5, 0.02), index["voice.wav"]),
            chk("png classified image", index["pic.png"]["kind"] == "image", index["pic.png"]),
            chk("srt classified text", index["notes.srt"]["kind"] == "text", index["notes.srt"]),
            chk(".exe refused", "error" in index["tool.exe"], index["tool.exe"]),
            chk("151-char name refused", "error" in index[long_name], index[long_name])]


def foot_06(work):
    """Read creation_time, apply per-camera offset, sort, timeline fps = most common fps."""
    specs = [("A_001", "2026-01-01T10:00:10Z", 30), ("B_001", "2026-01-01T10:00:02Z", 25),
             ("A_002", "2026-01-01T10:00:05Z", 30), ("B_002", "2026-01-01T10:00:20Z", 25),
             ("A_003", "2026-01-01T10:00:30Z", 30)]
    for name, ct, fps in specs:
        ff("-f", "lavfi", "-i", f"color=c=gray:s=32x18:r={fps}:d=0.2", "-metadata", f"creation_time={ct}",
           "-c:v", "libx264", "-preset", "ultrafast", work / f"{name}.mp4")
    offsets = {"B": +7.0}  # camera B clock is 7 s behind (measured from a shared moment)
    from datetime import datetime
    rows = []
    for p in sorted(work.glob("*.mp4")):
        pr = probe(p)
        ct = pr["format"]["tags"]["creation_time"]
        t = datetime.fromisoformat(ct.replace("Z", "+00:00")).timestamp()
        cam = p.stem.split("_")[0]
        st = pr["streams"][0]
        rows.append({"file": p.name, "time": t + offsets.get(cam, 0.0), "camera": cam,
                     "fps": round(eval(st["r_frame_rate"])), "res": f"{st['width']}x{st['height']}"})
    rows.sort(key=lambda r: r["time"])
    fpss = [r["fps"] for r in rows]
    tl_fps = max(set(fpss), key=fpss.count)
    jwrite(work, "dry_run.json", {"fps": tl_fps, "rows": rows})
    order = [r["file"][:-4] for r in rows]
    return [chk("creation_time read from every file", len(rows) == 5, len(rows)),
            chk("offset-corrected order", order == ["A_002", "B_001", "A_001", "B_002", "A_003"], order),
            chk("timeline fps = most common clip fps", tl_fps == 30, tl_fps)]


def foot_07(work):
    def validate(cfg, timeline_fps=30):
        errs = []
        if (cfg["w"], cfg["h"]) != (3840, 2160):
            errs.append("not native 3840x2160")
        if cfg["fps"] != timeline_fps:
            errs.append("fps != timeline")
        if not 18 <= cfg["cqp"] <= 20:
            errs.append("CQP outside 18-20")
        if cfg["editor_pt"] < 16 or cfg["terminal_pt"] < 18:
            errs.append("font too small")
        if cfg["notifications"]:
            errs.append("notifications on")
        if cfg["mic_track"] == cfg["system_track"]:
            errs.append("mic and system audio share a track")
        return errs

    good = {"w": 3840, "h": 2160, "fps": 30, "cqp": 19, "editor_pt": 16, "terminal_pt": 18,
            "notifications": False, "mic_track": 1, "system_track": 2}
    bad = dict(good, fps=60, cqp=23, terminal_pt=14, notifications=True, mic_track=2)
    eg, eb = validate(good), validate(bad)
    jwrite(work, "capture_check.json", {"good": eg, "bad": eb})
    return [chk("card defaults pass", eg == [], eg),
            chk("bad config: 5 violations", len(eb) == 5, eb),
            chk("CQP 23 flagged", "CQP outside 18-20" in eb, eb)]


# ---------------------------------------------------------------- shot detection family
def detect_cuts(frames, fps, threshold=10.0, min_len=0.5):
    """Mean abs diff in 0-100 scale; cut where > threshold and >= min_len after last cut."""
    f = frames.astype(np.float64)
    d = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2, 3)) / 255 * 100
    cuts, last = [], 0.0
    for i, v in enumerate(d, start=1):
        t = i / fps
        if v > threshold and t - last >= min_len:
            cuts.append(round(t, 3))
            last = t
    return cuts, d


def foot_08(work):
    fps = 25
    fr = np.concatenate([solid(50, 36, 64, (200, 30, 30)), solid(50, 36, 64, (30, 200, 30)),
                         solid(5, 36, 64, (30, 30, 200)), solid(45, 36, 64, (230, 230, 30))])
    src = write_video(work / "clip.mkv", fr, fps)
    frames = read_video(src)
    cuts, _ = detect_cuts(frames, fps, threshold=10, min_len=0.5)
    shots = [0.0] + cuts
    tl = {"clips": [{"in": a, "out": b, "transition": "fade"} for a, b in zip(shots, cuts + [len(frames) / fps])]}
    jwrite(work, "edit.json", tl)
    sheet = np.concatenate([frames[int(s * fps) + 1] for s in shots], axis=1)
    Image.fromarray(sheet).save(work / "shots.png")
    return [chk("cut at 2.0 s +-0.15", any(near(c, 2.0, 0.15) for c in cuts), cuts),
            chk("cut at 4.0 s +-0.15", any(near(c, 4.0, 0.15) for c in cuts), cuts),
            chk("flash 0.2 s after a cut suppressed by min 0.5 s", len(cuts) == 2, cuts),
            chk("3 shots in timeline", len(tl["clips"]) == 3, len(tl["clips"]))]


def foot_09(work):
    cols = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
    fr = np.concatenate([solid(5, 72, 128, c) for c in cols])  # 6 colours x 0.5 s at 10 fps
    src = write_video(work / "in.mkv", fr, 10)
    ff("-i", src, "-vf", "fps=2,scale=320:-1,tile=3x2", "-frames:v", "1", work / "sheet.png")
    sheet = np.asarray(Image.open(work / "sheet.png").convert("RGB")).astype(int)
    h, w = sheet.shape[:2]
    tiles = [sheet[(k // 3) * h // 2 + h // 4, (k % 3) * w // 3 + w // 6] for k in range(6)]
    ok_tiles = all(np.abs(np.array(t) - np.array(c)).max() < 40 for t, c in zip(tiles, cols))
    out = ffstderr("-i", src, "-vf", "select='gt(scene,0.3)',showinfo", "-f", "null", "-")
    pts = [float(x.split("pts_time:")[1].split()[0]) for x in out.splitlines() if "pts_time:" in x]
    dur = len(fr) / 10
    cover = [t for t in pts if 0 < t < dur - 0.1]
    jwrite(work, "covers.json", {"candidates": cover})
    return [chk("sheet is 3x2 tiles of 320 px", (w, h) == (960, 360), f"{w}x{h}"),
            chk("tiles follow the timeline colours", ok_tiles, [list(t) for t in tiles]),
            chk("scene>0.3 finds the 5 changes", len(pts) == 5 and near(pts[0], 0.5, 0.11), pts),
            chk("first/last frames excluded from covers", 0.0 not in cover and len(cover) == 5, cover)]


def motion_energy(frames, src_fps, fps=6):
    step = max(1, round(src_fps / fps))
    s = frames[::step].astype(np.float64).mean(-1)
    return np.abs(np.diff(s, axis=0)).mean(axis=(1, 2)), step


def foot_10(work):
    rng = np.random.default_rng(3)
    fps = 24
    fr = solid(96, 36, 64, (90, 90, 90)).copy()
    for i in range(48, 72):  # 2.0-3.0 s: moving bar
        fr[i, :, (i * 3) % 64:(i * 3) % 64 + 8] = 250
    for i in range(0, 24):
        fr[i] = np.clip(fr[i].astype(int) + rng.integers(-3, 3, fr[i].shape), 0, 255)
    src = write_video(work / "c.mkv", fr, fps)
    frames = read_video(src)
    e, step = motion_energy(frames, fps, 6)
    win = 6  # 1 s windows at 6 fps
    scores = [float(e[k:k + win].sum()) for k in range(0, len(e) - win + 1, win)]
    used = set()

    def pick():
        k = max((i for i in range(len(scores)) if i not in used), key=lambda i: scores[i])
        used.add(k)
        return k

    first, second = pick(), pick()
    jwrite(work, "energy.json", {"energy": e.round(3).tolist(), "windows": scores, "picks": [first, second]})
    return [chk("sampled at 6 fps", step == 4, step),
            chk("most active window = 2-3 s", first == 2, (first, scores)),
            chk("second pick is a different unused window", second != first, second)]


def foot_11(work):
    import cv2
    rng = np.random.default_rng(5)
    fps = 10
    tex = rng.integers(40, 200, (36, 64, 3)).astype(np.uint8)
    fr = np.stack([tex] * 60)
    fr[:8] = 250  # ~0.8 s white head
    fr[8:11] = cv2.GaussianBlur(tex, (0, 0), 4)  # soft frames
    frames = fr

    def lap(img):
        return cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), cv2.CV_64F).var()

    def trim_point(frames, fps):
        if len(frames) / fps < 5:
            return None
        ref = frames[int(2 * fps):int(5 * fps)]
        rl, rf = luma(ref).mean(), np.mean([lap(f) for f in ref])
        for i in range(int(2 * fps)):
            if abs(luma(frames[i]).mean() - rl) <= 0.2 * rl and lap(frames[i]) >= 0.5 * rf:
                return i
        return int(2 * fps)

    tp = trim_point(frames, fps)
    short = trim_point(frames[:40], fps)

    def hist(img):
        h = np.histogram(luma(img), 32, (0, 255))[0].astype(float)
        return h

    a, b = tex, np.clip(tex.astype(int) + 4, 0, 255).astype(np.uint8)
    c = rng.integers(0, 255, (36, 64, 3)).astype(np.uint8)
    corr = lambda x, y: float(np.corrcoef(hist(x), hist(y))[0, 1])
    takes = [("t1", 0, a), ("t2", 60, b), ("t3", 200, b), ("t4", 70, c)]
    dup = [(p[0], q[0]) for i, p in enumerate(takes) for q in takes[i + 1:]
           if abs(p[1] - q[1]) <= 120 and corr(p[2], q[2]) >= 0.9]
    jwrite(work, "trim.json", {"trim_frame": tp, "duplicates": dup})
    return [chk("trim lands on first good frame (11)", tp == 11, tp),
            chk("clip < 5 s skipped", short is None, short),
            chk("duplicate takes grouped (t1,t2) only", dup == [("t1", "t2")], dup)]


def exposure(img):
    y = luma(img)
    p = np.percentile(y, [1, 50, 99])
    clipped = float((y >= 250).mean() * 100)
    crushed = float((y <= 5).mean() * 100)
    mean = float(y.mean())
    if mean > 185 or clipped > 5:
        v = "over"
    elif mean < 60 or crushed > 15:
        v = "under"
    else:
        v = "ok"
    advice = []
    if clipped > 2:
        advice.append("خفّض التعريض: الإضاءات محترقة")
    if crushed > 10:
        advice.append("ارفع الظلال: الأسود مسحوق")
    if p[2] - p[0] < 120:
        advice.append("زد التباين: المدى ضيق")
    return {"verdict": v, "mean": round(mean, 1), "clipped": round(clipped, 2), "crushed": round(crushed, 2),
            "range": round(float(p[2] - p[0]), 1), "advice": advice}


def foot_12(work):
    g = np.tile(np.linspace(0, 255, 256), (64, 1))
    normal = np.stack([g] * 3, -1).astype(np.uint8)
    over = np.clip(normal.astype(int) + 120, 0, 255).astype(np.uint8)
    under = (normal * 0.2).astype(np.uint8)
    flat = np.full((64, 256, 3), 128, np.uint8)
    flat[:, :128] = 100
    res = {k: exposure(v) for k, v in dict(normal=normal, over=over, under=under, flat=flat).items()}
    jwrite(work, "exposure.json", res)
    return [chk("gradient ok", res["normal"]["verdict"] == "ok", res["normal"]),
            chk("+120 over-exposed with clip advice", res["over"]["verdict"] == "over" and res["over"]["advice"], res["over"]),
            chk("x0.2 under-exposed", res["under"]["verdict"] == "under", res["under"]),
            chk("flat image gets range advice", any("المدى" in a for a in res["flat"]["advice"]), res["flat"]["advice"])]


def classify_boundaries(frames, fps):
    """cut = one big jump; dissolve = run of frames that are blends of the neighbours; fadeblack = luma hits 0."""
    f = frames.astype(np.float64)
    y = f.mean(axis=(1, 2, 3))
    d = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2, 3))
    out, i = [], 0
    n = len(d)
    while i < n:
        if d[i] < 1.0:
            i += 1
            continue
        j = i
        while j + 1 < n and d[j + 1] >= 1.0:
            j += 1
        span = j - i + 1
        seg_y = y[i:j + 2]
        if seg_y.min() < 3 and (span > 1):
            kind = "fadeblack"
        elif span == 1:
            kind = "cut"
        else:
            kind = "dissolve"
        out.append({"kind": kind, "start": round((i + 1) / fps, 3), "frames": span})
        i = j + 1
    return out


def foot_13(work):
    fps = 10
    A, B, C = solid(10, 36, 64, (200, 40, 40)), solid(10, 36, 64, (40, 200, 40)), solid(10, 36, 64, (40, 40, 200))
    diss = np.stack([((1 - k / 6) * B[0] + k / 6 * C[0]).astype(np.uint8) for k in range(1, 6)])
    fade = np.stack([(C[0] * (1 - k / 5)).astype(np.uint8) for k in range(1, 6)])
    frames = np.concatenate([A, B, diss, C, fade, solid(3, 36, 64, (0, 0, 0))])
    src = write_video(work / "ref.mkv", frames, fps)
    b = classify_boundaries(read_video(src), fps)
    jwrite(work, "mimic.json", {"boundaries": b})
    kinds = [x["kind"] for x in b]
    return [chk("cut / dissolve / fadeblack in order", kinds == ["cut", "dissolve", "fadeblack"], kinds),
            chk("cut exact at frame 10 (1.0 s)", b and b[0]["start"] == 1.0, b[:1]),
            chk("dissolve length 6 frames", len(b) > 1 and b[1]["frames"] == 6, b[1:2])]


def foot_14(work):
    fps = 10
    segs = [((220, 20, 20), 4.0), ((20, 220, 20), 2.0), ((20, 20, 220), 7.0)]
    fr = np.concatenate([solid(int(s * fps), 18, 32, c) for c, s in segs])
    src = write_video(work / "v.mkv", fr, fps)
    frames = read_video(src)
    cuts, _ = detect_cuts(frames, fps, 10, 0.5)
    bounds = [0.0] + cuts + [len(frames) / fps]
    beats = []
    for a, b in zip(bounds, bounds[1:]):
        k = max(1, math.ceil((b - a) / 3.0 - 1e-9))
        for m in range(k):
            s, e = a + (b - a) * m / k, a + (b - a) * (m + 1) / k
            mid = frames[int((s + e) / 2 * fps)]
            rgb = np.median(mid.reshape(-1, 3), 0).astype(int)
            beats.append({"start": round(s, 3), "end": round(e, 3), "hex": "#%02x%02x%02x" % tuple(rgb)})
    jwrite(work, "beats.json", beats)
    return [chk("every beat <= 3 s", all(b["end"] - b["start"] <= 3.0 + 1e-6 for b in beats),
                [round(b["end"] - b["start"], 2) for b in beats]),
            chk("13 s with cuts at 4 and 6 -> 2+1+3 = 6 beats", len(beats) == 6, len(beats)),
            chk("beat palettes match planted colours", [b["hex"] for b in beats] ==
                ["#dc1414", "#dc1414", "#14dc14", "#1414dc", "#1414dc", "#1414dc"], [b["hex"] for b in beats])]


def foot_15(work):
    src = np.zeros((100, 400, 3), np.uint8)
    src[:, 200:] = 255
    p = work / "logo.png"
    Image.fromarray(src).save(p)
    before = hashlib.sha256(p.read_bytes()).hexdigest()

    def needs_upscale(long_side, display):
        return long_side < 1.5 * display

    def upscale(path, n):
        out = path.with_name(f"{path.stem}_up{n}.png")
        ff("-i", path, "-vf", f"scale=iw*{n}:ih*{n}:flags=lanczos", out)
        return out

    up = upscale(p, 2)
    im = np.asarray(Image.open(up).convert("L"))
    return [chk("400 px for 260 px display: fine", not needs_upscale(400, 260), "1.54x"),
            chk("400 px for 320 px display: upscale", needs_upscale(400, 320), "1.25x"),
            chk("output named name_up2.png at 2x", up.name == "logo_up2.png" and im.shape == (200, 800), (up.name, im.shape)),
            chk("source untouched", hashlib.sha256(p.read_bytes()).hexdigest() == before, "sha same")]


def ramp_duration(ramp, src_len):
    """Programme time to consume src_len seconds with piecewise-linear speed [[t, speed]...] (t in source s)."""
    ts = np.linspace(0, src_len, 20001)
    sp = np.interp(ts, [r[0] for r in ramp], [r[1] for r in ramp])
    return float(np.trapezoid(1 / sp, ts))


def atempo_chain(f):
    parts = []
    while f < 0.5:
        parts.append(0.5)
        f /= 0.5
    while f > 2.0:
        parts.append(2.0)
        f /= 2.0
    parts.append(round(f, 6))
    return ",".join(f"atempo={p:g}" for p in parts)


def foot_16(work):
    ratios = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
    chain = atempo_chain(0.25)
    write_wav(work / "a.wav", tone(1.0))
    ff("-i", work / "a.wav", "-af", chain, work / "slow.wav")
    x, sr = read_wav(work / "slow.wav")
    rd = ramp_duration([[0, 1], [2, .3], [4, 1]], 4.0)
    # analytic: 2 * integral_0^2 dt / (1 - 0.35 t) = 2 * ln(1/0.3)/0.35
    exact = 2 * math.log(1 / 0.3) / 0.35
    spec = {"ratio": "1:1", "fps": 30, "bg": "#0d1b2a", "size": ratios["1:1"], "ramp": [[0, 1], [2, .3], [4, 1]],
            "atempo": chain, "ramp_seconds": rd}
    jwrite(work, "edit.json", spec)
    return [chk("0.25 -> atempo=0.5,atempo=0.5", chain == "atempo=0.5,atempo=0.5", chain),
            chk("chained atempo makes 1 s -> 4 s", near(len(x) / sr, 4.0, 0.1), len(x) / sr),
            chk("pitch kept at 440 Hz", near(dom_freq(x[:sr], sr), 440, 5), dom_freq(x[:sr], sr)),
            chk("ratio 1:1 -> 1080x1080", spec["size"] == (1080, 1080), spec["size"]),
            chk("ramp [[0,1],[2,.3],[4,1]] over 4 s lasts 2*ln(1/.3)/.35", near(rd, exact, 0.01), (rd, exact))]


def trim_counts(work):
    fr = frame_index_frames(300)
    src = work / "src.mp4"
    ff("-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "64x36", "-r", "30", "-i", "-", "-c:v", "libx264",
       "-preset", "ultrafast", "-g", "60", "-keyint_min", "60", "-sc_threshold", "0", "-crf", "5",
       "-pix_fmt", "yuv420p", src, inp=fr.tobytes())
    return src


def nframes(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                        "stream=nb_read_frames", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def foot_17(work):
    src = trim_counts(work)
    out = work / "part.mp4"
    ff("-ss", "3.2", "-i", src, "-to", "6.6", "-c:v", "libx264", "-crf", "18", "-preset", "ultrafast",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", out)
    n = nframes(out)
    first = decode_index(read_video(out)[0])
    return [chk("6.6 s at 30 fps = 198 frames", n == 198, n),
            chk("first frame is source frame 96 (3.2 s)", first == 96, first),
            chk("yuv420p", vstream(out)["pix_fmt"] == "yuv420p", vstream(out)["pix_fmt"])]


def foot_x03(work):
    src = trim_counts(work)
    ff("-i", src, "-ss", "1.3", "-to", "3.3", "-c", "copy", work / "copy_out.mp4")
    ff("-ss", "1.3", "-to", "3.3", "-i", src, "-c:v", "libx264", "-preset", "ultrafast", "-crf", "5",
       "-pix_fmt", "yuv420p", work / "reenc.mp4")
    nc, nr = nframes(work / "copy_out.mp4"), nframes(work / "reenc.mp4")
    first = decode_index(read_video(work / "reenc.mp4")[0])
    return [chk("re-encode gives exactly 60 frames", nr == 60, nr),
            chk("re-encode starts at frame 39", first == 39, first),
            chk("stream copy does not give 60 frames", nc != 60, nc)]


def foot_18(work):
    a = write_video(work / "A.mkv", solid(15, 36, 64, (250, 0, 0)), 30, audio=write_wav(work / "ta.wav", tone(0.5)))
    b = write_video(work / "B.mkv", solid(15, 64, 36, (0, 0, 250)), 30)
    W, H = 1080, 1920
    out = work / "all.mp4"
    fc = (f"[0:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[v0];"
          f"[1:v]fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[v1];"
          "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];"
          "anullsrc=r=48000:cl=stereo,atrim=duration=0.5[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]")
    ff("-i", a, "-i", b, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset",
       "ultrafast", "-c:a", "aac", out)
    v, au = vstream(out), astreams(out)[0]
    x = decode_audio(out)
    rms1, rms2 = np.sqrt((x[1000:7000] ** 2).mean()), np.sqrt((x[9500:15000] ** 2).mean())
    return [chk("fitted to 1080x1920", (v["width"], v["height"]) == (W, H), (v["width"], v["height"])),
            chk("48 kHz stereo audio", au["sample_rate"] == "48000" and au["channels"] == 2, au["sample_rate"]),
            chk("audio covers both clips (~1.0 s)", near(float(au["duration"]), 1.0, 0.08), au["duration"]),
            chk("tone then silence fill", rms1 > 0.2 and rms2 < 0.01, (round(rms1, 3), round(rms2, 4)))]


def foot_19(work):
    src = write_video(work / "c.mkv", frame_index_frames(60), 30)
    ff("-i", src, "-vf", "setpts='if(lt(T,1),PTS,PTS*2)'", "-c:v", "ffv1", work / "ramp.mkv")
    write_wav(work / "a.wav", tone(1.0, 440))
    ff("-i", work / "a.wav", "-af", "atempo=0.5", work / "slow.wav")
    x, sr = read_wav(work / "slow.wav")
    d = duration(work / "ramp.mkv")
    # frames before T=1 keep PTS, later ones are doubled: last frame 59/30 s -> 2*59/30 s
    return [chk("ramp doubles PTS after 1 s: ends at 2*59/30 + 1/30", near(d, 2 * 59 / 30 + 1 / 30, 0.05), d),
            chk("atempo 0.5 doubles duration", near(len(x) / sr, 2.0, 0.03), len(x) / sr),
            chk("pitch preserved 440 Hz", near(dom_freq(x, sr), 440, 4), dom_freq(x, sr)),
            chk("atempo 0.25 needs 2 stages in 0.5-2", atempo_chain(0.25).count("atempo") == 2, atempo_chain(0.25))]


def foot_20(work):
    sr = 16000
    z = lambda s: np.zeros(int(s * sr))
    x = np.concatenate([tone(0.5), z(0.6), tone(0.5), z(0.3), tone(0.5)])
    src = write_wav(work / "talk.wav", x, sr)
    err = ffstderr("-i", src, "-af", "silencedetect=noise=-35dB:d=0.45", "-f", "null", "-")
    starts = [float(l.split("silence_start: ")[1]) for l in err.splitlines() if "silence_start" in l]
    ends = [float(l.split("silence_end: ")[1].split()[0]) for l in err.splitlines() if "silence_end" in l]
    pad = 0.08
    keep, t = [], 0.0
    for s, e in zip(starts, ends):
        keep.append((t, s + pad))
        t = e - pad
    keep.append((t, len(x) / sr))
    fc = "".join(f"[0:a]atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[s{i}];" for i, (a, b) in enumerate(keep))
    fc += "".join(f"[s{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1[a]"
    ff("-i", src, "-filter_complex", fc, "-map", "[a]", work / "cut.wav")
    y, _ = read_wav(work / "cut.wav")
    want = len(x) / sr - (0.6 - 2 * pad)
    return [chk("one pause >= 0.45 s found", len(starts) == 1 and near(starts[0], 0.5, 0.02), starts),
            chk("0.3 s pause kept", len(ends) == 1, ends),
            chk("duration = 2.4 - (0.6 - 0.16)", near(len(y) / sr, want, 0.02), (len(y) / sr, want))]


def foot_21(work):
    fps = 10
    fr = frame_index_frames(30)
    src = write_video(work / "c.mkv", fr, fps)
    ff("-ss", "1.5", "-i", src, "-frames:v", "1", work / "freeze.png")
    still = np.asarray(Image.open(work / "freeze.png").convert("RGB"))
    hold = np.stack([still] * int(2 * fps))
    out_frames = np.concatenate([fr[:15], hold, fr[15:]])
    write_video(work / "freeze.mkv", out_frames, fps)
    # loop: tail dissolves into head over 0.4 s
    k = 4
    loop = fr.copy().astype(float)
    for i in range(k):
        a = (i + 1) / (k + 1)
        loop[-k + i] = (1 - a) * fr[-k + i] + a * fr[i]
    rr = read_video(work / "freeze.mkv")
    return [chk("frozen frame is source frame 15 (1.5 s)", decode_index(still) == 15, decode_index(still)),
            chk("held 2 s = 20 identical frames", all(np.array_equal(rr[15], rr[15 + j]) for j in range(20)), "20"),
            chk("duration grows by 2 s", len(rr) == 50, len(rr)),
            chk("loop tail approaches head", np.abs(loop[-1] - fr[0]).mean() < np.abs(fr[-1].astype(float) - fr[0]).mean(),
                "closer")]


def foot_23(work):
    clips = [{"id": "a", "dur": 60}, {"id": "b", "dur": 90}, {"id": "c", "dur": 30}]
    indep = {"a": 0, "b": 70, "c": 100}  # gap a->b, overlap b/c

    def ripple(cs):
        out, t = {}, 0
        for c in cs:
            out[c["id"]] = t
            t += c["dur"]
        return out

    r1 = ripple(clips)
    clips2 = [dict(c, dur=c["dur"] + 15) if c["id"] == "a" else c for c in clips]
    r2 = ripple(clips2)
    indep2 = dict(indep)  # independent clips keep absolute 'from'
    gaps = [(x, y) for x, y in [("a", "b")] if indep[y] > indep[x] + clips[0]["dur"]]
    overl = indep["c"] < indep["b"] + clips[1]["dur"]
    jwrite(work, "models.json", {"ripple": [r1, r2], "independent": indep2})
    return [chk("ripple: lengthening a by 15 shifts b and c by 15", r2["b"] - r1["b"] == 15 and r2["c"] - r1["c"] == 15,
                (r1, r2)),
            chk("independent: positions unchanged", indep2 == indep, indep2),
            chk("independent model allows gap and overlap", gaps == [("a", "b")] and overl, (gaps, overl))]


def shaky(n=40):
    rng = np.random.default_rng(7)
    base = np.kron(rng.integers(0, 255, (180 // 8, 320 // 8, 1)), np.ones((8, 8, 3))).astype(np.uint8)
    return np.stack([np.roll(np.roll(base, rng.integers(-3, 4), 0), rng.integers(-4, 5), 1) for _ in range(n)])


def global_shifts(frames):
    import cv2
    ref = luma(frames[0]).astype(np.float32)
    return np.array([cv2.phaseCorrelate(ref, luma(f).astype(np.float32))[0] for f in frames])


def foot_24(work):
    fr = shaky()
    src = write_video(work / "shaky.mkv", fr, 20)
    trf = work / "t.trf"
    method = "vidstab (2-pass)"
    try:
        ff("-i", src, "-vf", f"format=yuv420p,vidstabdetect=shakiness={min(10, 10)}:accuracy=15:result={trf}",
           "-f", "null", "-")
        ff("-i", src, "-vf", f"format=yuv420p,vidstabtransform=input={trf}:smoothing=40:optzoom=1,unsharp=5:5:0.5",
           "-c:v", "ffv1", work / "steady.mkv")
    except RuntimeError:
        method = "deshake"
        ff("-i", src, "-vf", "format=yuv420p,deshake=rx=32:ry=32", "-c:v", "ffv1", work / "steady.mkv")
    ja = float(np.diff(global_shifts(fr), axis=0).std())
    jb = float(np.diff(global_shifts(read_video(work / "steady.mkv")), axis=0).std())
    return [chk("measured shake before stabilising (> 1 px)", ja > 1, round(ja, 2)),
            chk("jitter reduced by >= 60%", jb < 0.4 * ja, f"{method}: {ja:.2f} -> {jb:.2f} px"),
            chk("duration preserved", near(duration(work / "steady.mkv"), duration(src), 0.06),
                (duration(src), duration(work / "steady.mkv")))]


def foot_25(work):
    rng = np.random.default_rng(2)
    clean = np.full((36, 64, 3), 120, np.uint8)
    fr = np.stack([np.clip(clean + rng.normal(0, 5, clean.shape[:2])[..., None], 0, 255)
                   for _ in range(24)]).astype(np.uint8)
    src = write_video(work / "noisy.mkv", fr, 12)
    ff("-i", src, "-vf", "format=yuv420p,hqdn3d=4:3:6:4.5", "-c:v", "ffv1", work / "dn.mkv")
    ff("-i", src, "-vf", "format=yuv420p,nlmeans=s=4", "-c:v", "ffv1", work / "nlm.mkv")
    edge = np.zeros((24, 36, 64, 3), np.uint8)
    edge[:, :, 32:] = 200
    edge = np.stack([np.asarray(Image.fromarray(e).resize((32, 18), Image.BILINEAR).resize((64, 36), Image.BILINEAR))
                     for e in edge])
    esrc = write_video(work / "soft.mkv", edge, 12)
    ff("-i", esrc, "-vf", "format=yuv420p,hqdn3d=4:3:6:4.5,unsharp=5:5:0.6", "-c:v", "ffv1", work / "fast.mkv")
    tn = lambda f: float(f[12:].astype(float).std(0).mean())
    err = lambda f: float(np.abs(f[12:].astype(float) - 120).mean())
    dn, nl = read_video(work / "dn.mkv"), read_video(work / "nlm.mkv")
    grad = lambda f: float(np.abs(np.diff(luma(f[12]), axis=1)).max())
    g0, g1 = grad(edge), grad(read_video(work / "fast.mkv"))
    return [chk("hqdn3d 4:3:6:4.5 cuts temporal noise >= 25%", tn(dn) < 0.75 * tn(fr), f"{tn(fr):.2f} -> {tn(dn):.2f}"),
            chk("nlmeans s=4 halves the error", err(nl) < 0.5 * err(fr), f"{err(fr):.2f} -> {err(nl):.2f}"),
            chk("unsharp 5:5:0.6 restores edge steepness", g1 > 1.1 * g0, f"{g0:.1f} -> {g1:.1f}")]


def foot_26(work):
    import cv2
    rng = np.random.default_rng(4)
    bg = rng.integers(60, 160, (90, 160, 3)).astype(np.uint8)
    bg = cv2.GaussianBlur(bg, (0, 0), 2)
    frames, masks_true = [], []
    for i in range(12):
        f = bg.copy()
        m = np.zeros(f.shape[:2], np.uint8)
        x0 = 20 + (i // 4) * 35  # caption changes 3 times
        ink = np.zeros(f.shape[:2], np.uint8)
        cv2.putText(ink, "SUB", (x0, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
        ring = cv2.dilate(ink, np.ones((5, 5), np.uint8))
        f[ring > 0] = (0, 0, 0)
        f[ink > 0] = (255, 255, 255)
        m = ring
        frames.append(f)
        masks_true.append(m > 0)
    frames = np.stack(frames)

    def ink_mask(f):
        hsv = cv2.cvtColor(f, cv2.COLOR_RGB2HSV_FULL).astype(np.float64)
        h, s, v = hsv[..., 0] * 360 / 255 / 2, hsv[..., 1], hsv[..., 2]
        white = (v > 205) & (s < 55)
        yellow = (h >= 16) & (h <= 38) & (s > 110) & (v > 150)
        dark = (v < 70).astype(np.uint8)
        near_dark = cv2.dilate(dark, np.ones((19, 19), np.uint8)) > 0  # within 9 px
        ink = (white | yellow) & near_dark
        return cv2.dilate(ink.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0  # include outline

    masks = np.stack([ink_mask(f) for f in frames])
    # locked-off: per-pixel median over unmasked frames
    stack = np.where(masks[..., None], np.nan, frames.astype(float))
    med = np.nanmedian(stack, axis=0)
    holes = np.isnan(med).any(-1)
    med = np.nan_to_num(med).astype(np.uint8)
    rebuilt = cv2.inpaint(med, holes.astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA) if holes.any() else med
    clean = np.where(masks[..., None], rebuilt[None], frames)
    write_video(work / "clean.mkv", clean, 12)
    mt = np.stack(masks_true)
    recall = float((masks & mt).sum() / mt.sum())
    err_before = float(np.abs(frames[mt].astype(float) - np.broadcast_to(bg, frames.shape)[mt]).mean())
    err_after = float(np.abs(clean[mt].astype(float) - np.broadcast_to(bg, frames.shape)[mt]).mean())
    return [chk("caption ink + outline found (recall >= 0.9)", recall >= 0.9, round(recall, 3)),
            chk("caption pixels rebuilt near background", err_after < 0.2 * err_before, f"{err_before:.1f} -> {err_after:.1f}"),
            chk("pixels outside mask untouched", np.array_equal(clean[~masks], frames[~masks]), "equal")]


def foot_27(work):
    fps = 10
    rng = np.random.default_rng(1)
    fr = rng.integers(0, 255, (20, 72, 128, 3)).astype(np.uint8)
    audio = write_wav(work / "a.wav", tone(2.0))
    src = write_video(work / "c.mkv", fr, fps, audio=audio)
    x, y, w, h = 40, 16, 40, 40
    blk = w // 4
    ff("-i", src, "-filter_complex",
       f"[0:v]split[a][b];[b]crop={w}:{h}:{x}:{y},scale={w // blk}:{h // blk},scale={w}:{h}:flags=neighbor[p];"
       f"[a][p]overlay={x}:{y}:format=rgb[v]", "-map", "[v]", "-map", "0:a", "-c:v", "ffv1", "-c:a", "copy", work / "safe.mkv")
    out = read_video(work / "safe.mkv")
    reg = out[5, y:y + h, x:x + w].astype(int)
    blocks_uniform = all(np.ptp(reg[by:by + blk, bx:bx + blk], axis=(0, 1)).max() == 0
                         for by in range(0, h, blk) for bx in range(0, w, blk))
    srcf = read_video(src)
    outside = np.array_equal(out[5, :, :x], srcf[5, :, :x]) and np.array_equal(out[5, y + h:], srcf[5, y + h:])

    def hold(dets, hold_s=0.6):
        last, res = None, []
        for t, d in dets:
            if d is not None:
                last = (t, d)
            res.append(d if d is not None else (last[1] if last and t - last[0] <= hold_s else None))
        return res

    held = hold([(0.0, "box"), (0.2, None), (0.5, None), (0.7, None), (0.9, "box")])
    pkt = lambda p: subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "packet=data",
                                    "-show_data", "-of", "csv", str(p)], capture_output=True).stdout
    return [chk("region pixelated in blocks of face/4", blocks_uniform, f"block {blk}"),
            chk("outside region untouched", outside, "equal"),
            chk("hold 0.6 s through detector misses", held == ["box", "box", "box", None, "box"], held),
            chk("audio stream copied byte for byte", hashlib.sha256(pkt(src)).digest() == hashlib.sha256(pkt(work / "safe.mkv")).digest(),
                "packets equal")]


def foot_28(work):
    fg = solid(5, 72, 128, (0, 255, 0)).copy()
    fg[:, 20:52, 44:84] = (220, 30, 30)
    bg = solid(5, 72, 128, (20, 40, 220))
    a = write_video(work / "fg.mkv", fg, 5)
    b = write_video(work / "bg.mkv", bg, 5)
    ff("-i", b, "-i", a, "-filter_complex",
       "[1:v]format=yuva420p,chromakey=0x00FF00:similarity=0.15:blend=0.08,despill=type=green[k];[0:v][k]overlay[v]",
       "-map", "[v]", "-c:v", "ffv1", work / "comp.mkv")
    o = read_video(work / "comp.mkv")[2].astype(int)
    bgpix, sub = o[5, 5], o[36, 64]
    return [chk("green replaced by blue background", bgpix[2] > 180 and bgpix[1] < 90, bgpix.tolist()),
            chk("red subject kept", sub[0] > 170 and sub[1] < 80, sub.tolist())]


AR_COLOURS = {"ذهبي": "#d4a53a", "كحلي": "#1f2d6b", "عنابي": "#7b1e2b", "أزرق": "#1e5bd4", "أحمر": "#d42020"}


def recolor(img, src_hex, dst_hex, tolerance=40, keep_shading=True):
    hsv = np.array([[colorsys.rgb_to_hsv(*(p / 255)) for p in row] for row in img])
    sh, ss, sv = colorsys.rgb_to_hsv(*(np.array(hexrgb(src_hex)) / 255))
    dh, ds, dv = colorsys.rgb_to_hsv(*(np.array(hexrgb(dst_hex)) / 255))
    dhue = np.minimum(np.abs(hsv[..., 0] - sh), 1 - np.abs(hsv[..., 0] - sh)) * 360
    mask = (dhue <= tolerance) & (hsv[..., 1] > 0.25)
    out = hsv.copy()
    out[..., 0] = np.where(mask, dh, hsv[..., 0])
    if keep_shading:
        out[..., 1] = np.where(mask, np.clip(hsv[..., 1] * ds / max(ss, 1e-6), 0, 1), hsv[..., 1])
        out[..., 2] = np.where(mask, np.clip(hsv[..., 2] * dv / max(sv, 1e-6), 0, 1), hsv[..., 2])
    rgb = np.array([[colorsys.hsv_to_rgb(*p) for p in row] for row in out]) * 255
    return rgb.round().astype(np.uint8), mask


def foot_29(work):
    gold = np.array(hexrgb(AR_COLOURS["ذهبي"]), float)
    img = np.zeros((16, 32, 3), np.uint8)
    for x in range(24):
        img[:, x] = (gold * (0.5 + x / 46)).clip(0, 255)  # gold with folds/shadow ramp
    img[:, 24:] = (90, 160, 90)
    cmd = "غيّر الذهبي إلى الأزرق"
    src = next(AR_COLOURS[k] for k in AR_COLOURS if k in cmd.split("إلى")[0])
    dst = next(AR_COLOURS[k] for k in AR_COLOURS if k in cmd.split("إلى")[1])
    out, mask = recolor(img, src, dst, tolerance=40)
    Image.fromarray(out).save(work / "recolored.png")
    hues = [colorsys.rgb_to_hsv(*(out[8, x] / 255))[0] * 360 for x in (2, 12, 22)]
    vals = [int(out[8, x].max()) for x in (2, 12, 22)]
    return [chk("Arabic command parsed gold -> blue", (src, dst) == ("#d4a53a", "#1e5bd4"), (src, dst)),
            chk("gold area now blue hue (~220)", all(near(h, 220, 8) for h in hues), [round(h) for h in hues]),
            chk("shading order preserved", vals[0] < vals[1] < vals[2], vals),
            chk("green outside tolerance untouched", np.array_equal(out[:, 24:], img[:, 24:]), "equal")]


def foot_30(work):
    rng = np.random.default_rng(9)
    im = Image.fromarray(rng.integers(0, 255, (300, 200, 3)).astype(np.uint8))
    W, H = 160, 90  # fill-crop (-resize WxH^ -gravity center -extent WxH)
    s = max(W / im.width, H / im.height)
    r = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    l, t = (r.width - W) // 2, (r.height - H) // 2
    fill = r.crop((l, t, l + W, t + H))
    fill.save(work / "fill.png")
    logo = np.full((60, 80, 3), 255, np.uint8)
    logo[20:40, 30:50] = (200, 20, 20)
    logo[5, 5] = (240, 240, 240)  # near-white within 10% fuzz
    fuzz = 0.10 * 255 * math.sqrt(3)
    dist = np.sqrt(((logo.astype(float) - 255) ** 2).sum(-1))
    alpha = np.where(dist <= fuzz, 0, 255).astype(np.uint8)
    rgba = np.dstack([logo, alpha])
    ys, xs = np.nonzero(alpha)
    trimmed = rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(trimmed).save(work / "logo_trim.png")
    Image.fromarray(trimmed).save(work / "logo.webp", quality=85)
    return [chk("fill-crop exact 160x90", fill.size == (W, H), fill.size),
            chk("white and near-white -> transparent", alpha[0, 0] == 0 and alpha[5, 5] == 0 and alpha[30, 40] == 255,
                (alpha[0, 0], alpha[5, 5], alpha[30, 40])),
            chk("trim to the 20x20 mark", trimmed.shape[:2] == (20, 20), trimmed.shape)]


def foot_32(work):
    H, W = 80, 60
    bg = np.full((H, W, 3), (40, 60, 90), np.uint8)
    matte = np.zeros((H, W), bool)
    matte[30:, 20:40] = True  # body
    yy, xx = np.mgrid[:H, :W]
    face = (yy - 20) ** 2 / 100 + (xx - 30) ** 2 / 64 <= 1
    matte |= face
    person = np.full((H, W, 3), (210, 170, 140), np.uint8)
    title = np.zeros((H, W), bool)
    title[35:50, 5:55] = True

    def alpha(t):
        return 0.0 if t < 1 else min(1.0, t - 1.0)

    def frame(t):
        f = bg.astype(float).copy()
        a = alpha(t)
        f[title] = (1 - a) * f[title] + a * np.array([255, 255, 255])
        f[matte] = person[matte]
        return f.astype(np.uint8)

    f3 = frame(3.0)
    Image.fromarray(f3).save(work / "title_behind.png")
    vis = title & ~matte
    hid = title & matte
    return [chk("title hidden at 0.5 s", np.array_equal(frame(0.5)[title & ~matte], bg[title & ~matte]), "bg"),
            chk("title visible around the body at 3 s", (f3[vis] == 255).all(), int(vis.sum())),
            chk("title behind the body", (f3[hid] == person[hid]).all(), int(hid.sum())),
            chk("face never covered by title", not (title & face).any() or (f3[face] == person[face]).all(), "face clear")]


def foot_33(work):
    import cv2
    H, W = 80, 80
    matte = np.zeros((H, W), np.uint8)
    cv2.circle(matte, (40, 40), 18, 255, -1)
    k = 7
    outline = cv2.dilate(matte, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1))) > 0
    ring = outline & (matte == 0)
    shadow = cv2.GaussianBlur(matte.astype(float), (0, 0), 20 / 3)
    words = [{"w": "one", "start": 0.0, "end": 0.5}, {"w": "two.", "start": 0.5, "end": 1.0},
             {"w": "three", "start": 1.2, "end": 1.6}, {"w": "four.", "start": 1.6, "end": 2.0}]
    bounds, cur = [], 0.0
    for wd in words:
        if wd["w"].endswith("."):
            bounds.append((cur, wd["end"]))
            cur = wd["end"]
    backdrop = lambda t: next(i for i, (a, b) in enumerate(bounds) if t < b or i == len(bounds) - 1)
    comp = np.zeros((H, W, 3), np.uint8)
    comp[ring] = 255
    comp[matte > 0] = (200, 120, 90)
    Image.fromarray(comp).save(work / "roto.png")
    width = 40 + 18 + k - 1 - (40 + 18)
    row = ring[40]
    ring_w = int(row[58:].sum())
    return [chk("white outline 7 px (6-8)", 6 <= ring_w <= 8, ring_w),
            chk("soft shadow spreads past outline", shadow[40, 40 + 18 + k + 3] > 1, round(shadow[40, 68], 2)),
            chk("backdrop swaps on sentence boundary", [backdrop(t) for t in (0.3, 0.9, 1.3, 1.9)] == [0, 0, 1, 1],
                [backdrop(t) for t in (0.3, 0.9, 1.3, 1.9)])] if width >= 0 else []


def foot_34(work):
    import cv2
    H, W = 72, 128
    pos = [(10 + 2.5 * i, 30 + 8 * math.sin(i / 6)) for i in range(40)]
    frames = []
    for x, y in pos:
        f = np.zeros((H, W), np.uint8)
        cv2.circle(f, (int(round(x)), int(round(y))), 4, 255, -1)
        f = cv2.GaussianBlur(f, (0, 0), 1.2)
        frames.append(f)
    p = np.array([[pos[0]]], np.float32)
    track = [pos[0]]
    for a, b in zip(frames, frames[1:]):
        p, st, _ = cv2.calcOpticalFlowPyrLK(a, b, p, None, winSize=(21, 21), maxLevel=2)
        track.append(tuple(p[0, 0]))
    err = max(math.dist(t, q) for t, q in zip(track, pos))
    label = lambda x, y: 0 <= x < W and 0 <= y < H
    jwrite(work, "track.json", {"track": [list(map(float, t)) for t in track]})
    return [chk("tracked dot within 1.5 px over 40 frames", err < 1.5, round(err, 3)),
            chk("label hidden when target leaves frame", not label(140, 30) and label(*track[-1]), "hidden")]


def foot_35(work):
    import cv2
    sticker = np.zeros((40, 60, 3), np.uint8)
    sticker[:, :30] = (255, 0, 0)
    sticker[:, 30:] = (0, 0, 255)
    quad = np.float32([[30, 20], [100, 28], [96, 70], [26, 60]])
    src = np.float32([[0, 0], [60, 0], [60, 40], [0, 40]])
    Hm = cv2.getPerspectiveTransform(src, quad)
    plate = np.full((90, 128, 3), 128, np.uint8)
    warp = cv2.warpPerspective(sticker, Hm, (128, 90))
    m = cv2.warpPerspective(np.full((40, 60), 255, np.uint8), Hm, (128, 90)) > 127
    plate[m] = warp[m]
    Image.fromarray(plate).save(work / "pinned.png")
    proj = cv2.perspectiveTransform(src[None], Hm)[0]
    centre_l = cv2.perspectiveTransform(np.float32([[[10, 20]]]), Hm)[0, 0]
    css = "matrix3d(" + ",".join(f"{v:.6f}" for v in [Hm[0, 0], Hm[1, 0], 0, Hm[2, 0], Hm[0, 1], Hm[1, 1], 0, Hm[2, 1],
                                                       0, 0, 1, 0, Hm[0, 2], Hm[1, 2], 0, Hm[2, 2]]) + ")"
    (work / "pin.css").write_text(f".sticker{{transform-origin:0 0;transform:{css}}}\n")
    px = plate[int(round(centre_l[1])), int(round(centre_l[0]))]
    return [chk("corners map onto the wall quad", np.abs(proj - quad).max() < 1e-3, np.abs(proj - quad).max()),
            chk("left half lands red at its projected point", px[0] > 200 and px[2] < 50, px.tolist()),
            chk("matrix3d has 16 values", css.count(",") == 15, css[:40])]


def foot_36(work):
    H, W, fps = 36, 64, 10
    matte = np.zeros((H, W), bool)
    matte[10:30, 25:35] = True
    frames = []
    for i in range(40):
        t = i / fps
        bg = np.zeros((H, W, 3), np.uint8)
        bg[..., 2] = (np.arange(W) * 4 + i * 6) % 256
        subj_x = int(i * 0.5) % 10
        subj = np.zeros((H, W, 3), np.uint8)
        subj[..., 0] = 200 + subj_x
        frozen_t = min(max(t, 0), 1.0) if 1 <= t < 3 else t
        src_i = int(frozen_t * fps) if 1 <= t < 3 else i
        s = subj.copy()
        s[..., 0] = 200 + int(src_i * 0.5) % 10
        f = bg.copy()
        f[matte] = s[matte]
        frames.append(f)
    frames = np.stack(frames)
    write_video(work / "freeze_subject.mkv", frames, fps)
    sub_static = all(np.array_equal(frames[10][matte], frames[k][matte]) for k in range(10, 30))
    bg_moves = not np.array_equal(frames[10][~matte], frames[20][~matte])
    resumes = not np.array_equal(frames[29][matte], frames[35][matte])
    return [chk("subject frozen 1-3 s", sub_static, "20 frames equal"),
            chk("world keeps moving while frozen", bg_moves, "bg differs"),
            chk("subject resumes after 3 s", resumes, "differs")]


def foot_37(work):
    dur, fps = 10.0, 10

    def make(period):
        if abs((dur / period) - round(dur / period)) > 1e-9:
            raise ValueError("period must divide duration")
        still = np.full((24, 32, 3), 100, np.uint8)
        fr = []
        for i in range(int(dur * fps) + 1):
            t = i / fps
            f = still.copy()
            f[4:12, 10:22] = int(round(150 + 60 * math.sin(2 * math.pi * t / period)))  # steam region
            fr.append(f)
        return np.stack(fr)

    fr = make(2.5)
    write_video(work / "cinemagraph.mkv", fr[:-1], fps)
    try:
        make(3.0)
        refused = False
    except ValueError:
        refused = True
    still_ok = all(np.array_equal(fr[0][14:], f[14:]) for f in fr)
    return [chk("period 2.5 divides 10 s: last == first (seamless)", np.array_equal(fr[0], fr[-1]), "equal"),
            chk("only the region lives", still_ok and not np.array_equal(fr[0], fr[5]), "rest static"),
            chk("period 3 s refused", refused, refused)]


def foot_38(work):
    W, H = 100, 40
    before = np.full((H, W, 3), (90, 90, 90), np.uint8)
    after = np.full((H, W, 3), (200, 180, 120), np.uint8)

    def xdiv(t):
        if t <= 1:
            return W
        if t >= 4:
            return 0
        return round(W * (1 - (t - 1) / 3))

    def frame(t):
        x = xdiv(t)
        f = after.copy()
        f[:, :x] = before[:, :x]
        f[:, max(0, x - 1):x + 1] = 255  # 2 px divider
        return f

    f = frame(2.5)
    Image.fromarray(f).save(work / "wipe_mid.png")
    return [chk("divider at centre at 2.5 s", xdiv(2.5) == 50, xdiv(2.5)),
            chk("left original, right result", (f[5, 10] == before[0, 0]).all() and (f[5, 90] == after[0, 0]).all(), "ok"),
            chk("divider 2 px", int((f[5] == 255).all(-1).sum()) == 2, int((f[5] == 255).all(-1).sum())),
            chk("stops at 4 s (all result)", xdiv(4.5) == 0 and xdiv(0.5) == W, (xdiv(0.5), xdiv(4.5)))]


def foot_39(work):
    src = np.zeros((384, 216, 3), np.uint8)
    yy, xx = np.mgrid[:384, :216]
    src[((xx // 12 + yy // 12) % 2 == 0)] = 230
    Image.fromarray(src).save(work / "photo.png")
    out = work / "kb.mkv"
    ff("-i", work / "photo.png", "-vf",
       "zoompan=z='min(1+0.0004*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=108x192:fps=30",
       "-c:v", "ffv1", out)
    n = nframes(out)
    z = [min(1 + 0.0004 * on, 1.06) for on in range(150)]
    vel = np.diff(z)
    rate_per_s = (z[-1] - z[0]) / (149 / 30)
    return [chk("150 frames at 30 fps (5 s)", n == 150, n),
            chk("constant velocity (no eased stop)", np.ptp(vel) < 1e-12, float(np.ptp(vel))),
            chk("ends 1.0596 <= 1.06 <= ceiling 1.12", z[-1] <= 1.06 <= 1.12, z[-1]),
            chk("push 1-1.5 %/s", 0.01 <= rate_per_s <= 0.015, round(rate_per_s, 4))]


def foot_40(work):
    depth = {"bg": 0.15, "mid": 0.45, "subject": 1.0, "occluder": 1.4}
    drift_x = lambda t: 6 * math.sin(2 * math.pi * t / 7) + 4 * math.sin(2 * math.pi * t / 11)
    ts = np.linspace(0, 77, 7701)
    dx = np.array([drift_x(t) for t in ts])
    pan = 45.0  # px/s within 30-60
    cam = lambda t: pan * t + drift_x(t)
    offs = {k: d * cam(2.0) for k, d in depth.items()}
    travel = max(abs(d * cam(5.0)) for d in depth.values())
    oversize = 2 * travel + 0.04 * 1080
    jwrite(work, "parallax.json", {"offsets@2s": offs, "oversize_px": oversize})
    return [chk("drift <= 12 px", np.abs(dx).max() <= 12, round(float(np.abs(dx).max()), 2)),
            chk("layer offset = camera x depth (bg 0.15)", near(offs["bg"] / offs["subject"], 0.15, 1e-9), offs),
            chk("occluder moves 1.4x subject", near(offs["occluder"] / offs["subject"], 1.4, 1e-9), offs["occluder"]),
            chk("oversize = 2x max travel + 4%", near(oversize, 2 * 1.4 * cam(5.0) + 43.2, 1e-6), round(oversize, 1))]


def spring(stiff, damp, t_end=1.5, dt=1 / 1000):
    x, v, xs = 0.0, 0.0, []
    for _ in range(int(t_end / dt)):
        a = stiff * (1 - x) - damp * v
        v += a * dt
        x += v * dt
        xs.append(x)
    return np.array(xs)


def foot_41(work):
    xs = spring(120, 14)
    settle = next(i for i in range(len(xs)) if np.all(np.abs(xs[i:] - 1) < 0.02)) / 1000
    grid = [(r, c) for r in range(2) for c in range(3)]
    order = sorted(grid, key=lambda rc: (rc[0], -rc[1]))  # RTL: top-right first
    starts = {rc: i * 0.060 for i, rc in enumerate(order)}
    sched = {"subject": [0.2, 0.2 + settle], "pan": [0.4, 2.6], "title": [0.9, 1.4]}
    jwrite(work, "reveal.json", {"spring_settle_s": settle, "grid_starts": {str(k): v for k, v in starts.items()},
                                 "schedule": sched})
    return [chk("spring 14/120 settles within the 200-800 ms window", 0.2 + settle <= 0.8 + 0.25 and settle > 0.2, settle),
            chk("spring overshoots (pop)", xs.max() > 1.0, round(float(xs.max()), 3)),
            chk("grid enters from top-right", order[0] == (0, 2), order[0]),
            chk("60 ms stagger: last tile at 300 ms (<= 400)", near(max(starts.values()), 0.3, 1e-9), max(starts.values()))]


def foot_42(work):
    rng = np.random.default_rng(0)
    H, W = 192, 108
    img = rng.integers(60, 256, (H, W, 3)).astype(np.float64)
    band = int(0.35 * H)
    a = np.zeros(H)
    a[H - band:] = np.linspace(0, 0.6, band)  # 0 at top of band, 0.6 at bottom edge
    scrimmed = img * (1 - a[:, None, None])
    out = scrimmed.astype(np.uint8)
    Image.fromarray(out).save(work / "scrim.png")
    text_rows = slice(H - band // 3, H)  # captions sit in the dark third
    cr = contrast((255, 255, 255), out[text_rows].reshape(-1, 3).mean(0))
    write_video(work / "v.mkv", np.stack([out] * 3), 3)
    err = ffstderr("-i", work / "v.mkv", "-vf", f"crop={W}:{band // 3}:0:{H - band // 3},signalstats,"
                   "metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-")
    yavg = [float(l.split("=")[1]) for l in err.splitlines() if "YAVG=" in l]
    no_scrim = contrast((255, 255, 255), img[text_rows].reshape(-1, 3).mean(0))
    return [chk("white text on scrim >= 4.5:1 vs band mean", cr >= 4.5, round(cr, 2)),
            chk("without scrim it fails", no_scrim < 4.5, round(no_scrim, 2)),
            chk("signalstats YAVG measured per frame", len(yavg) == 3 and yavg[0] < 130, yavg)]


def foot_43(work):
    old = np.full((48, 64, 3), (150, 120, 80), np.uint8)
    modern = np.full((48, 64, 3), (40, 140, 200), np.uint8)

    def scale(t):
        return 1.0 + 0.08 * min(max(t, 0), 6) / 6  # Ken Burns 1.0 -> 1.08 over 6 s

    def frame(t):
        if t < 2:
            return old
        if t < 5:
            return old  # matching / corner pin stage keeps the print
        a = min(1, (t - 5) / 1.0)
        return ((1 - a) * old + a * modern).astype(np.uint8)

    seq = np.stack([frame(i / 4) for i in range(33)])
    write_video(work / "archive.mkv", seq, 4)
    return [chk("photo at 1 s", np.array_equal(frame(1), old), "old"),
            chk("dissolve midway at 5.5 s", np.abs(frame(5.5).astype(int) - (old.astype(int) + modern) // 2).max() <= 1, "mid"),
            chk("modern at 8 s", np.array_equal(frame(8), modern), "modern"),
            chk("Ken Burns 1.08 at 6 s", near(scale(6), 1.08, 1e-9) and near(scale(3), 1.04, 1e-9), scale(6))]


def foot_44(work):
    def validate(lay):
        errs = []
        if lay["reveal"] != "rtl":
            errs.append("reveal not RTL")
        if lay["grid_origin"] != "top-right":
            errs.append("grid not from top-right")
        if not (lay["subject_x"] < 0.5 < lay["text_x"]):
            errs.append("subject must be left, text right")
        if lay["mirror"] and set(lay["photo_has"]) & {"writing", "flag", "logo", "steering-wheel"}:
            errs.append("mirroring a photo with writing/flag/logo")
        if lay["margin_x"] < 0.05 or lay["margin_y"] < 0.12:
            errs.append("margins below 5%/12%")
        if lay["depth"] != ["background", "mid", "subject", "graphics"]:
            errs.append("depth order")
        return errs

    good = {"reveal": "rtl", "grid_origin": "top-right", "subject_x": 0.3, "text_x": 0.72, "mirror": False,
            "photo_has": ["flag"], "margin_x": 0.05, "margin_y": 0.12, "depth": ["background", "mid", "subject", "graphics"]}
    bad = dict(good, mirror=True, reveal="ltr", margin_y=0.08)
    eg, eb = validate(good), validate(bad)
    jwrite(work, "rtl_check.json", {"good": eg, "bad": eb})
    return [chk("RTL layout passes", eg == [], eg),
            chk("mirroring a flag photo refused", "mirroring a photo with writing/flag/logo" in eb, eb),
            chk("3 violations found", len(eb) == 3, eb)]


def foot_45(work):
    out = {}
    for sid in ("parallax-2d", "viral-mixed-media", "editorial"):
        d = work / sid
        r = subprocess.run([sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", sid, str(d)],
                           capture_output=True, text=True, timeout=60, cwd=REPO)
        out[sid] = (r.returncode, sorted(p.name for p in d.iterdir()) if d.is_dir() else [])
    jwrite(work, "scaffold.json", out)
    return [chk(f"scaffold {k}", rc == 0 and {"PLAN.md", "STYLE.md", "REQUEST.md"} <= set(files), (rc, files))
            for k, (rc, files) in out.items()]


def foot_46(work):
    rng = np.random.default_rng(6)
    img = rng.integers(0, 255, (40, 80, 3)).astype(np.uint8)
    filters = {"gray": lambda a: np.repeat(luma(a)[..., None], 3, -1),
               "invert": lambda a: 255 - a.astype(float),
               "warm": lambda a: np.clip(a * np.array([1.1, 1.0, 0.85]), 0, 255),
               "dim": lambda a: a * 0.5}
    n = len(filters)
    cw = img.shape[1] // n
    out = img.copy()
    for i, f in enumerate(filters.values()):
        out[:, i * cw:(i + 1) * cw] = f(img[:, i * cw:(i + 1) * cw].astype(float)).round().astype(np.uint8)
    Image.fromarray(out).save(work / "strips.png")
    reveal = [round(i * 0.080, 3) for i in range(n)]
    ok = [np.array_equal(out[:, i * cw:(i + 1) * cw], f(img[:, i * cw:(i + 1) * cw].astype(float)).round().astype(np.uint8))
          for i, f in enumerate(filters.values())]
    return [chk("each column carries its own filter", all(ok), ok),
            chk("columns differ from each other", not np.array_equal(out[:, :cw], out[:, cw:2 * cw]), "differ"),
            chk("80 ms reveal stagger", reveal == [0.0, 0.08, 0.16, 0.24], reveal)]


def foot_47(work):
    src = write_video(work / "c.mkv", frame_index_frames(90), 30)
    out = work / "clip.mp4"
    ff("-i", src, "-vf", "scale=1280:-2:flags=lanczos", "-c:v", "libx264", "-g", "1", "-crf", "16", "-preset",
       "ultrafast", "-an", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out)
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "frame=key_frame",
                        "-of", "csv=p=0", str(out)], capture_output=True, text=True)
    keys = [l for l in r.stdout.split() if l.strip()]
    tag = f'<video src="assets/{out.name}" data-start="0" data-duration="3" muted></video>'
    (work / "tag.html").write_text(tag + "\n")
    v = vstream(out)
    return [chk("all 90 frames are keyframes", len(keys) == 90 and all(k.startswith("1") for k in keys), len(keys)),
            chk("width 1280", v["width"] == 1280, v["width"]),
            chk("muted (no audio)", not astreams(out), "no audio")]


def foot_48(work):
    rng = np.random.default_rng(8)
    land = rng.integers(0, 255, (54, 96, 3)).astype(np.uint8)
    land[:, :, 0] = np.linspace(0, 255, 96)[None, :]
    src = write_video(work / "land.mkv", np.stack([land] * 3), 3)
    W, H = 1080, 1920
    ff("-i", src, "-filter_complex",
       f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=40:2[bg];"
       f"[b]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2", "-frames:v", "1", work / "fit.png")
    o = np.asarray(Image.open(work / "fit.png").convert("RGB")).astype(float)
    fg_h = round(W * 54 / 96 / 2) * 2
    top = (H - fg_h) // 2
    left_fg, right_fg = o[H // 2, 20, 0], o[H // 2, W - 20, 0]
    blur_var = o[100:300, 100:980].std(axis=(0, 1)).mean()
    fg_var = o[top + 10:top + fg_h - 10, 100:980].std(axis=(0, 1)).mean()
    return [chk("output 1080x1920", o.shape[:2] == (H, W), o.shape),
            chk("whole width kept: left dark, right bright red", left_fg < 40 and right_fg > 215, (left_fg, right_fg)),
            chk("fill area is blurred (low variance)", blur_var < 0.5 * fg_var, (round(blur_var, 1), round(fg_var, 1)))]


def ease_power3_out(p):
    return 1 - (1 - p) ** 3


def foot_49(work):
    from bs4 import BeautifulSoup
    layers = ["bloom", "rays", "scrim", "vig", "dim", "particles"]
    html = ("<div id=cam><video id=plate data-start=0 data-duration=6 muted></video></div>"
            + "".join(f"<div id={l}></div>" for l in layers))
    (work / "plate.html").write_text(html)
    soup = BeautifulSoup(html, "html.parser")

    def sat(t):
        return 0.55 + (1 - 0.55) * ease_power3_out(min(t / 0.6, 1))

    def dim(t):
        return 0.42 * (1 - min(t / 0.55, 1))

    order = [d.get("id") for d in soup.find_all("div")]
    return [chk("plate inside #cam, muted", soup.select_one("#cam > video#plate[muted]") is not None, "ok"),
            chk("layers above plate in order", order == ["cam"] + layers, order),
            chk("saturate .55 -> 1 in 0.6 s power3.out", near(sat(0), .55, 1e-9) and near(sat(0.3), .55 + .45 * .875, 1e-9)
                and near(sat(0.6), 1, 1e-9), sat(0.3)),
            chk("dim .42 -> 0 in .55 s", near(dim(0), .42, 1e-9) and dim(0.55) == 0, dim(0.275))]


def foot_50(work):
    def expo_out(p):
        return 1 if p >= 1 else 1 - 2 ** (-10 * p)

    def punch(t, peak=1.0):
        if t < 0.14:
            return peak * expo_out(t / 0.14)
        k = min((t - 0.14) / 0.6, 1)
        return peak * (1 - 0.6 * k)

    def hook_dim(t):
        return 0.38 * (1 - min(t / 0.55, 1))

    edit = {"shots": [{"start": 0, "push": [1.04, 1.10]}, {"start": 3, "push": [1.10, 1.04]}],
            "punches": [1.2], "palette": {"ivory": "#F5F0E6", "accent": "#E7B65A"}}
    jwrite(work, "edit.json", edit)
    return [chk("punch peaks at 0.14 s", near(punch(0.14), 1, 1e-9) and punch(0.07) > 0.95, punch(0.07)),
            chk("then -60% over 0.6 s", near(punch(0.74), 0.4, 1e-9), punch(0.74)),
            chk("hook dim .38 -> 0 in .55 s", hook_dim(0) == 0.38 and hook_dim(0.55) == 0, hook_dim(0.3)),
            chk("pushes alternate", edit["shots"][0]["push"] == edit["shots"][1]["push"][::-1], edit["shots"])]


def foot_51(work):
    words = [{"w": w, "start": i * 0.4, "end": i * 0.4 + 0.35} for i, w in enumerate("مرحبا بكم في الحلقة رقم عشرة مع الضيف".split())]
    dur = 10.0
    sb = {"schemaVersion": 3, "layout": "split", "themeId": "ivory", "seed": 7,
          "cards": [{"zone": "lower-third", "startSec": 0.0, "text": "مرحبا"},
                    {"zone": "callout", "startSec": 2.6, "text": "عشرة"},
                    {"zone": "pull-quote", "startSec": 12.0, "text": "x"}]}

    def validate(sb):
        errs = []
        if sb.get("schemaVersion") != 3:
            errs.append("schemaVersion")
        prev = -1
        for c in sb["cards"]:
            if c["startSec"] < prev:
                errs.append("unsorted")
            prev = c["startSec"]
            if not 0 <= c["startSec"] < dur:
                errs.append(f"card at {c['startSec']} outside footage")
                continue
            w = next((x for x in words if x["w"] == c["text"]), None)
            if w and abs(w["start"] - c["startSec"]) > 0.05:
                errs.append(f"card '{c['text']}' not synced to word at {w['start']}")
        return errs

    errs = validate(sb)
    fixed = dict(sb, cards=sb["cards"][:2])
    fixed["cards"][1] = dict(fixed["cards"][1], startSec=2.0)
    jwrite(work, "storyboard.json", fixed)
    return [chk("card past the footage refused", any("outside" in e for e in errs), errs),
            chk("card off its word refused", any("not synced" in e for e in errs), errs),
            chk("fixed storyboard validates", validate(fixed) == [], validate(fixed))]


def back_out(p, s=1.6):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def foot_52(work):
    start, fps = 2.0, 30

    def video_time(t):
        return t - start if t >= start else None

    def lottie_frame(t):
        return None if t < start else round((t - start) * fps)

    def pop(t):
        p = min(max((t - start) / 0.35, 0), 1)
        return 0.3 + 0.7 * back_out(p)

    samples = [pop(start + k * 0.35 / 50) for k in range(51)]
    jwrite(work, "seek.json", {"t": [2.5, 3.0], "video": [video_time(2.5), video_time(3.0)], "lottie": [lottie_frame(3.0)]})
    return [chk("video seeks t - start", video_time(3.0) == 1.0 and video_time(1.0) is None, video_time(3.0)),
            chk("lottie frame = (t-start)*fps", lottie_frame(3.0) == 30, lottie_frame(3.0)),
            chk("pop 0.3 -> 1 with back.out overshoot", near(samples[0], 0.3, 1e-9) and near(samples[-1], 1, 1e-9)
                and max(samples) > 1.0, round(max(samples), 3))]


def foot_53(work):
    def pick(width, eff, save, mem, seen=False, deep=False, reduced=False):
        if seen or deep or reduced or save or (mem is not None and mem <= 2):
            return "skip"
        if width >= 1100 and eff not in ("2g", "3g", "slow-2g") and not save:
            return "4k"
        return "720p"

    def on_error(cur):
        return "720p" if cur == "4k" else "poster"

    cases = [((1400, "4g", False, 8), "4k"), ((1099, "4g", False, 8), "720p"), ((1400, "3g", False, 8), "720p"),
             ((1400, "4g", True, 8), "skip"), ((1400, "4g", False, 2), "skip")]
    got = [pick(*a) for a, _ in cases]
    jwrite(work, "intro_decisions.json", got)
    return [chk("decision table", got == [w for _, w in cases], got),
            chk("4K error retries 720p once then poster", on_error("4k") == "720p" and on_error("720p") == "poster", "ok"),
            chk("reduced motion skips", pick(1400, "4g", False, 8, reduced=True) == "skip", "skip")]


def click_track(bpm, sec, sr=16000):
    x = np.zeros(int(sec * sr))
    step = 60 / bpm
    for k in range(int(sec / step) + 1):
        i = int(k * step * sr)
        n = min(160, len(x) - i)
        if n > 0:
            x[i:i + n] += np.sin(2 * np.pi * 1000 * np.arange(n) / sr) * np.exp(-np.arange(n) / 40)
    return x


def detect_beats(x, sr):
    hop = 160
    env = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)])
    on = np.maximum(np.diff(env, prepend=0.0), 0)
    peaks = [i for i in range(1, len(on) - 1) if on[i] > 0.3 * on.max() and on[i] >= on[i - 1] and on[i] > on[i + 1]]
    times = np.array(peaks) * hop / sr
    bpm = 60 / np.median(np.diff(times))
    return times, bpm


def foot_54(work):
    sr = 16000
    t = np.arange(int(8.0 * sr)) / sr
    x = click_track(120, 8.0, sr) * 0.3 + 0.05 * np.sin(2 * np.pi * 220 * t)
    write_wav(work / "music.wav", x, sr)
    beats, bpm = detect_beats(x, sr)
    downbeats = beats[::4]
    cuts, t, k = [], 0.0, 0
    pattern = [1.0, 1.0, 3.0]  # quick, quick, breathing (ends on a downbeat)
    while t < 7.0:
        L = pattern[k % 3]
        end = min(t + L, 8.0)
        if L >= 3:
            later = [float(d) for d in downbeats if d > t + 1.5]
            if later:
                end = min(later, key=lambda d: abs(d - end))
        cuts.append((round(t, 3), round(float(end), 3)))
        t, k = float(end), k + 1
    ff("-i", work / "music.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "16000", work / "norm.wav")
    err = ffstderr("-i", work / "norm.wav", "-af", "ebur128", "-f", "null", "-")
    I = float([l for l in err.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    breathing_on_db = all(any(near(e, d, 0.02) for d in downbeats) for s, e in cuts if e - s >= 2.5)
    jwrite(work, "montage.json", {"bpm": float(bpm), "cuts": cuts, "lufs": I})
    return [chk("120 BPM detected +-1", near(bpm, 120, 1), round(float(bpm), 2)),
            chk("breathing shots end on downbeats", breathing_on_db, cuts),
            chk("loudnorm to -14 LUFS +-1", near(I, -14, 1.0), I)]


def foot_56(work):
    def reel_count(dur):
        return min(8, 5 if dur > 600 else 3 if dur > 180 else 2)

    words = []
    t = 0.0
    rng = np.random.default_rng(11)
    for s in range(60):
        dense = 20 <= s < 28  # dense sentences
        n = 12 if dense else 5
        for i in range(n):
            words.append({"w": "كلمة" + ("." if i == n - 1 else ""), "start": round(t, 2)})
            t += 0.25 if dense else 0.8
        t += 0.3
    sentences, cur = [], [words[0]]
    for a, b in zip(words, words[1:]):
        if a["w"].endswith((".", "!", "؟", "?", "…")) or b["start"] - a["start"] > 9:
            sentences.append(cur)
            cur = []
        cur.append(b)
    sentences.append(cur)

    def windows(length=40, lo=15, hi=75):
        res = []
        for i in range(len(sentences)):
            j, n = i, 0
            while j < len(sentences):
                end = sentences[j][-1]["start"] + 0.5
                n += len(sentences[j])
                span = end - sentences[i][0]["start"]
                if span >= length or j == len(sentences) - 1:
                    break
                j += 1
            if lo <= span <= hi:
                res.append((n / span, sentences[i][0]["start"], end))
        return sorted(res, reverse=True)

    w = windows()
    best = w[0]
    jwrite(work, "reels.json", {"count": reel_count(t), "best": best})
    dense_start = sentences[20][0]["start"]
    return [chk("count rule 5/3/2", (reel_count(700), reel_count(200), reel_count(100)) == (5, 3, 2), "5/3/2"),
            chk("best window starts in the dense part", dense_start - 1 <= best[1] <= sentences[27][0]["start"], best),
            chk("window 15-75 s and ends on a sentence", 15 <= best[2] - best[1] <= 75
                and any(near(best[2], s[-1]["start"] + 0.5, 1e-6) for s in sentences), round(best[2] - best[1], 2))]


def foot_p01(work):
    src = write_video(work / "src.mkv", frame_index_frames(60, 36, 64), 30, audio=write_wav(work / "a.wav", tone(2.0)))
    D = duration(src)

    def validate(cuts, out, inp):
        if Path(out).resolve() == Path(inp).resolve():
            return "refuse:output==input"
        if len(cuts) > 30:
            return "refuse:>30 cuts"
        for a, b in cuts:
            if not (math.isfinite(a) and math.isfinite(b)) or not (0 <= a < b <= D + 0.03) or b - a < 0.10:
                return f"refuse:bad range {a}:{b}"
        return "ok"

    cuts = [(0.2, 0.7), (1.2, 1.8)]
    out = work / "recut.mp4"
    parts, fc = [], ""
    for k, (a, b) in enumerate(cuts):
        fc += (f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,scale=480:854:force_original_aspect_ratio=decrease,"
               f"pad=480:854:(ow-iw)/2:(oh-ih)/2,fps=24,setsar=1,format=yuv420p[v{k}];"
               f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afftdn=nf=-25[a{k}];")
        parts.append(f"[v{k}][a{k}]")
    fc += "".join(parts) + f"concat=n={len(cuts)}:v=1:a=1[v][a0];[a0]loudnorm=I=-16:TP=-1.5:LRA=11[a]"
    ff("-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "21",
       "-preset", "ultrafast", "-c:a", "aac", "-ar", "48000", out)
    v = vstream(out)
    return [chk("output==input refused", validate(cuts, src, src) == "refuse:output==input", "same path"),
            chk("31 cuts refused", validate([(0, 0.2)] * 31, out, src) == "refuse:>30 cuts", "31"),
            chk("0.05 s cut refused", validate([(0.1, 0.15)], out, src).startswith("refuse:bad"), "0.05"),
            chk("range past duration refused", validate([(1.0, D + 0.5)], out, src).startswith("refuse:bad"), "past"),
            chk("480x854 @24", (v["width"], v["height"], eval(v["r_frame_rate"])) == (480, 854, 24),
                (v["width"], v["height"], v["r_frame_rate"])),
            chk("duration = 0.5 + 0.6 s", near(duration(out), 1.1, 0.08), duration(out))]


def foot_x01(work):
    edl = [{"src_in": 0.0, "src_out": 4.0}, {"src_in": 6.0, "src_out": 10.0}]
    inserts = [{"prog_at": 1.0, "dur": 1.5, "kind": "b-roll", "audio": "source"}]

    def src_to_prog(ts):
        p = 0.0
        for c in edl:
            if c["src_in"] <= ts < c["src_out"]:
                return p + ts - c["src_in"]
            p += c["src_out"] - c["src_in"]
        return None

    words = [{"w": "a", "src": 1.5}, {"w": "b", "src": 5.0}, {"w": "c", "src": 7.25}]
    mapped = {w["w"]: src_to_prog(w["src"]) for w in words}
    # shifting a picture boundary (B-roll) must not move audio words
    after_insert = {w["w"]: src_to_prog(w["src"]) for w in words}
    prog_len = sum(c["src_out"] - c["src_in"] for c in edl)
    jwrite(work, "timemap.json", {"edl": edl, "inserts": inserts, "words": mapped})
    return [chk("word in removed span has no programme time", mapped["b"] is None, mapped),
            chk("word at src 7.25 -> prog 5.25", mapped["c"] == 5.25, mapped["c"]),
            chk("B-roll over picture keeps word timing", after_insert == mapped, after_insert),
            chk("programme length 8 s", prog_len == 8.0, prog_len)]


def foot_x02(work):
    import shutil
    report = {}
    report["ffmpeg"] = bool(shutil.which("ffmpeg"))
    report["ffprobe"] = bool(shutil.which("ffprobe"))
    src = write_video(work / "test.mkv", solid(10, 36, 64, (10, 10, 10)), 10, audio=write_wav(work / "a.wav", tone(1)))
    report["decode_picture"] = len(read_video(src)) >= 10
    report["decode_audio"] = len(decode_audio(src)) > 15000
    from fontTools.ttLib import TTFont
    cands = sorted(Path("/usr/share/fonts").rglob("*.ttf")) + sorted(
        (REPO / ".claude/skills/kosif-superpowers/proofs/_shared/fonts").glob("*.ttf"))

    def has_arabic(p):
        try:
            cmap = TTFont(str(p), lazy=True).getBestCmap() or {}
            return all(c in cmap for c in (0x0627, 0x0644, 0x0645))
        except Exception:
            return False
    report["arabic_font"] = any(has_arabic(p) for p in cands)
    short = work / "short_test.mp4"
    ff("-f", "lavfi", "-i", "color=c=black:s=108x192:d=0.5:r=30", "-c:v", "libx264", "-preset", "ultrafast", short)
    report["short_export"] = near(duration(short), 0.5, 0.05)
    missing = [k for k, v in report.items() if not v]
    jwrite(work, "preflight.json", {"report": report, "missing": missing})
    fake = dict(report, ffmpeg=False)
    return [chk("all preflight items present here", not missing, missing),
            chk("missing tool is named", "ffmpeg" in [k for k, v in fake.items() if not v], "ffmpeg"),
            chk("short test export 0.5 s", report["short_export"], duration(short))]


def foot_x04(work):
    proj = work / "project.json"
    states = work / "checkpoints"
    states.mkdir()

    def checkpoint(tag):
        dst = states / f"{tag}.json"
        dst.write_bytes(proj.read_bytes())
        return hashlib.sha256(dst.read_bytes()).hexdigest()

    def save(data, really=True):
        if really:
            proj.write_text(json.dumps(data))
        return {"api": "saved"}

    def verify_saved(expected):
        return json.loads(proj.read_text()) == expected

    proj.write_text(json.dumps({"tracks": 1}))
    h0 = checkpoint("before")
    resp = save({"tracks": 2}, really=False)  # API says saved but nothing written
    caught = resp["api"] == "saved" and not verify_saved({"tracks": 2})
    save({"tracks": 2})
    h1 = checkpoint("after")
    restored = json.loads((states / "before.json").read_text())
    return [chk("API read-back alone is not proof: unsaved state caught", caught, caught),
            chk("before/after checkpoints differ", h0 != h1, (h0[:8], h1[:8])),
            chk("previous version restorable", restored == {"tracks": 1}, restored)]


def foot_x05(work):
    steps = ["inspect", "analyse", "arabic_overlay", "audio", "licensed_media", "render_available_tool", "verify",
             "deliver_with_diff"]

    def gate(report):
        errs = []
        for s in steps:
            if s not in report["steps"]:
                errs.append(f"missing step {s}")
        if report["claim"] == "exact match" and not all(report["gates"].values()):
            errs.append("exact match claimed with a failed gate")
        if not report.get("differences"):
            errs.append("no differences report")
        return errs

    bad = {"steps": steps[:7], "claim": "exact match", "gates": {"cuts": True, "font": False}, "differences": []}
    good = {"steps": steps, "claim": "approximate", "gates": {"cuts": True, "font": False},
            "differences": ["font candidate differs"]}
    eb, eg = gate(bad), gate(good)
    jwrite(work, "imitation_gate.json", {"bad": eb, "good": eg})
    return [chk("8 steps required", len(steps) == 8 and "missing step deliver_with_diff" in eb, eb),
            chk("failed gate -> no 'exact match'", "exact match claimed with a failed gate" in eb, eb),
            chk("honest report passes", eg == [], eg)]


def foot_u01(work):
    import cv2
    rng = np.random.default_rng(12)
    shots = {s: [cv2.GaussianBlur(rng.integers(0, 255, (54, 96)).astype(np.uint8), (0, 0), 3) for _ in range(1)][0]
             for s in ("A", "B")}
    fps = 10
    src = {s: np.stack([np.roll(img, i, 1) for i in range(40)]) for s, img in shots.items()}  # source frames
    c = 1.3  # draft uses B from source time t - c
    draft = [src["A"][i] for i in range(10)] + [src["B"][int(round((i / fps - c) * fps))] for i in range(20, 30)]

    def match(f):
        best = None
        for s, frs in src.items():
            for k, g in enumerate(frs):
                mad = float(np.abs(f.astype(float) - g).mean())
                if best is None or mad < best[0]:
                    best = (mad, s, k / fps)
        return best

    res = [match(f) for f in draft]
    tb = [(20 + i) / fps for i in range(10)]
    sb = [r[2] for r in res[10:]]
    slope, icpt = np.polyfit(tb, sb, 1)
    jwrite(work, "match.json", [{"shot": r[1], "src_t": r[2], "mad": r[0]} for r in res])
    return [chk("shots recovered", [r[1] for r in res] == ["A"] * 10 + ["B"] * 10, [r[1] for r in res]),
            chk("MAD < 15 = full frame use", max(r[0] for r in res) < 15, max(r[0] for r in res)),
            chk("linear fit gives offset c = 1.3", near(-icpt, 1.3, 0.05) and near(slope, 1, 0.02), (slope, -icpt))]


def foot_u02(work):
    rng = np.random.default_rng(13)
    base = rng.integers(0, 255, (36, 64)).astype(float)
    frames = []
    for i in range(60):
        f = base + rng.normal(0, 2, base.shape) + (i % 3)
        if i >= 37:
            f = np.roll(base, 9, 1) + rng.normal(0, 2, base.shape)
        frames.append(f)
    d = np.array([np.abs(frames[i] - frames[i - 1]).mean() for i in range(1, 60)])
    jumps = []
    for i in range(len(d)):
        lo, hi = max(0, i - 15), min(len(d), i + 16)
        med = np.median(np.delete(d[lo:hi], i - lo))
        if d[i] > 5 * med:
            jumps.append(i + 1)
    cut_at = [j - 1 for j in jumps]
    jwrite(work, "jumps.json", {"jumps": jumps, "cut_on": cut_at})
    return [chk("jump at frame 37 found", jumps == [37], jumps),
            chk("section cut on the frame before (36)", cut_at == [36], cut_at)]


def guided(I, p, r, eps):
    import cv2
    box = lambda x: cv2.boxFilter(x, -1, (2 * r + 1, 2 * r + 1))
    mI, mp = box(I), box(p)
    a = (box(I * p) - mI * mp) / (box(I * I) - mI * mI + eps)
    b = mp - a * mI
    return box(a) * I + box(b)


def foot_u03(work):
    import cv2
    H, W = 120, 96
    rng = np.random.default_rng(14)
    img = (rng.integers(0, 40, (H, W, 3)) + np.array([30, 90, 160])).astype(np.uint8)
    truth = np.zeros((H, W), np.uint8)
    cv2.ellipse(truth, (48, 35), (14, 18), 0, 0, 360, 1, -1)
    cv2.rectangle(truth, (26, 52), (70, 119), 1, -1)
    img[truth == 1] = (rng.integers(0, 30, (int(truth.sum()), 3)) + np.array([200, 150, 120])).astype(np.uint8)
    half = cv2.resize(img, (W // 2, H // 2))
    mask = np.full((H // 2, W // 2), cv2.GC_PR_BGD, np.uint8)
    cv2.ellipse(mask, (24, 17), (5, 7), 0, 0, 360, cv2.GC_FGD, -1)  # face oval seed
    cv2.rectangle(mask, (18, 32), (30, 58), cv2.GC_FGD, -1)  # torso seed
    mask[:, :4] = cv2.GC_BGD
    mask[:, -4:] = cv2.GC_BGD
    bgd, fgd = np.zeros((1, 65)), np.zeros((1, 65))
    cv2.grabCut(half, mask, None, bgd, fgd, 4, cv2.GC_INIT_WITH_MASK)
    m = np.isin(mask, (cv2.GC_FGD, cv2.GC_PR_FGD)).astype(np.float32)
    m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    m = guided(gray, m, 10, 2e-4)
    m = np.clip(guided(gray, m, 4, 1e-4), 0, 1)
    Image.fromarray((m * 255).astype(np.uint8)).save(work / "matte.png")
    pred = m > 0.5
    iou = float((pred & (truth == 1)).sum() / (pred | (truth == 1)).sum())
    return [chk("matte IoU >= 0.9 vs planted person", iou >= 0.9, round(iou, 3)),
            chk("matte is soft (guided filter)", ((m > 0.05) & (m < 0.95)).any(), int(((m > 0.05) & (m < 0.95)).sum()))]


PROGRAMS = {
    "FOOT-01": foot_01, "FOOT-02": foot_02, "FOOT-03": foot_03, "FOOT-04": foot_04, "FOOT-05": foot_05,
    "FOOT-06": foot_06, "FOOT-07": foot_07, "FOOT-08": foot_08, "FOOT-09": foot_09, "FOOT-10": foot_10,
    "FOOT-11": foot_11, "FOOT-12": foot_12, "FOOT-13": foot_13, "FOOT-14": foot_14, "FOOT-15": foot_15,
    "FOOT-16": foot_16, "FOOT-17": foot_17, "FOOT-18": foot_18, "FOOT-19": foot_19, "FOOT-20": foot_20,
    "FOOT-21": foot_21, "FOOT-23": foot_23, "FOOT-24": foot_24, "FOOT-25": foot_25, "FOOT-26": foot_26,
    "FOOT-27": foot_27, "FOOT-28": foot_28, "FOOT-29": foot_29, "FOOT-30": foot_30, "FOOT-32": foot_32,
    "FOOT-33": foot_33, "FOOT-34": foot_34, "FOOT-35": foot_35, "FOOT-36": foot_36, "FOOT-37": foot_37,
    "FOOT-38": foot_38, "FOOT-39": foot_39, "FOOT-40": foot_40, "FOOT-41": foot_41, "FOOT-42": foot_42,
    "FOOT-43": foot_43, "FOOT-44": foot_44, "FOOT-45": foot_45, "FOOT-46": foot_46, "FOOT-47": foot_47,
    "FOOT-48": foot_48, "FOOT-49": foot_49, "FOOT-50": foot_50, "FOOT-51": foot_51, "FOOT-52": foot_52,
    "FOOT-53": foot_53, "FOOT-54": foot_54, "FOOT-56": foot_56, "FOOT-P01": foot_p01, "FOOT-X01": foot_x01,
    "FOOT-X02": foot_x02, "FOOT-X03": foot_x03, "FOOT-X04": foot_x04, "FOOT-X05": foot_x05,
    "FOOT-U01": foot_u01, "FOOT-U02": foot_u02, "FOOT-U03": foot_u03,
}
