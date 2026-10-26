# مصادر «بيانات متحركة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

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

## data-visualization (2690-build-web-data-visualization)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/build-web-data-visualization
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2690-build-web-data-visualization/10322-data-visualization
- الوصف: Route web data visualization work. Use when the user needs chart choice, visual critique, dashboards, maps or geospatial views, Gantt timelines, UML/software diagrams, scrollytelling, reports or exports, testing, accessibility, browser implementation, or concept-first visual design.

```markdown
# Web Data Visualization

## Overview

Use this skill as the implicit orchestrator for the plugin. Classify the task, choose the smallest useful specialist skill set, and route before doing deep chart, renderer, testing, accessibility, or export work. Specialist skills stay explicit-only unless this router hands off to them.

Default stance: the best visualization is the simplest truthful view that answers the user's question with the least decoding burden. Preserve evidence quality first: correct task abstraction, trustworthy data treatment, visible caveats, direct labels, accessible encodings, mobile viability, shareable state, and QA. Do not default to dashboards, 3D, animation, generated imagery, particles, or WebGL unless they carry analytical meaning.

Contextual imagery, atmospheric marks, and motion must be evidence-bearing. Do not use broad translucent brush strokes, wispy ribbons, bokeh/orbs, cinematic wallpaper, stock-photo haze, or decorative gradients as substitutes for data layers. When motion, flow, density, intensity, or spread appears, encode it with measured or clearly schematic contours, sampled fields, trajectories, particles with a defined unit or meaning, or annotated layers.

Mobile is a primary surface. Unless the user explicitly excludes it, treat large-screen and mobile portrait as sibling states. Add mobile landscape when a wide substrate, AR/camera/motion, two-handed interaction, or keyboard-heavy workflow needs it.

## Router Workflow

1. Classify the analytical job: comparison/ranking, time change, distribution/uncertainty, correlation, composition/flow, hierarchy/network, software/system structure, schedule, monitoring, geography, or export/reporting.
2. Classify the data shape: tabular, time series, multivariate, matrix, tree/graph, semantic diagram source, schedule/project plan, geospatial, stream, or generated/simulated story data.
3. Lock delivery constraints: static vs interactive, exploratory vs explanatory, browser/dashboard/report/PDF/slides, reuse level, scale, update rate, export, large-screen/mobile states, touch/keyboard/pinch, sensors, alerting, bandwidth, and persistence.
4. Define the reading path before the renderer: insight title, immediate evidence, on-demand detail, labels/keys/controls, caveats, mobile order, and what should stay visible when panels collapse.
5. Plan state explicitly: URL-backed filters, selections, ranges, zoom/map/camera, tabs, drill-down, saved-view ids, local/IndexedDB/remote persistence, invalid state, copy-link, refresh, and back-button behavior.
6. Choose whether a contextual substrate helps: map, field/court/track, floor plan, system schematic, terrain, object cutaway, or other domain surface. Use it only when it improves orientation or mark placement.
```

## client-rendered-dashboard-data-blob (3286-client-rendered-dashboard-data-blob)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/client-rendered-dashboard-data-blob
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3286-client-rendered-dashboard-data-blob/13800-client-rendered-dashboard-data-blob
- الوصف: Pull trustworthy numbers out of a dashboard that renders entirely client-side, by decoding the data blob it ships instead of scraping the DOM or driving a browser. Use when: (1) you want a dashboard's data as a feed for a report, a script, or another skill, (2) `curl` returns a big HTML page whose numbers are nowhere in the HTML, (3) you are about to reach for Playwright / headless Chrome just to 

```markdown
# Decode a client-rendered dashboard's data blob

## Problem

A dashboard shows exactly the numbers you want. You `curl` it and get a
megabyte of HTML with none of those numbers in it -- they are computed in the
browser. The obvious next step is a headless browser, which is slow, needs a
session, and gives you back only what is on screen.

Often you do not need any of that. Dashboards of this shape frequently ship
their **entire dataset** inline as a JavaScript literal and do all aggregation
client-side. One GET can therefore contain far more than the page displays --
every row, not just the visible page; the full history, not just the selected
window; every entity, not just the one you filtered to.

The second, subtler problem: once you have the raw data, the derived numbers
(ranks, percentages, scores) are **not** in it. You have to recompute them, and
the natural guess at what they mean is frequently wrong -- in a way that still
produces a believable number.

## Context / Trigger conditions

- `curl <dashboard-url>` returns HTTP 200 and a large HTML body, but
  `grep` for a value you can see on screen finds nothing.
- The page has one or two `<script>` blocks and no `application/json`.
- You are about to script a browser purely to read numbers.
- You want a dashboard as an upstream data source for a scheduled report.
- Your recomputed metric disagrees with the rendered one.
- You are about to quote "I'm ranked #N" from a URL that has a sort parameter
  in it.

## Solution

### 1. Find the blob

```bash
curl -sS -o page.html "<dashboard-url>"
grep -o '<script[^>]*>' page.html | sort | uniq -c        # how many script blocks
grep -n -o 'const [A-Za-z_]* *= *[[{]' page.html | head   # top-level data vars
```

Also worth trying, in rough order of how common they are:
`__NEXT_DATA__`, `window.__INITIAL_STATE__`, `self.__remixContext`,
`<script type="application/json">`, and a plain `const DATA = {...}`.

Extract and parse. Anchor the regex to the line so a trailing `;` or a second
statement on the same line does not corrupt the JSON:

```python
m = re.search(r"^const DATA = (\{.*\});?\s*$", html, re.M)
data = json.loads(m.group(1))
```

Note what that anchoring assumes: `.` does not cross newlines, so the blob must
stay on **one line**. That is load-bearing -- say so at the regex, and if the
page ever pretty-prints, widen with `re.S`.

### 2. Learn the schema from the page's own render loop

Big dashboards compress rows into **positional tuples of integers** with
parallel lookup arrays, because it is much smaller than repeated JSON keys. A
raw record looks meaningless:

```
[0, 4, 0, 0, 15, 49, 0]
```

Do not guess the fields. The page destructures them somewhere; find that and
read the names off it:

```bash
```

## end-of-period-dashboard (3565-xbert-end-of-period-dashboard)

- الترخيص: **MIT**  ·  الأصل: https://github.com/xbertintelligence/xbert-plugins/tree/7e6bcc16a3fd1da830522d1d30f97a76c52b67aa/plugins/xbert-end-of-period-dashboard
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3565-xbert-end-of-period-dashboard/14377-end-of-period-dashboard
- الوصف: Run the XBert End-of-Period Dashboard for a Connect tenant — fuse XBert work, ledger data quality and lodgement obligations into one per-client period-close readiness view. Use when the user asks about month-end, quarter-end, year-end, BAS readiness, payroll close, period-close status, who is ready to close, lodgement deadlines, or runs the /end-of-period-dashboard slash command. Also triggers on 

```markdown
**Source of truth — XBert MCP:** Every figure, client record, ledger transaction, payrun, and XBert notification referenced here must come from the connected XBert MCP server. Call XBert MCP tools to fetch the data — do not invent figures, estimate from context, or substitute from chat history. If the XBert MCP is not connected, ask the user to install and authenticate it before continuing.

# End-of-Period Dashboard

A cadence-aware per-client readiness view that fuses XBert work-in-flight, ledger data quality, and lodgement obligations. v1 is AU-first and runs one cadence at a time.

## Goal
Replace the practice manager's intuition with a deterministic per-client readiness band for the chosen close cycle, with named blockers and deadlines.

## Metrics
- **Readiness band** — Ready / Almost / Blocked / At Risk (computed, see thresholds)
- **DQ score** — per-client data-quality score
- **Outstanding work** — count and priority from the outstanding work board
- **Reconciliation status** — current reconciliation state per client
- **Lock date** — current lock date per client
- **Validation status** — BAS / VAT / Payroll reconciliation results
- **Deadline runway** — days until next lodgement for the cadence

## Default thresholds (practice-configurable)
| Band | DQ | Outstanding work | Validations | Lock date |
|---|---|---|---|---|
| Ready | >=90 | 0 high-priority | All pass | Within period |
| Almost | >=80 | <=3 high-priority | <=1 warning | Within period |
| Blocked | >=70 | >3 high-priority | >=1 fail | Behind period |
| At Risk | <70 OR deadline <=7 days AND not Ready | any | any | any |

**At Risk overrides** the other bands when a lodgement is due within 7 days and readiness is not yet Ready.

## Process / rules
1. **Cadence selection** — month / quarter / year. Pull only the obligations relevant to that cadence.
2. **Per-client computation** — band, blockers (named — e.g. "12 unreconciled bank transactions"), deadline runway.
3. **Lodgement calendar (AU v1)** — month-end (payroll STP, super deadlines), quarter (BAS), year (FBT, tax-time hand-off). Derive deadlines from the cadence and AU calendar context; do not assume an external lodgement feed.
4. **Deadline-first ranking** — At Risk first, then Blocked, then Almost. Ready clients are summarised but not detailed.
5. **First-page summary** — clients per band, lodgements due in 7 / 14 / 30 days, top three repeating blockers.
6. **Per-client detail** — only for non-Ready clients. Name blockers, name responsible workflow step, suggest next action (do not enact).

## Coverage caveats
- v1 is AU-only. If the practice has non-AU clients, exclude them from the obligation calendar and note this in the document.
```

## helm-chart-builder (172-helm-chart-builder)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/engineering/helm-chart-builder
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/172-helm-chart-builder/541-helm-chart-builder
- الوصف: Helm chart development agent skill and plugin for Claude Code, Codex, Gemini CLI, Cursor, OpenClaw — chart scaffolding, values design, template patterns, dependency management, security hardening, and chart testing. Use when: user wants to create or improve Helm charts, design values.yaml files, implement template helpers, audit chart security (RBAC, network policies, pod security), manage subchar

```markdown
# Helm Chart Builder

> Production-grade Helm charts. Sensible defaults. Secure by design. No cargo-culting.

Opinionated Helm workflow that turns ad-hoc Kubernetes manifests into maintainable, testable, reusable charts. Covers chart structure, values design, template patterns, dependency management, and security hardening.

Not a Helm tutorial — a set of concrete decisions about how to build charts that operators trust and developers don't fight.

---

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/helm:create` | Scaffold a production-ready Helm chart with best-practice structure |
| `/helm:review` | Analyze an existing chart for issues — missing labels, hardcoded values, template anti-patterns |
| `/helm:security` | Audit chart for security issues — RBAC, network policies, pod security, secrets handling |

---

## When This Skill Activates

Recognize these patterns from the user:

- "Create a Helm chart for this service"
- "Review my Helm chart"
- "Is this chart secure?"
- "Design a values.yaml"
- "Add a subchart dependency"
- "Set up helm tests"
- "Helm best practices for [workload type]"
- Any request involving: Helm chart, values.yaml, Chart.yaml, templates, helpers, _helpers.tpl, subcharts, helm lint, helm test

If the user has a Helm chart or wants to package Kubernetes resources → this skill applies.

---

## Workflow

### `/helm:create` — Chart Scaffolding

1. **Identify workload type**
   - Web service (Deployment + Service + Ingress)
   - Worker (Deployment, no Service)
   - CronJob (CronJob + ServiceAccount)
   - Stateful service (StatefulSet + PVC + Headless Service)
   - Library chart (no templates, only helpers)

2. **Scaffold chart structure**

   ```
   mychart/
   ├── Chart.yaml              # Chart metadata and dependencies
   ├── values.yaml             # Default configuration
   ├── values.schema.json      # Optional: JSON Schema for values validation
   ├── .helmignore             # Files to exclude from packaging
   ├── templates/
   │   ├── _helpers.tpl        # Named templates and helper functions
   │   ├── deployment.yaml     # Workload resource
   │   ├── service.yaml        # Service exposure
   │   ├── ingress.yaml        # Ingress (if applicable)
   │   ├── serviceaccount.yaml # ServiceAccount
   │   ├── hpa.yaml            # HorizontalPodAutoscaler
   │   ├── pdb.yaml            # PodDisruptionBudget
   │   ├── networkpolicy.yaml  # NetworkPolicy
   │   ├── configmap.yaml      # ConfigMap (if needed)
   │   ├── secret.yaml         # Secret (if needed)
   │   ├── NOTES.txt           # Post-install usage instructions
   │   └── tests/
   │       └── test-connection.yaml
   └── charts/                 # Subcharts (dependencies)
   ```

3. **Apply Chart.yaml best practices**

   ```
   METADATA
```

## dashboard (3534-dashboard)

- الترخيص: **MIT**  ·  الأصل: https://github.com/x-mesh/xm/tree/cb4b788703cf164f1344fc3f3bc3e20c5e4ae2b8/x-dashboard
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3534-dashboard/14317-dashboard
- الوصف: Web dashboard for .xm project state — start, stop, open in browser

```markdown
<Purpose>
Start, stop, or check the xm-dashboard web server that visualizes .xm/ project state.
</Purpose>

<Use_When>
- User says "dashboard", "open dashboard", "start dashboard", "show dashboard"
- User says "stop dashboard", "close dashboard", "kill dashboard"
- User says "dashboard status"
</Use_When>

<Do_Not_Use_When>
- User wants to query .xm data directly (use x-build status instead)
</Do_Not_Use_When>

# x-dashboard

## Model Routing

This entire skill is **haiku** (Agent tool). All commands (start/stop/status/open) are pure script execution — bun process management, curl health checks, browser open. Zero reasoning required.

| Command | Model | Reason |
|---------|-------|--------|
| `start` | **haiku** | nohup + sleep + curl |
| `stop` | **haiku** | bun --stop |
| `status` | **haiku** | curl + JSON display |
| `open` | **haiku** | macOS open command |

```
Agent tool: { model: "haiku", description: "x-dashboard <cmd>", prompt: "Run: <bash from command section>" } <!-- managed-model: writer -->
```

**Guardrail**: never haiku if the user asks "why is the dashboard showing X" or "interpret these metrics" — interpretation is sonnet-level reasoning.

## Arguments

User provided: $ARGUMENTS

## Routing

Parse `$ARGUMENTS`:

- `stop` / `close` / `kill` → [Command: stop]
- `restart` / `relaunch` / `reload` → [Command: restart]
- `status` → [Command: status]
- `open` → [Command: open]
- Empty or `start` or any other text → [Command: start]

## Command: start

1. Check if already running:
```bash
cat ~/.xm/run/xdashboard-server.pid 2>/dev/null && echo "PID_EXISTS" || echo "NO_PID"
```

2. If PID exists, check if alive:
```bash
kill -0 $(cat ~/.xm/run/xdashboard-server.pid 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['pid'])" 2>/dev/null) 2>/dev/null && echo "ALIVE" || echo "DEAD"
```

3. If alive → just open browser and report URL:
```
Dashboard already running at http://127.0.0.1:{port}
```

4. If not running → start server in background:
```bash
nohup bun x-dashboard/lib/x-dashboard-server.mjs --session > /dev/null 2>&1 &
sleep 2
curl -s http://127.0.0.1:19841/health
```

5. Report to user:
```
Dashboard started at http://127.0.0.1:19841
Session mode — auto-stops after 60 minutes of inactivity.
To stop: /xm:dashboard stop
```

## Command: stop

```bash
bun x-dashboard/lib/x-dashboard-server.mjs --stop
```

Report result to user.

## Command: restart

Stop the running server, then start a fresh one. Use this after the dashboard's
server code or served `public/` bundle changed — a long-lived server keeps
serving whatever it was launched with, so a restart is the cure for a stale
served bundle ("fixed but still shows the old UI").

```bash
bun x-dashboard/lib/x-dashboard-server.mjs --stop
```
