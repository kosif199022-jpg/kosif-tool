# مصادر «تنسيق الأمثلة ومجموعات البيانات» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## trace-to-training-data (3104-llm-finetuning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/llm-finetuning
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13294-trace-to-training-data
- الوصف: Convert evaluation traces and production logs into SFT examples and preference pairs. Use when graded traces or failure examples exist and need to become training data, when applying rejection sampling to model outputs, or when building DPO pairs from passing and failing runs.

```markdown
# Trace To Training Data

This skill assumes `eval-harness-first`
already graded the traces being
converted here — goldens, graders,
and `runs/<run-id>/results.json`
all exist before conversion
starts. This is the flywheel edge
that skill names in its own flow:
"the same labeled traces become
the training set." Conversion
happens here; grading already
happened upstream.

**Input:** graded traces —
`eval/goldens.jsonl` plus
`runs/<run-id>/results.json`, each
row carrying a `task_id`, a
`verdict` from the grader, and a
`reward` when the task supports a
scalar score (judge score,
execution partial-credit, or an
RLVR verifier):

```json
{"task_id": "t-042", "trace_id": "t-042-a3",
 "messages": [{"role": "user", "content": "..."}],
 "verdict": "pass", "reward": 0.91,
 "grader": "exact_match"}
```

**Output format:** rows shaped
exactly like `dataset-curation`'s
Format Selection table — SFT
`messages` rows or DPO
`prompt`/`chosen`/`rejected`
pairs — so this skill's output is
that skill's input with no
reshaping step in between.

## The Principle

The eval harness already did the
labeling work: every trace in
`results.json` carries a verdict,
and often a reward, before this
skill ever touches it. Converting
a graded trace into a training
row is mechanical — pick a shape
from `dataset-curation`'s table,
map fields, write JSONL.
**Curation is the work that
remains** — which traces clear a
quality bar, which pairs are
informative, and which rows must
never enter the training set at
all.

Treat any conversion step that
requires re-judging a trace as a
sign the harness is missing a
grader, not a gap this skill
should paper over. A trace with
no verdict or reward isn't
convertible yet — route it back
to `eval-harness-first` first,
don't hand-label it here to
unblock conversion.

## SFT From Traces

- **Keep the top-reward fraction
  of successful trajectories**,
  not every passing one. Rank
  passing traces by reward and
  take a fraction (the
  Agent-lightning pattern) rather
  than every trace that merely
  cleared the pass bar — a trace
  that barely passed is a weaker
  SFT signal than one that scored
  well above threshold.
- **Expert-corrected failures
  become gold SFT examples
  directly** (the Langfuse
  pattern) — when a human edits a
  failing trace's output into a
  correct one, that correction
  needs no reward threshold; a
  human already validated it.
  Route corrections straight into
  the SFT set.
- **Step-level masking beats
  whole-trajectory discard for
  multi-step traces.** When only
  some steps in a multi-step
  trajectory are bad, mask the
  loss on the bad steps and keep
  the good ones, rather than
  discarding the whole trajectory.
  SRFT reports 32.2% vs. 30.9% on
  SWE-bench for step-level critic
  masking over trajectory discard
```

## trace-to-training-data (3499-llm-finetuning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/llm-finetuning
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3499-llm-finetuning/14241-trace-to-training-data
- الوصف: Convert evaluation traces and production logs into SFT examples and preference pairs. Use when graded traces or failure examples exist and need to become training data, when applying rejection sampling to model outputs, or when building DPO pairs from passing and failing runs.

```markdown
# Trace To Training Data

This skill assumes `eval-harness-first`
already graded the traces being
converted here — goldens, graders,
and `runs/<run-id>/results.json`
all exist before conversion
starts. This is the flywheel edge
that skill names in its own flow:
"the same labeled traces become
the training set." Conversion
happens here; grading already
happened upstream.

**Input:** graded traces —
`eval/goldens.jsonl` plus
`runs/<run-id>/results.json`, each
row carrying a `task_id`, a
`verdict` from the grader, and a
`reward` when the task supports a
scalar score (judge score,
execution partial-credit, or an
RLVR verifier):

```json
{"task_id": "t-042", "trace_id": "t-042-a3",
 "messages": [{"role": "user", "content": "..."}],
 "verdict": "pass", "reward": 0.91,
 "grader": "exact_match"}
```

**Output format:** rows shaped
exactly like `dataset-curation`'s
Format Selection table — SFT
`messages` rows or DPO
`prompt`/`chosen`/`rejected`
pairs — so this skill's output is
that skill's input with no
reshaping step in between.

## The Principle

The eval harness already did the
labeling work: every trace in
`results.json` carries a verdict,
and often a reward, before this
skill ever touches it. Converting
a graded trace into a training
row is mechanical — pick a shape
from `dataset-curation`'s table,
map fields, write JSONL.
**Curation is the work that
remains** — which traces clear a
quality bar, which pairs are
informative, and which rows must
never enter the training set at
all.

Treat any conversion step that
requires re-judging a trace as a
sign the harness is missing a
grader, not a gap this skill
should paper over. A trace with
no verdict or reward isn't
convertible yet — route it back
to `eval-harness-first` first,
don't hand-label it here to
unblock conversion.

## SFT From Traces

- **Keep the top-reward fraction
  of successful trajectories**,
  not every passing one. Rank
  passing traces by reward and
  take a fraction (the
  Agent-lightning pattern) rather
  than every trace that merely
  cleared the pass bar — a trace
  that barely passed is a weaker
  SFT signal than one that scored
  well above threshold.
- **Expert-corrected failures
  become gold SFT examples
  directly** (the Langfuse
  pattern) — when a human edits a
  failing trace's output into a
  correct one, that correction
  needs no reward threshold; a
  human already validated it.
  Route corrections straight into
  the SFT set.
- **Step-level masking beats
  whole-trajectory discard for
  multi-step traces.** When only
  some steps in a multi-step
  trajectory are bad, mask the
  loss on the bad steps and keep
  the good ones, rather than
  discarding the whole trajectory.
  SRFT reports 32.2% vs. 30.9% on
  SWE-bench for step-level critic
  masking over trajectory discard
```

## gcp-examples-expert (1586-jeremy-gcp-starter-examples)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/ai-ml/jeremy-gcp-starter-examples
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1586-jeremy-gcp-starter-examples/4557-gcp-examples-expert
- الوصف: Generate production-ready Google Cloud code examples from official repositories

```markdown
# GCP Examples Expert

## Overview

Generate production-ready Google Cloud Platform code examples sourced from official repositories including ADK samples, Agent Starter Pack, Firebase Genkit, Vertex AI samples, Generative AI examples, and AgentSmithy. This skill maps user requirements to the appropriate GCP framework and delivers working code with security, monitoring, and deployment best practices baked in.

## Prerequisites

- Google Cloud project with billing enabled and Vertex AI API activated
- `gcloud` CLI authenticated with appropriate IAM roles (Vertex AI User, Cloud Run Developer)
- Node.js 18+ for Genkit/TypeScript examples or Python 3.10+ for ADK/Vertex AI examples
- Firebase CLI for Genkit deployments (`npm install -g firebase-tools`)
- API keys or service account credentials configured via Secret Manager (never hardcoded)

## Instructions

1. Identify the target framework by matching the request to one of six categories: ADK agents, Agent Starter Pack, Genkit flows, Vertex AI training, Generative AI multimodal, or AgentSmithy orchestration
2. Select the appropriate source repository and code pattern from `${CLAUDE_SKILL_DIR}/references/code-example-categories.md`
3. Adapt the template to the specified programming language (TypeScript, Python, or Go)
4. Configure security settings: IAM least-privilege service accounts, VPC Service Controls, Model Armor for prompt injection protection
5. Add monitoring instrumentation: Cloud Monitoring dashboards, alerting policies, structured logging, OpenTelemetry tracing
6. Set auto-scaling parameters with appropriate min/max instance counts for the deployment target
7. Include cost optimization: select Gemini 2.5 Flash for simple tasks, Gemini 2.5 Pro for complex reasoning, batch predictions for bulk workloads
8. Generate deployment configuration for the target platform (Cloud Run, Firebase Functions, or Vertex AI Endpoints)
9. Provide Terraform or IaC templates for reproducible infrastructure provisioning
10. Cite the source repository and link to official documentation for each pattern used

See `${CLAUDE_SKILL_DIR}/references/workflow.md` for the phased workflow and `${CLAUDE_SKILL_DIR}/references/best-practices-applied.md` for the full best-practices checklist.

## Output

- Complete, runnable code example with imports, configuration, and error handling
- Deployment configuration (Cloud Run service YAML, Firebase function config, or Terraform module)
- Environment variable template listing required secrets and API keys
- Monitoring setup: dashboard JSON, alerting policy definitions, log-based metrics
- Cost estimate guidance based on model selection and expected throughput
- Source repository citation and documentation links

## Error Handling

| Error | Cause | Solution |
```

## fine-tune (558-fine-tune-prep)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/fine-tune-prep
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/558-fine-tune-prep/1587-fine-tune
- الوصف: Generate dataset preparation for model fine-tuning

```markdown
Generate dataset preparation for model fine-tuning. This plugin is part of the Plugin Hub developer tools collection.

Use the tools provided by the plugin-hub MCP server to accomplish tasks related to fine-tune-prep.
```

## ai-evaluation-dataset (229-mas-ai-workflows)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alivirgo/major-ai-skills/tree/ba3a5729d60646626fee31c2d9906adc59f418dc/plugins/mas-ai-workflows
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/229-mas-ai-workflows/716-ai-evaluation-dataset
- الوصف: Build a versioned JSONL evaluation dataset for an AI workflow, with acceptance criteria, held-out cases, and leakage checks.

```markdown
# Evaluation Dataset

## Scope

Ask for the target task, deployment population, known failures, and which errors are unacceptable. Reuse the project's evaluator and data format when present; otherwise propose JSONL records with id, input, expected_behavior, forbidden_behavior, rubric, source, and split.

## Procedure

Separate training examples, prompt-development examples, and held-out evaluation cases. Split by originating document, user, or conversation rather than individual rows when rows share information. Keep near-duplicates in the same split. Remove secrets and obtain permission before including private user content.

## Checks

Include ordinary cases, boundary cases, ambiguous inputs, and explicit abstention cases. Label expected behavior before viewing candidate model outputs. For subjective outputs, use observable rubric criteria instead of a single preferred phrasing.

## Failure Handling

Report case counts by split and slice, provenance, duplicate findings, and unresolved label disagreements. Freeze a dataset version and content hash before comparing models. Never report evaluation accuracy without actually running the evaluator.

## Deliverable

Given several paraphrases of one support ticket, keep them in a single split; a random row split would leak the answer.
```

## dataset-curation (3104-llm-finetuning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/llm-finetuning
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13287-dataset-curation
- الوصف: Prepare, format, and validate datasets for supervised fine-tuning and preference training. Use when converting raw data into training format, applying chat templates, configuring sequence packing, generating synthetic training data, or writing a dataset card before a run.

```markdown
# Dataset Curation

This skill assumes `finetuning-method-selection`
already routed here — the next step is preparing
data, not choosing a method. What follows: format
selection by target method, the template/packing
mechanics behind the most common silent training
failures, rules for mixing in synthetic data
without collapse, and the dataset card that closes
out Phase 2 before a run starts.

**Input:** raw examples (demonstrations, preference
judgments, or task prompts) plus a routing decision
from `finetuning-method-selection`.
**Output format:** a formatted, packed, validated
JSONL dataset plus a completed dataset card — the
Phase 2 artifact `/finetune` checks before launching
training.

## Format Selection

| Method | Shape | Rows |
|---|---|---|
| SFT, single-turn | Instruct (`instruction`/`response` or `prompt`/`completion`) | ~1,000+ floor |
| SFT, multi-turn | Conversation / ChatML `messages` list | ~1,000+ floor |
| DPO / ORPO | Preference pair (`prompt`, `chosen`, `rejected`) | Method-dependent, see `preference-optimization` |
| KTO | Unpaired (`prompt`, `completion`, `label`) | Method-dependent, see `preference-optimization` |
| GRPO / RLVR | Prompt-only (`prompt` + verifier metadata) | Method-dependent, see `grpo-rlvr-training` |

- **~1,000+ rows is the recommended floor for SFT**,
  not a target. Below it, a handful of low-quality
  or duplicate examples can dominate the gradient;
  above it, **quality over quantity** — a smaller
  verified, deduplicated set beats a larger noisy one.
- The ChatML shape, for orientation; the other four
  formats plus a ShareGPT conversion note live in
  `references/formats-and-templates.md`:

  ```json
  {"messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]}
  ```

## Chat Templates and Loss Masking

Apply the target model's chat template **before**
any concatenation or packing, never after — packing
raw text and templating the packed blob afterward
corrupts turn boundaries, landing role markers in
the wrong place relative to each example.

- **Train on assistant responses only.** Mask the
  loss (`-100` in the labels tensor) over system/user
  turns and the template's own role markers — only
  assistant-turn content tokens contribute to loss.
- **Template/tokenizer mismatches are a top silent
  failure mode.** A model trained against one chat
  template but served or evaluated with a different
  one degrades without erroring. Verify the same
  template string used in training is applied at
  inference and eval time.
- **Keep the dataset in `messages` shape** and let
  the trainer template and mask it
  (`assistant_only_loss=True` in current TRL) —
  pre-rendering to a flat text field destroys the
  turn boundaries masking needs. Full code sketch:
```
