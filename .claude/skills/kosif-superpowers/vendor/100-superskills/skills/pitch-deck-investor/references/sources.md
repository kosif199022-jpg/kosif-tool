# مصادر «عرض المستثمرين» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## build-investor-pipeline (2386-startup-fundraising)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/startup-fundraising
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2386-startup-fundraising/9237-build-investor-pipeline
- الوصف: Build a tiered, stage-fit investor pipeline and a warm-intro-first outreach sequence for a founder running a round. Produces a target list scored by stage-fit + thesis-fit + check-size, a warm-path map for each target, and a sequenced outreach plan that builds momentum. Reach for this when the user asks "who should I pitch?", "build my investor list", or "how do I run outreach?". Used by `fundrais

```markdown
# Skill: build-investor-pipeline

> **Invoked by:** `fundraising-strategist` (primary). Coordinated with `pitch-and-narrative-coach` (the narrative must fit each target's thesis).
>
> **When to invoke:** "who should I raise from?"; "build my investor list"; "how do I sequence outreach?"; any time a founder is about to start (or is mid-) a raise.
>
> **Output:** a scored target list + a warm-intro path per target + a sequenced outreach plan + the CRM fields to track.

## Procedure

1. **Confirm the round shape first.** Pull stage, instrument, and target raise from the `fundraising-strategist` (or the stages decision tree, [`../../knowledge/fundraising-stages-decision-tree.md`](../../knowledge/fundraising-stages-decision-tree.md)). The pipeline is shaped by *who writes checks at this stage and size* — a Series A lead is noise in a pre-seed.
2. **Build the target universe.** Source from: existing network, angels/operators in the space, stage-appropriate funds, accelerator/syndicate networks, and "who funded comparable companies" (look up recent rounds for adjacent startups). Capture each as a CRM row.
3. **Score each target on three axes.**
   - **Stage-fit** — do they lead/follow at this stage and check size?
   - **Thesis-fit** — does the company match a stated thesis, sector, or recent investment pattern?
   - **Warm-path strength** — is there a strong intro, a weak intro, or only a cold path?
   Tier into **A / B / C** from the combined score.
4. **Map the warm path for every A and B target.** For each, name the best mutual connection and the specific ask of that connection. Warm intros convert far better than cold outreach — spend social capital deliberately.
5. **Sequence for momentum, not volume.** Open with a small "practice" tier (friendly, lower-stakes) to refine the pitch, then move to the highest-conviction A targets while the round has energy. Avoid burning all top targets simultaneously before the pitch is tight. Aim to create a sense of an active, time-boxed process.
6. **Define the CRM fields + cadence.** Minimum columns: firm/partner, tier, stage-fit, thesis-fit, warm path, status (not-contacted → intro-requested → intro'd → meeting → diligence → committed/passed), next action, next-action date, check-size, notes. Set a weekly review cadence; track the *funnel*, not just the list.
7. **Gate outreach on data-room readiness.** Don't go wide before the data room exists — drive [`../prepare-data-room/SKILL.md`](../prepare-data-room/SKILL.md) first so a "send me the deck/data" reply doesn't stall.

## Worked example

> Founder raising a $1.5M pre-seed on a post-money SAFE.

- Target universe → ~40 names: 12 angels/operators in the space, 18 pre-seed funds, 6 accelerator-network connections, 4 syndicate leads.
```

## presentation-builder (2663-presentation)

- الترخيص: **BSD-3-Clause**  ·  الأصل: https://github.com/neuromechanist/research-skills/tree/f0219bde233abb44d8a0c5d73f41ea27073e1493/plugins/presentation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2663-presentation/10128-presentation-builder
- الوصف: This skill should be used when the user asks to "create a presentation", "make slides", "build a slide deck", "create a talk", "make a keynote", "create a Reveal.js presentation", "generate presentation slides", "make a conference talk", "create a lecture", "build a poster presentation", "create presentation JSON", or mentions presentations, slides, slide decks, Reveal.js, talk preparation, confer

```markdown
# Presentation Builder

Create interactive Reveal.js presentations from JSON using the [Agentic Presentation Builder](https://github.com/neuromechanist/agentic-presentation-builder). The builder transforms structured JSON definitions into professional, interactive web-based presentations with Mermaid diagrams, LaTeX math, syntax-highlighted code, and animated progressive reveals.

## Pipeline Overview

```
1. Plan structure  -->  2. Author JSON  -->  3. Validate  -->  4. Serve & present
   (outline, theme)     (schema-driven)      (CLI validator)    (Vite dev server)
```

## Prerequisites: get the builder CLI

The engine ships an `apb` command (subcommands `validate`, `present`, `export`, `shoot`). Two ways to
run it; pick per situation. Pin the tag (`#v0.1.8`) for reproducibility.

**Zero-setup (default, no clone).** Run straight from the repo with bunx (or npx):

```bash
bunx github:neuromechanist/agentic-presentation-builder#v0.1.8 validate deck.json --json
```

**Iterative authoring / offline (recommended when validating repeatedly).** Use a managed
cache clone so each call does not re-resolve the git package. Resolve a builder home, cloning
once if needed, then run the `bun run` scripts from it:

```bash
APB_HOME="${APB_HOME:-$HOME/.cache/agentic-presentation-builder}"
if [ ! -d "$APB_HOME/.git" ]; then
  git clone --branch v0.1.8 https://github.com/neuromechanist/agentic-presentation-builder.git "$APB_HOME"
  (cd "$APB_HOME" && bun install)
fi
# then, e.g.:
(cd "$APB_HOME" && bun run validate -- "$(pwd)/deck.json" --json)
```

In the steps below, "`apb <command>`" means either the bunx form or `bun run <command> --`
from `$APB_HOME`. Both share one code path, so flags are identical.

## Step 1: Plan the Presentation

Before writing JSON, determine:

- **Topic and audience**: Shapes content depth and vocabulary
- **Slide count**: 8-12 for a short talk, 15-25 for a full session
- **Theme**: `academic` for research talks, `default` for general, `dark` for tech demos
- **Key visuals**: Which slides need Mermaid diagrams, images, code blocks, or tables
- **Speaker notes**: Include delivery guidance for each slide

## Step 2: Author the Presentation JSON

Write a `presentation.json` following the schema. See `references/schema-reference.md` for the complete field reference and `references/authoring-guide.md` for best practices.

### Minimal structure

```json
{
  "presentation": {
    "metadata": {
      "title": "My Presentation",
      "author": "Author Name",
      "theme": "academic",
      "aspectRatio": "16:9",
      "controls": {
        "slideNumbers": true,
        "progress": true
      }
    },
    "slides": [
      {
        "id": "title",
        "layout": "title",
        "elements": [
          {
            "type": "text",
```

## startup-financial-modeling (3524-startup-business-analyst)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/startup-business-analyst
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3524-startup-business-analyst/14299-startup-financial-modeling
- الوصف: Build comprehensive 3-5 year financial models with revenue projections, cost structures, cash flow analysis, and scenario planning for early-stage startups. Use this skill when creating financial projections, calculating burn rate or runway, modeling fundraising scenarios, or preparing investor-ready financials for a seed or Series A raise.

```markdown
# Startup Financial Modeling

Build comprehensive 3-5 year financial models with revenue projections, cost structures, cash flow analysis, and scenario planning for early-stage startups.

## Overview

Financial modeling provides the quantitative foundation for startup strategy, fundraising, and operational planning. Create realistic projections using cohort-based revenue modeling, detailed cost structures, and scenario analysis to support decision-making and investor presentations.

## Core Components

### Revenue Model

**Cohort-Based Projections:**
Build revenue from customer acquisition and retention by cohort.

**Formula:**

```
MRR = Σ (Cohort Size × Retention Rate × ARPU)
ARR = MRR × 12
```

**Key Inputs:**

- Monthly new customer acquisitions
- Customer retention rates by month
- Average revenue per user (ARPU)
- Pricing and packaging assumptions
- Expansion revenue (upsells, cross-sells)

### Cost Structure

**Operating Expenses Categories:**

1. **Cost of Goods Sold (COGS)**
   - Hosting and infrastructure
   - Payment processing fees
   - Customer support (variable portion)
   - Third-party services per customer

2. **Sales & Marketing (S&M)**
   - Customer acquisition cost (CAC)
   - Marketing programs and advertising
   - Sales team compensation
   - Marketing tools and software

3. **Research & Development (R&D)**
   - Engineering team compensation
   - Product management
   - Design and UX
   - Development tools and infrastructure

4. **General & Administrative (G&A)**
   - Executive team
   - Finance, legal, HR
   - Office and facilities
   - Insurance and compliance

### Cash Flow Analysis

**Components:**

- Beginning cash balance
- Cash inflows (revenue, fundraising)
- Cash outflows (operating expenses, CapEx)
- Ending cash balance
- Monthly burn rate
- Runway (months of cash remaining)

**Formula:**

```
Runway = Current Cash Balance / Monthly Burn Rate
Monthly Burn = Monthly Revenue - Monthly Expenses
```

### Headcount Planning

**Role-Based Hiring Plan:**
Track headcount by department and role.

**Key Metrics:**

- Fully-loaded cost per employee
- Revenue per employee
- Headcount by department (% of total)

**Typical Ratios (Early-Stage SaaS):**

- Engineering: 40-50%
- Sales & Marketing: 25-35%
- G&A: 10-15%
- Customer Success: 5-10%

## Financial Model Structure

### Three-Scenario Framework

**Conservative Scenario (P10):**

- Slower customer acquisition
- Lower pricing or conversion
- Higher churn rates
- Extended sales cycles
- Used for cash management

**Base Scenario (P50):**

- Most likely outcomes
- Realistic assumptions
- Primary planning scenario
- Used for board reporting

**Optimistic Scenario (P90):**

- Faster growth
- Better unit economics
- Lower churn
- Used for upside planning

### Time Horizon
```

## lf-member-pitch-deck (2867-member-pitch-deck)

- الترخيص: **MIT**  ·  الأصل: https://github.com/paulhinz/lf-marketing-os/tree/7afedc8b475a3fa4cfe0090bf30d6f4ade2ee593/plugins/member-pitch-deck
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2867-member-pitch-deck/11577-lf-member-pitch-deck
- الوصف: This skill should be used when a Linux Foundation membership development rep, Executive Director, or Project Leader says "lf-member-pitch-deck", "Create pitch deck for [project]", "build a member pitch deck for [project]", "make a first-meeting deck for [project]", "generate the member recruitment deck", or otherwise asks for a presentation to use in a first meeting with a prospective member or ot

```markdown
# LF Member Pitch Deck

Generate the standard first-meeting membership pitch deck for a Linux Foundation project or foundation. One standard deck per project — do NOT build fully custom per-prospect decks. Prospect-specific context goes into speaker notes and the prep brief only.

The deck must accomplish four goals, in order: grab attention (show deep understanding of the prospect segment's business challenges), explain value (a clear membership value proposition), build trust (social proof, data, case studies), and inspire action (one clear next step).

**Formatting is not a choice.** Every deck is built on the LF 2025 Template bundled at `assets/LF-2025-Template.pptx` by running `scripts/build_deck.py`. The script uses only the template's own slide layouts, so fonts, sizes, colors, the LF logo, the gradient footer bar and slide numbers all come from the template. Do not build the deck with the generic pptx skill, do not start from a blank presentation, and do not override the template's fonts, sizes or colors.

## Step 1 — Identify the project and gather foundational inputs

Determine the project name from the user's request. Then locate the three foundational documents, in priority order:

1. **Brand Kit** (or a link to brand guidelines) — voice, terminology, logo file, prohibited terms
2. **Message Foundation doc** — locked summaries, boilerplate, elevator pitch, messaging pillars, proof points
3. **ICP & Target Markets doc** — personas, segments, pain points, fit scoring

Look for them as conversation attachments, in the connected working folder, or in the project's Google Drive folder (via the Google Drive connector if connected). If a document can't be found, ask the user to attach it or provide a link.

**Fallback:** if some or all foundational docs are missing, do not invent positioning. Ask the presenter the key questions in `references/key-questions.md` — a minimum of 3 and a maximum of 7, selecting only the questions whose answers are not already covered by whichever docs exist. If no foundational docs exist AND the user declines to answer the questions, stop and explain that the deck cannot be responsibly generated without positioning inputs.

**Brand Kit and the template:** the LF 2025 Template sets the visual system (Open Sans, LF navy/blue/cyan, LF logo footer). The project's Brand Kit supplies the project logo (placed in picture placeholders), voice, terminology and approved imagery. It never overrides the template's layouts, fonts or colors.

## Step 2 — Optional prospect research (speaker notes only)

If the user named a prospect company, gather read-only context to personalize the presenter's prep — never the slides themselves:

- **HubSpot** (if connected): the prospect's company record, deal stage, prior touchpoints
```

## akbun-presentation-paper (1098-akbun-presentation)

- الترخيص: **MIT**  ·  الأصل: https://github.com/choisungwook/akbun-aitools/tree/b592650776c4ed1723087911010466d0b537fc6b/plugins/akbun-presentation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1098-akbun-presentation/2475-akbun-presentation-paper
- الوصف: 주제·원본 자료(글·논문·코드·장애 경험)를 받아 논문형식 발표 덱(.pptx)과 슬라이드별 상세 발표 대본(.md)을 함께 만든다. 기본은 라이트 샌드위치 형식 — 다크 표지·섹션 슬라이드가 흰 내용 슬라이드를 감싸고, 노란 세로 바 섹션 표지 + "N. 섹션명" 헤더 + ■/- 불릿 + 검정 얇은 선 다이어그램 + VS Code 스타일 코드 패널 + 링크 푸터 + 페이지 번호를 쓴다. 질문 훅으로 스토리를 끌고 가고 노랑 포인트·빨강 문제 강조를 쓴다. 발표 시간·슬라이드 수·청중·언어는 사용자 설정으로 받고, 미지정 항목은 기본값을 쓴다. 덱 스타일과 레이아웃은 design.md를 따르고, 삽입용 래스터 시각자료는 akbun-presentation-visual에 위임한다. 발표 대본은 발표자가 이 분야

```markdown
# akbun 논문형식 발표자료 생성

`paper`는 논문형식 발표를 뜻한다. 기존 `akbun-presentation`의 제작 방식을 이어받는다. 새 고정 다크 디자인은
[akbun-presentation](../akbun-presentation/SKILL.md)을 사용한다.

## 이 skill이 하는 일

주제 하나만 받아도, 원본 자료(블로그 글·논문·문서·코드·장애 회고)를 받아도 akbun 스타일 발표
덱으로 만든다. 산출물은 세 가지다.

1. **슬라이드 아웃라인** — 슬라이드별 유형·제목·핵심 메시지를 정리한 표. 생성 전 확인용.
2. **.pptx 파일** — pptxgenjs로 생성한 발표 파일. PowerPoint로 열거나 Google Slides로 가져간다.
3. **발표 대본 .md 파일** — 슬라이드별 상세 대본. 요약본이 아니라 발표자가 그대로 읽고 설명할 수
   있는 완성 원고다.

발표 대본이 이 skill의 절반이다. 슬라이드만 잘 만들고 대본을 슬라이드 요약으로 때우면 실패다.

## 사용자 설정

사용자가 설정을 주면 그대로 따르고, 주지 않은 항목은 아래 기본값을 쓴다. 설정을 물어보느라
작업을 멈추지 않는다. 쓴 값은 작업 시작할 때 한 번 요약해 보여준다.

| 항목 | 기본값 |
|---|---|
| 원본 자료 | 없으면 주제만으로 구성한다 |
| 참고할 기존 PPT | 없음 |
| 발표 시간 | 10분 |
| 목표 슬라이드 수 | 발표 시간 × 1.2~1.5장 (10분이면 12~15장), 상한 30장 |
| 청중 및 난이도 | 배경지식이 부족한 소프트웨어 엔지니어 |
| 발표자의 현재 배경지식 | 이 분야를 처음 접함 |
| 언어 | 슬라이드는 영어, 발표 대본은 한국어 |
| 스타일 | 라이트 샌드위치 (다크 스텝은 요청하거나 참고 PPT가 다크일 때) |

"30장 미만"은 상한이지 목표가 아니다. 10분에 30장이면 슬라이드당 20초라 대본을 읽을 수 없다.
사용자가 슬라이드 수를 직접 지정하지 않았다면 발표 시간에서 계산한 값을 쓰고, 아웃라인에
"10분 / 14장 / 슬라이드당 평균 43초"처럼 근거를 적어 보여준다.

참고 PPT가 주어지면 색·여백·글꼴·전반적인 분위기를 그쪽에 맞추고, 어떤 스타일로 판단했는지
아웃라인에 한 줄 적는다. 배치를 그대로 복사하지는 않는다.

## 작업 순서

1. **design.md 숙지.** [design.md](design.md)에서 색·타이포·레이아웃·그림 언어·말투를 읽는다.
2. **설정 확정.** 위 표대로 설정을 정하고, 원본 자료가 있으면 먼저 끝까지 읽는다.
3. **아웃라인 작성.** 아래 `1. 발표자료 구성` 규칙으로 슬라이드별 유형·제목·핵심 메시지를 표로 만든다.
4. **아웃라인 확인.** 사용자에게 보여주고 진행한다(피드백이 있으면 반영).
5. **대본 먼저 쓴다.** 슬라이드보다 대본을 먼저 쓰면 슬라이드에 뭘 넣고 뭘 빼야 하는지가 정해진다.
   [references/script-template.md](references/script-template.md)를 따른다.
6. **시각자료 생성.** 원본 시각자료로 설명이 부족한 슬라이드는
   [akbun-presentation-visual](../akbun-presentation-visual/SKILL.md)에 핵심 메시지·라벨·관계·출처·스타일을
   브리프로 넘겨 삽입용 이미지를 만든다.
7. **pptx 생성.** [references/pptxgenjs-kit.md](references/pptxgenjs-kit.md)의 검증된 스타일
   키트를 읽고 그대로 복사해 시작한다. 좌표를 잡을 때 라벨·마커가 겹치지 않는지 계산한다.
8. **QA.** 아래 `8. 최종 검수` 목록을 실제로 렌더링해 확인하고, 문제가 있으면 고친 뒤 다시 확인한다.
9. **출력.** 아래 `9. 최종 결과물` 형식으로 답한다.

## 1. 발표자료 구성

- 전체 분량은 확정한 목표 슬라이드 수에 맞춘다.
- 원본 자료가 있으면 그 논리와 전개 순서를 최대한 충실하게 반영한다.
- 기본 전개는 **문제·목적 → 필요한 배경지식 → 핵심 아이디어 → 구체적인 방법·시스템·과정 →
  수식·분석 → 결과와 근거 → 한계와 함의**다. 자료 성격에 맞지 않는 단계는 억지로 넣지 말고
  자연스럽게 조정한다. 논문에는 수식·분석 단계가 있지만 장애 회고에는 없다.
- 각 슬라이드는 **핵심 메시지 하나**만 전달한다. 말할 게 두 개면 슬라이드를 나눈다.
- **슬라이드 제목만 순서대로 읽어도 전체 발표의 논리 흐름이 이해돼야 한다.** 아웃라인을 다 쓴 뒤
  제목 열만 세로로 읽어보고, 흐름이 끊기면 제목을 고친다.
- 원본 자료의 중요한 Figure·Chart·Table·Diagram·Algorithm·수식·사례는 빠뜨리지 않는다.
- 발표 시간 안에 설명하기 어려운 부가 내용은 핵심 슬라이드에 욱여넣지 말고 대본이나 부록
  슬라이드로 분리한다.

## 2. 디자인

색·타이포·레이아웃·그림 언어·스크린샷 규칙 등 "결과물이 어떻게 생겼는가"는 모두
[design.md](design.md)가 단일 기준이다. 여기에 값을 다시 적지 않는다. design.md는 도구에
의존하지 않는 자기완결 스펙이라 다른 곳에 복붙해 재사용할 수 있고, 그 스펙을 pptxgenjs로 구현한
코드 키트는 [references/pptxgenjs-kit.md](references/pptxgenjs-kit.md)에 있다.

## 3. 글꼴과 크기

[design.md](design.md)의 타이포그래피 표를 따른다. 표의 하한선(라벨·표 글자 10pt, 수식 20pt)에
```

## akbun-presentation-visual (1098-akbun-presentation)

- الترخيص: **MIT**  ·  الأصل: https://github.com/choisungwook/akbun-aitools/tree/b592650776c4ed1723087911010466d0b537fc6b/plugins/akbun-presentation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1098-akbun-presentation/2476-akbun-presentation-visual
- الوصف: 발표 내용·슬라이드 브리프·원본 Figure를 받아 akbun 발표 스타일의 16:9 시각자료 이미지를 만든다. 라이트 샌드위치와 다크 스텝의 색 문법으로 시스템 구조·과정·비교·문제 흐름을 단순화하며, 연속 슬라이드는 같은 구도에서 마커와 강조만 바꾼다. 발표 덱이나 대본은 만들지 않는다. Trigger on: "발표용 이미지 그려줘", "슬라이드 시각자료", "이 내용을 akbun 발표 그림으로", or when akbun-presentation-paper needs a raster visual for a slide.

```markdown
# akbun 발표 시각자료 생성

발표에서 설명할 관계·순서·비교·문제 지점을 한눈에 읽히는 16:9 이미지로 만든다. 이미지 생성 규칙은
[references/visual-style.md](references/visual-style.md)가 단일 기준이다.

## 책임과 경계

- 산출물은 슬라이드에 삽입할 이미지다. 덱 아웃라인, `.pptx`, 발표 대본은 만들지 않는다.
- 장식용 삽화보다 설명용 시각자료를 우선한다. 관계가 없는 내용은 억지로 다이어그램으로 만들지 않는다.
- 원본 Figure·Chart·Table·Diagram이 있으면 원본을 우선한다. 단순화해 다시 그릴 때는 의미·수치·단위를
  유지하고 `adapted from ...` 또는 `simplified view`로 구분할 출처 문구를 함께 반환한다.
- 긴 URL과 출처 문구는 이미지 안에 굽지 않는다. 호출자가 편집 가능한 캡션으로 추가할 수 있게 별도
  텍스트로 반환한다.

## 입력 정리

사용자 입력이나 호출한 skill의 브리프에서 아래를 확정한다. 안전하게 추론할 수 있으면 질문하지 않는다.

- 핵심 메시지 한 줄
- 시각자료 유형: 시스템 구조, 과정, 비교, 문제 흐름, 원본 Figure 단순화 중 하나
- 반드시 보여줄 컴퍼넌트·관계·순서·수치
- 이미지에 표시할 짧은 라벨과 언어
- 스타일: 라이트 샌드위치가 기본이며, 덱이 다크 스텝이면 다크 스텝
- 출처와 `adapted` 여부
- 연속 장면이면 유지할 기준 구도와 장면별 변경점

입력에 없는 컴퍼넌트·관계·장애·수치를 만들지 않는다. 예시가 필요하면 이미지와 응답에서 모두
`Scenario` 또는 `가정`임을 드러낸다.

## 구성

- 컴퍼넌트는 역할이 드러나는 단위 3~7개로 줄인다. 함수·클래스·파일은 사용자가 요구하지 않으면 제외한다.
- 왼쪽→오른쪽 또는 위→아래 중 관계가 가장 적게 교차하는 읽기 방향을 고른다.
- 흐름은 5단계 이하로 줄이고, 순서가 중요할 때만 ①②③ 마커를 쓴다.
- 정상 흐름은 기본 선, 문제·에러·병목만 빨강으로 표시한다. 노랑은 주인공 한 곳에만 쓴다.
- 여러 장이 같은 시스템을 설명하면 첫 이미지의 배치·크기·라벨 위치를 잠그고 마커·강조·설명만 바꾼다.
- 참고 이미지가 있으면 여백·색·선·타이포그래피 같은 재사용 가능한 스타일만 추출한다. 피사체·문구·고정
  구도는 복제하지 않는다.

## 생성

1. [references/visual-style.md](references/visual-style.md)를 읽고 완성형 영어 프롬프트를 만든다.
2. 이미지 생성 기능이 있으면 즉시 생성한다. 연속 장면은 직전 이미지를 참조할 수 있는 기능을 사용해
   구도를 유지한다.
3. 생성된 이미지를 확인해 라벨 오류, 겹침, 잘린 요소, 색 문법, 흐름 방향을 검수한다. 문제가 있으면
   한 번에 구체적으로 수정해 다시 생성한다.
4. 이미지 생성 기능이 없으면 완성형 영어 프롬프트만 코드 블록으로 반환한다.

## 출력

이미지를 생성했으면 아래만 반환한다.

- 생성 이미지
- 핵심 메시지 한 줄
- 출처 캡션 문구(있을 때만)
- `adapted` 또는 가정 표시(해당할 때만)

프롬프트 대체 출력에서는 이미지 대신 완성형 영어 프롬프트 하나를 반환한다. 중간 분석과 초안 프롬프트는
출력하지 않는다.

## 완료 전 확인

- 하나의 핵심 메시지만 보이는가?
- 관계·수치·장애 표현에 입력 근거가 있는가?
- 라벨이 짧고 정확하며 서로 겹치지 않는가?
- 라이트 샌드위치 또는 다크 스텝 색 문법을 정확히 따르는가?
- 연속 장면의 구도가 유지되는가?
- 원본과 단순화한 그림, 사실과 가정이 구분되는가?
- 덱·대본 같은 경계 밖 산출물을 만들지 않았는가?
```
