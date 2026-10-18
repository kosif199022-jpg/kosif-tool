# العقل الفائق — Cognition: how to think at expert and genius level

> **لماذا هذا الملف؟** القدرات بلا تفكير جيد تنتج عملًا متوسطًا. هذا الدليل يحوّل «فكّر جيدًا» إلى إجراءات قابلة للتنفيذ والفحص: سلّم مستويات التفكير، عادات العباقرة، تطوير الأفكار، التخطيط، القرار، ونموذج القارئ البشري. كل إجراء له أمر في `scripts/think.py` أو سجل في الكتالوج.
> **Why:** powers without good thinking produce average work. This file turns "think well" into procedures you can run and check. Executable parts live in `scripts/think.py`; the 63 mental models in `data/mental_models.json` (family `mental-models`, MODEL-01…63).

## الفهرس / contents
1. [سلّم التفكير / the cognition ladder](#ladder)
2. [حلقة العمل الفائقة / the expert loop](#loop)
3. [عادات العباقرة / genius habits](#genius)
4. [تطوير الأفكار / idea development](#ideas)
5. [التخطيط / planning](#planning)
6. [القرار تحت عدم اليقين / deciding under uncertainty](#deciding)
7. [التفكير الشبيه بالبشر / human-like reasoning and communication](#human)
8. [المراقبة الذاتية / metacognition](#meta)
9. [النماذج الذهنية / mental models](#models)
10. [الأوامر / commands](#commands)

<a id="ladder"></a>
## 1. سلّم التفكير / the cognition ladder

Match the depth of thinking to the task. Under-thinking a design task is as costly as over-thinking a lookup. `python3 $SKILL_DIR/scripts/think.py ladder "<task>"` picks the level and its procedure.

| Level | Name | Task shape | Procedure | Artefact that proves it |
|---|---|---|---|---|
| L0 | استرجاع / recall | a fact, a command | answer from catalog or docs, cite, badge | the source line |
| L1 | فهم / understand | explain, summarise | restate in the reader's words, one example, one likely misreading | the explanation + example |
| L2 | تطبيق / apply | run a known procedure | `powers.py suggest` → `requirements.py for <ID>` → run → verify | the output file and its check |
| L3 | تحليل / analyse | diagnose, compare | issue tree or five whys, evidence per branch, rank by evidence | the tree with evidence |
| L4 | تركيب / synthesise | design, plan, combine | backcast, work breakdown with done-tests, thin slice first | plan + first slice |
| L5 | تقييم / evaluate | choose under uncertainty | 3 options + do-nothing, weighted matrix with sensitivity, pre-mortem | `think.py decide` output |
| L6 | إبداع وحكمة / create & judge | original work, strategy, people | diverge→converge, reframe twice, stakeholder and second-order effects, admit unknowns | idea matrix + chosen pitch + risks |

**Rule:** climb one level higher than the task looks when stakes are high or the request is ambiguous; never stay at L0–L2 for anything a user will ship.

<a id="loop"></a>
## 2. حلقة العمل الفائقة / the expert loop

1. **Frame / صغ العقد** — `think.py frame "<task>"`: goal as an outcome, reader, 3–7 observable done-criteria, constraints, non-goals, unknowns split into cheap assumptions vs costly questions, the first 5-minute probe.
2. **Recall / استدعِ** — `powers.py suggest` for powers, `requirements.py plan` for what must be installed, `think.py models` for the 3–5 mental models that fit.
3. **Explore / استكشف** — at least two genuinely different approaches; one safe, one bolder.
4. **Decide / قرّر** — weighted matrix when options are close; one-way doors slow, two-way doors fast.
5. **Build a thin slice / ابنِ شريحة** — end to end, visible early, smallest engine that works.
6. **Verify / تحقّق** — open the artefact itself; numbers computed in code; every explicit ask PASS or declared FAIL.
7. **Reflect / تأمّل** — what would an expert critic say? (`think.py critic draft.md`), what did I learn, what goes into the skill?

<a id="genius"></a>
## 3. عادات العباقرة / genius habits (as procedures)

Genius is not a mood. These are the repeatable behaviours behind outstanding work, written so you can execute them.

| Habit | Procedure | Check |
|---|---|---|
| **Problem finding / اكتشاف المشكلة الحقيقية** | Before solving, write three different statements of the problem (user's words, a root-cause version, an opportunity version). Solve the one with the most leverage. | three statements exist; the chosen one is justified |
| **Reframing / إعادة التأطير** | Ask: what if the constraint is the feature? What if the audience is different? What would make this unnecessary? | at least one reframe changed the plan or was rejected with a reason |
| **Quantity before quality / الكم قبل الكيف** | Generate 10–20 options before judging (`think.py ideas`). | the count, then a shortlist |
| **Distant analogy / التشبيه البعيد** | Find a field that solved the same *structure* (MODEL-32) and port the mechanism. | the borrowed mechanism is named |
| **Combinatorial play / اللعب التركيبي** | Fuse a power from the brief's domain with one from a distant domain (odd rows of `think.py ideas`). | one fused idea in the shortlist |
| **Simplicity after mastery / البساطة بعد الإتقان** | After it works, remove until it breaks; keep the last working version. | what was removed |
| **Taste / الذوق** | Compare against the best reference you can find (style atlas, a proof film); name the gap in specifics (spacing, timing, contrast). | a written gap list |
| **Obsessive verification / التحقق الهوسي** | Measure what matters (fps, LUFS, word sync, test pass) and show the numbers. | numbers in the report |
| **Long-horizon thinking / النفَس الطويل** | Ask what this enables next month; leave the work reusable (scripts, docs, tests). | a reusable piece left behind |
| **Intellectual honesty / الأمانة الفكرية** | State what you did not check and what could be wrong. | an explicit unknowns line |

<a id="ideas"></a>
## 4. تطوير الأفكار / idea development pipeline

Ideas grow in stages; skipping a stage is the usual reason a good seed ends as a generic result.

1. **Seed / البذرة** — the user's sentence, verbatim.
2. **Expand / التوسيع** — `think.py ideas "<seed>" -n 12`: twelve rows, each an operator (invert, fuse, constrain, exaggerate, minimise, swap audience, transplant, personify, time-shift, interactive, data-driven, Arabic-first) × a power. Fill one idea per row.
3. **Cluster / التجميع** — group similar ideas; name each cluster by its mechanism.
4. **Score / التقييم** — novelty × feasibility × fit-to-goal (1–5 each). Feasibility comes from `requirements.py for <ID>`, not from optimism.
5. **Strengthen / التقوية** — take the top 3; for each ask: what is the strongest objection (steelman), what one constraint would make it sharper, what would make it 10× better.
6. **Prototype / النموذج الأولي** — the smallest artefact that shows the idea (a 2-second render, a single frame, a mock page).
7. **Critique / النقد** — red-team it (MODEL-23) and run `think.py critic` on the pitch text.
8. **Pitch / العرض** — one line: who it is for, what it does differently, the proof you will show.

<a id="planning"></a>
## 5. التخطيط / planning

`think.py plan "<goal>" --weeks N` prints the scaffold below; fill every `…`.

- **End state:** artefacts, numbers, who uses them, and the check that proves it.
- **Backcast milestones** (MODEL-25): from the end state backwards to today; each milestone has a done-test. The first milestone is always a thin slice the user sees.
- **Work breakdown** (MODEL-27): deliverables → tasks of a few hours, each with an observable done-test.
- **Critical path** (MODEL-26): which chain decides the finish date; protect it, parallelise the rest (agents, workflows).
- **Requirements gate:** `requirements.py plan "<goal>"` — install what is missing *before* the schedule depends on it; paid or system-wide installs need consent.
- **Pre-mortem** (MODEL-24) with an early-warning signal per risk.
- **Kill / pivot criteria** (MODEL-50): a signal and a date, agreed before starting.
- **Next 10 minutes:** a concrete first action. Plans without a first action are wishes.

<a id="deciding"></a>
## 6. القرار تحت عدم اليقين / deciding under uncertainty

- Classify the door: reversible → decide with ~70% information; irreversible → slow down and get consent (MODEL-12).
- Generate three real options plus do-nothing.
- Weighted matrix in code: `think.py decide decision.json` returns totals, winner, margin and every ±1 weight change that flips the winner. **If it flips, the decision is really about the weights: ask the user or gather evidence.**
- Quantities you cannot look up: `think.py fermi "a*b*c" --range a=lo:hi …` gives p10/p50/p90; report the range.
- Expected value with a ruin check (MODEL-11); base rates before specifics (MODEL-09); update with evidence (MODEL-08).

<a id="human"></a>
## 7. التفكير الشبيه بالبشر / human-like reasoning and communication

What makes reasoning feel human and expert rather than mechanical:

- **Theory of mind (MODEL-38):** model the reader — what they know, want, fear, and what they will do next with your answer. Write for that person.
- **Concrete before abstract (MODEL-60):** every abstract claim gets one concrete example from the user's own material.
- **Commitment with calibrated doubt (MODEL-42):** give a recommendation, then the one thing that would change it.
- **Admit the edges:** say what you could not open, run or verify. Humans trust experts who know their limits.
- **One register, the user's language:** Arabic answers stay Arabic, with technical names in Latin only where needed (ARL rules); keep the dialect the user chose.
- **Plain words:** no intensifiers, no AI-tell vocabulary (`think.py critic`), numbers instead of adjectives.
- **Empathy without flattery:** acknowledge the goal, then do the work; disagree with a reason when needed.

<a id="meta"></a>
## 8. المراقبة الذاتية / metacognition

Run this check at every phase boundary and whenever two attempts fail:

1. Am I solving the problem the user asked, or one I find easier?
2. Which assumption, if false, breaks my plan? Have I tested it?
3. Am I looping (same fix twice)? → stop, write what I know and do not know, change approach (THINK-32).
4. Is my confidence higher than my evidence? (calibration)
5. What would the best expert in this field do differently right now?
6. Is there a power or tool I have not recalled? (`powers.py suggest` again with new words)

<a id="models"></a>
## 9. النماذج الذهنية / mental models

63 models across reasoning, probability, systems, planning, decision, creativity, strategy, economics, communication, learning, epistemics and biases. Each has triggers, a core question, steps, the expected output and the pitfall. `think.py models "<problem>" -n 5` ranks them for the problem (Arabic and English triggers, Arabic prefix stripping). Full list: [mental-models](powers/mental-models.md).

<a id="commands"></a>
## 10. الأوامر / commands

```bash
python3 $SKILL_DIR/scripts/think.py ladder "<task>"          # which level of thinking, which procedure
python3 $SKILL_DIR/scripts/think.py frame  "<task>"          # the contract
python3 $SKILL_DIR/scripts/think.py models "<problem>" -n 5  # mental models to apply
python3 $SKILL_DIR/scripts/think.py plan   "<goal>" --weeks 4
python3 $SKILL_DIR/scripts/think.py ideas  "<seed>" -n 12 --seed 7
python3 $SKILL_DIR/scripts/think.py decide decision.json     # {"criteria":{"quality":3,"cost":-2},"scores":{"A":{"quality":4,"cost":2}}}
python3 $SKILL_DIR/scripts/think.py fermi  "views*ctr*price" --range views=2e4:8e4 ctr=0.01:0.04 price=5:15
python3 $SKILL_DIR/scripts/think.py critic draft.md
```

The scripts produce scaffolds and numbers; the thinking that fills them is yours, and its result must still be verified on the real artefact.
