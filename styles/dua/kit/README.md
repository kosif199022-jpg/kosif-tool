# «الدعاء» kit — build a Friday dua reel from your own clips and voice

عدة جاهزة تعيد بناء أسلوب «الدعاء» بالقياسات نفسها (التوقيت، الأماكن، الألوان، الخطوط، الانتقالات) على لقطاتك وصوتك أنت.

## Files

| File | What it does |
|---|---|
| `../dua.style.json` | Measured spec: timing grammar, cut rule, layer boxes, colours, halo, grade, transitions, intro/outro motion |
| `../ANALYSIS.md` | Human-readable analysis (Arabic + English), measured vs assumed |
| `layers.cjs` | Renders each text layer to a transparent 1080×1920 PNG in Chromium (real Arabic shaping) |
| `build_dua.py` | Composes shots + transitions + text layers frame by frame and encodes one H.264 MP4 with your voice copied untouched |
| `fonts/` | Marhey (gold line) and Scheherazade New Bold (dua line), both SIL OFL 1.1, unmodified, with licences |
| `example/project.json` | A filled project you can copy |

The title «الجُمُعَة» and the date use the repo's KOSIF Jumuah font kit (`fonts/kosif-jumuah/`).

## Use it

```bash
# 1. put your clips (mp4/mov or jpg/png, one per phrase) and your voice in a folder
cp styles/dua/kit/example/project.json my-dua/project.json   # edit paths, date, lines, timings

# 2. preview (half size, fast)
python3 styles/dua/kit/build_dua.py my-dua/project.json --preview

# 3. final render
python3 styles/dua/kit/build_dua.py my-dua/project.json --out my-dua/dua.mp4
```

Needs Python 3 with numpy and Pillow, ffmpeg, Node with Playwright (`npm i playwright` or set `KOSIF_PLAYWRIGHT`). OpenCV speeds up the blurs when present.

### Timings from the voice

Each line needs `start`/`end` in seconds: the phrase onset is the cut. Either type them, or transcribe and pass `"asr": "asr.json"` (faster-whisper segments, one per line, in order). With faster-whisper, decode the audio yourself and pass a float32 numpy array; some PyAV builds reject its file path loader.

### Project keys

- `clips`: one per line, cycled if fewer. Video is cover-fitted and looped; stills get a 3 % slow push-in.
- `audio`: AAC/MP3/ALAC/AC-3/Opus are stream-copied (`-c:a copy`); the output audio packets are byte-identical to your file. Other codecs (e.g. WAV/PCM) cannot go in MP4, so they are encoded to AAC 320k and the report says so; keep your master.
- `date`, `subtitle`: the day number (first two digits) is its own animated layer.
- `transitions`: `"reference"` (the measured sequence) or a list of `blur_in | mirror_out_blur_in | zoom_out_cut | spin_zoom_blur | cut`, one per cut.
- `grade`: 0..1, how far each shot is pulled toward the measured warm low-key look.

The builder writes `<out>.report.json` (frames, fps, duration, transitions, audio mode). Verify with `python3 .claude/skills/kosif-superpowers/scripts/verify_video.py <out>`.

## Footage that fits

Quran, roses, incense burner with smoke, candles, warm lamps, prayer beads, ceramic vases; warm practical light, shallow depth of field. Avoid faces, logos, daylight and busy detail behind the top-right title.

## Rights

Use your own or licensed clips and voice. The reference reel, its footage, audio and creator handle are not part of this kit and are never reused.
