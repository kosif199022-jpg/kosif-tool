"""Shared helpers for programs that need a locally installed library or a downloaded model.

Models are cached under KOSIF_MODEL_CACHE (default ~/.cache/kosif-models) so a second run is offline.
These programs are registered with env_scope=local: they prove the technique on this machine only.
"""
from __future__ import annotations
import json
import os
import subprocess
import urllib.request
import wave
from pathlib import Path

CACHE = Path(os.environ.get("KOSIF_MODEL_CACHE", Path.home() / ".cache" / "kosif-models"))
PIPER_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/ar/ar_JO/kareem/medium/"
PIPER_VOICE = "ar_JO-kareem-medium.onnx"
# A short planted Arabic line: its words are the known answer for speech round trips.
LINE_AR = "القراءة نور والكتاب صديق لا يخون"


def fetch(url: str, dest: Path) -> Path:
    if dest.is_file() and dest.stat().st_size:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url, timeout=120) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 20):
            f.write(chunk)
    tmp.rename(dest)
    return dest


def piper_model() -> Path:
    d = CACHE / "piper"
    fetch(PIPER_BASE + PIPER_VOICE + ".json", d / (PIPER_VOICE + ".json"))
    return fetch(PIPER_BASE + PIPER_VOICE, d / PIPER_VOICE)


def piper_say(text: str, out_wav: Path, length_scale: float = 1.0, alignments: bool = False):
    """Synthesise text with Piper; returns (seconds, words) where words are phoneme-timed spans."""
    import numpy as np
    from piper import PiperVoice, SynthesisConfig
    voice = PiperVoice.load(str(piper_model()), include_alignments=alignments) if alignments \
        else PiperVoice.load(str(piper_model()))
    cfg = SynthesisConfig(length_scale=length_scale)
    sr = voice.config.sample_rate
    pcm, words, cursor = [], [], 0
    kw = {"include_alignments": True} if alignments else {}
    for chunk in voice.synthesize(text, cfg, **kw):
        if alignments and chunk.phoneme_alignments:
            pos, cur = cursor, None
            for al in chunk.phoneme_alignments:
                ph = al.phoneme
                if ph in (" ", "^", "$"):
                    if cur is not None:
                        words.append(cur)
                        cur = None
                elif ph not in ".,،؟!:;":
                    if cur is None:
                        cur = {"start": pos / sr}
                    cur["end"] = (pos + al.num_samples) / sr
                pos += al.num_samples
            if cur is not None:
                words.append(cur)
        pcm.append(chunk.audio_int16_array)
        cursor += len(chunk.audio_int16_array)
    data = np.concatenate(pcm)
    with wave.open(str(out_wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(data.tobytes())
    return len(data) / sr, words, sr


def whisper(model_name: str = "base"):
    from faster_whisper import WhisperModel
    return WhisperModel(model_name, device="cpu", compute_type="int8",
                        download_root=str(CACHE / "whisper"))


def transcribe_words(model, wav: Path, language: str | None = "ar") -> tuple:
    segs, info = model.transcribe(pcm16k(wav), language=language, word_timestamps=True, beam_size=5,
                                  vad_filter=False)
    words = []
    for s in segs:
        for w in s.words or []:
            words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3),
                          "p": round(w.probability, 3)})
    return words, info


def pcm16k(path: Path):
    """Decode any audio/video to 16 kHz mono float32 with ffmpeg (no PyAV dependency)."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path), "-f", "s16le",
                          "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype("float32") / 32768.0


def norm_ar(s: str) -> str:
    import re
    s = re.sub(r"[ً-ْـ]", "", s)  # tashkeel and tatweel
    s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
    return re.sub(r"[^\w\s]", "", s).strip()


def word_match(said: list, heard: list) -> float:
    """Share of planted words heard, in order (longest common subsequence over normalised words)."""
    a = [norm_ar(x) for x in said]
    b = [norm_ar(x) for x in heard if norm_ar(x)]
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a)):
        for j in range(len(b)):
            dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
    return dp[-1][-1] / max(1, len(a))


def ffmpeg(*args) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-y", *args], check=True)


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams",
                          str(path)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)
