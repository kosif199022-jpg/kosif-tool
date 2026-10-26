#!/usr/bin/env python3
"""Transcribe an audio file with Gemini, with clear errors and a local fallback.

Why: a bare `urllib.request.urlopen(...)` call to Gemini dies with a traceback that hides the
reason (bad key, model not found, quota, file too large). This tool prints Google's own error
message, retries what can be retried, tries the next model, and can fall back to faster-whisper.

Usage:
  python3 tools/transcribe_audio.py out/<job>/voice/test.wav
  python3 tools/transcribe_audio.py voice.wav --prompt "Transcribe this Arabic audio verbatim." --json out.json
  python3 tools/transcribe_audio.py voice.wav --engine whisper        # local only, no key needed
  python3 tools/transcribe_audio.py --check                           # test the key and model, no audio

Key: GEMINI_API_KEY (or GOOGLE_API_KEY). Models are tried in order (--model, repeatable).
Files under ~14 MB go inline; bigger files are uploaded with the Gemini Files API.
Exit codes: 0 ok, 1 every engine failed, 2 bad input (missing file, no key and no fallback).
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://generativelanguage.googleapis.com"
DEFAULT_MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash"]
DEFAULT_PROMPT = ("Transcribe this Arabic audio verbatim. Then, on one final line, "
                  "give the dialect and the speaker's gender.")
# Gemini caps a whole request at 20 MB; base64 adds about a third, so keep raw inline audio under 14 MB.
INLINE_LIMIT = 14 * 1024 * 1024
RETRY_STATUS = {429, 500, 502, 503, 504}
AUDIO_MIME = {".wav": "audio/wav", ".mp3": "audio/mp3", ".m4a": "audio/aac", ".aac": "audio/aac",
              ".flac": "audio/flac", ".ogg": "audio/ogg", ".opus": "audio/ogg", ".aiff": "audio/aiff",
              ".aif": "audio/aiff", ".webm": "audio/webm", ".mp4": "video/mp4"}


class GeminiError(Exception):
    """An API failure with a readable reason. `next_model` says whether another model may work."""

    def __init__(self, message: str, status: int | None = None, next_model: bool = False,
                 retry: bool = False):
        super().__init__(message)
        self.status = status
        self.next_model = next_model
        self.retry = retry


def api_key() -> str | None:
    return (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip() or None


def mime_for(path: Path) -> str:
    return AUDIO_MIME.get(path.suffix.lower()) or mimetypes.guess_type(path.name)[0] or "audio/wav"


def explain_http_error(err: urllib.error.HTTPError, model: str) -> GeminiError:
    """Turn an HTTPError into a GeminiError that carries Google's message and a hint."""
    raw = b""
    try:
        raw = err.read() or b""
    except Exception:  # noqa: BLE001 - the body is best-effort
        pass
    text = raw.decode("utf-8", "replace")
    message, status_name, reason = text.strip()[:500], "", ""
    try:
        e = json.loads(text).get("error", {})
        message = e.get("message") or message
        status_name = e.get("status", "")
        for d in e.get("details", []) or []:
            reason = reason or d.get("reason", "")
    except (ValueError, AttributeError):
        pass
    code = err.code
    hint = ""
    if reason == "API_KEY_INVALID" or "API key not valid" in message:
        hint = "GEMINI_API_KEY is wrong or revoked: make a new key at https://aistudio.google.com/apikey"
    elif code == 403:
        hint = ("the key has no access (Generative Language API disabled for its project, "
                "a key restriction, or the region is not supported)")
    elif code == 404:
        hint = f"model '{model}' is not available to this key; trying the next model"
    elif code == 413:
        hint = "request too large; the file will be sent through the Files API"
    elif code == 429:
        hint = "quota or rate limit reached; waiting and retrying, then the next model"
    elif code >= 500:
        hint = "Google server error; retrying"
    elif code == 400 and "audio" in message.lower():
        hint = "the audio format was refused; try converting to 16 kHz mono WAV or MP3"
    full = f"HTTP {code} {status_name} from {model}: {message}".strip()
    if hint:
        full += f"\n  -> {hint}"
    return GeminiError(full, status=code, next_model=code in (404, 429) or code >= 500,
                       retry=code in RETRY_STATUS)


def _request(url: str, key: str, data: bytes | None = None, headers: dict | None = None,
             method: str = "POST", timeout: int = 180):
    h = {"x-goog-api-key": key}
    h.update(headers or {})
    return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h, method=method),
                                  timeout=timeout)


def upload_file(path: Path, key: str, mime: str) -> str:
    """Resumable upload to the Gemini Files API; returns the file URI once it is ACTIVE."""
    size = path.stat().st_size
    start = _request(f"{API}/upload/v1beta/files", key,
                     data=json.dumps({"file": {"display_name": path.name}}).encode(),
                     headers={"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
                              "X-Goog-Upload-Header-Content-Length": str(size),
                              "X-Goog-Upload-Header-Content-Type": mime,
                              "Content-Type": "application/json"})
    upload_url = start.headers.get("X-Goog-Upload-URL") or start.headers.get("x-goog-upload-url")
    if not upload_url:
        raise GeminiError("Files API did not return an upload URL")
    done = _request(upload_url, key, data=path.read_bytes(),
                    headers={"Content-Length": str(size), "X-Goog-Upload-Offset": "0",
                             "X-Goog-Upload-Command": "upload, finalize"}, timeout=600)
    info = json.load(done).get("file", {})
    name, uri = info.get("name"), info.get("uri")
    for _ in range(30):  # audio is usually ACTIVE at once; poll briefly if not
        if info.get("state") in (None, "ACTIVE"):
            break
        if info.get("state") == "FAILED":
            raise GeminiError(f"Files API could not process {path.name}")
        time.sleep(2)
        info = json.load(_request(f"{API}/v1beta/{name}", key, method="GET"))
    if not uri:
        raise GeminiError("Files API returned no file URI")
    return uri


def extract_text(resp: dict, model: str) -> str:
    cands = resp.get("candidates") or []
    if not cands:
        block = (resp.get("promptFeedback") or {}).get("blockReason")
        raise GeminiError(f"{model} returned no answer" + (f" (blocked: {block})" if block else ""),
                          next_model=not block)
    parts = (cands[0].get("content") or {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts).strip()
    if not text:
        reason = cands[0].get("finishReason", "unknown")
        raise GeminiError(f"{model} returned an empty answer (finishReason={reason})", next_model=True)
    return text


def gemini_transcribe(path: Path, prompt: str, models: list[str], key: str, retries: int = 2,
                      log=print) -> tuple[str, str]:
    """Returns (text, model). Raises GeminiError with the last reason when every model fails."""
    mime = mime_for(path)
    use_files = path.stat().st_size > INLINE_LIMIT
    file_uri = None
    last: GeminiError | None = None
    for model in models:
        for attempt in range(retries + 1):
            try:
                if use_files and file_uri is None:
                    log(f"[gemini] {path.name} is {path.stat().st_size / 1e6:.1f} MB; uploading with the Files API")
                    file_uri = upload_file(path, key, mime)
                audio_part = ({"fileData": {"mimeType": mime, "fileUri": file_uri}} if file_uri else
                              {"inlineData": {"mimeType": mime,
                                              "data": base64.b64encode(path.read_bytes()).decode()}})
                body = {"contents": [{"parts": [audio_part, {"text": prompt}]}]}
                resp = _request(f"{API}/v1beta/models/{model}:generateContent", key,
                                data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
                return extract_text(json.load(resp), model), model
            except urllib.error.HTTPError as err:
                last = explain_http_error(err, model)
                if err.code == 413 and not use_files:
                    use_files = True
                    log(f"[gemini] {last}")
                    continue
            except urllib.error.URLError as err:
                last = GeminiError(f"cannot reach {API} ({err.reason}); check the network or proxy",
                                   retry=True)
            except TimeoutError:
                last = GeminiError(f"{model} timed out", retry=True, next_model=True)
            except GeminiError as err:
                last = err
            log(f"[gemini] {last}")
            if not last.retry or attempt == retries:
                break
            time.sleep(2 ** (attempt + 1))
        if last is not None and not last.next_model:
            break  # a bad key or a refused file will fail on every model too
    raise last or GeminiError("no model was tried")


def whisper_transcribe(path: Path, language: str = "ar", size: str = "small") -> str:
    from faster_whisper import WhisperModel  # optional: pip install faster-whisper
    model = WhisperModel(size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(path), language=language or None, beam_size=5)
    return " ".join(s.text.strip() for s in segments).strip()


def check_key(models: list[str], key: str) -> int:
    for model in models:
        try:
            info = json.load(_request(f"{API}/v1beta/models/{model}", key, method="GET", timeout=30))
            print(f"[ok] key works; {info.get('name', model)} is available")
            return 0
        except urllib.error.HTTPError as err:
            e = explain_http_error(err, model)
            print(f"[fail] {e}")
            if not e.next_model and err.code != 404:
                return 1
        except urllib.error.URLError as err:
            print(f"[fail] cannot reach {API} ({err.reason})")
            return 1
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("audio", nargs="?", help="audio file (wav, mp3, m4a, flac, ogg...)")
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--model", action="append", help=f"model to try, repeatable (default {', '.join(DEFAULT_MODELS)})")
    ap.add_argument("--engine", choices=["auto", "gemini", "whisper"], default="auto",
                    help="auto = Gemini, then faster-whisper if Gemini fails (default)")
    ap.add_argument("--language", default="ar", help="language for the whisper fallback (default ar)")
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--json", dest="json_out", help="also write {engine, model, text} to this file")
    ap.add_argument("--check", action="store_true", help="only test the key and model, then exit")
    args = ap.parse_args(argv)
    models = args.model or DEFAULT_MODELS
    key = api_key()

    if args.check:
        if not key:
            print("[fail] GEMINI_API_KEY is not set")
            return 2
        return check_key(models, key)
    if not args.audio:
        ap.error("an audio file is required (or --check)")
    path = Path(args.audio)
    if not path.is_file() or path.stat().st_size == 0:
        print(f"[fail] audio file not found or empty: {path}", file=sys.stderr)
        return 2

    result, errors = None, []
    if args.engine in ("auto", "gemini"):
        if not key:
            errors.append("GEMINI_API_KEY (or GOOGLE_API_KEY) is not set")
            print(f"[gemini] {errors[-1]}", file=sys.stderr)
        else:
            try:
                text, model = gemini_transcribe(path, args.prompt, models, key, args.retries,
                                                log=lambda m: print(m, file=sys.stderr))
                result = {"engine": "gemini", "model": model, "text": text}
            except GeminiError as err:
                errors.append(str(err))
    if result is None and args.engine in ("auto", "whisper"):
        try:
            print("[whisper] transcribing locally with faster-whisper", file=sys.stderr)
            result = {"engine": "faster-whisper", "model": "small",
                      "text": whisper_transcribe(path, args.language)}
        except ImportError:
            errors.append("faster-whisper is not installed (pip install faster-whisper)")
        except Exception as err:  # noqa: BLE001 - report any local failure plainly
            errors.append(f"faster-whisper failed: {err}")

    if result is None:
        print("[fail] transcription failed:\n  - " + "\n  - ".join(errors), file=sys.stderr)
        return 2 if not key and args.engine == "gemini" else 1
    print(result["text"])
    print(f"[ok] {result['engine']} ({result['model']})", file=sys.stderr)
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
