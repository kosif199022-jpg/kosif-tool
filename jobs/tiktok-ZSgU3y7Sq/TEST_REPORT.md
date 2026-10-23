# TEST REPORT — «مطر الرحمة» دعاء الجمعة 23-10-2026 (Plan B)

| Check | Target | Measured | Result |
|---|---|---|---|
| Frame | 1080×1920, 9:16 | 1080×1920 | ✅ |
| fps / frames | 30 | 30 fps, 1,411 frames | ✅ |
| Duration | = audio (47.02 s) | video 47.033 s / audio 47.020 s | ✅ |
| Audio | original, untouched | stream copy, MD5 `3f00146c…` source = output | ✅ |
| Footage | real Masjid al-Haram, vertical | 9 Pexels clips (1080×1920 / 2160×3840; one 720×1280), fetched by id with `stock_fetch.py`, no API key | ✅ |
| Rain | real, follows the dua | Pexels 36344044 rain-on-black, screen-blended in two depth layers; intensity 0.22 → 0.95 at «يا ملاذي عند كربتي» → 0.3 at «بردًا وسلامًا» → 0 at «ودبّر لي أمري» | ✅ |
| Text | correct, readable | full tashkeel; Al-Ahqaf 46:15 written from the Mushaf with ﴿ ﴾ and citation; soft letter halo, no band over the footage | ✅ |
| Word sync | onset | faster-whisper large-v3 word timings (17 of 18 phrases matched 1:1, one even split) | ✅ |
| Visual QA | frames checked | 10 key moments, two legibility crops at full size, reframing check, 10 frames from the delivered MP4 | ✅ |

Changes made during QA: the verse moved from the kiswah close-up (gold on gold) to night Kaaba shots; two crowd shots reframed towards the Kaaba.

## Credits and licences
- Footage: Pexels License — 20324052, 35155732, 35325576, 35189276, 9112700, 27411329, 20525447, 35155761, 34683762, 34444589, 35189259; rain 36344044.
- Audio: dua from @ali1.697 (TikTok sound reuse, as with the previous jobs); credited on screen.
- Fonts (SIL OFL 1.1): Amiri, Reem Kufi.
