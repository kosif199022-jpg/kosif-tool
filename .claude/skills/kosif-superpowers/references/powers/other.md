# قدرات مساندة — Supporting powers

> فصل مُجمَّع آليًا من 111 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **111 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 111 powers deduplicated by name from 111 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 12 · 🟢 جاهز 2 · 📦 بأمر تثبيت 16 · 🔑 مفتاح/خدمة 5 · 👁 شوهد في فيديو 1 · 📄 موصوف 75

#### MISC-01 · استوديو كاشف للمراجعة · KOSIF Audit Studio app (purpose) · ✅ مُثبت هنا
- **ماذا / what:** No-build vanilla-JS PWA (KOSIF 4 legacy + V5 continuous review) for Arabic audit files: trial-balance engine, analytics (ratios, Benford), council, report studio, and a live voice assistant. Visual value: several stacked themes, voice orb + waveform, SVG mini-charts, conic dials, and a stub 'cinema'…
- **كيف / how:** Serve statically (python3 -m http.server 8080) and open index.html (V5) or legacy.html (KOSIF 4 with voice panel).
- **أرقام / params:** v4.0.0 package; node --test tests/*.test.js
- **الدليل / proof:** `kosif-audit-studio/README.md` · `kosif-audit-studio/package.json` · `kosif-audit-studio/index.html`

#### MISC-02 · خادم MCP لـ Claude Code · MCP server for Claude Code (22 tools) · ✅ مُثبت هنا
- **ماذا / what:** A JSON-RPC MCP endpoint that lets Claude drive the studio: plan/validate/compile, read the environment, list and run recipes as jobs, poll jobs, read/write/create projects, check/save timelines, list transitions, render manifests and run the review loop.
- **كيف / how:** claude mcp add --transport http kosif-web http://127.0.0.1:8766/mcp; methods initialize (protocol 2025-03-26), tools/list, tools/call, ping.
- **أرقام / params:** tools: motion_plan, motion_validate, motion_compile, motion_templates, kosif_env, kosif_recipes, kosif_run, kosif_job, kosif_jobs, kosif_media, kosif_projects, kosif_project_read, kosif_project_write, kosif_project_create, kosif_timeline_check, kosif_timeline_save, kosif_transitions, kosif_render_ma…
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:697` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:205`

#### MISC-03 · عقد رد Claude والتطبيق بعد التأكيد · Studio reply contract and gated apply · ✅ مُثبت هنا
- **ماذا / what:** Claude answers with one ```json block holding notes, recipe actions, project files and an optional timeline; nothing runs until the user presses تطبيق, then files are written with .bak, the timeline is saved and actions are queued as jobs.
- **كيف / how:** claude_bridge.extract() (fenced json or bare object) → POST /api/claude/apply {plan}; index.html writes re-sync the kit (motion.sync_assets).
- **أرقام / params:** shape {notes, actions:[{recipe,args}], files:[{project,path,content}], timeline:{…}, timeline_name}
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/claude_bridge.py:146` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:653`

#### MISC-04 · ملف مشروع Studio وإعادة ربط الوسائط · Studio project file (.kosif.json) with media re-link · ✅ مُثبت هنا
- **ماذا / what:** Projects save as a small JSON without media; on open, the user re-picks originals and they re-link by name, size and modification time; unknown or executable properties are dropped.
- **كيف / how:** Save → NAME.kosif.json; Open (≤ 1 MB) → sanitizeProject() (version 1 only); assetKey = name:size:lastModified.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:161` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:7` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:13`

#### MISC-05 · موجّه القدرات · Deterministic capability router · ✅ مُثبت هنا
- **ماذا / what:** Routes Arabic/English requests to capability families, skills and tools by keyword (animation/motion graphics/video words go to the cinema family).
- **كيف / how:** kosif_route text=...; kosif_capabilities; kosif_skill_read name=...; kosif_doctor for environment status.
- **أرقام / params:** 18 families
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/tools_core.py:21` · `kosif-one/tools/kosif-omni/skills/kosif-omni/SKILL.md`

#### MISC-06 · سجل مصادر كتب درايف · Drive book provenance registry · ✅ مُثبت هنا
- **ماذا / what:** Registers Drive sources/chunks with SHA-256 dedupe, prompt-injection taint flags and revocation so book-derived craft rules stay traceable.
- **كيف / how:** skills/kosif-knowledge-atlas/scripts/knowledge_atlas.py (register_source, register_chunk, revoke_source, taint_scan); self-test script provided.
- **أرقام / params:** content_sha256 64 hex
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-knowledge-atlas/scripts/knowledge_atlas.py` · `kosif-one/tools/kosif-omni/skills/kosif-knowledge-atlas/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-knowledge-atlas/scripts/knowledge_atlas_self_test.py`

#### MISC-07 · بوابة الأفعال ونقاط التدخل البشري · Human-checkpoint action gate · ✅ مُثبت هنا
- **ماذا / what:** Classifies planned GUI/browser steps RUN/CONFIRM/HANDOFF/BLOCK (CAPTCHA, OTP, passwords, payments, send/delete/install).
- **كيف / how:** kosif_action_gate {goal, steps[], approved[], allowed_domains[]}; kosif_ui_ground for element grounding; kosif_risk_gate for publish/send.
- **أرقام / params:** exit 0 RUN, 1 CONFIRM, 4 HANDOFF, 3 BLOCK
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-computer-use/scripts/action_gate.py` · `kosif-one/tools/kosif-omni/skills/kosif-computer-use/scripts/ui_ground.py` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_server.py:210`

#### MISC-08 · أفضل وقت للنشر · Best time to post from own analytics · ✅ مُثبت هنا
- **ماذا / what:** Median metric per weekday x 3-hour block from the account's own export, vs overall median; refuses below 8 posts.
- **كيف / how:** python social.py besttime export.csv [--metric views] [--block 3].
- **أرقام / params:** >= 2 posts per cell
- **الدليل / proof:** `kosif-one/tools/kosif-social/SKILL.md`

#### MISC-09 · البحث في الاستايلات · Style search · ✅ مُثبت هنا
- **ماذا / what:** Searches 288 catalog entries by id, name, creator, keywords, category.
- **كيف / how:** python3 tools/kosif.py search <words> / list --category KEY / show <id> / stats.
- **الدليل / proof:** `kosif-tool/tools/kosif.py` · `kosif-tool/STYLE_INDEX.md`

#### MISC-10 · عرض الاستايلات · kosif.py list · ✅ مُثبت هنا
- **ماذا / what:** Table/JSON of styles filtered by category key or label, origin, type; sort by rank/name/published.
- **كيف / how:** python3 tools/kosif.py list [--category charts] [--origin KOSIF] [--type Style] [--sort rank|name|published] [--limit N] [--json]
- **الدليل / proof:** `kosif-tool/tools/kosif.py:329`

#### MISC-11 · البحث في الفهرس · kosif.py search · ✅ مُثبت هنا
- **ماذا / what:** Case-insensitive AND search over id, names, creator, keywords, summaries, categories and legacy labels; id hits score double.
- **كيف / how:** python3 tools/kosif.py search kinetic arabic [--limit N] [--json]
- **الدليل / proof:** `kosif-tool/tools/kosif.py:374`

#### MISC-12 · عرض استايل · kosif.py show · ✅ مُثبت هنا
- **ماذا / what:** Prints STYLE.json, BRIEF.md and playbook paths (with exists flag) and SKILL path for one id; suggests close ids on typos.
- **كيف / how:** python3 tools/kosif.py show <id>
- **أرقام / params:** difflib cutoff 0.5, 5 suggestions
- **الدليل / proof:** `kosif-tool/tools/kosif.py:400` · `kosif-tool/tools/kosif.py:227`

#### MISC-13 · شريط التقدم والتذييل · Footer label and progress bar · 🟢 جاهز
- **ماذا / what:** A small lime caption with the scene id and a rounded progress bar along the bottom showing playback position.
- **كيف / how:** label '600 {w*.024}px Arial' #c9f96d at y=.92h; track #293951 and fill #c9f96d rounded rect at y=.96h, width .82w*t/duration.
- **أرقام / params:** bar at 96% height, 82% width
- **الدليل / proof:** `fastify-motion-bro/web/motion.js:20-21` · `fastify-motion-bro/web/editorial.js:82-84`

#### MISC-14 · تسمية آمنة وتهريب النص · Safe naming and escaping · 🟢 جاهز
- **ماذا / what:** Project names are one folder (letters incl. Arabic, digits, _ -, ≤64 chars); titles are HTML-escaped and JSON placed in <script> has '</' escaped.
- **كيف / how:** motion.safe_name, html_text, json_for_script
- **أرقام / params:** regex ^[\w\u0600-\u06FF][\w\u0600-\u06FF-]{0,63}$
- **الدليل / proof:** `kosif-studio/motion/motion.py:85`

#### MISC-15 · التعرف الضوئي على النصوص في المسح والإطارات · OCR of scans and frames · 📦 بأمر تثبيت
- **ماذا / what:** Check whether a PDF has a text layer first (a many-page document returning only a few bytes from pdftotext is an image scan) before concluding something is absent; add an invisible OCR layer without changing appearance; Arabic needs the 'ara' traineddata.
- **كيف / how:** ocrmypdf + tesseract (needs install); for video frames: ffmpeg frame grab -> tesseract -l ara+eng.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1387-pdf-skills/3268-pdf-ocr-adding/SKILL.md`

#### MISC-16 · تطبيق كاشف للمراجعة الموحد · KOSIF Audit Pro app (purpose) · 📦 بأمر تثبيت
- **ماذا / what:** Arabic RTL audit workspace (Next.js 16 / React 19 / Tailwind 4 / shadcn new-york) that runs a deterministic BigInt trial-balance pipeline, 10 audit rounds, 26 gates and an advisory AI council. Its value for motion work is the tested design-token + cinematic CSS motion system, not the audit logic.
- **كيف / how:** Read app/globals.css tokens and components/kosif/*.tsx as a reference implementation of an RTL dashboard with contract-tested palette and motion; reuse tokens in HTML/Remotion compositions.
- **أرقام / params:** Node >=22.13; deps not installed here (no node_modules)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-audit-pro/README.md` · `kosif-audit-pro/package.json` · `kosif-audit-pro/app/layout.tsx`

#### MISC-17 · كتالوج الكتل والمكونات · Registry blocks & components catalog · 📦 بأمر تثبيت
- **ماذا / what:** 210 blocks and ~260 components (transitions, lower thirds, carousels, maps, charts, captions, cursors, liquid glass).
- **كيف / how:** hyperframes add <name>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks` · `kosif-one/vendor/hyperframes/registry/components`

#### MISC-18 · مشروع مثال night_boat · Example project night_boat · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'night_boat'.
- **كيف / how:** python scripts/kmotion.py sync projects/night_boat; render projects/night_boat --engine studio
- **أرقام / params:** 5 s 1920x1080 sea, felucca, 1900K lantern, fish splash at 2.8 s synced plink
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-19 · مشروع مثال blue_hour · Example project blue_hour · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'blue_hour'.
- **كيف / how:** python scripts/kmotion.py sync projects/blue_hour; render projects/blue_hour --engine studio
- **أرقام / params:** sodium lamps vs blue hour, car light trails, star arcs
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-20 · مشروع مثال koi_pond · Example project koi_pond · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'koi_pond'.
- **كيف / how:** python scripts/kmotion.py sync projects/koi_pond; render projects/koi_pond --engine studio
- **أرقام / params:** shallow water, caustics, koi, petals
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-21 · مشروع مثال lab_rabbit_lion · Example project lab_rabbit_lion · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'lab_rabbit_lion'.
- **كيف / how:** python scripts/kmotion.py sync projects/lab_rabbit_lion; render projects/lab_rabbit_lion --engine studio
- **أرقام / params:** 20 s 960x540 24 fps lab schematic
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-22 · مشروع مثال bunny_twin · Example project bunny_twin · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'bunny_twin'.
- **كيف / how:** python scripts/kmotion.py sync projects/bunny_twin; render projects/bunny_twin --engine studio
- **أرقام / params:** 5 s 1080x1920 plush bunny + truss
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-23 · مشروع مثال midnight_cat · Example project midnight_cat · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'midnight_cat'.
- **كيف / how:** python scripts/kmotion.py sync projects/midnight_cat; render projects/midnight_cat --engine studio
- **أرقام / params:** 12 s 1280x720 24 fps 2.5D scene
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-24 · مشروع مثال sound_ground · Example project sound_ground · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'sound_ground'.
- **كيف / how:** python scripts/kmotion.py sync projects/sound_ground; render projects/sound_ground --engine studio
- **أرقام / params:** spectrogram canyon + chrome orb
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-25 · مشروع مثال water_cycle_3d · Example project water_cycle_3d · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'water_cycle_3d'.
- **كيف / how:** python scripts/kmotion.py sync projects/water_cycle_3d; render projects/water_cycle_3d --engine studio
- **أرقام / params:** 3D explainer
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-26 · مشروع مثال showreel · Example project showreel · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'showreel'.
- **كيف / how:** python scripts/kmotion.py sync projects/showreel; render projects/showreel --engine studio
- **أرقام / params:** showreel
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-27 · مشروع مثال premium_edit · Example project premium_edit · 📦 بأمر تثبيت
- **ماذا / what:** Example composition source 'premium_edit'.
- **كيف / how:** python scripts/kmotion.py sync projects/premium_edit; render projects/premium_edit --engine studio
- **أرقام / params:** directed footage edit
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:226` · `100-superskills/skills/kosif-montage-motion/SKILL.md:432`

#### MISC-28 · التحكم بسطح المكتب مع البث الحي · Desktop control with Live View (KOSIF Mouse) · 📦 بأمر تثبيت
- **ماذا / what:** Background-first Windows automation: observe UIA tree/OCR with refs, ground Arabic/English instructions, gated batched actions with Claude's own pen pointer, Live View event stream.
- **كيف / how:** kosif_mouse_status/observe/find/act/do/live; emergency stop top-left corner or hold Esc; refuses over HTTP transport.
- **أرقام / params:** observe max_side 1280; idle guard 600 ms; settle 0.03 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/desktop.py:1` · `kosif-one/tools/kosif-omni/skills/kosif-mouse/SKILL.md` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_desktop.py:43`

#### MISC-29 · الوصول لمكتبة الأطلس · KOSIF Atlas library access (search/read/inspect/vendor) · 📦 بأمر تثبيت
- **ماذا / what:** Search, read-as-data, statically inspect and (with approval) vendor third-party skills from a 14,708-skill / 3,635-plugin permissive library — the place to find Remotion, ffmpeg, captions, music skills.
- **كيف / how:** kosif_atlas_status -> kosif_atlas_search query=... [no_executables=true] -> kosif_atlas_read skill_id=... -> kosif_atlas_inspect -> kosif_atlas_vendor confirm=true. Embedded pack file mcp-server/kosif_mcp/data/atlas_pack*.kpack is NOT present in this checkout; use KOSIF_ATLAS_SOURCE=external or the hosted edge API.
- **أرقام / params:** verdicts READ_ONLY_OK / REVIEW_BEFORE_INSTALL / DO_NOT_INSTALL; licenses MIT 3,280, Apache-2.0 337, BSD-3 10, ...
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/atlas.py:180` · `kosif-one/tools/kosif-omni/skills/kosif-atlas/SKILL.md` · `kosif-one/tools/kosif-omni/ATLAS_NOTICES.md`

#### MISC-30 · بحث نصي في الأطلس · Atlas full-text skill search · 📦 بأمر تثبيت
- **ماذا / what:** FTS5 search over 15,122 third-party skills to find a technique source.
- **كيف / how:** tools/deep_index.py builds SQLite FTS5; query with sqlite3 MATCH.
- **أرقام / params:** 15,107,396 words indexed
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/DEEP-INDEX.md` · `100-superskills/tools/deep_index.py`

#### MISC-31 · جسر Claude بأربع طرق · Claude bridge with four routes (CLI, API, MCP, copy-paste) · 🔑 مفتاح/خدمة
- **ماذا / what:** Sends the user's request plus live studio context to Claude and reads back a JSON plan: through the Claude Code CLI, the Anthropic API with a locally stored key, MCP (Claude drives the site), or a prompt package copied into any chat and the reply pasted back.
- **كيف / how:** POST /api/claude/ask {task, context:{media, projects, timeline, project}}; /api/claude/package returns the prompt; backend order auto→cli→api→mcp; CLI `claude -p PROMPT --output-format text` (prompt via stdin over 28,000 chars); API POST https://api.anthropic.com/v1/messages max_tokens 8000.
- **أرقام / params:** settings: backend auto|cli|api|mcp|none, model default 'claude-sonnet-5-5', timeout 240 s; context ≤ 60,000 chars; project file excerpt ≤ 40,000 chars; key shown only as first 7 chars
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/claude_bridge.py:27` · `100-superskills/skills/kosif-montage-motion/scripts/web/claude_bridge.py:73` · `100-superskills/skills/kosif-montage-motion/scripts/web/claude_bridge.py:108`

#### MISC-32 · واجهة الأطلس المستضافة · Hosted Atlas edge API · 🔑 مفتاح/خدمة
- **ماذا / what:** Cloudflare Worker for hosts without the local server: FTS search, read, Jev-judged select, Arabic->English translate, MCP endpoint.
- **كيف / how:** GET /search?q=&license=, GET /skill/<id>?file=, POST /select {task, top}, POST /translate, POST /mcp, GET /openapi.json at https://kosif-atlas-api.kosif199022.workers.dev.
- **أرقام / params:** rate limits 60/min search-read, 12/min Jev-translate; 14,793 skills
- **الدليل / proof:** `kosif-one/tools/kosif-omni/edge/atlas-api/README.md` · `kosif-one/tools/kosif-omni/chatgpt/custom-gpt/ATLAS-ACTION.md`

#### MISC-33 · اختيار المهارة تلقائياً · Auto skill selection (Jev-judged) · 🔑 مفتاح/خدمة
- **ماذا / what:** One call that understands the task (Arabic glossary/edge translation), gathers built-in + Atlas candidates, lets the live Jev service choose (asked twice, reversed) and returns the playbook.
- **كيف / how:** kosif_skill_auto task='اعمل موشن جرافيك لصوت' [top 2-9] [jev true|false]; falls back to deterministic ranking offline.
- **أرقام / params:** top default 8
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/skillengine.py:1` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/skillengine.py:282`

#### MISC-34 · عميل منصة العمل بالموافقة · Consent-gated workbench client · 🔑 مفتاح/خدمة
- **ماذا / what:** Reads/writes plans to the private KOSIF Motion Workbench only with a token supplied through an approved flow.
- **كيف / how:** python site_bridge.py ... (KOSIF_SITE_TOKEN).
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/site_bridge.py` · `kosif-one/tools/kosif-studio/tests/bridge/test_site_bridge.py`

#### MISC-35 · فحص واجهة أطلس المهارات · Skill Atlas API probe · 🔑 مفتاح/خدمة
- **ماذا / what:** Probes the KOSIF Atlas worker: health, skill search, Arabic->English translate, and task->skill selection with Jev.
- **كيف / how:** python probe.py (network) against /health, /search?q=, /translate, /select.
- **الدليل / proof:** `kosif-one/tools/kosif-edge-build/probe.py` · `kosif-one/tools/kosif-edge-build/defender-scan.json`

#### MISC-36 · علامة مائية قطرية · Diagonal trial watermark · 👁 شوهد في فيديو
- **ماذا / what:** repeat translucent text rotated -15°
- **الدليل / proof:** `style:pm-henkpoley-3d3407`

#### MISC-37 · منصة S.KOSIF / SQC (سياق المنتج) · S.KOSIF / SQC product (context) · 📄 موصوف
- **ماذا / what:** An Arabic-first, offline-capable web platform (PWA) for accounting, audit/assurance and accountant helper tools, entered section-first (accounting, audit, helper tools) then sector then company; reporting, analytics and AI are cross-cutting. Its visual work (themes, crystal world, cinematic intro, A…
- **كيف / how:** Reference only: when a user asks for motion or brand work for this product, respect the three-entry structure and the 'one identity' rule (FOUNDATION 3.11.2); never invent financial numbers in visuals.
- **أرقام / params:** 3 primary entries; brand names: S.KOSIF / KOSIF / SQC - Smart Quality Control; default identity «دفتر KOSIF» since 2026-10-09
- **الدليل / proof:** `kosif-earth-ci-fork/docs/START_HERE.md` · `kosif-earth-ci-fork/FOUNDATION.md:226` · `kosif-earth-ci-fork/FOUNDATION.md:679`

#### MISC-38 · قائمة مهارات الأطلس حسب المحور · Atlas skill shortlist by theme (cross-reference) · 📄 موصوف
- **ماذا / what:** Index of 12 candidate skills per axis (9 axes, incl. animation/3D, visual design, brand, data viz, UI QA) pulled from kosif-atlas with license and risk flags; reviewed as untrusted reference only.
- **كيف / how:** JSON: {axis: [{score,id,plugin,skill,license,risk,path}]}; motion axis tops: awwwards-motion (MIT, 10), webgpu-threejs-tsl (MIT), threejs-data-visualization (MIT), scrollytelling (MIT), three-webgl-game (MIT), gsap (Apache-2.0), microinteractions (MIT).
- **أرقام / params:** 9 axes x 12 = 108 entries
- **الدليل / proof:** `kosif-earth-ci-fork/tools/fixtures/atlas-themes.json` · `kosif-earth-ci-fork/docs/rebuild/ATLAS_REVIEW_ar.md`

#### MISC-39 · قاعدة المدخلات غير الموثوقة · Untrusted-input safety rule · 📄 موصوف
- **ماذا / what:** Treat uploaded ZIPs and public repos as data; validate archive paths, sizes, nested archives and secrets; never commit user media or API keys.
- **كيف / how:** .gitignore excludes .env, output/, assets/user/*, *.mp4/*.mov/*.wav/*.mp3 and per-profile sessions; agent inspects archives before use.
- **الدليل / proof:** `fastify-motion-bro/AGENTS.md:19-22` · `fastify-motion-bro/.gitignore:1-23` · `fastify-motion-bro/.env.example`

#### MISC-40 · تدقيق تراخيص المصادر · Source licence audit · 📄 موصوف
- **ماذا / what:** Inventory of inspiration repos with licences: motion-starter-kit MIT, brag MIT, scroll-world MIT, ai-design-skills MIT, hyperframes Apache-2.0, mcp-higgsfield-landing unverified (do not copy), kosif-one/kosif-studio owner.
- **كيف / how:** Consult before borrowing ideas; no vendor code is vendored here.
- **أرقام / params:** 8 sources
- **الدليل / proof:** `fastify-motion-bro/docs/SOURCE_AUDIT.md:1-11` · `fastify-motion-bro/README.md:69-77`

#### MISC-41 · عقود دخول الوكلاء · Agent entry contracts (multi-agent) · 📄 موصوف
- **ماذا / what:** Same contract wired for Claude (CLAUDE.md, .claude/skills), Codex/Cursor (AGENTS.md, .agents/skills), Gemini (GEMINI.md) and Copilot (.github/copilot-instructions.md).
- **كيف / how:** Each entry file points to AGENTS.md + the matching SKILL.md.
- **أرقام / params:** 9 skills x 3 identical copies
- **الدليل / proof:** `fastify-motion-bro/CLAUDE.md` · `fastify-motion-bro/GEMINI.md` · `fastify-motion-bro/.github/copilot-instructions.md`

#### MISC-42 · خريطة مصادر الحركة من الأطلس · Atlas-derived motion knowledge map · 📄 موصوف
- **ماذا / what:** The skill credits Atlas skills it distilled: awwwards-motion (MIT), hyperframes (Apache-2.0), ffmpeg/mas-video-lab (MIT), youtube subtitles/captions (MIT), remotion-best-practices (MIT), kinetic-inflated-hero/ui-motion (MIT), hyperframes sound/ambience (MIT, procedural risers/impacts/pads).
- **كيف / how:** Read the originals with kosif_atlas_read or from github.com/kosif199022-jpg/kosif-atlas before reuse; the procedural SFX synthesis it mentions has no code in this repo.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/atlas_15k_synthesis.md`

#### MISC-43 · خريطة المراكز والوكلاء · Hubs/agents lens map · 📄 موصوف
- **ماذا / what:** Maps the user's AI-Studio hubs (AutoDirector, CharacterForge, WorldBuilder, MotionVFX, CommercialFactory, VideoStudio, MusicStudio, VisualForensic...) to Omni skills/tools so Claude can speak from each lens.
- **كيف / how:** Look up the hub in the table and load the listed skill/tool.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/hubs-and-agents.md`

#### MISC-44 · تنفيذ الصور الآمن في وضع Full Pro · Full Pro secure image execution · 📄 موصوف
- **ماذا / what:** Pro-mode chain: SceneSpec -> digest freeze -> runtime authorization ticket -> secure executor -> pixel QA; host-native generation counts as bypass.
- **كيف / how:** Only when Full Pro is explicitly requested; local engine labels receipts LOCAL_ENGINE; the HMAC secure executor backend is packaged, not deployed.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/SKILL.md`

#### MISC-45 · معيار اختيار الأداة · Tool-choice scoring rubric · 📄 موصوف
- **ماذا / what:** Scores candidate tools before acting: capability 0-30, live availability 0-20, owner authority 0-15, verification/receipt 0-15, reversibility/safety 0-10, latency/cost 0-5, continuity 0-5; Jev picks among 2-5 viable ones.
- **كيف / how:** Apply when several render/edit routes exist (e.g. ffmpeg vs Remotion vs external app).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-source-router/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-source-router/references/mode-tool-routing-v10.md`

#### MISC-46 · مشغل التفكير الاحترافي · KOSIF Think Pro / Full Pro runtime · 📄 موصوف
- **ماذا / what:** Full Pro runtime, receipts, deterministic reasoning helpers (decision sensitivity, probability, calibration, KCL probes, project forge).
- **كيف / how:** Load skill kosif-think-pro (Skill tool or kosif_skill_read name=kosif-think-pro).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-think-pro/SKILL.md`

#### MISC-47 · التفكير أولاً · KOSIF Think (BrowserJev) · 📄 موصوف
- **ماذا / what:** Think-first orchestration, indexed browser action graphs, Jev ambiguity resolution, bounded recovery.
- **كيف / how:** Load skill kosif-think (Skill tool or kosif_skill_read name=kosif-think).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-think/SKILL.md`

#### MISC-48 · النواة المعرفية · Cognitive Core 28-module graph · 📄 موصوف
- **ماذا / what:** 28 reasoning modules (M01-M28) selected by task type; claim lifecycle and calibration.
- **كيف / how:** Load skill kosif-cognitive-core (Skill tool or kosif_skill_read name=kosif-cognitive-core).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cognitive-core/SKILL.md`

#### MISC-49 · مجلس الخمسمئة · Council-500 orchestration · 📄 موصوف
- **ماذا / what:** Same-input fan-out of up to 500 expert personas with Jev convergence and Einstein chair (not executable locally).
- **كيف / how:** Load skill kosif-council-500 (Skill tool or kosif_skill_read name=kosif-council-500).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-council-500/SKILL.md`

#### MISC-50 · كبير الخبراء أينشتاين · Einstein chief expert synthesis · 📄 موصوف
- **ماذا / what:** Seven-stage synthesis producing 2-4 candidates while preserving dissent.
- **كيف / how:** Load skill kosif-einstein-chief-expert (Skill tool or kosif_skill_read name=kosif-einstein-chief-expert).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-einstein-chief-expert/SKILL.md`

#### MISC-51 · مجلس العباقرة · Genius Council roster (1,040) · 📄 موصوف
- **ماذا / what:** 40 elite + 1,000 scholars, 51 domains; kosif_council_panel/expert/search/protocol.
- **كيف / how:** Load skill kosif-expert-council (Skill tool or kosif_skill_read name=kosif-expert-council).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-expert-council/SKILL.md`

#### MISC-52 · التداول السريع مع جيف · Expert-Jev fast convergence · 📄 موصوف
- **ماذا / what:** Clusters expert proposals and runs closed-set tournaments.
- **كيف / how:** Load skill kosif-expert-jev-deliberation (Skill tool or kosif_skill_read name=kosif-expert-jev-deliberation).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-expert-jev-deliberation/SKILL.md`

#### MISC-53 · التدقيق والمعايير الدولية · Audit & IFRS desk · 📄 موصوف
- **ماذا / what:** Accounting/IFRS/VAT controls with kosif_ledger_check.
- **كيف / how:** Load skill kosif-audit-ifrs (Skill tool or kosif_skill_read name=kosif-audit-ifrs).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-audit-ifrs/SKILL.md`

#### MISC-54 · تحكيم جيف · Jev closed-set arbitration · 📄 موصوف
- **ماذا / what:** Packets for yes/no, choice and rubric scoring; kosif_jev_decide calls the live service.
- **كيف / how:** Load skill kosif-jev (Skill tool or kosif_skill_read name=kosif-jev).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-jev/SKILL.md`

#### MISC-55 · متصفح جيف · Jev Browser · 📄 موصوف
- **ماذا / what:** Jev-guided browser planning through host browsers.
- **كيف / how:** Load skill kosif-jev-browser (Skill tool or kosif_skill_read name=kosif-jev-browser).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-jev-browser/SKILL.md`

#### MISC-56 · جسر واتساب · Guarded WhatsApp bridge · 📄 موصوف
- **ماذا / what:** Manual confirmed low-volume sends via the user's bridge.
- **كيف / how:** Load skill kosif-whatsapp (Skill tool or kosif_skill_read name=kosif-whatsapp).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-whatsapp/SKILL.md`

#### MISC-57 · جداول كوسيف · KOSIF Sheets · 📄 موصوف
- **ماذا / what:** Excel/SQLite builder playbook (see chart atom).
- **كيف / how:** Load skill kosif-sheets (Skill tool or kosif_skill_read name=kosif-sheets).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-sheets/SKILL.md`

#### MISC-58 · مشغل جيت هب · GitHub operator · 📄 موصوف
- **ماذا / what:** Safe git/GitHub workflows with kosif_gh_preflight.
- **كيف / how:** Load skill kosif-github (Skill tool or kosif_skill_read name=kosif-github).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-github/SKILL.md`

#### MISC-59 · أوركسترا كل الخبراء · Full Pro all-experts orchestra · 📄 موصوف
- **ماذا / what:** Policy that every 'kosif think 20 s' call is Council-500 Full Pro.
- **كيف / how:** Load skill kosif-full-pro-all-experts (Skill tool or kosif_skill_read name=kosif-full-pro-all-experts).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-full-pro-all-experts/SKILL.md`

#### MISC-60 · محرك التنفيذ · Full Pro execution engine · 📄 موصوف
- **ماذا / what:** Depth-first queue of real expert/Jev actions with receipts.
- **كيف / how:** Load skill kosif-full-pro-execution-engine (Skill tool or kosif_skill_read name=kosif-full-pro-execution-engine).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-full-pro-execution-engine/SKILL.md`

#### MISC-61 · بوابة التنفيذ · Full Pro execution gate · 📄 موصوف
- **ماذا / what:** Fail-closed authorization before substantive execution.
- **كيف / how:** Load skill kosif-full-pro-execution-gate (Skill tool or kosif_skill_read name=kosif-full-pro-execution-gate).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-full-pro-execution-gate/SKILL.md`

#### MISC-62 · مدخل Full Pro · Full Pro host entry · 📄 موصوف
- **ماذا / what:** Durable request registration; MCP kosif_full_pro_entry.
- **كيف / how:** Load skill kosif-full-pro-host-entry (Skill tool or kosif_skill_read name=kosif-full-pro-host-entry).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-full-pro-host-entry/SKILL.md`

#### MISC-63 · جسر الجوال · Mobile Full Pro bridge · 📄 موصوف
- **ماذا / what:** Mobile gateway fallback for Full Pro.
- **كيف / how:** Load skill kosif-mobile-full-pro-bridge (Skill tool or kosif_skill_read name=kosif-mobile-full-pro-bridge).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-mobile-full-pro-bridge/SKILL.md`

#### MISC-64 · جسر الإصدارات · Release bridge (GitHub/Cloudflare) · 📄 موصوف
- **ماذا / what:** Commit-to-deployment correlation and live verification.
- **كيف / how:** Load skill kosif-release-bridge (Skill tool or kosif_skill_read name=kosif-release-bridge).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-release-bridge/SKILL.md`

#### MISC-65 · منسق التشغيل · Runtime orchestrator · 📄 موصوف
- **ماذا / what:** Leased jobs, receipts and resume for Full Pro.
- **كيف / how:** Load skill kosif-runtime-orchestrator (Skill tool or kosif_skill_read name=kosif-runtime-orchestrator).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-runtime-orchestrator/SKILL.md`

#### MISC-66 · المنفذ الآمن · Secure executor (HMAC tickets) · 📄 موصوف
- **ماذا / what:** One-time execution tickets; packaged, not deployed. Hosts the strict SceneSpec validator.
- **كيف / how:** Load skill kosif-secure-executor (Skill tool or kosif_skill_read name=kosif-secure-executor).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-secure-executor/SKILL.md`

#### MISC-67 · سيد الكود · Code Master · 📄 موصوف
- **ماذا / what:** Programming playbook with kosif_code_scan and kosif_delivery_gate.
- **كيف / how:** Load skill kosif-code-master (Skill tool or kosif_skill_read name=kosif-code-master).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-code-master/SKILL.md`

#### MISC-68 · مهارة الماوس · KOSIF Mouse skill · 📄 موصوف
- **ماذا / what:** Playbook for Windows desktop control and Paint drawing (see drawing atoms).
- **كيف / how:** Load skill kosif-mouse (Skill tool or kosif_skill_read name=kosif-mouse).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-mouse/SKILL.md`

#### MISC-69 · أنماط تدقيق الإتاحة · WCAG 2.2 audit patterns (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-accessibility-compliance-wcag-audit-patterns.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-accessibility-compliance-wcag-audit-patterns/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-70 · قاعدة هندسة البرومبت · Prompt-engineering knowledge base (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-ai-tooling-prompt-engineering.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-ai-tooling-prompt-engineering/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-71 · التحقق العميق من الادعاءات · Deep claim verification (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-discipline-do-your-research-deep.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-discipline-do-your-research-deep/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-72 · محاسبة hledger · hledger plain-text accounting (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-hledger-hledger.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-hledger-hledger/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-73 · بناء حكم آلي · Build an LLM judge (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-llm-evaluation-engineering-build-llm-judge.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-llm-evaluation-engineering-build-llm-judge/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-74 · تصميم حزمة تقييم · Design an eval suite (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-llm-evaluation-engineering-design-eval-suite.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-llm-evaluation-engineering-design-eval-suite/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-75 · التحقق من الاستشهادات · AI citation verification (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-mas-ai-workflows-ai-citation-verification.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-mas-ai-workflows-ai-citation-verification/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-76 · كتابة وثيقة متطلبات · Create a PRD (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-pm-execution-create-prd.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-pm-execution-create-prd/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-77 · استخلاص المتطلبات · Requirements elicitation (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-requirements-elicitation-requirements-elicitation.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-requirements-elicitation-requirements-elicitation/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-78 · نمذجة التهديدات STRIDE · STRIDE threat modelling (vendored Atlas skill) · 📄 موصوف
- **ماذا / what:** Third-party skill vendored unmodified (except name) from the Atlas with LICENSE and ATTRIBUTION.md.
- **كيف / how:** Load skill atlas-security-scanning-stride-analysis-patterns.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/atlas-security-scanning-stride-analysis-patterns/SKILL.md` · `kosif-one/tools/kosif-omni/THIRD_PARTY_NOTICES.md`

#### MISC-79 · تصميم وتحليل التجارب · A/B Testing & Experiments · 📄 موصوف
- **ماذا / what:** Owner-built skill "A/B Testing & Experiments" (own words): workflow guidance for a/b testing & experiments; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill ab-testing-experiments (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/ab-testing-experiments/SKILL.md`

#### MISC-80 · قيود يومية صحيحة ومعايير IFRS/IAS مطبّقة · Accounting, Journal Entries & IFRS · 📄 موصوف
- **ماذا / what:** Owner-built skill "Accounting, Journal Entries & IFRS" (own words): workflow guidance for accounting, journal entries & ifrs; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill accounting-ifrs-journal (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/accounting-ifrs-journal/SKILL.md`

#### MISC-81 · برومبتات الوكلاء وأوصاف الأدوات وملفات S · Agent & Tool Instructions · 📄 موصوف
- **ماذا / what:** Owner-built skill "Agent & Tool Instructions" (own words): workflow guidance for agent & tool instructions; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill agent-tool-instructions (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/agent-tool-instructions/SKILL.md`

#### MISC-82 · واجهات API متينة (REST أو GraphQL) · Backend & API Design · 📄 موصوف
- **ماذا / what:** Owner-built skill "Backend & API Design" (own words): workflow guidance for backend & api design; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill backend-api-design (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/backend-api-design/SKILL.md`

#### MISC-83 · يحوّل كتاباً أو وثائق إلى مهارة قابلة لل · Book-to-Skill Knowledge Compiler · 📄 موصوف
- **ماذا / what:** Owner-built skill "Book-to-Skill Knowledge Compiler" (own words): workflow guidance for book-to-skill knowledge compiler; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill book-to-skill-knowledge (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/book-to-skill-knowledge/SKILL.md`

#### MISC-84 · من الفكرة إلى وثيقة قابلة للتنفيذ · Business Plan & PRD · 📄 موصوف
- **ماذا / what:** Owner-built skill "Business Plan & PRD" (own words): workflow guidance for business plan & prd; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill business-plan-prd (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/business-plan-prd/SKILL.md`

#### MISC-85 · Workers وPages وD1 وKV وR2 وQueues · Cloudflare & Edge Deployment · 📄 موصوف
- **ماذا / what:** Owner-built skill "Cloudflare & Edge Deployment" (own words): workflow guidance for cloudflare & edge deployment; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill cloudflare-edge-deploy (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/cloudflare-edge-deploy/SKILL.md`

#### MISC-86 · مراجعة صحة أولاً · Code Review & Refactoring · 📄 موصوف
- **ماذا / what:** Owner-built skill "Code Review & Refactoring" (own words): workflow guidance for code review & refactoring; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill code-review-refactor (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/code-review-refactor/SKILL.md`

#### MISC-87 · ما يدخل السياق وما لا يدخل · Context Window Budget · 📄 موصوف
- **ماذا / what:** Owner-built skill "Context Window Budget" (own words): workflow guidance for context window budget; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill context-window-budget (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/context-window-budget/SKILL.md`

#### MISC-88 · يحوّل أي مهارة أو خبرة إلى مساعد قابل لل · Custom GPT & Claude Project Builder · 📄 موصوف
- **ماذا / what:** Owner-built skill "Custom GPT & Claude Project Builder" (own words): workflow guidance for custom gpt & claude project builder; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill custom-gpt-claude-project (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/custom-gpt-claude-project/SKILL.md`

#### MISC-89 · تصميم قواعد بيانات صحيحة · Database Schema & Migrations · 📄 موصوف
- **ماذا / what:** Owner-built skill "Database Schema & Migrations" (own words): workflow guidance for database schema & migrations; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill database-schema-migrations (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/database-schema-migrations/SKILL.md`

#### MISC-90 · إصلاح أي خطأ من جذره · Root-Cause Debugging · 📄 موصوف
- **ماذا / what:** Owner-built skill "Root-Cause Debugging" (own words): workflow guidance for root-cause debugging; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill debugging-root-cause (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/debugging-root-cause/SKILL.md`

#### MISC-91 · إكسل كمنصّة أتمتة · Advanced Excel Automation · 📄 موصوف
- **ماذا / what:** Owner-built skill "Advanced Excel Automation" (own words): workflow guidance for advanced excel automation; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill excel-automation-power (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/excel-automation-power/SKILL.md`

#### MISC-92 · تحويل ملفات إكسل الفوضوية إلى بيانات نظي · Excel Data Cleaning & Automation · 📄 موصوف
- **ماذا / what:** Owner-built skill "Excel Data Cleaning & Automation" (own words): workflow guidance for excel data cleaning & automation; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill excel-data-cleaning-automation (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/excel-data-cleaning-automation/SKILL.md`

#### MISC-93 · نماذج إكسل تصمد أمام مراجعة مجلس الإدارة · Excel Financial Model Architect · 📄 موصوف
- **ماذا / what:** Owner-built skill "Excel Financial Model Architect" (own words): workflow guidance for excel financial model architect; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill excel-model-architect (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/excel-model-architect/SKILL.md`

#### MISC-94 · حل أي مشكلة إكسل · Excel Power Formulas · 📄 موصوف
- **ماذا / what:** Owner-built skill "Excel Power Formulas" (own words): workflow guidance for excel power formulas; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill excel-power-formulas (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/excel-power-formulas/SKILL.md`

#### MISC-95 · أمثلة ومجموعات تدريب وتقييم عالية الجودة · Few-Shot & Dataset Curation · 📄 موصوف
- **ماذا / what:** Owner-built skill "Few-Shot & Dataset Curation" (own words): workflow guidance for few-shot & dataset curation; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill few-shot-dataset-curation (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/few-shot-dataset-curation/SKILL.md`

#### MISC-96 · تعلّم بالاستدعاء النشط · Flashcards, Quizzes & Exam Prep · 📄 موصوف
- **ماذا / what:** Owner-built skill "Flashcards, Quizzes & Exam Prep" (own words): workflow guidance for flashcards, quizzes & exam prep; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill flashcards-quiz-exam-prep (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/flashcards-quiz-exam-prep/SKILL.md`

#### MISC-97 · تطبيق SaaS كامل من الصفر · Full-Stack SaaS Starter · 📄 موصوف
- **ماذا / what:** Owner-built skill "Full-Stack SaaS Starter" (own words): workflow guidance for full-stack saas starter; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill fullstack-saas-starter (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/fullstack-saas-starter/SKILL.md`

#### MISC-98 · إدارة المستودعات باحتراف · Git & GitHub Workflow · 📄 موصوف
- **ماذا / what:** Owner-built skill "Git & GitHub Workflow" (own words): workflow guidance for git & github workflow; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill git-github-workflow (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/git-github-workflow/SKILL.md`

#### MISC-99 · أتمتة Sheets وDocs وSlides وDrive وGmail · Google Workspace Automation · 📄 موصوف
- **ماذا / what:** Owner-built skill "Google Workspace Automation" (own words): workflow guidance for google workspace automation; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill google-workspace-automation (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/google-workspace-automation/SKILL.md`

#### MISC-100 · وثائق أعمال جاهزة · Invoices, Quotes & Contracts · 📄 موصوف
- **ماذا / what:** Owner-built skill "Invoices, Quotes & Contracts" (own words): workflow guidance for invoices, quotes & contracts; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill invoices-quotes-contracts (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/invoices-quotes-contracts/SKILL.md`

#### MISC-101 · نقل الأنظمة القديمة بأمان · Legacy Code Migration · 📄 موصوف
- **ماذا / what:** Owner-built skill "Legacy Code Migration" (own words): workflow guidance for legacy code migration; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill legacy-code-migration (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/legacy-code-migration/SKILL.md`

#### MISC-102 · برومبتات جاهزة ومُفحوصة لـ Copilot وChat · Office Prompts Library · 📄 موصوف
- **ماذا / what:** Owner-built skill "Office Prompts Library" (own words): workflow guidance for office prompts library; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill office-prompts-library (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/office-prompts-library/SKILL.md`

#### MISC-103 · كل ما يخص PDF · PDF Forms & Reports · 📄 موصوف
- **ماذا / what:** Owner-built skill "PDF Forms & Reports" (own words): workflow guidance for pdf forms & reports; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill pdf-forms-reports (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/pdf-forms-reports/SKILL.md`

#### MISC-104 · تأمين تطبيقات النماذج · Prompt Injection Defense · 📄 موصوف
- **ماذا / what:** Owner-built skill "Prompt Injection Defense" (own words): workflow guidance for prompt injection defense; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill prompt-injection-defense (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/prompt-injection-defense/SKILL.md`

#### MISC-105 · بناء نظام أسئلة وأجوبة على ملفاتك · RAG & Knowledge Base · 📄 موصوف
- **ماذا / what:** Owner-built skill "RAG & Knowledge Base" (own words): workflow guidance for rag & knowledge base; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill rag-knowledge-base (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/rag-knowledge-base/SKILL.md`

#### MISC-106 · مراجعة أمنية دفاعية · Security Audit (STRIDE) · 📄 موصوف
- **ماذا / what:** Owner-built skill "Security Audit (STRIDE)" (own words): workflow guidance for security audit (stride); helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill security-audit-stride (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/security-audit-stride/SKILL.md`

#### MISC-107 · قرارات عالية الأثر بمنهج · Strategy & Decision Sensitivity · 📄 موصوف
- **ماذا / what:** Owner-built skill "Strategy & Decision Sensitivity" (own words): workflow guidance for strategy & decision sensitivity; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill strategy-decision-sensitivity (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/strategy-decision-sensitivity/SKILL.md`

#### MISC-108 · توثيق يُقرأ · Technical Docs & README · 📄 موصوف
- **ماذا / what:** Owner-built skill "Technical Docs & README" (own words): workflow guidance for technical docs & readme; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill technical-docs-readme (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/technical-docs-readme/SKILL.md`

#### MISC-109 · جمع بيانات عامة من المواقع باحترام الشرو · Web Scraping & Automation · 📄 موصوف
- **ماذا / what:** Owner-built skill "Web Scraping & Automation" (own words): workflow guidance for web scraping & automation; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill web-scraping-automation (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/web-scraping-automation/SKILL.md`

#### MISC-110 · حدود توجيه KOSIF SEE · KOSIF SEE routing limits · 📄 موصوف
- **ماذا / what:** Register Montage & Motion as a media execution extension under kosif-media-motion; method packs and specialists capped; never claim a render from consultation.
- **كيف / how:** Follow when integrating with KOSIF SEE / Atlas.
- **أرقام / params:** max 4 method packs in Deep/Full Pro (2 normally); dynamic specialists ≤ 2 (1 normally); Atlas snapshot 15,122 skills (2026-10-07) as method evidence only
- **الدليل / proof:** `kosif-studio/motion/references/KOSIF_SEE_INTEGRATION.md`

#### MISC-111 · قائمة المصادر المسموحة · Source allowlist and reuse limits · 📄 موصوف
- **ماذا / what:** Allowed reference sources with licences (frontend-design Apache-2.0, HyperFrames+GSAP skills Apache-2.0, web-performance Apache-2.0, animation production MIT, GSAP matchMedia/Motion accessibility docs); others examined but not reused for missing licence text.
- **كيف / how:** Verify source, licence and version before moving text or code.
- **أرقام / params:** skill description < 200 chars
- **الدليل / proof:** `kosif-studio/motion/references/sources-ar.md`

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### MISC-P01 · سلّم اختيار سطح التشغيل وحزمة التنفيذ · Capability-surface ladder + execution packet · 📄 موصوف / documented only
- **ماذا / what:** قبل إضافة أداة أو خادم اختر أصغر سطح آمن يكفي، واحمل المهمة كحزمة صغيرة بدل سرد كل القدرات. / Before adding a tool or server pick the smallest safe surface that suffices, and carry the task as a small packet instead of listing every capability.
- **كيف / how:** Ladder: (1) always-on deterministic invariant → an existing rule; (2) on-demand procedure → an existing skill, not a new pack; (3) repeated structured tool with a live server → the canonical MCP after a live probe; (4) bounded deterministic operation → a trusted local CLI (Python/ffmpeg) verified installed; (5) narrow authenticated provider call → an approved API with budget. Context budget: router → at most 2 packs (4 in deep mode) → one reference → tool. Execution packet = {goal, artifact, constraints, owner, tools_allowed, evidence_required, state, next_step}. Separate "executed" from "verified"; retry only idempotent stages. Adapted from ECC (MIT) docs on capability-surface selection, harness construction and context budget. **أرقام / params:** 5 rungs · ≤2 packs (≤4 deep) · 8-field packet
- **الرخصة / license:** owner package; method adapted from affaan-m/ECC (MIT), no ECC code
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/ECC_DISTILLED_CORE.md` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/ECC_ROUTING_AND_EVAL.json`

#### MISC-P02 · حارس تصادم المسارات بعشر حالات ظل · Route-collision guard with 10 shadow cases · 📄 موصوف / documented only
- **ماذا / what:** جدول حالات اختبار يثبت أن طلب الفيديو لا يخطف طلب الصورة أو الأغنية أو الجهاز، والعكس. / A test table proving a video request never hijacks image, song or device routes, and vice versa.
- **كيف / how:** Negative routes: still image only → visual prompt core (no video engine); Suno/lyrics → Suno branch; "download from link" only → media-fetch owner, no auto-imitation; build/merge a skill → skill orchestrator + eval; device/Windows → computer owner; Full Pro only on explicit ask; "how many tokens now" → live meter or "unknown", never invented. Ten shadow cases in JSON (skill_self_dev, agent_contract, software_bug, image_prompt, video_edit, suno_lyrics, live_context, accounting, full_pro, device) each with route + whether ECC method applies. The package test asserts all 10 and the never_auto_install_third_party flag. Reuse the pattern for kosif-tool routing tests. **أرقام / params:** 10 cases · normal ≤2 packs, deep ≤4 · dynamic 1/2
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/ECC_ROUTING_AND_EVAL.json` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/KOSIF_SEE_CINEMATIC_ROUTER.md` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tests/test_ecc_upgrade.py`

#### MISC-P03 · اقتراح درس مشروعي بموافقة صريحة · Consent-gated, project-scoped lesson proposal · ✅ مُثبت هنا / proven here
- **ماذا / what:** الخبرة لا تُحفظ تلقائيًا: ملاحظة يقدمها المستخدم تصبح اقتراح درس داخل مشروع واحد فقط، وتُرفض بلا موافقة أو إن حوت سرًا. / Experience is never saved automatically: a user-supplied note becomes a lesson proposal for one project only, rejected without consent or if it contains a secret.
- **كيف / how:** python3 integrations/kosif-see/ecc_contract_gate.py propose-lesson rec.json --consent. Record needs project_id (regex [A-Za-z0-9_-]{3,80}, blocks path traversal), trigger, action, evidence, observed_at; scope must be "project" (global needs separate review, evidence from ≥2 distinct projects, negative-trigger tests and approval); secret-like text (sk-…, api_key=…, private keys) is rejected. Output status proposed_not_published, promotion manual_review_required. Covered by 5 passing package tests here. **أرقام / params:** project scope only · ≥2 projects before global · exit 0/2
- **الرخصة / license:** owner package; method adapted from affaan-m/ECC (MIT), no ECC code
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/ecc_contract_gate.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tests/test_ecc_upgrade.py`

#### MISC-P04 · كتالوج 60 معاينة مفهومية مولّدة بالكود · 60-card concept-preview catalog generator (A01–A60) · ✅ مُثبت هنا / proven here
- **ماذا / what:** ستون بطاقة قدرة (مسار، نابض، رسم بياني، كاميرا، كتابة، واجهة، جسيمات، شخصية، موجة صوت، فيلم)، لكل واحدة صورة ومقطع قصير مرسومان بالكود ومعيار قبول. / Sixty capability cards, each with a code-drawn thumbnail, a short clip and an acceptance test.
- **كيف / how:** python3 tools/render_catalog.py --id A22 (or --all [--fps 15 --seconds 2]); 280×498 frames in ten visual families (path, spring, chart, camera, type, ui, particle, person, wave, film). references/CAPABILITIES.csv lists for each Axx the mechanism, prerequisite, sample output and acceptance check (e.g. A23 word-by-word reveal: sync ±100 ms on key words; A50 deterministic seek: shuffled-seek test; A52 frame-diff spike report). catalog/index.html is a searchable offline gallery. These clips illustrate the idea — they are not proof that 3D, ASR, lip-sync or mimic run. Ran --id A22 here: OK. **أرقام / params:** 60 cards · 280×498 · 10 families
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/render_catalog.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/references/CAPABILITIES.csv` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/catalog/CATALOG.json` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/catalog/index.html`
