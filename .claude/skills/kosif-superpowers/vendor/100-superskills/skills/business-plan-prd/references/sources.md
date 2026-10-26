# مصادر «خطة العمل ووثيقة المنتج» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## prd-roadmap (2973-pwdev-prd)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/pwdev-solucoes/pwdev-claude-marketplace/tree/c7b210504bd3a6b5ff32636c999fc6a2ccc5c44a/plugins/pwdev-prd
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2973-pwdev-prd/12545-prd-roadmap
- الوصف: Use when an approved PRD must become an executable roadmap — 'gerar roadmap do PRD', 'quebrar o PRD em épicos e features', 'cadeia de dependências', 'roadmap with dependencies' — Phase/Epic/Feature/Task with explicit dependencies, waves and critical path, validated by a deterministic checker, with an approval gate. Do NOT use for a PRD that is not approved (prd- create/prd-refine first).

```markdown
# PRD roadmap with dependencies

## Method
You run in the MAIN session as the orchestrator: you validate, dispatch the roadmap
writer, run the deterministic checker, and hold the approval gate. When the runtime has a
subagent mechanism you never write the roadmap files yourself — the writer does, and on change
requests you re-dispatch it. Without one, follow `references/roadmap-agent.md` inline (see
`references/runtime.md`), then continue from STEP 5 exactly the same way.
Format contract: `<plugin-root>/references/roadmap-format.md`.

## Input
the arguments: PRD slug (required).

## Flow

### STEP 0 — Language
Follow `<plugin-root>/references/language.md` (resolve `lang` from
`.planning/config.json`; ask only if unset).

### STEP 1 — Load and gate the PRD

```bash
SLUG="<slug>"   # first word of the arguments
PRD=".planning/prds/$SLUG/PRD.md"
[ -f "$PRD" ] && grep -m1 -E '^Status:' "$PRD" || { echo "PRD_NOT_FOUND"; ls .planning/prds/ 2>/dev/null; }
```

- `PRD_NOT_FOUND` → show the available slugs and STOP.
- `Status:` is not `APPROVED` (or missing, in PRDs made before v2.1) → read the PRD, show a
  3-line summary, and ask: `Approve PRD "{slug}" so the roadmap can be generated? (y/n)`.
  On yes, set `Status: APPROVED` in the header and log
  `sh "<plugin-root>/scripts/audit-log.sh" event roadmap "" approved "$PRD" "prd gate"`.
  On no, STOP and point to `/pwdev-prd:refine {slug}`.

### STEP 2 — Readiness check
Read the PRD. Check it has: objectives with metric and target, functional requirements with
`FR-xx` IDs, acceptance criteria, and in/out of scope. If any is missing, name it. If **three
or more** are missing, STOP: the roadmap would be fiction — send the user to
`/pwdev-prd:refine {slug}`. If FRs lack IDs but everything else is there, ask to number them
(`FR-01`…) in the PRD first; traceability depends on it. A PRD without a
`### Business Rules` section (written before v3.0) is not blocking: say that the stories will
carry no RN until `prd-refine` adds them.

### STEP 3 — Existing roadmap
If `.planning/prds/{slug}/roadmap/roadmap.json` exists, ask:
```
A roadmap already exists for "{slug}".
1. Regenerate from the current PRD (replaces it)
2. Revise it with specific changes
3. Keep it and stop
```

### STEP 4 — Dispatch the roadmap writer
Dispatch it per `references/runtime.md` (Claude `subagent_type: "pwdev-prd:roadmap"`, Codex
`spawn_agent`, Hermes `delegate_task`, OpenCode `task`, or inline) with this dispatch block,
and nothing it has to ask back:

```
PRD: .planning/prds/{slug}/PRD.md
Roadmap dir: .planning/prds/{slug}/roadmap/
Contract: <plugin-root>/references/roadmap-agent.md
Format reference: <plugin-root>/references/roadmap-format.md
Checker: python3 "<plugin-root>/scripts/roadmap-check.py" .planning/prds/{slug}/roadmap/roadmap.json
```

## prd-stories (2973-pwdev-prd)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/pwdev-solucoes/pwdev-claude-marketplace/tree/c7b210504bd3a6b5ff32636c999fc6a2ccc5c44a/plugins/pwdev-prd
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2973-pwdev-prd/12546-prd-stories
- الوصف: Use when the user wants to evolve the features of a PRD roadmap with user stories — 'refinar as histórias da feature', 'escrever histórias de usuário', 'critérios de aceite', 'regras de negócio da feature', 'deixar a feature pronta', 'user stories for FT01' — one feature at a time, interviewing the human until each story meets the Definition of Ready: persona, value, INVEST, CA (Gherkin, happy and

```markdown
# Evolve features with user stories, CA and RN

You interview the human in the MAIN session, one question at a time — never in a subagent.
Quality bar: `<plugin-root>/references/user-stories.md` (format, INVEST, CA, RN, Definition of
Ready, anti-patterns, review checklist). Read it before the first question.

## Input
The arguments: `<slug>` (required) and optionally a feature ID (`F01-E02-FT01`) or `next`.

## Flow

### STEP 0 — Language
Follow `references/language.md` (resolve `lang` from `.planning/config.json`; ask only if unset).

### STEP 1 — Load

```bash
SLUG="<slug>"   # first word of the arguments
DIR=".planning/prds/$SLUG/roadmap"
[ -f "$DIR/roadmap.json" ] || { echo "NO_ROADMAP"; ls .planning/prds/ 2>/dev/null; }
python3 "<plugin-root>/scripts/roadmap-check.py" "$DIR/roadmap.json" --json
```

- `NO_ROADMAP` → point to `prd-roadmap {slug}` and STOP.
- Checker `FAIL` for reasons unrelated to stories → show them and STOP (the roadmap needs
  `prd-roadmap` revise mode first).
- Read `.planning/prds/{slug}/PRD.md` for personas (Target Audience), FRs and the
  `### Business Rules` section, and `roadmap.json` for features, `rules[]` and `stories[]`.

### STEP 2 — Pick the feature
Without a feature in the arguments, show the progress table and ask which one:

```
📚 Stories of "{slug}" — {ready}/{total} ready · {rules} business rules
| Wave | Feature | Stories | Ready | Missing |
| 1 | F01-E01-FT01 Login | 1 | 0 | CA error path, RN-01 not verified |
...
Suggested next: {first feature in wave order with draft stories}
```

`next` means that suggestion. Refine **one feature per pass**.

### STEP 3 — Review the feature's stories
For each story of the feature, run the review checklist and INVEST from `user-stories.md` and
show a compact diagnosis (story line, CA with paths, RN, what fails). Then fix it with the
human, **one question at a time**, offering 2–3 concrete options when they hesitate:

1. **Persona** — must be named in the PRD audience; never "o sistema".
2. **Split or merge** — a story-epic becomes one story per capability; a feature ends with
   1–5 stories.
3. **Value** — non-circular.
4. **CA** — happy path first, then at least one error or edge path; Gherkin when there is
   state + trigger + observable result; numbers instead of "rápido/fácil"; 3–8 per story.
5. **RN** — ask which business rules decide this behavior. Use existing `RN-xx` from the PRD.
   A new rule discovered here: agree name, one-sentence rule and a concrete example, then it
   goes to the PRD (STEP 5) with the next free ID — never kept only inside the story. Each RN
   listed by the story is verified by at least one CA (`"rules": ["RN-xx"]` on that CA).
6. **Dependencies and out of scope** — `depends_on` other `US-xx`; out-of-scope when the title
```

## code-to-prd (201-code-to-prd)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/product-team/code-to-prd
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/201-code-to-prd/647-code-to-prd
- الوصف: Reverse-engineer any codebase into a complete Product Requirements Document (PRD). Analyzes routes, components, state management, API integrations, and user interactions to produce business-readable documentation detailed enough for engineers or AI agents to fully reconstruct every page and endpoint. Works with frontend frameworks (React, Vue, Angular, Svelte, Next.js, Nuxt), backend frameworks (N

```markdown
## Name

Code → PRD

## Description

Reverse-engineer any frontend, backend, or fullstack codebase into a complete Product Requirements Document (PRD). Analyzes routes, components, models, APIs, and user interactions to produce business-readable documentation detailed enough for engineers or AI agents to fully reconstruct every page and endpoint.

# Code → PRD: Reverse-Engineer Any Codebase into Product Requirements

## Features

- **3-phase workflow**: global scan → page-by-page analysis → structured document generation
- **Frontend support**: React, Vue, Angular, Svelte, Next.js (App + Pages Router), Nuxt, SvelteKit, Remix
- **Backend support**: NestJS, Express, Django, Django REST Framework, FastAPI, Flask
- **Fullstack support**: Combined frontend + backend analysis with unified PRD output
- **Mock detection**: Automatically distinguishes real API integrations from mock/fixture data
- **Enum extraction**: Exhaustively lists all status codes, type mappings, and constants
- **Model extraction**: Parses Django models, NestJS entities, Pydantic schemas
- **Automation scripts**: `codebase_analyzer.py` for scanning, `prd_scaffolder.py` for directory generation
- **Quality checklist**: Validation checklist for completeness, accuracy, readability

## Usage

```bash
# Analyze a project and generate PRD skeleton
python3 scripts/codebase_analyzer.py /path/to/project -o analysis.json
python3 scripts/prd_scaffolder.py analysis.json -o prd/ -n "My App"

# Or use the slash command
/code-to-prd /path/to/project
```

## Examples

### Frontend (React)
```bash
/code-to-prd ./src
# → Scans components, routes, API calls, state management
# → Generates prd/ with per-page docs, enum dictionary, API inventory
```

### Backend (Django)
```bash
/code-to-prd ./myproject
# → Detects Django via manage.py, scans urls.py, views.py, models.py
# → Documents endpoints, model schemas, admin config, permissions
```

### Fullstack (Next.js)
```bash
/code-to-prd .
# → Analyzes both app/ pages and api/ routes
# → Generates unified PRD covering UI pages and API endpoints
```

---

## Role

You are a senior product analyst and technical architect. Your job is to read a frontend codebase, understand every page's business purpose, and produce a complete PRD in **product-manager-friendly language**.

### Dual Audience

1. **Product managers / business stakeholders** — need to understand *what* the system does, not *how*
2. **Engineers / AI agents** — need enough detail to **fully reconstruct** every page's fields, interactions, and relationships

Your document must describe functionality in non-technical language while omitting zero business details.

### Supported Stacks

| Stack | Frameworks |
|-------|-----------|
```

## create-prd (2878-pm-execution)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-execution
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2878-pm-execution/11606-create-prd
- الوصف: Create a Product Requirements Document using a comprehensive 8-section template covering problem, objectives, segments, value propositions, solution, and release planning. Use when writing a PRD, documenting product requirements, preparing a feature spec, or reviewing an existing PRD.

```markdown
# Create a Product Requirements Document

## Purpose

You are an experienced product manager responsible for creating a comprehensive Product Requirements Document (PRD) for $ARGUMENTS. This document will serve as the authoritative specification for your product or feature, aligning stakeholders and guiding development.

## Context

A well-structured PRD clearly communicates the what, why, and how of your product initiative. This skill uses an 8-section template proven to communicate product vision effectively to engineers, designers, leadership, and stakeholders.

## Instructions

1. **Gather Information**: If the user provides files, read them carefully. If they mention research, URLs, or customer data, use web search to gather additional context and market insights.

2. **Think Step by Step**: Before writing, analyze:
   - What problem are we solving?
   - Who are we solving it for?
   - How will we measure success?
   - What are our constraints and assumptions?

3. **Apply the PRD Template**: Create a document with these 8 sections:

   **1. Summary** (2-3 sentences)
   - What is this document about?

   **2. Contacts**
   - Name, role, and comment for key stakeholders

   **3. Background**
   - Context: What is this initiative about?
   - Why now? Has something changed?
   - Is this something that just recently became possible?

   **4. Objective**
   - What's the objective? Why does it matter?
   - How will it benefit the company and customers?
   - How does it align with vision and strategy?
   - Key Results: How will you measure success? (Use SMART OKR format)

   **5. Market Segment(s)**
   - For whom are we building this?
   - What constraints exist?
   - Note: Markets are defined by people's problems/jobs, not demographics

   **6. Value Proposition(s)**
   - What customer jobs/needs are we addressing?
   - What will customers gain?
   - Which pains will they avoid?
   - Which problems do we solve better than competitors?
   - Consider the Value Curve framework

   **7. Solution**
   - 7.1 UX/Prototypes (wireframes, user flows)
   - 7.2 Key Features (detailed feature descriptions)
   - 7.3 Technology (optional, only if relevant)
   - 7.4 Assumptions (what we believe but haven't proven)

   **8. Release**
   - How long could it take?
   - What goes in the first version vs. future versions?
   - Avoid exact dates; use relative timeframes

4. **Use Accessible Language**: Write for a primary school graduate. Avoid jargon. Use clear, short sentences.

5. **Structure Output**: Present the PRD as a well-formatted markdown document with clear headings and sections.

6. **Save the Output**: If the PRD is substantial (which it will be), save it as a markdown document in the format: `PRD-[product-name].md`

## Notes
```

## market-segments (2880-pm-market-research)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-market-research
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2880-pm-market-research/11629-market-segments
- الوصف: Identify 3-5 potential customer segments with demographics, JTBD, and product fit analysis. Use when exploring market segments, identifying target audiences, evaluating new markets, or learning how to segment a market.

```markdown
# Market Segments

## Purpose
Identify and analyze 3-5 distinct customer segments for your product, understanding their unique jobs-to-be-done, desired outcomes, pain points, and product fit. Use this skill to evaluate market opportunities, prioritize target audiences, or expand into new market segments.

## Instructions

You are a strategic market research expert skilled in market segmentation, customer profiling, and total addressable market (TAM) analysis.

### Input
Your task is to identify and analyze potential customer segments for **$ARGUMENTS**.

If research data, market studies, customer databases, or existing segmentation documents are provided, read and analyze them directly. Look for behavioral patterns, demographic clusters, and distinct needs across segments.

### Analysis Steps (Think Step by Step)

1. **Market Exploration**: Consider the full addressable market for $ARGUMENTS
2. **Segmentation Criteria**: Identify logical segmentation dimensions (behavioral, demographic, firmographic, needs-based)
3. **Segment Definition**: Create 3-5 distinct, non-overlapping customer segments
4. **Characterization**: For each segment, synthesize profiles and validate distinctness
5. **Opportunity Assessment**: Evaluate market size, growth potential, and competitive intensity per segment

### Output Structure

For each of the 3-5 segments, provide:

**Segment Name & Overview**
- Clear, memorable segment identifier
- Size estimate (% of total market or absolute numbers if data available)
- Growth trajectory and market dynamics

**Key Demographics & Firmographics**
- Core characteristics (age, role, company size, industry, geography, etc.)
- Decision-maker profiles if B2B

**Jobs-to-be-Done**
- Primary job and desired outcome for this segment
- Frequency, context, and stakes of the job
- Success criteria and desired outcomes

**Key Pain Points & Obstacles**
- Barriers to job completion specific to this segment
- Consequences of not solving the problem

**Desired Gains & Success Factors**
- What outcomes matter most to this segment
- Preferred solution characteristics
- Cost and time constraints

**Product Fit Analysis**
- How well $ARGUMENTS serves this segment's needs
- Unique value proposition for this segment
- Potential adoption barriers or resistance

**Competitive Landscape**
- Existing solutions or workarounds this segment uses
- Alternative approaches or competitors

## Best Practices

- Ensure segments are measurable, accessible, and distinct
- Prioritize segments with clear jobs-to-be-done and pain points
- Validate segment assumptions with available data
- Consider both greenfield opportunities and underserved segments
- Flag segments requiring additional market research

---

### Further Reading
```

## market-sizing (2880-pm-market-research)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-market-research
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2880-pm-market-research/11630-market-sizing
- الوصف: Estimate market size using TAM, SAM, and SOM with top-down and bottom-up approaches. Use when sizing a market opportunity, estimating addressable market, preparing for investor pitches, or evaluating market entry.

```markdown
# Estimate Market Size (TAM, SAM, SOM)

## Purpose
Estimate the Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM) for a product. Includes both top-down and bottom-up estimation approaches, growth projections, and key assumptions to validate.

## Instructions

You are a strategic market analyst specializing in market sizing, opportunity assessment, and growth forecasting.

### Input
Your task is to estimate the market size for **$ARGUMENTS** within the specified market constraints (geography, industry vertical, customer type, etc.).

If the user provides market research, industry reports, financial data, or competitor information, read and analyze them directly. Use web search to find current market data, industry reports, and growth projections.

### Analysis Steps (Think Step by Step)

1. **Market Definition**: Define the market boundaries — what problem space, which customer segments, what geography or constraints apply
2. **Top-Down Estimation**: Start from total industry size and narrow to the relevant slice
3. **Bottom-Up Estimation**: Build from unit economics (customers × price × frequency) to cross-validate
4. **SAM Scoping**: Identify which portion of TAM is realistically serviceable given product capabilities, channels, and constraints
5. **SOM Estimation**: Estimate achievable share in the next 1-3 years based on competitive position and go-to-market capacity
6. **Growth Projection**: Forecast how TAM, SAM, and SOM may evolve over the next 2-3 years
7. **Assumption Mapping**: Surface the key assumptions underlying each estimate

### Output Structure

**Market Definition**
- Problem space and customer need
- Geographic and segment boundaries
- Key constraints or scoping decisions

**TAM (Total Addressable Market)**
- Top-down estimate with sources and reasoning
- Bottom-up estimate for cross-validation
- Reconciliation of the two approaches
- Current TAM value (annual revenue opportunity)

**SAM (Serviceable Addressable Market)**
- Which portion of TAM the product can realistically serve
- Constraints: geography, language, channels, product capabilities, pricing tier
- SAM as percentage of TAM with reasoning

**SOM (Serviceable Obtainable Market)**
- Realistic share achievable in 1-3 years
- Basis: competitive position, go-to-market capacity, current traction
- SOM as percentage of SAM with reasoning

**Market Summary Table**

| Metric | Current Estimate | 2-3 Year Projection |
|--------|-----------------|---------------------|
| TAM    |                 |                     |
| SAM    |                 |                     |
| SOM    |                 |                     |

**Growth Drivers & Trends**
- Key factors that could expand or contract the market
```
