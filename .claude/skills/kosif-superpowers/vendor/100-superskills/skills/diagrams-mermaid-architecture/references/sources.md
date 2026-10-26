# مصادر «المخططات والرسوم الهندسية» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## ln-25-architecture-diagram-builder (2179-architecture-suite)

- الترخيص: **MIT**  ·  الأصل: https://github.com/levnikolaevich/claude-code-skills/tree/a5d6eabb550ac95d4d9a1ae08ab6006d1ef508f1/plugins/architecture-suite
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2179-architecture-suite/7964-ln-25-architecture-diagram-builder
- الوصف: Creates evidence-backed current or target architecture diagrams; not UI design.

```markdown
# Architecture Diagram Builder

**Goal:** Create the smallest set of understandable, evidence-backed diagrams needed to communicate current or proposed architecture. Change only approved architecture documentation; do not invent relationships, perform visual product design, replace prose evidence, audit fitness, or edit implementation.

**Execution contract:** The checklist defines completion. Track each item internally as `PENDING`, `PROVEN` with evidence, `CLEARED` with evidence its condition is absent, or `UNPROVEN` with a gap; reading, delegation, tool failure, a zero exit status, or a self-reported success is not proof; only the observed outcome is. Reconcile after each section. Before returning, resolve all `PENDING`, count only `PROVEN` and `CLEARED`, and apply verdict and approval rules to every gap.
Preserve intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. When no one can answer during the run, state the exact question and apply the skill's verdict for the remaining gap instead of waiting or guessing. Scale depth to material risk without skipping checks. Preserve dependency and safety order; otherwise choose an appropriate verification method.
Accept equivalent user or repository evidence; no other skill, named artifact, or complete lifecycle is required. Preserve source requirement and decision IDs. Bind reused evidence to relevant source versions, dirty changes, configuration, and environment; invalidate only affected claims.
On continuation, reconcile task, authorization, current state, and unresolved evidence. For long work, return a compact continuation record or update an already authorized artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and external-action authority.
Prepare authorized work before required approval. If blocked by an instruction, cite its exact source and unresolved boundary; do not invent approval gates from caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Architecture evidence | Repository files, runtime wiring, IaC, contracts, and approved artifacts | User-provided model with `UNVERIFIED` labels |
| Relationship tracing | Language intelligence, dependency tools, and focused search | Direct inspection of producers, consumers, and registrations |
| Diagram format | Existing repository convention and renderer | Mermaid in Markdown, then plain ASCII |
| Syntax verification | Repository renderer, parser, or preview | Manual fence, identifier, and relationship inspection |
| Document mutation | Minimal patch to approved diagram artifacts | Return `BLOCKED` if path or evidence boundary is unsafe |
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

## architecture-diagram (x4919-visual-gen)

- الترخيص: **WTFPL**  ·  الأصل: https://github.com/widnyana/eyay-toolkits/tree/50e222e396d3ea0b9a9cc65c4a5cf58d3c1cfa39/plugins/visual-gen
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/x4919-visual-gen/x20317-architecture-diagram
- الوصف: This skill should be used when the user asks to "create a diagram", "make an architecture diagram", "design a system diagram", "draw an architecture", "create a technical diagram", "make a deployment diagram", "visualize infrastructure", "create a data flow diagram", "draw system components", "make a network diagram", "diagram a cloud architecture", "draw an AWS diagram", "create a Kubernetes diag

```markdown
# Architecture Diagram

End-to-end architecture diagram generation. Gathers system information, produces an HTML file, renders it to PNG via Chrome headless, and delivers the final image. The entire export is automated -- the user never needs to open a browser or run a script manually.

Two visual styles: **dark theme** (default, SVG-based) and **light theme** (div-based, print-friendly).

## Workflow

### Step 1: Gather information

Before writing markup, identify from the request (ask clarifying questions if anything is ambiguous):

- **Components**: servers, services, databases, queues, external systems
- **Data flow**: direction of requests (top-down, left-to-right, mixed)
- **Groupings**: which components belong together (VPC, cluster, tier)
- **Boundary types**: cloud regions, security groups, Kubernetes namespaces
- **Theme**: dark (default) or light (for print/slides/white-background docs)
- **Output path**: where to save the final PNG (default: `tmp/` in the project directory)

When the request references a blog post or design document, read it and extract component names and relationships before writing markup.

Ask the user for clarification only when the system description is genuinely ambiguous. Do not ask questions that can be reasonably inferred.

### Step 2: Select style and start the file

**Dark theme (default):** Copy `resources/template.html` as the starting point. Includes inline SVG, CSS, grid background, arrowhead marker, export toolbar stub, and example component patterns.

**Light theme:** Build from the patterns in `references/diagram-styles.md`. Div-based layout with CSS classes (`.node .service`, `.db`, `.group`), Inter font, white `#FFFFFF` background.

For either style, do not start from a blank file. Save the working HTML to `tmp/` with a descriptive filename (e.g., `tmp/my-project-architecture.html`).

### Step 3: Place components

**Dark theme:** SVG `<rect>` + `<text>` pairs.

**Light theme:** div elements with category CSS classes.

Assign colors by semantic type:

| Type | Dark Stroke | Light Class | Use For |
|------|------------|-------------|---------|
| Frontend | `#22d3ee` (cyan) | `.service` | Web apps, mobile clients, SPAs |
| Backend | `#34d399` (emerald) | `.server` | API servers, microservices, workers |
| Database | `#a78bfa` (violet) | `.storage` | SQL, NoSQL, caches, object stores |
| Cloud | `#fbbf24` (amber) | `.infra` | AWS/GCP/Azure managed services |
| Security | `#fb7185` (rose) | `.external` | Auth providers, WAFs, IAM |
| Message Bus | `#fb923c` (orange) | `.storage` | Kafka, RabbitMQ, SQS, event buses |
| External | `#94a3b8` (slate) | `.external` | Third-party APIs, CDN, SaaS |

For exact fill values, SVG code snippets, and light-theme CSS, consult:
- Dark theme: `references/design-system.md`
```

## mermaid-cli (1245-mermaid-cli)

- الترخيص: **MIT**  ·  الأصل: https://github.com/dashed/claude-marketplace/tree/f6a24dbc08da57aeb80e7423da2508457d0b3398/plugins/mermaid-cli
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1245-mermaid-cli/2925-mermaid-cli
- الوصف: Generate, validate, and fix diagrams from Mermaid markup using the mermaid-cli (mmdc) tool. Use when creating flowcharts, sequence diagrams, class diagrams, state diagrams, ER diagrams, Gantt charts, pie charts, mindmaps, or any Mermaid-supported diagram type. Also use when validating, verifying, or fixing Mermaid diagram syntax. Triggers on mentions of mermaid, mmdc, diagram generation, diagram v

```markdown
# Mermaid CLI

## Overview

`mmdc` (Mermaid CLI) converts Mermaid diagram definitions into SVG, PNG, or PDF output. It is the official command-line interface for the Mermaid diagramming library, enabling text-based diagram generation without a browser.

Write diagram definitions in `.mmd` files using Mermaid's declarative syntax, then run `mmdc` to produce publication-ready output. This is the primary tool for generating diagrams from text in automated and scripting workflows.

`mmdc` also serves as a **syntax validator**: any render attempt validates the diagram. If the Mermaid syntax is invalid, mmdc exits with a non-zero code and reports parse errors to stderr. This enables iterative validate-and-fix workflows.

## Prerequisites

**CRITICAL**: Before proceeding, you MUST verify that mermaid-cli is installed:

```bash
mmdc --version
```

**If mmdc is not installed:**
- **DO NOT** attempt to install it automatically
- **STOP** and inform the user that mermaid-cli is required
- **RECOMMEND** manual installation with the following options:

```bash
# npm (global install)
npm install -g @mermaid-js/mermaid-cli

# npx (no install, run directly)
npx -p @mermaid-js/mermaid-cli mmdc --help

# Docker
docker pull minlag/mermaid-cli

# See https://github.com/mermaid-js/mermaid-cli for more options
```

**If mmdc is not available, exit gracefully and do not proceed with the workflow below.**

## Basic Workflow

### Step 1: Write the Diagram

Create a `.mmd` file with Mermaid syntax:

```bash
cat <<'EOF' > diagram.mmd
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
EOF
```

### Step 2: Generate Output

```bash
# Generate SVG (default, best for web)
mmdc -i diagram.mmd -o diagram.svg

# Generate PNG (raster image)
mmdc -i diagram.mmd -o diagram.png

# Generate PDF (document embedding)
mmdc -i diagram.mmd -o diagram.pdf
```

### Step 3: Verify

On success, mmdc prints `Generating single mermaid chart` and exits with code 0. Check that the output file was created and is non-empty.

## Common Patterns

### Pattern 1: Generate SVG from File

The most common workflow. SVG is the default and recommended format.

```bash
mmdc -i flowchart.mmd -o flowchart.svg
```

### Pattern 2: Generate PNG with Theme and Background

Customize appearance with theme and background color.

```bash
# Dark theme with white background
mmdc -i diagram.mmd -o diagram.png -t dark -b white

# Forest theme with transparent background
mmdc -i diagram.mmd -o diagram.png -t forest -b transparent
```

### Pattern 3: Generate PDF with Fit-to-Page

Use `--pdfFit` to scale the diagram to fit the PDF page.

```bash
mmdc -i diagram.mmd -o diagram.pdf --pdfFit
```

### Pattern 4: Inline Diagram via Heredoc
```

## aws-architecture-diagram (373-deploy-on-aws)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/awslabs/agent-plugins/tree/097fe8ad56d8a1d5e2c81d7880adf145553cf244/plugins/deploy-on-aws
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/373-deploy-on-aws/1376-aws-architecture-diagram
- الوصف: Generate validated AWS architecture diagrams as draw.io XML using official AWS4 icon libraries. Use this skill whenever the user wants to create, generate, or design AWS architecture diagrams, cloud infrastructure diagrams, or system design visuals. Also triggers for requests to visualize existing infrastructure from CloudFormation, CDK, or Terraform code. Supports two modes: analyze an existing c

```markdown
You are an AWS architecture diagram generator that produces draw.io XML files with official AWS4 icons. The diagrams you produce MUST match the style of official AWS Reference Architecture diagrams — professional title and subtitle, teal numbered step badges with a right sidebar legend, 48x48 service icons inside colored category containers, clean Helvetica typography, and clear data flow.

## Workflow

### Step 1: Determine Mode

**Mode A — Codebase Analysis:** If the user says "analyze", "scan", "from code", or references their existing project:

1. Scan for infrastructure files: CloudFormation (`AWSTemplateFormatVersion`, `AWS::*`), CDK (`cdk.json`, construct definitions), Terraform (`resource "aws_*"`)
2. Extract services, relationships, VPC structure, and data flow direction
3. If NO AWS infrastructure files found, scan for non-AWS technologies: Dockerfiles, database configs, API integrations, ML frameworks (pytorch, tensorflow, coreml), message brokers (kafka, rabbitmq). Map discovered technologies using `references/general-icons.md`
4. For MIXED architectures (AWS + non-AWS): use AWS icons for AWS services, general icons for non-AWS. Same layout rules apply.
5. Confirm discovered architecture with user before generating
6. Ask which diagram type best represents the architecture

**Mode B — Brainstorming:** If the user describes an architecture or says "brainstorm"/"design"/"from scratch":

1. Ask 3-5 focused questions (purpose, services, scale, security, traffic pattern)
2. Propose the architecture with service recommendations and data flow
3. Iterate if needed, then generate

### Step 2: Styling Selections

These are independent of Mode and apply after mode selection:

- **Sketch mode**: Activated ONLY if user says "sketch", "hand-drawn", or "sketchy". Default: OFF (Helvetica, no sketch attributes). See Sketch Mode in Style Rules below.
- **Legend panel**: Activated by default for 7+ services or multiple branching paths. Disabled ONLY if user says "no legend", "without legend", "skip steps", or "no sidebar".
- **Export format**: Check for format keywords (png, svg, pdf). Default: `.drawio` only.

### Step 3: Generate Diagram XML

**Load references now** (not before this step):

1. Read `references/xml-rules.md` for shape styles, label placement, and structural rules
2. Read `references/style-guide.md` for colors, fonts, and dark mode
3. Read `references/xml-templates-structure.md` for XML code blocks
4. Read `references/layout-guidelines.md` for spacing and edge routing
5. Use the example entries in the table below only as conceptual guidance for edge routing and layout patterns; do not open or read any `.drawio` files as reference.

**Example selection** — pick the most relevant example for the user's architecture:
```

## akbun-draw-architecture (1095-akbun-draw-architecture)

- الترخيص: **MIT**  ·  الأصل: https://github.com/choisungwook/akbun-aitools/tree/b592650776c4ed1723087911010466d0b537fc6b/plugins/akbun-draw-architecture
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1095-akbun-draw-architecture/2428-akbun-draw-architecture
- الوصف: 시스템 아키텍처를 경계(조직, 네트워크, 실행 환경 등)는 점선 박스로, 그 안의 컴포넌트는 역할별 색 박스로 그리는 flat SVG 그림을 만든다. 데이터가 저장되는 경로는 실선, 조회 경로는 점선으로 구분한다. 특정 벤더나 제품에 묶이지 않는 추상 표현을 쓴다. Trigger on: "아키텍처 그려줘", "구조 시각화", "데이터 흐름 그림", "경계 나눠서 그려줘", "architecture diagram", "boundary diagram", or any request to draw system structure or data flow in this style.

```markdown
# 경계 아키텍처 그림

한 장에 하나의 질문만 답하는 설명용 SVG를 만든다. "무엇이 어느 경계 안에 있고, 데이터가 어느 방향으로 흐르나"가 3초 안에 읽혀야 한다.

## 먼저 정할 것

그리기 전에 세 가지를 한 줄씩 정한다. 정하지 못하면 그리지 말고 질문부터 다시 받는다.

1. 이 그림이 답하는 질문 한 줄 (예: "저장소는 왜 혼자 데이터를 받지 못하나")
2. 경계 목록: 소유, 네트워크, 실행 환경, 신뢰 영역처럼 점선 박스가 될 것
3. 흐름 목록: 저장·쓰기 경로(실선)와 조회·읽기 경로(점선)

## 추상화 규칙

- 그림 안 라벨은 역할로 쓴다: 서비스, 처리기, 수집기, 저장소, 조회 화면, 사용자, 게이트웨이, 큐
- 사용자가 준 자료에 제품명이 있어도, 사용자가 이름을 넣으라고 하지 않으면 역할 이름으로 바꾼다
- 경계 라벨도 역할로 쓴다: "소스 영역 A", "중앙 영역", "외부 제공자", "실행 환경"
- 특정 벤더의 아이콘, 로고, 색은 쓰지 않는다

## 캔버스

- `viewBox="0 0 680 H"`, `width="100%"`. 가로 680은 바꾸지 않는다. 내용이 좁으면 가운데에 둔다
- H는 가장 아래 요소 + 40px
- 안전 영역: x 30~650, y 30~(H-30)
- 루트 `<svg>`에 `role="img"`, 첫 자식으로 `<title>`(2~4단어)과 `<desc>`(한 문장 요약)
- 배경은 투명. 그라데이션, 그림자, blur, 이미지 아이콘은 쓰지 않는다

## 도형 규칙

| 요소 | 모양 |
|---|---|
| 경계 | `rx="8"`, fill 없음, stroke `#888780`, `stroke-dasharray="4 4"`, 왼쪽 위에 12px 라벨 |
| 컴포넌트 | `rx="4"` 사각형, 높이 44~64, 제목 14px + 부제 12px 두 줄 |
| 외부가 운영하거나 선택 사항인 컴포넌트 | 컴포넌트 테두리에 `stroke-dasharray="4 3"` |
| 화살표 | stroke `#888780`, 1px, 끝에 삼각형 marker 하나 |
| 저장·쓰기 경로 | 실선 |
| 조회·읽기 경로 | `stroke-dasharray="3 3"` |
| 화살표 라벨 | 12px, 선 위 10px, 3~6글자 동사 ("긁기", "넣기", "조회") |

- 한 가로줄에 컴포넌트는 4개까지. 넘으면 줄을 나누거나 그림을 둘로 나눈다
- 같은 줄의 박스 사이 간격은 20px 이상
- 경계 박스끼리 60px 이상 띄워 화살표 라벨 자리를 남긴다

## 색은 의미로만 쓴다

한 그림에 색 ramp는 회색 + 최대 2개까지 쓴다. 순서대로 돌려 쓰지 않는다.

| 의미 | ramp | 라이트 fill / stroke / 제목 / 부제 | 다크 fill / stroke / 제목 / 부제 |
|---|---|---|---|
| 중립(서비스, 사용자, 입력) | gray | #F1EFE8 / #5F5E5A / #444441 / #5F5E5A | #444441 / #B4B2A9 / #F1EFE8 / #B4B2A9 |
| 직접 운영, 상태 없음 | teal | #E1F5EE / #0F6E56 / #085041 / #0F6E56 | #085041 / #5DCAA5 / #E1F5EE / #5DCAA5 |
| 저장, 상태 있음 | coral | #FAECE7 / #993C1D / #712B13 / #993C1D | #712B13 / #F0997B / #FAECE7 / #F0997B |
| 외부가 운영 | purple | #EEEDFE / #534AB7 / #3C3489 / #534AB7 | #3C3489 / #AFA9EC / #EEEDFE / #AFA9EC |

- 색 박스 위 글자는 같은 ramp의 진한 단계만 쓴다. 검정이나 회색을 쓰지 않는다
- 색이 의미를 가지면 그림 아래에 한 줄 범례를 둔다

다크 모드는 SVG 안 `<style>`의 class와 media query로 처리한다. 아래는 SVG `<style>`에 그대로 넣는 CSS다.

```css
.n-gray rect{fill:#F1EFE8;stroke:#5F5E5A}.n-gray .th{fill:#444441}.n-gray .ts{fill:#5F5E5A}
.n-teal rect{fill:#E1F5EE;stroke:#0F6E56}.n-teal .th{fill:#085041}.n-teal .ts{fill:#0F6E56}
.n-coral rect{fill:#FAECE7;stroke:#993C1D}.n-coral .th{fill:#712B13}.n-coral .ts{fill:#993C1D}
.n-purple rect{fill:#EEEDFE;stroke:#534AB7}.n-purple .th{fill:#3C3489}.n-purple .ts{fill:#534AB7}
.th{font:500 14px sans-serif;fill:#2C2C2A}.ts{font:400 12px sans-serif;fill:#5F5E5A}
@media (prefers-color-scheme:dark){
.n-gray rect{fill:#444441;stroke:#B4B2A9}.n-gray .th{fill:#F1EFE8}.n-gray .ts{fill:#B4B2A9}
.n-teal rect{fill:#085041;stroke:#5DCAA5}.n-teal .th{fill:#E1F5EE}.n-teal .ts{fill:#5DCAA5}
.n-coral rect{fill:#712B13;stroke:#F0997B}.n-coral .th{fill:#FAECE7}.n-coral .ts{fill:#F0997B}
```
