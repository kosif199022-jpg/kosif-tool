# مصادر «مستندات وورد الاحترافية» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## infer-office (2370-report-regeneration)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/report-regeneration
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2370-report-regeneration/9158-infer-office
- الوصف: Stage 1 of the report-regeneration OFFICE (docx) pipeline. Parses a Word .docx template into a schema-valid Report Structure Graph (RSG) via stdlib zipfile + xml.etree over word/document.xml: per-node OOXML body-walk anchor, role, rebind class, confidence, provenance, plus the deterministic data-shaped-literal detector reused from the HTML lane. Stdlib-only, Python 3.9; python-docx optional.

```markdown
# infer-office

The **first stage** of the `report-regeneration` **Office (Word/`.docx`)** pipeline — the exact
analogue of [`infer-report-structure`](../infer-report-structure/SKILL.md) for OOXML. It reads a
Word `.docx` **template** and emits a **Report Structure Graph (RSG)** — the same format-neutral
ordered tree, node taxonomy, and deterministic detector as the HTML lane, but keyed on **OOXML
anchors** instead of CSS selectors. The RSG is an **addressing-and-verification structure, NEVER a
generator** (`knowledge/core-architecture-spec.md` §2).

## How it parses (stdlib-first)

`infer_office.py` opens the `.docx` (an OPC/ZIP package) with **`zipfile`**, reads
`word/document.xml`, and walks `w:body` in **document order** (order is load-bearing — the V2
frozen-complement diff and V3 re-inference isomorphism both depend on it) with **`xml.etree`**. It
emits one RSG node per content element: paragraphs (`w:p`), runs (`w:r`), tables
(`w:tbl`/`w:tr`/`w:tc`), and inline images (`w:drawing`). Non-content property elements
(`w:pPr`/`w:rPr`/`w:sectPr`/…) are not emitted as nodes but are still counted in anchor indices.

`python-docx` is **optional acceleration** via a graceful `try`/import that changes nothing when
absent (the stdlib `zipfile` + `xml.etree` walk is the sole code path). No network, no live LLM call.

## The OOXML anchor grammar (owned by the shared resolver)

Every anchor is `kind:"ooxml_path"` (the only Office kind the RSG schema admits) and is **produced
by — and resolves back through — the shared grammar in [`scripts/rr_anchor.py`](../../scripts/rr_anchor.py)**,
which OWNS the Office anchor contract. Two forms, both pinned in `core-architecture-spec.md` §2:

| Anchor | When | Example |
|---|---|---|
| `body`-rooted body-walk path | the default for any node | `body/p[3]/r[1]`, `body/tbl[1]/tr[2]/tc[2]/p[1]/r[1]` |
| `bookmark(NAME)` path | a `w:bookmarkStart` governs the node (the surgical-KPI archetype) | `bookmark(revenue_total)` |

A `step` is `local[n]` — a **namespace-stripped** local name plus a **1-based index among
same-local-name element siblings, document order**. Because indices bucket by local name, property
elements never perturb a run's or paragraph's index. Both the producer (this skill, over `xml.etree`
children) and the resolver (`rr_anchor`, over `expat` children) apply the **one** shared indexing
rule (`rr_anchor.ooxml_sibling_index`), and a cross-check test locks their agreement in both
directions — so producer/consumer anchor grammar cannot drift. `rebind-office` and the Office
fidelity-harness extension build on this contract next wave.

## The load-bearing detector — reused verbatim

The `data_shaped_literal` field is the output of **the same** deterministic, non-inference detector
```

## infer-report-structure (2370-report-regeneration)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/report-regeneration
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2370-report-regeneration/9159-infer-report-structure
- الوصف: Stage 1 of the report-regeneration HTML pipeline. Parses an HTML template into a schema-valid Report Structure Graph (RSG): per-node stable anchor, role, rebind class, confidence, provenance, plus the deterministic non-inference data-shaped-literal detector that drives the earned-frozen rule. Stdlib-only, runs on Python 3.9.

```markdown
# infer-report-structure

The **first stage** of the `report-regeneration` HTML pipeline. It reads an HTML report
**template** and emits a **Report Structure Graph (RSG)** — a format-neutral ordered tree that
downstream stages (binding-manifest generation, surgical rebind, the fidelity harness) address
and verify against. The RSG is an **addressing-and-verification structure, NEVER a generator**
(`knowledge/core-architecture-spec.md` §2).

## What it produces

`infer.py` walks the template in **document order** (order is load-bearing — the V2 frozen-
complement diff and V3 re-inference isomorphism both depend on it) and emits one RSG node per
element. Each node validates against [`knowledge/rsg.schema.json`](../../knowledge/rsg.schema.json)
and carries:

| Field | Source |
|---|---|
| `anchor` | a **stable node identity** — `element_id` when the element has an `id`, else a `css_selector` built from `nth-of-type` steps anchored at the nearest id-bearing ancestor. **Never a raw char-offset** (RT1-F10). |
| `role` | rule-based semantic role (`kpi-value`/`table-cell`/`narrative`/`chart`/`image`/`period-label`/`heading`/`metadata`/`static-chrome`/`unknown`). |
| `class` | rebind class (`frozen`/`surgical`/`regenerate`/`needs-review`). |
| `confidence` | 0–1; sub-threshold ⇒ `needs-review`. |
| `provenance` | `method` (`native-parse`/`rule-based`/`llm-labeled`), `source`, **`source_period`**, and `pbi_route` (`xmla`/`rest`/`screenshot`/null) for Power-BI-sourced nodes. |
| `data_shaped_literal` | output of the pinned, **non-inference, deterministic** detector. |

## The load-bearing detector — `data_shaped_literal`

`detect_data_shaped_literal(text)` flags **currency / number / date / percent / unit /
known-entity** shapes deterministically. It is intentionally blind to meaning: it **cannot** tell
`100%` the marketing tagline from `100%` the KPI, or `Fiscal Year 2024` the static citation from a
data-bound period — and it must not try. That is exactly why it is the right tool for the
**earned-frozen** rule (§4): **any data-shaped literal in a candidate-`frozen` node force-demotes
it to `needs-review`, regardless of classifier confidence.** It is independent of the LLM-accuracy
ceiling.

## The two SPEC hard rules (override any annotation or confidence)

1. **Construction rule (§4/§6.4)** — a node that renders as a **raster** or carries an
   **embedded binary/data cache** is FORCED to `regenerate` (a transplanted binary cannot be
   proven data-free). This holds even when the fixture annotates the image `data-role="frozen"`
   (e.g. the header logo, the Power BI screenshot).
2. **Earned-frozen rule (§4)** — a data-shaped literal in a candidate-`frozen` node FORCE-DEMOTES
   it to `needs-review`.
```

## publish-report-board (1024-publish-report-board)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/plugins/publish-report-board
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1024-publish-report-board/2307-publish-report-board
- الوصف: Publish a recurring analysis, such as backlog triage, as a report board with a stable URL. Use for "publish a report board" or "refresh the board".

```markdown
# Publish Report Board

Publish an analysis as a report board, and re-sync it in place when its source data changes.

A report board is an analysis with three properties that terminal output serves badly: it is re-run against source data that keeps changing, it is scanned for what to do next rather than read top to bottom, and it stays open as a working surface. Each board type is a fixed page template plus a reference describing the data it needs and how to derive it.

**A board renders the source of truth and never becomes one.** GitHub, or whatever else a board reads, stays authoritative, and every sync re-derives the board from it. The page holds nothing a later sync would contradict: no checkboxes, no editable status, no runtime state, and no page that saves its own versions, which would also conflict with every republish.

## Board Types

| Board type       | Answers                                                           | Reference                                    |
| ---------------- | ----------------------------------------------------------------- | -------------------------------------------- |
| `backlog-triage` | What to start next, what can run in parallel, and what is blocked | `./references/board-types/backlog-triage.md` |

Only `backlog-triage` ships a template. When the user wants a board for another kind of analysis, such as CI health or release readiness, say that no template exists for it yet and deliver the analysis in the terminal. Do not improvise a page outside the templates: boards read as one system because they share one design, described in `./references/design-conventions.md`.

## Workflow

### 1. Decide Whether a Board Is Warranted

Read `./references/choosing-a-board.md`. A one-time answer belongs in the terminal; say so in one sentence and answer there.

### 2. Locate the Script

The `report-board` script ships with this plugin. It validates board data, renders it into the template, reads it back out of a published page, and compares two syncs. Invoke it via `bash` followed by the quoted path:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/report-board"
```

Claude Code replaces the plugin-root placeholder with the installed plugin's absolute, version-correct directory before this file reaches you, so there is no search step and no need for a shell variable. Keeping `bash` as the command prefix keeps the command token stable across plugin versions, which is what permission allowlist rules match on.
```

## dev-report (1074-dev-report)

- الترخيص: **MIT**  ·  الأصل: https://github.com/ccplugins/awesome-claude-code-plugins/tree/5bd4f168edf7c18a8303cbfde20708ff62aabc4d/plugins/dev-report
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1074-dev-report/2383-dev-report
- الوصف: Write up a coding session for a non-technical stakeholder — the context, what was built, and the engineering reasoning behind it — the way a senior engineer briefs a product manager who does not read code. Use ONLY when explicitly invoked, either through the /dev-report slash command or one of its localized aliases (/개발보고 and similar), or when the user directly asks for a stakeholder-facing write-

```markdown
# Dev Report

Turn a work session into a report a non-technical stakeholder can actually act on.

## Invocation

This skill is explicit-only. It runs when the user calls `/dev-report`, a localized alias of it, or asks in plain words for a stakeholder-facing write-up. A casual "what did you just do?" is not an invocation — answer that normally.

Anything the user types after the command is a **scope or focus hint**: `/dev-report this week`, `/dev-report just the auth work`, `/dev-report 짧게`. With no hint, report on the current conversation session. Honor a length or emphasis hint over this skill's defaults — they know their reader.

## Who you are writing for

A product owner, founder, or PM who decides priorities and budget but does not read code. Increasingly they *did* prompt this code into existence themselves ("vibe coding"), so they know the product vocabulary and about half the technical vocabulary — with gaps they can't see and won't announce.

The failure mode to avoid is **not** "too technical." It is **technical words with no referent**. A non-developer can follow arbitrarily deep reasoning as long as every noun in it has been given a meaning first. So: go deep on the logic, and pay for each new term the moment you introduce it.

Two things they need that a peer-to-peer standup would skip:

- **Consequence.** Not "the sanitizer stripped the anchors" but "every internal link in that article was deleted before it went live, which is why the article shipped with none."
- **Confidence level.** Which claims you measured, which you inferred, which you haven't checked. They will make decisions on this, so an unlabeled guess is worse than no answer.

## Output language

Write the report in **the language of the message that invoked the skill**. `/dev-report 이번 주 작업 정리해줘` → Korean. `/dev-report` with no text → the language the conversation has been in.

Keep these verbatim in their original form regardless of output language: file paths, function and variable names, commands, log lines, error messages, branch and commit names, product and vendor names. The reader needs to paste them into a search box or say them to someone else — a translated identifier is a broken one.

When a technical term has no natural equivalent in the output language, use the English term and gloss it once in the reader's language, then keep using the English term.

## Step 1 — Gather

**The conversation is the primary source.** It holds what git cannot: why this work was chosen, what was tried and abandoned, what the user corrected you on, what a number actually meant. Reconstruct from it first.

Then corroborate the facts a report will be judged on:

```bash
git log --oneline -15
git diff --stat HEAD~1        # or the session's base commit
git status --short
```
```

## import-template (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4051-import-template
- الوصف: Import deliverable templates — proposal formats, report structures, brief layouts — and convert them into reusable placeholder-marked templates saved per brand, so commands like /digital-marketing-pro:performance-report and /digital-marketing-pro:content-brief format their output your way instead of the default. Triggers on \"/digital-marketing-pro:import-template\", \"our reports always follow th

```markdown
# /digital-marketing-pro:import-template

## Purpose

Import deliverable templates that define the output format for plugin commands. Templates specify section structure, content requirements, and formatting rules for proposals, reports, briefs, presentations, and other marketing deliverables.

When a command like `/digital-marketing-pro:performance-report` runs, it checks for a custom template first. If one exists, the output follows the template format instead of the default.

## Input Required

The user provides:

- **Template content**: Pasted template structure, section headings, or format specifications
- **Template name**: What this template is for (e.g., "proposal", "performance-report", "content-brief", "campaign-plan")
- **Description** (optional): When to use this template

If the user doesn't provide a name, infer it from the content structure.

## Process

1. **Load brand context**: Read `~/.claude-marketing/brands/_active-brand.json` for the active slug, then load `~/.claude-marketing/brands/{slug}/profile.json`. Apply brand voice, compliance rules for target markets (`skills/context-engine/compliance-rules.md`), and industry context. **Also check for existing guidelines** at `~/.claude-marketing/brands/{slug}/guidelines/_manifest.json` — if present, load restrictions and relevant category files. Check for custom templates at `~/.claude-marketing/brands/{slug}/templates/`. Check for agency SOPs at `~/.claude-marketing/sops/`. If no brand exists, ask: "Set up a brand first (/digital-marketing-pro:brand-setup)?" — or proceed with defaults.

2. **Analyze the template structure**:
   - Identify section headings and hierarchy
   - Note content requirements per section (length, data points, format)
   - Identify placeholder markers for dynamic content
   - Detect format preferences (bullet vs. narrative, data-heavy vs. summary)

3. **Structure into a reusable template**:
   - Preserve all section headings and ordering
   - Add content guidance comments (what goes in each section)
   - Mark which sections are required vs. optional
   - Include format notes (max length, style requirements)
   - Add placeholder syntax: `{{variable_name}}` for dynamic content

4. **Map to commands** — Identify which plugin commands should use this template:
   - Template named "performance-report" → `/digital-marketing-pro:performance-report`
   - Template named "proposal" → campaign plan outputs
   - Template named "content-brief" → `/digital-marketing-pro:content-brief`
   - Custom templates can be referenced by any module

5. **Check for existing templates** — If a template with this name already exists:
   - Show the current template
   - Ask: replace (overwrite) or keep both (rename new one)

6. **Save the template**:
```

## investigation-report (2551-investigation-report)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/motlin/claude-code-plugins/tree/d2bf81c6f3fc69e498397c3ff0a6c624c8b5c880/plugins/investigation-report
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2551-investigation-report/9904-investigation-report
- الوصف: Produce a single self-contained HTML report that explains a command-line investigation — the commands actually run, their real output, and just enough reasoning to teach it. Use when the user asks for a walkthrough, tutorial, write-up, teaching artifact, or "show me how you did that" of a shell debugging or exploration session.

```markdown
# Command-Line Investigation Report

Produce a chronological command log as one HTML page: what you ran, what it printed, and enough reasoning that the reader could rerun it and understand every flag. The goal is teaching, not a status update.

Before designing it, read [Red Blob Games' Making of: Circle drawing tutorial](https://www.redblobgames.com/making-of/circle-drawing/) as the quality benchmark for teaching through an HTML page.

## Structure it as a chronological command log

Walk the investigation in the order it happened, including dead ends, wrong hypotheses, and the commands that disproved them. Do not sanitize it into a clean after-the-fact story. Each step is the command, its real output, one line of why you ran it, and, only where the evidence changed your conclusion, a short "changed my mind" note. Make those turning points stand out; they are the spine of the story.

## Show real commands and real output

- Reproduce commands verbatim. Never clean up flags or show a command you did not run.
- Paste actual output, trimmed to what matters, and mark every cut visibly (e.g. `... ~60 more lines ...`).
- For commands that revealed nothing useful, skip the output and just note what you ran and why.

## Explain unfamiliar commands and flags

- For non-obvious commands, add a breakdown with one plain-language row per flag.
- Split fused flags: `-nrk3` is `-n -r -k3`.
- Explain a pipeline inside-out, like nested parentheses: command substitution first, then the tools it feeds.
- For a likely unfamiliar tool (e.g. `pgrep`), add a short "what is X": the basics, the flags used here, and its closest sibling (`pgrep`/`pkill`).
- Let the reader's questions drive depth: skip what they know, expand what they ask about.

## Keep commentary out

Cut editorializing, "lessons learned" summaries, and meta-commentary about method unless asked. Prefer "here is what I did" over "here is what you should learn."

## End with a command reference

Close with a compact table mapping question → command → what to read from the output.

## Keep styling minimal

Emit one self-contained HTML file with no external assets, so it opens with a double-click. Keep styling minimal and do not ask the user about it.

## Deliver and open the file

Write it to a durable location (the project directory or wherever the user names, not a scratch or temp path), then `open <file>`.
```
