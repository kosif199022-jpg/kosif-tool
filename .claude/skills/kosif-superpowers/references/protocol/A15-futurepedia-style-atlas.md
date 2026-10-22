# A15 — Futurepedia AI Style Atlas: 15 verified-description method routes

> **Trigger / متى تقرأه:** ابتكار أسلوب بصري جديد للرسم أو الموشن أو المونتاج؛ fusion / دمج أكثر من أسلوب؛ طلب "أساليب Futurepedia"، رسوم explainer، أسلوب السبورة البيضاء، الإضاءة السينمائية، منظور أيزومتري.
>
> **Canonical routing:** [PROTOCOL.md](../../PROTOCOL.md) → [A14 drawing academy](A14-drawing-cinematic-academy.md) → [A8 motion brain](A8-motion-brain.md).

## Provenance and real capability boundary

Read-only page: https://www.futurepedia.io/resources/ai-style-atlas/view
The site advertises **86 visual styles**. Only **15 publicly visible descriptions** were actually retrieved and reviewed in this task. The remaining 71 **are not registered** as read/reviewed, executable, trained or accessed. The public page explains that each style provides a comparison video and a copy-prompt feature, but the original prompts, videos and assets are **not redistributed or imported here**. The summaries and method contracts below are independent syntheses of visible characteristics, not copied service implementations.

**Method preset (FA-01..15) ≠ image/video render engine**. The new `scripts/style_atlas_bridge.py` does run offline to search 15 methods, compose one/two styles into a typed workflow recipe, and produce an original *static SVG study*. It does **not** replay an original video, generate photorealism, use paid credits, fine-tune weights, render a final MP4, or claim that the original style is reproduced pixel-perfect. Rendering and word/audio alignment remain gated steps requiring licensed inputs and separate executing engines.

## Capability index and actionable synthesis

| ID | Style | Reusable composition skill | Planned handoff (NOT execution proof) |
|---|---|---|---|
| FA-01 | Flat-Vector Science | Bold vector masses, layered gradients, soft glowing scientific diagram | shapes → `unified_draw` → `motion_director` |
| FA-02 | Watercolor Wash | Low-opacity pigment layers, paper texture, clean unpainted lights | layered paint → image study → visual evaluation |
| FA-03 | Shadow Puppet Theatre | Silhouette, backlit projection, segmented puppet joints | character drawing → `character_ik` → animated study |
| FA-04 | Whiteboard Explainer | Plan stroke order, draw-on path, word-led rhythm | `creative_principles` → `motion_director` with word timings |
| FA-05 | Psychedelic Poster | Complementary ink colours, symmetry and repeated swirling bands | shapes + color `perspective_color_lab` → original poster |
| FA-06 | Tech Glow Explainer | Node hierarchy, luminous connections and pulse timing | SVG nodes → `motion_director` → brightness QA |
| FA-07 | Papercraft Models | Folded faces, seam diagrams, craft-board perspective | `native_3d` or paper vector → fold action |
| FA-08 | 1940s Film Noir | Controlled hard light, shadow bands, restrained monochrome | lighting design → `montage_pro` → tonal continuity QA |
| FA-09 | Manim-Style Math | Consistent axes and exact equations, stepwise proof narration | verified math → vector scene → timed build |
| FA-10 | Illuminated Manuscript | Original gilded initial, botanical borders and vellum tonality | `creative_paint` → fonts and decorative QA |
| FA-11 | Editorial Essay Collage | Licensed clipping layers, typography and archival textures | sources + rights → cut plan → `montage_pro` |
| FA-12 | Bioluminescent Deep Sea | Emission-driven focal lighting, deep-black layered particles | particles and organic animation → luminance QA |
| FA-13 | Product Launch Reveal | Key/rim/specular light, product hero focus, truthful proportions | 3D render → camera sweep → brand QA |
| FA-14 | Halftone Pop Panel | Dot matrix and tapered outlines, safe bubble/titles | brush/pattern layer → `font_fidelity_lab` → panel timing |
| FA-15 | Isometric Pastel | Exact 30° projection, three-valued faces and object order | `native_3d` or `perspective_color_lab` → geometric review |

Data: [`data/futurepedia_style_methods_15.json`](../../data/futurepedia_style_methods_15.json); command-line bridge: [`scripts/style_atlas_bridge.py`](../../scripts/style_atlas_bridge.py).

## Task to capability synthesis: not just a list

1. **Stage 0 / specify:** determine purpose, audience, aspect ratio, original audio timestamps, rights, desired realism, and explicit exclusions (Katana always analysis-only and only via verified no-credit read-only endpoint).
2. **Select:** choose a dominant FA style from catalog by name or ID. Optionally select **one** secondary style supplying an accent. More mixtures require human approval: mixing 5 incompatible looks is not self-evidently better.
3. **Compose:** build the typed five-node graph `rights_and_assets → art_direction → original_scene → timed_animation → independent_verification`. The method layer can mark only the direction recipe verified, not other nodes.
4. **Produce original visual:** `study-svg` writes a static, independent drawing exercise for that style. It is a visual debugging artifact **not** a final illustration or an MP4.
5. **Real render only after gates:** choose live installed KOSIF executors; inspect/measure narration; produce actual original scenes; render; verify Arabic layout, camera, sound, rights and real frame results. Record results via FusionForge as `tested`/ `verified` only with evidence.
6. **Self-learning:** store actual tested graph and QA receipt in **project-isolated** FusionForge lessons; never treat reading a style page as new model weights, and never share private company assets across projects.

### Copy/paste commands (skill directory)

```bash
python scripts/style_atlas_bridge.py list
python scripts/style_atlas_bridge.py search "سبورة"
python scripts/style_atlas_bridge.py plan --topic "كيف يتعلم الذكاء الاصطناعي" --style FA-04 --accent FA-06 --duration 15 --aspect 9:16 --out out/draw-tech-plan.json
python scripts/style_atlas_bridge.py study-svg --style FA-04 --topic "My original idea" --out out/whiteboard-study.svg
python -m unittest discover -s evals -p test_style_atlas_bridge.py -v
```

Use an output filename that does **not** already exist. The tool refuses overwrites. Input topics are treated only as labels, XML escaped, not as instructions or executed commands. The CLI requires only Python 3 stdlib and the checked-in JSON; no accounts or media API credits.

### Acceptance gates

- 15 exact source-scoped entries; stable FA IDs and unique slugs; 71 missing titles never guessed.
- Search and per-ID lookup deterministic; mixed recipe keeps **85% primary + 15% accent** as a design starting constraint, not an objective color metric.
- Five typed handoffs, each marked verified only for tested method planning; actual render, asset usage and sound QA are explicitly unverified until executed.
- Every static study parses as SVG and differs by style; no external images, active JS or live network fetches; prompt labels escaped.
- Audio, temporal accuracy, visual fidelity, source licenses and final social export remain separate **unverified** tasks.

**Origin caution:** The source's comparative clip and copy-prompt interface were described on the accessible page, but the service requires sign-in for other data. This module is **not** a mirror or an extractor of paywalled/private materials.

**Katana/Higgsfield constraint:** NO spending image/video credits or calling create/remix; analysis only through an explicitly verified zero-cost read-only interface and with source rights. If none exists, use native vision/FFmpeg and say Katana was not invoked.
