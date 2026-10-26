# مصادر «الإعلان الإبداعي 30 ثانية» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## launch-ad-campaign (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4062-launch-ad-campaign
- الوصف: Create and launch a paid ad campaign on Google, Meta, LinkedIn, or TikTok through the connected ad-platform MCP — campaign structure, audience targeting, bid strategy, negative targeting, creative quality scoring, compliance review, and a post-launch monitoring schedule. A mandatory execution gate shows the full spend summary and requires an explicit typed yes before anything goes live; budgets ov

```markdown
# /digital-marketing-pro:launch-ad-campaign

## Purpose

Create and launch a paid advertising campaign on the specified ad platform with proper campaign structure, audience targeting, bid strategy, budget controls, and compliance checks. Includes mandatory budget safeguards that require explicit re-confirmation when spend exceeds brand thresholds, and sets up post-launch monitoring to catch early performance issues before budget is wasted on underperforming configurations.

## Execution gate (MANDATORY — cannot be skipped)

1. Present the full preview — recipients / spend / changes / compliance — as an **Execution Summary** before touching any live system.
2. The user must type `yes` (or an equivalent explicit approval). ANY other input — ambiguous, implied, partial, or absent approval — cancels the run.
3. Never proceed on ambiguous input. Never auto-retry a failed execution; a failure needs human review before any re-run.
4. Record the approval with `python "${CLAUDE_PLUGIN_ROOT}/scripts/approval-manager.py" --brand {slug} --action create-approval --data '{"risk_level":"<tier>","summary":"..."}'` **before** executing, then `python "${CLAUDE_PLUGIN_ROOT}/scripts/approval-manager.py" --brand {slug} --action mark-executed --id {approval_id}` after the platform confirms success.

## Input Required

The user must provide (or will be prompted for):

- **Ad platform**: Where to launch — Google Ads, Meta Ads, LinkedIn Ads, or TikTok Ads — must have the corresponding MCP server connected
- **Campaign objective**: Primary goal — awareness (reach/impressions), consideration (traffic/engagement/video views), or conversion (leads/sales/app installs/ROAS target)
- **Budget**: Daily budget or lifetime budget with currency and any maximum CPC or CPA caps the brand requires
- **Campaign dates**: Start date, end date, and any dayparting or ad scheduling preferences (hours of day, days of week)
- **Audience targeting**: Demographics (age, gender, income), interests, behaviors, custom audiences (email lists, website visitors), lookalike or similar audiences, and retargeting segments — with geographic and language targeting
- **Ad creative**: Headlines (multiple variants for responsive ads), descriptions, images or video assets, display URLs, final URLs, and sitelink extensions or callout assets where applicable
- **Bid strategy preference**: Manual CPC, maximize conversions, target CPA, target ROAS, maximize clicks, or platform-recommended — with any bid caps, floors, or portfolio bid strategy settings
- **Conversion tracking**: Which conversion events to optimize for, pixel or tag installation status, conversion value assignment, and attribution window preference (7-day click, 1-day view, etc.)
```

## ad-creative (192-marketing-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/marketing-skill
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/192-marketing-skills/570-ad-creative
- الوصف: When the user needs to generate, iterate, or scale ad creative for paid advertising. Use when they say 'write ad copy,' 'generate headlines,' 'create ad variations,' 'bulk creative,' 'iterate on ads,' 'ad copy validation,' 'RSA headlines,' 'Meta ad copy,' 'LinkedIn ad,' or 'creative testing.' This is pure creative production — distinct from paid-ads (campaign strategy). Use ad-creative when you ne

```markdown
# Ad Creative

You are a performance creative director who has written thousands of ads. You know what converts, what gets rejected, and what looks like it should work but doesn't. Your goal is to produce ad copy that passes platform review, stops the scroll, and drives action — at scale.

## Before Starting

**Check for context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

Gather this context (ask if not provided):

### 1. Product & Offer
- What are you advertising? Be specific — product, feature, free trial, lead magnet?
- What's the core value prop in one sentence?
- What does the customer get and how fast?

### 2. Audience
- Who are you writing for? Job title, pain point, moment in their day
- What do they already believe? What objections will they have?

### 3. Platform & Stage
- Which platform(s)? (Google, Meta, LinkedIn, Twitter/X, TikTok)
- Funnel stage? (Awareness / Consideration / Decision)
- Any existing copy to iterate from, or starting fresh?

### 4. Performance Data (if iterating)
- What's currently running? Share current copy.
- Which ads are winning? CTR, CVR, CPA?
- What have you already tested?

---

## How This Skill Works

### Mode 1: Generate from Scratch
Starting with nothing. Build a complete creative set from brief to ready-to-upload copy.

**Workflow:**
1. Extract the core message — what changes in the customer's life?
2. Map to funnel stage → select creative framework
3. Generate 5–10 headlines per formula type
4. Write body copy per platform (respecting character limits)
5. Apply quality checks before handing off

### Mode 2: Iterate from Performance Data
You have something running. Now make it better.

**Workflow:**
1. Audit current copy — what angle is each ad taking?
2. Identify the winning pattern (hook type, offer framing, emotional appeal)
3. Double down: 3–5 variations on the winning theme
4. Open new angles: 2–3 tests in unexplored territory
5. Validate all against platform specs and quality score

### Mode 3: Scale Variations
You have a winning creative. Now multiply it for testing or for multiple audiences/platforms.

**Workflow:**
1. Lock the core message
2. Vary one element at a time: hook, social proof, CTA, format
3. Adapt across platforms (reformat without rewriting from scratch)
4. Produce a creative matrix: rows = angles, columns = platforms

---

## Platform Specs Quick Reference

| Platform | Format | Headline Limit | Body Copy Limit | Notes |
|----------|--------|---------------|-----------------|-------|
| Google RSA | Search | 30 chars (×15) | 90 chars (×4 descriptions) | Max 3 pinned |
| Google Display | Display | 30 chars (×5) | 90 chars (×5) | Also needs 5 images |
```

## paid-advertising (1520-digital-marketing-pro)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/indranilbanerjee/digital-marketing-pro
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1520-digital-marketing-pro/4082-paid-advertising
- الوصف: Plan, structure, and audit paid media campaigns across Google, Meta, LinkedIn, TikTok, Microsoft, programmatic, retail media, native, and audio — campaign hierarchy, audience architecture, bid strategy, budget allocation and pacing, creative strategy, and current platform API changes (Google Ads v24/v25, Meta v25). Produces campaign plans, platform audit scorecards, budget models, creative briefs,

```markdown
# Paid Advertising

## Recent platform API changes (as of July 2026)

Target **Google Ads API v24.2** for stable integrations (v24 line supported into 2027). **v25 (July 2026) is the new major release with breaking changes**: the legacy `CustomerLifecycleGoal`/`CampaignLifecycleGoal` resources are removed (migrate to the unified `Goal` + `CampaignGoalConfig` schema), plus new loyalty-retention optimization goals, social-engagement metrics for Shorts ads, duration-level breakdowns for non-skippable YouTube inventory, and YouTube third-party conversion attribution. Adopt v25 deliberately, not by default. Full detail — including AI Max — lives in [`google-ads.md`](google-ads.md), the single source for the Google Ads API surface. Sources: [release notes](https://developers.google.com/google-ads/api/docs/release-notes) · [v25 announcement](https://ads-developers.googleblog.com/2026/07/announcing-v25-of-google-ads-api.html).

**Meta (Marketing API v25, in effect):** standalone Advantage+ Shopping / App campaigns can no longer be created via the API on any version (since 19 May 2026); v26 (Sept 2026) pauses remaining ones — use the unified Advantage+ setup ([details in meta-ads.md](meta-ads.md)). The new **Page Viewer metric** replaces legacy reach (Post/Page Reach, Video Impressions, and Story Impressions retire from the Graph API) — update any reporting that reads those fields. **LinkedIn:** version `202607` is live (monthly cadence); it adds an automatic "Not Interested" CTA on Message Ads and a `SHA256_IP_ADDRESS` identifier in the Conversions API.

**Highlights that affect campaign construction:**

- **v24.2 (24 Jun 2026):** first-class **Local Services Ads** support (`AssetGroup.google_local_services_info`), landing-page-text auto-generation (`AssetAutomationType.GENERATE_LANDING_PAGE_TEXT`), and a beta Multi-Party Auth review resource for regulated verticals (finance, health, political).
- **v24.1 (13 May 2026) — AI Max:** four new experiment types (`ADOPT_AI_MAX`, `ADOPT_BROAD_MATCH_KEYWORDS`, `OPTIMIZE_ASSETS`, `PMAX_REPLACEMENT_SHOPPING`). **Run an `ADOPT_AI_MAX` experiment before any AI Max rollout** — it gives statistically-clean lift numbers vs the baseline. Also adds `mobile_device_platform` (iOS vs Android) reporting segmentation.
- **v24.0 (22 Apr 2026) — breaking:** `videos` + `logo_images` now REQUIRED on `DemandGenVideoResponsiveAdInfo`/`VideoResponsiveAdInfo` (and `business_name` on the latter); `Campaign.video_brand_safety_suitability` REMOVED (moved to the Customer level); `CallAd`/`CallAdInfo` fully removed (use Call Assets).
```

## codex-hook-wire-schema-from-binary (3302-codex-hook-wire-schema-from-binary)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/codex-hook-wire-schema-from-binary
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3302-codex-hook-wire-schema-from-binary/13816-codex-hook-wire-schema-from-binary
- الوصف: Read the Codex CLI hook contract straight out of the shipped native binary with `strings` instead of probing it with a live turn: the `PreToolUse` payload fields, the output envelope, the `permissionDecision` values the host accepts and the ones it refuses by name, the plugin environment variables, and the hook-trust gate. Use when: (1) you need Codex's hook stdin payload field names and `codex --

```markdown
> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/codex-hook-wire-schema-from-binary/SKILL.md`). Updates go through
> the repo's worktree + PR workflow — open an issue, branch, PR.

## Problem

Codex CLI documents its hooks thinly. `codex --help` exposes no `hooks`
subcommand, and `~/.codex/hooks.json` on a real machine is usually written by
a third-party wrapper (cmux), so it shows what that wrapper wired -- not what
Codex supports. The obvious next move, a live probe turn with a stub hook, is
slow and fails for reasons unrelated to hooks (provider unreachable, auth,
network-gated router), producing no evidence either way.

Meanwhile the entire contract is compiled into the shipped binary: the wire
structs, the JSON Schema, and -- most usefully -- the literal validation error
strings that name every value the host rejects.

A prior session looked in `@openai/codex/bin/`, found only `codex.js`, and
concluded no native binary existed. The binary is real; it is two
`node_modules` levels deeper in a platform-specific package.

## Context / Trigger Conditions

Invoke when:

- You need Codex's `PreToolUse` (or any hook) stdin payload field names.
- You need to know which `permissionDecision` values Codex honors before
  writing a hook that returns one.
- A live Codex probe hangs, times out, or never reaches a tool call, and you
  need the contract anyway.
- Someone reports "Codex has no native binary to inspect" -- they looked in
  the wrong directory.
- You are porting a Claude Code hook to Codex and need to know what differs.

Do NOT invoke when:

- The question is runtime behavior rather than contract, e.g. "does deny
  actually stop execution under `approval_policy = \"never\"`". Strings cannot
  answer that; only a live turn can.

## Solution

### 1. Find the binary

The `bin/codex` on `PATH` is a JS shim. The native executable lives in the
platform package nested under it:

```
$(dirname $(readlink -f $(which codex)))/../node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/bin/codex
```

Locate it without guessing the platform triple:

```bash
find "$(dirname "$(readlink -f "$(which codex)")")/.." \
     -path '*vendor*/bin/codex' -type f 2>/dev/null
```

It is large (~205 MB for 0.148.0), which is why `strings` finds so much.

### 2. Pull the hook contract

```bash
CX=<path from step 1>

# Payload fields and decision vocabulary live in one adjacent run of strings
strings -n 4 "$CX" | grep -F 'PreToolUseHookSpecificOutputWire'

# The authoritative part: what the host REFUSES, stated literally
strings -n 20 "$CX" | grep -F 'PreToolUse hook returned'
```

The rejection strings are the contract. They name unsupported values
explicitly, so there is no inference step.
```

## test-a-commit-blocking-hook (3369-test-a-commit-blocking-hook)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/test-a-commit-blocking-hook
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3369-test-a-commit-blocking-hook/13884-test-a-commit-blocking-hook
- الوصف: Verify a pre-commit hook that is supposed to REFUSE commits, without destroying the hook while testing it. Use when: (1) you just wrote a pre-commit hook and need to prove it blocks and allows the right things, (2) a hook you wrote reports "nothing changed" during a commit even though files are obviously staged, (3) you ran `git reset --hard HEAD~1` to undo a test commit and lost real work that wa

```markdown
> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/test-a-commit-blocking-hook/SKILL.md`). Updates go through the
> repo's worktree + PR workflow.

# Testing a commit-blocking hook

## Problem

A pre-commit hook whose whole job is to **refuse** a commit can only be tested
by attempting a commit. That creates two traps that bite in sequence, and the
second one destroys work.

## Trigger conditions

- You wrote a `pre-commit` hook and want to prove it blocks the bad case and
  allows the good one.
- Your hook runs a script that reports "no files changed" while files are
  plainly staged.
- You ran `git reset --hard HEAD~1` to clean up a test commit and the hook, the
  script, or the CI workflow vanished with it.

## Trap 1: a commit-range diff is empty in pre-commit

The natural way to ask "what changed?" is a commit range:

```sh
git diff --name-only "$BASE...HEAD"
```

In a `pre-commit` hook that returns **nothing**. The change is in the index; it
has not been committed, so it is not in any range ending at `HEAD`. The hook
runs, the script reports no changes, the check passes, and the commit you meant
to block goes through. The hook appears installed and does nothing.

Read the index instead:

```sh
git diff --cached --name-only          # which paths are staged
git show ":path/to/file"               # the staged blob's content
```

Give the script an explicit mode rather than guessing:

```sh
# in .githooks/pre-commit
python3 "$(git rev-parse --show-toplevel)/scripts/check.py" --staged
```

`--staged` compares the index against `HEAD`. The same script keeps its normal
range mode for CI, where the change genuinely is committed.

## Trap 2: cleaning up the test destroys the tooling

Sequence that loses work, and it looks completely reasonable at each step:

1. Write the hook, the script and the CI workflow. They are untracked.
2. Make a throwaway edit to trip the hook.
3. `git add -A` — this stages the throwaway edit **and all the new tooling**.
4. Commit. The hook lets it through (trap 1) or you bypass it to test something
   else.
5. `git reset --hard HEAD~1` to undo the test commit.
6. The tooling is gone. It only ever existed in that commit.

`git add -A` during a test is the actual error. The reset is just where the
cost lands.

## Solution: commit the tooling first, then test with throwaway files only

**Commit the guard before testing it.** A version-bump guard, a secret
scanner, a lint gate: the tooling commit itself usually does not trip its own
rule, so it lands cleanly.

```sh
git add scripts/check.py .githooks/pre-commit .github/workflows/checks.yml
git commit -m "ci: add the guard"      # safe: touches nothing the guard checks
```
```

## commercial-policy (147-commercial-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/commercial
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/147-commercial-skills/477-commercial-policy
- الوصف: Use when designing or revising a company's commercial policy — the rules of engagement governing discounts off list price, approver thresholds, exception flows, and the deal framework that Deal Desk and AEs operate under. Covers discount matrix design (ARR band x term length x payment terms x strategic value), commercial policy design, exception policy, discount governance, approval thresholds, de

```markdown
# commercial-policy

## Purpose

Design the **rules of engagement** that govern discounting off list price — the artifact that Deal Desk and AEs operate under. Three deterministic tools:

1. `discount_matrix_builder.py` — builds a 4-dimensional matrix (ARR band × term length × payment terms × strategic value tier), each cell carrying an approved discount band backed by current win-rate + NRR data, plus an approver tier (AE / Manager / Director / VP / CFO).
2. `exception_router.py` — when an asks-for-discount lands outside the matrix, routes it through the named approver chain, attaches required compensating commitments (multi-year prepay + named expansion path + reference commitment + MSA tightening), produces machine-readable audit-trail metadata, and flags precedent risk if 3+ similar exceptions have landed in the trailing quarter.
3. `policy_linter.py` — lints the matrix for governance defects: approver inversion, band inversion, margin-floor violation, coverage gaps, cliff edges, undefined strategic tiers, inconsistent margin floors, thin data backing.

The output is the **policy itself** (matrix + exception flow + lint report), not a per-deal application of it.

## When to use

- A new Head of Commercial or Head of Deal Desk is writing the company's first formal commercial policy
- The existing matrix is older than 6 months and discount drift is showing in margin reviews
- Reps are citing "Maria approved 28% on Acme last quarter" as precedent and you need to break the precedent loop
- Q-over-Q exception count is rising and you suspect the matrix bands are mispriced
- CFO has tightened the margin floor and the matrix needs to be rebuilt against the new constraint
- A board / exec is asking "why do we discount this much?" and you need a data-backed defensible policy

**Do NOT use this skill to:**
- Approve a specific deal — that's `commercial/skills/deal-desk`
- Set the pricing model + list price — that's `commercial/skills/pricing-strategist`
- Author a proposal / SOW / MSA prose — that's `business-growth/contract-and-proposal-writer`
- Make the strategic "when do we hire a VP Sales" call — that's `c-level-advisor/cro-advisor`

## Workflow

1. **Audit current discount distribution.** Pull the last 4 quarters of closed-won + closed-lost deals from CRM. Fill `assets/policy_design_template.md` (~20 minutes). Capture: `arr`, `discount_pct`, `term_months`, `payment_terms_days`, `strategic_value`, `win_lost`, `nrr_12mo` per deal.
```
