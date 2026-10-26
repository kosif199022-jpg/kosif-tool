# مصادر «الفواتير والعروض والعقود» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## contract-to-billing (107-airwallex-agentos)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/airwallex/airwallex-marketplace/tree/b418b9913e4919f85257aa1e25319e59464e8fae/plugins/airwallex-agentos
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/107-airwallex-agentos/265-contract-to-billing
- الوصف: Extract billing details from purchase orders, contracts, or quotes, then set up Airwallex Billing by creating invoices and/or subscriptions — matching existing customers, products, and prices to avoid duplicates. Use when the user says "create invoice from this PO", "set up billing from this contract", "create a subscription from this agreement", "invoice this quote", "bill this customer", or atta

```markdown
# Contract to Billing

Reads a customer document (PO, contract, quote), extracts line items with AI, and creates a fully populated invoice in Airwallex Billing.

## When to use

- User uploads or references a purchase order, contract, quote, or billing document
- User asks to "create an invoice" from a document
- User wants to extract billing details and set up products/prices/customers
- User says "bill this customer" with a document attached

## When NOT to use

This skill only covers Billing-domain operations — invoices (list, create, retrieve, finalize, void, mark-as-paid, plus line-item add / update / delete / list), products (list, create), prices (list, create), customers (list, retrieve, create, update), subscriptions (create, list items), coupons (list, create, update), meters (list, create, update), payment sources (list), and billing transactions (list, retrieve). Credit notes follow `create` → `line-items add` → `finalize` — if the operation is not exposed on the current surface, direct the user to the Airwallex Dashboard.

If the task requires capabilities outside this domain, **stop — this is the wrong skill.** Redirect the user:

- Wire transfers / payouts → not yet available (use Airwallex Dashboard)
- Setting up suppliers / beneficiaries → **beneficiary-creation** skill
- FX conversions, balances, treasury → **manage-cashflow** skill
- Provisioning corporate cards → **card-provisioning** skill
- Ad-hoc tasks outside billing workflow → **awx-best-practices** skill (fallback)

## Non-negotiables

### Terminology

- **Invoices = receivables (money in).** Issued BY the user TO their customers. Never say "obligation" for invoices.
- **Invoice lifecycle.** **DRAFT → add line items → finalize → FINALIZED (immutable)**. To correct after finalize: void → create new.
- **Products & prices.** Every invoice line item needs a product. For document-specific ad-hoc fees (shipping, handling, setup fees, tax), always use the **inline price mechanism** (see Path B in Workflow) with a newly created product rather than matching existing fee products — fee amounts and descriptions vary per order. Only reuse existing products for the core goods/services sold (e.g., "Widget Alpha").
- **Invoice vs Subscription.** One-time quote → Invoice. Recurring terms → Subscription. Choose before creating.
- **ONE_OFF vs RECURRING.** Baked in at price creation — cannot flip later.
- **`collection_method` mapping from document language:**

| Document says | API value |
| --- | --- |
| "send invoice", "bank transfer", "wire transfer", "offline payment", "pay by bank" | `OUT_OF_BAND` |
| "online payment", "checkout", "payment link", "pay online" | `CHARGE_ON_CHECKOUT` |
| "auto-debit", "direct debit", "auto-charge" | `AUTO_CHARGE` |
```

## contract-and-proposal-writer (136-business-growth-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/business-growth
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/136-business-growth-skills/384-contract-and-proposal-writer
- الوصف: Generate professional, jurisdiction-aware business documents: freelance contracts, project proposals, SOWs, NDAs, and MSAs. Structured Markdown output with docx conversion instructions. Covers US (Delaware), EU (GDPR), UK, and DACH (German law) jurisdictions. Not a substitute for legal counsel — use as strong starting points. Use when drafting a freelance contract, preparing a client proposal, wri

```markdown
# Contract & Proposal Writer

**Tier:** POWERFUL
**Category:** Business Growth
**Domain:** Legal Documents, Business Development, Client Relations

---

## Overview

Generate professional, jurisdiction-aware business documents: freelance contracts, project proposals, SOWs, NDAs, and MSAs. Outputs structured Markdown with docx conversion instructions. Covers US (Delaware), EU (GDPR), UK, and DACH (German law) jurisdictions.

**Not a substitute for legal counsel.** Use these templates as strong starting points; review with an attorney for high-value or complex engagements.

---

## Core Capabilities

- Freelance development contracts (fixed-price & hourly)
- Project proposals with timeline/budget breakdown
- Statements of Work (SOW) with deliverables matrix
- NDAs (mutual & one-way)
- Master Service Agreements (MSA)
- Jurisdiction-specific clauses (US/EU/UK/DACH)
- GDPR Data Processing Addenda (EU/DACH)

---

## Key Clauses Reference

| Clause | Options |
|--------|---------|
| Payment terms | Net-30, milestone-based, monthly retainer |
| IP ownership | Work-for-hire (US), assignment (EU/UK), license-back |
| Liability cap | 1x contract value (standard), 3x (high-risk) |
| Termination | For cause (14-day cure), convenience (30/60/90-day notice) |
| Confidentiality | 2-5 year term, perpetual for trade secrets |
| Warranty | "As-is" disclaimer, limited 30/90-day fix warranty |
| Dispute resolution | Arbitration (AAA/ICC), courts (jurisdiction-specific) |

---

## When to Use

- Starting a new client engagement and need a contract fast
- Client asks for a proposal with pricing and timeline
- Partnership or vendor relationship requiring an MSA
- Protecting IP or confidential information with an NDA
- EU/DACH project requiring GDPR-compliant data clauses

---

## Workflow

### 1. Gather Requirements

Ask the user:

    1. Document type? (contract / proposal / SOW / NDA / MSA)
    2. Jurisdiction? (US-Delaware / EU / UK / DACH)
    3. Engagement type? (fixed-price / hourly / retainer)
    4. Parties? (names, roles, business addresses)
    5. Scope summary? (1-3 sentences)
    6. Total value or hourly rate?
    7. Start date / end date or duration?
    8. Special requirements? (IP assignment, white-label, subcontractors)

### 2. Select Template

| Type | Jurisdiction | Template |
|------|-------------|----------|
| Dev contract fixed | Any | Template A |
| Consulting retainer | Any | Template B |
| SaaS partnership | Any | Template C |
| NDA mutual | US/EU/UK/DACH | NDA-M |
| NDA one-way | US/EU/UK/DACH | NDA-OW |
| SOW | Any | SOW base |

### 3. Generate & Fill

Fill all [BRACKETED] placeholders. Flag missing data as "REQUIRED".

### 4. Convert to DOCX

```bash
# Install pandoc
brew install pandoc        # macOS
apt install pandoc         # Ubuntu
```

## contract-review (335-small-business)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/anthropics/knowledge-work-plugins/tree/8444efcd48f7012f09797778a36a33e73d0861f4/small-business
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/335-small-business/1144-contract-review
- الوصف: Lightweight NDA, MSA, and vendor contract review for SMBs without legal on staff. Reads contracts from local files, mail attachments (Gmail or M365), a connected file store (Google Drive or M365), or DocuSign envelopes; flags non-standard terms; explains risks in plain English; and outputs a marked-up redline as a separate DOCX. Use when the user says "review this contract," "what am I signing," "

```markdown
# Contract Review

## Where this skill sits

Two standing jobs, neither dependent on any chain:

1. **Standalone review** — the owner forwards or uploads any NDA, MSA, lease,
   or vendor agreement and gets the plain-English risk read and the redline.
   This is the everyday case for a business with no legal on staff.
2. **The counterparty's paper in a deal** — when `proposal-builder` sends a
   proposal out and the customer's own contract comes back, this skill is the
   risk read on that paper before the owner signs. That pairing is the
   quote-to-cash story's closing beat.

## Quick start

Attach a contract file, forward the email containing it, or paste the text directly.

```
User: "Review this MSA and flag anything I should push back on."
→ Skill reads the document, identifies parties and contract type,
  analyzes 8 risk categories, returns a severity-tiered summary
  with a negotiation playbook, and exports a redlined DOCX.
```

## Workflow

1. **Get the contract** — **Use what the user already gave you first.** If they attached a file or pasted the text, that is the document; go straight to step 2 and do not touch a connector.
   - **Local file or paste**: Read the PDF (chunked via `pages` parameter for 10+ page files) or DOCX via Read tool. If the user pastes text directly, work with what's provided.
   - **Gmail or Microsoft 365** (only when nothing was handed over): Search the connected mailbox for recent emails with contract attachments (see `reference/gmail-fetch.md`, or `reference/m365-fetch.md` for Microsoft 365)
   - **Google Drive or Microsoft 365** (only when nothing was handed over, and only in a folder the owner names): search the connected file store for the document by counterparty name or agreement title — never browse recent files (see `reference/m365-fetch.md`)
   - **DocuSign** (only when nothing was handed over): Fetch the envelope by ID or search recent drafts awaiting signature (see `reference/docusign-fetch.md`)

   If no connector is available and nothing was handed over, ask the user to paste the text or attach the file. That is a normal path, not a failure.

   A connected mailbox, file store, or DocuSign account is the owner's only once its address or tenant matches the `## Business context` block or the owner names it; on a mismatch, stop and ask, and use nothing read from it (`../../shared/tenant-scope.md`).

   Read the full document before analyzing. Dangerous clauses are frequently in exhibits and schedules at the back.
```

## box-legal-workflows-contract (893-box)

- الترخيص: **MIT**  ·  الأصل: https://github.com/box/skills/tree/35567f913a2bfd7f8b59367c9df3ae14b5ad4cfe
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/893-box/2022-box-legal-workflows-contract
- الوصف: Automate contract review and monitoring with Box MCP — find new or expiring contracts, compare them against firm templates to flag material variances, write structured contract metadata back to Box for searchability, and produce variance reports with citations. Use this skill when the user mentions contract review or monitoring, NDA or MSA review, contract expiration or renewals, contract metadata

```markdown
# Contract Review Agent

> **PREREQUISITES:**
>
> - Use the `box` skill for Box MCP auth, tool selection, and base workflows. If it is not installed, run: `npx skills add https://github.com/box/skills --skill box`
> - Use the `box-legal-workflows` skill for Box collaboration role definitions, Box AI usage boundaries, and reusable confirmation phrasings. If it is not installed, run: `npx skills add box/skills --skill box-legal-workflows`

Do contract review *in Box*: find contracts with Box search, compare against the firm's template with Box AI, persist results as Box metadata so they stay searchable, and monitor dates with metadata search. This skill is the contract-specific recipe; the underlying Box tool mechanics live in the capability references below. Materiality, risk, and favorability are firm-supplied criteria confirmed by an attorney — the agent extracts facts, stores them, and routes. It does not provide legal advice or decide risk.

## Box capability references

Reach for these for tool mechanics rather than restating them here:

- The `box` skill's `references/mcp-search.md` — find contracts; metadata vs. keyword search, folder scoping, template schema lookup
- The `box` skill's `references/ai-and-retrieval.md` — compare to template and extract fields; pacing, text-rep/file limits, citations
- The `box` skill's `references/content-workflows.md` — metadata templates, `set_file_metadata`, report uploads, file comments
- The `box` skill's `references/collaboration.md` — grant the reviewing attorney access

## Box metadata model

Persist review results as file metadata so contracts stay searchable. Find or inspect the firm's template using the `box` skill's `references/mcp-search.md`; create one using its `references/content-workflows.md` if none exists.

- **Representative fields** (confirm the firm's actual set): `counterparty_name`, `contract_type`, `execution_date`, `effective_date`, `expiration_date`, `auto_renewal`, `notice_period_days`, `contract_value`, `governing_law`, `status` (active/expired/terminated/under_negotiation), `risk_rating`, `review_date`, `next_review_date`, `expiration_alert_date`. Link to matters with `matter_id`, `practice_area`, `matter_owner`.
- The `risk_rating` value is the firm/attorney's determination — store it, don't decide it.

## Contract search recipes

Once contracts carry metadata, use `search_files_metadata` (mechanics in the `box` skill's `references/mcp-search.md`; otherwise `search_files_keyword` with date filters):

- New since last review: `execution_date >= 'YYYY-MM-DD' AND execution_date <= 'YYYY-MM-DD'`
- Expiring window: `expiration_date >= 'YYYY-MM-DD' AND expiration_date <= 'YYYY-MM-DD' AND status = 'active'`
```

## implement-metered-billing (2388-subscription-billing-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/subscription-billing-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2388-subscription-billing-engineering/9245-implement-metered-billing
- الوصف: Implement usage-based / metered billing correctly — idempotent usage recording, aggregation & rating to billable quantities, on-time usage reporting before invoice close, and counted-vs-billed reconciliation. Use when billing on API calls, seats used, GB, events, or any consumption metric.

```markdown
# Skill: Implement Metered Billing

Usage-based billing is a **metering problem before it is a billing problem**. Revenue is silently lost when usage is under-counted and clawed back when over-counted. This skill builds the counting → rating → reporting → reconciliation path so billed usage equals real usage.

## When to use

- Billing on consumption (API calls, compute, storage, messages, events) or metered seats.
- Adding overage to a base plan (hybrid model).
- Diagnosing a discrepancy between what you counted and what the provider invoiced.

## Steps

1. **Define the meter precisely.** What single unit is billable, at what granularity, with what rounding, over what window (aligned to the billing period)? Ambiguity here becomes a billing dispute.
2. **Record usage idempotently.** Every usage event carries a stable, caller-supplied event key; dedupe on it so retries/at-least-once producers can't double-count. Store raw events before aggregation so you can re-derive.
3. **Aggregate and rate.** Roll raw events to billable quantity per subscription per period; apply the rating rules (tiers, included allowance, overage price). Keep aggregation deterministic and replayable from raw events.
4. **Report before invoice close.** Push usage to the provider (or generate the invoice line) before the billing period closes, respecting the provider's cutoff. Late usage either misses the invoice or triggers a correction — decide which on purpose.
5. **Reconcile counted-vs-billed.** A scheduled job compares your aggregated quantity to what the provider billed and alerts on drift. This is the safety net that catches dropped or duplicated usage. See [`../../knowledge/webhooks-idempotency-and-revrec.md`](../../knowledge/webhooks-idempotency-and-revrec.md).
6. **Handle backfills and corrections explicitly.** When late/corrected usage arrives after close, apply it as an adjustment on the next invoice, not a silent mutation of a closed period.

## Anti-patterns

- Recording usage without an idempotency key, so a producer retry double-bills.
- Aggregating destructively (no raw events) so you can't re-derive or reconcile.
- Reporting usage after the provider's cutoff and losing it silently.
- No counted-vs-billed reconciliation — drift is invisible until a customer disputes.
- Mutating a closed billing period instead of issuing an adjustment.

## Output

A metering implementation: meter definition → idempotent recording → deterministic aggregation/rating → on-time reporting → reconciliation job + drift alert → backfill/correction policy. Prove it with duplicate- and out-of-order-delivery fixtures.
```

## contract-review-and-redline (2326-legal-ops-clm)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/legal-ops-clm
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2326-legal-ops-clm/8929-contract-review-and-redline
- الوصف: Build a clause library with standard / fallback / walk-away positions, run a redline review that flags only the material deviations by risk tier, extract key terms into a structured schema, and route approval by the highest-tier deviation — operational support, not legal advice.

```markdown
# Contract Review & Redline

> Operational/process support only — not legal advice. A lawyer sets the standard/fallback positions and signs off on any deviation; this skill flags, structures, and routes — it does not adjudicate.

## Build the clause library: standard / fallback / walk-away
For each key clause — limitation of liability, indemnity, IP ownership, term/termination, confidentiality — encode the **standard** (preferred) position, the **fallback** (acceptable) position, and the **walk-away** (never-acceptable) line. Set by a lawyer once, applied consistently. The fallback is what lets a non-lawyer negotiate within bounds.

## Redline against the standard — flag what's material
Compare the counterparty draft to standard/fallback. Surface the deviations that change risk; note the rest without escalating. Escalating every comma drowns the signal. Concentrate on the key clauses where exposure concentrates.

## Tier every flag and route approval
Each deviation gets a risk tier — within fallback (self-serve), beyond fallback (escalate to the tier's approver), or walk-away (stop). The tier is the contract between business speed and legal control; it drives who must approve. A flag with no tier and no named approver is just a highlight.

## Extract key terms to a schema
Pull parties, value, effective/term dates, liability cap, indemnity scope, IP ownership, termination rights, governing law, and renewal mechanics into named fields — not prose — so the repository, the obligations tracker, and reporting can consume them.

## Output
A clause library (standard/fallback/walk-away + tier + approver per clause), a structured redline review (material deviations flagged + tiered + routed), and/or a key-term extraction. Hand the playbook wiring to `legal-ops-lead`; the obligations/dates the terms create to `obligations-and-renewals-analyst`; any legal opinion or deviation sign-off to a human lawyer.
```
