# مصادر «مهندس النماذج المالية في إكسل» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## chronograph-budget-vs-actuals-variance (1102-chronograph-gp)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/chronograph-pe/chronograph-gp-claude-plugin/tree/35cb3d12cf4e24823c0efca4abe6f13c2fd0e5f5
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1102-chronograph-gp/2495-chronograph-budget-vs-actuals-variance
- الوصف: Compare portfolio company operating actuals against budget/plan, compute variances,

```markdown
# Budget vs. Actuals Variance

**Requirements:** A connected Chronograph MCP server as a GP client.

## Overview
Compare portfolio company operating results (revenue, EBITDA, and other tracked KPIs) against budget or plan for the same periods, compute the variance in amount and percent, flag companies tracking off-plan beyond a threshold, trend the variance over time, and roll up to the fund.

## Scenarios — how budget and actuals are distinguished
Company operating metrics are retrieved with the **`company-metrics`** tool, which exposes a **Scenario** field that separates budget/plan figures from actuals. **Scenario labels are client-specific** — a client may name them differently (e.g. "Budget", "Plan", "Forecast", "Actual") and may carry more than one budget scenario (original vs. revised, or multiple cases). Before computing any variance:

1. Query `company-metrics` to see which Scenario values exist for the company.
2. **Confirm with the user** which Scenario represents actuals and which represents the budget/plan to compare against (and which to ignore) — do not assume from the labels.
3. Apply the confirmed scenarios consistently across every company and period in the analysis.

## Workflow
1. Resolve scope: a single company, a set, or the whole fund; and the periods to compare.
2. Establish the Scenario mapping (above) — confirm the actuals and budget scenarios with the user.
3. Pull the tracked metrics (revenue, gross profit, EBITDA, and any KPIs in scope) from `company-metrics` for both the actuals and budget scenarios, same periods.
4. Compute variance per metric: actual − budget, and percent variance; label favorable/unfavorable.
5. Flag companies off-plan beyond a threshold (default ±10%, configurable); trend variance across periods to show whether gaps are widening or closing.
6. Roll up to the fund and present per-company variance with off-plan flags and a coverage note.

## Chronograph MCP usage
Use the `company-metrics` tool for operating metrics; prefer platform metric types over display labels (same discipline as the one-pager), and select the Scenario per the confirmed mapping. Make the metric-discovery call before querying. Never default currency to USD; display `—` where a value is unavailable.

## Output standards

- **Disclaimer footer (required).** Every rendered deliverable (HTML page, Excel sheet, PDF, or document) must show a footer on each page/sheet, and any chat-only output must close with the same line: *For informational purposes only — not investment advice. Source: Chronograph · as of {as-of date}.*
- Per-company variance table: metric, period, actual, budget, Δ amount, Δ %, favorable/unfavorable.
- State which Scenario values were used for actuals vs. budget.
```

## build-cash-forecast-and-liquidity-plan (2399-treasury-management)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/treasury-management
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2399-treasury-management/9289-build-cash-forecast-and-liquidity-plan
- الوصف: Build a cash position + rolling forecast and a liquidity plan by traversing the treasury decision tree (cash position → forecast method (direct/receipts-and-disbursements vs indirect) → 13-week build & drivers → variance loop → minimum-cash/buffer sizing → committed vs uncommitted facility mix), then return the daily cash position, the 13-week forecast, the buffer target (stress-tested), the facil

```markdown
# Skill: build-cash-forecast-and-liquidity-plan

> **Invoked by:** `cash-and-risk-operations-specialist` (primary, for the position + forecast build) and `treasury-strategy-lead` (for the buffer/facility policy the forecast grounds).
>
> **When to invoke:** "build our 13-week cash forecast"; "what's today's cash position?"; "how much minimum cash / liquidity buffer should we hold?"; "direct or indirect forecasting?"; "committed vs uncommitted facilities / how much revolver headroom?"; any "how much cash and where" question.
>
> **Output:** the daily cash position + the rolling 13-week (direct) forecast + a variance loop + the stress-tested minimum-cash/buffer target + the committed vs uncommitted facility mix & revolver headroom + the 1-2 conditions that resize it.

## Procedure

1. **Position cash first — from where the money actually is.** Build today's **cash position** per currency and entity: opening bank balances + confirmed receipts − confirmed disbursements → **closing / available liquidity** (net of holds, minimums, and un-cleared items). This is the anchor; a forecast that doesn't start from the real position is untethered.
2. **Pick the forecast method by horizon.** **Direct (receipts-and-disbursements)** — actual expected cash in/out, driver-based — for the **operating horizon (the 13-week and shorter)**; it's what treasury runs day-to-day. **Indirect** (net income + working-capital changes + non-cash add-backs) — for the **longer, statement-linked** view where you forecast from the P&L/balance sheet. Don't use indirect for the 13-week (too coarse) or direct for the annual (too granular to sustain).
3. **Build the 13-week from drivers, not a straight line.** Lay out 13 weekly columns; populate **receipts** (collections driven by DSO / the AR aging, plus known one-offs) and **disbursements** (AP payment-run timing driven by DPO, payroll, tax, debt service, capex, dividends). Each line is a *driver*, not a plug — so a variance is diagnosable.
4. **Attach a variance loop — every week.** Forecast → actuals → **variance by line** → re-forecast. Tune the drivers from the miss (collections slower than DSO assumed? a payment run slipped a week?). A 13-week without a back-test is a wish, not a forecast.
5. **Size the minimum-cash / buffer against a stress, not the average.** Traverse the buffer-sizing branch in [`../../knowledge/treasury-management-decision-tree.md`](../../knowledge/treasury-management-decision-tree.md): take the forecast's **trough** (the worst intra-period low), then stress it — a receipts shock (a big customer slips), a facility pulled, a covenant tightening, a seasonality low — and set the buffer so the trough-under-stress stays above zero (and above any covenant/minimum-operating-cash floor).
```

## experiment-sensitivity-optimization (2199-lvtd-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/LVTD-LLC/skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8069-experiment-sensitivity-optimization
- الوصف: Improve experiment sensitivity and reduce traffic or duration requirements. Use when choosing sensitive metrics, working with minimum detectable effect, reducing variants, applying capping metrics, CUPED, variance reduction, or deciding how to get trustworthy A/B test signal with fewer users.

```markdown
# Experiment Sensitivity Optimization

Use this skill to redesign an experiment so it can detect meaningful effects
with fewer users, less time, or clearer metrics. It focuses on minimum
detectable effect, metric sensitivity, capping, variant reduction, CUPED, and
variance reduction.

## Source Traceability

Primary source: *Next-Level A/B Testing* by Leemay Nassery. Guidance is
transformed and paraphrased from Chapter 3 on experiment design, sensitive
metrics, minimum detectable effect, capping, reducing variants, and CUPED; and
Chapter 6 on stratified random sampling and covariate adjustments.

Related skills:

- `ab-test-design-brief` for baseline experiment specs.
- `trustworthy-experiment-insights` for judging whether a result is believable.
- `experimentation-throughput-strategy` for capacity and test scheduling.

## Reference Routing

| Need | Read |
|------|------|
| Sensitivity concepts | `references/core/knowledge.md` |
| Metric, variance, and sample-size rules | `references/core/rules.md` |
| Optimization scenarios | `references/core/examples.md` |
| Step-by-step sensitivity review | `workflows/optimize-experiment-sensitivity.md` |

## Workflow

1. State the decision and the smallest practically meaningful effect.
2. Check whether the current primary metric is close enough to the feature's
   mechanism.
3. Reduce unnecessary variants and separate learning tests from launch tests.
4. Consider metric capping, CUPED, stratification, or other variance reduction.
5. Record data prerequisites, risks, and interpretation limits.
6. Update the experiment brief with the revised measurement plan.

## Output Format

```markdown
# Experiment Sensitivity Plan

## Decision
[What the experiment must decide.]

## Current Constraint
[Traffic | Duration | Noisy metric | Too many variants | Weak proxy | Other]

## Recommended Changes
| Change | Why It Helps | Requirement | Risk |
|--------|--------------|-------------|------|

## Metric Plan
- Primary metric:
- More sensitive alternative:
- Guardrails:
- Minimum detectable effect:

## Variance Reduction
- Technique:
- Data needed:
- Validation:

## Interpretation Notes
- What this design can conclude:
- What it cannot conclude:
```

## Quality Bar

- Do not optimize sensitivity by switching to a metric that no longer answers
  the product decision.
- Do not add CUPED, stratification, or capping unless the data requirements and
  interpretation risks are named.
- Do not keep extra variants when they are not needed for the decision.
- Do not treat a smaller detectable effect as useful unless it is practically
  meaningful.
```

## thirteen-week-cash-forecast (2294-finance)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/finance
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2294-finance/8797-thirteen-week-cash-forecast
- الوصف: Build and operate a 13-week direct-method cash forecast — receipts by source, disbursements by category, week-by-week roll, variance-to-prior-forecast cadence, covenant headroom view, and the trigger thresholds for management action. Reach for this skill when a business is cash-tight, in workout, lender-monitored, or post-fundraise discipline-building. Used by `treasury-analyst` (primary) and `fpa

```markdown
# Skill: thirteen-week-cash-forecast

**Purpose:** Build the standard short-horizon cash visibility tool — the 13-week direct cash forecast. Different mechanic than the indirect-method cash flow in a 3-statement model; this is the tactical instrument lenders and management ask for when the cash conversation matters. Used by `treasury-analyst` (primary).

## When to use

- Liquidity-tight situations (any time runway < 12 months without committed financing)
- Covenant-monitored lending relationships
- Workout / restructuring engagements
- Pre-IPO / pre-strategic-event discipline-building
- Acquisition integration (during the first 2-4 quarters)
- After any near-miss on cash (one bad month is a wake-up; two is a process gap)
- Recurring discipline for any business with material seasonality, customer concentration, or working-capital intensity

## Why 13 weeks

Long enough to see a full quarter and a regulator/lender filing window. Short enough that every line is forecastable from real receivables / payables / payroll dates — not extrapolated from a P&L.

13 weeks ≈ one quarter. Most lender covenants test quarterly; this matches. The standard horizon is rolling (a week drops off the front, a week gets added to the back, every Monday).

## Direct method vs. indirect

This forecast is **direct method** — every line is an actual cash event (a receipt or a disbursement) with a known date. Not derived from accruals.

| Direct method | Indirect method |
|---|---|
| Cash receipts (AR collections, deposits, transfers) | Net income |
| Cash disbursements (AP runs, payroll, taxes, debt service) | ± non-cash items |
| Net cash flow | ± Δ working capital |
| Beginning cash + Net = Ending cash | = Cash from operations |

The 13W is direct method. The 3-statement model uses indirect. They reconcile but aren't the same artifact.

## Structure

A 13W cash forecast has four sections, always in this order:

1. **Beginning cash** (sum of all operating bank accounts, excluding restricted)
2. **Receipts** (grouped by source)
3. **Disbursements** (grouped by category)
4. **Net change + Ending cash** (the answer)

Optionally a 5th section: **Covenant / availability roll** (for lender-monitored businesses).

### Receipts

Group receipts the way the business collects:

| Group | Examples |
|---|---|
| Customer AR collections | By customer for top concentrations; "other" for the long tail |
| Recurring contractual | Subscription billings, milestone payments, fee accruals |
| Non-operating | Refunds, settlements, asset sales, tax refunds |
| Financing | Draws on revolver, new debt, equity issuance |
```

## variance-analysis (321-finance)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/anthropics/knowledge-work-plugins/tree/8444efcd48f7012f09797778a36a33e73d0861f4/finance
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/321-finance/977-variance-analysis
- الوصف: Decompose financial variances into drivers with narrative explanations and waterfall analysis. Use when analyzing budget vs. actual, period-over-period changes, revenue or expense variances, or preparing variance commentary for leadership.

```markdown
# Variance Analysis

**Important**: This skill assists with variance analysis workflows but does not provide financial advice. All analyses should be reviewed by qualified financial professionals before use in reporting.

Techniques for decomposing variances, materiality thresholds, narrative generation, waterfall chart methodology, and budget vs actual vs forecast comparisons.

## Variance Decomposition Techniques

### Price / Volume Decomposition

The most fundamental variance decomposition. Used for revenue, cost of goods, and any metric that can be expressed as Price x Volume.

**Formula:**
```
Total Variance = Actual - Budget (or Prior)

Volume Effect  = (Actual Volume - Budget Volume) x Budget Price
Price Effect   = (Actual Price - Budget Price) x Actual Volume
Mix Effect     = Residual (interaction term), or allocated proportionally

Verification:  Volume Effect + Price Effect = Total Variance
               (when mix is embedded in the price/volume terms)
```

**Three-way decomposition (separating mix):**
```
Volume Effect = (Actual Volume - Budget Volume) x Budget Price x Budget Mix
Price Effect  = (Actual Price - Budget Price) x Budget Volume x Actual Mix
Mix Effect    = Budget Price x Budget Volume x (Actual Mix - Budget Mix)
```

**Example — Revenue variance:**
- Budget: 10,000 units at $50 = $500,000
- Actual: 11,000 units at $48 = $528,000
- Total variance: +$28,000 favorable
  - Volume effect: +1,000 units x $50 = +$50,000 (favorable — sold more units)
  - Price effect: -$2 x 11,000 units = -$22,000 (unfavorable — lower ASP)
  - Net: +$28,000

### Rate / Mix Decomposition

Used when analyzing blended rates across segments with different unit economics.

**Formula:**
```
Rate Effect = Sum of (Actual Volume_i x (Actual Rate_i - Budget Rate_i))
Mix Effect  = Sum of (Budget Rate_i x (Actual Volume_i - Expected Volume_i at Budget Mix))
```

**Example — Gross margin variance:**
- Product A: 60% margin, Product B: 40% margin
- Budget mix: 50% A, 50% B → Blended margin 50%
- Actual mix: 40% A, 60% B → Blended margin 48%
- Mix effect explains 2pp of margin compression

### Headcount / Compensation Decomposition

Used for analyzing payroll and people-cost variances.

```
Total Comp Variance = Actual Compensation - Budget Compensation

Decompose into:
1. Headcount variance    = (Actual HC - Budget HC) x Budget Avg Comp
2. Rate variance         = (Actual Avg Comp - Budget Avg Comp) x Budget HC
3. Mix variance          = Difference due to level/department mix shift
4. Timing variance       = Hiring earlier/later than planned (partial-period effect)
5. Attrition impact      = Savings from unplanned departures (partially offset by backfill costs)
```

### Spend Category Decomposition
```

## forecast-and-alert (2295-finops-cloud-cost)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/finops-cloud-cost
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2295-finops-cloud-cost/8800-forecast-and-alert
- الوصف: Forecast spend and set anomaly thresholds so cost is managed, not a monthly surprise. Reach for this on a budget/anomaly question.

```markdown
# Skill: Forecast and alert

An anomaly alert catches a runaway resource in hours, not on the invoice (§3 #7).

## Step 1 — Build the forecast
Trend the allocated spend forward; budget against the forecast (§3 #7).

## Step 2 — Set the threshold
Alert on deviation from forecast, sized to catch a runaway early (§3 #7).

## Step 3 — Route the alert
To the owning team via showback, so the alert reaches the spender (§3 #6).

## Step 4 — Tune false positives
A threshold too tight is noise; calibrate to real anomalies.

## Output
A spend forecast with an anomaly threshold routed to the owning team.
```
