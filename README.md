# KOSIF TOOL — أطلس الموشن جرافيك لـ Claude Code

<!-- stats:start -->
**297** styles · **251** PromptsMotion references · **46** KOSIF base styles · **45** original briefs · **19** playbooks · **225** credited creators
<!-- stats:end -->

## ابدأ من هنا — خريطة المستودع / Start here

مستودع واحد فيه ثلاث طبقات تعمل معًا. اقرأ هذه الخريطة مرة واحدة فتعرف أين كل شيء.

| الطبقة / layer | ما هي / what | من أين تبدأ / start |
|---|---|---|
| **المهارة العامة** `.claude/skills/kosif-superpowers/` | تعرّف Claude بقدراته الحقيقية في كل جلسة وبطرق التفكير والإبداع والتحقق، مع كتالوج 5,860 قدرة في 10 مجالات، لكل قدرة مستلزماتها (التفكير، الكتابة والعربية، الكود، البيانات، المستندات، البحث، التطبيقات، الصور والصوت، المنتج والمال، الموشن) لكل منها شارة دليل، وأكثر من 90 أداة تُشغَّل فعلًا وباب واحد للبحث فيها | [SKILL.md](.claude/skills/kosif-superpowers/SKILL.md) ثم [الفهرس](.claude/skills/kosif-superpowers/references/INDEX.md) و[الخريطة الذهنية](.claude/skills/kosif-superpowers/references/capability-map.md) |
| **أطلس الموشن** `styles/` `playbooks/` `catalog/` | 289 أسلوب موشن جرافيك، لكل منها SKILL.md وSTYLE.json وBRIEF.md، و17 دليل إنتاج | [STYLE_INDEX.md](STYLE_INDEX.md) · [AGENTS.md](AGENTS.md) |
| **الأدوات** `tools/` `starters/` `templates/` | `kosif.py` (بحث وتجهيز مشروع)، `render_html.cjs` (رندر HTML إلى فيديو)، `verify_video.py` (فحص الناتج)، ومشروعا بداية html-canvas وRemotion | [tools/render_html.md](tools/render_html.md) |
| **مهارة المونتاج التحريري** `.claude/skills/editorial-film-edit/` | مهارة مستقلة لمونتاج لقطات بأسلوب أرشيفي تحريري مع مراجع متصفح جاهزة | [SKILL.md](.claude/skills/editorial-film-edit/SKILL.md) |
| **المشاريع** `projects/` | أفلام منتهية بمصادرها القابلة للتعديل: مفاتيح الثروة، تحية مصر والسعودية، وثلاث ريلز أدعية | [projects/README.md](projects/README.md) |
| **الموقع** `index.html` `web/` | واجهة تصفح الأساليب ومولّد الطلبات، تُنشر على GitHub Pages | https://kosif199022-jpg.github.io/kosif-tool/ |

**لـ Claude — ابدأ هنا:** إن وصلك رابط هذا المستودع فقط فاقرأ [CAPABILITIES.md](CAPABILITIES.md) (خريطتك الذاتية المولّدة: ماذا تستطيع، وماذا تحتاج، وكيف تفكّر). داخل المستودع شغّل `python3 .claude/skills/kosif-superpowers/scripts/boot.py` ثم `python3 .claude/skills/kosif-superpowers/scripts/hub.py find "<المهمة>"`: يعطيك الأداة التي تشغّلها بأمر جاهز، والقدرات المناسبة، والدليل الذي تقرؤه.

**لأي تطبيق أو وكيل / for any app or agent:** خادم MCP للقراءة فقط `.claude/skills/kosif-superpowers/scripts/kosif_mcp.py` (يسجّله [.mcp.json](.mcp.json) داخل المستودع)، و[manifest.json](.claude/skills/kosif-superpowers/manifest.json) لكل الأدوات والعائلات والأدلة بصيغة JSON، و[AGENTS.md](AGENTS.md) لوكلاء البرمجة الآخرين، و[llms.txt](llms.txt) للنماذج.
**لـ Claude:** حين تفتح هذا المستودع، حمّل `.claude/skills/kosif-superpowers/SKILL.md` ونفّذ بروتوكول التشغيل فيه قبل أن تبدأ، ثم اقرأ `AGENTS.md` إن كان الطلب موشن جرافيك. الفحص الكامل: `python3 tools/validate.py` و`python3 -m unittest discover -s tests`.
**For Claude:** given only this repo's link, read [CAPABILITIES.md](CAPABILITIES.md) (generated self-model; also [llms.txt](llms.txt)); inside the repo run `scripts/boot.py`, then `scripts/hub.py find "<task>"` for the tool to run, the powers that apply and the guide to read. On entering this repo, load the superpowers SKILL.md first and run its power-up protocol; read AGENTS.md for motion work. Every branch is merged into `main`.


**الموقع:** https://kosif199022-jpg.github.io/kosif-tool/ · **الفهرس:** [STYLE_INDEX.md](STYLE_INDEX.md) · **الدلائل:** [playbooks/](playbooks/)

<div dir="rtl">

## ما هذا المستودع؟

مكتبة استايلات موشن جرافيك يقرؤها Claude Code كدليل إنتاج. كل استايل له:

- `styles/<id>/STYLE.json` — بيانات وصفية موثقة (المصدر، المبدع، النسبة، التاريخ، التقنيات المذكورة، الترتيب الشعبي).
- `styles/<id>/SKILL.md` — دليل تنفيذ أصلي من KOSIF: المرجع، التصنيفات، الدلائل، قواعد الحركة، وخطوات الإنتاج.
- `styles/<id>/BRIEF.md` — ملف إبداعي أصلي (عربي/إنجليزي): الفكرة، المشاهد المقترحة، قواعد الحركة بالأرقام، التقنية والمدة والصعوبة.

وفوق ذلك: دلائل تنفيذ لكل تصنيف في `playbooks/`، قوالب إنتاج في `templates/`، مشاريع بداية في `starters/`، وأدوات في `tools/`، وموقع ثابت يعمل على GitHub Pages من جذر المستودع.

## مهارة القدرات الخارقة لـ Claude

المجلد [`.claude/skills/kosif-superpowers/`](.claude/skills/kosif-superpowers/SKILL.md) مهارة تعرّف Claude بقدراته الحقيقية في كل جلسة: الأدوات والموصلات، والمكتبات التي يثبّتها بأمر واحد، وطرق التفكير والإبداع والتحقق، وكتالوج من 5,800+ قدرة في 10 مجالات (التفكير، الكتابة والعربية، الكود، البيانات، المستندات، البحث، التطبيقات، الصور والصوت، المنتج والمال، الموشن) لكل منها وصفة ودليل.

- **في Claude Code:** تُحمَّل تلقائيًا من هذا المستودع، أو انسخ المجلد إلى `~/.claude/skills/`.
- **في claude.ai:** `python3 .claude/skills/kosif-superpowers/scripts/package_skill.py` ثم ارفع ملف `.skill` الناتج.
- **ابدأ بـ:** `python3 .claude/skills/kosif-superpowers/scripts/boot.py` ثم `hub.py find "<طلبك>"` (أدوات + قدرات + أدلة)، و`hub.py doctor` لما يعمل على جهازك الآن. الخريطة الذهنية للقدرات: [capability-map.md](.claude/skills/kosif-superpowers/references/capability-map.md).

## الاستخدام السريع مع Claude Code

1. افتح [الموقع](https://kosif199022-jpg.github.io/kosif-tool/) واختر استايلًا (أو ابحث في `STYLE_INDEX.md`).
2. اضغط «انسخ طلب Claude» أو خصّص الطلب في المولّد (المادة، النسبة، المدة، التقنية، الهوية).
3. الصق الطلب في Claude Code مع المستودع وأرفق الصوت/الفيديو/النص.
4. يكتب Claude ملفي `STYLE.md` و`PLAN.md`، يبني الحركة، يعرض معاينة، ثم يرندر MP4 بعد موافقتك.

من الطرفية:

```bash
python3 tools/kosif.py search "سبورة"                 # بحث عربي/إنجليزي
python3 tools/kosif.py show pm-ror-fly-9950f1         # السجل + الملف الإبداعي + الدلائل
python3 tools/kosif.py prompt pm-ror-fly-9950f1 --aspect 9:16 --duration 20 --source "audio voice.mp3"
python3 tools/kosif.py scaffold pm-ror-fly-9950f1 ./my-film --starter html-canvas
node tools/render_html.cjs --in ./my-film/index.html --out ./my-film/film.mp4 --preview      # لوحة إطارات → my-film/film_preview.png
node tools/render_html.cjs --in ./my-film/index.html --out ./my-film/film.mp4 --audio voice.mp3
python3 tools/words_convert.py captions.srt ./my-film/words.json       # ترجمة → توقيتات كلمات
python3 tools/verify_video.py ./my-film/film.mp4 --aspect 9:16 --fps 30 --duration 20 --audio voice.mp3   # بوابة التسليم
```

## صيانة الفهرس

```bash
python3 tools/sync_catalog.py      # مزامنة مع مكتبة المصدر (بيانات وصفية وروابط فقط)
python3 tools/import_briefs.py DIR # استيراد ملفات إبداعية جديدة
python3 tools/build.py             # إعادة توليد SKILL.md وSTYLE_INDEX.md والفهارس وخريطة الموقع
python3 tools/validate.py          # فحص السلامة
npm test                           # اختبارات Node وPython
```

</div>

## English

A Claude-readable atlas of motion-graphics styles with a static website, original creative briefs, category playbooks, production templates, starter projects and a deterministic HTML-to-video renderer.

| Path | What it is |
|---|---|
| `index.html`, `web/` | The website (library, request generator, playbooks reader, guide). Arabic/English, RTL/LTR, dark/light. Served by GitHub Pages from the repo root. |
| `catalog/` | `styles.json` (all records, see `SCHEMA.md`), `briefs.json`, `playbooks.json`, `categories.json`, `meta.json`. |
| `styles/<id>/` | `STYLE.json`, `SKILL.md`, `BRIEF.md` per style. |
| `playbooks/` | Production playbooks per category plus Arabic typography, audio sync and render pipeline. |
| `templates/` | `claude_request.{ar,en}.txt` (single source of truth for generated requests), `STYLE.md`, `PLAN.md`, `TEST_REPORT.md`, `words.example.json`. |
| `starters/html-canvas/` | Dependency-free deterministic timeline film (Canvas + SVG + word-synced Arabic captions) exposing `window.__kosif.seek(t)`. |
| `starters/remotion/` | Minimal Remotion v4 project (title reveal, SVG chart, logo card, word-level captions). |
| `tools/` | `kosif.py` CLI, `render_html.cjs` (Playwright + ffmpeg), `words_convert.py` (SRT/VTT/Whisper → words.json), `verify_video.py` (delivery gate with loudness), `sync_catalog.py`, `import_briefs.py`, `build.py`, `validate.py`, `check_originality.py`. |
| `tests/` | Python `unittest` and Node `node:test` suites run by CI. |
| `.claude/skills/kosif-superpowers/` | Claude Code skill: a searchable catalog of 5,800+ powers in 10 domains with requirements, evidence badges and proofs, 90+ runnable tools behind one front door (`scripts/hub.py find`), a read-only MCP server (`scripts/kosif_mcp.py`) and a JSON manifest, a thinking engine (think.py), a capability graph, executable motion tools, a credited 125-repository tool map, a permissioned reference inspector and font matching. |
| `fonts/kosif-jumuah/` | KOSIF Jumuah, an OFL type family matched to the Friday-greeting reference (Amiri Arabic with stacked ligatures + Bodoni Moda figures), with the reproducible build script, a seek-driven demo and the match report. |

### Quick start

```bash
python3 tools/kosif.py search "recipe"
python3 tools/kosif.py prompt pm-ror-fly-9950f1 --lang en --aspect 1:1 --duration 30
python3 tools/kosif.py scaffold pm-ror-fly-9950f1 ./negroni --starter html-canvas
node tools/render_html.cjs --in ./negroni/index.html --out ./negroni/film.mp4 --fps 30
```

### Website

The site is plain static files at the repository root and needs no build step. `.github/workflows/pages.yml` deploys it with GitHub Actions on every push to `main`; alternatively set Pages to "Deploy from a branch" (main, `/`), both work. `.github/workflows/sync.yml` opens a weekly pull request when the source library changes, and `ci.yml` validates the catalog, derived files and tests.

## Attribution and source policy

- Third-party video, posters, prompts, voice and music are never rehosted. Links point to the owners' pages; creators are credited on every entry.
- `SKILL.md`, `BRIEF.md` and the playbooks are original KOSIF writing. Briefs are derived from an entry's title, categories and public description and were written without watching the videos, except those whose note says they were revised against frames sampled from the reference video; `tools/check_originality.py` guards against reused wording.
- An externally linked example is not a claim that the exact animation has been coded or validated here.
- Source terms: https://www.promptsmotion.com/terms · Contact for removals: see the source site.

## Related repositories

- https://github.com/motalim-ai/motion-starter-kit
- https://github.com/latent-spaces/brag
- https://github.com/oso95/scroll-world
- https://github.com/elayadesign/ai-design-skills
- https://github.com/midudev/mcp-higgsfield-landing
- https://github.com/heygen-com/hyperframes
- https://github.com/kosif199022-jpg/kosif-one
- https://github.com/kosif199022-jpg/fastify-motion-bro
- https://github.com/kosif199022-jpg/kosif-studio
- https://github.com/kosif199022-jpg/kosif-render-lab
- https://github.com/kosif199022-jpg/kosif-omni
- https://github.com/kosif199022-jpg/100-superskills

## KOSIF Superpowers × 100 Super Skills (114 مهارة)

تم ربط مكتبة [100-superskills](https://github.com/kosif199022-jpg/100-superskills) داخل KOSIF Superpowers منسوخة بالكامل داخل المستودع في `.claude/skills/kosif-superpowers/vendor/100-superskills` (682 ملفًا ببصمة SHA-256، من غير أي خطوة إضافية بعد الاستنساخ). ابحث عن المهارة المناسبة بـ `python3 .claude/skills/kosif-superpowers/scripts/superskills.py find "<طلبك>"`.
الفهرس والأوامر داخل [دليل دمج 114 مهارة](.claude/skills/kosif-superpowers/references/100-superskills-integration.md)؛ جرّب `python3 .claude/skills/kosif-superpowers/scripts/superskills_bridge.py doctor` لتمييز المتاح فعليًا عمّا يتطلب تجهيزًا.
