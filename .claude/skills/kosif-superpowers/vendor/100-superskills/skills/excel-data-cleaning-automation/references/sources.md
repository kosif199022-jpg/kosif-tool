# مصادر «تنظيف البيانات وأتمتة إكسل» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## claude-code-plugin-release-automation (3279-claude-code-plugin-release-automation)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/claude-code-plugin-release-automation
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3279-claude-code-plugin-release-automation/13790-claude-code-plugin-release-automation
- الوصف: Make a Claude Code / Codex plugin repo tag itself and publish release notes from its manifest version, and make the version bump non-optional. Use when: (1) the repo has merges piling up with no tags, no GitHub releases, or tags that exist but have no release attached, (2) a CONTRIBUTING/CLAUDE.md rule says "bump the version on every shipping merge" and nothing enforces it, (3) you are hand-runnin

```markdown
# Claude Code plugin repos: automatic tags and release notes

## Problem

A plugin repo has a version field in `.claude-plugin/plugin.json` that is
already load-bearing — it is the cache key for
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`, so an
unchanged version means no install re-extracts and every user keeps running
the old build (see `claude-code-plugin-update-flow`).

Two things go wrong around that field, and both are silent:

1. **The bump is honour-system.** A repo can document "every shipping merge
   bumps the version" and still merge fifty PRs without one, because nothing
   checks. The failure surfaces months later as "your fix never reached me".
2. **Tagging and release notes are manual, so they don't happen.** Repos end
   up with tags and no releases, or no tags at all, and the only record of
   what shipped is `git log`.

The fix for both is the same observation: **the version is already in the
repo and already changes in the PR.** Nothing else needs to be invented — no
CHANGELOG.md, no release-drafter, no semantic-release, no separate VERSION
file. CI can read the field and do the rest.

## Context / Trigger conditions

- `gh release list` is empty on a repo that has been shipping for months.
- `git tag` shows tags with no matching releases.
- Your contributing docs describe a manual tag-after-merge sequence.
- You are tempted to add a CHANGELOG.md that duplicates PR titles.
- You want a merge to be blocked when the author forgot the bump.

## Solution

One workflow file, two jobs, opposite triggers.

```yaml
name: release

on:
  push:
    branches: [master]          # or main
  pull_request:
    branches: [master]
    # Docs/CI-only exemption: users never execute these paths, so a PR
    # touching nothing else is not shipping and owes no bump. Mirror
    # whatever exemption your contributing docs already state.
    paths-ignore:
      - '.github/**'
      - 'tests/**'

permissions:
  contents: read

env:
  VERSION_FILE: .claude-plugin/plugin.json

jobs:
  version-bumped:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Version must advance
        env:
          BASE: ${{ github.base_ref }}
        run: |
          git fetch --no-tags --depth=1 origin "$BASE"
          old=$(git show "FETCH_HEAD:$VERSION_FILE" | jq -r .version)
          new=$(jq -r .version "$VERSION_FILE")
          if [ "$old" = "$new" ]; then
            echo "::error::$VERSION_FILE#version is still $old - bump it."
            exit 1
          fi
          if [ "$(printf '%s\n%s\n' "$old" "$new" | sort -V | head -1)" != "$old" ]; then
            echo "::error::$new does not advance past $old."
            exit 1
          fi
          echo "$old -> $new"
```

## merge-main (1017-merge-main)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/plugins/merge-main
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1017-merge-main/2301-merge-main
- الوصف: Merge the base branch into this branch, resolve conflicts, and push. Use for "merge main" or "sync with main"; to rebase, use rebase-onto-main.

```markdown
# Merge Main

Fetch and merge the repository's base branch into the current feature branch.

## Options

The user may provide these options inline:

- **--base `<branch>`**: Override the auto-detected base branch (e.g., `--base develop`)

## Skill dependencies

- **Required:** None
- **Optional:** `commit`

## Workflow

### 1. Pre-Flight Checks

Run these commands in parallel to understand the current state:

```bash
# Check for uncommitted changes
git status

# Detect the repository's default branch
gh repo view --json defaultBranchRef -q '.defaultBranchRef.name'

# Confirm which branch we are on
git branch --show-current
```

If `--base <branch>` was specified, use that value instead of the detected default branch.

**If `gh` is not available**, fall back to detecting the default branch with:

```bash
git remote show origin | grep 'HEAD branch' | sed 's/.*: //'
```

**If the current branch is the default branch itself**, warn the user that merging the base branch into itself is a no-op and stop.

### 2. Handle Uncommitted Changes

If `git status` shows uncommitted changes (staged or unstaged):

1. Warn the user that there are uncommitted changes.
1. Ask whether to:
   - **Stash**: Run `git stash` before proceeding, then `git stash pop` after the merge completes.
   - **Commit first**: Invoke the `/commit` skill, then continue with the merge. `commit` is an optional dependency: if it is not installed, leave this choice out and tell the user why, so they can commit by hand, or install `commit`, before running this skill again.
   - **Abort**: Stop without doing anything.

### 3. Fetch and Merge

```bash
git fetch origin <default-branch>
git merge origin/<default-branch>
```

Where `<default-branch>` is the detected or overridden base branch name.

### 4. Handle Merge Result

#### Clean Merge

If the merge completes without conflicts:

1. Report success.
1. Show a summary of what was merged:

```bash
git log HEAD@{1}..HEAD --oneline
```

#### Already Up to Date

If git reports "Already up to date.", report that the branch is already current with the base branch and stop.

#### Conflicts

If the merge produces conflicts, proceed to the conflict resolution workflow below.

### 5. Conflict Resolution

When merge conflicts occur:

1. **List conflicted files**:

```bash
git diff --name-only --diff-filter=U
```

1. **Resolve each conflicted file**:
   - Read the file and examine the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
   - Use the surrounding code context, the intent of both sides, and the project's conventions to determine the correct resolution.
   - For trivial conflicts (whitespace, import ordering, adjacent non-overlapping changes), resolve automatically.
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

## pr-amend-force-push-lost-to-racing-merge (3343-pr-amend-force-push-lost-to-racing-merge)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/pr-amend-force-push-lost-to-racing-merge
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3343-pr-amend-force-push-lost-to-racing-merge/13857-pr-amend-force-push-lost-to-racing-merge
- الوصف: A review-fix amend + force-push that lands after the reviewer's squash-merge succeeds silently and never reaches the default branch: the merge snapshots the head GitHub had when the merge ran, the later force-push still updates the branch ref without any warning, and the default branch keeps the pre-review version. Use when: (1) you force-pushed to a PR branch while the PR was under active review 

```markdown
> **Canonical source.** This skill lives in the repo at
> https://github.com/voitta-ai/skillz (file:
> `skills/pr-amend-force-push-lost-to-racing-merge/SKILL.md`). Updates go
> through the repo's worktree + PR workflow - open an issue, branch, PR.

# Amend + force-push racing an in-flight merge loses silently

## Problem

Review feedback arrives; you amend the commit and force-push. The reviewer
squash-merges in the same window. Two facts make the outcome invisible:

- The merge snapshots whatever head GitHub had **when the merge API call
  ran**, not whatever the branch points at later.
- A force-push to the branch of an already-merged PR **succeeds** — the
  branch ref updates normally (the branch still exists until someone deletes
  it), the PR stays `MERGED`, and nothing anywhere warns that the two events
  crossed.

Net result: your branch and your local checkout contain the fix; the default
branch carries the pre-review version; the PR page reads as if the review
round concluded normally. Nobody finds out until something downstream trips
over the missing change.

## How it actually surfaced

The miss was discovered late, through a stacked follow-up branch: after
retargeting it to the default branch and rebasing, `terraform validate`
failed with

```
Error: Reference to undeclared resource
```

because the follow-up assumed a resource the amendment had introduced — and
the default branch still had the pre-amendment shape. Confirmed with:

```bash
git show origin/main:<file>        # pre-review content, amendment absent
```

Any validator, compiler, or test in a dependent branch can be the tripwire;
until one fires, the loss is invisible.

## Detection — do this after any force-push to a PR under review

Cheap and immediate:

```bash
gh pr view <N> --repo OWNER/REPO --json state,mergeCommit,headRefOid
```

If `state` is `MERGED` and the merge happened around your push, check whether
your amendment made it in. Squash merges break ancestry, so
`git merge-base --is-ancestor` proves nothing — **diff the trees**:

```bash
git fetch origin
git diff <mergeCommit-sha> <your-branch-head> -- <files you amended>
```

Non-empty output on the files you amended means the amendment missed the
merge window. (An empty diff means the merge caught your push — you are
fine.)

## Recovery

Do not rewrite the default branch, and a revert is overkill — the merged
content is not wrong, it is merely incomplete:

1. **Carry the lost fix forward as its own commit** in the stacked follow-up
   PR (or a small new PR if none exists), with a commit body that says it
   carries over the review fix from the merged PR, which missed its merge
   window. Keeping it a separate commit preserves the review trail.
```

## merge-main (954-merge-main)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/dist/codex/plugins/merge-main
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/954-merge-main/2239-merge-main
- الوصف: Merge the base branch into this branch, resolve conflicts, and push. Use for "merge main" or "sync with main"; to rebase, use rebase-onto-main.

```markdown
# Merge Main

Fetch and merge the repository's base branch into the current feature branch.

## Options

The user may provide these options inline:

- **--base `<branch>`**: Override the auto-detected base branch (e.g., `--base develop`)

## Skill dependencies

- **Required:** None
- **Optional:** `commit`

## Workflow

### 1. Pre-Flight Checks

Run these commands in parallel to understand the current state:

```bash
# Check for uncommitted changes
git status

# Detect the repository's default branch
gh repo view --json defaultBranchRef -q '.defaultBranchRef.name'

# Confirm which branch we are on
git branch --show-current
```

If `--base <branch>` was specified, use that value instead of the detected default branch.

**If `gh` is not available**, fall back to detecting the default branch with:

```bash
git remote show origin | grep 'HEAD branch' | sed 's/.*: //'
```

**If the current branch is the default branch itself**, warn the user that merging the base branch into itself is a no-op and stop.

### 2. Handle Uncommitted Changes

If `git status` shows uncommitted changes (staged or unstaged):

1. Warn the user that there are uncommitted changes.
1. Ask whether to:
   - **Stash**: Run `git stash` before proceeding, then `git stash pop` after the merge completes.
   - **Commit first**: Invoke the `/commit` skill, then continue with the merge. `commit` is an optional dependency: if it is not installed, leave this choice out and tell the user why, so they can commit by hand, or install `commit`, before running this skill again.
   - **Abort**: Stop without doing anything.

### 3. Fetch and Merge

```bash
git fetch origin <default-branch>
git merge origin/<default-branch>
```

Where `<default-branch>` is the detected or overridden base branch name.

### 4. Handle Merge Result

#### Clean Merge

If the merge completes without conflicts:

1. Report success.
1. Show a summary of what was merged:

```bash
git log HEAD@{1}..HEAD --oneline
```

#### Already Up to Date

If git reports "Already up to date.", report that the branch is already current with the base branch and stop.

#### Conflicts

If the merge produces conflicts, proceed to the conflict resolution workflow below.

### 5. Conflict Resolution

When merge conflicts occur:

1. **List conflicted files**:

```bash
git diff --name-only --diff-filter=U
```

1. **Resolve each conflicted file**:
   - Read the file and examine the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
   - Use the surrounding code context, the intent of both sides, and the project's conventions to determine the correct resolution.
   - For trivial conflicts (whitespace, import ordering, adjacent non-overlapping changes), resolve automatically.
```
