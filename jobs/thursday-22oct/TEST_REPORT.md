# TEST REPORT — دعاء يوم الخميس 22-10-2026 (Plan B «نور الكلمة»)

| Check | Target | Measured | Result |
|---|---|---|---|
| Frame | 1080×1920, 9:16 | 1080×1920 | ✅ |
| fps / frames | 30 | 30 fps, 745 frames | ✅ |
| Duration | = audio (24.845 s) | video 24.833 s / audio 24.845 s (Δ 12 ms) | ✅ |
| Audio untouched | bit-identical to source | stream MD5 `f00c01a4…` source = output (stream copy) | ✅ |
| Loudness | TikTok ≈ −14 LUFS | −14.3 LUFS, peak −0.3 dBFS (original, unchanged) | ✅ |
| Word sync | words appear on onset | each word fades in at onset −0.14 s, glows until end +0.12 s (faster-whisper medium timings) | ✅ |
| Cuts | on phrase onsets | 13 shots, cut 80 ms before each phrase, 0.36 s dissolve | ✅ |
| Date | Thursday 22 Oct 2026 | 22.10.2026 · ١١ جمادى الأولى ١٤٤٨ هـ (Umm al-Qura; source 08.10 = 27 Rabi' II checked) | ✅ |
| Handle | @OAUN.11 | at the arch base from 1.6 s | ✅ |
| Arabic shaping | joined, RTL | checked on full-res frame 24.4 s and 8-frame preview | ✅ |
| Safe zones | clear of TikTok UI | text between y 200 and 1700, centred width ≤ 800 px | ✅ (visual) |

## Credits and licences
- Footage: Mixkit free stock video (Mixkit Free License), clips 9998, 6850, 15694, 11922, 9805, 21168, 21114, 34189, 22166, 34251, 4312, 17255, 9736 — 720p sources (4312 at 1080p).
- Fonts (SIL OFL 1.1): Aref Ruqaa Bold (title), Reem Kufi (dates, handle), Amiri Bold (dua), KOSIF Jumuah Bold («آمين»).
- Audio: the user's own TikTok video (@oaun.11), unchanged.

## Rebuild
`python3 build/shots.py` (needs `stock/*.mp4`) → `node tools/render_html.cjs --in jobs/thursday-22oct/film/index.html --out jobs/thursday-22oct/out/video_noaudio.mp4 --crf 16` → mux `-map 0:v -map 1:a -c copy` with `source/src.mp4`.
