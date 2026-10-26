# مصادر «أتمتة Google Workspace» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## google-workspace-cli (150-google-workspace-cli)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alirezarezvani/claude-skills/tree/19392f7a08264ed00486a251f5b2098321771f94/engineering-team/google-workspace-cli
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/150-google-workspace-cli/493-google-workspace-cli
- الوصف: Google Workspace administration via the gws CLI (github.com/googleworkspace/cli). Install, authenticate, and automate Gmail, Drive, Sheets, Calendar, Docs, Chat, and Tasks. Run security audits and use local recipe templates and persona bundles. Use for Google Workspace admin, gws CLI setup, Gmail automation, Drive management, or Calendar scheduling.

```markdown
# Google Workspace CLI

Expert guidance and automation for Google Workspace administration using the open-source `gws` CLI ([github.com/googleworkspace/cli](https://github.com/googleworkspace/cli), Apache-2.0). The CLI builds its command surface dynamically from Google's Discovery Service, so it covers every supported Workspace API plus `+`-prefixed helper commands. This skill adds local Python tools (doctor, auth guide, recipe catalog, security audit, output analyzer).

> **Verify before scripting:** `gws` generates commands at runtime from Google's API discovery documents, and the CLI is pre-v1.0. Always confirm a command's exact surface with `gws --help`, `gws <service> --help`, or `gws schema <service>.<resource>.<method>` before putting it in automation. Commands in this skill marked *(verify)* are illustrative of the `gws <service> <resource> <method>` pattern and must be checked against your installed version.

---

## Quick Start

### Check Installation

```bash
# Verify gws is installed and authenticated
python3 scripts/gws_doctor.py
```

### Send an Email

```bash
gws gmail +send --to "team@company.com" \
  --subject "Weekly Update" --body "Here's this week's summary..."
```

### List Drive Files

```bash
gws drive files list --params '{"pageSize": 20}' | python3 scripts/output_analyzer.py --select "name,mimeType,modifiedTime" --format table
```

---

## Installation

### npm (recommended; requires Node.js 18+)

```bash
npm install -g @googleworkspace/cli
gws --version
```

### Homebrew (macOS/Linux)

```bash
brew install googleworkspace-cli
```

### Cargo (from source)

```bash
cargo install --git https://github.com/googleworkspace/cli --locked
gws --version
```

### Pre-built Binaries

Download from [github.com/googleworkspace/cli/releases](https://github.com/googleworkspace/cli/releases) for macOS, Linux, or Windows. Nix users: `nix run github:googleworkspace/cli`.

### Verify Installation

```bash
python3 scripts/gws_doctor.py
# Checks: PATH, version, auth status, service connectivity
```

---

## Authentication

### OAuth Setup (Interactive)

```bash
# Step 1: Create Google Cloud project and OAuth credentials
python3 scripts/auth_setup_guide.py --guide oauth

# Step 2: Run interactive auth setup (uses gcloud if available)
gws auth setup

# Step 3: Log in, requesting only the scopes you need
gws auth login -s drive,gmail,sheets
```

### Headless/CI

```bash
# Generate setup instructions
python3 scripts/auth_setup_guide.py --guide service-account

# Export credentials from an interactive machine, then point the CLI at them
gws auth export --unmasked > credentials.json
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=/path/to/credentials.json
```

### Environment Variables

```bash
# Generate .env template
```

## google-drive (2700-google-drive)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/google-drive
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2700-google-drive/10373-google-drive
- الوصف: Use connected Google Drive as the single entrypoint for Drive, Docs, Sheets, and Slides work. Use when the user wants to find, fetch, organize, share, export, copy, or delete Drive files, or summarize and edit Google Docs, Google Sheets, and Google Slides through one unified Google Drive plugin.

```markdown
# Google Drive

Use this as the top-level router for Google file work inside the unified Google Drive plugin. Do not route the user toward separate Google Docs, Google Sheets, or Google Slides plugins.

Start with Google Drive for file discovery and file lifecycle tasks, then route to narrower sibling skills only when the task becomes specific to Docs, Sheets, or Slides.

## Workflow

1. Ground the target file first.
- If the user did not provide an exact file URL or ID, use Google Drive search, recent files, folder listing, or metadata reads to identify the right file.
- If the request starts as "find X and then update it," do the Drive discovery step first instead of guessing the target.

2. Stay in the base Google Drive workflow for Drive-native tasks.
- Use the base workflow for search, fetch, recent files, folders, sharing, copying, deleting, exporting, revision history, file moves, and other file-lifecycle work that is not primarily about editing Docs, Sheets, or Slides content.
- For version-history requests, including "previous version," "revision history," "what changed since the last version," or "compare to the prior revision," ground the file, fetch the current content, use `list_file_revisions`, fetch the immediately previous revision or the user-named revision with `fetch_file_revision`, then compare the fetched revision against the current content. Do not say previous versions are unsupported until you have checked whether revision tools are available for the target file.
- For file move requests, ground the source file and target folder, read the file metadata including its current parents, then use `update_file` with `addParents` for the target folder and `removeParents` for only the verified source parent or parents that should no longer contain it. Preserve unrelated parents, and verify the move by reading metadata or listing the target folder before the final response.
```

## gws-gmail-forward (2907-google-workspace)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/google-workspace
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2907-google-workspace/11806-gws-gmail-forward
- الوصف: Gmail: Forward a message to new recipients.

```markdown
# gmail +forward

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

Forward a message to new recipients

## Usage

```bash
gws gmail +forward --message-id <ID> --to <EMAILS>
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--message-id` | ✓ | — | Gmail message ID to forward |
| `--to` | ✓ | — | Recipient email address(es), comma-separated |
| `--from` | — | — | Sender address (for send-as/alias; omit to use account default) |
| `--body` | — | — | Optional note to include above the forwarded message (plain text, or HTML with --html) |
| `--no-original-attachments` | — | — | Do not include file attachments from the original message (inline images in --html mode are preserved) |
| `--attach` | — | — | Attach a file (can be specified multiple times) |
| `--cc` | — | — | CC email address(es), comma-separated |
| `--bcc` | — | — | BCC email address(es), comma-separated |
| `--html` | — | — | Treat --body as HTML content (default is plain text) |
| `--dry-run` | — | — | Show the request that would be sent without executing it |
| `--draft` | — | — | Save as draft instead of sending |

## Examples

```bash
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --body 'FYI see below'
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --cc eve@example.com
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --body '<p>FYI</p>' --html
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com -a notes.pdf
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --no-original-attachments
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --draft
```

## Tips

- Includes the original message with sender, date, subject, and recipients.
- Original attachments are included by default (matching Gmail web behavior).
- With --html, inline images are also preserved via cid: references.
- In plain-text mode, inline images are not included (matching Gmail web).
- Use --no-original-attachments to forward without the original message's files.
- Use -a/--attach to add extra file attachments. Can be specified multiple times.
- Combined size of original and user attachments is limited to 25MB.
- With --html, the forwarded block uses Gmail's gmail_quote CSS classes and preserves HTML formatting. Use fragment tags (<p>, <b>, <a>, etc.) — no <html>/<body> wrapper needed.
- Use --draft to save the forward as a draft instead of sending it immediately.

## See Also

- [gws-shared](../gws-shared/SKILL.md) — Global flags and auth
```

## gws-gmail-read (2907-google-workspace)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/google-workspace
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2907-google-workspace/11807-gws-gmail-read
- الوصف: Gmail: Read a message and extract its body or headers.

```markdown
# gmail +read

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

Read a message and extract its body or headers

## Usage

```bash
gws gmail +read --id <ID>
```

## Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--id` | ✓ | — | The Gmail message ID to read |
| `--headers` | — | — | Include headers (From, To, Subject, Date) in the output |
| `--format` | — | text | Output format (text, json) |
| `--html` | — | — | Return HTML body instead of plain text |
| `--dry-run` | — | — | Show the request that would be sent without executing it |

## Examples

```bash
gws gmail +read --id 18f1a2b3c4d
gws gmail +read --id 18f1a2b3c4d --headers
gws gmail +read --id 18f1a2b3c4d --format json | jq '.body'
```

## Tips

- Converts HTML-only messages to plain text automatically.
- Handles multipart/alternative and base64 decoding.

## See Also

- [gws-shared](../gws-shared/SKILL.md) — Global flags and auth
- [gws-gmail](../gws-gmail/SKILL.md) — All send, read, and manage email commands
```

## session-workspace (1334-session-workspace)

- الترخيص: **MIT**  ·  الأصل: https://github.com/devgirishattri/agent-plugins/tree/12fa4f331b3792bbe48d59bebcdc010eac295333/codex/plugins/session-workspace
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1334-session-workspace/3012-session-workspace
- الوصف: When and how to use session-workspace lifecycle commands, its strict-v1 multi-agent harness, and schema-v4 reviewed Git orchestration. Use before workspace/harness commands or workspace-orchestrator so you understand the config model, safety gates, and provider-neutral coordination boundary.

```markdown
# session-workspace: config-driven tmux workspace engine

`session-workspace` is a shared engine that replaces hand-maintained
per-project `workspace.sh` launchers. Instead of six near-identical scripts
drifting independently, one engine reads a versioned, project-local
`.agent-workspace/workspace.json` config and drives tmux session/window/pane
lifecycle from it.

**Current status: fully implemented.** Config load/validation, mutation-free
planning, runtime argv/env construction, and tmux session/pane lifecycle
(create, adopt, reconcile, stop, restart) are all live and enforced — this
is not a scaffold.

## Commands

| Command | Purpose |
|---|---|
| `/workspace-doctor` | Read-only dependency/config health check |
| `/workspace-plan` | Dry-run plan (human + JSON); mutates nothing |
| `/workspace-start` | Bring up sessions/panes/agents/services (idempotent) |
| `/workspace-status` | Current lifecycle state; mutates nothing |
| `/workspace-stop` | Tear down sessions/panes (destructive, needs `--confirmed`) |
| `/workspace-restart` | Stop then start (destructive, confirmation implicit) |
| `/workspace-reconcile` | Dry-run by default; `--apply` repairs drift; `--adopt --confirmed` claims unmanaged panes |
| `/workspace-install` | Install/refresh the machine-wide `workspace` dispatcher on PATH; no config, no tmux, idempotent |
| `/workspace-browser-config` | Render/apply project MCP entries for the configured browser |
| `/harness-status` | Read-only: is the opt-in harness active (mode/profile/roles/gates), and does this pane's engine identity match the plan |
| `/harness-doctor` | Read-only harness health: config validity, activation, hook registration, python3, live identity match |
| `$session-workspace:workspace-orchestrator` | Schema-v4 status/plan/dispatch/review/commit/push/deploy lifecycle using configured executor/reviewer pairs |

## Configuration model (enforced)

A project opts in by creating `.agent-workspace/workspace.json`
(`schema_version: 1`, `2` for the optional harness, `3` for shared guard packs,
or `4` for reviewed orchestration) describing:

- `project` — id/display name/root
- `runtimes` — named launch profiles (e.g. `claude`, `codex`), replacing any
  free-form custom-command entry
- `roles` — per-role runtime, optional `agent.{model,effort,profile}`,
  `--add-dir` grants, env group
- `stores` — which coordination stores (`messages`, `scheduler`, `contexts`)
  get exported/session-pinned, plus memory topology (`shared` vs `per-pane`)
- `sessions[].panes[]` — declarative session/window/pane plan, including a
  `split_tree` layout kind for hand-built layouts a named layout can't
  express, and `optional: true` for a pane whose `cwd` may not exist yet (an
  un-cloned child repo) — such a pane is skipped, never launched with a
```

## workspace-doctor (1334-session-workspace)

- الترخيص: **MIT**  ·  الأصل: https://github.com/devgirishattri/agent-plugins/tree/12fa4f331b3792bbe48d59bebcdc010eac295333/codex/plugins/session-workspace
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1334-session-workspace/3014-workspace-doctor
- الوصف: Dependency/config health check for the session-workspace engine. Use when the user asks to check workspace health, diagnose session-workspace, or verify config/dependencies.

```markdown
# workspace-doctor

When this skill is invoked, do not add a preamble or narrate the plan. Run
the relevant script directly, then return only the formatted result.

Resolve `PLUGIN_ROOT` from this selected skill's installed source path: it
is the directory two levels above this `SKILL.md`. Use that absolute path;
never infer it from cwd or hardcode a marketplace cache version.

Run:

```bash
bash "$PLUGIN_ROOT/scripts/workspace-doctor.sh" $ARGUMENTS
```

Real flags:
- `--config PATH`: use a specific workspace config instead of discovery.
- `--json`: emit the health report as JSON.

`workspace-doctor` is strictly read-only: it diagnoses and never repairs,
creates, starts, stops, attaches, or kills anything. It does not execute
config-supplied runtime programs; runtime checks use `command -v` only.

It checks required tooling (tmux >= 3.2, jq, git), config discovery + full
validation, plugin dependency versions and cache-vs-source drift, pane cwds,
secret-file metadata gates, state-dir availability, runtime availability,
coordination-base drift, and session-chat helper resolution.

Each check reports `OK`, `INFO`, `WARN`, or `ERROR` with remediation text; the
script exits non-zero only when at least one check is `ERROR`. Relay the
per-check statuses and remediation lines. Do not run suggested fixes yourself
unless the user asks.
```
