# الترسانة — كل مكتبة تقدر تنزّلها وتستخدمها / Libraries arsenal

فُحص فعليًا في هذه الحاوية يوم 2026-10-16: كل الحزم أدناه موجودة في سجلها وتُثبَّت بأمر واحد (`npm i <pkg>` أو `pip install <pkg>`).
Probed on 2026-10-16: every package below resolves in its registry. Install only what the job needs.

## مثبت الآن / installed now
- ffmpeg 6.1.1 (libass, fribidi, harfbuzz, xfade بـ58 انتقالًا, loudnorm, sidechaincompress, vidstab, rubberband, lut3d, tmix لضبابية الحركة)
- Chromium + Playwright عبر `kosif-tool/tools/render_html.cjs` · Node 22 · Python 3 · numpy · Pillow (RAQM يشكّل العربية)
- خطوط OFL عربية في `proofs/_shared/fonts`: Amiri, Cairo, Reem Kufi, Aref Ruqaa, Tajawal, Lalezar

## مُجرَّب هنا فعلًا / actually run here
- **Piper TTS عربي** (صوت `ar_JO-kareem-medium` من huggingface) ← صوت عربي بلا مفتاح ✅
- **faster-whisper small** بالعربية مع توقيت كل كلمة ✅ — مرّر مصفوفة numpy من `librosa.load(path, sr=16000)` لا مسار الملف. توقيته مبكر ~135 مللي ثانية؛ لمزامنة ≤100 مللي ثانية استخدم محاذاة Piper أو CTC.
- librosa · soundfile · pyloudnorm ✅ · render_html + verify_video ✅ (أفلام الإثبات 13/13)

## مكتبات JavaScript (npm)
| الحزمة | الإصدار والرخصة |
|---|---|
| `remotion` | {"version":"4.0.536","license":"SEELICENSEINLICENSE.md"} |
| `@remotion/cli` | {"version":"4.0.536","license":"SEELICENSEINLICENSE.md"} |
| `@remotion/renderer` | {"version":"4.0.536","license":"SEELICENSEINLICENSE.md"} |
| `@remotion/transitions` | {"version":"4.0.536","license":"UNLICENSED"} |
| `@remotion/captions` | {"version":"4.0.536","license":"MIT"} |
| `@remotion/three` | {"version":"4.0.536","license":"MIT"} |
| `@remotion/lottie` | {"version":"4.0.536","license":"SEELICENSEINLICENSE.md"} |
| `@remotion/media-utils` | {"version":"4.0.536","license":"MIT"} |
| `@remotion/paths` | {"version":"4.0.536","license":"MIT"} |
| `@remotion/shapes` | {"version":"4.0.536","license":"MIT"} |
| `@remotion/noise` | {"version":"4.0.536","license":"MIT"} |
| `@remotion/google-fonts` | {"version":"4.0.536","license":"SEELICENSEINLICENSE.md"} |
| `@remotion/layout-utils` | {"version":"4.0.536","license":"MIT"} |
| `@remotion/motion-blur` | {"version":"4.0.536","license":"MIT"} |
| `hyperframes` | {"version":"0.8.164","license":"Apache-2.0"} |
| `@hyperframes/cli` | {"error":{"code":"E404","summary":"NotFound-GEThttps://registry.npmjs.org/@hyperframes%2fcli-Notfound","detail":"'@hyperframes/cli@*'isnotinthisregistry.\n\nNotethatyoucanalsoinstallfroma\ntarball,folder,httpurl,orgiturl."}} |
| `gsap` | {"version":"3.15.0","license":"Standard'nocharge'license:https://gsap.com/standard-license."} |
| `three` | {"version":"0.186.1","license":"MIT"} |
| `@react-three/fiber` | {"version":"9.8.2","license":"MIT"} |
| `@react-three/drei` | {"version":"10.7.9","license":"MIT"} |
| `@react-three/postprocessing` | {"version":"3.2.0","license":"MIT"} |
| `postprocessing` | {"version":"6.39.5","license":"Zlib"} |
| `lottie-web` | {"version":"5.13.0","license":"MIT"} |
| `@lottiefiles/dotlottie-web` | {"version":"0.81.0","license":"MIT"} |
| `animejs` | {"version":"4.5.0","license":"MIT"} |
| `motion` | {"version":"14.3.0","license":"MIT"} |
| `framer-motion` | {"version":"14.3.0","license":"MIT"} |
| `@motion-canvas/core` | {"version":"3.17.2","license":"MIT"} |
| `@motion-canvas/2d` | {"version":"3.17.2","license":"MIT"} |
| `@theatre/core` | {"version":"0.7.2","license":"Apache-2.0"} |
| `@rive-app/canvas` | {"version":"2.44.2","license":"MIT"} |
| `@mojs/core` | {"version":"1.7.1","license":"MIT"} |
| `vivus` | {"version":"0.4.6","license":"MIT"} |
| `flubber` | {"version":"0.4.2","license":"MIT"} |
| `@svgdotjs/svg.js` | {"version":"3.2.8","license":"MIT"} |
| `roughjs` | {"version":"4.6.6","license":"MIT"} |
| `rough-notation` | {"version":"0.5.1","license":"MIT"} |
| `p5` | {"version":"2.3.4","license":"LGPL-2.1"} |
| `pixi.js` | {"version":"8.22.0","license":"MIT"} |
| `zdog` | {"version":"1.1.3","license":"MIT"} |
| `paper` | {"version":"0.12.18","license":"MIT"} |
| `matter-js` | {"version":"0.20.0","license":"MIT"} |
| `cannon-es` | {"version":"0.20.0","license":"MIT"} |
| `@dimforge/rapier3d-compat` | {"version":"0.21.0","license":"Apache-2.0"} |
| `d3` | {"version":"7.9.0","license":"ISC"} |
| `chart.js` | {"version":"4.5.1","license":"MIT"} |
| `echarts` | {"version":"6.1.0","license":"Apache-2.0"} |
| `vega` | {"version":"6.4.0","license":"BSD-3-Clause"} |
| `vega-lite` | {"version":"6.5.0","license":"BSD-3-Clause"} |
| `maplibre-gl` | {"version":"6.14.0","license":"BSD-3-Clause"} |
| `leaflet` | {"version":"1.9.4","license":"BSD-2-Clause"} |
| `@turf/turf` | {"version":"7.4.0","license":"MIT"} |
| `topojson-client` | {"version":"3.1.0","license":"ISC"} |
| `world-atlas` | {"version":"2.0.2","license":"ISC"} |
| `opentype.js` | {"version":"2.0.0","license":"MIT"} |
| `harfbuzzjs` | {"version":"1.6.3","license":"MIT"} |
| `fontkit` | {"version":"2.0.4","license":"MIT"} |
| `canvas-confetti` | {"version":"1.9.4","license":"ISC"} |
| `@tsparticles/engine` | {"version":"4.4.0","license":"MIT"} |
| `simplex-noise` | {"version":"4.0.3","license":"MIT"} |
| `culori` | {"version":"4.0.2","license":"MIT"} |
| `chroma-js` | {"version":"3.2.0","license":"(BSD-3-ClauseANDApache-2.0)"} |
| `tone` | {"version":"15.1.22","license":"MIT"} |
| `wavesurfer.js` | {"version":"8.0.2","license":"BSD-3-Clause"} |
| `meyda` | {"version":"5.6.3","license":"MIT"} |
| `@ffmpeg/ffmpeg` | {"version":"0.12.15","license":"MIT"} |
| `playwright` | {"version":"1.64.1","license":"Apache-2.0"} |
| `puppeteer` | {"version":"25.14.0","license":"Apache-2.0"} |
| `satori` | {"version":"0.62.0","license":"MPL-2.0"} |
| `@resvg/resvg-js` | {"version":"2.6.2","license":"MPL-2.0"} |
| `sharp` | {"version":"0.35.5","license":"Apache-2.0"} |
| `ogl` | {"version":"1.0.11","license":"Unlicense"} |
| `twgl.js` | {"version":"7.0.0","license":"MIT"} |
| `mermaid` | {"version":"12.2.0","license":"MIT"} |
| `@excalidraw/excalidraw` | {"version":"0.18.1","license":"MIT"} |
| `tldraw` | {"version":"5.5.2","license":"SEELICENSEINLICENSE.md"} |
| `lenis` | {"version":"1.3.27","license":"MIT"} |
| `@splinetool/runtime` | "2.0.88" |
| `typed.js` | {"version":"3.0.0","license":"GPL-3.0"} |
| `splitting` | {"version":"1.1.0","license":"MIT"} |
| `kokoro-js` | {"version":"1.2.1","license":"Apache-2.0"} |
| `@xenova/transformers` | {"version":"2.17.2","license":"Apache-2.0"} |
| `@huggingface/transformers` | {"version":"4.3.1","license":"Apache-2.0"} |
| `web-audio-beat-detector` | {"version":"8.2.39","license":"MIT"} |
| `music-metadata` | {"version":"12.2.1","license":"MIT"} |
| `svg-path-morph` | {"version":"1.0.5","license":"MIT"} |
| `polymorph-js` | {"version":"1.0.2","license":"MIT"} |
| `gl-transitions` | {"version":"1.76.0","license":"MIT"} |
| `ffmpeg-static` | {"version":"5.3.0","license":"GPL-3.0-or-later"} |

## مكتبات Python (pip)
| الحزمة | الإصدار |
|---|---|
| `moviepy` | moviepy (2.2.1) |
| `openai-whisper` | openai-whisper (20250625) |
| `faster-whisper` | faster-whisper (1.2.1) |
| `whisperx` | whisperx (3.8.6) |
| `stable-ts` | stable-ts (2.19.1) |
| `librosa` | librosa (1.0.0) |
| `aubio` | aubio (0.4.9) |
| `pydub` | pydub (0.25.1) |
| `soundfile` | soundfile (0.14.0) |
| `pyloudnorm` | pyloudnorm (0.2.0) |
| `noisereduce` | noisereduce (3.0.3) |
| `demucs` | demucs (4.1.0) |
| `scenedetect` | scenedetect (0.7.2) |
| `opencv-python-headless` | opencv-python-headless (5.0.0.93) |
| `mediapipe` | mediapipe (1.1.1) |
| `rembg` | rembg (2.0.85) |
| `manim` | manim (0.22.0) |
| `cairosvg` | cairosvg (2.9.1) |
| `skia-python` | skia-python (144.0.post2) |
| `pycairo` | pycairo (1.29.2) |
| `arabic-reshaper` | arabic-reshaper (3.0.1) |
| `python-bidi` | python-bidi (0.6.11) |
| `edge-tts` | edge-tts (7.3.1) |
| `gTTS` | gTTS (2.5.4) |
| `piper-tts` | piper-tts (1.8.0) |
| `kokoro` | kokoro (0.7.16) |
| `TTS` | NOTFOUND |
| `pyttsx3` | pyttsx3 (2.99) |
| `ffmpeg-python` | ffmpeg-python (0.2.0) |
| `imageio-ffmpeg` | imageio-ffmpeg (0.6.0) |
| `bpy` | bpy (5.2.2) |
| `trimesh` | trimesh (5.1.1) |
| `pyrender` | pyrender (0.1.45) |
| `svgpathtools` | svgpathtools (1.8.0) |
| `fonttools` | fonttools (4.67.0) |
| `uharfbuzz` | uharfbuzz (0.56.3) |
| `freetype-py` | freetype-py (2.5.1) |
| `colorthief` | colorthief (0.2.1) |
| `colour-science` | colour-science (0.4.7) |
| `ultralytics` | ultralytics (8.4.178) |
| `mutagen` | mutagen (1.48.1) |
| `basic-pitch` | basic-pitch (0.4.0) |
| `madmom` | madmom (0.16.1) |
| `pretty_midi` | pretty_midi (0.2.11.post0) |
| `mido` | mido (1.3.3) |
| `music21` | music21 (10.5.0) |
| `pedalboard` | pedalboard (0.9.26) |
| `auto-editor` | auto-editor (29.3.1) |
| `pysrt` | pysrt (1.1.2) |
| `webvtt-py` | webvtt-py (0.5.1) |
| `ass` | ass (1.0.3) |
| `playwright` | playwright (1.64.0) |
| `pymupdf` | pymupdf (1.28.2) |
| `qrcode` | qrcode (8.2) |
| `noise` | noise (1.2.2) |
| `opensimplex` | opensimplex (0.4.5.1) |
| `vtracer` | vtracer (0.6.15) |
| `potracer` | potracer (0.0.4) |
| `pyvips` | pyvips (3.2.0) |

## تنبيهات الرخص / license traps
- GSAP: رخصة Standard مجانية لكن ليست MIT. Remotion: رخصة شركة للفرق الكبيرة. p5: LGPL. typed.js و ffmpeg-static: GPL. satori/resvg: MPL. piper-tts: GPL-3 (وراجع رخصة الصوت). حزمة `TTS` (Coqui) غير موجودة في pip.

## الشبكة / hosts
- متاح: npm, pypi, huggingface (نماذج whisper/kokoro/piper), Google Fonts API, raw.githubusercontent.com/google/fonts, jsdelivr, unpkg, Wikimedia Commons, archive.org, بلاطات OSM وopenfreemap.
- محجوب هنا: pexels, pixabay, freesound, صور NASA, edge-tts. بمفاتيح: ElevenLabs, Veo, Kling, Runway. Higgsfield متاح كموصّل MCP عند ربطه (توليد صور/فيديو/صوت/3D، تحليل فيديو، توقع الانتشار).

## مكتبات متقدمة أوصى بها المالك / owner-recommended power-ups
| المكتبة | القوة التي تمنحها |
|---|---|
| matter-js · cannon-es · rapier | فيزياء: نصوص وأشكال تسقط وتتصادم (اخبز المحاكاة مسبقًا ليبقى seek(t) حتميًا) |
| popmotion · motion | نوابض وتلاشٍ وkeyframes عضوية |
| ogl · twgl.js · pixi.js | شيدرات GLSL خفيفة، تموجات، تشويه صور، آلاف العناصر على GPU |
| postprocessing · @react-three/postprocessing | Bloom، عمق ميدان، انحراف لوني |
| scenedetect (PySceneDetect) · opencv-python-headless | قص تلقائي على تغير اللقطات، تتبع حركة، كروما |
| lottie-web · @lottiefiles/dotlottie-web | تشغيل رسوم After Effects والتحكم بالإطار عبر الزمن |
| flubber · polymorph-js | تحوّل أشكال SVG بعدد نقاط مختلف |
| @motion-canvas/core · manim | شروحات هندسية ورياضية بتسلسل زمني |
| @theatre/core · bpy | إخراج كاميرا ثلاثي الأبعاد؛ Blender بلا واجهة (`blender -b -P script.py` أو `pip install bpy`) |
| editly · moviepy · ffmpeg-python | مونتاج برمجي من JSON/بايثون |
| pedalboard · pydub · demucs · noisereduce | هندسة صوت، دمج، فصل الصوت عن الموسيقى، إزالة ضوضاء |
| satori · sharp · rembg · pycairo · skia-python | صور مصغرة من HTML، معالجة صور، إزالة خلفية، رسم متجه |
| tone · meyda · web-audio-beat-detector | توليد وتحليل صوت في المتصفح |

## التوليفات الذهبية / golden stacks
| المشروع | التوليفة |
|---|---|
| إعلان تطبيق / SaaS | صفحة `seek(t)` + render_html (بلا تثبيت) أو Remotion + Tailwind + lucide + flubber، ثم ffmpeg |
| تايبوغرافي حركي | Canvas/HTML `seek(t)` + GSAP + render_html + `ffmpeg tmix` لضبابية الحركة |
| شرح بياني/مالي | D3 + Canvas seek(t) أو Manim / Motion Canvas + librosa للإيقاع |
| 3D سينمائي | Three.js + postprocessing (bloom) أو bpy headless |
| ريل بصوت عربي | صوت المستخدم أو Piper → faster-whisper → words.json → Canvas → loudnorm -14 LUFS → verify_video |
| مونتاج على الإيقاع | librosa beats → ffmpeg xfade / moviepy → loudnorm |

## Remotion بالعربية
- `import { loadFont } from '@remotion/google-fonts/Cairo'` ثم `loadFont('normal', {weights: ['400','700','900'], subsets: ['arabic']})` — ينتظر الخط قبل التقاط الإطارات.
- `dir="rtl"` على الحاويات، والتقسيم بالكلمات `split(' ')` لا بالحروف أبدًا؛ أو أقنعة `clip-path`.
- `spring({frame, fps, config: {damping: 14, stiffness: 120}})` و`interpolate(..., {extrapolateRight: 'clamp'})`.
- مشهد لكل ملف في `src/scenes/` يُجمع بـ`<Series>`؛ المعاينة `npx remotion studio`؛ الرندر `npx remotion render src/index.ts Comp out/video.mp4`.
