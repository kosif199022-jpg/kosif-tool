# Test report — Monday dua reel
- Output: out/KOSIF_Monday_Dua_1080x1920_60fps.mp4 (master, CRF 16) and out/KOSIF_Monday_Dua_share.mp4 (CRF 21)
- Video: H.264 High, 1080x1920, 60/1 fps, yuv420p, bt709, 1688 frames, 28.133 s
- Audio: original AAC (HE-AACv2 44.1 kHz stereo) stream-copied; packet MD5 identical to the supplied file (e96e0cea…)
- Decode: full ffmpeg decode, no errors
- Sync: caption words light at forced-aligned word onsets (MMS_FA, 39/39 words); cuts at phrase onsets minus 0.12 s
- Visual QA: contact sheet every 140 frames reviewed; no watermarks, embedded captions, or women/girls in used ranges
- Limits: 7 of 10 shots come from 720p free-tier sources, upscaled ~2.7x (sharpened, no detail invented)
