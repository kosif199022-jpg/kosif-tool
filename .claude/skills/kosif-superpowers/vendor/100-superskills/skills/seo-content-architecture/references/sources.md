# مصادر «SEO وبنية المحتوى» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## seo-schema (347-legends-seo-dungeon)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/avalonreset/seo-dungeon
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/347-legends-seo-dungeon/1268-seo-schema
- الوصف: Detect, validate, and generate Schema.org structured data. JSON-LD format preferred. Use when user says "schema", "structured data", "rich results", "JSON-LD", or "markup".

```markdown
# Schema Markup Analysis & Generation

## Detection

1. Scan page source for JSON-LD `<script type="application/ld+json">`
2. Check for Microdata (`itemscope`, `itemprop`)
3. Check for RDFa (`typeof`, `property`)
4. Always recommend JSON-LD as primary format (Google's stated preference)

## Validation

- Check required properties per schema type
- Validate against Google's supported rich result types
- Test for common errors:
  - Missing @context
  - Invalid @type
  - Wrong data types
  - Placeholder text
  - Relative URLs (should be absolute)
  - Invalid date formats
- Flag deprecated types (see below)

## Schema Type Status (as of June 2026)

Read `../seo/references/schema-types.md` for the full list. Key rules:

### ACTIVE (recommend freely):
Organization, LocalBusiness, SoftwareApplication, WebApplication, Product (with Certification markup as of April 2025), ProductGroup, Offer, Service, Article, BlogPosting, NewsArticle, Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ProfilePage, ContactPage, VideoObject, ImageObject, Event, JobPosting, Course, DiscussionForumPosting

### VIDEO & SPECIALIZED (recommend freely):
BroadcastEvent, Clip, SeekToAction, SoftwareSourceCode

See `schema/templates.json` for ready-to-use JSON-LD templates for these types.

> **JSON-LD and JavaScript rendering:** Per Google's December 2025 JS SEO guidance, structured data injected via JavaScript may face delayed processing. For time-sensitive markup (especially Product, Offer), include JSON-LD in the initial server-rendered HTML.

### NO RICH RESULTS, KEEP IF USEFUL:
- **FAQPage**: Google retired FAQ rich results for ALL sites on May 7, 2026 (supersedes the Aug 2023 gov/health restriction). No Google SERP rich-result benefit; flag existing FAQPage at Info (not Critical) rather than removal. For genuine user Q&A pages, use **QAPage**.

### DEPRECATED (never recommend):
Read `references/deprecated-types-2024-2026.md` before advising on deprecated
rich result types or replacements.

- **HowTo**: Rich results removed September 2023
- **SpecialAnnouncement**: Deprecated July 31, 2025
- **CourseInfo, EstimatedSalary, LearningVideo**: Retired June 2025
- **ClaimReview**: Retired from rich results June 2025
- **VehicleListing**: Retired from rich results June 2025
- **Practice Problem**: Deprecation notice 2025-11-05; Search Console / Rich Results Test support removed 2026-01-06
- **Book Actions**: Deprecated/removed from Google rich results; do not recommend it for SERP features.
- Search Console / Rich Results Test / appearance-filter support for CourseInfo, EstimatedSalary, LearningVideo, SpecialAnnouncement, VehicleListing was removed 2025-09-09; Practice Problem support was removed 2026-01-06.

### Supported for Dataset Search only:
```

## seo-schema (881-codex-seo)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/BestLemoon/codex-seo
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/881-codex-seo/1961-seo-schema
- الوصف: Detect, validate, and generate Schema.org structured data. JSON-LD format preferred. Use when user says "schema", "structured data", "rich results", "JSON-LD", or "markup".

```markdown
# Schema Markup Analysis & Generation

## Detection

1. Scan page source for JSON-LD `<script type="application/ld+json">`
2. Check for Microdata (`itemscope`, `itemprop`)
3. Check for RDFa (`typeof`, `property`)
4. Always recommend JSON-LD as primary format (Google's stated preference)

## Validation

- Check required properties per schema type
- Validate against Google's supported rich result types
- Test for common errors:
  - Missing @context
  - Invalid @type
  - Wrong data types
  - Placeholder text
  - Relative URLs (should be absolute)
  - Invalid date formats
- Flag deprecated types (see below)

## Schema Type Status (as of Feb 2026)

Read `references/schema-types.md` for the full list. Key rules:

### ACTIVE (recommend freely):
Organization, LocalBusiness, SoftwareApplication, WebApplication, Product (with Certification markup as of April 2025), ProductGroup, Offer, Service, Article, BlogPosting, NewsArticle, Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ProfilePage, ContactPage, VideoObject, ImageObject, Event, JobPosting, Course, DiscussionForumPosting

### VIDEO & SPECIALIZED (recommend freely):
BroadcastEvent, Clip, SeekToAction, SoftwareSourceCode

See `schema/templates.json` for ready-to-use JSON-LD templates for these types.

> **JSON-LD and JavaScript rendering:** Per Google's December 2025 JS SEO guidance, structured data injected via JavaScript may face delayed processing. For time-sensitive markup (especially Product, Offer), include JSON-LD in the initial server-rendered HTML.

### RESTRICTED (only for specific sites):
- **FAQ**: ONLY for government and healthcare authority sites (restricted Aug 2023)

### DEPRECATED (never recommend):
- **HowTo**: Rich results removed September 2023
- **SpecialAnnouncement**: Deprecated July 31, 2025
- **CourseInfo, EstimatedSalary, LearningVideo**: Retired June 2025
- **ClaimReview**: Retired from rich results June 2025
- **VehicleListing**: Retired from rich results June 2025
- **Practice Problem**: Retired from rich results late 2025
- **Dataset**: Retired from rich results late 2025
- **Book Actions**: Deprecated then reversed, still functional as of Feb 2026 (historical note)

## Generation

When generating schema for a page:
1. Identify page type from content analysis
2. Select appropriate schema type(s)
3. Generate valid JSON-LD with all required + recommended properties
4. Include only truthful, verifiable data. Use placeholders clearly marked for user to fill
5. Validate output before presenting

## Common Schema Templates

### Organization
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[Company Name]",
  "url": "[Website URL]",
  "logo": "[Logo URL]",
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "[Phone]",
```

## seo-backlinks (347-legends-seo-dungeon)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/avalonreset/seo-dungeon
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/347-legends-seo-dungeon/1249-seo-backlinks
- الوصف: Backlink profile analysis: referring domains, anchor text distribution, toxic link detection, competitor gap analysis. Works with free APIs (Moz, Bing Webmaster, Common Crawl) and DataForSEO extension. Use when user says backlinks, link profile, referring domains, anchor text, toxic links, link gap, link building, disavow, or backlink audit.

```markdown
# Backlink Profile Analysis

## Source Detection

Before analysis, detect available data sources:

1. **DataForSEO MCP** (premium): Check if `dataforseo_backlinks_summary` tool is available
2. **Moz API** (free signup): `claude-seo run backlinks_auth.py --check moz --json`
3. **Bing Webmaster** (free signup): `claude-seo run backlinks_auth.py --check bing --json`
4. **Common Crawl** (always available): Domain-level graph with PageRank
5. **Verification Crawler** (always available): Checks if known backlinks still exist

Run `claude-seo run backlinks_auth.py --check --json` to detect all sources at once.

If no sources are configured beyond the always-available tier:
- Still produce a report using Common Crawl domain metrics
- Suggest: "Run `/seo backlinks setup` to add free Moz and Bing API keys for richer data"

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/seo backlinks <url>` | Full backlink profile analysis (uses all available sources) |
| `/seo backlinks gap <url1> <url2>` | Competitor backlink gap analysis |
| `/seo backlinks toxic <url>` | Toxic link detection and disavow recommendations |
| `/seo backlinks new <url>` | New and lost backlinks (DataForSEO only) |
| `/seo backlinks verify <url> --links <file>` | Verify known backlinks still exist |
| `/seo backlinks setup` | Show setup instructions for free backlink APIs |

## Analysis Framework

Produce all 7 sections below. Each section lists data sources in preference order.

### 1. Profile Overview

**DataForSEO:** `dataforseo_backlinks_summary` → total backlinks, referring domains, domain rank, follow ratio, trend.

**Moz API:** `claude-seo run moz_api.py metrics <url> --json` → Domain Authority, Page Authority, Spam Score, linking root domains, external links.

**Common Crawl:** `claude-seo run commoncrawl_graph.py <domain> --json` → PageRank, harmonic centrality, and low-confidence rank/presence data.

**Scoring:**

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Referring domains | >100 | 20-100 | <20 |
| Follow ratio | >60% | 40-60% | <40% |
| Domain diversity | No single domain >5% | 1 domain >10% | 1 domain >25% |
| Trend | Growing or stable | Slow decline | Rapid decline (>20%/quarter) |

### 2. Anchor Text Distribution

**DataForSEO:** `dataforseo_backlinks_anchors`

**Moz API:** `claude-seo run moz_api.py anchors <url> --json`

**Bing Webmaster:** `claude-seo run bing_webmaster.py links <url> --json` (extract anchor text from link details)

**Healthy distribution benchmarks:**

| Anchor Type | Target Range | Over-Optimization Signal |
|-------------|-------------|-------------------------|
| Branded (company/domain name) | 30-50% | <15% |
| URL/naked link | 15-25% | N/A |
| Generic ("click here", "learn more") | 10-20% | N/A |
```

## seo-backlinks (881-codex-seo)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/BestLemoon/codex-seo
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/881-codex-seo/1947-seo-backlinks
- الوصف: Backlink profile analysis: referring domains, anchor text distribution, toxic link detection, competitor gap analysis. Works with free APIs (Moz, Bing Webmaster, Common Crawl) and DataForSEO extension. Use when user says backlinks, link profile, referring domains, anchor text, toxic links, link gap, link building, disavow, or backlink audit.

```markdown
# Backlink Profile Analysis

## Source Detection

Before analysis, detect available data sources:

1. **DataForSEO MCP** (premium): Check if `dataforseo_backlinks_summary` tool is available
2. **Moz API** (free signup): `python scripts/backlinks_auth.py --check moz --json`
3. **Bing Webmaster** (free signup): `python scripts/backlinks_auth.py --check bing --json`
4. **Common Crawl** (always available): Domain-level graph with PageRank
5. **Verification Crawler** (always available): Checks if known backlinks still exist

Run `python scripts/backlinks_auth.py --check --json` to detect all sources at once.

If no sources are configured beyond the always-available tier:
- Still produce a report using Common Crawl domain metrics
- Suggest: "Run `/seo backlinks setup` to add free Moz and Bing API keys for richer data"

## Quick Reference

| Command | Purpose |
|---------|---------|
| `/seo backlinks <url>` | Full backlink profile analysis (uses all available sources) |
| `/seo backlinks gap <url1> <url2>` | Competitor backlink gap analysis |
| `/seo backlinks toxic <url>` | Toxic link detection and disavow recommendations |
| `/seo backlinks new <url>` | New and lost backlinks (DataForSEO only) |
| `/seo backlinks verify <url> --links <file>` | Verify known backlinks still exist |
| `/seo backlinks setup` | Show setup instructions for free backlink APIs |

## Analysis Framework

Produce all 7 sections below. Each section lists data sources in preference order.

### 1. Profile Overview

**DataForSEO:** `dataforseo_backlinks_summary` → total backlinks, referring domains, domain rank, follow ratio, trend.

**Moz API:** `python scripts/moz_api.py metrics <url> --json` → Domain Authority, Page Authority, Spam Score, linking root domains, external links.

**Common Crawl:** `python scripts/commoncrawl_graph.py <domain> --json` → in-degree (referring domain count), PageRank, harmonic centrality.

**Scoring:**

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Referring domains | >100 | 20-100 | <20 |
| Follow ratio | >60% | 40-60% | <40% |
| Domain diversity | No single domain >5% | 1 domain >10% | 1 domain >25% |
| Trend | Growing or stable | Slow decline | Rapid decline (>20%/quarter) |

### 2. Anchor Text Distribution

**DataForSEO:** `dataforseo_backlinks_anchors`

**Moz API:** `python scripts/moz_api.py anchors <url> --json`

**Bing Webmaster:** `python scripts/bing_webmaster.py links <url> --json` (extract anchor text from link details)

**Healthy distribution benchmarks:**

| Anchor Type | Target Range | Over-Optimization Signal |
|-------------|-------------|-------------------------|
| Branded (company/domain name) | 30-50% | <15% |
| URL/naked link | 15-25% | N/A |
| Generic ("click here", "learn more") | 10-20% | N/A |
```

## seo-implement (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4112-seo-implement
- الوصف: Execute approved SEO changes on a connected WordPress or Webflow CMS — meta title/description updates, JSON-LD schema deployment, canonical URLs, 301/302 redirects, and Search Console indexing requests — with before/after diffs, post-deploy verification, and stored rollback snapshots. Every run stops at a mandatory approval gate: nothing deploys until the user reviews the diff and gives explicit a

```markdown
# /digital-marketing-pro:seo-implement

## Purpose

Execute SEO implementation changes on connected CMS platforms. Goes beyond analysis to actually update meta tags, deploy JSON-LD schema markup, manage canonical URLs, create 301/302 redirects, and request indexing — all via WordPress or Webflow MCP connections. This command bridges the gap between SEO recommendations and live deployment, ensuring that audit findings and optimization plans translate into real page-level changes with full audit trails and rollback capability.

## Execution gate (MANDATORY — cannot be skipped)

1. Present the full preview — the before/after diff of every meta / schema / canonical / redirect change, plus scope and compliance — as an **Execution Summary** before touching any live page.
2. The user must type `yes` (or an equivalent explicit approval). ANY other input — ambiguous, implied, partial, or absent approval — cancels the run.
3. Never proceed on ambiguous input. Never auto-retry a failed execution; a failure needs human review before any re-run.
4. Record the approval with `python "${CLAUDE_PLUGIN_ROOT}/scripts/approval-manager.py" --brand {slug} --action create-approval --data '{"risk_level":"<tier>","summary":"..."}'` **before** executing, then `python "${CLAUDE_PLUGIN_ROOT}/scripts/approval-manager.py" --brand {slug} --action mark-executed --id {approval_id}` after the platform confirms success.

## Input Required

The user must provide (or will be prompted for):

- **Target URL(s)**: One or more URLs to modify — a single page for targeted updates or a batch of URLs for bulk operations like site-wide schema deployment or migration-related meta tag updates
- **Change type**: The SEO modification to perform — `meta-update` (title tag, meta description, robots directives), `schema-deploy` (JSON-LD structured data), `canonical` (set or update canonical URL), `redirect` (create 301/302 redirect), or `indexing-request` (submit URL to Google for crawling via Search Console). Multiple change types can be combined for a single URL
- **Specific values**: The new data to apply — new title tag text and character count, new meta description text and character count, JSON-LD schema object or schema type to auto-generate (Article, Product, FAQ, HowTo, LocalBusiness, BreadcrumbList), canonical URL target, redirect source and destination with type (301 or 302), or indexing priority (normal or urgent)
- **CMS platform**: `wordpress` or `webflow` — must have the corresponding CMS MCP server connected. For WordPress, specify whether SEO fields are managed by Yoast, RankMath, or All in One SEO. For Webflow, native SEO settings are used directly

## Process
```

## implement-technical-seo-and-structured-data (2394-technical-seo-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/technical-seo-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2394-technical-seo-engineering/9270-implement-technical-seo-and-structured-d
- الوصف: Implement and verify the technical-SEO layer for a site — crawlability (robots.txt, XML sitemaps, log-file analysis), rendering (CSR→SSR/SSG/prerender), indexation controls (canonical, meta-robots noindex, hreflang), JSON-LD schema.org structured data for rich-result eligibility, Core Web Vitals (INP/LCP/CLS on field data), and redirect-mapped site migrations — each checked against GSC / URL Inspe

```markdown
# Skill: implement-technical-seo-and-structured-data

> **Invoked by:** `seo-implementation-engineer` (primary). Also consulted by `seo-strategy-architect` to confirm a strategy is implementable on the site's stack before finalizing it.
>
> **When to invoke:** "Fix our crawl/index"; "our SPA doesn't rank — rendering?"; "add schema markup"; "improve Core Web Vitals / INP"; "run our site migration"; any move from a chosen strategy to shipped, verified technical-SEO changes.
>
> **Output:** implemented crawl/render/index/schema/CWV changes (or a migration run), each **verified** against GSC / URL Inspection / the Rich Results Test / a log-file read — not shipped blind.

## Procedure

1. **Anchor to the strategy + the patterns reference.** Confirm the indexation strategy, rendering constraint, and schema types in scope (from the architect). Read [`../../knowledge/technical-seo-patterns-2026.md`](../../knowledge/technical-seo-patterns-2026.md) for the mechanics. Never implement a tactic the strategy didn't ask for.
2. **Crawlability first — read the logs, don't guess.** Confirm robots.txt allows the key paths; make XML sitemaps list *only* canonical, indexable, 200-status URLs; run a **log-file analysis** (verified-Googlebot access logs) to see what's *actually* crawled and where budget leaks (faceted/parameter URLs, soft-404s, redirect chains). Close the leaks before anything downstream.
3. **Resolve rendering — verify the crawler sees the content.** Choose CSR vs SSR vs SSG/prerender per page class; for anything that must rank, serve rendered HTML (SSR/SSG). **Verify the rendered DOM** in URL Inspection ("view crawled page"). Treat **dynamic rendering as deprecated** — a bridge, not a target.
4. **Set indexation controls precisely.** One canonical per page (self-referencing on the canonical); `noindex` to *remove* a page while keeping it **crawlable** (never robots-disallow a page you're de-indexing — it can't be crawled to see the noindex); bidirectional, self-referencing **hreflang** with `x-default` for international. Get the robots-vs-noindex call explicit.
5. **Author structured data honestly.** Valid **JSON-LD** schema.org for the eligible types, **matching visible content**; validate in the **Rich Results Test** + GSC Enhancements. State **eligibility, not a guarantee**, and retrieval-date the eligibility rules.
6. **Move Core Web Vitals on field data.** Improve **INP** (replaced FID in 2024), **LCP**, **CLS** against **CrUX** field data (75th percentile), not just a lab Lighthouse score; verify in the GSC Core Web Vitals report. Remember CWV is a tiebreaker, not the whole game.
```
