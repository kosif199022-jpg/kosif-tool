# أسطح Claude وما يستطيعه كل منها — Claude surfaces and their capabilities

What this gives you: per-surface tables (Claude Code terminal, web/cloud, Desktop and IDE; claude.ai apps; the Claude API; the Agent SDK) of what tools, network, installs, skills and limits each one has, how to tell which one you are on, and a "tool present → powers unlocked" map.
Open it after reading your tool list (SELF-05) and before promising network, installs, long jobs or file delivery. Facts are dated 2026-10-16 with source URLs. Products change, so re-fetch the source before quoting a number, and re-run `python3 scripts/probe_env.py` for machine facts.

## الفهرس / contents
1. Which surface am I on?
2. Claude Code (terminal, web/cloud, Desktop, IDE, CI)
3. claude.ai apps (web, desktop, mobile)
4. Claude API and platform
5. Agent SDK
6. Tool present → powers unlocked
7. Environment snapshot (Claude Code on the web, 2026-10-16)
8. Sources

Legend: ✅ checked by running something in a Claude container (proof in `proofs/general-discovery/README.md`) · 📄 from official docs fetched on 2026-10-16 · ❓ not confirmed (title or memory only, verify first).

---

## 1. أين أنا؟ / Which surface am I on?

| Evidence you can check | Likely surface | What follows |
|---|---|---|
| `/root/.ccr` exists, `CLAUDE_CODE_REMOTE` set, `mcp__claude-code-remote__*` tools, HTTPS via a local agent proxy ✅ | Claude Code cloud session (web, mobile, Desktop "Cloud", `claude --cloud`, routines) | Linux container, root, network per environment setting, GitHub through a repo-scoped proxy |
| `CLAUDECODE=1` but none of the above; home under `/Users/<name>` or `C:\Users` | Claude Code on the user's own machine (terminal, IDE, Desktop "Local") | The user's real files and network; be careful with destructive commands |
| `CI=true`, `GITHUB_ACTIONS`, `GITLAB_CI` | Claude Code headless in CI | No human to answer questions; follow the workflow's permissions |
| A code-execution tool, no network (instant failure), Python 3.11, 1 CPU 📄 | Claude API code-execution sandbox | Preinstalled libraries only; no installs; inline your assets |
| Chat with file creation; `/mnt/user-data`, `/home/claude` ❓; egress depends on plan/admin | claude.ai app sandbox | Probe the network first; 30 MB per file |
| `mcp__Claude_Browser__*`, `mcp__computer-use__*` or `enable__mcp__…` tools | Desktop app, or a cloud session linked to the user's computer | Load the browser or computer-use skill before the first step |

Never infer a surface from one clue only. Combine two or more, then run the network test (SELF-15).

## 2. Claude Code

Same engine everywhere: CLAUDE.md, settings, skills and MCP servers carry across the terminal CLI, the VS Code/Cursor and JetBrains extensions, the Desktop app (macOS, Windows x64/ARM64, Linux beta), the web at claude.ai/code, the mobile app, Slack, and GitHub Actions/GitLab CI 📄. Hand-offs: `claude --teleport` (cloud → terminal), `claude --cloud` (terminal → cloud), `/desktop`, Remote Control (continue a local session from phone or browser), Dispatch (phone → Desktop task) 📄.

### 2.1 Per-surface table

| Capability | Terminal CLI / IDE (local) | Web / cloud session | Desktop app |
|---|---|---|---|
| Runs where | the user's machine | Anthropic-managed Linux container 📄; measured 4 vCPU, 15 GiB, root ✅ | Local, Cloud, SSH or WSL environment 📄 |
| Network | the machine's own | per environment: None, Trusted (default: package registries, GitHub, cloud SDKs, Docker Hub), Full, Custom 📄; this account's env reached every tested host ✅ | per environment |
| Installs | whatever the user allows | pip, uv, npm and apt as root, each one command ✅ | per environment |
| GitHub | the user's git/gh | git read of public repos ✅; `gh api` and `gh search` repo-scoped (403 outside attached repos) ✅; `add_repo` and the GitHub MCP tool | Desktop also has PR monitoring, auto-fix CI, auto-merge 📄 |
| Skills from | `~/.claude/skills`, project `.claude/skills`, plugins; account skills when signed in 📄 | project + account skills ✅ (13 account skills listed) | local: `~/.claude/skills` + account skills; SSH reads the remote folder 📄 |
| MCP / connectors | `claude mcp add`, `.mcp.json`, settings 📄 | servers attached to the session ✅ (github, graphify, Claude_Docs, Higgsfield in this account) | connectors and plugins through the + button (not in cloud sessions) 📄 |
| Browser / GUI | Playwright yourself; Chrome extension ❓ | headless Playwright Chromium ✅ | browser pane (per-site approval), computer use on macOS/Windows, Pro/Max, preview 📄 |
| Parallel work | Agent (subagents), worktrees, agent teams 📄 | same; this session itself was a spawned subagent ✅ | parallel sessions with worktree isolation 📄 |
| Scheduling | `/loop` in-session; Desktop scheduled tasks; cloud Routines (`/schedule`) 📄 | `send_later` / scheduled tasks tools ✅ (listed) | scheduled tasks 📄 |
| Deliver files | files on disk | Artifact pages; files in the repo branch; SendUserFile where present ❓ | file editor + local disk |
| Limits | the user's hardware | 4 vCPU / 16 GB / 30 GB 📄; no GPU ✅; Docker daemon not running in the measured container ✅ (docs list Docker) | cloud sessions lack file editor, plugin browser and connector button 📄 |

### 2.2 Built-in tools and what each unlocks (📄 tools reference)
| Tool | Unlocks |
|---|---|
| Bash / PowerShell | any CLI: ffmpeg, Python, Node, git, installs, tests |
| Read / Write / Edit / NotebookEdit | files, images and PDFs (vision on your own renders), notebooks |
| Glob / Grep | file search (the reference says they can be absent on some installs; then use `rg`/`find` via Bash) |
| Agent | subagents with their own context (explore, plan, general, custom in `.claude/agents/*.md`) |
| Workflow | scripted fan-out of many subagents with one consolidated result (when enabled) |
| Skill | invoke a skill; the listing shows one line per skill |
| ToolSearch | load schemas of deferred tools |
| WebFetch / WebSearch | live pages and search (permission-gated, often deferred) |
| Monitor | background command with streamed lines (long renders, logs) |
| CronCreate/List/Delete, ScheduleWakeup, RemoteTrigger | in-session recurring prompts, self-paced loops, cloud routines |
| TaskCreate/Get/List/Update/Stop | task list; stop background tasks |
| EnterWorktree / ExitWorktree | isolated git worktree |
| SendMessage / ListAgents | talk to subagents, teammates, other sessions |
| ListMcpResourcesTool / ReadMcpResourceTool | MCP resources |
| LSP | definitions, references, type errors through language servers |
| Artifact | private shareable page on claude.ai, optional runtime capabilities (db, shared state, files) |
| AskUserQuestion, EnterPlanMode/ExitPlanMode, PushNotification, SendUserFile | clarify, plan first, notify, deliver files |

Permission rules look like `Bash(npm run *)`, `Edit(/src/**)`, `WebFetch(domain:example.com)`, `Skill(deploy *)` 📄.

### 2.3 Skills facts (📄 code.claude.com/docs/en/skills)
- Precedence: enterprise > personal `~/.claude/skills/<n>/SKILL.md` > project `.claude/skills/<n>/SKILL.md`; nested `.claude/skills` load when files there are touched; plugin skills are namespaced `plugin:skill`.
- The listing truncates description + when_to_use at **1,536 characters**, so put trigger words in the first ~300. Keep SKILL.md **under 500 lines**. After compaction each skill keeps its first **5,000 tokens**, within a shared **25,000-token** budget.
- Frontmatter keys include name, description, when_to_use, allowed-tools, disallowed-tools, context: fork, paths (glob gating), effort; unknown keys are ignored. Substitutions: `$ARGUMENTS`, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_PROJECT_DIR}`; `` !`cmd` `` injects command output.

### 2.4 Cloud environments (📄 code.claude.com/docs/en/cloud-environments)
Plans: Pro, Max, Team, Enterprise (premium or Chat+Code seats). Network levels: None / Trusted / Full / Custom; the Anthropic API is always reachable; GitHub goes through a dedicated proxy that holds credentials. Network secrets are injected as headers by the proxy, so the session never sees the key. A setup script runs before Claude and is cached. Resources: 4 vCPU, 16 GB RAM, 30 GB disk. The same environments serve Desktop cloud sessions, mobile, `claude --cloud` and routines.

## 3. تطبيقات claude.ai / claude.ai apps (web, desktop, mobile)

| Feature | Facts (2026-10-16) | Source |
|---|---|---|
| Code execution & file creation | Sandbox that creates .xlsx, .pptx, .docx, .pdf, PNG charts, scripts and artifacts (HTML, React, Markdown, Mermaid, SVG). On by default. Uses more of the plan's usage limit | 📄 support article 12111783 |
| Network (Free/Pro/Max) | one "Allow network egress" toggle; on by default for these plans | 📄 same |
| Network (Team/Enterprise) | owner picks Off (preinstalled only), Package managers only (npm, PyPI, crates, Ubuntu, Yarn, GitHub), Package managers + specific domains, or All domains. Team's default is described inconsistently in the article; Enterprise default is off | 📄 same |
| File size | 30 MB per file for upload and download; larger PDFs can be processed without loading into context | 📄 same |
| Apps | web, Claude Desktop, mobile (Settings → Capabilities) | 📄 same |
| Custom skills | zip with the skill folder at root, SKILL.md with name + description; enable in Customize → Skills; name ≤64 chars; help article says description ≤200 chars (the API spec allows 1,024, so design for 200); needs code execution; per user, with provisioning on Team/Enterprise | 📄 support article 12512198 |
| Pre-built skills | docx, xlsx, pptx, pdf, active automatically | 📄 platform skills overview |
| Artifacts | interactive pages; in Claude Code the Artifact tool can add runtime capabilities (database, shared state, viewer identity, ask-Claude, file storage) | 📄 + ✅ tool description seen |
| Connectors | remote MCP servers added in Settings → Connectors; Claude Docs is a first-party document connector | ✅ seen in this account; details ❓ |
| Web search, Research, Memory, Projects, Chrome extension, Cowork, desktop extensions | exist; specifics not re-fetched | ❓ |

## 4. Claude API / platform

Server tools (run by Anthropic) and client tools (you execute) 📄 tool reference. Type strings carry dates and change, so copy them from the docs or the `claude-api` skill, never from memory.

| Tool | Type string family (2026-10-16) | Runs |
|---|---|---|
| Web search | `web_search_2026…` / `web_search_20250305` | server |
| Web fetch | `web_fetch_2026…` / `web_fetch_20250910` | server |
| Code execution | `code_execution_20260521` (latest), `_20260120` (REPL state + programmatic tool calling), `_20250825` (bash + files) | server |
| Tool search | `tool_search_tool_regex_20251119`, `tool_search_tool_bm25_20251119` | server |
| MCP connector | `mcp_toolset` (beta header) | server |
| Advisor | `advisor_20260301` (beta header) | server |
| Memory | `memory_20250818` | client |
| Bash / text editor | `bash_20250124`, `text_editor_20250728` | client |
| Computer use / browser use | `computer_toolset_20260801`, `browser_toolset_20260801` | client |

Tool-definition options: `cache_control`, `strict`, `defer_loading` (load through tool search), `allowed_callers` (programmatic tool calling), `input_examples`.

**Code-execution sandbox** (📄 fetched 2026-10-16, proof P18): Python 3.11, x86_64 Linux; **1 CPU, 5 GiB RAM, 5 GiB disk**; **no internet, no outbound requests, no runtime installs**; containers reusable by id, checkpointed after ~5 min idle, expire 30 days after creation; each REPL cell is limited to 90 s with programmatic tool calling. Preinstalled: pandas, numpy, scipy, scikit-learn, statsmodels, matplotlib, seaborn, pyarrow, openpyxl, xlsxwriter, xlrd, pillow, python-pptx, python-docx, pypdf, pdfplumber, pypdfium2, pdf2image, pdfkit, tabula-py, reportlab, img2pdf, sympy, mpmath, tqdm, python-dateutil, pytz, joblib; CLIs unzip, unrar, 7zip, bc, rg, fd, sqlite. Pricing: 1,550 free container-hours per organization per month, then $0.05 per container-hour; free when the request also uses recent web search or web fetch.

**Agent Skills in the API** 📄: pass skills through the `container` parameter (pre-built pptx/xlsx/docx/pdf or custom ones uploaded via `/v1/skills`). They need code execution, and the same no-network rule applies.

Also documented, not re-fetched ❓: Files API, prompt caching, Message Batches, citations, extended/adaptive thinking, vision and PDF input, context editing/compaction, structured outputs, Managed Agents. For current parameters use the `claude-api` skill when it is listed.

## 5. Agent SDK
Python and TypeScript libraries exposing the Claude Code loop: custom tools, MCP, subagents, skills, plugins, hooks, permissions, sessions, structured outputs, tool search, file checkpointing, OpenTelemetry and cost tracking 📄 (code.claude.com/docs/en/agent-sdk/overview). Packages: `claude-agent-sdk` (PyPI, MIT) and `@anthropic-ai/claude-agent-sdk` (npm, "SEE LICENSE IN README.md", meaning Anthropic terms) — see `arsenal-general.md`. An API key is needed (🔑).

## 6. أداة موجودة ← قوة مفتوحة / Tool present → powers unlocked

| If you find | You can | Watch out |
|---|---|---|
| Bash or code execution | run any CLI: ffmpeg renders, Python and Node libraries, data analysis, file conversion, tests | API sandbox: no network |
| Bash + network | pip/uv/npm installs in a scratch env, apt as root, `git clone`, downloads, API calls | proxy rules; licenses |
| ffmpeg/ffprobe | cut, concat, transcode, captions (libass), loudnorm, xfade, frame extraction, QA numbers | check `ffmpeg -filters` for libass/xfade |
| Playwright Chromium | HTML/CSS/Canvas/WebGL → frames/MP4, screenshots, HTML→PDF, mermaid-cli | software GL only without GPU |
| soffice / pandoc | docx/pptx/xlsx ↔ PDF, Markdown ↔ docx, formula recalculation | headless flags |
| apt + root | tesseract(-ara), graphviz, inkscape, texlive, sox, fonts, blender | install time and disk |
| GPU (`nvidia-smi`) | local diffusion and large models | none in the measured cloud container |
| Read on images/PDF | look at your own frames, charts and pages before delivering | say which frames you actually viewed |
| WebSearch / WebFetch | current facts, official docs, license checks, citations | cache ~15 min; cite URLs |
| Agent / Workflow | parallel research, fan-out renders, independent review | keep lanes independent |
| Monitor / background Bash | long renders with progress, log watching | stop what you start |
| Cron / scheduled tasks / send_later / routines | recurring or delayed work | name the schedule plainly |
| Artifact (+ capabilities) | shareable pages, dashboards, previews, shared database | private by default |
| SendUserFile | deliver renders to the user's device | where present |
| Skill tool + listing | domain playbooks (docx, pptx, xlsx, pdf, dataviz, design, motion) | invoke before acting |
| `mcp__github__*` | repo search, files, PRs, issues, CI logs | write actions need intent |
| `mcp__graphify__*` | code-graph queries, impact analysis, shared workspace memory | indexed snapshot may be stale |
| `mcp__Claude_Docs__*` | collaborative documents | first-party docs connector |
| `mcp__Higgsfield__*` | AI image/video/audio/3D, upscale, background removal, voice | **paid credits**: user intent first |
| browser pane / Chrome / computer use | logged-in websites, desktop apps, screenshots | load their skill first; per-site approvals |
| EnterWorktree | safe parallel branches | clean up |
| memory tool / CLAUDE.md / auto memory | persistence across sessions | no secrets |
| `read_documentation` (cloud) | exact settings pages for network, deps, secrets, GitHub, resources | shows the user a settings button |

## 7. لقطة البيئة / Environment snapshot (Claude Code on the web, 2026-10-16)

Lease, not truth: re-run `python3 scripts/probe_env.py` (or the commands in `proofs/general-discovery/README.md`) in your session.
- Ubuntu 24.04.5, Firecracker kernel, 4 vCPU, 15 GiB RAM, 24-30 GB free disk, uid 0 with sudo, no GPU ✅
- python3 3.13.16 (system pip has ~86-89 distributions: numpy, pandas, pillow, requests, lxml, bs4, openpyxl, python-docx, reportlab, pypdf), uv 0.11.32, node 22.22.0, npm 10.9.4, bun, pnpm, yarn, go, rust, Java 21, gcc/clang ✅
- ffmpeg 6.1.1, ImageMagick 6 (`convert`), LibreOffice (`soffice`), pandoc, jq, git, gh, rg, Playwright 1.56 CLI with chromium-1194 in `/opt/pw-browsers`, docker client (daemon not running) ✅
- Missing at probe time: blender, `dot` (graphviz), `sqlite3` CLI, `duckdb` CLI, `yt-dlp`, `magick` (IM7), deno, R. tesseract + `ara` appeared later the same day after an apt install ✅
- Arabic fonts in the system: DejaVu, FreeMono/FreeSerif and Unifont only, so ship OFL fonts ✅
- Network through the agent proxy: pypi, npm, api.github.com, huggingface.co, jsdelivr, raw.githubusercontent.com and example.com all reachable; cdn-lfs.huggingface.co blocked, but HF downloads still worked through redirects ✅
- Account-specific (this owner): MCP servers github, graphify, Claude_Docs, Higgsfield; 13 account skills; no account plugins ✅. Other users will see different lists.

## 8. Sources (fetched 2026-10-16 unless marked)
- https://code.claude.com/docs/llms.txt (index of Claude Code pages; fetch first when refreshing)
- https://code.claude.com/docs/en/overview · /tools-reference · /skills · /cloud-environments · /desktop · /sub-agents · /mcp · /plugins/overview (index title) · /agent-sdk/overview
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference · /tool-use/code-execution-tool · /agent-skills/overview (docs.claude.com redirects here)
- https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude · https://support.claude.com/en/articles/12512198-creating-custom-skills
- Anthropic documentation is not openly licensed: everything above is paraphrased and linked, not copied.
