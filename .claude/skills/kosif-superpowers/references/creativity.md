# الإبداع — Creativity engine (IDEA)

> **What this gives you:** a diverge-then-converge protocol, 16 creativity operators (each with a how-to, a general example and a motion/design example), taste guards, and power combos that join families from different domains into one deliverable. **Open it** for any creative, design, naming, campaign or "make it better / different" request, and after the safe plan exists when you want one bolder option.
> Records: `python3 scripts/powers.py family creativity-engine` (IDEA-01…IDEA-25). The thinking loop is in [thinking.md](thinking.md); judging and checking in [verification.md](verification.md).

## المحتويات — Contents
1. [التباعد ثم التقارب — Diverge → converge](#1-التباعد-ثم-التقارب--diverge--converge)
2. [المشغلات الستة عشر — The 16 operators](#2-المشغلات-الستة-عشر--the-16-operators)
3. [الاتجاهات والذوق — Directions and taste](#3-الاتجاهات-والذوق--directions-and-taste)
4. [توليفات القوى — Power combos](#4-توليفات-القوى--power-combos)
5. [مثال كامل — Worked example](#5-مثال-كامل--worked-example)
6. [المصادر — Sources and licences](#6-المصادر--sources-and-licences)

---

## 1. التباعد ثم التقارب — Diverge → converge

IDEA-01. Two separate phases; never judge while generating.

1. **Diverge.** Pick 3–5 operators that suit the task (table below). Aim for 8–20 raw ideas, one line each. Quantity first; weird is welcome.
2. **Merge.** Collapse near-duplicates; turn pure rules (e.g. "text ≥6% of frame height") into constraints for every idea instead of counting them as ideas.
3. **Converge.** Score 1–5 on: fit to the done-criteria · feasibility with ✅/🟢 powers (check with `python3 scripts/powers.py search …`) · novelty · risk (5 = low). Sum the scores in code if there are many.
4. **Keep a pair.** One safe option and one bold option. When taste matters, show both early (a still, a one-paragraph treatment, or three previews — IDEA-18), then build the chosen one.

These operators give structured diversity. They are heuristics with weak controlled evidence for language models specifically; their value is that they force genuinely different directions instead of the first idea.

---

## 2. المشغلات الستة عشر — The 16 operators

| ID | Operator | How (one line) | General example | Motion / design example |
|---|---|---|---|---|
| IDEA-02 | **First principles** | Ask "what is this for?" three times; design from true constraints, not habits. | "Faster weekly report": the goal is a decision → a one-number alert when the metric crosses a threshold. | "Intro animation": the goal is two seconds of attention → one bold kinetic word on frame 1 beats a six-second logo sting. |
| IDEA-03 | **Inversion** | List 5–10 ways to guarantee failure; turn each into a rule. | Onboarding fails if a password comes first → magic-link sign-in. | A reel fails if text is unreadable on a phone → type ≥ ~6% of frame height, safe zone, check at 360 px wide. |
| IDEA-04 | **Pre-mortem** | "It failed — why?" ×3; one mitigation per reason. | Migration failed on time zones → write the tz test first. | Render failed on audio drift → lock fps, ffprobe duration and audio length before the final render. |
| IDEA-05 | **Fermi estimate** | Multiply guessable factors; sanity-check the order of magnitude (compute in code). | 10k users × 5 calls × 2k tokens ≈ 100M tokens/month → caching matters. | 60 s × 30 fps = 1,800 frames × 0.3 s ≈ 9 min render → preview at half scale first. |
| IDEA-06 | **SCAMPER** | Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse — one variant each. | CLI tool: combine with chat, eliminate the config file, reverse into push notifications. | Captions: substitute words with icons, reverse so text exits before it enters, eliminate the box. |
| IDEA-07 | **Morphological matrix** | Dimensions × options table; sample odd rows. | Pricing {seat, usage, flat} × {monthly, annual} × {free tier y/n}. | {serif, kufi, mono} × {spring, glitch, draw-on} × {duotone, neon, paper} → kufi + draw-on + paper. |
| IDEA-08 | **Analogy transfer** | Abstract the structure; find 3 distant domains; borrow one mechanism. | Code-review queue run like hospital triage (severity, then age). | Transitions borrowed from origami folds or a split-flap departure board. |
| IDEA-09 | **Constraint injection** | Add one hard artificial limit. | Explain the feature in seven words, or without screenshots. | Two colours and one font weight for the whole film; every cut on a beat. |
| IDEA-10 | **Constraint removal** | "If this were free or infinite?" → find a cheap approximation. | Unlimited support staff → an FAQ triage bot for the top 20 questions. | Infinite budget = live action → 3D scene + depth of field + film grain. |
| IDEA-11 | **Exaggerate / minimise** | Push one parameter to 10× or 0.1×. | A report at 10× frequency becomes a live dashboard. | A word at 10× scale fills the frame; the camera flies through its letters. |
| IDEA-12 | **Perspective swap** | Re-describe the task as 2–3 personas. | Explain the outage as the angriest customer would, then answer that. | Storyboard from the viewer's thumb: what stops the scroll on frame 1? |
| IDEA-13 | **Worst idea first** | Write 5 terrible ideas fast; flip each. | "Hide the price" → "price in the first line". | "Comic Sans everywhere" → a playful hand-drawn Arabic face used with intent. |
| IDEA-14 | **Random stimulus** | Draw 3 random catalog powers (snippet below); force a link. | Random word "tide" → a feature flag that rolls out and back. | A random particle power applied to a chart reveal: bars assemble from drifting particles. |
| IDEA-15 | **Ensemble and judge** | 3 deliberate variants; judge one criterion at a time; merge the best parts. | Three email drafts, judged for clarity and tone; merge the best opening and close. | Three style frames as stills, judged on readability, brand, wow; build the winner. |
| IDEA-16 | **Remix the masters** | Two references, one mechanism from each; describe by visible properties; never copy assets. | Payment-docs clarity + language-app streaks → learning docs with streaks. | Swiss grid + Arabic calligraphic stroke reveal (study `styles-atlas.md` first). |
| IDEA-17 | **Capability cross-over** | Pick a family from another domain the user did not ask for; write one idea with it. | A CSV summary gains a published interactive dashboard with numbers locked in code. | A talking-head edit gains kinetic Arabic captions on word timing and a live data counter. |

Random stimulus snippet (run from the skill directory; add `random.seed(7)` to make it reproducible):
```bash
python3 -c "import json,glob,random; P=[r for f in glob.glob('data/powers/*.json') for r in json.load(open(f,encoding='utf-8'))]; [print(r['id'], r['name_en']) for r in random.sample(P,3)]"
```
The motion catalog also has a seeded lateral-ideation power (STORY-78) and critique lenses (STORY-44).

**Which operators for which job.** Stuck on the obvious → first principles, worst idea first, random stimulus. Risky delivery → inversion, pre-mortem, Fermi. Bland look → constraint injection, exaggerate, remix, anti-cliché sweep. Unclear audience → perspective swap. Need breadth → morphological matrix, SCAMPER. Need quality → ensemble and judge. Need surprise → capability cross-over.

---

## 3. الاتجاهات والذوق — Directions and taste

**Show, don't ask (IDEA-18).** Instead of a taste questionnaire, make three small previews that differ on a real axis (type, palette or motion grammar), each one still or one slide, name each in two words, and ask one question: "which direction?". For motion, render one still per direction through the scene's `seek(t)` and put them on a contact sheet (QA-58).

**Anti-cliché sweep (IDEA-19).** Before showing a draft, flag worn defaults and replace each with an intended choice:

| Default to flag | Ask instead |
|---|---|
| gradients everywhere, purple → blue | what single palette says this brand? |
| decorative blobs, glassmorphism with no purpose | what does this layer communicate? |
| cards inside cards, over-rounded everything | what is the one hierarchy? |
| centred hero over a stock gradient, vague hero copy | what is the one sentence and the one memorable detail? |
| scroll or fade animation on everything | which motion explains a change of state? |
| personality-less sans stack | which typeface carries the tone (and covers Arabic)? |
| random easing; text split into letters | one easing family; whole words — never split Arabic into letters |

Write the intent first — purpose, audience, three tone words, one memorable detail — then change the flagged defaults.

**Safe + bold.** Always carry one of each to the user when taste is open. The bold one usually comes from exaggerate, analogy or capability cross-over (THINK-16).

---

## 4. توليفات القوى — Power combos

A combo joins families from different domains so one request produces a richer deliverable. Prefixes refer to families in this catalog: data-analysis ANLY, writing-humanizer WRITE, knowledge-graph GRAPH, web-research WEB, documents-office DOC, apps-artifacts APP, media-image-audio MEDIA, strategy-finance PROD, prompt-craft PROMPT, arabic-language ARL, plus motion families (DATA, STORY, SYNC, VOICE, ARAB, EXPL, DRAW, UI, GEN, BEAT, FOOT). Browse any of them with `python3 scripts/powers.py family <name>`.

| Combo | Recipe (short) | Check that proves it | Record |
|---|---|---|---|
| **ANLY + motion data story** | CSV → 3 facts computed and frozen in code → chart by question (DATA-01) → 3–5 beats (STORY-32) → springs, odometer counter, Arabic-Indic digits | numbers on the frames = numbers in code; ffprobe | IDEA-20 |
| **WRITE + VOICE + SYNC** | script → humanize with numbers/names locked (before alignment) → TTS → `words.json` → whole Arabic words enter on their start time | max word offset ≤1 frame; −14 LUFS | IDEA-21 |
| **GRAPH + animated mind map** | graph from a repo or notes (keep parsed vs inferred) → centre + 2 rings → edges draw on in BFS order; parsed solid, inferred dashed → HTML + MP4 | node count on screen = graph | IDEA-22 |
| **WEB + DOC** | 3–5 sub-questions → parallel search → claim ledger → cited doc or deck + one computed chart | every number traces to a ledger row; links open | IDEA-23 |
| **APP + MEDIA** | interactive page with code-drawn or generated visuals → scripted Playwright walkthrough → captioned reel | works at 390/1440 px; reel passes ffprobe | IDEA-24 |
| **PROD + ANLY** | options incl. do-nothing → Fermi model in python → inputs ±30% → tornado chart → decision memo with flip thresholds | break-even per assumption computed | IDEA-25 |
| ARL + ARAB | correct and lightly diacritise an Arabic verse → animate whole words on its rhythm with a face that covers Arabic | joined letters on a frame grab; right-to-left order | — |
| PROMPT + GEN | one master visual spec with identity/product locks → per-platform prompts → variants that change one dimension each (paid generation 🔑, confirm first) | lock held across variants | — |
| DOC + DATA | PDF report → tables extracted in code → frozen figures → 30 s summary reel | figures match the PDF tables | — |
| MEDIA + BEAT | photo set → detected beats → cuts on beats with slow push-ins | cut times vs beat times measured on the MP4 | — |

Combos are 📄 recipes: each part may be proven, but the joined pipeline has not been run end to end unless a record says so (IDEA-20 and IDEA-21 cite proofs for their motion half: `proofs/data-story`, `proofs/arabic-voice-kinetic`).

---

## 5. مثال كامل — Worked example

**Brief:** «ريل ٢٠ ثانية لإطلاق تطبيق ميزانية اسمه "دفتر"» — a 20 s 9:16 launch reel for a budgeting app called *Daftar* (Egyptian audience).

**Diverge** (5 operators → 12 raw ideas):
1. *First principles* — the goal is one feeling, "I know where my money went": a receipt prints itself and sorts into categories.
2. *First principles* — open on the outcome: the month's spending bar shrinking to target.
3. *Inversion* — fails if it looks like every fintech ad → paper-and-ink look, hand-drawn Arabic-Indic numerals.
4. *Inversion* — fails if numbers are unreadable on a phone → at most 3 numbers on screen, large (merged as a constraint for all ideas).
5. *Constraint* — two colours, one weight, every cut on a beat.
6. *Constraint* — only real UI: a recorded walkthrough cut to music.
7. *Analogy* — an old paper ledger (a *daftar*) whose pages flip into the app screens.
8. *Analogy* — the budget as a leaking water tank, categories as taps.
9. *Cross-over ANLY* — a sample budget computed in code; the counter lands on the exact computed saving.
10. *Cross-over VOICE + SYNC* — an Egyptian voice line «فلوسك راحت فين؟» with words appearing on their timing.
11. *Exaggerate* — the receipt is 10× long and scrolls past the camera like a red carpet.
12. *Worst idea flipped* — "show a spreadsheet for 20 s" → spreadsheet cells fold into the app icon.

**Converge** (fit, feasibility, novelty, risk; 1–5 each; totals computed in code):

| Idea | Fit | Feas. | Nov. | Risk | Total |
|---|---|---|---|---|---|
| 1 receipt sorts itself | 5 | 4 | 4 | 4 | 17 |
| 3 paper-and-ink look | 4 | 5 | 3 | 5 | 17 |
| 7 ledger pages flip into UI | 5 | 4 | 4 | 4 | 17 |
| 10 voice line on word timing | 5 | 5 | 3 | 4 | 17 |
| 2 outcome first | 4 | 5 | 2 | 5 | 16 |
| 11 10× receipt | 4 | 4 | 5 | 3 | 16 |
| 5 two colours, cuts on beats | 3 | 5 | 3 | 4 | 15 |
| 9 computed saving counter | 4 | 4 | 3 | 4 | 15 |
| 12 cells fold into icon | 4 | 3 | 5 | 3 | 15 |
| 6 real UI only | 4 | 4 | 2 | 4 | 14 |
| 8 water tank | 3 | 3 | 3 | 3 | 12 |

**Pair shown to the user:**
- *Safe* = 7 + 3 + 10: paper ledger pages flip into the app screens, ink palette, the Egyptian voice line drives the timing (VOICE + SYNC are ✅ in this catalog).
- *Bold* = 11 + 9: a 10× receipt rushes past the camera and the counter lands on the exact saving computed in code.
Then build the chosen one as a thin slice (one scene rendered and checked) before the rest.

---

## 6. المصادر — Sources and licences

- Classic public methods (ideas are not copyrightable; all wording here is ours): divergent/convergent thinking (J. P. Guilford), Double Diamond (UK Design Council, 2005), SCAMPER (B. Eberle 1971, from A. Osborn), morphological analysis (F. Zwicky), TRIZ ideal result and contradictions, inversion (C. G. J. Jacobi, popularised by C. Munger), pre-mortem (G. Klein, HBR 2007), Fermi estimation, random entry (E. de Bono), reverse brainstorming.
- [affaan-m/ECC](https://github.com/affaan-m/ECC) — MIT © 2026 Affaan Mustafa: "show, don't ask" previews from `skills/frontend-slides`; the defaults-to-flag list from `skills/design-system` and `skills/frontend-design-direction` (community-salvaged); UI recording idea from `skills/ui-demo`. Paraphrased.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — parallel voting and evaluator patterns behind "ensemble and judge" (copyrighted; paraphrased, link only).
- Owner material: KOSIF SEE v1.7.5 product-strategy and finance-data packs (owner; rewritten); this catalog's own proofs `proofs/data-story` and `proofs/arabic-voice-kinetic`.
- Graph confidence labels (parsed / inferred / ambiguous) follow [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) documentation (Apache-2.0 and MIT files present).
- Session-2026-10-16 distillations used: thinking-methods §4, ecc-skills-a 2.13, ecc-skills-b 2.8 and 2.12, see-core §4.

## KOSIF Inventive Engineering Lab
Use `python3 scripts/invention_lab.py invent "precise problem" --count 20 --constraint "hard restriction"` for deterministic technique-by-lens candidates, explicit hypotheses, metrics and rejection criteria. Source atlas: [50 projects in font fidelity and innovation](font-innovation-50.md). The priority score is a sorting heuristic, not a validated novelty or quality finding. Select 2–3 candidates and test against baselines rather than generating hundreds of unsupported claims.
