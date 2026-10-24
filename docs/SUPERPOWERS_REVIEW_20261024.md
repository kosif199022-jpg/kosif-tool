# KOSIF Superpowers — full review and intelligence upgrade (2026-10-24)

## 1. What exists today (measured on this checkout)

| Layer | What it is | Numbers |
|---|---|---|
| Skills | `kosif-superpowers` (main), `kosif-infinite-matrices`, `editorial-film-edit` | 3 skills |
| Catalog | power cards with evidence and status badges | 5,848 powers · 62 families · 15 task groups · 10 domains |
| Evidence | proven ✅ 1,013 · ready 🟢 674 · needs install 📦 980 · needs key 🔑 176 | 369 ✅ records have no proof file in this repo |
| Runnable tools | `data/tools.json`, front door `hub.py find` | 169 tools in 12 areas · 151 ready on a plain cloud box · 136 tested here, 15 tested elsewhere, 18 untested |
| Protocol | USIP v5.6: level → request card → 100% catalog scan → plans A/B/C → user's word | PROTOCOL.md 112 KB + 33 appendices |
| Thinking stack | `skill_intelligence.py` (brief), `think.py`, `council.py`, `decision_math.py`, `fusionforge.py` (recipes and lessons), SEE Pro gate | — |
| Tests | repo tests, skill evals, routing evals | 290 repo tests · 1,221 skill eval tests · 109/109 routing evals · 11 Node tests — all green |

Tool areas: discover 26 · motion 21 · sources 18 · think 17 · draw 17 · edit 15 · investigate 14 · maintain 13 · 3d 11 · image 11 · audio 5 · local computer 1.

The catalog is heavily weighted to motion (3,833 of 5,848 powers). Strategy (126), research (37) and media (71) are thin.

## 2. How the "intelligence" works, and where it broke

Everything starts with the request card in `skill_intelligence.py analyse()`: it decides the level (L0–L3) and the primary deliverable (video, code, data, document…). The deliverable then decides which catalog groups are "home", which are penalised, which plan archetypes (A/B/C) are used and which verifiers may judge the result. If the card is wrong, every plan after it is wrong.

The existing evals (109 routing cases, 98 routing-quality cases) all passed, but they were written against the cases the engine was tuned on. A fresh set of everyday requests showed the gaps:

| Request | Before | Problem |
|---|---|---|
| «صلح البج اللي بيخلي صفحة تسجيل الدخول تقع على الموبايل» | L0, text | A bug fix read as a one-line question; plans picked phone-editor video transitions |
| "should I raise prices by 10% given churn of 5%?" | unspecified | Plan A had spring easing, stagger budgets and a paper texture |
| «اعمل خطة تسويق…» / «دراسة جدوى…» / business plan | unspecified | No business/decision deliverable existed at all |
| «ترجم العقد ده… وراجع البنود الخطيرة» | L0, text | A contract review treated as a quick translation |
| «حلل ملف المبيعات sales.xlsx…» | unspecified | `.xlsx`, sales and profit were not data signals |
| "fix the memory leak in my Node.js server", "Debug why my React form submits twice" | unspecified | Bug and debug work was not code unless the word "code" appeared |

## 3. What changed (this PR)

1. **New `strategy` deliverable** for business decisions and plans (marketing, pricing, feasibility, competitors, business plans, "should I…", starting a shop): home group *thinking*, its own A/B/C archetypes (decision frame → scenarios and sensitivity → editable financial model and a small experiment), verifiers from strategy/finance and data families, and off-domain penalties for motion, 3D, audio and drawing.
2. **Catalog vote when nothing is named**: when the request names no deliverable, the top 40 matching powers vote by group (media groups excluded) and the brief takes the leader only when it leads by 25% or more; otherwise it stays `unspecified`. The vote is kept in `analysis.primary_votes` and `primary_inferred` so the report can say why.
3. **Richer signals**: bugs, crashes, debug, login, frameworks and Python as code; `.xlsx`, sales, revenue, profit and forecasts as data; contracts and clauses as documents; Egyptian/Arabic business, data-cleaning and bug words as search aliases.
4. **Compound requests are work, not L0**: a short intent followed by a second job («ترجم… وراجع…», "translate and flag…") is no longer a one-line answer. "What's the best time to post" stays a question.
5. **Council roster for strategy**: a strategy council seats a strategist, a devil's advocate against the plan, a CFO, the target customer and an assumptions-and-numbers checker.
6. **New gate**: `evals/routing_generalization.json` (50 fresh requests in 3 batches), `evals/routing_generalization.py` (scorer) and `evals/test_routing_generalization.py`, now a named CI step (the catch-all eval step runs it too).

## 4. Measured result

| Set | Request card correct (before → after) | Off-domain picks in the recommended plan (before → after) |
|---|---|---|
| All 50 fresh requests | 26/50 → 46/50 | 46/337 (14%) → 2/312 (<1%) |
| Batch 3 only (written after the changes, measured once, never tuned) | 8/14 → 10/14 | 11/95 → 1/89 |

The existing gates still pass: 98/98 routing-quality cases, 109/109 routing evals, the council tests and the full eval suite.

Remaining misses in batch 3, left in on purpose so the gate stays honest: "Which KPIs should a SaaS startup track" (reads as code because of "SaaS"), «حلل استبيان العملاء» (reads as strategy, should be data), "Should we hire a designer or freelancers" (reads as image because of "designer"), «احسب نقطة التعادل» (no clear vote).

## 5. Gaps and next steps, by value

1. **Word matching is the ceiling.** The card is regex plus tf-idf. Each fix above is a rule, and batch 3 shows rules generalise only partly (71%). Next: an optional semantic fallback (for example Model2Vec, MIT, numpy only) used only when the rules and the catalog vote abstain, measured on new untouched batches.
2. **Lessons do not learn from outcomes.** FusionForge records lessons, but nothing scores which lessons helped. Next: helpful/harmful counters per lesson, de-duplication and pruning (the ACE pattern), with `reuse` ranking by those counters.
3. **No grader for real sessions.** All evals check routing, not whether the final work was good. Next: a small model-graded suite on recorded sessions: right tool picked, A/B/C really different, uncertainty stated when it should be.
4. **Evidence debt.** 369 ✅ records point to receipts outside this repo, and 18 tools are marked untested (four of them, the atlas scripts, already have passing tests in CI under `scripts/` and can be relabelled `tested-here`).
5. **Thin domains.** Strategy, research and media have few powers compared with motion. The new strategy deliverable routes well, but it can only pick from 126 strategy powers and 17 thinking tools.
6. **Size of the instructions.** PROTOCOL.md is 112 KB and SKILL.md 80 KB. A lot of reading happens before small jobs. The L0/L1 fast path matters more as the files grow.
