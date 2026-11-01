# Claude Skill-to-Tool Bridge + Black Dragon Pro Max

## What is real

KOSIF Superpowers contains three distinct capability types:

1. Agent Skills: SKILL.md plus supporting files that Claude can discover/load.
2. MCP tools: callable functions exposed by a local stdio server.
3. Reviewed runtime adapters: selected Python executors with genuine artifact receipts.

This bridge offers eleven stable MCP tools, not thousands of invented executors. It runs locally, without network listeners, cloud tokens, payments or automatic installations.

## Quick start: read-only MCP for Claude Code

From the repository root:

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py inventory
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py search "تحليل مالي" --limit 10
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py plan "أراجع تقرير مالي"
~~~

Register Claude Code using an **absolute path** to the repository checkout:

~~~bash
claude mcp add --transport stdio kosif-superpowers -- python3 /ABSOLUTE/PATH/kosif-tool/.claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py serve
~~~

Verify with Claude Code /mcp. GitHub commits alone do not connect an external Claude account.

| MCP tool | Purpose | Default effects |
|---|---|---|
| kosif_search | Search full installed skill, power and tool catalog | Read-only |
| kosif_describe | Bounded source excerpt + SHA-256 | Read-only |
| kosif_plan_pro_max | Exhaustive assignment plan with concise summary | Read-only |
| kosif_run_pro_max | Generate exhaustive assignment plan, evidence ledger and QA report | Writes one new job under out/; no adapters run without explicit approval |
| kosif_route_reviewed | Select task-matching reviewed executable adapters and show their prerequisites | Read-only |
| kosif_preview_reviewed | Bind exact task, reviewed IDs, dependency waves, adapter definitions, script hashes and runtime bounds to a SHA-256 plan | Read-only; no job created |
| kosif_execute_reviewed | Execute only the tool IDs and file versions in a matching approval plan with artifact receipts | Requires matching approval_digest and three execution approvals; writes an isolated job |
| kosif_review_execution | Recheck receipt hashes and artifacts of a prior selected-tool job | Read-only |

Discovery is not execution. Missing runtime permissions mean blocked, not succeeded.

## Focused reviewed-tool execution (v1.1)

This is different from exhaustive Black Dragon planning. Rather than mark thousands of documentation cards as "executed", Claude can now route one task to a small set of **39 currently reviewed adapters** and run only the exact approved IDs. The list is generated from the live bundled registry; the count can change. Tool routing uses lexical matches (Arabic or English), not a semantic AI embedding model, and returned candidates have runtime_verified=false until the individual adapter actually runs.

Read-only route:

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py route-reviewed "financial reporting" --limit 8
~~~

Example MCP sequence:

1. Call kosif_route_reviewed with task="finance report". Review its suggested exact IDs and required prerequisites.
2. Call kosif_preview_reviewed with exact task, explicit IDs including prerequisites, workers and timeout. Inspect its dependency waves and SHA-256 approval_digest, which commits to scripts, registry, task and runtime settings.
3. The user reviews and approves the exact plan, tool IDs and requested side effects; an approval_digest is **not** consent or a signed authorization. Start MCP with serve --allow-execution and KOSIF_ALLOW_ADAPTER_EXECUTION=1 only with explicit approval.
4. Call kosif_execute_reviewed with the same task, IDs, workers, timeout, unique job_name, allow_execution=true and the returned approval_digest. A changed task, selected ID, adapter definition, script or registry refuses execution and requires a new preview. No unreviewed ID or hidden prerequisite is permitted.
5. Call kosif_review_execution with job_name. Its passed/verified_executed flags come from re-opening the receipts and artifact checksums. If any artifact changes, the review fails.

The selected execution writes to out/claude-reviewed-tools/JOB_NAME/{artifacts,receipts} and reviewed_execution.json. It can report selected_subset_fully_executed=true, **never** entire_catalog_executed=true: only an explicitly selected subset of tools was run. A plain successful CLI help/metadata lookup does not prove a creative or professional-quality output.

Security: maximum eight selected IDs, at most four parallel subprocess workers, only registered repo-relative Python adapters, required artifact placeholders, no shell interpolation and strict JSON tool inputs. The OS account is still not sandboxed; review every registered adapter before approval. Never send private task inputs to external systems without separate authorization.

## Skill-to-Tool Factory (v1.2): inspect first, approve later

New **static, no-execution** skill workshop: verify the source and detect Python CLI candidates, rather than pretending every SKILL.md is runnable. The scanner checks SHA-256, declared relative references, CLI parsing and main guards, and flags risky imported modules. It does not import, run, install, certify licenses, or automatically register code.

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py inspect-skill kosif-superpowers --script-limit 100
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py draft-skill-tool kosif-superpowers --out out/skill-tool-proposals/superpowers.json
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py doctor
~~~

The generated JSON is explicitly **PENDING_HUMAN_REVIEW_NOT_EXECUTABLE**, with missing argument/output contracts. A developer must review side effects and dependencies, test a real artifact with SHA-256, then separately register a vetted adapter. There is no direct promotion from a draft to the runtime catalog.

After exporting a portable ZIP, verify it without extraction or script execution:

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py verify-skill-zip out/kosif-superpowers-claude.zip
~~~

This verifies root SKILL.md, exact SHA-256 manifest coverage, duplicate/unsafe ZIP paths and bounded total unpacked size. A passing integrity check does **not** prove runtime safety, skill quality, compatible Claude subscription limits or license rights.

Three new MCP tools are **read-only**:
- kosif_toolify_skill — static source analysis of a named installed skill (returns candidates, not executors)
- kosif_verify_skill_package — verify an existing package ZIP under the repository out/ directory
- kosif_bridge_doctor — report reviewed-adapter configuration defects and approval state

The original seven MCP tools remain available; the focused execution action now requires a matching plan digest (v1.3). No skill is installed into an external Claude account by committing these changes to GitHub.

## Export a portable custom Agent Skill ZIP

Claude's custom skill ZIP expects SKILL.md at archive root. The exporter copies every file from the selected installed skill directory, keeps relative resource paths, adds per-file SHA-256 manifest and fails closed on partial exports, size limits or symlinks.

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py export-skill kosif-superpowers --out out/kosif-superpowers-claude.zip --max-mb 512
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

CI workflow .github/workflows/claude-tool-bridge-ci.yml verifies compilation, all bridge/router tests, permission gates, dependency handling, artifact tamper detection, inventory access and the actual eleven-tool stdio JSON-RPC handshake.

- MCP has four declared tools, not arbitrary shell command execution.
- Source excerpts are bounded; archive and source symlink traversals are rejected.
- ZIP output must be under repository out/, and existing ZIPs are not overwritten.
- Evidence requires a real artifact hash; exhaustive *assignment* is not exhaustive *execution*.
- Full Pro means stronger task planning and QA orchestration here, not an upgrade to the underlying Claude model.

## Plan integrity (v1.3) — التنين الأسود

Before authorizing execution, inspect a stable SHA-256 preview:

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/_claude_tool_bridge.py \
  preview-reviewed "finance report" --ids tool:capability-atlas tool:powers --workers 2 --timeout 60
~~~

The selected IDs above are **examples**; verify they are present in the current registry and match the task before use. A preview requires every dependency to be explicitly listed. It never executes a script or writes a job. A changed source hash, registry, dependency, task, worker limit or timeout invalidates the digest at the subsequent MCP execution call. This is a local integrity binding, not cryptographic identity verification or a guarantee that other processes cannot modify files between verification and spawn. The three explicit execution approvals still apply; the OS process remains unsandboxed.

Read-only audit was tightened: an empty or structurally invalid selected-job ledger no longer counts as a valid successful run.
