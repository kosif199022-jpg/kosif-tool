# مصادر «اختبارات A/B والتجارب» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## experiment-analysis (2235-applied-statistics)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/applied-statistics
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2235-applied-statistics/8495-experiment-analysis
- الوصف: Analyze a completed A/B test or experiment defensibly — check it against the pre-registered plan, run the primary-metric test, report effect size + CI (not just p), check guardrail metrics, apply a multiple-comparison correction across metrics/segments, and screen for the peeking/p-hacking pitfalls before declaring a winner. Used by `applied-statistician` (primary).

```markdown
# Skill: experiment-analysis

> **Invoked by:** `applied-statistician` (primary). Pairs with [`../power-and-sample-size/SKILL.md`](../power-and-sample-size/SKILL.md) (run first, at design time) and [`../choose-statistical-test/SKILL.md`](../choose-statistical-test/SKILL.md) (names the underlying test).
>
> **When to invoke:** "is this A/B winner real?"; "the experiment finished — what does it say?"; "can we ship variant B?"
>
> **Output:** a verdict (ship / don't ship / inconclusive) backed by the primary-metric effect size + CI, the guardrail check, the multiplicity correction, and an explicit pitfall screen.

## Procedure

1. **Recover the analysis plan.** Was there a pre-registered primary metric, test, and stopping rule ([`../../templates/analysis-plan.md`](../../templates/analysis-plan.md))? If analysis decisions were made *after* seeing data, flag the p-hacking exposure (pitfall #1) and treat findings as exploratory.
2. **Check the stopping rule.** Was the test stopped at the planned sample, or stopped early when it "looked significant"? Early stopping on a fixed-horizon test = peeking (pitfall #3) → the nominal p-value is not valid; downgrade confidence.
3. **Run the primary-metric test** (via `choose-statistical-test`). Report the **effect size + confidence interval** as the headline — the p-value is secondary (pitfall #6). "Significant but the CI includes trivially small effects" is not a ship signal.
4. **Check guardrail metrics.** A primary-metric win that degrades a guardrail (latency, churn, revenue/user) is not a win. State each guardrail's movement + CI.
5. **Correct for multiplicity.** If you tested several metrics or segments, apply Holm/Bonferroni (confirmatory) or Benjamini-Hochberg (exploratory) — see [`../../knowledge/statistical-pitfalls.md`](../../knowledge/statistical-pitfalls.md). A "winning segment" found after slicing 10 ways is usually noise.
6. **Sanity-check for Simpson's paradox** (pitfall #4): does the aggregate result hold within key subgroups, or does the group mix drive it?
7. **Verdict** in plain language: ship / don't ship / inconclusive (underpowered) — with the effect, CI, and the main caveat.

## Output shape

```
Primary metric: <metric> — variant B <+X% / +X units>, 95% CI [<lo>, <hi>], p = <p>
Decision-relevant? <effect vs the MDE that justified the test>
Guardrails: <metric: movement + CI; pass/fail> ...
Multiplicity: <# metrics/segments tested; correction applied>
Pitfall screen: pre-registered? stopped at planned n? peeking? Simpson's?
Verdict: SHIP / DON'T SHIP / INCONCLUSIVE — <one-line reason + main caveat>
```

## Guardrails
- The headline is the **effect size + CI**, never a bare "p < 0.05."
```

## setting-up-experiment-tracking (1581-experiment-tracking-setup)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-ml/experiment-tracking-setup
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1581-experiment-tracking-setup/4552-setting-up-experiment-tracking
- الوصف: Implement machine learning experiment tracking using MLflow or Weights

```markdown
# Experiment Tracking Setup

Configure ML experiment tracking with MLflow or Weights & Biases, including environment setup and code for logging parameters, metrics, and artifacts.

## Overview

This skill streamlines the process of setting up experiment tracking for machine learning projects. It automates environment configuration, tool initialization, and provides code examples to get you started quickly.

## How It Works

1. **Analyze Context**: The skill analyzes the current project context to determine the appropriate experiment tracking tool (MLflow or W&B) based on user preference or existing project configuration.
2. **Configure Environment**: It configures the environment by installing necessary Python packages and setting environment variables.
3. **Initialize Tracking**: The skill initializes the chosen tracking tool, potentially starting a local MLflow server or connecting to a W&B project.
4. **Provide Code Snippets**: It provides code snippets demonstrating how to log experiment parameters, metrics, and artifacts within your ML code.

## When to Use This Skill

This skill activates when you need to:

- Start tracking machine learning experiments in a new project.
- Integrate experiment tracking into an existing ML project.
- Quickly set up MLflow or Weights & Biases for experiment management.
- Automate the process of logging parameters, metrics, and artifacts.

## Examples

### Example 1: Starting a New Project with MLflow

User request: "track experiments using mlflow"

The skill will:

1. Install the `mlflow` Python package.
2. Generate example code for logging parameters, metrics, and artifacts to an MLflow server.

### Example 2: Integrating W&B into an Existing Project

User request: "setup experiment tracking with wandb"

The skill will:

1. Install the `wandb` Python package.
2. Generate example code for initializing W&B and logging experiment data.

## Best Practices

- **Tool Selection**: Consider the scale and complexity of your project when choosing between MLflow and W&B. MLflow is well-suited for local tracking, while W&B offers cloud-based collaboration and advanced features.
- **Consistent Logging**: Establish a consistent logging strategy for parameters, metrics, and artifacts to ensure comparability across experiments.
- **Artifact Management**: Utilize artifact logging to track models, datasets, and other relevant files associated with each experiment.

## Integration

This skill can be used in conjunction with other skills that generate or modify machine learning code, such as skills for model training or data preprocessing. It ensures that all experiments are properly tracked and documented.

## Prerequisites

- Appropriate file access permissions
- Required dependencies installed

## Instructions
```

## oss-contribution-shape-by-conversion-rate (3337-oss-contribution-shape-by-conversion-rat)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/oss-contribution-shape-by-conversion-rate
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3337-oss-contribution-shape-by-conversion-rat/13851-oss-contribution-shape-by-conversion-rat
- الوصف: Decide whether to contribute to an open-source repo as a pull request or as an issue by measuring the repo's conversion rate first: what share of merged PRs come from the maintainers, how many outside PRs sit open, how far main is ahead of the last release, and what reviews an outside PR actually gets (bots only, or a human). Use when: (1) you are about to write a patch for a fast-moving repo (tho

```markdown
# Contribution shape by conversion rate

> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/oss-contribution-shape-by-conversion-rate/SKILL.md`).

## Problem

The internet says "send a patch". On a repo where three people merge 95% of
everything and land thousands of commits between releases, an outside patch is
a liability with a diff attached: somebody has to hold it against a `main`
that moved thousands of times, and nobody has the time. The same repo will
take a well-argued issue and reimplement it as a maintainer PR within weeks.
Sending the wrong shape costs you the work and costs the maintainer triage.

Measured on one such repo over two months: the two features asked for in
issues shipped together in one maintainer PR; the patch sent for one of those
features sat 32 days with seven green bot checks, none of the required
workflows ever run, and no human review, then was superseded. The required
workflows had been added to the repo after the PR's last push; nothing ever
asked them to run. A bug with nine competing fix PRs, four by the maintainer, got
its fix attached to a duplicate issue filed four months after the original.

## Context / Trigger Conditions

- Before writing a patch for a repo you do not maintain.
- A PR of yours shows `BLOCKED` with green bot checks and no runs of the
  required checks; or `mergeStateStatus` stays `UNKNOWN`/`UNSTABLE` with
  nobody assigned. Check the dates before blaming the fork: a workflow added
  to the base branch after your last push never fires on your PR, and a
  ruleset that requires its context then waits forever. A rebase and push
  (or close and reopen) fires it.
- The review log on a maintainer PR reads "automated pre-merge suggestion
  triage", CodeRabbit, Cursor, greptile ("too many files"), Bugbot ("spend
  limit reached"): the repo reviews by robot.
- A maintainer PR "Fixes #<duplicate>" and never mentions the original.

## Solution

### 1. Measure four numbers (five minutes, read-only)

Use the search API's `total_count` for counts, with the date window pinned
at **both** ends. Two traps, both verified:

- `gh pr list --search ...` rides on the GitHub Search API, which refuses
  anything past result 1000 (`422 Only the first 1000 search results are
  available` on page 11). `--limit 3000` silently returns 1000. A count built
  from that listing was off by 5x.
- `total_count` is not capped, but an open-ended window (`merged:>=DATE`) is a
  live number: 1,889 one day, 2,112 six days later, same query. Pin the upper
  bound and record the date next to the number.

```bash
R=owner/repo; WIN=2026-07-10..2026-09-09
q() { gh api -X GET search/issues -f q="repo:$R $1" --jq .total_count; }
```

## surge-experiment (1567-tonone)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-agency/tonone
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4346-surge-experiment
- الوصف: Growth experiment design — structure a growth hypothesis, define metric, baseline, expected lift, and kill condition for a single experiment. Use when asked to "design a growth experiment", "test this growth idea", "experiment framework", "how do we test if this works", or "growth hypothesis".

```markdown
# Growth Experiment Design

You are Surge — the growth engineer on the Product Team. Design the experiment before you build anything.

Follow the output format defined in docs/output-kit.md — 40-line CLI max, box-drawing skeleton, unified severity indicators, compressed prose.

## Steps

### Step 1: State the Growth Lever

Identify which part of the funnel this experiment targets:

| Funnel Stage | Examples                                                       |
| ------------ | -------------------------------------------------------------- |
| Acquisition  | SEO, paid ads, referral, partner integrations, content         |
| Activation   | Onboarding flow, time-to-value, setup wizard, templates        |
| Retention    | Habit loops, notifications, win-back emails, feature discovery |
| Revenue      | Upgrade triggers, paywall design, pricing page, trial length   |
| Referral     | Invite mechanics, share flows, virality coefficient            |

State: "This experiment targets [stage] and specifically [the lever]."

### Step 2: Write the Growth Hypothesis

Use this format:

```
Hypothesis: If we [specific change], then [primary metric] will [increase/decrease]
            by [X%], because [mechanism — the causal theory].

We believe this because: [evidence — past experiment, user research, competitor observation,
                           or first-principles reasoning]

Kill condition: If [primary metric] does not move by [MDE] within [N days], we stop.
```

The mechanism is mandatory. Without it, you're guessing and won't learn from the result.

### Step 3: Define the Experiment

```
Experiment name: [short, memorable]
Type: A/B test / Multi-variate / Phased rollout / Qualitative test

Control: [what the current experience is]
Variant: [exactly what changes — be specific enough to implement]

Target population: [who is included — new users / existing / paid / all?]
Exclusions: [who is excluded — why]
Traffic split: [50/50 / 90/10 / staged rollout — and why]
```

### Step 4: Define Metrics

**Primary metric** (one only — the decision metric):

- Metric: [name]
- Baseline: [current value]
- MDE: [minimum detectable effect — the smallest lift worth shipping for]
- Direction: [increase / decrease]

**Secondary metrics** (directional, not decision):

- [metric 1] — expected direction
- [metric 2] — expected direction

**Guardrail metrics** (must not regress):

- [metric] — must not drop more than [X%]

### Step 5: Size and Timeline

```
Required users per variant: [N] — (use lumen-abtest for precise calculation)
Daily eligible traffic: [N]
Minimum run time: 14 days (for weekly seasonality)
Estimated run time: [N] days
Decision date: [date]
```

If run time exceeds 6 weeks, the experiment is too ambitious for available traffic. Options:
```

## surge-experiment (1567-tonone)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-agency/tonone
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1567-tonone/4508-surge-experiment
- الوصف: Growth experiment design — structure a growth hypothesis, define metric, baseline, expected lift, and kill condition for a single experiment. Use when asked to "design a growth experiment", "test this growth idea", "experiment framework", "how do we test if this works", or "growth hypothesis".

```markdown
# Growth Experiment Design

You are Surge — the growth engineer on the Product Team. Design the experiment before you build anything.

Follow the output format defined in docs/output-kit.md — 40-line CLI max, box-drawing skeleton, unified severity indicators, compressed prose.

## Steps

### Step 1: State the Growth Lever

Identify which part of the funnel this experiment targets:

| Funnel Stage | Examples                                                       |
| ------------ | -------------------------------------------------------------- |
| Acquisition  | SEO, paid ads, referral, partner integrations, content         |
| Activation   | Onboarding flow, time-to-value, setup wizard, templates        |
| Retention    | Habit loops, notifications, win-back emails, feature discovery |
| Revenue      | Upgrade triggers, paywall design, pricing page, trial length   |
| Referral     | Invite mechanics, share flows, virality coefficient            |

State: "This experiment targets [stage] and specifically [the lever]."

### Step 2: Write the Growth Hypothesis

Use this format:

```
Hypothesis: If we [specific change], then [primary metric] will [increase/decrease]
            by [X%], because [mechanism — the causal theory].

We believe this because: [evidence — past experiment, user research, competitor observation,
                           or first-principles reasoning]

Kill condition: If [primary metric] does not move by [MDE] within [N days], we stop.
```

The mechanism is mandatory. Without it, you're guessing and won't learn from the result.

### Step 3: Define the Experiment

```
Experiment name: [short, memorable]
Type: A/B test / Multi-variate / Phased rollout / Qualitative test

Control: [what the current experience is]
Variant: [exactly what changes — be specific enough to implement]

Target population: [who is included — new users / existing / paid / all?]
Exclusions: [who is excluded — why]
Traffic split: [50/50 / 90/10 / staged rollout — and why]
```

### Step 4: Define Metrics

**Primary metric** (one only — the decision metric):

- Metric: [name]
- Baseline: [current value]
- MDE: [minimum detectable effect — the smallest lift worth shipping for]
- Direction: [increase / decrease]

**Secondary metrics** (directional, not decision):

- [metric 1] — expected direction
- [metric 2] — expected direction

**Guardrail metrics** (must not regress):

- [metric] — must not drop more than [X%]

### Step 5: Size and Timeline

```
Required users per variant: [N] — (use lumen-abtest for precise calculation)
Daily eligible traffic: [N]
Minimum run time: 14 days (for weekly seasonality)
Estimated run time: [N] days
Decision date: [date]
```

If run time exceeds 6 weeks, the experiment is too ambitious for available traffic. Options:
```

## diagnosing-experiment-results (2957-posthog)

- الترخيص: **MIT**  ·  الأصل: https://github.com/posthog/ai-plugin/tree/469d1773e9cb55cb2d0cffd0a91e12bbeff8d32e
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2957-posthog/12302-diagnosing-experiment-results
- الوصف: Diagnoses bias, anomalies, and strange results on a PostHog experiment. Covers 0-exposure experiments, sample ratio mismatch, identity fragmentation, multi-variant exposure, uneven-split exclusion bias, significance traps (peeking, A/A, Bayesian vs Frequentist), PostHog-vs-SQL discrepancies, surprises after mid-run edits, and qualitative follow-up via a variant-split survey.\nTRIGGER when: user as

```markdown
# Diagnosing experiment results

This skill answers: **My PostHog experiment results look wrong, biased, or empty — what's going on?**

Match the user's complaint in the dispatch table, then read the matching reference file for the
diagnostic.

Each diagnostic in the reference files is tagged `[HIGH]`, `[MEDIUM]`, or `[LOW]` based on how
strongly it's verified — `[HIGH]` is verified directly in PostHog code, `[MEDIUM]` is partially or
team-source verified, `[LOW]` describes SDK/external behavior that wasn't verified here. Treat `[LOW]`
items as hypotheses to test, not facts to assert.

## Step 1 — Resolve the experiment

If the user refers to an experiment by name or description, load the `finding-experiments` skill first to
resolve it to a concrete ID.

Call `experiment-get` and pull these fields. They are inputs for almost every diagnostic:

- `parameters.feature_flag_variants[].rollout_percentage` — the variant split
- `parameters.rollout_percentage` — the overall rollout (% of users entering the experiment)
- `exposure_criteria.multiple_variant_handling` — defaults to `"exclude"` if absent
- `exposure_criteria.exposure_config.event` — unset means the default exposure event; read which one
  from `resolved_exposure_event` (`$feature_flag_called` or `$experiment_exposure` — resolved
  server-side, same properties either way)
- `exposure_criteria.filterTestAccounts` — defaults to `true`
- `feature_flag.active`, status (`draft` / `running` / `paused` / `exposure_frozen` / `stopped`), `start_date`, `end_date`
- `feature_flag.filters.groups[]` — for each group read `variant`, `properties`, and
  `rollout_percentage`. Any non-null `variant` is a forced-variant override on the matched cohort
  (release-condition assignment, not randomized) — surfaces A7. Watch for the severe shape (A7b): a
  variant-pinned group with broad/empty `properties` at high rollout, or no group left randomized
  (`variant: null`) / no release path to one arm — that starves the other variant (one arm gets ~0
  analyzable exposures). See `references/bias-and-skew.md`.
- `stats_config` — Bayesian (default) or Frequentist

## Step 1.5 — Pull a diagnostic snapshot (verify before asking)

Before asking the user clarifying questions, pull the diagnostic snapshot in
[references/diagnostic-snapshot.md](references/diagnostic-snapshot.md). Most diagnostics in this skill
can be confirmed or ruled out from that data without an interview.

## Step 2 — Match symptom to diagnostic

| User says...                                                                               | Diagnostic group                             |
| ------------------------------------------------------------------------------------------ | -------------------------------------------- |
```
