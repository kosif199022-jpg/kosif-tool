# مصادر «بحث السوق والمنافسين» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## competitor-analysis (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4005-competitor-analysis
- الوصف: Run a multi-dimensional competitive teardown of 2-5 competitors — content strategy, SEO, paid ads, social, AI answer-engine visibility, and pricing/positioning — producing a competitor overview matrix, per-competitor SWOT, gap analysis, and strategic recommendations prioritized by opportunity size. Triggers on \"/digital-marketing-pro:competitor-analysis\", \"analyze our competitors\", \"how do we

```markdown
# /digital-marketing-pro:competitor-analysis

## Purpose

Deliver a comprehensive competitive intelligence report across all major marketing dimensions. Identify competitor strengths, weaknesses, strategies, and gaps the brand can exploit.

## Input Required

The user must provide (or will be prompted for):

- **Competitors**: 2-5 competitor names and/or URLs
- **Analysis scope**: Full analysis or specific dimensions (SEO, content, ads, social, pricing)
- **Key battleground keywords**: Terms where the brand competes head-to-head
- **Industry/category**: For contextual benchmarking

## Process

1. **Load brand context**: Read `~/.claude-marketing/brands/_active-brand.json` for the active slug, then load `~/.claude-marketing/brands/{slug}/profile.json`. Apply brand voice, compliance rules for target markets (`skills/context-engine/compliance-rules.md`), and industry context. **Also check for guidelines** at `~/.claude-marketing/brands/{slug}/guidelines/_manifest.json` — if present, load restrictions and relevant category files. Check for custom templates at `~/.claude-marketing/brands/{slug}/templates/`. Check for agency SOPs at `~/.claude-marketing/sops/`. If no brand exists, ask: "Set up a brand first (/digital-marketing-pro:brand-setup)?" — or proceed with defaults.
2. **Content analysis**: Content types, publishing frequency, top-performing content, content gaps, topic authority
3. **SEO analysis**: Domain authority, keyword overlap, ranking gaps, backlink comparison, technical health
4. **Paid advertising**: Ad copy themes, landing page strategies, estimated spend, platform focus
5. **Social media**: Platform presence, follower growth, engagement rates, content mix, posting cadence
6. **AI visibility**: How competitors appear in AI answer engines versus the brand
7. **Pricing and positioning**: Pricing models, value proposition, messaging frameworks, market positioning
8. Synthesize findings into strategic opportunities and threats
9. Generate actionable recommendations for competitive advantage

## Output

A structured competitive analysis containing:

- Competitor overview matrix with key metrics per competitor
- Content strategy comparison with gap analysis
- SEO competitive landscape with keyword and link opportunities
- Paid media intelligence with creative and targeting insights
- Social media benchmarking with engagement analysis
- AI visibility comparison across platforms
- Pricing and positioning map
- SWOT summary per competitor
- Strategic recommendations prioritized by opportunity size

## Agents Used

- **competitive-intel** — All competitive dimensions, benchmarking, gap analysis, and strategic recommendations
```

## competitor-analysis (2880-pm-market-research)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-market-research
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2880-pm-market-research/11627-competitor-analysis
- الوصف: Analyze competitors with strengths, weaknesses, and differentiation opportunities. Identifies direct competitors and maps the competitive landscape. Use when doing competitive research, preparing a competitive brief, or finding differentiation opportunities.

```markdown
# Competitor Analysis

## Purpose
Conduct a comprehensive competitive analysis to understand the landscape, identify 5 direct competitors, and uncover differentiation opportunities. This skill maps competitive positioning, synthesizes competitor strengths and weaknesses, and highlights opportunities for strategic differentiation.

## Instructions

You are a strategic product analyst and competitive intelligence expert specializing in competitive positioning and market landscape mapping.

### Input
Your task is to analyze the competitive landscape for **$ARGUMENTS** in the **[market/industry segment]** (if specified).

Conduct web research to identify direct competitors. If the user provides market research, competitor data, pricing sheets, feature comparisons, or customer feedback about competitors, read and analyze them directly. Synthesize data into a comprehensive competitive view.

### Analysis Steps (Think Step by Step)

1. **Market Scoping**: Define the market, industry, and addressable customer base for $ARGUMENTS
2. **Competitor Identification**: Use web search to identify 5 primary direct competitors
3. **Competitive Intelligence**: Research each competitor's positioning, features, pricing, go-to-market strategy
4. **Strengths & Weaknesses**: Assess competitor capabilities, limitations, and market positioning
5. **Differentiation Mapping**: Identify gaps, overlaps, and opportunities for $ARGUMENTS to differentiate
6. **Strategic Synthesis**: Develop insights about competitive dynamics and future threats

### Output Structure

**Market Overview & Definition**
- Market size and growth trends
- Primary customer segments and use cases
- Key success factors in this market
- Market dynamics and competitive intensity

**Competitive Set Summary**
- 5 primary direct competitors identified
- Market positions: leaders, challengers, niche players
- Estimated market share or positioning
- Notable adjacent or indirect competitors

For each of the 5 competitors:

**Competitor Profile**
- Company name, founding date, funding/status
- Primary market focus and customer segments served
- Estimated market share or customer base size
- Market positioning and go-to-market strategy

**Core Product Strengths**
- Key features and capabilities
- Unique competitive advantages
- Customer value proposition
- Technology differentiation or moats
- Customer satisfaction and retention signals

**Product Weaknesses & Gaps**
- Missing features or use cases
- Known limitations or pain points for customers
- Technical or operational weaknesses
- Market positioning gaps
- Customer dissatisfaction areas

**Business Model & Pricing**
- Pricing structure (per-seat, per-usage, flat-fee, freemium, etc.)
- Price point(s) in market
- Go-to-market channels and sales motion
```

## swot-analysis (2883-pm-product-strategy)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-product-strategy
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2883-pm-product-strategy/11662-swot-analysis
- الوصف: Perform a detailed SWOT analysis — strengths, weaknesses, opportunities, and threats with actionable recommendations. Use when doing strategic assessment, competitive analysis, or evaluating a product or business position.

```markdown
# SWOT Analysis

## Metadata
- **Name**: swot-analysis
- **Description**: Perform a detailed SWOT analysis for a product. Identifies strengths, weaknesses, opportunities, and threats with actionable recommendations.
- **Triggers**: SWOT analysis, strengths weaknesses, SWOT matrix, strategic assessment

## Instructions

You are a strategic analyst conducting a SWOT analysis for $ARGUMENTS.

Your task is to thoroughly evaluate the internal and external factors that will impact product success and competitive positioning.

## Input Requirements
- Product description and current state
- Competitive landscape and market context
- Company capabilities, resources, and constraints
- Market trends and industry dynamics
- Customer feedback or usage data (optional)

## SWOT Analysis Framework

### 1. Strengths (Internal, Positive)
What internal capabilities and advantages do we have?

- Unique capabilities or expertise
- Brand recognition or reputation
- Customer relationships and loyalty
- Technology or IP advantages
- Cost advantages or operational efficiency
- Team talent and experience
- Existing customer base or distribution

### 2. Weaknesses (Internal, Negative)
What internal limitations or gaps do we have?

- Resource constraints (budget, team size, skills)
- Technology or infrastructure limitations
- Lack of brand awareness or market presence
- Weak customer relationships or high churn
- High cost structure relative to competitors
- Outdated processes or legacy systems
- Dependence on key people or partners

### 3. Opportunities (External, Positive)
What external trends or market dynamics could we leverage?

- Growing market segments or customer needs
- Technological advances enabling new solutions
- Regulatory changes favoring our approach
- Competitor weaknesses or market gaps
- Partnership or acquisition opportunities
- Expansion into adjacent markets or segments
- Shifting customer preferences or behaviors

### 4. Threats (External, Negative)
What external factors could negatively impact us?

- Emerging or stronger competitors
- Changing customer preferences or needs
- Technological disruption or obsolescence
- Regulatory changes or compliance risks
- Economic downturns or market contraction
- Supply chain disruptions
- Supplier or partner consolidation

## Output Process
1. Identify 5-7 strengths (be honest about competitive advantages)
2. List 5-7 weaknesses (avoid minimizing; focus on addressable gaps)
3. Map 5-7 opportunities (prioritize by market size and alignment)
4. Flag 5-7 threats (assess probability and impact)
5. Cross-reference analysis for strategic insights:
   - How do we leverage strengths to capture opportunities?
   - How do we shore up weaknesses to mitigate threats?
   - Which opportunities can overcome weaknesses?
```

## competitive-positioning-analysis (2385-staffing-operations)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/staffing-operations
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2385-staffing-operations/9228-competitive-positioning-analysis
- الوصف: Build a segment-by-segment competitive-positioning analysis for a staffing firm — placing it on a players-by-segment grid, naming where it wins and where scale competitors lead, with a source on every claim. Reach for this when the question is where the firm is strong vs. losing in the competitive set.

```markdown
# Skill: Competitive-positioning analysis

"Are we competitive?" has no single answer — only a per-segment one. A firm strong in allied health can be a rounding error in travel nursing. This skill builds the honest, segment-resolved picture.

## Step 1 — Name the segments in scope
Don't average across them (§3 #9). For a dual-segment firm: healthcare-travel, locum, allied, per-diem; education-special-ed/therapy, teletherapy, substitutes. Score competitiveness *within* each.

## Step 2 — Place the firm and competitors on the grid
Use the players-by-segment map in [`../../knowledge/competitor-landscape.md`](../../knowledge/competitor-landscape.md). For each segment, list who leads and roughly how big (SIA-anchored). For a Soliant-shaped firm, note that only Amergis, Cross Country, Supplemental Health Care, and Sunbelt share the dual-segment shape.

## Step 3 — Identify the firm's structural advantages
What does its shape give it? (e.g., dual-segment breadth, allied + school-therapy depth, all-50-state reach, a compliance certification like Joint Commission since 2011). Tie each to a segment where it converts to a win.

## Step 4 — Name where competitors lead, by lane
Be specific and current: travel-nurse scale (Aya/AMN/Medical Solutions), locums (CHG ~31% share/Jackson), teletherapy *software* (Presence/eLuma — software-native vs. a service line), substitutes at scale (ESS/Kelly), therapy roll-up (TSSG), public-market capital (AMN/CCRN/Kelly). Don't claim a strength the firm doesn't have.

## Step 5 — Keep the facts current
Verify before asserting: Soliant's parent is **Vistria** (not Adecco); the **Aya–Cross Country merger was terminated** (Dec 2025) so both remain independent. A stale ownership or M&A fact in front of an operator is a credibility hit (§3 #9).

## Step 6 — Translate to a "where to play" recommendation
For each segment: defend (a strength under attack), invest (a winnable gap), or cede (a scale game not worth entering — e.g., a non-substitute firm shouldn't chase ESS/Kelly on subs). Make the recommendation, don't just describe the map.

## Step 7 — Source every claim
Every size, rank, and ownership fact gets a URL + retrieval date; aggregator estimates are marked `[ESTIMATE]`/`[unverified]`. SIA's full ranked list is paywalled — note where a figure is from the free editorial vs. secondary press.

## Output
Use [`../../templates/competitive-landscape-brief.md`](../../templates/competitive-landscape-brief.md). For the trend context behind the positioning, pair with [`trend-analysis-readout`](../trend-analysis-readout/SKILL.md).
```

## competitor-positioning (2666-nimble)

- الترخيص: **MIT**  ·  الأصل: https://github.com/nimbleway/agent-skills/tree/2890fdf94f0adfae79bf05b4de3c91667701bafb
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2666-nimble/10152-competitor-positioning
- الوصف: Tracks how competitors position themselves online — scrapes homepages, features, pricing, and blogs to extract messaging, value props, CTAs, and pricing models. Compares against previous snapshots to surface positioning shifts with before/after tracking. Produces messaging matrices, content gap analysis, white space maps, and battlecard inputs.

```markdown
# Competitor Positioning

Marketing-focused competitive positioning analysis powered by Nimble's web data APIs.
Built for marketing teams who need to understand how competitors present themselves —
messaging, value props, content themes, pricing — and how that evolves over time.

The output is a **marketing briefing**, not a signal feed. Every insight should answer:
"what does this mean for our messaging and positioning?"

User request: $ARGUMENTS

**Argument parsing** — determine what to do before running anything:
- No arguments → run full workflow (scope confirmation in Step 2)
- Competitor names (e.g., "Exa, Tavily") → research only those, skip scope confirmation
- "battlecard [competitor]" → skip to Battlecard Generation (see below) using
  existing snapshots from memory
- "delta" / "what changed" → force delta mode regardless of timing

**Before running any commands**, read `references/nimble-playbook.md` for Claude Code
constraints (no shell state, no `&`/`wait`, sub-agent permissions, communication style).

---

## Instructions

### Step 0: Preflight

Follow the transport selection + standard preflight from `references/nimble-playbook.md` — pick CLI or MCP at session start, then run the standard preflight calls (date calc, today, profile, memory index) in parallel.

From the results:
- CLI missing or API key unset → `references/profile-and-onboarding.md`, stop
- Tag all `nimble` CLI calls: `nimble --client-source nimble-agent-skills <subcommand>`. MCP requests are attributed at the transport level — see `references/nimble-playbook.md`.
- Profile exists → load prior data from two sources:
  - `~/.nimble/memory/positioning/*.md` — prior positioning snapshots (used for
    delta detection in Steps 4 + 5)
  - `~/.nimble/memory/competitors/*.md` — business signals from competitor-intel
    runs (provides context for *why* positioning may have shifted, e.g., a funding
    round or leadership change that preceded a messaging pivot)
  Determine mode:
  - **Full snapshot:** first run OR no prior positioning data OR last run > 14 days ago
  - **Delta mode:** last run < 14 days ago — only surface what changed
  - **Same-day repeat:** if `last_runs.competitor-positioning` is today, check for
    existing report at `~/.nimble/memory/reports/competitor-positioning-[today].md`.
    If found, ask: "Already ran today. Run again for fresh data?" Don't silently re-run.
  - Skip to Step 2
- No profile → Step 1

### Step 1: First-Run Onboarding (2 prompts max)

This skill shares the competitor list from `competitor-intel`. If a profile already
exists with competitors, skip onboarding entirely.

If no profile exists, follow `references/profile-and-onboarding.md` for the full
onboarding flow. The profile and competitor list created here will be shared across
```

## competitor-analysis (3620-zoominfo)

- الترخيص: **MIT**  ·  الأصل: https://github.com/zoominfo/zoominfo-mcp-plugin/tree/d07402feb2b9967ccc118f55bacd41a79c822d6a
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3620-zoominfo/14670-competitor-analysis
- الوصف: Produce a fact-led competitive intel brief on one or more competitors — firmographics, recent strategic moves, product positioning, ICP overlap, and discovery questions. Defaults to your configured competitors from GTM context if none specified. Combines ZoomInfo data (account_research, scoops, intent, exec teams, similar companies) with web search for product/pricing/customer-sentiment intelligen

```markdown
# Competitor Analysis

Produce a fact-led competitive intel brief. Lead with an executive comparison across competitors, then a per-competitor section. Pull positioning verbatim from the GTM context — don't invent your own opinions about who wins or who's the biggest threat.

## Input

The user will provide via `$ARGUMENTS`:

- **Competitor identifiers (optional)** — zero or more of:
  - **Preferred**: ZoomInfo account/company IDs (numeric). Use directly as `companyId`; skip the search step for that competitor.
  - **Fallback**: competitor names. Resolve via `search_companies` (use `companyWebsite` from GTM context's `url` field if present; otherwise `companyName`).
  - If omitted entirely, default to all competitors configured in your GTM context.
  - For named competitors NOT in GTM context, flag as "uncovered" — research proceeds, but pre-built positioning is missing.
- **Research context (strongly recommended)** — a free-form description of *why* this brief is being pulled and what decision it supports. Richer is better — flat depth enums and deal one-liners produce flat briefs. Capture as much as is true: the deal or situation in play, what you're losing or winning on, the offering or product line under pressure, the audience for the brief (AE prep / leadership review / enablement), how exhaustive the analysis needs to be, and any specific angles or hypotheses to test. Examples:
  - *"Losing the mid-market segment to Clay on data orchestration. Need to understand their recent product moves, pricing, and where their customer reviews show cracks. AE-facing — concrete discovery questions matter most."*
  - *"Quarterly competitive review for leadership. All configured competitors. Want a scannable Executive Comparison plus 90-day strategic moves. Depth on each is light."*
  - *"Deep dive on Acme before a head-to-head bake-off next month. Their security platform vs ours. Want G2/TrustRadius sentiment themes, recent CISO commentary, and the exact products they'd field against our SKUs."*

This context drives depth allocation (deep vs scan), the `account_research` query framing, scoops/news triage, web-search angles, and the discovery-question slant.

## Workflow

Parallelize aggressively — once each competitor's company ID is resolved, all per-competitor calls can fan out in parallel. When briefing multiple competitors, run all competitors' fan-outs in the same parallel batch.

1. **Anchor on purpose.** Read the research context from `$ARGUMENTS`.
   - If supplied, restate it in 1-2 sentences as the *brief purpose* and keep it as the framing lens for every downstream step.
```
