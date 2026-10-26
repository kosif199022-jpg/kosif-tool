# مصادر «استوديو الرسم بالبيكسل (KOSIF Studio)» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## akbun-draw-book-illustration (1094-akbun-draw)

- الترخيص: **MIT**  ·  الأصل: https://github.com/choisungwook/akbun-aitools/tree/b592650776c4ed1723087911010466d0b537fc6b/plugins/akbun-draw
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2415-akbun-draw-book-illustration
- الوصف: 소재·글씨를 monogray 삽화 스타일(진회색 잉크 손그림 + 플랫 회색 + 오렌지 포인트 하나)로 그리되, 구도를 자유롭게 두지 않고 참고 이미지에서 뽑은 고정 레이아웃 5종(아이콘 스트립·확대·대화·흐름· 포스터 카드)과 상하좌우 간격에 맞춰 배치하는 이미지 생성 프롬프트와, Figma/Canva로 가져와 편집할 수 있는 SVG 파일을 함께 만든다. 글씨가 없으면 내용을 분석해 skill이 문구를 만든다. Trigger on: "책 삽화 레이아웃", "고정 레이아웃 삽화", "아이콘 스트립 삽화", "확대 삽화", "대화 삽화", "흐름도 삽화", "삽화 레이아웃 SVG", "book figure layout", "icon strip illustration", or any request to lay a

```markdown
# 책 삽화 레이아웃 이미지 프롬프트 + SVG 생성

## 이 skill이 하는 일

개념, 장면, 짧은 글을 받아 **기술책 삽화**를 만들 수 있게 두 가지 산출물을 만든다.

1. GPT image나 nano-banana 같은 이미지 생성 모델(또는 이미지 생성 agent)에 그대로 붙여넣을
   **영어 이미지 생성 프롬프트**
2. Figma나 Canva로 가져와 직접 편집할 수 있는 **SVG 파일**

이 skill은 그림을 직접 렌더링하지 않는다. 프롬프트는 이미지 모델이 그리고, SVG는 사용자가
디자인 툴에서 다듬는다.

이 skill은 진회색 잉크 + 플랫 회색 + 오렌지 포인트 하나 + off-white 종이의 monogray 팔레트를
사용하고, **참고 이미지에서 뽑은 고정 레이아웃 5종과 상하좌우 간격에 맞춰 배치한다.**

## 결과물 형식

항상 세 가지를 출력한다.

1. **영어 이미지 생성 프롬프트** — 한 개의 코드 펜스 블록(```text)에 담아 그대로 복사할 수 있게 한다.
2. **SVG 파일** — 작업 디렉터리에 `<주제-slug>.svg`로 저장하고 경로를 알려준다.
   SVG 작성 규칙은 `references/svg-rules.md`를 따른다.
3. **한국어 한 줄 설명** — 어떤 레이아웃을 골랐고, 어떤 문구를 넣었고, 오렌지 포인트를 어디에
   줬는지 1~2문장.

## 입력 다루기

- **그림 소재**: 텍스트 설명, 개념 이름, 참고 이미지 등 무엇이든 받는다. 참고 이미지는 픽셀
  단위로 복제할 대상이 아니라 소재·구도를 읽는 참고다.
- **글씨(옵션)**: 사용자가 그림에 넣을 문구를 줬으면 **바꾸지 않고 그대로** 넣는다. 요약하거나
  다듬지 않는다.
- **글씨가 없으면 skill이 만든다.** 소재를 분석해 레이아웃에 맞는 짧은 문구(라벨, 제목, 캡션,
  말풍선)를 만든 뒤 그림 작업을 진행한다. 만든 문구는 한국어 한 줄 설명에서 알려준다.
- 문구는 짧게 유지한다. 라벨은 2~6자, 캡션·말풍선은 15자 안팎이 안전하다. 길수록 이미지
  모델이 글자를 틀릴 확률이 높다.

## 레이아웃 고르기

레이아웃은 아래 5종으로 고정한다. 각 레이아웃의 구성과 상하좌우 간격 수치는
`references/layout-patterns.md`에 있다. **간격 수치는 임의로 바꾸지 않는다.**

| 레이아웃 | 쓰임 |
|---|---|
| `flow-stack` | 단계·구조 설명. 세로 블록 스택 + 그룹 음영 + 오렌지 화살표 흐름 |
| `zoom-detail` | 대상의 내부·세부 강조. 주 피사체 + 확대 원 + 오렌지 링 |
| `poster-card` | 인용·장면 각인. 액자 프레임 + 상단 제목 + 중앙 장면 + 하단 캡션 |
| `dialog-scene` | 상호작용·의문 표현. 좌측 인물(생각 풍선) + 우측 상대(말풍선) |
| `icon-strip` | 수치·팩트 나열. 가로 아이콘 3~4개 + 아래 라벨 |

선택 기준: 내용이 "순서·구조"면 `flow-stack`, "안을 들여다보기"면 `zoom-detail`,
"한 문장을 각인"이면 `poster-card`, "묻고 답하기·오해"면 `dialog-scene`,
"숫자 비교·나열"이면 `icon-strip`. 사용자가 레이아웃을 지정하면 그것을 따른다.

## 비주얼 스타일 (고정 monogray 팔레트)

모든 산출물(프롬프트와 SVG)은 아래 스타일과 팔레트를 그대로 따른다. 바꾸지 않는다.

- **배경**: 따뜻한 off-white 종이(`#F4F2ED`). 종이 질감이 은은하다.
- **선**: 진회색(`#3A3A3A`) 잉크 아웃라인. 굵고 둥근 손그림 선이며 살짝 흔들린다(완벽한
  직선·정원이 아니다). 선 끝은 둥글다(round join/cap).
- **면**: 플랫한 회색 두 톤 — 밝은 회색(`#E3E3E3`), 중간 회색(`#C9C9C9`). 모니터·화면처럼
  어두운 면은 `#5A5A5A`. 그룹 배경은 사선 해칭(스크린톤) 느낌의 회색 라운드 사각형.
- **포인트 컬러**: 따뜻한 오렌지(`#E8833A`) **한 색만**. 화살표, 강조 블록, 물음표, 링 같은
  "가장 말하고 싶은 요소" 1~3곳에만 쓴다. 그 외 색은 쓰지 않는다.
- **텍스트**: 한국어 손글씨 느낌. 영어 제목은 세리프 대문자에 자간을 넓게.
- **여백**: 사방 캔버스의 약 10%. 요소를 가장자리에 붙이지 않는다.
- **인물/캐릭터**: 인물이 필요한 자리(예: `dialog-scene`의 인물)에는 소재에 맞는 인물·캐릭터를
  정해 이 그림체로 그린다.

## 폰트 규칙 (저작권 무료)

- SVG의 텍스트는 **SIL OFL 라이선스의 무료 폰트만** 지정한다.
  한글 손글씨 기본은 `Gaegu`, 대안은 `Nanum Pen Script`, 라틴 대체는 `Patrick Hand`를 쓴다.
  영어 세리프 제목이 필요하면 `Nanum Myeongjo`를 쓴다. 모두 Google
  Fonts에서 무료로 쓸 수 있다.
- 유료·상용 폰트나 라이선스 불명 폰트 이름을 지정하지 않는다.
- Figma는 Google Fonts를 내장 지원하므로 그대로 열린다. Canva는 폰트가 없으면 대체되므로,
  필요 시 OFL 폰트 파일을 Canva에 업로드하라고 안내한다.

## 작업 순서

1. **소재와 글씨 파악.** 사용자가 준 소재를 읽는다. 글씨가 있으면 그대로 쓰고, 없으면 소재를
   분석해 문구를 만든다.
2. **레이아웃 결정.** 위 선택 기준으로 5종 중 하나를 고른다.
```

## blog-figure-svg (1814-publishing-skills)

- الترخيص: **MIT-0**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/productivity/publishing-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1814-publishing-skills/4861-blog-figure-svg
- الوصف: Design accessible, source-backed SVG editorial figures and optionally rasterize reviewed assets for a blog or CMS. Use when a post needs a flow, comparison, taxonomy, terminal mock, or feature card. Trigger with "add a figure to this post" or "make an SVG diagram".

```markdown
# Accessible Editorial SVG Figures

## Overview

Create lightweight editorial artwork whose visual claims are traceable to the approved article or source data. Supported shapes are process flows, comparison bars, taxonomies, terminal mocks, and `1600x840` feature cards.

The editable SVG is the source of truth. PNG rasterization is optional, and CMS upload remains a separate approved action.

## Prerequisites

- Final or near-final article copy with the intended anchor paragraph
- Approved title, caption, data points, source URLs, brand palette, and output directory
- A writable local draft directory such as `tmp/blog-drafts/`
- For PNG output, one installed rasterizer: ImageMagick, `rsvg-convert`, Inkscape, or CairoSVG
- Optional `pngquant` or `oxipng` for lossless or reviewed lossy compression

## Tool Discipline

Use `Read` to inspect the approved article and brand tokens. Use `Write` or `Edit` for local SVG, caption, and receipt files. The scoped `Bash` commands may only detect or invoke the named local renderers and Python validator; never interpolate untrusted titles, SVG fragments, filenames, or shell arguments.

## Instructions

1. Identify the single information structure to communicate. Choose `flow` for ordered steps, `compare` for sourced numeric values, `taxonomy` for categories, `terminal` for verified command output, or `feature` for a title card.
2. Extract the exact facts from the approved source. Record a URL or article anchor for every number, quote, product claim, and terminal line. Omit unsupported content.
3. Create a safe kebab-case filename, refuse parent traversal or absolute output paths, and avoid overwriting an existing asset unless the owner approves.
4. Lay out the figure on a responsive SVG `viewBox`. Use text elements rather than embedded fonts, preserve readable contrast, and keep labels legible at the target display width.
5. Add a unique `<title>` and `<desc>`, then connect them with `role="img"` and `aria-labelledby`. Decorative shapes should not add noise to the accessibility tree.
6. Keep the SVG self-contained: no scripts, event handlers, remote images, external stylesheets, `foreignObject`, or unreviewed embedded data.
7. Validate the XML and scan for forbidden active content. Review clipping, reading order, contrast, label accuracy, and source correspondence.
8. If PNG output is requested, choose an installed rasterizer, pass fully quoted local paths, render at the required dimensions, and verify the output type and dimensions.
9. Compress only after preserving the SVG source. Compare before/after dimensions and file size, and retain quality acceptable for text and fine lines.
10. Return paths, dimensions, alt text, caption, evidence mapping, validation results, and any upload action still awaiting approval.
```

## svg-figure (2657-figures)

- الترخيص: **BSD-3-Clause**  ·  الأصل: https://github.com/neuromechanist/research-skills/tree/f0219bde233abb44d8a0c5d73f41ea27073e1493/plugins/figures
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2657-figures/10113-svg-figure
- الوصف: This skill should be used when the user asks to "create an SVG figure", "make a schematic", "draw a diagram", "create a schematic diagram", "draw a flowchart", "draw a process flow", "draw a workflow", "draw a workflow diagram", "make an SVG schematic", "create a process diagram", "create a pipeline diagram", "create a block diagram", "draw a system diagram", "system architecture diagram", "make t

```markdown
# SVG Figure

Conventions for SVG schematics and diagrams (flowcharts, process diagrams, system diagrams, anatomical illustrations) with element-consistency guarantees: text aligned to box bounds, arrows pointing at their targets, lines passing under shapes by z-order. The output SVGs are designed to be composed as panels by the `figures:scientific-figure` skill and verified by the `figures:figure-qa` agent's SVG branch.

## When to use this skill

**For new programmatic work, use `figures:svg-primitives` instead.** It implements every convention below as a mechanical guarantee — text auto-fits boxes, arrowheads stay tangent-correct on curves, paint order is deterministic, and `Canvas.save(validate='strict')` raises if any of those invariants are violated. `examples/schematic_from_primitives.py` in this skill is the canonical programmatic example.

Reach for **this** skill when:

- You are writing SVG **by hand** or with an editor like Inkscape, and need the conventions the figure-qa agent expects.
- You are using a non-Python tool to emit SVG and want to know what shape it should take.
- You are reading hand-authored SVG produced by an external collaborator and want to understand the layout grammar.
- You are debugging a figure-qa finding on an SVG that did not come from `svg-primitives`.
- The figure is a **schematic** (boxes, arrows, labels) rather than data plotted from numbers — for plots use `figures:plot-styling`.

Reach for a different tool when:

- You are writing Python → use `figures:svg-primitives`.
- The figure is a **plot** of data → use `figures:plot-styling`.
- The figure is **pictorial substrate** (a brain, a microscope, a setup photo aesthetic) → use `figures:ai-full-figure` for the substrate and overlay labels via `figures:svg-primitives`.
- The figure needs **icon-style elements** repeated across panels → generate the icons via `figures:transparent-icons` and place them as `<image>` references in the SVG.

## Programmatic authoring (recommended path)

See `figures:svg-primitives`. The canonical example in this skill is `examples/schematic_from_primitives.py` which reproduces `examples/schematic.svg` using `Canvas`, `LabeledBox`, `Arrow.connect`, and `Annotation`. Run it:

```bash
cd plugins/figures/skills
uv run --with drawsvg --with svgpathtools --with Pillow --with fonttools \
    --with cairosvg --with lxml \
    python svg-figure/examples/schematic_from_primitives.py
```

## Hand-authoring conventions

The recipes below apply when SVG is written by hand or emitted by a non-Python tool. `figures:svg-primitives` enforces every one of them mechanically; this section is the reference for the underlying SVG conventions and is what the figure-qa agent expects when validating arbitrary SVG inputs.

### 1. Sizing
```

## svg-primitives (2657-figures)

- الترخيص: **BSD-3-Clause**  ·  الأصل: https://github.com/neuromechanist/research-skills/tree/f0219bde233abb44d8a0c5d73f41ea27073e1493/plugins/figures
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2657-figures/10114-svg-primitives
- الوصف: Use when the user asks to build a programmatic SVG schematic in Python: flowcharts, boxes and arrows, auto-fit SVG text, mm-precise diagrams, edge-snapped arrows, tangent-correct curve arrowheads, orthogonal or Manhattan routing, deterministic z-order layers, labeled groups, bracket groupings, leader-line annotations, or strict Canvas.save validation for text overflow. Use figure-qa instead for af

```markdown
# SVG Primitives

Build mm-precise SVG schematics in Python with three mechanical guarantees:

1. **Text never overflows its container** — labeled shapes auto-size to fit measured text bbox + padding.
2. **Arrowheads stay tangent-correct** — arrows emit `<marker orient="auto">` so the renderer rotates the head along the path's terminal tangent; works on straight lines and cubic Beziers.
3. **Paint order is deterministic** — layers paint in registration order; connectors visibly pass under boxes without manual reordering.

The skill ships an end-to-end pytest suite (50+ tests) that renders SVGs and asserts these invariants on the rendered output, so the guarantees are enforced by construction rather than by hand-checking each figure.

## When to use this skill

Reach for `svg-primitives` when:

- The figure is a **schematic** (boxes, arrows, labels) and you're driving it from Python — e.g. nodes come from a YAML config, or the layout depends on data.
- You need the boxes to **auto-fit** their labels (no hand-tuning widths).
- The figure has **curved arrows** that must point cleanly at their targets.
- You want **deterministic z-order** so connectors sit under shapes without manual element reordering.
- The output will be **composed into a multi-panel figure** as a panel SVG that `scientific-figure/compose.py` loads.

Reach for a different tool when:

- The figure is **plotted from numbers** (matplotlib/seaborn/plotnine) → use `figures:plot-styling`.
- The figure is a **photographic / pictorial substrate** (a brain scene, microscope setup) → use `figures:ai-full-figure` for the substrate and overlay labels via Arrow/LabeledBox here.
- The figure is **hand-authored SVG** or the patterns are reference material for hand-authoring → use `figures:svg-figure` (this skill's library-agnostic counterpart).

## Quick start

```python
from svg_primitives import Canvas, LabeledBox, Arrow

c = Canvas(width_mm=183, height_mm=80)
boxes = c.layer("boxes")
arrows = c.layer("connectors")

raw = boxes.add(LabeledBox(x=10, y=20, text="Raw EEG", font_size=7))
band = boxes.add(LabeledBox.next_to(raw, side="E", gap=10, text="Bandpass\nfilter", font_size=7))
ica = boxes.add(LabeledBox.next_to(band, side="E", gap=10, text="Independent component\nanalysis", font_size=7))

arrows.add(Arrow.connect(raw, band))                          # straight, snapped to edges
arrows.add(Arrow.connect(band, ica))                          # straight
arrows.add(Arrow.connect(ica, raw, curve="cubic", bow=14,     # feedback arc
                          stroke="#C45146"))                  # red — gets its own red marker

c.save("eeg.svg", output_png=True)
```

`examples/eeg_pipeline.py` is the canonical reference; run it to see the full output:

```bash
```

## raster-logo-svg (2981-designer-skill)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/PyModel/designer-skill
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2981-designer-skill/12626-raster-logo-svg
- الوصف: Turn a raster logo (PNG, JPG, WebP) into a pixel-identical, self-contained SVG by base64 embedding. Use when an .svg logo is needed without a vector source, or a redrawn SVG does not match the original.

```markdown
# raster-logo-svg

Create an **SVG wrapper** around an existing raster logo so the output is **pixel-identical** to the source. This is not true vectorization.

## Choose the approach

| Need | Do |
|------|-----|
| Match an existing raster logo exactly | **Embed** (this skill) |
| Crisp at any size, editable paths | Export from Figma/Illustrator, or commission true vector |
| Quick monochrome outline | Potrace (usually wrong for brand logos with color/gold/type) |
| Hand-redrawn paths | Only if no raster exists and user accepts approximation |

Default to **embed** when a `.webp`, `.png`, or `.jpg` logo already exists and the user wants `.svg`.

## Workflow

1. **Source of truth** — keep the raster (e.g. `docs/logo.webp`). Do not delete it.
2. **Generate SVG** — run the script from repo root or skill directory:

```bash
python3 skills/raster-logo-svg/scripts/embed-logo.py docs/logo.webp -o docs/logo.svg -l "project-name"
```

Requires **ImageMagick** (`magick identify`) for dimensions. Install: `brew install imagemagick`.

3. **README** — prefer the **raster** in GitHub README for reliable rendering:

```markdown
<img src="docs/logo.webp" alt="project-name" width="580" />
```

Use the **SVG** for plugin manifests, favicons, npm package icons, or anywhere a `.svg` path is required.

4. **Verify** — open the SVG locally; it must look identical to the raster. Do not commit temp traces (`icon-traced.svg`, potrace output, failed hand-drawn attempts).

## Output format

The script produces:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 W H" role="img" aria-label="…">
  <image width="W" height="H" href="data:image/webp;base64,…"/>
</svg>
```

- `viewBox` matches source pixel dimensions from `magick identify`.
- MIME: `image/webp`, `image/png`, or `image/jpeg` from file extension.
- Self-contained: no external `href="logo.webp"` (breaks when SVG is copied alone).

## Tradeoffs (tell the user when relevant)

- **Pros:** Perfect visual match, fast, no design source needed.
- **Cons:** Not true vector; upscaling very large may soften (same as the raster).
- **Size:** SVG file ≈ base64(raster) + ~200 bytes overhead (~33% larger than raw binary).

## Do not

- Hand-draw paths to “recreate” a brand logo when the raster exists — results rarely match.
- Use potrace/ImageMagick trace for full-color wordmarks.
- Replace the canonical raster with only SVG unless the user explicitly drops the raster.
- Embed secrets or sensitive images in public repos without user confirmation.

## Optional: external-reference SVG

Only for local tooling that resolves sibling files (not GitHub README `<img src="logo.svg">`):

```xml
<image href="logo.webp" width="1163" height="350"/>
```

Prefer **base64 embed** for portable `.svg` files.

## Example (designer-skill)
```

## 9526-scene (2460-pixel-art)

- الترخيص: **MIT**  ·  الأصل: https://github.com/melodic-software/claude-code-plugins/tree/c8fa858c9059d3183cfc08f646e4a97f44b33973/plugins/pixel-art
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2460-pixel-art/9526-scene
- الوصف: Build animated pixel-art scenes as one self-contained HTML file (Canvas 2D, no libraries, no external assets): cutscenes, title screens, dialogue beats, ambient loops, short pixel films, card reveals, and backgrounds with parallax, particles, lighting by palette steps, bitmap text and dither transitions. Reuses sprite specs from /pixel-art:sprite and /pixel-art:animate, takes an optional audio fil

```markdown
# Scene

Compose a moving pixel-art scene the user opens in any browser.

## 1. Brief

Follow [`brief.md`](${CLAUDE_PLUGIN_ROOT}/reference/brief.md): the shared fields, the `brief.md`
file before the first build, one-line defaults, and the presence-gated `/planning:interview`
offer (planning owns a numbered-question brief; the in-skill brief is the fallback and the
default). Then add:

- **Beats**: what happens, in order, and how long each lasts; loop or play once.
- **Cast and set**: characters (existing sprite specs or new ones), location, time of day.
- **Resolution**: a fixed logical size such as 160x144, 240x160, 320x180; everything is drawn
  there and integer-scaled.
- **Audio**: none, or a WAV path / audio artifact from another tool, passed in explicitly.

Mood, palette, style references, and proportions still come from the shared brief and apply to
the cast. When view does not apply, default it to "scene" in the defaults line.

When a cast member is an existing spec with `brief.md` beside it, read that file and extend it.
Do not re-ask fields it answers. Write this scene's `brief.md` beside the scene template before
the first build.

## 2. Author

Follow [`scene-canvas.md`](${CLAUDE_PLUGIN_ROOT}/reference/scene-canvas.md). Write a template HTML
file beside the output:

- Characters come from sprite specs: embed them with `/*EMBED:relative/path.json*/null` and build
  one offscreen canvas per frame at load, so sprites stay the same source the engine sheet uses.
  Missing characters: author them first with `/pixel-art:sprite` or `/pixel-art:animate`.
- Beats are a timeline or state machine driven by a fixed 60 Hz step; sprite cadence stays 8 to 12
  fps; every draw lands on integer coordinates.
- Light and fades step through palette colors or Bayer-dither patterns; never alpha, gradients or
  blur.
- Audio, when given: put `/*WAV:relative/file.wav*/null` in the template. `embed.py` inlines a
  `data:audio/wav;base64,...` URL (the output stays one file). Play it with WebAudio: this plugin
  starts it on the first click and rewinds the scene clock on that click, so the picture and the
  loop share a start. Also set `audio` on `window.__pixelScene` to that same URL so `--record` can
  mux it. Browser behavior and its record: `scene-canvas.md` Audio.

A worked example is `${CLAUDE_PLUGIN_ROOT}/examples/campfire/scene.html` (title card, dithered sky,
parallax, fire particles, walking character, typed dialogue); copy the folder into the working
directory before adapting it.

Expose `window.__pixelScene` as [`scene-canvas.md`](${CLAUDE_PLUGIN_ROOT}/reference/scene-canvas.md)
describes under Review capture (`seek`, `frameDataURL`, `play`, `duration`) so the review command
can land on a timeline point.

Then inline the embeds into one file:

```bash
```
