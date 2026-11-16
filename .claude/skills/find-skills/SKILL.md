---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill. In KOSIF it searches the skills already in this repository first, then the open skills.sh ecosystem. Egyptian Arabic triggers: دوّر على مهارة، فيه مهارة تعمل كذا؟، لاقيلي مهارة، ابحث عن مهارات، find-skills.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query] [--owner <owner>]` - Search for skills interactively or by keyword, optionally scoped to a GitHub owner
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Check the Leaderboard First

Before running a CLI search, check the [skills.sh leaderboard](https://skills.sh/) to see if a well-known skill already exists for the domain. The leaderboard ranks skills by total installs, surfacing the most popular and battle-tested options.

For example, top skills for web development include:
- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs each)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)

### Step 3: Search for Skills

If the leaderboard doesn't cover the user's need, run the find command:

```bash
npx skills find [query] [--owner <owner>]
```

For example:

- User asks "how do I make my React app faster?" → `npx skills find react performance`
- User asks "can you help me with PR reviews?" → `npx skills find pr review`
- User asks "I need to create a changelog" → `npx skills find changelog`

### Step 4: Verify Quality Before Recommending

**Do not recommend a skill based solely on search results.** Always verify:

1. **Install count** — Prefer skills with 1K+ installs. Be cautious with anything under 100.
2. **Source reputation** — Official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.
3. **GitHub stars** — Check the source repository. A skill from a repo with <100 stars should be treated with skepticism.

### Step 5: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The install count and source
3. The install command they can run
4. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

### Step 6: Offer to Install

If the user wants to proceed, you can install the skill for them:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```

## Inside KOSIF

Vendored from github.com/vercel-labs/skills, `skills/find-skills/SKILL.md` (commit b716f9d, MIT, © 2026 Vercel,
Inc.; the licence is `LICENSE` in this folder). The upstream text above is unchanged. KOSIF adds only this section
and the last two sentences of the description.

**Search what is already here first.** This repository already holds about 800 skills and 5,800+ catalog powers,
so before going to skills.sh run these from the repository root, in this order, and stop at the first good fit:

```bash
python3 .claude/skills/kosif-superpowers/scripts/hub.py find '<what the user needs>'        # tools, powers, super skills, animation principles
python3 .claude/skills/kosif-superpowers/scripts/superskills.py find '<need>'                   # the owner's 114 super skills
python3 .claude/skills/kosif-superpowers/scripts/animation_principles.py find '<need>'          # 144 Disney-principle animation skills
python3 .claude/skills/kosif-superpowers/scripts/micro_index.py find '<words>'                   # one-line address of any power or tool
python3 .claude/skills/kosif-superpowers/scripts/skills_lint.py --json                           # every SKILL.md in the repo, with name and description
```

Put the user's words inside single quotes, never double quotes, and write any `'` in them as `'\''`, so `$(...)`, backticks or `$VAR` in a request stay plain text and are never run by the shell.

Say which one you found and where its `SKILL.md` is. Go to the open ecosystem (`npx skills find`, the skills.sh
leaderboard) only when nothing here fits, or when the owner asks for outside skills by name.

**Installing from outside is the owner's call.** A skill from skills.sh is third-party text and often scripts. Show
the owner the name, source repository, install count, licence and what it would run, and install only after their
yes. Prefer adding it to this repository the way earlier outside skills were added (whole folder, licence kept,
a row in `THIRD_PARTY_NOTICES.md`) over `npx skills add -g`, which writes outside the repository and is lost when a
cloud session ends. A cloud session may have no network to skills.sh: say so instead of guessing results.

**Language.** Answer in the owner's language and dialect; search terms for `npx skills find` stay in English.

