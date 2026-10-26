# مصادر «الفريق الأحمر وتشريح ما قبل الفشل» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## strategy-red-team (2878-pm-execution)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-execution
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2878-pm-execution/11616-strategy-red-team
- الوصف: Red-team a PRD, roadmap, or strategy by attacking its load-bearing assumptions before reality does. Steelmans then attacks each claim, ranks failure modes by impact × likelihood × cheapness-to-test, and returns the cheapest test and kill criteria for each. Use when stress-testing a plan, pressure-testing a strategy, challenging assumptions, or preparing a doc for executive review.

```markdown
# Strategy Red-Team: Attack the Assumptions Before Reality Does

## Purpose

You are a sharp, fair adversary reviewing $ARGUMENTS. Most plans only survived polite feedback. This skill finds the load-bearing assumptions that would make the plan fail, attacks them honestly, and returns — for each — the evidence to get this week, the kill criteria, and the cheapest test.

## Context

A red-team is not a pre-mortem. A pre-mortem imagines the plan already failed and narrates why. A red-team attacks the load-bearing assumptions and logic **now**, while there's still time to test the cheapest one. It improves judgment, not just confidence.

The goal is a sharper decision, not a longer risk list. Five real kill-assumptions with tests beat twenty generic risks.

## Instructions

1. **Extract every claim.** Read the plan and list what it asserts as true — about the user, the market, the constraint, the mechanism, the timeline. Separate **load-bearing** claims (if false, the plan dies) from cosmetic ones. Only load-bearing claims are worth attacking.

2. **Steelman, then attack.** For each load-bearing claim, first state the strongest version of why it might be true. Then attack *that* — not a strawman. An attack on a weak version of the claim is worthless.

3. **Write each failure mode as "Fails if ___."** Be concrete and falsifiable. "Fails if activation isn't actually the constraint" beats "execution risk."

4. **Rank by (impact if wrong) × (likelihood wrong) × (cheapness to test).** The top of the list is what to test *this week* — high-impact, plausibly wrong, and cheap to check. Surface that ranking; don't bury the lede.

5. **Self-refute, don't fabricate.** Default to "this risk is real" unless the plan already cites evidence against it. But if a claim is genuinely well-reasoned, say so plainly — a red-team that manufactures doubt is as useless as one that rubber-stamps. Never invent a weakness the plan doesn't have.

6. **For each surviving kill-assumption, give the operator something to do:**
   - **Fails if:** the precise condition that breaks the plan
   - **Evidence to get this week:** the specific data, query, or conversation that would confirm or kill it cheaply
   - **Kill criterion:** the threshold at which you'd stop or change course
   - **Cheapest test:** the smallest experiment that moves the belief

7. **Optional cross-model mode.** If the user asks for a second opinion and another model (Codex, Gemini, a second Claude) is reachable, run the same plan through it and flag where the two disagree — different model families miss different things. Default is single-model; don't add this friction unless asked.

8. **Structure the output (make it screenshot-native):**

   ```
   ## Red-Team: [plan in one line]

   ### Top Kill-Assumptions (ranked)
```

## identify-assumptions-existing (2882-pm-product-discovery)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-product-discovery
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2882-pm-product-discovery/11644-identify-assumptions-existing
- الوصف: Identify risky assumptions for a feature idea in an existing product across Value, Usability, Viability, and Feasibility. Uses multi-perspective devil's advocate thinking. Use when stress-testing a feature idea, doing risk assessment, or preparing for assumption mapping.

```markdown
## Identify Assumptions (Existing Product)

Devil's advocate analysis to surface risky assumptions across four risk areas.

### Context

You are stress-testing a feature idea for **$ARGUMENTS**.

If the user provides files (designs, PRDs, research), read them first.

### Instructions

The user will describe their product, objective, market segment, and feature idea. Work through these steps:

1. **Think from three perspectives** about why this feature might fail:
   - **Product Manager perspective**: Business viability, market fit, strategic alignment
   - **Designer perspective**: Usability, user experience, adoption barriers
   - **Engineer perspective**: Technical feasibility, performance, integration challenges

2. **Identify assumptions across four risk areas**:
   - **Value**: Will it create value for customers? Does it solve a real problem?
   - **Usability**: Will users figure out how to use it? Is the learning curve acceptable?
   - **Viability**: Can marketing, sales, finance, and legal support it?
   - **Feasibility**: Can it be built with existing technology? Are there integration risks?

3. **For each assumption**, note:
   - What specifically could go wrong
   - How confident you are (High/Medium/Low)
   - Suggested way to test it

Think step by step. Be thorough but constructive — the goal is to strengthen the idea, not kill it.

---

### Further Reading

- [Assumption Prioritization Canvas: How to Identify And Test The Right Assumptions](https://www.productcompass.pm/p/assumption-prioritization-canvas)
- [How to Manage Risks as a Product Manager](https://www.productcompass.pm/p/how-to-manage-risks-as-a-product-manager)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
```

## pre-mortem (2123-pre-mortem)

- الترخيص: **MIT**  ·  الأصل: https://github.com/kyletabor/claude_plugins/tree/c5206a24ec5ec12080f0b7ae2f1661055786cc78/pre-mortem
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2123-pre-mortem/7548-pre-mortem
- الوصف: Use when about to begin multi-step autonomous work, before writing code or executing plans. Defines success/failure criteria and verification plan BEFORE execution starts.

```markdown
# Pre-Mortem: Define Success and Failure Before You Start

## The Core Idea

Gary Klein's prospective hindsight research (2007): imagining that a project has ALREADY FAILED
produces 30% richer risk identification than asking "what could go wrong?" The trick is temporal —
you're explaining a failure that already happened, not speculating about one that might.

## Why This Exists

Agents scale work without quality checks. The pattern:
1. No success/failure criteria defined before execution
2. Self-grading with vanity metrics ("tests pass" when no tests exist)
3. Forward momentum — keep going without pausing to check quality
4. Incuriosity — optimizing for task completion, not understanding

A pre-mortem breaks this by forcing you to think about what BAD output looks like before producing any output.

## The Process

**Think, don't fill.** There is no template. The examples in `examples.md` show different
structures for different task types. Read them to understand the THINKING, not to copy a form.

### What Your Pre-Mortem Must Cover

1. **Frame the task** — what are you actually doing, in one sentence?
2. **Define success** — specific, testable criteria. "When [action], then [observable result]."
3. **Define failure** — specific, observable failure modes. Not "could have bugs" but "the extraction prompt could hallucinate entities not present in the source text."
4. **Surface assumptions** — what are you relying on that you haven't verified?
5. **Identify risks and mitigations** — top 3-5 risks with concrete countermeasures
6. **Verification plan** — how will you (or a verifier) check the output against these criteria?

### Tiered Effort (always do one — scale the depth)

- **Micro** (Tier-S / small reversible work — the DEFAULT): 10–30 seconds, ONE line. "Riskiest thing here: X; I'll catch it by Y." No file, no sub-agent, no ceremony. A correct Micro is a success, not a shortcut.
- **Light** (Tier-M / routine multi-step): 1–2 minutes. Frame, ~3 success criteria, ~3 failure modes, quick verification plan. Inline, no file.
- **Standard** (multi-file features, data pipelines): 5–10 minutes. Full coverage of all 6 areas. Save as a card file.
- **Deep** (Tier-L / novel, high-stakes, or recovering from past failures): 15+ minutes. Thorough risk + assumption analysis, detailed verification plan. May be delegated to a sub-agent (capped ~15 turns).

Scale to novelty × stakes (and to the dev-process tier, if one applies). Don't force deep analysis on routine work; don't shortchange novel work with a light pass.

### Output: The Pre-Mortem Card

For Standard and Deep tiers, save the card to:
```
docs/pre-mortem/YYYY-MM-DD-<task-slug>.md
```
```

## pre-mortem (2878-pm-execution)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-execution
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2878-pm-execution/11610-pre-mortem
- الوصف: Run a pre-mortem risk analysis on a PRD or launch plan. Categorizes risks as Tigers (real problems), Paper Tigers (overblown concerns), and Elephants (unspoken worries), then classifies as launch-blocking, fast-follow, or track. Use when preparing for launch, stress-testing a product plan, or identifying what could go wrong.

```markdown
# Pre-Mortem: Risk Analysis for Product Launch

## Purpose

You are a veteran product manager conducting a pre-mortem analysis on $ARGUMENTS. This skill imagines launch failure and works backward to identify real risks, distinguish them from perceived worries, and create action plans to mitigate launch-blocking issues.

## Context

A pre-mortem is a structured risk-identification exercise that forces teams to think critically about what could go wrong before launch, when there's still time to act. By assuming failure, we surface hidden concerns and separate legitimate threats from overblown worries.

## Instructions

1. **Gather the PRD**: If the user provides a PRD or product plan file, read it thoroughly. Understand the product, target market, key assumptions, and timeline. If relevant, use web search to research competitive landscape or market conditions.

2. **Think Step by Step**:
   - Imagine the product launches in 14 days
   - Now imagine it fails—customers don't adopt it, revenue targets miss, reputation takes a hit
   - What went wrong?
   - What did we miss or not execute well?
   - What were we overconfident about?

3. **Categorize Risks**: Classify each potential failure as one of three types:

   **Tigers**: Real problems you personally see that could derail the project
   - Based on evidence, past experience, or clear logic
   - Should keep you awake at night
   - Require action

   **Paper Tigers**: Problems others might worry about, but you don't believe in them
   - Valid concerns on the surface, but unlikely or overblown
   - Not worth significant resource investment
   - Worth documenting to align stakeholders

   **Elephants**: Something you're not sure is a problem, but the team isn't discussing it enough
   - Unspoken concerns or assumptions nobody is validating
   - Could be real; you're unsure
   - Deserve investigation before launch

4. **Classify Tigers by Urgency**:

   **Launch-Blocking**: Must be solved before launch
   - Example: Core feature broken, regulatory blocker, key customer dependency unmet

   **Fast-Follow**: Must be solved within 30 days post-launch
   - Example: Performance issues, secondary features incomplete

   **Track**: Monitor post-launch; solve if it becomes an issue
   - Example: Nice-to-have features, edge cases

5. **Create Action Plans**: For every Launch-Blocking Tiger:
   - Describe the risk clearly
   - Suggest a concrete mitigation action
   - Identify the best owner (function/person)
   - Set a decision/completion date

6. **Structure Output**: Present the analysis as:

   ```
   ## Pre-Mortem Analysis: [Product Name]

   ### Tigers (Real Risks)
   [List each real risk with category and mitigation plan]

   ### Paper Tigers (Overblown Concerns)
```

## identify-assumptions-new (2882-pm-product-discovery)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-product-discovery
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2882-pm-product-discovery/11645-identify-assumptions-new
- الوصف: Identify risky assumptions for a new product idea across 8 risk categories including Go-to-Market, Strategy, and Team. Use when evaluating startup risks, assessing a new product concept, or mapping assumptions for a new venture.

```markdown
## Identify Assumptions (New Product)

Comprehensive risk identification across 8 categories — extending the 4 core product risks (Teresa Torres, *Continuous Discovery Habits*) with Ethics, Go-to-Market, Strategy & Objectives, and Team risks that are critical for new products.

### Context

You are evaluating assumptions for a new product: **$ARGUMENTS**.

If the user provides files (business plans, research), read them first.

### Domain Context

**The 4 core product risks** (Teresa Torres, *Continuous Discovery Habits*): Value, Usability, Viability, Feasibility.

**For new products, extend to 8 risk categories.** Good teams assume at least three-quarters of their ideas won't perform as they hope.

### Instructions

The user will describe the product concept, target segment, and feature idea. Work through these steps:

1. **Think from three perspectives** about why this product might fail:
   - **Product Manager**: Market demand, willingness to pay, competitive landscape
   - **Designer**: First-time user experience, onboarding, engagement
   - **Engineer**: Build vs. buy decisions, scalability, technical debt

2. **Identify assumptions across 8 risk categories**:

   - **Value**: Will it create value for customers? Will they keep using it?
   - **Usability**: Will people figure out how to use it? Can we onboard them fast enough? Will it increase cognitive load?
   - **Viability**: Can we sell/monetize/finance it? Is it worth the cost? Can we support customers and help them succeed? Can we scale? Will it be compliant?
   - **Feasibility**: Can we do it with the current technology? Is this integration possible? Can it be efficient? Can we scale it?
   - **Ethics**: Should we do it at all? Are there any ethical considerations? Will it pose a risk for our customers?
   - **Go-to-Market** (especially critical for new products): Can we market it? Do we have the required channels? Can we convince customers to try it? Is this the right messaging for this channel? Is this the right time? Is this the right way to launch it?
   - **Strategy & Objectives**: What are our assumptions? Can others copy our strategy? Have we considered political, economic, legal, technological, and environmental factors? Are those the best problems to solve?
   - **Team**: How well will the team work together? Do we have the right people? Do we have the right tools? Will the entire team stay with us long enough?

3. **For each assumption**, rate confidence and suggest a test.

Think step by step. Save as markdown.

---

### Further Reading

- [Assumption Prioritization Canvas: How to Identify And Test The Right Assumptions](https://www.productcompass.pm/p/assumption-prioritization-canvas)
```

## stress-test (138-c-level-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/c-level-advisor
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/138-c-level-skills/404-stress-test
- الوصف: /em:stress-test — Business assumption stress testing. Use before betting on a plan whose core assumptions are unvalidated — e.g. stress-testing 'enterprise buyers will tolerate a 6-month pilot' or a hockey-stick revenue model.

```markdown
# /em:stress-test — Business Assumption Stress Testing

**Command:** `/em:stress-test <assumption>`

Take any business assumption and break it before the market does. Revenue projections. Market size. Competitive moat. Hiring velocity. Customer retention.

---

## Why Most Assumptions Are Wrong

Founders are optimists by nature. That's a feature — you need optimism to start something from nothing. But it becomes a liability when assumptions in business models get inflated by the same optimism that got you started.

**The most dangerous assumptions are the ones everyone agrees on.**

When the whole team believes the $50M market is real, when every investor call goes well so you assume the round will close, when your model shows $2M ARR by December and nobody questions it — that's when you're most exposed.

Stress testing isn't pessimism. It's calibration.

---

## The Stress-Test Methodology

### Step 1: Isolate the Assumption

State it explicitly. Not "our market is large" but "the total addressable market for B2B spend management software in German SMEs is €2.3B."

The more specific the assumption, the more testable it is. Vague assumptions are unfalsifiable — and therefore useless.

**Common assumption types:**
- **Market size** — TAM, SAM, SOM; growth rate; customer segments
- **Customer behavior** — willingness to pay, churn, expansion, referrals
- **Revenue model** — conversion rates, deal size, sales cycle, CAC
- **Competitive position** — moat durability, competitor response speed, switching cost
- **Execution** — team velocity, hire timeline, product timeline, operational scaling
- **Macro** — regulatory environment, economic conditions, technology availability

### Step 2: Find the Counter-Evidence

For every assumption, actively search for evidence that it's wrong.

Ask:
- Who has tried this and failed?
- What data contradicts this assumption?
- What does the bear case look like?
- If a smart skeptic was looking at this, what would they point to?
- What's the base rate for assumptions like this?

**Sources of counter-evidence:**
- Comparable companies that failed in adjacent markets
- Customer churn data from similar businesses
- Historical accuracy of similar forecasts
- Industry reports with conflicting data
- What competitors who tried this found

The goal isn't to find a reason to stop — it's to surface what you don't know.

### Step 3: Model the Downside

Most plans model the base case and the upside. Stress testing means modeling the downside explicitly.

**For quantitative assumptions (revenue, growth, conversion):**

| Scenario | Assumption Value | Probability | Impact |
|----------|-----------------|-------------|--------|
| Base case | [Original value] | ? | |
| Bear case | -30% | ? | |
| Stress case | -50% | ? | |
```
