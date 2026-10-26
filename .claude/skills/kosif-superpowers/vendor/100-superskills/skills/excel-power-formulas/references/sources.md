# مصادر «إكسل: الصيغ والقوة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## excel-pivot-wizard (1633-excel-analyst-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/business-tools/excel-analyst-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1633-excel-analyst-pro/4606-excel-pivot-wizard
- الوصف: Create advanced Excel pivot tables with calculated fields and slicers.

```markdown
# Excel Pivot Wizard

## Overview

Creates advanced pivot tables with calculated fields, slicers, and dynamic dashboards for data analysis and reporting.

## Prerequisites

- Excel or compatible spreadsheet software
- Tabular data with headers
- Clear understanding of analysis dimensions and measures

## Instructions

1. Verify source data is in tabular format with headers
2. Create pivot table from data range
3. Configure rows, columns, values, and filters
4. Add calculated fields for custom metrics
5. Insert slicers for interactive filtering
6. Format and style for presentation

## Output

- Configured pivot table with appropriate aggregations
- Calculated fields for derived metrics
- Interactive slicers for filtering
- Dashboard-ready formatting

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Field not found | Changed source data | Refresh data connection |
| Calculated field error | Invalid formula | Check field names match exactly |
| Slicer not updating | Disconnected report | Reconnect slicer to pivot |

## Examples

**Example: Sales Dashboard**
Request: "Create a pivot summarizing sales by region and product"
Result: Pivot with region rows, product columns, revenue values, and date slicer

**Example: Financial Analysis**
Request: "Build a pivot showing monthly trends by cost center"
Result: Time-series pivot with calculated YoY growth fields

## Resources

- [Microsoft Pivot Table Guide](https://support.microsoft.com/)
- `${CLAUDE_SKILL_DIR}/references/pivot-formulas.md` for calculated field syntax
```

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

## render-xlsx (3589-xbert-working-paper)

- الترخيص: **MIT**  ·  الأصل: https://github.com/xbertintelligence/xbert-plugins/tree/7e6bcc16a3fd1da830522d1d30f97a76c52b67aa/plugins/xbert-working-paper
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3589-xbert-working-paper/14403-render-xlsx
- الوصف: Render an XBert working-paper schedule as a real .xlsx file from a structured payload. Use when an XBert plugin (Tax Reconciliation, Div 7A Schedule, Trial Balance Alignment, Practice Metrics, FBT Prep, Payment Run, Month-End Pack and similar) has finished its analysis and produced a schedule-shaped payload that needs to become an Excel workbook with formula-live cells. Triggers include "Excel sch

```markdown
# Render an Excel schedule

Take a structured schedule payload from an XBert consumer plugin and write a `.xlsx` file with formula-live cells. Validate the workbook before reporting success, including a mandatory recalculation step that fails on `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`.

## Payload schema

```json
{
  "check_reference_id": "TAXRECON-2026FY-11752-001",
  "plugin": "xbert-tax-reconciliation",
  "tenant_name": "Acme Pty Ltd",
  "period": "FY2026",
  "title": "Accounting-to-Tax Reconciliation",
  "sheets": [
    {
      "name": "Reconciliation",
      "columns": ["Item", "Accounting", "Adjustment", "Tax"],
      "column_widths": [40, 14, 14, 14],
      "rows": [
        ["Accounting profit",        125000.00, 0,        125000.00],
        ["Add: Entertainment 50%",      0,      2400.00,    2400.00],
        ["Less: Accounting depreciation", 0,  -18500.00,  -18500.00],
        ["Add: Tax depreciation",       0,    21300.00,   21300.00],
        ["Taxable income",            "=SUM(B2:B5)", "=SUM(C2:C5)", "=SUM(D2:D5)"]
      ],
      "header_style": "default",
      "freeze_top_row": true,
      "number_format": "#,##0.00;(#,##0.00)"
    }
  ]
}
```

Cells that start with `=` are interpreted as Excel formulas (per Anthropic's xlsx skill guidance — always prefer formulas to hard-coded calculated values). Save the payload to `outputs/<check_reference_id>/payload.json`.

## Render

```!
python3 "${CLAUDE_SKILL_DIR}/scripts/render_xlsx.py" --payload outputs/<check_reference_id>/payload.json --out outputs/<check_reference_id>/working-paper.xlsx
```

The script uses `openpyxl` for writing and `pandas` if numeric reshaping is needed. It emits a JSON line on stdout: `path`, `exists`, `size_bytes`, `sheet_count`, `cell_count`, `status`.

If `openpyxl` is not installed:

```!
pip install --quiet openpyxl pandas
```

## Mandatory recalc gate

After writing the file, force a recalculation pass and scan for errors. Anthropic's official xlsx skill mandates this:

```!
python3 "${CLAUDE_SKILL_DIR}/scripts/recalc.py" outputs/<check_reference_id>/working-paper.xlsx 30
```

If LibreOffice (`soffice`) is on PATH the script uses it headlessly to recalculate formulas; otherwise it scans the saved file for static error cells. Either way, the script returns JSON with `status: "ok"` or `status: "errors_found"` plus a list of offending cells.

## Verification gate

Report success **only** when:

- The render script JSON has `status == "ok"` and `cell_count > 0`.
- The recalc script JSON has `status == "ok"` and no errors listed.
- The file exists and `size_bytes > 1024`.

If anything fails, surface the offending cells (sheet + cell ref + error code) verbatim. Do not paper over `#REF!`.

## Output handoff
```

## excel (549-excel-tools)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/excel-tools
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/549-excel-tools/1578-excel
- الوصف: Generate Excel reading and writing

```markdown
# excel

Generate Excel reading and writing.

## Tools

This skill uses the following tools:

- **Read** - Read files from the filesystem
- **Write** - Write files to the filesystem
- **Edit** - Edit existing files with precise replacements
- **Bash** - Execute shell commands
- **Grep** - Search file contents with regex patterns
- **Glob** - Find files by name patterns
```

## adobe-anyexcel (103-adobe-for-creativity)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/adobe/skills/tree/acb6d76475e6c522a5b109d2df7c8a794ee74ea7/plugins/creative-cloud/adobe-for-creativity
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/103-adobe-for-creativity/227-adobe-anyexcel
- الوصف: MANDATORY when an Excel/XLSX task's source content is an uploaded PDF — including when the PDF's text or tables are already extracted and visible in the conversation. Covers: 'convert this pdf to excel/xlsx', 'pull the tables from this pdf into a spreadsheet', 'turn this pdf into a spreadsheet'. Requires viewing THIS file before defaulting to hand-authoring a spreadsheet with openpyxl/pandas. Rout

```markdown
# Adobe AnyExcel

This is a routing file, not a standalone authoring tool. It exists for exactly one decision: **is this XLSX task's source content a PDF?**

## Tool Reference

| Step | Tool | Notes |
|---|---|---|
| Initialize | `adobe_mandatory_init` | Required before `pdf_export` |
| Convert PDF to XLSX | `pdf_export` | `target_format: xlsx` |

## Workflow

### Step 0 — Initialize Adobe Tools

Call `adobe_mandatory_init` before calling `pdf_export`.

```json
{ "skill_name": "adobe-anyexcel", "skill_version": "1.0.0" }
```

### Router

- **Source is an uploaded/attached PDF (even if its text or tables are already visible in the conversation as extracted content)** → this is a PDF-to-XLSX conversion. Check the `adobe-anypdf` skill, call `adobe_mandatory_init`, then `pdf_export` with `target_format: xlsx`. Do this *before* opening the public `xlsx` skill or writing any `openpyxl`/`pandas` code.
- **No PDF involved** — building a spreadsheet from scratch, cleaning a `.csv`, editing an existing `.xlsx`, building a financial model or chart — this file has nothing to add. Go straight to the public `xlsx` skill.

### When to still prefer hand-authoring over `pdf_export`

`pdf_export` reproduces the PDF's tables and layout as a spreadsheet — it does not restructure data, build formulas, or clean up inconsistent tables. Prefer building the spreadsheet by hand with the `xlsx` skill instead, even when the source is a PDF, if:

- The user wants the extracted data *cleaned, restructured, or turned into a model* (formulas, pivot-style summaries) rather than a literal table dump.
- `pdf_export` fails with a clear transient error — retry once. If it still fails, is unavailable, or the Adobe connector isn't reachable at all, fall back to hand-authoring with the `xlsx` skill.
- The user has already seen the `pdf_export` output and asked for something different.

When in doubt, running `pdf_export` first and showing the result costs little — a direct conversion is a fine starting point to compare against, and the user can then ask for cleanup if the table structure didn't carry over well.

### Known failure mode — do not repeat

This file exists because of a reproduced, confirmed failure in the equivalent PPTX case: given a PDF with its text already extracted into the conversation, plus a request to convert it, the model has repeatedly defaulted straight to hand-authoring with the target format's own skill — skipping `pdf_export` entirely, even when `adobe-anypdf`'s own MANDATORY router already covered the request. The same pattern is expected to apply here. If you notice yourself about to call `openpyxl`, `pandas.to_excel`, or build a spreadsheet from visible PDF text by hand, stop and check `pdf_export` first.
```

## google-sheets (2700-google-drive)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/google-drive
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2700-google-drive/10375-google-sheets
- الوصف: Analyze and edit connected Google Sheets with range precision. Use when the user wants to create Google Sheets, find a spreadsheet, inspect tabs or ranges, search rows, plan formulas, create or repair charts, clean or restructure tables, write concise summaries, or make explicit cell-range updates.

```markdown
# Google Sheets

Use this skill to keep spreadsheet work grounded in the exact spreadsheet, sheet, range, headers, and formulas that matter.

### Spreadsheets clarification questions

- Ask for new spreadsheets or major rewrites. Skip this for edits/conversions.
- Inspect prompt, conversation history, existing file and relevant references to figure out what questions to ask.
- Questions should cover topic, audience, and purpose and come before planning
- When asking questions, focus on consequential dimensions not stated or clearly implied.
- When the artifact is a new analysis, focus on which definition, metric, or lens should drive conclusions.
- Unresolved reference labels or question marks are user-owned: ask, don't infer.
- Once topic, audience, and purpose are clear, proceed without asking. Choose emphasis, format, length, style, details. Use placeholders for missing facts.

Use `request_user_input` once if available, else ask via a message. Have the best suggestion first. Append `(Recommended)` to its label. Have another good alternative second. Have `Use your judgment` as the third and final option. If the request times out or returns no answer, proceed using your best judgment; do not ask again.

## Purpose Of This File

This file is intentionally minimal and only covers:

1. routing to the right spreadsheet workflow
2. stateful operation and mandatory routing to reference files
3. live-read/search safety for direct connector calls

Detailed editing, formula, chart, upload, live-read/search, and batch-update rules live in `references/`.
Latency is not a constraint for this skill, so always read the relevant reference files before performing the task.
If the user has not provided explicit style direction, read `references/style-profiles.md` and apply the appropriate Google Sheets destination default before authoring workbook formatting.

## Default Routing

1. New Google Sheet from a native Google Sheets reference or template URL: copy the entire source workbook with the Drive file-copy action, then trim or repair the copy. Treat a deep-linked `gid` as the initial view, not copy scope. Duplicate one source sheet only when the user explicitly requests a single-sheet extraction. Do not rebuild through `.xlsx` when chips, validation, formulas, rich links, or formatting matter.
2. Other new Google Sheets creation: Inspect the available skills and plugins for the registered `Spreadsheets` capability. It may be exposed as the `$Spreadsheets` skill, the `@Spreadsheets` plugin, or the plugin URI `plugin://spreadsheets@openai-primary-runtime`. If found, load and follow its instructions.
```
