# الترسانة العامة — General libraries arsenal (non-motion)

What this gives you: 139 general-purpose Python and npm libraries (data, documents, web, ML, image, audio, geo, math, Arabic, quality, agents, apps, 3D, finance) with version, license, what each unlocks, and whether it was actually installed and run in a Claude container. It also lists the license red flags and the API changes your training data does not know about.
Open it when a task needs a library you have not used in this session, before writing code from memory, and before saying something cannot be done. Motion and video libraries live in `arsenal-libraries.md`; how to discover and verify is in `self-discovery.md`.

## الفهرس / contents
1. How this was verified, and how to re-verify
2. Training-data APIs are stale: lessons
3. Golden pairs
4. Install recipes for the awkward ones
5. Library table by domain (17 groups)
6. License red flags
7. Credits

## 1. كيف فُحص / How this was verified, and how to re-verify
- Date and place: 2026-10-16, a Claude Code on the web container (Linux, Python 3.13.16, Node 22.22.0, npm 10.9.4, 4 vCPU, no GPU). Re-run `python3 scripts/probe_env.py` to see your own machine.
- Versions and licenses: re-queried on 2026-10-16 from PyPI JSON (`license_expression`, else `license`, else classifiers) and `npm view <pkg> version license --json`, then normalised to SPDX or a short note.
- ✅ = installed as a wheel into a venv and one real operation ran (the "evidence" column says which). 69 of 69 attempted wheel installs succeeded, each in under 3 minutes; npm `docx`, `pptxgenjs`, `exceljs` and `pdf-lib` each wrote a real file. 📦 = the registry resolves, but it was not installed. ❌ = tried and failed (the reason is given).
- ✅ is a lease from that container. In a new session, re-check with:
```bash
python3 -m venv /tmp/v && /tmp/v/bin/pip install -q --only-binary=:all: <pkg> && /tmp/v/bin/python -I -c "import <mod>; print(<mod>.__version__)"
curl -s https://pypi.org/pypi/<pkg>/json | python3 -c "import json,sys;i=json.load(sys.stdin)['info'];print(i['version'],i.get('license_expression') or i.get('license'),i['requires_python'])"
npm view <pkg> version license --json
```
Totals in the table: ✅ 77 · 📦 62 · ❌ 0.

## 2. واجهات الذاكرة قديمة / Training-data APIs are stale: lessons
Check the version and run one line before you build on remembered code. Each of these was caught in a real run (re-confirmed items marked P16, see `proofs/general-discovery/README.md`):
1. **pulp 4.0**: `pulp.LpVariable('x',0,4)` raises TypeError (the core is now Rust) and `PULP_CBC_CMD` is gone; the only bundled solver is HiGHS. Use `x = m.add_variable('x', 0, 4); m.solve(pulp.HiGHS(msg=False))`, or use ortools (P16). Do not import pulp 4 (highspy) and ortools in one Python process: both bundle HiGHS, so ortools fails with an ImportError (undefined symbol in libortools) or pulp reports "HiGHS: Not Available". Use separate processes or venvs.
2. **mcp 2.x**: `from mcp.server.fastmcp import FastMCP` fails; use `from mcp.server import MCPServer` with `@srv.tool()` (P16).
3. **markitdown 0.1.8**: the bare install fails on .docx; install `"markitdown[docx,pdf,xlsx,pptx]"`.
4. **pymupdf**: `import fitz` is deprecated; use `import pymupdf`. It is AGPL-3.0.
5. **plotly**: `write_html` inlines 4.8 MB of JS; pass `include_plotlyjs="cdn"`.
6. **openpyxl** stores formulas but never computes them (P16 read back `'=A1*2'`); recalculate with `soffice --headless --convert-to xlsx`.
7. **pytesseract** is only a wrapper; it needs the `tesseract` binary (`apt-get install -y tesseract-ocr tesseract-ocr-ara`). easyocr is a pure-pip alternative but pulls torch.
8. **graphviz** (Python) only builds DOT source; rendering needs the `dot` binary (`apt-get install -y graphviz`), mermaid-cli or viz.js.
9. **faker('ar_EG')** returned a Latin name: do not trust locales for Arabic fixtures.
10. **weasyprint 70** rendered RTL Arabic HTML to PDF (pango present). It is the best HTML→PDF path for Arabic reports.
11. **Pillow 12 and matplotlib 3.11 shape Arabic themselves** (both wheels bundle libraqm 0.10.5): pass raw logical text. Adding `arabic_reshaper.reshape()` + `bidi.algorithm.get_display()` on top reverses it (`proofs/general-data`, `mpl_arabic_modes.png`). Route on `PIL.features.check('raqm')` or `matplotlib.ft2font.__libraqm_version__`; use reshaper+bidi only for reportlab or a build without raqm.
12. **Major bumps**: pandas 3, numpy 2.5, polars 2, opencv 5, transformers 5, sentence-transformers 6, librosa 1.0, mermaid 12, next 16, vite 8, tailwind 4, react 19.
13. **npm `plantuml` is a 0.0.2 stub**: use plantuml.jar with Java. `@hyperframes/cli` does not exist on npm; the HyperFrames CLI is the `hyperframes` bin.
14. **Python-version gates**: `kokoro` resolves to 0.7.16 on Python 3.13 (latest needs below 3.13); `TTS` (Coqui) needs below 3.12, so use the `coqui-tts` fork or `uv venv --python 3.12` (P14).
15. **torch default wheel pulls CUDA (GBs)**: use `--index-url https://download.pytorch.org/whl/cpu` (21 s, 769 MB).

## 3. التوليفات الذهبية / Golden pairs
| Job | Pair | Why |
|---|---|---|
| SQL on files | duckdb + polars (or pandas) | query CSV/Parquet in place, fast, MIT |
| Documents out | python-docx / python-pptx / openpyxl / xlsxwriter + weasyprint or reportlab | real Office and PDF files; weasyprint handles Arabic RTL |
| Documents in | markitdown[extras] + pdfplumber / pypdf | any office file or PDF → Markdown or tables for reading |
| Exact reasoning | sympy, z3-solver, ortools, cvxpy | compute instead of guessing: algebra, constraints, LP/MIP, convex |
| Audio analysis | librosa + pyloudnorm (+ pedalboard, GPL) | pitch, beats, onsets, LUFS, effects |
| Maps | geopandas + shapely + pyproj + folium | reproject, buffer, Leaflet HTML |
| Self-verification | ruff + bandit + pytest + hypothesis | lint, security, tests, property tests |
| Agents | anthropic + mcp (Python) / @modelcontextprotocol/sdk | build Claude API apps and MCP servers (API key 🔑) |
| Web text | httpx + trafilatura (+ beautifulsoup4/lxml) | fetch through the proxy, then extract the main text |

## 4. وصفات تثبيت / Install recipes for the awkward ones
- CPU torch: `pip install torch --index-url https://download.pytorch.org/whl/cpu`
- markitdown: `pip install "markitdown[docx,pdf,xlsx,pptx]"`
- OCR: `apt-get install -y tesseract-ocr tesseract-ocr-ara && pip install pytesseract`
- Diagrams: `apt-get install -y graphviz` (for `graphviz`, `diagrams`) or `npm i -g @mermaid-js/mermaid-cli` (uses Chromium)
- Browser automation: `pip install playwright && python -m playwright install chromium` (~150 MB), unless a bundled Chromium already exists (check `$PLAYWRIGHT_BROWSERS_PATH`)
- Old-Python-only libraries: `uv venv --python 3.12 /tmp/v312 && uv pip install --python /tmp/v312/bin/python <pkg>`
- Heavy model downloads (whisper, rembg, transformers, easyocr): test Hugging Face reachability first (`curl -sI https://huggingface.co`); keep models small on CPU.

## 5. جدول المكتبات / Library table by domain
Columns: package · ecosystem · version (2026-10-16) · license · what it unlocks · status · evidence and caveats.

### البيانات والتحليل — Data & analysis
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `pandas` | PyPI | 3.0.6 | BSD-3-Clause | DataFrames, CSV/Excel/Parquet IO, groupby | ✅ | sum of column =6 |
| `polars` | PyPI | 2.0.0 | MIT | fast Rust DataFrames, lazy queries | ✅ | mean =2.0; v2.0 API changes vs 1.x |
| `duckdb` | PyPI | 1.5.6 | MIT | SQL over CSV/Parquet/pandas in-process | ✅ | select 42*2 =84 |
| `pyarrow` | PyPI | 26.0.0 | Apache-2.0 | Parquet/Arrow IO | ✅ | parquet round-trip 2 rows |
| `numpy` | PyPI | 2.5.4 | BSD-3-Clause (+0BSD, MIT, Zlib, CC0 parts) | arrays | ✅ | (dependency of all) |
| `scipy` | PyPI | 1.18.1 | BSD-3-Clause | optimize, stats, signal | ✅ | minimize (x-3)^2 -> 3.0 |
| `statsmodels` | PyPI | 0.15.0 | BSD-3-Clause | regression, time series, tests | ✅ | OLS slope 2.0 |
| `scikit-learn` | PyPI | 1.9.1 | BSD-3-Clause | classic ML, pipelines | ✅ | RF on iris score 1.0 |
| `xgboost` | PyPI | 3.4.1 | Apache-2.0 | gradient boosting | ✅ | fit/predict |
| `lightgbm` | PyPI | 4.7.0 | MIT (upstream; PyPI field blank) | fast GBDT | ✅ | fit/predict |
| `prophet` | PyPI | 1.5.0 | MIT | business forecasting | 📦 | pulls cmdstan; heavy |

### الرسوم البيانية — Charts & visualization
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `matplotlib` | PyPI | 3.11.2 | PSF-based (matplotlib license) | static PNG/SVG/PDF charts | ✅ | saved PNG 26,860 B; PSF-style license |
| `seaborn` | PyPI | 0.13.2 | BSD-3-Clause | statistical plots | ✅ | histplot |
| `plotly` | PyPI | 7.1.0 | MIT | interactive HTML charts | ✅ | write_html 4.8 MB (full JS inlined; use include_plotlyjs="cdn"); PNG export needs kaleido+Chrome |
| `altair` | PyPI | 6.3.0 | BSD-3-Clause | Vega-Lite declarative charts | ✅ | chart JSON |
| `bokeh` | PyPI | 3.10.1 | BSD-3-Clause | interactive web plots | 📦 |  |
| `d3` | npm | 7.9.0 | ISC | custom SVG viz | 📦 |  |

### المستندات والمكتب — Documents & office
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `python-docx` | PyPI | 1.2.0 | MIT | write/read .docx | ✅ | wrote+read Arabic+English paragraph |
| `python-pptx` | PyPI | 1.0.2 | MIT | write/read .pptx | ✅ | title round-trip |
| `openpyxl` | PyPI | 3.1.5 | MIT | xlsx read/write incl. formulas | ✅ | formula =A1*2 stored (not computed); no formula calc; use LibreOffice headless to recalc |
| `xlsxwriter` | PyPI | 3.2.9 | BSD-2-Clause | rich xlsx writing, charts | ✅ |  |
| `reportlab` | PyPI | 5.0.1 | BSD (ReportLab) | programmatic PDF | ✅ | PDF 1,352 B |
| `weasyprint` | PyPI | 70.0 | BSD-3-Clause | HTML/CSS -> PDF (RTL works) | ✅ | RTL Arabic h1 -> PDF 3,033 B; needs pango system libs (present here) |
| `pypdf` | PyPI | 6.21.0 | BSD-3-Clause | PDF split/merge/text | ✅ | extracted "Hello PDF" |
| `pdfplumber` | PyPI | 0.11.10 | MIT | PDF text+tables with positions | ✅ | "Hello PDF" |
| `pymupdf` | PyPI | 1.28.2 | AGPL-3.0 or Artifex commercial | fast PDF render/text/edit | ✅ | text + page->PNG; AGPL-3.0 (or commercial); `import fitz` deprecated, use `import pymupdf` |
| `markitdown` | PyPI | 0.1.8 | MIT | any office/PDF -> Markdown for LLM | ✅ | after `pip install "markitdown[docx,pdf,xlsx,pptx]"`; bare install FAILS on docx (MissingDependency); install extras |
| `docling` | PyPI | 2.140.0 | MIT | layout-aware PDF->MD/JSON (IBM) | 📦 | pulls torch + models; large |
| `camelot-py` | PyPI | 2.0.0 | MIT | PDF table extraction | 📦 | needs ghostscript/opencv |
| `tabula-py` | PyPI | 2.10.0 | MIT | PDF tables via Java | 📦 | needs Java |
| `docx` | npm | 9.11.0 | MIT | .docx from JS | ✅ | Packer.toBuffer 9,533 B |
| `pptxgenjs` | npm | 4.0.1 | MIT | .pptx from JS | ✅ | writeFile a.pptx |
| `exceljs` | npm | 4.4.0 | MIT | xlsx from JS | ✅ |  |
| `pdf-lib` | npm | 1.17.1 | MIT | create/modify PDF in JS | ✅ | 834 B |
| `pdfkit` | npm | 0.20.2 | MIT | PDF gen JS | 📦 |  |
| `jspdf` | npm | 4.2.1 | MIT | browser PDF | 📦 |  |

### الويب والجلب — Web, HTTP & scraping
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `httpx` | PyPI | 0.28.1 | BSD-3-Clause | HTTP client sync/async, HTTP/2 | ✅ | GET pypi -> 200 via proxy |
| `requests` | PyPI | 2.34.2 | Apache-2.0 | HTTP client | ✅ | (installed as dep) |
| `beautifulsoup4` | PyPI | 4.15.0 | MIT | HTML parsing | ✅ | with lxml |
| `lxml` | PyPI | 6.1.3 | BSD-3-Clause | fast XML/HTML, XPath | ✅ |  |
| `trafilatura` | PyPI | 2.3.1 | Apache-2.0 | main-text extraction from pages | ✅ | extracted article text |
| `playwright` | PyPI | 1.64.0 | Apache-2.0 | headless browser automation, screenshots | 📦 | needs `playwright install chromium` (~150 MB) |
| `selenium` | PyPI | 4.51.0 | Apache-2.0 | browser automation | 📦 | needs driver/browser |
| `scrapy` | PyPI | 2.19.0 | BSD-3-Clause | crawling framework | 📦 |  |
| `feedparser` | PyPI | 6.0.14 | BSD-2-Clause | RSS/Atom | ✅ | parsed item title |
| `newspaper4k` | PyPI | 0.9.6 | MIT | news article extraction | 📦 |  |

### التعلم الآلي المحلي واللغة — Local ML & NLP
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `torch` | PyPI | 2.14.1 | compound: Apache-2.0 AND BSD-3-Clause AND MIT AND … (PyPI) | tensors, NN | ✅ | CPU wheel: 21 s install, 769 MB on disk; 2.14.1+cpu ran tensor inverse; use --index-url https://download.pytorch.org/whl/cpu (default pulls CUDA, GBs) |
| `transformers` | PyPI | 5.20.1 | Apache-2.0 | HF models | 📦 | models download from HF hub; check network |
| `sentence-transformers` | PyPI | 6.1.0 | Apache-2.0 | embeddings/semantic search | 📦 | needs torch |
| `onnxruntime` | PyPI | 1.31.0 | MIT | run ONNX models CPU | ✅ | providers CPU+Azure |
| `faster-whisper` | PyPI | 1.2.1 | MIT | speech-to-text (CTranslate2), word timestamps | 📦 | model download |
| `openai-whisper` | PyPI | 20250625 | MIT | STT reference impl | 📦 | needs torch |
| `piper-tts` | PyPI | 1.8.0 | GPL-3.0-or-later | offline TTS | 📦 | GPL-3.0 |
| `diffusers` | PyPI | 0.41.0 | Apache-2.0 | image diffusion | 📦 | GPU realistically required |
| `accelerate` | PyPI | 1.15.0 | Apache-2.0 | HF device mgmt | 📦 |  |
| `spacy` | PyPI | 3.8.16 | MIT | NER, parsing pipelines | 📦 | models separate |
| `nltk` | PyPI | 3.10.3 | Apache-2.0 | classic NLP utils | ✅ | edit_distance=3; corpora need nltk.download |
| `gensim` | PyPI | 4.4.0 | LGPL-2.1-only | topic models, word2vec | 📦 | LGPL-2.1 |
| `llama-cpp-python` | PyPI | 0.3.36 | MIT | GGUF LLMs on CPU | 📦 | compiles from source (slow) |

### الصور وOCR — Image & OCR
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `pillow` | PyPI | 12.3.0 | MIT-CMU | image create/edit | ✅ | rendered text PNG |
| `opencv-python-headless` | PyPI | 5.0.0.93 | Apache-2.0 | CV ops | ✅ | Canny edges; v5.0 major bump |
| `scikit-image` | PyPI | 0.26.0 | BSD-3-Clause | scientific image processing | ✅ | sobel |
| `rembg` | PyPI | 2.0.85 | MIT | background removal | 📦 | downloads U2Net model |
| `imageio` | PyPI | 2.38.1 | BSD-2-Clause | image/video IO | ✅ | read PNG |
| `pillow-heif` | PyPI | 1.8.1 | BSD-3-Clause | HEIC/AVIF | 📦 |  |
| `cairosvg` | PyPI | 2.9.1 | LGPL-3.0-or-later | SVG -> PNG/PDF | ✅ | PNG 602 B; LGPL-3.0; needs libcairo (present) |
| `pytesseract` | PyPI | 0.3.13 | Apache-2.0 | OCR wrapper | ✅ | first run failed (no tesseract binary); after the binary was apt-installed later the same day, OCR of a rendered PNG returned 'Kosif OCR 2026' exactly, langs ara/eng/osd (proof P20); needs the tesseract binary (apt) |
| `easyocr` | PyPI | 1.7.2 | Apache-2.0 | OCR incl. Arabic, pure pip | 📦 | needs torch + model download |
| `sharp` | npm | 0.35.5 | Apache-2.0 | fast libvips image ops | 📦 |  |

### الصوت — Audio
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `librosa` | PyPI | 1.0.0 | ISC | analysis: pitch, beats, onsets | ✅ | YIN pitch of 440 Hz sine = 440.4 (venv in the 2026-10-16 run; not preinstalled — `pip install librosa`) |
| `soundfile` | PyPI | 0.14.0 | BSD-3-Clause | WAV/FLAC IO | ✅ |  |
| `pydub` | PyPI | 0.25.1 | MIT | simple audio editing via ffmpeg | 📦 | ffmpeg present; pydub unmaintained & audioop removed in py3.13 |
| `pyloudnorm` | PyPI | 0.2.0 | MIT | LUFS loudness (BS.1770) | ✅ | -9.76 LUFS on test sine |
| `demucs` | PyPI | 4.1.0 | MIT | stem separation | 📦 | torch + model; slow on CPU |
| `pedalboard` | PyPI | 0.9.26 | GPL-3.0 | Spotify effects (reverb, compressor, VST) | ✅ | chain applied; GPL-3.0 |

### الخرائط — Geo & maps
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `geopandas` | PyPI | 1.2.0 | BSD-3-Clause | geo DataFrames | ✅ | reproject to EPSG 3857 |
| `shapely` | PyPI | 2.2.0 | BSD-3-Clause | geometry ops | ✅ | buffer area 3.137 |
| `pyproj` | PyPI | 3.8.0 | MIT | CRS transforms | ✅ | Cairo lon 31.2 -> x 3,473,168 |
| `folium` | PyPI | 0.20.0 | MIT | Leaflet HTML maps | ✅ | map.html |
| `osmnx` | PyPI | 2.1.1 | MIT | OSM street networks | 📦 | needs network to Overpass |
| `rasterio` | PyPI | 1.5.2 | BSD-3-Clause | raster GIS | 📦 |  |

### الرياضيات والمنطق والتحسين — Math, logic, optimization, graphs
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `sympy` | PyPI | 1.14.0 | BSD-3-Clause | symbolic algebra | ✅ | solve x²-5x+6 -> [2,3]; ∫sin² |
| `mpmath` | PyPI | 1.4.1 | BSD-3-Clause | arbitrary precision | ✅ | (sympy dep) |
| `z3-solver` | PyPI | 5.3.1.0 | MIT | SMT solving/puzzles/verification | ✅ | a+b=10,a-b=4 -> a=7,b=3 |
| `ortools` | PyPI | 9.15.6755 | Apache-2.0 | LP/MIP/CP-SAT/routing | ✅ | GLOP maximize -> 10.0 |
| `pulp` | PyPI | 4.0.1 | MIT | LP modelling | ✅ | only with v4 API: `m.add_variable("x",0,4)` + `pulp.HiGHS(msg=False)`; classic `LpVariable(...)`/`PULP_CBC_CMD` FAIL; pulp 4.0 broke API and no longer bundles CBC |
| `cvxpy` | PyPI | 1.9.3 | Apache-2.0 | convex optimization | ✅ | argmin (x-2)² = 2.0 |
| `networkx` | PyPI | 3.7 | BSD-3-Clause | graph algorithms | ✅ | shortest path |
| `igraph` | PyPI | 1.0.0 | GPL (version per repo) | fast graph analytics | 📦 | GPL-2.0+ |

### اللغة العربية — Arabic language
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `camel-tools` | PyPI | 1.6.0 | MIT | morphology, dialect ID, NER | 📦 | data packages to download |
| `pyarabic` | PyPI | 0.6.15 | GPL (version not stated) | tashkeel strip, normalize | 📦 | GPL |
| `arabic-reshaper` | PyPI | 3.0.1 | MIT | glyph shaping for non-shaping renderers (reportlab, or PIL/matplotlib builds without raqm) | ✅ | reshaped+bidi "سلام" |
| `python-bidi` | PyPI | 0.6.11 | LGPL (version per repo) | bidi reorder | ✅ | LGPL |
| `farasapy` | PyPI | 0.1.1 | none on PyPI | Farasa segmenter wrapper | 📦 | needs Java; no license on PyPI |

### الجودة والاختبار والأمان — Quality, testing & security
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `bandit` | PyPI | 1.9.4 | Apache-2.0 | Python security lint | ✅ | flagged shell=True (3 issues) |
| `semgrep` | PyPI | 1.181.0 | LGPL-2.1-or-later | multi-lang SAST | 📦 | LGPL; rules registry online |
| `pip-audit` | PyPI | 2.10.1 | Apache-2.0 | dependency CVE audit | 📦 |  |
| `ruff` | PyPI | 0.17.1 | MIT | lint+format, very fast | ✅ | F401 reported |
| `mypy` | PyPI | 2.4.0 | MIT | type check | 📦 |  |
| `pyright` | PyPI | 1.1.414 | MIT | type check (node) | 📦 | downloads node pkg |
| `black` | PyPI | 26.10.1 | MIT | formatter | 📦 |  |
| `pytest` | PyPI | 9.1.1 | MIT | tests | ✅ | with hypothesis: "1 passed" |
| `hypothesis` | PyPI | 6.170.1 | MPL-2.0 | property-based testing | ✅ | MPL-2.0 |

### الوكلاء وواجهات النماذج — LLM & agents
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `anthropic` | PyPI | 1.15.0 | MIT | Claude API SDK | ✅ | import 1.15.0; needs ANTHROPIC_API_KEY 🔑 |
| `mcp` | PyPI | 2.3.0 | MIT | build MCP servers/clients | ✅ | with v2 API `from mcp.server import MCPServer`; `mcp.server.fastmcp` FAILS in 2.x |
| `claude-agent-sdk` | PyPI | 0.2.168 | MIT | programmatic Claude Code agents | 📦 | needs key |
| `@anthropic-ai/sdk` | npm | 0.135.0 | MIT | Claude API TS | 📦 | 🔑 |
| `@modelcontextprotocol/sdk` | npm | 1.32.1 | MIT | MCP TS | 📦 |  |
| `@anthropic-ai/claude-agent-sdk` | npm | 0.3.301 | SEE LICENSE IN README.md (Anthropic terms, not OSI) | agents TS | 📦 | (license: SEE LICENSE IN README = proprietary terms) |

### التطبيقات والواجهات — Apps & UI
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `fastapi` | PyPI | 0.143.3 | MIT | HTTP APIs | ✅ | TestClient GET / -> {ok:1} |
| `flask` | PyPI | 3.1.3 | BSD-3-Clause | web apps | 📦 |  |
| `streamlit` | PyPI | 1.66.0 | Apache-2.0 | data apps | 📦 |  |
| `gradio` | PyPI | 6.30.0 | Apache-2.0 | ML demo UIs | 📦 |  |
| `jinja2` | PyPI | 3.1.6 | BSD-3-Clause | templating | ✅ |  |
| `vite` | npm | 8.3.4 | MIT | bundler/dev server | 📦 |  |
| `react` | npm | 19.3.1 | MIT | UI | 📦 |  |
| `next` | npm | 16.4.2 | MIT | full-stack React | 📦 |  |
| `svelte` | npm | 5.57.2 | MIT | UI compiler | 📦 |  |
| `tailwindcss` | npm | 4.3.3 | MIT | utility CSS | 📦 |  |

### المخططات — Diagrams
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `graphviz` | PyPI | 0.21 | MIT | DOT source builder | ✅ | source built; render ❌ no `dot` binary; apt install graphviz to render |
| `diagrams` | PyPI | 0.25.1 | MIT | cloud architecture diagrams | 📦 | needs graphviz binary |
| `@mermaid-js/mermaid-cli` | npm | 12.0.0 | MIT | mmdc -> SVG/PNG (needs Chromium via puppeteer) | 📦 |  |
| `mermaid` | npm | 12.2.0 | MIT | diagram renderer | 📦 |  |
| `plantuml` | npm | 0.0.2 | MIT (0.0.2 stub) | npm pkg is a stub 0.0.2 — use plantuml.jar + Java instead | 📦 | ⚠ |

### ثلاثي الأبعاد — 3D & CAD
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `trimesh` | PyPI | 5.1.1 | MIT | meshes, STL/GLB | ✅ | box volume 1.0, STL export |
| `open3d` | PyPI | 0.20.0 | MIT | point clouds | 📦 | big; py3.13 wheels may lag |
| `cadquery` | PyPI | 2.8.0 | Apache-2.0 | parametric CAD -> STEP/STL | 📦 | OCP wheel large |
| `bpy` | PyPI | 5.2.2 | GPL-3.0 | Blender as module | 📦 | GPL-3.0; pinned Python version |
| `three` | npm | 0.186.1 | MIT | WebGL 3D | 📦 |  |

### المال — Finance
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `yfinance` | PyPI | 1.7.0 | Apache-2.0 | Yahoo market data | 📦 | scraped unofficial API, ToS |
| `pandas-ta` | PyPI | 0.4.71b0 | none on PyPI | technical indicators | 📦 | beta; no license field |
| `quantstats` | PyPI | 0.0.86 | Apache-2.0 | portfolio tearsheets | 📦 |  |

### أدوات مساعدة — Utilities
| package | eco | version | license | unlocks | status | evidence / caveat |
|---|---|---|---|---|---|---|
| `rich` | PyPI | 15.0.0 | MIT | pretty terminal | ✅ |  |
| `typer` | PyPI | 0.27.3 | MIT | CLIs | ✅ | 0.27.3 |
| `tqdm` | PyPI | 4.70.1 | MPL-2.0 AND MIT | progress bars | ✅ | (dep); MPL-2.0+MIT |
| `pydantic` | PyPI | 2.14.1 | MIT | validation/schemas | ✅ | coerced "5"->5 |
| `faker` | PyPI | 40.43.0 | MIT | fake data | ✅ | (ar_EG locale returned Latin name "Laurie White" — locale not fully Arabic) |
| `qrcode` | PyPI | 8.2 | BSD | QR PNG | ✅ | 449 B |
| `python-barcode` | PyPI | 0.16.1 | MIT | EAN/Code128 PNG/SVG | ✅ | bc.png |

## 6. تنبيهات الرخص / License red flags
| Class | Packages here | What it means for you |
|---|---|---|
| AGPL | pymupdf (or commercial) | fine as a tool on the user's files; do not ship it inside a networked product without compliance |
| GPL | piper-tts, pedalboard, igraph, pyarabic, bpy | fine for producing output; bundling or redistributing the code makes the whole work GPL |
| LGPL | gensim, cairosvg, python-bidi, semgrep | dynamic use is fine; modified copies of the library must stay LGPL |
| MPL | hypothesis, tqdm (+MIT) | file-level copyleft on modified files only |
| Not OSI / see README | @anthropic-ai/claude-agent-sdk | Anthropic commercial terms; read before redistributing |
| Blank or unclear on PyPI | lightgbm (upstream MIT), farasapy, pandas-ta | check the repo LICENSE before vendoring |
| Unofficial data source | yfinance | scraped API: terms of service apply |
Using any of these as tools to make the user's files is normally fine. Copying their code or text into this skill is not, unless the license allows it and the notice is kept.

## 7. المصادر / Credits
- Package metadata: PyPI JSON API and the npm registry, queried 2026-10-16. Smoke tests and installs: a same-day general-arsenal run in a Claude Code on the web container; traps re-confirmed in `proofs/general-discovery/README.md` (P14-P17).
- Reuse-before-build and license-scoring ideas: ECC `search-first` skill, MIT (c) 2026 Affaan Mustafa, https://github.com/affaan-m/ECC (paraphrased).
