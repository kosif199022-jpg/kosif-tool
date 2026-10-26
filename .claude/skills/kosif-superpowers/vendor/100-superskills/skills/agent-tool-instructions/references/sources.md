# مصادر «تعليمات الوكلاء والأدوات» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## agent-host-skill-loading (3261-agent-host-skill-loading)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/agent-host-skill-loading
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3261-agent-host-skill-loading/13772-agent-host-skill-loading
- الوصف: Make a non-Claude, non-Codex agent load skillz-format `SKILL.md` files, so procedures written once reach every agent you run instead of being restated per host. Covers the two-stage disclosure that keeps the standing prompt small (menu line in the system prompt, full body behind a `load_skill` tool), the measured cost of each alternative, frontmatter parsing that survives block scalars, ordered-pa

```markdown
> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/agent-host-skill-loading/SKILL.md`). Updates go through the repo's
> worktree + PR workflow — open an issue, branch, PR.

# agent-host-skill-loading

## Problem

A skill catalog targets specific hosts. Claude Code and Codex read
`skills/<name>/SKILL.md` natively; anything else you run — a Slack agent, a
cron worker, your own tool-calling loop — cannot. The knowledge exists, and the
agent standing in the channel with you does not have it. You end up restating
the same procedure in that agent's prompt, where it drifts from the catalog
copy.

Adding a third host is mostly a delivery question, not a parsing one. The
parsing is twenty lines. The decision that matters is **how much of the catalog
sits in the standing prompt**, because a system prompt is paid on every turn, by
every model in a fallback chain, forever.

## Format contract

A skill is a directory holding `SKILL.md`:

    ---
    name: some-skill
    description: |
      One or more sentences. Often long — written for a host that injects
      the whole thing.
    ---

    # some-skill
    ...body...

Two parsing points that bite:

- **Use a YAML parser, not a regex.** Descriptions routinely use block scalars
  (`description: |`) and run to several hundred characters over many lines. A
  `^description:\s*(.*)$` regex silently captures the empty string after the
  pipe, and you get a catalog of nameless menu entries that the model cannot
  match against anything.
- **Split on the frontmatter fence, then parse only the fence.** `text.split("---", 2)`
  gives you `["", frontmatter, body]`; feeding the whole file to the YAML parser
  fails the moment a body contains a `:` in prose, which is always.

Fall back to the directory name when `name:` is missing, and skip a file whose
frontmatter will not parse rather than failing the whole scan — one malformed
skill in a catalog of forty should not cost you the other thirty-nine.

## The delivery decision

Three options, and the cost of each is measurable before you build it. Numbers
below are from a 44-skill catalog; scale linearly.

| Approach | Standing cost | Failure mode |
|---|---|---|
| Full descriptions inline (what Claude Code does) | ~25 KB | Every turn, every fallback model, pays for 44 skills to use zero or one |
| Nothing in prompt, `find_skill(query)` tool only | 0 | Never invoked — **a model cannot search for what it does not know exists** |
| Menu line per skill + `load_skill(name)` tool | ~7 KB | None material; costs one extra tool round-trip on the turns that use a skill |

The third is the one to build. Concretely:

1. **The menu** — one line per skill in the system prompt: name plus the
```

## setup-mcp-agent-analytics (2874-setup-mcp-agent-analytics)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pendo-io/claude-pendo-plugin/tree/340d503c23eed487be83693aa4c1837df4a7dcd4/plugins/setup-mcp-agent-analytics
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2874-setup-mcp-agent-analytics/11589-setup-mcp-agent-analytics
- الوصف: Instrument an MCP server with Pendo MCP analytics in Python, TypeScript, or Go. Detects which language/SDK the server is built with and wires up the matching Pendo integration — PendoMCPServer (Python), initMcp() (TypeScript), or gosdk.Instrument() (Go) — then verifies data is flowing to Pendo Agent Analytics. Use this whenever the user wants Pendo analytics on an MCP server, mentions "MCP analyti

```markdown
# Set up Pendo MCP Analytics

Instrument an MCP server so tool calls, user intent, and client info flow to
Pendo Agent Analytics. The guiding contract, set by product: **a customer
installing for MCP analytics gets ONLY MCP analytics** — never silently
instrument their other LLM/agent code. This applies identically across all
three SDKs below.

There are three SDKs, one per language — your first job is to detect which
one applies.

---

## Phase 0: Identify the SDK (Python, TypeScript, or Go)

Look at the project for the MCP framework in use:

| Signal | SDK |
|--------|-----|
| `pyproject.toml` / `requirements.txt` with `mcp`; `Server(` from `mcp.server.lowlevel` or `FastMCP(` from `mcp.server.fastmcp` | **Python** — `pendo-server-sdk` (pip, `[mcp]` extra) |
| `package.json` with `@modelcontextprotocol/sdk`; `new McpServer(` or `new Server(` | **TypeScript** — `pendo-server-sdk` (npm) |
| `go.mod` with `github.com/modelcontextprotocol/go-sdk` (or another Go MCP framework, e.g. `mark3labs/mcp-go`) | **Go** — `github.com/pendo-io/go-sdk` |

If several MCP servers exist (possibly in different languages, e.g. a
monorepo), confirm which to instrument — each gets its own agent ID. State
the detected language in one line ("I'll use the **TypeScript SDK** — this
is an `@modelcontextprotocol/sdk` server") and confirm before proceeding,
unless the user already named the language or only one server is present.

Then jump to the matching section below: **[Python](#python-pendo-server-sdk)**,
**[TypeScript](#typescript-pendo-server-sdk)**, or **[Go](#go-github-compendo-iogo-sdk)**.

---

## Phase 1: Collect the required values (all languages)

Ask, don't guess:

- **API key** — the Pendo application API key (the key in
  `POST /data/agenticsdk/<api_key>`). Called `api_key` / `apiKey` / `APIKey`
  / the app's **Public App ID** depending on SDK.
- **Agent ID** — the Agent Analytics agent this data routes to; the user
  creates it in the Pendo UI first (Product → Agent Analytics → settings
  icon next to the agent name).
- **Endpoint** — only for non-US-prod (EU / dev stacks). All three SDKs
  default to `https://app.pendo.io`, sending to
  `<endpoint>/data/agenticsdk/<api_key>`.

If the user wants the wiring validated before they've gathered real values,
wire it with obvious placeholders (e.g. `api_key="test-api-key"`) to prove
the code runs and the schema/event shape is correct, then swap in the real
values once supplied for an end-to-end check — two clearly separated passes,
not two rounds of guessing.

---

## Python (`pendo-server-sdk`)

### Find the MCP server

Look for the `mcp` package (`modelcontextprotocol` Python SDK): `Server(`
from `mcp.server.lowlevel` (low-level) or `FastMCP(` from `mcp.server.fastmcp`
```

## agent-skill-init (1215-agent-skill-init)

- الترخيص: **MIT**  ·  الأصل: https://github.com/dashed/claude-marketplace/tree/f6a24dbc08da57aeb80e7423da2508457d0b3398/plugins/agent-skill-init
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1215-agent-skill-init/2897-agent-skill-init
- الوصف: Create a repo-local Agent Skill following the open agentskills.io specification. Use when the user wants to create, scaffold, or initialize a new skill in the current repo, mentions a 'repo-local skill' or the agentskills.io spec, or needs a spec-compliant SKILL.md placed under .agents/skills/ (or .claude/skills/). Scaffolds the directory, writes valid name/description frontmatter, and validates w

```markdown
# Agent Skill Init

## Overview

Scaffold a single, spec-compliant Agent Skill into the current repository — fast.
A skill is just a directory containing a `SKILL.md` (required) plus optional
`scripts/`, `references/`, and `assets/`. This skill walks you from intent to a
validated skill folder, following the open [agentskills.io](https://agentskills.io)
specification so the result works across any client that reads the spec, not just
one vendor.

The whole point is **low ceremony, high fidelity**: get a correct `name`/`description`
frontmatter, a lean body, the right placement, and a green `skills-ref validate` —
without an evaluation harness or a multi-round authoring loop.

## When to use this skill

Reach for it when the user wants to stand up a new skill in *this* repo and have it
be spec-correct on the first try:

| Use when the user… | This skill gives them… |
|---|---|
| "Create / scaffold / init a skill for X" | a ready directory + valid `SKILL.md` |
| Mentions a "repo-local skill" or "`.agents/skills`" | correct placement + precedence guidance |
| Names the **agentskills.io spec** or asks for cross-client compatibility | frontmatter that satisfies the open spec |
| Wants a copy-paste `SKILL.md` starter | the minimal template below + `assets/SKILL.md.template` |
| Asks "is my frontmatter valid?" | the field table + `skills-ref validate` |

### Not to be confused with

- **`skill-creator`** — the heavyweight authoring *loop*: draft → write test prompts →
  run evals → benchmark with variance → optimize the description. Use that when the skill's
  quality must be *measured and iterated*. Use **this** skill to get a correct skeleton on
  the ground quickly; hand off to `skill-creator` only if you then need eval-driven tuning.
- **`skill-reviewer`** — a quality *audit* of an existing skill (progressive disclosure,
  scope, mental-model language). Run that *after* a skill exists. This skill *produces* the
  skill; the reviewer *grades* it.
- **Marketplace plugin authoring** — wiring a skill into this repo's
  `.claude-plugin/marketplace.json`, changelogs, and `plugins/<name>/skills/<name>/` layout
  is a separate concern handled per `CLAUDE.md`. This skill targets a **repo-local** skill
  (`.agents/skills/<name>/`), not a published marketplace plugin.

## The create workflow

Follow these steps in order. Each one is short; explain choices to the user as you go.

### 1. Capture intent

Pin down two things before touching the filesystem:

1. **What** should the skill let Claude do? (the capability)
2. **When** should it trigger? (the user phrases, file types, and contexts)

The conversation may already contain the answer ("turn this into a skill"). Extract the
workflow, tools, and steps from history first, then confirm the gaps with the user.
```

## agent-team-orchestration (3263-agent-team-orchestration)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/agent-team-orchestration
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3263-agent-team-orchestration/13774-agent-team-orchestration
- الوصف: Run a team of AI agents against the outstanding issues of a GitHub repo: an architect plans what can be parallelized, then each issue gets a small squad - a developer, an adversarial reviewer, an SDET/QA, and a productivity engineer that watches for process bottlenecks - with every agent individually watchable and steerable. Use when: (1) you want to work a whole backlog (not one issue) with agent

```markdown
> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/agent-team-orchestration/SKILL.md`). Updates go through the repo's
> worktree + PR workflow - open an issue, branch, PR.

# agent-team-orchestration

## Problem
You have a repo with a backlog of open issues and you want a *team* of agents to
work them - not a single agent grinding one issue at a time. Two things make
that more than "spawn N agents":

1. **What can run in parallel is a judgment call.** Some issues touch the same
   files, share a migration, or must land in order. Deciding the parallel set is
   architectural work that should happen *before* any developer agent starts.
2. **One agent per issue is too few.** A lone developer agent marks its own
   homework. Real throughput-with-quality comes from giving each issue a small
   squad with separated concerns (build / attack / verify) plus a meta-role that
   watches the *process*, not the code.

This skill is the orchestration recipe: the roles, who reports to whom, how the
parallel set is chosen, and how to keep every agent watchable and steerable.

## The shape
```
                        ┌─────────────┐
        you  ◄────────► │  architect  │   (plans parallel set; owns the conversation)
                        └──────┬──────┘
            ┌──────────────────┼──────────────────┐
        ┌───┴───┐          ┌───┴───┐          ┌───┴───┐
        │issue A│          │issue B│          │issue C│      (parallel where safe)
        └───┬───┘          └───┬───┘          └───┬───┘
       dev│rev│qa         dev│rev│qa         dev│rev│qa       (a squad per issue)
              └──────── productivity engineer ───────┘        (watches the whole run)
```

## Start with a conversation, not a spawn
The run **begins with the architect**, in a conversation with you - not by
immediately fanning out agents. The architect:
- reads every open issue (`gh issue list`, `gh issue view`) and the repo,
- groups issues into a **parallel set** (independent) vs **serialized chains**
  (shared files / ordering / a migration that must land first),
- proposes the wave plan and the per-issue squad assignments,
- gets your go-ahead before squads start.

Arm the architect with the team's own reusable knowledge: this `skillz`
catalog (https://github.com/voitta-ai/skillz) and any internal playbook repo, so
its plan reuses existing skills (e.g. `work-on-pr`, `review-pr-loop`) instead of
reinventing the loop.

## Step 0: runtime precondition (before any spawn)
Detect the surface **before** the first agent is spawned, not at spawn time. The
architect runs, as a precondition:
```bash
which tmux        # is a tmux/cmux shim on PATH?
echo "$TMUX"      # are we inside a tmux/cmux session?
```

## agent-sync-check-workflow (2815-agent-sync)

- الترخيص: **MIT**  ·  الأصل: https://github.com/paat/claude-plugins/tree/e60ac1fa9cca11cdab467b0021e542ac0f94c56d/plugins/agent-sync
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2815-agent-sync/11426-agent-sync-check-workflow
- الوصف: Run /agent-sync:check workflow from agent-sync.

```markdown
# /agent-sync:check Codex Workflow

This generated skill is the Codex-native plugin surface for `/agent-sync:check`.
Also use it when the user invokes that command or asks for the same workflow by name.

Source command: `../../commands/check.md`

## Run Protocol

1. Treat the user text after the command name as `$ARGUMENTS`.
2. Read the source command file before executing. It is the workflow checklist after applying the Codex replacements in this skill.
3. Execute the workflow through Codex-native mechanisms: Codex skills, direct task sequencing in the current session, the Codex CLI, or Codex-supported multi-agent tooling when available.
4. Do not create user-local `~/.codex/prompts` wrappers. This skill is the reusable plugin-bundled workflow surface.
5. When the source command says `Skill('plugin:skill')`, load the named plugin skill normally.
6. When the source command references `${CLAUDE_PLUGIN_ROOT}/path`, resolve it to this installed plugin root and use `path` under that root. Do not require the environment variable to exist.
7. When the source command contains a Claude-only primitive, use the Codex replacement:
   - `AskUserQuestion` -> ask the user directly; in non-interactive runs, stop and report the exact required input.
   - Claude slash-command execution -> invoke this skill or the corresponding plugin skill.
   - Claude `Task` / `Agent` / `TeamCreate` dispatch -> use Codex-native multi-agent tooling if available, `codex exec --dangerously-bypass-approvals-and-sandbox` when a separate Codex process is useful, or a fresh role phase in the current Codex session. The development container is the security boundary.
   - `ScheduleWakeup` -> use Codex session continuation or an explicit user-visible status checkpoint; do not depend on a Claude lifecycle hook.

## Command Metadata

- Plugin: `agent-sync`
- Command aliases: `/agent-sync:check`
- Source description: Verify AGENTS.md is in sync with Claude Code configuration files
```

## agent-sync-generate-workflow (2815-agent-sync)

- الترخيص: **MIT**  ·  الأصل: https://github.com/paat/claude-plugins/tree/e60ac1fa9cca11cdab467b0021e542ac0f94c56d/plugins/agent-sync
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2815-agent-sync/11427-agent-sync-generate-workflow
- الوصف: Run /agent-sync:generate workflow from agent-sync.

```markdown
# /agent-sync:generate Codex Workflow

This generated skill is the Codex-native plugin surface for `/agent-sync:generate`.
Also use it when the user invokes that command or asks for the same workflow by name.

Source command: `../../commands/generate.md`

## Run Protocol

1. Treat the user text after the command name as `$ARGUMENTS`.
2. Read the source command file before executing. It is the workflow checklist after applying the Codex replacements in this skill.
3. Execute the workflow through Codex-native mechanisms: Codex skills, direct task sequencing in the current session, the Codex CLI, or Codex-supported multi-agent tooling when available.
4. Do not create user-local `~/.codex/prompts` wrappers. This skill is the reusable plugin-bundled workflow surface.
5. When the source command says `Skill('plugin:skill')`, load the named plugin skill normally.
6. When the source command references `${CLAUDE_PLUGIN_ROOT}/path`, resolve it to this installed plugin root and use `path` under that root. Do not require the environment variable to exist.
7. When the source command contains a Claude-only primitive, use the Codex replacement:
   - `AskUserQuestion` -> ask the user directly; in non-interactive runs, stop and report the exact required input.
   - Claude slash-command execution -> invoke this skill or the corresponding plugin skill.
   - Claude `Task` / `Agent` / `TeamCreate` dispatch -> use Codex-native multi-agent tooling if available, `codex exec --dangerously-bypass-approvals-and-sandbox` when a separate Codex process is useful, or a fresh role phase in the current Codex session. The development container is the security boundary.
   - `ScheduleWakeup` -> use Codex session continuation or an explicit user-visible status checkpoint; do not depend on a Claude lifecycle hook.

## Command Metadata

- Plugin: `agent-sync`
- Command aliases: `/agent-sync:generate`
- Source description: Generate or update AGENTS.md from Claude Code configuration files
```
