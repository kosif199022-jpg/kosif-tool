#!/usr/bin/env python3
"""Build words.json / words.js (word, start, end) for the film.

Text: faster-whisper words, checked 1:1 against the script (line.txt); the
display spelling and key-word flags come from line.txt.

Timing, measured on this voice against Piper's own phoneme durations:
  whisper-small word starts are EARLY by a median of ~130 ms (max 670 ms after
  a pause), even when run per pause-chunk. Pause snapping fixes phrase-initial
  words, but interior Arabic word joins have no energy dip to snap to.
So:
  * with tts_align.json (TTS voice): start/end = Piper phoneme timing + lead
    (exact; sub-frame), whisper times kept as asr_start/asr_end for the audit;
  * without it (a human voice): whisper + pause snapping (a word whose span
    contains a >=150 ms pause starts after it / ends before it).
    Expect ~+-150 ms; use a CTC forced aligner when you need <=100 ms.

usage: python align_words.py voice_master.wav asr_raw.json line.txt words.json words.js [tts_align.json LEAD_S]
"""
import json
import sys

import librosa
import numpy as np

HOP = 0.010
wav, asr_path, line_path, out_json, out_js = sys.argv[1:6]
oracle = json.load(open(sys.argv[6], encoding="utf-8")) if len(sys.argv) > 7 else None
lead = float(sys.argv[7]) if oracle else 0.0

# ---- text ------------------------------------------------------------------
asr = json.load(open(asr_path, encoding="utf-8"))
lines = [l.rstrip("\n") for l in open(line_path, encoding="utf-8") if l.strip() and not l.startswith("#")]
display = [w.strip() for w in lines[1].split("|")]
keys = {int(k) for k in lines[2].split()}
assert len(display) == len(asr), f"{len(display)} script words vs {len(asr)} recognised words"
strip = lambda s: "".join(ch for ch in s if "ء" <= ch <= "ي")  # letters only, no tashkeel/punct
norm = lambda s: strip(s).replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")
text_match = sum(norm(a["word"]) == norm(d) for a, d in zip(asr, display))

# ---- whisper + pause snapping (the general path) ---------------------------
y, sr = librosa.load(wav, sr=16000, mono=True)
rms = librosa.feature.rms(y=y, frame_length=int(sr * 0.025), hop_length=int(sr * HOP))[0]
db = 20 * np.log10(np.maximum(rms, 1e-6))
quiet = db < np.median(db[db > -60]) - 26          # >= 26 dB under typical speech
pauses, i = [], 0
while i < len(quiet):                               # runs of quiet hops >= 150 ms (geminate stops are shorter)
    if quiet[i]:
        j = i
        while j < len(quiet) and quiet[j]:
            j += 1
        if j - i >= 15:
            pauses.append((i * HOP, j * HOP))
        i = j
    else:
        i += 1
a_start = [w["start"] for w in asr]
a_end = [w["end"] for w in asr]
for k in range(len(asr)):
    for p0, p1 in pauses:
        if a_start[k] - 0.05 <= p0 and p1 <= a_end[k] - 0.08:   # pause inside the head of the word
            a_start[k] = p1
        if a_start[k] + 0.08 <= p0 < a_end[k]:                 # pause inside the tail of the word
            a_end[k] = p0
            break

# ---- final timing ----------------------------------------------------------
words, err_raw, err_snap = [], [], []
for k, w in enumerate(asr):
    rec = {"word": display[k], "asr": w["word"], "key": k in keys}
    if oracle:
        s, e = oracle[k]["start"] + lead, oracle[k]["end"] + lead
        rec.update(start=round(s, 3), end=round(e, 3), timing="piper-phoneme")
        err_raw.append(1000 * (w["start"] - s))
        err_snap.append(1000 * (a_start[k] - s))
    else:
        rec.update(start=round(a_start[k], 3), end=round(a_end[k], 3), timing="whisper+pause-snap")
    rec.update(asr_start=round(a_start[k], 3), asr_end=round(a_end[k], 3))
    words.append(rec)

json.dump(words, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(out_js, "w", encoding="utf-8") as f:
    f.write("// Generated from words.json by align_words.py so the page also opens from file://\n")
    f.write("window.KOSIF_WORDS = " + json.dumps(words, ensure_ascii=False) + ";\n")

print(f"text: {text_match}/{len(asr)} whisper words match the script")
for k, w in enumerate(words):
    extra = f"  whisper raw {err_raw[k]:+5.0f} ms, snapped {err_snap[k]:+5.0f} ms" if oracle else ""
    print(f"{k:2d} {w['word']:>9s} {w['start']:6.3f}-{w['end']:6.3f}{' KEY' if w['key'] else '    '}{extra}")
if oracle:
    r, s_ = np.abs(err_raw), np.abs(err_snap)
    print(f"whisper start error vs Piper truth: raw median {np.median(r):.0f} / max {r.max():.0f} ms; "
          f"pause-snapped median {np.median(s_):.0f} / max {s_.max():.0f} ms; "
          f"snapped <=100 ms: {(s_ <= 100).sum()}/{len(s_)}  -> film uses Piper timing (error 0 ms by construction)")
