# librosa/librosa - dissection for the Black Dragon (2026-11-10)

Commit 9fd51bee82537f099c040d1625c70f168702efda, ISC license, ~8.8k stars, installed version 1.0.0.

## What it really is
Pure-Python (NumPy/SciPy/numba) music-analysis library. No GPU, no network. Source under `librosa/`:
`beat.py` (beat_track, plp), `onset.py`, `segment.py` (recurrence_matrix, path_enhance, agglomerative,
subsegment), `decompose.py` (hpss, nn_filter), `feature/rhythm.py` (tempogram, tempo), `feature/spectral.py`
(chroma_cqt, mfcc, rms, melspectrogram), `effects.py`, `pitch.py` (yin/pyin).

## What the Dragon already uses (Grep over kosif-tool)
`librosa.load`, `onset.onset_strength`, `onset.onset_detect`, `beat.beat_track`, `frames_to_time`,
`feature.rms`, `feature.melspectrogram`, `yin` (dm_analyze.py:627-644, proofs/beat-sync/drums.py, fam_w3_05.py, make_media.py).
NOT used anywhere: `segment.*`, `beat.plp`, `feature.tempogram`, `decompose.hpss`/`effects.hpss`, `chroma_*`,
`mfcc`, `util.sync`.

## Capabilities worth taking (see capabilities.json)
1. Structural segmentation: `segment.py:1057` agglomerative on beat-synced chroma+MFCC -> sections.
2. Recurrence matrix + path_enhance (`segment.py:345`, `:1151`) for repeat detection (verse/chorus). Source-linked only.
3. HPSS `decompose.py:208`: percussive part for beats, harmonic part for chroma.
4. PLP `beat.py:312`: tempo-drift tolerant pulse, used as beat fallback.
5. Tempogram `feature/rhythm.py:38`: tempo-change evidence (source-linked).
6. Chroma key estimate `feature/spectral.py:1333` + Krumhansl profiles (own port of published numbers).
7-10. Own heuristics on top (native): downbeat phase, drop/climax from RMS contrast, strong cut list, energy curve.

## Native implementation
`native_musicmap.py` (stdlib+numpy+librosa). Subcommands: `map <audio> [--sections N] [--max-sec S] [--out f.json] [--json]`, `self-test`.
JSON keys: tempo_bpm, beats, downbeats, downbeat_phase, strong_cuts[{t,kind}], sections[{start,end,mean_energy,role}],
drops[{t,rise}], climax_t, energy_curve{hz:2,values}, key.
Self-test builds a 48 s synthetic track (120 BPM: soft pad, build-up, loud kick drop at 32 s) and asserts results.

Actual output of `python -I native_musicmap.py self-test`:
```
PASS tempo ~120 (or 60/240 octave): 117.5
PASS beats found: 96
PASS downbeat spacing = 4 beats: 2.0
PASS drop within 1.5s of 32s: [{'t': 33.27, 'rise': 0.755}]
PASS climax in last section (>=32s): 45.1
PASS section boundaries near 16s and 32s (+-3s): [16.02, 32.16]
PASS last section is high-energy: {'start': 32.16, 'end': 48.0, 'mean_energy': 0.922, 'role': 'high'}
PASS strong cuts include drop/section/downbeat: 45
PASS key estimated: {'key': 'A minor', 'confidence': 0.898}
SELF-TEST OK (9/9)
```
Note: tempo 117.5 vs 120 (beat tracker prior), drop snapped to the nearest downbeat (1.27 s late, within tolerance);
a finer snap can use the raw contrast peak. First run is slow (numba JIT, ~2+ min cold).

## Dragon coverage vs new
Covered: load, onset, beat_track, rms, yin. New: sections, HPSS, PLP fallback, key, downbeat heuristic, drops,
climax, merged cut list. Hook point: dm_analyze.py music step could call `native_musicmap.analyze()` and feed
`strong_cuts` into dm_edl.

## License
ISC (permissive). May vendor with the license line. Our script is original code using the public API; no copied chunks.

## Risks
Heuristics only: octave errors in tempo, downbeat phase has no meter model, drop threshold 0.18 tuned on synthetic
data (validate on real songs), 4/4 assumed, mp3 needs ffmpeg/audioread. Dependency weight (numba).

## REA evidence log
REA is not a fit for a plain-source Python library (REA skill says use normal reading). Ran only `rea --version`
(6.8.0, confirms install). No MCP REA tools run, no Evidence ids. Everything else read by hand with Grep/Read.
