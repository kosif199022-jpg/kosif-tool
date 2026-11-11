---
name: kosif-black-dragon
description: "التنين الأسود (Black Dragon): one door to every KOSIF skill, tool and power. v1.0 is the clean rebuild (python -m dragon find / doctor / verify / cut / beats / words / mix / film / engines / run, 11 engines with parity tests); this repo copy also keeps the native-fusion catalog, the mandatory video protocol, the creative council, 3D build studio and motion styles. Use first when the user says «التنين الأسود»، «قدراتك»، «فيه أداة/مهارة لـ…», or before any video, montage or creative task to pick the right skill, engine or tool."
---

# التنين الأسود — Black Dragon (Native Fusion)

## v1.0 — the clean rebuild (start here)

The rebuild of kosif-tool into one clean repo, **black-dragon**, is done (phases 1–6, all gates measured, 150 tests passing). It is the single door for day-to-day work. Plan, phase gates and evidence: [`references/REBUILD_PLAN.md`](references/REBUILD_PLAN.md).

Repo on the owner's PC: `C:\Users\cinde\OneDrive\Desktop\التنين الأسود` (dev copy `C:\Users\cinde\kosif-own\black-dragon`). The original repos, including this one, stay untouched by it.

```
cd "C:\Users\cinde\OneDrive\Desktop\التنين الأسود"
python -m dragon find "الطلب بكلام المستخدم"      # best tools (with a runnable command), skills (with SKILL.md path), superpowers, powers
python -m dragon show <id|name>                    # one item in full
python -m dragon doctor                            # programs + Python modules this machine really has
python -m dragon stats                             # what the catalog holds
python -m dragon build                             # re-index after adding repos/skills (sources in data/sources.json)
python -m dragon verify out.mp4 --expect 1080x1920 --out evidence.json   # duration, size, fps, LUFS, true peak, audio/video length mismatch
python -m dragon cut in.mp4 12.4 31.0 out.mp4      # frame-accurate smart cut (exact frame count)
python -m dragon beats song.wav --out beats.json   # tempo + beat grid for cuts
python -m dragon words song.wav --lang ar --out words.json   # sung/spoken lines with word timings
python -m dragon mix mix.json out.wav              # song section + voices, song ducks under voice, exact length, -14 LUFS
python -m dragon film spec.json --stills 1.5,7.5,12  # footage cinema: review stills first
python -m dragon film spec.json [--reuse] [--remux]  # full film -> MP4 -> verify (templates: engines/cinema/templates/*.json)
python -m dragon engines                           # every engine with its purpose
python -m dragon run <engine> <subcommand> ...     # run any engine (same as python -m engines.<engine> ...)
python -m pytest -q tests                          # full suite incl. old-vs-new parity tests
```

### Engines (each rewritten from the old kosif module, each with old-vs-new parity tests)
| Engine | Use it for | Main subcommands |
|---|---|---|
| `dragon_montage` | footage + task in the owner's words -> reasoned, reviewed edit (analyze, brief, taste, EDL, render, review) | `edit`, `plan`, `go`, `doctor`, `station <name>`, `tool <module>` |
| `talking_head` | one talking-to-camera recording -> vertical editorial reel (pause cuts, mastered voice, animated text) | `check prepare transcribe words cut master validate stills render sheet` |
| `cinema` (via `dragon film`) | real footage + song -> cinematic 9:16 tribute/celebration films | `dragon film spec.json` |
| `web_film` | motion films built as seek-driven web pages | `plan scaffold check render`, `world example\|beats\|check\|build\|review\|render` |
| `editorial` | archival editorial look: grain, bloom, kinetic captions | `doctor example check build render` |
| `shadow_theatre` | silhouette / shadow-theatre films from a scene JSON | `doctor library analyze check stills render` |
| `voice_studio` | speech with word timings, voice clone/design, transcription to SRT/VTT | `doctor voices speak transcribe clone design verify` |
| `reel_hooks` | score a reel's first line, beat sheet for a script, Arabic humanizer | `hook beats clean` |
| `kling_director` | Kling short-film prompt pack + 3x3 storyboard + lint (never calls Kling) | `plan build check` |
| `matrices` | invent new visual systems from causal bricks, A/B/C tests, ledger | `experiment generate ideate laws bricks ledger …` |
| `cards` | one interpreter for the method cards (old generated runners turned into data) | `list`, `run <id>`, `run --family X`, `stats` |

Shared core: `engines/media.py`, `engines/audio.py`, `engines/montage.py`, `engines/render/render.cjs` (frames piped straight to ffmpeg, full BT.709 tags). `engines/cinema`: spec → graded shots → canvas page → MP4. Gate proof: Mayar film 1 rebuilt = VMAF 99.46.

### What the v1.0 catalog holds (built from data, no data inside code)
- 22,319 entries: 15k+ skills from kosif-atlas, 114 from 100-superskills, kosif-tool's skills, fastify-motion-bro, installed skills, downloaded repos.
- 212 runnable tools with commands, 5,917 powers with status (proven / ready / install / key / documented / idea), 485 superpowers.
- Arabic-aware search: diacritics, alef/ya/ta-marbuta forms, Arabic digits and the article «ال» are normalised; BM25 ranking with names weighted 4x.
- Not ported: Apple Vision tools (Mac only) and the FCPXML exporter (optional); 1,901 method cards are marked «مش متنقل» with a reason each (`data/cards/_parity.json`).

### How to work with it
1. `dragon find` the request, then open the chosen SKILL.md or run the tool's command. Report what was really executed separately from what was only consulted.
2. Status `proven`/`ready` beats `documented`/`idea`; check `requires` with `dragon doctor` before promising.
3. Measure every media output with `dragon verify` before calling it done.
4. Footage → cinematic films: `black-dragon-cinema` skill (Mayar films pipeline). Montage folder rules: `C:\Users\cinde\OneDrive\Desktop\المونتاج\CLAUDE.md` (quality first, best tool per job, cinematic not educational).
5. Third-party skills (kosif-atlas mirror, dragon-repos) are reference: read scripts before running, respect each licence.
6. No spending, publishing or pushing to GitHub without the owner's explicit yes.

## In this repo (kosif-tool): native fusion, protocol and council

Everything below still works from the kosif-tool repository root and is kept as is. Use it when you are inside this repo, or for the video protocol, the creative council, the 3D build studio and the motion styles.

**Product:** one new skill with its own analysis and synthesis logic. It is not a wrapper around thousands of old scripts.

## Working contract

1. Open and extract every catalog entry, preserving its original ID, source path, source SHA-256, methods, requirements, and any actual code-file fingerprint.
2. Link the entry immediately to the new Black Dragon source ledger. No orphan entries and no double counting.
3. Distinguish the four completion levels: **source-linked**, **machine-extracted**, **native-implemented**, **real-execution-verified**. Never label extraction as implementation.
4. Synthesize overlapping knowledge into a coherent new approach, preserving non-overlapping constraints. Keep original references as an audit trail, not as mandatory runtime dependencies.
5. Turn extracted insights into native executable features when practical. Only mark a feature implemented after its new code exists. Count executed only from real task evidence.
6. Original Black Dragon / Dragon Mind / standalone tool routing is **off by default**; legacy IDs can be returned as **optional links**, without executing them.

## Mandatory video-product protocol (إلزامي)

Any request for a video product (reel, ad, promo, montage, motion, film, intro,
shorts) walks ONE fixed path of seven stages: `brief → concept → color-design →
shots → produce → qa-color → deliver`. Read `references/VIDEO_PROTOCOL.md` and drive
it with `scripts/video_protocol.py` (`start`, `record`, `color`, `check`). A stage can
only be recorded after the previous one; each stage is sealed; the two color stages
are measured from real pixels (60/30/10 palette, ONE accent on the hero, chosen by
the contrast / emotion / neon rule). Every stage first runs its MANDATORY CORE SKILLS
for real with `video_protocol.py core <id> --job J -- <args>` (sealed receipt, exit 0):
Dragon Mind + tool matrix (brief), Infinite Matrices + 86-style atlas + hook scorer
(concept), motion-graphics repos + a shot planner (shots), one renderer (produce),
the delivery gate (qa). `video_protocol.py cores` prints the map. Never deliver a video until
`video_protocol.py check --job <job>` exits 0. `compose` adds a `video_protocol`
block automatically when the task mentions video.

## Commands

Run from repository root:

    python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py index --out out/black-dragon-fusion-01
    python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py compose "اعمل مونتاج سينمائي على الإيقاع" --index out/black-dragon-fusion-01/sources.jsonl
    python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py verify --out out/black-dragon-fusion-01

**Use `plan` for day-to-day work** — it turns the same composition into a short readable Markdown plan (six stages with their question and success check, merged method steps with source IDs, the catalog's documented commands, requirements, input gaps). It takes ≈5 s on an existing index; build the index once (≈5 min, 7,400+ sources) and reuse it:

    python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py plan "اعمل ريل مونتاج سينمائي على الإيقاع" --index out/black-dragon-fusion-01/sources.jsonl --save out/plan.md

Follow the plan, run only the commands you actually need (they are listed, not executed), and report real outputs. On Windows `python3` must be a real Python (not the Microsoft Store alias). To include *only optional pointers* to catalog entries, add `--legacy-links` to compose. No external process, paid model, or original adapter is invoked by these commands.

## Repo fusion (REA, 2026-11-10) and the media hunter

Ten public repositories were dissected with REA. Their best new capabilities were re-implemented natively as nine self-tested modules in `scripts/fusion/`; the remaining capabilities stay source-linked with exact `path:line`. The ten repositories are lemo-opuscar, video-shotcraft, pixelfx, ClaudeAnimationBase, mcp-for-blender, three.js, react-three-rapier, librosa, awesome-opus5-5-videos and opus-video-prompts.

The modules cover the music map, rhythm and reading checks, the beat grid and CapCut/JianYing draft planning, pixel VFX and hit-stop, reads and boil lint, the Blender scene audit, deterministic three.js frames, the physics bake and a video-prompt lint.

Routing and evidence: `scripts/repo_fusion.py` (`list`, `find "<task>" [--stage]`, `show`, `modules`, `self-test`). Overview: [references/REPO_FUSION.md](references/REPO_FUSION.md). The capability count is 101 (47 native, 54 source-linked); report those numbers, not "all repos integrated".

Footage and photo search: `tools/media_hunter/mh.py` searches 615 sites and 19 live API sources, 15 of them keyless, and returns real file URLs with licences. Guide: [references/MEDIA_HUNTER.md](references/MEDIA_HUNTER.md).

    python3 .claude/skills/kosif-black-dragon/scripts/repo_fusion.py find "قص على الدروب"
    python3 .claude/skills/kosif-black-dragon/scripts/fusion/native_musicmap.py map song.mp3 --out map.json
    python3 -I .claude/skills/kosif-black-dragon/tools/media_hunter/mh.py hunt "camel desert sunset" --type video

## Native reasoning absorbed from Dragon Mind

The new `scripts/native_mind.py` **contains its own** 26-faculty taxonomy and six-stage cognitive
cycle, based on Dragon Mind's controlled vocabulary. It does **not** import or run
`kosif-dragon-mind`, the legacy `black_dragon.py`, or their adapters.

`compose` now includes a `native_mind` result with:

- Task-specific faculty classification and the six thinking stages:
  frame → explore → decide → build → verify → learn.
- Native, source-traceable merging of identical method fragments. **Different
  constraints are preserved**, even when methods are similar.
- Typed input/output handoffs and an explicit critic for missing inputs.
- A source-ID lineage for every extracted method and a clear distinction between
  native thinking implemented and original features not yet reimplemented.
- Original tool references remain links only when `--legacy-links` is explicitly requested.

## Catalog-wide native fusion atlas

The `index` command now creates **`fusion_atlas.json`** in addition to `sources.jsonl`:
it feeds *all catalog records* through the independent 26-faculty native mind,
combines exactly repeated instructions without losing their contributing source IDs,
and retains each distinct instruction and original source lineage. Unlike task-specific
`compose`, the atlas is built across the full indexed catalog rather than the
top 12 matching sources. Markdown skills, playbooks and protocols contribute their
full original text rather than headings alone. `verify` also checks the atlas hash
and every source ID in its membership list. A changed or missing atlas fails verification.

The atlas is **a knowledge artifact, not an executable substitute for 7,000 programs**.
Semantic equivalence, conflicts, execution, and media/API capabilities still require
further implementation and evidence. Optional pointers to old tools remain disabled
by default; no legacy process is executed during fusion.

This is a first **native cognitive fusion engine**. It is deterministic text/knowledge
synthesis; it does not independently render video, transcribe audio, or execute all
underlying programs. Source hashing, extraction, reasoning, implementation, and
actual execution must continue to be reported as separate milestones.

## Verified composition and Arabic matching

- Task lookup now normalizes Arabic diacritics, tatweel and common Alef variants; it retains original tokens while also matching common prefixes such as `الـ`, `والـ` and `للـ`. This is deterministic lexical matching, not a semantic language model.
- When a sibling `fusion_atlas.json` exists, `compose` checks its checksum, the source-index checksum and its full source-ID membership against `summary.json`. Modified or stale indexes and atlases fail closed; regenerate with `index` instead of presenting unverified synthesis.
- `verify` rejects out-of-root paths and symlinked source/code references even if the referenced bytes happen to hash to the expected value.
- These checks are **local integrity guards, not cryptographic signatures, authority validation, or runtime execution proofs**. Running the old tools remains disabled by default.

## Evidence and limits

`sources.jsonl` stores one machine-extracted link per catalog entry with its source hash and code fingerprint (where a local file exists). `summary.json` stores the exact input count and index hash. `verify` detects changed or missing sources. These are fast bookkeeping checks, **not** 7,000 functional test runs.

The current implementation covers full-catalog extraction, exact linking, catalog-wide method grouping and lineage, task-specific native composition, and integrity checking. It **does not** claim that every catalog method has been rewritten into one runtime program, or that every original feature has been manually reviewed. Those milestones require actual further code and cannot be inferred from a generated index.

## Creative Council — no artistic gatekeepers

The new independent creative council has **12 expert roles** (not a rights officer): chair, analyst, dramatic writer, creative director, visual director, motion/render engineer, adversarial critic, decision specialist, researcher, systems thinker, audience advocate, and learning specialist.

It reads **443 core cognition records across nine datasets, plus 82 contextual Atlas Mind operating records (525 total)**: 159 Dragon Mind frameworks, 63 Superpowers mental models, 47 thinking-core powers, 29 creativity powers, 14 planning powers, 41 prompt-design powers, 18 strategy powers, 64 book-derived methods and eight reasoning modes, as well as 82 Atlas Mind workflow/memory/verification methods. It assigns every record to one primary expert, with nonexclusive secondary lenses. The 63 mirror cards in `data/powers/mental-models.json` are not double-counted. An independent set of 100 persona profiles is consulted only as optional specialist prompts. Counts are not independent agents, live tools, or semantically unique methods. See [the reviewed source audit](../../../docs/BLACK_DRAGON_THINKING_REVIEW_20261106.md).

From the repository root:

```bash
python3 .claude/skills/kosif-black-dragon/scripts/creative_council.py roster
python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py council "اعمل مونتاج درامي من صوت" --out out/creative-council.json
python3 .claude/skills/kosif-black-dragon/scripts/creative_council.py verdict --plan out/creative-council.json --submissions submissions.json --out out/verdict.json
```

There is **no compulsory member quorum, debate-round count, artistic rights seat, rights veto, or forced final vote**. The optional rounds are proposals, cross-examination, and scoring, and may be supplied partly or not at all. Unscored or incomplete opinions stay advisory, without invented winners or evidence. The optional weighted scoring uses only provided criteria and never proves aesthetic merit. A claim of independent expert runs needs corresponding distinct run IDs; simulated or unverified opinions are clearly labelled.

**Safety and action boundary:** no hard artistic censorship or veto seat, but council planning cannot itself pay for tools, upload media or publish anything. Those actions still require the appropriate authorization and actual licence/rights checks at the execution stage. Do not claim a video, preview, independent council debate, or completed media QA from a planning receipt.

Run the quick tests with:

```bash
python3 -m unittest discover -s tests -p test_black_dragon_creative_council.py
```

## The Arena — after the council, when the answer is rejected

The council decides a plan before the work. When the owner rejects a finished answer («الإجابة وحشة»، «خليهم يتنافسوا»، «الحلبة»), use the vendored [arena skill](../arena/SKILL.md) (MIT, Jake Schincariol): the same task, byte for byte, goes to N sub-agents (16 with `--quick`, 100 only when the owner asks), each with a different card (15 reasoning modes × 12 workflows × 12 strategies). They attack each other's solutions, defend and revise, and a judge scores every match on [the rubric](../arena/rubric.md) until one survives; a blind final check compares it with the rejected answer. `bracket.py` keeps the whole bracket in one JSON file, so a compacted context resumes with `bracket.py next`. The orchestrator never judges. The Black Dragon adapter `skill:arena` proves the bracket with stand-in agents and known answers; it does not call a model.


## Book-informed judgment guard (Thinking, Fast and Slow)

A new optional cognitive review is implemented at
scripts/judgment_guard.py and exposed through the Black Dragon CLI:

~~~bash
python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py think-review \
  --input video_brief.json --out out/judgment-review.json

python3 -m unittest discover -s tests -p test_black_dragon_judgment_guard.py
~~~

It uses eleven documented lenses from the 468-page user-supplied edition
of *Thinking, Fast and Slow*: two-system workflow metaphor, hard-question
substitution, missing evidence / WYSIATI, base rates, anchoring, availability,
expert intuition, outside view, premortem, framing and remembering versus
experiencing the edit. It assigns review questions to existing council seats,
without reinstating a rights seat or mandatory debate cycles.

**Important:** This is deterministic, adaptive review planning rather than
a new independent AI reasoner. It does not assert that any video has been
rendered, any audience response measured, or any cognitive bias solved.
See docs/BLACK_DRAGON_KAHNEMAN_THINKING_UPGRADE_20261106.md for source page
numbers, sample inputs, testing and limitations.


## Source-linked external Atlas candidate bridge (2026-11-06)

The **current 525** core/contextual source records remain separately counted and uniquely
assigned to the 12 council seats. A new **non-executing candidate bridge** reads
`docs/atlas_thinking_candidates_20261106.json`, pinned to Atlas commit
`99bb108dff169880dd531359f474a01b73c4b233`, and routes its **26 inspected
source paths** to those same seats, recording an exact byte-duplicate pair. It
does **not** count the sample as complete Atlas coverage.

`scripts/atlas_council_bridge.py` provides **23 locally adapted, source-linked
planning procedures** (nine cognitive-operation labels + fourteen reasoning-pattern
labels) with a primary seat, optional supporting seats, a question, expected evidence,
and a source trace. These are candidate *procedures*, not 23 proven novel mental
models or runnable external agents. They are returned under `external_atlas`
when using `black_dragon.py council`, and appear in each relevant council seat.
They do not inflate `total_source_records=525`, do not fetch third-party code,
and cannot perform autonomous research, execution, or media rendering.

Test the integration from repository root with:

~~~bash
python3 -m unittest discover -s tests -p 'test_black_dragon_atlas_council_bridge.py' -v
python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py council "فكر في سبب مشكلة البرنامج واختر خطة إصلاح" --out out/council-with-atlas.json
~~~

The bridge validates source paths, roles, pinned source commit, and the known
duplicate reference before planning. Title/keyword relevance is only lexical;
semantic de-duplication of all external Atlas skills and end-to-end agent execution
remain separate, uncompleted work. CI must pass before merging to `main`.

## Combined book-to-council thinking integration (PR #238 + PR #233)

The Dragon Mind's **39** new `tfs-*` frameworks from *Thinking, Fast and Slow* are
counted once within the 525 native source records, alongside the 82 existing
contextual Atlas Mind records. The updated book record reports 468 PDF pages
with 584 page-cited insights; the PDF is not committed. Three older frameworks
were also enriched with book references and are not counted again.

The council calls the **existing** `dragon_mind.py scan_traps` function during
planning, rather than approximating its logic. It routes task-linked
questions, correction moves and PDF page citations to each trap's primary
expert and the critic seat, without adding a compulsory quorum or a
rights-only member. The complete summary is returned as
`kahneman_review`; each seat receives `kahneman_review_questions`.
The always-checked WYSIATI, substitution and overconfidence questions are
precautionary **hypotheses**, not proof that a real person or model has a bias.

Together, the external Atlas candidate procedures and book guards are
advisory reasoning scaffolds. They do not claim independently run experts,
actual tool execution or superior results without measured comparisons.
Verify tests on the combined PR head before merging into `main`.


## 3D Build Studio — Blender / Unreal (2026-11-07)

A native planning module, `scripts/build_studio.py`, studied from a public
"Claude Code 3D Build Library" (21 builds, a setup prompt, live mode and
troubleshooting prompts) and **rewritten in our own words and structure** in
`data/build3d_recipes.json`. No prompt is copied verbatim; the source link and
study date are recorded in the file. Reference: `references/3d-build-studio.md`.

It holds **21 recipes** (product turntable, logo reveal, floating island, data
chart, mascot, thumbnail icons, motion loops, iso room, solar lesson, domino
physics, printable minis, floor-plan home, studio set, gallery, OSM
neighborhood, open world, dungeon level, trade booth, event layout, venue pitch,
notes castle) and **18 working principles** (scene-as-script, visual self-check,
plan-then-first-piece, draft-then-final, free assets only, exact-click handoff,
safe fixture first, data-is-truth, swappable slot, options before commit,
multi-format delivery, domain gates, self play-test, explain the choice,
blockout-to-realism, follow-ups as variant axes, attribution and plugin
vetting, live vs background).

```bash
S=.claude/skills/kosif-black-dragon/scripts/black_dragon.py
python3 $S build3d list
python3 $S build3d match "فيديو دوّار لزجاجة عطر"
python3 $S build3d brief product-turntable --fill product="زجاجة عطر 50 مل" --format md
python3 $S build3d lint --text "Make a dungeon level in Unreal"
python3 $S build3d kit          # setup contract, live mode, troubleshooting
python3 -m unittest discover -s tests -p test_black_dragon_build_studio.py
```

- `brief` returns stages, deliverables, domain gates, variant axes and the
  principles applied; big or Unreal builds start with a plan for approval.
  Unfilled inputs stay as open questions and are never invented.
- `lint` checks a user-written 3D prompt for 7 habits (self-check, output
  spec, rebuildable script, stages, free assets, named inputs, options) and
  suggests the missing ones. It is lexical, not a quality score.
- **Limits:** status is `PLANNING_BRIEF_NOT_A_RENDER`. Nothing launches
  Blender or Unreal, downloads assets or spends money. Rendering happens only
  with the owner's app and approval, and must then pass the brief's gates
  with real frames before anything is called done.

## Code-Motion Style Studio (2026-11-07)

A second native module, `scripts/motion_styles.py`, studied from a public
motion-graphics style library (7 code-drawn styles, its storyboard and
voiceover options and its clone-from-screenshot flow) and **restated in our
own words** in `data/motion_styles.json` (no prompt text or reference source
copied; the site's prompts sit behind its own sign-up). It holds **7 style
cards** (creator motion, chalk talk, clean tech, software walkthrough, data
story, warm canvas, pop info) and **16 principles** (frame is a function of t,
seeded randomness, one timeline for picture and sound, engine-vs-story
contract, storyboard gate, word-timed voiceover, mix discipline, phone
legibility floor, frame budget, deterministic render, pace contract, one job
per color, safe proof shots, clone the style not the content, assumptions
ledger, ask for missing inputs).

```bash
S=.claude/skills/kosif-black-dragon/scripts/black_dragon.py
python3 $S motion match "شرح برنامج خطوة بخطوة"
python3 $S motion brief data-story --topic "نمو المبيعات" [--srt voice.srt] [--direct]
python3 $S motion clone-plan --topic "عادات النوم"
python3 $S motion vo-timeline --srt voice.srt --out out/words.json
python3 $S motion cue-check --cues cues.json [--speech out/words.json]
python3 -m unittest discover -s tests -p test_black_dragon_motion_styles.py
```

- `vo-timeline` really computes word timings from an SRT (line cues are
  spread by word length) and the duration (last word + 1.2 s).
- `cue-check` really checks a cue list against the mix rules (≤3 at once,
  ticks ≤12/s, booms for 2–3 moments, quiet before the biggest hit; with a
  voiceover: small sounds soft, no riser or drone under speech). It reads cue
  names and times, not audio, and exits 3 when a rule fails.
- **Limits:** briefs are `STYLE_BRIEF_NOT_A_RENDER`. `kosif-web-film` and
  `tools/render_html.cjs` stay the renderers.


## Wired into the Black Dragon engine (2026-11-07)

The council is now a registered program of the main engine
(`kosif-superpowers/scripts/black_dragon.py`), not just a file in the repo:

- **Adapter `skill:kosif-black-dragon`** (recipe `creative-council` in
  `_black_dragon_skill.py`). `black_dragon.py run ... --execute-adapters` convenes the
  council on the task twice and checks: 12 distinct seats, all 525 records with one
  primary seat each, a stable fingerprint, 31 Kahneman traps loaded with the three
  System 2 gates routed to the critic, 23 Atlas procedures routed to seats, the
  11-lens `think-review`, and a known-answer verdict (the clearly better route must
  win; a fake `INDEPENDENT` claim without run IDs must be refused).
- **`compose`** now returns `thinking_guards`: Dragon Mind's real `scan_traps` on the
  task, with question, debiasing move, book pages and reviewing seats.
- **`think-review`** now adds `book_trap_scan` (the full 31-trap scanner) next to the
  11 fixed lenses.
- The **`dragon-mind`** adapter now also checks the book: the always-on gates are in
  the plan, a planted anchor is caught with pages 103–108, and page 69 is served
  from the 468-page record.

Try it:

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/_black_dragon_skill.py creative-council out/cc.json --task="اختار أفضل خطة مونتاج"
~~~

These are still planning and scoring steps: no agent, model, media or paid tool runs.
