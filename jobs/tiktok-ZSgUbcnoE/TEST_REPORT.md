# TEST REPORT — دعاء الخميس «ولسوف يعطيك ربك فترضى» (Plan B «خط النور»)

| Check | Target | Measured | Result |
|---|---|---|---|
| Frame | 1080×1920, 9:16 | 1080×1920 | ✅ |
| fps / frames | 30 | 30 fps, 812 frames | ✅ |
| Duration | = audio | video 27.067 s / audio 27.099 s (source 27.074 s + AAC padding) | ✅ |
| Audio sync | lag 0 | cross-correlation vs source: 0.0 ms | ✅ |
| Audio change | uniform gain only (approved) | +5.0 dB measured, no compression/EQ | ✅ |
| Loudness | ≈ −14 LUFS | −14.5 LUFS, peak −0.8 dBFS (source −19.5 / −5.8) | ✅ |
| Footage clarity | nothing over the footage between transitions | no blur, wash, particles or text inside the panel; effects only in a 0.54 s window around each cut | ✅ |
| Panel sharpness | ≤ 1.4× upscale | 778×720 crop of 720p source → 1000×926 (1.29×) | ✅ |
| Verse | exact text | ﴿وَلَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَىٰ﴾ (الضحى ٥), revealed with the recitation, not split into effects | ✅ |
| Word sync | onset | each word enters at onset −0.16 s; gold kashida under the spoken word | ✅ |
| Date / handle | 22.10.2026 · ١١ جمادى الأولى ١٤٤٨ هـ · @kosif | rendered | ✅ |
| Visual QA | frames checked | 8-frame preview, 10 transition mid-points, 8 frames from the delivered MP4 | ✅ |

## Transitions (meaning-matched)
star bloom (open) · cross-zoom «يا رب» · eight-point star «سورة الواقعة» · light blade «الخالق والرازق» · vertical push «إلا إليك» · double doors «أبواب الخير» · dissolve «ديوننا» · light wave «وفرّج همومنا» · rain ripples «عطاءً واسعًا» · dissolve «حياة طيبة» · bloom «وفرحًا يدوم»

## Credits and licences
- Footage: Mixkit free stock video (Mixkit Free License) — 9998, 34223, 34208, 31629, 34251, 30867, 22166, 21168, 25375, 11926, 4312.
- Fonts (SIL OFL 1.1, in `../thursday-22oct/fonts/`): Aref Ruqaa, Reem Kufi, Amiri, KOSIF Jumuah.
- Audio: the user's own TikTok video (@oaun.11), gain +5 dB only.
