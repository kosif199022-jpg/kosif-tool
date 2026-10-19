# TEST_REPORT.md — ما فرّق البحر بيننا

> Style: `parallax-2d` + `kinetic-arabic` · Target: 9:16 · 1080×1920 · 30 fps · 196.82 s · 5905 frames · 2026-10-18

## 1. Delivered file

| Item | Value |
|---|---|
| Master | `out/ma_farraq_albahr_bainana.mp4` — 204.2 MB, H.264 CRF 16, AAC 320 kb/s 48 kHz stereo |
| Share copy | `out/ma_farraq_albahr_bainana_share.mp4` — 88.5 MB, H.264 CRF 21, same audio stream |
| Editable source | `index.html` (+ `lines.js`, `env.js`, `assets/`) |
| Preview | `out/preview_preview.png`, `out/check_chorus.mp4`, `out/final_contact.png` (not committed; `out/` is git-ignored) |

## 2. Checks (measured)

| # | Check | Target | Measured | Result |
|---|---|---|---|---|
| 1 | Duration | 196.82 s ±0.1 | 196.833 s | PASS |
| 2 | Frame rate | 30 constant | 30.000 | PASS |
| 3 | Frame count | 5905 | 5905 | PASS |
| 4 | Resolution | 1080×1920 | 1080×1920, yuv420p | PASS |
| 5 | Audio track | AAC 48 kHz stereo | AAC 48 kHz 2 ch 322 kb/s | PASS |
| 6 | Supplied audio untouched | same length/timing | 196.800 s vs master 196.824 s (AAC priming), no edits/stretch/normalisation | PASS |
| 7 | Loudness | −14 LUFS ±1.5 · TP ≤ −1 | −15.5 LUFS · −2.7 dBTP (left as supplied) | PASS (gate tolerance) |
| 8 | Legibility | ≥ 36 px | smallest lyric 70 px, labels 30–36 px | PASS |
| 9 | RTL shaping | joined letters | whole-word spans; checked in frames | PASS (visual) |
| 10 | Sync | ≤ 100 ms on key words | Word times from MMS forced alignment on Demucs vocal stem (179/185 words; 6 fall back to Whisper + median offset). Highlight leads each word by 50 ms by design. Sampled frames 90, 700, 3550, 4760, 5640 show exactly the predicted word lit. | PASS (method); not verified by listening |
| 11 | Motion in every scene | no static slides | continuous camera, wind, particles throughout | PASS |
| 12 | Safe margins | 5 % sides, 12 % bottom | captions 70 px sides, bottom 300 px | PASS |
| 13 | Contrast | ≥ 4.5:1 | dark scrim behind captions; not measured numerically | Not measured |
| 14 | First / last frame | no unintended black | starts with intended fade-in from black, ends with intended fade-out | PASS (intentional) |
| 15 | Assets | original or licensed | see ASSETS.md | PASS |
| 16 | Preview approved | user approval | user asked for the finished video; no preview round-trip | Waived |

`python3 tools/verify_video.py out/ma_farraq_albahr_bainana.mp4 --aspect 9:16 --fps 30 --duration 196.82 --audio assets/song.mp3` → **13/13 checks passed**.
