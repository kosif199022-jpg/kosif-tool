# مصادر «الرسوم المتجهة والأيقونات» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## generate-favicon (3170-generate-favicon)

- الترخيص: **MIT**  ·  الأصل: https://github.com/svyatov/agent-toolkit/tree/30316cebb256ff4a11d9483445c8769c1d1e4050/plugins/generate-favicon
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3170-generate-favicon/13499-generate-favicon
- الوصف: Generate a minimal favicon set from SVG: ICO, SVG with dark mode, Apple Touch Icon, PWA icons, manifest

```markdown
# Generate Favicon

Generate a complete favicon set from an SVG source file. Produces 6 files + 1 manifest that cover all modern browsers, PWAs, and legacy support.

## Output Files

| File | Size | Purpose |
|------|------|---------|
| `favicon.ico` | 32x32 | Legacy browsers, RSS readers |
| `icon.svg` | vector | Modern browsers, dark mode support |
| `apple-touch-icon.png` | 180x180 | iPhone/iPad home screen |
| `icon-192.png` | 192x192 | Android home screen (PWA) |
| `icon-512.png` | 512x512 | PWA splash screen |
| `icon-mask.png` | 512x512 (409x409 safe zone) | Android adaptive/maskable icon |
| `manifest.webmanifest` | — | PWA manifest with icon entries |

## Prerequisites

The user must have an SVG icon file. If they don't, help them create or obtain one first.

Required CLI tools (check availability before starting):
- `magick` (ImageMagick 7+) — for ICO and PNG conversion
- `npx svgo` — for SVG optimization (optional but recommended)

If ImageMagick is not installed, suggest: `brew install imagemagick` (macOS) or the platform equivalent.

## Process

### Step 1: Locate SVG Source and Output Directory

Ask the user which SVG file to use as the source icon. Verify:
- File exists and is valid SVG
- Has a `viewBox` attribute (needed for correct scaling)
- Is roughly square (width ≈ height in viewBox)

If the SVG is not square, warn the user before proceeding.

Detect the project's static/public directory by looking for `public/`, `static/`, `src/assets/`, or fall back to the project root. Confirm the output location with `AskUserQuestion`, offering the detected directory first. All generated files go into this directory.

### Step 2: Add Dark Mode to SVG

Read the SVG file. If it doesn't already have a `prefers-color-scheme: dark` media query, ask with `AskUserQuestion` whether they want dark mode support.

If yes:
1. Identify the actual fill/stroke colors used in the SVG (inspect `<path>`, `<circle>`, `<rect>`, etc.)
2. Propose specific dark-mode color swaps based on what's in the file — don't assume hardcoded values
3. Add a `<style>` block inside the `<svg>` element with the swaps:

```xml
<style>
  @media (prefers-color-scheme: dark) {
    .favicon-dark { fill: #PROPOSED_LIGHT_COLOR }
  }
</style>
```

4. Add the class to the relevant elements and ensure their default `fill`/`stroke` is set for light mode

If the SVG already uses CSS variables or classes, adapt to its existing structure rather than adding a parallel system.

Save the result as `icon.svg` in the output directory.

### Step 3: Optimize SVG

Run SVGO before generating PNGs — optimized SVGs produce cleaner rasterizations:

```bash
SVG=icon.svg
npx svgo --multipass "$SVG"
```

### Step 4: Generate All Image Files
```

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

## diagram (3135-diagram)

- الترخيص: **MIT**  ·  الأصل: https://github.com/studykit/studykit-plugins/tree/6a5646890354a748db7f1e18094b0c90cc74001c/diagram
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3135-diagram/13445-diagram
- الوصف: Create, explain, or validate diagrams as code in PlantUML, D2, or Structurizr DSL. Use when the user asks to draw or generate a diagram (sequence, class, activity, state, ER, Gantt, mind map, architecture, flowchart, C4 system context / container / deployment), add a diagram block to Markdown, asks for PlantUML, D2, or Structurizr syntax, or wants a .puml, .d2, .dsl file or diagram block checked o

```markdown
# Diagram

Compose diagrams as code for the user's request. On Claude Code the request is
`$ARGUMENTS`; otherwise it is the user's message.

## 1. Pick the mode

Use an explicit leading `create`, `reference`, or `check`. Otherwise infer it:

| Mode | Intent cues | Writes files |
|---|---|---|
| `create` | draw, create, generate, make, add to Markdown, insert into file | Yes |
| `reference` | syntax, how do I write, example for, reference | No, unless asked |
| `check` | check, validate, lint, is this valid, why does this fail, render | No, unless asked |

## 2. Pick the engine

Take the first rule that applies:

1. The user names an engine (`plantuml`, `d2`, `structurizr`), or an existing source
   decides it: `.puml`/`.plantuml`/`.pu`/`.iuml`/`.wsd` or a ```` ```plantuml ````
   fence → PlantUML; `.d2` or ```` ```d2 ```` → D2; `.dsl` or ```` ```structurizr ```` → Structurizr.
2. The project already keeps diagrams in one engine (look for existing sources or
   fences next to the target) → stay consistent with it, unless that engine lacks the
   requested diagram type (see the table below).
3. Otherwise choose by what is being drawn:

| Request | Engine | Why |
|---|---|---|
| C4 model with several views (landscape, context, container, component, deployment, dynamic) from one model | Structurizr | One model, many consistent views |
| UML: sequence, class, activity, state, use case, object, timing, component/deployment UML | PlantUML | Most complete UML coverage |
| Gantt, mind map, WBS, network (nwdiag), JSON/YAML, wireframe (salt), archimate, EBNF/regex | PlantUML | Only engine with these types |
| Architecture or system overview, flowchart, box-and-arrow, grid layout, polished visual output | D2 | Modern layout and themes |
| ERD / SQL tables | D2 (`sql_table`) or PlantUML (ER) | D2 unless UML notation is asked for |
| A single quick C4 diagram inside Markdown | PlantUML (C4-PlantUML) | No workspace needed |

If two engines fit equally and the choice matters to the user, ask once, then proceed.

## 3. Load references

Always open `references/<engine>/skill-map.md` before writing or explaining syntax, even
for a simple diagram, then only the files it points to for this request. Do not load
another engine's references. If they do not cover a feature, use the official
documentation links in that skill map.

## 4. Run the mode

### `create`

1. Draft the diagram from the loaded references.
2. Apply a theme when the engine has one: D2 theme 3 (Flagship Terrastruct) and
   Structurizr "C4 Blue" unless the user asked for another style.
3. Write a standalone source file, or a fenced block (` ```plantuml `, ` ```d2 `,
   ` ```structurizr `) into an existing Markdown file when the context calls for it.
```

## vector (857-vector-db)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/vector-db
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/857-vector-db/1886-vector
- الوصف: Generate vector database setup

```markdown
Generate vector database setup. This plugin is part of the Plugin Hub developer tools collection.

Use the tools provided by the plugin-hub MCP server to accomplish tasks related to vector-db.
```

## engineer-design-diagram (1722-engineer-design-diagram)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/devops/engineer-design-diagram
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1722-engineer-design-diagram/4729-engineer-design-diagram
- الوصف: Generate production-grade engineering design diagrams (architecture,\

```markdown
# Engineer Design Diagram

Generates production-grade engineering design diagrams as single-file HTML with inline SVG, grounded in real repository topology. Credit: design palette + arrow-masking pattern inspired by [Cocoon AI's architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) (MIT). See [THIRD_PARTY_LICENSES.md](references/THIRD_PARTY_LICENSES.md).

## Overview

Most diagramming tools produce pretty pictures disconnected from reality. This skill does the opposite: it reads the actual repo (package manifests, docker-compose, k8s, terraform, import graph) and emits a diagram that reflects the real system. It also knows how the system *changed* — PR-diff mode highlights structural deltas, trace mode turns a stack/log into a sequence diagram, and drift mode detects when the architecture has wandered from a stored fingerprint.

Four modes share a common pipeline (DCI grounding → node/edge graph → template fill → fingerprint write). Output is a single self-contained HTML file that opens in any browser, plus a Mermaid text block for copy-paste into docs. Dark theme with semantic OKLCH color coding by component role. Accessible by default (ARIA, `<title>`/`<desc>`, reduced-motion, keyboard navigation).

## Layout Philosophy — pick the shape before you draw

Dense technical systems want to render **wide**. This is how Anthropic docs, Linear docs, and Vercel architecture pages present multi-component systems: a sticky left rail for context (nav, invariants, legend) and a generous main column for the diagram itself. Mimic that pattern when your content is dense, and use the simpler single-SVG hero when it isn't.

Two supported output shapes, one decision up front:

| Shape | Use when | Template |
|-------|----------|----------|
| **Single-SVG hero** (classic) | ≤8 nodes, one-screen takeaway, no sub-grouping, no accompanying explanation needed | `templates/base.html` |
| **Docs-layout page** (widescreen) | ≥8 nodes, multiple planes/groupings/sub-blocks, want invariants + detail cards + legend alongside the diagram | `templates/docs-layout.html` |

**Widescreen-first for docs-layout.** Target `min-width: 1024px`; do *not* add mobile breakpoints for docs-layout output — it's architecture documentation, not a landing page. The diagram needs horizontal breathing room. On narrow viewports the diagram stage scrolls horizontally inside its card while the sidebar stays visible.
```
