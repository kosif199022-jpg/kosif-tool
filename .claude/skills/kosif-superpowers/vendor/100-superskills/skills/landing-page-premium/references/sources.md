# مصادر «صفحة الهبوط الفاخرة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## landing-page-generator (198-product-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/product-team
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/198-product-skills/634-landing-page-generator
- الوصف: Generates high-converting landing pages as complete Next.js/React (TSX) components with Tailwind CSS. Creates hero sections, feature grids, pricing tables, FAQ accordions, testimonial blocks, and CTA sections using proven copy frameworks (PAS, AIDA, BAB). Outputs SEO meta tags, structured data, and performance-optimised code targeting Core Web Vitals (LCP < 1s, CLS < 0.1). Use when the user asks t

```markdown
# Landing Page Generator

Generate high-converting landing pages from a product description. Output complete Next.js/React components with multiple section variants, proven copy frameworks, SEO optimization, and performance-first patterns. Not lorem ipsum — actual copy that converts.

**Target:** LCP < 1s · CLS < 0.1 · FID < 100ms
**Output:** TSX components + Tailwind styles + SEO meta + copy variants

---

## Core Capabilities

- 5 hero section variants (centered, split, gradient, video-bg, minimal)
- Feature sections (grid, alternating, cards with icons)
- Pricing tables (2–4 tiers with feature lists and toggle)
- FAQ accordion with schema markup
- Testimonials (grid, carousel, single-quote)
- CTA sections (banner, full-page, inline)
- Footer (simple, mega, minimal)
- 4 design styles with Tailwind class sets

---

## Generation Workflow

Follow these steps in order for every landing page request:

1. **Gather inputs** — collect product name, tagline, audience, pain point, key benefit, pricing tiers, design style, and copy framework using the trigger format below. Ask only for missing fields.
2. **Analyze brand voice** (recommended) — if the user has existing brand content (website copy, blog posts, marketing materials), run it through `marketing-skill/skills/content-production/scripts/brand_voice_analyzer.py` to get a voice profile (formality, tone, perspective). Use the profile to inform design style and copy framework selection:
   - formal + professional → **enterprise** style, **AIDA** framework
   - casual + friendly → **bold-startup** style, **BAB** framework
   - professional + authoritative → **dark-saas** style, **PAS** framework
   - casual + conversational → **clean-minimal** style, **BAB** framework
3. **Select design style** — map the user's choice (or infer from brand voice analysis) to one of the four Tailwind class sets in the Design Style Reference.
4. **Apply copy framework** — write all headline and body copy using the chosen framework (PAS / AIDA / BAB) before generating components. Match the voice profile's formality and tone throughout.
5. **Generate sections in order** — Hero → Features → Pricing → FAQ → Testimonials → CTA → Footer. Skip sections not relevant to the product.
6. **Validate against SEO checklist** — run through every item in the SEO Checklist before outputting final code. Fix any gaps inline.
7. **Output final components** — deliver complete, copy-paste-ready TSX files with all Tailwind classes, SEO meta, and structured data included.

---

## Triggering This Skill

```
Product: [name]
Tagline: [one sentence value prop]
Target audience: [who they are]
Key pain point: [what problem you solve]
Key benefit: [primary outcome]
Pricing tiers: [free/pro/enterprise or describe]
```

## landing-page-audit (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4059-landing-page-audit
- الوصف: Audit a landing page across six conversion dimensions — above-fold clarity, trust signals, form friction, message match against the upstream ad or email, page speed, and mobile experience — each scored 1-10, rolled into an overall score benchmarked against industry averages, with the top 5 fixes ranked by expected conversion impact. Assessment and recommendations only; it does not edit the page. T

```markdown
# /digital-marketing-pro:landing-page-audit

## Purpose

Evaluate a landing page across six key conversion dimensions and deliver a scored assessment with specific, actionable recommendations to improve conversion rate.

## Input Required

The user must provide (or will be prompted for):

- **Landing page URL**: The page to audit
- **Traffic source**: Where visitors come from (paid search, social ads, email, organic)
- **Target action**: Desired conversion (form submit, purchase, signup, download, call)
- **Ad copy or email**: The upstream message driving traffic (for message match analysis)
- **Current conversion rate**: If known, for benchmarking

## Process

1. **Load brand context**: Read `~/.claude-marketing/brands/_active-brand.json` for the active slug, then load `~/.claude-marketing/brands/{slug}/profile.json`. Apply brand voice, compliance rules for target markets (`skills/context-engine/compliance-rules.md`), and industry context. **Also check for guidelines** at `~/.claude-marketing/brands/{slug}/guidelines/_manifest.json` — if present, load restrictions and relevant category files. Check for custom templates at `~/.claude-marketing/brands/{slug}/templates/`. Check for agency SOPs at `~/.claude-marketing/sops/`. If no brand exists, ask: "Set up a brand first (/digital-marketing-pro:brand-setup)?" — or proceed with defaults.
2. **Above-fold clarity** (score 1-10): Headline clarity, value proposition, visual hierarchy, CTA visibility within first viewport
3. **Trust signals** (score 1-10): Social proof, testimonials, logos, security badges, guarantees, reviews
4. **Form friction** (score 1-10): Number of fields, field labels, error handling, progressive disclosure, mobile form UX
5. **Message match** (score 1-10): Alignment between traffic source (ad/email) and landing page headline, imagery, offer
6. **Page speed** (score 1-10): Load time, Core Web Vitals, render-blocking resources, image optimization
7. **Mobile experience** (score 1-10): Responsive design, tap targets, scroll depth, mobile-specific CTAs
8. Calculate overall score and benchmark against industry averages
9. Prioritize recommendations by expected conversion impact

## Output

A structured landing page audit containing:

- Overall conversion score (1-10) with industry benchmark comparison
- Dimension-by-dimension scoring with evidence and screenshots/notes
- Top 5 priority fixes ranked by expected impact
- Detailed recommendations per dimension with implementation guidance
- Message match analysis with specific misalignment callouts
- Mobile-specific issues and fixes
- Quick wins vs. major redesign items

## Agents Used

- **analytics-analyst** — Performance scoring, conversion benchmarking, data-driven recommendations
```

## visual-html-renderer (3215-reviewable-html-workbench)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/u-ichi/reviewable-html-workbench
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3215-reviewable-html-workbench/13601-visual-html-renderer
- الوصف: HTMLを最終成果物として生成・検証・プレビューしたい時に使う共通レンダラー。Use this shared renderer when the user wants content turned into a final, validated, previewable HTML artifact. 現行rendererの表現能力を前提にagentが文書モデルを直接設計し、表・リスト・コード・注記・図・生成画像を選んだHTML bundleとセッション限定のプレビューURLを提示する。Triggers: html出力して, HTMLにして, HTMLで出して, この内容をHTMLで出して, HTMLでプレビューして, HTMLレンダラー, HTML出力を共通化, 図示つきHTML, visual HTML renderer, render this as HTML, turn this i

```markdown
# visual-html-renderer

## 役割

HTML出力系skillの共通レンダラーとして、個別HTML生成ロジックを置き換える。

重い処理は `scripts/html_review_workbench/` のPython実装に委譲し、このskillは入力確認、呼び出し順、ガード、検証を担当する。

## Role

Use this skill as the shared renderer for HTML-output workflows. It replaces one-off HTML generation logic with a fixed flow: understand the requested content, design the document model, run the shared CLI, validate the bundle, and return a preview URL. Heavy implementation stays in `scripts/html_review_workbench/`; this skill owns input handling, workflow order, gates, and verification.

Plan Mode 中の計画確認プレビューには、このskillを使わない。その場合は `plan-preview` を使い、一時HTML previewとして扱う。`visual-html-renderer` は通常の最終HTML成果物、レポート、レビュー可能な文書のbundle生成だけを担当する。

Do not use this skill for Plan Mode proposal previews. Route those requests to `plan-preview`; this skill is only for final HTML artifacts, reports, and reviewable document bundles.

## Strict procedure profile

- Strictness: strict-procedure。HTML表現設計、文書モデルread-back、render、validate、preview URL提示までがこのskillの成果。
- Hard gates: 外部サービス送信、画像生成、外部アップロード、shared state変更は該当する承認ゲートに従う。
- Forcing function: rendererブロック対応表、render前自己レビュー、`check-model` CLI、Completion receipt。
- Completion receipt: HTML表現設計、生成物、検証、preview、未実施層を最終応答に必ず含める。

## 言語方針 / Language behavior

Follow the language of the latest user request for progress updates, final responses, preview handoff text, and user-facing summaries. 日本語の依頼には日本語で、英語の依頼には英語で返す。入力本文や引用内容は、ユーザーが翻訳を求めない限り勝手に翻訳しない。HTML内の見出しや本文は、元資料の言語、ユーザーの指定、レビュー対象読者に合わせる。

## 基本手順

0. Plan Mode 中の計画確認プレビュー、`<proposed_plan>` の視覚確認、計画URLの追加が目的なら、このskillではなく `plan-preview` を使う。
1. 文書モデルとレンダリングオプションを確認する。
2. 文書モデルが未指定の場合は、直前の成果物またはユーザー指定内容を読み、HTML表現設計フェーズで構成を決める。
3. 現行rendererのブロック型に合わせて、agentが `document-model.json` を直接作る。
4. 一時的な入力退避が必要な場合だけ `build-model` で source-capture draft を作ってよい。ただし draft は最終モデルではないため、そのまま `render` へ渡さない。
5. render前に `document-model.json` を読み返し、未再構成テキストの流し込みやrenderer非対応型の使用がないことを確認する。
6. `image.generation_status=requested` のブロックがある場合は、`imagegen` skillで画像を生成し、`attach-image` CLIで文書モデルへ添付する。
7. `check-model` CLIで最終render前の文書モデル品質を検査する。
8. `render` CLIでHTML bundleを生成する。
9. `validate` CLIでHTML、asset、comment schema、図・画像の非空を検証する。
10. ユーザー向け最終HTMLでは既定で `preview` CLIを `--mode auto` で起動し、返却JSONの `url` と `stop_command` を最終応答に必ず書く。
11. preview 起動直後に、Monitor ツールで `watch-comments` を開始する。これによりブラウザからのコメントを自動検知できるようになる。Monitor 起動コマンド: `python3 -m scripts.html_review_workbench.cli watch-comments --root <output-dir>`。自前の polling スクリプトではなく、この CLI を使うこと。イベント受信後の処理は `reviewable-design-doc` skill の「コメント自動回答と解決待ちゲート」セクションに従う。

## Basic Workflow

0. If the request is a Plan Mode proposal preview, `<proposed_plan>` visual check, or plan preview URL request, use `plan-preview` instead of this skill.
```

## oss-contribution-shape-by-conversion-rate (3337-oss-contribution-shape-by-conversion-rat)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/oss-contribution-shape-by-conversion-rate
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3337-oss-contribution-shape-by-conversion-rat/13851-oss-contribution-shape-by-conversion-rat
- الوصف: Decide whether to contribute to an open-source repo as a pull request or as an issue by measuring the repo's conversion rate first: what share of merged PRs come from the maintainers, how many outside PRs sit open, how far main is ahead of the last release, and what reviews an outside PR actually gets (bots only, or a human). Use when: (1) you are about to write a patch for a fast-moving repo (tho

```markdown
# Contribution shape by conversion rate

> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/oss-contribution-shape-by-conversion-rate/SKILL.md`).

## Problem

The internet says "send a patch". On a repo where three people merge 95% of
everything and land thousands of commits between releases, an outside patch is
a liability with a diff attached: somebody has to hold it against a `main`
that moved thousands of times, and nobody has the time. The same repo will
take a well-argued issue and reimplement it as a maintainer PR within weeks.
Sending the wrong shape costs you the work and costs the maintainer triage.

Measured on one such repo over two months: the two features asked for in
issues shipped together in one maintainer PR; the patch sent for one of those
features sat 32 days with seven green bot checks, none of the required
workflows ever run, and no human review, then was superseded. The required
workflows had been added to the repo after the PR's last push; nothing ever
asked them to run. A bug with nine competing fix PRs, four by the maintainer, got
its fix attached to a duplicate issue filed four months after the original.

## Context / Trigger Conditions

- Before writing a patch for a repo you do not maintain.
- A PR of yours shows `BLOCKED` with green bot checks and no runs of the
  required checks; or `mergeStateStatus` stays `UNKNOWN`/`UNSTABLE` with
  nobody assigned. Check the dates before blaming the fork: a workflow added
  to the base branch after your last push never fires on your PR, and a
  ruleset that requires its context then waits forever. A rebase and push
  (or close and reopen) fires it.
- The review log on a maintainer PR reads "automated pre-merge suggestion
  triage", CodeRabbit, Cursor, greptile ("too many files"), Bugbot ("spend
  limit reached"): the repo reviews by robot.
- A maintainer PR "Fixes #<duplicate>" and never mentions the original.

## Solution

### 1. Measure four numbers (five minutes, read-only)

Use the search API's `total_count` for counts, with the date window pinned
at **both** ends. Two traps, both verified:

- `gh pr list --search ...` rides on the GitHub Search API, which refuses
  anything past result 1000 (`422 Only the first 1000 search results are
  available` on page 11). `--limit 3000` silently returns 1000. A count built
  from that listing was off by 5x.
- `total_count` is not capped, but an open-ended window (`merged:>=DATE`) is a
  live number: 1,889 one day, 2,112 six days later, same query. Pin the upper
  bound and record the date next to the number.

```bash
R=owner/repo; WIN=2026-07-10..2026-09-09
q() { gh api -X GET search/issues -f q="repo:$R $1" --jq .total_count; }
```

## tailwind-best-practices (1483-tailwind)

- الترخيص: **MIT**  ·  الأصل: https://github.com/gopherguides/gopher-ai/tree/953b31bdf242c5d05ae91d7ca4cf997c0adbe051/plugins/tailwind
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1483-tailwind/3674-tailwind-best-practices
- الوصف: Tailwind CSS v4 guidance: utility-first patterns, @theme directive for color/spacing/font config, @source for content paths, dark mode, responsive design, oklch colors, custom variants, v4 vs v3 differences. Use when user writes Tailwind utility classes, configures @theme or @source in CSS, asks about v4 syntax, or styles components.

```markdown
# Tailwind CSS v4 Best Practices

Use the bundled references for Tailwind CSS v4 guidance. Consult the linked official documentation when current upstream behavior matters.

## Reference Files

Read the relevant file for detailed patterns, code examples, and documentation URLs:

### `docs-urls.md` — Official Documentation URLs
URL tables organized by category (Getting Started, Core Concepts, Layout, Spacing, Sizing, Typography, Backgrounds & Borders, Effects, Transforms & Animation, Interactivity). Use with WebFetch when current upstream behavior needs verification.

### `v4-syntax.md` — Tailwind CSS v4 Core Syntax
**CRITICAL**: v4 changed significantly from v3. Covers `@import "tailwindcss"`, `@theme` directive for CSS-based configuration (colors, fonts, spacing), `@source` for detection, class-based `@custom-variant dark` plus `.dark` selectors, `@layer components` for extraction, and `@plugin` for plugins.

### `best-practices.md` — Best Practices
Class ordering convention (layout → spacing → sizing → typography → colors → effects → interactive), responsive design (mobile-first, breakpoint reference), component extraction rule (3+ times), theme variables over hardcoded values, accessibility (focus-visible, sr-only, contrast).

### `anti-patterns.md` — v4 Anti-Patterns
v3 → v4 migration table (tailwind.config.js → @theme, @tailwind → @import, etc.), common mistakes (inline styles, px values, duplicate/conflicting utilities).

### `quick-reference.md` — Quick Reference
Response guidelines for helping with Tailwind, example response flow, spacing scale table, common utility patterns (centered content, card, responsive grid, truncation, gradient, fixed header).

---

*For the latest documentation, always refer to https://tailwindcss.com/docs*
```

## markdown-html-orchestrator (191-markdown-html-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/markdown-html
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/191-markdown-html-skills/565-markdown-html-orchestrator
- الوصف: Use when a user wants to convert any markdown file in their Claude project into a single-file, lightly-interactive HTML — long-form documents (specs, plans, RFCs, reports, explainers), code reviews with diffs and severity-tagged annotations, or slide decks. Triggers on "convert this markdown to HTML", "make this an HTML file", "turn this into an interactive document", "render this report as HTML",

```markdown
# Markdown → HTML — Domain Orchestrator

Thariq Shihipar's argument (Claude Code HTML output essay, Medium 2026): **markdown collapses past 100 lines for agent-generated artifacts.** Long specs, code reviews, and architecture explainers lose density, hierarchy, and lightweight interaction the moment they exceed a screen of text. HTML restores all three — single-file, browser-native, shareable.

This orchestrator forks context, classifies the input markdown deterministically, routes to the right converter sub-skill, and returns a digest with the output path. Heavy intake (full markdown bodies, diffs, slide decks) stays in the forked context.

**Domain status (complete):** all five skills are live — orchestrator + `design-system` (onboarding + shared brand tokens) + the three converter sub-skills (`md-document`, `md-review`, `md-slides`). Always route conversions to the shipped converter's scripts; never hand-render HTML inline.

## When to invoke

| Symptom | Sub-skill |
|---|---|
| "Convert this RFC / spec / report / explainer to HTML" — long-form doc | `md-document` |
| "Turn this PR writeup / code review into HTML" — markdown with diff blocks | `md-review` |
| "Make a slide deck from this markdown" — `---` boundaries or H1 cadence | `md-slides` |

## Pre-flight gates (hard refusals)

1. **Below the 100-line threshold.** Markdown wins below 100 lines (Shihipar). The classifier prints `below_min_lines: true` and `route_explainer.py` refuses. Tell the user to keep their input as markdown.
2. **Design-system not onboarded.** If `~/.config/markdown-html/design-system.json` doesn't exist (or its `setup_completed_at` is null), refuse. Point the user at `python3 markdown-html/skills/design-system/scripts/onboard.py` (or `--defaults` for a zero-touch run).
3. **Unwritable save location.** `output_path_resolver.py` refuses if the configured `default_output_dir` (or `--out` override) isn't writable.

## Routing logic (deterministic)

Two-signal threshold pattern lifted from `research-ops/skills/research-ops-skills/SKILL.md`. Filename hint = 2 points; each content signal = 1 point. Silent-route allowed when winner ≥ 3 AND (runner-up = 0 OR winner ≥ 2× runner-up). Below threshold → one clarifying question with a recommended answer.

### Signal table

| Signal class | Filename hints | Content signals | Sub-skill |
|---|---|---|---|
| DOCUMENT | `report.md`, `*-doc.md`, `spec.md`, `rfc-*.md`, `*-analysis.md`, `*-explainer.md` | `## Table of Contents` (2), `^# `, `^## `, markdown table rows, `> [!NOTE]/[!TIP]/[!IMPORTANT]` callouts | `md-document` |
| REVIEW | `review.md`, `*-pr-*.md`, `*.diff.md`, `code-review*.md` | ` ```diff ` (2), `^[-+]{3} ` (2), `^@@` (2), `> [!BLOCKER]/[!MAJOR]/[!MINOR]/[!NIT]` (2), `LGTM`/`nit:`/`blocker:` | `md-review` |
```
