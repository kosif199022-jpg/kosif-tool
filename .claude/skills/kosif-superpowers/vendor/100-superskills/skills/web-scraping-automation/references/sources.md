# مصادر «جمع البيانات من الويب» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## playwright (1251-playwright)

- الترخيص: **MIT**  ·  الأصل: https://github.com/dashed/claude-marketplace/tree/f6a24dbc08da57aeb80e7423da2508457d0b3398/plugins/playwright
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1251-playwright/2931-playwright
- الوصف: Browser automation with Playwright for Python. Use when testing websites, taking screenshots, filling forms, scraping web content, or automating browser interactions. Triggers on browser, web testing, screenshots, selenium, puppeteer, or playwright.

```markdown
# Playwright Browser Automation

## Overview

Playwright enables browser automation for web testing, screenshots, form filling, and scraping. This skill uses Python with `uv` for self-contained scripts that require no global installation.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- Playwright browser binaries (one-time setup)

## Setup (First Time Only)

> **Claude: Do not run browser installation commands directly.** Suggest these commands to the user and let them run manually. This is a one-time setup that downloads ~200MB of browser binaries.

Suggest the user run:

```bash
# Install Chromium (recommended, ~200MB)
uv run --with playwright playwright install chromium

# Or install all browsers
uv run --with playwright playwright install
```

To verify installation:
```bash
uv run /path/to/plugins/playwright/scripts/check_setup.py
```

## Quick Start

Take a screenshot of any URL:

```bash
uv run /path/to/plugins/playwright/scripts/screenshot.py https://example.com
```

Output: `/tmp/screenshot-{timestamp}.png`

## Common Patterns

### Take a Screenshot

```bash
# Default (visible browser)
uv run scripts/screenshot.py https://example.com

# Full page, headless
uv run scripts/screenshot.py https://example.com --full-page --headless

# Custom output path
uv run scripts/screenshot.py https://example.com -o /tmp/my-shot.png
```

### Navigate and Extract Content

```bash
# Get page title and URL
uv run scripts/navigate.py https://example.com

# Extract all links as JSON
uv run scripts/navigate.py https://example.com --links

# Get page text content
uv run scripts/navigate.py https://example.com --text
```

### Fill and Submit Forms

```bash
uv run scripts/fill_form.py https://example.com/login \
  --field "email=test@example.com" \
  --field "password=secret123" \
  --submit
```

### Execute JavaScript

```bash
uv run scripts/evaluate.py https://example.com "document.title"
uv run scripts/evaluate.py https://example.com "document.querySelectorAll('a').length"
```

## Writing Custom Scripts

Save this template to `/tmp/my-automation.py`:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.56.0"]
# ///
"""Custom Playwright automation script."""

import os
import sys
from playwright.sync_api import sync_playwright

HEADLESS = os.getenv("HEADLESS", "0").lower() in ("1", "true", "yes")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        try:
            page.goto("https://example.com")
            print(f"Title: {page.title()}")

            # Use semantic locators (preferred)
            page.get_by_role("button", name="Submit").click()
```

## 286-browser-automation (112-browser)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alexei-led/cc-thingz/tree/ce56bb43c7f803a192be038135c5e2bb4cd2249f/dist/claude/browser
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/112-browser/286-browser-automation
- الوصف: 

```markdown
# Browser Automation

Prove rendered behavior in a real browser and report pass, fail, or blocked with
evidence. Keep automation temporary unless the user asks for permanent tests.

## Runtime

Use the cheapest runtime that proves the claim:

1. Browser tools exposed in the current session. See
   [`references/platform-browser-tools.md`](references/platform-browser-tools.md).
2. The project's configured browser runner. Infer the package manager from the
   lockfile; do not invent a runner.
3. The bundled Playwright scripts in this skill's `scripts/` directory. Read
   [`references/playwright.md`](references/playwright.md) for setup, the script
   skeleton, helpers, and custom headers.
4. None available: report blocked and name the missing tool or package.

## Rules

- Target: reuse a reachable dev server; start one only when its command is
  known. Ask when no server or several servers are found.
- Data: use seeded users, fixed dates, reset state, and mocked external
  services. Credentials, production data, and destructive actions need explicit
  user approval.
- Locators: role, label, text, or test id first; CSS last.
- Waiting: wait on observable state such as a selector, URL, network response,
  or accessibility snapshot. Never add fixed sleeps. For SPA or HTMX pages,
  assert the DOM after swaps and client-side route changes.
- Headless: when the platform exposes no visible browser (Pi, CI, most CLIs),
  use headless screenshots plus a manifest as visual evidence. Use headed mode
  only when the user can see the browser.
- Files: write generated scripts and artifacts to `/tmp/playwright-*`. Write to
  the project only when the user asked for permanent tests, and never write into
  the skill directory.
- Failures: fix the app or tests only when that is in scope. After two failed
  scoped attempts, save evidence, quote the failing line or UI state, and stop.
- Permanent tests: done when the relevant build/test/lint checks pass on what
  you changed, or you name each check that did not run and why.

## Bundled Playwright scripts

Run them by absolute path from the caller's working directory, where
`<skill-dir>` is the directory that contains this `SKILL.md`. Prefer the
screenshot scripts over custom batch scripts:

```bash
node <skill-dir>/scripts/screenshot-url.js --url <url> --selector <ready-selector> \
  --out /tmp/playwright-page.png --json
node <skill-dir>/scripts/screenshot-sequence.js --url-template '<url/{n}>' --from 1 --to 10 \
  --selector <ready-selector> --out-dir /tmp/playwright-shots --json
node <skill-dir>/scripts/run.js --json /tmp/playwright-check.js
```

- Manifests record URL, title, screenshot path, viewport, console errors,
  network failures, and HTTP responses with status >=400.
```

## 313-browser-automation (119-browser)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alexei-led/cc-thingz/tree/ce56bb43c7f803a192be038135c5e2bb4cd2249f/dist/codex/browser
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/119-browser/313-browser-automation
- الوصف: 

```markdown
# Browser Automation

Prove rendered behavior in a real browser and report pass, fail, or blocked with
evidence. Keep automation temporary unless the user asks for permanent tests.

## Runtime

Use the cheapest runtime that proves the claim:

1. Browser tools exposed in the current session. See
   [`references/platform-browser-tools.md`](references/platform-browser-tools.md).
2. The project's configured browser runner. Infer the package manager from the
   lockfile; do not invent a runner.
3. The bundled Playwright scripts in this skill's `scripts/` directory. Read
   [`references/playwright.md`](references/playwright.md) for setup, the script
   skeleton, helpers, and custom headers.
4. None available: report blocked and name the missing tool or package.

## Rules

- Target: reuse a reachable dev server; start one only when its command is
  known. Ask when no server or several servers are found.
- Data: use seeded users, fixed dates, reset state, and mocked external
  services. Credentials, production data, and destructive actions need explicit
  user approval.
- Locators: role, label, text, or test id first; CSS last.
- Waiting: wait on observable state such as a selector, URL, network response,
  or accessibility snapshot. Never add fixed sleeps. For SPA or HTMX pages,
  assert the DOM after swaps and client-side route changes.
- Headless: when the platform exposes no visible browser (Pi, CI, most CLIs),
  use headless screenshots plus a manifest as visual evidence. Use headed mode
  only when the user can see the browser.
- Files: write generated scripts and artifacts to `/tmp/playwright-*`. Write to
  the project only when the user asked for permanent tests, and never write into
  the skill directory.
- Failures: fix the app or tests only when that is in scope. After two failed
  scoped attempts, save evidence, quote the failing line or UI state, and stop.
- Permanent tests: done when the relevant build/test/lint checks pass on what
  you changed, or you name each check that did not run and why.

## Bundled Playwright scripts

Run them by absolute path from the caller's working directory, where
`<skill-dir>` is the directory that contains this `SKILL.md`. Prefer the
screenshot scripts over custom batch scripts:

```bash
node <skill-dir>/scripts/screenshot-url.js --url <url> --selector <ready-selector> \
  --out /tmp/playwright-page.png --json
node <skill-dir>/scripts/screenshot-sequence.js --url-template '<url/{n}>' --from 1 --to 10 \
  --selector <ready-selector> --out-dir /tmp/playwright-shots --json
node <skill-dir>/scripts/run.js --json /tmp/playwright-check.js
```

- Manifests record URL, title, screenshot path, viewport, console errors,
  network failures, and HTTP responses with status >=400.
```

## 340-browser-automation (126-browser)

- الترخيص: **MIT**  ·  الأصل: https://github.com/alexei-led/cc-thingz/tree/ce56bb43c7f803a192be038135c5e2bb4cd2249f/dist/grok/browser
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/126-browser/340-browser-automation
- الوصف: 

```markdown
# Browser Automation

Prove rendered behavior in a real browser and report pass, fail, or blocked with
evidence. Keep automation temporary unless the user asks for permanent tests.

## Runtime

Use the cheapest runtime that proves the claim:

1. Browser tools exposed in the current session. See
   [`references/platform-browser-tools.md`](references/platform-browser-tools.md).
2. The project's configured browser runner. Infer the package manager from the
   lockfile; do not invent a runner.
3. The bundled Playwright scripts in this skill's `scripts/` directory. Read
   [`references/playwright.md`](references/playwright.md) for setup, the script
   skeleton, helpers, and custom headers.
4. None available: report blocked and name the missing tool or package.

## Rules

- Target: reuse a reachable dev server; start one only when its command is
  known. Ask when no server or several servers are found.
- Data: use seeded users, fixed dates, reset state, and mocked external
  services. Credentials, production data, and destructive actions need explicit
  user approval.
- Locators: role, label, text, or test id first; CSS last.
- Waiting: wait on observable state such as a selector, URL, network response,
  or accessibility snapshot. Never add fixed sleeps. For SPA or HTMX pages,
  assert the DOM after swaps and client-side route changes.
- Headless: when the platform exposes no visible browser (Pi, CI, most CLIs),
  use headless screenshots plus a manifest as visual evidence. Use headed mode
  only when the user can see the browser.
- Files: write generated scripts and artifacts to `/tmp/playwright-*`. Write to
  the project only when the user asked for permanent tests, and never write into
  the skill directory.
- Failures: fix the app or tests only when that is in scope. After two failed
  scoped attempts, save evidence, quote the failing line or UI state, and stop.
- Permanent tests: done when the relevant build/test/lint checks pass on what
  you changed, or you name each check that did not run and why.

## Bundled Playwright scripts

Run them by absolute path from the caller's working directory, where
`<skill-dir>` is the directory that contains this `SKILL.md`. Prefer the
screenshot scripts over custom batch scripts:

```bash
node <skill-dir>/scripts/screenshot-url.js --url <url> --selector <ready-selector> \
  --out /tmp/playwright-page.png --json
node <skill-dir>/scripts/screenshot-sequence.js --url-template '<url/{n}>' --from 1 --to 10 \
  --selector <ready-selector> --out-dir /tmp/playwright-shots --json
node <skill-dir>/scripts/run.js --json /tmp/playwright-check.js
```

- Manifests record URL, title, screenshot path, viewport, console errors,
  network failures, and HTTP responses with status >=400.
```

## agent-browser (3622-agent-browser)

- الترخيص: **MIT**  ·  الأصل: https://github.com/zot24/skills/tree/2de01185a2a6f9085e943801d2426d098e729380/skills/agent-browser
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3622-agent-browser/14695-agent-browser
- الوصف: Expert on browser automation with AI agents using Vercel's agent-browser CLI. Use when the user wants to automate browsers, scrape websites, capture screenshots, or build AI-powered web workflows. Triggers on mentions of agent-browser, browser automation, headless browsing, web scraping with AI.

```markdown
# Agent Browser Skill

Expert at browser automation for AI agents using Vercel's agent-browser CLI.

## Overview

**agent-browser** is a headless browser automation CLI optimized for AI agents with:
- 50+ commands for navigation, forms, screenshots, network, and storage
- AI-optimized snapshots with element refs for deterministic selection
- Multi-session support for isolated browser instances
- Cross-platform native Rust CLI with Node.js fallback

## Quick Start

```bash
npm install -g agent-browser
agent-browser install

agent-browser open example.com
agent-browser snapshot -i          # Get interactive elements with refs
agent-browser click @e2            # Click using ref
agent-browser fill @e3 "text"      # Fill input using ref
agent-browser screenshot page.png
agent-browser close
```

## Core Concepts

### Refs (Recommended for AI)
Element references from snapshots provide deterministic selection:
```bash
agent-browser snapshot        # Shows: button "Submit" [ref=e2]
agent-browser click @e2       # Click using ref
```

### Sessions
Isolated browser instances with independent state:
```bash
agent-browser --session agent1 open site.com
agent-browser --session agent2 open other.com
```

## Documentation

For detailed information, see the reference documentation:

- **[Installation](docs/installation.md)** - npm, source builds, custom browsers
- **[Quick Start](docs/quick-start.md)** - Basic workflow and examples
- **[Commands](docs/commands.md)** - Full 50+ command reference
- **[Selectors](docs/selectors.md)** - Refs, CSS, semantic locators
- **[Sessions](docs/sessions.md)** - Multi-session and authentication
- **[Snapshots](docs/snapshots.md)** - Accessibility tree and options
- **[Streaming](docs/streaming.md)** - WebSocket viewport streaming
- **[Agent Mode](docs/agent-mode.md)** - AI agent integration patterns
- **[CDP Mode](docs/cdp-mode.md)** - Chrome DevTools Protocol

## Common Workflows

### Login Flow
```bash
agent-browser open https://example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait navigation
```

### Data Extraction
```bash
agent-browser open https://example.com/data
agent-browser snapshot --json > data.json
agent-browser get text ".product-title"
```

### Screenshot Capture
```bash
agent-browser screenshot viewport.png
agent-browser screenshot full.png --full
```

## Upstream Sources

- **Repository**: https://github.com/vercel-labs/agent-browser
- **Documentation**: https://agent-browser.dev/

## Sync & Update

When user runs `sync`: fetch latest from upstream sources, update docs/ files.
When user runs `diff`: compare current vs upstream, report changes.
```

## 9552-playwright (2464-playwright)

- الترخيص: **MIT AND Apache-2.0**  ·  الأصل: https://github.com/melodic-software/claude-code-plugins/tree/c8fa858c9059d3183cfc08f646e4a97f44b33973/plugins/playwright
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2464-playwright/9552-playwright
- الوصف: Live E2E browser automation via Microsoft's @playwright/cli: named sessions, accessibility-ref snapshots, click/fill by ref, screenshots, console and network capture, network mocking, tracing, video, and auth state, with artifacts written to disk so only paths enter context (far fewer tokens than Playwright MCP). Use when: 'playwright', 'E2E test', or any task that needs a real browser driven agai

```markdown
# Playwright CLI, live browser automation

Wraps Microsoft's [`@playwright/cli`](https://github.com/microsoft/playwright-cli) for token-efficient browser automation. Snapshots and screenshots write to disk; only paths come back into context, a substantial token reduction versus Playwright MCP's in-context payloads.

Requires `playwright-cli` on PATH (`npm install -g @playwright/cli`). If it is missing, tell the user to install it rather than substituting a different automation surface.

## Quick start (90% of use)

```bash
playwright-cli kill-all                              # start clean (no stale sessions)
playwright-cli -s=<flow> open <url>                  # named session, headless by default
playwright-cli -s=<flow> snapshot                    # writes YAML with element refs (e1, e2, ...)
playwright-cli -s=<flow> click e42                   # interact by ref
playwright-cli -s=<flow> fill e37 "input" --submit   # fill + press Enter
playwright-cli -s=<flow> screenshot --filename=meaningful-name.png
playwright-cli -s=<flow> console                     # summarize console messages
playwright-cli -s=<flow> close                       # tear down
```

Read the YAML snapshot file directly to locate element refs. Do not dump it into context.

## Conventions

- **Always use named sessions** (`-s=<flow>`) for multi-step work. Default (unnamed) sessions are hard to isolate when things go sideways
- **`kill-all` at the start** of a fresh E2E run guards against stale daemon state from prior sessions
- **`close` at the end**. Don't leave zombie browsers
- **`--headed` only when the user explicitly wants to observe.** On Windows, headed browsers spawn in the background and don't auto-focus. See [reference/windows-quirks.md](reference/windows-quirks.md)
- **Artifacts land in `.playwright-cli/` relative to CWD at command time.** Add `.playwright-cli/` to the project's `.gitignore` if it isn't already. For meaningful artifacts (evidence for PRs, regression baselines), pass `--filename=<descriptive>.png`; let timestamp-named snapshots pile up as throwaway intermediate state
- **Use element refs from snapshots** (`e15`, `e37`), not CSS selectors. Snapshots use accessibility roles, which survive cosmetic UI changes
- **Judge visual questions from the screenshot itself.** The snapshot YAML carries roles and text, not layout or color. For "does the modal cover the button" or "does the chart match the table", Read the screenshot file and answer that one specific question from the image; share the file path as evidence rather than retyping what it shows

## Progressive disclosure map

Load the right reference file for the scenario. Each is distilled from Microsoft's upstream skill:

| Scenario | Reference |
|----------|-----------|
```
