# أدوات المجال `think` (11 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `anchor-gate` — بوابة حفظ الحقائق عند إعادة الصياغة / Rewrite Fact Anchor Gate

| الحقل | القيمة |
|---|---|
| المسار | `scripts/anchor_gate.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `writing-humanizer`, `prompt-craft`, `arabic-language`, `qa-verification` |

**ما تفعله:** يقارن النص قبل إعادة الصياغة وبعدها (بالعربية والإنجليزية) ويعرض كل مرتكز حقائقي حُذف أو أُضيف: الاقتباسات، والأرقام بالأرقام أو بالحروف، والعملات، والشهور، وأيام الأسبوع، وعناوين البريد، والروابط، والمسارات، والحسابات، والإصدارات، والنسب والأوقات، والأسماء التي يجب أن تبقى، ثم يعطي النتيجة PASS أو REVIEW_REQUIRED.

**What it does:** Compares a text before and after a rewrite (English and Arabic) and reports every factual anchor that was dropped or added (quotes, numbers in digits or words, currencies, months, weekdays, emails, URLs, paths, @handles, versions, ratios/times and must-keep names), returning PASS or REVIEW_REQUIRED.

#### متى تُستدعى

- «اتأكد إن إعادة الصياغة ما غيرتش أي رقم أو اسم أو تاريخ»
- «تحقق أن البرومبت المحسّن ما ضيّع تفاصيل طلبي الأصلي»
- «قارن النص الأصلي بالنسخة المعدلة وقل لي وش انحذف من الحقائق»
- «check that my rewrite kept every number, name and link»
- «verify the optimized prompt didn't drop any of the user's details»
- «gate a humanized draft so no facts were invented or lost»

#### الأوامر

- **rewrite (files)**: Default rewrite mode: PASS only if nothing was dropped and nothing was added. --text prints a one-line summary instead of JSON. Exits 0 on PASS, 2 on REVIEW_REQUIRED.
  - `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/en_before.txt --after proofs/general-writing/pairs/en_after_drift.txt --text`
- **--keep (must-keep names file)**: Adds terms (one per line) that must survive; they are counted by presence, not by count. Prints the JSON report.
  - `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/cafe_before.txt --after proofs/general-writing/pairs/cafe_after.txt --keep proofs/general-writing/pairs/cafe_keep.txt`
- **inline text + --keep-term**: Compares inline strings; --keep-term can be repeated.
  - `python3 scripts/anchor_gate.py --before-text "قابلنا أحمد يوم الخميس" --after-text "قابلنا محمود يوم الجمعة" --keep-term أحمد --text`
- **--mode prompt**: Prompt mode: PASS when nothing was dropped; additions are listed for review (for checking an optimized prompt against the user's raw prompt).
  - `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/prompt_raw.txt --after proofs/general-writing/pairs/prompt_good.txt --mode prompt --text`
- **stdin**: Reads one side from stdin ('-'); giving '-' for both sides is a usage error (exit 64).
  - `cat proofs/general-writing/pairs/en_after_good.txt \| python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/en_before.txt --after - --text`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: It only checks that surface anchors survived, so a PASS does not prove that meaning, tone, attribution or unlisted names were preserved.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py`
- مرجع: `.claude/skills/kosif-superpowers/references/humanizer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/prompt-optimizer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/verification.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/writing-humanizer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/prompt-craft.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/arabic-language.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:anchor-gate --evidence <ملف>`.

### `architecture-sizer` — مقدّر سعة الأنظمة / System Capacity Sizer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/architecture_sizer.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `code-engineering`, `planning-execution` |

**ما تفعله:** يحسب تقديرًا تقريبيًا حتميًا لسعة النظام (متوسط الطلبات في الثانية وذروتها، والحد الأدنى من النسخ المتماثلة، والتخزين المنطقي والمكرَّر بالبايت والجيبيبايت) انطلاقًا من افتراضات الحِمل والعتاد التي يقدّمها المستخدم، وبحساب عشري دقيق.

**What it does:** Computes a deterministic back-of-envelope capacity estimate (average and peak RPS, minimum replicas, logical and replicated storage in bytes and GiB) from caller-supplied traffic and hardware assumptions, using exact decimal arithmetic.

#### متى تُستدعى

- «احسب لي كم سيرفر محتاج لو عندي مليون طلب في اليوم»
- «قدّر مساحة التخزين المطلوبة لمدة الاحتفاظ دي»
- «كم نسخة نحتاج للخدمة وقت الذروة؟»
- «estimate replicas and storage for 10M requests per day»
- «do a back-of-envelope system design sizing»
- «how much storage for 30-day retention with 2 copies»

#### الأوامر

- **size**: Prints JSON with status, the echoed inputs, average_rps, peak_rps, peak_rps_ceiling, minimum_replicas, logical_storage_bytes, retained_storage_bytes, storage_gib, assumptions, exclusions, executed_benchmark=false and source_reference.
  - `python3 scripts/architecture_sizer.py --daily-requests 86400 --peak-factor 5 --payload-bytes 1000 --retention-days 7 --replica-rps 100 --target-utilization 0.5 --copies 2`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Linear arithmetic on assumed numbers only; it runs no load test and leaves out indexes, log overhead, backups, compression, burst shape, network, CDN, failover headroom and regional placement.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_system_python.py`
- مرجع: `.claude/skills/kosif-superpowers/references/community-source-atlas.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:architecture-sizer --evidence <ملف>`.

### `book-methods` — مناهج مستخلصة من الكتب: التفكير الجانبي والهندسة العملية والأدلة البايزية والشخصية وفحوص المحاسبة ووضوح البرومنت / Book-distilled methods: lateral ideas, pragmatic engineering, Bayesian evidence, personality, accounting checks, prompt clarity

| الحقل | القيمة |
|---|---|
| المسار | `scripts/book_methods.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `planning-execution`, `qa-verification` |

**ما تفعله:** يبحث في 45 منهجًا مستخلصًا بكلماتنا من عشرة ملفات PDF، ويشغّل خمسة مساعدين: كلمات عشوائية محفّزة، وحساب بايزي بسجل أدلة بالديسيبل، وبوابة وضوح البرومنت، وفاحص قيود محاسبية، وبطاقة شخصية بالعوامل الخمسة.

**What it does:** Searches 45 methods distilled in our own words from ten uploaded PDFs (lateral-thinking course, The Pragmatic Programmer, Jaynes's Bayesian framework, the Cambridge Handbook of Personality Psychology, an IFRS/ISA accounting skill report, the owner's KOSIF v8 prompt spec, Shawqi's diwan, two English coursebooks), and runs five helpers: seeded random-word provocation, a Bayesian posterior with a decibel evidence ledger, a prompt clarity/context/specificity gate, a journal-entry checker (balance, integer minor units, VAT, duplicates, bank-receipt-is-settlement) and a Big Five character card.

#### متى تُستدعى

- «أعطني أفكار غير تقليدية لإعلان»
- «افحص وضوح هذا البرومنت قبل التوليد»
- «تأكد أن القيود متوازنة وأن التحصيل ليس إيرادًا»
- «Build a character's voice from a Big Five profile»
- «Weigh this evidence with Bayes in decibels»

#### الأوامر

- **search**: Arabic/English method search.
  - `python3 scripts/book_methods.py search "شخصية حوار"`
- **rest**: Seeded random-word provocation in four modes.
  - `python3 scripts/book_methods.py rest --problem "إعلان لمقهى" --seed 7`
- **bayes**: Posterior and decibel evidence ledger.
  - `python3 scripts/book_methods.py bayes --h fraud=0.01 --h ok=0.99 --e "flag:fraud=0.9,ok=0.05"`
- **clarity**: Clarity/context/specificity score; exit 3 = REVISE.
  - `python3 scripts/book_methods.py clarity "صورة جميلة لشخص"`
- **ledger**: Draft journal-entry checks; exit 1 on an error.
  - `python3 scripts/book_methods.py ledger --file entries.json --revenue 4101 --receivable 1201`
- **persona**: Character card with speech rules and if-then signatures.
  - `python3 scripts/book_methods.py persona --name سارة --big5 O=4,C=2,E=5,A=2,N=3`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: Reads only the given files and prints JSON; generates no media, posts no entry and profiles no real person.
- الحدود: Methods are summaries, not the books; clarity is a word-list heuristic; ledger is a draft check, not posting or an audit opinion; persona is for fiction and tone only.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_book_methods.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A20-book-distilled-methods.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:book-methods --evidence <ملف>`.

### `business-workflows` — الذكاء الاصطناعي في الأعمال: 9 وظائف و64 خطة عمل بخطط تشغيل لClaude / AI for business: 9 functions, 64 workflows, Claude-native gated runbooks

| الحقل | القيمة |
|---|---|
| المسار | `scripts/business_workflows.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `planning-execution`, `agent-orchestration` |

**ما تفعله:** يبحث في مؤشر تبني الذكاء الاصطناعي لـ9 وظائف و64 خطة عمل، ويعيد توجيه كل خطوة إلى ما ينفذه Claude بنفسه أو إلى موصّل، ويكتب خطة تشغيل عربية ببوابات موافقة.

**What it does:** Searches Futurepedia's business adoption index and 64 workflow playbooks (36 library + 28 creator), re-routes every step from the named third-party tool to what Claude can do in the session or to a connector, measures native coverage, and writes an Arabic runbook with approval gates for send, post, spend and recording.

#### متى تُستدعى

- «اعمل لي workflow للمبيعات بالذكاء الاصطناعي»
- «أي أداة ذكاء اصطناعي أستخدم في التسويق»
- «Turn a podcast into a content plan with AI»
- «Plan an AI workflow for my sales team»

#### الأوامر

- **functions**: Business functions by adoption with matching workflows.
  - `python3 scripts/business_workflows.py functions`
- **search**: Arabic/English workflow search.
  - `python3 scripts/business_workflows.py search "بودكاست"`
- **coverage**: Native vs connector/approval steps per workflow.
  - `python3 scripts/business_workflows.py coverage`
- **plan**: Writes a gated Claude-native runbook.
  - `python3 scripts/business_workflows.py plan --workflow FW-07 --context "حلقة بودكاست عربية" --out out/biz/plan.md`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only the new --out file; never sends, posts, spends or records; plans mark every such step as needing explicit approval.
- الحدود: Facts only from the site (no prompts); third-party tool features and prices change; connector availability is checked at run time, not here.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_business_workflows.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A18-futurepedia-business-workflows.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:business-workflows --evidence <ملف>`.

### `capability-mindmap` — الخريطة الذهنية المرحلية وتدقيق التكرار / Task-stage capability mind map and duplicate audit

| الحقل | القيمة |
|---|---|
| المسار | `scripts/capability_mindmap.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `planning-execution`, `mental-models` |

**ما تفعله:** يرتب القدرات حسب مرحلة المهمة (افهم، خطّط، اصنع، حسّن، ارندر، تحقّق، سلّم)، ويبني خطة مرحلية لأي طلب و12 خريطة جاهزة، ويدقق التكرار والتشابه والأزواج التي تتطور معًا.

**What it does:** Orders every superpower by task stage (understand, plan, create, refine, assemble, verify, deliver), builds stage plans for any request and 12 ready task maps with Mermaid flowcharts, and audits same-name groups, twins, cross-superpower look-alikes and pairs to develop together.

#### متى تُستدعى

- «رتب القدرات في خريطة ذهنية لمهمتي»
- «Give me a stage-by-stage plan for a beat-synced reel»
- «فين القدرات المكررة اللي ممكن نوحدها؟»

#### الأوامر

- **build**: Writes data/capability_mindmap.json, references/capability-mindmap.md and references/capability-audit.md.
  - `python3 scripts/capability_mindmap.py build`
- **task**: Stage plan for a ready task map id or any free-text request (--mermaid for a flowchart).
  - `python3 scripts/capability_mindmap.py task reels-edit`
- **audit**: Duplicate and merge summary.
  - `python3 scripts/capability_mindmap.py audit`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: build overwrites its generated files only
- الحدود: Stage classification is keyword-based; accurate for motion and editing, weaker for thinking powers.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_capability_mindmap.py`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-mindmap.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-audit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:capability-mindmap --evidence <ملف>`.

### `charter-ingest` — إدخال قائمة الميثاق: مجلس الخبراء 500 فهرسًا للاستشارة / Charter roster ingest: the 500-expert council as a consultable index

| الحقل | القيمة |
|---|---|
| المسار | `scripts/charter_ingest.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `agent-orchestration`, `qa-verification`, `security-safety` |

**ما تفعله:** يحوّل قائمة مجلس الخبراء في ميثاق المستخدم بنتيجة حتمية إلى فهرس data/experts_500.json: لكل بطاقة دورها ومهامها وخصائصها وعائلات الكتالوج المناسبة، وأوسام العام المكرر والدور المكرر والحساس (موافقة/منظَّم). يرفض ما لم يكن 50×10 (إلا مع --allow-partial) ويرفض الأسرار. المجلس يستشيره فهرسًا؛ لا تُشغَّل بطاقة ولا تصوّت ولا تُعدّ دليلًا.

**What it does:** Deterministically parses the user's charter roster (sectors «القطاع N», numbered entries with الدور/المهام/الخصائص) into data/experts_500.json (kosif.experts-index.v1): every entry keeps its role, tasks and traits, maps by keywords to catalog families, and is flagged (boilerplate traits, duplicate_of, sensitive consent/regulated). Refuses unless 50 sectors × 10 entries (or --allow-partial) and refuses credential-like text. The council's plan consults it as an index; no persona runs, votes or counts as evidence.

#### متى تُستدعى

- «حوّل قائمة الخبراء الـ500 في الميثاق لفهرس»
- «Index my 500-expert charter roster for the council»

#### الأوامر

- **ingest**: Parses the roster text and writes the flagged index with a receipt (sectors, experts, boilerplate, duplicates, consent, regulated); exit 2 on a wrong shape or credentials.
  - `python3 scripts/charter_ingest.py roster.txt --out data/experts_500.json`
- **council-consult**: Records up to 3 consulted persona cards per member in council.json consulted_index; the verdict says 'index consulted: N personas'.
  - `python3 scripts/council.py plan "<request>" --dir out/demo/council --roster data/experts_500.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only the --out file; runs no model, spends nothing, publishes nothing.
- الحدود: Keyword flags and family mapping are heuristic (light Arabic stemming); the index is persona cards, not executed experts, and never enters the coverage receipt or the powers count.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_charter_index.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A13-pro-council.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:charter-ingest --evidence <ملف>`.

### `council` — مجلس البرو: خمسة أعضاء متعارضين وثلاث جولات وحكم بالدرجات / Pro Council: five opposing members, three rounds, a scored verdict

| الحقل | القيمة |
|---|---|
| المسار | `scripts/council.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `agent-orchestration`, `planning-execution`, `verification-evals` |

**ما تفعله:** يخطط لمجلس من خمسة أعضاء متعارضين (المبتكر، محامي الشيطان، المهندس العملي، صوت الجمهور، الحارس)، لكل منهم مسار أدلة مختلف وتخصص حسب مخرج الطلب، ويكتب مطالبة كل عضو في كل جولة (مواقف مستقلة، استجواب متبادل، تصويت بالدرجات)، ويتحقق من كل رد ويبصمه ويرفض الأسرار، ثم يحسب حكمًا بطريقة بوردا مع الرأي المخالف والتحذيرات وإيصال SHA-256. لا يستدعي أي نموذج: Claude يشغّل الأعضاء وكلاء منفصلين، أو يسميهم COUNCIL_SIMULATED.

**What it does:** Plans a five-member adversarial council for a request (Visionary, Skeptic, Builder, Audience, Guardian, each with its own evidence lane and a specialisation from the brief's deliverable), writes every member's prompt for each round (independent positions, cross-examination, scored vote), validates and fingerprints each answer, refuses secrets, and computes a Borda verdict with recorded dissent, warnings and a SHA-256 receipt. It never calls a model: Claude runs the members as separate agents, or labels them COUNCIL_SIMULATED.

#### متى تُستدعى

- «اعمل مجلس خمسة يتناقشوا في الفكرة دي قبل ما تقرر»
- «وضع البرو: عايز نقاش بين آراء متعارضة»
- «Run a five-member adversarial council on these three plans»
- «Debate this decision with opposing experts and give me the verdict and the dissent»

#### الأوامر

- **plan**: Writes council.json: five members with stances, evidence lanes and a specialisation, the options and the session rules.
  - `python3 scripts/council.py plan "اعمل ريلز دعاء" --dir out/demo/council --options A,B,C`
- **prompts**: Writes prompts_r<N>.json with one prompt per member; round 2 and 3 include the earlier rounds and refuse to run before the previous round is complete.
  - `python3 scripts/council.py prompts --dir out/demo/council --round 1`
- **ingest**: Validates one member's JSON answer for a round, refuses secrets, fingerprints it and records it (--simulated marks a voice written in Claude's own context).
  - `python3 scripts/council.py ingest --dir out/demo/council --round 1 --member M1 --file m1.json`
- **status**: Shows which members answered which rounds.
  - `python3 scripts/council.py status --dir out/demo/council`
- **verdict**: Sums round-3 scores per option, records the dissent and warnings (NO_DISSENT, CLOSE_CALL, WEAK_EVIDENCE), and writes verdict.json and minutes.md with a SHA-256 receipt.
  - `python3 scripts/council.py verdict --dir out/demo/council`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only inside the --dir folder; it runs no model, spends nothing and publishes nothing.
- الحدود: The council's quality depends on the members Claude runs; the script checks structure, evidence fields and votes, not whether an argument is correct, and a council without separate agents is only COUNCIL_SIMULATED.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_council.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A13-pro-council.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:council --evidence <ملف>`.

### `invention-lab` — مختبر الابتكار الهندسي / Invention Lab Candidates

| الحقل | القيمة |
|---|---|
| المسار | `scripts/invention_lab.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `creativity-engine`, `thinking-core`, `planning-execution` |

**ما تفعله:** يحوّل وصف مشكلة واحدة إلى قائمة JSON مرتّبة وقابلة لإعادة الإنتاج من أفكار هندسية قابلة للتفنيد (16 طريقة ابتكار على نهج TRIZ × 4 زوايا)، لكل فكرة فرضية واختبار ومقياس نجاح وحدّ للرفض.

**What it does:** Turns one problem statement into a reproducible, ranked JSON list of falsifiable engineering ideas (16 TRIZ-style inventive methods × 4 lenses), each with a hypothesis, test, success metric and rejection threshold.

#### متى تُستدعى

- «اقترح لي حلول مبتكرة لمشكلة بطء الترجمة على الموبايل»
- «عايز أفكار جديدة لتحسين الأداة دي مع معايير نجاح واضحة»
- «ابغى أفكار هندسية قابلة للاختبار لمشكلة عندي»
- «brainstorm falsifiable engineering alternatives for this bottleneck»
- «invent options to make our render pipeline more resilient»
- «give me TRIZ-style ideas with kill criteria»

#### الأوامر

- **methods**: Prints the 16 inventive methods (method, technique, suggested experiment) as JSON.
  - `python3 scripts/invention_lab.py methods`
- **invent**: Prints schema kosif-invention-candidates-v1 JSON with up to --count (1-64, default 12) candidates sorted by a deterministic heuristic priority; --constraint is repeatable and the first six values are copied into every candidate's risk field.
  - `python3 scripts/invention_lab.py invent "Make Arabic captions render faster on mobile" --count 12 --constraint "no paid APIs"`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Fills fixed templates from the problem string and ranks them with a SHA-256-seeded heuristic, so it gives no real novelty, feasibility, cost or patent assessment.

#### الاختبارات والأدلة

- `tests/test_invention_lab.py`
- مرجع: `.claude/skills/kosif-superpowers/references/creativity.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:invention-lab --evidence <ملف>`.

### `see-pro-cognitive-gate` — فاحص عقود التفكير والتوليف KOSIF SEE Pro / SEE Pro Cognitive Fusion contract verifier

| الحقل | القيمة |
|---|---|
| المسار | `scripts/see_pro_cognitive_gate.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `planning-execution`, `self-discovery` |

**ما تفعله:** يفحص عقد التفكير المركب: حدود حزم SEE، وتوافق مخارج ومدخلات المهارات، واختلاف معماريات الخطط، وتوثيق الأدلة والحسابات وعزل الشركات، ويمنع وصف Full Pro أو مجلس الخبراء بأنه نُفذ من دون إيصالات طلب حقيقية.

**What it does:** Validates cognitive-packet metadata: bounded SEE method packs, typed capability handoffs, genuinely distinct A/B/C planning keys, evidence provenance, deterministic numeric checks, cross-company isolation, and receipt-based truth for Full Pro execution and Council reviewer counts.

#### متى تُستدعى

- «راجع التوليفة الذكية وتأكد أن بروتوكول SEE Pro ملتزم بشروطه»
- «افحص هل خطة Full Pro أو مجلس الخبراء لها إثبات تشغيل»
- «Validate proposed cognitive packet before executing a composite workflow»

#### الأوامر

- **--self-test**: Runs deterministic in-process shadow checks for Full Pro claim truth, incompatible typed edges, privacy and planning limits.
  - `python3 scripts/see_pro_cognitive_gate.py --self-test`
- **check**: Checks a JSON reasoning packet and emits PASS/HARD_FAIL with concrete contract errors.
  - `python3 scripts/see_pro_cognitive_gate.py check --file .claude/skills/kosif-superpowers/examples/see_pro_cognitive_packet.example.json`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: No approval required; read-only cognitive packet validation.
- الحدود: Metadata consistency check only, not independent proof of artifact quality or external Full Pro availability.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_see_pro_cognitive_gate.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A12-see-pro-cognitive-fusion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:see-pro-cognitive-gate --evidence <ملف>`.

### `tell-scan` — فاحص العبارات الكتابية النمطية / Writing Tell Scanner

| الحقل | القيمة |
|---|---|
| المسار | `scripts/tell_scan.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `writing-humanizer`, `arabic-language`, `qa-verification` |

**ما تفعله:** يفحص النصوص الإنجليزية والعربية (الفصحى والمصرية) بحثًا عن العبارات النمطية التي توحي بالكتابة الآلية وعن بقايا أدوات التوليد، ويعرض كل إشارة مع رقم سطرها وقوتها، ثم يصدر حكمًا عامًا على النص (EDIT/REVIEW/LOOK/LEAVE/CLEAN).

**What it does:** Scans English and Arabic (MSA and Egyptian) prose for stock 'AI-sounding' writing habits and tool leftovers, and reports each hit with its line, strength and an overall verdict (EDIT/REVIEW/LOOK/LEAVE/CLEAN).

#### متى تُستدعى

- «الكلام ده باين عليه مكتوب بالذكاء الاصطناعي؟ افحصه»
- «راجع المقال وطلّع العبارات الآلية قبل ما أنشره»
- «أبغى أعرف وش الجمل اللي تحتاج إعادة صياغة في المسودة»
- «scan this draft for AI writing tells before I publish»
- «check my LinkedIn post for chatbot phrases»
- «make CI fail if the reply text has strong AI tells»

#### الأوامر

- **scan**: Prints a human report per file: verdict, word and sentence stats, then each hit (strength, rule id, line, label, matched text), strongest first.
  - `python3 scripts/tell_scan.py proofs/general-writing/samples/en_ai.txt`
- **scan --json**: Prints a machine-readable JSON report (a list when several files are given) with verdict, families, hits, rhythm stats and notes.
  - `python3 scripts/tell_scan.py proofs/general-writing/samples/en_ai.txt --json`
- **stdin**: Scans text piped on stdin ('-').
  - `cat proofs/general-writing/samples/ar_msa_ai.txt \| python3 scripts/tell_scan.py - --json`
- **--fail-on**: Exits 1 when any file's verdict is at or above the given level (edit, review or look); useful as a gate.
  - `python3 scripts/tell_scan.py proofs/general-writing/samples/en_ai.txt --fail-on review`
- **--include-code / --include-quotes**: Also scans fenced/inline code, URLs and blockquotes, and the inside of quotations (all masked by default).
  - `python3 scripts/tell_scan.py proofs/general-writing/samples/markdown_code.md --include-code --include-quotes`
- **--list-rules**: Prints every rule id (pattern rules H1-H25, X1 and AR1-AR26, with gaps, plus computed rules H7, H8+, H20t, H20+, AR26d, AR26t), its strength and label, then exits.
  - `python3 scripts/tell_scan.py --list-rules`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: A regex-based editing aid that shows where to look; it is not an authorship or AI detector, and it never rewrites text or judges meaning.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py`
- مرجع: `.claude/skills/kosif-superpowers/references/humanizer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/writing-humanizer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/arabic-language.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/general-writing/README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:tell-scan --evidence <ملف>`.

### `think` — محرك التفكير وقوالبه / Thinking engine scaffolds

| الحقل | القيمة |
|---|---|
| المسار | `scripts/think.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `thinking-core`, `mental-models`, `planning-execution`, `creativity-engine` |

**ما تفعله:** يحوّل إجراءات التفكير إلى قوالب نصية قابلة للفحص. يختار مستوى التفكير (L0–L6)، ويكتب عقد المهمة، ويرتّب 63 نموذجًا ذهنيًا، ويصوغ خطة بالتخطيط العكسي، ويبني مصفوفة أفكار من قدرات الكتالوج، ويقيّم قرارًا موزونًا مع اختبار الحساسية، ويجري تقدير فيرمي بطريقة مونت كارلو، ويرصد الصياغات الضعيفة في المسودة. وأضاف USIP v5.4 أربع أدوات استدلال: ترتيب ثمانية أنماط استدلال للمهمة، وتحديث الاعتقاد بنسب الأرجحية مع اختبار حساسية بالتنصيف والمضاعفة، وحكم استمر/حوّل/أوقف/انتظر من عتبات مكتوبة مسبقًا، ودفتر ادعاء ← دليل للمسودة. وأضاف USIP v5.5 أربعة قوالب ذكاء: كشف نوع مخرج الطلب وتصنيف خاناته إلى مملوءة ومفترضة ومسؤولة (بميزانية أسئلة المستوى) وحاجبة، وفحص رسم المهام وحساب ترتيبه ومساره الحرج المتفائل والمتشائم وأبوابه التي لا رجعة فيها، ومعايير الجودة لاثني عشر نوع مخرج مع حكم ناجح/فاشل/ناقص من الإجابات، وسلم التعافي لكل صنف خطأ في FusionForge بميزانية محاولات.

**What it does:** Turns thinking procedures into checkable text scaffolds. It picks a reasoning level (L0–L6), writes a task contract, ranks 63 mental models, drafts a backcast plan, builds an idea matrix from catalog powers, scores a weighted decision with sensitivity, runs a Monte-Carlo Fermi estimate and flags weak wording in a draft. USIP v5.4 adds four reasoning tools: it ranks eight reasoning modes for a task, updates a belief by likelihood ratios with a halve/double sensitivity, gives a GO/PIVOT/KILL/HOLD verdict from thresholds written in advance, and builds a claim-to-evidence ledger for a draft. USIP v5.5 adds four intelligence scaffolds: it detects a request's deliverable kind and sorts its slots into filled, assumed, asked (within the level's question budget) and blocking; checks a task DAG and computes its order, optimistic and pessimistic critical path and one-way doors; prints the quality bar of twelve deliverable kinds and gives PASS, FAIL or INCOMPLETE from answers; and prints the recovery ladder for a FusionForge error class with an attempt budget.

#### متى تُستدعى

- «فكّر بعمق في المهمة دي قبل ما تبدأ»
- «اعطني أفكار مبتكرة لريل الجمعة»
- «Which option should I choose? Run a weighted decision with sensitivity»
- «Estimate the range for users × conversion × price»
- «راجع المسودة وطلّع لي العبارات المبالغ فيها»
- «Plan the course launch over 6 weeks»
- «أي طريقة تفكير تناسب المشكلة دي؟»
- «Update my confidence with these two pieces of evidence»
- «راجع تقريري: أي ادعاء ما عليه دليل؟»
- «افهم طلبي ده: إيه اللي ناقص وإيه اللي تفترضه؟»
- «Check my task plan for cycles and the critical path»
- «What quality checks does a video deliverable need?»
- «الأمر فشل بخطأ، أعمل إيه؟»

#### الأوامر

- **ladder**: Picks the reasoning level L0–L6 from keywords (default L2; tasks over 25 words go to at least L4), prints its steps, and from L4 up the models worth running
  - `python3 scripts/think.py ladder "design a 30-day plan for a course launch"`
- **frame**: Prints a contract template: goal, reader, done-criteria, constraints (numbers pulled from the task), non-goals, unknowns, first probe, plus the powers.py suggest and requirements.py plan commands for the task
  - `python3 scripts/think.py frame "a 15 s reel at 30 fps"`
- **models**: Ranks mental models from data/mental_models.json and prints each one's question, steps, output and pitfall
  - `python3 scripts/think.py models "pricing a new subscription" -n 3 --json`
- **plan**: Backcast plan template: end state, week milestones, WBS skeleton, critical path, pre-mortem, kill criteria
  - `python3 scripts/think.py plan "launch the course" --weeks 6`
- **ideas**: Idea matrix: creative operators paired with nearby and far-domain catalog powers, with each power's requirements
  - `python3 scripts/think.py ideas "Arabic Friday reel" -n 12 --seed 7`
- **decide**: Weighted decision matrix; JSON with totals, winner, margin, robust, and the flips under a ±1 weight change
  - `python3 scripts/think.py decide ./decision.json`
- **fermi**: Monte-Carlo range (log-uniform when lo>0, default 20,000 samples, --seed 7) for an arithmetic factor tree; JSON with p10, p50, p90, mean and samples
  - `python3 scripts/think.py fermi "a*b*c" --range a=1:3 b=10:20 c=0.1:0.3 --samples 2000`
- **critic**: Flags intensifiers, unverified claims, absolutes, vague lists, AI-tell words and bare completion claims, with file:line, and counts the digits in the text
  - `python3 scripts/think.py critic ./draft.md`
- **modes**: Ranks the eight reasoning modes of data/reasoning_modes.json (deductive, inductive, abductive, analogical, causal, systems, lateral, Bayesian) by keyword overlap and prints each one's procedure, trap and check; --json for the records
  - `python3 scripts/think.py modes "why does the render crash" -n 2`
- **bayes**: Bayesian update by likelihood ratios (or --json with priors for several hypotheses): posterior per step, bits per evidence item, the posterior when each ratio is halved or doubled, and with --threshold an ACT/DO_NOT_ACT decision and whether it is robust
  - `python3 scripts/think.py bayes --prior 0.2 --lr "fails on main=4" "one report only=0.5" --threshold 0.5`
- **gate**: Decision gate from go/pivot/kill criteria written before the result: KILL beats PIVOT beats GO, any unobserved go criterion holds, and a one-way door (reversible=false) holds while anything is unobserved and still needs explicit approval on GO; --template prints a starter file
  - `python3 scripts/think.py gate gate.json`
- **audit**: Self-audit: lists every line with a number, strong claim or superlative and no evidence on the same line (a command, link, file path or '(evidence: …)'), then five calibration questions; --strict exits 1 when a claim is unsupported
  - `python3 scripts/think.py audit report.md --strict`
- **intake**: Detects the deliverable kind(s) from data/usip_intelligence.json and lists filled, assumed (with the suggested default), asked (capped by the level's question budget) and blocking slots, and flags spend/publish/personal-data words for the safe default
  - `python3 scripts/think.py intake "اعمل لي ريلز 30 ثانية من صوتي" --level L2`
- **decompose**: Checks a task DAG (unique ids, known deps, no cycle, done and verify on every task, valid [low, high] estimates) and prints the topological order, optimistic and pessimistic critical path, one-way doors and risk-first advice; --template prints an example; exit 0 OK, 1 FIX, 2 invalid
  - `python3 scripts/think.py decompose plan.json`
- **qa**: Prints the quality bar of a deliverable kind (hard and soft checks with the tool that measures each); with answers it returns PASS, FAIL (a hard check failed) or INCOMPLETE (a hard check unmeasured or n/a)
  - `python3 scripts/think.py qa video --answers qa.json`
- **recover**: Prints the diagnose / fix / fallback / escalate ladder for one of the eight FusionForge error classes (guessed from the message when not given) and says STOP when the attempt budget is spent
  - `python3 scripts/think.py recover --message "ModuleNotFoundError: No module named cv2" --attempts 1`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: It produces templates and keyword-based rankings to think with; the blanks (…) still have to be filled and tested, it does not reason about or verify claims by itself, and critic is a plain regex sweep that misses Arabic words written with tanween (جدًا، دائمًا). modes ranks by keywords only, and bayes, gate and audit compute exactly what they are given: the priors, ratios, thresholds and evidence markers are the user's or Claude's judgement.

#### الاختبارات والأدلة

- `tests/test_think.py`
- `tests/test_think_reasoning.py`
- `tests/test_think_intel.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A24-reasoning-modes-decision-gates.md`
- مرجع: `.claude/skills/kosif-superpowers/references/cognition.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `CAPABILITIES.md`
- مرجع: `README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A25-task-intake-clarification.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A26-planning-decomposition.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A27-verification-quality-standards.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A29-failure-recovery.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:think --evidence <ملف>`.

