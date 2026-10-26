# مصادر «القصص والسكربتات» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## game-story-world-character (2199-lvtd-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/LVTD-LLC/skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8090-game-story-world-character
- الوصف: Design or evaluate game story, world, characters, spaces, presence, aesthetics, and indirect control. Use when adding narrative, quests, levels, environments, character arcs, worldbuilding, environmental storytelling, or emotional context to gameplay.

```markdown
# Game Story World Character

Use this skill to make narrative and world design serve play instead of competing with it. The output should give the coding agent clear content structures, state needs, triggers, and constraints.

## Source Traceability

Primary source: *The Art of Game Design: A Book of Lenses, Third Edition* by Jesse Schell, especially chapters 17-23 on story, indirect control, worlds, characters, spaces, presence, and aesthetics. The workflow is transformed and paraphrased.

Supporting source: MDA for separating authored mechanics from player-experienced dynamics and aesthetics.

## Workflow

1. Define the role of story: premise, motivation, context, consequence, mystery, comedy, identity, or emotional payoff.
2. Align story beats with player action and system state.
3. Use indirect control through goals, affordances, layout, rewards, information, and character cues.
4. Specify world rules, character functions, spaces, mood, and aesthetic constraints.
5. Convert narrative intent into implementable triggers, content schema, and test cases.

## Required Output

- `Narrative Function`: why the game needs story or world detail.
- `Story-Gameplay Map`: beats tied to player actions and system state.
- `World Rules`: facts, boundaries, tone, and contradictions to avoid.
- `Character Specs`: role, desire, behavior hooks, dialogue constraints, and gameplay purpose.
- `Implementation Notes`: state flags, triggers, content data, level cues, and tests.

## Local References

Before producing a story/world spec, read:

- `references/core/guide.md`
- `workflows/narrative-systems-spec.md`
```

## plot-structure (1213-story-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/danjdewhurst/story-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2877-plot-structure
- الوصف: This skill should be used when the user asks to "create a plot arc", "story structure", "add a plot point", "story timeline", "track foreshadowing", "pacing", "sagging middle", "act structure", "story arc", "plot outline", "snowflake method", or wants to plan and manage the narrative structure of a story. It owns book-level pacing; NOT for scene outcomes or writing a chapter hook (use scene-craft)

```markdown
# Plot Structure

## Overview

Plan and manage story arcs, plot points, foreshadowing, and narrative timeline. Each arc is a markdown file in `plot/arcs/` with a chronological timeline maintained in `plot/timeline.md`. The plot index tracks all arcs, their status, and theme coverage.

## Prerequisites

A story project must already exist (created via the story-init skill). Verify by checking for `story.md` in the project root.

## Choosing a Story Structure

1. Read `story.md` for genre, themes, and `form` (`novel`, `novella`, `novelette`, `short-story`, `flash`, `serial`, `picture-book`, `chapter-book`). For `short-story` and `flash`, use `references/short-story-form.md` instead of a multi-act beat sheet
2. Consult `references/structure-models.md` for available structures
3. Recommend a structure based on genre (default to three-act if unclear). If the user wants to design the whole book top-down before drafting, or asks for the Snowflake Method, follow `references/snowflake.md` on top of the chosen structure
4. Update `plot/_index.md` frontmatter `structure` field
5. Populate the story structure section with the beat sheet
6. When CLI access is available, run `story validate .`

## Creating an Arc

1. Read `story.md` for themes
2. Read `plot/_index.md` for existing arcs
3. Read `characters/_index.md` to understand available characters
4. Ask for:
   - Arc name
   - Type (main, subplot, character, thematic)
   - Which characters are involved
   - Which themes it serves
   - Which MICE threads the arc carries (optional `mice-threads:` frontmatter, written as a block list with one `- event` or `- character` item per line, not a `[event, character]` flow list; see `references/mice-quotient.md`)
5. Build the arc through conversation: setup, escalations, climax, resolution
6. Write the file using `references/arc-template.md` (or scaffold it with `story add arc "{Name}" --type main --character {id} --theme {theme}`, then fill in the sections)
7. Save to `plot/arcs/{arc-name-kebab}.md`
8. Update `plot/_index.md` arcs table
9. Update theme tracking in `plot/_index.md`
10. If characters are referenced, verify they exist in `characters/`
11. When CLI access is available, run `story reindex .`, `story links .`, and `story validate .`

## Managing Plot Points

Plot points live within arc files in the "Plot Points" table. When adding a plot point:

1. Read the relevant arc file
2. Add the plot point to the table with chapter reference (if known)
3. Add the event to `plot/timeline.md` in chronological order
4. If the plot point involves foreshadowing, add it to the arc's foreshadowing table
5. If the plot point creates a reader promise or mystery, create or update a record in `continuity/promises/` or `continuity/questions/`
```

## character-management (1213-story-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/danjdewhurst/story-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2871-character-management
- الوصف: This skill should be used when the user asks to "create a character", "update a character", "add a character", "build a family tree", "character relationships", "character timeline", "character arc", "character profile", "relationship graph", "name a character", or needs to manage characters in a story project. NOT for character voices or dialogue style (use voice-style), or for a thematic arc's l

```markdown
# Character Management

## Overview

Create and manage rich character profiles for a story project. Each character is a markdown file with YAML frontmatter in the `characters/` directory. Characters are cross-referenced with other story elements through kebab-case identifiers.

## Prerequisites

A story project must already exist (created via the story-init skill). Verify by checking for `story.md` in the project root.

## Creating a Character

1. Read `story.md` for genre, themes, and tone context
2. Read `characters/_index.md` for existing characters
3. Ask for the character's name and role (protagonist, antagonist, supporting, minor, narrator, deuteragonist). Before settling the name, run `story names "{Name}"` (several candidates can be checked at once): it errors on an exact clash with any existing character, alias, location, faction, artifact, system, or glossary term, and warns about look-alikes and names sharing an initial with a major character. Invented names from a culture should follow its naming rules (see `references/naming-languages.md` in the `worldbuilding` skill)
4. Build the profile through conversation, exploring:
   - Appearance and distinguishing features
   - Personality, traits, and quirks
   - Backstory and formative events
   - Motivations (external wants vs internal needs)
   - Voice and speech patterns (ask for example dialogue), plus `voice-words` (words and phrases they reach for) and `voice-avoid` (words they would never say)
   - Pronunciation, when the name is invented or easily misread (`pronunciation: "SEER-sha"`)
   - Character arc (starting state, turning points, ending state)
   - Key life events for the timeline
5. Write the character file using the template in `references/character-template.md`
6. Save to `characters/{name-kebab}.md`, or use `story add character "{Name}" --role "{role}"` when the CLI is available. Cyrillic and Greek names are transliterated (`Пётр` gives `characters/petr.md`). When the name is in a script with no transliteration table (`李明`), or the user wants a different spelling, choose the ASCII id yourself and pass it: `story add character "李明" --id li-ming --role supporting` keeps `name: 李明` in the file
7. Update `characters/_index.md` registry table
8. If relationships reference existing characters, update those character files too
9. When CLI access is available, run the maintenance pass in the story root:

```shell
story reindex .
story links .
story validate .
```

## Updating a Character

1. Read the existing character file
2. Read `characters/_index.md` for context on other characters
```

## book-fiction (1376-velith)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/epicsagas/Velith
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1376-velith/3218-book-fiction
- الوصف: Fiction craft reference for all subgenres: structure options, scene design, character depth, dialogue, POV and distance, the fiction-specific AI tells, and language notes. Read by architect, scene-generator, chapter-writer, editors, and beta-reader on fiction projects.

```markdown
# Fiction

The reader of a novel is not looking for a well-structured story. They are looking for the experience of being inside someone else's consequential life. Structure is how you keep them there. This file is craft, not a template.

## Structure: choose, do not apply

Pick the shape that fits the premise and say why in `outline.md`. Options:

- **Three-act** (setup 25% / confrontation 50% / resolution 25%). Midpoint reversal. Works for almost everything; risk is a flat second act.
- **Save the Cat 15-beat** (Opening Image → Theme Stated → Setup → Catalyst 10% → Debate → Break into Two 20% → B Story → Fun and Games → Midpoint 50% → Bad Guys Close In → All Is Lost 75% → Dark Night → Break into Three 80% → Finale → Final Image). Best for commercial genre fiction. Risk: fifteen equal-sized chapters that feel engineered.
- **Hero's Journey** (12 stages). Best for quest and coming-of-age. Risk: mentor and threshold scenes that feel obligatory.
- **Story Grid / five commandments per scene** (inciting incident, progressive complication, crisis, climax, resolution) applied at scene, sequence, act, and global level. Best for making every unit turn.
- **Snowflake** for planning: one sentence → paragraph → character summaries → expand. A planning method, not a book shape.
- **Bespoke**: braided timelines, epistolary, nested frames, reverse chronology. Only when the premise demands it and the author agrees.

Whatever the shape: the inciting incident is inside the first 10-12% or the reader leaves; the midpoint changes what the protagonist wants or believes, not just what happens; the ending is caused by a choice the protagonist could only make after everything that came before.

**Subplots** carry theme or contrast. Each needs its own small arc and must converge with the main line by the third act or be cut.

**POV plan** in the outline: whose head, what distance, which chapters. Do not change the plan mid-draft without updating the bible.

## Scene design

A scene is a unit where something changes. If nothing changes, it is not a scene; cut it or merge it.

- **Goal / conflict / outcome** (action scenes) alternating with **reaction / dilemma / decision** (sequel scenes). Alternate by need, not by rule; three action scenes in a row can be right.
- **Enter late, leave early.** Start after the greeting, end before the reflection.
- **Outcome types**: yes-but, no-and, no-but. A clean "yes" ends tension.
- **Subtext**: what the scene is about is not what the characters talk about.
- **Withholding**: every scene should have one thing the reader wants to know and does not yet.
- **Scene length follows weight.** A two-line scene can be the most important in the chapter.
```

## book-screenplay (1376-velith)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/epicsagas/Velith
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1376-velith/3228-book-screenplay
- الوصف: Screenplay craft reference: format, three-act and sequence structure, scene construction, dialogue subtext, A/B/C story weaving, series bibles, and screenplay-specific AI tells. Read by all agents on film, TV, and web-series projects.

```markdown
# Screenplay

A screenplay is a document for collaborators, read by people who read hundreds. It must be fast, visual, and impossible to put down on page 10. Novelistic interiority does not exist here; everything the audience learns, they see or hear.

## Structure

- **Three acts by page**: feature 90-120 pages; Act 1 to ~25, Act 2 to ~85, Act 3 to end. One page ≈ one minute.
- **Eight sequences** (two per act in 1 and 3, four in 2), each 12-15 pages with its own mini-arc: status quo → disruption → strategy → complication → crisis → decision → new status quo. Sequences prevent the second-act sag.
- **Beat placement**: inciting incident by page 10-12; first-act turn ~25; midpoint ~55 (a reversal, not an event); low point ~75; third-act turn ~85.
- **TV**: cold open, act breaks at commercial points (4-5 acts for network, 3 for streaming), A/B/C stories per episode, season arc bible with per-episode outlines. Pilot must establish the engine (what generates episodes forever).
- **Web series**: 8-15 pages per episode, hook in the first 30 seconds, cliffhanger every episode.
- **Short**: 5-30 pages, one turn, no subplot.

## Scene

- **Slug line**: `INT./EXT. LOCATION - DAY/NIGHT`. Location names consistent across the script (bible).
- **Every scene**: someone wants something, something is in the way, the scene ends with the situation changed. Outcome: yes-but, no-and, no-but.
- **Enter late, leave early.** Cut the arrival, the greeting, the goodbye.
- **Action lines**: present tense, only what can be seen or heard, 3-4 lines max per paragraph, white space is pacing. No "we see." No camera directions unless writer-director.
- **Character introduction**: NAME in caps at first appearance, age, one telling detail. Not a paragraph of backstory.

## Dialogue

- Subtext over statement. Characters talk around the thing.
- Distinct voice per character: rhythm, vocabulary, what they never say. Cover the names; the reader should still know who is speaking.
- Monologues ≤ 5 lines unless the script earns a set piece.
- Parentheticals rarely; the actor decides.
- V.O. and O.S. sparingly and consistently.
- Korean: 존댓말/반말 relationships fixed per pair in the bible; a shift is a story event. 지문 in 현재형.

## A/B/C stories

A-story (main plot, ~70%), B-story (relationship or theme, ~25%), C-story (runner, ~5%). B carries the theme; A carries the plot; they collide at the midpoint and the climax. Alternate A and B every 2-3 scenes; do not run five A scenes in a row.

## Format

Industry-standard layout (Courier 12, 1.5" left margin, dialogue block width). Drafts are markdown with a strict convention so `book-publish` can export to Fountain and PDF:

```
INT. KITCHEN - NIGHT

Action line.

CHARACTER
(parenthetical)
Dialogue.
```
```

## archetypes-storytelling-arcs (1503-universal-design-principles)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/HDeibler/universal-design-principles
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3732-archetypes-storytelling-arcs
- الوصف: Use this skill when designing narrative content — landing pages, case studies, onboarding flows, marketing campaigns, sales decks, ad arcs. Trigger when picking how to frame a customer story, when writing a launch campaign, or when the user mentions "this campaign feels flat" or "we need a better narrative." Sub-aspect of `archetypes`; read that first.

```markdown
# Storytelling arcs and the hero's journey

Stories are the most efficient way to convey emotional truth. A list of features is forgotten; a story of a user transformed by a product is remembered. Archetypes structure stories — the hero's journey is the most-cited template — and using them deliberately makes marketing, onboarding, and case studies dramatically more effective.

## The hero's journey (Campbell, 1949)

Joseph Campbell distilled cross-cultural mythology into a single recurring pattern. The full version has 17 stages; the simplified product-narrative version has roughly 8:

1. **Ordinary world** — the user's status quo (their pain, their constraint).
2. **Call to adventure** — the product is introduced.
3. **Hesitation** — the natural skepticism, the reasons not to.
4. **Mentor** — the product (or its team) offers guidance.
5. **Crossing the threshold** — first use, signing up.
6. **Trials** — the work of using the product.
7. **Reward** — the outcome, the transformation.
8. **Return / sharing** — the user becomes an advocate.

This arc structures most successful marketing campaigns, customer case studies, and product launches.

## Applying to product narratives

### Customer case studies

A typical case study before applying the arc:

> "Acme Corp uses our product. They report 40% productivity improvement."

Same case study with the arc:

> "Acme Corp's marketing team was spending 4 days a week on reports — too much manual work, too little strategy. They tried our product as an experiment. After two weeks of integration, they automated 70% of their reporting workflow. Today, the team spends those reclaimed days on campaigns that have driven a 30% increase in qualified leads."

The arc gives the data emotional shape: pain → adventure → mentor → trials → reward.

### Onboarding flows

Onboarding can follow the arc:

- Welcome screen acknowledges the pain (ordinary world).
- Setup is the call (adventure).
- Tutorial is the mentor.
- First successful task is the threshold-crossing.
- Building momentum is the trials.
- Achievement screen is the reward.
- "Invite teammates" is the return / sharing.

### Landing pages

Landing pages often follow a compressed arc:

- Hero section: the call.
- Problem section: the ordinary world.
- Solution section: the mentor (your product).
- Social proof: testimonials of others who completed the journey.
- CTA: cross the threshold.

### Marketing campaigns

A multi-touch campaign can play out across emails, ads, and content over weeks:

- Week 1: name the problem (ordinary world).
- Week 2: introduce the solution (call).
- Week 3: address objections (hesitation).
- Week 4: demo / trial (mentor + threshold).
- Week 5: success stories (reward).

## Picking the user's role
```
