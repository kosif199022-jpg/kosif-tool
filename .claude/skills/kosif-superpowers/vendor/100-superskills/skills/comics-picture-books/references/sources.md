# مصادر «القصص المصوّرة وكتب الأطفال» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## reader-panel (1213-story-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/danjdewhurst/story-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2880-reader-panel
- الوصف: This skill should be used when the user asks for a "simulated beta read", "reader panel", "persona read", "first read before my beta readers", "how would a genre reader react", "would a reader keep going", "pre-beta read", "mock beta readers", or wants structured persona reads of a chapter range before human readers see it. NOT for real reader feedback (use feedback-triage), a paid sensitivity or 

```markdown
# Reader Panel

## Overview

Run structured persona reads of a chapter range and write each one as a
feedback file in the shape `feedback-triage` already reads, so the
existing triage flow takes over unchanged. The panel is a first read
before human readers see the draft: it finds the problems a reader would
trip on, so the human round spends its attention on what only people can
tell you.

Every panel read is simulated. It is written by the agent, marked
`source: simulated`, and never presented as feedback from a real reader.

## Prerequisites

A story project (`story.md` in the root) with the chapters in range
drafted. The `feedback-triage` skill must be available for the synthesis.

## When to Use

- Before the first beta round, to catch the obvious problems cheaply
- After a revision, to check a fix landed before sending it to people
- When the user has no readers yet and wants a structured first read
- NOT as a substitute for human readers. A simulated round cannot close
  a book as `ready` for submission or publication
- NOT for a sensitivity or authenticity read. The sensitivity persona
  only flags passages for a paid human reader (use `editorial-review`)

## Personas

Each persona has a reference file listing what it reads for, what it
never comments on, and how it rates severity. Load only the personas in
the panel.

| Persona | File id | Reads for | Reference |
|---------|---------|-----------|-----------|
| Target-genre reader | `genre-reader` | Does the book deliver the genre's promises? Pacing sags, missing beats, broken conventions | `references/genre-reader.md` |
| Line editor | `line-editor` | Sentence-level craft: POV slips and head-hopping, filter words, repetition, unclear antecedents, voice drift | `references/line-editor.md` |
| Sensitivity reader | `sensitivity-reader` | Portrayals that need a human sensitivity or authenticity reader. Flags, never clears | `references/sensitivity-reader.md` |
| Continuity-minded reader | `continuity-reader` | Facts, names, objects, timeline, and what each character can know at this point | `references/continuity-reader.md` |
| First-page reader | `first-page-reader` | Would they keep going? The opening page, each chapter's first lines, and the last line before they could put it down | `references/first-page-reader.md` |

## Workflow

### 1. Scope the panel

1. Ask the user for the chapter range (default: every drafted chapter)
   and which personas to run (default: all five). Take genre, form, POV,
   and tense from the `story context` output in step 2 (its Story
   essentials section), not from `story.md`, whose Synopsis may describe
   the ending. The genre reader needs the genre. Also read `language` from
   `story.md` frontmatter only (a missing field means `en`): it is no
```

## story-init (1213-story-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/danjdewhurst/story-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1213-story-skills/2885-story-init
- الوصف: This skill should be used when the user asks to "start a new story", "initialize a story project", "create a story", "new book", "set up a story", or wants to begin a new fiction writing project from scratch.

```markdown
# Story Initialization

## Overview

Initialize a new story project with a structured markdown folder layout. Creates the story bible, registries, scene tracking, continuity state, glossary, worldbuilding folders, plot structure, and chapter tracker - all as cross-referenced markdown files with YAML frontmatter.

## When to Use

- Starting a new story, book, or fiction project
- Setting up the folder structure for an existing story idea
- NOT for adding to an existing story project (use the domain-specific skills instead)
- NOT for a sequel, prequel, or companion to an existing book: use `series-continuity`, which links the projects and carries canon across
- NOT for finding the idea itself: when the user has only a vague notion ("something about lighthouses"), several competing ideas, or no premise yet, run the `premise-workshop` skill first, then return here with the chosen premise, form, and genre
- NOT for converting an existing manuscript or chapter drafts: run `story import <source> --title '{Title}'` instead, then build out the bible from the entity candidates it prints. Import does not accept `--form`, so afterwards set `form` and `target-words` in `story.md` by hand (see the form list and defaults below); without them `story validate` never checks length and `story progress` has no target

## Workflow

1. Ask for basic story information (if a `premise-workshop` session produced a premise, logline, genre, and form, reuse them rather than asking again):
   - Title
   - Form: `novel`, `novella`, `novelette`, `short-story`, `flash`, `serial`, `picture-book`, or `chapter-book`. Without `--form`, `story init` writes no `form` and no `target-words`, so if the user doesn't choose, pass `--form novel`
   - Genre and sub-genre
   - Brief synopsis (2-3 sentences)
   - Setting era/time period
   - Key themes (2-4)
   - POV style (first-person, third-person-limited, third-person-omniscient)
   - Tense (past, present, future, mixed)
   - Language the book is written in, as a BCP 47 tag: `en`, `en-GB`, `fr`, `es-MX`, `pt-BR`, `de`, `ja`, `zh-Hans`. Add a region only when it matters (spelling, punctuation, or market). If the user writes to you in a language other than English, confirm rather than assume. Default `en`

If the Story CLI is available, prefer using it to create the starter project, then inspect and refine the generated files as needed:

```shell
story init '{Title}' --form '{form}' --genre '{genre}' --sub-genre '{sub-genre}' --setting-era '{era}' --pov '{pov-style}' --tense '{tense}' --synopsis '{synopsis}' --theme '{theme-1}' --theme '{theme-2}'
```
```

## panel (3540-panel)

- الترخيص: **MIT**  ·  الأصل: https://github.com/x-mesh/xm/tree/cb4b788703cf164f1344fc3f3bc3e20c5e4ae2b8/x-panel
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3540-panel/14323-panel
- الوصف: Cross-vendor entry point + adversarial panel engine. `/xm:panel <verb>` routes multi-model work to the matching consumer in --cross-vendor mode (review→x-review, plan(brainstorm)/debate/council→x-op, solve→x-solver, eval→x-eval, consensus→x-build, fan-out→x-agent); `/xm:panel <target>` runs the panel engine itself (N model CLIs refute each other → consensus verdict); bare `/xm:panel` is an interac

```markdown
# x-panel — Cross-Model Adversarial Review Panel

## Overview

`x-panel` is the **multi-model entry point**. It has two jobs:

1. **Router** — `/xm:panel <verb>` (review/debate/council/solve/eval/consensus/fan-out) delegates to
   the matching consumer (x-review/x-op/x-solver/x-eval/x-build/x-agent) in `--cross-vendor` mode.
   The domain logic stays in the consumer; panel just picks the door. This is why "do it with
   several models" has ONE obvious entry point instead of remembering each plugin's flag.
2. **Engine** — `/xm:panel <target>` runs the native panel: N model CLIs review the
   same target in one round by default, and a verdict separates **consensus** (how many models
   agreed — confidence) from **diversity** (what only one model saw). The orchestrator is a
   tool-neutral CLI, so the "leader" is not a fixed model.

Different models have different blind spots — in dogfooding, codex missed a perf issue claude/agy
caught, and cursor missed a SQL injection. That diversity is the whole point of both jobs.

For reviews, these jobs are alternatives, not consecutive stages. `/xm:panel review` routes once to
x-review, which owns target selection, lenses, severity, lifecycle, verdict, and convergence; panel
only replaces x-review Phase 3 as its execution backend. Never run the native panel afterward as a
second review. A bare `xm panel <target>` is an ad-hoc consensus tool and does not create an
x-review lifecycle/verdict artifact.

## When to Use

- "여러 모델로 같이 리뷰", "다중모델로 토론/문제해결/평가" → route to the matching consumer (§1)
- "panel review" or a formal PR/code review with lifecycle artifacts → the `review` route
- An ad-hoc cross-model second opinion on supplied text/file, with no x-review lifecycle → native engine (§3)
- `/xm:panel` (picker), `/xm:panel <file>` (native engine), `/xm:panel review|debate|solve|eval …` (route)
- `/xm:panel review ...` delegates to `xm review run ... --cross-vendor`; use
  `/xm:panel review --engine native ...` only when the ad-hoc panel engine is explicitly required.

## Do NOT Use When

- A **single-model** review/op is wanted → call that consumer directly without `--cross-vendor`.
- The user wants to *recall* a prior panel result → x-recall (`xm recall show panel --last`).

## CLI Invocation

> **⚠ Call `xm panel <command>` directly. Claude Code's Bash tool starts a fresh shell on every invocation — shell functions (`xp()`) defined in one call do NOT persist to the next, causing `command not found`. Never define a helper across calls; always use the dispatcher.**
>
> **Fallback** (only when `xm` is not in PATH — rare; `${CLAUDE_PLUGIN_ROOT}` is NOT exported to Bash subprocesses):
> ```bash
> XPANEL_CLI=$(ls -d ~/.claude/plugins/cache/xm/{x-panel,panel,xm}/*/lib/x-panel-cli.mjs 2>/dev/null | sort -V | tail -1)
```

## internal-narrative (138-c-level-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/c-level-advisor
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/138-c-level-skills/433-internal-narrative
- الوصف: Build and maintain one coherent company story across all audiences — employees, investors, customers, candidates, and partners. Detects narrative contradictions and ensures the same truth is framed for each audience's needs. Use when preparing investor updates, all-hands presentations, board communications, recruiting narratives, crisis communications, or when user mentions company narrative, mess

```markdown
# Internal Narrative Builder

One company. Many audiences. Same truth — different lenses. Narrative inconsistency is trust erosion. This skill builds and maintains coherent communication across every stakeholder group.

## Keywords
narrative, company story, internal communication, investor update, all-hands, board communication, crisis communication, messaging, storytelling, narrative consistency, audience translation, founder narrative, employee communication, candidate narrative, partner communication

## Core Principle

**The same fact lands differently depending on who hears it and what they need.**

"We're shifting resources from Product A to Product B" means:
- To employees: "Is my job safe? Why are we abandoning what I built?"
- To investors: "Smart capital allocation — they're doubling down on the winner"
- To customers of Product A: "Are they abandoning us?"
- To candidates: "Exciting new focus — are they decisive?"

Same fact. Four different narratives needed. The skill is maintaining truth while serving each audience's actual question.

---

## Framework

### Step 1: Build the Core Narrative

One paragraph that every other communication derives from. This is the source of truth.

**Core narrative template:**
> [Company name] exists to [mission — present tense, specific]. We're building [what you're building] because [the problem you're solving]. Our approach is [your unique way of doing this]. We're at [honest description of current state] and heading toward [where you're going in concrete terms].

**Good core narrative (example):**
> Acme Health exists to reduce preventable falls in elderly care using smartphone-based mobility analysis. We're building an AI diagnostic tool for care teams because current fall risk assessments are subjective, infrequent, and often wrong. Our approach — using the phone's camera during a 10-second walking test — means no new hardware, no specialist required. We have 80 care facilities in DACH paying us €800K ARR, and we're heading to €3M ARR by demonstrating clinical value at scale before our Series B.

**Bad core narrative:**
> Acme Health is an innovative AI company revolutionizing elderly care through cutting-edge technology that empowers care providers and improves patient outcomes across the continuum of care.

The good version is usable. The bad version says nothing.

---

### Step 2: Audience Translation Matrix

Take the core narrative and translate it for each audience. Same truth, different frame.

| Fact | Employees need to hear | Investors need to hear | Customers need to hear | Candidates need to hear |
|------|----------------------|----------------------|----------------------|------------------------|
```

## game-story-world-character (2199-lvtd-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/LVTD-LLC/skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8090-game-story-world-character
- الوصف: Design or evaluate game story, world, characters, spaces, presence, aesthetics, and indirect control. Use when adding narrative, quests, levels, environments, character arcs, worldbuilding, environmental storytelling, or emotional context to gameplay.

```markdown
# Game Story World Character

Use this skill to make narrative and world design serve play instead of competing with it. The output should give the coding agent clear content structures, state needs, triggers, and constraints.

## Source Traceability

Primary source: *The Art of Game Design: A Book of Lenses, Third Edition* by Jesse Schell, especially chapters 17-23 on story, indirect control, worlds, characters, spaces, presence, and aesthetics. The workflow is transformed and paraphrased.

Supporting source: MDA for separating authored mechanics from player-experienced dynamics and aesthetics.

## Workflow

1. Define the role of story: premise, motivation, context, consequence, mystery, comedy, identity, or emotional payoff.
2. Align story beats with player action and system state.
3. Use indirect control through goals, affordances, layout, rewards, information, and character cues.
4. Specify world rules, character functions, spaces, mood, and aesthetic constraints.
5. Convert narrative intent into implementable triggers, content schema, and test cases.

## Required Output

- `Narrative Function`: why the game needs story or world detail.
- `Story-Gameplay Map`: beats tied to player actions and system state.
- `World Rules`: facts, boundaries, tone, and contradictions to avoid.
- `Character Specs`: role, desire, behavior hooks, dialogue constraints, and gameplay purpose.
- `Implementation Notes`: state flags, triggers, content data, level cues, and tests.

## Local References

Before producing a story/world spec, read:

- `references/core/guide.md`
- `workflows/narrative-systems-spec.md`
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
