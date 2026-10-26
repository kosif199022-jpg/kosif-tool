# مصادر «بناء GPT مخصص ومشروع Claude» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## grafana-assistant-cli (1486-grafana-assistant)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/grafana/ai-marketplace/tree/12be5634a492f73c189d466c5449d09b853ad7a4/plugins/grafana-assistant
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1486-grafana-assistant/3689-grafana-assistant-cli
- الوصف: Use the grafana-assistant CLI to interact with Grafana Assistant via A2A API. Covers installation, configuration, prompting, keeping conversation context, and practical patterns for ops investigations. Use when the user mentions grafana-assistant, Grafana Assistant CLI, assistant tunnel, or wants to query a Grafana instance via the assistant.

```markdown
# grafana-assistant CLI

CLI tool for interacting with Grafana Assistant via the A2A API.

## Prerequisites

The `grafana-assistant` binary must already be installed and available on `$PATH`. **Do not attempt to install it automatically.** If the command is not found, stop and tell the user to install it first.

Installation instructions and pre-built binaries: [github.com/grafana/assistant-cli](https://github.com/grafana/assistant-cli)

A Docker image is also available: [github.com/grafana/assistant-cli/pkgs](https://github.com/grafana/assistant-cli/pkgs)

## Configuration

### Config file locations (first found wins)

1. `GRAFANA_ASSISTANT_CONFIG` env var (if set)
2. `./grafana-assistant.yaml` (current directory, use `--local` flag)
3. `~/.config/grafana-assistant/config.yaml`

### Config file format

```yaml
current-instance: prod

instances:
  localhost:
    url: http://localhost:3000
    token: glsa_abcd1234
  prod:
    url: https://mystack.grafana.net
    token: ${GRAFANA_PROD_TOKEN}  # env var expansion supported

projects:
  - name: my-app
    path: ~/projects/my-app

tunnel:
  tools:
    filesystem:
      allowed_paths: [/var/log/myapp]
      deny_paths: ["**/*.key", "**/secrets.yaml"]
    terminal:
      allowed_commands: [git, kubectl, docker]
      deny_commands: ["rm -rf"]
      passthrough_env: [AWS_PROFILE, KUBECONFIG]
```

### Environment variables

| Variable | Description |
|---|---|
| `GRAFANA_URL` | Grafana instance URL (overrides config) |
| `GRAFANA_SA_TOKEN` | Service account token (overrides config) |
| `GRAFANA_ASSISTANT_CONFIG` | Override config file path |

### Credential resolution priority

1. `--url` and `--token` flags
2. `GRAFANA_URL` and `GRAFANA_SA_TOKEN` env vars
3. `--instance <name>` flag
4. `current-instance` from config file

### Quick setup

```bash
grafana-assistant config set-instance mystack --url https://mystack.grafana.net
grafana-assistant config use-instance mystack
grafana-assistant auth                    # opens browser for PKCE auth
grafana-assistant chat                    # start interactive chat
```

The **Assistant CLI User** role is required for browser auth. Users with **Editor** role or above get this automatically. For custom roles, include the `grafana-assistant-app.tokens:access` permission.

### Managing instances

```bash
grafana-assistant config set-instance <name> -u <url> -t <token>
grafana-assistant config use-instance <name>
grafana-assistant config current
grafana-assistant config list
grafana-assistant config delete-instance <name>
grafana-assistant config path
```

Token supports env var references: `-t '${MY_TOKEN_VAR}'`

### Managing projects

Projects are named directories the assistant can access via the tunnel.

```bash
grafana-assistant config add-project <name> <path>
```

## actions-billing-usage (2153-github-actions-plugin)

- الترخيص: **MIT**  ·  الأصل: https://github.com/laurigates/claude-plugins/tree/9caa2be8e7b4b35823e4154c610e3846af05635c/github-actions-plugin
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2153-github-actions-plugin/7752-actions-billing-usage
- الوصف: Measure GitHub Actions cost with the billing-usage API — per repo, month and SKU; net vs gross; per-job rounding. Use when optimizing CI cost or speed, or before removing a workflow as expensive.

```markdown
# Before Optimizing CI Cost, Read the Billing-Usage API

Promoted from the always-loaded `ci-cost-read-the-billing-api.md` portfolio
rule, whose stub keeps the gate line.

Any "make CI cheaper / faster" task starts with a guess about *where the cost
is*, and across a portfolio that guess is reliably wrong. The intuition follows
**where the interesting work is** (the private repos, the big builds); the
actual minutes follow **how often a workflow fires**, which is dominated by
automation nobody thinks of as expensive. GitHub will tell you exactly, per
repo, per month, per SKU — ask it first, then optimize.

## When to Use This Skill

| Use this skill when... | Skip when... |
|---|---|
| A runner-tier, concurrency, caching, or scheduling change is pitched as a cost or speed win | The target is a single known-slow workflow you are already measuring directly |
| About to *remove* a workflow "because it must be expensive" | |
| A bill moved and the cause isn't obvious — the per-repo × per-month breakdown localizes it in one call | |
| Adding automation, to decide whether it gets its own job | |

## The endpoint (the obvious one is gone)

```
gh api "/users/<user>/settings/billing/usage"
```

> `/users/<user>/settings/billing/actions` — the endpoint most examples and most
> recall still name — now returns **HTTP 410** *"This endpoint has been moved."*
> That 410 is easy to misread as "no billing data available on this plan" and
> skip the measurement entirely.

Org equivalent of the working endpoint: `/orgs/<org>/settings/billing/usage`.

Aggregate before reading; the raw response is one row per repo × month × SKU:

```
gh api "/users/<u>/settings/billing/usage" --jq '[.usageItems[] | select(.product=="actions" and .unitType=="Minutes")] | group_by(.repositoryName) | map({repo:.[0].repositoryName, minutes:(map(.quantity)|add), net:(map(.netAmount)|add)}) | sort_by(-.minutes)'
```

## Reading it correctly

- **The filter takes the *bare* repo name, not `owner/repo`.**
  `select(.repositoryName == "<owner>/<repo>")` returns `[]`, which is
  indistinguishable from "this repo bills nothing"; `"<repo>"` returns the rows.
  The owner-qualified filter has reported nothing for a repo billing thousands
  of minutes that month, and a cost argument was nearly built on that empty
  result. Control-test an empty billing filter against a repo you know is
  active before believing it.
- **`netAmount`, not `grossAmount`, is the spend.** Public-repo minutes are free
  and unlimited, so their rows read `grossAmount == discountAmount` and
  `netAmount == 0`. A repo showing a large gross may be costing nothing — but
  it's still where a runner-tier change would pay off *once* charges begin, so
  read both: gross for **exposure**, net for **current spend**.
```

## github-actions-auth-security (2153-github-actions-plugin)

- الترخيص: **MIT**  ·  الأصل: https://github.com/laurigates/claude-plugins/tree/9caa2be8e7b4b35823e4154c610e3846af05635c/github-actions-plugin
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2153-github-actions-plugin/7755-github-actions-auth-security
- الوصف: GitHub Actions auth and security for Claude Code — OIDC, AWS Bedrock, Vertex AI, secrets, permission scoping. Use when setting up workflow authentication or security.

```markdown
# GitHub Actions Authentication and Security

## When to Use This Skill

| Use this skill when... | Use claude-code-github-workflows instead when... |
|---|---|
| Choosing between Anthropic API, AWS Bedrock, or Vertex AI authentication | Authoring the workflow trigger, prompt, or job orchestration |
| Scoping `permissions:` blocks to least-privilege per task | Adding a new automation pattern (PR review, issue triage, CI auto-fix) |
| Hardening against prompt injection or external-contributor attack surface | Configuring `--mcp-config` and tool allowlists — see github-actions-mcp-config |
| Rotating `ANTHROPIC_API_KEY` / `AWS_ROLE_ARN` / `GCP_CREDENTIALS` secrets | Inspecting failing workflow runs — see github-actions-inspection |

Expert knowledge for securing GitHub Actions workflows with Claude Code, including authentication methods, secrets management, and security best practices.

## Core Expertise

**Authentication Methods**
- Anthropic Direct API with API keys
- AWS Bedrock with OIDC
- Google Vertex AI with service accounts
- Secrets management and rotation

**Security Best Practices**
- Permission scoping and least-privilege access
- Prompt injection prevention
- Commit signing and audit trails
- Access control and validation

## Authentication Methods

### Anthropic Direct API
```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Setup**:
1. Generate API key from Anthropic Console
2. Add to repository: Settings → Secrets → New repository secret
3. Name: `ANTHROPIC_API_KEY`
4. Value: `sk-ant-api03-...`

### AWS Bedrock
```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
    aws-region: us-east-1

- uses: anthropics/claude-code-action@v1
  with:
    claude_args: --bedrock-region us-east-1
```

**Setup**:
1. Create IAM role with Bedrock permissions
2. Configure OIDC provider in AWS
3. Add `AWS_ROLE_ARN` to repository secrets
4. Grant role access to Bedrock Claude models

**Required IAM Permissions**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-*"
    }
  ]
}
```

### Google Vertex AI
```yaml
- uses: google-github-actions/auth@v2
  with:
    credentials_json: ${{ secrets.GCP_CREDENTIALS }}

- uses: anthropics/claude-code-action@v1
  with:
    claude_args: |
      --vertex-project-id ${{ secrets.GCP_PROJECT_ID }}
      --vertex-region us-central1
```

**Setup**:
1. Create service account in GCP
2. Grant Vertex AI User role
3. Generate and download JSON key
```

## github-actions-startup-failure-triage (3316-github-actions-startup-failure-triage)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/github-actions-startup-failure-triage
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3316-github-actions-startup-failure-triage/13830-github-actions-startup-failure-triage
- الوصف: Tell a broken workflow file apart from a GitHub Actions outage, and get a PR unstuck without bypassing branch protection. Use when: (1) a workflow run's conclusion is `startup_failure` and you are about to debug YAML you did not change, (2) `gh pr checks` reports "no checks reported on the '<branch>' branch" minutes after opening a PR, (3) `commits/<sha>/check-runs` shows a check stuck `queued` wh

```markdown
# `startup_failure` usually is not your YAML

## Problem

A pull request opens, and CI never reports. `gh pr checks` says:

```
no checks reported on the 'my-branch' branch
```

The obvious reading is that something in the PR broke the workflow — and if
the diff touched `.github/workflows/`, that is where an hour goes. But a
`startup_failure` conclusion is also what GitHub returns when its own Actions
control plane cannot start the run, and the two look identical from the PR.

The cost of guessing wrong is asymmetric. Debugging a workflow file that was
never broken is an hour; worse, the "it must be my branch" theory leads to
force-merging past a required check that simply never got the chance to run.

An outage also produces a second, quieter shape: the push event is **dropped
entirely** and no run is ever created — covered in its own section below,
because both the diagnosis and the retrigger differ.

## The three-signal test

Ask three questions. All three pointing the same way settles it in a minute.

### 1. Read the run, not the checks

The checks view lags, badly, and it lags in the direction that misleads:

```bash
gh api "repos/OWNER/REPO/commits/$(git rev-parse HEAD)/check-runs" \
  --jq '.check_runs[] | "\(.name): \(.status) \(.conclusion)"'
# → check: queued null            <- stale; polling this waits forever
```

while the authoritative view already knows the run is dead:

```bash
gh api "repos/OWNER/REPO/actions/runs?branch=$(git rev-parse --abbrev-ref HEAD)" \
  --jq '.workflow_runs[] | "\(.name) \(.status)/\(.conclusion) \(.created_at)"'
# → checks  completed/startup_failure  2026-...T15:09:43Z
# → release completed/startup_failure  2026-...T15:09:50Z
```

Poll `actions/runs`, not `check-runs`. A loop waiting on `check-runs` to leave
`queued` will spin past the point where the run has already failed — measured
at four minutes of polling `queued` against a run that was `completed` the
whole time.

### 2. Zero jobs, zero annotations

A genuine YAML error produces something to read. Infra produces nothing:

```bash
gh api "repos/OWNER/REPO/actions/runs/$RUN_ID/jobs" --jq '.jobs[].name'   # → empty
gh api "repos/OWNER/REPO/check-runs/$CHECK_ID/annotations"                # → []
```

A malformed workflow normally surfaces an annotation naming the file and line
("Invalid workflow file"). **No jobs and no annotations at all** is the
signature of a run that never started, not one that started and rejected your
config.

### 3. Did the workflow file change in this PR?

```bash
git diff --name-only origin/HEAD...HEAD -- .github/workflows/
```

Empty output, plus a green run of the same workflow on the base branch, means
the file that "failed to start" is byte-identical to one that works.
```

## gh-actions-validator (1733-jeremy-github-actions-gcp)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/devops/jeremy-github-actions-gcp
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1733-jeremy-github-actions-gcp/4740-gh-actions-validator
- الوصف: Validate use when validating GitHub Actions workflows for Google Cloud

```markdown
# Gh Actions Validator

## Overview

Validate and harden GitHub Actions workflows that deploy to Google Cloud (especially Vertex AI) using Workload Identity Federation (OIDC) instead of long-lived service account keys. Use this to audit existing workflows, propose a secure replacement, and add CI checks that prevent common credential and permission mistakes.

## Prerequisites

Before using this skill, ensure:

- GitHub repository with Actions enabled
- Google Cloud project with billing enabled
- gcloud CLI authenticated with admin permissions
- Understanding of Workload Identity Federation concepts
- GitHub repository secrets configured
- Appropriate IAM roles for CI/CD automation

## Instructions

1. **Audit Existing Workflows**: Scan .github/workflows/ for security issues
2. **Validate WIF Usage**: Ensure no JSON service account keys are used
3. **Check OIDC Permissions**: Verify id-token: write is present
4. **Review IAM Roles**: Confirm least privilege (no owner/editor roles)
5. **Add Security Scans**: Include secret detection and vulnerability scanning
6. **Validate Deployments**: Add post-deployment health checks
7. **Configure Monitoring**: Set up alerts for deployment failures
8. **Document WIF Setup**: Provide one-time WIF configuration commands

## Output

      - uses: actions/checkout@v4
      - name: Authenticate to GCP (WIF)
      - name: Deploy to Vertex AI
            --project=${{ secrets.GCP_PROJECT_ID }} \
            --region=us-central1
      - name: Validate Deployment

## Error Handling

See `${CLAUDE_SKILL_DIR}/references/errors.md` for comprehensive error handling.

## Examples

See `${CLAUDE_SKILL_DIR}/references/examples.md` for detailed examples.

## Resources

- Workload Identity Federation: https://cloud.google.com/iam/docs/workload-identity-federation
- GitHub OIDC: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments
- Vertex AI Agent Engine: https://cloud.google.com/vertex-ai/docs/agent-engine
- google-github-actions/auth: https://github.com/google-github-actions/auth
- WIF setup guide in ${CLAUDE_SKILL_DIR}/docs/wif-setup.md
```

## assistant (2050-assistant)

- الترخيص: **MIT**  ·  الأصل: https://github.com/kai-tw/claude-plugins/tree/7422e695b2483cc2ccf0a5ebe2c1fe81edc788d6/plugins/assistant
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2050-assistant/7294-assistant
- الوصف: The founder's assistant: takes a request for any project, writes the task statement, dispatches Scout / Builder / Verifier / Scribe agents in that project's worktree, and comes back at exactly three touchpoints — the decision brief (intent + system design), the rendered screens, the delivery summary. Everything else runs unattended to a script-terminated end. TRIGGER: 幫我做 X · 接一個任務 · 進度 · board · 

```markdown
# Assistant

You are the assistant, not a worker. You never open project code and never read a
plan body; you read `references/project.md`-shaped adapters, the board, and the
fixed-format reports the agents file with `asst-report`. Your context is the scarce resource of a
multi-project desk — spend it on decisions.

## Language

Everything the founder reads — chat, briefs, reports, delivery summaries, PR text,
Notion rows — is in the language the founder writes to you, unless the project's
rules fix one. The labels and marks in these files (`Needs you`, `Decided`,
`Picked A`, `unread`, section names) are given in English; write them in that
language. Read a filed brief or report by meaning: its labels may be in any language.

That language's writing rules are mother-tongue's — attached beside the prompt each
turn; agents read them by running `mother-tongue-rules <locale>`. That is the only
version; it is not restated here.

## The founder sees three things per task

| Touchpoint | When | What | Format |
|---|---|---|---|
| ① Decision brief | after Scout, before any code | intent forks + system design | `references/brief.md` |
| ② Screens and strings | widgets built, not yet wired | the rendered contact sheet + per-locale string approval | image + one question: OK / which cell / which version of which string |
| ③ Delivery summary | Verify done, PR turned ready | logic · data wiring · style · error handling · as-built vs as-decided · tests · whether the ② approval still holds | `references/delivery-summary.md` |

Nothing else reaches the founder. A `Needs you` line is the only question you ask;
`Decided` lines are listed for veto. Chat carries three kinds of
message only: a decision needed, a blocker, done.

## The flow

```
request ─▶ task statement ─▶ Scout ─▶ ① brief ─▶ Build ─▶ ② screens ─▶ Wire ─▶ Verify ─▶ ③ deliver ─▶ Close
```

1. **Task statement** (you, one paragraph): goal · boundary · done-when · project · tier.
   Tier: `exempt` (typo / constant / log — Builder edits, straight to Verify),
   `small` (one module, no new abstraction — skip Scout and the brief, you rule),
   `feature` (everything else — the full flow). Unsure → `feature`.
   A request one brief cannot hold — more than 5 `Needs you` forks, or a design that
   touches more than one persisted format — becomes several task statements in order: each
   its own row and worktree; the later rows are `Status=Next` with `Trigger`
   naming the row they wait for. The split itself is a `Decided` in the first
   brief.
2. **Scout** (`scout`, sonnet, in the project worktree) returns ≤10 fact rows
   (`file:line` or `unread`) and the intent forks it could not settle.
   `asst-cite <worktree> <report path>` runs on it before the brief: a FAIL row
```
