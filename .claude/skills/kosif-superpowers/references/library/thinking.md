# التفكير والتخطيط والاستراتيجية — Reasoning & strategy (`thinking`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: think reasoning idea brainstorm strategy plan finance decision تحليل تخطيط ابتكار قرار

لا خط عمل مسجّل لهذه المجموعة؛ ركّبه من الأدوات أدناه.

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 17 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 8 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 308 | 📄 documented: a described method; needs building or wiring before it runs |
| `install` | 2 | 📦 install: needs a package, binary or model first |
| **المجموع** | **335** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `anchor-gate` | بوابة حفظ الحقائق عند إعادة الصياغة | `python3 scripts/anchor_gate.py --before proofs/general-writing/pairs/en_before.txt --after proofs/general-writing/pairs/en_after_drift.txt --text` | tested-here |
| `architecture-sizer` | مقدّر سعة الأنظمة | `python3 scripts/architecture_sizer.py --daily-requests 86400 --peak-factor 5 --payload-bytes 1000 --retention-days 7 --replica-rps 100 --target-utilization 0.5 --copies 2` | tested-here |
| `book-methods` | مناهج مستخلصة من الكتب: التفكير الجانبي والهندسة العملية والأدلة البايزية والشخصية وفحوص المحاسبة ووضوح البرومنت | `python3 scripts/book_methods.py search "شخصية حوار"` | tested-here |
| `business-workflows` | الذكاء الاصطناعي في الأعمال: 9 وظائف و64 خطة عمل بخطط تشغيل لClaude | `python3 scripts/business_workflows.py functions` | tested-here |
| `capability-atlas` | أطلس القدرات للبحث والتخطيط | `python3 scripts/capability_atlas.py stats --json` | tested-here |
| `capability-mindmap` | الخريطة الذهنية المرحلية وتدقيق التكرار | `python3 scripts/capability_mindmap.py build` | tested-here |
| `capability-runtime-router` | موجّه القدرات التنفيذية | `python3 scripts/capability_runtime_router.py --task "حلل فيديو مرجعي وأنتج مونتاج مشابه بأصولي" --limit 5 --json` | tested-here |
| `council` | مجلس البرو: خمسة متعارضين أو مجلس مناسب من 100 شخصية، ثلاث جولات وحكم بالدرجات | `python3 scripts/council.py plan "اعمل ريلز دعاء" --dir out/demo/council --options A,B,C` | tested-here |
| `fusionforge` | FusionForge v2 لوصفات الـWorkflow المركبة داخل المشروع | `python3 scripts/fusionforge.py propose "مونتاج ريلز بترجمة عربية" --project demo_project --from-brief out/20261021-reel/brief.json` | tested-here |
| `fusionforge-shared` | ذاكرة FusionForge المشتركة بوصفات مهارات معزولة | `python3 scripts/fusionforge_shared.py audit` | untested |
| `invention-lab` | مختبر الابتكار الهندسي | `python3 scripts/invention_lab.py methods` | tested-here |
| `prompt-lab` | مختبر البرومبت | `python3 scripts/prompt_lab.py kinds` | tested-here |
| `prompt-pack` | حزمة المطالبات: كل مطالبة في كتلة كود قابلة للنسخ مع فحص يحذّر فقط | `python3 scripts/prompt_pack.py build prompts.json --out out/demo/prompts --engine midjourney` | tested-here |
| `repo-kosif` | أداة سطر أوامر لأطلس أنماط KOSIF | `python3 tools/kosif.py list --category charts --limit 10` | tested-here |
| `requirements` | مخطط متطلبات القدرات | `python3 scripts/requirements.py present --json` | tested-here |
| `see-pro-cognitive-gate` | فاحص عقود التفكير والتوليف KOSIF SEE Pro | `python3 scripts/see_pro_cognitive_gate.py --self-test` | tested-here |
| `skill-intelligence` | محرك بروتوكول ذكاء المهارات الشامل | `python3 scripts/skill_intelligence.py brief "مونتاج ريلز على الإيقاع بترجمة عربية"` | tested-here |
| `style-library` | مكتبة الأساليب: 586 أسلوبًا بصريًا بالاسم (86 من أطلس Futurepedia + 500 أصلي) — بحث ووصف وبرومنت وعينة وكتالوج PDF مصوّر | `python3 scripts/style_library.py groups` | tested-here |
| `superpowers-unified` | موجّه مهارات العمل ومثبّتها | `python3 scripts/superpowers_unified.py doctor` | tested-here |
| `think` | محرك التفكير وقوالبه | `python3 scripts/think.py ladder "design a 30-day plan for a course launch"` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `atlas-mind` | 54 | [atlas-mind.md](../powers/atlas-mind.md) |
| `atlas-strategy` | 72 | [atlas-strategy.md](../powers/atlas-strategy.md) |
| `creativity-engine` | 29 | [creativity-engine.md](../powers/creativity-engine.md) |
| `mental-models` | 63 | [mental-models.md](../powers/mental-models.md) |
| `planning-execution` | 12 | [planning-execution.md](../powers/planning-execution.md) |
| `prompt-craft` | 41 | [prompt-craft.md](../powers/prompt-craft.md) |
| `strategy-finance` | 18 | [strategy-finance.md](../powers/strategy-finance.md) |
| `thinking-core` | 46 | [thinking-core.md](../powers/thinking-core.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `IDEA-26` | مصفوفة الأفكار: عوامل × قدرات | Idea matrix: operators × powers | proven | python3, npm:three |
| `IDEA-29` | الجدوى من المستلزمات لا من التفاؤل | Feasibility from requirements, not optimism | proven | python3 |
| `PLAN-01` | مخطط الخطة الكاملة من الهدف | Full plan scaffold from a goal | proven | python3 |
| `PLAN-05` | بوابة المستلزمات قبل الجدولة | Requirements gate before scheduling | proven | python3 |
| `PROMPT-02` | دفتر الحفظ وفحصه الآلي | Preservation ledger with an automatic check | proven | python3 |
| `PROD-03` | المخاطر كتوزيع لا كرقم | Risk as a distribution (Monte Carlo) | proven | pip:numpy, npm:p5 |
| `PROD-10` | مزيج إنتاج أمثل | Optimal product mix (LP) | proven | pip:scipy, pip:sympy, pip:ortools |
| `PROD-11` | السعر الأمثل ونقطة التعادل | Optimal price and break-even | proven | pip:sympy |
| `PROD-16` | OR-Tools: حل مسائل الجدولة والتوجيه والتعيين بأمثلية عبر | OR-Tools: Solve scheduling, routing and assignment problems optimally with CP-SAT | proven | pip:ortools |
| `PROD-17` | PuLP: نمذجة مسائل البرمجة الخطية والصحيحة كتوزيع الميزانيات | PuLP: Model linear and integer programs such as budget splits and blends | proven | pip:ortools, pip:pulp |
| `THINK-04` | استدعاء القوى من الفهرس | Recall powers from the catalog (powers.py suggest / search / show) | proven | python3 |
| `THINK-35` | سلّم مستويات التفكير L0–L6 | Cognition ladder L0–L6 | proven | python3 |
| `THINK-36` | العقد التلقائي للمهمة | Auto-framed task contract | proven | python3 |
| `THINK-37` | مصفوفة قرار بفحص الحساسية | Decision matrix with sensitivity | proven | python3 |
| `THINK-38` | تقدير فيرمي بمونت كارلو | Monte-Carlo Fermi estimate | proven | python3 |
| `THINK-39` | ناقد المسودة الآلي | Automatic draft critic | proven | python3 |
| `THINK-40` | اختيار النماذج الذهنية للمشكلة | Mental-model selection for a problem | proven | python3 |
| `PROMPT-23` | اطلب أي أسلوب بصري بالاسم من مكتبة 586 أسلوبًا | Ask for any visual style by name from a 586-style library | ready | python3 |
| `PROMPT-24` | دمج أسلوبين 70/30 في برومنت واحد | Fuse two styles 70/30 in one prompt | ready | python3 |
| `PROMPT-25` | كتالوج أساليب مصوّر PDF بعينات مولّدة | Illustrated style catalog PDF with generated swatches | ready | python3, chromium |
| `PROMPT-34` | مصفوفة تقييم بالتأكيدات | Assertion matrix eval | ready | python3 |
| `PROMPT-35` | قالب صورة بمتغيرات وأقفال | Parameterized image prompt template | ready | python3 |
| `PROMPT-39` | فحص البرومبت الحتمي | Deterministic prompt lint | ready | python3 |
| `PROMPT-40` | قوالب حسب نوع البرومبت | Prompt templates by kind | ready | python3 |
| `PROMPT-41` | حَكَم مقارن بترتيب معكوس (طريقة Jev) | Order-swapped pairwise judge (Jev method) | ready | python3 |
| `AMIND-01` | تصميم ذاكرة الوكيل وتقييمها وتدقيق التسميم | Agent memory design, eval and poisoning audit | documented |  |
| `AMIND-02` | فرز النهج الوكيلي وتصميم الأدوات وتحصين التقييم | Agentic approach triage, tool design and eval hardening | documented |  |
| `AMIND-03` | تنظيم الذاكرة التلقائية وترقيتها | Auto-memory curation and promotion | documented |  |
| `AMIND-04` | حلقة وكيل محدودة بإنجاز يتحقق منه الجهاز | Bounded agent loop with machine-verified completion | documented |  |
| `AMIND-05` | حلقة محاولات محدودة مع تقرير توقف | Bounded retry loop with stop-report | documented |  |
| `AMIND-06` | حفظ تصحيحات الجلسة في ذاكرة دائمة عبر الجلسات | Capture session corrections into persistent memory | documented |  |
| `AMIND-07` | مراسلة وكلاء مشاريع أخرى عبر الألواح | Cross-project agent messaging via terminal panes | documented |  |
| `AMIND-08` | سجل حالة المهام عبر الجلسات | Cross-session task-state journal | documented | git |
| `AMIND-09` | قرار التفويض للوكلاء أو التنفيذ المباشر | Delegate-or-inline decision for subagents | documented | claude:tools |
| `AMIND-10` | نقطة حفظ مدعومة بالأدلة لاستئناف المهمة | Evidence-based checkpoint manifest for resume | documented |  |
| `AMIND-11` | تنفيذ الخطط بوكلاء مسمّين وسجل تقدم دائم | Execute plans with named agents and progress ledger | documented | git, claude:tools |
| `AMIND-12` | نقل نتائج الوكلاء بأمانة | Faithful relay of agent results | documented |  |
| `AMIND-13` | بروتوكول صندوق وارد وتحكم بالملفات بين الوكلاء | File-based multi-agent inbox and control protocol | documented |  |
| `AMIND-14` | خط إشراف قاضٍ مع تفويض بين نماذج | Judge-orchestrated cross-model delegation pipeline | documented |  |
| `AMIND-15` | إبقاء الأسرار خارج سجلات الوكلاء | Keep credentials out of agent transcripts | documented |  |
| `AMIND-16` | تشخيص ذاتي لكسر الحلقات وانضباط التحقق | Loop-break self-diagnosis and verification discipline | documented |  |
| `AMIND-17` | توضيح الرسائل المعقدة قرارًا قرارًا | One-decision-at-a-time clarification of dense messages | documented |  |
| `AMIND-18` | إطلاق وكلاء متوازين لكل مجال فشل مستقل | Parallel agent dispatch per independent failure domain | documented | claude:tools |
| `AMIND-19` | مراسلة الوكلاء عبر لوحات tmux | Peer agent messaging over tmux panes | documented |  |
| `AMIND-20` | مراسلة مباشرة بين جلسات Claude Code العاملة | Peer messaging between running Claude Code sessions | documented | chromium |
| `AMIND-21` | شجرة قرار حدود المراحل والتسليم بين الجلسات | Phase-boundary tree: continue, clear, handoff, delegate, compact | documented | claude:tools |
| `AMIND-22` | تسييج حقن الأوامر في المحتوى غير الموثوق | Prompt-injection fencing for untrusted content | documented |  |
| `AMIND-23` | استرجاع الذاكرة قبل التنفيذ وتسجيلها بعده | Recall-before-act and remember-after-act agent memory | documented |  |
| `AMIND-24` | استرجاع نتائج الوكيل الصامت قبل إعادة إطلاقه | Recover silent subagent results before respawning | documented | claude:tools |
| `AMIND-25` | عقد مسار عمل للوكيل بحدود نطاق صارمة | Scope-fenced worker lane contract | documented | git |
| `AMIND-26` | نقطة حفظ وتسليم بين الجلسات عبر مجلد .context | Session checkpoint and handoff via a .context store | documented |  |
| `AMIND-27` | وثيقة تسليم جلسة تشير للمراجع بدل التكرار | Session handoff document with artifact references | documented |  |
| `AMIND-28` | ملف تسليم الجلسة مع عتبات ضغط السياق | Session handoff file with context-pressure thresholds | documented |  |
| `AMIND-29` | تسليم الجلسة وإعادة التثبيت والمطابقة | Session handoff, reanchor and reconcile | documented |  |
| `AMIND-30` | ملخص الجلسة من سجلات الوكيل | Session recap from Claude and Codex logs | documented |  |
| `AMIND-31` | تنفيذ مهمة موجهة بالمواصفات مع دليل RED | Spec-driven task execution with RED evidence | documented |  |
| `AMIND-32` | خط حل مرحلي: توضيح فتفكيك فتنفيذ فمراجعة | Stage-gated clarify-decompose-execute-revise solve pipeline | documented |  |
| `AMIND-33` | أنماط تنسيق وكلاء متعددين بحسب الاستراتيجية | Strategy-based multi-agent orchestration patterns | documented | claude:tools |
| `AMIND-34` | معايير تدقيق إعداد الوكلاء الفرعيين | Subagent configuration standards and audit | documented | claude:tools |
| `AMIND-35` | مذكرة تسليم جلسة موثقة واستئنافها | Validated session handoff note and resume | documented |  |
| `AMIND-36` | استئناف سير عمل متوقف بالتحقق أولاً | Verify-first workflow resume from sidecar state | documented |  |
| `AMIND-37` | إرسال على دفعات مع تحقق مستقل لكل مرحلة | Wave-capped dispatch with independent phase verification | documented |  |
| `AMIND-38` | أسطول worktree لمهام معتمدة متوازية | Worktree fleet for parallel approved tasks | documented | git |
| `AMIND-39` | قاطع التكرار العقيم بعد محاولتين فاشلتين | Anti-thrashing circuit breaker after two failed fixes | documented |  |
| `AMIND-40` | إثبات التراجع قبل أي إجراء لا رجعة فيه | Prove rollback before irreversible action | documented |  |
| `AMIND-41` | تصدير خريطة ذهنية تفاعلية | Interactive mindmap export (force graph, MarkMind) | documented | python3 |
| `AMIND-42` | مراجعة الافتراضات وإعادة التقييم | Challenge approach before commitment | documented |  |
| `AMIND-43` | قسم الملاحظات والحالة الختامي | Closing Caveats and status section | documented |  |
| `AMIND-44` | تحقق خصومي أعمى من البراهين | Blind adversarial verification of proofs | documented | latex |
| `AMIND-45` | تطوير قائم على الشك: مراجعة عدائية للقرارات غير البديهية | Doubt-driven development for non-trivial decisions | documented |  |
| `AMIND-46` | تخطيط بأسلوب Heuer: اختبار الافتراضات دون مجاملة | Heuer-style structured planning with tested premises | documented | pip:hypothesis |
| `AMIND-47` | استخراج المتطلبات: اسأل ولا تخترع | Requirements elicitation: elicit, do not invent | documented |  |
| `AMIND-48` | توجيه إلى أخصائي واحد مع إلزام القراءة | Route to one specialist, read before answering | documented |  |
| `AMIND-49` | أعد الاستخدام أو استبدل علناً: لا طريقتين لشيء واحد | Reuse or openly replace: one way to do a thing | documented |  |
| `AMIND-50` | تحديث خارطة الطريق من الأدلة مع ذكر وضع الفحص | Evidence-based roadmap update with an explicit scan mode | documented |  |
| `AMIND-51` | زرع العيب لإثبات أن الفحص يستطيع أن يفشل | Plant the defect to prove a check can fail | documented |  |
| `AMIND-52` | خطة تحقق يدوي مرقمة قابلة للاستئناف | Resumable numbered manual verification plan | documented |  |
| `AMIND-53` | الإطلاق في الظل لاختبار نظام بديل تحت حمل الإنتاج | Shadow mode (dark launch) to validate a replacement under real load | documented |  |
| `AMIND-54` | تنقيح المواصفات بتحليل الفجوات وأسئلة متتابعة مرجّحة | Specification refinement: gap analysis and ranked one-at-a-time questions | documented |  |
| `ASTRAT-01` | تدقيق جدوى تعدد الوكلاء مقابل وكيل واحد | Audit multi-agent topology against single-agent baseline | documented |  |
| `ASTRAT-02` | حلقة مستقلة لتصريف قائمة المهام | Autonomous backlog-draining loop and single-task ralph loop | documented |  |
| `ASTRAT-03` | توجيه أسئلة المؤسس إلى أدوار المستشارين التنفيذيين | Route founder questions to C-suite advisor roles | documented |  |
| `ASTRAT-04` | إرسال المهام على موجات مع بوابات تحقق | Sequential wave dispatch with verification gates | documented |  |
| `ASTRAT-05` | تقدير ميزانية الوكلاء قبل التشغيل | Size agent budget before running a workflow | documented |  |
| `ASTRAT-06` | خريطة تذاكر قرارات للعمل الضخم | Wayfinder decision-ticket map for huge work | documented |  |
| `ASTRAT-07` | تأهيل العميل بمراحل وبوابات تحقق | Client onboarding with phase gate checks | documented |  |
| `ASTRAT-08` | تقرير استخدام الطاقة وانحراف العمل قيد التنفيذ | Practice utilisation and WIP variance report | documented |  |
| `ASTRAT-09` | تخطيط دفعة الموردين الأسبوعية مع الاستثناءات | Weekly supplier pay-run planning with exclusions | documented |  |
| `ASTRAT-10` | فحص كلمات ASO وتدقيق القائمة | App Store Optimization keyword probe and lint | documented |  |
| `ASTRAT-11` | رحلة من الفكرة إلى التطبيق بمتتبع | Idea-to-app journey with docs tracker | documented |  |
| `ASTRAT-12` | مراجعة مخاطر ما قبل البناء | Pre-build risk review and kill-test | documented |  |
| `ASTRAT-13` | قرار تخزين البيانات على السلسلة أو خارجها | On-chain versus off-chain data placement | documented |  |
| `ASTRAT-14` | اختبار استراتيجية تداول بمقاييس المخاطر | Backtest trading strategy with risk metrics | documented | pip:numpy, pip:pandas, pip:matplotlib |
| `ASTRAT-15` | تقييم DCF متين مع فحوص تقاطعية | Defensible DCF valuation with cross-checks | documented |  |
| `ASTRAT-16` | سجل مخاطر مؤسسي مع التقييم | Enterprise risk register with scoring | documented |  |
| `ASTRAT-17` | بناء الأعمال ومراجعة طلب التمويل للمؤسسين | Founder business building and fundraising review | documented | key:video-gen |
| `ASTRAT-18` | بروتوكول مداولات مجلس إدارة متعدد الأدوار | Multi-role board deliberation protocol | documented |  |
| `ASTRAT-19` | تصميم استراتيجية التسعير والربحية | Pricing and monetization strategy design | documented |  |
| `ASTRAT-20` | ميزانية البحث والتطوير والحرق وتوجيه الرسملة | R&D program budget, burn and capitalization routing | documented | key:video-gen |
| `ASTRAT-21` | نموذج جدول الملكية وتخفيف الحصص | Startup cap table and dilution model | documented |  |
| `ASTRAT-22` | لوحات الاستراتيجية وSWOT وفحص الافتراضات | Strategy canvases, SWOT and red-team | documented | lean |
| `ASTRAT-23` | توقع نقدي متدحرج 13 أسبوع | 13-week rolling cash forecast with variance loop | documented |  |
| `ASTRAT-24` | تقسيم العملاء والمستخدمين حسب القيمة | Customer and user segmentation by value | documented |  |
| `ASTRAT-25` | مواصفة تجربة مع بوابة قرار | Experiment design spec with go/no-go gate | documented | pip:hypothesis |
| `ASTRAT-26` | تشخيص تسرب القمع والاحتفاظ | Funnel and retention drop-off diagnosis | documented |  |
| `ASTRAT-27` | هيكلة المقاييس ووثائق التعريف | Metrics architecture and definition docs | documented | lean |
| `ASTRAT-28` | تحليل الأسباب الجذرية والمخاطر | Root-cause and risk analysis (fishbone, PFMEA, lean) | documented | lean |
| `ASTRAT-29` | دراسة الاستعداد للدفع وتغيير الأسعار | Willingness-to-pay and price change planning | documented |  |
| `ASTRAT-30` | قرار البث مقابل الدفعات | Streaming versus batch decision | documented |  |
| `ASTRAT-31` | اختيار قاعدة بيانات سحابية مناسبة | Cloud database selection and managed-service routing | documented |  |
| `ASTRAT-32` | سلسلة خمسة لماذا مع تحقق | 5-Why root cause chain with validation | documented |  |
| `ASTRAT-33` | دليل حادثة: فرز واحتواء واستعادة ومراجعة | Incident runbook: triage, contain, recover, review | documented |  |
| `ASTRAT-34` | فرز الحادث مقابل المشكلة وتحديد الخطورة | Incident vs problem triage and severity | documented |  |
| `ASTRAT-35` | تحليل السبب الجذري بخمسة لماذا وإيشيكاوا | Root cause analysis with 5 Whys and fishbone | documented |  |
| `ASTRAT-36` | إسناد تكلفة استخدام API وضوابط الإنفاق | API usage cost attribution and spend controls | documented |  |
| `ASTRAT-37` | أدلة قرارات معمارية السحابة | Cloud architecture decision playbooks | documented |  |
| `ASTRAT-38` | حصاد هدر السحابة وترتيب تسرب التكلفة | Cloud waste harvest and cost leak ranking | documented |  |
| `ASTRAT-39` | تعريف SLI وSLO وميزانية الخطأ | Define SLIs, SLOs and error budgets | documented |  |
| `ASTRAT-40` | تدقيق خفض التكلفة المبني على الاستخدام | Usage-driven cost tuning audit for SaaS/API spend | documented |  |
| `ASTRAT-41` | خطة اختبار اختراق للذكاء الاصطناعي ومعالجتها | AI red-team plan and remediation | documented |  |
| `ASTRAT-42` | سلم توجيه النماذج حسب التكلفة | Cost-per-task model routing ladder | documented |  |
| `ASTRAT-43` | جاهزية قانون الذكاء الأوروبي وفحص التحيز | EU AI Act readiness and bias check | documented |  |
| `ASTRAT-44` | تدقيق تكلفة LLM والتوجيه | LLM cost audit and routing | documented |  |
| `ASTRAT-45` | مراجعة برنامج مكافحة غسل الأموال | AML program review against FATF/FFIEC | documented |  |
| `ASTRAT-46` | تشخيص هامش الربح ومزيج الخدمات | Small-business margin and mix diagnostics | documented |  |
| `ASTRAT-47` | مراجعة التصميم بالقواعد الإرشادية | Design review heuristics and critique | documented |  |
| `ASTRAT-48` | جولة موازنة اقتصاد اللعبة | Game balance and economy tuning pass | documented | python3 |
| `ASTRAT-49` | تصميم الآليات وتجربة اللاعب | Game mechanics and player experience design | documented |  |
| `ASTRAT-50` | تصنيف مؤشرات DORA الأربعة | DORA four keys classification | documented |  |
| `ASTRAT-51` | قراءة المؤشرات التشغيلية الصناعية | Frequency vs severity operating metrics | documented |  |
| `ASTRAT-52` | تفكيك المتطلبات لمهام قابلة للتنفيذ | Task breakdown with sizing rules | documented |  |
| `ASTRAT-53` | إصدار أمني منسق | Coordinated security release | documented |  |
| `ASTRAT-54` | بطاقات أنكي عبر AnkiConnect | Anki flashcards via AnkiConnect | documented | os:macos, network |
| `ASTRAT-55` | إعداد دورة Google Classroom والطلاب | Google Classroom course setup and roster | documented |  |
| `ASTRAT-56` | مدرب تعلم متعدد الجلسات بحالة محفوظة | Multi-session learning coach with persistent state | documented |  |
| `ASTRAT-57` | بروتوكول تدريس سقراطي سؤال واحد كل مرة | Socratic one-question-at-a-time tutoring protocol | documented |  |
| `ASTRAT-58` | الوظائف المطلوب إنجازها بأبعادها الثلاثة | Jobs to Be Done with all three dimensions | documented |  |
| `ASTRAT-59` | التموضع: السياق قبل الرسالة | Positioning as context (Obviously Awesome canvas) | documented |  |
| `ASTRAT-60` | تحسين التحويل: اكتشف ولا تخمّن | Conversion optimisation: discover, do not guess | documented |  |
| `ASTRAT-61` | تحسين الظهور في البحث ومحركات الإجابة والذكاء التوليدي | SEO, answer-engine and generative-engine visibility | documented |  |
| `ASTRAT-62` | مراجعة تصميم بأسلوب الطرح حتى الجوهر | Subtractive design review from the customer backwards | documented |  |
| `ASTRAT-63` | مقابلة سؤال-بسؤال لاستخراج النية الحقيقية قبل البناء | One-question interview to extract real intent | documented |  |
| `ASTRAT-64` | خطاب تقديم وظيفي مفصّل على الإعلان بلا عبارات آلية | Tailored cover letter without AI tells | documented | latex |
| `ASTRAT-65` | التفاوض بالتعاطف التكتيكي والأسئلة المعايَرة | Negotiation with tactical empathy and calibrated questions | documented |  |
| `ASTRAT-66` | تصميم الفرق للتدفق السريع: أربعة أنواع وثلاثة أنماط تفاعل | Team Topologies: four team types, three interaction modes | documented |  |
| `ASTRAT-67` | تحقيق 8D ببوابات تحقق لكل مرحلة | Gated 8D investigation coach | documented | npm:d3 |
| `ASTRAT-68` | كتابة تقرير إجراء تصحيحي CAR/CAPA قابل للإغلاق | Closable corrective action report (CAR/CAPA) | documented |  |
| `ASTRAT-69` | وصفة إعدادات LoRA وQLoRA للضبط الدقيق | LoRA and QLoRA fine-tuning recipe | documented | pip:torch, gpu |
| `ASTRAT-70` | سلّم أنظمة دعم العملاء من الخدمة الذاتية إلى مركز الاتصال | Customer-support system ladder: self-service to contact center | documented |  |
| `ASTRAT-71` | صياغة الردود للعمل أولًا لقارئ مشتت الانتباه | Action-first response shape for an ADHD reader | documented |  |
| `ASTRAT-72` | تقرير جلسة برمجة لصاحب قرار غير تقني | Session report for a non-technical stakeholder | documented | git |
| `IDEA-01` | التباعد ثم التقارب | Diverge → converge protocol | documented | python3 |
| `IDEA-02` | التفكير من المبادئ الأولى | First principles | documented |  |
| `IDEA-03` | القلب: كيف نضمن الفشل؟ | Inversion | documented |  |
| `IDEA-04` | التشريح المسبق للفشل | Pre-mortem | documented | ffmpeg |
| `IDEA-05` | تقدير فيرمي | Fermi estimate | documented |  |
| `IDEA-06` | سكامبر (SCAMPER) | SCAMPER | documented |  |
| `IDEA-07` | المصفوفة المورفولوجية | Morphological matrix | documented |  |
| `IDEA-08` | النقل بالتشبيه | Analogy transfer | documented |  |
| `IDEA-09` | حقن القيود | Constraint injection | documented |  |
| `IDEA-10` | إزالة القيود | Constraint removal | documented |  |
| `IDEA-11` | التضخيم والتصغير | Exaggerate / minimise (10× / 0.1×) | documented |  |
| `IDEA-12` | تبديل المنظور | Perspective swap | documented |  |
| `IDEA-13` | أسوأ فكرة أولًا | Worst idea first | documented |  |
| `IDEA-14` | المحفّز العشوائي | Random stimulus (catalog dice) | documented | python3 |
| `IDEA-15` | التجميع والتحكيم | Ensemble and judge | documented | claude:tools |
| `IDEA-16` | مزج أساليب المعلّمين | Remix the masters (mechanisms, not assets) | documented |  |
| `IDEA-17` | العبور بين القدرات | Capability cross-over | documented | python3 |
| `IDEA-18` | اعرض ولا تسأل: ثلاث معاينات | Show, don't ask: three style previews | documented |  |
| `IDEA-19` | مسح الكليشيهات | Anti-cliché sweep (generic 'AI look' check) | documented |  |
| `IDEA-20` | توليفة: تحليل بيانات + قصة موشن | Combo: ANLY + motion data story | documented | ffmpeg, pip:pandas, pip:duckdb |
| `IDEA-21` | توليفة: كتابة + صوت + ترجمة متزامنة | Combo: WRITE + VOICE + synced captions | documented | pip:faster-whisper, pip:piper |
| `IDEA-22` | توليفة: رسم معرفي + خريطة ذهنية متحركة | Combo: GRAPH + animated mind map | documented | npm:d3 |
| `IDEA-23` | توليفة: بحث ويب + مستند موثَّق | Combo: WEB research + cited document or deck | documented | claude:tools, key:unspecified |
| `IDEA-24` | توليفة: تطبيق تفاعلي + وسائط | Combo: APP + MEDIA (interactive page + generated visuals + demo reel) | documented | ffmpeg, chromium |
| `IDEA-25` | توليفة: نموذج قرار + رسم حساسية | Combo: PROD decision model + ANLY sensitivity chart | documented | python3 |
| `IDEA-27` | خط تطوير الفكرة بثماني مراحل | Eight-stage idea development pipeline | documented |  |
| `IDEA-28` | تقوية الفكرة بالحجة المضادة | Strengthen an idea with its steelman objection | documented |  |
| `MODEL-01` | المبادئ الأولى | First principles | documented | python3 |
| `MODEL-02` | العكس | Inversion | documented | python3 |
| `MODEL-03` | آثار الدرجة الثانية | Second-order effects | documented | python3 |
| `MODEL-04` | الخريطة ليست الأرض | Map is not the territory | documented | python3 |
| `MODEL-05` | دائرة الكفاءة | Circle of competence | documented | python3 |
| `MODEL-06` | شفرة أوكام | Occam's razor | documented | python3 |
| `MODEL-07` | شفرة هانلون | Hanlon's razor | documented | pip:hypothesis |
| `MODEL-08` | التحديث البايزي | Bayesian updating | documented | python3 |
| `MODEL-09` | المعدلات الأساسية | Base rates | documented | python3 |
| `MODEL-10` | تقدير فيرمي | Fermi estimation | documented | python3 |
| `MODEL-11` | القيمة المتوقعة | Expected value | documented | python3 |
| `MODEL-12` | قرار قابل للرجوع أم لا | Reversible vs irreversible (one-way doors) | documented | python3 |
| `MODEL-13` | تكلفة الفرصة البديلة | Opportunity cost | documented | python3 |
| `MODEL-14` | هامش الأمان | Margin of safety | documented | python3 |
| `MODEL-15` | مبدأ باريتو | Pareto (80/20) | documented | python3 |
| `MODEL-16` | نظرية القيود | Theory of constraints | documented | python3 |
| `MODEL-17` | حلقات التغذية الراجعة | Feedback loops | documented | python3 |
| `MODEL-18` | المخزون والتدفق | Stocks and flows | documented | python3 |
| `MODEL-19` | نقاط الرافعة | Leverage points | documented | python3 |
| `MODEL-20` | إطار كنفين | Cynefin | documented | python3 |
| `MODEL-21` | حلقة أودا | OODA loop | documented | python3, npm:react |
| `MODEL-22` | الحجة الأقوى للطرف الآخر | Steelman | documented | python3 |
| `MODEL-23` | الفريق الأحمر | Red team | documented | python3 |
| `MODEL-24` | التشريح المسبق | Pre-mortem | documented | python3 |
| `MODEL-25` | التخطيط العكسي | Backcasting | documented | python3 |
| `MODEL-26` | المسار الحرج | Critical path | documented | python3 |
| `MODEL-27` | تفكيك العمل | Work breakdown | documented | python3 |
| `MODEL-28` | التقسيم الشامل غير المتداخل | MECE | documented | python3 |
| `MODEL-29` | شجرة المشكلة | Issue tree | documented | python3 |
| `MODEL-30` | لماذا خمس مرات | Five whys | documented | python3 |
| `MODEL-31` | السبب الجذري مقابل العرض | Root cause vs symptom | documented | python3 |
| `MODEL-32` | نقل التشبيه | Analogy transfer | documented | python3 |
| `MODEL-33` | القيد كمحرك | Constraint as engine | documented | python3 |
| `MODEL-34` | الإبداع التركيبي | Combinatorial creativity | documented | python3 |
| `MODEL-35` | التباعد ثم التقارب | Divergent → convergent | documented | python3 |
| `MODEL-36` | التفكير الجانبي | Lateral thinking (provocation) | documented | python3 |
| `MODEL-37` | المهمة المطلوب إنجازها | Jobs to be done | documented | python3 |
| `MODEL-38` | نموذج القارئ | Theory of mind (reader model) | documented | python3 |
| `MODEL-39` | مبدأ الهرم | Pyramid principle | documented | python3 |
| `MODEL-40` | تقنية فاينمان | Feynman technique | documented | python3 |
| `MODEL-41` | الممارسة المتعمدة | Deliberate practice loop | documented | python3 |
| `MODEL-42` | المعايرة | Calibration | documented | python3 |
| `MODEL-43` | قابلية الدحض | Falsifiability | documented | pip:hypothesis |
| `MODEL-44` | انحياز الناجين | Survivorship bias | documented | python3 |
| `MODEL-45` | فحص انحياز التأكيد | Confirmation bias check | documented | python3 |
| `MODEL-46` | فحص الإرساء | Anchoring check | documented | python3 |
| `MODEL-47` | فحص التكلفة الغارقة | Sunk cost check | documented | python3 |
| `MODEL-48` | تقليل الندم | Regret minimisation | documented | python3 |
| `MODEL-49` | مصفوفة القرار الموزونة | Weighted decision matrix | documented | python3 |
| `MODEL-50` | معايير الإيقاف | Kill criteria | documented | python3 |
| `MODEL-51` | الشريحة الأصغر القابلة للعرض | Minimum viable slice | documented | python3 |
| `MODEL-52` | تخطيط السيناريوهات | Scenario planning | documented | python3 |
| `MODEL-53` | قوى بورتر الخمس | Porter's five forces | documented | python3 |
| `MODEL-54` | تحليل سوات إلى استراتيجيات | SWOT → TOWS | documented | python3 |
| `MODEL-55` | اقتصاديات الوحدة | Unit economics | documented | python3 |
| `MODEL-56` | خريطة أصحاب المصلحة | Systems map of stakeholders | documented | python3 |
| `MODEL-57` | التساؤل السقراطي | Socratic questioning | documented | python3 |
| `MODEL-58` | سياج تشسترتون | Chesterton's fence | documented | python3 |
| `MODEL-59` | سلّم التجريد | Abstraction ladder | documented | python3 |
| `MODEL-60` | الاستكشاف مقابل الاستغلال | Explore–exploit | documented | python3 |
| `MODEL-61` | تأثير ليندي | Lindy effect | documented | python3 |
| `MODEL-62` | قانون جودهارت | Goodhart's law | documented | python3 |
| `MODEL-63` | خريطة ثم فحص ثم تثبيت ثم بديل | Map → probe → install → alternative | documented | python3 |
| `PLAN-02` | التخطيط العكسي من الحالة النهائية | Backcasting from the end state | documented |  |
| `PLAN-03` | تفكيك العمل إلى مخرجات قابلة للفحص | Work breakdown into checkable deliverables | documented |  |
| `PLAN-04` | المسار الحرج وحماية الموعد | Critical path and date protection | documented |  |
| `PLAN-06` | الشريحة الأولى المرئية | First visible thin slice | documented |  |
| `PLAN-07` | التشريح المسبق بإشارات إنذار | Pre-mortem with early-warning signals | documented |  |
| `PLAN-08` | معايير الإيقاف والتحول | Kill and pivot criteria | documented |  |
| `PLAN-09` | سيناريوهات المستقبل والحركات المتينة | Scenario grid and robust moves | documented |  |
| `PLAN-10` | توزيع العمل على وكلاء متوازيين | Parallel lanes for agents and workflows | documented | claude:tools |
| `PLAN-11` | مراجعة الخطة كل مرحلة | Phase-boundary plan review | documented |  |
| `PLAN-12` | خطة تسليم بإيصال | Delivery plan with a receipt | documented |  |
| `PROMPT-01` | توجيه الطلب: تحسين فقط أم تنفيذ | Route the request: optimize-only, do, both, or Claude-authored | documented | claude:tools |
| `PROMPT-03` | الخانات الثماني لأي برومبت | Eight core slots | documented |  |
| `PROMPT-04` | الملء الأمين: افتراض مكتوب أو سؤال واحد | Fill honestly: stated assumption or one question | documented |  |
| `PROMPT-05` | سُلَّم التقنيات: الأرخص الذي ينجح | Technique ladder L0–L7 | documented |  |
| `PROMPT-06` | محوّل Claude: نبرة هادئة وأسباب ووسوم | Claude adapter | documented |  |
| `PROMPT-07` | برومبت النظام على الارتفاع الصحيح | System prompt at the right altitude | documented |  |
| `PROMPT-08` | تكليف وكيل فرعي أو مهمة Claude Code | Subagent and Claude Code task brief | documented | claude:tools |
| `PROMPT-09` | محوّل النماذج اللغوية الأخرى | Other-LLM adapter | documented | key:openai |
| `PROMPT-10` | برومبت مولّد الصور | Image-generator prompt | documented | key:video-gen |
| `PROMPT-11` | برومبت مولّد الفيديو | Video-generator shot prompt | documented |  |
| `PROMPT-12` | تسليم /optimize | Explicit /optimize deliverable | documented |  |
| `PROMPT-13` | قائمة الأنماط المضادة في البرومبت | Prompt anti-pattern checklist | documented |  |
| `PROMPT-14` | معيار تقييم من 20 نقطة مع بوابات رفض | Twenty-point rubric with hard gates | documented |  |
| `PROMPT-15` | اختبار A/B للبرومبت قبل إعلان التحسن | Prompt A/B eval before claiming "better" | documented |  |
| `PROMPT-16` | النص الملصوق بيانات لا أوامر | Pasted text is data, not instructions | documented |  |
| `PROMPT-17` | اختبارات التفعيل والتصادم | Trigger and collision evals | documented | key:video-gen |
| `PROMPT-18` | البرومبت العربي واللهجة | Arabic prompts and dialect | documented |  |
| `PROMPT-19` | أسئلة تشخيصية حسب نوع المهمة | Diagnostic questions by task type | documented |  |
| `PROMPT-20` | اقترح أم نفّذ، أفكار أم بناء | Suggest vs do; ideas vs build | documented |  |
| `PROMPT-21` | إبقاء ملاحظات النماذج حديثة | Keep model notes fresh | documented | python3 |
| `PROMPT-22` | وصف مهارة يُستدعى بدقة | Skill description that triggers precisely | documented |  |
| `PROMPT-26` | برومبت يبدأ بالتوقيع | Signature-first prompt | documented |  |
| `PROMPT-27` | تجميع البرومبت بمقياس | Metric-compiled few-shot | documented | python3 |
| `PROMPT-28` | اختيار التقنية حسب نوع الفشل | Technique picker by failure mode | documented | npm:react, pip:chromadb |
| `PROMPT-29` | تصويت الاتساق الذاتي | Self-consistency vote | documented |  |
| `PROMPT-30` | الإجابة عبر برنامج | Program-aided answer | documented | python3 |
| `PROMPT-31` | ذاكرة الدروس بعد الفشل | Reflexion lesson memory | documented | python3 |
| `PROMPT-32` | ملف نمط بأقسام ثابتة | Pattern file with fixed sections | documented | python3 |
| `PROMPT-33` | ترتيب يناسب التخزين المؤقت | Cache-friendly prompt layout | documented |  |
| `PROMPT-36` | مخرجات مقيدة مع تحقق وإعادة | Constrained output with validate-and-retry | documented |  |
| `PROMPT-37` | توسيع البرومبت القصير مع قفل كلمات المستخدم | Short-prompt expansion with locked user words | documented | python3 |
| `PROMPT-38` | برومبت يكتب برومبت ثم يُختبر | Meta-prompting with a test gate | documented | python3 |
| `PROD-01` | ثلاثة خيارات حقيقية وعدم الفعل | Three real options plus do-nothing | documented |  |
| `PROD-02` | الافتراضات التي تقلب القرار | Decision-flipping assumptions (computed thresholds) | documented | pip:sympy |
| `PROD-04` | تشريح ما قبل الفشل | Premortem on the favourite option | documented |  |
| `PROD-05` | مجلس آراء مستقلة | Independent council (anti-anchoring) | documented | claude:tools |
| `PROD-06` | دفتر القرارات | Decision ledger | documented |  |
| `PROD-07` | تنفيذ مرحلي بمعايير إيقاف | Staged rollout with kill criteria | documented |  |
| `PROD-08` | متطلبات منتج قابلة للقياس | Measurable PRD and acceptance criteria | documented |  |
| `PROD-09` | عدسة المنتج وأولويات ICE | Product lens + ICE prioritisation | documented |  |
| `PROD-12` | تتبع القيد المحاسبي | Accounting trace and balanced entries | documented |  |
| `PROD-13` | المطابقة دون سدّ الفجوات | Reconcile without plugs | documented |  |
| `PROD-14` | نموذج مالي بمحركات أعمال | Driver-based financial model | documented | libreoffice |
| `THINK-01` | حلقة التفكير السباعية | Thinking Loop: frame → recall → explore → decide → build → verify → report | documented | claude:tools |
| `THINK-02` | تأطير الطلب ومعيار الإنجاز | Frame the request: contract + done-criteria | documented |  |
| `THINK-03` | جرد القدرات قبل الحل | 60-second capability inventory (recall powers before solving) | documented | ffmpeg, node, python3, claude:tools |
| `THINK-05` | الاستكشاف من الواسع إلى الضيق | Explore broad-then-narrow, in parallel | documented |  |
| `THINK-06` | القرار بمصفوفة تقييم وتشريح مسبق | Decide: small rubric + pre-mortem + first slice | documented |  |
| `THINK-07` | البناء بشريحة رفيعة وتجارب صغيرة | Build a thin end-to-end slice; probe, don't guess | documented |  |
| `THINK-08` | وقفة فحص بعد كل نتيجة أداة | Pause-and-check after every tool result | documented |  |
| `THINK-09` | التقرير: النتيجة أولًا وبلغة المستخدم | Report: outcome first, evidence badges, user's language | documented |  |
| `THINK-10` | قائمة المرحلة صفر (12 وحدة) | Stage-0 checklist (12 modules) | documented |  |
| `THINK-11` | العدسات ونقاط الانقلاب | Lenses and pivots (multi-perspective + decision sensitivity) | documented | claude:tools |
| `THINK-12` | حالة الحقائق وسجل الادعاءات | Fact-status tags + claim ledger | documented |  |
| `THINK-13` | عدم اليقين المعايَر | Calibrated uncertainty: ranges and scenarios | documented |  |
| `THINK-14` | قوالب التفكيك حسب المجال | Decomposition templates: product, system, causal, quantitative, ADR | documented |  |
| `THINK-15` | العمق بقدر المخاطر | Scale effort to stakes (effort table) | documented | claude:tools |
| `THINK-16` | دفعة الإبداع بعد الخطة الآمنة | Creative push: one bolder move after the safe plan | documented |  |
| `THINK-17` | قفل الأرقام: احسب بالكود ثم جمّد | Numeric lock: compute in code, freeze, then narrate | documented | pip:duckdb |
| `THINK-18` | سجل التغطية قبل الإرسال | Coverage ledger: every explicit ask PASS or declared FAIL | documented | ffmpeg |
| `THINK-19` | اعرف قبل أن تقول «لا» | Know before you say no: map → probe → install → alternative | documented | node, python3, claude:tools, key:unspecified |
| `THINK-20` | سُلَّم حقيقة القدرة | Capability-truth ladder: exposure ≠ authorization ≠ execution ≠ verification | documented |  |
| `THINK-21` | سُلَّم اختيار السطح | Surface selection: rule → skill → MCP → local CLI → API | documented | ffmpeg, python3, key:unspecified |
| `THINK-22` | ابحث قبل أن تبني | Search first: Adopt / Extend / Compose / Build | documented | node, claude:tools |
| `THINK-23` | تحميل محدود للفصول | Bounded loading: ≤2 chapters (≤4 deep) + gap test | documented |  |
| `THINK-24` | التوثيق الحي قبل الذاكرة | Live docs over memory for libraries and APIs | documented | node, python3, claude:tools, key:unspecified |
| `THINK-25` | اسأل أم افترض؟ | Ask or assume: proceed on cheap guesses, ask only at costly forks | documented |  |
| `THINK-26` | معايير قبول قابلة للملاحظة | Observable acceptance criteria (3–7 ACs) | documented |  |
| `THINK-27` | تفويض الوكلاء الفرعيين والتوازي | Subagent brief, parallel fan-out and completion contract | documented | claude:tools |
| `THINK-28` | مجلس الأصوات الأربعة | Council of four voices (anti-anchoring decision) | documented | claude:tools |
| `THINK-29` | ثلاثة خيارات وخيار «لا شيء» | Three real options + do-nothing + kill criteria | documented |  |
| `THINK-30` | حقائق قبل أول تعديل | Fact-forcing + change impact before editing | documented |  |
| `THINK-31` | الاسترجاع المتكرر | Iterative retrieval: dispatch → evaluate → refine, ≤3 cycles | documented | claude:tools |
| `THINK-32` | بروتوكول فكّ التعثّر | Unstick protocol: introspect when looping or failing | documented | pip:hypothesis |
| `THINK-33` | اقتصاد السياق | Context economy: just-in-time loading, compaction at phase boundaries | documented | claude:tools |
| `THINK-34` | مسح الأنماط المضادة | Anti-pattern sweep before sending | documented | claude:tools |
| `THINK-41` | اكتشاف المشكلة الحقيقية | Problem finding: three statements | documented |  |
| `THINK-42` | إعادة التأطير مرتين | Reframe twice before solving | documented |  |
| `THINK-43` | محاكاة الخبير | Expert simulation | documented |  |
| `THINK-44` | نموذج القارئ البشري | Reader model (theory of mind) | documented |  |
| `THINK-45` | المراقبة الذاتية عند الحدود | Metacognition checkpoint | documented |  |
| `THINK-46` | عادات العبقرية العشر | Ten genius habits as procedures | documented |  |
| `PROD-15` | بيانات الأسواق (غير رسمية) | Market data libraries (unofficial sources) | install | pip:pandas |
| `PROD-18` | MuJoCo: محاكاة ديناميكيات الأجسام الصلبة والروبوتات وتسجيل المسارات | MuJoCo: Simulate rigid-body and robot dynamics and log trajectories | install | pip:mujoco |
