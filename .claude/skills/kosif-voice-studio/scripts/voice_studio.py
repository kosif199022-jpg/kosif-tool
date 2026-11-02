#!/usr/bin/env python3
"""KOSIF Voice Studio - speech, voice cloning, voice design and transcription from one CLI.

استوديو الصوت: تعليق صوتي، استنساخ صوت، تصميم صوت من وصف، وتفريغ بطوابع زمنية للكلمات.

Engines, tried in this order by --engine auto:
  voicestudio  a running VoiceStudio backend (github.com/debpalash/VoiceStudio, AGPL-3.0), reached
               over its HTTP API only (default http://localhost:3900, or $VOICESTUDIO_URL).
               Clone, design, 646 languages, transcription. Nothing of its code is copied here.
  edge         edge-tts (pip install edge-tts): free, no key, needs the internet, Egyptian voices
               (ar-EG-SalmaNeural, ar-EG-ShakirNeural) and word timings. No cloning.
  piper        piper-tts (pip install piper-tts): offline on the CPU with a downloaded .onnx voice
               (Arabic: ar_JO-kareem-medium). No cloning.
  whisper      faster-whisper (pip install faster-whisper): offline transcription with word timings.

Commands (run from the repo root; add --json for machine output)
  doctor                              what can run on this machine, and the install line for the rest
  voices [--engine E] [--lang ar]     list voices of one engine
  speak "TEXT" | --file F --out OUT.(mp3|wav) [--engine E] [--voice V] [--rate +0%] [--words words.json]
                                      text to speech; writes OUT, a receipt OUT.receipt.json and, when
                                      the engine gives word timings, words.json ([{word,start,end}])
  transcribe AUDIO --out OUT.(json|srt|vtt|txt) [--engine E] [--model small] [--lang ar] [--words W]
  clone REF_AUDIO --name NAME --i-own-this-voice [--ref-text T] [--lang Arabic]   (voicestudio only)
  design "DESCRIPTION" --name NAME [--save]                                      (voicestudio only)
  verify AUDIO                        measured duration, codec, sample rate and loudness (ffprobe/ffmpeg)
  --self-test                         offline checks, exit 0

Rules: never reports audio it did not measure; a failed engine is reported, never hidden. Cloning needs
--i-own-this-voice (the user owns the voice or has the speaker's consent). Bad input: exit 2.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.util
import json
import mimetypes
import os
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import uuid
from pathlib import Path

DEFAULT_URL = "http://localhost:3900"
EDGE_DEFAULT = {"ar": "ar-EG-SalmaNeural", "en": "en-US-AvaMultilingualNeural"}
PIPER_DIR = Path(os.environ.get("PIPER_VOICES_DIR", Path.home() / ".cache/kosif/piper"))
PIPER_DEFAULT = "ar_JO-kareem-medium"
INSTALL = {
    "edge": "pip install edge-tts",
    "piper": f"pip install piper-tts && python3 -m piper.download_voices --download-dir {PIPER_DIR} {PIPER_DEFAULT}",
    "whisper": "pip install faster-whisper",
    "voicestudio": "install the app from github.com/debpalash/VoiceStudio/releases (or: curl -fsSL https://voicestudio.sh/install | sh), open it, then rerun doctor",
    "ffmpeg": "apt-get install ffmpeg  (macOS: brew install ffmpeg)",
}
ARABIC = re.compile(r"[؀-ۿ]")


class Fail(Exception):
    """A user-facing failure with an exit code."""

    def __init__(self, msg: str, code: int = 1):
        super().__init__(msg)
        self.code = code


# ---------------------------------------------------------------- helpers
def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def lang_of(text: str) -> str:
    return "ar" if ARABIC.search(text or "") else "en"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def ca_context() -> ssl.SSLContext | None:
    """Honour a corporate/proxy CA bundle when the user set one (SSL_CERT_FILE or REQUESTS_CA_BUNDLE)."""
    for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
        path = os.environ.get(var)
        if path and Path(path).is_file():
            return ssl.create_default_context(cafile=path)
    return None


def ticks_to_s(t: int) -> float:  # edge-tts offsets are 100 ns ticks
    return round(t / 10_000_000, 3)


def edge_words(events: list[dict]) -> list[dict]:
    out = []
    for e in events:
        if e.get("type") != "WordBoundary" or not str(e.get("text", "")).strip():
            continue
        start = ticks_to_s(int(e["offset"]))
        out.append({"word": e["text"].strip(), "start": start, "end": round(start + ticks_to_s(int(e["duration"])), 3)})
    return clean_words(out)


def clean_words(words: list[dict]) -> list[dict]:
    """Sorted, non-overlapping [{word,start,end}] (the playbooks/audio-sync.md format)."""
    words = sorted((w for w in words if str(w.get("word", "")).strip()), key=lambda w: w["start"])
    for a, b in zip(words, words[1:]):
        if a["end"] > b["start"]:
            a["end"] = b["start"]
    for w in words:
        w["end"] = max(w["end"], w["start"])
    return words


def fmt_ts(sec: float, sep: str) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def to_subtitles(segments: list[dict], kind: str) -> str:
    sep = "," if kind == "srt" else "."
    lines = ["WEBVTT", ""] if kind == "vtt" else []
    for i, s in enumerate(segments, 1):
        if kind == "srt":
            lines.append(str(i))
        lines += [f"{fmt_ts(s['start'], sep)} --> {fmt_ts(s['end'], sep)}", s["text"].strip(), ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- measuring
def verify_audio(path: Path) -> dict:
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        raise Fail(f"no audio at {path} (missing or empty)")
    if not shutil.which("ffprobe"):
        raise Fail("ffprobe not found; " + INSTALL["ffmpeg"])
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                        "stream=codec_name,sample_rate,channels:format=duration", "-of", "json", str(path)],
                       capture_output=True, text=True)
    info = json.loads(p.stdout or "{}")
    streams = info.get("streams") or []
    if p.returncode or not streams:
        head = path.read_bytes()[:200].decode("utf-8", "replace")
        raise Fail(f"{path} is not audio (ffprobe found no audio stream); first bytes: {head!r}")
    st = streams[0]
    dur = float(info.get("format", {}).get("duration") or 0)
    rep = {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path), "codec": st.get("codec_name"),
           "sample_rate": int(st.get("sample_rate") or 0), "channels": st.get("channels"), "duration_s": round(dur, 3)}
    if shutil.which("ffmpeg"):
        v = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                           capture_output=True, text=True)
        m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", v.stderr)
        if m:
            rep["mean_volume_db"] = -999.0 if m.group(1) == "-inf" else float(m.group(1))
    rep["ok"] = dur > 0.05 and rep.get("mean_volume_db", 0.0) > -70
    if not rep["ok"]:
        rep["problem"] = "too short or silent"
    return rep


def to_format(src: Path, out: Path) -> None:
    """Re-encode src into out's extension (wav/mp3/ogg/m4a) with ffmpeg; same extension = move."""
    if src.suffix.lower() == out.suffix.lower():
        shutil.move(str(src), out)
        return
    if not shutil.which("ffmpeg"):
        raise Fail("ffmpeg needed to write " + out.suffix + "; " + INSTALL["ffmpeg"])
    codec = {".mp3": ["-c:a", "libmp3lame", "-b:a", "192k"], ".m4a": ["-c:a", "aac", "-b:a", "192k"],
             ".ogg": ["-c:a", "libopus", "-b:a", "96k"], ".wav": ["-c:a", "pcm_s16le"]}.get(out.suffix.lower())
    if codec is None:
        raise Fail(f"unsupported output extension {out.suffix} (use .wav .mp3 .m4a .ogg)", 2)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), *codec, str(out)], check=True)
    src.unlink(missing_ok=True)


# ---------------------------------------------------------------- VoiceStudio over HTTP
class VoiceStudio:
    def __init__(self, url: str | None = None, token: str | None = None, timeout: float = 600):
        self.url = (url or os.environ.get("VOICESTUDIO_URL") or DEFAULT_URL).rstrip("/")
        self.token = token if token is not None else os.environ.get("VOICESTUDIO_TOKEN")
        self.timeout = timeout
        self._paths: list[str] | None = None

    def _req(self, method: str, path: str, body: bytes | None = None, ctype: str | None = None,
             timeout: float | None = None) -> tuple[int, bytes, str]:
        req = urllib.request.Request(self.url + path, data=body, method=method)
        if ctype:
            req.add_header("Content-Type", ctype)
        if self.token:  # never printed
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=timeout or self.timeout) as r:
                return r.status, r.read(), r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            detail = e.read()[:500].decode("utf-8", "replace")
            if e.code in (401, 403):
                raise Fail(f"VoiceStudio refused the call ({e.code}): set VOICESTUDIO_TOKEN to the configured key; {detail}")
            raise Fail(f"VoiceStudio {method} {path} -> HTTP {e.code}: {detail}")
        except (urllib.error.URLError, OSError) as e:
            raise Fail(f"VoiceStudio not reachable at {self.url} ({getattr(e, 'reason', e)}); {INSTALL['voicestudio']}")

    def json(self, method: str, path: str, payload=None, timeout=None):
        body = None if payload is None else json.dumps(payload).encode()
        _, data, _ = self._req(method, path, body, "application/json" if body else None, timeout)
        return json.loads(data or b"null")

    def health(self) -> dict:
        return self.json("GET", "/health", timeout=4)

    def up(self) -> bool:
        try:
            self.health()
            return True
        except Fail:
            return False

    def path(self, suffix: str, method: str = "post") -> str:
        """Find the running version's route that ends with suffix (prefixes change between versions)."""
        if self._paths is None:
            spec = self.json("GET", "/openapi.json", timeout=15)
            self._paths = [p for p, ops in (spec.get("paths") or {}).items() if isinstance(ops, dict)
                           for m in ops if m.lower() == method] if spec else []
            self._paths = [f"{method}:{p}" for p in self._paths]
        hits = sorted((p.split(":", 1)[1] for p in self._paths if p.startswith(method + ":") and p.endswith(suffix)), key=len)
        if not hits:
            raise Fail(f"this VoiceStudio version has no {method.upper()} *{suffix} route (checked /openapi.json)")
        return hits[0]

    def multipart(self, path: str, fields: dict, files: dict) -> dict:
        boundary = uuid.uuid4().hex
        parts = []
        for k, v in fields.items():
            if v is None:
                continue
            parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
        for k, fp in files.items():
            fp = Path(fp)
            ctype = mimetypes.guess_type(fp.name)[0] or "application/octet-stream"
            parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"; filename="{fp.name}"\r\n'
                         f"Content-Type: {ctype}\r\n\r\n".encode() + fp.read_bytes() + b"\r\n")
        body = b"".join(parts) + f"--{boundary}--\r\n".encode()
        _, data, _ = self._req("POST", path, body, f"multipart/form-data; boundary={boundary}")
        return json.loads(data or b"null")

    def voices(self):
        return self.json("GET", "/v1/audio/voices")

    def speak(self, text: str, out: Path, voice: str | None) -> None:
        payload = {"model": "tts-1", "input": text, "voice": voice or "alloy", "response_format": "wav"}
        _, data, ctype = self._req("POST", "/v1/audio/speech", json.dumps(payload).encode(), "application/json")
        if "json" in ctype or not data:
            raise Fail(f"VoiceStudio returned no audio: {data[:300].decode('utf-8', 'replace')}")
        out.write_bytes(data)

    def transcribe(self, audio: Path) -> dict:
        return self.multipart("/v1/audio/transcriptions", {"model": "whisper-1", "response_format": "verbose_json",
                                                          "timestamp_granularities[]": "word"}, {"file": audio})

    def clone(self, ref: Path, name: str, ref_text: str, lang: str) -> dict:
        return self.multipart(self.path("/profiles"), {"name": name, "kind": "clone", "ref_text": ref_text,
                                                       "language": lang}, {"ref_audio": ref})

    def describe(self, description: str) -> dict:
        return self.json("POST", self.path("/design/describe"), {"description": description})

    def design(self, description: str, name: str) -> dict:
        d = self.describe(description)
        if not d.get("matched"):
            raise Fail(f"VoiceStudio mapped no voice attribute from this description (unmatched: {d.get('unmatched')})")
        prof = self.multipart(self.path("/profiles"), {"name": name, "kind": "design", "instruct": d.get("instruct", ""),
                                                       "vd_states": json.dumps(d.get("attrs") or {})}, {})
        return {"describe": d, "profile": prof}


# ---------------------------------------------------------------- local engines
def edge_speak(text: str, out: Path, voice: str | None, rate: str) -> list[dict]:
    if not has_module("edge_tts"):
        raise Fail("edge-tts not installed; " + INSTALL["edge"])
    import edge_tts
    import edge_tts.communicate as comm
    ctx = ca_context()
    if ctx is not None:  # the library pins certifi; use the CA bundle the user configured
        comm._SSL_CTX = ctx
    voice = voice or EDGE_DEFAULT[lang_of(text)]
    events: list[dict] = []

    async def run():
        c = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
        with open(out, "wb") as f:
            async for ch in c.stream():
                if ch["type"] == "audio":
                    f.write(ch["data"])
                else:
                    events.append(ch)
    try:
        asyncio.run(run())
    except Exception as e:  # network, bad voice name, service change
        raise Fail(f"edge-tts failed ({type(e).__name__}: {str(e)[:200]})")
    return edge_words(events)


def edge_voices(lang: str | None):
    if not has_module("edge_tts"):
        raise Fail("edge-tts not installed; " + INSTALL["edge"])
    import edge_tts
    import edge_tts.communicate as comm
    ctx = ca_context()
    if ctx is not None:
        import edge_tts.voices as ev
        ev._SSL_CTX = comm._SSL_CTX = ctx
    vs = asyncio.run(edge_tts.list_voices())
    rows = [{"voice": v["ShortName"], "locale": v["Locale"], "gender": v["Gender"]} for v in vs]
    return [r for r in rows if not lang or r["locale"].lower().startswith(lang.lower())]


def piper_model(voice: str | None) -> Path:
    v = voice or PIPER_DEFAULT
    p = Path(v)
    if p.suffix == ".onnx" and p.is_file():
        return p
    cand = PIPER_DIR / f"{v}.onnx"
    if cand.is_file():
        return cand
    raise Fail(f"piper voice {v} not downloaded; {INSTALL['piper']}")


def piper_speak(text: str, out_wav: Path, voice: str | None) -> None:
    if not has_module("piper"):
        raise Fail("piper-tts not installed; " + INSTALL["piper"])
    model = piper_model(voice)
    p = subprocess.run([sys.executable, "-m", "piper", "-m", str(model), "-f", str(out_wav)],
                       input=text, capture_output=True, text=True)
    if p.returncode:
        raise Fail("piper failed: " + p.stderr.strip()[-300:])


def whisper_transcribe(audio: Path, model: str, lang: str | None) -> dict:
    if not has_module("faster_whisper"):
        raise Fail("faster-whisper not installed; " + INSTALL["whisper"])
    if not shutil.which("ffmpeg"):
        raise Fail("ffmpeg needed for transcription; " + INSTALL["ffmpeg"])
    import wave

    import numpy as np
    from faster_whisper import WhisperModel
    with tempfile.TemporaryDirectory() as td:  # decode with ffmpeg: avoids PyAV version clashes
        wav = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(audio), "-ar", "16000", "-ac", "1", str(wav)], check=True)
        with wave.open(str(wav)) as w:
            pcm = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, info = m.transcribe(pcm, language=lang, word_timestamps=True)
    segments, words = [], []
    for s in segs:
        segments.append({"start": round(float(s.start), 3), "end": round(float(s.end), 3), "text": s.text.strip()})
        for w in s.words or []:
            words.append({"word": w.word.strip(), "start": round(float(w.start), 3), "end": round(float(w.end), 3)})
    return {"engine": "whisper", "model": model, "language": info.language,
            "text": " ".join(s["text"] for s in segments).strip(), "segments": segments, "words": clean_words(words)}


def normalise_vs_transcript(r: dict) -> dict:
    segs = [{"start": float(s.get("start", 0)), "end": float(s.get("end", 0)), "text": str(s.get("text", "")).strip()}
            for s in (r.get("segments") or [])]
    words = [{"word": str(w.get("word", "")).strip(), "start": float(w.get("start", 0)), "end": float(w.get("end", 0))}
             for w in (r.get("words") or [])]
    return {"engine": "voicestudio", "language": r.get("language"), "text": (r.get("text") or "").strip(),
            "segments": segs, "words": clean_words(words)}


# ---------------------------------------------------------------- doctor
def doctor(vs: VoiceStudio) -> dict:
    vs_ok, vs_info = False, None
    try:
        vs_info = vs.health()
        vs_ok = True
    except Fail as e:
        vs_info = str(e)
    piper_voice = None
    try:
        piper_voice = str(piper_model(None))
    except Fail:
        pass
    rows = {
        "voicestudio": {"ready": vs_ok, "url": vs.url, "detail": vs_info if vs_ok else None,
                        "can": "speak, clone, design, transcribe, dub (646 languages)", "install": None if vs_ok else INSTALL["voicestudio"]},
        "edge": {"ready": has_module("edge_tts"), "can": "speak (Egyptian ar-EG voices, word timings; online, no key)",
                 "install": None if has_module("edge_tts") else INSTALL["edge"]},
        "piper": {"ready": has_module("piper") and piper_voice is not None, "voice": piper_voice,
                  "can": "speak offline on CPU", "install": None if (has_module("piper") and piper_voice) else INSTALL["piper"]},
        "whisper": {"ready": has_module("faster_whisper"), "can": "transcribe offline with word timings",
                    "install": None if has_module("faster_whisper") else INSTALL["whisper"]},
        "ffmpeg": {"ready": bool(shutil.which("ffmpeg") and shutil.which("ffprobe")), "can": "verify, convert",
                   "install": None if shutil.which("ffmpeg") else INSTALL["ffmpeg"]},
    }
    speak = [e for e in ("voicestudio", "edge", "piper") if rows[e]["ready"]]
    listen = [e for e in ("voicestudio", "whisper") if rows[e]["ready"]]
    return {"engines": rows, "speak_order": speak, "transcribe_order": listen,
            "clone_and_design": "voicestudio" if vs_ok else "unavailable here (needs a running VoiceStudio, or Higgsfield create_voice with the user's yes)"}


# ---------------------------------------------------------------- commands
def cmd_speak(a, vs: VoiceStudio) -> dict:
    text = Path(a.file).read_text(encoding="utf-8") if a.file else (a.text or "")
    text = text.strip()
    if not text:
        raise Fail("nothing to say: give TEXT or --file", 2)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    order = [a.engine] if a.engine != "auto" else ["voicestudio", "edge", "piper"]
    errors = {}
    for eng in order:
        tmp = out.with_name(out.stem + f".{eng}.tmp" + (".mp3" if eng == "edge" else ".wav"))
        try:
            words: list[dict] = []
            if eng == "voicestudio":
                if a.engine == "auto" and not vs.up():
                    raise Fail("not running")
                vs.speak(text, tmp, a.voice)
            elif eng == "edge":
                words = edge_speak(text, tmp, a.voice, a.rate)
            elif eng == "piper":
                piper_speak(text, tmp, a.voice)
            else:
                raise Fail(f"unknown engine {eng}", 2)
            verify_audio(tmp)
            to_format(tmp, out)
            rep = verify_audio(out)
            if not rep["ok"]:
                raise Fail(f"{eng} produced unusable audio: {rep.get('problem')}")
            receipt = {"kind": "kosif.voice.receipt.v1", "command": "speak", "engine": eng,
                       "voice": a.voice or (EDGE_DEFAULT[lang_of(text)] if eng == "edge" else PIPER_DEFAULT if eng == "piper" else "alloy"),
                       "chars": len(text), "audio": rep, "skipped": errors}
            if words:
                wpath = Path(a.words) if a.words else out.with_name("words.json")
                wpath.write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")
                receipt["words_json"] = {"path": str(wpath), "count": len(words)}
            Path(str(out) + ".receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
            return receipt
        except Fail as e:
            errors[eng] = str(e)
            tmp.unlink(missing_ok=True)
            if a.engine != "auto":
                raise
    raise Fail("no speech engine worked: " + json.dumps(errors, ensure_ascii=False))


def cmd_transcribe(a, vs: VoiceStudio) -> dict:
    audio = Path(a.audio)
    verify_audio(audio)
    order = [a.engine] if a.engine != "auto" else ["voicestudio", "whisper"]
    errors, res = {}, None
    for eng in order:
        try:
            if eng == "voicestudio":
                if a.engine == "auto" and not vs.up():
                    raise Fail("not running")
                res = normalise_vs_transcript(vs.transcribe(audio))
            elif eng == "whisper":
                res = whisper_transcribe(audio, a.model, a.lang)
            else:
                raise Fail(f"unknown engine {eng}", 2)
            break
        except Fail as e:
            errors[eng] = str(e)
            if a.engine != "auto":
                raise
    if res is None:
        raise Fail("no transcription engine worked: " + json.dumps(errors, ensure_ascii=False))
    if not res["text"]:
        raise Fail(f"{res['engine']} returned an empty transcript (silence, music only, or wrong --lang)")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ext = out.suffix.lower()
    if ext in (".srt", ".vtt"):
        out.write_text(to_subtitles(res["segments"], ext[1:]), encoding="utf-8")
    elif ext == ".txt":
        out.write_text(res["text"] + "\n", encoding="utf-8")
    else:
        out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    if res["words"]:
        wpath = Path(a.words) if a.words else out.with_name("words.json")
        wpath.write_text(json.dumps(res["words"], ensure_ascii=False, indent=1), encoding="utf-8")
    return {"engine": res["engine"], "language": res.get("language"), "out": str(out), "segments": len(res["segments"]),
            "words": len(res["words"]), "preview": res["text"][:160], "skipped": errors}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--url", help="VoiceStudio backend (default $VOICESTUDIO_URL or %s)" % DEFAULT_URL)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("doctor")
    p = sub.add_parser("voices")
    p.add_argument("--engine", default="edge", choices=["voicestudio", "edge", "piper"])
    p.add_argument("--lang")
    p = sub.add_parser("speak")
    p.add_argument("text", nargs="?")
    p.add_argument("--file")
    p.add_argument("--out", required=True)
    p.add_argument("--engine", default="auto", choices=["auto", "voicestudio", "edge", "piper"])
    p.add_argument("--voice")
    p.add_argument("--rate", default="+0%")
    p.add_argument("--words")
    p = sub.add_parser("transcribe")
    p.add_argument("audio")
    p.add_argument("--out", required=True)
    p.add_argument("--engine", default="auto", choices=["auto", "voicestudio", "whisper"])
    p.add_argument("--model", default="small")
    p.add_argument("--lang")
    p.add_argument("--words")
    p = sub.add_parser("clone")
    p.add_argument("ref")
    p.add_argument("--name", required=True)
    p.add_argument("--ref-text", default="")
    p.add_argument("--lang", default="Auto")
    p.add_argument("--i-own-this-voice", action="store_true", dest="consent")
    p = sub.add_parser("design")
    p.add_argument("description")
    p.add_argument("--name", required=True)
    p.add_argument("--save", action="store_true", help="create the profile (default: only show the mapping)")
    p = sub.add_parser("verify")
    p.add_argument("audio")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.cmd:
        ap.print_help()
        return 2
    vs = VoiceStudio(a.url)
    try:
        if a.cmd == "doctor":
            res = doctor(vs)
        elif a.cmd == "voices":
            res = vs.voices() if a.engine == "voicestudio" else edge_voices(a.lang) if a.engine == "edge" else \
                sorted(p.stem for p in PIPER_DIR.glob("*.onnx"))
        elif a.cmd == "speak":
            res = cmd_speak(a, vs)
        elif a.cmd == "transcribe":
            res = cmd_transcribe(a, vs)
        elif a.cmd == "clone":
            if not a.consent:
                raise Fail("cloning needs --i-own-this-voice: the voice is the user's own or the speaker consented", 2)
            verify_audio(Path(a.ref))
            res = vs.clone(Path(a.ref), a.name, a.ref_text, a.lang)
        elif a.cmd == "design":
            res = vs.design(a.description, a.name) if a.save else vs.describe(a.description)
        elif a.cmd == "verify":
            res = verify_audio(Path(a.audio))
    except Fail as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False) if a.json else f"error: {e}", file=sys.stderr)
        return e.code
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=None if a.json else 2))
    return 0


def self_test() -> int:
    ev = [{"type": "WordBoundary", "offset": 1_000_000, "duration": 5_875_000, "text": "أهلاً"},
          {"type": "WordBoundary", "offset": 5_000_000, "duration": 2_000_000, "text": "دي"},
          {"type": "SentenceBoundary", "offset": 0, "duration": 1, "text": "x"}]
    w = edge_words(ev)
    assert [x["word"] for x in w] == ["أهلاً", "دي"], w
    assert w[0]["start"] == 0.1 and w[0]["end"] == 0.5, w  # overlap clipped to the next start
    assert fmt_ts(3725.5, ",") == "01:02:05,500"
    srt = to_subtitles([{"start": 0, "end": 1.25, "text": "سلام"}], "srt")
    assert srt.startswith("1\n00:00:00,000 --> 00:00:01,250\nسلام"), srt
    assert to_subtitles([{"start": 0, "end": 1, "text": "x"}], "vtt").startswith("WEBVTT")
    assert lang_of("hello") == "en" and lang_of("ازيك") == "ar"
    print("voice_studio self-test: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
