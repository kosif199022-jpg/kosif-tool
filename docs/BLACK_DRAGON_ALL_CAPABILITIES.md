# KOSIF Black Dragon — التنين الأسود / Full Catalog Activation

**Invocation:** «استدعِ التنين الأسود» or «شغّل التنين الأسود». The owner's rule: **every capability is used, none is left out; the dragon's intelligence decides how and where each one is used.** The existing `kosif-web-film` remains the separate code-drawn video director; Black Dragon is an **orchestrator**, not a film renderer.

## What it uses (7,383 entries on 2026-11-01)

`black_dragon.py inventory` counts every type, failing loudly on duplicates:

| kind | source | today |
|---|---|---:|
| skill | every `SKILL.md` under `.claude/skills/` | 473 |
| power | `data/powers/*.json` | 5,860 |
| tool | `data/tools.json` | 205 |
| superpower | `data/superpowers.json` (fused powers) | 483 |
| style | `catalog/styles.json` (motion style atlas) | 297 |
| playbook | `playbooks/*.md` | 19 |
| protocol | `PROTOCOL.md` + `references/protocol/A*.md` | 46 |

## How the brain decides "how" (`_black_dragon_brain.py`)

For the task it gives **every** entry:

- **part** — one of the seven stages of the capability mind map (`data/capability_mindmap.json`): افهم، خطّط، اصنع، حسّن، جمّع وارندر، تحقّق، سلّم.
- **mode** — `execute` (a reviewed adapter runs it), `run-tool`, `follow-skill`, `apply-method`, `protocol-rule`, `visual-reference` or `quality-gate`.
- **weight** — `lead` (the top 5 of its part for this task), `core` (shares words with the task) or `support` (still assigned, never dropped).
- **application** — one line saying what it does for this task.

Relevance orders and weights; it never removes. Adapter `depends_on` lists build dependency waves (Kahn order), and an entry whose prerequisite did not execute is blocked, not run. The brain is deterministic and lexical, not an LLM; the same task gives the same `assignment_sha256`.

## Evidence tiers (never mixed)

| tier | meaning | how |
|---|---|---|
| assigned | in the plan with part, mode, weight; one line in `briefs.jsonl` with the SHA-256 of its source file | always, all entries |
| probed (static-only) | AST parses an argparse CLI declaration without importing or running the module; **not** proof of startup | `--probe-tools` |
| executed | a reviewed adapter ran on the task, exit 0, nonempty artifact, SHA-256 receipt checked | `--reviewed-adapters` or `--adapters FILE`, plus `--execute-adapters` |
| validated (separate) | **structural card validation, not execution**: the card passed real per-kind checks (fields, cross references, referenced files) with one receipt line in `validation.jsonl` | `--validate-cards` on `run`, or `black_dragon.py validate [--out out/...]` |
| applied (separate) | **a method card applied to the task by a generic applier, not execution**: an adapter whose script is `kosif-dragon-mind/scripts/card_apply.py` (or that sets `"method_applier": true`) wrote a task-specific procedure with a receipt. The ledger keeps it `blocked` with `applied_receipt`, `blocked_why.method_applied` counts it, and it never adds to `executed` or `full_coverage` | `run --adapters FILE --execute-adapters` with an applier file; the report line «method cards applied (NOT execution)» |

`full_coverage=true` needs **every** entry executed with a receipt, so today the run honestly exits 4. Assigned, probed and validated are never reported as executed, and validation never changes the executed count or `full_coverage`.

### Structural card validation (`validated`, `_black_dragon_validate.py`)

Most entries (7,157 on 2026-11-03) are written methods with no program, so they can never honestly be executed. This tier checks every one of the cards instead, with a receipt per card: `entry`, `source_sha256` (the file it comes from), `card_sha256` (its record), the `checks` run, the `problems` found and `status` (`validated` / `invalid`). The job also gets `validation_summary.json` with the SHA-256 of `validation.jsonl`, and the report adds the line «validated: N/total (invalid: M)», labelled as structural card validation.

| kind | what is checked |
|---|---|
| power | required fields present, key strings non-empty, list types, unique id, status and `proof_scope` enums, family equals its file, proven has a proof; every `kosif-tool/…` proof path exists (a `:line` reference must be inside the file), every `style:` proof and `styles` entry names a real style, every `requires` key is in `data/requirements.json` |
| superpower | fields; every fused component power exists and its status matches the power; no component twice; `size`, `status_mix` and `families` equal what the components really are; twins and linked superpowers exist; requirements and proof paths as for powers |
| tool | fields; kind and root enums; the program path exists; every listed test and doc exists; `power_id` and families exist; a CLI documents a command |
| skill | `SKILL.md` has a YAML frontmatter block that parses (PyYAML when installed) with `name` and `description`; every relative markdown link outside code resolves |
| style | the repository's own style schema (`tools/validate.py`): enums, known categories, https URLs, `styles/<id>/SKILL.md`, `STYLE.json` parses and equals the catalog record, listed playbooks and brief exist |
| playbook / protocol | readable, non-empty, has a heading, relative links resolve; the core `PROTOCOL.md` lists its appendices in the trigger table and each one exists |

Proofs in the owner's other repositories, URLs, owner uploads and session receipts cannot be checked from this copy: they are counted under `external_refs_not_checkable` and never make a card more than structurally valid. `verify --job` re-hashes `validation.jsonl` against the summary, checks one receipt per catalog entry and re-hashes every validated source, so an edit after validation or a forged receipt fails the audit.

Measured on 2026-11-03 (about 1.3 s for the whole catalog): **7,339 of 7,392 validated, 53 invalid**, all of them skills: 48 vendored KOSIF Atlas skills whose relative links point at upstream files that were not copied (`../../agents/…`, `../../context/…`, sibling plugin folders; 4 of them also have no `name` in their frontmatter), 4 vendored skills whose frontmatter is not valid YAML (an unquoted `: ` inside a value: three of the 100 Super Skills and the Atlas `instruction-audit`), and `editorial-film-edit`, whose `SKILL.md` links `references/*.md` files that are not in the repository. Powers, superpowers, tools, styles, playbooks and protocol rules all validated. The vendored folders are copied verbatim with SHA-256 manifests, so they are reported, not edited.

## Try it (from repo root)

```bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py inventory
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py plan "اعمل مونتاج ريلز بصوت"
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "اعمل مونتاج ريلز بصوت" \
  --job out/black-dragon/<unique-job> --workers 8 --probe-tools --reviewed-adapters --execute-adapters
```

The job folder gets `black_dragon_report.md` (Arabic/English summary), `black_dragon_report.json`, `black_dragon_plan.json`, `briefs.jsonl`, `all_skills_ledger.json`, `all_skills_report.json`, `receipts/`, `artifacts/` and `probes/`. Historical pre-hardening measurement (2026-10-31, when --help actually executed): 7,377 assigned, 186 of 204 tools started, 24 of 24 reviewed adapters executed with receipts, 0 failed, about 12 s.

### Reviewed adapters

`data/black_dragon_adapters.json` holds 39 read-only repo tools (brief, hub find, discovery, routers, thinking, council and gate self-tests, export standard, agent-guard rules, evidence audit, and since USIP v6.5 the capability atlas, power and superpower suggestions, requirement plans, style and drawing finders, superskills and source scouts…) run on the task through `scripts/_black_dragon_exec.py`, which keeps the tool's own exit code and writes its stdout as the artifact. To connect more, map an **exact catalog entry ID** to a repo-relative Python script and its argv:

```json
{
  "tool:YOUR_REAL_TOOL_ID": {
    "script": ".claude/skills/kosif-superpowers/scripts/_black_dragon_exec.py",
    "args": ["{artifact}", "path/to/tool.py", "--task", "{task}"],
    "depends_on": ["tool:skill-intelligence"]
  }
}
```

### Media adapters (video and audio tools that really run)

Eight more adapters (`"media": true`) run the production tools on real footage through `scripts/_black_dragon_media.py RECIPE {artifact} --media={media}`:

| entry | recipe | what runs | checked |
|---|---|---|---|
| `tool:music-rhythm-engine` | rhythm | audio_cue_mapper → music_rhythm_engine: tempo and beat grid | grid written; self-test tempo 120 ±3 BPM |
| `tool:audio-cue-mapper` | audio-cues | onsets and RMS energy curve | self-test finds its 12 clicks ±1 |
| `tool:cinema-lab` | cinema | vid.stab stabilize, teal-orange LUT grade + `.cube`, tracked 16:9 → 9:16 reframe | outputs probed; reframe is 9:16; self-test shake goes down |
| `tool:montage-pro` | montage | intake (loudness, cuts, energy cues) + build options; calm vs peak seconds | cues measured |
| `tool:verify-video` | verify | delivery checks (codec, fps, aspect, loudness, true peak) | checks evaluated; failed checks are reported as findings |
| `tool:video-eyes` | eyes | contact strip, onion skin, frozen spans, clipping flags | report files written; flags are findings |
| `tool:look-pipeline` | look | every look vs its reference maths, then a cinematic grade | all looks match; output probed |
| `tool:fast-edit` | cut | frame-exact cut | output length matches ±0.1 s |

Pass your file with `black_dragon.py run ... --media FILE` (never modified; its SHA-256 goes in the report). Without `--media` each adapter first renders a **self-test clip with known answers** (120 BPM clicks, shaking camera, colour bars) and its artifact says `"kind": "self-test"`, so CI proves the tools work without pretending it edited your footage. Every output stays in the artifact's `.work` folder inside the job; a tool error or a failed required check exits non-zero, so it can never be counted as executed. Long footage needs a larger `--timeout` (a 62 s 720p clip took about 6 minutes for all eight).

Kling 3.0 / Higgsfield are **not** adapters: they spend credits and run through the Higgsfield connector only after the owner sees the exact price and approves.

### Skill adapters (skills that ship a program)

Of 478 skills (counted 2026-11-03), most are written methods with no code; 28 ship an argparse program, and 27 of them are now adapters (`"skill_program": true`) run through `scripts/_black_dragon_skill.py RECIPE {artifact} --task={task} [--media={media}]`:

| entry | recipe | what runs | checked |
|---|---|---|---|
| `skill:…/prompt-master-pro` | prompt-master | prompt_build from the task (+tests, A/B variants, blind spots), then prompt_lint | lint verdict given; the task is inside the prompt |
| `skill:…/prompt-architect-reasoning-models` | prompt-architect | injection_shield writes its 20 attack test cases; prompt_frontier analyses the task | 20 cases written; analysis returned |
| `skill:kosif-reel-hooks` | reel-hooks | scores the task as an opening hook | score returned |
| `skill:…/excel-automation-power` | excel-lambdas | workbook of named LAMBDA functions | ≥10 functions; a real xlsx |
| `skill:…/kosif-social` | social | platform limits + post pack measured from the video | three platforms; video measured |
| `skill:…/pro-video-editor-ffmpeg` | video-editor | probe + beat-cut points | self-test tempo 120 ±3 BPM |
| `skill:…/motion-director-pro` | motion-energy | per-frame motion energy and still spans | frames measured; self-test is never still |
| `skill:…/image-prompt-forge` | image-prompts | prompts for 6 image models from the task, then a spec with 3 planted flaws | 6 platforms; task inside; all 3 planted flaws caught |
| `skill:…/video-prompt-director` | video-prompts | shot prompts for 7 video models, then shots with 3 planted flaws | 12 s shot clamped to Veo 8 s / Kling 10 s; all 3 flaws caught |
| `skill:…/excel-model-architect` | excel-model | 3-statement model, audit, then audit of a copy with a planted constant | PnL/CF/BS/Checks; no hard-coded numbers; planted constant reported |
| `skill:…/excel-power-formulas` | excel-check | xlsx_check on a clean workbook and on one with planted flaws | clean passes; NOW/OFFSET and number-as-text found |
| `skill:…/llm-judge-eval-lab` | judge-eval | scores fixed test judges; regression gate | hand-computed answers (8.0, 5.4, 6.96, not passed); gate exit 3 |
| `skill:…/audio-reactive-captions-studio` | captions-audio | task words to caption pages + SRT/VTT/ASS; per-frame audio energy | every word kept; self-test tempo 120 ±3 BPM |
| `skill:kosif-upload-link` | upload-join | joins 3 upload parts, then with one part deleted | sha256 identical; missing part refused |
| `skill:living-site` | credit-ledger | credit ledger with test entries | double billing refused; over-budget blocks (no credits spent) |
| `skill:kosif-shadow-theatre` | shadow-theatre | check, stills, 22 s preview render, analyze the input | planted gap + missing memorable caught; stills not flat; duration 22 s with sound |
| `skill:kosif-web-film` | web-film | plan, scaffold, check; World Film example, check, build (structure only, no video render) | check passes; planted gap + uncovered requirement caught; World Film example passes and 3 planted breaks (said-and-typed text, small type, dead camera stop) caught |
| `skill:kosif-infinite-matrices` | causal-laws | reruns the elastic-memory law, verifies, tampers a frame | recorded effect 0.097492994 reproduced exactly; tamper detected |
| `skill:kosif-instagram-video-research` | reel-research | search links (no network), index, review, export | foreign link refused; only the reviewed reel exported |
| `skill:kosif-voice-studio` | voice-check | self-test, engine doctor, audio verify | duration matches ffprobe; planted silence rejected (speech needs an engine) |
| `skill:…/claude-animation-studio` | animation-qa | frame QA on the first 8 s, then frames with a planted freeze and black frame | both planted problems caught |
| `skill:…/hyperframes-animation-studio` | hyperframes-beats | motion.py beats + motion measure | self-test 120 ±3 BPM and never still |
| `skill:…/kosif-montage-motion` | montage-tools | probe, 9:16 reframe, silence cut on a planted clip | 1080x1920; silence found at 1.0 s |
| `skill:…/kosif-mimic` | mimic-analyze | mm_analyze on a known-cut clip, then on the first 20 s of the input | exactly 2 shots and the hard cut at 3.0 s |
| `skill:…/pixel-studio-painter` | pixel-painter | film.py paints a known SVG pixel by pixel; judge.py rates it | final centre red and background blue; first frame not yet painted |
| `skill:kosif-kling-director` | kling-director | kling_director.py builds a Kling 4.0 prompt pack from the task (master prompt + 3x3 storyboard per block, plan.json), then lints a known clean story and a copy with 4 planted mistakes | 45 s = 0-23 + 23-45 s; clean story PASS; polish, brands, Arabic dialogue and a clock gap all caught; text only, 0 credits |
| `skill:kosif-dragon-mind` | dragon-mind | dragon_mind.py runs its six-step think cycle (frame, explore, decide, build, verify, learn) on the task, twice, and on a different task | one tier per catalog entry; T4 = the reviewed registry; every graph node typed with champions; same task = same digest, different task = different digest; a planner, executes nothing |

Where a skill's script is a checker, the recipe also feeds it a copy with a planted mistake: a checker that misses a known mistake earns no receipt (tested). One skill ships a program that cannot run here and says why in its blocked reason: `davinci-resolve-pipeline` needs the DaVinci Resolve app and its scripting API. `kosif-mimic`'s blur fallback was fixed for Pillow 12 (which refuses GaussianBlur on float images); it and `pixel-studio-painter` need OpenCV, which the Black Dragon CI job installs. Finding: `studio.py --code FILE --render PNG` renders the default scene and ignores the code, so the adapter uses `film.py drawing`.

The injection suite only *writes* attack cases for testing a model; it is not a model test by itself.

### Tool adapters (every registered program has its own runner)

The tool registry (`data/tools.json`) lists 208 programs. 47 of them have the hand-written adapters above; the other 161 now go through `scripts/_black_dragon_tool.py TOOL_ID {artifact} --task={task}` (`"tool_suite": true`), and 158 of those earn receipts:

* **own-test-suite (147 tools):** the tool's registered test files run against its real code, each in its own subprocess, from the repository root, with `TMPDIR` inside the job. Python files run under unittest, JavaScript files under `node --test`, plain test scripts must exit 0 and print their cases, and a documented `--self-test` runs too. A pass needs, for every file: it names the tool's script, at least one test really ran (a suite that skips everything does not count), and the runner reported OK. A registered test file that never names the tool is listed as `unrelated_tests_not_run` and proves nothing; a tool with no test file and no recipe is refused (exit 2).
* **known-answer recipe (11 tools with no tests):** `scripts/_black_dragon_tool_recipes.py` builds a fixture inside the job, runs the real tool on it and checks the answer it must give: `atlas-transfer` (5 verifier rows, each with a known fate), `atlas-review-summary` (only the eligible methods; wrong schema refused), `build-chapters` (byte-identical chapter; planted stale chapter caught), `relabel-proofs` (8 paths with known proof scopes), `protocol-lint` (clean fixture release passes; three planted drifts caught as S, T, C), `probe-env` (Python version and ffmpeg/git/node presence match this machine), `collect-links` (real Chromium on a local page; mailto dropped; `--filter`), `render-text` (Arabic through Chromium; ink measured), `color-media` (oil painting of a red disc on blue; colours measured), `repo-build` (`tools/build.py --check`), `starter-remotion` (Remotion bundles the starter and lists exactly one composition, `KosifFilm` at 30 fps, 1080x1920, 360 frames; frames 0 and 60 render in headless Chromium to non-blank 1080x1920 PNGs that differ; `tsc --noEmit` passes; planted flaw: an unknown composition id is refused and writes nothing).

These runners say `"mode": "own-test-suite"` or `"known-answer-recipe"` in their artifact: they prove the tool's code works on this machine now, **not** that it was run on the task text. While wiring them up, 11 registry entries got the real tests that already existed for them, and one real bug was fixed: `collect_links.js` used `require()` inside the repository, whose `package.json` says `"type": "module"`, so it crashed on every call; it now loads Playwright with `import()` and runs both inside the repo and in the standalone skill.

**Blender and Remotion without the apps (2026-11-03).** `blender-rescue-scene` and `blender-cat-fur-upgrade` now run their 10 real tests (`scripts/test_blender_cat_fur_upgrade.py`) under the official `bpy` module from PyPI (`pip install bpy`, Blender 5.2 built as a Python module; it needs CPython 3.13) when no `blender` binary is present: the same scripts run as `python3 SCRIPT -- ARGS`, and the tests check the 56-object, 24-frame Cycles base scene, exactly 320 fur strands and 6 whiskers at seed 2307, 64+ objects, preserved motion, and three planted flaws (existing output, already-upgraded source, fur count 20000) that must be refused. Without the Blender app and without `bpy` every test skips, and the runner then fails instead of passing. `starter-remotion` needs `npm ci` in `starters/remotion` (its `node_modules/` is gitignored, never committed); without it the recipe's first check fails. `remotion.config.ts` now also finds the newer Playwright Chromium layout (`chrome-headless-shell-linux64/`) and `~/.cache/ms-playwright`, so Remotion uses the local headless shell instead of downloading one. Installing `bpy` also wakes the Blender suites that were skipping before (`blender-cinema` renders real Cycles stills and an orbit through it and needs `libegl1`); two plain-Python checks that assumed no `bpy` were fixed: the rescue/fur scripts answer `--help` without Blender, and the `blender_worker.py` outside-Blender test runs with `python3 -S`.

Three programs cannot earn a receipt here and say why in their blocked reason (`TOOL_BLOCKERS` in `black_dragon.py`): `rea-owned-repo-batch` and `rebalance-creative-repos` work on the owner's GitHub repositories over the network, and `repo-ashell-cinema` is an a-Shell script for the iPhone. The Black Dragon CI job installs what the runners need (Python 3.13 for `bpy`, Node 22, Playwright Chromium, ffmpeg, fonts, the Python packages including `bpy`, and `npm ci` in `starters/remotion`) and runs with `--timeout 1200`; the slowest suite (`fusionforge`) takes about 3.5 minutes.

### Why the rest stay blocked

The report's `blocked_why` splits the blocked entries: `method_description` (powers, skills without code, styles, playbooks, protocol rules, superpowers: written methods applied in the plan through `briefs.jsonl`, never counted as executed, because there is no program to run), `tool_without_adapter` (registered programs that still need a reviewed adapter) and `skill_program_without_adapter` (skills whose folder ships an argparse Python script with no adapter yet). The last two are the honest backlog. Measured on 2026-11-03 on a real 62 s clip: 7,391 entries, 227 of 227 adapters executed (47 hand-written tool adapters + 155 tool runners + 25 skills), 0 failed; blocked 7,157 method descriptions + 6 tools + 1 skill whose programs cannot run here (Blender, Remotion, the owner's GitHub over the network, the iPhone script, DaVinci Resolve). Before the tool runners the same run executed 72 of 72 with 161 tools blocked. After the Blender/Remotion unblock and the Kling director skill (pro-max, self-test clip, `--validate-cards`): 7,393 entries (with Dragon Mind from main), **232 of 232** adapters executed, 0 failed; blocked 7,157 method descriptions + 3 tools (the owner's GitHub over the network, the iPhone script) + 1 skill (DaVinci Resolve); structural card validation 7,340 validated / 53 invalid (separate tier, not execution); `verify` integrity passed for both audits.

Execution is **explicitly opt-in**. Keep network calls, paid services, deployment, installation and uploads out of adapters unless the owner authorises them separately. No shell string is built from user text. Adapters run with the local user's permissions; this is not a sandbox, so review them.

## Limits

- A power card that is documentation has no command; it is assigned and briefed, not executed.
- Session connectors (MCP servers such as Higgsfield or Suno) are not in the repository inventory and are never called by Black Dragon.
- The audit cannot certify artistic quality or what a third-party executor really did.
- Cinema Pro and `kosif-web-film` remain the renderers for real montage; Black Dragon does not make an MP4 by being invoked.

### Tests

```bash
python3 -m unittest discover -s tests -p 'test_black_dragon*.py' -v
```

They cover inventory of every kind against its sources, part/mode/weight for every entry, determinism, dependency waves and blocked dependents, explicit execution gating, unsafe paths, job reuse, the AST-only (no-execution) CLI probe, the exec wrapper's exit code and a real run of reviewed adapters with checked receipts. The `Black Dragon checks` workflow also runs a full job on every pull request and uploads its receipts.

## In the USIP pipeline (v6.5, appendix A49)

The dragon is no longer only a named command. At L3 it runs right after the USIP brief with `--probe-tools --reviewed-adapters` (assigned + probed); when the owner answers `نفّذ بأقصى قوة` it also gets `--execute-adapters`, since every reviewed adapter only reads. Each stage leader that would change the engine or the verification method goes into plan C, and the report carries one line: assigned · probed · executed with receipt · `full_coverage`. Historical pre-hardening measurement on 2026-11-01: 7,381 assigned, 187 of 205 tools probed, 39 of 39 adapters executed with receipts, 0 failed.


## Full-tool activation: inspect first, then schedule (proposed unified version)

The following read-only mode scans the **entire capability catalog**, statically
checks **every registered tool's metadata and local source**, and writes a
dependency-ordered usage plan. It does **not** run any of those tools.

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py activate \
  "اعمل فيديو سينمائي مع مراجعة الجودة" --selection all \
  --out out/black-dragon/full-tools-plan.json
~~~

The alternative is --selection smart: it still inspects the entire catalog,
but chooses a focused set of reviewed adapter candidates. --selection all
selects all reviewed adapters, not all arbitrary Python files. Both modes
assign every catalog item a workflow stage.

The JSON file contains a purpose and static source SHA-256 for every
registered tool, path/metadata errors, readiness labels, risk declarations,
dependency waves, a five-perspective council **plan**, a plan SHA-256,
and the explicit human approval gate. No approval is granted by mode choice.
"Inspected" means the local source and registry entry were found, **not**
runtime functionality. "Candidate" means its reviewed manifest can be
scheduled, **not** that it has executed successfully or is free of risk.
Unreviewed capabilities stay represented as knowledge, references, or
protocol requirements, and must not be counted as executed adapters.

The proposed workflow is: request -> ALL tool metadata and sources inspected ->
stage assignments -> dependency waves and council prompts -> review + explicit
approval -> separately authorized execution -> receipt/evidence verification.
Never claim independent council reviewers actually ran without their genuine
outputs. For actual execution use the pre-existing reviewed, approval-gated
execution path, not the static activation command.

Tests:
~~~bash
python3 -m unittest tests/test_black_dragon_brain.py -v
~~~


## Skill linkage audit (v1.6): do all catalog entries have real skills?

\`capability_graph.json\` was originally a **power-family → script/test** graph, not
a skill-to-capability linkage graph; its absence of explicit skill nodes is not
evidence that every catalog capability is routed to an installed skill.

The new **complete ownership audit** provides an explicit link for **every**
item in \`black_dragon.full_inventory()\` to a real installed
\`skill:kosif-superpowers\` file. Each skill also links to its own \`SKILL.md\`.
It validates every capability source path and its existence, blocks traversal
and symlink sources, and reports any missing source or orphan. The ownership
map is attached to the output of \`black_dragon.py activate\`, so the full
activation plan contains individual \`skill_links\` for every item.

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py links
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py links \
  --out out/black-dragon/skill-links.json
~~~

The first prints an independent summary; the second writes the full
capability-to-skill index and its deterministic SHA-256. These are read-only
audits, and the output filename must be new.

**Three different claims must not be confused:**

1. **Central skill ownership (verified by paths):** each catalog item has the
   installed KOSIF Superpowers controller as its owner. That is a real
   organizational link, *not* proof every item runs.
2. **Specialist skill relationship (suggested):** where at least two distinct
   specialist-name tokens match the capability's metadata, the audit records
   up to three candidates with \`suggested_not_verified\`. The model/user must
   still inspect the specialist's instructions, inputs, permissions and tests.
   Items with no specialist match are counted explicitly.
3. **Actual execution (independently evidenced):** still needs a reviewed
   adapter, permission gates, task outputs and receipts; merely adding a link
   never upgrades a documented power into an executable tool.

CI enforces **zero missing sources and zero orphan ownership links** on the
real catalog. It does **not** imply that all 7,383 entries have 473 distinct,
validated specialist mappings or runnable implementations.


## Owner-approved roadmap (2026-11-02)

The owner approved all 100 decisions in
[BLACK_DRAGON_100_DESIGN_DECISIONS.md](BLACK_DRAGON_100_DESIGN_DECISIONS.md)
with a specific override to Q4: **FULL means a goal to run ALL registered
tools and apply EVERY installed skill appropriately**. The owner additionally
approved all 200 decisions Q101–Q300 in
[BLACK_DRAGON_200_MORE_DECISIONS_101_TO_300.md](BLACK_DRAGON_200_MORE_DECISIONS_101_TO_300.md).

These 300 approved decisions are a prioritized **roadmap**, not 300 features
already implemented. There is no permission for unauthorized file writes,
external publishing, paid API calls or unreviewed script execution.

The inspect-first ALL activation includes:

- One tool entry per registered tool, including those lacking adapters.
- A complete skill-usage plan (all installed skills, each with a task stage).
- A deterministic, per-tool **qualification backlog**:
  source missing/unsafe -> repair registry; bad reviewed adapter or dependency ->
  repair/test; no reviewed adapter -> design, review and separately test one.
- Every unqualified tool reports unqualified_not_executed and an action.
  The all_tools_executed and all_skills_applied fields remain false until real
  execution and application evidence exist.

Next phases: (1) qualify additional read-only adapters in measured batches,
(2) verify specialist skill-to-capability links, (3) enable task-scoped,
permission-gated execution and collect per-tool receipts, (4) expand domain
integrations with their own sandboxing and authorization checks. CI must pass
before merging any phase.

## 2026-11-03 security and QA remediation (follow-up to PR #207)

- **--probe-tools is now AST-only:** it parses local Python CLI files and writes `static-only` evidence; no Python subprocess is launched. Import-time code is not safe merely because a file contains `argparse`. `probe_passed` is therefore zero unless a *separate, future reviewed* executable probe is introduced. This change deliberately reduces apparent runtime readiness without losing real adapter execution.
- **Financial models:** numeric literals inserted into the calculated PnL, BS, CF or Checks grid are now HIGH findings, increase `hardcoded`, and fail the audit. Genuine input numbers belong in Assumptions/Inputs.
- **Pixel Studio:** headless `--code SOURCE.svg --render OUTPUT.png` and scene JSON render the specified data source. Headless Python source is explicitly rejected rather than executing untrusted code or silently rendering the default scene; interactive Python still requires the existing trust prompt.
- **KOSIF Mimic:** translation-compensated verification suppresses handheld camera shake masquerading as shot changes; gradual transitions with confidence below 0.20 are not published as real edits.
- **beat_cuts:** avoids publishing BPM from a single lucky histogram bin; requires repeatable onset intervals and coherent phase, and returns `null` when no steady tempo is supported. Different analyzers may still disagree on ambiguous audio; neither produces a verified musical BPM.
- Regression tests: `tests/test_black_dragon_quality_regressions.py` creates local synthetic malicious CLI, formula-overwrite workbook, SVG, translated frames and irregular/click onsets without network or paid providers.
