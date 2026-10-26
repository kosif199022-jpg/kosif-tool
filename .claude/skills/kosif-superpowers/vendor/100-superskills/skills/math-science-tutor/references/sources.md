# مصادر «معلّم الرياضيات والعلوم» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## math-unicode (3259-claude-math)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/vladimirrott/claude-math
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3259-claude-math/13770-math-unicode
- الوصف: Use when a response needs mathematical notation (equations, filters, set-builder notation, statistics, calculus, linear algebra, logic, ratios, drops, counts) and the output goes to a terminal or TUI that cannot render LaTeX: Claude Code, Codex CLI, SSH and tmux sessions, CI logs. Load it before composing, including when the user explicitly mentions math-unicode. Emit Unicode glyphs inline, never 

```markdown
# math-unicode

When emitting mathematical notation in a terminal coding agent (Claude Code, Codex CLI, or similar), **always use Unicode glyphs inline** — never wrap math in `$…$`, `\(...\)`, or `$$...$$`. These terminals do not render LaTeX; raw delimiters appear as plain dollar signs and reduce readability.

## When this skill applies

Two conditions, both required: the response carries mathematical notation, and
the surface it lands on does not render LaTeX.

Surfaces that do not render LaTeX (apply the skill):
- Claude Code, Codex CLI, and other terminal or TUI coding agents
- Anything read through SSH, tmux, a pager, or a CI log

Surfaces that render math natively (do not apply the skill):
- ChatGPT and Codex on desktop and web, where math already renders
- Notebooks, and any target consumed by KaTeX or MathJax

No host exposes a per-surface predicate to a skill today, so this boundary is a
judgement the model makes from its own context. If you cannot tell, and the
session is a terminal coding agent, apply the skill.

Triggers (use Unicode math):
- Equations, formulas, derivations
- Filter conditions, set-builder notation
- Statistics: probabilities, expectations, distributions
- Calculus, linear algebra, logic
- Counts, ratios, fractions, drops where precision matters

Skip (do not transform):
- The user explicitly asks for LaTeX or a `.tex` file
- Math inside fenced code blocks (preserve source syntax)
- Strings being passed to a system that consumes LaTeX (KaTeX MCP, etc.)

## Glyph cheatsheet

### Greek

```
lowercase   α β γ δ ε ζ η θ ι κ λ μ ν ξ ο π ρ σ τ υ φ χ ψ ω
uppercase   Α Β Γ Δ Ε Ζ Η Θ Ι Κ Λ Μ Ν Ξ Ο Π Ρ Σ Τ Υ Φ Χ Ψ Ω
variants    ϵ ϑ ϕ ϖ ϱ ς
```

### Operators

```
arithmetic     + − × ÷ ± ∓ · ∗ ⋅ ∘ ⊕ ⊖ ⊗ ⊘ ⊙
big            ∑ ∏ ∐ ∫ ∬ ∭
roots          √ ∛ ∜
calculus       ∂ ∇ Δ ∆
constants      ∞ ∅
```

### Relations

```
equality       =  ≠  ≈  ≅  ≡  ≜  ≝  ≐  ∝  ∼  ≃  ≢
order          <  >  ≤  ≥  ⊴  ⊵
set            ∈ ∉ ∋ ∌  ⊂ ⊃ ⊆ ⊇ ⊊ ⊋  ⊏ ⊐ ⊑ ⊒
set ops        ∪ ∩ ⊎ ⊔ ⊓        (set difference: A \ B)
```

### Logic & arrows

```
logic          ∧ ∨ ¬ ⊕   ⊢ ⊥ ⊤
quantifiers    ∀ ∃ ∄ ∴ ∵
arrows         → ← ↔ ⇒ ⇐ ⇔ ↦ ↪ ↩ ↑ ↓ ⇑ ⇓ ⟶ ⟵ ⟷ ⊸
```

### Number sets & brackets

```
sets           ℕ ℤ ℚ ℝ ℂ ℙ ℍ
brackets       ⟨ ⟩  ⌈ ⌉  ⌊ ⌋  ‖ ‖
```

### Sub/superscript glyph blocks

```
superscript    ⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹  ⁺ ⁻ ⁼ ⁽ ⁾  ⁱ ⁿ ᵃ ᵇ ᶜ ᵈ ᵉ ᶠ ᵍ ʰ ʲ ᵏ ˡ ᵐ ᵒ ᵖ ʳ ˢ ᵗ ᵘ ᵛ ʷ ˣ ʸ ᶻ
sup (capital)  ᴬ ᴮ ᴰ ᴱ ᴳ ᴴ ᴵ ᴶ ᴷ ᴸ ᴹ ᴺ ᴼ ᴾ ᴿ ᵀ ᵁ ⱽ ᵂ
sup (Greek)    ᶿ                    (θ only; the rest are opt-in)
subscript      ₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉  ₊ ₋ ₌ ₍ ₎  ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ
```

**Do not invent or approximate a missing glyph.** A whitelist on its own is not
a membership test; these are the exact gaps that make the bare `^x` / `_x`
```

## long-form-math (1244-long-form-math)

- الترخيص: **MIT**  ·  الأصل: https://github.com/dashed/claude-marketplace/tree/f6a24dbc08da57aeb80e7423da2508457d0b3398/plugins/long-form-math
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1244-long-form-math/2924-long-form-math
- الوصف: Write mathematics in a long-form, understanding-focused style with detailed proofs and rich exposition. Use when explaining mathematical concepts, writing proofs, tutoring math, creating educational math content, or when the user asks for mathematical explanations. Inspired by Jay Cummings' Real Analysis and Chartrand's Mathematical Proofs. Triggers on proof writing, theorem explanations, mathemat

```markdown
# Long-Form Mathematics

Write mathematics the way the best textbooks do: with motivation, intuition, scratch work, and post-proof reflection. Every proof tells a story. Every definition earns its place.

## When to Use

- Writing or explaining proofs
- Introducing mathematical definitions, theorems, or concepts
- Tutoring someone in mathematics
- Creating educational math content (lecture notes, textbook-style explanations)
- Answering "why" questions about mathematical results
- Working through problem sets with a student

## Core Philosophy

| Principle | Meaning |
|-----------|---------|
| Understanding over economy | A longer explanation that builds understanding beats a terse proof that sacrifices clarity |
| Show the thinking | Make the invisible reasoning process visible -- scratch work, false starts, technique selection |
| Words between symbols | Never present bare equation chains; every step gets connective text explaining WHY |
| Math is communication | Writing quality matters as much as correctness; the reader must be convinced AND enlightened |

## Proof Writing Workflow

Every proof follows three phases. Do not skip phases 1 and 3.

### Phase 1: Pre-Proof Strategy

Before writing the proof, show the reader how the proof was discovered.

**Scratch Work.** Work backward from the desired conclusion. Show the exploratory reasoning that reveals what to prove and how. Label this section explicitly.

> Example: "We want to show |a_n - 0| < e. Unraveling, this means 1/n < e, so n > 1/e. This tells us to pick N = ceil(1/e)."

**Technique Selection.** State which proof technique to use and WHY.

| Try this technique... | When... |
|----------------------|---------|
| Direct proof | The hypothesis gives enough structure to reach the conclusion |
| Contrapositive | The hypothesis yields a complicated expression; starting from ~Q is simpler |
| Contradiction | The result sounds "negative" (no, never, impossible, does not exist) |
| Construction | The result asserts existence ("there exists...") |
| Cases | The domain splits naturally (even/odd, positive/negative/zero) |
| Both directions | The result is biconditional ("if and only if") |

**Proof Idea.** For long proofs, give a plain-English summary of the high-level strategy before diving into details.

> Example: "The idea is to show |a - b| < e for all e > 0, forcing |a - b| = 0."

### Phase 2: The Proof

Write the polished proof following these structural rules:

1. **State assumptions first.** Open with "Assume that..." or "Let... be..."
2. **Type every variable.** When introducing k, say "where k is an integer." Never leave a variable untyped.
```

## collab-proof (163-collab-proof)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/engineering/collab-proof
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/163-collab-proof/532-collab-proof
- الوصف: Use when you want to understand what Claude contributed vs what you drove in a session. Triggers on: /collab-proof, session retrospective, ai contribution analysis, collaboration evidence, what did claude do.

```markdown
# collab-proof

Surfaces AI collaboration evidence the developer didn't consciously record.
Vela 3-layer pipeline × ADHD 4-frame reasoning — prompt-native, zero dependencies.

---

## Layer 01 — Signal detection

Run `git log --oneline -10` and `git diff --stat HEAD~3..HEAD` first.

Classify signal level using this rubric (pick the highest that matches):

**HIGH** → full artifacts (DECISIONS.md + session-history + WORKLOG + HTML)
- New file created, OR
- 4+ files modified, OR
- Explicit option comparison in conversation ("vs", "instead of", "chose X over Y"), OR
- Design discussion lasted 15+ exchanges, OR
- **Bug with root cause diagnosis** — conversation contains WHY the bug happened
  (not just "fixed X" but "the bug was caused by Y because Z")

**BUG_FIXING special rule** — override file count:
Even if only 1 file changed, classify as HIGH if the conversation contains:
- Root cause explanation ("the bug was...", "this happened because...", "the issue is...")
- Diagnosis process ("I checked...", "turned out...", "the problem was...")
- Fix rationale ("chose this approach because...", "instead of X, used Y because...")
File count doesn't matter for bugs — a well-diagnosed single-file fix is more valuable
than a 10-file feature with no discussion.

**MEDIUM** → WORKLOG only
- 1–3 files modified with no root cause discussion, OR
- Minor feature added, no tradeoffs discussed

**LOW** → silence, tell user "Routine session — nothing recorded."
- No code changes, only planning/discussion, OR
- Single trivial change with no context ("change this text", "fix typo", "rename variable")

Show the user: `Signal: HIGH / MEDIUM / LOW — [one-line reason]`

---

## Layer 02 — WorkIntentClassifier

Run all four frames simultaneously against conversation context + git diff.
Score each frame 0.0–1.0 using the rubric below. Then apply pruning and classification rules.

### Frame scoring rubric

**Frame A — Technical** (code churn complexity)
- `1.0` New module/file created, complex logic added (state machine, Lua script, novel algorithm)
- `0.5` Existing function logic modified, simple API endpoint added
- `0.1` Typo fix, comment change, plain text edit

**Frame B — Uncertainty** (developer doubt signals)
- `1.0` Code written then fully rolled back, explicit doubt expressed ("이게 맞나?", "동작 안 하네"), `git revert`
- `0.5` Advice sought from Claude mid-implementation, 2+ revision requests on same area
- `0.0` Uninterrupted directive execution — developer knew exactly what to build

**Frame C — Fork** (decision branch presence)
- `1.0` Two or more alternatives explicitly compared in conversation (A vs B)
- `0.5` No explicit comparison but tradeoff mentioned (performance vs readability)
- `0.0` Single standard approach applied, no alternatives considered
```

## red-green-proof (3014-red-green-proof)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/RooAGI/red-green-proof
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3014-red-green-proof/12878-red-green-proof
- الوصف: Turns a suspected bug into a proven one. Verify the cause against reality before claiming it, write a test that FAILS on the current code, apply the fix, watch it pass — then revert the fix and confirm the test goes red again, because a test that passes both ways proves nothing. Invoked bare after a debugging conversation, it takes the target from context rather than asking. Use when fixing a bug,

```markdown
# Red-Green-Proof

A bug is not fixed because the tests pass. A bug is fixed when a test **fails without your fix and passes with it**, and you have watched it do both.

Most "regression tests" written after a fix never had the chance to fail. They are decoration. This skill is the discipline that separates a real test from a decorative one.

## Picking the target

**With an argument**, that is the target: `/red-green-proof the status endpoint reports finished runs as running`.

**With no argument, take the target from the conversation.** The usual case is that you have just spent a long stretch investigating something — the bug is already on screen. Do not ask what to work on. Scan back through the session and pick, in this order:

1. A defect just identified but not yet fixed.
2. A fix applied without a failing test to back it — the most valuable target, because the test still has to be proven load-bearing.
3. A test written but never verified red.
4. Something described as "still open", "not fixed yet", or "characterization only".

State your pick in one line and start:

> Target: the buffer discards events when the flush write fails (`checkpointBuffer.ts:271`). Verifying before writing the test.

Only ask the user if two or more candidates are genuinely equal in priority — then list them as a short numbered choice and stop. If several *related* defects came up, handle them one at a time through the full loop rather than batching; each needs its own red.

If nothing in the conversation qualifies, say so and ask for a target rather than inventing one.

## The loop

Run these in order. Do not skip 1, and never skip 4.

### 1. Verify the cause. Do not infer it.

Before you write a line of test code, establish what actually happened using evidence you can point at: the real record from the database or API, the real log line, the actual source of the function you are blaming.

Say which of these you have:

- **Proven** — I read the value / ran the code / pulled the record.
- **Inferred** — consistent with the evidence, but I have not confirmed it.
- **Unknown** — I cannot determine this from what is available.

State the label out loud. If the honest answer is Unknown, say so and name the one artifact that would settle it. A confident wrong cause costs more than an admitted gap, because it sends the fix to the wrong place.

Two traps worth naming:
- **A plausible mechanism is not the mechanism.** Rank candidates, then go rule them out one at a time by reading code, not by reasoning about it.
- **Check whether the "bug" was deliberate.** `git log -S '<the exact line>'` and read the commit. If a test already asserts the current behaviour, someone may have wanted it. Understand why before you invert it.

### 2. Write the test. Watch it fail.
```

## balance-sheet-explain (3555-xbert-balance-sheet-explain)

- الترخيص: **MIT**  ·  الأصل: https://github.com/xbertintelligence/xbert-plugins/tree/7e6bcc16a3fd1da830522d1d30f97a76c52b67aa/plugins/xbert-balance-sheet-explain
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3555-xbert-balance-sheet-explain/14367-balance-sheet-explain
- الوصف: Walk a client's balance sheet opening-to-closing with movement narrative, reconciliation status per account, manual journal trace, and fixed-asset-register-to-GL accumulated depreciation check. Use when the user asks to review the balance sheet, explain BS movements, prep for year-end or audit, walk the BS, or runs the /balance-sheet-explain slash command. Also triggers on "what moved on the balan

```markdown
**Source of truth — XBert MCP:** Every figure, client record, ledger transaction, payrun, and XBert notification referenced here must come from the connected XBert MCP server. Call XBert MCP tools to fetch the data — do not invent figures, estimate from context, or substitute from chat history. If the XBert MCP is not connected, ask the user to install and authenticate it before continuing.

# Balance Sheet Explain

## Goal
Walk every line of the balance sheet from opening to closing, state the reconciliation status of every reconcilable account, trace every material manual journal, and check that the fixed asset register accumulated depreciation agrees with the GL. Produce a Word narrative review.

## Metrics
- **Movement coverage** — % of material movements with a named journal or reconciliation behind them
- **Reconciliation completeness** — count of reconcilable accounts (Cash, AR, AP, FAR) with stated rec status
- **FAR-GL agreement** — absolute variance between FAR accumulated depreciation and GL accumulated depreciation account

## Default thresholds (practice-configurable)
| Threshold | Value | Used in |
|---|---|---|
| Material movement (per account) | $1,000 or 5% of opening — whichever is greater | Section 1, Section 4 |
| Unexplained-mover flag | Material movement with no source journal | Section 4 |
| FAR-GL variance tolerance | $1 | Section 2 |
| Manual journal materiality | $500 | Section 3 |
| Aged AR / AP "overdue" threshold | 60+ days | Section 2 |

## Process / rules

### Section 1 — Opening → closing walk
- One row per balance sheet line item with opening balance, closing balance, $ movement, % movement
- Flag lines exceeding the material-movement threshold for narrative explanation
- Always present comparative period side-by-side — never close-only

### Section 2 — Reconciliation status
For each reconcilable account, state the status from the underlying data:
- **Cash / bank**: result of the bank reconciliation check
- **Aged receivables**: GL receivables total vs aged debtors total
- **Aged payables**: GL payables total vs aged creditors total
- **Fixed asset register vs GL**: FAR accumulated depreciation total vs GL accumulated depreciation account
- Status options: **Reconciled** (within tolerance), **Reconciled with variance** (named variance), **Not reconciled** (named gap), **No FAR present**

### Section 3 — Manual journal trace
- Pull every manual journal in the period above the materiality threshold
- For each: date, narration, accounts touched, $ amount, supporting doc reference if present
- Confidence label per journal: **Direct** (clear narration + supporting doc), **Likely** (clear narration only), **Needs review** (no narration, no doc, unclear purpose)

### Section 4 — Unexpected movers
```

## write-math (1057-write-math)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/plugins/write-math
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1057-write-math/2340-write-math
- الوصف: Apply mathematical exposition conventions from Tao, Knuth, and Halmos whenever writing or discussing mathematics, including proofs and notation.

```markdown
# Write Math

Apply the mathematical writing conventions from the reference files below when
drafting or editing mathematical content in any format.

## Core Principles

1. **Clarity over cleverness** -- write so a graduate student beginning studies
   in the field can follow your argument
1. **Reader-centered exposition** -- minimize the reader's effort at every turn;
   signal where you are going and why
1. **Consistent notation** -- define symbols before use, reuse the same letter
   for the same concept, and never overload
1. **Structured proofs** -- state the theorem first, summarize the proof
   strategy, then present the formal argument in linear forward flow
1. **Communication over impression** -- plain language beats jargon; repetition
   beats synonym-hunting

## Workflow

1. Review against the essential checklist:
   `./references/essential/checklist.md`
1. For specific questions, consult the comprehensive references below

## Reference Navigation

**Quick reviews (default):**

- `references/essential/checklist.md` -- condensed, actionable rules

**Deep dives by topic:**

- `references/comprehensive/notation.md` -- notation principles, implicit
  conventions, TeX macros, disambiguation
- `references/comprehensive/theorems-and-proofs.md` -- theorem/lemma hierarchy,
  proof structure, statement design
- `references/comprehensive/paper-structure.md` -- title, abstract,
  introduction, body, conclusions, appendices
- `references/comprehensive/english-usage.md` -- sentence structure, word
  choice, logical connectives, common errors
- `references/comprehensive/reader-centered-writing.md` -- audience awareness,
  examples, signposting, assertion status
- `references/comprehensive/citations-and-references.md` -- signposting
  citations, specific references, journal selection
- `references/comprehensive/revision-and-process.md` -- drafting workflow,
  revision strategy, collaboration, reading math

## Sources

- Tao, T. "Advice on Writing Papers" (6 posts). terrytao.wordpress.com.
- Knuth, D., Larrabee, T., and Roberts, P. _Mathematical Writing_. 1989.
- Cohn, H. "Advice." cohn.mit.edu.
- Poonen, B. "Practical Suggestions for Mathematical Writing." MIT.
- Conrad, K. "Advice on Mathematical Writing." UConn.
- Su, F. E. "Guidelines for Good Mathematical Writing."
- Tsitsiklis, J. N. "A Few Tips on Writing Papers with Mathematical Content."
- Lagarias, J. C. "How to Write a Math Paper."
- Goldreich, O. "How to Write a Paper."
- Pak, I. "How to Write a Clear Math Paper: Some 21st Century Tips."
- Trzeciak, J. _Writing Mathematical Papers in English_. EMS, 1995.
- Berndt, B. C. "How to Write Mathematical Papers." UIUC.
- Krantz, S. G. "How to Write Your First Paper." AMS, 2007.
```
