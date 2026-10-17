---
name: kosif-superpowers
description: Production superpowers for KOSIF TOOL motion-graphics films — observe the reference (fetch permitted media, sample frames, cuts, palette), animate, render deterministically, 3D space, draw, data, voice sync, Arabic text, captions, generative assets, orchestration and design — each backed by a verified catalog of 100 major open-source GitHub repositories with licenses and invocation notes, plus a doctor that says which tools are installed here. Use when planning, building, inspecting or verifying a film from this atlas, when a playbook step needs a tool beyond tools/, or when the user says superpowers, superskills, قوى, kosif-superpowers.
---

# KOSIF Superpowers — قوى KOSIF

Twelve production superpowers for films made from this atlas. Each one is a capability a KOSIF film-maker reaches for at a known step (observe → plan → build → sync → render → verify → deliver), backed by a verified catalog of **100 major open-source repositories** (`repos.json`, rendered as `references/repos.md`), concrete recipes (`references/capabilities.md`), two scripts and process rules adapted from the Claude Code skills ecosystem. The catalog links and credits; it never vendors third-party code, prompts, media or model weights, and a plan may only promise tools that `scripts/superpowers.py doctor` marks as installed.

**بالعربية:** اثنتا عشرة قوة إنتاجية لأفلام هذا الأطلس. كل قوة قدرة يستعين بها صانع الفيلم في خطوة معروفة (رصد → تخطيط → بناء → مزامنة → رندر → تحقق → تسليم)، مدعومة بفهرس موثّق من **100 مستودع مفتوح المصدر** (`repos.json` ← `references/repos.md`)، ووصفات تنفيذ (`references/capabilities.md`)، وسكربتَين، وقواعد عملية مستوحاة من منظومة مهارات Claude Code. الفهرس يربط وينسب الفضل ولا يضمّن كودًا أو نصوصًا أو وسائط لطرف ثالث، والخطة لا تعِد إلا بما يؤكده `doctor` أنه مثبّت.

## 1. When to use — متى تستخدمه

- Right after CLAUDE.md → AGENTS.md → the style's `SKILL.md`/`STYLE.json`/`BRIEF.md` → its playbooks, whenever a step needs more than the repository's own `tools/`: inspecting a reference video, word-level alignment, 3D text in Arabic, beat-driven cuts, generative placeholder assets, palette extraction, parallel scene builds.
- When the user says *superpowers*, *superskills*, *قوى*, *ما الأدوات المتاحة*, or asks which open-source tool fits a need.
- Before promising any integration: run the doctor first.

This skill never replaces the style guide or the playbooks; it extends their steps with vetted tools and a stricter process.

**بالعربية:** استخدمه بعد قراءة ملفات الاستايل ودلائله عندما تحتاج خطوة إلى أكثر من أدوات المستودع، أو حين يسأل المستخدم عن القوى أو عن الأداة المناسبة لحاجة ما. وقبل أن تعِد بأي تكامل شغّل `doctor`.

## 2. Codebase map — خريطة المستودع

The repository was indexed with Graphify (commit `629a59b`, 1,255 nodes · 2,135 edges); this is the dependency picture that index gives, so you know where to start reading before you extend anything.

| module | role | depends on | start reading at |
|---|---|---|---|
| `tools/kosif.py` | CLI: `list`, `search`, `show`, `prompt`, `scaffold`, `validate`, `stats`. The `Atlas` class is a read-only view of `catalog/styles.json` + `catalog/categories.json`; `cmd_scaffold` fills `templates/*.md` and copies a starter. Referenced by every `styles/<id>/SKILL.md` (175 files). | `catalog/`, `templates/`, `starters/`, `tools/validate.py` | `Atlas.__init__`, `cmd_scaffold`, `build_prompt` |
| `tools/build.py` | Regenerates `styles/<id>/SKILL.md`, `STYLE_INDEX.md`, `catalog/playbooks.json`, `catalog/meta.json`, `sitemap.xml` and the README statistics block; `--check` guards CI. | `catalog/`, `playbooks/` | `skill_md()`, `main()` |
| `tools/validate.py` | 14 catalog and policy checks (`Report`), including *no rehosted media*; imported by `tests/test_catalog.py`. | `catalog/`, `styles/` | `run()` |
| `tools/sync_catalog.py` | Pulls metadata and links (never prompt text) from the source library into `styles.json`. | network, `catalog/categories.json` | `main()`, `base_records()` |
| `tools/render_html.cjs` | Deterministic HTML → MP4 with Playwright + ffmpeg (`seek` and `virtual` modes, `--preview` contact sheet). Referenced by 172 style skills and `playbooks/render-pipeline.md`. | Playwright, ffmpeg | `tools/render_html.md` |
| `tools/verify_video.py`, `tools/words_convert.py` | Delivery gate (ffprobe, EBU R128) and subtitle/Whisper → `words.json`. | ffmpeg | module docstrings |
| `web/app.js`, `web/generator.js` | Static site: loads `catalog/*.json`, renders library and request generator from `templates/claude_request.*.txt`. | `catalog/`, `templates/` | `load()`, `viewStyle()`, `cliCommand()` |
| `starters/html-canvas`, `starters/remotion` | Film starters: `window.__kosif.seek(t)` timeline with word-synced Arabic captions; Remotion v4 composition. | — | each `README.md` |
| `tests/` | Python `unittest` (synthetic fixture in `_fixture.py`) + Node `node:test`; CI runs validate → build --check → tests. | everything above | `tests/_fixture.py` |

Reading order for a newcomer: `AGENTS.md` → `tools/kosif.py` (Atlas, scaffold) → `playbooks/render-pipeline.md` → `tools/render_html.md` → `starters/html-canvas/README.md` → this skill. Re-index after structural changes; the Graphify tools answer "who calls X", "what does a change affect" and "which tests cover it" faster than grep.

**بالعربية:** الجدول أعلاه هو صورة الاعتماديات كما يراها فهرس Graphify: `kosif.py` يقرأ الفهرس ويبني المشروع، `build.py` يولّد الملفات المشتقة، `validate.py` يفحص السياسة، `render_html.cjs` يرندر حتميًا، والموقع يقرأ `catalog/*.json`. ترتيب القراءة: AGENTS.md ثم kosif.py ثم دليل الرندر ثم المشاريع البادئة ثم هذه المهارة.

## 3. The twelve superpowers — القوى الاثنتا عشرة

| key | بالعربية | adds | reach first for | details |
|---|---|---|---|---|
| `observe` | رصد المرجع | fetch permitted media, contact sheet, scene cuts, palette, frame-step analysis | `scripts/fetch_reference.py`, ffmpeg; OpenCV / PySceneDetect when installed | [reference-inspection.md](references/reference-inspection.md), [capabilities.md#observe](references/capabilities.md#observe) |
| `animate` | التحريك | timelines, easing, path and shape morphing, physics, particles | GSAP / anime.js / motion in `starters/html-canvas`; flubber for morphs | [capabilities.md#animate](references/capabilities.md#animate) |
| `render` | الرندر | deterministic frames, encoding, programmatic video, previews, gates | `tools/render_html.cjs`, Remotion, ffmpeg | [capabilities.md#render](references/capabilities.md#render) |
| `space` | الفضاء ثلاثي الأبعاد | WebGL scenes, cameras, 3D text, model loading, depth-based parallax | three.js (+ troika for Arabic 3D text), react-three-fiber | [capabilities.md#space](references/capabilities.md#space) |
| `draw` | الرسم | SVG/Canvas drawing, sketchy looks, draw-on strokes, creative coding | p5.js, Rough.js, Paper.js, PixiJS | [capabilities.md#draw](references/capabilities.md#draw) |
| `data` | البيانات | charts, maps, diagrams, data-driven motion | D3, ECharts, Vega-Lite, MapLibre, Mermaid | [capabilities.md#data](references/capabilities.md#data) |
| `voice` | الصوت | word timestamps, forced alignment, TTS, beat and loudness analysis | faster-whisper / WhisperX (install first), librosa, `tools/words_convert.py` | [capabilities.md#voice](references/capabilities.md#voice) |
| `arabic` | النص العربي | RTL shaping, bidi, fonts, diacritics, Arabic NLP | HarfBuzz-backed browsers, arabic-reshaper + python-bidi, Noto/Amiri fonts | [capabilities.md#arabic](references/capabilities.md#arabic), `playbooks/arabic-typography.md` |
| `captions` | الترجمات | subtitle formats, word-timing conversion, karaoke captions | `tools/words_convert.py`, pysubs2, ffsubsync | [capabilities.md#captions](references/capabilities.md#captions) |
| `generate` | التوليد | AI images, video, 3D, talking heads, voices as original assets | ComfyUI-class pipelines run elsewhere; weights licenses checked | [capabilities.md#generate](references/capabilities.md#generate) |
| `orchestrate` | التنسيق | Claude Code skills, subagents, worktrees, MCP, browser automation for QA | process checklist below; Playwright MCP, chrome-devtools-mcp | [capabilities.md#orchestrate](references/capabilities.md#orchestrate) |
| `design` | التصميم | UI motion patterns, icon sets, design tokens, scroll/parallax | Lucide / Phosphor icons, open-props tokens, Lenis | [capabilities.md#design](references/capabilities.md#design) |

Every repository in the catalog carries: GitHub URL, stars, license and a license note (permissive · weak copyleft · copyleft: run as an external tool · model/weights license · custom), bilingual summary, the KOSIF step it serves, a one-line invocation and the playbooks it strengthens. `python3 .claude/skills/kosif-superpowers/scripts/superpowers.py search <words>` finds them in Arabic or English.

## 4. Production runbook with superpowers — خطوات الإنتاج بالقوى

0. **Doctor.** `python3 .claude/skills/kosif-superpowers/scripts/superpowers.py doctor` — promise only what is ✓. On the KOSIF cloud machine that is Node 22, Python 3.13, ffmpeg 6, Playwright with Chromium under `/opt/pw-browsers` (never run `playwright install`), git; Whisper, OpenCV, Blender and any GPU are **not** installed — write "install first" or "run elsewhere and import the result".
1. **Brainstorm before code.** Restate concept, audience, aspect, duration and source material; list unknowns; ask at most one batch of questions (AGENTS.md 3). Pick the style ID with `python3 tools/kosif.py search`.
2. **Observe.** `python3 .claude/skills/kosif-superpowers/scripts/fetch_reference.py <page-or-media-url>` → `.kosif-cache/reference/<slug>/{reference.mp4, contact.png, cuts.json, palette.json, REPORT.md}` — permitted media only, encrypted streams refused, nothing committed. If the player hides the URL (`blob:`), read the network panel or a page-scanning extension first ([reference-inspection.md](references/reference-inspection.md)). If you could not open it, say so in STYLE.md.
3. **Plan.** `python3 tools/kosif.py scaffold <id> <dir> --starter html-canvas|remotion`; fill STYLE.md (*observed* = measured numbers, *assumed* = inferred) and PLAN.md scene by scene with timestamps from `words.json` or `cuts.json`.
4. **Build scene by scene.** One scene = one reviewable commit. For parallel scenes, dispatch subagents in separate git worktrees, each returning a preview frame and the exact files it changed; merge, then re-run the preview on the whole film.
5. **Sync.** Voice is the master clock: transcribe with word timestamps (install faster-whisper or WhisperX first, or import a `words.json` produced elsewhere), convert with `tools/words_convert.py`, start each action 40–80 ms before its word, check key words ≤ 100 ms (`playbooks/audio-sync.md`).
6. **Verify before claiming done.** Contact sheet, a 2–4 s motion clip at half resolution, user approval, final render, `python3 tools/verify_video.py` gate, `TEST_REPORT.md` filled with measured values. "Done" without a passing gate is not done.
7. **Review and finish.** Request review with the checklist (observed vs assumed honoured, licenses credited, no rehosted media, determinism, Arabic shaping intact, timings within tolerance); apply the feedback; commit, push, open the PR only when asked.

**بالعربية:** (0) شغّل `doctor` ولا تعِد إلا بما هو مثبّت. (1) فكّر قبل الكود واسأل حزمة أسئلة واحدة. (2) ارصد المرجع بسكربت الجلب أو اكتب أنك لم تستطع فتحه. (3) ابنِ STYLE.md وPLAN.md مشهدًا مشهدًا. (4) ابنِ كل مشهد في التزام منفصل، ووزّع المشاهد المتوازية على وكلاء في worktrees. (5) الصوت هو الساعة الأساسية. (6) تحقق قبل أن تقول «تم». (7) اطلب المراجعة ثم أنهِ الفرع.

## 5. Guardrails — الضوابط

- **Licenses.** Permissive → install, import, ship with credit. Weak copyleft → link or run as-is. Copyleft (GPL/AGPL) → call as an external CLI, never vendor. Model/weights licenses → read commercial terms before delivery. Credit every tool in `TEST_REPORT.md`'s stack line. Legend in [repos.md](references/repos.md).
- **Originality.** This repository stores no third-party prompt text, code, media or weights; recipes describe steps in KOSIF's own words and link the owner's repository.
- **Determinism.** frame = f(t); seeded randomness; fonts ready before frame 0; no network at render time; preview before the final render.
- **Arabic.** Shape and bidi are the browser's job (HarfBuzz); never split joined letters to animate them; test with the Arabic playbook's checklist.
- **Audio.** Never stretched or resampled; the film fits the voice.
- **Media policy.** Fetched references stay in `.kosif-cache/` (git-ignored); delete before sharing; never cut into the deliverable.
- **Honesty.** Never imply an integration that is not installed; never claim to have watched what you could not open.

**بالعربية:** التزم بالتراخيص (المتساهل يُثبَّت، GPL يُستدعى كأداة خارجية فقط، أوزان النماذج تُقرأ شروطها)، ولا تخزّن نصوصًا أو كودًا أو وسائط لطرف ثالث، واحفظ الحتمية، ولا تفصل حروف العربية، ولا تمسّ الصوت، وأبقِ المراجع في `.kosif-cache/`، ولا تدّعِ تكاملًا غير مثبّت أو مشاهدة لم تحدث.

## 6. Files — الملفات

| path | content |
|---|---|
| `SKILL.md` | this guide |
| `repos.json` | the catalog: 100 verified repositories, twelve capabilities, fourteen research domains |
| `references/repos.md` | the catalog rendered as tables (generated — run `scripts/superpowers.py build`) |
| `references/capabilities.md` | one section per superpower: what it adds, decision table, recipes, pitfalls, playbooks extended |
| `references/reference-inspection.md` | the observe superpower in depth: permission, three routes to the media, what to measure, limits |
| `scripts/superpowers.py` | `list · search · show · doctor · stats · build · check` |
| `scripts/fetch_reference.py` | page / direct / HLS → `reference.mp4` + probe, contact sheet, cuts, palette, report |
| `../../../tests/test_superpowers.py` | tests for all of the above (run with `npm test` or `python3 -m unittest tests.test_superpowers`) |

## 7. Commands — الأوامر

```bash
python3 .claude/skills/kosif-superpowers/scripts/superpowers.py doctor                 # what is installed here
python3 .claude/skills/kosif-superpowers/scripts/superpowers.py list --capability voice # tools for one superpower
python3 .claude/skills/kosif-superpowers/scripts/superpowers.py search محاذاة كلمات     # Arabic or English search
python3 .claude/skills/kosif-superpowers/scripts/superpowers.py show openai/whisper     # one record with license and caveats
python3 .claude/skills/kosif-superpowers/scripts/fetch_reference.py https://example.com/post --list   # media URLs on a page
python3 .claude/skills/kosif-superpowers/scripts/fetch_reference.py https://cdn.example.com/clip.mp4  # fetch + measure
python3 .claude/skills/kosif-superpowers/scripts/superpowers.py check                  # catalog + derived file sanity (CI)
```

Attribution: every repository named in this skill belongs to its authors under its own license; see [repos.md](references/repos.md) for the full credited list.
