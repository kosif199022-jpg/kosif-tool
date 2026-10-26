# مصادر «التوثيق التقني وREADME» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## generating-api-docs (1610-api-documentation-generator)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/api-development/api-documentation-generator
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1610-api-documentation-generator/4581-generating-api-docs
- الوصف: Create comprehensive API documentation with examples, authentication

```markdown
# Generating API Documentation

## Overview

Create comprehensive, interactive API documentation from OpenAPI specifications with runnable code examples, authentication guides, error reference tables, and SDK quick-start tutorials. Generate documentation sites using Redoc, Stoplight Elements, or Swagger UI with custom branding, versioned navigation, and full-text search.

## Prerequisites

- OpenAPI 3.0+ specification with descriptions, examples, and complete schema definitions
- Documentation generator: Redoc, Stoplight Elements, Swagger UI, or Docusaurus with OpenAPI plugin
- Code example generator for multiple languages (curl, JavaScript, Python, Go)
- Static site hosting for documentation deployment (GitHub Pages, Netlify, Vercel)
- Custom branding assets (logo, color scheme) for white-labeled documentation

## Instructions

1. Read the OpenAPI specification using Read and audit documentation completeness: verify all operations have `summary`, `description`, parameter descriptions, and at least one example per request/response.
2. Enrich the specification with long-form descriptions using Markdown: add getting-started guides, authentication flow explanations, and rate limiting documentation in the `info.description` or `x-documentation` extensions.
3. Generate interactive documentation using Redoc or Stoplight Elements with "Try It" functionality that allows consumers to execute requests directly from the documentation page.
4. Create runnable code examples for every endpoint in curl, JavaScript (fetch/axios), Python (requests/httpx), and Go (net/http), with proper authentication header injection.
5. Build an authentication guide covering all supported auth schemes: API key setup, OAuth2 authorization code flow walkthrough, JWT token lifecycle, and credential rotation procedures.
6. Add an error reference section that documents every error code, its meaning, common causes, and resolution steps -- organized by HTTP status code with searchable error code index.
7. Configure documentation versioning so consumers can switch between API versions (v1, v2) with visual diff highlighting showing changes between versions.
8. Set up automated documentation deployment: on OpenAPI spec changes, regenerate the documentation site and deploy to hosting with cache invalidation.

See `${CLAUDE_SKILL_DIR}/references/implementation.md` for the full implementation guide.

## Output

- `${CLAUDE_SKILL_DIR}/docs/site/` - Generated documentation website (HTML/CSS/JS)
- `${CLAUDE_SKILL_DIR}/docs/guides/authentication.md` - Authentication flow guide with code examples
- `${CLAUDE_SKILL_DIR}/docs/guides/getting-started.md` - Quick-start tutorial for first API call
- `${CLAUDE_SKILL_DIR}/docs/reference/errors.md` - Complete error code reference with resolution steps
```

## technical-documentation (3429-code-craftsmanship)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wondelai/skills/tree/c172996495bed0fcd26896a9416b2093fd7073f0/plugins/code-craftsmanship
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3429-code-craftsmanship/14066-technical-documentation
- الوصف: Audit, write, and improve developer documentation using Google''s Developer Documentation Style Guide and Technical Writing courses. Use this skill for any documentation work, even when the user names no style guide: "audit our docs", "review this README", "write a README", "getting started guide", "how-to or tutorial", "API reference", "docstrings", "CLI help text", "changelog or release notes", 

```markdown
# Technical Documentation

Audit, write, and improve developer documentation the way Google's technical writers do: start from the reader's task, verify every fact against the code, then apply the style guide in severity order — structure before voice, voice before word choice.

## Core Principle

**Write for the reader's task, not the product's feature list.** Google's guide asks for prose that is conversational but not frivolous, precise, and consistent, because a developer reading docs is trying to get something done, not to admire the product. Two framing rules from the guide shape everything below:

- **Guidelines, not rules.** Depart from the guide when doing so improves the content — established domain terminology wins — but stay consistent within the document.
- **Precedence.** A project's own style guide comes first, then Google's guide, then Merriam-Webster (spelling), the Chicago Manual of Style (general style), and the Microsoft Writing Style Guide (technical style).

Rules come in two layers. Structural and content rules (headings, procedures, code samples, second person, active voice, timeless docs, accessibility) apply to documentation in any language. Rules tagged `[EN]` (spelling, serial comma, contractions, the word list) apply only to English text — skip them for other languages, and never translate a document unless asked.

## Scoring

**Goal: 10/10.** Score = number of Quick Diagnostic rows passed (10 rows, 1 point each; the `[EN]` row auto-passes for non-English docs). Bands: **9-10** = ships as is; **7-8** = word- and voice-level edits only; **5-6** = restructure sections, then re-edit; **≤4** = rewrite from the doc-type skeleton. Blocking findings — wrong or unverifiable facts, a procedure that can't be completed, information that exists only in an image or in an image without alt text — are a separate gate: the doc is **not shippable** at any score until they're fixed. Report the score, the failed rows, and the exact edits that reach 10/10.

## Framework

### 1. Know the Reader and the Document's Job

**Core concept:** Every page serves one reader with one task. Name both before writing a word — audience and level, what they'll be able to do afterwards — and pick the document type that fits: tutorial (learn by doing), how-to (accomplish a task), concept (understand), reference (look up), README (orient and start).

**Why it works:** Readers scan for their task; a page that mixes concept, procedure, and reference forces them to read everything to find anything.

**Key insights:**
- Google's Technical Writing course opens a doc with an audience statement and a scope plus non-scope statement — the non-scope rescues readers who are on the wrong page
```

## docs-create-workflow (60-codebase-mapper)

- الترخيص: **MIT**  ·  الأصل: https://github.com/acaprino/daodan/tree/39443d215d28fcbc32d651895b3cc45c64f24b6f/exports/codex/plugins/codebase-mapper
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/60-codebase-mapper/94-docs-create-workflow
- الوصف: Documents a project from its source, on one dimension or many. TRIGGER WHEN: the user asks to create technical documentation, API docs, architecture guides, data model / schema docs, data flow / pipeline docs, dependency maps, or any new documentation for a codebase. DO NOT TRIGGER WHEN: the user wants to audit existing docs (use /codebase-mapper:docs-maintain) or just a README (use /docs:maintain

```markdown
> `<plugin-root>` names the directory that holds this plugin's `.codex-plugin/plugin.json`. Resolve it once from where this file was loaded, then substitute it into every path below that starts with it.
> Arguments: `<target path or description> [--interfaces] [--config] [--integrations] [--architecture] [--data-model] [--data-flows] [--state-machines] [--dependencies] [--concurrency] [--glossary] [--auth] [--errors] [--observability] [--deployment] [--testing] [--build-release] [--migrations] [--performance] [--compliance] [--component] [--full] [--scope <dim1,dim2,...>] [--format markdown|html] [--output <path>] [--audience technical|general|mixed]`. Wherever `<arguments>` appears below, substitute the text the user typed after the skill name.


# Create Documentation

## CRITICAL RULES

1. **Analyze code before writing.** Read the actual source code first. Never write documentation based on assumptions.
2. **Bottom-up approach.** Start from code structure, then build documentation that reflects reality.
3. **Confirm scope with user.** Present what will be documented before generating.
4. **Never enter plan mode.** Execute immediately.

## Step 1: Analyze Target

Determine what to document from `<arguments>`:

- If a file/directory path: scan the code structure
- If a class/module name: find it in the codebase
- If no target: scan the entire project

```bash
# Discover project structure
find [target] -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.rs" -o -name "*.go" -o -name "*.java" \) | head -50
```

Identify:
- **Language & framework** (from package.json, Cargo.toml, pyproject.toml, etc.)
- **Key modules** (entry points, API routes, core business logic)
- **Existing docs** (README, docstrings, JSDoc, rustdoc, etc.)
- **Public API surface** (exports, endpoints, CLI commands)

## Step 2: Confirm Documentation Plan

Present the plan and ask for approval. The documentation dimensions are grouped into 5 fasce. The user can pick one dimension, several (combined into a single artifact with sections), an entire fascia, or `--full` for everything.

```
Documentation plan for: [target]

Language: [detected]
Framework: [detected]

Files to document:
- [file1] -- [type: API endpoint / class / module / ORM model / config / etc.]
- [file2] -- [type]
- ...

Documentation dimensions (pick one or more; can also pick a whole fascia):

SURFACE (what the system exposes)
- [ ] interfaces       -- HTTP/REST, gRPC, GraphQL, WebSocket, CLI, library exports, events emitted (Kafka topics, RabbitMQ exchanges, webhooks emitted)
- [ ] config           -- env vars, config files, feature flags, secrets references, runtime profiles
- [ ] integrations     -- webhooks consumed, third-party APIs called, message queues, scheduled jobs/cron
```

## documentation (319-engineering)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/anthropics/knowledge-work-plugins/tree/8444efcd48f7012f09797778a36a33e73d0861f4/engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/319-engineering/959-documentation
- الوصف: Write and maintain technical documentation. Trigger with "write docs for", "document this", "create a README", "write a runbook", "onboarding guide", or when the user needs help with any form of technical writing — API docs, architecture docs, or operational runbooks.

```markdown
# Technical Documentation

Write clear, maintainable technical documentation for different audiences and purposes.

## Document Types

### README
- What this is and why it exists
- Quick start (< 5 minutes to first success)
- Configuration and usage
- Contributing guide

### API Documentation
- Endpoint reference with request/response examples
- Authentication and error codes
- Rate limits and pagination
- SDK examples

### Runbook
- When to use this runbook
- Prerequisites and access needed
- Step-by-step procedure
- Rollback steps
- Escalation path

### Architecture Doc
- Context and goals
- High-level design with diagrams
- Key decisions and trade-offs
- Data flow and integration points

### Onboarding Guide
- Environment setup
- Key systems and how they connect
- Common tasks with walkthroughs
- Who to ask for what

## Principles

1. **Write for the reader** — Who is reading this and what do they need?
2. **Start with the most useful information** — Don't bury the lede
3. **Show, don't tell** — Code examples, commands, screenshots
4. **Keep it current** — Outdated docs are worse than no docs
5. **Link, don't duplicate** — Reference other docs instead of copying
```

## diataxis-documentation (2395-technical-writing-docs)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/technical-writing-docs
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2395-technical-writing-docs/9273-diataxis-documentation
- الوصف: Apply the Diataxis framework: identify which of the four documentation kinds you're writing (tutorial/how-to/reference/explanation), keep them separate, and organize the whole docs set around the reader's journey rather than the system's structure.

```markdown
# Diataxis Documentation

## The four kinds (don't mix them)
| Kind | Serves | Oriented to |
|---|---|---|
| **Tutorial** | learning | the newcomer, hand-held |
| **How-to guide** | a task | the practitioner with a goal |
| **Reference** | information | the one who needs facts |
| **Explanation** | understanding | the one asking 'why' |

Most bad docs blur all four. Separating them is the biggest single improvement.

## Organize by the reader
Map audiences + journeys (newcomer / integrator / operator); structure around what they're doing, **not** your module tree.
```

## readme-craft (26-docs)

- الترخيص: **MIT**  ·  الأصل: https://github.com/acaprino/daodan/tree/39443d215d28fcbc32d651895b3cc45c64f24b6f/exports/claude/plugins/docs
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/26-docs/36-readme-craft
- الوصف: Author the front door of an open-source repository: detect stack and structure, gather missing metadata, then write the file. TRIGGER WHEN: the user asks to write, create, draft, or scaffold a README.md for a project (English or Italian phrasing: "readme", "write a readme", "create readme", "scrivi il readme", "crea il readme"). DO NOT TRIGGER WHEN: auditing an existing README (use /docs:maintain-

```markdown
# README Craft

You are a world-class open-source README writer. Your goal is to produce a magnetic, adoption-driving README.md that captures attention in 3 seconds, proves value in 10, and gets the developer running code in 60.

**CRITICAL: Execute ALL steps yourself in this conversation. Do NOT spawn agents or delegate to subagents.**

---

## Psychology Principles

Weave these into every section you write:

1. **3-Second Hook** -- Developers scan before they read. Wall of text = bounce. Clean centered logo, punchy one-liner, colorful badges.
2. **Time-To-Value (TTV)** -- Quick Start must be frictionless. Copy-pasteable commands, no 5-paragraph prerequisites.
3. **Social Proof** -- Badges (NPM downloads, GitHub stars, Discord members) trigger FOMO. Real user quotes build trust.
4. **Zero-BS Vibe** -- Developer-to-developer tone. Acknowledge pain points directly ("Configuring webpack sucks. We fixed it.").

---

## BEFORE ANYTHING ELSE: Project Context Scan

**YOUR VERY FIRST ACTION must be scanning the project. Do NOT output ANY text before completing this scan.** No greetings, no questionnaire. SCAN FIRST, TALK SECOND.

### Scan procedure (execute silently before any output):

1. **Read project files** using Read/Glob/Grep:
   - README.md (existing, if any), CLAUDE.md, package.json, pyproject.toml, Cargo.toml, setup.py, go.mod
   - LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, CHANGELOG.md
   - docs/ directory, .github/ directory (workflows, templates)
   - Source entry points (src/index.*, src/main.*, lib/*, app/*)
   - Any existing badges, logo files, screenshots, GIFs in assets/ or docs/
   - CI/CD config (.github/workflows/, .gitlab-ci.yml, Dockerfile)

2. **Extract what you can**:
   - Project name, description, version
   - Tech stack and language(s)
   - Install commands (from package manager configs)
   - CLI commands or API surface (from help output, argparse, commander, clap)
   - License type
   - Author/organization
   - Existing badges or shields
   - Architecture patterns (monorepo, microservices, CLI tool, library, web app)
   - Key features (from code, docs, or existing README)

3. **Present a pre-filled brief** showing what you inferred:

   > **Inferred project profile** (confirm or adjust):
   > - **Name:** [from manifest]
   > - **One-liner:** [inferred from description/code]
   > - **Tech stack:** [detected]
   > - **Type:** [CLI / library / web app / API / framework / ...]
   > - **License:** [from LICENSE file or manifest]
   > - **Author/Org:** [from manifest or git config]
   > - **Version:** [from manifest]
   > - **Install command:** [inferred from package manager]
   > - **Key features:** [bullet list, inferred from code]
   > - **Logo:** [found / not found -- path if found]
```
