# لقطة البيئة — Environment snapshot

What this gives you: a dated capability card of the machine where the skill was last probed — runtimes, CLI tools, packages, fonts, network reach, and which power families each finding unlocks. Open it when planning what you can build, but trust it only for that machine and date: run `python3 scripts/probe_env.py` (or `python3 scripts/powers.py env`) in your own session first.

> Snapshot taken 2026-10-16 on a **Claude Code cloud session** by `scripts/probe_env.py`. Facts change per machine and per session — re-run to refresh; never quote these versions as timeless truth.

## الفهرس / contents

- Capability card — بطاقة القدرات
  - Domains — المجالات
  - Top unlocks → powers — ماذا يفتح كل اكتشاف
  - One-line fixes — إصلاحات بسطر واحد
  - Network — الشبكة
  - Machine & runtimes — الجهاز والبيئات
  - Python & Node packages — الحزم
  - Fonts & browsers — الخطوط والمتصفحات
  - Credentials & connectors — المفاتيح والموصلات
  - Host evidence — دليل نوع المضيف

## Capability card — بطاقة القدرات

**Claude Code cloud session** · Ubuntu 24.04.5 LTS · 4 CPU · 15.7 GiB RAM · 22.3 GiB free disk · GPU: none · network: **full** · python 3.13.16 · node 22.22.0 · probe 1.7 s

Legend: 🟢 present now (answered a version or import check) · 📦 one install command away (manager present and its registry reachable) · 🔑 needs a key, account or connector · ❌ not available here · ❔ unknown. The probe proves presence, not quality: ✅ stays reserved for powers with a real run and a proof path.

### Domains — المجالات

| Domain | State | Present here | Fix if missing | Power families |
|---|---|---|---|---|
| Video / فيديو | 🟢 | ffmpeg 6.1.1, ffprobe | — | ENG TRANS SYNC FOOT QA FMT |
| Image / صور | 🟢 | convert 6.9.12, py:pillow | — | MEDIA TEX |
| Audio / صوت | 🟢 | ffmpeg | — | BEAT VOICE MEDIA |
| Speech-to-text / تفريغ | 📦 | — | `python3 -m pip install faster-whisper` | SYNC VOICE MEDIA |
| OCR | 🟢 | tesseract 5.3.4 | — | MEDIA DOC |
| Docs & PDF / مستندات | 🟢 | soffice 24.2.7.2, pandoc 3.1.3, pdftotext, py:python-docx, py:openpyxl, py:python-pptx | — | DOC |
| LaTeX / معادلات | 📦 | — | `apt-get update -qq && apt-get install -y texlive-xetex texlive-lang-arabic` | DOC EXPL |
| Browser / متصفح | 🟢 | playwright: chromium, chromium-1194, chromium_headless_shell-1194 | — | APP WEB QA ENG UI |
| Data / بيانات | 🟢 | py:pandas, py:numpy, jq 1.7, psql 16.15, py:sqlite3 | — | ANLY DATA |
| Charts / رسوم | 📦 | — | `python3 -m pip install matplotlib plotly` | ANLY DATA |
| Diagrams / مخططات | 📦 | — | `apt-get update -qq && apt-get install -y graphviz` | GRAPH EXPL |
| Local AI / ذكاء محلي | 🟢 | py:onnxruntime | — | GEN MEDIA |
| Arabic text / نص عربي | 🟢 | skill fonts: 15 files | — | ARAB ARL TYPE |
| 3D | 📦 | — | `apt-get update -qq && apt-get install -y blender` | 3D |
| Dev & build / تطوير | 🟢 | git 2.43.0, gcc 13.3.0, node 22.22.0, go 1.24.7, rustc 1.97.0, java 21.0.12.1 | — | CODE CHECK |
| Repos & cloud / سحابة | 🟢 | gh 2.89.0, gcloud | — | CODE APP AGENT |

### Top unlocks → powers — ماذا يفتح كل اكتشاف

- 🟢 **ffmpeg 6.1.1** → cut, concat, transcode, loudnorm −14 LUFS, burn captions (libass), frames/audio extract, xfade, probe for QA → `ENG TRANS SYNC BEAT FOOT QA FMT MEDIA`
- 🟢 **headless Chromium (Playwright)** → render HTML/CSS/Canvas/WebGL scenes to frames and MP4, screenshots, HTML→PDF, page checks → `ENG UI EXPL QA APP WEB DOC`
- 🟢 **soffice 24.2.7.2 + pandoc 3.1.3** → convert docx/xlsx/pptx/md/html ↔ PDF headless → `DOC`
- 🟢 **python: python-docx, openpyxl, python-pptx, reportlab, pypdf** → generate and edit Word/Excel/PowerPoint/PDF files from code → `DOC`
- 🟢 **python: pandas, numpy** → load, clean, join, aggregate and test data; sqlite3 is built in → `ANLY DATA`
- 🟢 **tesseract 5.3.4** → OCR of scans and video frames → `MEDIA DOC`
- 🟢 **ImageMagick/Pillow** → resize, composite, contact sheets, format conversion → `MEDIA TEX QA`
- 🟢 **skill-bundled fonts (proofs/_shared/fonts)** → load Cairo/Amiri/Tajawal/Reem Kufi/Aref Ruqaa files directly (system Arabic faces are weak here) → `ARAB ARL TYPE`
- 🟢 **git 2.43.0 + gh 2.89.0** → clone, branch, diff, PRs and CI logs (gh auth not checked) → `CODE AGENT`
- 🟢 **compilers: gcc, clang, go, rustc, java** → build native tools from source when no package exists → `CODE`
- 🟢 **open outbound network** → fetch docs, papers and pages from the shell (respect licenses and robots) → `WEB`
- 📦 **pip / uv + pypi reachable** → any wheel library is one command away (python3 -m pip install); 26 📦 catalog powers name a pip command → `ANLY MEDIA DOC SYNC GEN`
- 📦 **npm + registry reachable** → Remotion, d3, three.js, lottie, Motion Canvas, mermaid-cli; 327 📦 catalog powers name an npm/npx command → `APP ENG 3D DATA UI`
- 📦 **apt-get as root + mirror reachable** → system packages: tesseract, texlive, graphviz, blender, sox, fonts-noto; 2 📦 catalog powers name an apt/brew command → `MEDIA GRAPH 3D ARAB DOC`
- 📦 **huggingface.co reachable (no GPU)** → download small model weights and datasets; CPU only, keep models small (whisper tiny/base) → `GEN MEDIA SYNC`
- ❔ **docker client only (daemon not reachable)** → isolated services and toolchains → `CODE APP`

### One-line fixes — إصلاحات بسطر واحد

- good system Arabic font: `apt-get update -qq && apt-get install -y fonts-noto-core fonts-kacst` (ARAB TYPE)
- matplotlib: `python3 -m pip install matplotlib` (ANLY DATA)
- faster-whisper: `python3 -m pip install faster-whisper` (SYNC VOICE)
- librosa: `python3 -m pip install librosa` (BEAT)
- opencv-python-headless: `python3 -m pip install opencv-python-headless` (MEDIA QA)
- yt-dlp: `python3 -m pip install yt-dlp` (DL)
- duckdb: `python3 -m pip install duckdb` (ANLY)
- graphviz (dot): `apt-get update -qq && apt-get install -y graphviz` (GRAPH EXPL)
- XeLaTeX (Arabic math/print): `apt-get update -qq && apt-get install -y texlive-xetex texlive-lang-arabic` (DOC)
- blender: `apt-get update -qq && apt-get install -y blender` (3D)
- sox: `apt-get update -qq && apt-get install -y sox` (BEAT VOICE)

### Network — الشبكة

Level **full**. Proxy env names: HTTPS_PROXY, https_proxy, NO_PROXY, no_proxy. CA bundle loaded from: SSL_CERT_FILE, REQUESTS_CA_BUNDLE, CURL_CA_BUNDLE (verification stays on).
Agent proxy: enabled=True, covers every host=True, selective=False, preconfigured CLIs: bq, gcloud, gh, gsutil; recent relay failures: cdn-lfs.huggingface.co:443 (connect_rejected), www.gnu.org:443 (ws_closed_mid_exchange ×5). Rules: never disable TLS verification or unset the proxy; a 403/407/502 is a policy answer to report, not to route around; Node's built-in fetch needs NODE_USE_ENV_PROXY=1; details in /root/.ccr/README.md.

| Host | Role | Class | HTTP | ms |
|---|---|---|---|---|
| pypi.org | pip | ok | 200 | 39 |
| registry.npmjs.org | npm | ok | 200 | 50 |
| github.com | git | reachable | 400 | 288 |
| api.github.com | git | reachable | 400 | 288 |
| huggingface.co | models | ok | 200 | 697 |
| cdn.jsdelivr.net | cdn | ok | 200 | 671 |
| fonts.googleapis.com | fonts | ok | 200 | 457 |
| api.anthropic.com | claude-api | reachable | 404 | 44 |
| example.com | generic | ok | 200 | 406 |
| en.wikipedia.org | generic | ok | 200 | 579 |
| archive.ubuntu.com | apt | ok | 200 | 116 |

Classes: ok = 2xx/3xx · reachable = the host answered 4xx/5xx (normal for bare roots) · blocked = proxy refused · offline = DNS/timeout · tls-error = certificate not trusted.

### Machine & runtimes — الجهاز والبيئات

- OS: Ubuntu 24.04.5 LTS (x86_64, kernel 6.18.44-fc-v139) · user: root · container markers: none
- CPU 4 · RAM 15.7 GiB (14.9 GiB free) · disk free 22.3 GiB of 252.0 · temp write 157 MB/s · GPU: none (CPU rendering only)
- Versions: bun 1.4.2 · convert 6.9.12 · docker 29.8.2 · ffmpeg 6.1.1 · gcc 13.3.0 · gh 2.89.0 · git 2.43.0 · go 1.24.7 · java 21.0.12.1 · jq 1.7 · node 22.22.0 · npm 10.9.4 · pandoc 3.1.3 · pip 24.0 · playwright 1.56.1 · psql 16.15 · rustc 1.97.0 · soffice 24.2.7.2 · tesseract 5.3.4 · uv 0.11.32
- Package managers: pip usable · npm usable · apt usable · brew absent
- CLI tools by group: **pkg** apt-get · **cloud** bq, gcloud, gsutil · **dev** bun, cargo, clang, cmake, docker, g++, gcc, gh, git, go, java, make, node, npm, npx, perl, php, pip, pip3, pnpm, rg, ruby, rustc, uv, yarn · **image** convert, identify, tesseract · **misc** curl, fc-list, sudo, unzip, wget, zip · **video** ffmpeg, ffprobe · **data** jq, psql, redis-cli, redis-server, yq · **docs** libreoffice, pandoc, pdftoppm, pdftotext, soffice · **browser** playwright
- Not found on PATH: yt-dlp, mkvmerge, HandBrakeCLI, mpv, magick, inkscape, gimp, rsvg-convert, cwebp, exiftool, potrace, optipng, sox, lame, flac, espeak-ng, piper, qpdf, gs, pdflatex, xelatex, lualatex, tectonic, wkhtmltopdf, dot, mmdc, plantuml, d2, chromium, chromium-browser, google-chrome, google-chrome-stable, firefox, sqlite3, duckdb, mysql, mongosh, fd, deno, pipx, conda, podman, R, julia, dotnet, blender, openscad, aws, az, kubectl, terraform, wrangler, vercel, netlify, flyctl, firebase, nvidia-smi, ollama

### Python & Node packages — الحزم

- Python 3.13.16: 87 distributions; notable present: beautifulsoup4, jinja2, lxml, numpy, onnxruntime, openpyxl, pandas, pdfplumber, pillow, pypdf, pypdfium2, python-docx, python-pptx, reportlab, requests, xlsxwriter
- Notable absent (install on demand): aiohttp, altair, anthropic, arabic-reshaper, duckdb, fastapi, faster-whisper, flask, fonttools, graphviz, httpx, imageio, imageio-ffmpeg, jupyter, librosa, manim, markdown, matplotlib, moviepy, networkx, openai, openai-whisper, opencv-python, opencv-python-headless, playwright, plotly, polars, pyarrow, pydub, pymupdf, pytest, python-bidi, scikit-learn, scipy, seaborn, selenium, soundfile, statsmodels, streamlit, sympy, torch, transformers, weasyprint, yt-dlp
- venv yes · ensurepip yes · pip module yes · inside a venv no · system Python externally managed (PEP 668) no · sqlite3 3.45.1
- Node global packages (15): @anthropic-ai/claude-code, chromedriver, corepack, docx, eslint, http-server, nodemon, npm, playwright, pnpm, prettier, serve, ts-node, typescript, yarn

### Fonts & browsers — الخطوط والمتصفحات

- 28 font families; Arabic-capable: DejaVu Sans, DejaVu Sans Mono, FreeMono, FreeSerif, Unifont, Unifont Sample, Unifont-JP
- Good Arabic display faces installed: none — install fonts-noto-core or load the skill fonts
- Skill-bundled font files (proofs/_shared/fonts): Amiri-Bold.ttf, Amiri-Regular.ttf, ArefRuqaa-Regular.ttf, Cairo[slnt,wght].ttf, Lalezar-Regular.ttf, ReemKufi[wght].ttf, Tajawal-Bold.ttf, cairo-arabic-600-normal.woff2, cairo-arabic-800-normal.woff2, cairo-latin-600-normal.woff2, cairo-latin-800-normal.woff2, jetbrains-mono-latin-500-normal.woff2, jetbrains-mono-latin-700-normal.woff2, space-grotesk-latin-500-normal.woff2, space-grotesk-latin-700-normal.woff2
- Playwright browsers: chromium, chromium-1194, chromium_headless_shell-1194 · browsers on PATH: none

### Credentials & connectors — المفاتيح والموصلات

- MCP connectors, deferred tools and skills are invisible to this script: read your own tool list, load deferred tools with ToolSearch, and check the skills listing before deciding what you can do.

### Host evidence — دليل نوع المضيف

- Type: claude-code-cloud (scores claude-code-cloud=10, claude-ai-sandbox=1)
  - /root/.ccr exists
  - local agent proxy answered /__agentproxy/status
  - CLAUDE_CODE_REMOTE is set
  - working dir under /home/user

---
_Generated by `python3 scripts/probe_env.py --write references/environment.md`; do not edit by hand._
