# الترسانة — كل مكتبة تقدر تنزّلها وتستخدمها / Libraries arsenal

فُحص فعليًا في هذه الحاوية يوم 2026-10-16: كل الحزم أدناه موجودة في سجلها وتُثبَّت بأمر واحد (`npm i <pkg>` أو `pip install <pkg>`) إلا ما عليه ❌.
Probed on 2026-10-16: every package below resolves in its registry except rows marked ❌. Versions and licenses were re-queried the same day (`npm view <pkg> version license --json`; PyPI JSON `license_expression` → `license` → classifiers), and the Python versions are what resolves on Python 3.13. Install only what the job needs. General (non-motion) libraries: `arsenal-general.md`; how to probe and verify: `self-discovery.md`.

## الفهرس / contents
1. مثبت الآن / installed now
2. مُجرَّب هنا فعلًا / actually run here
3. مكتبات JavaScript (npm)
4. مكتبات Python (pip)
5. تنبيهات الرخص / license traps
6. الشبكة / hosts
7. مكتبات متقدمة أوصى بها المالك / owner-recommended power-ups
8. التوليفات الذهبية / golden stacks
9. Remotion بالعربية

## مثبت الآن / installed now
لقطة 2026-10-16 لحاوية Claude Code على الويب؛ أعد تشغيل `python3 scripts/probe_env.py` في جلستك. — Snapshot of a Claude Code on the web container on 2026-10-16; re-run `python3 scripts/probe_env.py` in your session.
- ffmpeg 6.1.1 (libass, fribidi, harfbuzz, xfade بـ58 انتقالًا, loudnorm, sidechaincompress, vidstab, rubberband, lut3d, tmix لضبابية الحركة)
- Chromium + Playwright عبر `kosif-tool/tools/render_html.cjs` · Node 22 · Python 3 · numpy · Pillow (RAQM يشكّل العربية)
- خطوط OFL عربية في `proofs/_shared/fonts`: Amiri, Cairo, Reem Kufi, Aref Ruqaa, Tajawal, Lalezar

## مُجرَّب هنا فعلًا / actually run here
> هذه نتائج جلسات سابقة في بيئات venv، وليست مثبتة مسبقًا: في حاوية جديدة لم يكن `faster_whisper` ولا `librosa` قابلين للاستيراد (2026-10-16). ثبّت ثم تحقق قبل الادعاء. — These ran in earlier sessions' venvs and are not preinstalled; in a fresh container `faster_whisper` and `librosa` were not importable (2026-10-16). Install, then verify, before claiming.
- **Piper TTS عربي** (صوت `ar_JO-kareem-medium` من huggingface) ← صوت عربي بلا مفتاح ✅
- **faster-whisper small** بالعربية مع توقيت كل كلمة ✅ (جلسة سابقة 2026-10-16، غير مثبت الآن: `pip install faster-whisper`) — مرّر مصفوفة numpy من `librosa.load(path, sr=16000)` لا مسار الملف. توقيته مبكر ~135 مللي ثانية؛ لمزامنة ≤100 مللي ثانية استخدم محاذاة Piper أو CTC.
- librosa · soundfile · pyloudnorm ✅ (جلسة سابقة، غير مثبتة الآن: `pip install librosa soundfile pyloudnorm`) · render_html + verify_video ✅ (أفلام الإثبات 13/13)

## مكتبات JavaScript (npm)
| الحزمة / package | الإصدار / version | الرخصة / license |
|---|---|---|
| `remotion` | 4.0.536 | Remotion License (see LICENSE.md; paid company license for larger teams) |
| `@remotion/cli` | 4.0.536 | Remotion License (see LICENSE.md; paid company license for larger teams) |
| `@remotion/renderer` | 4.0.536 | Remotion License (see LICENSE.md; paid company license for larger teams) |
| `@remotion/transitions` | 4.0.536 | UNLICENSED in npm metadata (Remotion monorepo; treat as Remotion License) |
| `@remotion/captions` | 4.0.536 | MIT |
| `@remotion/three` | 4.0.536 | MIT |
| `@remotion/lottie` | 4.0.536 | Remotion License (see LICENSE.md; paid company license for larger teams) |
| `@remotion/media-utils` | 4.0.536 | MIT |
| `@remotion/paths` | 4.0.536 | MIT |
| `@remotion/shapes` | 4.0.536 | MIT |
| `@remotion/noise` | 4.0.536 | MIT |
| `@remotion/google-fonts` | 4.0.536 | Remotion License (see LICENSE.md; paid company license for larger teams) |
| `@remotion/layout-utils` | 4.0.536 | MIT |
| `@remotion/motion-blur` | 4.0.536 | MIT |
| `hyperframes` | 0.8.165 | Apache-2.0 |
| `@hyperframes/cli` | ❌ not in registry (E404) | — the HyperFrames CLI ships as the `hyperframes` bin of package `hyperframes` (`npx hyperframes`) |
| `gsap` | 3.15.0 | GSAP Standard "no charge" license (not OSI) |
| `three` | 0.186.1 | MIT |
| `@react-three/fiber` | 9.8.2 | MIT |
| `@react-three/drei` | 10.7.9 | MIT |
| `@react-three/postprocessing` | 3.2.0 | MIT |
| `postprocessing` | 6.39.5 | Zlib |
| `lottie-web` | 5.13.0 | MIT |
| `@lottiefiles/dotlottie-web` | 0.81.0 | MIT |
| `animejs` | 4.5.0 | MIT |
| `motion` | 14.3.0 | MIT |
| `framer-motion` | 14.3.0 | MIT |
| `@motion-canvas/core` | 3.17.2 | MIT |
| `@motion-canvas/2d` | 3.17.2 | MIT |
| `@theatre/core` | 0.7.2 | Apache-2.0 |
| `@rive-app/canvas` | 2.44.2 | MIT |
| `@mojs/core` | 1.7.1 | MIT |
| `vivus` | 0.4.6 | MIT |
| `flubber` | 0.4.2 | MIT |
| `@svgdotjs/svg.js` | 3.2.8 | MIT |
| `roughjs` | 4.6.6 | MIT |
| `rough-notation` | 0.5.1 | MIT |
| `p5` | 2.3.4 | LGPL-2.1 |
| `pixi.js` | 8.22.0 | MIT |
| `zdog` | 1.1.3 | MIT |
| `paper` | 0.12.18 | MIT |
| `matter-js` | 0.20.0 | MIT |
| `cannon-es` | 0.20.0 | MIT |
| `@dimforge/rapier3d-compat` | 0.21.0 | Apache-2.0 |
| `d3` | 7.9.0 | ISC |
| `chart.js` | 4.5.1 | MIT |
| `echarts` | 6.1.0 | Apache-2.0 |
| `vega` | 6.4.0 | BSD-3-Clause |
| `vega-lite` | 6.5.0 | BSD-3-Clause |
| `maplibre-gl` | 6.14.0 | BSD-3-Clause |
| `leaflet` | 1.9.4 | BSD-2-Clause |
| `@turf/turf` | 7.4.0 | MIT |
| `topojson-client` | 3.1.0 | ISC |
| `world-atlas` | 2.0.2 | ISC |
| `opentype.js` | 2.0.0 | MIT |
| `harfbuzzjs` | 1.6.3 | MIT |
| `fontkit` | 2.0.4 | MIT |
| `canvas-confetti` | 1.9.4 | ISC |
| `@tsparticles/engine` | 4.4.0 | MIT |
| `simplex-noise` | 4.0.3 | MIT |
| `culori` | 4.0.2 | MIT |
| `chroma-js` | 3.2.0 | BSD-3-Clause AND Apache-2.0 |
| `tone` | 15.1.22 | MIT |
| `wavesurfer.js` | 8.0.2 | BSD-3-Clause |
| `meyda` | 5.6.3 | MIT |
| `@ffmpeg/ffmpeg` | 0.12.15 | MIT |
| `playwright` | 1.64.1 | Apache-2.0 |
| `puppeteer` | 25.14.0 | Apache-2.0 |
| `satori` | 0.62.0 | MPL-2.0 |
| `@resvg/resvg-js` | 2.6.2 | MPL-2.0 |
| `sharp` | 0.35.5 | Apache-2.0 |
| `ogl` | 1.0.11 | Unlicense |
| `twgl.js` | 7.0.0 | MIT |
| `mermaid` | 12.2.0 | MIT |
| `@excalidraw/excalidraw` | 0.18.1 | MIT |
| `tldraw` | 5.5.2 | tldraw license, SEE LICENSE IN LICENSE.md (not OSI) |
| `lenis` | 1.3.27 | MIT |
| `@splinetool/runtime` | 2.0.91 | none in npm metadata (check spline.design terms) |
| `typed.js` | 3.0.0 | GPL-3.0 |
| `splitting` | 1.1.0 | MIT |
| `kokoro-js` | 1.2.1 | Apache-2.0 |
| `@xenova/transformers` | 2.17.2 | Apache-2.0 |
| `@huggingface/transformers` | 4.3.1 | Apache-2.0 |
| `web-audio-beat-detector` | 8.2.39 | MIT |
| `music-metadata` | 12.2.1 | MIT |
| `svg-path-morph` | 1.0.5 | MIT |
| `polymorph-js` | 1.0.2 | MIT |
| `gl-transitions` | 1.76.0 | MIT |
| `ffmpeg-static` | 5.3.0 | GPL-3.0-or-later |

## مكتبات Python (pip)
| الحزمة / package | الإصدار / version | الرخصة / license |
|---|---|---|
| `moviepy` | 2.2.1 | MIT |
| `openai-whisper` | 20250625 | MIT |
| `faster-whisper` | 1.2.1 | MIT |
| `whisperx` | 3.8.6 | BSD-2-Clause |
| `stable-ts` | 2.19.1 | MIT |
| `librosa` | 1.0.0 | ISC |
| `aubio` | 0.4.9 | GPL-3.0-or-later |
| `pydub` | 0.25.1 | MIT |
| `soundfile` | 0.14.0 | BSD-3-Clause |
| `pyloudnorm` | 0.2.0 | MIT |
| `noisereduce` | 3.0.3 | MIT (classifier says BSD) |
| `demucs` | 4.1.0 | MIT |
| `scenedetect` | 0.7.2 | BSD-3-Clause |
| `opencv-python-headless` | 5.0.0.93 | Apache-2.0 |
| `mediapipe` | 1.1.1 | Apache-2.0 |
| `rembg` | 2.0.85 | MIT |
| `manim` | 0.22.0 | MIT |
| `cairosvg` | 2.9.1 | LGPL-3.0-or-later |
| `skia-python` | 144.0.post2 | BSD (classifier) |
| `pycairo` | 1.29.2 | LGPL-2.1-only OR MPL-1.1 |
| `arabic-reshaper` | 3.0.1 | MIT |
| `python-bidi` | 0.6.11 | LGPL (classifier) |
| `edge-tts` | 7.3.1 | LGPL-3.0 (classifier) |
| `gTTS` | 2.5.4 | MIT |
| `piper-tts` | 1.8.0 | GPL-3.0-or-later (check each voice's own license) |
| `kokoro` | 0.7.16 on Python 3.13 (latest 0.9.4 needs Python <3.13) | Apache-2.0 (repo LICENSE; PyPI field blank) |
| `TTS` | ❌ 0.22.0 needs Python <3.12, so nothing installs on 3.13; use fork `coqui-tts` 0.27.5 (MPL-2.0) | MPL-2.0 |
| `pyttsx3` | 2.99 | MPL-2.0 |
| `ffmpeg-python` | 0.2.0 | Apache-2.0 |
| `imageio-ffmpeg` | 0.6.0 | BSD-2-Clause |
| `bpy` | 5.2.2 | GPL-3.0 |
| `trimesh` | 5.1.1 | MIT |
| `pyrender` | 0.1.45 | MIT |
| `svgpathtools` | 1.8.0 | MIT |
| `fonttools` | 4.67.0 | MIT |
| `uharfbuzz` | 0.56.3 | Apache-2.0 |
| `freetype-py` | 2.5.1 | BSD (classifier) |
| `colorthief` | 0.2.1 | BSD |
| `colour-science` | 0.4.7 | BSD-3-Clause |
| `ultralytics` | 8.4.178 | AGPL-3.0 |
| `mutagen` | 1.48.1 | GPL-2.0-or-later |
| `basic-pitch` | 0.4.0 | Apache-2.0 (repo LICENSE; PyPI field blank) |
| `madmom` | 0.16.1 | BSD code; model files CC BY-NC-SA (non-commercial) |
| `pretty_midi` | 0.2.11.post0 | MIT |
| `mido` | 1.3.3 | MIT |
| `music21` | 10.5.0 | BSD-3-Clause |
| `pedalboard` | 0.9.26 | GPL-3.0 |
| `auto-editor` | 29.3.1 | Unlicense |
| `pysrt` | 1.1.2 | GPL-3.0 |
| `webvtt-py` | 0.5.1 | MIT |
| `ass` | 1.0.3 | MIT |
| `playwright` | 1.64.0 | Apache-2.0 |
| `pymupdf` | 1.28.2 | AGPL-3.0 or Artifex commercial (COPYING checked) |
| `qrcode` | 8.2 | BSD |
| `noise` | 1.2.2 | MIT (classifier) |
| `opensimplex` | 0.4.5.1 | MIT |
| `vtracer` | 0.6.15 | MIT |
| `potracer` | 0.0.4 | GPL-2.0-or-later |
| `pyvips` | 3.2.0 | MIT |

## تنبيهات الرخص / license traps
- GSAP: رخصة Standard مجانية لكن ليست MIT. Remotion: رخصة شركة للفرق الكبيرة. p5: LGPL. typed.js و ffmpeg-static: GPL. satori/resvg: MPL. piper-tts: GPL-3 (وراجع رخصة الصوت). حزمة `TTS` (Coqui) موجودة في PyPI لكنها لا تُثبَّت على Python 3.13 (تتطلب أقل من 3.12)؛ استخدم الفرع `coqui-tts` (MPL-2.0).
- AGPL: `ultralytics`، و`pymupdf` (أو رخصة تجارية). GPL: `aubio`، و`pysrt`، و`mutagen` (GPL-2.0+)، و`potracer` (GPL-2.0+)، و`pedalboard`، و`bpy`. LGPL: `edge-tts`، و`python-bidi`، و`cairosvg`؛ و`pycairo` (LGPL-2.1 أو MPL-1.1). `madmom`: الكود BSD لكن ملفات النماذج CC BY-NC-SA غير تجارية. — AGPL/GPL/LGPL and non-commercial model files found in the 2026-10-16 license re-query.
- `@remotion/transitions` موسومة UNLICENSED في npm، و`@splinetool/runtime` بلا حقل رخصة، و`tldraw` برخصة خاصة: راجعها قبل التوزيع. — Check these before redistributing. `@hyperframes/cli` غير موجودة في السجل (E404)؛ الأداة هي `npx hyperframes`.

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
