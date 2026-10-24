# TEST REPORT — «العينين سابقة الكلام» neon lyric film

| Check | Target | Measured | Result |
|---|---|---|---|
| Frame | 1080×1920, 9:16 | 1080×1920 | ✅ |
| fps / frames | 30 | 30 fps, 1366 frames | ✅ |
| Duration | = source 45.533 s | 45.533 s (render_html VERIFY OK) | ✅ |
| Audio sync | lag 0 | cross-correlation vs source: 0.0 ms | ✅ |
| Audio change | none | no gain/EQ/effects; re-muxed as AAC 198 kb/s, waveform correlation 0.9996 with source | ✅ |
| Lyrics | match on-screen text of source | 17 lines checked against source frames every 0.5 s | ✅ |
| Word sync | ignition on sung word | whisper word onsets, hand-corrected to the source's line changes (±0.25 s) | ✅ |
| Arabic | no split letters | words lit whole, RTL layout, auto-fit ≤ 900 px | ✅ |
| Visual QA | frames checked | 12 stills during build + 5 frames from the delivered MP4 | ✅ |
| Render time | — | 1057 s on CPU (≈0.77 s/frame) | — |

## Credits and licences
- Style: AI Style Atlas #19 «Neon Sign at Night» (Futurepedia), prompt + reference techniques supplied by the user.
- Fonts (SIL OFL 1.1, in `film/fonts/`): Marhey, Aref Ruqaa, Reem Kufi, Lalezar.
- Audio and lyrics: the TikTok video supplied by the user (@rap_societyy_); kept local, never committed.
