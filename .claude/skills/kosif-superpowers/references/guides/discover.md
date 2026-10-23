# اكتشاف القدرات والتوجيه والتفكير — Discover, route and think

كيف يعرف Claude ما يستطيعه الآن ويختار القدرة الصحيحة، ويعمل حين يمنع الوضع التلقائي الكود الخارجي، ويستعمل أطلس القدرات وموجّه التشغيل ومحرك التفكير وطبقة عمليات obra.

How Claude learns what it can do right now and picks the right capability: the capability atlas, the runtime router, the bilingual finder, local-first use under Auto mode, cognition and requirements, the invention lab and the obra process-skill layer.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:discover:start -->

**الأدوات / tools (25)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `ai-tool-discovery` | Ranks KOSIF catalog powers for an Arabic or English task using weighted field matching with corpus-rarity scoring over the local atlas index, and returns IDs, matched terms, claimed status and requirements with runtime_verified=false. | `python3 scripts/ai_tool_discovery.py "تحريك شخصيات فيديو" --top 8` | tested-here |
| `boot` | Prints a short self-briefing for Claude: machine facts, catalog counts per domain, how many powers have every listed requirement present, the installs that unlock the most powers, the runnable-tool count and the next commands to run (hub.py, think.py, requirements.py). It can also regenerate or check the repo-root CAPABILITIES.md and llms.txt. | `python3 scripts/boot.py` | tested-here |
| `capability-atlas` | Searches the 4,751-power KOSIF catalog in Arabic or English, plans a task by picking capability IDs, process skills, routes and local requirement checks, and rebuilds the atlas index and its guide. | `python3 scripts/capability_atlas.py stats --json` | tested-here |
| `capability-graph` | Builds one connected graph of the skill: root → domains → families → the requirements they need, the scripts that run them, and the tests that mention those scripts. Code edges come from a local AST import pass merged with the committed Graphify snapshot. The graph is written as data/capability_graph.json plus an offline, searchable HTML page, and the tool answers stats and neighbour queries on it. | `python3 scripts/capability_graph.py build` | tested-here |
| `capability-runtime-router` | Matches an Arabic or English task to the 22 KOSIF routes in data/capability_routes.json (17 backed by a local script, 5 external) and returns, for each one, the runbook command, which binaries are present or missing, the permissions it needs that have not been granted, and a status that never claims execution. | `python3 scripts/capability_runtime_router.py --task "حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي" --limit 5 --json` | tested-here |
| `hub` | One question in, everything relevant out: the runnable tools for a task (with a copy-paste command and whether this machine has their requirements), the catalog powers, the guides and, for motion work, reference styles. | `python3 scripts/hub.py find "اعمل فيديو موشن عربي متزامن مع صوتي"` | tested-here |
| `kosif-mcp` | Read-only stdio MCP server that lets any MCP client (Claude Code, Claude Desktop, Cursor …) ask the same questions as hub.py: find, tool cards, doctor, power search and records, families and guides. | `python3 scripts/kosif_mcp.py` | tested-here |
| `local-first` | A no-network, no-clone entry point. `doctor` checks the installed skill and reports catalog record counts by status and whether the full style atlas is present; `search` forwards to the local power catalog or, inside a full kosif-tool checkout, to the style atlas. | `python3 scripts/local_first.py doctor` | tested-here |
| `powers` | Searches, filters and explains the 4,751-record power catalog in Arabic or English. It offers stats, free-text search, one power in full, a whole family, brief-to-powers suggestions with reference styles, a domain breakdown and a Mermaid mind map (text or a standalone HTML page). It forwards `env` to probe_env.py. | `python3 scripts/powers.py stats --domain motion --json` | tested-here |
| `probe-env` | Probes the current machine (OS, CPU/RAM/disk/GPU, runtimes, CLI tools and versions, Python and Node packages, Arabic fonts, browsers, credential env-var names, proxy and network reach). It prints a Markdown capability card or JSON that maps each finding to the power families it unlocks. | `python3 scripts/probe_env.py` | tested-elsewhere |
| `python-package-probe` | Reports whether each named Python distribution (up to 50) has installed metadata and which version it is, without importing, installing or contacting the network. | `python3 scripts/python_package_probe.py pandas numpy httpx` | tested-here |
| `requirements` | Reports what each catalog power needs (tools, pip/npm packages, keys, platforms, fonts, models), which of those this machine has, and the install commands for the powers suggested for a task. Maintainer subcommands re-derive the `requires` fields and regenerate references/requirements.md. | `python3 scripts/requirements.py present --json` | tested-here |
| `superpowers-unified` | Picks an ordered subset of the 15 vendored obra/superpowers v7 process skills (brainstorming, debugging, TDD, verification and others) for a task, checks the vendored sources, and can install KOSIF plus those skills into ~/.claude/skills with backups. | `python3 scripts/superpowers_unified.py doctor` | tested-here |
| `repo-kosif` (repo root) | Searches, lists and shows records of the motion-graphics style atlas (289 records in catalog/styles.json). It also fills a ready-to-paste Claude Code request from templates/claude_request.<lang>.txt, scaffolds a project folder (STYLE.md, PLAN.md, TEST_REPORT.md, words.json, REQUEST.md and an optional starter copy), prints catalog statistics and runs the repository validator. | `python3 tools/kosif.py list --category charts --limit 10` | tested-here |
| `atlas-capability-miner` | Indexes or queries metadata of third-party Atlas skills with an opt-in REA path; source presence is not execution proof. | `python3 scripts/atlas_capability_miner.py --help` | tested-here |
| `atlas-5000` | Maps the 5,116-skill safe core of KOSIF Atlas (READ_ONLY_OK, permissive license, no risk flags) against the KOSIF catalog: per-theme coverage, the themes with the most undistilled skills and their next candidates, and a bilingual search that shows which power already covers each Atlas skill. | `python3 scripts/atlas_5000.py stats --json` | tested-here |
| `atlas-ledger` | Gives every one of the 14,793 KOSIF Atlas skills exactly one review status: covered (a power cites it), pattern (one vendor's instance of a method a power already holds), duplicate, excluded (needs install review, copyleft or risk-flagged) or pending (safe, unique and not yet decided). Built from the inert Atlas metadata index, the power files and the reviewed rules in data/atlas-ledger-decisions.json; REA's hash receipt for the whole Atlas is in proofs/atlas-rea/. | `python3 scripts/atlas_ledger.py stats --json` | tested-here |
| `atlas-task-method-router` | Finds source-backed Atlas method candidates for a task without executing their code. | `python3 scripts/atlas_task_method_router.py --help` | untested |
| `smart-capabilities` | Deterministically classifies every KOSIF power ID into 15 task-based integration candidate groups, finds matches for Arabic or English prompts, and checks source-to-index completeness without claiming runtime fusion. It also generates the USIP v5.5 protocol library references/library/ (an index plus one routing chapter per group: status counts, the runnable tools serving the group's families, its families and every power with its status and requirements) and checks it for staleness. With cards it writes the full USIP v5.5 protocol library usip-library/ at the repo root (over 400,000 lines): a protocol card per catalog power and per runnable tool that applies the intake, readiness, planning, verification and recovery rules of appendices A25-A29 to that record, plus reasoning-mode, mental-model and quality pages and a master index; --single writes the whole library as one file. | `python3 scripts/smart_capabilities.py groups` | tested-here |
| `skill-intelligence` | Before any substantial request: scans 100% of the catalog records with a SHA-256 coverage receipt that fails closed on unreadable or unclassified records, checks that every derived index is fresh, drafts a request analysis, ranks groups, fused superpowers, powers and runnable tools, scores candidates (fit 35, integration 20, feasibility 15, evidence 10, cost 10, creativity 10) and drafts plans A/B/C with a recommendation and the approval question. | `python3 scripts/skill_intelligence.py brief "مونتاج ريلز على الإيقاع بترجمة عربية"` | tested-here |
| `fusionforge` | Turns the USIP brief (skill_intelligence is the single ranker) into a project-scoped candidate recipe: typed workflow nodes per stage holding catalog superpowers fingerprinted by their atom IDs, input/output artifact kinds, an executor reference and handoff edges, with plans A/B/C taken from the brief. It then records the approved plan, per-node traces with hashed evidence and every status change through an enforced state machine (candidate, planned, tested, then verified or failed) whose verified gate checks the records; validate runs checks V01-V12, and lessons, reuse and propose's recall rank the same project's earlier recipes. Cards and redacted bundles carry recipes to another session. Writes only under out/fusionforge/<project>/; it never executes a power, installs, publishes or edits the catalog. | `python3 scripts/fusionforge.py propose "مونتاج ريلز بترجمة عربية" --project demo_project --from-brief out/20261021-reel/brief.json` | tested-here |
| `fusionforge-shared` | Audits verified project-private FusionForge v2 promotion proposals; counts independent QA proofs across distinct projects, requires separate human privacy/security/collision and baseline-improvement review before exporting only allowlisted structural skill graphs. Never exports client objectives, transcripts, evidence, secrets or project names. | `python3 scripts/fusionforge_shared.py audit` | untested |
| `superpower-fusion` | Partitions every catalog power into exactly one fused superpower (per-family TF-IDF k-means, near-identical powers unified, tiny groups absorbed), marks twin powers that do the same job, links each superpower to its nearest neighbours in one connected graph, and reports an honest status mix. | `python3 scripts/superpower_fusion.py build` | tested-here |
| `kosif-groups` | For each of the 15 smart groups lists its fused superpowers ordered by readiness, entry scripts, a start command, linked groups and a per-group install plan that separates pip/npm lines (run with --apply) from system tools and keys that need the user's approval. | `python3 scripts/kosif_hubs.py` | tested-here |
| `owned-repos` | Joins every repository on the owner's GitHub account to the 15 smart capability groups: a curated purpose and state (integrated, partial, learnable, reference, archive, empty) per repo, a static gitingest-style digest of shallow clones (files, languages, SKILL.md, tests, CI, manifests, secret-like pattern counts without values), live catalog proof citations per repo, relations between repos and the live Cloudflare services they build (atlas edge API, Jev decision service, KOSIF Think Full Pro server) with their safety rules, and a have-now vs learnable table per capability group. | `python3 scripts/owned_repos.py find "رسم شخصيات"` | tested-here |

<!-- hub:area:discover:end -->

<!-- hub:area:think:start -->

**الأدوات / tools (12)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `anchor-gate` | Compares a text before and after a rewrite (English and Arabic) and reports every factual anchor that was dropped or added (quotes, numbers in digits or words, currencies, months, weekdays, emails, URLs, paths, @handles, versions, ratios/times and must-keep names), returning PASS or REVIEW_REQUIRED. | `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/en_before.txt --after proofs/general-writing/pairs/en_after_drift.txt --text` | tested-here |
| `architecture-sizer` | Computes a deterministic back-of-envelope capacity estimate (average and peak RPS, minimum replicas, logical and replicated storage in bytes and GiB) from caller-supplied traffic and hardware assumptions, using exact decimal arithmetic. | `python3 scripts/architecture_sizer.py --daily-requests 86400 --peak-factor 5 --payload-bytes 1000 --retention-days 7 --replica-rps 100 --target-utilization 0.5 --copies 2` | tested-here |
| `invention-lab` | Turns one problem statement into a reproducible, ranked JSON list of falsifiable engineering ideas (16 TRIZ-style inventive methods × 4 lenses), each with a hypothesis, test, success metric and rejection threshold. | `python3 scripts/invention_lab.py methods` | tested-here |
| `tell-scan` | Scans English and Arabic (MSA and Egyptian) prose for stock 'AI-sounding' writing habits and tool leftovers, and reports each hit with its line, strength and an overall verdict (EDIT/REVIEW/LOOK/LEAVE/CLEAN). | `python3 scripts/tell_scan.py proofs/general-writing/samples/en_ai.txt` | tested-here |
| `think` | Turns thinking procedures into checkable text scaffolds. It picks a reasoning level (L0–L6), writes a task contract, ranks 63 mental models, drafts a backcast plan, builds an idea matrix from catalog powers, scores a weighted decision with sensitivity, runs a Monte-Carlo Fermi estimate and flags weak wording in a draft. USIP v5.4 adds four reasoning tools: it ranks eight reasoning modes for a task, updates a belief by likelihood ratios with a halve/double sensitivity, gives a GO/PIVOT/KILL/HOLD verdict from thresholds written in advance, and builds a claim-to-evidence ledger for a draft. USIP v5.5 adds four intelligence scaffolds: it detects a request's deliverable kind and sorts its slots into filled, assumed, asked (within the level's question budget) and blocking; checks a task DAG and computes its order, optimistic and pessimistic critical path and one-way doors; prints the quality bar of twelve deliverable kinds and gives PASS, FAIL or INCOMPLETE from answers; and prints the recovery ladder for a FusionForge error class with an attempt budget. | `python3 scripts/think.py ladder "design a 30-day plan for a course launch"` | tested-here |
| `council` | Plans a five-member adversarial council for a request (Visionary, Skeptic, Builder, Audience, Guardian, each with its own evidence lane and a specialisation from the brief's deliverable), writes every member's prompt for each round (independent positions, cross-examination, scored vote), validates and fingerprints each answer, refuses secrets, and computes a Borda verdict with recorded dissent, warnings and a SHA-256 receipt. It never calls a model: Claude runs the members as separate agents, or labels them COUNCIL_SIMULATED. | `python3 scripts/council.py plan "اعمل ريلز دعاء" --dir out/demo/council --options A,B,C` | tested-here |
| `see-pro-cognitive-gate` | Validates cognitive-packet metadata: bounded SEE method packs, typed capability handoffs, genuinely distinct A/B/C planning keys, evidence provenance, deterministic numeric checks, cross-company isolation, and receipt-based truth for Full Pro execution and Council reviewer counts. | `python3 scripts/see_pro_cognitive_gate.py --self-test` | tested-here |
| `capability-mindmap` | Orders every superpower by task stage (understand, plan, create, refine, assemble, verify, deliver), builds stage plans for any request and 12 ready task maps with Mermaid flowcharts, and audits same-name groups, twins, cross-superpower look-alikes and pairs to develop together. | `python3 scripts/capability_mindmap.py build` | tested-here |
| `charter-ingest` | Deterministically parses the user's charter roster (sectors «القطاع N», numbered entries with الدور/المهام/الخصائص) into data/experts_500.json (kosif.experts-index.v1): every entry keeps its role, tasks and traits, maps by keywords to catalog families, and is flagged (boilerplate traits, duplicate_of, sensitive consent/regulated). Refuses unless 50 sectors × 10 entries (or --allow-partial) and refuses credential-like text. The council's plan consults it as an index; no persona runs, votes or counts as evidence. | `python3 scripts/charter_ingest.py roster.txt --out data/experts_500.json` | tested-here |
| `business-workflows` | Searches Futurepedia's business adoption index and 64 workflow playbooks (36 library + 28 creator), re-routes every step from the named third-party tool to what Claude can do in the session or to a connector, measures native coverage, and writes an Arabic runbook with approval gates for send, post, spend and recording. | `python3 scripts/business_workflows.py functions` | tested-here |
| `book-methods` | Searches 45 methods distilled in our own words from ten uploaded PDFs (lateral-thinking course, The Pragmatic Programmer, Jaynes's Bayesian framework, the Cambridge Handbook of Personality Psychology, an IFRS/ISA accounting skill report, the owner's KOSIF v8 prompt spec, Shawqi's diwan, two English coursebooks), and runs five helpers: seeded random-word provocation, a Bayesian posterior with a decibel evidence ledger, a prompt clarity/context/specificity gate, a journal-entry checker (balance, integer minor units, VAT, duplicates, bank-receipt-is-settlement) and a Big Five character card. | `python3 scripts/book_methods.py search "شخصية حوار"` | tested-here |
| `prompt-lab` | Makes the prompt-craft method runnable for eight kinds of prompt (system, agent brief, code, research, writing, LLM judge, image, video). build renders a kind's slots in order and turns every unfilled required slot into a question; lint scores a prompt out of 20 (required slots present, anti-patterns such as vague or shouted words, hype tokens and negative-heavy rules, in English and Arabic) with hard gates for a secret, a chain-of-thought request or undelimited pasted data; refine orders the fixes and prints the missing-slot skeleton; eval runs deterministic assertions on saved outputs and keeps a variant only when it beats the baseline with no regression; pairwise prints order-swapped judge prompts and counts only verdicts that agree in both orders, the way the owner's Jev service judges. | `python3 scripts/prompt_lab.py kinds` | tested-here |

<!-- hub:area:think:end -->

## الفهرس / contents

0. [The front door: hub.py](#the-front-door-hubpy)
1. [Claude Code permission-aware local-first bootstrap](#claude-code-permission-aware-local-first-bootstrap)
2. [Original bilingual task-to-capability finder](#original-bilingual-task-to-capability-finder)
3. [Capability Atlas — start here for every substantial task](#capability-atlas--start-here-for-every-substantial-task)
4. [أطلس الـ5000 مهارة — what Claude knows from the Atlas and what it could still learn](#أطلس-الـ5000-مهارة--what-claude-knows-from-the-atlas-and-what-it-could-still-learn)
5. [اختر قدرة حقيقية واعرف صلاحياتها — Capability runtime routing](#اختر-قدرة-حقيقية-واعرف-صلاحياتها--capability-runtime-routing)
6. [مراجع أخرى / other references](#مراجع-أخرى--other-references)
7. [العقل الفائق والمستلزمات والخريطة — Cognition, requirements, graph](#العقل-الفائق-والمستلزمات-والخريطة--cognition-requirements-graph)
8. [KOSIF Innovation lab — invention candidates](#kosif-innovation-lab--invention-candidates)
9. [KOSIF Superpowers Ultimate — integrated obra/superpowers v7 process layer (2026-10-19)](#kosif-superpowers-ultimate--integrated-obrasuperpowers-v7-process-layer-2026-10-19)

## The front door: hub.py

`scripts/hub.py` joins every finder in this skill into one answer, so Claude does not have to remember which of the older routers to call.

```bash
python3 scripts/hub.py find "حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي"   # tools to run + powers + guides (+ styles)
python3 scripts/hub.py find "render a spinning cube without blender" --json  # the same for apps and agents
python3 scripts/hub.py tool reference-edit-engine                             # commands, requirements here, safety, tests, limits
python3 scripts/hub.py doctor                                                 # which tools run on this machine, which installs unlock most
```

How `find` ranks: the task's words (Arabic is normalised: hamza forms, ta marbuta, clitics like و/ال/بال) are matched against each tool's `keywords` and `use_when` requests (strong) and its summary and commands (weaker) in `data/tools.json`; tools whose families match the catalog powers that `powers.py suggest` picks for the same task get a boost, as do tools named by a `data/capability_routes.json` alias; tested tools win ties. The powers list is exactly `powers.py suggest`; the guides list matches titles and headings of `references/guides/*.md` and `references/*.md`.

The older finders still work and answer narrower questions: `powers.py suggest` (catalog only), `capability_atlas.py plan` (catalog with source hashes and requirement states), `capability_runtime_router.py --task` (22 runnable routes with permission ledgers), `ai_tool_discovery.py` (bilingual ranker), `superpowers_unified.py plan` (process skills: how to work).

## Claude Code permission-aware local-first bootstrap

**Do NOT require git clone before using this skill.** If Claude Code Auto Mode denies 'Code from External', do not bypass the permission classifier. Run the already-installed local script: python scripts/local_first.py doctor and python scripts/local_first.py search silhouette --scope powers from this skill's root (or use the full relative path under the repo root). A complete local checkout also supports --scope styles; standalone skills honestly report that the full style index is unavailable. If the skill isn't installed and access is blocked, request explicit user authorization or a supplied package instead of using an alternative tool to secretly clone. Read [the auto-mode recovery guide](../claude-auto-local-first.md) and [evidence audit](../rea-ghidra-catalog-audit-20261019.md). For catalog health, run python scripts/catalog_evidence_audit.py: every catalog record is assessed for local link coverage but NOT executed.

## Original bilingual task-to-capability finder

For a task like "تحريك شخصيات فيديو" or "video animation", the local-only
discovery algorithm scripts/ai_tool_discovery.py ranks existing KOSIF capabilities.
Run python scripts/ai_tool_discovery.py "تحريك شخصيات فيديو" --top 8.
The algorithm retains proof/requirements caveats and never treats catalog status
as actual runtime verification. No third-party ranking algorithm is copied.
See [REA website investigation](../taaft-rea-discovery-audit.md).

## Capability Atlas — start here for every substantial task

Use the **generated bilingual capability index** at [references/capability-atlas.md](../capability-atlas.md). Run `python scripts/capability_atlas.py plan "<user task>" --json` to select source-backed capability IDs, requirements, workflow skills and suggested execution routes. Drill into a selected ID with `python scripts/capability_atlas.py show <ID> --json`; run `doctor --json` to detect a stale index and `build` after catalog edits. Never treat catalog status as confirmation of live execution or silently install dependencies. See the full protocol in the guide.

## أطلس الـ5000 مهارة — what Claude knows from the Atlas and what it could still learn

The safe core of KOSIF Atlas (5,116 skills: READ_ONLY_OK, permissive license, no risk flags) is mapped against the catalog by `python3 scripts/atlas_5000.py`. `stats` shows per-theme coverage, `gaps` lists the themes with the most skills not yet distilled and the next candidates, `find "<task>"` shows matching Atlas skills with the power that already covers each (`--uncovered` for the rest), and `show <id>` prints one record. Covered means a power cites the Atlas folder, never that the skill ran. The 2026-10-23 batch, sources and boundaries are in [atlas-5000-mining-20261023.md](../atlas-5000-mining-20261023.md).

The wider question, what happened to every one of the 14,793 Atlas skills, is answered by `python3 scripts/atlas_ledger.py`. Each skill has one status: covered (a power cites it), pattern (one vendor's copy of a method a power already holds), duplicate, excluded-review, excluded-copyleft, excluded-risk, or pending (safe, unique, not yet decided). `stats` gives the counts, `show <id>` one skill, and `list --status pending --theme <theme>` the next batch. REA's hash receipt for the whole Atlas is `proofs/atlas-rea/receipt.json`; the pass and its numbers are in [atlas-ledger-20261023.md](../atlas-ledger-20261023.md).

## اختر قدرة حقيقية واعرف صلاحياتها — Capability runtime routing

**المعرفة لا تكفي: شغّل موجّه القدرات.** أي مهمة صوت، رسم، موشن، كاتانا، تحليل مستودع، تطبيق، بحث أو مراجعة تبدأ بمطابقة الطلب مع قدرة مثبتة في الشفرة؛ شخّص البيئة والصلاحيات أولًا:

    python3 $SKILL_DIR/scripts/capability_runtime_router.py --task "حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي" --json
    python3 $SKILL_DIR/scripts/capability_runtime_router.py --doctor --json
    python3 $SKILL_DIR/scripts/capability_runtime_router.py --id reference-edit-remix --json

اقرأ دليل [Capability Operating Manual](../capability-operating-manual.md) لخطوات التشغيل الفعلية: تحليل الفيديو وتوقيت القطعات، الصوت وتوقيته، إنشاء مشروع مونتاج، تحريك SVG، فحص Python/الحزم، اختبار جودة القرار، صلاحيات أجهزة المستخدم، والسماح بالتثبيت والرفع والتوليد المدفوع. النتائج تقول صراحة **source_present_not_executed** أو **missing_host_prerequisites** أو **external_not_integrated**؛ لا تعني إمكانية تشغيل نموذج خارجي، امتلاك مفتاح أو موافقة مستخدم. سجل الحقوق ورخص المصدر، وشغّل الأداة وحقق الناتج قبل إعلان الإنجاز. لا تنسخ Katana ولا تعامل وجود روابط GitHub على أنه دمج المكتبات أو تدريب Claude.

## مراجع أخرى / other references

- [environment.md](../environment.md) — لقطة مؤرخة لهذه الحاوية من `probe_env.py`. أعد توليدها: `python3 $SKILL_DIR/scripts/probe_env.py --write $SKILL_DIR/references/environment.md`.
- [arsenal-general.md](../arsenal-general.md) — 139 مكتبة عامة بإصداراتها ورخصها وما فُحص منها، ودروس «واجهات بيانات التدريب قديمة». [arsenal-libraries.md](../arsenal-libraries.md) — مكتبات الموشن.
- [method-packs.md](../method-packs.md) — طرق البحث بالأدلة، والتقييم والثقة، والمال والبيانات، واستراتيجية المنتج، وعقود الوكلاء.
- [ecc-harness.md](../ecc-harness.md) و[ecc-skills-index.md](../ecc-skills-index.md) — خلاصة Everything Claude Code (MIT) وفهرس مهاراته الـ311.
- [graphify.md](../graphify.md) — فهم أي مستودع أو مجموعة مهارات بسرعة برسم معرفي (محليًا أو عبر Graphify MCP).
- [humanizer.md](../humanizer.md) — كتابة عربية وإنجليزية بلا علامات آلية، مع حراسة الحقائق؛ أداتاه `scripts/tell_scan.py` و`scripts/anchor_gate.py`.
- [external-skills.md](../external-skills.md) · [cinematic-director-pro.md](../cinematic-director-pro.md) · [video-download.md](../video-download.md) — مصادر المالك للموشن والتحميل.
- [proofs/README.md](../../proofs/README.md) — أفلام الإثبات وملفات الإثبات العامة. `data/powers/*.json` و`data/styles.json` — البيانات الخام.

## العقل الفائق والمستلزمات والخريطة — Cognition, requirements, graph

- **التفكير / thinking:** [cognition.md](../cognition.md) يحوّل «فكّر جيدًا» إلى إجراءات: سلّم L0–L6، حلقة الخبير، عشر عادات للعبقرية، خط تطوير الفكرة بثماني مراحل، التخطيط، القرار، التفكير الشبيه بالبشر، المراقبة الذاتية. المحرك `scripts/think.py`: `ladder` · `frame` · `models` (63 نموذجًا ذهنيًا) · `plan` · `ideas` · `decide` (مع الحساسية) · `fermi` · `critic`. العائلتان الجديدتان: [mental-models](../powers/mental-models.md) MODEL و[planning-execution](../powers/planning-execution.md) PLAN.
- **المستلزمات / requirements:** كل قدرة لها حقل `requires` من سجل [requirements.json](../../data/requirements.json) (أدوات، حزم، مفاتيح، منصات، خطوط، نماذج). `requirements.py for <ID>` قائمة قدرة واحدة؛ `requirements.py plan "<المهمة>"` قائمة المهمة كلها مع ▶ لما يبدأ الآن؛ الفهرس المقلوب: [requirements.md](../requirements.md).
- **الخريطة المترابطة / graph:** [capability-graph.html](../capability-graph.html) تربط المجالات ← العائلات ← المستلزمات والسكربتات والاختبارات؛ طبقة الكود من Graphify ([graphify_code_layer.json](../../data/graphify_code_layer.json)) ومراجعة محلية بالـAST. `python3 $SKILL_DIR/scripts/capability_graph.py build`.
- **اختبار API / Bruno:** عائلة [api-testing](../powers/api-testing.md) API تبني مجموعات طلبات كملفات git وتشغّلها كاختبارات قبول (تأكيدات، Chai، بيانات CSV، تقارير JUnit، بوابة فشل CI، استيراد OpenAPI، تحويل Postman) — 15 قدرة مُثبتة بتشغيل Bruno CLI 4.2.1 هنا: [bruno-api](../../proofs/bruno-api/README.md).
- **حزام الأدوات الموسَّع / extended toolbelt:** 42 قدرة جديدة (رياضيات رمزية وبراهين، SQL وجداول سريعة، تعلم آلة وتنبؤ، تحسين وجدولة، جغرافيا وكيمياء وأحياء، زحف واستخراج، تحليل مستندات، شرائح ومخططات بالكود، تدوين موسيقي، رؤية حاسوبية، CAD، إمكانية الوصول، فحص أمني، اختبارات خصائص، ترجمة ومعالجة عربية، RAG وMCP)؛ 20 منها شُغّلت فعلًا: [toolbelt-smoke](../../proofs/toolbelt-smoke/README.md).

## KOSIF Innovation lab — invention candidates

When asked to invent, brainstorm or design a new capability, consult [50 repository research index](../font-innovation-50.md) and generate falsifiable engineering candidates with `scripts/invention_lab.py invent "problem statement" --count 15`; evaluate prototypes against a baseline and include kill criteria. These are **unverified ideas**, not patent-clearance or expert-council results.

## KOSIF Superpowers Ultimate — integrated obra/superpowers v7 process layer (2026-10-19)

**KOSIF remains the canonical master and full capability map.** We additionally bundle all 15 original MIT-licensed obra/superpowers v7.0.0 process skills as *methods*, not alternative capability inventories. A process skill determines **how to work**; KOSIF determines **what can actually be executed** with verified tools in this session. Preserve all existing KOSIF families, badges, media editors, source catalogs, and execution rules.

**Mandatory discovery when the task is substantial:** initialize KOSIF with `boot.py`, `probe_env.py` and `powers.py suggest "<task>"`, then run:
```bash
python $SKILL_DIR/scripts/superpowers_unified.py doctor
python $SKILL_DIR/scripts/superpowers_unified.py plan "<user task, verbatim>"
```
Read the suggested original process skill's `SKILL.md` from `vendor/obra-superpowers-v7/skills/<skill-name>/SKILL.md` and follow its methodology when applicable. Use `brainstorming` for new designs, `writing-plans` for implementation plans, `systematic-debugging` for failures, `test-driven-development` for coding, `requesting-code-review` for appropriate reviews and `verification-before-completion` before reporting successful completion. Keep the KOSIF capability router and original user permissions in force.

The bundled 15 process skills are installed alongside the KOSIF main skill for Claude Code discovery via an explicitly invoked `superpowers_unified.py install`. Existing unrelated user skills are preserved; name conflicts are skipped unless separately authorized and backed up. Details, provenance, commands and rollback: [Superpowers unification](../superpowers-unification.md).

**Do not confuse vendor source presence with actual installation, invocation, or proven task execution. No paid tools, outside publication, system-wide installs or external media uploads without authorization.**

## Owned repositories — reuse what the owner already built

Before building a capability from scratch, check whether one of the owner's own repositories already has it: `python3 scripts/owned_repos.py find "<task>"` (from the skill folder). `skills` prints, per capability group, what Claude has now (✅ proven + 🟢 ready), the methods it applies directly, what becomes available after an install or a key, and which owned repos are still `learnable`. The full table, relations and findings live in [owned-repos-map.md](../owned-repos-map.md). To refresh after the account changes: shallow-clone the repos outside the repository, run `digest` then `merge`, `render` and `verify`. Private repositories stay counts-only in this public skill.
