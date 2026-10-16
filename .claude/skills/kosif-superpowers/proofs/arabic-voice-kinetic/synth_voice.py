#!/usr/bin/env python3
"""Piper (ar_JO-kareem-medium) voice + ground-truth word timing from the model itself.

Piper >= 1.8 can expose per-phoneme sample counts (include_alignments=True, needs the
`onnx` package). We split each sentence's phonemes on spaces to get word spans, so
tts_align.json is the exact time the model spent on every word. The film itself is
timed from Whisper (the general pipeline for any voice); tts_align.json is the oracle
that measures how far Whisper's timing is from the truth.

usage: python synth_voice.py model.onnx line.txt voice_raw.wav tts_align.json
"""
import json
import sys
import wave

import numpy as np
from piper import PiperVoice, SynthesisConfig

model, line_path, out_wav, out_json = sys.argv[1:5]
LENGTH_SCALE, SENTENCE_SILENCE = 0.95, 0.30

lines = [l.strip() for l in open(line_path, encoding="utf-8") if l.strip() and not l.startswith("#")]
text = lines[0]
voice = PiperVoice.load(model, include_alignments=True)
cfg = SynthesisConfig(length_scale=LENGTH_SCALE)
sr = voice.config.sample_rate

pcm, words, cursor = [], [], 0
for i, chunk in enumerate(voice.synthesize(text, cfg, include_alignments=True)):
    if i > 0:
        gap = np.zeros(int(sr * SENTENCE_SILENCE), dtype=np.int16)
        pcm.append(gap)
        cursor += len(gap)
    assert chunk.phoneme_alignments, "model did not return alignments"
    pos, cur = cursor, None
    for al in chunk.phoneme_alignments:
        ph = al.phoneme
        if ph in (" ", "^", "$"):  # word / sentence boundary
            if cur is not None:
                words.append(cur)
                cur = None
        elif ph in ".,،؟!:;":  # espeak break marks (also inside words): never extend a word
            pass
        else:
            if cur is None:
                cur = {"phonemes": "", "start": pos / sr}
            cur["phonemes"] += ph
            cur["end"] = (pos + al.num_samples) / sr
        pos += al.num_samples
    if cur is not None:
        words.append(cur)
    audio = chunk.audio_int16_array
    pcm.append(audio)
    cursor += len(audio)

data = np.concatenate(pcm)
with wave.open(out_wav, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(sr)
    w.writeframes(data.tobytes())
for w_ in words:
    w_["start"], w_["end"] = round(w_["start"], 3), round(w_["end"], 3)
json.dump(words, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(data) / sr:.3f} s, {len(words)} words")
for w_ in words:
    print(f'{w_["start"]:6.3f}-{w_["end"]:6.3f}  {w_["phonemes"]}')
