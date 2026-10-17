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

## 5. Rebuild after the container resets — إعادة البناء

```bash
cd kosif-tool
python3 -m venv .venv && .venv/bin/pip install faster-whisper librosa soundfile opencv-python-headless scenedetect pillow
python3 -m venv .venv-agents && .venv-agents/bin/pip install langgraph dspy pydantic-ai-slim
(cd starters/remotion && npm ci)
```

## 6. Needs your decision — يحتاج موافقتك

- **WhisperX + PyTorch + Arabic alignment model (~2 GB)**: worth it only for tighter (≤ 50 ms) forced alignment on sung Arabic.
- **API keys** (Anthropic/OpenAI…) for DSPy and Pydantic AI to call real models.
- **Remotion company license** if the user's company has more than 3 people.
- Nothing needed admin rights or system security changes. No personal files or existing programs were deleted or replaced.
