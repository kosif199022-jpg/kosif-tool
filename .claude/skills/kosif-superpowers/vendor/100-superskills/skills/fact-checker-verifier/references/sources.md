# مصادر «مدقّق الحقائق والمُحقِّق» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## verify-claims (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4131-verify-claims
- الوصف: Extract every verifiable claim in marketing copy — statistics, rankings, awards, citations, performance and time-bound assertions — and check each against a user-supplied evidence JSON, classifying it verified, partially verified, unverified, or contradicted, with corrected-text and hedged-language suggestions. Without an evidence file it runs extraction-only and generates a template to fill in. T

```markdown
# /digital-marketing-pro:verify-claims

## Purpose

Cross-check marketing claims against user-provided evidence data. Extracts all verifiable claims from content — statistics, percentages, rankings, awards, certifications, named citations, performance metrics, customer counts, and time-bound assertions — then matches each against an evidence file and classifies it as verified, partially verified, unverified, or contradicted. This command is the dedicated deep-dive for claim integrity, while /digital-marketing-pro:eval-content includes claim verification as one dimension of its broader quality assessment.

Marketing content that cites specific numbers, awards, or results without verified backing is a brand risk. Contradicted claims erode trust if caught by customers, journalists, or regulators. This command ensures every factual assertion in your content is backed by real data, clearly sourced, and defensible under scrutiny.

## Input Required

The user must provide (or will be prompted for):

- **Content with claims**: The text to verify — provided inline, as a pasted block, or as a file path. Any marketing content that makes factual assertions: landing pages, case studies, press releases, ad copy, pitch decks, investor materials, product pages, or client reports
- **Evidence file** (optional but strongly recommended): A JSON file containing source data to verify against. Format: `[{"claim": "descriptive claim text", "source": "data source name or URL", "date": "YYYY-MM-DD when verified", "verified": true/false, "value": "the verified number or fact"}]`. Can be exported from GA4, CRM, sales data, certification bodies, or assembled manually. If not provided, the command operates in extraction-only mode and guides the user on creating an evidence file
- **Specific claim to check** (optional): A single claim to focus on instead of scanning the full content — useful for quick spot-checks on a particular statistic or assertion

## Process

1. **Load brand context**: Read `~/.claude-marketing/brands/_active-brand.json` for the active slug, then load `~/.claude-marketing/brands/{slug}/profile.json`. Apply compliance rules for target markets (`skills/context-engine/compliance-rules.md`) — some industries and regions have stricter requirements for substantiating claims (financial services, healthcare, EU consumer protection). Also check for guidelines at `~/.claude-marketing/brands/{slug}/guidelines/_manifest.json` — if present, load messaging restrictions that may define approved claims and prohibited assertions. Check for agency SOPs at `~/.claude-marketing/sops/`. If no brand exists, ask: "Set up a brand first (/digital-marketing-pro:brand-setup)?" — or proceed with defaults.
```

## rp-source-evidence (3419-wix)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wix/skills/tree/8fc544d319c4a4dfc7ccf3ba4adf328e1fa9866f
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14023-wix-headless-replatform/resources/rp-source-evidence
- الوصف: Produce fresh browser-derived source evidence and implementation contracts for a headless clone.

```markdown
# Source evidence

Load this resource only after project context is valid and when source evidence is missing
or stale. It owns extraction and generated planning artifacts; it does not implement the
clone.

Read `references/workflow.md`, `references/extraction-schema.md`,
`references/interaction-runtime-contract.md`,
`references/layout-blueprint-contract.md`,
`references/control-and-visual-fidelity-contract.md`, and
`references/ui-normalization-contract.md`.

Run `site-clone.mjs` using the active mode and refresh canonical `docs/site-clone/`
artifacts before generating new ones. Emit stage-level progress. Browser extraction is
mandatory: capture source screenshots at required viewports and use browser evidence for
shared chrome and first-viewport content, not SEO metadata or an HTML-only fallback.

Resolve the home page before capture. This resource implements home scope only; do not
accept explicit additional URLs or silently run the previous multi-page artifact flow.
An ambiguous or unreachable home identity is a global blocker with an exact unblock action.

Capture observations, then project and freeze the source-of-truth tree under
`docs/site-clone/extraction/<capture-id>/`: page resolution/capture, foundation, metadata,
shared chrome, recursively owned section/component specs, gap records, spec index, and the
immutable extraction manifest. Write `extraction/latest.json` as the stable pointer. The
builder receives only the manifest-derived build plan, never observations or the source.

Preserve evidence rather than inference: source `@font-face` tuples and files, exact logo
variants/rendered dimensions, structured navigation hierarchy, visible hero text, repeaters,
core interaction scenes and timelines, background-media roles, composition geometry, and
responsive behavior. Safe probing is public/unauthenticated and presentation-only; block and
record navigation, forms, commerce/account actions, mutation, and unclassified controls.

Local gaps never block unrelated units. Use at most two distinct targeted recovery attempts,
then freeze the affected dependency closure provisionally with explicit assumptions and
omissions. Only a global blocker prevents manifest freeze. Once the manifest passes integrity
verification, return to the root supervisor so it can load implementation instructions.
```

## rp-source-evidence (3419-wix)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wix/skills/tree/8fc544d319c4a4dfc7ccf3ba4adf328e1fa9866f
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3419-wix/14027-rp-source-evidence
- الوصف: Produce fresh browser-derived source evidence and implementation contracts for a headless clone.

```markdown
# Source evidence

Load this resource only after project context is valid and when source evidence is missing
or stale. It owns extraction and generated planning artifacts; it does not implement the
clone.

Read `references/workflow.md`, `references/extraction-schema.md`,
`references/interaction-runtime-contract.md`,
`references/layout-blueprint-contract.md`,
`references/control-and-visual-fidelity-contract.md`, and
`references/ui-normalization-contract.md`.

Run `site-clone.mjs` using the active mode and refresh canonical `docs/site-clone/`
artifacts before generating new ones. Emit stage-level progress. Browser extraction is
mandatory: capture source screenshots at required viewports and use browser evidence for
shared chrome and first-viewport content, not SEO metadata or an HTML-only fallback.

Resolve the home page before capture. This resource implements home scope only; do not
accept explicit additional URLs or silently run the previous multi-page artifact flow.
An ambiguous or unreachable home identity is a global blocker with an exact unblock action.

Capture observations, then project and freeze the source-of-truth tree under
`docs/site-clone/extraction/<capture-id>/`: page resolution/capture, foundation, metadata,
shared chrome, recursively owned section/component specs, gap records, spec index, and the
immutable extraction manifest. Write `extraction/latest.json` as the stable pointer. The
builder receives only the manifest-derived build plan, never observations or the source.

Preserve evidence rather than inference: source `@font-face` tuples and files, exact logo
variants/rendered dimensions, structured navigation hierarchy, visible hero text, repeaters,
core interaction scenes and timelines, background-media roles, composition geometry, and
responsive behavior. Safe probing is public/unauthenticated and presentation-only; block and
record navigation, forms, commerce/account actions, mutation, and unclassified controls.

Local gaps never block unrelated units. Use at most two distinct targeted recovery attempts,
then freeze the affected dependency closure provisionally with explicit assumptions and
omissions. Only a global blocker prevents manifest freeze. Once the manifest passes integrity
verification, return to the root supervisor so it can load implementation instructions.
```

## citation-management (3199-evidence-lab-core)

- الترخيص: **MIT**  ·  الأصل: https://github.com/timsmykov/evidence-lab-plugins/tree/06321de859aedfeaf96863dbce8907403f95eedf/packs/core/evidence-lab-core
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3199-evidence-lab-core/13556-citation-management
- الوصف: Comprehensive citation management for academic research. Search OpenAlex, PubMed, and Google Scholar for papers, extract accurate metadata, validate citations, and generate properly formatted BibTeX entries. This skill should be used when you need to find papers, verify citation information, convert DOIs to BibTeX, or ensure reference accuracy in scientific writing.

```markdown
# Citation Management

## Overview

Manage citations systematically throughout the research and writing process. This skill provides tools and strategies for searching academic databases (Google Scholar, PubMed), extracting accurate metadata from multiple sources (CrossRef, PubMed, arXiv), validating citation information, and generating properly formatted BibTeX entries.

Critical for maintaining citation accuracy, avoiding reference errors, and ensuring reproducible research. Integrates seamlessly with the literature-review skill for comprehensive research workflows.

## When to Use This Skill

Use this skill when:
- Searching for specific papers on Google Scholar or PubMed
- Converting DOIs, PMIDs, or arXiv IDs to properly formatted BibTeX
- Extracting complete metadata for citations (authors, title, journal, year, etc.)
- Validating existing citations for accuracy
- Cleaning and formatting BibTeX files
- Finding highly cited papers in a specific field
- Verifying that citation information matches the actual publication
- Building a bibliography for a manuscript or thesis
- Checking for duplicate citations
- Ensuring consistent citation formatting

If a document built from these citations needs a versionable diagram, route that
separately to `markdown-mermaid-writing`.

---

## Core Workflow

Citation management follows a systematic process. Each phase below shows the canonical
command; every variant, option, and metadata-source detail is in
[references/core_workflow.md](references/core_workflow.md).

### Phase 1: Paper Discovery and Search

Find relevant papers. Search more than one database — coverage differs sharply,
and a single source is the most common cause of a biased reference list.

```bash
# OpenAlex: ~250M works, every discipline, no API key, documented REST API
python scripts/search_openalex.py "CRISPR gene editing" --limit 50 --output results.json

# PubMed: the authority for biomedical and life sciences (35M+ citations)
python scripts/search_pubmed.py "Alzheimer's disease treatment" --limit 100 --output alz.json

# Google Scholar: broadest reach, but scraped -- rate-limited and prone to blocking
python scripts/search_google_scholar.py "CRISPR gene editing" --limit 50 --output scholar.json
```

Prefer OpenAlex or PubMed as the primary source. Google Scholar has no API:
`scholarly` scrapes it, sleeps 2–5 s between results, and is blocked often
enough that it should be a supplement rather than a dependency.

Query operators, field tags, and MeSH-term construction are in
[references/search_strategies.md](references/search_strategies.md).

### Phase 2: Metadata Extraction

Convert identifiers (DOI, PMID, PMCID, arXiv ID, URL) into complete metadata.
CrossRef is the primary source for DOIs.

```bash
```

## hallucination-checks (3052-adlc-verify)

- الترخيص: **MIT**  ·  الأصل: https://github.com/shmulikdav/adlc-skills/tree/f0445434337a5fbf05ccc731dadbc7fa993d736e/adlc-verify
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3052-adlc-verify/13153-hallucination-checks
- الوصف: Use before merging agent-generated code, when a build fails on an unknown symbol, package, or flag, when an agent adds or suggests a new dependency, or when PR text claims results without evidence.

```markdown
# Hallucination Checks

**Grounded in:** Spracklen et al.: package hallucinations by code-generating LLMs; OpenSSF: Security-Focused Guide for AI Code Assistant Instructions; NIST SP 800-218A: SSDF Community Profile for Generative AI.





## Purpose

Plausible-but-nonexistent references are a signature failure of generated code. Research on package hallucinations (Spracklen et al.) found code-generating models regularly recommend packages that don't exist, which attackers can register ("slopsquatting"). Some are just broken builds; nonexistent package names are a supply-chain risk, because an attacker can register the name an agent tends to invent.

## Checklist

1. **Dependencies:** for every new or changed dependency, confirm it exists on the official registry, check the exact name (typosquats), publisher, download history, last release date, and licence. Pin versions.
2. **Imports & symbols:** confirm each imported module and called function exists in the installed version (type-check, compile, or inspect the package source).
3. **APIs:** for external APIs, confirm endpoints, parameters, and response fields against current official docs or the SDK types.
4. **Config & flags:** confirm config keys, environment variables, and CLI flags exist and are spelled as the tool expects.
5. **Paths & links:** confirm referenced files exist; confirm documentation URLs resolve.
6. **Necessity:** before vetting a new dependency, ask whether it is needed at all. Can an existing dependency or the standard library do the job? Every new package is permanent attack surface.
7. **Approval and pinning:** a new dependency is a human decision, not an agent's. Require explicit approval, pin the exact version, and commit the lockfile.
8. **Claims in PR text:** "tests pass", "no breaking changes", "performance improved" must be backed by output in the PR.

## The rule this skill must follow itself

Never state that something exists or does not exist unless you checked it in this session. If you cannot reach the registry or docs (no network, no shell), say so plainly, mark the reference **unverified**, and give the exact commands for a human to check it, for example `npm view <package> name version time maintainers repository`, `pip index versions <package>`, or the package page URL. Flagging a name as *suspicious* is fine; declaring it *nonexistent* without evidence is the same failure this skill exists to catch.

## Instructions

Run what can be run (install, build, type-check, tests). For what can't be run, check against authoritative sources. Report each reference as `verified`, `not found`, or `unverified` with the evidence; `not found` requires an actual lookup.

## Output

`| Reference | Type | Status | Evidence | Action |`
```

## analytics-verify (1277-analytics-verify)

- الترخيص: **MIT**  ·  الأصل: https://github.com/davekim917/bootstrap/tree/e179e878904a0bf41bfde2b1a20af62f0a88447d/plugins/analytics-verify
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1277-analytics-verify/2955-analytics-verify
- الوصف: Verification loop for analytics and research deliverables: a claim ledger, a mechanical check script, an independent verifier on a fresh context, a re-check of every fix, and a receipt tied to the exact file sent. Load BEFORE sending numbers or factual claims from data or research to anyone (a report, deck, PDF, CSV, dashboard, a draft for someone else, or a chat answer someone will act on or forw

```markdown
# Analytics verify

In agent-written analyses the computation is usually right. The errors sit in the
claims around it: numbers rounded up or retyped, the wrong unit ("people" for
accounts), sums that don't add, dropped rows, vague cutoffs, stale or wrong-location
sources, embellished copy, and new errors added while fixing old ones. Rereading your
own work doesn't catch these, because you reread your own beliefs. What catches them is
binding every claim to its source, then having someone who didn't write it check it.

The costliest error sits upstream of all of these: an exact calculation on the wrong
measure, such as shipments to a retailer when the question was the retailer's sales. So
the loop starts from the question, and the verifier checks that before any number.

## Which loop

- **Full loop (default):** anything someone may forward, publish or act on, including
  a chat answer.
- **Exploratory:** only when the requester is exploring and nothing will be forwarded
  or decided yet. Run the ledger check if you show numbers, and end with: "Exploratory,
  not verified. Ask for a check before using these numbers."

If you're unsure, use the full loop.

## Author loop

1. **Pin down the question before any query.** Fill in the ledger's `ask`: the request
   in the requester's own words and where it came from (the message, thread or call
   transcript), the exact measure (what is counted or summed, on what basis, for which
   population, grain and period), and your assumptions. When the request could mean two
   measures (sales to a retailer or by it, accounts or people, gross or net), settle it
   from the source material or ask. Don't pick one silently.
2. **Put the deliverable in a file** (message, Markdown, or the HTML a PDF renders
   from). What you send is exactly that file, including any caveats or open questions
   you plan to send with it (step 7).
3. **Keep a ledger as you work:** `claims.json` next to the deliverable, in the format
   in [references/ledger.md](references/ledger.md).
   - Numbers are read from result files, never typed. `scaffold` turns a result CSV
     into claims that point at their cells. Name each result column for what it counts
     (`AS new_customers`, not `value` or `col1`): the verifier reads every number against
     that name. When a report renders from a data file
     (a list of accounts, say), have the same script write `claims.json` from that
     data, so the ledger and the report can't drift apart.
   - Every web fact carries the source's own words, the exact business and location,
     and the date of the evidence.
   - Every sentence that combines numbers ("did both", "of which", "brings the total
     to") gets a `relations` entry.
```
