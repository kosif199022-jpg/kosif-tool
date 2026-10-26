# مصادر «عروض باوربوينت» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## pptx-deck-context (3508-pptx-deck-creation)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/pptx-deck-creation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3508-pptx-deck-creation/14254-pptx-deck-context
- الوصف: Use when preparing the narrative, sources, and design context for a new editable PPTX deck.

```markdown
# PPTX Deck Context

Prepare the deck before coordinates or PPTX objects are authored. This skill owns the business narrative, source lineage, and design lock.

## Decision sequence

1. Confirm audience, decision, slide count, language, sources, and brand requirements.
2. Use the user-selected narrative framework. If none is specified, offer `mckinsey`, `scqa`, `pyramid`, `mece`, `action-title`, `assertion-evidence`, `exec-summary-first`, or `custom`; do not choose silently.
3. Assign stable source IDs and plan a `source_ref` for every metric, quotation, chart value, and factual claim.
4. Choose a documented design direction. Prefer a user brand guide, then read-only reference-deck evidence, then a reusable profile from `references/design-profiles.md`.
5. Record the framework, assumptions, source manifest, palette, typography, spacing, and signature elements in `summary` before authoring slides.

## Rules

- One slide should communicate one message, with an action-style title where the framework calls for it.
- Treat design references as design evidence, not content or asset sources.
- Do not copy external fonts, images, icons, or logos without recorded licensing evidence.
- Translate design signals into explicit fills, typography, spacing, and bboxes; do not rely on an automatic layout engine.
- Keep long source material concise. Ask for a summary or decision-relevant excerpt instead of turning a deck spec into a document dump.

See `references/design-profiles.md` for reusable profile guidance.
```

## pptx-reference-deck-analysis (3508-pptx-deck-creation)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/pptx-deck-creation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3508-pptx-deck-creation/14256-pptx-reference-deck-analysis
- الوصف: Use when analyzing a reference PPTX for read-only structure, theme, typography, layout rhythm, diagnostics, derived template catalogs, or safe OOXML package inspection.

```markdown
# PPTX Reference Deck Analysis

Inspect a reference deck as design evidence. This skill never copies, clones, or mutates a source deck.

## Contract

Implement required extraction on demand with a small task-local `python-pptx` script. Capture only the information required for the new deck:

- compact prompt context: slide count and size, text summaries, shape counts, styles, brand signals, template use, and layout rhythm;
- full extraction: `summary`, slides, and read-only `layout_tree` evidence;
- folder diagnostics: one result per deck plus a manifest;
- style-master analysis: colors, fonts, size distribution, master/layout use, and flow patterns;
- derived template catalog: zero-based source indices, layout roles, usable regions, placeholders, visual structures, and constraints.

## Rules

- Keep the source deck read-only and independently author every target-slide coordinate.
- Use the bundled OOXML utilities only for raw themes, relationships, notes, comments, animations, media, masters, or layouts that high-level extraction cannot expose.
- Record inspected parts and parsing exceptions in the analysis manifest.
- Do not use extracted content, fonts, images, or proprietary assets in a generated deck without explicit permission and license evidence.

## OOXML package inspection

Install `defusedxml` from `requirements.txt` before using the bundled utilities.

1. Run `scripts/inspect.py <deck.pptx>` for a compact JSON report of slide order, text, theme tokens, relationships, notes, comments, animations, and media.
2. Run `scripts/validate_package.py <deck.pptx> --output <report.json>` for malformed XML, broken internal relationships, content-type gaps, duplicate layout links, and orphaned parts.
3. Run `scripts/unpack.py <deck.pptx> <output-dir>` only when raw-package evidence is necessary.
4. Resolve relationship targets relative to the `.rels` owner; never infer slide order from filenames.

### Safety

- Never modify a supplied deck or blindly copy package parts into a new deck.
- Run the scripts from a trusted workspace; they reject path traversal, symlinks, oversized members, and archive bombs.
- Parse untrusted XML with `defusedxml`; do not enable entity expansion, DTD loading, or network access.
- Treat theme colors as tokens unless fully resolved against the color scheme.

See `references/reference-deck-analysis.md` for output shapes, `references/reference-deck-analysis-patterns.md` for documentation-only patterns, and `references/ooxml-parsing.md` for package part maps.
```

## presentation-builder (2663-presentation)

- الترخيص: **BSD-3-Clause**  ·  الأصل: https://github.com/neuromechanist/research-skills/tree/f0219bde233abb44d8a0c5d73f41ea27073e1493/plugins/presentation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2663-presentation/10128-presentation-builder
- الوصف: This skill should be used when the user asks to "create a presentation", "make slides", "build a slide deck", "create a talk", "make a keynote", "create a Reveal.js presentation", "generate presentation slides", "make a conference talk", "create a lecture", "build a poster presentation", "create presentation JSON", or mentions presentations, slides, slide decks, Reveal.js, talk preparation, confer

```markdown
# Presentation Builder

Create interactive Reveal.js presentations from JSON using the [Agentic Presentation Builder](https://github.com/neuromechanist/agentic-presentation-builder). The builder transforms structured JSON definitions into professional, interactive web-based presentations with Mermaid diagrams, LaTeX math, syntax-highlighted code, and animated progressive reveals.

## Pipeline Overview

```
1. Plan structure  -->  2. Author JSON  -->  3. Validate  -->  4. Serve & present
   (outline, theme)     (schema-driven)      (CLI validator)    (Vite dev server)
```

## Prerequisites: get the builder CLI

The engine ships an `apb` command (subcommands `validate`, `present`, `export`, `shoot`). Two ways to
run it; pick per situation. Pin the tag (`#v0.1.8`) for reproducibility.

**Zero-setup (default, no clone).** Run straight from the repo with bunx (or npx):

```bash
bunx github:neuromechanist/agentic-presentation-builder#v0.1.8 validate deck.json --json
```

**Iterative authoring / offline (recommended when validating repeatedly).** Use a managed
cache clone so each call does not re-resolve the git package. Resolve a builder home, cloning
once if needed, then run the `bun run` scripts from it:

```bash
APB_HOME="${APB_HOME:-$HOME/.cache/agentic-presentation-builder}"
if [ ! -d "$APB_HOME/.git" ]; then
  git clone --branch v0.1.8 https://github.com/neuromechanist/agentic-presentation-builder.git "$APB_HOME"
  (cd "$APB_HOME" && bun install)
fi
# then, e.g.:
(cd "$APB_HOME" && bun run validate -- "$(pwd)/deck.json" --json)
```

In the steps below, "`apb <command>`" means either the bunx form or `bun run <command> --`
from `$APB_HOME`. Both share one code path, so flags are identical.

## Step 1: Plan the Presentation

Before writing JSON, determine:

- **Topic and audience**: Shapes content depth and vocabulary
- **Slide count**: 8-12 for a short talk, 15-25 for a full session
- **Theme**: `academic` for research talks, `default` for general, `dark` for tech demos
- **Key visuals**: Which slides need Mermaid diagrams, images, code blocks, or tables
- **Speaker notes**: Include delivery guidance for each slide

## Step 2: Author the Presentation JSON

Write a `presentation.json` following the schema. See `references/schema-reference.md` for the complete field reference and `references/authoring-guide.md` for best practices.

### Minimal structure

```json
{
  "presentation": {
    "metadata": {
      "title": "My Presentation",
      "author": "Author Name",
      "theme": "academic",
      "aspectRatio": "16:9",
      "controls": {
        "slideNumbers": true,
        "progress": true
      }
    },
    "slides": [
      {
        "id": "title",
        "layout": "title",
        "elements": [
          {
            "type": "text",
```

## create-presentation (2112-pptx-dev-kit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/ksarelto/dev-ai-plugins/tree/aa2a58815f38800a8ab6d98f80ca032aa1c2fa18/pptx-dev-kit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2112-pptx-dev-kit/7527-create-presentation
- الوصف: Build a complete, polished .pptx presentation from a topic or brief — design schema, slide outline, per-slide content, deck.json, and the pptx-dev-kit layout renderer. Use when asked to create a new presentation, pitch deck, or slides on a topic, including matching the style of a reference .pptx. Do not use when the user wants to edit or update an existing .pptx file in place.

```markdown
# SKILL: create-presentation

**Invoked as**: `/pptx-dev-kit:create-presentation`
**Pipeline driver**: `pptx-orchestrator` (`MODE: Create`)
**Edit an existing file**: `/pptx-dev-kit:edit-presentation` instead

## Purpose

Turns a topic, brief, or outline into a finished `.pptx` by driving design schema → outline →
content + `deck.json` → `render_deck.py` → validate. This skill owns intake; the orchestrator
never asks the user anything.

If the user wants to **change a file they already have**, stop and use `edit-presentation`. Do not
strip that file and rebuild it.

## Prerequisites

A **topic or brief**. If the request is empty, ask:

```
I need a bit more to work with — what's the presentation about, who's the audience, and roughly
how many slides? (Defaults: professional audience, 6–12 slides, clean modern style, if you'd
rather I just pick.)
```

## Steps

### 1. Intake

Extract `BRIEF`, `AUDIENCE` (default professional), `PURPOSE`, `TONE` (default clean, modern,
confident), `SLIDE_COUNT_TARGET` (default `10–15`, or `5–8` if they said “short”), `BRAND`,
`REFERENCE_PPTX` (style only). State defaults in one line.

### 2. Output dir + python-pptx

```bash
OUTPUT_DIR="presentations/{slug}-$(date -u +%Y%m%d-%H%M%S)" && mkdir -p "$OUTPUT_DIR" && echo "$OUTPUT_DIR"
python3 -c "import pptx; print(pptx.__version__)" || python3 -m pip install python-pptx
```

Use the printed path as `OUTPUT_DIR`.

### 3. Spawn orchestrator

```
MODE: Create
BRIEF: {verbatim}
AUDIENCE: {AUDIENCE}
PURPOSE: {PURPOSE}
TONE: {TONE}
SLIDE_COUNT_TARGET: {SLIDE_COUNT_TARGET}
BRAND: {BRAND or "none"}
REFERENCE_PPTX: {absolute path or none}
OUTPUT_DIR: {printed path}
KIT_DIR: {this kit's root}
PULSE: {OUTPUT_DIR}/watch/pptx-orchestrator.json
PULSE_SCRIPT: {resolved check-pulse.mjs}
```

Spawn with `run_in_background: true`, then run the Liveness parent loop. Do not block on the Agent call.

### Liveness — poll the orchestrator

Canonical procedure: `{PULSE_SCRIPT directory}/../references/agent-liveness.md` when that file exists. It wins if this section disagrees. Resolve `PULSE_SCRIPT` in order: `app-dev-kit/frontend-orchestrator-kit/skills/orchestrate-frontend/scripts/check-pulse.mjs` from the workspace root, then `{KIT_DIR}/../frontend-orchestrator-kit/skills/orchestrate-frontend/scripts/check-pulse.mjs`.

`PULSE` is `{OUTPUT_DIR}/watch/pptx-orchestrator.json`.

1. Record `agent_id`. Touch `--role pptx-orchestrator --status working --station start`.
2. Every 60 seconds, `sleep 60` once, then `node {PULSE_SCRIPT} --check --pulse {PULSE}`. Do not end the turn while `status` is `working`.
```

## edit-presentation (2112-pptx-dev-kit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/ksarelto/dev-ai-plugins/tree/aa2a58815f38800a8ab6d98f80ca032aa1c2fa18/pptx-dev-kit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2112-pptx-dev-kit/7529-edit-presentation
- الوصف: Edit or update an existing PowerPoint .pptx in place — change slide copy, add or delete or reorder slides, fill a template — via OOXML unpack/clone/replace/pack without flattening formatting. Use when the user already has a .pptx and wants it modified, not when they want a new deck generated from a brief.

```markdown
# SKILL: edit-presentation

**Invoked as**: `/pptx-dev-kit:edit-presentation`
**Pipeline driver**: `pptx-orchestrator` with `MODE: Edit`
**Upstream**: `docs/pptx/editing.md`

## When to use

The user has a `.pptx` and wants it **changed**: rewrite a title, swap numbers, add a slide,
drop a slide, reorder, fill placeholder copy in a template. The original file is copied, never
overwritten.

A new deck from a topic, even “in the style of this file,” is `create-presentation` — not this
skill.

## Inputs (from the user)

- `SOURCE_PPTX` — path to the existing file (required)
- `EDIT_INSTRUCTIONS` — what to change
- Optional: which slide numbers, replacement text, whether to add/delete/reorder

If the path is missing, ask for it. Do not invent a new deck instead.

## Steps

### 1. Scaffold

```bash
OUTPUT_DIR="presentations/{slug}-$(date -u +%Y%m%d-%H%M%S)" && mkdir -p "$OUTPUT_DIR" && echo "$OUTPUT_DIR"
cp "{SOURCE_PPTX}" "$OUTPUT_DIR/source.pptx"
```

Never write `SOURCE_PPTX`. Confirm python-pptx:

```bash
python3 -c "import pptx; print(pptx.__version__)" || python3 -m pip install python-pptx
```

### 2. Spawn the orchestrator

```
MODE: Edit
SOURCE_PPTX: {absolute path to OUTPUT_DIR/source.pptx}
EDIT_INSTRUCTIONS: {verbatim}
OUTPUT_DIR: {printed path}
KIT_DIR: {kit root}
PULSE: {OUTPUT_DIR}/watch/pptx-orchestrator.json
PULSE_SCRIPT: {resolved check-pulse.mjs}
```

Spawn with `run_in_background: true`, then run the same Liveness parent loop as `create-presentation` (pulse `{OUTPUT_DIR}/watch/pptx-orchestrator.json`, role `pptx-orchestrator`). Do not block on the Agent call. A stale agent stops with the build-failure form (`Error: stale-agent`). Do not claim `deck.pptx` was produced.

### 3. Report

Relay Mode: Edit, what changed, `{OUTPUT_DIR}/deck.pptx`, and validation. If the file could not
be packed, report the verbatim error and list artifacts that did complete.

## Failure handling

| Scenario | Response |
|---|---|
| No source file | Ask for the `.pptx` path. |
| Legacy `.ppt` | Must be re-saved as `.pptx` first. |
| User also wants a new visual system | That is Create (style-matched), not Edit. Say so. |
| Chart on a cloned slide | Clones share chart parts — do not edit chart XML on the clone if the source must keep original data. |
```

## slides (1428-openai-office-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/fcakyon/claude-codex-settings/tree/d3974af4e8991489df54c87b51989e13d3d6f265/plugins/openai-office-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1428-openai-office-skills/3406-slides
- الوصف: Create and edit presentation slide decks (`.pptx`) with PptxGenJS, bundled layout helpers, and render/validation utilities. Use when tasks involve building a new PowerPoint deck, recreating slides from screenshots/PDFs/reference decks, modifying slide content while preserving editable output, adding charts/diagrams/visuals, or diagnosing layout issues such as overflow, overlaps, and font substitut

```markdown
# Slides

## Overview

Use PptxGenJS for slide authoring. Do not use `python-pptx` for deck generation unless the task is inspection-only; keep editable output in JavaScript and deliver both the `.pptx` and the source `.js`.

Keep work in a task-local directory. Only copy final artifacts to the requested destination after rendering and validation pass.

## Bundled Resources

- `assets/pptxgenjs_helpers/`: Copy this folder into the deck workspace and import it locally instead of reimplementing helper logic.
- `scripts/render_slides.py`: Rasterize a `.pptx` or `.pdf` to per-slide PNGs.
- `scripts/slides_test.py`: Detect content that overflows the slide canvas.
- `scripts/create_montage.py`: Build a contact-sheet style montage of rendered slides.
- `scripts/detect_font.py`: Report missing or substituted fonts as LibreOffice resolves them.
- `scripts/ensure_raster_image.py`: Convert SVG/EMF/HEIC/PDF-like assets into PNGs for quick inspection.
- `references/pptxgenjs-helpers.md`: Load only when you need API details or dependency notes.

## Workflow

1. Inspect the request and determine whether you are creating a new deck, recreating an existing deck, or editing one.
2. Set the slide size up front. Default to 16:9 (`LAYOUT_WIDE`) unless the source material clearly uses another aspect ratio.
3. Copy `assets/pptxgenjs_helpers/` into the working directory and import the helpers from there.
4. Build the deck in JavaScript with an explicit theme font, stable spacing, and editable PowerPoint-native elements when practical.
5. Run the bundled scripts from this skill directory or copy the needed ones into the task workspace. Render the result with `render_slides.py`, review the PNGs, and fix layout issues before delivery.
6. Run `slides_test.py` for overflow checks when slide edges are tight or the deck is dense.
7. Deliver the `.pptx`, the authoring `.js`, and any generated assets that are required to rebuild the deck.

## Authoring Rules

- Set theme fonts explicitly. Do not rely on PowerPoint defaults if typography matters.
- Use `autoFontSize`, `calcTextBox`, and related helpers to size text boxes; do not use PptxGenJS `fit` or `autoFit`.
- Use bullet options, not literal `•` characters.
- Use `imageSizingCrop` or `imageSizingContain` instead of PptxGenJS built-in image sizing.
- Use `latexToSvgDataUri()` for equations and `codeToRuns()` for syntax-highlighted code blocks.
- Prefer native PowerPoint charts for simple bar/line/pie/histogram style visuals so reviewers can edit them later.
- For charts or diagrams that PptxGenJS cannot express well, render SVG externally and place the SVG in the slide.
```
