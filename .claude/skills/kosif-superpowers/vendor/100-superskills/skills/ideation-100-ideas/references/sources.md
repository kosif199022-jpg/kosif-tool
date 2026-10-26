# مصادر «مولّد الأفكار: 100 فكرة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## brainstorm-ideas-existing (2882-pm-product-discovery)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-product-discovery
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2882-pm-product-discovery/11642-brainstorm-ideas-existing
- الوصف: Brainstorm product ideas for an existing product using multi-perspective ideation from PM, Designer, and Engineer viewpoints. Use when generating new feature ideas, brainstorming solutions for an identified opportunity, or ideating with a product trio.

```markdown
## Brainstorm Product Ideas (Existing Product)

Multi-perspective ideation for continuous product discovery. Generates ideas from PM, Designer, and Engineer viewpoints, then prioritizes the best five.

### Context

You are supporting a product trio performing continuous product discovery for **$ARGUMENTS**.

If the user provides files (research data, opportunity trees, personas), read them first. If they mention a product URL, use web search to understand the product.

### Domain Context

**Product Trio** (Teresa Torres, *Continuous Discovery Habits*): PM + Designer + Engineer collaborate on discovery together. "Best ideas often come from engineers." Discovery is not linear — loop back if experiments fail. Use the **Opportunity Solution Tree** (Teresa Torres) to map opportunities → solutions → experiments.

### Instructions

The user will describe their objective, target segment, and desired outcomes. Work through these steps:

1. **Understand the opportunity**: Confirm the product, objective, market segment, and desired outcomes. Ask for clarification if anything is ambiguous.

2. **Ideate from three perspectives** — generate 5 ideas each from:
   - **Product Manager**: Focus on business value, strategic alignment, and customer impact
   - **Product Designer**: Focus on user experience, usability, and delight
   - **Software Engineer**: Focus on technical possibilities, data leverage, and scalable solutions

3. **Prioritize the top 5 ideas** across all perspectives based on:
   - Strategic alignment with the stated objective
   - Potential impact on desired outcomes
   - Feasibility and effort required
   - Differentiation from existing solutions

4. **For each prioritized idea**, provide:
   - A clear name and one-sentence description
   - Why it was selected (reasoning)
   - Key assumptions to validate

Think step by step. Present ideas in a clear, structured format.

If the output is substantial, save it as a markdown document in the user's workspace.

---

### Further Reading

- [What Is Product Discovery? The Ultimate Guide Step-by-Step](https://www.productcompass.pm/p/what-exactly-is-product-discovery)
- [Product Trio: Beyond the Obvious](https://www.productcompass.pm/p/product-trio)
- [The Extended Opportunity Solution Tree](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)
- [Product Model First Principles: Product Discovery, Product Delivery, and Product Culture In Depth](https://www.productcompass.pm/p/product-model-first-principles-discovery-deliver)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
```

## brainstorm-ideas-new (2882-pm-product-discovery)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-product-discovery
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2882-pm-product-discovery/11643-brainstorm-ideas-new
- الوصف: Brainstorm feature ideas for a new product in initial discovery from PM, Designer, and Engineer perspectives. Use when starting product discovery for a new product, exploring features for a startup idea, or doing initial ideation.

```markdown
## Brainstorm Product Ideas (New Product)

Multi-perspective ideation for initial product discovery of a new product. Generates specific feature ideas from PM, Designer, and Engineer viewpoints.

### Context

You are supporting initial product discovery for a new product: **$ARGUMENTS**.

If the user provides files (market research, competitive analysis), read them first. Use web search to understand the market if needed.

### Domain Context

**Initial Discovery vs Continuous Discovery**: Initial Discovery focuses on vision, business model, and market validation — you're testing whether the product should exist. Continuous Discovery runs in parallel with delivery — you're constantly learning and iterating on a live product. This skill is for **initial discovery**.

### Instructions

The user will describe their target segment, opportunity, and desired outcomes. Work through these steps:

1. **Understand the opportunity**: Confirm the product concept, target market segment, and what the users want to achieve.

2. **Ideate from three perspectives** — generate 5 specific feature ideas each from:
   - **Product Manager**: Focus on market fit, value creation, and competitive advantage
   - **Product Designer**: Focus on user experience, onboarding, and engagement
   - **Software Engineer**: Focus on technical innovation, API integrations, and platform capabilities

3. **Prioritize the top 5 ideas** across all perspectives. For a new product, weight heavily toward:
   - Core value delivery (does it solve the primary problem?)
   - Speed to validate (can we test this quickly?)
   - Differentiation potential

4. **For each prioritized idea**, provide reasoning and key assumptions to test.

Think step by step. Save substantial output as a markdown document.

---

### Further Reading

- [Startup Canvas: Product Strategy and a Business Model for a New Product](https://www.productcompass.pm/p/startup-canvas)
- [Product Innovation Masterclass](https://www.productcompass.pm/p/product-innovation-masterclass) (video course)
- [Continuous Product Discovery Masterclass (CPDM)](https://www.productcompass.pm/p/cpdm) (video course)
```

## brainstorm (3228-brainstorm)

- الترخيص: **MIT**  ·  الأصل: https://github.com/umputun/cc-thingz/tree/fb520ca89c606f806408ca56874d8895fe9b83b3/plugins/brainstorm
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3228-brainstorm/13641-brainstorm
- الوصف: Use before any creative work or significant changes. Activates on "brainstorm", "let's brainstorm", "deep analysis", "analyze this feature", "think through", "help me design", "explore options for", or when user asks for thorough analysis of changes, features, or architectural decisions. Guides collaborative dialogue to turn ideas into designs through one-at-a-time questions, approach exploration,

```markdown
# Brainstorm

Turn ideas into designs through collaborative dialogue before implementation.

## custom rules loading

before starting, run this command via Bash tool to check for user-provided custom rules:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/resolve-rules.sh brainstorm-rules.md ${CLAUDE_PLUGIN_DATA}
```

if the output is non-empty, treat it as additional instructions that supplement (not replace) the built-in rules below. apply custom rules alongside the skill's own instructions throughout the brainstorm process — they may influence design preferences, naming conventions, technology choices, or other aspects of the brainstorm session. custom rules content is guidance for the brainstorm dialogue, not content to embed verbatim in the output.

### rules management

when the user asks to add, show, or clear custom brainstorm rules, handle these operations:

- **show rules**: run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/resolve-rules.sh brainstorm-rules.md ${CLAUDE_PLUGIN_DATA}` and display the output. if the output is empty, tell the user no custom rules are configured at either level. otherwise, to determine the source, check if `.claude/brainstorm-rules.md` exists and is non-empty (project-level) — if not, the output came from user-level. tell the user which level it came from.
- **add/update project rules**: write content to `.claude/brainstorm-rules.md` in the current working directory.
- **add/update user rules**: first check if `$CLAUDE_PLUGIN_DATA` is set (run `echo "$CLAUDE_PLUGIN_DATA"`). if empty, tell the user that user-level rules require the plugin to be installed from the marketplace and offer project-level instead. if set, write content to `$CLAUDE_PLUGIN_DATA/brainstorm-rules.md`.
- **clear project rules**: delete `.claude/brainstorm-rules.md`.
- **clear user rules**: if `$CLAUDE_PLUGIN_DATA` is set, delete `$CLAUDE_PLUGIN_DATA/brainstorm-rules.md`. if not set, tell the user user-level rules are not available.

project-level rules (`.claude/brainstorm-rules.md`) take precedence over user-level rules (`$CLAUDE_PLUGIN_DATA/brainstorm-rules.md`). when both non-empty files exist, only project-level rules are loaded. empty files are treated as absent and fall through to the next level. see `${CLAUDE_PLUGIN_ROOT}/references/custom-rules.md` for full documentation on the rules mechanism.

**CRITICAL: this skill must NEVER modify its own files (skills, scripts, references, hooks, plugin.json). the ONLY files it may create or modify for rules management are `.claude/brainstorm-rules.md` and `$CLAUDE_PLUGIN_DATA/brainstorm-rules.md`. if the user asks to change the skill's behavior, suggest creating a plan — do not edit skill files directly.**

## Process

### Phase 1: Understand the Idea
```

## brainstorm (1397-brainstorm)

- الترخيص: **MIT**  ·  الأصل: https://github.com/falconiere/toolu/tree/3e245327ad55d0a080c985ed67bfea98b3aeee03/plugins/brainstorm
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1397-brainstorm/3333-brainstorm
- الوصف: Use to think a change through before building — scope, evidence, alternatives, trade-offs, and a recommended approach — without editing code. Triggers on "brainstorm", "think through", "design options", "how should we approach", "trade-offs". delivery-flow runs it as phase 1.

```markdown
# Brainstorm

Choose the smallest amount of design work that removes material uncertainty.
Default-and-proceed is the baseline: do not turn routine work into an interview.

## Modes

- **Standalone** — the user invoked this skill directly. Work through the
  procedure, post the capsule, and suggest the next step (for example
  `/delivery-flow:delivery-flow` or `$delivery-flow:delivery-flow` to build it).
  Standalone brainstorm never edits code, commits, or starts delivery; the user
  decides what happens next.
- **Delivery** — delivery-flow invoked this skill as its first phase. Record the
  outcome, evidence, risks, and decisions, then hand off to `spec` in the same
  turn without waiting for confirmation.

## Triage

- **Minimal** — mechanical work with no design decision: record the requested
  outcome, existing convention, and direct check before proceeding.
- **Compact** — bounded work with a material default or a small compatibility
  risk. Produce a concise capsule, then continue.
- **Full** — use only for cross-cutting work, a public interface,
  persistence-or-migration, security-privacy, external-cost, or an unclear goal.
  Evaluate only relevant axes from
  [design-questions.md](references/design-questions.md) and compare only
  genuinely distinct alternatives.

## Evidence and decisions

Start with memory recall, one targeted structural or exact-text search, then
inspect the best hits. Reuse demonstrated repository conventions when they
settle the choice. Outside a repository, say "no repository evidence" and work
from the request. Delegate only when the search needs a broad map, on a
read-only exploration tier; keep the final trade-off decision in the main
thread on the most capable tier.

When Jev is installed, call it to compare concrete alternatives against the
user's stated preferences before deciding. When it is unavailable, say so once
and decide from explicit evidence. Jev informs the choice; it never replaces the
agent's own feasibility and architecture judgment.

Set material defaults and proceed. Ask one structured question (2–3 options)
only when prompt and repository evidence cannot settle a
goal-defining or hard-to-reverse fork. If several forks qualify, ask about the
highest-blast-radius decision and record defaults and risks for the rest. Use
the host's structured-choice tool: `AskUserQuestion` in Claude Code,
`request_user_input` in Codex when available; otherwise ask one concise plain
question.

## Capsule

- **Outcome:** the intended, observable result.
- **Material defaults/non-goal:** the chosen boundary and what stays out.
- **Repository evidence:** the recalled decision or best matching hit.
- **Risk:** the remaining compatibility, behavior, or delivery risk.
```

## positioning-ideas (2881-pm-marketing-growth)

- الترخيص: **MIT**  ·  الأصل: https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0/pm-marketing-growth
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2881-pm-marketing-growth/11636-positioning-ideas
- الوصف: Brainstorm product positioning ideas differentiated from competitors. Identifies top competitors and generates positioning statements with rationale. Use when developing product positioning, differentiating from competitors, or crafting brand positioning strategy.

```markdown
# Positioning Ideas

Brainstorm product positioning ideas differentiated from competitors. Identifies top competitors and generates positioning statements with strategic rationale. Use when developing product positioning, differentiating from competitors, or crafting brand positioning strategy.

## When to Use

- Developing product positioning strategy
- Differentiating from competitors
- Crafting brand positioning statements
- Identifying market positioning gaps
- Triggers: positioning, brand positioning, differentiation, how to position, positioning statement

## Prompt

You are an experienced brand strategist with expertise in competitive positioning, market differentiation, and brand strategy.

Given the following product and market context: $ARGUMENTS

Follow these steps:

**Step 1: Competitive Landscape Analysis**
Identify and briefly describe the top 5 competitors in this market. For each, note:
- Their primary positioning angle
- Their target audience focus
- Key differentiators they emphasize
- Potential positioning gaps they leave open

**Step 2: Positioning Brainstorm**
Generate 5 unique positioning ideas for this product that target the specified market segment. Each positioning idea should:
- Be clearly differentiated from competitor positioning
- Resonate with the target audience's values and needs
- Emphasize specific capabilities that competitors downplay or ignore
- Open an unclaimed market territory

**Step 3: Positioning Statements**
For each idea, provide:

1. **Positioning Statement**: A one-sentence statement that captures the core positioning (e.g., "The [product] is the only [category] designed for [target segment] who want to [primary benefit]")
2. **Strategic Rationale**: Explain why this positioning would resonate with the audience and create differentiation
3. **Supporting Message**: Key supporting messages that reinforce this positioning
4. **Competitive Advantage**: What specific advantages enable this positioning claim

## Tips for Best Results

- Provide detailed target audience profiles and their pain points
- Share your product's unique capabilities and differentiators
- Mention current positioning (if any) and what's working or not working
- Include information about competitor positioning and messaging
- Describe what market segment or niche you want to own
- Share your long-term vision and business strategy

---

### Further Reading

- [Product Management vs. Product Marketing vs. Product Growth 101](https://www.productcompass.pm/p/product-management-vs-product-marketing)
- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)
```

## ce-brainstorm (1391-compound-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/EveryInc/compound-engineering-plugin/tree/9af474a/
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1391-compound-engineering/3280-ce-brainstorm
- الوصف: Explore vague or ambitious ideas into a right-sized requirements-only unified plan. Use when the user wants to brainstorm or scope what to build. Not for executing already-specified work. Use ce-pov for a verdict on adopting a named external technology.

```markdown
# Brainstorm a Feature or Improvement

Brainstorming answers **WHAT** to build through dialogue; `ce-plan` then enriches the same unified plan artifact with **HOW**. This skill does not implement code. **The current year is 2026**, for dating the artifact.

**Outcome:** a result sized to the work that `ce-plan` can build on without inventing product behavior, scope boundaries, or success criteria: a chat paragraph for Lightweight work, or a requirements-only unified plan under `<root>/plans/` when a file is earned.

**Done, on the brainstorm path:** that artifact is written and passes the Ready for Planning Check — or no file was written because the dialogue produced no decision that a later reader (the planner, a reviewer, or a future reader) needs recorded under a stable ID and the user asked for none — and Phase 4's handoff has been presented.

**Lightweight work ends in chat.** Phase 0.3 classifies the tier from the request and bounded inline reads before anything is dispatched; when the tier is uncertain, take the heavier one. Lightweight work — small, well-bounded, low ambiguity — ends in a chat paragraph with no file, no grounding scout, no approach generation, and no claim verifier. A file is earned only by a decision that a later reader needs recorded under a stable ID, or by the user asking for one.

**Stop and route instead** in three cases, decided by `references/phase-0.md`, not from memory. Each ends the run its own way, so the done condition above does not apply: non-software work, where `references/universal-brainstorming.md` replaces Phases 0.2–4; a verdict question about a named external candidate, where you offer the `ce-pov` handoff; and neither — quick help, a factual question, a single-step task — answered directly.

The feature description is what the invocation carries, whether the user wrote it or a calling skill passed it. If none came, ask the user what they want to explore and do not proceed until you have one.

**`mode:return-to-caller`** (a leading token a calling skill such as `lfg` sets): strip it, run the dialogue unchanged, and replace Phase 4 with the structured return `references/handoff.md` defines: no menu, no `lfg` or `ce-plan` invocation.


## Artifact Root

Resolve `<root>` the first time you compose or read a `<root>/` path, never earlier; a scratch-only or no-repo run that touches none skips this entirely.

**Resolve the CE artifact root `<root>` before composing any artifact path.**

- **Read** `docs_root` from `<repo-root>/.compound-engineering/config.yaml` only (`<repo-root>` = `git rev-parse --show-toplevel`). Do not read it from `config.local.yaml`. Unset -> `<root>` is `docs`, exactly as before.
```
