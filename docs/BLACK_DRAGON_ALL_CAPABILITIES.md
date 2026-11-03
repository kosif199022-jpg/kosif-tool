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
| probed | a CLI tool with argparse answered `--help` on this machine (it starts and its imports load) | `--probe-tools` |
| executed | a reviewed adapter ran on the task, exit 0, nonempty artifact, SHA-256 receipt checked | `--reviewed-adapters` or `--adapters FILE`, plus `--execute-adapters` |

`full_coverage=true` needs **every** entry executed with a receipt, so today the run honestly exits 4. Assigned and probed are never reported as executed.

## Try it (from repo root)

```bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py inventory
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py plan "اعمل مونتاج ريلز بصوت"
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "اعمل مونتاج ريلز بصوت" \
  --job out/black-dragon/<unique-job> --workers 8 --probe-tools --reviewed-adapters --execute-adapters
```

The job folder gets `black_dragon_report.md` (Arabic/English summary), `black_dragon_report.json`, `black_dragon_plan.json`, `briefs.jsonl`, `all_skills_ledger.json`, `all_skills_report.json`, `receipts/`, `artifacts/` and `probes/`. Measured on 2026-10-31 in a cloud container: 7,377 assigned, 186 of 204 tools started, 24 of 24 reviewed adapters executed with receipts, 0 failed, about 12 s.

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

Of 473 skills, 443 are written methods with no code. The rest ship scripts, and 25 of them are now adapters (`"skill_program": true`) run through `scripts/_black_dragon_skill.py RECIPE {artifact} --task={task} [--media={media}]`:

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
| `skill:kosif-web-film` | web-film | plan, scaffold, check (structure only, no video render) | check passes; planted gap + uncovered requirement caught |
| `skill:kosif-infinite-matrices` | causal-laws | reruns the elastic-memory law, verifies, tampers a frame | recorded effect 0.097492994 reproduced exactly; tamper detected |
| `skill:kosif-instagram-video-research` | reel-research | search links (no network), index, review, export | foreign link refused; only the reviewed reel exported |
| `skill:kosif-voice-studio` | voice-check | self-test, engine doctor, audio verify | duration matches ffprobe; planted silence rejected (speech needs an engine) |
| `skill:…/claude-animation-studio` | animation-qa | frame QA on the first 8 s, then frames with a planted freeze and black frame | both planted problems caught |
| `skill:…/hyperframes-animation-studio` | hyperframes-beats | motion.py beats + motion measure | self-test 120 ±3 BPM and never still |
| `skill:…/kosif-montage-motion` | montage-tools | probe, 9:16 reframe, silence cut on a planted clip | 1080x1920; silence found at 1.0 s |
| `skill:…/kosif-mimic` | mimic-analyze | mm_analyze on a known-cut clip, then on the first 20 s of the input | exactly 2 shots and the hard cut at 3.0 s |
| `skill:…/pixel-studio-painter` | pixel-painter | film.py paints a known SVG pixel by pixel; judge.py rates it | final centre red and background blue; first frame not yet painted |

Where a skill's script is a checker, the recipe also feeds it a copy with a planted mistake: a checker that misses a known mistake earns no receipt (tested). One skill ships a program that cannot run here and says why in its blocked reason: `davinci-resolve-pipeline` needs the DaVinci Resolve app and its scripting API. `kosif-mimic`'s blur fallback was fixed for Pillow 12 (which refuses GaussianBlur on float images); it and `pixel-studio-painter` need OpenCV, which the Black Dragon CI job installs. Finding: `studio.py --code FILE --render PNG` renders the default scene and ignores the code, so the adapter uses `film.py drawing`.

The injection suite only *writes* attack cases for testing a model; it is not a model test by itself.

### Tool adapters (every registered program has its own runner)

The tool registry (`data/tools.json`) lists 208 programs. 47 of them have the hand-written adapters above; the other 161 now go through `scripts/_black_dragon_tool.py TOOL_ID {artifact} --task={task}` (`"tool_suite": true`), and 155 of those earn receipts:

* **own-test-suite (145 tools):** the tool's registered test files run against its real code, each in its own subprocess, from the repository root, with `TMPDIR` inside the job. Python files run under unittest, JavaScript files under `node --test`, plain test scripts must exit 0 and print their cases, and a documented `--self-test` runs too. A pass needs, for every file: it names the tool's script, at least one test really ran (a suite that skips everything does not count), and the runner reported OK. A registered test file that never names the tool is listed as `unrelated_tests_not_run` and proves nothing; a tool with no test file and no recipe is refused (exit 2).
* **known-answer recipe (10 tools with no tests):** `scripts/_black_dragon_tool_recipes.py` builds a fixture inside the job, runs the real tool on it and checks the answer it must give: `atlas-transfer` (5 verifier rows, each with a known fate), `atlas-review-summary` (only the eligible methods; wrong schema refused), `build-chapters` (byte-identical chapter; planted stale chapter caught), `relabel-proofs` (8 paths with known proof scopes), `protocol-lint` (clean fixture release passes; three planted drifts caught as S, T, C), `probe-env` (Python version and ffmpeg/git/node presence match this machine), `collect-links` (real Chromium on a local page; mailto dropped; `--filter`), `render-text` (Arabic through Chromium; ink measured), `color-media` (oil painting of a red disc on blue; colours measured), `repo-build` (`tools/build.py --check`).

These runners say `"mode": "own-test-suite"` or `"known-answer-recipe"` in their artifact: they prove the tool's code works on this machine now, **not** that it was run on the task text. While wiring them up, 11 registry entries got the real tests that already existed for them, and one real bug was fixed: `collect_links.js` used `require()` inside the repository, whose `package.json` says `"type": "module"`, so it crashed on every call; it now loads Playwright with `import()` and runs both inside the repo and in the standalone skill.

Six programs cannot earn a receipt here and say why in their blocked reason (`TOOL_BLOCKERS` in `black_dragon.py`): `blender-cat-fur-upgrade` and `blender-rescue-scene` need the Blender app (every test skips without it), `starter-remotion` needs an npm install of Remotion and its headless Chrome, `rea-owned-repo-batch` and `rebalance-creative-repos` work on the owner's GitHub repositories over the network, and `repo-ashell-cinema` is an a-Shell script for the iPhone. The Black Dragon CI job installs what the runners need (Node 22, Playwright Chromium, ffmpeg, fonts and the Python packages) and runs with `--timeout 1200`; the slowest suite (`fusionforge`) takes about 3.5 minutes.

### Why the rest stay blocked

The report's `blocked_why` splits the blocked entries: `method_description` (powers, skills without code, styles, playbooks, protocol rules, superpowers: written methods applied in the plan through `briefs.jsonl`, never counted as executed, because there is no program to run), `tool_without_adapter` (registered programs that still need a reviewed adapter) and `skill_program_without_adapter` (skills whose folder ships an argparse Python script with no adapter yet). The last two are the honest backlog. Measured on 2026-11-03 on a real 62 s clip: 7,391 entries, 227 of 227 adapters executed (47 hand-written tool adapters + 155 tool runners + 25 skills), 0 failed; blocked 7,157 method descriptions + 6 tools + 1 skill whose programs cannot run here (Blender, Remotion, the owner's GitHub over the network, the iPhone script, DaVinci Resolve). Before the tool runners the same run executed 72 of 72 with 161 tools blocked.

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

They cover inventory of every kind against its sources, part/mode/weight for every entry, determinism, dependency waves and blocked dependents, explicit execution gating, unsafe paths, job reuse, the `--help` probe, the exec wrapper's exit code and a real run of reviewed adapters with checked receipts. The `Black Dragon checks` workflow also runs a full job on every pull request and uploads its receipts.

## In the USIP pipeline (v6.5, appendix A49)

The dragon is no longer only a named command. At L3 it runs right after the USIP brief with `--probe-tools --reviewed-adapters` (assigned + probed); when the owner answers `نفّذ بأقصى قوة` it also gets `--execute-adapters`, since every reviewed adapter only reads. Each stage leader that would change the engine or the verification method goes into plan C, and the report carries one line: assigned · probed · executed with receipt · `full_coverage`. Measured on 2026-11-01: 7,381 assigned, 187 of 205 tools probed, 39 of 39 adapters executed with receipts, 0 failed.


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
