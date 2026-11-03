# أدوات المجال `discover` (31 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `ai-tool-discovery` — باحث القدرات ثنائي اللغة بلا اتصال / Offline bilingual capability finder

| الحقل | القيمة |
|---|---|
| المسار | `scripts/ai_tool_discovery.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** يرتّب قدرات كتالوج KOSIF لمهمة مكتوبة بالعربية أو الإنجليزية بمطابقة موزونة للحقول مع ترجيح الكلمات النادرة في فهرس الأطلس المحلي، ويعيد المعرّفات والكلمات المطابقة والحالة المعلنة والمتطلبات مع التنبيه إلى أنها لم يُتحقَّق منها تشغيليًا.

**What it does:** Ranks KOSIF catalog powers for an Arabic or English task using weighted field matching with corpus-rarity scoring over the local atlas index, and returns IDs, matched terms, claimed status and requirements with runtime_verified=false.

#### متى تُستدعى

- «ابحث عن قدرات لتحريك شخصيات في فيديو»
- «عايز أدوات رسم وسكتش، فيه إيه في الكتالوج؟»
- «Find KOSIF powers for blender 3d geometry»
- «Rank catalog capabilities for 'video animation motion' offline»

#### الأوامر

- **task (positional)**: Scores each power by name_en/name_ar (weight 6), tags (4), when (2) and summary (1) times a log rarity weight, with a few Arabic aliases (e.g. تحريك→animation, rig) and a coverage factor for explicit task words; prints the top N (--top must be 1–30) with score, matched_terms, claimed_catalog_status, proof_scope, requirements and runtime_verified=false.
  - `python3 scripts/ai_tool_discovery.py "تحريك شخصيات فيديو" --top 8`
- **--doctor**: Confirms the atlas index loads, then reports status index_available, the record count and network_requests=0.
  - `python3 scripts/ai_tool_discovery.py --doctor`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: Lexical rarity-weighted ranking over the prebuilt atlas index; it neither checks that the index is fresh nor that requirements are met on this host, and it runs nothing.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_ai_tool_discovery.py`
- مرجع: `.claude/skills/kosif-superpowers/references/taaft-rea-discovery-audit.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:ai-tool-discovery --evidence <ملف>`.

### `atlas-5000` — خريطة تغطية أطلس الـ5000 مهارة / Atlas-5000 coverage map

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_5000.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `software-investigation` |

**ما تفعله:** يقارن النواة الآمنة لأطلس KOSIF (5,116 مهارة بحكم READ_ONLY_OK وترخيص مفتوح وبلا علامات خطر) بكتالوج القدرات: التغطية لكل موضوع، والمواضيع الأكثر مهارات غير مستخرجة مع المرشحين التاليين، وبحث عربي وإنجليزي يبيّن أي قدرة تغطي كل مهارة.

**What it does:** Maps the 5,116-skill safe core of KOSIF Atlas (READ_ONLY_OK, permissive license, no risk flags) against the KOSIF catalog: per-theme coverage, the themes with the most undistilled skills and their next candidates, and a bilingual search that shows which power already covers each Atlas skill.

#### متى تُستدعى

- «ايه المهارات اللي في أطلس الـ5000 ولسه ما اتعلمتهاش؟»
- «دوّر في الأطلس على مهارات رسم ويبتون وشخصيات»
- «Which Atlas themes are least covered by KOSIF powers?»
- «Find Atlas skills for storyboard drawing and show which power covers them»

#### الأوامر

- **stats**: Prints the Atlas total, the safe-core size, and per theme how many safe skills a KOSIF power already cites (covered) with the coverage percentage.
  - `python3 scripts/atlas_5000.py stats --json`
- **gaps**: Ranks themes by safe skills no power cites yet and lists up to --per-theme candidates per theme (one per plugin, no duplicate descriptions).
  - `python3 scripts/atlas_5000.py gaps --top 8 --per-theme 3`
- **find**: Searches the safe core by name, theme and description with a few Arabic-to-English aliases; each hit lists covered_by power IDs. --uncovered keeps only skills not yet distilled.
  - `python3 scripts/atlas_5000.py find "storyboard character webtoon" --top 10 --json`
- **show**: Prints one Atlas skill's metadata, whether it is in the safe core and which powers cite it; an unknown id exits 2.
  - `python3 scripts/atlas_5000.py show 2425 --json`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: None needed: it only reads two local data files.
- الحدود: covered means a power's proof or source cites the Atlas folder, not that the skill was run or verified; search is keyword overlap on metadata, and Atlas themes come from a keyword taxonomy that can misfile a skill.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_atlas_5000.py`
- مرجع: `.claude/skills/kosif-superpowers/references/atlas-5000-mining-20261023.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-5000 --evidence <ملف>`.

### `atlas-capability-miner` — منقّب قدرات الأطلس من البيانات الوصفية / Atlas metadata capability miner

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_capability_miner.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `software-investigation` |

**ما تفعله:** يفهرس البيانات الوصفية لمهارات الأطلس الخارجية أو يستعلم عنها، مع مسار REA اختياري؛ وجود المصدر ليس دليل تشغيل.

**What it does:** Indexes or queries metadata of third-party Atlas skills with an opt-in REA path; source presence is not execution proof.

#### متى تُستدعى

- «Review documented Atlas or Blender capabilities»
- «Inspect relevant tool arguments before running»
- «طلّع القدرات المفيدة من بيانات مهارات الأطلس»
- «ابحث في فهرس الأطلس عن مهارات تناسب طلبي»

#### الأوامر

- **--help**: Show documented options; inspect inputs and authorization requirements before running any non-help action.
  - `python3 scripts/atlas_capability_miner.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: runs-external-programs
- الموافقة: Require the user's authorization before analyzing third-party installations, invoking REA or Blender, writing files, or performing any external actions. --help is informational.
- الحدود: Registration describes discovery; verify CLI and run targeted tests. Do not infer that Atlas entries are runnable or that Blender/Ghidra work without installed binaries.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_atlas_capability_miner.py`
- مرجع: `.claude/skills/kosif-superpowers/SKILL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-capability-miner --evidence <ملف>`.

### `atlas-ledger` — سجل الأطلس: حالة واحدة لكل مهارة / Atlas ledger: one status for every Atlas skill

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_ledger.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `atlas-code` |

**ما تفعله:** يعطي كل مهارة من مهارات أطلس KOSIF الـ14,793 حالة مراجعة واحدة: مغطاة (قدرة تستشهد بها)، أو نمط (نسخة مزوّد من منهج تملكه قدرة)، أو مكررة، أو مستبعدة (تحتاج مراجعة تثبيت أو رخصة copyleft أو علامات خطر)، أو معلّقة (آمنة وفريدة ولم يُقرر فيها بعد). يُبنى من فهرس الأطلس الوصفي وملفات القدرات وقواعد المراجعة، وإيصال REA لبصمات الأطلس كله في proofs/atlas-rea/.

**What it does:** Gives every one of the 14,793 KOSIF Atlas skills exactly one review status: covered (a power cites it), pattern (one vendor's instance of a method a power already holds), duplicate, excluded (needs install review, copyleft or risk-flagged) or pending (safe, unique and not yet decided). Built from the inert Atlas metadata index, the power files and the reviewed rules in data/atlas-ledger-decisions.json; REA's hash receipt for the whole Atlas is in proofs/atlas-rea/.

#### متى تُستدعى

- «كل مهارة في الأطلس حصل لها ايه؟ كام اتنقلت وكام اتسابت وليه؟»
- «ايه مهارات الأطلس الآمنة اللي لسه ما اتراجعتش في موضوع الأمان؟»
- «What happened to each Atlas skill: covered, duplicate, excluded or pending?»
- «List pending safe Atlas skills for the next transfer batch»

#### الأوامر

- **stats**: Counts per status, overall and per theme.
  - `python3 scripts/atlas_ledger.py stats --json`
- **show**: One Atlas skill's status, covering powers, reason and folder link; unknown exits 2.
  - `python3 scripts/atlas_ledger.py show 6802`
- **list**: Skills with one status, optionally one theme.
  - `python3 scripts/atlas_ledger.py list --status pending --theme security --top 20`
- **build**: Writes data/atlas_ledger.json.gz; --check exits 1 when it is stale.
  - `python3 scripts/atlas_ledger.py build`
- **self-test**: Synthetic index covering every status; prints ok or FAIL per check.
  - `python3 scripts/atlas_ledger.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- optional: rea (only to refresh proofs/atlas-rea/receipt.json, run separately)
- الأمان: read-only
- الموافقة: None needed.
- الحدود: A status is a review decision over metadata and SKILL.md text read as data, not an execution receipt; pattern means the method is held, while vendor endpoints and limits still live in the Atlas folder and must be re-checked against current vendor docs.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_atlas_ledger.py`
- مرجع: `.claude/skills/kosif-superpowers/references/atlas-ledger-20261023.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-ledger --evidence <ملف>`.

### `atlas-task-method-router` — موجّه مناهج الأطلس حسب المهمة / Atlas task method router

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_task_method_router.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `untested` |
| العائلات | `software-investigation` |

**ما تفعله:** يجد مناهج مرشحة من الأطلس مدعومة بالمصادر لمهمة ما دون تشغيل كودها.

**What it does:** Finds source-backed Atlas method candidates for a task without executing their code.

#### متى تُستدعى

- «Review documented Atlas or Blender capabilities»
- «Inspect relevant tool arguments before running»
- «إيه مناهج الأطلس المناسبة للمهمة دي؟»
- «وجّهني لمنهج من الأطلس يحل المشكلة دي»

#### الأوامر

- **--help**: Show documented options; inspect inputs and authorization requirements before running any non-help action.
  - `python3 scripts/atlas_task_method_router.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: Require the user's authorization before analyzing third-party installations, invoking REA or Blender, writing files, or performing any external actions. --help is informational.
- الحدود: Registration describes discovery; verify CLI and run targeted tests. Do not infer that Atlas entries are runnable or that Blender/Ghidra work without installed binaries.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/SKILL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-task-method-router --evidence <ملف>`.

### `black-dragon` — التنين الأسود — العقل المنسق لكل القدرات / Black Dragon — All-Capability Cognitive Orchestrator

| الحقل | القيمة |
|---|---|
| المسار | `scripts/black_dragon.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `untested` |
| العائلات | `agent-orchestration`, `self-discovery`, `qa-verification` |

**ما تفعله:** يخطط لكل المهارات والقدرات والأدوات المسجلة بدون استبعاد، ويوزع الأدوار والاعتماديات والتشغيل المتوازي، ويُظهر ما نُفذ بالدليل وما تعذر تنفيذه.

**What it does:** Plans EVERY registered skill, catalog power and tool, with relevance-ranked roles, exact inventory and explicit dependency-aware concurrent execution. Produces audit receipts and reports unexecuted items truthfully.

#### متى تُستدعى

- «استدعِ التنين الأسود وشغّل كل المهارات في المهمة»
- «شغّل كل قدرات سوبر باور بذكاء من غير استبعاد أي مهارة»
- «Use all KOSIF skills with dependency-aware intelligent parallel coordination»
- «Invoke Black Dragon and audit every registered capability»

#### الأوامر

- **inventory**: Count all registered skills, powers and tools without executing them.
  - `python3 scripts/black_dragon.py inventory`
- **plan**: Produce ranked all-entry plan with roles and dependency waves; skips no catalog entry.
  - `python3 scripts/black_dragon.py plan "اصنع مونتاج"`
- **run**: Record every entry, launch only explicitly reviewed adapters when enabled, produce SHA-256 evidence and blocked/failed counts.
  - `python3 scripts/black_dragon.py run "اصنع مونتاج" --job ../../../out/black-dragon/demo --workers 8`

#### المتطلبات والأمان

- binaries: python3
- الأمان: runs-external-programs
- الموافقة: Adapter execution requires user authorization and --execute-adapters. No automatic payment, upload, installation or production deployment.
- الحدود: A full catalog dispatch is not universal same-instant execution. Documentation-only powers or unavailable adapters are blocked, not credited. Plans are heuristic and do not establish cinematic quality.

#### الاختبارات والأدلة

- `tests/test_black_dragon.py`
- مرجع: `docs/BLACK_DRAGON_ALL_CAPABILITIES.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:black-dragon --evidence <ملف>`.

### `boot` — إحاطة بدء الجلسة / Session boot briefing

| الحقل | القيمة |
|---|---|
| المسار | `scripts/boot.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** يطبع إحاطة ذاتية سريعة لـ Claude تشمل معلومات الجهاز، وأعداد القدرات في كل مجال، وعدد القدرات التي تتوفر كل متطلباتها المسجّلة، والتثبيتات التي تفتح أكبر عدد من القدرات، وعدد الأدوات القابلة للتشغيل، والأوامر التالية المقترحة (hub.py وthink.py وrequirements.py). ويستطيع أيضًا إعادة توليد الملفين CAPABILITIES.md وllms.txt في جذر المستودع أو فحص تقادمهما.

**What it does:** Prints a short self-briefing for Claude: machine facts, catalog counts per domain, how many powers have every listed requirement present, the installs that unlock the most powers, the runnable-tool count and the next commands to run (hub.py, think.py, requirements.py). It can also regenerate or check the repo-root CAPABILITIES.md and llms.txt.

#### متى تُستدعى

- «ابدأ الجلسة وقولي تقدر تعمل ايه هنا»
- «وش القدرات الجاهزة على هذا الجهاز الحين؟»
- «Boot the KOSIF skill and brief yourself first»
- «Is CAPABILITIES.md stale after my catalog change?»
- «Regenerate llms.txt and CAPABILITIES.md for the repo link»

#### الأوامر

- **live**: Text briefing: machine (OS, python, node/ffmpeg/GPU), catalog counts and status, ready-now count, a per-domain table, the top 8 installs to unlock more, the runnable-tool count from data/tools.json, and next steps (hub.py find/tool, think.py ladder, requirements.py plan)
  - `python3 scripts/boot.py`
- **json**: The same briefing as JSON: machine, catalog, ready_now, by_domain, requirements, top_unlocks (the runnable-tool count and next steps are text-only)
  - `python3 scripts/boot.py --json`
- **static-check**: Read-only: prints 'stale: <file>' and exits 1 if CAPABILITIES.md or llms.txt at the repo root differs from what the current catalog and boot.py would generate; exits 0 when both are current
  - `python3 scripts/boot.py --static --check`
- **static-write**: Regenerates and overwrites CAPABILITIES.md and llms.txt at the repo root (numbers, tools-by-area table from data/tools.json, families, biggest unlocks, guide and raw links)
  - `python3 scripts/boot.py --static --write`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: --static --write overwrites CAPABILITIES.md and llms.txt at the repo root; run it only as a maintainer after a catalog change
- الحدود: 'Ready now' means only that every listed requirement was detected, and powers with no listed requirement (including documented, seen and idea records) also count, so it is not proof that any power works.

#### الاختبارات والأدلة

- `tests/test_boot.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`
- مرجع: `README.md`
- مرجع: `CLAUDE.md`
- مرجع: `CAPABILITIES.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:boot --evidence <ملف>`.

### `capability-atlas` — أطلس القدرات للبحث والتخطيط / Capability Atlas search and planner

| الحقل | القيمة |
|---|---|
| المسار | `scripts/capability_atlas.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `planning-execution` |

**ما تفعله:** يبحث بالعربية أو الإنجليزية في كتالوج KOSIF الذي يضم 4,751 قدرة، ويخطط للمهمة باختيار معرّفات القدرات ومهارات العمل والمسارات المناسبة مع فحص المتطلبات محليًا، ويعيد بناء فهرس الأطلس ودليله.

**What it does:** Searches the 4,751-power KOSIF catalog in Arabic or English, plans a task by picking capability IDs, process skills, routes and local requirement checks, and rebuilds the atlas index and its guide.

#### متى تُستدعى

- «ايه القدرات اللي تنفع لمهمة تايبوغرافي عربي متحرك؟»
- «خطط لي بناء تطبيق محاسبة آمن من كتالوج القدرات»
- «Which KOSIF powers match 'Arabic kinetic typography'?»
- «Show me the full catalog record for DOC-05»
- «Is the capability atlas index stale after I edited data/powers?»
- «وش القدرات المتوفرة في مجال الموشن؟»

#### الأوامر

- **stats**: Prints catalog totals by domain, family and status, the route count, and index_fresh (whether the stored index matches the SHA-256 of data/powers/*.json and data/capability_routes.json).
  - `python3 scripts/capability_atlas.py stats --json`
- **doctor**: Reports ready or stale_index, the number of powers and routes, and no_external_calls=true. It exits 0 even when the index is stale.
  - `python3 scripts/capability_atlas.py doctor --json`
- **search**: Ranks catalog powers by keyword hits in name (weight 7), family/domain (4), tags (3) and summary/when (1), with a few Arabic-to-English aliases (e.g. محاسبة→accounting) and a small bonus for proven/ready status. --top is clamped to 1–50; --domain filters by domain such as motion, code or mind.
  - `python3 scripts/capability_atlas.py search "Arabic kinetic typography" --top 10 --domain motion --json`
- **plan**: Returns the top capabilities with requirement states (detected, not_detected or unverified, via PATH or Python import spec), up to 4 matching routes from data/capability_routes.json, the obra process skills chosen by superpowers_unified.plan, and a planning-only notice. --top is clamped to 1–30.
  - `python3 scripts/capability_atlas.py plan "Build a secure accounting app" --top 7 --json`
- **show**: Prints the full source record for one capability ID (case-insensitive) with requirement checks. An unknown ID prints a plain-text error to stderr and exits with code 2.
  - `python3 scripts/capability_atlas.py show DOC-05 --json`
- **build**: Regenerates data/capability_atlas_index.json and references/capability-atlas.md from data/powers/*.json and data/capability_routes.json, and prints the catalog totals.
  - `python3 scripts/capability_atlas.py build`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: build overwrites the tracked files data/capability_atlas_index.json and references/capability-atlas.md, so run it only after catalog edits. The other commands are read-only.
- الحدود: Ranks by keyword overlap with catalog text and checks requirements only by PATH or import-spec lookup (pip requirements are looked up by distribution name, so installed Pillow or OpenCV show as not_detected); it never runs or verifies any capability.

#### الاختبارات والأدلة

- `tests/test_capability_atlas.py`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-atlas.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:capability-atlas --evidence <ملف>`.

### `capability-graph` — باني خريطة القدرات المترابطة / Capability Graph Builder

| الحقل | القيمة |
|---|---|
| المسار | `scripts/capability_graph.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `knowledge-graph`, `self-discovery`, `code-engineering` |

**ما تفعله:** يبني خريطة واحدة مترابطة للمهارة: الجذر ← المجالات ← العائلات ← المستلزمات التي تحتاجها، والسكربتات التي تنفّذها، والاختبارات التي تذكر تلك السكربتات. تأتي روابط الكود من تحليل محلي لعبارات الاستيراد عبر شجرة الصياغة المجرّدة (AST)، مدموجًا مع لقطة Graphify المحفوظة في المستودع. تُكتب الخريطة في data/capability_graph.json مع صفحة HTML قابلة للبحث تعمل دون اتصال، وتجيب الأداة عن استعلامات الإحصاء والعُقد المجاورة.

**What it does:** Builds one connected graph of the skill: root → domains → families → the requirements they need, the scripts that run them, and the tests that mention those scripts. Code edges come from a local AST import pass merged with the committed Graphify snapshot. The graph is written as data/capability_graph.json plus an offline, searchable HTML page, and the tool answers stats and neighbour queries on it.

#### متى تُستدعى

- «ورّيني خريطة القدرات المترابطة للمهارة»
- «وش العائلات اللي تحتاج ffmpeg؟»
- «ابني الخريطة المترابطة من جديد بعد ما ضفت سكربت»
- «show me the capability graph of the skill»
- «which scripts run the thinking-core family and which tests cover them?»
- «rebuild capability_graph.json and check it is current»

#### الأوامر

- **build**: Rewrites the tracked files data/capability_graph.json and references/capability-graph.html, then prints node counts per kind, the edge count and how many Graphify edges were confirmed. Running the script with no arguments does the same.
  - `python3 scripts/capability_graph.py build`
- **build --check**: Writes nothing. Exits 1 and names the stale file(s) if a fresh build would differ from the committed ones; otherwise prints 'capability graph up to date'.
  - `python3 scripts/capability_graph.py build --check`
- **build --out-dir**: Writes capability_graph.json and capability-graph.html into the given folder instead of the tracked locations.
  - `python3 scripts/capability_graph.py build --out-dir ./out/`
- **stats**: Prints node counts by kind and edge counts by relation (Python Counter reprs), read from the committed data/capability_graph.json.
  - `python3 scripts/capability_graph.py stats`
- **path**: Prints up to 3 nodes whose id contains the key, or whose family ID prefix equals it, with their incoming and outgoing edges (has, needs, runs, imports, tested_by). Keys can be a family stem, a requirement such as ffmpeg, or a script such as scripts/powers.py. Exits 1 with 'no node' when nothing matches.
  - `python3 scripts/capability_graph.py path thinking-core`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: build (and a bare run with no arguments) overwrites the tracked files data/capability_graph.json and references/capability-graph.html; use build --check or build --out-dir <folder> to preview. --help and a mistyped flag only print usage.
- الحدود: Edges are inferred from text mentions (script paths in how/proof fields, file names inside tests) and import statements, so 'tested_by' means a test names the script, not that it passed; stats and path read the committed JSON, which may be stale.

#### الاختبارات والأدلة

- `tests/test_capability_graph.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-map.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:capability-graph --evidence <ملف>`.

### `capability-runtime-router` — موجّه القدرات التنفيذية / Capability runtime router

| الحقل | القيمة |
|---|---|
| المسار | `scripts/capability_runtime_router.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `planning-execution`, `security-safety` |

**ما تفعله:** يطابق مهمة مكتوبة بالعربية أو الإنجليزية مع مسارات KOSIF الاثنين والعشرين في data/capability_routes.json (منها 17 مسارًا لها سكربت محلي و5 خارجية)، ويعيد لكل مسار أمر التشغيل والأدوات الموجودة والناقصة والأذونات المطلوبة التي لم تُمنح بعد، مع حالة لا تدّعي أن شيئًا نُفّذ.

**What it does:** Matches an Arabic or English task to the 22 KOSIF routes in data/capability_routes.json (17 backed by a local script, 5 external) and returns, for each one, the runbook command, which binaries are present or missing, the permissions it needs that have not been granted, and a status that never claims execution.

#### متى تُستدعى

- «حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي، أي سكربت أشغّل؟»
- «عايز أقلد إيقاع مونتاج فيديو بكاتانا، إيه الأداة المناسبة؟»
- «Which KOSIF script should I run to analyze song energy?»
- «Check prerequisites for every executable route on this machine»
- «Inspect the reference-edit-remix route and its permissions»

#### الأوامر

- **--task**: Scores route aliases against the task (1–500 characters): a multi-word alias found as a phrase scores 12, a single-word alias equal to the whole task 8, any other alias whose words all appear 2. Returns up to --limit choices (1–20), each with its runbook, status, present and missing binaries, and required permissions.
  - `python3 scripts/capability_runtime_router.py --task "حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي" --limit 5 --json`
- **--id**: Assesses one route by its exact ID. An unknown ID prints a JSON error to stderr and exits with code 2.
  - `python3 scripts/capability_runtime_router.py --id reference-edit-remix --json`
- **--doctor**: Assesses all 22 routes for source-file presence and missing binaries on PATH.
  - `python3 scripts/capability_runtime_router.py --doctor --json`
- **--list**: Lists the ID and title of every route.
  - `python3 scripts/capability_runtime_router.py --list --json`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: Matches only against hand-written aliases for 22 routes and checks binaries on PATH; it never runs a runbook, never verifies permissions and never proves that a route works.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_capability_runtime_router.py`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-operating-manual.md`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-visual-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:capability-runtime-router --evidence <ملف>`.

### `fusionforge` — FusionForge v2 لوصفات الـWorkflow المركبة داخل المشروع / FusionForge v2 project-scoped composite workflow recipes

| الحقل | القيمة |
|---|---|
| المسار | `scripts/fusionforge.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `agent-orchestration`, `planning-execution` |

**ما تفعله:** يحوّل تقرير USIP (والمرتِّب الوحيد هو skill_intelligence) إلى وصفة مرشحة داخل المشروع: عُقد Workflow لكل مرحلة تحمل قدرات الكتالوج ببصمة ذراتها، وأنواع المدخلات والمخرجات، ومرجع المنفّذ، وحواف التسليم، مع الخطط A وB وC من التقرير نفسه. ثم يسجّل الخطة المعتمدة، وسجل تنفيذ لكل عقدة ببصمات الأدلة، وكل تغيير حالة عبر آلة حالات مُلزمة (candidate ثم planned ثم tested ثم verified أو failed) لها بوابة تحقق تفحص السجلات؛ ويجري validate الفحوص V01–V12، وترتّب lessons وreuse واستدعاءُ propose وصفاتِ المشروع نفسه السابقة. والبطاقات والحزم المنقّحة تنقل الوصفات إلى جلسة أخرى. يكتب فقط في out/fusionforge/<project>/، ولا ينفّذ قدرة ولا يثبّت شيئًا ولا ينشر ولا يعدّل الكتالوج.

**What it does:** Turns the USIP brief (skill_intelligence is the single ranker) into a project-scoped candidate recipe: typed workflow nodes per stage holding catalog superpowers fingerprinted by their atom IDs, input/output artifact kinds, an executor reference and handoff edges, with plans A/B/C taken from the brief. It then records the approved plan, per-node traces with hashed evidence and every status change through an enforced state machine (candidate, planned, tested, then verified or failed) whose verified gate checks the records; validate runs checks V01-V12, and lessons, reuse and propose's recall rank the same project's earlier recipes. Cards and redacted bundles carry recipes to another session. Writes only under out/fusionforge/<project>/; it never executes a power, installs, publishes or edits the catalog.

#### متى تُستدعى

- «اعمل وصفة توليف مهارات للمهمة دي وسجّل خطوات التنفيذ»
- «ابتكر workflow مركب من مهارات متعددة واحفظه للمشروع»
- «رتّب وصفات المشروع السابقة لهدف جديد وقل لي أي تجربة فاشلة أتجنبها»
- «Compose several superpowers into a reusable workflow recipe for this project»
- «Record the evidence for each step of the composite workflow I just ran»
- «Export this project's FusionForge recipes so the next cloud session can import them»

#### الأوامر

- **propose**: Builds a candidate v2 recipe from the brief (without --from-brief it runs the brief in process; the brief is saved beside the recipe): typed nodes and edges for plans A/B/C, recall of this project's earlier recipes and similar-unverified links. Needs a complete coverage receipt; NO_MATCH exits 3 with a --terms hint. Also --terms, --max-capabilities 1-60 (default 24) and --id.
  - `python3 scripts/fusionforge.py propose "مونتاج ريلز بترجمة عربية" --project demo_project --from-brief out/20261021-reel/brief.json`
- **reuse**: Read-only: ranks this project's earlier recipes by sim x strength x recency x freshness (sim_basis says goal text or goal + capabilities) and lists failed ones under avoid with their lessons. --top N, --no-brief, --terms.
  - `python3 scripts/fusionforge.py reuse "مونتاج ريلز بترجمة عربية" --project demo_project --from-brief out/20261021-reel/brief.json`
- **validate**: Read-only checks V01-V12: schema, status log, handoff kinds, a final verify, executors, evidence present and unchanged, secrets, self-evidence, verified without a run, catalog drift and unknown capabilities (the last two warnings). Exit 4 on any error.
  - `python3 scripts/fusionforge.py validate --project demo_project --id FUSE-20261021-0123456789`
- **choose**: Records the user's plan (A, B, C, or D with --nodes N01,N02) and moves candidate to planned; needs a clean validate and resets every node to pending. Node results count only after this.
  - `python3 scripts/fusionforge.py choose --project demo_project --id FUSE-20261021-0123456789 --plan B --why "balanced quality for a 30-second reel"`
- **trace**: Appends one executed step and updates the node's status (skipped needs --observed; failed can carry --error-class); records tool substitutions; refuses credentials, unknown capability IDs and final recipes. Also --input, --output, --capabilities.
  - `python3 scripts/fusionforge.py trace --project demo_project --id FUSE-20261021-0123456789 --stage verify --node N06 --action "Ran verify_video.py on the render" --result passed --tool tool:verify-video --observed "1080x1920, 30 fps, -14.1 LUFS" --evidence out/20261021-reel/qa.json`
- **record**: Enforced transitions with a status log: tested needs evidence and at least one trace with a result; failed needs evidence and --note; planned is set only by choose (USE_CHOOSE).
  - `python3 scripts/fusionforge.py record --project demo_project --id FUSE-20261021-0123456789 --status tested --evidence out/20261021-reel/qa.json`
- **record --status verified**: The verified gate: tested state, --qa-pass, every node of the chosen plan passed or skipped, a verify node passed with local evidence, evidence unlike any failure evidence of the project and not already used to verify another recipe, and a clean validate. --baseline FILE keeps the comparison file (stored, not compared).
  - `python3 scripts/fusionforge.py record --project demo_project --id FUSE-20261021-0123456789 --status verified --evidence out/20261021-reel/final-qa.json --qa-pass`
- **lessons**: Rebuilds <project>/lessons.json from every recipe's traces: WORKED, FAILED, REPLACED, HANDOFF and RECIPE_FAILED, with per-executor counts (assumed executors counted apart).
  - `python3 scripts/fusionforge.py lessons --project demo_project`
- **fork**: New candidate from any recipe (verified and failed are final) with statuses reset and forked_from kept; --new-id sets its ID.
  - `python3 scripts/fusionforge.py fork --project demo_project --id FUSE-20261021-0123456789`
- **set-graph**: Replaces a candidate's nodes, edges and plans after checking every field and handoff kind (GRAPH_INVALID otherwise).
  - `python3 scripts/fusionforge.py set-graph --project demo_project --id FUSE-20261021-0123456789 --file out/20261021-reel/graph.json`
- **bind**: Sets a node's executor on a candidate or planned recipe: tool:<tools.json id>, bin:<name>, mcp:<server/tool>, method:<atom id> or human.
  - `python3 scripts/fusionforge.py bind --project demo_project --id FUSE-20261021-0123456789 --node N03 --executor tool:montage-pro`
- **card**: Writes <project>/cards/<id>.md (or --out FILE.md): a Markdown card with an embedded kosif.fusionforge.card.v2 JSON block, no absolute paths, evidence by sha256, for claude.ai without a shell.
  - `python3 scripts/fusionforge.py card --project demo_project --id FUSE-20261021-0123456789`
- **import-card**: New candidate from a card (status forced to candidate, provenance card); malformed cards stop with CARD_INVALID.
  - `python3 scripts/fusionforge.py import-card out/fusionforge/demo_project/cards/FUSE-20261021-0123456789.md --project other_project`
- **export**: Writes a redacted kosif.fusionforge.bundle.v2 (recipes + lessons) to <project>/exports/<project>-<YYYYMMDD>.json (or --out FILE.json) for opt-in persistence; never committed. --include-candidates adds unfinished recipes.
  - `python3 scripts/fusionforge.py export --project demo_project`
- **import**: Imports a bundle of the same project; statuses kept with imported: true; evidence not on this machine is a warning and weighs x0.8 in reuse; verified and promote need a new local verify run.
  - `python3 scripts/fusionforge.py import out/fusionforge/demo_project/exports/demo_project-20261021.json --project demo_project`
- **migrate**: Converts v1 recipes to v2 with byte-identical backups under <project>/legacy/; a v1 verified recipe with no trace is flagged legacy_unproven (x0.3 in reuse, never promoted).
  - `python3 scripts/fusionforge.py migrate --project demo_project`
- **promote**: Writes <project>/promotions/<id>.proposal.json in state pending_human for a verified recipe proved on this machine; never edits the catalog.
  - `python3 scripts/fusionforge.py promote --project demo_project --id FUSE-20261021-0123456789`
- **show**: Read-only: one recipe (a malformed record gets a short summary instead of a crash).
  - `python3 scripts/fusionforge.py show --project demo_project --id FUSE-20261021-0123456789 --json`
- **catalog**: Read-only listing of the project's recipes by status; invalid files are listed, never fatal; creates no folders.
  - `python3 scripts/fusionforge.py catalog --project demo_project`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only under the FusionForge root (out/fusionforge/<project>/, or --root / $KOSIF_FUSIONFORGE_ROOT); evidence files are read, hashed and copied there, never uploaded; nothing is committed, published or sent.
- الحدود: It never executes a power or tool: 'verified' means the caller's own QA passed this engine's gate on the records (states, traces, evidence hashes), not that the engine judged the work, and --baseline is stored but not compared. 'Learning' is lessons and rankings computed from the same project's recorded traces: nothing is learned across projects, no model is trained and nothing is swapped automatically. Records are local files under out/fusionforge/ (git-ignored): a new machine or a new cloud container starts empty unless the user exports a bundle or card and imports it there. Node I/O contracts are drafts (default_unconfirmed) until set-graph replaces them, the picks are only as good as the brief, and project isolation is the project folder name.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_fusionforge.py`
- `.claude/skills/kosif-superpowers/evals/test_usip_shadow.py`
- مرجع: `.claude/skills/kosif-superpowers/PROTOCOL.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A4-fusionforge-composition.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:fusionforge --evidence <ملف>`.

### `fusionforge-hub-runner` — جسر تنفيذ وصفات FusionForge عبر Hub / FusionForge to Hub execution bridge

| الحقل | القيمة |
|---|---|
| المسار | `scripts/fusionforge_hub_runner.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `agent-orchestration`, `planning-execution` |

**ما تفعله:** يشغّل عُقد وصفة FusionForge v2 اختار المستخدم خطتها: يرتبها حسب الحواف، ويشغّل كل عقدة tool: عبر hub.py run، ويمرّر ملفات المخرجات المعلنة للعقد التالية ويفحصها (جديدة وغير فارغة وJSON صالح)، ويسجّل كل عقدة بـfusionforge.py trace، ويتوقف عند أول فشل أو حجب، ويعزل ملفات العقدة الفاشلة، ويستأنف بعد العقد المسجلة ناجحة. يكتب إيصال JSON مُبصَّمًا؛ والوضع الافتراضي تجربة بلا تشغيل.

**What it does:** Runs the nodes of a FusionForge v2 recipe whose plan the user already chose: orders them by their edges, runs each tool: node with hub.py run, passes declared output files to later nodes and checks them (new, non-empty, valid JSON), records every node with fusionforge.py trace, stops at the first failure or blocked node, quarantines a failed node's files and resumes after nodes the recipe already shows as passed. Writes a hashed JSON receipt; dry run by default.

#### متى تُستدعى

- «شغّل خطة FusionForge اللي اخترتها بأدوات Hub وسجّل كل خطوة»
- «كمّل تنفيذ الوصفة من آخر عقدة نجحت بعد ما خلصت الخطوة اليدوية»
- «Run the chosen FusionForge plan through the Hub tools and trace every node»
- «Dry-run a planned recipe to see which nodes are blocked and why»

#### الأوامر

- **dry run**: Checks the recipe (status planned, plan unchanged, no cycle), the plan file (args, inputs, outputs, {N.name} references), hub.py doctor readiness and approvals; launches nothing. Exit 0 ready, 2 blocked.
  - `python3 scripts/fusionforge_hub_runner.py --recipe out/fusionforge/demo_project/recipes/FUSE-20261030-0123456789.json --plan-file out/job/io.json --report out/job/bridge-dry.json`
- **execute**: Runs the plan's tool: nodes in edge order with hub.py run, checks each node's declared outputs, traces every node with fusionforge.py (a trace that fails fails the node), stops at the first FAIL or BLOCKED. --allow-network / --allow-external / --allow-consent only after the user's explicit approval; --fusionforge-root, --timeout. Exit 0 executed, 1 failed, 2 blocked.
  - `python3 scripts/fusionforge_hub_runner.py --recipe out/fusionforge/demo_project/recipes/FUSE-20261030-0123456789.json --plan-file out/job/io.json --report out/job/bridge-run1.json --execute`

#### المتطلبات والأمان

- الأمان: runs-external-programs
- الموافقة: With --execute it runs the recipe's Hub tools: confirm the user chose the plan, and pass --allow-network, --allow-external or --allow-consent only after the user explicitly approved those steps.
- الحدود: EXECUTED means every selected command exited 0 and its declared files exist, are new, non-empty and parse as JSON when .json; that is not QA of the content, and the bridge never records tested or verified. method:/human nodes are manual (trace them, then rerun), bin:/mcp: executors are not run, and declared outputs must not exist before a node runs.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_fusionforge_hub_runner.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A4-fusionforge-composition.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:fusionforge-hub-runner --evidence <ملف>`.

### `fusionforge-shared` — ذاكرة FusionForge المشتركة بوصفات مهارات معزولة / FusionForge Shared Memory: reviewed cross-project skill structures

| الحقل | القيمة |
|---|---|
| المسار | `scripts/fusionforge_shared.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `untested` |
| العائلات | `self-discovery`, `planning-execution` |

**ما تفعله:** يفحص وصفات FusionForge v2 المُثبتة محليًا، ويشترط أدلة اختبار مستقلة عبر مشاريع مختلفة ثم مراجعة الخصوصية والأمان وتعارض الكتالوج والتفوق على خط الأساس قبل حفظ مخطط هيكلي مجرد؛ لا ينقل أسماء الشركات أو الملفات أو الأسرار.

**What it does:** Audits verified project-private FusionForge v2 promotion proposals; counts independent QA proofs across distinct projects, requires separate human privacy/security/collision and baseline-improvement review before exporting only allowlisted structural skill graphs. Never exports client objectives, transcripts, evidence, secrets or project names.

#### متى تُستدعى

- «استدعِ توليفة مهارات مشتركة آمنة متحققة من مشاريع سابقة»
- «افحص هل يمكن ترقية وصفة FusionForge بين مشاريع مستقلة»
- «Audit cross-project workflow promotion with three independent QA proofs»

#### الأوامر

- **audit**: Read-only: examines local independent verified promotion proposals and prints eligibility tiers; does not approve.
  - `python3 scripts/fusionforge_shared.py audit`
- **recall**: Read-only: returns only explicitly approved, allowlisted structural graphs for the named output kind.
  - `python3 scripts/fusionforge_shared.py recall --kind video`
- **review-template**: Prints the independent privacy/security/QA and baseline comparison review template without approving.
  - `python3 scripts/fusionforge_shared.py review-template --signature "$SIG"`
- **approve**: Writes a sanitized graph into the project-local shared registry only after independent test, review and security gates.
  - `python3 scripts/fusionforge_shared.py approve --signature "$SIG"`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Approval command requires explicit authorized human review and writes only sanitized generic graphs into the local shared registry.
- الحدود: Does not execute methods or prove human review by itself. 3 distinct reviewed projects and quality improvement required before shared approval; paths remain local and unshared.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_fusionforge_shared.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A10-self-evolution.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:fusionforge-shared --evidence <ملف>`.

### `hub` — بوابة KOSIF الموحّدة / KOSIF hub (front door)

| الحقل | القيمة |
|---|---|
| المسار | `scripts/hub.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `agent-orchestration` |

**ما تفعله:** سؤال واحد يعطي كل ما يلزم: الأدوات القابلة للتشغيل للمهمة بأمر جاهز ومعرفة هل يملك الجهاز مستلزماتها، والقدرات المناسبة من الكتالوج، والأدلة، والأساليب المرجعية لطلبات الموشن.

**What it does:** One question in, everything relevant out: the runnable tools for a task (with a copy-paste command and whether this machine has their requirements), the catalog powers, the guides and, for motion work, reference styles.

#### متى تُستدعى

- «ابدأ أي مهمة: ايش الأداة اللي أشغّلها؟»
- «قدراتك في المونتاج والموشن ايه؟»
- «which KOSIF tool should I run for this task?»
- «what can run on this machine right now?»
- «show me the exact commands for the 3D renderer»

#### الأوامر

- **find**: rank tools to run, catalog powers, guides and styles for a task (Arabic or English); --json for apps
  - `python3 scripts/hub.py find "اعمل فيديو موشن عربي متزامن مع صوتي"`
- **tool**: one tool card: when to use it, every command, inputs/outputs, requirements present or missing here, safety, consent, tests, guides
  - `python3 scripts/hub.py tool native-3d`
- **list**: every tool grouped by area
  - `python3 scripts/hub.py list --area 3d`
- **areas**: the 12 areas and their tool ids
  - `python3 scripts/hub.py areas`
- **doctor**: which tools can run on this machine now and which installs unlock the most
  - `python3 scripts/hub.py doctor`
- **power**: one catalog record (same data as powers.py show)
  - `python3 scripts/hub.py power 3D-01`
- **docs**: list or search the reference guides
  - `python3 scripts/hub.py docs blender`
- **run**: run a tool by id (arguments after --); tools that need consent or touch the network or external programs require --yes, except a plain --help
  - `python3 scripts/hub.py run native-3d doctor`
- **build**: regenerate (or check) manifest.json, references/INDEX.md and the generated tool tables
  - `python3 scripts/hub.py build --check`
- **mcp-config**: print the claude mcp add command and JSON config for the catalog MCP server on this OS
  - `python3 scripts/hub.py mcp-config`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: —
- الحدود: Ranks by keywords, registry metadata and catalog families; a high score means relevant, not proven to work for this exact request — open the tool card and run its doctor first.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_hub.py`
- مرجع: `.claude/skills/kosif-superpowers/references/INDEX.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:hub --evidence <ملف>`.

### `kosif-groups` — خريطة المجموعات مع القدرات الخارقة والسكربتات وخطط التثبيت / Group map with superpowers, scripts and install plans

| الحقل | القيمة |
|---|---|
| المسار | `scripts/kosif_hubs.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** لكل مجموعة من المجموعات الخمس عشرة: قدراتها الخارقة مرتبة بالجاهزية، والسكربتات، وأمر البداية، والمجموعات المرتبطة، وخطة تثبيت تفصل pip/npm عن أدوات النظام والمفاتيح.

**What it does:** For each of the 15 smart groups lists its fused superpowers ordered by readiness, entry scripts, a start command, linked groups and a per-group install plan that separates pip/npm lines (run with --apply) from system tools and keys that need the user's approval.

#### متى تُستدعى

- «ثبّت كل متطلبات مجموعة الموشن»
- «Route this task to a group and show the install plan»

#### الأوامر

- **map**: The 15 groups with counts and ready-now.
  - `python3 scripts/kosif_hubs.py`
- **route**: Best groups, superpowers, scripts and install plan for a task.
  - `python3 scripts/kosif_hubs.py route "ارسم شخصية وحركها"`
- **install**: Install plan for a group; --apply runs only plain pip/npm lines.
  - `python3 scripts/kosif_hubs.py install motion`

#### المتطلبات والأمان

- optional: bin:pip, bin:npm
- الأمان: runs-external-programs
- الموافقة: install --apply runs pip/npm install lines: confirm first; never system packages or keys
- الحدود: Presence detection is not quality; a proven badge still needs a real run.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_kosif_hubs.py`
- مرجع: `.claude/skills/kosif-superpowers/references/hubs.md`
- مرجع: `.claude/skills/kosif-superpowers/START.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:kosif-groups --evidence <ملف>`.

### `kosif-mcp` — خادم MCP لكتالوج KOSIF / KOSIF catalog MCP server

| الحقل | القيمة |
|---|---|
| المسار | `scripts/kosif_mcp.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `agent-orchestration` |

**ما تفعله:** خادم MCP للقراءة فقط عبر stdio يتيح لأي عميل MCP (Claude Code وClaude Desktop وCursor وغيرها) طرح أسئلة hub.py نفسها: البحث، بطاقات الأدوات، الجاهزية، القدرات وعائلاتها، والأدلة.

**What it does:** Read-only stdio MCP server that lets any MCP client (Claude Code, Claude Desktop, Cursor …) ask the same questions as hub.py: find, tool cards, doctor, power search and records, families and guides.

#### متى تُستدعى

- «اربط Claude Desktop بكتالوج قدرات KOSIF»
- «expose the KOSIF catalog to Cursor or another MCP client»
- «an agent without a shell needs to discover KOSIF tools»
- «خلي أي تطبيق يكتشف أدوات المهارة»

#### الأوامر

- **serve**: serve MCP over stdio (newline-delimited JSON-RPC 2.0); tools kosif_find, kosif_tool, kosif_list_tools, kosif_doctor, kosif_search_powers, kosif_power, kosif_family, kosif_guides, kosif_read_guide
  - `python3 scripts/kosif_mcp.py`
- **selftest**: run a full in-process MCP session (handshake, every tool once, path-escape refusal, unknown method) and print PASS/FAIL
  - `python3 scripts/kosif_mcp.py --selftest`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Answers questions only: it never runs a tool, installs, writes files or touches the network; query text is capped at 2,000 characters and list sizes at 50. For bounded file access use kosif-remote-commander.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_hub.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/local-computer.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:kosif-mcp --evidence <ملف>`.

### `local-first` — مدخل محلي بلا استنساخ / Local-first no-clone entry

| الحقل | القيمة |
|---|---|
| المسار | `scripts/local_first.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** مدخل يعمل محليًا بلا شبكة وبلا استنساخ للمستودع. يفحص الأمر doctor المهارة المثبتة ويعرض عدد سجلات الكتالوج حسب الحالة ووجود أطلس الأساليب الكامل، ويحيل الأمر search البحث إلى كتالوج القدرات المحلي أو إلى أطلس الأساليب عند توفر نسخة كاملة من المستودع.

**What it does:** A no-network, no-clone entry point. `doctor` checks the installed skill and reports catalog record counts by status and whether the full style atlas is present; `search` forwards to the local power catalog or, inside a full kosif-tool checkout, to the style atlas.

#### متى تُستدعى

- «شغّل المهارة من غير ما تعمل git clone»
- «Auto mode blocked the clone, so use the installed skill instead»
- «Is the full style atlas available locally?»
- «دوّر على أسلوب silhouette في النسخة المحلية بس»
- «Search the power catalog offline»

#### الأوامر

- **doctor**: Prints one JSON line: local_only, network false, clone_required false, full_style_atlas_available, power_records, families, status_counts, next_step
  - `python3 scripts/local_first.py doctor`
- **search-powers**: Runs powers.py search with the given words
  - `python3 scripts/local_first.py search neon glow --scope powers`
- **search-styles**: Runs tools/kosif.py search when the full repo is present; otherwise prints a JSON error, exits 2 and never clones
  - `python3 scripts/local_first.py search sketch --scope styles`
- **search-auto**: Default --scope auto: searches the style atlas (tools/kosif.py) when the full repo is present, otherwise the power catalog (powers.py)
  - `python3 scripts/local_first.py search silhouette`
- **skill-dir**: Points at another installed skill folder (the global option goes before the subcommand)
  - `python3 scripts/local_first.py --skill-dir . doctor`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: It never fetches, clones or installs anything, so in a standalone skill bundle the style atlas stays unavailable; doctor counts records and does not prove that any power runs.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_local_first.py`
- مرجع: `.claude/skills/kosif-superpowers/references/claude-auto-local-first.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:local-first --evidence <ملف>`.

### `micro-index` — الفهرس الدقيق: سطر لكل قدرة وأداة وقدرة خارقة / Micro index: one line per power, tool and superpower

| الحقل | القيمة |
|---|---|
| المسار | `scripts/micro_index.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** يبني أدق خريطة للمهارة: لكل قدرة ذرية وأداة قابلة للتشغيل وقدرة خارقة مدخل واحد فيه مجموعتها ومجالها وعائلتها وقدرتها الخارقة وشارتها ومستلزماتها وأدوات عائلتها وفصلها وبطاقتها في المكتبة. يكتب data/micro_index.json وreferences/micro-index/ (صفحة لكل مجموعة وصفحة للأدوات وأخرى للقدرات الخارقة)؛ find يبحث فيه بالعربية أو الإنجليزية وshow يعرض أي معرّف مع جيرانه. الخيار --check يبلغ عن الملفات غير المحدّثة دون كتابة.

**What it does:** Builds the finest-grained map of the skill: every atomic power, runnable tool and fused superpower gets one entry with its group, domain, family, superpower, badge, requirements, the tools of its family, its chapter and its library card. Writes data/micro_index.json and references/micro-index/ (one page per group plus tools and superpowers); find searches it in Arabic or English and show prints any id with its neighbours. --check reports stale files without writing.

#### متى تُستدعى

- «اعرض لي الفهرس الدقيق لكل القدرات»
- «فين القدرة دي وإيه الأدوات اللي معاها»
- «Find every power, tool and superpower about loudness»
- «Show SP-0042 with its members and links»

#### الأوامر

- **build**: Writes data/micro_index.json and the pages under references/micro-index/; --check writes nothing and exits 1 when stale.
  - `python3 scripts/micro_index.py build`
- **find**: Ranked one-line matches across powers, tools and superpowers; --kind narrows, --json for machines.
  - `python3 scripts/micro_index.py find "قص على الإيقاع" --top 10`
- **show**: One id (power, TOOL-NN, tool id or SP-NNNN) with its superpower, family tools, chapter, card, members or links.
  - `python3 scripts/micro_index.py show SP-0001`
- **stats**: Counts per kind, status and group.
  - `python3 scripts/micro_index.py stats`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: build writes only its own generated files; find, show and stats only read.
- الحدود: An entry is an address, not a proof: badges are the records' own and a proven badge still needs a real run.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_micro_index.py`
- مرجع: `.claude/skills/kosif-superpowers/references/micro-index/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:micro-index --evidence <ملف>`.

### `owned-repos` — خريطة مستودعات المالك وخريطة المهارات / Owned-repositories map and skill map

| الحقل | القيمة |
|---|---|
| المسار | `scripts/owned_repos.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** يربط كل مستودع على حساب المالك بمجموعات القدرات الخمس عشرة: غرض وحالة لكل مستودع (مدمج، جزئي، قابل للتعلّم، مرجع، أرشيف، فارغ)، ومسحًا ساكنًا بنمط gitingest للنسخ الضحلة (ملفات، لغات، مهارات، اختبارات، CI، ملفات تعريف، وعدد أنماط تشبه المفاتيح بلا قيمها)، وعدد استشهادات الكتالوج لكل مستودع، والعلاقات بين المستودعات والخدمات الحية التي تبنيها على Cloudflare (مكتبة الحافة، Jev، خادم KOSIF Think) مع قواعد أمانها، وجدول المتاح الآن والقابل للتعلّم لكل مجموعة.

**What it does:** Joins every repository on the owner's GitHub account to the 15 smart capability groups: a curated purpose and state (integrated, partial, learnable, reference, archive, empty) per repo, a static gitingest-style digest of shallow clones (files, languages, SKILL.md, tests, CI, manifests, secret-like pattern counts without values), live catalog proof citations per repo, relations between repos and the live Cloudflare services they build (atlas edge API, Jev decision service, KOSIF Think Full Pro server) with their safety rules, and a have-now vs learnable table per capability group.

#### متى تُستدعى

- «راجع كل مستودعاتي واعرف إيه اللي ممكن نستفيد منه»
- «ايه المهارات اللي عندي واللي ممكن اتعلمها؟»
- «Which of my repos helps with an audit report?»
- «Map all my GitHub repositories into the superpowers skill»

#### الأوامر

- **find**: Ranks owned repos for a task by word overlap with purpose, keywords and their capability groups; archive and empty repos rank lower.
  - `python3 scripts/owned_repos.py find "رسم شخصيات"`
- **skills**: Per capability group: powers, have now (proven+ready), methods, learnable by install or key, owned repos feeding it and those still to learn from.
  - `python3 scripts/owned_repos.py skills`
- **list**: One line per repo with visibility, state, live catalog citations and groups.
  - `python3 scripts/owned_repos.py list`
- **show**: Prints one registry entry in full.
  - `python3 scripts/owned_repos.py show think`
- **digest**: Static scan of shallow clones named owner_repo; reads files only, counts secret-like patterns by name.
  - `python3 scripts/owned_repos.py digest <clones-dir> --out <work-dir>/digest.json`
- **merge**: Refreshes measured fields; private repos keep counts only.
  - `python3 scripts/owned_repos.py merge <work-dir>/digest.json`
- **render**: Writes or checks references/owned-repos-map.md.
  - `python3 scripts/owned_repos.py render --check`
- **verify**: Checks states, groups, links, privacy, the repo count, citations for integrated repos and the rendered doc.
  - `python3 scripts/owned_repos.py verify`
- **--self-test**: Digest, privacy and routing self-test on a temporary fixture.
  - `python3 scripts/owned_repos.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- optional: git (to make the clones)
- الأمان: read-only
- الموافقة: Cloning private repositories needs the owner's access in the session; never commit private repo content to a public repo.
- الحدود: Purposes and states are curated judgements refreshed by hand; the digest is a static file count, not a test run, and a secret-like hit is a pattern match to check, not proof of a live key.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_owned_repos.py`
- مرجع: `.claude/skills/kosif-superpowers/references/owned-repos-map.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:owned-repos --evidence <ملف>`.

### `powers` — البحث في كتالوج القدرات / Power catalog search

| الحقل | القيمة |
|---|---|
| المسار | `scripts/powers.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `knowledge-graph` |

**ما تفعله:** يبحث في كتالوج القدرات (4,751 سجلًا) بالعربية أو الإنجليزية ويصفّيه ويشرحه. يقدّم الإحصاءات والبحث الحر وعرض قدرة كاملة وعرض عائلة كاملة، ويقترح القدرات والأساليب المرجعية لطلب ما، ويعرض توزيع المجالات وخريطة ذهنية بصيغة Mermaid نصًا أو صفحة HTML مستقلة. ويحيل الأمر env إلى probe_env.py.

**What it does:** Searches, filters and explains the 4,751-record power catalog in Arabic or English. It offers stats, free-text search, one power in full, a whole family, brief-to-powers suggestions with reference styles, a domain breakdown and a Mermaid mind map (text or a standalone HTML page). It forwards `env` to probe_env.py.

#### متى تُستدعى

- «دورلي على قدرة توهج نيون للنص»
- «ايش القدرات المناسبة لريلز دعاء هادئ 9:16؟»
- «Which powers fit an Arabic reel with synced captions?»
- «Show me power GLOW-03 in full»
- «اعمل لي خريطة ذهنية لكل قدراتك»
- «List every proven power in the light-glow-bloom family»

#### الأوامر

- **stats**: Counts per family, status and domain (optionally one domain)
  - `python3 scripts/powers.py stats --domain motion --json`
- **search**: Free-text search (Arabic or English) with intent expansion; filters by --status and --domain; exits 1 when nothing matches
  - `python3 scripts/powers.py search glow neon --status proven ready --limit 10`
- **show**: Prints one power record in full (what, when, how, params, install, license, proof); exits 1 for an unknown id
  - `python3 scripts/powers.py show GLOW-03`
- **family**: Lists every power in a family, by stem or by prefix such as GLOW
  - `python3 scripts/powers.py family light-glow-bloom --status proven`
- **suggest**: Ranks powers for a brief across domains (spread across families), adds reference styles and the output format for motion briefs, and lists chapters and hints
  - `python3 scripts/powers.py suggest "Arabic reel with synced captions 9:16" --limit 12 --json`
- **styles**: Lists watched reference styles from data/styles.json, filtered by genre
  - `python3 scripts/powers.py styles --genre explainer --limit 10`
- **domains**: Counts per domain, then family, then status, with Arabic and English titles
  - `python3 scripts/powers.py domains --json`
- **mindmap**: Prints a Mermaid mindmap of domains and families, or drills into one domain down to its top powers
  - `python3 scripts/powers.py mindmap --domain mind --top 3 --en`
- **mindmap-html**: Writes a standalone HTML page that renders the map with Mermaid from a CDN and falls back to a text list offline
  - `python3 scripts/powers.py mindmap --html ./out/map.html`
- **env**: Runs probe_env.py with the given flags
  - `python3 scripts/powers.py env --no-network --json`

#### المتطلبات والأمان

- binaries: python3
- network: true
- الأمان: network
- الموافقة: `env` runs probe_env.py, which contacts public hosts unless --no-network is passed and installs packages from PyPI and npm with --install-test. `mindmap --html PATH` writes a file at PATH, and the page loads Mermaid from cdn.jsdelivr.net when opened.
- الحدود: It ranks catalog records by keyword and intent matching; a match or badge describes a recorded recipe, not a run on this machine, and nothing in a record is executed.

#### الاختبارات والأدلة

- `tests/test_superpowers.py`
- `.claude/skills/kosif-superpowers/evals/test_rea_routing.py`
- `.claude/skills/kosif-superpowers/evals/test_installer_triage.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `.claude/skills/kosif-superpowers/references/self-discovery.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-map.md`
- مرجع: `.claude/skills/kosif-superpowers/references/cognition.md`
- مرجع: `AGENTS.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:powers --evidence <ملف>`.

### `probe-env` — فحص قدرات الجهاز / Machine capability probe

| الحقل | القيمة |
|---|---|
| المسار | `scripts/probe_env.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-elsewhere` |
| العائلات | `self-discovery` |

**ما تفعله:** يفحص الجهاز الحالي: النظام والمعالج والذاكرة والقرص ووحدة الرسوميات، وبيئات التشغيل والأدوات وإصداراتها، وحزم بايثون وNode، والخطوط العربية، والمتصفحات، وأسماء متغيرات المفاتيح، والوكيل وإمكانية الوصول إلى الشبكة. ثم يطبع بطاقة قدرات بصيغة Markdown أو JSON تربط كل نتيجة بعائلات القدرات التي تفتحها.

**What it does:** Probes the current machine (OS, CPU/RAM/disk/GPU, runtimes, CLI tools and versions, Python and Node packages, Arabic fonts, browsers, credential env-var names, proxy and network reach). It prints a Markdown capability card or JSON that maps each finding to the power families it unlocks.

#### متى تُستدعى

- «افحص الجهاز وشوف ايه المتاح عليه»
- «هل عندي ffmpeg وخطوط عربية ومتصفح هنا؟»
- «Probe this machine before I promise a render»
- «Can this sandbox reach pypi and npm?»
- «Write a dated environment snapshot to a file»

#### الأوامر

- **card**: Markdown capability card, including HEAD requests to 11 public hosts (default budget 18 s)
  - `python3 scripts/probe_env.py`
- **json**: The same probe as JSON (probe, host, system, gpu, bins, versions, python, node, fonts, browsers, proxy, network, keys, docker, catalog, domains, unlocks, gaps, timed_out, elapsed_s)
  - `python3 scripts/probe_env.py --json`
- **no-network**: Skips the public-host reachability checks (offline or CI); the loopback agent-proxy status query still runs
  - `python3 scripts/probe_env.py --no-network --json`
- **budget**: Sets the total time budget in seconds (minimum 3, default 18)
  - `python3 scripts/probe_env.py --no-network --budget 10`
- **write**: Also writes a dated Markdown snapshot to the given path (the parent folder must already exist)
  - `python3 scripts/probe_env.py --no-network --write ./environment.md`
- **install-test**: Also times a real venv+pip install (six, plus packaging via uv) and an npm install (is-number) inside a temp dir
  - `python3 scripts/probe_env.py --install-test`

#### المتطلبات والأمان

- binaries: python3
- network: true
- optional: bin:docker, bin:fc-list, bin:node, bin:npm, bin:nvidia-smi, bin:uv
- الأمان: network
- الموافقة: A default run sends HEAD requests to 11 public hosts (pypi.org, registry.npmjs.org, github.com, api.github.com, huggingface.co, cdn.jsdelivr.net, fonts.googleapis.com, api.anthropic.com, example.com, en.wikipedia.org, plus an apt mirror); use --no-network if outbound contact is not wanted. --install-test downloads and installs packages from PyPI (six, packaging via uv) and npm (is-number) into a temp dir and needs explicit approval. Every run also executes local version commands, writes and deletes a 32 MB temp file, and runs 'sudo -n true' when not root.
- الحدود: It detects presence and reachability only (version strings, import specs, HEAD responses), not whether a tool produces correct output, and the card holds only for this machine at this moment.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `.claude/skills/kosif-superpowers/references/self-discovery.md`
- مرجع: `.claude/skills/kosif-superpowers/references/environment.md`
- مرجع: `.claude/skills/kosif-superpowers/references/surfaces.md`
- مرجع: `.claude/skills/kosif-superpowers/references/verification.md`
- مرجع: `AGENTS.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:probe-env --evidence <ملف>`.

### `python-package-probe` — فاحص وجود حزم بايثون / Python package presence probe

| الحقل | القيمة |
|---|---|
| المسار | `scripts/python_package_probe.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** يبيّن لكل توزيعة بايثون مذكورة (حتى 50 توزيعة) هل بياناتها الوصفية مثبتة وما إصدارها، دون استيرادها أو تثبيتها أو الاتصال بالشبكة.

**What it does:** Reports whether each named Python distribution (up to 50) has installed metadata and which version it is, without importing, installing or contacting the network.

#### متى تُستدعى

- «هل pandas وnumpy متسطبين على الجهاز ده؟»
- «تأكد من وجود مكتبة httpx قبل ما أكتب الكود»
- «Check which of pandas, numpy and httpx are installed here»
- «What version of pillow is available in this Python?»

#### الأوامر

- **probe (positional names)**: For each distribution name, prints status (distribution_metadata_found or not_found_in_environment), version, and import_tested, execution_tested and ready_for_production, which are always false.
  - `python3 scripts/python_package_probe.py pandas numpy httpx`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: Reads installed distribution metadata only and never imports the package, so a found package is not proven to import or work.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_system_python.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `.claude/skills/kosif-superpowers/references/community-source-atlas.md`
- مرجع: `.claude/skills/kosif-superpowers/references/repository-capability-transfer.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:python-package-probe --evidence <ملف>`.

### `repo-kosif` — أداة سطر أوامر لأطلس أنماط KOSIF / KOSIF style atlas CLI

| الحقل | القيمة |
|---|---|
| المسار | `tools/kosif.py` (جذر: repo) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `story-direction-ideas`, `prompt-craft`, `planning-execution` |

**ما تفعله:** يبحث في أطلس أنماط الموشن جرافيك (289 سجلًا في catalog/styles.json)، ويسرد سجلاته ويعرض أيًّا منها بالتفصيل. ويملأ كذلك طلبًا جاهزًا للصق في Claude Code من القالب templates/claude_request.<lang>.txt، وينشئ مجلد مشروع يضم STYLE.md وPLAN.md وTEST_REPORT.md وwords.json وREQUEST.md مع نسخة اختيارية من مشروع بداية، ويطبع إحصاءات الفهرس ويشغّل فاحص المستودع.

**What it does:** Searches, lists and shows records of the motion-graphics style atlas (289 records in catalog/styles.json). It also fills a ready-to-paste Claude Code request from templates/claude_request.<lang>.txt, scaffolds a project folder (STYLE.md, PLAN.md, TEST_REPORT.md, words.json, REQUEST.md and an optional starter copy), prints catalog statistics and runs the repository validator.

#### متى تُستدعى

- «دوّر لي على استايل موشن عربي كينتك في الأطلس»
- «أبغى طلب جاهز لـ Claude Code لاستايل معيّن بمقاس 9:16 ومدة 15 ثانية»
- «جهّز لي مجلد مشروع فيديو من استايل kinetic-arabic مع ستارتر html-canvas»
- «find a whiteboard or kinetic typography style in the atlas»
- «scaffold a motion-graphics project from a catalog style»
- «how many styles per category are in the catalog?»

#### الأوامر

- **list**: Shows a table of styles (id, name, categories, type, rank). Filters by category key or label, origin (PromptsMotion\|KOSIF) and type; sorts by rank, name or published date; --json prints the full records.
  - `python3 tools/kosif.py list --category charts --limit 10`
- **search**: Case-insensitive free-text search. Every word must match somewhere in the id, names, creator, keywords, summaries or category labels; words found in the id score higher.
  - `python3 tools/kosif.py search kinetic arabic --limit 5`
- **show**: Prints styles/<id>/STYLE.json, then BRIEF.md when present, then the category playbook paths (and whether each exists) and the SKILL.md path. An unknown id suggests close matches.
  - `python3 tools/kosif.py show kinetic-arabic`
- **prompt**: Fills the ar or en request template with the style, playbooks, aspect and resolution, fps, duration, source, stack, brand, audio policy and on-screen language. Prints the request, or writes it with --out FILE (parent folders are created).
  - `python3 tools/kosif.py prompt kinetic-arabic --lang en --aspect 9:16 --duration 15 --source "audio voice.mp3" --audio keep`
- **scaffold**: Creates a project folder with filled STYLE.md, PLAN.md and TEST_REPORT.md, a words.json copied from templates/words.example.json, and REQUEST.md; optionally copies starters/html-canvas or starters/remotion without node_modules. Refuses a non-empty folder unless --force is given.
  - `python3 tools/kosif.py scaffold kinetic-arabic ./out/my-film --starter html-canvas`
- **validate**: Runs tools/validate.py in a child Python process on the same --root, passes extra flags through (--quiet, --json) and exits with its code.
  - `python3 tools/kosif.py validate --quiet`
- **stats**: Prints counts by origin, type, category and aspect_label, the top creators, BRIEF.md coverage and how many category playbooks exist.
  - `python3 tools/kosif.py stats --top 5 --json`
- **help**: Prints the bilingual usage text (exit 0). With no arguments it prints the same text and exits 2; `<command> --help` shows that subcommand's options.
  - `python3 tools/kosif.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: runs-external-programs
- الموافقة: scaffold writes into the chosen folder; with --force it overwrites STYLE.md, PLAN.md, TEST_REPORT.md, words.json, REQUEST.md and starter files already there, so confirm the destination first. prompt --out overwrites that file. validate only spawns the repo's own read-only tools/validate.py with the same Python.
- الحدود: It only searches and scaffolds from the motion style atlas (catalog/styles.json); it does not search the skill's 4,700-power catalog, render video or install starter dependencies (it only prints an npm install reminder).

#### الاختبارات والأدلة

- `tests/test_cli.py`
- `tests/test_aspects.py`
- مرجع: `README.md`
- مرجع: `AGENTS.md`
- مرجع: `CLAUDE.md`
- مرجع: `templates/claude_request.README.md`
- مرجع: `starters/html-canvas/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-kosif --evidence <ملف>`.

### `requirements` — مخطط متطلبات القدرات / Power requirements planner

| الحقل | القيمة |
|---|---|
| المسار | `scripts/requirements.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `planning-execution` |

**ما تفعله:** يبيّن ما تحتاجه كل قدرة في الكتالوج من أدوات وحزم pip وnpm ومفاتيح ومنصات وخطوط ونماذج، وما المتوفر منها على هذا الجهاز، وأوامر التثبيت للقدرات المقترحة لمهمة ما. وتعيد أوامر الصيانة اشتقاق حقول requires وتوليد الملف references/requirements.md.

**What it does:** Reports what each catalog power needs (tools, pip/npm packages, keys, platforms, fonts, models), which of those this machine has, and the install commands for the powers suggested for a task. Maintainer subcommands re-derive the `requires` fields and regenerate references/requirements.md.

#### متى تُستدعى

- «ايش لازم أثبت عشان أسوي ريلز بتعليق صوتي وترجمة متزامنة؟»
- «القدرة GLOW-05 محتاجة ايه عشان تشتغل؟»
- «What do I need to install before starting this task?»
- «Which registered requirements are present on this machine?»
- «Check that every power's requires field is up to date»

#### الأوامر

- **present**: Marks every registered requirement present, missing or unknown on this machine (read-only, about 1 s)
  - `python3 scripts/requirements.py present --json`
- **for**: Checklist for one power: each requirement's state, kind and install command
  - `python3 scripts/requirements.py for GLOW-05`
- **plan**: Suggests powers for a task, then merges their requirements into one checklist with install commands; ▶ marks powers whose requirements are all present
  - `python3 scripts/requirements.py plan "Arabic reel with voice-over and synced captions" --limit 8 --json`
- **derive-check**: Exits 1 if re-deriving `requires` from install/how text would change any record; read-only
  - `python3 scripts/requirements.py derive --check`
- **derive**: Rewrites the `requires` field in data/powers/*.json from the patterns in data/requirements.json
  - `python3 scripts/requirements.py derive`
- **index**: Regenerates references/requirements.md (requirement to powers unlocked); --probe adds present/missing marks for this machine
  - `python3 scripts/requirements.py index --probe`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: `derive` (without --check) rewrites data/powers/*.json and `index` rewrites references/requirements.md inside the skill; both are maintainer actions. The install commands it prints need user approval before anyone runs them, especially paid or system-wide installs.
- الحدود: It detects presence only (shutil.which, importlib find_spec, env-var name set, font file exists), never version fit or output quality, and it treats a power with no listed requirement as ready.

#### الاختبارات والأدلة

- `tests/test_requirements.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`
- مرجع: `.claude/skills/kosif-superpowers/references/requirements.md`
- مرجع: `.claude/skills/kosif-superpowers/references/cognition.md`
- مرجع: `CAPABILITIES.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:requirements --evidence <ملف>`.

### `skill-intelligence` — محرك بروتوكول ذكاء المهارات الشامل / Universal Skill Intelligence Protocol engine

| الحقل | القيمة |
|---|---|
| المسار | `scripts/skill_intelligence.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `agent-orchestration`, `planning-execution` |

**ما تفعله:** قبل أي طلب حقيقي: يفحص 100% من سجلات الكتالوج بإيصال تغطية وبصمة SHA-256 يفشل عند أي سجل تالف أو غير مصنف، ويتحقق من حداثة الفهارس، ويكتب مسودة تحليل الطلب، ويرتب المجموعات والقدرات الخارقة والقدرات والأدوات، ويقيّم المرشحات، ويصوغ الخطط A وB وC مع توصية وسؤال الموافقة.

**What it does:** Before any substantial request: scans 100% of the catalog records with a SHA-256 coverage receipt that fails closed on unreadable or unclassified records, checks that every derived index is fresh, drafts a request analysis, ranks groups, fused superpowers, powers and runnable tools, scores candidates (fit 35, integration 20, feasibility 15, evidence 10, cost 10, creativity 10) and drafts plans A/B/C with a recommendation and the approval question.

#### متى تُستدعى

- «حلل طلبي وراجع كل المهارات واقترح ثلاث خطط»
- «Scan every KOSIF capability for this request and propose three plans»
- «عايز تستفيد من كل القدرات الخارقة في المهمة دي»
- «Prove you reviewed the whole catalog before planning»

#### الأوامر

- **brief**: Prints the Arabic report: request analysis, 100% coverage receipt, index freshness, plan comparison, shortlist and the approval question; --json/--out for machines.
  - `python3 scripts/skill_intelligence.py brief "مونتاج ريلز على الإيقاع بترجمة عربية"`
- **verify**: Coverage and index freshness only; exit 1 on any gap.
  - `python3 scripts/skill_intelligence.py verify`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: none: read-only (writes only the optional --out file)
- الحدود: The analysis and plans are deterministic drafts from catalog text; Claude must think them over, and no capability is executed or verified by this tool.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_skill_intelligence.py`
- `.claude/skills/kosif-superpowers/evals/test_routing_quality.py`
- `.claude/skills/kosif-superpowers/evals/test_usip_shadow.py`
- مرجع: `.claude/skills/kosif-superpowers/PROTOCOL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:skill-intelligence --evidence <ملف>`.

### `skill-loader` — خريطة التحميل الخفيف للمهارات / Light skill loader map

| الحقل | القيمة |
|---|---|
| المسار | `scripts/skill_loader.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `agent-orchestration` |

**ما تفعله:** يكتب LOADER.md: خريطة صغيرة لكل مهارة في .claude/skills/ وللمجموعات الخمس عشرة ولكل ملحق بروتوكول بمحفّزه ولنطاقات أسطر أقسام كل SKILL.md، فيقرأ Claude ملفًا قصيرًا واحدًا ثم يفتح الأسطر التي تحتاجها المهمة فقط. need يسمّي الملفات ونطاقات الأسطر لمهمة، وfull يطبع ترتيب القراءة في وضع التفعيل الكامل.

**What it does:** Writes LOADER.md, one small map of every skill under .claude/skills/, the 15 capability groups, every protocol appendix with its trigger and the line ranges of each SKILL.md section, so Claude reads one short file and then opens only the lines a task needs. need names the few files and line ranges for a task; full prints the full-power reading order.

#### متى تُستدعى

- «فعّل كل القدرات»
- «اقرأ المهارات بسرعة من غير ما تحمّل كل حاجة»
- «Which skill files should I open for this task?»
- «Activate full power mode»

#### الأوامر

- **build**: Writes LOADER.md; with --check exits 1 when it is stale
  - `python3 scripts/skill_loader.py build --check`
- **need**: Lists the groups, appendices, skills and SKILL.md line ranges that match a task, best first; --json for records
  - `python3 scripts/skill_loader.py need "اعمل مونتاج ريلز" -n 6`
- **full**: Prints the full-power mode rule and the reading order
  - `python3 scripts/skill_loader.py full`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: —
- الحدود: need ranks by plain word overlap with titles, triggers and keywords; it narrows what to read and does not judge which skill is best.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_skill_loader.py`
- مرجع: `.claude/skills/kosif-superpowers/LOADER.md`
- مرجع: `.claude/skills/kosif-superpowers/PROTOCOL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:skill-loader --evidence <ملف>`.

### `smart-capabilities` — فهرس ذكي للقدرات من أجل Claude / Smart capability index for Claude

| الحقل | القيمة |
|---|---|
| المسار | `scripts/smart_capabilities.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** يصنف جميع القدرات إلى 15 مجموعة ويبحث بالعربية والإنجليزية مع حفظ المعرّفات والأدلة والمتطلبات. ويولّد مكتبة بروتوكول USIP v5.5 في references/library/ (فهرس وفصل توجيه لكل مجموعة: أعداد الحالات، والأدوات القابلة للتشغيل لعائلاتها، وعائلاتها، وكل قدرة بحالتها ومتطلباتها) ويفحص تقادمها. وبأمر cards يكتب مكتبة بروتوكول USIP v5.5 الكاملة usip-library/ في جذر المستودع (أكثر من 400,000 سطر): بطاقة بروتوكول لكل قدرة ولكل أداة تطبّق عليها قواعد الاستقبال والجاهزية والتخطيط والتحقق والتعافي من الملاحق A25–A29، مع صفحات أنماط الاستدلال والنماذج الذهنية والجودة وفهرس رئيسي؛ و--single يكتبها ملفًا واحدًا.

**What it does:** Deterministically classifies every KOSIF power ID into 15 task-based integration candidate groups, finds matches for Arabic or English prompts, and checks source-to-index completeness without claiming runtime fusion. It also generates the USIP v5.5 protocol library references/library/ (an index plus one routing chapter per group: status counts, the runnable tools serving the group's families, its families and every power with its status and requirements) and checks it for staleness. With cards it writes the full USIP v5.5 protocol library usip-library/ at the repo root (over 400,000 lines): a protocol card per catalog power and per runnable tool that applies the intake, readiness, planning, verification and recovery rules of appendices A25-A29 to that record, plus reasoning-mode, mental-model and quality pages and a master index; --single writes the whole library as one file.

#### متى تُستدعى

- «Give Claude an overview of the entire repository quickly»
- «Find related power groups and candidate IDs for a task»
- «فهرس القدرات الذكي»
- «اعثر على الأدوات المتكاملة»

#### الأوامر

- **groups**: List 15 candidate integration groups and counts.
  - `python3 scripts/smart_capabilities.py groups`
- **find**: Rank task-relevant groups and candidate power IDs.
  - `python3 scripts/smart_capabilities.py find "رسم خطوط وأشكال" --json`
- **verify**: Verify all original powers appear once and that generated index matches sources.
  - `python3 scripts/smart_capabilities.py verify`
- **build**: Rebuild source-derived JSON index and two compact reference documents.
  - `python3 scripts/smart_capabilities.py build`
- **library**: Writes references/library/INDEX.md and one chapter per group from data/powers/*.json and data/tools.json (deterministic), removing orphaned chapters
  - `python3 scripts/smart_capabilities.py library`
- **library-check**: Exits 1 when a library chapter is stale, missing or orphaned; writes nothing
  - `python3 scripts/smart_capabilities.py library-check`
- **cards**: Writes usip-library/ (README index, cards/<group>/<family>.md, tools/<area>.md, methods/*.md) deterministically from data/powers/*.json, data/tools.json and data/usip_intelligence.json, removes orphaned files, and with --single also writes the concatenated library
  - `python3 scripts/smart_capabilities.py cards --single out/USIP_LIBRARY_FULL.md`
- **cards-check**: Exits 1 when a usip-library/ file is stale, missing or orphaned; writes nothing
  - `python3 scripts/smart_capabilities.py cards-check`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: —
- الحدود: Logical group recommendations only; not execution proof or REA/Ghidra analysis; no promise that all 5,185 tools are executable.

#### الاختبارات والأدلة

- `tests/test_protocol_library.py`
- مرجع: `.claude/skills/kosif-superpowers/references/CLAUDE_3_MINUTE_MAP.md`
- مرجع: `.claude/skills/kosif-superpowers/references/SMART_CAPABILITY_GROUPS.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A28-capability-routing.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:smart-capabilities --evidence <ملف>`.

### `superpower-fusion` — دمج القدرات في قدرات خارقة مترابطة / Superpower fusion (powers to connected superpowers)

| الحقل | القيمة |
|---|---|
| المسار | `scripts/superpower_fusion.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `knowledge-graph` |

**ما تفعله:** يقسّم كل قدرة في الكتالوج إلى قدرة خارقة واحدة بالضبط، ويعلّم التوائم التي تؤدي العمل نفسه، ويربط كل قدرة خارقة بأقرب جيرانها في رسم واحد متصل، مع توزيع صادق للشارات.

**What it does:** Partitions every catalog power into exactly one fused superpower (per-family TF-IDF k-means, near-identical powers unified, tiny groups absorbed), marks twin powers that do the same job, links each superpower to its nearest neighbours in one connected graph, and reports an honest status mix.

#### متى تُستدعى

- «ادمج القدرات المتشابهة في قدرات أكبر»
- «Which superpower contains BEAT-16 and what are its twins?»
- «اقترح القدرات الخارقة لمونتاج ريلز»

#### الأوامر

- **build**: Writes data/superpowers.json and references/superpowers.md.
  - `python3 scripts/superpower_fusion.py build`
- **suggest**: Ranks superpowers for a brief.
  - `python3 scripts/superpower_fusion.py suggest "مونتاج ريلز بإيقاع الموسيقى"`
- **show**: Ordered members, twins, requirements and links of one superpower.
  - `python3 scripts/superpower_fusion.py show SP-0280`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: build overwrites its two generated files only
- الحدود: Clustering is by catalog wording; superpower names come from the most central member and a cluster can hold loosely related powers.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_superpower_fusion.py`
- مرجع: `.claude/skills/kosif-superpowers/references/superpowers.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:superpower-fusion --evidence <ملف>`.

### `superpowers-unified` — موجّه مهارات العمل ومثبّتها / Process-skill router and installer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/superpowers_unified.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `agent-orchestration`, `planning-execution`, `self-discovery` |

**ما تفعله:** يختار للمهمة مجموعة مرتّبة من مهارات العمل الخمس عشرة المضمّنة من obra/superpowers الإصدار 7 (مثل العصف الذهني وتتبّع الأخطاء والتطوير المقاد بالاختبارات والتحقق)، ويفحص المصادر المضمّنة، ويستطيع تثبيت KOSIF مع تلك المهارات في ‎~/.claude/skills مع نسخ احتياطية.

**What it does:** Picks an ordered subset of the 15 vendored obra/superpowers v7 process skills (brainstorming, debugging, TDD, verification and others) for a task, checks the vendored sources, and can install KOSIF plus those skills into ~/.claude/skills with backups.

#### متى تُستدعى

- «أي مهارات عمل أستخدمها لإصلاح عطل في التطبيق؟»
- «اعمل خطة لتطوير برنامج المونتاج، أي منهجية أتبع؟»
- «Which process skills apply to 'Fix the crash in the montage app'?»
- «Install KOSIF Superpowers and the obra process skills into my Claude skills folder»
- «Check whether the vendored superpowers skills are complete»

#### الأوامر

- **doctor**: Checks the vendored MIT LICENSE and the 15 process SKILL.md files, and reports whether KOSIF and how many process skills are installed under ~/.claude/skills. Exits with code 2 if sources are missing.
  - `python3 scripts/superpowers_unified.py doctor`
- **plan**: Uses a fixed keyword table (English and Arabic) to return an ordered list of process skills, starting with using-superpowers and ending with verification-before-completion, adding test-driven-development for code/app tasks.
  - `python3 scripts/superpowers_unified.py plan "Fix the crash in the montage app"`
- **list**: Lists the 15 vendored process-skill names.
  - `python3 scripts/superpowers_unified.py list`
- **install**: Copies the whole kosif-superpowers folder (~30 MB) and the 15 process skills into ~/.claude/skills; identical copies are reported already_current and differing existing ones are skipped unless --force is given, which backs them up to ~/.claude/backups/kosif-ultimate-<UTC stamp> before replacing. Without --no-global-instructions it also appends a marked policy block to ~/.claude/CLAUDE.md (backing up an existing file first).
  - `python3 scripts/superpowers_unified.py install --no-global-instructions`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: install writes outside the repository: it copies 16 skill folders (about 30 MB) into ~/.claude/skills, replaces existing ones with --force (after backing them up), and appends to ~/.claude/CLAUDE.md unless --no-global-instructions is given. Get explicit user approval before running install. doctor, plan and list are read-only.
- الحدود: plan is a fixed keyword-to-skill lookup and doctor checks only that files exist; neither one runs, verifies or tests any skill.

#### الاختبارات والأدلة

- `tests/test_superpowers_unified.py`
- مرجع: `.claude/skills/kosif-superpowers/references/superpowers-unification.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:superpowers-unified --evidence <ملف>`.

### `superskills` — المهارات الخارقة: الـ114 مهارة الكاملة من مستودعك داخل سوبر باور / 100 Super Skills: the owner's 114 whole skills, vendored and routable

| الحقل | القيمة |
|---|---|
| المسار | `scripts/superskills.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `agent-orchestration` |

**ما تفعله:** يضع مستودعك 100-superskills كاملًا داخل سوبر باور: كل مجلدات الـ114 مهارة (110 مهارة خارقة مفهرسة ومعها kosif-one وkosif-social وkosif-mimic وkosif-montage-motion، أي 682 ملفًا و143 سكربتًا) منسوخة في vendor/100-superskills ببصمة SHA-256 لكل ملف. يختار المهارة المناسبة لأي طلب بالعربي أو الإنجليزي، ويعرض منهجها وسكربتاتها واختباراتها ومصادرها، ويثبّت أي مهارة في ~/.claude/skills، ويتحقق من كل ملف ببصمته، ويشغّل اختبارات المهارات نفسها في نسخة مؤقتة. و hub.py find بقى يعرض المهارات الخارقة المناسبة كمان.

**What it does:** Holds the owner's repository kosif199022-jpg/100-superskills inside Superpowers: all 114 skill folders (110 catalogued super skills plus kosif-one, kosif-social, kosif-mimic and kosif-montage-motion, 682 files with 143 scripts) copied into vendor/100-superskills with a SHA-256 manifest. It finds the right super skill for a request in Arabic or English, shows its method, scripts, tests and sources, installs one into ~/.claude/skills, verifies every file against its hash and runs the skills' own unit tests in a temporary copy. hub.py find lists the matching super skills too.

#### متى تُستدعى

- «انقل قدرات مستودع الـ114 مهارة لسوبر باور»
- «أنهي مهارة من المهارات الخارقة تنفع للطلب ده؟»
- «ثبّت مهارة النماذج المالية في إكسل عندي»
- «عايز مجلس خبراء لقرار صعب»
- «Which of my 100 super skills fits this request?»
- «Install the kinetic Arabic typography skill»

#### الأوامر

- **find**: Ranks the 114 super skills for the request (Arabic-aware: article and joined و/ب/ل prefixes dropped) and prints the best five with their domain and script count; --json for machines.
  - `python3 scripts/superskills.py find "نموذج مالي في إكسل"`
- **list**: Lists every super skill grouped into its ten domains (motion, image-video, prompts-ai, office-data, web-code, business, ultra, pixel, hyperframes, kosif-core).
  - `python3 scripts/superskills.py list --domain motion`
- **show**: Prints a skill's description, vendored path, scripts, tests, source skills and licences and the install command; --full adds the whole SKILL.md.
  - `python3 scripts/superskills.py show genius-council-decision --full`
- **install**: Copies one skill folder into ~/.claude/skills (or --dest); refuses to overwrite unless --force, and then keeps a .bak copy.
  - `python3 scripts/superskills.py install kinetic-typography-arabic --dry-run`
- **verify**: Checks every vendored file against the SHA-256 in vendor/100-superskills/KOSIF_INTEGRATION.json and reports unlisted files.
  - `python3 scripts/superskills.py verify`
- **selftest**: Runs the skills' own unit tests (pixel-studio-painter, kosif-montage-motion, kosif-one, kosif-social) in a temporary copy of the skills folder.
  - `python3 scripts/superskills.py selftest kosif-one`
- **sync**: Owner action: re-copies the skills from a 100-superskills checkout, re-applies the KOSIF patches, rewrites the manifest and data/superskills.json.
  - `python3 scripts/superskills.py sync --src ../100-superskills`

#### المتطلبات والأمان

- optional: ffmpeg, opencv-python-headless, scipy, pillow, numpy
- الأمان: writes-files
- الموافقة: find, list, show and verify only read. install writes one folder under ~/.claude/skills (never overwrites without --force). selftest runs the vendored skills' own tests in a temporary copy. Nothing is published or downloaded.
- الحدود: The ranking is keyword matching over titles and descriptions, not semantic search; broken Arabic plurals (فاتورة / فواتير) can miss. Nine large media files (videos, big PNGs, a tessdata model, demo WAVs) stay upstream and are listed per skill. vendor/ is left out of the claude.ai zip, so there only the index and descriptions travel. The selftest needs ffmpeg, opencv-python-headless, scipy, pillow and numpy for the full set.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_superskills.py`
- مرجع: `.claude/skills/kosif-superpowers/vendor/100-superskills/KOSIF_README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:superskills --evidence <ملف>`.

### `superskills-bridge` — جسر المهارات الخارقة: بحث للقراءة فقط في فهرس الـ114 مهارة / 100 Super Skills bridge: read-only index lookup

| الحقل | القيمة |
|---|---|
| المسار | `scripts/superskills_bridge.py` (جذر: skill) |
| المجال | `discover` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** بحث للقراءة فقط في data/100-superskills-index.json (فهرس الـ114 مهارة اللي اتضاف في PR #153): doctor يقول كام ملف SKILL.md موجود، وlist وfind وshow وpath يطبعوا المهارة وتصنيفها ومسارها. skill_loader.py need بيستخدم نفس الفهرس. للترتيب والتثبيت وفحص البصمات واختبارات المهارات استخدم superskills.

**What it does:** Read-only lookup over data/100-superskills-index.json (the 114-skill index added with PR #153): doctor reports how many SKILL.md files are present, list, find, show and path print entries with their category and vendored path. skill_loader.py need uses the same index. For ranking, install, hash checks and the skills' own tests use superskills.

#### متى تُستدعى

- «هل ملفات الـ114 مهارة موجودة؟»
- «فين مسار مهارة kosif-mimic؟»
- «Is every super skill file present in this checkout?»

#### الأوامر

- **doctor**: Counts the catalogued skills and the SKILL.md files present under vendor/100-superskills.
  - `python3 scripts/superskills_bridge.py doctor`
- **find**: Token match over slug, Arabic and English names and description.
  - `python3 scripts/superskills_bridge.py find "excel"`
- **path**: Prints the vendored SKILL.md path of one skill.
  - `python3 scripts/superskills_bridge.py path kosif-mimic`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: Reads the index and checks file presence only.
- الحدود: Plain token overlap, no Arabic prefix handling; it does not install, verify hashes or run anything.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_superskills.py`
- مرجع: `.claude/skills/kosif-superpowers/references/100-superskills-integration.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:superskills-bridge --evidence <ملف>`.

