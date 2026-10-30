# A20 — Book-distilled methods: lateral thinking, pragmatic engineering, Bayesian evidence, personality, accounting controls, prompt clarity, Arabic verse, conceptual thinking, cinematography, code construction and classical logic

> **متى تقرأه / when to read:** طلب يحتاج توليد أفكار غير تقليدية، أو انضباطًا هندسيًا في كود أو أداة، أو قرارًا بأدلة ناقصة، أو بناء شخصية أو نبرة أو حوار، أو قيودًا محاسبية أو IFRS/ISA، أو فحص وضوح برومبت صورة/فيديو، أو فيلم قصيدة/دعاء عربي، أو درسًا تعليميًا، أو تحليل مفهوم وتركيب أفكار ومفاضلة بشبكة، أو قرارات تصوير (غالق، عمق بؤري، ليل نهاري، مسار لون)، أو تعريفًا وتصنيفًا دقيقًا. Any request that needs lateral ideas, engineering discipline, Bayesian weighing of evidence, character/tone design, accounting entries or standards, prompt clarity scoring, Arabic verse on screen, a lesson design, concept analysis and grid decisions, camera and colour decisions, or a precise definition or taxonomy.
>
> **Canonical routing:** [PROTOCOL.md](../../PROTOCOL.md) → this appendix → `scripts/book_methods.py` and `data/book_methods.json`.

## الفهرس / contents

1. [Provenance and boundary](#provenance-and-boundary)
2. [What each file contributed](#what-each-file-contributed)
3. [Where the methods plug into USIP](#where-the-methods-plug-into-usip)
4. [KOSIF v8 reconciled with v5.3](#kosif-v8-reconciled-with-v53)
5. [Commands](#commands)
6. [Gates](#gates)

## Provenance and boundary

The owner uploaded ten PDFs on 2026-10-23 and five more on 2026-10-30 (with skills and protocol files, handled elsewhere). Each was opened and identified: the short ones read in full (the accounting report and the v8 spec, the latter as rendered pages because its text layer is broken), the long ones through their contents pages and the chapters that carry the methods. [`data/book_methods.json`](../../data/book_methods.json) holds **62 methods in 12 domains**, written in our own words, each with steps, a check and the KOSIF stage it plugs into. No book text, exercise, answer, prompt or dialogue is stored. Methods and ideas are attributed to their authors. Reading a contents page and a few chapters is not reading 900 pages, so we never claim the whole book was studied. Two of the 2026-10-30 files are scans with no text layer and no OCR on the machine that read them (Code Complete, Ibn Sina): they were identified from their rendered pages and metadata, and their cards restate the books' well-known methods, marked `identified`, not `used`.

## What each file contributed

| file | what it really is | status | contribution |
|---|---|---|---|
| Lateral-Thinking-Course (100 pp) | a lateral-thinking course teaching REST, the Random External Stimulus Technique (2014) | used | LT-01…06: two stages (ideas first, judgement later), seeded random words, four ways to mine a word, provocation, challenging habits with "why", defining the problem. Runnable: `rest` |
| the-pragmatic-programmer (352 pp) | Hunt & Thomas, *The Pragmatic Programmer*, 1st ed. (1999): 46 sections, 70 tips | used | PP-01…10: DRY, orthogonality and reversibility, tracer bullets vs prototypes, estimating, debugging, contracts and crash-early, no coincidence, digging for requirements, automation and ruthless testing, broken windows |
| Testbank-Probability-Theory (258 pp) | **not the book**: a reseller's sales teaser (one product card, then the same "get it from the shop" line on every page) | teaser only | nothing taken from the file and its links not followed. BY-01…04 come from Jaynes's published framework (*Probability Theory: The Logic of Science*, 2003) as generally known: probability as extended logic, evidence in decibels, keeping rival explanations, maximum entropy. Runnable: `bayes` |
| Cambridge Handbook of Personality Psychology (906 pp) | Corr & Matthews (eds., 2009), 8 parts, 46 chapters | used | PS-01…07: Five-Factor profile, if-then signatures (CAPS), narrative identity, approach/avoidance (RST), self-determination needs, trait adjectives and attachment styles for dialogue, and a guard on culture and ethics. Runnable: `persona` |
| AI_Powered_Accounting_Skill report (16 pp) | an applied research report (v1.0, 13 Sep 2026) on an AI accounting skill | used | AC-01…08: setup package, batch manifest and "finished" as a control, three-layer routing (the model never posts), new-party questions, one event many documents, integer halala, a standards map (IFRS 15/9/16/18, IAS 2/7/8/12/16/36, ISA 315/500/530, COSO), release gates and Saudi PDPL/ZATCA controls. Runnable: `ledger` |
| KOSIF_SKILL_v8_ENHANCED (12 pp) | the owner's own cinematic-director spec v8.0 (2026-09-12) | used, reconciled | KV-01…04: runtime router, clarity/context/specificity filters with HARD/MEDIUM/SOFT locks, project card plus three preflight blocks and 6Q, a timed emotional arc and platform tone. Runnable: `clarity` |
| 41.pdf (921 pp) | Ahmed Shawqi, *Al-Shawqiyyat* (Hindawi edition, 2012); the poet died in 1932 | used | AR-01…03: putting classical verse on screen (whole hemistichs, rhyme letter), the occasion poem and the verse fable as formats, and the Arabic PDF extraction hazard found in this very file |
| Safari 3 (108 pp) | *Impact* Student's Book 1, Bahrain Edition (National Geographic Learning, 2021) | used | ED-01: can-do outcomes first, a photo hook, one task per outcome |
| Safari 4 (8 pp) | Unit 1 "Entertainment" of a National Geographic Learning English coursebook | used | ED-02: notice, check, practise, personalise, with partner swaps |
| Smart-Thinking (329 pp) | Bryan Greetham, *Smart Thinking*: three stages (conceptual thinking, creative thinking, making decisions), 17 chapters | used | ST-01…06: create a concept from examples, analyse a vague word in three steps, four kinds of synthesis, trigger questions × perspectives × levels, four ways to adapt a stuck structure, grid analysis with paired comparisons and frequencies for risk |
| American-Cinematographer-Manual-10 (1445 pp) | ASC, *American Cinematographer Manual*, 10th ed. | used | AM-01…05: the look serves the story inside the budget, 180° shutter and safe pans, hyperfocal distance by formula, day-for-night, a reversible per-shot colour decision in one managed colour space |
| Code-Complete (966 pp) | McConnell, *Code Complete* 2nd ed., Chinese translation, scanned with no text layer | identified | CC-01…04 from the book's well-known practices: prerequisites before construction, pseudocode first, defensive programming at the trust boundary, reviews plus measuring before tuning |
| Al-Shifa, Logic 1, al-Madkhal (714 pp) | Ibn Sina, *al-Shifa'*, Logic part 1 (the Isagoge), scanned | identified | IS-01/02: the five universals (genus, species, differentia, property, common accident) and definition by nearest genus plus differentia, used for catalogue levels and skill descriptions |
| 23.pdf (303 pp) | Diwan of Mahmoud Sami al-Baroudi (Hindawi edition) | used | confirms AR-01…03; no new method |
| Safari 2 (390 pp) | an unlicensed Arabic fan translation of the play *Harry Potter and the Cursed Child* | **excluded** | nothing used. DR-01 records only generic stage-script layout, which needs no source |

## Where the methods plug into USIP

| USIP step | methods to apply | why |
|---|---|---|
| request card | LT-06, PP-08 | one-sentence problem, real vs assumed constraints |
| questions with defaults | AC-04, KV-01 | ask one specific question; the level decides how many |
| plans A/B/C | PP-03 (A = tracer path), PP-02 (seams for C), LT-01/02 (diverge before choosing) | plans are compared only after the idea list is closed |
| SEE lenses / council | BY-03 (keep a rival explanation), LT-05 (why-chain), PS-07 (ethics) | disconfirming objection with numbers |
| decisions with numbers | BY-01/02, PP-04, AC-06 | prior, likelihoods and a dB ledger; ranges; integer money |
| story and prompts (A17) | PS-01…06, KV-02…04, AR-01/02 | a fixed trait profile is a HARD LOCK; the prompt passes ≥8/8/7 before any generation |
| code and tools | PP-01, PP-05…07, PP-09/10 | a bug found once becomes a test; builders keep one source |
| finance (kosif-finance-data) | AC-01…08 | the model proposes, deterministic code validates, a human approves |
| teaching and explainers (A14/A15/A18) | ED-01/02 | outcomes first, discovery before the rule |
| request card for vague words | ST-02, IS-02 | a loaded word becomes 2-4 checkable features; a term is defined by kind plus difference |
| synthesis and plan C | ST-03, ST-05 | name the synthesis kind; plan C changes the structure, not just adds to it |
| choosing between plans | ST-06 | written grid, stated weights, base rates as frequencies |
| film, motion and video prompts (A8, Kling) | AM-01…05 | look sheet first; fps, shutter, lens, stop and colour stated, not implied |
| catalogue and skill descriptions | IS-01/02 | families as genus, powers as species, the deciding feature as differentia |
| tools and scripts | CC-01…04 | pseudocode first, validate at the edge, measure before tuning |

## KOSIF v8 reconciled with v5.3

| v8 rule | v5.3 today | decision |
|---|---|---|
| five runtime modes (FULL_WORKFLOW, SINGLE_IMAGE, SCOPED_ASSET, CONTINUE, AUDIT) | levels L0–L3 and narrow follow-ups | kept as a mapping (KV-01); the level rule in the core wins |
| three opening questions (idea + emotion, duration + audience, tool + style) | A17 question packs: 5 at L1, 10 at L2/L3, inside the one report with suggested answers | A17 wins; v8's three are the first three of the pack |
| "generate the images" after the preflight packet | no spending or generation without explicit approval; prompts are delivered as code blocks | v5.3 wins: v8's step 4 becomes "deliver the prompts" |
| clarity, context, specificity filters; hollow-word ban; HARD/MEDIUM/SOFT locks; commit when ≥8/≥8/≥7 | not machine-checked before | adopted, now runnable as `book_methods.py clarity` (exit 3 = REVISE) |
| project card, three blocks, 6Q, emotional arc, platform tone, negative prompts | A17 story charter and `prompt_pack.py` | adopted as KV-03/04 and cross-linked |
| roadmap v8.1 (prompt chains, multimodal, style DNA, ethics checklist, metrics) | FusionForge recipes, A15 style atlas, A6 guards, shadow evals | already covered; no new claim |

## Commands

```bash
python3 scripts/book_methods.py sources                     # every source file and its status
python3 scripts/book_methods.py search "شخصية حوار"         # Arabic/English search
python3 scripts/book_methods.py show PP-05
python3 scripts/book_methods.py rest --problem "إعلان لمقهى" --words 3 --seed 7
python3 scripts/book_methods.py bayes --h fraud=0.01 --h ok=0.99 --e "flag:fraud=0.9,ok=0.05"
python3 scripts/book_methods.py clarity "صورة لامرأة في مطبخ قديم صباحًا، ضوء من اليسار، حنين، اقتراب بطيء لتأسيس الوحدة"
python3 scripts/book_methods.py ledger --file entries.json --revenue 4101 --receivable 1201
python3 scripts/book_methods.py persona --name سارة --big5 O=4,C=2,E=5,A=2,N=3
```

`ledger` reads JSON entries `{id, source: invoice|bank, party, event_key, vat: {net, tax, rate}, lines: [{account, debit|credit}]}`. Amounts must be strings or integers (a float is refused). Exit 1 means an error was found: an unbalanced entry, a VAT mismatch, a duplicate event key, or a bank receipt credited to revenue when it matches an invoice.

## Gates

- A method card is guidance, not execution: `book_methods.py` scores, checks and drafts. It generates no image, posts no entry and diagnoses no one.
- `clarity` is a word-list heuristic, so a human read decides. Use it as a gate before paid generation, never as proof of quality.
- `ledger` is a draft check. Posting needs authorised approval, privilege and an idempotency key (AC-03). Check standards and effective dates live on ifrs.org before relying on them.
- `persona` is for fiction, tone and design only. Never score, profile or diagnose a real person (PS-07).
- `bayes` refuses a zero prior, because ruling a hypothesis out completely is a claim the evidence cannot undo.
- Quote Arabic from a PDF only after checking it against the rendered page (AR-03).
- Never claim the scanned books (Code Complete, Ibn Sina) were read; their cards are marked `identified`.
- Never claim the uploaded books were read in full, that the testbank held content, or that anything from the excluded fan translation was used.
