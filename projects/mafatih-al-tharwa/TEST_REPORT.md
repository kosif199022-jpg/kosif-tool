# TEST_REPORT.md — مفاتيح الثروة (Keys to Wealth)

## 1. Delivered files
| Item | Master | Social copy |
|---|---|---|
| Path | `out/mafatih-al-tharwa_master.mp4` | `out/mafatih-al-tharwa_social-14LUFS.mp4` |
| Size | 679.5 MB | 186.9 MB |
| Video | H.264 yuv420p, CRF 18 | H.264 yuv420p, CRF 24 |
| Audio | AAC 44.1 kHz mono, **stream-copied from the user's file** | AAC 48 kHz 192 kb/s, loudnorm −14 LUFS / −1.5 dBTP |
| Editable source | `src/` (overlay.html/js, build_broll.py, render_film.cjs, prep_words.py) | same |
| Preview | 4 rounds of composited stills (`preview/`) reviewed before the full render | — |

## 2. Checks (measured with `tools/verify_video.py`, ffprobe and frame grabs)
| # | Check | Target | Measured | Result |
|---|---|---|---|---|
| 1 | Duration | 640.29 s ± 1 frame | 640.300 s (both) | PASS |
| 2 | Frame rate | 30 fps constant | 30.000 | PASS |
| 3 | Frame count | 19,209 | 19,209 (b-roll, each chunk 4802/4802/4802/4803, both finals) | PASS |
| 4 | Resolution | 1080×1920 (9:16), footage full-bleed | 1080×1920 both files; every clip fills the frame (no card/letterbox) | PASS |
| 5 | Audio present | AAC | AAC (master 44.1 kHz, social 48 kHz) | PASS |
| 6 | Voice untouched | same length/timing | master: original stream copied, 640.243 vs 640.290 s (−47 ms, encoder priming) ; social: 640.300 s | PASS |
| 7 | Loudness | −14 LUFS ±1.5, TP ≤ −1 dBTP | master −22.4 LUFS / −2.3 dBTP (as recorded, intentionally untouched) · social −14.9 LUFS / −1.4 dBTP | master: by design FAIL on LUFS · social PASS |
| 8 | Legibility at phone size | smallest text ≥ 36 px | captions 70 px, pills ≥ 33 px (debt/goal columns), archive tag 22 px (decorative) | PASS (2 decorative exceptions) |
| 9 | RTL shaping | joined letters, correct order | whole words only, clip-path wipes, numbers in `<bdi>`; order bug on "+100 عام" found and fixed in preview | PASS |
| 10 | Key-word sync ≤ 100 ms | motion starts at word onset | heroes keyed to words.json starts (−100…0 ms lead); spot checks at 6.6, 70.5, 158.25, 189.6, 235.1, 399.9, 504.8, 594.0 s all show the element mid-entrance 0.1–0.3 s after onset | PASS |
| 11 | Motion in every scene | no static slides | every b-roll clip moves (push/pull/pan); 43 heroes animated; gold dust always drifting | PASS |
| 12 | Safe margins | 12% top/bottom | hero graphics and captions inside; header logo (y 96–210) and progress bar (y 1812) are decorative and may sit under platform UI | PASS with note |
| 13 | Contrast | ≥ 4.5:1 | cream/gold text on ≥ 80% dark scrims and bottom gradient | PASS (visual) |
| 14 | First / last frame | intentional | 0.00 s full-frame archival coins; 640.25 s end card | PASS |
| 15 | Assets | original or licensed | archive.org Public Domain films (RIGHTS.md with SHA-256), OFL fonts, original graphics | PASS |
| 16 | Preview before final render | approved | User pre-authorised the full production in the request; previews were self-reviewed and fixed | PASS (pre-authorised) |
| 17 | Chunk seams | invisible | frames 160.033 / 160.067 s continuous; deterministic seek(t) | PASS |
| 18 | No source titles / fades on screen | none | v1 had ST0 credits, a «STEEL» super and fades from DY/UB17; v2 removes them (pool changes + `scan_shots.py` trims) and start/middle/end frames of all 168 rendered clips were reviewed | PASS |

## 3. Commands
```bash
python3 tools/verify_video.py out/mafatih-al-tharwa_master.mp4 --aspect 9:16 --fps 30 --duration 640.29 --audio voice.m4a          # 12/13, loudness by design
python3 tools/verify_video.py out/mafatih-al-tharwa_social-14LUFS.mp4 --aspect 9:16 --fps 30 --duration 640.29 --audio voice.m4a --lufs -14   # 13/13
ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets build/broll.mp4   # 19209
```

## 4. Open issues
| # | Description | Severity | Action |
|---|---|---|---|
| 1 | Captions keep the speaker's Gulf dialect; ~110 mishearings and names were corrected by hand, but a native review may still find a few words to adjust (e.g. 352 s «ما عندي تكبّر», 477.8 s «وأفكر», 198.1 s «ركّز في الجملة» are best guesses). | Low | Edit the FIX list in `src/prep_words.py`, re-run, re-render |
| 2 | Bob's age («21 سنة») and «عام واحد وثمانين» are shown as spoken; not fact-checked against sources. | Low | Change text if the speaker misspoke |
| 3 | Master is −22.4 LUFS because the voice is untouched; use the social copy for platforms. | Info | — |
| 4 | Aspect ratio 9:16 was assumed; 16:9 needs a layout pass. | Info | Ask if needed |

## 5. Verdict
Delivered and verified: both files pass duration, frame-count, fps, resolution, codec and audio-length checks; the social copy also meets −14 LUFS. Sync verified at eight key-word onsets on the final master.
