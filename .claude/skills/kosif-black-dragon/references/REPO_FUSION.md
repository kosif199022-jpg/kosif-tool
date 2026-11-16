# Repo fusion: 10 repositories dissected with REA (2026-11-10)

On 2026-11-10 ten public repositories were shallow-cloned into an isolated folder and dissected with REA 6.8.0. REA was used where it applies: `analyze_javascript_application` on JS applications, and `inspect_artifact` / `open_binary` on shipped files. Plain source was read by hand, as REA's own skill advises.

The most valuable new capabilities were re-implemented as **our own code** under `scripts/fusion/`. Each module has a `self-test` that builds its own input and asserts real results. No upstream code is executed or vendored.

- **Data:** `data/repo_fusion.json` (schema `kosif.black_dragon.repo_fusion.v1`).
- **CLI:** `scripts/repo_fusion.py`.
- **Per-repo reports:** `references/repo-fusion/<repo>.md`. Each report covers what the code really does, capabilities with `path:line`, what the Dragon already had versus what is new, the license, caveats and the REA evidence log.

```bash
python3 .claude/skills/kosif-black-dragon/scripts/repo_fusion.py list
python3 .claude/skills/kosif-black-dragon/scripts/repo_fusion.py find "قص على الإيقاع والدروب" --stage shots
python3 .claude/skills/kosif-black-dragon/scripts/repo_fusion.py show pixelfx
python3 .claude/skills/kosif-black-dragon/scripts/repo_fusion.py modules
python3 .claude/skills/kosif-black-dragon/scripts/repo_fusion.py self-test          # runs all 9 module self-tests
```

## Totals

101 capabilities: 47 native-implemented, 54 source-linked. 9 native modules.

## Repositories and modules

| repo | license | native module | what it adds to the Dragon | stage |
|---|---|---|---|---|
| lemomo-ai/lemo-opuscar | MIT | `native_opuscar.py` | Rhythm report: cuts, pace CV, silences, hit→onset ms. Reading-time check that knows Arabic, CJK and Latin. Director-rule treatment lint. | shots, qa |
| Vincentwei1021/video-shotcraft | Apache-2.0 | `native_shotcraft.py` | Promo energy arc. Gated beat grid (LSQ, half/double judged by kick). Render audio-lag. SFX peak placement. JianYing/CapCut draft planner with a safe Windows installer. | concept, shots, deliver |
| patch-gg/pixelfx | MIT | `native_pixelfx.py` | Pixel-art VFX over real footage with an additive light layer. Hit-stop + shake + anime impact frame. Hue-shifted palette ramps. Sprite sheets. | produce |
| JohnHeibel/ClaudeAnimationBase | MIT | `native_cab.py` | Viewer "reads" storyboard lint. Line-boil jitter audit. Bit-exact boil seed. Missing-frame todo. Render determinism check. | shots, qa |
| ahujasid/mcp-for-blender | MIT | `native_blender_audit.py` | Headless Blender scene audit: real size, grounded or floating, mesh health, rig weights, textures, scale. Poly Haven CC0 search. | produce, qa |
| mrdoob/three.js | MIT | `native_three.py` | Virtual-clock shim for deterministic TSL/WebGPU frames, a frame harness with a Playwright driver, and a node catalog. | produce |
| pmndrs/react-three-rapier | MIT | `native_rapier_bake.py` | Deterministic multi-body 2D physics bake on a frame clock, with impact frame numbers for SFX. | produce |
| librosa/librosa | ISC | `native_musicmap.py` | Music map: sections, beats, downbeats, drops, climax, energy curve, strong cut points, key. | brief, shots |
| yihui-dev/awesome-opus5-5-videos | MIT | `native_promptlib.py` + `data/opus_video_cases_index.json` | Searchable index of 703 code-as-video cases (links and metadata only) and a 12-rule video-prompt linter. | concept |
| joeseesun/opus-video-prompts | none | — | Links and metadata only. Lessons rewritten in our own words; no text copied. | concept |

## Honest limits

- **Not run in a real browser or GPU:** the three.js harness HTML. It was generated and checked; the virtual clock was executed in Node.
- **Network needed:** the Blender audit's Poly Haven step.
- **Hand-tuned on synthetic signals:** the musicmap drop threshold and the 4/4 downbeat guess. Try them on real songs before relying on them.
- **No real JianYing to test against:** JianYing drafts are planned and a pyJianYingDraft builder script is generated. A `draft_content.json` is never written blind. The upstream Windows install path is unverified, so run a smoke draft first.
- **Simplified physics:** 2D circles against static boxes and circles; no joints.
- **English-tuned lint:** the prompt linter is regex-based and tuned on English prompts.
- **Not vendored:** pixelfx's `PatchPixel` font (all rights reserved), and the prompt texts of either prompt library. Those texts belong to their authors; open `post_url` instead.
- **Excluded upstream policy:** opuscar's DIRECTOR.md §13 is the authors' map and border policy, not a craft rule, and is not imported.
