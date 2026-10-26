# مصادر «سيّد البرومبتات الاحترافي» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## prompt-engineering-patterns (3103-llm-application-dev)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/llm-application-dev
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3103-llm-application-dev/13282-prompt-engineering-patterns
- الوصف: This skill should be used when the user asks to "optimize a prompt", "improve prompt performance", "design a prompt template", "write better prompts", "debug prompt issues", "use chain-of-thought", "structured prompting", "few-shot prompting", or wants to apply advanced prompt engineering patterns for production LLM applications.

```markdown
# Prompt Engineering Patterns

Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability.

## When to Use This Skill

- Designing complex prompts for production LLM applications
- Optimizing prompt performance and consistency
- Implementing structured reasoning patterns (chain-of-thought, tree-of-thought)
- Building few-shot learning systems with dynamic example selection
- Creating reusable prompt templates with variable interpolation
- Debugging and refining prompts that produce inconsistent outputs
- Implementing system prompts for specialized AI assistants
- Using structured outputs (JSON mode) for reliable parsing

## Core Capabilities

### 1. Few-Shot Learning

- Example selection strategies (semantic similarity, diversity sampling)
- Balancing example count with context window constraints
- Constructing effective demonstrations with input-output pairs
- Dynamic example retrieval from knowledge bases
- Handling edge cases through strategic example selection

### 2. Chain-of-Thought Prompting

- Step-by-step reasoning elicitation
- Zero-shot CoT with "Let's think step by step"
- Few-shot CoT with reasoning traces
- Self-consistency techniques (sampling multiple reasoning paths)
- Verification and validation steps

### 3. Structured Outputs

- JSON mode for reliable parsing
- Pydantic schema enforcement
- Type-safe response handling
- Error handling for malformed outputs

### 4. Prompt Optimization

- Iterative refinement workflows
- A/B testing prompt variations
- Measuring prompt performance metrics (accuracy, consistency, latency)
- Reducing token usage while maintaining quality
- Handling edge cases and failure modes

### 5. Template Systems

- Variable interpolation and formatting
- Conditional prompt sections
- Multi-turn conversation templates
- Role-based prompt composition
- Modular prompt components

### 6. System Prompt Design

- Setting model behavior and constraints
- Defining output formats and structure
- Establishing role and expertise
- Safety guidelines and content policies
- Context setting and background information

## Quick Start

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Define structured output schema
class SQLQuery(BaseModel):
    query: str = Field(description="The SQL query")
    explanation: str = Field(description="Brief explanation of what the query does")
    tables_used: list[str] = Field(description="List of tables referenced")

# Initialize model with structured output
llm = ChatAnthropic(model="claude-sonnet-5")
structured_llm = llm.with_structured_output(SQLQuery)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
```

## prompt-engineering-patterns (3498-llm-application-dev)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/llm-application-dev
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3498-llm-application-dev/14229-prompt-engineering-patterns
- الوصف: This skill should be used when the user asks to "optimize a prompt", "improve prompt performance", "design a prompt template", "write better prompts", "debug prompt issues", "use chain-of-thought", "structured prompting", "few-shot prompting", or wants to apply advanced prompt engineering patterns for production LLM applications.

```markdown
# Prompt Engineering Patterns

Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability.

## When to Use This Skill

- Designing complex prompts for production LLM applications
- Optimizing prompt performance and consistency
- Implementing structured reasoning patterns (chain-of-thought, tree-of-thought)
- Building few-shot learning systems with dynamic example selection
- Creating reusable prompt templates with variable interpolation
- Debugging and refining prompts that produce inconsistent outputs
- Implementing system prompts for specialized AI assistants
- Using structured outputs (JSON mode) for reliable parsing

## Core Capabilities

### 1. Few-Shot Learning

- Example selection strategies (semantic similarity, diversity sampling)
- Balancing example count with context window constraints
- Constructing effective demonstrations with input-output pairs
- Dynamic example retrieval from knowledge bases
- Handling edge cases through strategic example selection

### 2. Chain-of-Thought Prompting

- Step-by-step reasoning elicitation
- Zero-shot CoT with "Let's think step by step"
- Few-shot CoT with reasoning traces
- Self-consistency techniques (sampling multiple reasoning paths)
- Verification and validation steps

### 3. Structured Outputs

- JSON mode for reliable parsing
- Pydantic schema enforcement
- Type-safe response handling
- Error handling for malformed outputs

### 4. Prompt Optimization

- Iterative refinement workflows
- A/B testing prompt variations
- Measuring prompt performance metrics (accuracy, consistency, latency)
- Reducing token usage while maintaining quality
- Handling edge cases and failure modes

### 5. Template Systems

- Variable interpolation and formatting
- Conditional prompt sections
- Multi-turn conversation templates
- Role-based prompt composition
- Modular prompt components

### 6. System Prompt Design

- Setting model behavior and constraints
- Defining output formats and structure
- Establishing role and expertise
- Safety guidelines and content policies
- Context setting and background information

## Quick Start

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Define structured output schema
class SQLQuery(BaseModel):
    query: str = Field(description="The SQL query")
    explanation: str = Field(description="Brief explanation of what the query does")
    tables_used: list[str] = Field(description="List of tables referenced")

# Initialize model with structured output
llm = ChatAnthropic(model="claude-sonnet-5")
structured_llm = llm.with_structured_output(SQLQuery)

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
```

## enrich-prompt (1146-enrich-prompt)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coachlou/ambient-library/tree/2b66a4a4e764bd5884e652e8759a80cacab244fe/library/enrich-prompt
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1146-enrich-prompt/2727-enrich-prompt
- الوصف: Rewrites and augments a prompt to surface implicit constraints and blind spots, then answers the enriched version; use for "make this prompt better", "I keep getting shallow answers".

```markdown
Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/enrich-prompt/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
```

## prompt-pattern-selection (2361-prompt-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/prompt-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2361-prompt-engineering/9116-prompt-pattern-selection
- الوصف: Choose the prompting pattern — zero-shot, few-shot, chain-of-thought, decomposition/chaining, role framing, or self-consistency — by tracing the task against reliability need and token/latency cost. Reach for this when a prompt is inconsistent, when you're about to add examples 'just in case', or when one prompt is quietly doing several jobs. Pairs with structured-output-design.

```markdown
# Skill: Prompting-pattern selection

Pick the **cheapest pattern that clears the reliability bar.** Every step up the
ladder buys reliability with tokens and/or latency — so start low and climb only
on evidence of failure.

## Step 0 — One opinion up front
**Default to zero-shot.** A clear, well-ordered instruction solves more than people
expect. Reach for examples, CoT, or chaining only when a zero-shot prompt *measurably*
fails the hard cases — not preemptively.

## Step 1 — Characterize the failure
Run the prompt on the hard/edge cases and name *how* it fails:
- **Format/style drift** the model can't infer from words → few-shot.
- **Wrong multi-step reasoning** → CoT (one chain) or decomposition (separate jobs).
- **Wrong persona/domain register** → role framing.
- **Occasional wrong high-stakes answer** → self-consistency (sample N, vote).
- **Doing several jobs at once** → decomposition, always.

## Step 2 — Trace the tree
Traverse [`../../knowledge/prompt-decision-trees.md`](../../knowledge/prompt-decision-trees.md) §1
to a leaf. Record the path and the runner-up.

## Step 3 — Price the choice
Name what the pattern costs: few-shot adds input tokens; CoT adds output tokens +
latency; decomposition adds calls (latency, orchestration); self-consistency
multiplies cost by N. If the cost isn't justified by the reliability gain, drop back.

## Step 4 — Verify empirically
Run the chosen pattern against the regression set (owned by
`prompt-reliability-engineer`). Keep it only if it beats the simpler pattern on
*evidence*, not on a single lucky example.

## Step 5 — Hand off
- The **wording + example curation** → `prompt-implementation-engineer`.
- The **eval + regression gate** → `prompt-reliability-engineer`.
- If wording can't fix it, the problem is **architectural** → `prompt-architect`.

## Output
A pattern recommendation with the tree path, the runner-up and why it lost, the
token/latency cost named, and the empirical check that justified it.
```

## prompt-engineering (15-ai-tooling)

- الترخيص: **MIT**  ·  الأصل: https://github.com/acaprino/daodan/tree/39443d215d28fcbc32d651895b3cc45c64f24b6f/exports/claude/plugins/ai-tooling
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/15-ai-tooling/24-prompt-engineering
- الوصف: Knowledge base behind the prompt-engineer agent and /prompt-optimize: the source-of-truth order for model facts, the model-class gate, and six on-demand references covering reasoning patterns, output-shape enforcement, extraction prompting, judge prompts, agent and tool instructions, and dated vendor guidance. TRIGGER WHEN: designing, reviewing or optimizing a prompt, system message or agent instr

```markdown
# Prompt engineering knowledge base

The `prompt-engineer` agent and the `/prompt-optimize` command carry the method: extract the
behavioral contract, classify the archetype, diagnose, rewrite, report the semantic diff, label
every claim predicted, measured or verified. This skill carries the knowledge the method draws
on, split into references that are read only when a task needs them. Read this file first; it
tells you which reference to open and what every reference assumes you already decided.

## Source of truth

Model facts move faster than any bundled document. Three tiers, stop at the first that answers:

1. **The target model's current official page.** Anthropic: "Prompting best practices" at
   platform.claude.com plus the per-model page. OpenAI: the Model guidance hub and the
   reasoning best-practices page at developers.openai.com. Google: the Gemini 3 developer
   guide and the Gemma prompt-formatting page at ai.google.dev. When a prompt ships to
   production, fetch the page and confirm any vendor fact the rewrite restates.
2. **A measurement on that model**, yours or a published one on the same model and task.
3. **These references.** Orientation, dated, quoted; never the authority over tier 1.

A fact you could not confirm is unconfirmed, not confirmed absent: tag it *(verify)* in the
rewrite rather than deleting it or letting it read as checked.

## What decays and what does not

| Shelf life | Content | Lives in |
|---|---|---|
| **Stable** | The method: behavioral contract, archetype-aware rubric, semantic diff, epistemic labels, audit depth | the `prompt-engineer` role |
| **Slow** | The pattern catalog, the extraction shapes, the enforcement ladder, the judge shape, the agent-instruction anatomy | `reasoning-patterns.md`, `extraction-prompting.md`, `structured-output.md`, `judge-prompting.md`, `agent-instructions.md` |
| **Model-sensitive** | Thinking modes, effort names, prefill, cache multipliers, structured-output support, Gemma templates, the model-fit rows below | `model-guidance.md`; refresh every three months, like the `agent-sdk-builder` skill |
| **Measured and dated** | Every number with an arXiv ID or a vendor benchmark | the reference that cites it; each carries its check date |

## The model-class gate

Every reference assumes this decision was made first. Turn the target model into a class, then
read the row; the vendor matters less than the class.

| Class | Examples | Thinking control | Reasoning scaffold | Examples | Output shape | Measure first |
|---|---|---|---|---|---|---|
```

## langchain-prompt-engineering (1875-langchain-py-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/langchain-py-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1875-langchain-py-pack/6120-langchain-prompt-engineering
- الوصف: Manage LangChain 1.0 prompts like code \u2014 LangSmith prompt hub versioning,\n\

```markdown
# LangChain Prompt Engineering (Python)

## Overview

A team inherits a LangChain 1.0 codebase with **47 prompt strings** embedded as
f-string literals across 12 Python files. Nobody knows which version is live in
production. Rollback is git-only — requires a deploy. An A/B test on a single
prompt requires shipping code and running two services in parallel. A user pastes
a JSON snippet containing `{` into a chat endpoint and the whole thing throws:

```
KeyError: '"model"'
  File ".../langchain_core/prompts/string.py", line ..., in format
```

That is pain-catalog entry P57 — `ChatPromptTemplate.from_messages` with
f-string templates treat every brace-delimited identifier as a variable
marker — including ones that appear inside user content. Any literal braces in
user input (code snippets, JSON, LaTeX, CSS selectors) crash the chain. Four
prompt-layer pitfalls this skill fixes:

- **P57** — f-string template breaks on literal `{` in user input
- **P58** — Claude expects system content in the top-level `system` field,
  not a later `HumanMessage`; reordering middleware silently loses persona
- **P53** — Pydantic v2 strict default rejects the helpful extra fields
  models love to add to extraction schemas
- **P03** — `with_structured_output(method="function_calling")` silently drops
  `Optional[list[X]]` fields; use discriminated unions instead

Sections cover: consolidating scattered prompts into a `prompts/` module as
`ChatPromptTemplate` objects, pushing/pulling from the LangSmith prompt hub
(pinning production to 8-char commit hashes), switching to jinja2 template
format, Claude XML-tag conventions (`<document>`, `<example>`, `<context>`),
dynamic few-shot with semantic/MMR selectors, and A/B testing two prompt
versions via feature flag. Pin: `langchain-core 1.0.x`, `langsmith >= 0.1.99`,
`langchain-anthropic 1.0.x`, `langchain-openai 1.0.x`. Pain-catalog anchors:
P03, P53, P57, P58.

## Prerequisites

- Python 3.10+
- `langchain-core >= 1.0, < 2.0`
- `langsmith >= 0.1.99` (for `Client.push_prompt` / `pull_prompt`)
- At least one provider package: `pip install langchain-anthropic langchain-openai`
- `LANGSMITH_API_KEY`, `LANGSMITH_TRACING=true`, optional `LANGSMITH_PROJECT`
- Provider API key: `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`

## Instructions

### Step 1 — Consolidate scattered prompts into a `prompts/` module

Stop embedding prompt strings next to the call site. Create a flat module with
one file per logical prompt, exporting `ChatPromptTemplate` objects:

```python
# prompts/extract_invoice.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

EXTRACT_INVOICE = ChatPromptTemplate.from_messages([
    ("system",
     "You extract invoice fields from document text. Return only the declared "
```
