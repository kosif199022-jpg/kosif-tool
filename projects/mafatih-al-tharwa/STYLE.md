# STYLE.md — مفاتيح الثروة (Keys to Wealth)

## 1. Reference
| Item | Value |
|---|---|
| Style id | `kinetic-arabic` (KOSIF original style) — used as creative direction |
| Reference video | None supplied; the kinetic-arabic entry has no video. Nothing was copied from any reference. |
| Deliverable | 9:16 · 1080x1920 · 30 fps · 640.29 s · H.264 + AAC |
| Stack | ffmpeg-graded archival b-roll + deterministic HTML/SVG/Canvas overlay (seek(t)) composited with Playwright + ffmpeg |

## 2. Observed (measured from the inputs)
| Observation | Evidence |
|---|---|
| Voice: Gulf Arabic monologue, 640.29 s, mono AAC 44.1 kHz 64 kb/s, −22.4 LUFS integrated, LRA 10.2 LU | ffprobe, ffmpeg ebur128 |
| 12 s passage at 214.8–224.5 s missed by Whisper's VAD; recovered by re-transcribing without VAD | silencedetect showed speech energy; fill.json |
| Archival films are 640×480, 4:3; mix of B&W (Steel, Bank, Money, Books) and colour (Dynamic City, Copper) | ffprobe / contact sheets |

## 3. Assumed
| Assumption | Reason | Impact if wrong |
|---|---|---|
| Vertical 9:16 for phones, footage full-bleed | User asked for 9:16 with every video fitted to it | 4:3 sources lose their sides and are upscaled ~4×; grain hides the softness |
| Dialect kept in captions, only mishearings and names corrected | Captions should match what is heard | User may prefer MSA captions — edit `src/prep_words.py` FIX list |
| "21 سنة" (Bob's age) and "واحد وثمانين" shown only as spoken | Facts not verified; no hero graphic asserts an unspoken date except "1981" on the timeline, which the speaker says | If the speaker misspoke, change words/timeline text |
| Spelling of names: كارنيجي، نابليون هيل، بوب بروكتر، راي ستانفورد، إيرل نايتنجيل، لويد كونانت، ساندي | Common Arabic spellings | Cosmetic |

## 4. Design tokens
### 4.1 Colours
| Token | Value | Use |
|---|---|---|
| ink | #0B0906 | scrims, panels |
| gold | #E2B65C | accents, active word, frames, icons |
| gold-hi / gold-lo | #F6DC9A / #9A7432 | gradient foil, glints |
| cream | #F4EAD6 | primary text |
| muted | rgba(244,234,214,.55) | secondary text, upcoming words |
| red | #D9573F | debt, "مستحيل" stamps, failure |
| footage grade | hue s=0 → sepia matrix → contrast 1.12, brightness −0.07, gamma .95; lanczos 2560×1920 → 1080×1920 crop; unsharp 0.45; vignette π/4.5; grain 8 | archival unity, full-bleed 9:16 |

### 4.2 Type (all OFL, bundled in src/fonts)
| Role | Family | Weight | Size @1080 | Direction |
|---|---|---|---|---|
| Hero titles / names | Reem Kufi | 700 | 92–200 px | RTL |
| Quotes / book titles | Amiri | 700 | 64–120 px | RTL |
| Captions | Cairo | 800 | 70 px, line-height 1.55 | RTL |
| Pills / labels | Cairo | 700–800 | 33–64 px | RTL |
| Numbers | Cairo 900, tabular, `<bdi>` LTR isolate inside RTL lines | 900 | 110–200 px | LTR isolated |

### 4.3 Motion
| Element | Timing | Easing |
|---|---|---|
| Caption phrase in / out | 0.22 s in from −0.15 s; 0.14 s out | out-cubic / linear |
| Active word | lights 60 ms before onset; scale 1→1.07 | back |
| Key-word underline | sweeps over the spoken word duration | out-cubic |
| Word/line reveals | right→left clip-path wipe 0.5–0.9 s | out-cubic |
| Pills | 0.4–0.45 s pop | back (s=1.6) |
| Counters | 0.9–10 s count | out-quint |
| Stamps | 0.32 s scale 2.4→1 + damped shake | out-quint |
| B-roll | push-in 1.00→1.07 / pull-out / 220 px sliding pan per clip | linear |

Arabic words are never split into letters; no letter-spacing on Arabic.
