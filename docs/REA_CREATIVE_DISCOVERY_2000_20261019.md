# KOSIF 2,000-Source Creative Discovery and REA Evidence Audit

**Date:** 2026-10-19. **Scope:** licensed video editing, motion graphics, photography, images, audio synchronization, computer vision, creative coding and animation.

> Important: **2,000 sources cataloged is not 2,000 sources analyzed with REA**. This distinction is enforced in data schemas, search responses, and automated tests. Catalog-only and actual inspection counts are reported separately.

## Verified current results

| Workstream | Completed and verified | What it establishes |
| --- | ---: | --- |
| Public GitHub source catalog | **1,000 distinct repositories** | GitHub metadata, search query, description, topic/language, star count and SPDX *metadata*, not code inspection |
| Curated creative website index | **1,000 distinct hostnames** | Extracted outbound links from named motion, design, photography and video resource directories; page function/availability not independently checked |
| Owner account inventory | **26 repositories** across `kosif199022-jpg` and `elkosif0-cmd` | 21 public, 5 private; stored in a private local directory, not committed |
| Owner Git tree coverage | **26/26 attempted, 24 populated, 2 empty, 0 failures** | GitHub repository tree filenames and language/extension patterns; not equivalent to code tracing |
| REA owned-source analysis | **9 successfully analyzed repos** | Static JavaScript graph evidence: 536 parsed JS files and 4,446 structural findings. Details/paths and private evidence remain local |
| REA website analysis | **5 passively observed public pages** | Remotion, Jitter, Photopea, Blackmagic Design and CapCut; browser/CDP observations only, not a complete product implementation audit |
| REA deep page-bundle reconstruction | **0 successes** | A bounded Remotion bundle analysis failed inside Node; not reported as successful |
| KOSIF implemented new tools in this change | **3 research/discovery utilities plus REA batch adapter** | Reproducible catalog creation, balancing, search and bounded first-party source analysis; no third-party software feature copied |

### Repository category coverage (1,000 unique)

- Video/film: **380**
- Motion and VFX: **207**
- Image and photography: **320**
- Computer vision / creative coding: **93**

The public index is in `.claude/skills/kosif-superpowers/data/rea-creative-research/`. Every record is marked `metadata only`, `curated link only` or its corresponding evidence level.

**Do not interpret GitHub stars as independent security, maturity, quality or licensing evidence.** GitHub's SPDX badge is metadata; inspect the actual LICENSE and dependencies before code integration.

### Discovery origins

The website index collects outbound links from public, topic-relevant sections of curated source lists, including:

- https://github.com/beast-ofcourse/awesome-motion-graphics
- https://github.com/Supersynergy/awesome-ai-video-editing
- https://github.com/ad-si/awesome-video-production
- https://github.com/AaronAust1n/awesome-video-skills
- https://github.com/iRajatDas/awesome-image-tools
- https://github.com/stimQQ/awesome-ai-image-tools
- https://github.com/eric-erki/awesome-creative-coding
- https://github.com/sergey-pimenov/awesome-web-animation
- https://github.com/goabstract/Awesome-Design-Tools

These are curated reference lists, not guarantees of present website availability or permissive media licenses. Badges and obviously non-tool assets were excluded when rebuilding the list.

## Actually performed with REA

**Tool:** `rea-agents@6.7.0`, installed on the authorized Windows laptop.

**REA static source:** `analyze-javascript-application` on nine repos with eligible/accessible JavaScript and TypeScript source directories; analysis of their code does **not** execute it. We retained evidence IDs, parsed-file and AST statistics and structural observations. Summed findings are not unique KOSIF capabilities.

**REA public sites:** `inspect-web-page` through an isolated Chrome CDP session, exact-origin scoped. This can observe structural page behavior available during the observation window, but does not prove hidden internal algorithms, privileged functionality or business rules. The `analyze-web-bundle` attempt failed; no success is claimed.

**Owned repository privacy:** local full inventory, private repository names, source-tree paths, REA Evidence JSON and cloned first-party source remain outside Git-tracked directories under the laptop's `KOSIF_RESEARCH_PRIVATE_20261019` workspace. Nothing from a private repository is automatically copied into this public index.

**REA supported scope:** primarily read-only JavaScript artifacts, passive browser observations and matching static artifact types. It is not a universal Python/Rust/C++ source auditor. The remaining repositories were inventoried through Git trees rather than falsely tagged as REA-inspected.

## High-value capability families extracted as *opportunities*

These families come from documented descriptions and research themes. Their status is `CANDIDATE_REQUIRES_IMPLEMENTATION` unless an existing KOSIF component independently passes an end-to-end test.

| Family | What Claude should investigate next | Required proof before marking AVAILABLE |
| --- | --- | --- |
| Footage-first automatic scene assembly | Phrase-aligned licensed video discovery, thumbnail/contact-sheet review, source selection | License evidence, footage media verification, visual QA, fully rendered film |
| Arabic word-level kinetic captions | Stable RTL shaping, word onset cues, highlighted names/numbers | Audible alignment error measurement and rendered font review |
| Smart subject-aware 9:16 reframing | Object detection, motion tracking, ROI smoothing and source resolution check | Annotated test clips and no cropped subjects |
| Shot/beat-aware editing | Waveform features, silence boundaries, camera rhythm, fixed timeline | Frame count, cut timing and regression comparison |
| Tracking and masking | Tracked overlays, vector mattes, verified object-mask quality | Segmentation mask QA and temporal flicker check |
| Professional color grading | Exposure matching, shot color normalization, LUT pipeline | Before/after frames with stable color across cuts |
| Image restoration and enhancement | Repair, denoise, upscale, super-resolution | Independent perceptual checks; no fabricated detail claims |
| Multitrack non-destructive editing | B-roll, original voice, captions, VFX and reusable transitions | Reproducible edit operations and master audio hash checks |
| Programmatic motion graphics | Remotion, Motion Canvas, Three.js, SVG or deterministic browser render | Reproducible MP4 and keyframe timing tests |
| Procedural effects | Dust, rain, light, particles, mask transitions | Composited examples, performance bounds and render QA |
| Transcript-native interface | Search/scrub narration words without destroying original audio | Actual synchronized timeline editor, not transcript-only mockup |
| Standard interchange | OpenTimelineIO and metadata-safe EDL exports | Reimport to a supported NLE and frame accuracy check |
| Vector design and Arabic font checks | SVG editing, font licensing, glyph shaping and font-substitution QA | Test renders of Arabic, numbers and RTL punctuation |
| Rights and provenance verification | Asset source URL, actual license terms, hashes, creator credits | Individual asset rights evidence, not site-wide assumptions |
| Reference edit analysis | Cut geometry, motion style, titles, transitions and rhythm | Side-by-side verifiable measurements; no copied protected assets |
| Creative agent routing | REA static evidence + KOSIF capability atlas + task intent | Successful real task execution, not raw catalog counts |

Reference repositories such as `Zulko/moviepy`, `OpenShot/openshot-qt` and `hkchengrex/Tracking-Anything-with-DEVA` appear in GitHub discovery, but **are not yet integrated or proven running inside KOSIF**. Licensing and dependency review must precede such integration.

## How Claude must discover the 2,000 sources

```bash
# No internet required after the catalogs have been built:
python .claude/skills/kosif-superpowers/scripts/creative_external_search.py stats

python .claude/skills/kosif-superpowers/scripts/creative_external_search.py search "motion graphics Arabic captions" --top 20

python .claude/skills/kosif-superpowers/scripts/creative_external_search.py search "صور مونتاج خلفية" --kind repo --top 12

# Cross-reference executable KOSIF capabilities, separately:
python .claude/skills/kosif-superpowers/scripts/capability_atlas.py plan "Arabic motion graphics using real footage" --json
```

For reproducible **public metadata/curated-link collection**:

```bash
python .claude/skills/kosif-superpowers/scripts/rea_creative_research_atlas.py repos --limit 1000 --pages 3
python .claude/skills/kosif-superpowers/scripts/rebalance_creative_repos.py
python .claude/skills/kosif-superpowers/scripts/rea_creative_research_atlas.py sites --limit 1000
```

Repository scanning on one's own machines is a separate, permission-checked operation. The helper `rea_owned_repo_batch.py` only analyzes bounded eligible code checkouts, retains raw evidence locally and does not execute third-party source. It requires an explicit private output destination, installed REA CLI and authenticated repository access.

## Quality gates and limitations

1. Never represent search metadata or a public website link as a REA reverse-engineering result.
2. Do not infer a software product's complete feature set from an installer file.
3. Never claim REA can reveal hosted internal backend, proprietary model weights or non-public code from a webpage.
4. Public/private account isolation is mandatory. Only share private-derived information with explicit permission and deliberate review.
5. Do not clone, build or execute arbitrary thousand-repository code without checking licenses, safety, bandwidth and practical cost.
6. External implementations require license, security, API cost and provenance review; mere presence of a catalog entry does not transfer a working feature to KOSIF.
7. Number of sources, source files, REA observations and deployed KOSIF capabilities are **four different metrics**.
8. Research is staged. The 1,000 indexed public repositories remain metadata-level, while nine independently selected owned repositories were inspected with REA. Only five selected public sites received passive REA observations; the rest are index entries, not completed website audits.

### Next verifiable milestones

- Deep static REA inspection of more *authorized, technically compatible* repositories in bounded batches, prioritizing KOSIF motion and audio resources.
- Verify actual docs, supported APIs, licensing and quality of the best-ranked 50 candidates rather than blindly adding all 2,000.
- Add code-level integrations only when a real project end-to-end render demonstrates value.
- Extend the existing `cinematic_cut_planner.py` and `cinematic_broll_render.py` with word-accurate Arabic kinetic captions and realistic moving-footage QA.
