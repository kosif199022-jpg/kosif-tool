# تحليل أسلوب «الدعاء» / «Dua» style analysis

Measured on 2026-10-18 from an owner-supplied 15.43 s vertical reel (1080×1920, 60 fps, 926 frames). Every number below was read from the frames or the audio with code (OpenCV/numpy, ffmpeg ebur128, faster-whisper). Items marked **assumed** are judgement, not measurement. The machine-readable version is [`dua.style.json`](dua.style.json); the builder is in [`kit/`](kit/README.md).

قِيس كل رقم هنا من إطارات المقطع أو صوته بالكود. ما عليه علامة **assumed** تقدير وليس قياساً.

## 1. البنية والإيقاع / Structure and rhythm

- **القاعدة:** عبارة دعاء واحدة = لقطة واحدة = سطر واحد على الشاشة. 8 لقطات، 7 قطعات.
- **Rule:** one spoken phrase = one shot = one on-screen line. 8 shots, 7 cuts at 1.67, 4.52, 6.30, 8.02, 9.76, 11.22, 14.18 s.
- Cuts land on phrase onsets: mean |offset| 0.10 s, max 0.18 s.
- Shot length follows the phrase: 1.25–2.96 s, median 1.73 s. The long phrases (5+ words) get the longest shots.
- Dua line: fades in 0.2 s after its cut, out 0.3 s before the next cut; about 0.45 s with no line between phrases.

## 2. الألوان / Colour

| Element | Measured |
|---|---|
| White text (title, date, dua) | `#FEFEFD` |
| Gold subtitle | `#FED27E` (flat, no gradient) |
| Halo | `#0C0805`, tight glow: background luma ~57 falls to ~13 at 2 px and recovers by 6 px; darkest slightly to the left. **Not** an offset drop shadow |
| Footage | warm low-key: Lab L 28–42, a +4…+13, b +4…+23, saturation 0.27–0.62, soft contrast; mean L 35.9 a 8.7 b 11.5 |
| Footage palette | `#402721` `#5C4C45` `#140C08` `#9E8B80` `#776B69` `#74351A` `#A46942` `#C5B8AE` |
| Vignette | none added (corner/centre luma ratio 1.065) |

## 3. الخطوط والتخطيط / Type and layout (1080×1920 px)

| Layer | Box (x0, y0, x1, y1) | Font used in the kit |
|---|---|---|
| Title «الجُمُعَة» | 603, 280, 955, 440 — right-aligned, 124 px right margin | composed Thuluth title from `fonts/kosif-jumuah` (OFL) |
| Date `22.08.2025` | 443, 450, 957, 570 — right-aligned | KOSIF Jumuah (Bodoni-style digits, OFL) |
| Gold «ليلة جمعة مبـــاركة» | 274, 665, 817, 789 — centred | Marhey 700 (OFL) — **assumed** closest match; the original is a rounded handwritten app font with a hooked kaf |
| Dua line | centred in 110–990 × 850–1100; single line centred at y 985; ink height 105 px; max width 880 px | Scheherazade New Bold (OFL) with manual kashida (ـــ) on final words — **assumed** closest match |

- العنوان والتاريخ والسطر الذهبي ثابتون طوال المقطع؛ سطر الدعاء وحده يتبدل.
- The reference shows a creator handle near y 1129–1170. The kit does not reproduce it; add the user's own handle there only if asked.

## 4. حركة الكتابة / Text motion

- **Intro (0–1.1 s):** footage fades from black over 0.6 s; title, date and gold line fade in 0.05→0.6 s. The day number «22» is a separate layer: it starts at the centre (~y 1020), rises on a soft arc past the gold line and lands in its slot left of `.08.2025`, 0.1→1.1 s, easeOutCubic. It is the only text element that travels.
- **Dua line:** opacity only. In 0.17 s (easeOutQuad), still hold (no scale, no drift), out 0.15 s (easeInQuad).
- **Outro:** «اللَّهُمَّ آمين 🤲» in at 14.37 s; the day number drifts −40 px (14.7→15.05 s, easeInOutSine); all text fades out 15.05→15.38 s while the footage continues.

## 5. الانتقالات / Transitions

CapCut-style, applied to the footage only. The text sits above and is never blurred.

| Kind | What happens | Used at |
|---|---|---|
| `blur_in` | hard cut; the incoming shot starts motion-blurred (~28 px) and clears in 0.17–0.35 s, easeOutCubic | 1.67, 6.30 s |
| `mirror_out_blur_in` | ~0.3 s before the cut the lower half of the outgoing shot reflects about the frame middle, then a `blur_in` | 4.52, 8.02, 9.76 s |
| `zoom_out_cut` | outgoing pushes in ~6 % over 0.1 s, cut into a light `blur_in` | 11.22 s |
| `spin_zoom_blur` | outgoing gets a growing radial/spin blur for ~0.45 s, cut into a strong radial blur that clears in ~0.17 s | 14.18 s |

## 6. الكاميرا واللقطات / Camera and footage

- Near-static shots, drift ≤ 3 px/s; the last shot is handheld (~10 px/s).
- Subjects: Quran, roses, vase, incense burner, books, lamp, prayer beads; warm practical light, shallow depth of field, bokeh.
- The kit adds a 3 % slow push-in to stills so photos do not sit dead.

## 7. الصوت / Audio

- Voice-dominant recited dua, −12.9 LUFS integrated, LRA 1.6 LU, −2.3 dBTP, spectral centroid 1422 Hz, AAC 44.1 kHz stereo. No music bed detected (**assumed** from the spectrum and the ASR, which hears only voice).
- The kit copies the user's track untouched (`-c:a copy`); a test build confirmed all 665 output audio packets byte-identical to the input.

## 8. ما لم يُنسخ / What is not reused

The reference footage, its audio and its creator handle are not stored in this repository and are not used by the kit. Fonts are open (OFL) substitutes, not the reference app fonts.
