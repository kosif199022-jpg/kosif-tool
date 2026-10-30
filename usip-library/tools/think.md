# أدوات المجال `think` (21 أداة)

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

### `council` — مجلس البرو: خمسة متعارضين أو مجلس مناسب من 100 شخصية، ثلاث جولات وحكم بالدرجات / Pro Council: five opposing members or a task-fitted council from 100 personas, three rounds, a scored verdict

| الحقل | القيمة |
|---|---|
| المسار | `scripts/council.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `agent-orchestration`, `planning-execution`, `verification-evals` |

**ما تفعله:** يخطط لمجلس من خمسة أعضاء متعارضين (المبتكر، محامي الشيطان، المهندس العملي، صوت الجمهور، الحارس)، لكل منهم مسار أدلة مختلف وتخصص حسب مخرج الطلب، ويكتب مطالبة كل عضو في كل جولة (مواقف مستقلة، استجواب متبادل، تصويت بالدرجات)، ويتحقق من كل رد ويبصمه ويرفض الأسرار، ثم يحسب حكمًا بطريقة بوردا مع الرأي المخالف والتحذيرات وإيصال SHA-256. لا يستدعي أي نموذج: Claude يشغّل الأعضاء وكلاء منفصلين، أو يسميهم COUNCIL_SIMULATED. ومع --seats N (من 5 إلى 15) يُجلس مجلسًا مناسبًا للطلب بحتمية من data/council_100.json: مئة شخصية فريدة مخترعة، عشرون لكل مسار أدلة، لكل منها وصف مفصل وثلاث قدرات خارقة وثلاثة أسئلة توقيع ونقطة عمياء معلنة والدليل الذي تطلبه وخصم مقابل؛ و--personas يختارها بالمعرّف، و--full يُجلس المئة بطلب صريح، والمجالس فوق تسعة ترى ملخص ردود الآخرين، والأمر personas يعرض القائمة ويبحث فيها ويعرض بطاقة.

**What it does:** Plans a five-member adversarial council for a request (Visionary, Skeptic, Builder, Audience, Guardian, each with its own evidence lane and a specialisation from the brief's deliverable), writes every member's prompt for each round (independent positions, cross-examination, scored vote), validates and fingerprints each answer, refuses secrets, and computes a Borda verdict with recorded dissent, warnings and a SHA-256 receipt. It never calls a model: Claude runs the members as separate agents, or labels them COUNCIL_SIMULATED. With --seats N (5-15) it seats a deterministic, task-fitted council from data/council_100.json: 100 unique invented personas, 20 per evidence lane, each with a detailed character, three superpowers, three signature questions, a declared blind spot, the evidence it demands and a counterpart; --personas picks them by id, --full seats all 100 on explicit request, councils above nine see a digest of the other answers, and the personas command lists, searches or shows the roster.

#### متى تُستدعى

- «اعمل مجلس خمسة يتناقشوا في الفكرة دي قبل ما تقرر»
- «وضع البرو: عايز نقاش بين آراء متعارضة»
- «Run a five-member adversarial council on these three plans»
- «Debate this decision with opposing experts and give me the verdict and the dissent»
- «نفّذ بأقصى قوة: اعمل مجلس من الشخصيات المناسبة للطلب ده»
- «Seat a nine-member council from the 100 personas for this decision»
- «مين أنسب شخصيات المجلس لمراجعة الكود ده؟»

#### الأوامر

- **plan**: Writes council.json: five members with stances, evidence lanes and a specialisation, the options and the session rules. --seats N / --personas ids / --full seat personas from the 100-persona roster instead.
  - `python3 scripts/council.py plan "اعمل ريلز دعاء" --dir out/demo/council --options A,B,C`
- **plan --seats**: Seats a task-fitted council of 9 from the 100 personas: the best of each lane first, then the most relevant; deterministic.
  - `python3 scripts/council.py plan "اعمل ريلز موشن عربي" --dir out/demo/council9 --seats 9 --no-roster`
- **prompts**: Writes prompts_r<N>.json with one prompt per member; round 2 and 3 include the earlier rounds and refuse to run before the previous round is complete.
  - `python3 scripts/council.py prompts --dir out/demo/council --round 1`
- **ingest**: Validates one member's JSON answer for a round, refuses secrets, fingerprints it and records it (--simulated marks a voice written in Claude's own context).
  - `python3 scripts/council.py ingest --dir out/demo/council --round 1 --member M1 --file m1.json`
- **status**: Shows which members answered which rounds.
  - `python3 scripts/council.py status --dir out/demo/council`
- **verdict**: Sums round-3 scores per option, records the dissent and warnings (NO_DISSENT, CLOSE_CALL, WEAK_EVIDENCE), and writes verdict.json and minutes.md with a SHA-256 receipt.
  - `python3 scripts/council.py verdict --dir out/demo/council`
- **personas**: Lists the roster (--lane), shows one full persona card (--id P024), or shows which council a request would seat (--find).
  - `python3 scripts/council.py personas --find "راجع أمان الكود" --seats 7`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only inside the --dir folder; it runs no model, spends nothing and publishes nothing.
- الحدود: The council's quality depends on the members Claude runs; the script checks structure, evidence fields and votes, not whether an argument is correct, and a council without separate agents is only COUNCIL_SIMULATED. The 100 personas are invented stance prompts selected by keyword relevance; they add perspectives, not verified expertise, and a full 100-member council is 300 answers.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_council.py`
- `.claude/skills/kosif-superpowers/evals/test_think_models.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A13-pro-council.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A30-council-100.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:council --evidence <ملف>`.

### `decision-math` — رياضيات القرار: نطاقات مونت كارلو ونقطة التعادل وترتيب ICE والقيمة الحالية ونقطة انقلاب القرار / Decision math: Monte Carlo ranges, break-even, ICE, NPV/IRR and flip thresholds

| الحقل | القيمة |
|---|---|
| المسار | `scripts/decision_math.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `atlas-strategy`, `strategy-finance` |

**ما تفعله:** يشغّل محاكاة مونت كارلو ببذرة ثابتة لنموذج ربح بمدخلات مثلثية/منتظمة/طبيعية (P10/P50/P90 واحتمال الخسارة)، ويحسب نقطة التعادل، ويرتب قائمة العمل بطريقة ICE، ويحسب القيمة الحالية الصافية ومعدل العائد الداخلي، ويجد بالتنصيف قيمة الافتراض التي ينقلب عندها القرار.

**What it does:** Runs a seeded Monte Carlo over a profit model with triangular/uniform/normal inputs (P5/P10/P50/P90/P95 and probability of loss), computes break-even units and revenue, ranks a backlog by ICE, computes NPV and IRR by bisection, and finds by bisection the value of one assumption at which the go/no-go decision flips.

#### متى تُستدعى

- «احسب احتمال الخسارة ونطاق الربح للمشروع ده»
- «عند كام وحدة هنغطي التكاليف؟»
- «رتّب الأفكار دي بطريقة ICE»
- «What is the probability this launch loses money?»
- «At what price does this decision flip?»
- «Compute NPV and IRR for these cash flows»

#### الأوامر

- **montecarlo**: P5-P95 profit range, mean, sd and probability of profit below target.
  - `echo '{"inputs":{"price":{"dist":"triangular","low":8,"mode":10,"high":13},"units":{"dist":"uniform","low":800,"high":1200},"cost":{"dist":"normal","mean":6,"sd":0.5},"fixed":2500},"profit":"(price - cost) * units - fixed"}' \| python3 scripts/decision_math.py montecarlo - --runs 20000 --seed 7`
- **breakeven**: Break-even units (exact and rounded up), revenue and contribution margin.
  - `python3 scripts/decision_math.py breakeven --price 25 --fixed 10000 --variable 15`
- **ice**: ICE ranking (impact x confidence x ease, 1-10 each) of a CSV backlog.
  - `printf 'name,impact,confidence,ease\nA,8,7,5\nB,9,9,9\nC,3,4,10\n' \| python3 scripts/decision_math.py ice - --text`
- **npv**: NPV at the rate and IRR by bisection (flags non-unique IRR).
  - `python3 scripts/decision_math.py npv --rate 0.1 --flows -1000,300,400,500`
- **flip**: Value of one input where profit crosses the target, with headroom from the base case.
  - `echo '{"inputs":{"price":{"dist":"triangular","low":8,"mode":10,"high":13},"units":{"dist":"uniform","low":800,"high":1200},"cost":{"dist":"normal","mean":6,"sd":0.5},"fixed":2500},"profit":"(price - cost) * units - fixed"}' \| python3 scripts/decision_math.py flip - --var price`
- **self-test**: Offline self-check.
  - `python3 scripts/decision_math.py --self-test`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Inputs are sampled independently (no correlations); the profit expression allows arithmetic and min/max/abs/round only; flip varies one input with the others at their base values; IRR may be non-unique when flows change sign more than once.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_decision_math.py`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:decision-math --evidence <ملف>`.

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

### `lesson-integrity` — فاحص أرقام الدروس والشروح / Lesson number integrity checker

| الحقل | القيمة |
|---|---|
| المسار | `scripts/lesson_integrity.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `verification-evals`, `apps-artifacts` |

**ما تفعله:** يفحص الأرقام التي يعرضها شرح أو فيديو تعليمي أو إنفوجراف أو درس تفاعلي. values يتحقق من سجل قيم يذكر لكل رقم مصدره والجملة المقتبسة التي تثبته أو ملاحظة فجوة صريحة، ويعيد حساب المجاميع والحواصل المشتقة؛ render يملأ العناصر النائبة {v:id} و{v:id\|dp} و{n:id} في السكربت أو الصفحة ويفشل مغلقًا على قيمة غير موجودة أو فجوة أو وحدة بلا شكل طباعة (و--strict يكشف الأرقام المكتوبة مباشرة في النص)؛ ledger يتحقق من توازن دفتر حفظ (طاقة، ميزانية، وقت) ويعرض الحصص والكفاءة؛ scale يختار سعة عدّاد 1-2-5؛ sprite يفحص قائمة مناطق ملف المؤثرات الصوتية (تداخل، طول الملف، رخصة معتمدة لكل مؤثر). مكتبة Python القياسية فقط، ولا يشغّل شيئًا.

**What it does:** Checks the numbers an explainer, lesson film, infographic or interactive lesson shows. values validates a registry where every value names its source and quotes the supporting sentence, or carries an explicit gap note, and recomputes derived sums and products; render fills {v:id}, {v:id\|dp} and {n:id} placeholders in a script or page and fails closed on an unknown value, a gap or a unit with no print form (--strict also flags numbers typed straight into the text); ledger checks that a conservation ledger (energy, budget, time) balances and reports shares and efficiency; scale picks a 1-2-5 gauge capacity; sprite checks a sound-sprite manifest for overlapping regions, file length and a credited allowed licence per cue. Stdlib only; it runs nothing.

#### متى تُستدعى

- «اتأكد إن كل رقم في سكربت الفيديو التعليمي ليه مصدر»
- «تأكد أن مخطط سانكي للطاقة متوازن وما دخل يساوي ما خرج»
- «check every number in my explainer script has a cited source»
- «check my sound sprite regions and credits before shipping»

#### الأوامر

- **values**: Errors on a number with no source and no gap note, an unknown source ref, a missing quote, a value outside its range or a derived value that no longer matches its parts; warns when the number is not in its quote and for every gap.
  - `python3 scripts/lesson_integrity.py values --registry values.json`
- **render**: Fills the placeholders and writes --out only when there is no error; without --out prints the text.
  - `python3 scripts/lesson_integrity.py render --registry values.json --content script.md --strict --out script.out.md`
- **ledger**: Reports in, out, gap, each output's share and the efficiency of the 'useful' outputs; exits 1 when the ledger does not balance or holds a negative amount.
  - `python3 scripts/lesson_integrity.py ledger --file ledger.json --json`
- **scale**: Prints the smallest 1, 2 or 5 x 10^n capacity the value fills to at most --headroom (default 0.9).
  - `python3 scripts/lesson_integrity.py scale 14.7`
- **sprite**: Checks regions and layers do not overlap, fit the file and that every cue has a credits row under an allowed licence (CC0, CC-BY 4.0, owner, original).
  - `python3 scripts/lesson_integrity.py sprite --manifest sounds.json --credits CREDITS.md --duration 20`
- **self-test**: Runs the 11 built-in checks on synthetic data.
  - `python3 scripts/lesson_integrity.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: render --out writes only that file, and only when every placeholder resolved.
- الحدود: It checks the registry against itself: it cannot tell whether a source is right or whether the quoted sentence really appears in it, it does not solve a physics model or generate challenges, and sprite reads the manifest and credits only, without decoding or measuring the audio. --strict recognises common SI units only.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_lesson_integrity.py`
- مرجع: `.claude/skills/kosif-superpowers/references/lesson-integrity-methods.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:lesson-integrity --evidence <ملف>`.

### `llm-council` — مجلس الخمسة الإلزامي: بوابة تحدد العمق، خمسة مستشارين متعارضين، مراجعة مجهولة، وحكم رئيس واحد / Mandatory five-member council: a gate sets the depth, five opposed advisors, anonymous peer review, one chairman verdict

| الحقل | القيمة |
|---|---|
| المسار | `scripts/llm_council.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `thinking-core`, `mental-models`, `planning-execution` |

**ما تفعله:** ينفذ مجلس الخمسة الإلزامي بلا نداء نموذج: gate يحدد العمق لكل طلب L1+ ولا يتخطاه، وframe يشتق القرار من الخطط ويضع قيود المستخدم الملزمة (--constraints) كاملة بلا اقتطاع بعد السؤال مباشرة في كل مطالبة حتى مطالبة الغريب والمراجعين والرئيس، ويبلّغ عن ملفات السياق التي سقطت بالحد الأقصى (dropped_context وتحذير)، ويقسم المدخلات إلى أدلة ومجهولات والغريب بلا سياق، وreview يكشف الأصوات المكررة والإجماع ويخفي الأسماء، وverdict يفحص العناوين الخمسة وحرف الخطة والخطوة الواحدة ويسجل هل غيّر الحكم الخطة، وstats يقيس نفع المجلس.

**What it does:** Runs USIP v5.8's mandatory council (A38 §7) without calling a model. gate sets the depth for every L1+ request (LIGHT at L1, STANDARD at L2, FULL at L3 or for money, publishing, personal data, architecture or irreversible steps, or on request) and never skips; frame derives the decision from the brief's plans A/B/C, puts the user's hard rules (--constraints, e.g. «لا ترجمة للآيات») never truncated in their own section «Hard constraints / قيود ملزمة» right after the question in every prompt (the five advisors, the Outsider's bare prompt, the reviewers, the chairman and LIGHT), gives at most four context files and lists whatever that cap drops in dropped_context with a stderr warning when the user's own --context items are cut, splits inputs into evidence and named unknowns (REA's pattern), and gives the Outsider no context; ingest rejects an advisor answer with no evidence and no named unknown and records the plan it backs; review catches duplicate voices (word-set Jaccard > 0.6), detects a 4-of-5 consensus and writes anonymised reviewer prompts with a shuffled, per-question letter map; chair de-anonymises; verdict checks the five headings, a plan letter, no hedging and one first step, and records CHANGED or NO_DELTA against the brief; stats measures depth mix, receipts and how often the council changed the plan.

#### متى تُستدعى

- «اعرض القرار ده على المجلس»
- «council this»
- «مجلس كامل على الخطة دي»
- «pressure-test this decision»
- «أي خطة أحسن: A ولا B ولا C؟»
- «اعرضها على المجلس بشرط: لا ترجمة للآيات»

#### الأوامر

- **gate**: Depth and reason for this request (never skips L1+).
  - `python3 scripts/llm_council.py gate --level L2 --from-brief out/<work>/brief.json`
- **frame**: Derived question, hard constraints right after it in every prompt (never truncated), evidence/unknowns, five advisor prompts; JSON lists dropped_context.
  - `python3 scripts/llm_council.py frame "<question>" --dir out/<work>/council5 --from-brief out/<work>/brief.json --constraints "لا ترجمة للآيات" --unknowns "budget"`
- **review**: Duplicate-voice and consensus checks, anonymised reviewer prompts.
  - `python3 scripts/llm_council.py review --dir out/<work>/council5`
- **verdict**: Checks the verdict and writes the receipt with CHANGED/NO_DELTA; exit 3 = fix.
  - `python3 scripts/llm_council.py verdict --dir out/<work>/council5 --file verdict.md`
- **stats**: How often the council changed the plan, by depth and receipt.
  - `python3 scripts/llm_council.py stats --root out`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: Writes only inside the given --dir; never calls a model or the network.
- الحدود: The voices are thinking styles run by Claude, not different models; LIGHT and SIMULATED receipts are not a run of agents. The checks test form and grounding words, not the quality of the reasoning; the user's explicit plan choice outranks the verdict. --constraints puts the rules in every prompt but nothing checks that an answer or the verdict obeys them; a rule typed as --context instead is still capped at four items (it is only reported).

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_v58_mastery.py`
- `.claude/skills/kosif-superpowers/evals/test_llm_council.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A38-v58-thinking-books-github-pulse.md`
- مرجع: `docs/protocol/council-20261026-smart-council.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:llm-council --evidence <ملف>`.

### `memory-ops` — عمليات الذاكرة / Memory Ops

| الحقل | القيمة |
|---|---|
| المسار | `scripts/memory_ops.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `agent-orchestration`, `self-discovery` |

**ما تفعله:** يحفظ ملف ذاكرة محليًا طويل المدى بلا تناقضات: لكل معلومة مرشحة يقترح عملية واحدة بسببها (إضافة إن لم يوجد مثلها، تحديث إن تغيرت قيمة لنفس الموضوع والخاصية أو أضافت صياغة أدق تفصيلًا، حذف إن تراجعت عن محفوظ، ولا شيء للمكرر)، ويرفض المعلومات التي فيها أسرار، وينفذ الخطة المعتمدة مع حفظ كل قيمة قديمة في السجل، ويبحث في المخزن. يوحّد النص العربي والإنجليزي قبل المقارنة.

**What it does:** Keeps a local long-term memory file free of contradictions: for every candidate fact it proposes one operation with its reason (ADD when nothing similar is stored, UPDATE when the same subject and attribute get a new value or a closer restatement adds detail, DELETE when the fact retracts a stored one, NOOP for duplicates), refuses facts that contain a secret, applies an approved plan while keeping every old value in history, and searches the store. English and Arabic text is normalised before comparison.

#### متى تُستدعى

- «احفظ تفضيلاتي دي من غير ما تتكرر أو تتناقض مع القديم»
- «المستخدم غير رأيه في اللهجة، حدّث الذاكرة»
- «decide whether these new facts should update or replace what we stored»
- «search the project memory for the export settings»

#### الأوامر

- **propose**: One ADD/UPDATE/DELETE/NOOP/REFUSE per fact with its reason; nothing is written to the store
  - `python3 scripts/memory_ops.py propose --store memory.json --facts facts.json --out plan.json`
- **apply**: Writes the store from an approved plan; replaced and deleted memories go to history
  - `python3 scripts/memory_ops.py apply --store memory.json --plan plan.json --when 2026-10-23`
- **search**: BM25-style ranked memories
  - `python3 scripts/memory_ops.py search --store memory.json "export settings"`
- **--self-test**: Runs the built-in decision cases
  - `python3 scripts/memory_ops.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: apply writes the memory file the user names; what may be remembered is still the user's and the project's call.
- الحدود: Decisions use word overlap and subject/attribute keys, not meaning, so a paraphrase with different words can be added twice and a short unrelated sentence with shared words can be merged; review the plan before apply.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_memory_ops.py`
- مرجع: `.claude/skills/kosif-superpowers/references/agents-memory-reasoning-repos.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:memory-ops --evidence <ملف>`.

### `prompt-lab` — مختبر البرومبت / Prompt Lab

| الحقل | القيمة |
|---|---|
| المسار | `scripts/prompt_lab.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `prompt-craft`, `verification-evals` |

**ما تفعله:** يجعل منهج كتابة البرومبت قابلًا للتشغيل لثمانية أنواع (نظام، تكليف وكيل، كود، بحث، كتابة، حَكَم، صورة، فيديو). build يرتب خانات النوع ويحوّل كل خانة مطلوبة ناقصة إلى سؤال؛ lint يعطي درجة من 20 (الخانات المطلوبة، والأنماط الضارة كالكلمات المبهمة والصياح وكلمات التهويل وكثرة النفي، بالعربية والإنجليزية) مع بوابات رفض للأسرار وطلب سلسلة التفكير والبيانات الملصقة بلا فواصل؛ refine يرتب الإصلاحات ويطبع هيكل الخانات الناقصة؛ eval يشغّل تأكيدات حتمية على نواتج محفوظة ويحتفظ بالنسخة فقط إن فازت على الأساس بلا تراجع؛ pairwise يطبع برومبتين للحكم بترتيب معكوس ولا يحتسب إلا الحكم المتفق عليه، كما يحكم Jev.

**What it does:** Makes the prompt-craft method runnable for eight kinds of prompt (system, agent brief, code, research, writing, LLM judge, image, video). build renders a kind's slots in order and turns every unfilled required slot into a question; lint scores a prompt out of 20 (required slots present, anti-patterns such as vague or shouted words, hype tokens and negative-heavy rules, in English and Arabic) with hard gates for a secret, a chain-of-thought request or undelimited pasted data; refine orders the fixes and prints the missing-slot skeleton; eval runs deterministic assertions on saved outputs and keeps a variant only when it beats the baseline with no regression; pairwise prints order-swapped judge prompts and counts only verdicts that agree in both orders, the way the owner's Jev service judges.

#### متى تُستدعى

- «اكتب لي برومبت فيديو تفصيلي ودقيق جدًا»
- «افحص البرومبت ده وقولي ناقصه إيه»
- «write a precise system prompt for my app»
- «is my new prompt actually better than the old one?»

#### الأوامر

- **kinds**: Lists the eight kinds and their slots (* = required)
  - `python3 scripts/prompt_lab.py kinds`
- **build**: Renders the kind's slots in order; unfilled required slots become [[questions]]; --lang ar adds the keep-dialect rule
  - `python3 scripts/prompt_lab.py build --kind video --set shot="Wide shot" --set subject="a fisherman" --set action="pulling a net" --set environment="on a boat at sunrise" --set camera="slow dolly in" --set style="warm light from the right" --set duration="6 seconds" --set aspect=16:9 --set audio="waves, no music"`
- **lint**: Score out of 20, band (ship / fix-lowest / rewrite / fail-gate), missing slots, anti-patterns and fixes; exit 1 on rewrite or a gate; --json
  - `echo "Make a nice image of a cat, 8k" \| python3 scripts/prompt_lab.py lint - --kind image`
- **refine**: Ordered fix list plus the skeleton of the missing slots to merge into
  - `echo "Write a blog post about AI" \| python3 scripts/prompt_lab.py refine - --kind writing`
- **eval**: Assertion matrix over saved outputs; keep=true only with a gain and no regression
  - `python3 scripts/prompt_lab.py eval --cases cases.json --outputs outputs.json --baseline A`
- **pairwise**: Prints the two order-swapped judge prompts; with --verdicts FILE counts only agreeing verdicts and flags position bias
  - `python3 scripts/prompt_lab.py pairwise --plan --a A.txt --b B.txt --task "Summarise the report for the board"`
- **--self-test**: Runs the built-in checks
  - `python3 scripts/prompt_lab.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: The linter reads text only: it shows whether slots and anti-patterns appear, not whether the prompt will work; eval needs outputs from real runs, and it never calls a model or the Jev service itself.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_prompt_lab.py`
- مرجع: `.claude/skills/kosif-superpowers/references/prompt-optimizer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:prompt-lab --evidence <ملف>`.

### `see-capability-bridge` — جسر توجيه قدرات SEE / SEE capability routing bridge

| الحقل | القيمة |
|---|---|
| المسار | `scripts/see_capability_bridge.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات |  |

**ما تفعله:** توجيه القدرات وأساليب التفكير بصورة للقراءة فقط مع حفظ حدود التنفيذ والتحقق.

**What it does:** Map the 11 cognitive lenses and nine SEE domains to specialist routes and live owners.

#### متى تُستدعى

- «Route specialist SEE methods for a finance task without running an external service»
- «Distinguish Full Pro or remote tool availability from execution and proof»

#### الأوامر

- **route**: Return a read-only SEE method routing record without executing agents.
  - `python3 scripts/see_capability_bridge.py --task "reconcile an Excel bank statement" --mode deep`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: This chooses guidance only; no proprietary source, hosted Full Pro, execution or verified output.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_see_capability_bridge.py`
- مرجع: `.claude/skills/kosif-superpowers/references/see-capability-bridge-20261030.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:see-capability-bridge --evidence <ملف>`.

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
  - `python3 scripts/see_pro_cognitive_gate.py check --file examples/see_pro_cognitive_packet.example.json`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: No approval required; read-only cognitive packet validation.
- الحدود: Metadata consistency check only, not independent proof of artifact quality or external Full Pro availability.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_see_pro_cognitive_gate.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A12-see-pro-cognitive-fusion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:see-pro-cognitive-gate --evidence <ملف>`.

### `see-superpower-unifier` — توحيد تخطيط SEE وسوبر باور / SEE and Superpowers unified planning

| الحقل | القيمة |
|---|---|
| المسار | `scripts/see_superpower_unifier.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات |  |

**ما تفعله:** توجيه القدرات وأساليب التفكير بصورة للقراءة فقط مع حفظ حدود التنفيذ والتحقق.

**What it does:** Enrich the one canonical Superpowers hub with bounded SEE cognitive and capability planning.

#### متى تُستدعى

- «Fuse SEE method candidates with the canonical Superpowers hub tool and power IDs»
- «Create a permission-conscious plan and validation chain without a duplicate registry»

#### الأوامر

- **route**: Return a read-only SEE method routing record without executing agents.
  - `python3 scripts/see_superpower_unifier.py plan "review bank invoices" --mode deep`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: This chooses guidance only; no proprietary source, hosted Full Pro, execution or verified output.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_see_superpower_unifier.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A12-see-pro-cognitive-fusion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:see-superpower-unifier --evidence <ملف>`.

### `stats-lab` — مختبر الإحصاء: اختبار A/B وحجم العينة ووصف عمود وأرباح الدفعات / Stats lab: A/B test, sample size, column statistics and FIFO/LIFO gains

| الحقل | القيمة |
|---|---|
| المسار | `scripts/stats_lab.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `atlas-data`, `data-analysis` |

**ما تفعله:** إحصاء حتمي للقرار: اختبار A/B بقيمة p وفترة ثقة للفرق والتحسن، وحجم العينة لكل مجموعة، ووصف عمود CSV مع القيم الشاذة وأرقام صفوفها، والأرباح المحققة لكل بيع بطريقة FIFO أو LIFO أو HIFO بحساب عشري دقيق.

**What it does:** Deterministic decision statistics with the standard library: a pooled two-proportion z-test with p-value, Wald CI of the difference and log risk-ratio CI of the lift; visitors per arm for a target lift, alpha and power; n, mean, median, sd, quartiles and IQR outliers (with row numbers) for a CSV column; and realized gains per sell from a trades CSV by FIFO, LIFO or HIFO lots with fees and exact decimals.

#### متى تُستدعى

- «هل الفرق بين النسختين في اختبار A/B حقيقي؟»
- «كم زائر أحتاج عشان أختبر تحسين 20%؟»
- «احسب أرباحي المحققة من ملف الصفقات بطريقة FIFO»
- «Is variant B's conversion lift statistically significant?»
- «How many users per arm do I need for this A/B test?»
- «Describe this CSV column and flag the outliers»

#### الأوامر

- **abtest**: Two-proportion z-test: z, p-value, CI of difference and lift, verdict.
  - `python3 scripts/stats_lab.py abtest --a 1000,100 --b 1000,130`
- **samplesize**: Visitors per arm and total for a relative (or --absolute) minimum detectable effect.
  - `python3 scripts/stats_lab.py samplesize --base 0.10 --mde 0.20 --power 0.8`
- **describe**: n, mean, median, sd, quartiles, IQR fences and outlier rows of one column.
  - `printf 'region,revenue\nA,120\nB,95\nC,130\nD,110\nE,900\n' \| python3 scripts/stats_lab.py describe - --col revenue`
- **lots**: Realized gain per sell with the lots used, totals per asset and open lots.
  - `printf 'date,side,qty,price,fee\n2024-01-05,buy,10,100,5\n2024-03-01,buy,10,150,5\n2024-06-01,sell,12,200,4\n' \| python3 scripts/stats_lab.py lots - --method fifo`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Normal-approximation tests (not exact or Bayesian, no sequential-peeking correction); lots is arithmetic, not tax advice (no wash-sale or holding-period rules).

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_stats_lab.py`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:stats-lab --evidence <ملف>`.

### `task-history` — سجل المهام: سجل لكل مهمة منجزة لإعادتها لاحقًا / Task history: record every finished task and repeat it later

| الحقل | القيمة |
|---|---|
| المسار | `scripts/task_history.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `self-discovery` |

**ما تفعله:** ذاكرة مهام على GitHub: سجل JSON واحد لكل مهمة منجزة تحت history/tasks/ بجذر المستودع، فيه الطلب بكلمات المستخدم والوضع والخطة والأدوات والأوامر بمعاملاتها والمدخلات والمخرجات (مع sha256 للملفات المحلية) وطريقة الإعادة. list وshow يجيبان «إيه المهام اللي عملتها؟»، وreplay يطبع خطة أو سكربت يعيد مهمة (لا يشغّل شيئًا ويعلّق خطوات الإذن)، وcompare يقارن المخرجات الجديدة بالبصمات المسجلة، وbuild يكتب history/INDEX.md وindex.json. والخيار add --print لا يكتب شيئًا ويعطي السجل وأمر حفظ في سطر ورابط GitHub مملوءًا لتطبيقات المحادثة التي لا تدفع. ويُرفض السجل الذي فيه مفتاح أو مسار جلسة أو رفع أو بريد أو هاتف.

**What it does:** Keeps a task memory on GitHub: one JSON record per finished task under history/tasks/ at the repo root, with the request in the user's words, the mode and plan, the tools and exact commands with their parameters, the inputs and outputs (sha256 added for local files) and how to reproduce it. list and show answer "what tasks have you done?", replay prints the plan or a shell script that repeats one (it runs nothing and keeps permission steps commented out), compare checks new outputs against the recorded hashes, and build writes history/INDEX.md and index.json. add --print writes nothing and gives the record, a one-line save command and a pre-filled GitHub new-file link for chat apps that cannot push. Records holding a credential, a session or upload path, an e-mail address or a phone number are refused.

#### متى تُستدعى

- «إيه المهام اللي عملتها قبل كده»
- «كرر المهمة رقم 3 بنفس النتيجة»
- «سجّل المهمة دي في الهيستوري على جيت هاب»
- «What tasks have you done? Repeat the Friday dua video»
- «Record this finished task so it can be reproduced»

#### الأوامر

- **new**: Prints a record template to fill.
  - `python3 scripts/task_history.py new --kind video`
- **add**: Validates the record (fields, privacy gate), adds sha256 and bytes for local files, writes history/tasks/<id>.json and rebuilds the index; --print writes nothing and prints the record, a one-line save command and a GitHub link.
  - `python3 scripts/task_history.py add --from entry.json`
- **list**: The recorded tasks, newest first and numbered; --q filters by words, --json for machines.
  - `python3 scripts/task_history.py list --kind video`
- **show**: One task in full by id, unique prefix, list number or last.
  - `python3 scripts/task_history.py show last`
- **replay**: Prints the replay plan (md), a script that checks input hashes then runs the recorded commands (sh), or JSON; it runs nothing.
  - `python3 scripts/task_history.py replay last --format sh`
- **compare**: Compares the outputs now on disk with the recorded hashes: identical, DIFFERENT, differs (not deterministic) or missing; exits 1 unless the result is the same.
  - `python3 scripts/task_history.py compare last`
- **build**: Writes history/INDEX.md and history/index.json; --check writes nothing and exits 1 when stale.
  - `python3 scripts/task_history.py build --check`
- **validate**: Checks every record; --strict also fails on a stale index.
  - `python3 scripts/task_history.py validate`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: add and build write only under history/; adding a record to main is covered by the user's standing permission limited to history/ (A35). list, show, replay, compare and validate only read.
- الحدود: A record is what the assistant reports it ran: replay repeats the recorded commands but cannot bring back a deleted input, an expired link or a paid model's randomness, and compare checks bytes only for outputs marked deterministic.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_task_history.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A35-task-history.md`
- مرجع: `history/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:task-history --evidence <ملف>`.

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

**ما تفعله:** يحوّل إجراءات التفكير إلى قوالب نصية قابلة للفحص. يختار مستوى التفكير (L0–L6)، ويكتب عقد المهمة، ويرتّب 63 نموذجًا ذهنيًا، ويصوغ خطة بالتخطيط العكسي، ويبني مصفوفة أفكار من قدرات الكتالوج، ويقيّم قرارًا موزونًا مع اختبار الحساسية، ويجري تقدير فيرمي بطريقة مونت كارلو، ويرصد الصياغات الضعيفة في المسودة. وأضاف USIP v5.4 أربع أدوات استدلال: ترتيب ثمانية أنماط استدلال للمهمة، وتحديث الاعتقاد بنسب الأرجحية مع اختبار حساسية بالتنصيف والمضاعفة، وحكم استمر/حوّل/أوقف/انتظر من عتبات مكتوبة مسبقًا، ودفتر ادعاء ← دليل للمسودة. وأضاف USIP v5.5 أربعة قوالب ذكاء: كشف نوع مخرج الطلب وتصنيف خاناته إلى مملوءة ومفترضة ومسؤولة (بميزانية أسئلة المستوى) وحاجبة، وفحص رسم المهام وحساب ترتيبه ومساره الحرج المتفائل والمتشائم وأبوابه التي لا رجعة فيها، ومعايير الجودة لاثني عشر نوع مخرج مع حكم ناجح/فاشل/ناقص من الإجابات، وسلم التعافي لكل صنف خطأ في FusionForge بميزانية محاولات. وأمر pro يطبع 4 أو 8 أو 12 طبقة ذكاء (قياسي، عميق، أقصى)، لكل طبقة سؤال ومخرج يُكتب واختبار إبطال يفرض الإعادة، ومعها مجلس مناسب من 5 أو 9 أو 15 شخصية ونمطا استدلال وثلاثة نماذج ذهنية.

**What it does:** Turns thinking procedures into checkable text scaffolds. It picks a reasoning level (L0–L6), writes a task contract, ranks 63 mental models, drafts a backcast plan, builds an idea matrix from catalog powers, scores a weighted decision with sensitivity, runs a Monte-Carlo Fermi estimate and flags weak wording in a draft. USIP v5.4 adds four reasoning tools: it ranks eight reasoning modes for a task, updates a belief by likelihood ratios with a halve/double sensitivity, gives a GO/PIVOT/KILL/HOLD verdict from thresholds written in advance, and builds a claim-to-evidence ledger for a draft. USIP v5.5 adds four intelligence scaffolds: it detects a request's deliverable kind and sorts its slots into filled, assumed, asked (within the level's question budget) and blocking; checks a task DAG and computes its order, optimistic and pessimistic critical path and one-way doors; prints the quality bar of twelve deliverable kinds and gives PASS, FAIL or INCOMPLETE from answers; and prints the recovery ladder for a FusionForge error class with an attempt budget. The Pro pass prints 4, 8 or 12 intelligence passes (standard, deep, max), each with a question, the artifact to write and a falsifier that forces a redo, plus a task-fitted council of 5, 9 or 15 personas, two reasoning modes and three mental models.

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
- «فكّر بأقصى قوة في القرار ده (برو)»
- «Run the deep Pro passes on this launch plan»

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
- **pro**: Prints the Pro passes of the depth (4/8/12) with question, artifact and falsifier, a fitted council (5/9/15), two modes and three models; --json for JSON.
  - `python3 scripts/think.py pro "اعمل فيديو إطلاق منتج" --depth max`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: It produces templates and keyword-based rankings to think with; the blanks (…) still have to be filled and tested, it does not reason about or verify claims by itself, and critic is a plain regex sweep that misses Arabic words written with tanween (جدًا، دائمًا). modes ranks by keywords only, and bayes, gate and audit compute exactly what they are given: the priors, ratios, thresholds and evidence markers are the user's or Claude's judgement.

#### الاختبارات والأدلة

- `tests/test_think.py`
- `tests/test_think_reasoning.py`
- `tests/test_think_intel.py`
- `tests/test_think_pro.py`
- `.claude/skills/kosif-superpowers/evals/test_think_models.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A24-reasoning-modes-decision-gates.md`
- مرجع: `.claude/skills/kosif-superpowers/references/cognition.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`
- مرجع: `CAPABILITIES.md`
- مرجع: `README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A25-task-intake-clarification.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A26-planning-decomposition.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A27-verification-quality-standards.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A29-failure-recovery.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A30-council-100.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:think --evidence <ملف>`.

### `thinking-books` — مكتبة كتب التفكير: 64 منهجًا من 40 كتابًا مشهورًا في طرق التفكير مربوطة بمراحل البروتوكول / Thinking-books library: 64 methods from 40 famous books on how to think, routed to USIP phases

| الحقل | القيمة |
|---|---|
| المسار | `scripts/thinking_books.py` (جذر: skill) |
| المجال | `think` |
| الدليل | `tested-here` |
| العائلات | `thinking-core`, `mental-models`, `planning-execution`, `creativity-engine` |

**ما تفعله:** 64 منهجًا بكلماتنا من 40 كتابًا في التفكير، لكل منهج مرحلة ومحفزات وخطوات ودليل تطبيق وفخ. route يختار الأنسب لمهمة، وstack منهجًا لكل مرحلة، وdebias يفحص التقرير للتحيزات، مع القبعات الست وتريز والتنبؤ بالنظرة الخارجية ودرجة براير.

**What it does:** Holds 64 methods restated in our own words from 40 widely known books on thinking (Kahneman, Tetlock, Pólya, de Bono, Meadows, Taleb, Minto, Klein, Rumelt, Galef, Sagan, Ibn Khaldun, Ibn al-Haytham, al-Ghazali and more), each with a stage, Arabic/English triggers, steps, a proof-of-use check and the trap it prevents. route ranks the best methods for a task from different books; stack picks one per stage mapped to USIP phases (adding the reuse-first ladder for code); debias sweeps a draft report for certainty without odds, a single option, no risks, numbers without a base rate, no sources, sunk cost and answer-last; plus Six Hats prompts, a TRIZ contradiction helper over the 40 principles, an outside-view forecast with capped adjustments and a Brier score.

#### متى تُستدعى

- «فكّر صح في القرار ده واستخدم مناهج الكتب»
- «افحص التقرير ده من التحيزات قبل ما أبعته»
- «قدّر مدة المشروع بالنظرة الخارجية»
- «عايز أفكار لحل تعارض بين السرعة والجودة»
- «Which thinking method fits this decision?»

#### الأوامر

- **stack**: One method per stage mapped to USIP phases.
  - `python3 scripts/thinking_books.py stack "عايز أطلق تطبيق جديد"`
- **route**: Best methods for a task from different books.
  - `python3 scripts/thinking_books.py route "قدّر مدة المشروع" -n 5`
- **debias**: Bias sweep of a draft; exit 3 = REVISE.
  - `python3 scripts/thinking_books.py debias report.md`
- **triz**: Contradiction to inventive principles.
  - `python3 scripts/thinking_books.py triz --improve speed --worsen quality`
- **forecast**: Outside view first, capped inside-view adjustments.
  - `python3 scripts/thinking_books.py forecast --base 0.3 --adjust "+0.1:strong team"`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: Reads only the data file and the given draft; prints to stdout.
- الحدود: Methods are summaries written from public knowledge of the books, not the books; routing and debias are keyword heuristics; a scaffold is not proof that the thinking was done.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_v58_mastery.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A38-v58-thinking-books-github-pulse.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:thinking-books --evidence <ملف>`.

