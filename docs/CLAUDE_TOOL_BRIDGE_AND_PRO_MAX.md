# Claude Skill-to-Tool Bridge + Black Dragon Pro Max

## What is real

KOSIF Superpowers contains three distinct capability types:

1. Agent Skills: SKILL.md plus supporting files that Claude can discover/load.
2. MCP tools: callable functions exposed by a local stdio server.
3. Reviewed runtime adapters: selected Python executors with genuine artifact receipts.

This bridge offers four stable MCP tools, not thousands of invented executors. It runs locally, without network listeners, cloud tokens, payments or automatic installations.

## Quick start: read-only MCP for Claude Code

From the repository root:

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/claude_tool_bridge.py inventory
python3 .claude/skills/kosif-superpowers/scripts/claude_tool_bridge.py search "تحليل مالي" --limit 10
python3 .claude/skills/kosif-superpowers/scripts/claude_tool_bridge.py plan "أراجع تقرير مالي"
~~~

Register Claude Code using an **absolute path** to the repository checkout:

~~~bash
claude mcp add --transport stdio kosif-superpowers -- python3 /ABSOLUTE/PATH/kosif-tool/.claude/skills/kosif-superpowers/scripts/claude_tool_bridge.py serve
~~~

Verify with Claude Code /mcp. GitHub commits alone do not connect an external Claude account.

| MCP tool | Purpose | Default effects |
|---|---|---|
| kosif_search | Search full installed skill, power and tool catalog | Read-only |
| kosif_describe | Bounded source excerpt + SHA-256 | Read-only |
| kosif_plan_pro_max | Exhaustive assignment plan with concise summary | Read-only |
| kosif_run_pro_max | Generate plan, evidence ledger and QA report | Writes one new job under out/; no adapters run without explicit approval |

Discovery is not execution. Missing runtime permissions mean blocked, not succeeded.

## Export a portable custom Agent Skill ZIP

Claude's custom skill ZIP expects SKILL.md at archive root. The exporter copies every file from the selected installed skill directory, keeps relative resource paths, adds per-file SHA-256 manifest and fails closed on partial exports, size limits or symlinks.

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/claude_tool_bridge.py export-skill kosif-superpowers --out out/kosif-superpowers-claude.zip --max-mb 512
~~~

Replace kosif-superpowers with an exact directory name under .claude/skills/ to export that skill. Upload the ZIP to Claude under Customize → Skills with code execution enabled, subject to Anthropic's size/plan restrictions. For Claude Code, the existing project .claude/skills/<name>/SKILL.md tree can be discovered without an upload. The exporter does not upload for you.

## Black Dragon Pro Max / التنين الأسود

The core Black Dragon still includes **every** registered skill, power, tool, superpower, style, playbook and protocol rule without relevance filtering. Pro Max adds an explicit three-path comparison (minimal baseline / exhaustive task distribution / adversarial QA), six reasoning lenses, dependency and permissions checks, and independent evidence verification. These are deterministic orchestration methods, NOT proof of external KOSIF Think/Full Pro or multiple LLM runs.

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py plan "حلل الشركة وابنِ تقريرًا" --mode pro-max
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "حلل الشركة وابنِ تقريرًا" --mode pro-max --job out/black-dragon/pro-max-001 --workers 8
~~~

Outputs include black_dragon_pro_max_plan.json (decision lenses and gates), black_dragon_plan.json, briefs.jsonl (every assignment), all_skills_ledger.json (actual status), black_dragon_pro_max_qa.json (separate SHA and count audit), and black_dragon_report.json/.md. Code 4 means **not every capability actually executed**, an honest incomplete result.

Only after reviewing the bundled adapters and separately authorizing execution:

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "task" --mode pro-max --job out/black-dragon/approved-001 --reviewed-adapters --execute-adapters
~~~

Adapters run under the current OS user's permissions. This is **not a sandbox**. No unreviewed code, payments, deployments or uploads are auto-allowed.

For MCP execution, all three independent gates are necessary: (1) start server with serve --allow-execution; (2) KOSIF_ALLOW_ADAPTER_EXECUTION=1 is set in that process environment; (3) call kosif_run_pro_max with allow_execution=true. Every invocation requires a new alphanumeric job_name. Without gates, the bridge rejects execution or produces blocked entries.

## Test and threat model

~~~bash
python3 -m unittest tests/test_claude_tool_bridge.py -v
python3 -m unittest discover -s tests -p 'test_black_dragon*.py' -v
~~~

CI workflow .github/workflows/claude-tool-bridge-ci.yml verifies compilation, unit tests, inventory access and the actual stdio JSON-RPC handshake.

- MCP has four declared tools, not arbitrary shell command execution.
- Source excerpts are bounded; archive and source symlink traversals are rejected.
- ZIP output must be under repository out/, and existing ZIPs are not overwritten.
- Evidence requires a real artifact hash; exhaustive *assignment* is not exhaustive *execution*.
- Full Pro means stronger task planning and QA orchestration here, not an upgrade to the underlying Claude model.
