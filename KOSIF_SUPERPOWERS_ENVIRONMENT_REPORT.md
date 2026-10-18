# KOSIF Superpowers — Environment Report / تقرير جاهزية البيئة

Date: 2026-10-17 · Session: Claude Code cloud container (ephemeral; every install below is lost when the container is reclaimed, so this report also tells you how to rebuild it).

## 1. Machine — الجهاز

| Item | Value |
|---|---|
| OS | Ubuntu 24.04.5 LTS, kernel 6.18.44 x86_64 |
| CPU | 4 vCPU, Intel Xeon @ 2.10 GHz |
| RAM | 15.7 GiB |
| Free disk | ~30 GiB at the start (session allowance) |
| GPU | none (no `nvidia-smi`) → every model runs on CPU |
| Network | full, through the agent proxy (TLS verification kept on) |
| Probe | `python3 .claude/skills/kosif-superpowers/scripts/probe_env.py` |

## 2. Tools — الأدوات

| Tool | Purpose | Was installed? | Installed now? | Version / source | Test result | Path KOSIF uses | License / notes |
|---|---|---|---|---|---|---|---|
| Python | scripts, catalog, analysis | yes | no | 3.13.16 (system) | `npm test` → 67/67 unittest OK | `/usr/bin/python3` | PSF |
| Node.js + npm | renderer, Remotion, site tests | yes | no | node 22.22.0, npm 10.9.4 | node --test 5/5 OK | `/opt/node22/bin/node` | MIT |
| Git | repository | yes | no | 2.43.0 | used in this session | `/usr/bin/git` | GPL-2.0 |
| FFmpeg / FFprobe | audio extraction, encoding, verification | yes | no | 6.1.1 (Ubuntu) | audio extracted, EBU R128 measured, final mux and probe | `/usr/bin/ffmpeg`, `/usr/bin/ffprobe` | LGPL/GPL build |
| Playwright + Chromium | HTML → frame-by-frame render | yes | no | playwright 1.56.1, chromium-1194 | rendered all 1,381 frames of the film | `/opt/node-tools/node_modules/playwright`, `/opt/pw-browsers` | Apache-2.0 / BSD |
| ImageMagick | contact sheets | yes | no | 6.9.12 | used to make preview sheets | `/usr/bin/convert` | ImageMagick license |
| Python venv (media) | isolated media libraries | no | **yes** | `python3 -m venv` | imports OK | `/home/user/kosif-tool/.venv` (1.2 GB, git-ignored) | — |
| faster-whisper | Arabic speech/song transcription with word timestamps | no | **yes** | 1.2.1 (PyPI) + CTranslate2 4.8.3 | transcribed the 46 s song: 43 words with timestamps | `.venv` | MIT. Model `small` (~480 MB) downloaded from Hugging Face. **Known bug:** with PyAV 19 the file-path input fails (`metadata_errors`); pass a numpy array read with soundfile instead (done here) |
| librosa | RMS envelope, onsets, tempo | no | **yes** | 1.0.0 (PyPI) | envelope at 30 fps drives the glow and the camera | `.venv` | ISC |
| soundfile | WAV reading | no | **yes** | 0.14.0 | OK | `.venv` | BSD-3 |
| OpenCV (headless) | frame reading and analysis | no | **yes** | 5.0.0 (PyPI) | read a frame (1024×576×3) | `.venv` | Apache-2.0 |
| PySceneDetect | cut detection | no | **yes** | 0.7.2 (PyPI) | found the cut at 41.97 s (TikTok end card) | `.venv` | BSD-3 |
| Pillow | images | no (venv) | **yes** | 13.0.0 | OK | `.venv` | MIT-CMU |
| Remotion (starter) | React video engine | no | **yes** | remotion / @remotion/cli 4.0.535 via `npm ci` (lockfile) | `tsc --noEmit` OK; `remotion still` rendered `starters/remotion/out/still.png` | `starters/remotion/node_modules` | **Remotion license:** free for individuals and companies of up to 3 people; larger companies need a company license |
| Python venv (agents) | agent frameworks, kept apart from media | no | **yes** | `python3 -m venv` | — | `/home/user/kosif-tool/.venv-agents` (401 MB) | — |
| LangGraph | agent graphs | no | **yes** | 1.2.16 | compiled and ran a 1-node graph (41→42) | `.venv-agents` | MIT |
| DSPy | declarative prompting | no | **yes** | 3.4.1 | built a `question -> answer` signature (no LLM call: that needs an API key) | `.venv-agents` | MIT |
| Pydantic AI | typed agents | no | **yes** | pydantic-ai-slim 2.57.0 | ran an agent on the offline `TestModel` | `.venv-agents` | MIT. Real models need provider keys 🔑 |
| WhisperX | forced word alignment | no | **no, awaiting your approval** | — | — | — | BSD-2. Pulls PyTorch (~700 MB CPU) and an Arabic wav2vec2 alignment model (~1.2 GB). That is a large model download, so per your rule I did not install it. faster-whisper word timestamps, checked against the burned-in lyrics, were enough for this film |
| Tesseract OCR, Blender, TeX | other powers | no | no | `apt-get` available | — | — | Not needed for this task; one command each (see probe) |

## 3. Original KOSIF tests — الاختبارات الأصلية

| Command | Result |
|---|---|
| `npm test` (node --test + python unittest) | 5/5 + 67/67 passed |
| `python3 tools/validate.py` | 14/14 checks passed |
| `python3 .claude/skills/kosif-superpowers/scripts/check_skill.py --evals` | structure OK; routing evals 37/37 (100%) |
| `starters/remotion`: `npm run typecheck`, `remotion still` | passed / still rendered |

## 4. Practical capability test — the film «عن فرحة»

Source: the uploaded concert clip (576×1024, 30 fps, 46.02 s, AAC 44.1 kHz stereo, −15.5 LUFS).
Pipeline: ffmpeg audio extract → faster-whisper `small` (prompted with the lyrics read from the video frames; an unprompted run agreed on the phrase boundaries) → librosa envelope → original canvas film (`out/farha/film.js`) → `tools/render_html.cjs` (1,381 frames) → mux with the **original AAC stream copied untouched** (`-c:a copy`) → ffprobe verification. Results are in `out/farha/TEST_REPORT.md`.

## 5. Full catalog install (round 2, approved by the user: "install every library the skill needs")

Source of the list: every `pip`/`npm`/`apt` command named in `.claude/skills/kosif-superpowers/data/powers/*.json` (220 distinct commands across 4,223 powers). The skill's own scripts need only the Python standard library.

### 5.1 Isolation layout

| Environment | Python | Contents | Size |
|---|---|---|---|
| `.venv` | 3.13 | media, data, documents, OCR, charts, ML-light, optimisation, geo | 3.6 GB |
| `.venv-agents` | 3.13 | agent frameworks, API SDKs, MCP, Graphify | 1.4 GB |
| `.venv-ml` | 3.13 | PyTorch **CPU** 2.8.0 + WhisperX, Demucs, EasyOCR, transformers, diffusers, docling, camel-tools, Piper, Blender `bpy` | 3.4 GB |
| `.venv-tts` | **3.12** (uv-managed) | Kokoro TTS (pins numpy 1.26.4, which has no Python 3.13 wheel) | 1.3 GB |
| `.kosif-node` | Node 22 | 50 JS packages, 811 modules incl. deps | 2.9 GB |
| apt (system) | — | tesseract-ocr + ara, ocrmypdf, fonts-noto-core/kacst/arabeyes, exiftool, poppler-utils, graphviz, sox, default-jre, texlive-xetex + lang-arabic, blender, libpango/libcairo dev | — |

The new environments are excluded locally via `.git/info/exclude`; nothing heavy is committed.

### 5.2 Python packages — 96/96 import

| Package | Version | Import | Env |
|---|---|---|---|
| altair | 6.3.0 | ✅ | `.venv` |
| arabic-reshaper | 3.0.1 | ✅ | `.venv` |
| beautifulsoup4 | 4.15.0 | ✅ | `.venv` |
| cairosvg | 2.9.1 | ✅ | `.venv` |
| curl_cffi | 0.16.3 | ✅ | `.venv` |
| cvxpy | 1.9.3 | ✅ | `.venv` |
| duckdb | 1.5.6 | ✅ | `.venv` |
| edge-tts | 7.3.1 | ✅ | `.venv` |
| emoji | 2.16.0 | ✅ | `.venv` |
| Faker | 40.43.0 | ✅ | `.venv` |
| farasapy | 0.1.1 | ✅ | `.venv` |
| faster-whisper | 1.2.1 | ✅ | `.venv` |
| feedparser | 6.0.14 | ✅ | `.venv` |
| geopandas | 1.2.0 | ✅ | `.venv` |
| httpx | 0.28.1 | ✅ | `.venv` |
| Jinja2 | 3.1.6 | ✅ | `.venv` |
| librosa | 1.0.0 | ✅ | `.venv` |
| lightgbm | 4.7.0 | ✅ | `.venv` |
| lxml | 6.1.3 | ✅ | `.venv` |
| manim | 0.22.0 | ✅ | `.venv` |
| markitdown | 0.1.8 | ✅ | `.venv` |
| matplotlib | 3.11.2 | ✅ | `.venv` |
| networkx | 3.7 | ✅ | `.venv` |
| numpy | 2.5.4 | ✅ | `.venv` |
| ocrmypdf | 17.13.0 | ✅ | `.venv` |
| onnxruntime | 1.31.0 | ✅ | `.venv` |
| opencv-python-headless | 5.0.0.93 | ✅ | `.venv` |
| openpyxl | 3.1.5 | ✅ | `.venv` |
| ortools | 9.15.6755 | ✅ | `.venv` |
| pandas | 3.0.6 | ✅ | `.venv` |
| pdfplumber | 0.11.10 | ✅ | `.venv` |
| pedalboard | 0.9.26 | ✅ | `.venv` |
| pillow | 12.3.0 | ✅ | `.venv` |
| pillow-heif | 1.8.1 | ✅ | `.venv` |
| plotly | 7.1.0 | ✅ | `.venv` |
| polars | 2.0.0 | ✅ | `.venv` |
| prophet | 1.5.0 | ✅ | `.venv` |
| PuLP | 4.0.1 | ✅ | `.venv` |
| pyarabic | 0.6.15 | ✅ | `.venv` |
| pyarrow | 26.0.0 | ✅ | `.venv` |
| pydub | 0.25.1 | ✅ | `.venv` |
| pyloudnorm | 0.2.0 | ✅ | `.venv` |
| pymupdf | 1.28.2 | ✅ | `.venv` |
| pypdf | 6.21.1 | ✅ | `.venv` |
| pypdfium2 | 5.14.0 | ✅ | `.venv` |
| pyproj | 3.8.0 | ✅ | `.venv` |
| pytesseract | 0.3.13 | ✅ | `.venv` |
| python-barcode | 0.16.1 | ✅ | `.venv` |
| python-bidi | 0.6.11 | ✅ | `.venv` |
| python-docx | 1.2.0 | ✅ | `.venv` |
| python-pptx | 1.0.2 | ✅ | `.venv` |
| qrcode | 8.2 | ✅ | `.venv` |
| quantstats | 0.0.86 | ✅ | `.venv` |
| rembg | 2.0.85 | ✅ | `.venv` |
| reportlab | 5.0.1 | ✅ | `.venv` |
| scenedetect | 0.7.2 | ✅ | `.venv` |
| scikit-image | 0.26.0 | ✅ | `.venv` |
| scikit-learn | 1.9.1 | ✅ | `.venv` |
| scipy | 1.18.1 | ✅ | `.venv` |
| seaborn | 0.13.2 | ✅ | `.venv` |
| shapely | 2.2.0 | ✅ | `.venv` |
| soundfile | 0.14.0 | ✅ | `.venv` |
| statsmodels | 0.15.0 | ✅ | `.venv` |
| sympy | 1.14.0 | ✅ | `.venv` |
| trafilatura | 2.3.1 | ✅ | `.venv` |
| vtracer | 0.6.15 | ✅ | `.venv` |
| weasyprint | 70.0 | ✅ | `.venv` |
| xgboost | 3.4.1 | ✅ | `.venv` |
| yfinance | 1.7.0 | ✅ | `.venv` |
| yt-dlp | 2026.8.19 | ✅ | `.venv` |
| z3-solver | 5.3.1.0 | ✅ | `.venv` |
| anthropic | 1.15.0 | ✅ | `.venv-agents` |
| dspy | 3.4.1 | ✅ | `.venv-agents` |
| fal-client | 1.0.3 | ✅ | `.venv-agents` |
| fastapi | 0.143.3 | ✅ | `.venv-agents` |
| google-genai | 2.31.0 | ✅ | `.venv-agents` |
| graphifyy | 0.9.91 | ✅ | `.venv-agents` |
| higgsfield-client | 0.2.0 | ✅ | `.venv-agents` |
| langgraph | 1.2.16 | ✅ | `.venv-agents` |
| mcp | 2.3.0 | ✅ | `.venv-agents` |
| pydantic-ai-slim | 2.57.0 | ✅ | `.venv-agents` |
| python-dotenv | 1.2.4 | ✅ | `.venv-agents` |
| streamlit | 1.66.0 | ✅ | `.venv-agents` |
| together | 2.41.0 | ✅ | `.venv-agents` |
| accelerate | 1.15.0 | ✅ | `.venv-ml` |
| bpy | 5.2.2 | ✅ | `.venv-ml` |
| camel-tools | 1.6.0 | ✅ | `.venv-ml` |
| demucs | 4.1.0 | ✅ | `.venv-ml` |
| diffusers | 0.35.2 | ✅ | `.venv-ml` |
| docling | 2.140.0 | ✅ | `.venv-ml` |
| easyocr | 1.7.2 | ✅ | `.venv-ml` |
| piper-tts | 1.8.0 | ✅ | `.venv-ml` |
| torch | 2.8.0+cpu | ✅ | `.venv-ml` |
| torchaudio | 2.8.0+cpu | ✅ | `.venv-ml` |
| transformers | 4.57.6 | ✅ | `.venv-ml` |
| whisperx | 3.8.6 | ✅ | `.venv-ml` |

### 5.3 Functional tests (real runs, not only imports)

| Capability | Test | Result |
|---|---|---|
| pyloudnorm | integrated loudness of the song | −15.51 LUFS (matches ffmpeg ebur128 −15.5) ✅ |
| pedalboard | compressor + reverb on 2 s | ✅ |
| matplotlib + arabic-reshaper + python-bidi | Arabic-titled plot with Amiri | ✅ |
| duckdb + pandas + polars | SQL over words.json | 43 words, mean 0.894 s ✅ |
| pymupdf + pdfplumber, python-docx + markitdown, weasyprint (RTL) | create → read back | ✅ |
| cairosvg + vtracer | SVG → PNG → SVG | ✅ |
| scikit-learn + xgboost, ortools + z3, geopandas + pyproj, sympy, networkx | small solves | ✅ |
| qrcode + OpenCV | encode → decode repo URL | ✅ |
| tesseract ara | on stylised burned-in captions | weak (expected); EasyOCR is better here |
| **EasyOCR (ar)** | lyric frame at 24 s | read «وانت بعينيك دول حاضنى» ✅ |
| **Demucs htdemucs** | 12 s of the song → vocals / music | 15 s on CPU; vocals −18.5 LUFS, music −25.3 LUFS ✅ (`out/farha/test_demucs_vocals.wav`) |
| **WhisperX** | transcription with `small` | ✅ (word alignment model not downloaded, see 6) |
| **Piper TTS** | Arabic voice ar_JO-kareem-medium (63 MB) | 2.98 s WAV ✅ (`out/farha/test_piper_ar.wav`) |
| bpy (Blender 5.2.2 LTS) + apt Blender 4.0.2 | create a cube | ✅ |
| camel-tools | ar2bw transliteration | «w>xyrA Al>yAm» ✅ |
| Kokoro | import in `.venv-tts` | ✅ (model not downloaded; Kokoro has no Arabic voice) |
| LangGraph, Pydantic AI (TestModel), DSPy | offline runs | ✅ |
| Browser bundle (esbuild → Chromium) | three.js WebGL, GSAP, roughjs, d3, ECharts, KaTeX, matter-js, perfect-freehand, flubber, lottie, motion, anime.js, turf, **Excalidraw mounted** | 15/15, no page errors ✅ |
| Node import | 44 packages | 42 OK; hyperframes is CLI-only (v0.8.164 runs), Excalidraw is bundler-only (passes in browser) |
| CLIs | mermaid-cli (with Playwright Chromium), odiff, serve 14.2.6, esbuild 0.28.2, Remotion 4.0.536 | ✅ |

### 5.4 Problems found and fixed

| Problem | Cause | Fix |
|---|---|---|
| Bulk install blocked once | permission classifier (untrusted code) | user explicitly approved round 2 |
| `manim` build failed | missing Pango headers | apt `libpango1.0-dev libcairo2-dev pkg-config`, reinstalled → 0.22.0 |
| apt `ocrmypdf` crashed | system `/usr/bin/python3` is 3.13; Ubuntu's python3-pikepdf is built for 3.12 | installed ocrmypdf 17.13.0 in `.venv` |
| `.venv-ml` grew to 7.4 GB, disk fell to 2 GB | WhisperX pinned torch 2.8.0 from PyPI = CUDA build (4.1 GB of nvidia libs, no GPU here) | removed nvidia/triton, reinstalled torch/torchaudio/torchvision 2.8.0+cpu, pinned with `requirements/constraints-cpu.txt`; cleared 5.3 GB pip cache |
| npm ECONNRESET | transient proxy reset | retried with fetch retries, succeeded |
| diffusers import error | camel-tools pins transformers<5 → huggingface_hub 0.36; diffusers 0.41 needs hub ≥1.32 | diffusers 0.35.2 (compatible) |
| Kokoro failed | pins numpy 1.26.4 (no 3.13 wheel) | separate Python 3.12 env `.venv-tts` via uv |
| `pip check`: whisperx requires triton | triton is GPU-only | intentionally not installed (CPU machine) |

## 6. Rebuild after the container resets — إعادة البناء

```bash
cd kosif-tool
apt-get install -y tesseract-ocr tesseract-ocr-ara fonts-noto-core fonts-kacst fonts-arabeyes libimage-exiftool-perl poppler-utils graphviz sox default-jre texlive-xetex texlive-lang-arabic blender libpango1.0-dev libcairo2-dev pkg-config
python3 -m venv .venv && .venv/bin/pip install -r requirements/media.txt
python3 -m venv .venv-agents && .venv-agents/bin/pip install -r requirements/agents.txt
python3 -m venv .venv-ml && .venv-ml/bin/pip install torch==2.8.0 torchaudio==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cpu
.venv-ml/bin/pip install -c requirements/constraints-cpu.txt --extra-index-url https://download.pytorch.org/whl/cpu -r requirements/ml.txt
uv venv --python 3.12 .venv-tts && uv pip install --python .venv-tts/bin/python --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cpu "torch==2.8.0+cpu" kokoro soundfile
(cd starters/remotion && npm ci)
mkdir -p .kosif-node && cd .kosif-node && echo '{"name":"kosif-node-tools","private":true}' > package.json && PUPPETEER_SKIP_DOWNLOAD=1 npm i $(cat ../requirements/node.txt)
```
The lists live in `requirements/` (media, agents, ml, node, constraints-cpu).

## 7. Still needs your decision — يحتاج موافقتك

- **Large models (not downloaded):** WhisperX Arabic alignment model (~1.2 GB), Stable Diffusion weights for diffusers (2–7 GB), docling layout models, camel-tools data packages, Kokoro weights (330 MB, no Arabic).
- **API keys** for anthropic, together, fal, google-genai, higgsfield, DSPy and Pydantic AI providers.
- **Licences:** Remotion company licence (>3 people); HyperFrames, GSAP and Kokoro/Piper voice licences before commercial use.
- Disk: about 14 GB free left of the session allowance.
- No personal files or existing programs were deleted or replaced.
