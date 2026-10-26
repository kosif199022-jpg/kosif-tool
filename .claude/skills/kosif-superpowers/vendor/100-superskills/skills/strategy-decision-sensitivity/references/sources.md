# مصادر «الاستراتيجية وحساسية القرار» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## seo-roadmap-prioritization (2199-lvtd-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/LVTD-LLC/skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8183-seo-roadmap-prioritization
- الوصف: Prioritize SEO initiatives as product roadmap work with impact, effort, confidence, resourcing, executive pitch, cross-functional ownership, quarterly planning, and business KPI alignment. Use when building SEO roadmaps, scoring SEO work, requesting engineering/design/content resources, annual planning, executive buy-in, or turning SEO recommendations into product-ready asks.

```markdown
# SEO Roadmap Prioritization

Use this skill to turn SEO ideas into product-style roadmap items that can compete for resources, survive planning, and ship through cross-functional teams.

This skill is derived from Eli Schwartz's *Product-Led SEO* and uses transformed guidance with durable book-topic references. Do not copy book prose into user outputs.

## Quick Start

1. Load `guidelines.md` to choose the relevant reference.
2. Use `workflows/prioritize-seo-roadmap.md` for roadmap work.
3. Translate SEO asks into business language, not SEO jargon.
4. Score initiatives by impact, effort, confidence, and strategic fit.
5. Include owners, dependencies, resource asks, and measurement.

## Default Output

When asked for a roadmap or prioritization, return:

1. **Roadmap table** - initiative, why, fix/build, impact, effort, confidence, owner, dependencies, timing.
2. **Recommended sequence** - now, next, later.
3. **Resource asks** - engineering, product, design, content, data, executive support.
4. **Executive pitch** - business KPI framing and expected payoff.
5. **Risks and tradeoffs** - what may be displaced or delayed.
6. **Measurement plan** - leading indicators and business outcomes.

## Contents

| Need | Start Here |
|------|------------|
| Understand SEO as product roadmap work | `references/core/knowledge.md` |
| Apply prioritization rules | `references/core/rules.md` |
| See scoring examples | `references/core/examples.md` |
| Build a roadmap | `workflows/prioritize-seo-roadmap.md` |
| Route by task | `guidelines.md` |
```

## experimentation-strategy-roadmap (2199-lvtd-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/LVTD-LLC/skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8073-experimentation-strategy-roadmap
- الوصف: Prioritize an experimentation platform roadmap across rate, quality, cost, usability, process, infrastructure, and advanced methods. Use when deciding which experimentation capability to build next, whether to platformize interleaving or adaptive testing, how to align experimentation with company goals, or how to trade off speed versus rigor.

```markdown
# Experimentation Strategy Roadmap

Use this skill to decide which experimentation capability deserves investment
next. It helps balance experimentation rate, quality, cost, usability, process,
infrastructure, and company strategy when adopting advanced techniques.

## Source Traceability

Primary source: *Next-Level A/B Testing* by Leemay Nassery. Guidance is
transformed and paraphrased from Chapter 1 on rate, quality, and cost; and
Chapter 9 on optimization strategies, process improvements, infrastructure,
company goals, user needs, robustness, cost versus quality, and evaluating new
strategies.

Related skills:

- `ab-testing-platform-strategy` for platform architecture and build/buy scope.
- `experimentation-throughput-strategy` for increasing experiment rate.
- `experiment-verification-monitoring` for quality investments.
- `experiment-sensitivity-optimization`, `ml-experiment-evaluation`, and
  `adaptive-experimentation-strategy` for advanced technique candidates.

## Reference Routing

| Need | Read |
|------|------|
| Roadmap concepts | `references/core/knowledge.md` |
| Prioritization and platformization rules | `references/core/rules.md` |
| Strategy examples | `references/core/examples.md` |
| Step-by-step roadmap workflow | `workflows/prioritize-experimentation-roadmap.md` |

## Workflow

1. State the company's strategic goals and current experimentation constraints.
2. Classify candidate work as optimization strategy, process improvement,
   infrastructure enhancement, or a combination.
3. Score each candidate against rate, quality, cost, usability, robustness, and
   adoption effort.
4. Prototype advanced strategies before platformizing them.
5. Sequence the roadmap so tools, processes, and education support each other.
6. Define success metrics for the platform itself.

## Output Format

```markdown
# Experimentation Strategy Roadmap

## Strategic Context
[Company/product goals and experimentation constraints.]

## Recommendation
[Top roadmap priority and why.]

## Candidate Initiatives
| Initiative | Type | Rate | Quality | Cost | Usability | Effort |
|------------|------|------|---------|------|-----------|--------|

## Roadmap
1. [Now]
2. [Next]
3. [Later]

## Adoption Plan
- Tooling:
- Process:
- Education:
- Success metrics:
```

## Quality Bar

- Do not platformize an advanced method before proving it in real use cases.
- Do not optimize for experimentation rate while ignoring trust and quality.
- Do not build tools without updating process and education.
- Do not adopt complexity that product teams cannot understand or operate.
```

## good-strategy-bad-strategy (3435-strategy-growth)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wondelai/skills/tree/c172996495bed0fcd26896a9416b2093fd7073f0/plugins/strategy-growth
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3435-strategy-growth/14105-good-strategy-bad-strategy
- الوصف: Formulate and audit real strategy using Richard Rumelt''s "Good Strategy Bad Strategy": an honest diagnosis, a guiding policy, and coherent action instead of goals, vision, and wishful thinking. Use when the user mentions "good strategy bad strategy", "strategy kernel", "diagnosis guiding policy coherent action", "our strategy is just goals", "strategic planning", "mission vs strategy", "annual pl

```markdown
# Good Strategy Bad Strategy

A framework for creating and auditing strategy, distilled from Richard Rumelt's *Good Strategy Bad Strategy: The Difference and Why It Matters*. Good strategy has a simple underlying logic — an honest diagnosis of the critical challenge, a guiding policy for overcoming it, and coherent actions that carry the policy out. Use this skill to detect the four hallmarks of bad strategy and to replace goal lists and vision decks with a working kernel.

## Core Principle

**Strategy is coherent action backed by an honest diagnosis — not goals, vision, or wishful thinking.** A goal ("20% growth") names an ambition; a strategy explains how the ambition will be achieved given the actual obstacles. Bad strategy is not the absence of strategy but an active substitute for it: buzzword fluff, refusal to name the challenge, and laundry lists of initiatives. The heart of strategy work is choice — concentrating effort and resources on the one or two pivotal objectives whose accomplishment unlocks everything else.

## Scoring

**Goal: 10/10.** Score strategies, plans, and strategy documents by walking the eight rows of the Quick Diagnostic and counting how many pass. Report the current score and the specific changes needed to reach 10/10. The bands below name what each tier looks like; the row count keeps the rating reproducible run to run.

- **9-10 (8 rows pass):** Complete kernel — honest diagnosis, choiceful guiding policy, coordinated resource-backed actions — aimed at a pivot point, with an explicit list of what will not be done
- **7-8 (6-7 pass):** Kernel present but one element weak: thin diagnosis, a policy that rules little out, or actions not yet coordinated and funded
- **5-6 (4-5 pass):** The challenge is named, but the plan is a list of independent initiatives and some goals masquerade as strategy
- **3-4 (2-3 pass):** Mostly goals, targets, and vision statements; no diagnosis; fluff in key passages; nothing ruled out
- **0-2 (0-1 pass):** Pure bad strategy — buzzword fluff, dog's-dinner objective lists, denial of the real challenge

## Framework

### 1. The Kernel of Good Strategy

**Core concept:** Every good strategy shares the same structure: a **diagnosis** that defines and simplifies the critical challenge, a **guiding policy** — the overall approach chosen to overcome the diagnosed obstacles — and **coherent actions**: coordinated, resource-backed steps that carry out the policy. A document missing any of the three is not yet a strategy.
```

## interactive-planning (3040-interactive-planning)

- الترخيص: **MIT**  ·  الأصل: https://github.com/shihwesley/interactive-planning/tree/2ef3b74/
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3040-interactive-planning/13078-interactive-planning
- الوصف: File-based planning with interactive gates and native task tracking. Use when user says /plan, needs to break a complex feature into phases, or wants structured implementation planning with user approval at key decision points. Supports task mode (single plan file) and spec mode (multi-file architecture).

```markdown
# Interactive Planning (Manus + AskUserQuestion)

Combines **file-based persistence** (Manus-style) with **interactive clarification gates**.

## Core Philosophy

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)
Task Tools = Structured progress (visible, stateful)
AskUserQuestion = User alignment (prevents rework)

→ Tasks for actions (TaskCreate/Update)
→ Files for knowledge (findings.md)
→ Ask users before committing to approaches
```

---

## Phase 0: Session Recovery

**Before anything else**, check for unsynced context:

```bash
python3 ~/.claude/skills/planning-with-files/scripts/session-catchup.py "$(pwd)"
```

If catchup shows unsynced context:
1. `git diff --stat` to see code changes
2. Read existing planning files
3. Update files based on context
4. Then proceed

---

## Phase 1: Interactive Requirements Gathering

### Gate 1: Planning Mode + Priority

Use AskUserQuestion BEFORE creating any files. Two questions:

**Question 1: Planning Mode**
```python
AskUserQuestion(
  question="What kind of planning does this need?",
  header="Mode",
  options=[
    {"label": "Task-based (Recommended)", "description": "Single task_plan.md with phases. Best for straightforward features."},
    {"label": "Spec-driven", "description": "Multiple spec files per concern, manifest index. Best for complex multi-domain work."}
  ]
)
```

If "Task-based" → continue with existing flow (Gates 2-4 unchanged).
If "Spec-driven" → continue with Gates 2, 3 (enhanced), 4 (enhanced) below.

**Question 2: Priority** (asked regardless of mode)
```python
AskUserQuestion(
  question="Which aspect is most important?",
  header="Priority",
  options=[
    {"label": "Speed (Recommended)", "description": "MVP approach, ship fast, iterate later"},
    {"label": "Quality", "description": "Tests, docs, edge cases, production-ready"},
    {"label": "Flexibility", "description": "Extensible, configurable, multiple use cases"},
    {"label": "Simplicity", "description": "Minimal, focused, easy to understand"}
  ]
)
```

### Gate 2: Requirements Validation

```python
AskUserQuestion(
  question="I identified these requirements. Select all that apply:",
  header="Requirements",
  multiSelect=True,
  options=[
    {"label": "[Inferred req 1]", "description": "..."},
    {"label": "[Inferred req 2]", "description": "..."},
    {"label": "[Inferred req 3]", "description": "..."},
    {"label": "Add more", "description": "I'll provide additional requirements"}
  ]
)
```

### Gate 3: Approach Decision (if multiple valid approaches)

```python
AskUserQuestion(
  question="There are a few ways to approach this:",
  header="Approach",
  options=[
    {"label": "Approach A", "description": "Tradeoffs: faster but less flexible"},
```

## brand-strategy (1632-brand-strategy-framework)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/business-tools/brand-strategy-framework
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1632-brand-strategy-framework/4603-brand-strategy
- الوصف: A 7-part brand strategy framework for building comprehensive brand foundations.

```markdown
# Brand Strategy Framework

A systematic 7-part methodology for building brand foundations — the same process top agencies use with Fortune 500 clients.

## Overview

This skill guides users through a comprehensive brand strategy process, from core identity through measurement. Each phase builds on the previous, creating a cohesive strategic foundation.

Walk the user through each phase sequentially. Ask discovery questions, synthesize their answers, and produce structured outputs for each section before moving to the next.

## The 7-Part Framework

### Phase 1: Brand Truth

The foundation. Define who the brand authentically is before anything else.

**Discovery Questions:**

- What problem does this brand exist to solve?
- What would be lost if this brand disappeared tomorrow?
- What does this brand believe that competitors don't?
- What's the origin story? Why was it created?
- What are the non-negotiable values?

**Output:** A Brand Truth statement (2-3 sentences) capturing the brand's reason for being, core belief, and authentic identity.

---

### Phase 2: Audience Architecture

Define who the brand serves — not demographics, but motivations.

**Discovery Questions:**

- Who benefits most from what this brand offers?
- What are they trying to achieve or avoid?
- What do they currently believe about this category?
- What would make them switch from their current solution?
- Who is explicitly NOT the target?

**Output:** 2-4 audience personas, each with:

- Name/archetype
- Core motivation (what they want)
- Current belief (what they think now)
- Tension point (what's holding them back)
- Success state (what winning looks like for them)

---

### Phase 3: Cultural Context

Position the brand within the broader landscape.

**Discovery Questions:**

- What's happening in culture that makes this brand relevant now?
- Who are the real competitors (including non-obvious ones)?
- What category conventions should be challenged?
- What cultural tension does this brand resolve?
- Where is the white space?

**Output:** A positioning statement that captures competitive differentiation and cultural relevance. Include a simple competitive landscape map.

---

### Phase 4: Messaging Framework

Translate strategy into language.

**Discovery Questions:**

- What's the one thing people should remember?
- What proof points support the core claim?
- What objections need to be overcome?
- What emotional territory does the brand own?
- What words should never be used?

**Output:** A messaging framework including:

- Core message (1 sentence)
- Supporting messages (3-5 proof points)
- Tone attributes (3-5 adjectives with definitions)
- Language do's and don'ts

---

### Phase 5: Visual Language

Define the principles (not the executions) for visual identity.
```

## planning-flow (2860-planning-flow)

- الترخيص: **MIT**  ·  الأصل: https://github.com/patrickdappollonio/claude-plugins/tree/2404ff735729a334ad462680a6d7cda7827a7a5f/plugins/planning-flow
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2860-planning-flow/11569-planning-flow
- الوصف: Use when the user asks for a plan for a coding change — "plan this", "how would we build", "write me a plan for", "/planning-flow <ask>" — before any code is written, especially when the change needs research across a codebase, has open questions only the user can answer, or will be handed to an implementation step afterwards. Also use when a user complains that a previous plan read like a change-

```markdown
# Planning Flow

## Overview

Turn a request into **one plan**: the current, complete answer to the user's ask, with the decisions that shaped it and the caveats that remain. The process behind it — parallel exploration, a zero-context review, rounds of questions, spikes, an adversarial review — exists to make the plan right; none of it belongs in the plan or in the message that delivers it.

**Five rules bind everything below:**

1. **The plan never describes its own earlier versions.** Every revision rewrites the file in place so it reads as if written fresh today. The only record of the past is the decisions section, where you record a choice with its alternative and its reason. No "revisited", no "Edit:", no "after the review", no struck text, no revision headings, and no reviewer tally in chat.
2. **The reader has not seen the code.** You read hundreds of lines; the user read none. A function, file, or variable name is a label for a thing you must explain in plain words, never the explanation. Full rules in `communication.md`.
3. **Technical direction is yours, logged; functional and operational direction is the user's, asked.** The authority table below decides which is which, and a decision the user already made is never asked again.
4. **Facts are yours to find; decisions are the user's to make.** Find the facts yourself. Ask the user only what the codebase cannot answer. Ask every question in the one shape in `question-format.md`, and in chat ask one per message, each after the questions it depends on are answered. Never answer a question you put to the user. A change can be so simple that there are no questions; do not invent them.
5. **The plan is a document, and it plans the simplest thing that works.** This skill produces one markdown file and nothing else: no prototype, no mockup, no scaffold, no demo, no code — a spike may run a throwaway probe, deleted before the plan is presented. Inside that file, use everything the viewer can render: Mermaid diagrams, diff and migration fences, API cards, file trees, question fences, a summary card. A picture of the design belongs in the plan; a working copy does not. The solution sits on the lowest rung of the ladder in `plan-template.md` that answers the ask: not needed → cut it; the codebase has it → reuse it; the standard library or platform has it → use it; an installed dependency has it → use it; otherwise the minimum that works. A higher rung is a decisions entry, rejected, with the reason. Never cut: validation at a trust boundary, data-loss handling, security, accessibility.

## Read the Companion Files First

This skill ships in two layers. `SKILL.md` carries the rules and a summary of each step; seven files beside it carry the full procedures:
```
