# النماذج الذهنية / mental models

> مولّد من `data/mental_models.json`. [الفهرس](../README.md)

## المبادئ الأولى / First principles (`MODEL-01`)

**discipline:** reasoning

**triggers:**

- why
- cost
- new design
- from scratch
- impossible
- مستحيل
- من الصفر
- تكلفة

**question:** What is true here regardless of how it is usually done?

**steps:**

- List the assumptions behind the usual approach
- Strike each one that is convention rather than law
- Rebuild the solution from the remaining facts and constraints

**output:** a solution path derived from facts, with the dropped conventions named

**pitfall:** stopping at the first convention that feels like physics

## العكس / Inversion (`MODEL-02`)

**discipline:** reasoning

**triggers:**

- fail
- avoid
- risk
- mistake
- خطأ
- فشل
- تجنب

**question:** What would guarantee failure, and how do I avoid each item?

**steps:**

- Write the recipe for the worst outcome
- Turn each ingredient into a guard or check
- Keep the three guards that prevent most damage

**output:** a short avoid-list turned into checks

**pitfall:** listing failures without converting them into actions

## آثار الدرجة الثانية / Second-order effects (`MODEL-03`)

**discipline:** systems

**triggers:**

- consequence
- then what
- policy
- change
- impact
- أثر
- نتيجة
- تغيير

**question:** And then what happens, one and two steps later?

**steps:**

- State the immediate effect
- Ask 'and then?' twice for each stakeholder
- Flag effects that reverse the first-order gain

**output:** an effects chain per stakeholder

**pitfall:** treating the first effect as the whole story

## الخريطة ليست الأرض / Map is not the territory (`MODEL-04`)

**discipline:** epistemics

**triggers:**

- model
- assumption
- data
- metric
- مؤشر
- نموذج

**question:** Where does my model differ from what is really there?

**steps:**

- Name the model or metric you are using
- List what it leaves out
- Check one omitted thing against reality before deciding

**output:** the model's blind spots and one reality check

**pitfall:** optimising the metric instead of the goal

## دائرة الكفاءة / Circle of competence (`MODEL-05`)

**discipline:** epistemics

**triggers:**

- expert
- unsure
- domain
- outside
- لست متأكد
- تخصص

**question:** Is this inside what I can verify, or outside it?

**steps:**

- Mark which parts you can check with tools or sources
- For the rest, find a source, a test or an expert
- Say plainly which claims are outside the circle

**output:** claims split into verified / sourced / outside

**pitfall:** confident tone on unverifiable parts

## شفرة أوكام / Occam's razor (`MODEL-06`)

**discipline:** reasoning

**triggers:**

- explain
- cause
- bug
- why does
- سبب
- تفسير

**question:** Which explanation needs the fewest new assumptions?

**steps:**

- List candidate explanations
- Count the extra assumptions each needs
- Test the simplest first, keep the others alive

**output:** a ranked list of explanations with the first test

**pitfall:** using simplicity as proof instead of as test order

## شفرة هانلون / Hanlon's razor (`MODEL-07`)

**discipline:** people

**triggers:**

- blame
- intent
- conflict
- why did they
- لماذا فعل
- خلاف

**question:** Is there a non-malicious explanation (missing info, rushed, unclear)?

**steps:**

- Assume the most charitable plausible cause
- Check it with one question or fact
- Escalate only if the evidence says otherwise

**output:** a charitable hypothesis and how to test it

**pitfall:** excusing repeated, evidenced harm

## التحديث البايزي / Bayesian updating (`MODEL-08`)

**discipline:** probability

**triggers:**

- probability
- likely
- evidence
- chance
- احتمال
- دليل

**question:** How much should this new evidence move my belief?

**steps:**

- State a prior as a number
- Estimate how much more likely the evidence is if true vs false
- Update proportionally and write the new number

**output:** prior → likelihood ratio → posterior, in numbers

**pitfall:** ignoring base rates

## المعدلات الأساسية / Base rates (`MODEL-09`)

**discipline:** probability

**triggers:**

- forecast
- estimate
- how often
- success rate
- نسبة
- توقع

**question:** How often does this kind of thing happen in general?

**steps:**

- Find the reference class
- Get its base rate from data or a source
- Adjust from the base rate only for specific evidence

**output:** an estimate anchored on a reference class

**pitfall:** starting from the vivid case

## تقدير فيرمي / Fermi estimation (`MODEL-10`)

**discipline:** quantitative

**triggers:**

- how many
- estimate
- size
- market
- rough
- كم
- تقدير
- حجم

**question:** Can I break the unknown number into factors I can estimate?

**steps:**

- Decompose into 3–6 multiplied factors
- Estimate each with a range
- Multiply in code; report the range, not one number

**output:** a range with its factor tree

**pitfall:** false precision

## القيمة المتوقعة / Expected value (`MODEL-11`)

**discipline:** decision

**triggers:**

- bet
- worth it
- gamble
- option
- يستحق
- رهان

**question:** Probability × payoff, summed over outcomes: which option wins?

**steps:**

- List outcomes per option with probability and value
- Compute EV in code
- Check the worst case is survivable

**output:** EV per option plus worst case

**pitfall:** ignoring ruin risk

## قرار قابل للرجوع أم لا / Reversible vs irreversible (one-way doors) (`MODEL-12`)

**discipline:** decision

**triggers:**

- decide
- commit
- launch
- delete
- migrate
- نهائي
- حذف
- إطلاق

**question:** Can this be undone cheaply?

**steps:**

- Classify the decision as two-way or one-way door
- Two-way: decide fast with 70% info
- One-way: slow down, gather evidence, get consent

**output:** door type and the matching speed

**pitfall:** treating every decision as irreversible

## تكلفة الفرصة البديلة / Opportunity cost (`MODEL-13`)

**discipline:** economics

**triggers:**

- priority
- time
- budget
- choose
- أولوية
- ميزانية
- وقت

**question:** What is the best thing I give up by doing this?

**steps:**

- Name the next-best use of the same time or money
- Compare value, not just cost
- Drop work whose value is below that line

**output:** the alternative and why this beats it

**pitfall:** comparing against doing nothing

## هامش الأمان / Margin of safety (`MODEL-14`)

**discipline:** engineering

**triggers:**

- deadline
- estimate
- capacity
- limit
- موعد
- سعة

**question:** How much buffer protects me if my estimate is wrong?

**steps:**

- Estimate the expected need
- Add a buffer proportional to uncertainty
- Design so failure inside the buffer is harmless

**output:** plan with explicit buffers

**pitfall:** buffers on every task (hidden padding)

## مبدأ باريتو / Pareto (80/20) (`MODEL-15`)

**discipline:** prioritisation

**triggers:**

- most important
- focus
- quick win
- أهم
- تركيز

**question:** Which 20% of the work gives 80% of the value?

**steps:**

- List the parts and their value
- Rank by value per effort
- Do the top slice first and re-measure

**output:** a ranked slice to do first

**pitfall:** assuming the ratio without measuring

## نظرية القيود / Theory of constraints (`MODEL-16`)

**discipline:** systems

**triggers:**

- bottleneck
- slow
- throughput
- pipeline
- بطء
- اختناق

**question:** Where is the single bottleneck that limits the whole system?

**steps:**

- Find the step with the longest queue or wait
- Exploit it fully before adding anything
- Subordinate other steps to it, then re-find the bottleneck

**output:** the bottleneck and one action on it

**pitfall:** optimising non-bottlenecks

## حلقات التغذية الراجعة / Feedback loops (`MODEL-17`)

**discipline:** systems

**triggers:**

- growth
- spiral
- stable
- viral
- dynamics
- نمو
- دوامة

**question:** Which loops reinforce and which balance?

**steps:**

- Draw causes as arrows with + or −
- Mark reinforcing and balancing loops
- Find the delay in each loop and where to intervene

**output:** a causal loop sketch with leverage points

**pitfall:** ignoring delays

## المخزون والتدفق / Stocks and flows (`MODEL-18`)

**discipline:** systems

**triggers:**

- accumulate
- backlog
- inventory
- debt
- تراكم
- تراكمات

**question:** What accumulates, and what fills or drains it?

**steps:**

- Name the stock
- Name inflows and outflows with rates
- Change the flow, then predict the stock over time in code

**output:** a stock-flow model with a projection

**pitfall:** confusing level with rate

## نقاط الرافعة / Leverage points (`MODEL-19`)

**discipline:** systems

**triggers:**

- change system
- intervene
- strategy
- تأثير
- رافعة

**question:** Where does a small change shift the whole system?

**steps:**

- List parameters, loops, rules, goals and mindsets
- Prefer higher leverage (rules, goals) when feasible
- Pick one intervention and its expected effect

**output:** a chosen intervention with its level

**pitfall:** only tweaking parameters

## إطار كنفين / Cynefin (`MODEL-20`)

**discipline:** complexity

**triggers:**

- unclear
- complex
- chaos
- new problem
- غامض
- معقد
- فوضى

**question:** Is this clear, complicated, complex or chaotic?

**steps:**

- Classify the situation
- Clear: apply best practice; complicated: analyse; complex: probe-sense-respond; chaotic: act to stabilise
- Pick the matching first move

**output:** domain label and first move

**pitfall:** analysing a complex problem as if it were complicated

## حلقة أودا / OODA loop (`MODEL-21`)

**discipline:** decision

**triggers:**

- fast
- competition
- react
- live
- سريع
- منافسة

**question:** Observe, orient, decide, act — how do I tighten the loop?

**steps:**

- Observe fresh signals
- Orient: update the mental model
- Decide and act on a small step, then loop

**output:** a short loop with the next step

**pitfall:** orientation frozen on old assumptions

## الحجة الأقوى للطرف الآخر / Steelman (`MODEL-22`)

**discipline:** argument

**triggers:**

- disagree
- debate
- critique
- opposite view
- رأي مخالف
- نقد

**question:** What is the strongest version of the view I reject?

**steps:**

- State the opposing view better than its holders
- Find what it gets right
- Update or answer that strongest form

**output:** the steelman and your reply

**pitfall:** arguing with a strawman

## الفريق الأحمر / Red team (`MODEL-23`)

**discipline:** argument

**triggers:**

- review
- attack
- weakness
- security
- ثغرة
- مراجعة

**question:** If I wanted to break or refute this, how would I?

**steps:**

- Switch role to an adversary
- List the three most damaging attacks
- Fix or disclose each

**output:** attack list with fixes

**pitfall:** attacking only the easy parts

## التشريح المسبق / Pre-mortem (`MODEL-24`)

**discipline:** planning

**triggers:**

- plan
- project
- launch
- risk
- خطة
- مشروع
- إطلاق

**question:** It failed six months from now — why?

**steps:**

- Imagine the failure vividly
- Write the top causes
- Turn each into a mitigation or an early warning signal

**output:** failure causes with mitigations and signals

**pitfall:** generic risks with no signal

## التخطيط العكسي / Backcasting (`MODEL-25`)

**discipline:** planning

**triggers:**

- goal
- vision
- roadmap
- target
- هدف
- رؤية
- خارطة

**question:** Starting from the finished goal, what must be true just before it?

**steps:**

- Describe the end state concretely
- Step backwards to the conditions that precede it
- Stop when you reach today; reverse the list into a plan

**output:** milestones derived from the goal

**pitfall:** planning forward from habits

## المسار الحرج / Critical path (`MODEL-26`)

**discipline:** planning

**triggers:**

- schedule
- dependencies
- timeline
- جدول
- مواعيد
- اعتماديات

**question:** Which chain of dependent tasks decides the finish date?

**steps:**

- List tasks with durations and dependencies
- Compute the longest path in code
- Protect that path; parallelise the rest

**output:** critical path and slack per task

**pitfall:** adding resources off the critical path

## تفكيك العمل / Work breakdown (`MODEL-27`)

**discipline:** planning

**triggers:**

- big task
- break down
- steps
- كبير
- مراحل
- خطوات

**question:** What are the smallest deliverable pieces, each with a done-test?

**steps:**

- Split the outcome into deliverables
- Split each into tasks under a few hours
- Give every task an observable done criterion

**output:** a WBS with done criteria

**pitfall:** splitting by activity instead of deliverable

## التقسيم الشامل غير المتداخل / MECE (`MODEL-28`)

**discipline:** structuring

**triggers:**

- structure
- categories
- analysis
- options
- تصنيف
- هيكلة

**question:** Are my categories mutually exclusive and collectively exhaustive?

**steps:**

- Draft the buckets
- Check overlaps and gaps
- Rename or split until each item fits exactly one

**output:** a clean issue tree

**pitfall:** forcing MECE on fuzzy human topics

## شجرة المشكلة / Issue tree (`MODEL-29`)

**discipline:** structuring

**triggers:**

- problem
- diagnose
- root cause
- مشكلة
- تشخيص

**question:** What sub-questions, answered, solve the main question?

**steps:**

- Write the key question
- Branch into 3–5 MECE sub-questions
- Attach a test or data source to each leaf

**output:** an issue tree with tests

**pitfall:** branches without tests

## لماذا خمس مرات / Five whys (`MODEL-30`)

**discipline:** diagnosis

**triggers:**

- root cause
- incident
- bug
- why
- سبب جذري
- عطل

**question:** Why did that happen — and why that?

**steps:**

- Ask why until you reach a process or design cause
- Check each link with evidence
- Fix the deepest controllable cause

**output:** causal chain with evidence

**pitfall:** one linear chain for a multi-cause failure

## السبب الجذري مقابل العرض / Root cause vs symptom (`MODEL-31`)

**discipline:** diagnosis

**triggers:**

- fix
- recurring
- again
- يتكرر
- إصلاح

**question:** Am I fixing the producer of the problem or patching its output?

**steps:**

- Trace the bad output to where it is produced
- Fix there
- Remove downstream patches made unnecessary

**output:** fix at the producing boundary

**pitfall:** stacking patches

## نقل التشبيه / Analogy transfer (`MODEL-32`)

**discipline:** creativity

**triggers:**

- idea
- inspiration
- creative
- new approach
- فكرة
- إبداع

**question:** Which distant field already solved a problem with this shape?

**steps:**

- Describe the problem abstractly
- Find two fields with the same structure
- Port the mechanism, not the surface

**output:** borrowed mechanism with the adaptation

**pitfall:** copying surface features

## القيد كمحرك / Constraint as engine (`MODEL-33`)

**discipline:** creativity

**triggers:**

- boring
- generic
- stuck
- cliché
- ممل
- تقليدي

**question:** What deliberate constraint would force an original answer?

**steps:**

- Add one hard constraint (one colour, no words, 3 s)
- Generate under it
- Keep what survives when the constraint is lifted

**output:** ideas born from a constraint

**pitfall:** constraints that only shrink quality

## الإبداع التركيبي / Combinatorial creativity (`MODEL-34`)

**discipline:** creativity

**triggers:**

- combine
- new idea
- mashup
- دمج
- فكرة جديدة

**question:** Which two unrelated elements fuse into something new?

**steps:**

- List elements from different domains
- Pair them randomly or systematically
- Score pairs for novelty × feasibility

**output:** a scored combination matrix

**pitfall:** only combining neighbours

## التباعد ثم التقارب / Divergent → convergent (`MODEL-35`)

**discipline:** creativity

**triggers:**

- brainstorm
- options
- ideas
- عصف
- خيارات

**question:** Have I generated widely before judging?

**steps:**

- Generate many options without judgement
- Cluster them
- Converge with explicit criteria

**output:** many options → shortlist → pick

**pitfall:** judging during generation

## التفكير الجانبي / Lateral thinking (provocation) (`MODEL-36`)

**discipline:** creativity

**triggers:**

- stuck
- no idea
- fresh
- عالق

**question:** What absurd statement could move me to a new position?

**steps:**

- Make a deliberate provocation ('the video has no picture')
- Extract the movement from it
- Shape the movement into a usable idea

**output:** a provocation and the idea it moved to

**pitfall:** stopping at the absurd

## المهمة المطلوب إنجازها / Jobs to be done (`MODEL-37`)

**discipline:** product

**triggers:**

- user
- customer
- feature
- need
- مستخدم
- عميل
- احتياج

**question:** What job is the user hiring this for, in their situation?

**steps:**

- Write: when <situation>, I want <motivation>, so I can <outcome>
- Find what they use today
- Design against that job, not the feature list

**output:** job statement and the current alternative

**pitfall:** asking users for features

## نموذج القارئ / Theory of mind (reader model) (`MODEL-38`)

**discipline:** communication

**triggers:**

- explain
- write
- audience
- client
- شرح
- جمهور
- عميل

**question:** What does this reader already know, want and fear?

**steps:**

- Describe the reader in two lines
- Remove what they know, add what they lack
- Order by what they need to decide

**output:** a reader model and an edited message

**pitfall:** writing for yourself

## مبدأ الهرم / Pyramid principle (`MODEL-39`)

**discipline:** communication

**triggers:**

- report
- summary
- recommend
- تقرير
- ملخص
- توصية

**question:** Does the answer come first, with supporting points grouped below?

**steps:**

- State the conclusion
- Group 3 supporting arguments
- Support each with evidence

**output:** conclusion-first structure

**pitfall:** building up to the point

## تقنية فاينمان / Feynman technique (`MODEL-40`)

**discipline:** learning

**triggers:**

- learn
- understand
- explain simply
- تعلم
- فهم
- ببساطة

**question:** Can I explain it simply enough for a newcomer?

**steps:**

- Explain in plain words
- Find where the explanation breaks
- Go back to the source for those gaps and re-explain

**output:** a simple explanation with the gaps fixed

**pitfall:** simplifying away the truth

## الممارسة المتعمدة / Deliberate practice loop (`MODEL-41`)

**discipline:** learning

**triggers:**

- improve
- skill
- quality
- تحسين
- مهارة
- جودة

**question:** What exact sub-skill failed, and what drill fixes it?

**steps:**

- Isolate the weakest sub-skill from evidence
- Design a short targeted attempt
- Measure, adjust, repeat

**output:** drill plan with a metric

**pitfall:** repeating whole tasks without feedback

## المعايرة / Calibration (`MODEL-42`)

**discipline:** epistemics

**triggers:**

- confidence
- sure
- certain
- متأكد
- ثقة

**question:** If I say 80%, am I right about 80% of the time?

**steps:**

- Attach a probability to key claims
- Prefer ranges for numbers
- Lower confidence where you have no check

**output:** claims with calibrated confidence

**pitfall:** 100% language for guesses

## قابلية الدحض / Falsifiability (`MODEL-43`)

**discipline:** epistemics

**triggers:**

- hypothesis
- claim
- theory
- test
- فرضية
- ادعاء

**question:** What observation would prove this wrong?

**steps:**

- State the claim precisely
- Write the result that would refute it
- Run or name that test

**output:** claim + refutation test

**pitfall:** unfalsifiable claims

## انحياز الناجين / Survivorship bias (`MODEL-44`)

**discipline:** biases

**triggers:**

- success story
- best practices
- winners
- قصة نجاح

**question:** What about the cases that failed and are not visible?

**steps:**

- Ask where the failures went
- Look for the silent denominator
- Re-judge the pattern with them

**output:** pattern checked against failures

**pitfall:** copying winners' habits

## فحص انحياز التأكيد / Confirmation bias check (`MODEL-45`)

**discipline:** biases

**triggers:**

- my idea
- prove
- agree
- أثبت
- فكرتي

**question:** Have I looked for evidence that would change my mind?

**steps:**

- Write what would disconfirm you
- Search for it first
- Report what you found either way

**output:** disconfirming search and its result

**pitfall:** searching only for support

## فحص الإرساء / Anchoring check (`MODEL-46`)

**discipline:** biases

**triggers:**

- estimate
- price
- number
- رقم
- سعر

**question:** Is my number pulled toward the first number I saw?

**steps:**

- Note the anchor
- Estimate independently from a reference class
- Compare and reconcile

**output:** independent estimate vs anchor

**pitfall:** adjusting slightly from the anchor

## فحص التكلفة الغارقة / Sunk cost check (`MODEL-47`)

**discipline:** biases

**triggers:**

- already spent
- continue
- abandon
- صرفنا
- نكمل

**question:** Would I start this today, knowing what I know?

**steps:**

- Ignore what is already spent
- Compare future cost vs future value
- Continue only if today you would start

**output:** continue/stop on future value

**pitfall:** finishing because of past effort

## تقليل الندم / Regret minimisation (`MODEL-48`)

**discipline:** decision

**triggers:**

- life decision
- career
- big choice
- قرار كبير

**question:** Which choice will I regret less in ten years?

**steps:**

- Project yourself forward
- Name the regret for each option
- Choose the one with the smaller lasting regret

**output:** regret comparison

**pitfall:** using it for small decisions

## مصفوفة القرار الموزونة / Weighted decision matrix (`MODEL-49`)

**discipline:** decision

**triggers:**

- compare
- choose
- options
- vendor
- tool
- اختيار
- مقارنة
- أداة

**question:** Which option wins on weighted criteria, and does the winner survive weight changes?

**steps:**

- List options and 3–6 criteria with weights
- Score 1–5 and compute in code
- Run a sensitivity check (±1 on each weight)

**output:** scores, winner and whether it flips

**pitfall:** precise weights for fuzzy criteria

## معايير الإيقاف / Kill criteria (`MODEL-50`)

**discipline:** planning

**triggers:**

- experiment
- pilot
- bet
- تجربة
- رهان

**question:** What signal, by when, makes us stop?

**steps:**

- Write a measurable stop signal and a date
- Agree on it before starting
- Check it at the date and act

**output:** stop signal + date

**pitfall:** moving the goalposts

## الشريحة الأصغر القابلة للعرض / Minimum viable slice (`MODEL-51`)

**discipline:** planning

**triggers:**

- start
- prototype
- mvp
- first step
- نموذج أولي
- نبدأ

**question:** What is the thinnest end-to-end version that shows the idea working?

**steps:**

- Cut scope to one path through every layer
- Build and show it
- Expand from feedback

**output:** a thin slice plan

**pitfall:** building one layer completely first

## تخطيط السيناريوهات / Scenario planning (`MODEL-52`)

**discipline:** strategy

**triggers:**

- future
- uncertain
- strategy
- مستقبل
- استراتيجية

**question:** What are 3–4 plausible futures, and which moves work in all?

**steps:**

- Pick two key uncertainties
- Cross them into four scenarios
- Find robust moves and signposts

**output:** scenario grid with robust moves

**pitfall:** predicting one future

## قوى بورتر الخمس / Porter's five forces (`MODEL-53`)

**discipline:** strategy

**triggers:**

- market
- competition
- industry
- سوق
- منافسين

**question:** How strong are rivals, entrants, substitutes, buyers and suppliers?

**steps:**

- Rate each force with evidence
- Find the force that caps profit
- Plan a move against it

**output:** forces table with the binding force

**pitfall:** rating without evidence

## تحليل سوات إلى استراتيجيات / SWOT → TOWS (`MODEL-54`)

**discipline:** strategy

**triggers:**

- swot
- position
- plan
- خطة
- وضع

**question:** Which strengths meet which opportunities, and which weaknesses meet which threats?

**steps:**

- List S, W, O, T with evidence
- Pair them into SO/ST/WO/WT moves
- Pick the top two moves

**output:** paired strategic moves

**pitfall:** a SWOT list with no moves

## اقتصاديات الوحدة / Unit economics (`MODEL-55`)

**discipline:** economics

**triggers:**

- pricing
- profit
- cac
- ltv
- تسعير
- ربح

**question:** Does one unit make money once all costs are counted?

**steps:**

- Define the unit
- Compute revenue and variable costs per unit in code
- Check payback and contribution margin

**output:** per-unit P&L

**pitfall:** ignoring variable costs

## خريطة أصحاب المصلحة / Systems map of stakeholders (`MODEL-56`)

**discipline:** people

**triggers:**

- stakeholders
- team
- politics
- أصحاب المصلحة
- فريق

**question:** Who gains, who loses, who decides?

**steps:**

- List stakeholders with interest and power
- Mark supporters, blockers, deciders
- Plan one message per group

**output:** stakeholder grid and messages

**pitfall:** ignoring silent blockers

## التساؤل السقراطي / Socratic questioning (`MODEL-57`)

**discipline:** learning

**triggers:**

- clarify
- assumption
- deep
- توضيح
- افتراض

**question:** What do you mean, how do you know, and what follows?

**steps:**

- Clarify terms
- Probe evidence and assumptions
- Explore implications and alternatives

**output:** a question sequence that exposes assumptions

**pitfall:** interrogating instead of exploring

## سياج تشسترتون / Chesterton's fence (`MODEL-58`)

**discipline:** engineering

**triggers:**

- remove
- refactor
- legacy
- delete
- حذف
- قديم

**question:** Do I know why this exists before removing it?

**steps:**

- Find the reason the thing was added (history, owner, tests)
- Decide with that reason in view
- Remove only with a replacement for its purpose

**output:** origin found before change

**pitfall:** removing what you do not understand

## سلّم التجريد / Abstraction ladder (`MODEL-59`)

**discipline:** communication

**triggers:**

- too abstract
- too detailed
- example
- مثال
- تجريد

**question:** Should I move up (why) or down (how, example)?

**steps:**

- Ask why to climb to purpose
- Ask how to descend to concrete steps
- Pair each abstract claim with one concrete example

**output:** message anchored at the right level

**pitfall:** staying at one level

## الاستكشاف مقابل الاستغلال / Explore–exploit (`MODEL-60`)

**discipline:** decision

**triggers:**

- try new
- stick
- option
- experiment
- نجرب

**question:** Should I try something new or use what is known to work?

**steps:**

- Estimate remaining horizon
- Explore more early or when stakes are low
- Exploit when time is short

**output:** explore/exploit choice with reason

**pitfall:** never exploring

## تأثير ليندي / Lindy effect (`MODEL-61`)

**discipline:** forecasting

**triggers:**

- new tech
- trend
- library choice
- مكتبة
- تقنية

**question:** Has this lasted long enough to probably keep lasting?

**steps:**

- Check age and maintenance history
- Prefer older, maintained options for foundations
- Use new ones where swapping is cheap

**output:** durability-weighted choice

**pitfall:** dismissing anything new

## قانون جودهارت / Goodhart's law (`MODEL-62`)

**discipline:** epistemics

**triggers:**

- kpi
- metric
- target
- benchmark
- مؤشر
- هدف

**question:** Will optimising this metric stop it measuring what I care about?

**steps:**

- Name the real goal
- Pair the metric with a counter-metric
- Audit samples by hand

**output:** metric pair and an audit

**pitfall:** rewarding the number

## خريطة ثم فحص ثم تثبيت ثم بديل / Map → probe → install → alternative (`MODEL-63`)

**discipline:** capability

**triggers:**

- can you
- not available
- install
- تقدر
- غير متاح
- تثبيت

**question:** Is it truly impossible, or one install away?

**steps:**

- Search the capability map
- Probe the machine
- Install in a sandbox and test
- Only then offer an alternative

**output:** a capability verdict with evidence

**pitfall:** saying no before probing

