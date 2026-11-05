"""VOICE-01 Piper offline Arabic TTS (env_scope=local): synthesize, resample 48 kHz, loudnorm."""
from __future__ import annotations
import re
import subprocess
from pathlib import Path
from ._mind_common import eq, truth
from . import _local_models as L


def voice01(work):
    work = Path(work)
    raw = work / "raw.wav"
    secs, _, sr = L.piper_say(L.LINE_AR, raw)
    slow = work / "slow.wav"
    secs_slow, _, _ = L.piper_say(L.LINE_AR, slow, length_scale=1.15)
    out = work / "voice48k.wav"
    L.ffmpeg("-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", str(out))
    meas = subprocess.run(["ffmpeg", "-nostdin", "-i", str(out), "-af", "ebur128", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", meas)[-1])
    a = L.probe(out)["streams"][0]
    words, _ = L.transcribe_words(L.whisper("small"), raw, "ar")
    return [eq("model sample rate", sr, 22050), eq("resampled", int(a["sample_rate"]), 48000),
            eq("loudness -16 LUFS", lufs, -16.0, tol=1.5),
            truth("length_scale 1.15 is slower", secs_slow > secs * 1.05, (secs, secs_slow)),
            truth("speech is the planted Arabic line (ASR >= 80%)",
                  L.word_match(L.LINE_AR.split(), [w["w"] for w in words]) >= 0.8)]


PROGRAMS = {"VOICE-01": voice01}
