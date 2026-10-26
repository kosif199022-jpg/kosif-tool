# مصادر «خط إنتاج DaVinci Resolve الاحترافي» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## davinci-resolve (235-mas-video-lab)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alivirgo/major-ai-skills/tree/ba3a5729d60646626fee31c2d9906adc59f418dc/plugins/mas-video-lab
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/235-mas-video-lab/753-davinci-resolve
- الوصف: Automate DaVinci Resolve media and timelines with its scripting API, build Fusion workflows, and configure render jobs.

```markdown
# Blackmagic DaVinci Resolve Studio AI Skill Guide (Claude)

## Overview & Engine Architecture
Blackmagic Design DaVinci Resolve Studio 19 is an industry-leading post-production platform unifying non-linear editing (Cut/Edit), node-based Hollywood color grading (Color), node-based visual effects (Fusion VFX), professional audio mixing (Fairlight), and multi-format mastering (Deliver). Resolve operates on a **32-bit floating-point YRGB color engine**, supports wide-gamut color management (**ACEScc/ACEScct, DaVinci Wide Gamut Intermediate**), embeds the **DaVinci Neural Engine (AI Magic Mask, SuperScale, Speed Warp)**, and exposes complete pipeline automation via the **DaVinci Resolve Python/Lua Scripting API (`DaVinciResolveScript`)**. Claude operates as a Principal Post-Production Systems Architect and Resolve Pipeline Engineer, specializing in **Python Scripting API automation**, **GPU VRAM & CUDA memory management**, **color management transform pipelines**, and **headless batch delivery rendering**.

### DaVinci Resolve Multi-Page Pipeline & Scripting Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 DaVinci Resolve Architecture                │
│                                                             │
│  Post-Production Page Ecosystem                             │
│  ├── Media & Cut/Edit Pages (Multicam, Smart Bins, Timelines│
│  ├── Color Page (Node Graph, Serial/Parallel/Layer Nodes)   │
│  ├── Fusion Page (2D/3D VFX Compositing Node Tree, Particle)│
│  ├── Fairlight Page (2000-Track Audio Mixer, Bus FlexRouting│
│  └── Deliver Page (Render Queue, H.265, ProRes, IMF Master) │
│                                                             │
│  Compute Engine & Neural Acceleration                       │
│  ├── 32-bit Floating-Point YRGB & ACES Color Science Engine │
│  ├── DaVinci Neural Engine (CUDA, Metal, ROCm AI Shaders)   │
│  └── Multi-GPU Load Balancer & Dedicated Optical Flow Engine│
│                                                             │
│  Pipeline Automation & Developer API                        │
│  ├── DaVinci Resolve Scripting API (Python 3.10-3.12 / Lua) │
│  ├── `fuscript.exe` Standalone Script Execution Binary      │
│  └── PostgreSQL / SQLite Project Library Database Core      │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **DaVinci Resolve Python Scripting Automation**: Author Python scripts connecting via `DaVinciResolveScript` to inspect Project Managers, import media clips, assemble multi-track timelines, apply LUTs, and trigger Deliver page render queues.
```

## render-networking (2993-render)

- الترخيص: **MIT**  ·  الأصل: https://github.com/render-oss/render-plugin-claude-code/tree/e8f889396634dbc8c368448a7f3de993ed4a5ac1
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2993-render/12715-render-networking
- الوصف: Connects Render services over the private network—internal DNS, service discovery, and cross-service communication. Use when the user needs to wire services together, resolve internal hostnames, troubleshoot connectivity between services, configure environment isolation, or understand which services can reach each other.

```markdown
# Render private networking

Render’s **private network** lets services talk to each other without exposing traffic on the public internet. Use this skill when users need internal connectivity, discovery across scaled instances, or correct URL/port behavior for Blueprints and the Dashboard.

## When to Use This Skill

- Designing or debugging **service-to-service** traffic on Render
- Questions about **internal hostnames**, **internal URLs**, or **Connect > Internal** in the Dashboard
- **Service discovery** across multiple instances (custom load balancing, mesh-style setups)
- **Port limits**, reserved ports, or **multi-port** web services (public vs private)
- **Free-tier** web services and **who can send vs receive** private traffic
- **Environment isolation** (Professional+) or **AWS PrivateLink** for private egress/ingress patterns

For step-by-step architecture examples and Blueprint patterns, see `references/communication-patterns.md`. For failure modes and fixes, see `references/troubleshooting.md`.

## Private Network Basics

Private connectivity is available only when **all** of the following hold:

- Services are in the **same region**
- Services are in the **same workspace**

If either differs, private DNS and internal routing will not connect those services.

### Who can communicate

| Resource | Private inbound | Private outbound | Internal hostname |
|----------|-----------------|------------------|-------------------|
| **Web Service** | Yes (paid tiers; see Free tier below) | Yes | Yes |
| **Private Service** | Yes | Yes | Yes |
| **Background Worker** | No | Yes | No |
| **Cron Job** | No | Yes | No |
| **Workflow Run** | No | Yes | No |
| **Static Site** | — | — | **Not on private network** |
| **Managed Postgres** | Via internal URL (from allowed clients) | N/A (datastore) | Via internal URL |
| **Key Value** | Via internal URL (from allowed clients) | N/A (datastore) | Via internal URL |

**Free-tier Web Services:** They may **send** private traffic to other services, but they **cannot receive** inbound private traffic. Plan upgrades or topology changes apply if a free web service must accept private connections.

Workers, crons, and workflow runs initiate outbound connections (e.g., to internal URLs or private service hostnames) but are **not** reachable by internal hostname for inbound calls.

## Internal Addresses

- Open the service in the Render Dashboard → **Connect** → **Internal** tab for the canonical internal hostname, URL, and connection details.
- Clients often need an **explicit scheme** in code or config, e.g. `http://service-name:port` or `https://...` when TLS applies—do not assume a bare hostname alone is enough for every HTTP client.
```

## resolve-copilot-pr-feedback (1028-resolve-copilot-pr-feedback)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/plugins/resolve-copilot-pr-feedback
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1028-resolve-copilot-pr-feedback/2311-resolve-copilot-pr-feedback
- الوصف: Process GitHub Copilot PR review comments: fix, reply to, and resolve each thread. Use for "resolve copilot feedback" or "handle copilot comments".

```markdown
# Copilot Feedback Resolver

Process and resolve GitHub Copilot's automated PR review comments systematically.

## PR Comments Prohibition (CRITICAL)

**NEVER leave comments directly on GitHub PRs.** This is strictly forbidden:

- `gh pr review --comment` - FORBIDDEN
- `gh pr comment` - FORBIDDEN (except the single required final workflow summary in step 7)
- Any GraphQL mutation that creates new reviews or PR-level comments - FORBIDDEN
- Responding to human review comments - FORBIDDEN

**This skill ONLY processes Copilot-authored feedback**, whether it arrives as a review thread or as a finding in a Copilot review body. Never interact with threads created by human reviewers.

**Permitted operations:**

- Fetch unresolved Copilot threads using the script's `fetch` command
- Fetch Copilot review-body findings using the script's `fetch-reviews` command
- Read existing PR comments (never write them) to check for prior summaries
- Reply to EXISTING Copilot threads using the script's `reply` command
- Resolve Copilot threads using the script's `resolve` command
- Reply and resolve in one step using the script's `reply-and-resolve` command

**Single exception:** Step 7 uses `gh pr comment` with `--body-file` to post one required final workflow summary after terminal workflow state once PR context exists. This is the ONLY permitted use of `gh pr comment` in this skill. The final summary is blocking: if it cannot be posted, the workflow is incomplete.

## Script Setup

All GraphQL operations use a dedicated script that handles pagination, variable binding, and Copilot author filtering automatically.

The script ships with this plugin. Invoke it via `bash` followed by the quoted path:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve-copilot-threads" fetch OWNER REPO PR_NUMBER
```

Claude Code replaces the plugin-root placeholder with the installed plugin's absolute, version-correct directory before this file reaches you, so there is no search step and no need for a shell variable. Keeping `bash` as the command prefix keeps the command token stable across plugin versions, which is what permission allowlist rules match on.

**If the path was not substituted**, it still begins with `$` rather than `/`. Codex CLI substitutes the placeholder only in hook commands, and OpenCode does not substitute it at all. In that case locate the script with `**/resolve-copilot-pr-feedback/**/scripts/resolve-copilot-threads`, prefer a match inside the harness's own installed-plugin directory, ignore any match under a `.bak` or other backup directory, confirm it with `test -x`, and use that absolute path for the rest of the session.
```

## resolve-copilot-pr-feedback (965-resolve-copilot-pr-feedback)

- الترخيص: **MIT**  ·  الأصل: https://github.com/cboone/agent-harness-plugins/tree/d9e1b396852487c90500486a7b4fe94d88c64bd0/dist/codex/plugins/resolve-copilot-pr-feedback
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/965-resolve-copilot-pr-feedback/2249-resolve-copilot-pr-feedback
- الوصف: Process GitHub Copilot PR review comments: fix, reply to, and resolve each thread. Use for "resolve copilot feedback" or "handle copilot comments".

```markdown
# Copilot Feedback Resolver

Process and resolve GitHub Copilot's automated PR review comments systematically.

## PR Comments Prohibition (CRITICAL)

**NEVER leave comments directly on GitHub PRs.** This is strictly forbidden:

- `gh pr review --comment` - FORBIDDEN
- `gh pr comment` - FORBIDDEN (except the single required final workflow summary in step 7)
- Any GraphQL mutation that creates new reviews or PR-level comments - FORBIDDEN
- Responding to human review comments - FORBIDDEN

**This skill ONLY processes Copilot-authored feedback**, whether it arrives as a review thread or as a finding in a Copilot review body. Never interact with threads created by human reviewers.

**Permitted operations:**

- Fetch unresolved Copilot threads using the script's `fetch` command
- Fetch Copilot review-body findings using the script's `fetch-reviews` command
- Read existing PR comments (never write them) to check for prior summaries
- Reply to EXISTING Copilot threads using the script's `reply` command
- Resolve Copilot threads using the script's `resolve` command
- Reply and resolve in one step using the script's `reply-and-resolve` command

**Single exception:** Step 7 uses `gh pr comment` with `--body-file` to post one required final workflow summary after terminal workflow state once PR context exists. This is the ONLY permitted use of `gh pr comment` in this skill. The final summary is blocking: if it cannot be posted, the workflow is incomplete.

## Script Setup

All GraphQL operations use a dedicated script that handles pagination, variable binding, and Copilot author filtering automatically.

The script ships with this plugin. Invoke it via `bash` followed by the quoted path:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/resolve-copilot-threads" fetch OWNER REPO PR_NUMBER
```

Claude Code replaces the plugin-root placeholder with the installed plugin's absolute, version-correct directory before this file reaches you, so there is no search step and no need for a shell variable. Keeping `bash` as the command prefix keeps the command token stable across plugin versions, which is what permission allowlist rules match on.

**If the path was not substituted**, it still begins with `$` rather than `/`. Codex CLI substitutes the placeholder only in hook commands, and OpenCode does not substitute it at all. In that case locate the script with `**/resolve-copilot-pr-feedback/**/scripts/resolve-copilot-threads`, prefer a match inside the harness's own installed-plugin directory, ignore any match under a `.bak` or other backup directory, confirm it with `test -x`, and use that absolute path for the rest of the session.
```

## render-background-workers (2993-render)

- الترخيص: **MIT**  ·  الأصل: https://github.com/render-oss/render-plugin-claude-code/tree/e8f889396634dbc8c368448a7f3de993ed4a5ac1
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2993-render/12701-render-background-workers
- الوصف: Sets up and configures background workers on Render for queue-based job processing. Use when the user needs to process async jobs, consume from a queue, run Celery/Sidekiq/BullMQ/Asynq/Oban workers, handle graceful shutdown with SIGTERM, wire a worker to Key Value (Redis), or choose between workers and cron jobs for background work. Trigger terms: background worker, async jobs, queue consumer, Cel

```markdown
# Render Background Workers

This skill explains **worker** services on Render: processes that **consume jobs from a queue** instead of serving HTTP. Pair with **render-blueprints**, **render-env-vars**, and **render-networking** when wiring `render.yaml` and private connectivity.

## When to Use

- Designing or debugging **queue-backed workers** (Celery, Sidekiq, BullMQ, Asynq, etc.)
- Choosing between a **worker**, **Cron Job**, or **Workflow** for background work
- Configuring **Render Key Value** as a **broker** (not a cache) with correct **eviction policy**
- Implementing **graceful shutdown** so in-flight jobs are not lost on deploy

Per-framework setup and signal-handling detail: `references/queue-framework-setup.md`, `references/graceful-shutdown.md`.

## How Workers Work

- **Long-running services** with **no inbound (HTTP) traffic**. Render does not expose a public URL or internal hostname for workers the way it does for web or private services—**workers cannot receive private network traffic directed at them**.
- The typical pattern is a **poll loop**: the process connects to a **queue backend** (often **Render Key Value**, Redis-compatible **Valkey 8**) and **pulls jobs**.
- Workers **can initiate outbound connections** on the private network—to **PostgreSQL**, **Key Value**, **private services**, **web services** (internal URLs), and the public internet—subject to your plan and firewall rules.

## Queue Framework Overview

| Framework | Language | Queue backend | Notes |
|-----------|----------|---------------|--------|
| Celery | Python | Redis / Key Value | Most common Python task queue |
| Sidekiq | Ruby | Redis / Key Value | Standard for Rails |
| BullMQ | Node.js | Redis / Key Value | Modern Node queue (Redis-based) |
| Asynq | Go | Redis / Key Value | Go async task processing |
| Oban | Elixir | **Postgres** (not Redis) | Queue stored in the database |

## Pairing with Key Value

- Use **Render Key Value** as the **job broker** when your framework expects Redis.
- Set **maxmemory policy** to **`noeviction`**. **`allkeys-lru`** and similar policies are for **caches**; evicting queue keys **drops jobs**.
- Wire **`REDIS_URL`** (or your framework’s equivalent) via **`fromService`** with `type: keyvalue` and `property: connectionString` in the Blueprint.
- **Blueprints require `ipAllowList`** on Key Value—include the CIDRs that should reach the instance (often `[]` for private-network-only access; see **render-blueprints** / Key Value field reference).

See `references/queue-framework-setup.md` for minimal app + YAML examples.

## Worker vs Cron vs Workflow

| Need | Use | Why |
|------|-----|-----|
| Always-on queue consumer | **Background Worker** | Polls continuously; long-lived process |
```

## render-blueprints (889-render)

- الترخيص: **MIT**  ·  الأصل: https://github.com/blockchainian/claude/tree/0e53403fa614c5162b54ed0149cb7720ca1414a9/plugins/render
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/889-render/2002-render-blueprints
- الوصف: Authors and validates render.yaml Blueprints for Render infrastructure. Use when the user needs to write or edit a render.yaml, wire services together with fromDatabase/fromService/fromGroup, set up projects and environments for multi-service apps, configure preview environments, validate against the schema, or fix immutable field errors. Trigger terms: render.yaml, Blueprint, IaC, fromDatabase, f

```markdown
# Render Blueprints (render.yaml)

Blueprints define Render infrastructure as YAML (commonly `render.yaml` at the repo root). This skill focuses on **authoring**, **wiring**, **projects/environments**, **previews**, **validation**, and **immutable fields**. Heavy detail lives under `references/`.

## When to Use

Apply this skill when the user:

- Creates or edits a `render.yaml` / Blueprint
- Wires databases, private services, or Key Value into app env vars
- Groups services with **projects** and **environments**
- Configures **preview environments** for pull requests
- Validates YAML against Render’s schema or CLI
- Asks what can or cannot change after a resource is created

For end-to-end deploy flows and MCP/CLI operations, see **render-deploy**. For env var strategy outside Blueprint syntax, see **render-env-vars**. For Docker-specific Blueprint fields, see **render-docker**.

## Blueprint Structure

### Top-level keys

| Key | Purpose |
|-----|---------|
| `services` | Web, worker, cron, private service, Key Value, static (via `web` + `runtime: static`) |
| `databases` | Managed PostgreSQL instances |
| `envVarGroups` | Reusable env var sets attached to services |
| `projects` | Optional grouping; contains `environments` and service lists |
| `previews` | Defaults for PR preview environments |

A Blueprint may also use patterns like **ungrouped** resources vs **environment-scoped** lists, depending on whether you adopt the projects model. Avoid duplicating the same logical resource in multiple places (see `references/common-mistakes.md`).

### Schema and IDE validation

- **JSON Schema URL:** `https://render.com/schema/render.yaml.json`
- Configure your editor to associate `render.yaml` with that schema for completions and diagnostics.

### Minimal example: web + PostgreSQL

```yaml
databases:
  - name: mydb
    plan: basic-256mb
    region: oregon

services:
  - type: web
    name: api
    runtime: node
    region: oregon
    plan: starter
    buildCommand: npm ci && npm run build
    startCommand: npm start
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: mydb
          property: connectionString
```

## Service Types

| `type` | Role |
|--------|------|
| `web` | Public HTTP service (use `runtime: static` for static sites) |
| `pserv` | Private service (internal HTTP/TCP; not public) |
| `worker` | Long-running background process |
| `cron` | Scheduled job (`schedule` required) |
| `keyvalue` | Managed Key Value (Redis-compatible); alias **`redis`** accepted in Blueprints |

## Runtimes

Common `runtime` values: **`node`**, **`python`**, **`go`**, **`ruby`**, **`rust`**, **`elixir`**, **`docker`**, **`image`**, **`static`**.
```
