# مصادر «سير عمل Git وGitHub» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## git-pr-merge-unblock (3311-git-pr-merge-unblock)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/git-pr-merge-unblock
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3311-git-pr-merge-unblock/13825-git-pr-merge-unblock
- الوصف: Work out why a pull request will not merge and who can actually unblock it, on github.com or a self-hosted GitHub Enterprise. Use when: (1) the PR shows "Code owner review required" and you need to find a human who can approve it, (2) the PR reports APPROVED reviews but `reviewDecision` is still REVIEW_REQUIRED, (3) a PR has sat for days with no human review because only *teams* were requested and

```markdown
# Git PR merge unblock

## Problem

A PR can be blocked by code-owner requirements, branch protection, commit-message
enforcement, or CI — and the UI rarely names the person who can clear it. Worse, a PR
can look *approved and green* and still be unmergeable, so the blocker is invisible
until someone goes looking.

Throughout: on GitHub Enterprise, `gh` needs `GH_HOST=your-ghe.example.com` as an **env
var**, not a `--hostname` flag. On github.com, drop the prefix. Examples below show the
env-var form; it is harmless on github.com if you set it correctly.

## Pre-flight: check commit conventions BEFORE you create the PR

Cheaper than discovering it at merge time. Inspect:

- `.github/workflows/` — CI running commitlint or a custom enforcement script
- `.husky/`, `.git/hooks/` — client-side hooks
- `package.json` — `commitlint` config, `lint-staged`
- `.commitlintrc.*`
- `scripts/` — repos often keep a bespoke `enforce-commit-msg*.sh` here

Default to conventional commits (`type(scope): description`) when nothing says otherwise.
Valid types: `fix`, `feat`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`,
`ci`, `revert`.

## Step 1: Read the actual blocker

```bash
GH_HOST=your-ghe.example.com gh pr view {PR} --repo {org}/{repo} \
  --json mergeStateStatus,reviewDecision,statusCheckRollup
```

Look for code-owner requirements, failing required checks, and commit-message validation.

## Step 2: `reviewDecision` is REVIEW_REQUIRED but `reviews` shows APPROVED

Both are true at once, and it is the single most confusing state a PR reaches. Two causes,
and one query shows both:

```bash
GH_HOST=your-ghe.example.com gh pr view {PR} --repo {org}/{repo} \
  --json reviewDecision,reviews,reviewRequests \
  --jq '{decision: .reviewDecision,
         reviews: [.reviews[] | "\(.author.login):\(.state)"],
         requested: [.reviewRequests[] | .login // .name]}'
```

**Cause 1 — every approval came from a bot.** Most orgs run review bots (a CI account, a
lint bot, an automated reviewer). Their APPROVED shows up in `reviews` and counts toward
nothing CODEOWNERS checks. The PR reads "2 approvals, all checks green" and is still
unmergeable.

**Cause 2 — only *teams* were requested.** If `requested` contains team names and no
individual logins, nobody's personal review queue ever received it. Team requests are
easy to ignore and PRs sit on them for weeks. Requesting named individuals is what gets
a human to look — Steps 3 and 5.

Neither cause produces an error message anywhere. You have to go read `reviews[].author`
and notice they are all bots.

## Step 3: Resolve the code owners **for the changed path**, then pick a human

CODEOWNERS is matched per-path, longest prefix wins. A repo-wide "who owns this repo"
```

## git-commit (1536-git-commit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jabworks/agentic-toolkit/tree/e31604d20e4d210722885122124a77828c616485/dist/plugins/git-commit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1536-git-commit/4219-git-commit
- الوصف: Use when staging changes and creating a git commit — derive a conventional-commit message from the diff and run the commit safely. Review before staging (never blind `git add .`), write multi-paragraph bodies via `-F`/heredoc (never chained `-m`), keep unwanted trailers out, and check the branch first. Covers the full local flow through verify and optional amend; stops before push — hand off to /r

```markdown
# git-commit

Craft a conventional-commit message from the actual diff and run the commit **safely**. The message format matters, but the real value is *how* the git commands run — the four guardrails below exist because these are where commits go wrong.

## When to use

- The user asks to commit, "save this", or "make a commit".
- You've finished a unit of work and changes are ready to record locally.
- A messy working tree needs splitting into clean, logical commits.

Not for: pushing, opening PRs, rebasing, cherry-picking. For choosing *which* git operation fits a situation, see the **git-operations** skill.

## Flow

```
1. Inspect     git status  +  git diff        (see everything before touching the index)
2. Branch chk  git branch --show-current       (on main/default? → guardrail 4)
3. Stage       git add <explicit pathspecs>    (never -A / . — guardrail 1)
4. Compose     type(scope): subject + body     (derive from the diff, confirm)
5. Commit      git commit -F <msgfile>          (multiline-safe — guardrail 2)
6. Verify      git show --stat  /  git log -1
7. Optional    amend / fixup on unpushed local commits only
```

## Guardrails

These are non-negotiable. Each is a "never / always" pair with the exact command.

### 1. Never blind-stage

**Never** `git add .`, `git add -A`, or `git add -u`. They sweep in unrelated edits, stray debug files, and secrets.

**Always** review first, then stage explicit pathspecs:

```bash
git status               # what's changed and what's untracked
git diff                 # unstaged changes, in detail
git diff --staged        # anything already staged
git add path/to/a path/to/b   # only the paths this commit is about
```

Untracked files are surfaced to the user, never auto-added. If unsure whether a file belongs, ask.

### 2. Never chain `-m` for bodies

**Never** build a body/footer from repeated `-m` flags (`-m subject -m body -m footer`) — it mangles blank lines and wrapping.

**Always** write the full message to a file and commit with `-F`:

```bash
# compose the message (subject, blank line, body, blank line, footer)
cat > "$(git rev-parse --git-dir)/COMMIT_EDIT.tmp" <<'EOF'
type(scope): short imperative subject

Body paragraph explaining what changed and why. Wrap at ~72 cols.

Refs: #123
EOF
git commit -F "$(git rev-parse --git-dir)/COMMIT_EDIT.tmp"
rm -f "$(git rev-parse --git-dir)/COMMIT_EDIT.tmp"
```

A single-line subject with no body may use `git commit -m "type(scope): subject"` — the ban is only on chaining `-m` for multi-part messages.

### 3. Never inject trailers

**Never** add `Co-Authored-By:`, tool attribution, or any trailer the user didn't ask for. Guard the footer block — only `Refs:`, `Fixes:`, `BREAKING CHANGE:`, or trailers the user explicitly requested belong there.
```

## git-worktree-convention (3315-git-worktree-convention)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/git-worktree-convention
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3315-git-worktree-convention/13829-git-worktree-convention
- الوصف: Keep every git repo on its default branch and do all branch work in a sibling `<repo>.worktrees/` directory. Use when: (1) starting branch work in any repo under a managed tree and you need to know where the worktree goes, (2) cloning a new repo and setting up its layout, (3) you notice a repo sitting on a non-default branch, or worktrees scattered outside `<repo>.worktrees/` (e.g. `repo-wt-87`, a

```markdown
# Git worktree convention: repo on default, branches in `<repo>.worktrees/`

Canonical source: this file in `voitta-ai/skillz`.

## The pattern

```
<parent-dir>/
  <repo>/              # ALWAYS on the default branch (main or master)
  <repo>.worktrees/    # sibling dir holding every branch worktree
    <branch-name>/     # one dir per active branch; path mirrors branch name
```

Rules:

1. The repo directory itself **never leaves the default branch**. It is the
   place you read "what is shipped" and the place you branch from.
2. All branch work happens in `<repo>.worktrees/<branch-name>/`.
3. On a fresh clone, create the `.worktrees` sibling immediately.
4. A branch name with a slash nests (`feature/x` -> `.worktrees/feature/x/`).
   That is correct — the path mirrors the branch name.

Why: a repo pinned to the default branch means `git log`, `gh pr create
--base`, and any tooling that reads the repo dir always sees a stable base,
and N branches can be worked (or reviewed, or built) at once without
stashing.

## Before starting branch work: check for drift

Run this in the repo whose branch you are about to touch. It is read-only.

```bash
REPO=/path/to/repo
git -C "$REPO" rev-parse --abbrev-ref HEAD          # expect main or master
git -C "$REPO" worktree list                        # expect only <repo> + <repo>.worktrees/*
ls -d "${REPO}"* 2>/dev/null                        # expect only <repo> and <repo>.worktrees
```

Three drift shapes, each with its own fix below:

| Symptom | Shape |
| ------- | ----- |
| `rev-parse` prints something other than main/master | repo dir is on a branch |
| `worktree list` shows a path outside `<repo>.worktrees/` (e.g. `repo-wt-87`, `repo.wt/x`) | ad-hoc worktree location |
| `worktree list` shows the repo name twice (`repo/repo.worktrees/x`) | worktree nested inside the repo |

## When you find drift: ASK, do not silently reorganize

Reorganizing moves someone's working directory. An editor, a terminal, a
running dev server, or a background agent may be sitting in the path you are
about to move, and a worktree with uncommitted changes is not yours to
relocate on a hunch.

So: **report what you found and ask before restructuring.** Say which repos
drifted, which shape each one is, and what the fix would do. Offer to do the
whole set, a subset, or nothing. Then act on the answer.

Two things to check before proposing a move, because they change the answer:

```bash
git -C "$WORKTREE" status --short          # uncommitted work?
git -C "$WORKTREE" rev-parse --abbrev-ref HEAD   # detached HEAD?
```

- **Uncommitted changes** — offer to commit or stash first; do not move over them.
- **Detached HEAD** — there is no branch to name the worktree after. Ask what
```

## git-merge-request (3611-spellbook-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/yyykf/spellbook-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3611-spellbook-skills/14522-git-merge-request
- الوصف: 一键提交并创建合并请求（GitHub Pull Request 或 GitLab Merge Request）。当用户说「创建 PR」「创建 MR」「提交并创建合并请求」「push 并开 PR/MR」「提 PR」「提 MR」「open a pull request」「open a merge request」或类似意图时触发。自动识别 GitHub / GitLab 远端，调用对应的 gh / glab CLI，完成暂存、Conventional Commit、推送、读取仓库内 PR/MR 模板（若存在）、创建并指派合并请求。不适用于：仅本地提交（用 git-commit 技能）、纯推送但不开合并请求、Bitbucket / Gitea 等其他平台。

```markdown
# Git Merge Request

## Overview

一键提交并创建合并请求，覆盖 GitHub Pull Request 与 GitLab Merge Request 两种平台。统一识别远端、复用 git-commit 技能完成提交、自动探测仓库内 PR/MR 模板、生成标题与描述、调用对应 CLI 创建并指派。

**Core principle:** 检测平台 → 复用 git-commit 提交 → 推送 → 仓库模板优先于内置模板 → 用户确认后通过 CLI 创建并指派。

**Announce at start:** "正在使用 git-merge-request skill 帮你创建合并请求。"

## Prerequisites

- 当前目录为 git 仓库且 `origin` 指向 GitHub 或 GitLab
- 平台对应 CLI 已安装并认证：
  - GitHub → `gh`（用 `gh auth status` 验证）
  - GitLab → `glab`（用 `glab auth status` 验证）

如果检测到平台但对应 CLI 缺失，**直接终止并明确告知安装命令，不要静默回退到另一个 CLI**：

| 平台 | 安装命令（macOS） |
|------|------|
| GitHub | `brew install gh && gh auth login` |
| GitLab | `brew install glab && glab auth login` |

## Inputs

从用户输入中提取下列参数，未指定时使用默认值：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| target_branch | 仓库默认分支 | 合并目标分支 |
| assignee | 当前 CLI 登录用户 | 指派人 |
| title | 自动生成 | 合并请求标题，从 commit 历史推导 |
| template | 自动选择 | 多模板时让用户选 |
| -y | false | 跳过确认直接创建 |

## Workflow

### Phase 1: 检测平台

读取 `git remote get-url origin`，按 host 判定平台：

| Host 关键词 | 平台 | CLI |
|------|------|------|
| `github.com` 或自建 GHE 域名 | GitHub | `gh` |
| `gitlab.com` 或自建 GitLab 域名 | GitLab | `glab` |
| 其他 | 不支持 | 终止并告知 |

如果是企业自建域名无法明确判断，先看仓库根是否存在 `.github/` 或 `.gitlab/` 目录辅助判断；仍无法确定时询问用户。

### Phase 2: 检查环境

平台判定后，运行对应命令验证 CLI 已认证：

```
# GitHub
gh auth status

# GitLab
glab auth status
```

同时查看当前仓库状态与提交风格：

```
git status
git log --oneline -5
```

### Phase 3: 暂存与提交（复用 git-commit 技能）

**优先调用 `git-commit` 技能完成提交**，避免在本技能里重复实现 commit 流程。git-commit 已经处理：
- 排除 `.env` 等敏感文件
- 读取仓库提交规范并优先遵守
- 生成 Conventional Commit（emoji 默认关闭，仅 `--emoji` 时启用且置于冒号后）
- 按仓库规范处理描述语言与 body 标记（如 `[#AI]`）
- 仓库提交风格识别

如果 git-commit 技能不可用，按以下规则手工提交：
- 若无已暂存文件，`git add` 已修改 / 新增文件（排除 `.env` / `*.key` / `credentials*` 等敏感文件）
- 用 `git diff --cached` 分析变更，生成 Conventional Commit（emoji 仅在仓库 / 用户要求时启用、且置于冒号后，描述用中文）
- body 末尾追加 `[#AI]` 标记
- 执行 `git commit`

### Phase 4: 推送

```
git push origin <current_branch>
```

若远程分支不存在，使用 `git push -u origin <current_branch>`。

### Phase 5: 解析目标分支并同步远程

优先级：用户指定 > 仓库默认分支。

| 平台 | 获取默认分支命令 |
|------|------|
| GitHub | `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'` |
| GitLab | `git remote show origin \| grep 'HEAD branch' \| awk '{print $NF}'` |

**关键：必须 fetch 远程目标分支以确保比较基准最新：**

```
git fetch origin <target_branch>
```

后续所有比较必须使用 `origin/<target_branch>` 而非本地 `<target_branch>`。本地分支可能滞后，会让 diff 与待合并 commit 列表不准确。

### Phase 6: 解析指派人

优先级：用户指定 > 当前 CLI 登录用户。

| 平台 | 获取当前用户命令 |
|------|------|
| GitHub | `gh api user --jq '.login'` |
| GitLab | `glab auth status 2>&1 \| grep 'Logged in' \| awk '{print $6}'` |

### Phase 7: 探测并选择仓库内模板

**核心规则：仓库内有模板就用仓库的，没有再用内置模板。** 团队往往在模板里放了 checklist、签署声明、影响范围说明等约定项，覆盖这些约定会让 review 流程出岔子。

按以下顺序查找模板文件，**第一个命中即停**：

#### GitHub（PR 模板）

1. `.github/PULL_REQUEST_TEMPLATE.md`
```

## git-worktree (1538-git-worktree)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jabworks/agentic-toolkit/tree/e31604d20e4d210722885122124a77828c616485/dist/plugins/git-worktree
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1538-git-worktree/4221-git-worktree
- الوصف: Use when working with git worktrees — creating an isolated workspace or parallel checkout for a task or agent, listing or switching trees, moving work between them, pruning stale ones, recovering a broken one. Triggers include "create a worktree", "new worktree for this fix". Native-first — prefer the host's own worktree tooling, fall back to `git worktree` only when there is none. Not for undo/di

```markdown
# git-worktree

A **decision router** for worktrees: given a situation, pick the right move, run it safely, and know the undo path. Same shape as `git-operations`, different topology — a worktree changes *where* a checkout lives, never what history says.

## When to use

- You need an isolated workspace for a task, a branch, or an agent.
- You have worktrees already and need to list, switch, move work, or clean up.
- A worktree is in a bad state — stale lock, deleted directory, branch stuck as checked-out elsewhere.

## Native first — the rule that matters most

**Prefer your platform's native worktree tooling. Fall back to `git worktree` only when there is none.**

Claude Code has `EnterWorktree` and `isolation: "worktree"` agents; other harnesses have their own. When a host manages worktrees for you, running `git worktree add` yourself creates **phantom state the harness cannot see or manage** — it won't clean it up, won't list it, and may collide with its own tree on the same branch.

The reverse is safe: `git worktree list` always tells the truth about what exists on disk, whoever created it.

## Step 0 — guards, before any command

Run these first. Two of them mean *stop, you're done or you're somewhere else*.

```bash
git rev-parse --show-superproject-working-tree   # non-empty → submodule, NOT a worktree
git rev-parse --git-dir                          # differs from --git-common-dir → already in a linked worktree
git rev-parse --git-common-dir
git worktree list                                # what already exists
```

| Result | What it means | Do |
|---|---|---|
| Superproject path returned | You're in a submodule | Treat as a normal repo — this skill does not apply |
| `--git-dir` ≠ `--git-common-dir` | You're already in a linked worktree | **Skip creation** — you have your isolation |
| Native tool available | Host manages worktrees | Use it (below); do not `git worktree add` |
| Neither, no native tool | Plain repo, manual path | Fall back to `git worktree add` |

## Decision map

Full routing table in `references/worktree-map.md`. The high-value forks:

| Situation | Choose → (not →) | Undo path |
|---|---|---|
| **Need isolation** | native host tool → (`git worktree add` only if none) | remove the tree; branch survives |
| **Where to put it** | `.worktrees/<name>` inside the repo, **verified gitignored** → (a sibling dir, if you'd rather keep the repo clean) | — |
| **Existing branch** | `git worktree add <path> <branch>` → (not `-b`, which fails if it exists) | `git worktree remove <path>` |
| **New branch** | `git worktree add -b <new> <path>` | remove tree, then `git branch -d <new>` |
| **Switch trees** | `cd <path>` — a worktree is a directory → (never `git switch` into a branch checked out elsewhere) | `cd` back |
```

## gh-pr-merge-delete-branch-closes-dependent-pr (3307-gh-pr-merge-delete-branch-closes-depende)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/gh-pr-merge-delete-branch-closes-dependent-pr
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3307-gh-pr-merge-delete-branch-closes-depende/13821-gh-pr-merge-delete-branch-closes-depende
- الوصف: Fix the surprising auto-close of stacked / dependent PRs when their base branch gets deleted on GitHub. Use when: (1) you ran `gh pr merge --delete-branch` (or any branch-deleting merge action) on PR A, and PR B which was based on PR A is now CLOSED with no warning — not retargeted to the repo's default branch as you might expect, (2) a stacked-PR workflow where each PR in the chain has its base s

```markdown
# `gh pr merge --delete-branch` closes (not retargets) dependent PRs

## Problem

You have a stacked PR chain on GitHub:

```
main ←— PR A (base=main,        head=feature/A)
        PR B (base=feature/A,   head=feature/B)
        PR C (base=feature/B,   head=feature/C)
```

You squash-merge PR A with `gh pr merge --delete-branch`. Two things
happen at the GitHub API level:

1. A squash commit lands on `main`.
2. The `feature/A` branch ref is **deleted** on the remote.

You'd expect GitHub to auto-retarget PR B's base to the repo's default
branch (`main`). It does not. Instead:

- **PR B is auto-CLOSED** (state goes to `CLOSED`, not `OPEN`).
- The review history, comments, approvals, and check results stay
  attached to PR B, but it's closed.
- `gh pr reopen B` fails with `GraphQL: Could not open the pull
  request. (reopenPullRequest)` because GitHub can't reopen a PR whose
  `baseRefName` points at a ref that no longer exists on the remote.

The cascade can chain: if you then merge PR B (after reopening), the
same thing happens to PR C, etc.

## Symptoms

- After `gh pr merge --delete-branch N`, querying a downstream PR M
  whose base was that branch shows:
  ```
  gh pr view M --json state,baseRefName,closed,closedAt
  → {"baseRefName":"feature/A","closed":true,"closedAt":"...","state":"CLOSED"}
  ```
- `gh pr reopen M` returns:
  ```
  GraphQL: Could not open the pull request. (reopenPullRequest)
  ```
- `gh pr edit M --base main` on the closed PR returns:
  ```
  GraphQL: Cannot change the base branch of a closed pull request. (updatePullRequest)
  ```

## Fix

Recreate the deleted base ref temporarily so the PR can be reopened
and retargeted:

```bash
# 1. Get a sensible SHA to point the resurrected branch at. main's tip
#    is fine — the PR's base ref just needs to *exist* for reopen to
#    succeed.
SHA=$(gh api repos/OWNER/REPO/branches/main --jq '.commit.sha')

# 2. Recreate the deleted branch ref at that SHA.
gh api repos/OWNER/REPO/git/refs \
  -f ref="refs/heads/<deleted-branch>" \
  -f sha="$SHA"

# 3. Reopen the dependent PR + retarget to your real base.
gh pr reopen M --repo OWNER/REPO
gh pr edit   M --repo OWNER/REPO --base main

# 4. Verify the PR is back open and pointed at main.
gh pr view M --repo OWNER/REPO --json state,baseRefName,mergeStateStatus,mergeable
# → state=OPEN, baseRefName=main

# 5. (Optional) clean up the resurrected branch — once PR M's base is
#    no longer pointed at it, it can be deleted again safely.
gh api -X DELETE repos/OWNER/REPO/git/refs/heads/<deleted-branch>
```

## Verification

After step 4:

- `state` is `OPEN`.
- `baseRefName` is `main` (or whichever real base you set).
- `mergeStateStatus` is `CLEAN` / `MERGEABLE` if the commits don't
```
