# مصادر «مكتبة الأساليب الفنية للتوليد» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## style-extractor (1268-style-extractor)

- الترخيص: **MIT**  ·  الأصل: https://github.com/dashed/claude-marketplace/tree/f6a24dbc08da57aeb80e7423da2508457d0b3398/plugins/style-extractor
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1268-style-extractor/2946-style-extractor
- الوصف: Extract and document writing styles from source texts into reusable style guides. Use when the user wants to analyze an author's voice, create a style guide from a book or document, capture writing patterns for replication, or build a writing style rubric. Triggers on 'extract style', 'analyze writing style', 'capture voice', 'style guide from', or 'writing style analysis'.

```markdown
# Style Extractor

Extract reusable writing style guides from any source text. Produces four standardized deliverables that capture general patterns — not copied phrases — so the style can be replicated for any topic.

## When to Use

- User asks to extract or analyze a writing style from a book, article, or document
- User wants to replicate an author's voice for new content
- User wants a style guide, voice card, or writing rubric from a source text
- User says "extract style from...", "analyze the writing style of...", or "capture this voice"

## Prerequisites

**MCP tools required:**
- `mcp__fuzzy-search` — PDF page counting, outline extraction, and page-level reading
- `mcp__plugin_sequential-thinking_think__sequentialthinking` — Structured analysis across dimensions

**Output location:** `writing-styles/<style-name>/` in the project root. See `writing-styles/README.md` for the collection structure and `writing-styles/_template/` for deliverable templates.

## Workflow

### Phase 1: Source Analysis

Identify the source text and assess its structure before reading.

**For PDFs:**

1. Get page count: `mcp__fuzzy-search__get_pdf_page_count`
2. Get outline/TOC: `mcp__fuzzy-search__get_pdf_outline`
3. Understand document structure before sampling

**Select 5–7 sampling points** distributed across the text:

| Sample | Location | Why |
|--------|----------|-----|
| Opening | First 10% | Capture introductory voice, setup patterns |
| Early-middle | 25–35% | Style settles after opening |
| Middle | 45–55% | Core voice, least influenced by beginning/ending effects |
| Late-middle | 65–75% | Check for drift or adaptation |
| End | 85–95% | Closing patterns, evolved voice |
| +1–2 optional | Varied | Specific chapters, asides, or structurally distinct sections |

**Read representative passages** using `mcp__fuzzy-search__extract_pdf_pages` or the Read tool. Aim for ~50–80 pages total across all samples.

**For non-PDF files:** Use the Read tool directly. Apply the same sampling distribution across the document's length.

### Phase 2: Dimension Extraction

Analyze **17 style dimensions** across all sampled passages. Use `mcp__plugin_sequential-thinking_think__sequentialthinking` to organize observations systematically.

| # | Dimension | What to look for |
|---|-----------|-----------------|
| 1 | Tone | Formal/informal, serious/playful, authoritative/conversational |
| 2 | Sentence length & structure | Average length, variation, complexity, use of fragments |
| 3 | Paragraph length & density | Short punchy vs. long expository, information density |
| 4 | Vocabulary level & register | Technical depth, word choice patterns, jargon usage |
| 5 | Transitions | How sentences, paragraphs, and sections connect |
```

## style-writer (1269-style-writer)

- الترخيص: **MIT**  ·  الأصل: https://github.com/dashed/claude-marketplace/tree/f6a24dbc08da57aeb80e7423da2508457d0b3398/plugins/style-writer
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1269-style-writer/2947-style-writer
- الوصف: Write content using stored writing styles from the writing-styles/ collection. Use when the user wants to write in a specific voice, apply a stored style, list available writing styles, or evaluate text against a style rubric. Triggers on 'write in [style] style', 'use [style] voice', 'list writing styles', 'apply style', or 'evaluate my writing'.

```markdown
# Style Writer

Write content in any stored writing style. Discovers available styles from the `writing-styles/` collection, loads the appropriate guide into context, applies it during writing, and optionally self-evaluates the result against the style's rubric.

## When to Use

- User wants to write content in a specific stored style
- User asks to "list available styles" or "what voices do we have?"
- User wants to edit or rewrite existing text to match a style
- User asks to evaluate or score text against a style rubric

## Style Discovery & Selection

List directories in `writing-styles/` (exclude `_template/`). Each directory is an available style.

**Selection logic:**

| Scenario | Action |
|----------|--------|
| User names a style exactly | Look it up directly in `writing-styles/<name>/` |
| User describes a style vaguely | List available styles, show each voice-card summary, let user choose |
| Only one style exists | Use it by default, confirm with user |
| No styles found | Tell user to create one with the style-extractor skill |

## Context Loading

Load compact files first — voice card + do/don't list give enough context for most tasks.

| Order | File | When to load | Purpose |
|-------|------|-------------|---------|
| 1 | `style/voice-card.md` | Always | Compact essential reference (~300 words) |
| 2 | `style/do-dont.md` | Always | Actionable guardrails for writing |
| 3 | `style/full-style-guide.md` | Long/complex pieces, or if voice card isn't enough | Deep reference with examples |
| 4 | `evals/style-rubric.md` | Only when evaluating | Scoring dimensions |

Read files using the Read tool.

## Writing

Apply the loaded style to the user's content request:

1. Use the voice card as the primary compass
2. Cross-check against the do/don't list while writing
3. For long pieces: write in chunks, periodically re-read the voice card to prevent drift
4. Incorporate style-appropriate transitions, sentence patterns, and rhetorical moves

### Fiction: Narrative Authenticity

When writing fiction or creative writing, also load [references/narrative-authenticity.md](references/narrative-authenticity.md) and:

1. **Pre-write:** Review the pre-writing checklist. Plan structural choices (timeline, subplots, character moral complexity) before drafting.
2. **During writing:** Vary scene types and emotional intensity. Resist the pull toward clean single-track plots, explicit thematic statements, and embodied-metaphor-only emotion.
3. **Post-write:** Run the post-writing checklist. Audit for AI narrative defaults — especially Claude-specific fingerprints (flat event escalation, epilogue endings, low event diversity).
```

## adhd-output-style (1411-adhd-output-style)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/fcakyon/claude-codex-settings/tree/d3974af4e8991489df54c87b51989e13d3d6f265/plugins/adhd-output-style
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1411-adhd-output-style/3349-adhd-output-style
- الوصف: This skill should be used when the user asks for "ADHD output", "fewer output tokens", "short numbered steps", "limited working memory formatting", or explicitly invokes "adhd-output-style".

```markdown
Format every response for a reader with limited working memory who needs
low-friction starts and visible progress, while still teaching. Apply to all
interactions in the current task.

## Structure (ADHD)

- Open with the actionable step or the answer, not context or setup.
- Break multi-step work into numbered lists, one action per step.
- End with a single next action that takes under two minutes.
- Keep secondary issues separate; do not bundle them into the main answer.
- Restate progress each turn (e.g. "step 3 of 5"); assume prior context is lost.
- Use concrete time estimates ("~2 min", "3 files"), never vague ones.
- State what now works in plain terms instead of burying it in a recap.
- Describe errors factually: cause, then fix. No alarmed language.
- Cap lists at five items; split longer ones into priority tiers.
- Cut preambles, recaps, and closing pleasantries. Start at the answer, stop when done.

Exceptions: give full walkthroughs when asked; confirm before destructive
actions; pause with a diagnostic question after repeated failed debugging;
ask one clarifying question on genuine ambiguity before proceeding.

## Education (Explanatory)

Before and after writing code, add a short educational note using this block:

`★ Insight ─────────────────────────────────────`
[2-3 codebase-specific educational points]
`─────────────────────────────────────────────────`

Put depth here, not in the main answer. Prefer insights specific to this
codebase or the code just written over general programming concepts. Cap at
three points so the block stays scannable. The rest of the response stays terse.
```

## prior-art (3175-prior-art)

- الترخيص: **MIT**  ·  الأصل: https://github.com/svyatov/agent-toolkit/tree/30316cebb256ff4a11d9483445c8769c1d1e4050/plugins/prior-art
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3175-prior-art/13504-prior-art
- الوصف: Check arXiv prior art before designing non-trivial architecture, algorithms, or protocols

```markdown
# Prior Art

Hours get wasted building something arXiv already solved, with the failure
modes already published. Read it first.

## Pre-flight (run before Phase 1)

This skill is expensive: a real arXiv fetch plus roughly one isolated
Agent call per paper (typically 10-20), plus scoring, clustering, and
convergence. Do not pay that cost when there's no real prior art to find.

**Step 1. Explicit invocation check.**

If the user invoked this skill by name, or explicitly asked to "check
arXiv", "check prior art", or "search for papers on this", **skip the rest
of this section and go straight to Phase 1**. The user opted in.

**Step 2. Self-judge (only if Step 1 did not match).**

Ask yourself three questions. If the answer to any is no, ABORT.

1. **Is there a technical mechanism to research?** Naming a variable,
   wiring a CRUD form, or gluing two documented SDKs together has no
   prior-art question worth asking. Designing a caching strategy, a
   consensus/coordination scheme, a ranking or retrieval approach, an
   ML training or inference technique, a novel protocol, or anything
   where "the naive version breaks at scale" does.
2. **Is the user about to commit real effort to it?** A one-off script
   doesn't earn a literature search. A component that will anchor the
   architecture, or that's expensive to redo once built wrong, does.
3. **Did the user leave the approach open?** If they already named the
   specific algorithm/paper/library to use, or said "just implement it
   the simple way", they've already converged. Don't re-open it. Abort.

If all three checks pass, proceed to Phase 1.

If any fails, ABORT and proceed with the direct implementation. Optionally
append one sentence: *"Say the word if you want this checked against arXiv
prior art first."*

## The loop

Three phases. Fetching is not divergence: it's find real documents, then
read each in isolation, then converge. Skipping the isolation step turns
this into an LLM guessing about papers it hasn't actually read.

### Phase 0: Categorize

Map the build problem onto 3-5 arXiv subject categories and 3-6 concrete
search terms (the technical mechanism words: "cache invalidation", not
"caching system"). Pick from the table below, or name another category id
if you're confident of it.

| Category | Covers |
|---|---|
| cs.AI | general AI systems, agents, planning, knowledge representation |
| cs.LG | learning algorithms, training methods, model architectures |
| cs.CL | NLP, language models, text processing |
| cs.CV | image/video understanding, generation, perception |
| cs.IR | search, ranking, recommendation, retrieval-augmented systems |
| cs.DC | distributed systems, consensus, sharding, replication, scheduling |
```

## style-pack (2058-style-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/kai-tw/claude-plugins/tree/7422e695b2483cc2ccf0a5ebe2c1fe81edc788d6/plugins/style-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2058-style-pack/7303-style-pack
- الوصف: The founder's cross-project style code — charter S1–S16 (`rules/index.md`) with Dart / C# / JS language files. `style-pack --paths <changed files>` prints the rules a diff is graded against; reviewers cite `S<N>.k` verbatim. To add or change a rule, read `rules/CONVENTIONS.md` first (legislative procedure and drafting form). TRIGGER: which style rule · style code · 撰寫法 · S6 · add a style rule

```markdown
# Style pack

- `style-pack --paths <file…>` — the charter + the language files those extensions map
  to (the map lives in the script). `style-pack dart csharp js` names them directly.
- `§Precedence` in `rules/index.md` is the one version of how the three ranks order:
  constitution (the charter) · statute (language files) · regulation (a project's
  `.claude/rules/`).
- Legislating: `${CLAUDE_PLUGIN_ROOT}/skills/style-pack/rules/CONVENTIONS.md`.
```

## art (1511-homie)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/homie-rocks/homie
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1511-homie/3889-art
- الوصف: Make a studio's game look like something at build time — a cover from a real frame of the game (free), painted covers, backdrops, textures and character plates from image models through the creator's OWN fal account under a hard budget with a receipt for every call, checked (does the texture tile, is the file small enough for a phone, does the cover promise only what the game contains) and loaded 

```markdown
# Art for a studio's game

**Build time, never a frame of play.** Everything here happens once, before anybody plays, and costs
nothing at runtime: never call an image model from a game's loop or from anything a person waits on.
If you want one there, you want a baked asset instead.

One script: `scripts/art.mjs` in this skill's folder (Claude Code:
`node "${CLAUDE_PLUGIN_ROOT}/skills/art/scripts/art.mjs" <command>`), from inside the studio. Node 22,
ffmpeg and Chrome; `--json` on every command. Art jobs live in `art/<slug>/` (the images, the
`budget.json`, the `.request` and `.json` receipts beside each generated file); every paid call is
also a line in `art/receipts.jsonl`.

```sh
node <art.mjs> check      # ffmpeg, Chrome, the studio; the fal key checked for free (only generated images need it)
```

## 1. The cover, first, always

The cover is what a stranger sees before pressing anything: the studio's game page, the directory
card, a link preview. Start from the game itself:

```sh
npm run dev                                                       # background task
node <art.mjs> frame <game> --url http://127.0.0.1:8787           # frames of the big screen playing, the busiest picked
node <art.mjs> cover <game> --from art/frames/frame-04.png [--focus 0.6,0.4]
```

`frame` films the game's big screen (bots playing in a live room) with the platform's own furniture
hidden (the join QR, the status chip, result cards) and keeps the frame with the most visible detail.
`cover` crops it to 16:9 around the focus, writes `cover.jpg` (1600x900, under 400 KB) into the game
and names it in `game.json` (`"cover": "cover.jpg"`): the site and the directory use it until the game's
landing has a still of its own (`hero/wide.jpg`), which then is its picture everywhere.

**Open the cover and look.** A cover is a picture of the GAME: no QR code, no share panel, no debug
text, not the waiting screen (a picture of nothing happening). Dark or featureless frames get a
warning: a black card on a page reads as a black box.

**A painted cover** from that frame, when the person wants one (paid, below): write the prompt from
the game you just played, never from its title. Describe what is on screen: the palette, the time of
day, what the player is doing, the shapes. A cover that promises something the game does not contain
is the one failure here that matters: a person presses Play expecting that picture and meets
something else. Use the real frame as the image reference (`"@file:art/frames/frame-04.png"` in the
input) so the painting keeps the game's layout.

## 2. Paid images: price, budget, one call at a time

Generated images come from fal through the person's own account: they create a key at
```
