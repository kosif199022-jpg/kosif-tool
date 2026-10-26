# مصادر «المخرج السينمائي (7 طبقات)» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## audit-agency-continuity (2997-agency-continuity-audit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/revertcreations/agency-continuity-audit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2997-agency-continuity-audit/12752-audit-agency-continuity
- الوصف: Run a read-only continuity and evidence audit of a persistent or autonomous agent workspace. Use when Codex must assess whether goals, memory, corrections, authority boundaries, commercial claims, schedules, or restart recovery are durable and verifiable; when an agent claims it can continue unattended; or before trusting a long-running multi-agent system after a session or machine restart.

```markdown
# Audit Agency Continuity

Run the deterministic auditor before interpreting narrative documents:

```bash
python3 scripts/audit_continuity.py --project <workspace> --state-dir <state-directory>
```

Use `--json` for machine consumption. The command is read-only.

Then:

1. Treat `fail` as a contradicted or missing durability requirement.
2. Treat `warn` as unproven, not achieved.
3. Inspect cited paths only for consequential findings; do not load an entire Markdown corpus by default.
4. Separate operational continuity from commercial success. A healthy scheduler or memory database never proves revenue.
5. Never repair findings unless the user asked for changes. For a requested repair, preserve existing state, add tests, and rerun the audit.
6. Report the smallest set of decisive findings: what survives restart, what can silently drift, what requires human authority, and which claimed outcome lacks external evidence.

Do not infer that numerous documents equal memory, that a timer equals successful execution, that model agreement equals external evidence, or that gross or pending revenue proves owner-available contribution.
```

## brand-film (101-video-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/video-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/101-video-skills/212-brand-film
- الوصف: Plan and make a narrative product brand film that moves from a human problem to a product reveal. Use for launch films, cinematic teasers, and campaign videos where story matters more than a step-by-step demo.

```markdown
# Brand film

A brand film earns the reveal. It makes the audience recognize a problem, turns that problem into a visual idea, then shows the real product as a credible answer.

## Shape the story

Plan a small number of beats: problem, escalation, turn, reveal, proof, and landing. The opening should give the viewer a human reason to care before showing the product. Let a physical or visual metaphor carry the problem, but do not let it replace evidence of what the product actually does.

Write one claim per beat. The proof beat should show the outcome in the real product or a faithful rendering of its UI. Check every capability and privacy statement against current product behavior.

## Keep one visual language

Read the brand's source materials: colors, typography, mark, materials, motion, sound, and examples. Use a limited set of recurring shapes and transitions so the film feels like one world. Change from the problem world to the product world with a motivated visual transition when possible. Keep text short enough to read in its allotted time.

Do not redraw a logo or end tag from memory if the actual asset exists. Use owned or licensed footage, music, and graphics. A metaphor may be invented; the product UI and claimed outcome must be accurate.

## Review before delivery

Storyboard the major frames and transitions. Watch a rough cut for story clarity before polishing. Then check final exports for timing, readable claims, audio mix, brand consistency, and aspect-ratio composition. The film should still make sense when viewed muted, unless the user specifically wants an audio-led piece.
```

## creator-visual-director (3067-youtube)

- الترخيص: **MIT**  ·  الأصل: https://github.com/sleestk/skills-pipeline/tree/cd75a3875f3b467fa5747ef71d334e1c79b83918/YouTube
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3067-youtube/13229-creator-visual-director
- الوصف: Visual Director Agent for [Creator]'s YouTube production pipeline. Acts as [Creator]'s Frontier Aesthetic Architect - takes a completed Script markdown file and generates a full Visual Production Brief covering scene-by-scene shot breakdowns, B-roll shot lists, screen recording instructions, graphic requirements, demo sequences, talking head setup notes, opening/closing shots, graphics package, an

```markdown
# Visual Director Agent — Frontier Aesthetic Architect

You are the Visual Director Agent for [Creator]'s YouTube production pipeline. Your job is to translate a completed script into a full **Visual Production Brief** — a ready-to-use guide for [Creator] (self-recording) and his Editor.

Every visual decision must reinforce the [Creator] brand and serve the Builder Avatar's experience.

---

## Brand Aesthetic — Non-Negotiables

**Brand Color Palette:**

| Role | Color | Hex | Usage |
|---|---|---|---|
| **Primary** | Bright Golden Orange | `#F5A500` | Logo, thumbnails, overlays, brand marks — the dominant energy |
| **Deep Orange** | Rich Burnt Orange | `#E8610A` | Edge/shadow variant, depth and contrast |
| **Accent** | Periwinkle Purple | `#6B6EC8` | Complement that makes orange pop — unexpected and ownable |
| **Background** | Soft Lavender White | `#E2E4F5` | Airy, light, modern — the canvas everything lives on |

- **Golden Orange is the signature.** Bright, magnetic, impossible to ignore — not tech-blue, not hype-red. Every visual decision should ask: does this feel like [Creator]'s energy?
- **Light backgrounds only.** `#E2E4F5` is the canvas. No dark backgrounds, no near-black, no moody gradients. The brand is bright and open.
- **Periwinkle is the unexpected weapon.** `#6B6EC8` is what makes the orange pop and the palette ownable. Use it for accents, overlays, and graphic elements that need to complement without competing.
- **Burnt Orange adds depth.** `#E8610A` for shadows, edge lighting, and contrast — keeps the palette from feeling flat.
- **[Creator]'s face is on camera everywhere** — long-form and short-form. Real face, real energy. Never hide behind slides or B-roll for more than 30–45 seconds without cutting back to [Creator].
- **No stock photo energy.** Real screenshots, real terminals, real tools [Creator] is actually using. The scout goes to the frontier — viewers can tell if you're faking it.
- **The overall vibe is: bright, bubbly (energetically, not literally), and magnetic.** The kind of visual energy that makes people stop scrolling and gravitate toward the channel.

---

## Signature Format — Blender Animation Strategy

[Creator]'s brand has a unique short-form and B-roll opportunity: **Blender-created animations** as a visual signature. When relevant, incorporate this into the brief:

**Format A — Animated B-roll:** [Creator]'s talking head is the anchor; Blender animations play underneath or as cutaways to visually illustrate what [Creator] is explaining. Orange/periwinkle palette applied to the 3D world.

**Format B — Voiceover Animation:** [Creator]'s voice plays over a standalone Blender animation sequence — no talking head. High-production feel, great for intros, concept explanations, or standalone Shorts.
```

## frontend-design-director (97-frontend-design-director)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/frontend-design-director
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/97-frontend-design-director/206-frontend-design-director
- الوصف: Design, build, or critique distinctive marketing websites and product frontends by first identifying the site archetype, then applying an evidence-backed structure, visual system, interaction model, and quality bar. Use for landing pages, multi-page marketing sites, SaaS and AI products, developer tools, fintech, ecommerce or physical products, research/editorial sites, portfolios, and high-concep

```markdown
# Frontend Design Director

Create a coherent design argument, not a decorated template. Preserve an existing brand or design system when one exists; these references supply reasoning and structure, never someone else’s identity, copy, assets, or signature composition. All recipes and code samples are optional starting points: adapt, combine, or ignore them when the product, repository, or audience calls for a different answer.

## Route before designing

### Ask about the existing UI first

Before designing or rebuilding a site, explicitly establish: **“Should we use the existing UI, or start from scratch?”** Ask once per project when the answer is not already explicit. For an existing brand, distinguish the marketing-site layout from the product UI shown within it: keeping the brand does not answer whether to preserve its application screens. A useful single question is “Keep the existing site/product UI, redesign the marketing site around the existing product UI, or design both from scratch?” If the user already chose, confirm that choice rather than asking again. For a genuinely new product with no UI, confirm the from-scratch direction.

Record the answer in the direction notes. While awaiting it, research and inventory the existing system, but do not finalize or replace its UI. Preserve mode uses real or faithfully reconstructed screens and the established design system; redesign mode permits new UI, clearly labeled as concept rather than actual product screenshots. This is Adam's requested intake gate, not a requirement to ask again before every small edit.

Identify the primary archetype and buying condition. If the brief spans categories, choose one primary archetype and at most one secondary influence.

| Archetype | User must believe | Default evidence | Read |
|---|---|---|---|
| Product-led SaaS / AI | “I understand the workflow and want to try it.” | product-in-action, use cases, customer proof | [saas-ai.md](references/saas-ai.md) |
| Developer platform / infrastructure | “It works, integrates, and will scale.” | live-looking output, code, architecture, benchmarks | [developer-platforms.md](references/developer-platforms.md) |
| Enterprise / fintech | “This is credible, controlled, and worth switching to.” | outcomes, controls, implementation, trust | [fintech-enterprise.md](references/fintech-enterprise.md) |
| Ecommerce / physical product | “I desire this object and can confidently buy it.” | product photography, detail, fit, proof, logistics | [commerce-physical.md](references/commerce-physical.md) |
| Research / science / editorial | “I grasp why this matters and trust the work.” | narrative, diagrams, publications, people | [research-editorial.md](references/research-editorial.md) |
```

## narrated-product-film (101-video-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/video-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/101-video-skills/216-narrated-product-film
- الوصف: Make a product film led by voiceover, with one real product surface or visual proof per spoken claim. Use for narrated launches, capability films, and scripted product stories.

```markdown
# Narrated product film

Let the voice lead, but make every line earn a picture. Pair each spoken claim with one visual subject that proves or clarifies it.

## Script first

Write short, speakable lines. One capability or claim per line usually makes one beat. Trace factual claims to the current product. When a feature depends on a mode or setting, name that condition in the line and show it on screen. Read the script aloud before building the timeline.

Mark the intended voice, pace, pronunciation, and pauses. Record or synthesize the voice only through a service the user has authorized and for which the voice rights are clear. Keep line and word timings so a revised read can retime captions and picture without guessing.

## Pair words and images

Make a beat table with the spoken line, the real UI or visual proof, the entry and exit, and any on-screen text. Use subtitles or highlighted words where they improve comprehension; do not stack the full script over a busy interface. A simple recurring layout can make different features feel like one film.

Timing should follow the voice. Let actions happen with the words that name them, and let the result settle before moving on. Keep transitions motivated by the product or story, not by the availability of an effect.

## Sound and verification

Mix music below intelligible speech and use sound effects only where they support a visible action. Use owned or licensed audio. Check the export by listening and watching separately: spoken words match the script, captions match the audio, each visual matches its line, no UI control is hidden, and the closing is long enough to read. Reframe and inspect each requested ratio.
```

## revision-continuity (1213-story-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/danjdewhurst/story-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2882-revision-continuity
- الوصف: This skill should be used when the user asks to revise a chapter, continuity check, find inconsistencies, audit character state, check timeline consistency, developmental edit, structural revision, "revision passes", "what pass next", "pacing check" as a revision pass, "clue check", or prepare existing story material for the next revision pass. NOT for planning book structure (use plot-structure),

```markdown
# Revision Continuity

## Overview

Revise existing Story Skills projects without losing continuity. Use this skill for targeted chapter edits, continuity audits, developmental revision, line edits, and pre-flight checks before drafting the next chapter.

## Prerequisites

A story project must already exist. Verify by checking for `story.md` in the project root, then run or inspect `story report .` when CLI access is available. Read `story.md` `language` (a missing field means `en`) and write every revision in that language; when a `story prose` or `story voices` check is reported as skipped for the language, do that check by reading.

## Named Revision Passes

Track a full revision as a ladder of named passes in `story.md`
`revision-passes`, so the work happens in order (big structural changes
before polishing sentences that may be cut) and survives between sessions:

```shell
story passes . --init            # writes the default ladder, keeping existing entries
story passes .                   # checklist with the checks each pass runs
story passes . --start pacing    # mark a pass in-progress
story passes . --done pacing     # mark it done
story next .                     # with story status revising, recommends the next unfinished pass
```

The default ladder is `structure`, `character`, `theme`, `continuity`,
`pacing`, `line`, `copyedit`, `proof`. Each entry is `{pass, status}` with
status `pending`, `in-progress`, or `done`; add a custom kebab-case pass
(`fact-check`, `sensitivity`) with `story passes . --start <name>`, which
appends it as `in-progress`. The checks per pass, as `story passes .`
prints them:

| Pass | Checks | Workflow below |
|------|--------|----------------|
| `structure` | `story timeline .`, `story pacing .`, `story diagram arcs` | Reverse outline, pacing waveform, removability audit |
| `character` | `story voices .`, `story knowledge <id> --at <chapter>`, `story diagram relationships` | Developmental revision (motivation, arcs) |
| `theme` | `story report .` | Theme audit |
| `continuity` | `story continuity .`, `story clues .`, `story links .` | Continuity audit, reveal economy, fact check |
| `pacing` | `story pacing .` | Pacing waveform |
| `line` | `story prose .`, `story voices .` | Line edit (the `line-editing` skill) |
| `copyedit` | `story prose .` + `style-sheet.md` | Copyedit (the `line-editing` skill) |
| `proof` | `story build --format print`, `story build --format html` | Proof (the `line-editing` skill) |

Mark a pass `--start` when beginning it and `--done` only when its checks
are clean or every remaining finding is a recorded decision. Set story
`status: revising` so `story next .` points at the next pass.

## Revision Workflow

1. Clarify the pass type unless the user already specified it:
```
