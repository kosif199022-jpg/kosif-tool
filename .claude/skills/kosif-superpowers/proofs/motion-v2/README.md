# إثبات أدوات الحركة v2 — Motion v2 harness proof

What this proves: the numeric and ffmpeg checks behind the v2 easing, QA and trim records (verification log V1, V2 and V8 in `../../references/external-skills.md` §15) can be re-run from this folder. The harnesses here are our own code (numpy + ffmpeg, synthetic inputs, no third-party media). Powers backed: EASE-X01…X05, EASE-X09 (spring line), QA-X01, QA-X02, QA-X04, FOOT-X03.

- **Date / surface:** first run 2026-10-16 in a Claude Code cloud container; re-run the same day for this note with numpy 2.5.3 and ffmpeg 6.1.1, `python3 -I`.
- **Not here:** the owner's tools behind V4–V7 (`music_window.py`, `cut_audio.py`, `sound_kit.py`, `lens.py`) and the song film's `analyze.py` are owner material and are not vendored, so BEAT-X01…X05, GLOW-X01 and SYNC-X01 are 📄 documented, not ✅. V3 (textcheck) and V9 (Playwright recording) were not re-run for this note.

## Commands and results
| # | Command | Result (file) |
|---|---|---|
| V1 | `python3 -I ease_math_check.py` | peaks 1.500 / 10.00 / 20.00 = 1/(1−a); expoIn/expoOut slopes 6.250 / 6.250; r2 6.254 → influence 84; spring max 1.0736 at k 0.315; relay 0.45 → 26.2 % / 57 %; needle list … 161 581 581 161 … ([ease_math_check.out.txt](ease_math_check.out.txt)) |
| V2 | `python3 -I make_defects.py defects.mp4` then `frame_qa.py defects.mp4` (code in external-skills.md §10) | OUTLIER @30 (dAB 221.5, dAC 0.9), JUMP @50 (7.1 vs 0.45), FREEZE 70–81, DEAD AIR 0.40 s; exit 1 as designed ([frame_qa_defects.out.txt](frame_qa_defects.out.txt)) |
| V8 | `python3 -I gop_test.py <dir>` (10 s, 30 fps, GOP 60; want 1.3–3.3 s) | input-seek copy 62 frames / 2.167 s; output-seek copy 41 frames starting at frame 60; re-encode 60 frames / 2.000 s ([gop_test.out.txt](gop_test.out.txt)) |

## Files
`ease_math_check.py`, `make_defects.py`, `gop_test.py` — original to kosif-superpowers (same licence as this skill). Outputs `*.out.txt` are their captured stdout.
