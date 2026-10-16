#!/usr/bin/env python3
"""faster-whisper (small, int8, CPU) -> raw word timestamps.
Pass a 16 kHz numpy array (librosa) instead of a path: PyAV in this venv breaks on paths.
usage: HF_HOME=<models/hf> python transcribe.py voice_master.wav asr_raw.json"""
import json
import sys

import librosa
from faster_whisper import WhisperModel

path, out = sys.argv[1], sys.argv[2]
audio, _ = librosa.load(path, sr=16000)
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, _ = model.transcribe(audio, language="ar", word_timestamps=True, beam_size=5, vad_filter=False)
words = [{"word": w.word.strip(), "start": round(float(w.start), 3), "end": round(float(w.end), 3),
          "p": round(float(w.probability), 3)} for s in segments for w in s.words]
json.dump(words, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(words), "words:", " ".join(w["word"] for w in words))
