# مصادر «لوحات المعلومات والتصور البياني» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## kpi-dashboard-design (3455-business-analytics)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/business-analytics
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3455-business-analytics/14162-kpi-dashboard-design
- الوصف: Design effective KPI dashboards with metrics selection, visualization best practices, and real-time monitoring patterns. Use this skill when building an executive SaaS metrics dashboard tracking MRR, churn, and LTV/CAC ratios; designing an operations center with live service health and request throughput; creating a cohort retention analysis view for a product team; or debugging a dashboard where 

```markdown
# KPI Dashboard Design

Comprehensive patterns for designing effective Key Performance Indicator (KPI) dashboards that drive business decisions.

## When to Use This Skill

- Designing executive dashboards
- Selecting meaningful KPIs
- Building real-time monitoring displays
- Creating department-specific metrics views
- Improving existing dashboard layouts
- Establishing metric governance

## Core Concepts

### 1. KPI Framework

| Level           | Focus            | Update Frequency  | Audience   |
| --------------- | ---------------- | ----------------- | ---------- |
| **Strategic**   | Long-term goals  | Monthly/Quarterly | Executives |
| **Tactical**    | Department goals | Weekly/Monthly    | Managers   |
| **Operational** | Day-to-day       | Real-time/Daily   | Teams      |

### 2. SMART KPIs

```
Specific: Clear definition
Measurable: Quantifiable
Achievable: Realistic targets
Relevant: Aligned to goals
Time-bound: Defined period
```

### 3. Dashboard Hierarchy

```
├── Executive Summary (1 page)
│   ├── 4-6 headline KPIs
│   ├── Trend indicators
│   └── Key alerts
├── Department Views
│   ├── Sales Dashboard
│   ├── Marketing Dashboard
│   ├── Operations Dashboard
│   └── Finance Dashboard
└── Detailed Drilldowns
    ├── Individual metrics
    └── Root cause analysis
```

## Detailed worked examples and patterns

Detailed sections (starting with `## Common KPIs by Department`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

## Best Practices

### Do's

- **Limit to 5-7 KPIs** - Focus on what matters
- **Show context** - Comparisons, trends, targets
- **Use consistent colors** - Red=bad, green=good
- **Enable drilldown** - From summary to detail
- **Update appropriately** - Match metric frequency

### Don'ts

- **Don't show vanity metrics** - Focus on actionable data
- **Don't overcrowd** - White space aids comprehension
- **Don't use 3D charts** - They distort perception
- **Don't hide methodology** - Document calculations
- **Don't ignore mobile** - Ensure responsive design

## Troubleshooting

### MRR shown on dashboard contradicts finance's number

The most common cause is inconsistent treatment of annual plans. Finance may prorate to a daily rate while the dashboard normalizes to monthly. Align on a single formula and document it directly on the dashboard card:

```sql
-- Explicit formula shown in tooltip / data dictionary
-- Annual plans: divide total contract value by 12
-- Quarterly plans: divide by 3
-- Monthly plans: use as-is
CASE subscription_interval
    WHEN 'monthly'   THEN amount
    WHEN 'quarterly' THEN amount / 3.0
    WHEN 'yearly'    THEN amount / 12.0
END AS normalized_mrr
```

### Dashboard shows green but product team reports users complaining
```

## d3-data-visualization (2690-build-web-data-visualization)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/build-web-data-visualization
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2690-build-web-data-visualization/10320-d3-data-visualization
- الوصف: Build custom data visualizations with D3. Use when the user needs SVG or DOM-based charts, rich annotation, domain-native contextual backgrounds, data joins, custom scales or interactions, scroll-driven SVG scene states, or precise control over browser visualization behavior.

```markdown
# D3 Data Visualization

## Overview

Use this skill for custom browser visualizations where SVG or DOM semantics matter and a declarative grammar no longer fits cleanly. D3 is strongest when the chart needs bespoke scales, marks, layouts, transitions, zooming, brushing, annotations, or vector export.

Default assumption: use D3 for scales, layouts, geometry, labels, annotation layers, and behavior. Do not turn D3 into the entire application architecture if a framework already owns the surrounding UI.

## Choose D3 When

- the chart needs custom marks or nonstandard layouts
- SVG quality matters for export, print, or accessibility
- annotation and labeling are part of the design, not an afterthought
- the visualization needs custom vector background geometry such as a field, court, track, floor plan, schematic, or other meaningful contextual surface
- an editorial story needs data-bound generated cutouts, illustrated substrates, scrollytelling/parallax states, or animated annotation reveals in SVG
- the mark count is moderate enough for DOM or SVG
- the interaction model needs zoom, brush, drag, or coordinated views
- a UML-like, dependency, architecture, state, or flow diagram needs bespoke SVG annotation or product-specific composition after `../uml-and-software-architecture-visualization/SKILL.md` has defined the diagram semantics
- a declarative grammar would become harder to read than the resulting D3 code

## Avoid D3-First DOM Rendering When

- mark counts are so large that DOM throughput becomes the bottleneck
- animation is continuous and frame budgets are tight
- the task would be faster to solve with Canvas2D or WebGL

## Working Pattern

1. Build a clean data model first.
2. Separate:
   - parsing and normalization
   - scale construction
   - derived geometry
   - rendering
   - interaction state
3. Prefer stable keys in joins.
4. Use D3 for math and behavior, not for hiding weak state management.
5. Assess how many D3 instances may coexist on the page so DOM, layout, and event costs are evaluated at dashboard scale.
6. If using a contextual surface, keep source units and render scales explicit, draw the background as a separate layer, and adapt mark placement or layout forces to the domain geometry.
7. For art-directed stories, keep generated image, substrate, data-mark, label, and annotation layers separate so each can be reviewed and exported.
8. Keep annotations and interaction overlays explicit.
9. For SVG output, apply `./references/svg-polish-and-crispness.md` before calling the chart finished. Explicitly set font sizes, tick padding, gridline strokes, data stroke widths, icon sizes, label alignment, and zoom-stable stroke behavior.
```

## gantt-chart-visualization (2690-build-web-data-visualization)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/build-web-data-visualization
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2690-build-web-data-visualization/10323-gantt-chart-visualization
- الوصف: Design, critique, route, and implement Gantt charts and schedule visualizations. Use when the user mentions Gantt charts, project schedules, roadmaps with task spans, milestones, dependencies, predecessors, critical path, baselines, WBS, resource plans, capacity timelines, MS Project, Primavera P6, Jira Advanced Roadmaps, GitHub Projects, Smartsheet, monday.com, Asana, ClickUp, Azure DevOps iterat

```markdown
# Gantt Chart Visualization

## Overview

Use this skill when work is organized around time spans, milestones, dependencies, resources, or schedule risk. A Gantt chart is a product surface as much as a chart: it usually combines a task grid, a calendar axis, bars, milestones, dependency links, editing rules, and integration with a project-management source of truth.

Default assumption: recommend a Gantt chart only when the schedule itself is the evidence. If the user mainly needs flow state, task ownership, ranking, issue status, or calendar booking, consider Kanban, tables, milestone timelines, dependency graphs, resource timelines, or uncertainty views first.

Gantt charts are wide by nature. Use `../../references/foundations/mobile-first-responsive-visualization.md` so mobile portrait gets a usable summary or focused slice, and mobile landscape is considered when horizontal schedule inspection matters.

## Core Workflow

1. Classify the scheduling question:
   - planned schedule, actual lifecycle timeline, roadmap, resource plan, capacity view, baseline variance, critical-path review, or stakeholder snapshot
   - whether the user needs read-only explanation, exploratory analysis, or editable project planning
2. Inspect the source before designing:
   - true schedule engine, task tracker, roadmap view, resource calendar, static export, or visual artifact
   - native fields, custom fields, date-only versus datetime values, timezone policy, hierarchy, dependency semantics, calendars, and permissions
   - provenance for every mapped field and any inferred value
3. Normalize into a Gantt model:
   - tasks, hierarchy or WBS, start, end, duration, progress, status, assignee or resource, milestones, dependencies, baselines, calendars, constraints, estimates, actuals, source IDs, and source confidence
4. Decide whether Gantt is the right surface:
   - use Gantt when time spans and dependency or resource reasoning drive the decision
   - use a milestone timeline for executive summaries with few dates
   - use Kanban for workflow state and throughput
   - use a table when lookup and exact fields dominate
   - use a dependency graph when structure matters more than dates
   - use a calendar or resource timeline for booking without project dependencies
   - use uncertainty views when date risk is probabilistic or estimates are still unstable
5. Design the default view:
   - frozen task grid plus calendar axis
   - today marker, visible scale, weekends or non-working time when meaningful
   - clear bars, milestones, dependency links, baselines, progress, and critical-path or risk styling
   - row grouping, hierarchy, and direct labels that work without hover
   - mobile portrait summary or focused default that does not shrink every row into illegibility
```

## kpi-dashboard-design (2385-staffing-operations)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/staffing-operations
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2385-staffing-operations/9232-kpi-dashboard-design
- الوصف: Lay out a staffing KPI dashboard so the most decision-relevant number is read first, every tile pairs with its partner metric, and a red number explains itself via drill-down. Reach for this when turning a scorecard spec into a dashboard layout (not the build — the design).

```markdown
# Skill: KPI dashboard design

A scorecard defines the numbers; the dashboard decides what an operator sees in the first three seconds. This skill is about layout and information hierarchy, not instrumentation.

## Step 1 — Lead with the decision metric
The top-left tile is the KPI that answers the dashboard's reason for existing (fill rate, margin, or FTE-on-assignment, depending on the audience). Everything else supports it.

## Step 2 — Pair tiles physically
Fill rate sits beside time-to-fill; margin beside its bill/pay/burden breakdown; revenue-per-recruiter beside reqs-per-recruiter. Adjacency enforces the constitution's pairing rule visually (§3 #2, #3, #4) — a viewer can't read one without seeing its partner.

## Step 3 — Every tile shows value + delta + baseline
No bare numbers. Each tile: current value, the delta vs. baseline, and what the baseline *is* (prior period / SLA / target). A trend sparkline (8–12 periods) gives the seasonality context that a point-in-time number hides.

## Step 4 — Make red explain itself
A red tile must surface its top 1–2 drivers on hover/drill — the components from the scorecard's drill-down field. A red number with no visible driver generates a meeting; a red number with its driver generates an action.

## Step 5 — Segment selector, not segment blend
A filter for healthcare-travel / locum / allied / per-diem / education-school-based. Never show a cross-segment average as a headline — the seasonalities and benchmarks differ enough to make the blend meaningless.

## Step 6 — Surface the triggered action
The recommended action for the current band, in plain language, on or beside the tile. If the operator has to remember the playbook, the dashboard isn't doing its job.

## Step 7 — Mark soft numbers visibly
Benchmarks shown as comparison lines are labeled `[ESTIMATE]` if advisory-sourced. The client's own baseline is the solid line; the benchmark is dashed.

## Output
Feeds [`../../templates/staffing-dashboard-spec.md`](../../templates/staffing-dashboard-spec.md). Demo data: [`../../bi-report/data.json`](../../bi-report/data.json). For the actual build/instrumentation, route to `ravenclaude-core/data-engineer`; for the metric definitions, [`staffing-scorecard-build`](../staffing-scorecard-build/SKILL.md).
```

## dashboard-layout-review (2390-tableau)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/tableau
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2390-tableau/9251-dashboard-layout-review
- الوصف: Checklist-driven review for Tableau dashboard layout, chart-type selection, formatting, and accessibility — covering the question-first design principle, attention hierarchy, filter placement, colour and font conventions, and the five layout anti-patterns that confuse users. Owned by tableau-viz-engineer.

```markdown
# Dashboard Layout Review

## When to invoke

- Before publishing a new dashboard to Tableau Server/Cloud.
- A stakeholder says the dashboard is "confusing" or "hard to use."
- Standardising dashboard design across a team.
- Reviewing a dashboard built by someone else for quality.

## Gate 1 — Question-first audit

Every sheet in the dashboard should answer a specific business question. For each sheet ask:

1. What is the question this chart answers? (Write it in one sentence.)
2. Does the chart type match the question type?
3. Can a user read the answer in < 5 seconds without explanation?

| Question type | Correct chart types | Common wrong choice |
|---|---|---|
| Trend over time | Line, area | Bar (for time-ordered data > 6 periods) |
| Comparison across categories | Bar (horizontal for long labels), dot plot | Pie / donut (> 5 categories) |
| Part-to-whole | Bar (stacked, 100%) for ≤ 5 categories; treemap for hierarchical | Pie chart with > 6 slices |
| Distribution | Box-whisker, histogram, violin | Average line only (hides spread) |
| Correlation | Scatter plot, heatmap | Dual-axis line (implies causality) |
| Geographic | Filled map, symbol map | Table of values with no spatial context |

Remove any sheet that cannot be assigned a question — it's decoration, not information.

## Gate 2 — Attention hierarchy

Users read dashboards in a Z or F pattern. Place the most important KPI or insight in the top-left. Review the hierarchy:

1. **Primary insight** — one number or chart that answers "so what?" Largest, most prominent.
2. **Supporting context** — 2–3 charts that explain the primary insight's drivers.
3. **Detail** — filters, secondary views, drill-down targets. Smaller, lower, or on a second sheet.

Anti-pattern: treating all charts as equal size and importance — the dashboard looks like a grid of tiles with no focal point.

## Gate 3 — Filter placement and performance review

| Filter type | Use when | Avoid when |
|---|---|---|
| Quick filter (Relevant Values) | Low-cardinality (≤ 50 values); user must see all options | High-cardinality (names, IDs) — use typed search |
| Context filter (Make Context Filter) | Drives FIXED LODs; needs to constrain other filter lists | Every filter — only promote when the dependency requires it |
| Action filter (filter action on click) | Guided drill-through; interactive exploration | Replace-all-values filter across every sheet — too aggressive |
| Parameter | Single-select, user-controlled inputs (date range, metric toggle) | Multi-select — use a set or quick filter |

Flag any quick filter set to "Show All Values" on a field with > 1 000 distinct values — it fires an expensive query on every dashboard load.

## Gate 4 — Formatting checklist
```

## analytics (1493-growthbook)

- الترخيص: **MIT**  ·  الأصل: https://github.com/growthbook/skills/tree/eb7960d4fe5034bd8d8f100320192d1691a173ac
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1493-growthbook/3702-analytics
- الوصف: Chart GrowthBook product data, build Analytics dashboards, manage the metric catalog, or query the warehouse directly — run Product Analytics explorations, save charts together on a dashboard, search metrics and fact tables, create fact metrics and their fact tables, or fall back to ad-hoc SQL. Use for "show me signups by country", "chart daily active users", "how many orders last week", "build me

```markdown
# analytics

Domain router for GrowthBook Product Analytics, Analytics dashboards, and the metric catalog. The workflows live in `references/`. Read this router, pick one, then read that file and follow it.

Analytics uses the **v1 API** — `/api/v1/product-analytics/search`, `/columns`, and `/column-values` for discovery, the metric, fact-table, data-source, and funnel `/api/v1/product-analytics/*-exploration` endpoints for charts, `/api/v1/product-analytics/explorations/:id` for polling, `/dashboards` for saved pages of charts, and `/fact-metrics` and `/fact-tables` for the catalog. The API also exposes SQL explorations, but this skill does not construct or execute arbitrary SQL exploration payloads.

All API calls go through the bundled helper. Under the Claude Code plugin install, it lives at `${CLAUDE_PLUGIN_ROOT}/scripts/gb-call` (the plugin root). Under `npx skills install`, it lives at `scripts/gb-call` relative to this skill's directory. Resolve that path once and substitute it whenever a reference example says `gb-call`; do not assume `gb-call` is on `PATH`. It reads `GB_API_KEY` from the environment first, then falls back to `~/.config/growthbook/.env` (written by **gb-setup**); environment variables take precedence.

When a workflow needs to construct a GrowthBook UI link from a root-relative path, a shell-capable runtime should call `gb-call app-origin` once per conversation, retain the returned trusted origin across workflow and domain handoffs, and prepend it to each path. If the origin is already in context, reuse it; do not call the command once per link. Embedded or MCP adapters that already know their trusted app origin may resolve paths directly. Never derive an app origin from `GB_API_URL`; if `app-origin` refuses because self-hosted configuration is incomplete, route to **gb-setup**. API-returned `explorationUrl` values are already complete and must be used unchanged.

## Pick a workflow

| Read this                         | When the user wants to                                                                                                      |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `references/metric-search.md`     | Browse, find, or audit metrics and fact tables — inventory, a specific definition, or "what can I chart" triage (read-only) |
| `references/metric-create.md`     | Create a fact metric, creating its underlying fact table first when necessary (writes configuration)                       |
| `references/analytics-explore.md` | Actually run a chart and report the numbers plus a deep link                                                                |
```
