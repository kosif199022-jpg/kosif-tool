# مصادر «مهندس برومبتات النظام» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## persona-exec-assistant (2907-google-workspace)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/google-workspace
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2907-google-workspace/11838-persona-exec-assistant
- الوصف: Manage an executive's schedule, inbox, and communications.

```markdown
# Executive Assistant

> **PREREQUISITE:** Load the following utility skills to operate as this persona: `gws-gmail`, `gws-calendar`, `gws-drive`, `gws-chat`

Manage an executive's schedule, inbox, and communications.

## Relevant Workflows
- `gws workflow +standup-report`
- `gws workflow +meeting-prep`
- `gws workflow +weekly-digest`

## Instructions
- Start each day with `gws workflow +standup-report` to get the executive's agenda and open tasks.
- Before each meeting, run `gws workflow +meeting-prep` to see attendees, description, and linked docs.
- Triage the inbox with `gws gmail +triage --max 10` — prioritize emails from direct reports and leadership.
- Schedule meetings with `gws calendar +insert` — always check for conflicts first using `gws calendar +agenda`.
- Draft replies with `gws gmail +send` — keep tone professional and concise.

## Tips
- Always confirm calendar changes with the executive before committing.
- Use `--format table` for quick visual scans of agenda and triage output.
- Check `gws calendar +agenda --week` on Monday mornings for weekly planning.
```

## persona-exec-assistant (2907-google-workspace)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/google-workspace
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2907-google-workspace/11933-persona-exec-assistant
- الوصف: Manage an executive's schedule, inbox, and communications.

```markdown
# Executive Assistant

> **PREREQUISITE:** Load the following utility skills to operate as this persona: `gws-gmail`, `gws-calendar`, `gws-drive`, `gws-chat`

Manage an executive's schedule, inbox, and communications.

## Relevant Workflows
- `gws workflow +standup-report`
- `gws workflow +meeting-prep`
- `gws workflow +weekly-digest`

## Instructions
- Start each day with `gws workflow +standup-report` to get the executive's agenda and open tasks.
- Before each meeting, run `gws workflow +meeting-prep` to see attendees, description, and linked docs.
- Triage the inbox with `gws gmail +triage --max 10` — prioritize emails from direct reports and leadership.
- Schedule meetings with `gws calendar +insert` — always check for conflicts first using `gws calendar +agenda`.
- Draft replies with `gws gmail +send` — keep tone professional and concise.

## Tips
- Always confirm calendar changes with the executive before committing.
- Use `--format table` for quick visual scans of agenda and triage output.
- Check `gws calendar +agenda --week` on Monday mornings for weekly planning.
```

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

## persona-ci-integration (1892-persona-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/persona-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1892-persona-pack/6497-persona-ci-integration
- الوصف: Build Persona CI around offline contract fixtures and bounded sandbox smoke tests without production identity data. Use when adding integration gates. Trigger with: "test Persona in CI", "Persona contract tests", "Persona GitHub Actions".

```markdown
# Contract-Safe Persona CI

## Overview

Keep the required CI gate deterministic and secret-minimal. Offline fixtures validate JSON:API, version, idempotency, webhook HMAC, replay, and unknown additions; an optional protected sandbox job proves connectivity without making production a test dependency.

## Prerequisites

- Repository test conventions and required status names
- Redacted signed fixtures for REST and webhook contracts
- Protected sandbox secret scope and synthetic test identities

## Instructions

### Step 1: Define the offline denominator

List parsers, commands, event transitions, security checks, error envelopes, pagination, and compatible-addition cases that must run on every change.

### Step 2: Pin contract provenance

Record source URLs, retrieval date, split fingerprints, API version, template context, and redaction method for every fixture.

### Step 3: Test mutations safely

Assert operation IDs, idempotency-key reuse only with identical parameters, timeout reconciliation, and no automatic duplicate inquiry.

### Step 4: Test webhook adversaries

Cover modified raw body, stale timestamp, multiple `v1` candidates, constant-time comparison, duplicates, reordering, and unknown event types.

### Step 5: Isolate the sandbox smoke lane

Run only for trusted branches, use a sandbox key, create a unique synthetic inquiry, cap calls, and retain redacted evidence.

### Step 6: Fail closed on leaks and drift

Scan fixtures and logs for key, token, signature, PII, and wrong-host patterns; make unexplained contract drift fail the gate.

## Authentication

Required offline tests use no live credential. The optional protected job uses only a sandbox bearer key and sandbox webhook secret supplied by the CI secret store.

## Tool Discipline

Use Read and Grep to inspect application configuration, provider documentation, fixtures, schemas, tests, and redacted operational evidence before proposing a change. Use Write or Edit only for an approved implementation, configuration, test, runbook, or redacted receipt. Do not create, resume, approve, decline, redact, rotate, revoke, deploy, or otherwise mutate production Persona resources without explicit operator approval.

## Output

- Required offline contract-test suite
- Protected optional sandbox-smoke workflow
- Fixture provenance, drift, and redaction receipts

Return the environment, resource and event identifiers, API version, template context, source-contract fingerprint, evidence, unresolved risk, rollback state, and final decision without exposing bearer keys, webhook secrets, inquiry session tokens, raw identity documents, or unnecessary PII.

## Examples
```

## persona-common-errors (1892-persona-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/persona-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1892-persona-pack/6498-persona-common-errors
- الوصف: Triage Persona authentication, JSON:API, inquiry, session, webhook, and throttle failures with redacted evidence. Use when an integration is failing. Trigger with: "debug Persona error", "Persona 401", "Persona inquiry failed".

```markdown
# Persona API and Inquiry Failure Triage

## Overview

Diagnose from the outer boundary inward: environment and credentials, request contract, resource lifecycle, session state, webhook authenticity, then provider limits. Preserve the original status and request evidence while keeping identity data out of logs.

## Prerequisites

- Timestamp, environment, endpoint, status, and provider request identifier
- Redacted request fingerprint and relevant inquiry or event ID
- Access to current Dashboard configuration and application logs

## Instructions

### Step 1: Freeze the evidence

Record UTC time, method, canonical host and path, API version, status, request ID, idempotency key hash, and response-body hash.

### Step 2: Check environment and auth

Confirm `api.withpersona.com`, the target environment, key state, permissions, and explicit version. A 401 is not fixed by printing or widening the key.

### Step 3: Validate the request envelope

Check JSON:API shape, template selector, content headers, account auto-create metadata, and replay parameters.

### Step 4: Reconcile lifecycle state

Read the inquiry before retrying a create, resume, or transition. Distinguish pending, terminal, redacted, and unavailable resources.

### Step 5: Verify event intake

Use raw bytes, timestamp-plus-dot-plus-body HMAC, all `v1` candidates, constant-time compare, event-ID dedupe, and creation-time ordering.

### Step 6: Respect limit signals

Read live `RateLimit-*` and `Quota-*` headers and Dashboard product quotas. On 429, reduce the responsible lane and use bounded backoff.

## Authentication

Authenticate REST diagnostics with the correct environment bearer key and webhook diagnostics with the endpoint’s signing secret. Redact both before creating a ticket or debug bundle.

## Tool Discipline

Use Read and Grep to inspect application configuration, provider documentation, fixtures, schemas, tests, and redacted operational evidence before proposing a change. Use Write or Edit only for an approved implementation, configuration, test, runbook, or redacted receipt. Do not create, resume, approve, decline, redact, rotate, revoke, deploy, or otherwise mutate production Persona resources without explicit operator approval.

## Output

- Ranked root-cause hypothesis with evidence
- Safe retry, reconciliation, or manual-review action
- Redacted escalation packet and unresolved risks

Return the environment, resource and event identifiers, API version, template context, source-contract fingerprint, evidence, unresolved risk, rollback state, and final decision without exposing bearer keys, webhook secrets, inquiry session tokens, raw identity documents, or unnecessary PII.

## Examples
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
