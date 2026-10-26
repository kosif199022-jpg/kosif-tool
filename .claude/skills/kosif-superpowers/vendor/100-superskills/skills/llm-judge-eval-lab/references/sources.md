# مصادر «مختبر التقييم والقاضي الآلي» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## prompt-eval-and-regression (2361-prompt-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/prompt-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2361-prompt-engineering/9115-prompt-eval-and-regression
- الوصف: Build the eval/regression set that gates prompt changes — labeled input/expected pairs over the hard cases, a scoring method (exact / schema-valid / rubric / LLM-judge with its caveat), a pass threshold, a CI gate with the model pinned, and injection cases. Reach for this before shipping a prompt, when a tweak silently broke other cases, or to defend against prompt injection. Pairs with structured

```markdown
# Skill: Prompt eval & regression

Turn "it worked when I tried it" into "it is verified to still work." A prompt is
**unverified until the regression set is green.**

## Step 0 — One opinion up front
**Prompts are code.** They live in version control, change in reviewable diffs, and
must pass an eval before merge — exactly like any other code.

## Step 1 — Build the regression set
Collect labeled `input → expected` pairs covering:
- The **known-hard/edge cases**.
- **Every past failure** (each production bug becomes a permanent test).
- **Injection/jailbreak cases** (see §4 of the decision-trees doc).
Keep it in the repo next to the prompt.

## Step 2 — Choose a scoring method
Match the method to the task:
- **Exact / schema-valid** — closed-form or structured tasks. Cheapest, most
  reproducible; prefer it wherever possible.
- **Rubric** — explicit criteria, human or model graded.
- **LLM-as-judge** — scalable but the judge is a fallible prompt. **Judge the
  judge:** validate against human labels first; never let a model grade its own
  output unaudited; watch for position/verbosity/self-preference bias.
Set a **pass threshold** a change must clear.

## Step 3 — Pin for reproducibility
Pin the **model + version + temperature (+ seed where available)**. Handle
nondeterminism: temperature 0 where the task allows; multiple samples + a tolerance
where it doesn't. An eval against an unpinned model proves nothing tomorrow.

## Step 4 — Wire the CI gate
Run the regression set on every change to a prompt file; **fail the build on a
regression.** State honestly what the set does and doesn't cover — a green gate
over a thin set is false safety.

## Step 5 — Version & roll out
Prompts carry a version (semver or content hash). Roll changes out shadow → canary
→ full, with a watched metric and a rollback trigger.

## Step 6 — Hand off
- The **large offline eval program / benchmark design** → `llm-evaluation-engineering`.
- **Adversarial attacks on the running system** → `ai-red-teaming`.
- The **fix** for what the evals catch → `prompt-implementation-engineer` / `prompt-architect`.

## Output
A regression set + scoring method + threshold, a CI gate with the model pinned,
injection cases included, an honest coverage statement, and a versioning + canary
rollout plan.
```

## eval-ladder (2013-eval-ladder)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jrichlen/agent-plugins/tree/013353ad6ae0efb71384e0e14a0196b1be1884f6/plugins/eval-ladder
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2013-eval-ladder/7179-eval-ladder
- الوصف: Design and audit the eval ladder for an agent system: build tiers bottom-up from observed failures, pick the cheapest rung that can catch a given regression, name what each rung structurally cannot prove, validate every LLM judge against human labels (TPR and TNR separately, never raw agreement), and score irreversible-action scenarios pass^k rather than by majority. Use when designing, auditing, 

```markdown
# eval-ladder

## Invariant

Never present an eval result as evidence beyond what its tier structurally
proves: every green is reported with its blind spot, every LLM-judge verdict is
bounded by that judge's measured TPR/TNR against human labels, and a scenario
guarding an irreversible action passes only when EVERY trial passes (pass^k) —
never on a k-of-N majority.

A green check is a claim. The claim is not "the system works"; it is "this
tier's specific probe did not fire." Stating the difference is the whole skill.

## When to use this

- Designing an eval suite for an agent, skill, prompt, or tool from scratch.
- Auditing an existing suite: what does it cover, what can it structurally never
  cover, where would a real regression walk through.
- Adding a tier, a judge, or a scenario — deciding which rung it belongs on.
- A suite that is all-green and has never gone red: it may be measuring nothing.
- Reviewing someone's claim that a change is "verified" or "tested".
- Choosing a metric: pass@k, pass^k, a pass-rate floor, or a hard gate.

Do **not** use it to write the eval's actual content for a domain you have not
looked at. The first rung is looking at real failures; this skill will send you
there rather than let you skip it.

## The order that matters most

Build **bottom-up from observed failures**, not top-down from imagined
invariants. The single highest-return activity is error analysis: sample 20–100
real traces, have one person write a free-text note on the *first* thing that
goes wrong in each, cluster those notes into 4–8 failure modes, then build one
narrow binary check per mode. Suites authored from design intent test the
failures you imagined; suites authored from traces test the ones you have.

A suite with no error-analysis origin is a hypothesis, not a measurement. Say so
when you report it. See [judge-alignment.md](references/judge-alignment.md).

## The ladder

Cheapest first. Each rung catches a class of defect the rungs below it
structurally cannot — that "cannot" is what earns the rung its cost.

| # | Rung | Catches | Structurally cannot |
|---|---|---|---|
| 0 | **Structural** — parses, wiring, manifests, load-bearing greps | Broken plumbing, deleted invariant text | Whether a sentence still *means* anything |
| 1 | **Discriminating corpus** — mutate a known-good baseline, assert rejection *for the right reason* | A gate that has stopped gating | Defects it has no fixture for |
| 2 | **Code assertion** — regex, schema, state query, per observed failure | Anything a deterministic predicate can decide | Subjective quality; unanticipated shapes |
| 3 | **LLM judge** — binary, few-shot-critique-grounded rubric | Residual subjective failures | Anything beyond its measured TPR/TNR |
```

## eval-regression (2992-development-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/reidemeister94/development-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2992-development-skills/12687-eval-regression
- الوصف: Check skill routing or behavior, investigate a regression, or compare plugin changes with a base commit.

```markdown
# Eval regression

Use deterministic repository tests first. Stop when the target has no behavioral diff.

Resolve the plugin from the argument or cwd. Its catalog is `evals/evals.json`; the runner is `scripts/run_evals.py` in this skill.
Require the user to choose agent, model, and effort. Never select a costly model or high effort silently.

## Normal check

1. Select cases by changed paths with `--changed-from <base>`, or name them with `--case`. Do not select the full catalog implicitly.
2. Run the command without `--run`. The runner prints cases, modes, repeats, sessions, timeout, and maximum duration without starting an agent.
3. An approved plan that names this exact run already authorizes it. For a standalone eval, present the run plan and stop once.
4. After approval, repeat the same command with `--run`. Default to candidate-only, one run per case, 180 seconds, and four sessions maximum.
5. Report every failed assertion, timeout, non-zero exit, duration, and token count. Missing evidence is inconclusive.

## Escalation

- Compare base and candidate only when the user asks, or when a failed candidate check needs a baseline.
- Extract the base with `git archive`. Use the same cases, agent, model, effort, repeats, and timeout on both versions.
- Repeat only a failed or observably unstable case. Three repeats are a stability benchmark, not a default.
- `--all`, `--repeat > 1`, more sessions, or a longer timeout is new scope. Update the run plan and get authority first.
- Routing cases stop at the first Skill selection. Tool assertions are appropriate because routing is the contract.

Remove temporary base copies after the comparison. Do not edit or commit the target.

Deterministic assertions are `tool`, `tool_not`, `clean_worktree`, `changed_files_exact`, `file_contains`, `file_not_contains`, `transcript_contains`, and `tool_sequence`.
Use a semantic judge only when no filesystem, command, tool, ordering, or assistant-output observation can express the contract.
```

## eval (342-kernel)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/ariaxhan/kernel-claude
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/342-kernel/1220-eval
- الوصف: Eval-Driven Development (EDD) for AI workflows. pass@k metrics, capability evals, regression evals. Triggers: eval, edd, pass@k, capability, regression, benchmark.

```markdown
<skill id="eval">

<prerequisite>
AgentDB read-start has run. Check for existing eval definitions in _meta/research/.
Understand what behavior you're evaluating before writing evals.
</prerequisite>

<reference>
Skill-specific: skills/eval/reference/eval-research.md
</reference>

<core_principles>
1. DEFINE BEFORE CODE: Evals written first force clear thinking about success criteria.
2. CODE GRADERS > MODEL GRADERS: Deterministic checks beat probabilistic judgments.
3. STRUCTURAL SEPARATION FOR HIGH-STAKES: When stakes are real (security, payments, eval-of-evals, agent quality scoring), use the blind-evaluator agent — never self-score. Self-scoring inflates results ~36% structurally; procedural separation ("I won't peek") does not fix it.
4. TRACK PASS@K: pass@1 (first attempt), pass@3 (within 3 attempts). Target pass@3 > 90%.
5. REGRESSION BEFORE SHIP: Every change must pass existing evals before merge.
6. FAST EVALS GET RUN: Slow evals get skipped. Keep evaluation fast.
</core_principles>

<workflow>
1. DEFINE: Write eval criteria before implementation. (gate: criteria exist in writing before any code)
2. IMPLEMENT: Code to pass defined evals.
3. EVALUATE: Run evals, record pass@k. (gate: pass@3 > 90% for capability; pass^3 = 100% for regression)
4. REPORT: Document results in eval report format. See reference for template.
</workflow>

<blind_evaluation_protocol>
Use when implementing agent would otherwise score its own output (high-stakes: security, payments, agent quality):

1. Spawn `agents/blind-evaluator.md` as a fresh agent.
2. Pass ONLY: problem statement, rubric (3-7 criteria with PASS conditions + weights), artifact path.
3. Do NOT pass: implementer's checkpoint, summary, commit message, prompt, or expected solution.
4. (gate: blind evaluator runs contamination check — if forbidden inputs detected, returns INVALID; clean inputs and retry)
5. (gate: confidence < 0.7 from blind evaluator → escalate to human grader)

Two-phase eval protocol:
- Run 1: implementing agent solves cold, no eval feedback. Blind evaluator scores. This is the externally-reportable number.
- Run 2: implementing agent gets Run 1 score + rubric breakdown, then optimizes. For iteration only.
</blind_evaluation_protocol>

<metrics>
pass@k: "At least one success in k attempts"
- pass@1: First attempt success rate
- pass@3: Success within 3 attempts (typical target: > 90%)

pass^k: "All k trials succeed"
- pass^3: 3 consecutive successes
- Use for critical paths (auth, payments)

See reference for calculation formula and worked examples.
</metrics>

<grader_selection>
1. Code-based (preferred): grep, test suite, build, type-check — deterministic, fast.
2. Model-based: for open-ended outputs that can't be checked deterministically. Run multiple times, take majority.
```

## eval-harness-first (3104-llm-finetuning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/llm-finetuning
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13288-eval-harness-first
- الوصف: Build the evaluation harness that gates every fine-tuning run — golden sets, per-failure-mode graders, judge calibration, and base-model baselines. Use when starting a fine-tuning effort, when converting traces into an eval set, or when calibrating a judge against human labels.

```markdown
# Eval Harness First

The Phase 0 gate for the whole plugin:
`finetuning-method-selection` and every downstream
skill assume this harness exists before a training
config gets written. The harness is not a run-end
side artifact — it is the data-curation engine. The
same labeled traces that build the goldens feed
training data, minus an explicit holdout.

**Input:** production/agent traces if they exist, or
a task spec if they don't, plus labelers willing to
grade ≥100 examples.
**Output format:** the `eval/` directory below —
goldens, graders, drift suite, and the base-model
baseline that later phases gate on.

## The Gate

No eval harness, no fine-tune. Skip to a training
config and there is nothing to measure against,
nothing to catch regressions, and no labeled data
to train on. The flywheel:

1. **Collect traces** — production/agent spans, or
   synthetic tasks if none exist yet.
2. **Error analysis** — open coding on ≥100 traces,
   axial coding into 4–8 failure buckets.
3. **One grader per bucket** — deterministic first;
   calibrated LLM-judge only for genuinely
   subjective criteria.
4. **Prioritize** by frequency × severity × value.
5. **The labeled traces feed dataset curation, minus
   an explicit holdout.** Every `eval/goldens.jsonl`
   ID stays excluded from training data by ID.
6. **Train.**
7. **Re-run the same harness** on the checkpoint —
   not a different, looser one.
8. **Drift detection feeds back to step 2** — new
   production failure modes re-open error analysis.

Steps 2–4 build the harness; steps 5–8 are why it
must exist first — it is both the training data
source and the checkpoint's exit gate.

## Building Goldens

- **From traces, when they exist:** run error
  analysis — open coding on ≥100 real traces (read
  them, tag failures in your own words, no fixed
  taxonomy yet), then axial coding to collapse those
  tags into 4–8 named failure buckets. Fewer than 4
  means the coding pass was too shallow; more than 8
  means buckets need merging. **Exception:**
  single-failure-surface tasks (e.g. strict-schema
  extraction) may land at 1–2 buckets with per-field
  sub-metrics inside one grader — don't invent
  artificial splits with no evidence behind them.
- **Synthetic, when traces don't exist yet:**
  dimension-based generation — enumerate the axes
  that matter (task type, difficulty, edge case,
  persona) and sample the cross-product; free-
  generated prompts cluster around whatever's
  easiest to write.
- **Goldens are versioned like code** — commit
  `eval/goldens.jsonl`, diff it in review, tag it per
  release. It doubles as the CI regression suite.

## Graders

One grader per failure bucket from error analysis —
not one for the whole eval set. A single blended
score hides which bucket regressed.
```

## eval-harness-first (3499-llm-finetuning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/llm-finetuning
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3499-llm-finetuning/14235-eval-harness-first
- الوصف: Build the evaluation harness that gates every fine-tuning run — golden sets, per-failure-mode graders, judge calibration, and base-model baselines. Use when starting a fine-tuning effort, when converting traces into an eval set, or when calibrating a judge against human labels.

```markdown
# Eval Harness First

The Phase 0 gate for the whole plugin:
`finetuning-method-selection` and every downstream
skill assume this harness exists before a training
config gets written. The harness is not a run-end
side artifact — it is the data-curation engine. The
same labeled traces that build the goldens feed
training data, minus an explicit holdout.

**Input:** production/agent traces if they exist, or
a task spec if they don't, plus labelers willing to
grade ≥100 examples.
**Output format:** the `eval/` directory below —
goldens, graders, drift suite, and the base-model
baseline that later phases gate on.

## The Gate

No eval harness, no fine-tune. Skip to a training
config and there is nothing to measure against,
nothing to catch regressions, and no labeled data
to train on. The flywheel:

1. **Collect traces** — production/agent spans, or
   synthetic tasks if none exist yet.
2. **Error analysis** — open coding on ≥100 traces,
   axial coding into 4–8 failure buckets.
3. **One grader per bucket** — deterministic first;
   calibrated LLM-judge only for genuinely
   subjective criteria.
4. **Prioritize** by frequency × severity × value.
5. **The labeled traces feed dataset curation, minus
   an explicit holdout.** Every `eval/goldens.jsonl`
   ID stays excluded from training data by ID.
6. **Train.**
7. **Re-run the same harness** on the checkpoint —
   not a different, looser one.
8. **Drift detection feeds back to step 2** — new
   production failure modes re-open error analysis.

Steps 2–4 build the harness; steps 5–8 are why it
must exist first — it is both the training data
source and the checkpoint's exit gate.

## Building Goldens

- **From traces, when they exist:** run error
  analysis — open coding on ≥100 real traces (read
  them, tag failures in your own words, no fixed
  taxonomy yet), then axial coding to collapse those
  tags into 4–8 named failure buckets. Fewer than 4
  means the coding pass was too shallow; more than 8
  means buckets need merging. **Exception:**
  single-failure-surface tasks (e.g. strict-schema
  extraction) may land at 1–2 buckets with per-field
  sub-metrics inside one grader — don't invent
  artificial splits with no evidence behind them.
- **Synthetic, when traces don't exist yet:**
  dimension-based generation — enumerate the axes
  that matter (task type, difficulty, edge case,
  persona) and sample the cross-product; free-
  generated prompts cluster around whatever's
  easiest to write.
- **Goldens are versioned like code** — commit
  `eval/goldens.jsonl`, diff it in review, tag it per
  release. It doubles as the CI regression suite.

## Graders

One grader per failure bucket from error analysis —
not one for the whole eval set. A single blended
score hides which bucket regressed.
```
