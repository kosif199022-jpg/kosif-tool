# مصادر «المحاسبة والقيود وIFRS» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## tax-reconciliation (3584-xbert-tax-reconciliation)

- الترخيص: **MIT**  ·  الأصل: https://github.com/xbertintelligence/xbert-plugins/tree/7e6bcc16a3fd1da830522d1d30f97a76c52b67aa/plugins/xbert-tax-reconciliation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3584-xbert-tax-reconciliation/14396-tax-reconciliation
- الوصف: Walk accounting profit to taxable income for a year-end tax reconciliation worksheet — company, trust, or partnership structure, with every adjustment tied to its source journal or account. Use when the user asks for the tax reconciliation, the accounting-to-tax walk, the tax-effect walk, the year-end tax worksheet, or runs the /tax-reconciliation slash command. Also triggers on "what's the taxabl

```markdown
**Source of truth — XBert MCP:** Every figure, client record, ledger transaction, payrun, and XBert notification referenced here must come from the connected XBert MCP server. Call XBert MCP tools to fetch the data — do not invent figures, estimate from context, or substitute from chat history. If the XBert MCP is not connected, ask the user to install and authenticate it before continuing.

# Tax Reconciliation

## Goal
Produce a tax-effect reconciliation from accounting profit to taxable income for a single entity, with each adjustment line tied to a journal, account or schedule. Structure adapts to entity type — company, trust, or partnership.

## Metrics
- **Adjustment coverage** — % of material adjustments tied to a named source (journal, account, schedule)
- **Reconciliation closure** — starting profit + add-backs − deductions = taxable income, no orphan lines
- **Confidence breakdown** — count of Direct vs Likely vs Needs-review adjustments

## Default thresholds (practice-configurable)
| Threshold | Value | Used in |
|---|---|---|
| Material adjustment | $500 | All sections |
| Non-deductible entertainment | 100% add-back | Add-back section |
| Non-deductible fines/penalties | 100% add-back | Add-back section |
| Private-use motor vehicle | FBT-method-dependent (logbook / stat) | Add-back section |
| Donation deductibility | DGR check required | Conditional add-back |
| Foreign-source income | Per-jurisdiction treatment | Conditional adjustment |

## Per-entity-type structure

### Company
- Starting: accounting profit before tax
- Add: non-deductible expenses
- Add: accounting depreciation
- Add: provisions movement (accounting basis)
- Less: tax depreciation
- Less: prior-year tax losses recouped
- Less: R&D concession
- Adjust: FBT (if reportable)
- Adjust: foreign-source income
- Result: taxable income → company tax @ current rate

### Trust
- Starting: trust accounting profit
- Same add-backs and deductions as company
- Distribution of net income to beneficiaries — flag if any income is undistributed (s99A risk)
- Result: net income for distribution

### Partnership
- Starting: partnership accounting profit
- Same add-backs and deductions
- Allocation to partners per agreed split — flag if split appears inconsistent with prior years
- Result: net partnership income per partner

## Adjustment categories

### Add-backs (always)
- Entertainment (fully non-deductible per ITAA s32-5)
- Fines and penalties
- Donations to non-DGRs
- Private-use portion of motor vehicle (logbook or statutory method)
- Capital expenditure expensed in books
- Accounting depreciation (replaced by tax depreciation)
- Accruals at year-end that aren't deductible until paid (e.g. annual leave for some entities)

### Deductions
- Tax depreciation per fixed asset register
```

## ias-prep (3571-xbert-ias-prep)

- الترخيص: **MIT**  ·  الأصل: https://github.com/xbertintelligence/xbert-plugins/tree/7e6bcc16a3fd1da830522d1d30f97a76c52b67aa/plugins/xbert-ias-prep
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3571-xbert-ias-prep/14383-ias-prep
- الوصف: IAS readiness methodology for Australian clients — verify the client is ready to lodge an Instalment Activity Statement with the ATO and produce a Word audit document with the supporting evidence. Use when the user asks to prep an IAS, check if a client is IAS-ready, run a monthly PAYG readiness review, or runs the /ias-prep slash command. Also triggers on: "is the IAS ready", "monthly PAYG lodgem

```markdown
**Source of truth — XBert MCP:** Every figure, client record, ledger transaction, payrun, and XBert notification referenced here must come from the connected XBert MCP server. Call XBert MCP tools to fetch the data — do not invent figures, estimate from context, or substitute from chat history. If the XBert MCP is not connected, ask the user to install and authenticate it before continuing.

# IAS Prep

A structural readiness check for an Australian IAS lodgement. Verifies bookkeeping is complete, balanced, and audit-defensible before lodging with the ATO. Produces a Word audit document with a unique check reference ID, preparer details, and the supporting evidence.

## What an IAS reports

An IAS is the form for:
- **PAYG Withholding** (W labels) — tax withheld from employee wages
- **PAYG Instalments** (T labels) — business or investment income instalments
- **FBT Instalments** — if applicable

Used by entities NOT registered for GST, and medium withholders ($25K-$1M annual withholding) who must report monthly.

### Key labels

| Label | Description |
|---|---|
| W1 | Total salary, wages and other payments (gross) |
| W2 | Amount withheld from W1 payments |
| W3 | Other amounts withheld (interest, dividends, no TFN) |
| W4 | Amounts withheld where no ABN quoted |
| W5 | Total withheld (W2 + W3 + W4) |
| T1 | Instalment income (gross business + investment income — option-1 core field) |
| T2 | Applied instalment rate |
| T3 | New varied rate (if varying under option 1) |
| T4 | Reason code for an option-1 variation |
| T7 | Reason code for an option-2 variation |
| T8 | Variation amount |
| T9 | Instalment amount payable |
| T11 | Varied instalment amount (option 2) |

## Readiness checks

1. **Bank reconciliation** — all transactions for the IAS period reconciled
2. **Payroll data** — payruns posted, W1 source (gross wages) and W2 source (tax withheld) populated
3. **Superannuation** — SG posted for all payruns in the period
4. **PAYG-W labels** — W1, W2, W3, W4 and W5 verified against payrun totals
5. **PAYGW liability** — PAYGW account exists and balance matches W5 plus prior carry-over
6. **PAYG instalments** — T7 / T11 calculated correctly where applicable
7. **Outstanding XBerts** — ALL outstanding XBerts block lodgement

## Blocking rule

**All outstanding XBerts for the period block lodgement.** Do not filter by risk type. Surface each unresolved XBert with the resolution instruction; do not auto-resolve.

## Audit document structure

Generate a Word document containing:
1. Cover page — client name, ABN, IAS period, generation date
2. First-page summary — overall readiness status, count of blocking issues
3. Readiness sections (1-7 above) with pass/fail and evidence
```

## vat-prep (3587-xbert-vat-prep)

- الترخيص: **MIT**  ·  الأصل: https://github.com/xbertintelligence/xbert-plugins/tree/7e6bcc16a3fd1da830522d1d30f97a76c52b67aa/plugins/xbert-vat-prep
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3587-xbert-vat-prep/14399-vat-prep
- الوصف: VAT readiness methodology for UK clients — verify the client is ready to submit their VAT return to HMRC via MTD and produce a Word audit document. Use when the user asks to prep VAT, check if a client is VAT-ready, run a pre-submission review, check MTD compliance, or runs the /vat-prep slash command. Also triggers on: "is the VAT ready", "VAT quarter close", "MTD submission check", "VAT return p

```markdown
**Source of truth — XBert MCP:** Every figure, client record, ledger transaction, payrun, and XBert notification referenced here must come from the connected XBert MCP server. Call XBert MCP tools to fetch the data — do not invent figures, estimate from context, or substitute from chat history. If the XBert MCP is not connected, ask the user to install and authenticate it before continuing.

# VAT Prep

A structural readiness check for a UK VAT return submission. Verifies bookkeeping is complete, balanced, and HMRC-defensible before submitting via Making Tax Digital. Produces a Word audit document with a unique check reference ID, preparer details, and supporting evidence.

## VAT framework

- **Registration threshold** — £90,000 taxable turnover (mandatory)
- **Standard rate** — 20%
- **Reduced rate** — 5%
- **Zero-rated** — 0% (food, children's clothes, books, public transport)
- **Exempt** — insurance, finance, education, health services
- **Outside scope** — wages, dividends, non-business income
- **Filing** — quarterly (standard), monthly (repayment traders), annually (Annual Accounting Scheme)
- **Deadline** — 1 month and 7 days after the end of the VAT period
- **MTD** — all VAT-registered businesses must file digitally

### VAT return boxes (HMRC)

| Box | Description |
|---|---|
| 1 | VAT due on sales and other outputs |
| 2 | VAT due on acquisitions from EU member states (NI only) |
| 3 | Total VAT due (Box 1 + Box 2) |
| 4 | VAT reclaimed on purchases and other inputs |
| 5 | Net VAT to pay or reclaim (Box 3 - Box 4) |
| 6 | Total value of sales excluding VAT |
| 7 | Total value of purchases excluding VAT |
| 8 | Total value of supplies to EU excluding VAT (NI only) |
| 9 | Total value of acquisitions from EU excluding VAT (NI only) |

## Readiness checks

1. **Data quality** — score >= 50 to proceed
2. **Lock dates** — prior period must be locked
3. **Bank reconciliation** — all accounts reconciled for the period
4. **VAT control accounts** — output and input VAT accounts reconciled, suspense at zero
5. **VAT code accuracy** — correct codes on transactions
6. **Zero-rated vs exempt** — proper classification verified
7. **Credit notes** — correct VAT treatment
8. **P&L review** — revenue consistent with Box 6, compared to prior period
9. **Balance sheet review** — VAT accounts and suspense at zero
10. **Payroll & PAYE** — PAYE / NI deductions verified, pension auto-enrolment checked
11. **Accounts payable** — outstanding bills reviewed
12. **Accounts receivable** — outstanding invoices reviewed, debtor management flagged
13. **Cash flow** — period cash movements reviewed
14. **Outstanding XBerts** — ALL block submission
15. **MTD compliance** — digital filing path verified
```

## tres-ledger-link (261-tres-finance-plugin)

- الترخيص: **MIT**  ·  الأصل: https://github.com/anthropics/claude-plugins-community/tree/87c843d52c12f4bc91bb23b47132eb08b70e6cb6/tres-finance-plugin
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/261-tres-finance-plugin/882-tres-ledger-link
- الوصف: Build a TRES Finance dashboard ledger URL (Transactions tab) with a precise filter set — date range, wallets, assets, tags, status, amount, and more — so it can be shared with a customer or reused. Use whenever the user asks for a "ledger link", "dashboard link", "filter URL", or "send <customer> a link to <some filtered view>". Scoped to the Transactions tab only (not Accounting, Roll Forward, Pi

```markdown
# Generate Dashboard Ledger Link

Your job is to produce a working TRES Finance dashboard URL that opens the **Transactions tab of the
ledger** with a precise filter set applied, so the user can share it with a customer (or use it
themselves).

This skill is scoped to the **Transactions tab only**. If the user asks for a link to Accounting,
Roll Forward, Pivot Tables, Cost Basis, or Trial Balances — stop and tell them this skill does not
cover those tabs.

---

## Step 1 — Resolve the org subdomain

The dashboard URL is `https://<org-subdomain>.tres.finance/ledger`.

Resolve `<org-subdomain>` from the MCP `get_viewer` query (use the returned `orgName`). **Do not ask
the user.**

```graphql
query { viewer { orgName } }
```

State the subdomain you used in your final message so the user can correct it in one shot if it is
wrong.

---

## Step 2 — Collect the filters the user wants

Read the filters out of the user's request in plain English (date range, wallets, assets, tags,
status, etc.). If a filter is ambiguous (e.g. "USDC" when the org has multiple USDC variants, or "Q1"
without a year), ask before generating. A wrong value silently produces a broken / empty view.

Only include filters the user explicitly asked for. The dashboard fills in defaults for everything
else — extra params just add noise.

---

## Step 3 — Build the URL

Base path is always:

```
https://<org-subdomain>.tres.finance/ledger
```

No path segment after `/ledger` (that is the Transactions tab).

Append `?` and the query string built from the rules below. URL-encode every value (spaces → `%20`).
Inside a single value, encode commas; between distinct array items, a comma is the literal delimiter.

### 3.1 Date & pagination

| Param      | Format / values | Notes |
|------------|-----------------|-------|
| `fromDate` | `YYYY-MM-DD` | UTC date |
| `toDate`   | `YYYY-MM-DD` | UTC date |
| `dateType` | `Month to date`, `Year to date`, `Last 30 days`, `Last month`, `Before this month`, `Custom date`, `All time`, `Year`, `Quarters` | URL-encode spaces. **Omit** if `Last 30 days` (default). For an arbitrary `fromDate`/`toDate` range, use `Custom date`. |
| `page`     | integer | Omit if `1`. |
| `pageSize` | integer | Omit if `20` (default). |

If `dateType=All%20time`, `fromDate` / `toDate` are ignored — do not include them.

### 3.2 Multi-select array filters (comma-joined IDs)

| Param | What goes in it |
|-------|-----------------|
| `internalAccounts` | numeric database ID of org-owned wallets |
| `tags` | wallet group IDs, or `no-label` for unlabeled |
| `thirdPartyAccounts` | raw address string of an external account (sender/receiver identifier on a sub-transaction — not necessarily a named contact in the system) |
| `customNameLabelTags` | contact group IDs |
```

## accounting-inbox (1196-carrel-finance)

- الترخيص: **MIT**  ·  الأصل: https://github.com/coltonbearden/carrel/tree/84f7053d2551038986e54865274059d5986d103a/plugins/carrel-finance
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1196-carrel-finance/2839-accounting-inbox
- الوصف: The end-to-end recipe for turning a folder of invoices, receipts, statements and billing emails into a searchable archive with carrel — extract fields, cross-reference by invoice/PO/IBAN numbers, name and file by date or fiscal period, then query with meta find and tag find. Use when the user has an accounting inbox, a pile of receipts, or asks which documents belong to a payment.

```markdown
# The accounting inbox with carrel

Five commands do the whole job: `fields` reads a document, `refs` links documents that share a number, `rename` names them, `intake` files them, and `meta`/`search`/`tag` answer questions afterwards. Everything is dry-run first; run `carrel doctor` once to see what your environment can read.

## 1. Read one document before trusting the batch

```bash
carrel --json fields invoice.pdf              # vendor, invoice_no, po, date, due, subtotal, tax, total, currency, iban
carrel --json fields receipts/ --profile receipt --date-order dmy --ocr
```

Each field carries a **confidence**: `high` (it followed its label — `Total Due`, `Invoice Date`), `medium` (a heuristic: the largest amount, the first date, `Net 30` → due date, the first name-like line as vendor), `low` (a fallback: the file's mtime or name). Fix a wrong one with `--set vendor="Acme Corp"` for that run. Only `high`/`medium`/`user` values are ever written to the desk.

## 2. Link the documents that belong together

```bash
carrel --json refs ~/accounting --link        # values that appear in more than one file
carrel --root ~/accounting refs ~/accounting --tag
carrel --root ~/accounting tag find ref:invoice:inv-2026-0042
```

Kinds: label-driven `invoice`, `po`, `order`, `check`, `account`, `tracking`, `ticket`, plus check-digit-verified `iban`, `routing`, `ein`, `vat`, `isbn`, `gtin`, `doi`, `ups`, `usps`. A value with a check digit only appears when the digit verifies, so a nine-digit number is a routing number only when it really is one. Add a house format with `--pattern acme='ACME-(?P<v1>\d+)'`.

## 3. Name and file

```bash
carrel rename ~/inbox/*.pdf --template '{date}_{vendor}_{ref}{ext}'          # dry-run
carrel intake ~/inbox --to ~/accounting                                       # dry-run: the whole pipeline
carrel intake ~/inbox --to ~/accounting --apply --by period --fiscal-start 7  # FY2027/Q1/...
```

`intake` per file: fields → refs → name → move into `YYYY/MM` (or `FY<year>/Q<n>`) → index → save fields → tag. Scans are OCRed into a searchable copy and the original is kept under `_originals/`. Nothing is overwritten; nothing is deleted. `--watch --stable 5` keeps filing what arrives, waiting for slow scanners to finish writing.

## 4. Ask the questions

```bash
carrel --root ~/accounting meta find 'total>1000' 'due<2026-11'
carrel --root ~/accounting meta find 'vendor~acme' 'paid=false'
carrel --root ~/accounting search 'overdue OR reminder' --meta 'total>500' --type pdf,eml
carrel --root ~/accounting meta export -o fields.csv        # the folder as a spreadsheet
```

Numbers compare numerically and ISO dates chronologically (`due<2027` works as a prefix), because `fields --save` and `intake` store them canonically with a kind.
```

## reconciliation-automatch (2294-finance)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/finance
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2294-finance/8794-reconciliation-automatch
- الوصف: Auto-match GL journal lines to sub-ledger / bank lines (exact, tolerance, and many-to-one grouped) and AUTO-CERTIFY an account only when its unexplained residual is within materiality — else FLAG for a human. The auto-match engine reconcile_summary.py's static tie-out lacked. Runs scripts/recon_match.py. Used by `controller`.

```markdown
# Skill: reconciliation-automatch

**Purpose:** Turn balance-sheet reconciliation from *eyeball every account* into *review-by-exception*. The static [`reconciliation-summary`](../reconciliation-summary/SKILL.md) skill compares a book balance to a single sub-ledger **total** and flags the delta — it is the tie-out readout, but it cannot say *which lines* explain the difference, so a human still reviews everything. This skill is the auto-**match** engine that closes that gap: it pairs GL lines to sub-ledger / bank lines, explains the difference line-by-line, and auto-certifies only the accounts whose unexplained residual is immaterial. This is the FloQast AutoRec / Numeric discipline.

Engine: [`../../scripts/recon_match.py`](../../scripts/recon_match.py) (stdlib only, Python 3.8+).

## When to use

- You have per-line GL detail and a sub-ledger / bank export for the same accounts (CSV: `account,reference,amount[,description]`), and you want the engine to match them and tell you *only* the accounts a human must actually look at.
- You are wiring the close cycle and want reconciliation to gate on **material** breaks, not on every penny.

## The match ladder (greedy, in order — earlier stages win)

1. **exact** — same `reference` and amount equal to the cent.
2. **tolerance** — same `reference` and `|amount delta| <= --tolerance` (bank rounding, FX pennies, a fee netted on one side). The delta is **recorded in the trail, never hidden**.
3. **grouped** — many-to-one / one-to-many: remaining lines that **share a reference**, where the group's GL sum ties to its sub-ledger sum within tolerance (e.g. two partial receipts booked against one bank deposit).

Anything still unmatched is a **break**.

## Review-by-exception, and why it is materiality-bounded

For each account:

```
residual = GL_total − subledger_total − matched_delta
```

`matched_delta` is the net `(GL − sub)` across every matched pair/group (0 for an exact match, the epsilon for a tolerance match, the group net for a grouped match). By construction the residual equals `(unmatched GL) − (unmatched sub)` — i.e. **the residual is exactly the net of the break items**; matched lines cancel. The engine asserts that identity every run as an independent cross-check.

- `|residual| <  materiality` → **AUTO-CERTIFIED** (review-by-exception). An account can auto-certify while still carrying an *immaterial* unmatched item — the item stays disclosed in the match trail; it just does not warrant a human's time.
- `|residual| >= materiality` → **FLAGGED**. A human controller owns it. `--strict` makes the whole run exit non-zero (rc 3) so the close cannot advance past an un-cleared material break.
```
