# مصادر «النماذج المالية في إكسل» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## excel-dcf-modeler (1633-excel-analyst-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/business-tools/excel-analyst-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1633-excel-analyst-pro/4604-excel-dcf-modeler
- الوصف: Build discounted cash flow (DCF) valuation models in Excel. Use when

```markdown
# Excel DCF Modeler

## Overview

Creates professional DCF valuation models following investment banking standards with WACC calculations and sensitivity analysis.

## Prerequisites

- Excel or compatible spreadsheet software
- Historical financial data for target company
- Industry comparables for WACC estimation

## Instructions

1. Create assumptions sheet with revenue growth, margins, WACC, and terminal growth rate
2. Build free cash flow projections (5-year forecast)
3. Calculate terminal value using Gordon Growth Model
4. Discount cash flows and terminal value to present value
5. Sum to get enterprise value, subtract net debt for equity value
6. Add sensitivity tables for key assumptions

## Output

- Complete 4-sheet DCF model with assumptions, projections, valuation, and sensitivity
- Enterprise value and equity value per share
- Sensitivity analysis on WACC and terminal growth rate

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| #DIV/0! in terminal value | WACC equals terminal growth | Terminal growth must be less than WACC |
| Negative FCF | High CapEx or WC needs | Review assumptions, may need different model |
| Unrealistic EV | Extreme growth assumptions | Benchmark against industry comparables |

## Examples

**Example: Value a SaaS Company**
Request: "Create a DCF model for a $50M ARR SaaS company growing 30%"
Result: 4-sheet model with 5-year projections, 12% WACC, 3% terminal growth, sensitivity tables

**Example: M&A Valuation**
Request: "DCF analysis for acquisition target"
Result: Model with synergy adjustments, scenario analysis, and per-share valuation

## Resources

- [Damodaran Online DCF Resources](https://pages.stern.nyu.edu/~adamodar/)
- [WSO DCF Modeling Guide](https://www.wallstreetoasis.com/)
- `${CLAUDE_SKILL_DIR}/references/dcf-formulas.md` for Excel formula templates
```

## excel-lbo-modeler (1633-excel-analyst-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/business-tools/excel-analyst-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1633-excel-analyst-pro/4605-excel-lbo-modeler
- الوصف: Build leveraged buyout (LBO) models in Excel with debt schedules and

```markdown
# Excel LBO Modeler

## Overview

Creates leveraged buyout models with debt structuring, amortization schedules, and sponsor returns analysis for private equity transactions.

## Prerequisites

- Excel or compatible spreadsheet software
- Target company financial data
- Debt term sheet parameters
- Entry/exit multiple assumptions

## Instructions

1. Set up transaction structure (purchase price, debt/equity split)
2. Build debt schedules for each tranche (senior, mezzanine, etc.)
3. Create operating projections with debt service
4. Calculate cash flow available for debt paydown
5. Model exit scenarios and calculate IRR/MOIC

## Output

- Complete LBO model with sources & uses, debt schedules, and returns
- IRR and MOIC at various exit multiples and years
- Sensitivity tables for entry/exit multiple and leverage

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Negative cash flow | Debt service exceeds EBITDA | Reduce leverage or restructure debt terms |
| IRR #NUM! | No valid solution | Check exit value exceeds equity contribution |
| Circular reference | Cash sweep tied to interest | Enable iterative calculation |

## Examples

**Example: Mid-Market LBO**
Request: "Build an LBO model for a $100M EBITDA company at 8x entry"
Result: 60% senior / 40% equity structure, 5-year model, IRR analysis at 7x-10x exits

**Example: Add-On Acquisition**
Request: "Model a bolt-on acquisition with synergies"
Result: Integrated model with synergy phase-in and accretion analysis

## Resources

- [Macabacus LBO Modeling](https://macabacus.com/)
- [WSO PE Interview Prep](https://www.wallstreetoasis.com/)
- `${CLAUDE_SKILL_DIR}/references/lbo-formulas.md` for debt schedule templates
```

## dcf-valuation (2294-finance)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/finance
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2294-finance/8782-dcf-valuation
- الوصف: Run a defensible discounted-cash-flow valuation — explicit projection period, terminal value (Gordon vs exit-multiple), WACC build, sensitivities, scenario weighting, and the cross-check against trading / precedent multiples. Reach for this skill on any valuation work (pre-investment, 409A, fairness opinion, M&A) where a number has to survive board / counterparty scrutiny. Used by `valuation-analy

```markdown
# Skill: dcf-valuation

**Purpose:** Build a DCF that holds up under cross-examination. The mechanics are simple; the defensibility lives in the assumption set and the cross-checks. Used by `valuation-analyst` (primary).

## When to use

- Pre-investment / pre-acquisition valuation
- 409A refresh
- Fairness-opinion support
- Strategic value-creation modeling (board / LP discussion)
- M&A diligence (buy-side or sell-side)
- Impairment testing (goodwill, indefinite-lived intangibles)

## The pieces

A DCF has four parts. Each requires defensible inputs:

1. **Explicit projection period** — typically 5-10 years, ending when the business is at steady-state
2. **Terminal value** — Gordon growth OR exit multiple (do both, compare, explain)
3. **Discount rate (WACC)** — build from comparable-set betas, current risk-free, ERP, size premium, company-specific premium
4. **Enterprise → equity bridge** — net debt, minority interest, preferred, options dilution

## Explicit projection period

**Length:** long enough that the terminal year reflects steady-state. Most growth-stage businesses need 7-10 years. Mature businesses can use 5. Avoid 3-year DCFs — terminal value dominates and the model is a single-line bet on the multiple.

**Steady-state criteria** (terminal year should satisfy):

- Revenue growth has converged to a sustainable long-run rate (typically 2-3% real; can be higher for genuinely durable platforms)
- Margins have stabilized (not still climbing the curve)
- Reinvestment rate (capex + ΔNWC / revenue) is consistent with the long-run growth rate
- Tax rate is at expected long-run effective rate

If the year-N → year-N+1 trajectory still shows margin expansion or growth deceleration, extend the projection. Forcing terminal value on a non-steady-state year overstates value.

**Use the [`../driver-based-forecasting/SKILL.md`](../driver-based-forecasting/SKILL.md) skill to build the projection.** A DCF on a top-down "grow 15% a year" forecast is just a calculator.

## Terminal value: do both methods

### Gordon growth (perpetuity)

```
TV = FCF_(N+1) / (WACC - g)
```

Where:
- `FCF_(N+1)` = next year's free cash flow (NOT the terminal year — one year forward)
- `g` = long-run nominal growth rate (typically 2-3%, capped at long-run GDP nominal)

**Smell test:** terminal value > 75% of enterprise value usually means either projection too short OR g too high.

### Exit multiple

```
TV = Terminal-year EBITDA × Exit multiple
```

Where the exit multiple comes from the comparable-set trading multiples at the implied terminal-year size / growth / margin profile — NOT today's multiple applied forward.

**Reconciliation:** implied perpetuity-growth from the exit multiple should be defensible. Solve:

```
g_implied = WACC - (FCF_(N+1) / TV_(exit multiple))
```
```

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

## cash-flow-snapshot (335-small-business)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/anthropics/knowledge-work-plugins/tree/8444efcd48f7012f09797778a36a33e73d0861f4/small-business
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/335-small-business/1141-cash-flow-snapshot
- الوصف: Reads AR/AP, historical cash timing, and known fixed costs from the ledger (MYOB, NetSuite, QuickBooks, Xero, or Zoho Books) or from PayPal, Square, or Stripe — or a CSV upload — and produces a 30/60/90-day cash flow forecast with percentage-variance confidence bands and named risk flags. Delivers a chat summary and a downloadable XLSX. Use when the user asks "forecast my cash flow," "will I make 

```markdown
# Cash Flow Snapshot

Produces a 30/60/90-day cash flow forecast with percentage-variance confidence
bands and named risk flags. Delivers a two-part output: a concise chat summary
and a downloadable XLSX workbook.

**Quick start**

> "Will I make payroll next month?"

Claude pulls the current bank balance, AR/AP, and fixed costs from connected
sources, calculates expected inflows and outflows across 30, 60, and 90-day
windows, applies confidence bands from each customer's payment variance, and
flags specific risks by name.

---

## Workflow

### Step 1 — Identify available data sources

Check which connectors are live. Pull from every one that is, in one batch:

1. The ledger — MYOB, NetSuite, QuickBooks, Xero, or Zoho Books, whichever is connected — for AR aging, AP, fixed costs, and the cash balance. Ledgers are peers (`../../shared/connector-neutrality.md`); if two are connected, ask which is the source of record and take totals from that one only
2. PayPal — transaction history and settlement timing
3. Square — sales and payout history
4. Stripe — charge and payout history
5. Shopify — orders (`list-orders`) as the inflow, plus payout timing. Shopify on its own is enough to run: for a commerce business it is often the largest inflow. The payout read may fail because the connector's scopes exclude Shopify Payments — then ask the owner for their payout schedule and model from that; never infer a lag (`reference/v2_sources.md`)
6. CSV upload — when no connector is connected

If no connector is live and no file is attached, ask the user to either connect
a source or upload a CSV (income/expense tabular data, any reasonable format).
Note which sources were used in the output — this affects confidence band width.

**Always establish the starting cash balance** — "will I make payroll" is a
question about the balance, not the net. Pull it in Step 2, or ask: "What's in
the business account right now, and as of what date?" **Never assume one.** If
nobody knows, head the output "no opening balance — net change only" and drop
cash-on-hand from the risk flags.

### Step 2 — Pull the data

**From the ledger:**
- Balance sheet: bank and cash balances with the as-of date — the opening balance
  (MYOB holds none; see `reference/v2_sources.md`)
- AR aging report: customer name, invoice amount, invoice date, due date, days outstanding
- AP: vendor name, amount due, due date
- Recurring fixed costs: rent, payroll, subscriptions (look for recurring transactions)

**From Gusto, when connected:**
- The next payroll run's date and expected amount, and the regular pay-schedule
  cadence — the real numbers for the biggest fixed cost, instead of inferring
  payroll from recurring transactions. When Gusto and the ledger disagree on
```

## financial-analyst (189-finance-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/finance
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/189-finance-skills/560-financial-analyst
- الوصف: Performs financial ratio analysis, DCF valuation, budget variance analysis, and rolling forecast construction for strategic decision-making. Use when analyzing financial statements, building valuation models, assessing budget variances, or constructing financial projections and forecasts. Also applicable when users mention financial modeling, cash flow analysis, company valuation, financial projec

```markdown
# Financial Analyst Skill

## Overview

Production-ready financial analysis toolkit providing ratio analysis, DCF valuation, budget variance analysis, and rolling forecast construction. Designed for financial modeling, forecasting & budgeting, management reporting, business performance analysis, and investment analysis.

## 5-Phase Workflow

### Phase 1: Scoping
- Define analysis objectives and stakeholder requirements
- Identify data sources and time periods
- Establish materiality thresholds and accuracy targets
- Select appropriate analytical frameworks

### Phase 2: Data Analysis & Modeling
- Collect and validate financial data (income statement, balance sheet, cash flow)
- **Validate input data completeness** before running ratio calculations (check for missing fields, nulls, or implausible values)
- Calculate financial ratios across 5 categories (profitability, liquidity, leverage, efficiency, valuation)
- Build DCF models with WACC and terminal value calculations; **cross-check DCF outputs against sanity bounds** (e.g., implied multiples vs. comparables)
- Construct budget variance analyses with favorable/unfavorable classification
- Develop driver-based forecasts with scenario modeling

### Phase 3: Insight Generation
- Interpret ratio trends and benchmark against industry standards
- Identify material variances and root causes
- Assess valuation ranges through sensitivity analysis
- Evaluate forecast scenarios (base/bull/bear) for decision support

### Phase 4: Reporting
- Generate executive summaries with key findings
- Produce detailed variance reports by department and category
- Deliver DCF valuation reports with sensitivity tables
- Present rolling forecasts with trend analysis

### Phase 5: Follow-up
- Track forecast accuracy (target: +/-5% revenue, +/-3% expenses)
- Monitor report delivery timeliness (target: 100% on time)
- Update models with actuals as they become available
- Refine assumptions based on variance analysis

## Tools

### 1. Ratio Calculator (`scripts/ratio_calculator.py`)

Calculate and interpret financial ratios from financial statement data.

**Ratio Categories:**
- **Profitability:** ROE, ROA, Gross Margin, Operating Margin, Net Margin
- **Liquidity:** Current Ratio, Quick Ratio, Cash Ratio
- **Leverage:** Debt-to-Equity, Interest Coverage, DSCR
- **Efficiency:** Asset Turnover, Inventory Turnover, Receivables Turnover, DSO
- **Valuation:** P/E, P/B, P/S, EV/EBITDA, PEG Ratio

```bash
python scripts/ratio_calculator.py assets/sample_financial_data.json
python scripts/ratio_calculator.py assets/sample_financial_data.json --format json
python scripts/ratio_calculator.py assets/sample_financial_data.json --category profitability
```

### 2. DCF Valuation (`scripts/dcf_valuation.py`)
```
