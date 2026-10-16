# إثبات Graphify — خريطة الكود محليًا وعبر MCP / Graphify proof (local CLI + hosted MCP)

What this proves: Claude installed Graphify in a fresh venv, mapped real code from this repo into a knowledge graph with no API key and no LLM, queried it, measured change impact, saved lessons, served it over a local MCP server, turned it into a mind map, and called the hosted Graphify MCP connector. Powers backed by this folder: GRAPH-01…08, GRAPH-11…13, GRAPH-17, CODE-03, SEC-14. Narrative guide: [../../references/graphify.md](../../references/graphify.md).

- **Date / surface:** 2026-10-16, Claude Code cloud session (Linux, 4 vCPU), Python 3.13.16.
- **Package:** `graphifyy==0.9.91` with the `[mcp]` extra (PyPI name has a double "y"; the command is `graphify`).
- **Input:** a copy of `kosif-tool/tools/` + `kosif-superpowers/scripts/` (13 files: 11 `.py`, 1 `.cjs`, 1 `.md`, 204 KB) from branch `claude/kosif-superpowers` at commit `6921e48`; plus a copy of all 871 tracked files for the scale run. The real repo was never scanned in place (Graphify writes `graphify-out/` inside the scanned folder).
- **Isolation:** every command ran as `env -i PATH=$V/bin:/usr/bin:/bin HOME=$V/home GRAPHIFY_NO_TIPS=1 …`, so no cloud credentials, API keys or `claude` binary were visible and no paid backend could be chosen. Afterwards `~/.graphify` and `~/.cache/graphify` did not exist and `git status` showed only new skill files.

## 1. التثبيت / Install
```bash
V=$SCRATCH/venvs/graphify-sk
python3 -m venv $V && $V/bin/pip install -q "graphifyy[mcp]==0.9.91"
```
15.8 s, 61 lines in `pip list`, venv 241 MB.

## 2. الأوامر والنتائج / Commands and results
Full transcript with outputs: [run-log.txt](run-log.txt). Times are wall-clock.

| Command | Result | Exit | Time |
|---|---|---|---|
| `graphify extract . --code-only` | 12 code files (1 doc skipped) → **244 nodes, 586 edges, 8 communities** | 0 | 1.49 s |
| `graphify cluster-only . --no-label` | GRAPH_REPORT.md, graph.html; 94% EXTRACTED, 6% INFERRED, token cost 0 | 0 | 0.55 s |
| `graphify god-nodes --top 6` | Atlas 25, main() 24, build_prompt() 16, run() 14, CliError 12, doc_variables() 12 | 0 | 0.29 s |
| `graphify query "build prompt" --budget 600` | BFS from build_prompt(); 107 nodes found, 27 shown, says "raise budget to 2563" | 0 | 0.31 s |
| `graphify explain "cmd_scaffold()"` | 10 connections, e.g. `--> build_prompt() [calls] [EXTRACTED] tools/kosif.py:L589`, `<-- main() [indirect_call] [INFERRED]` | 0 | 0.27 s |
| `graphify explain "main()"` | "Ambiguous: matches 11 nodes" + candidate ids | **3** | 0.25 s |
| `graphify explain "zzzqqq"` | "No node matching" | **4** | 0.29 s |
| `graphify affected "aspects.py" --depth 2` | **11 dependents**: 3 importing files + 8 call sites with file:line | 0 | 0.23 s |
| `graphify path "cmd_scaffold()" "resolve()"` | 2 hops via `contains` + `imports` (structural, not a call chain) | 0 | 0.26 s |
| `graphify query "كيف يتم بناء البرومبت"` | No matching nodes (no translation/stemming) | **4** | 0.41 s |
| `graphify query "فيديو" --budget 300` | hit bilingual docstrings (aspects.py, fetch_video.py); 33 nodes | 0 | 0.43 s |
| `graphify export wiki` | 18 articles, `wiki/index.md` = agent entry point | 0 | 0.32 s |
| `graphify save-result … --outcome useful` / `dead_end` | 2 memory files | 0 | 0.15 s |
| `graphify reflect --graph graphify-out/graph.json` | [LESSONS.md](LESSONS.md): 1 tentative lesson group, 1 known dead end | 0 | 0.14 s |
| `graphify benchmark` | 16,266 naive tokens vs ~4,576 per query = 3.6x (subgraph size, not answer quality) | 0 | 0.32 s |

Scale run on a copy of the whole repo (871 tracked files, 393 parsed as code): `extract --code-only` **3.66 s → 685 nodes, 1,456 edges, 32 communities** (9 data-only JS files warned as "no symbols"); `cluster-only --no-label` 1.06 s; god nodes Atlas 25, main() 24, FixtureValidateTest 23, viewStyle() 21.

## 3. خادم MCP محلي / Local MCP server
`graphify-mcp <graph.json>` driven over stdio JSON-RPC by a small client ([mcp-stdio-probe.txt](mcp-stdio-probe.txt)): server `graphify 0.9.91` (empty instructions); **10 tools** (query_graph, get_node, get_neighbors, get_community, god_nodes, graph_stats, shortest_path, list_prs, get_pr_impact, triage_prs) and **6 resources** (graphify://report, stats, god-nodes, surprises, audit, questions); `graph_stats` → 244 nodes / 586 edges / 8 communities; session 1.06 s. Registration with `claude mcp add` was **not** run (it would change the user's MCP config).

## 4. خريطة ذهنية / Mind map (graph → communities → mind map)
Our own stdlib script [graph_mindmap.py](graph_mindmap.py) (run with `python3 -I`, exit 0) names each community by its dominant source file, lists the best-connected symbols (stdlib hubs skipped) and ranks cross-community bridges:
- [mindmap-tools.md](mindmap-tools.md) — the 13-file sample: 8 branches (render_html.cjs 53 nodes, kosif.py 51, …); strongest bridge kosif.py ↔ words_convert.py group (4 edges).
- [mindmap-repo.md](mindmap-repo.md) — the whole repo: 32 branches (tests/fixtures, web app.js, proof sound.py scripts, render_html.cjs, kosif.py, powers.py, Remotion starter, …).
The Mermaid `mindmap` text was generated but not rendered in this session; the Markdown outline is plain text.

## 5. Graphify المستضاف / Hosted Graphify MCP (🔑 connector present in this session)
Read-only calls through the session's `mcp__graphify__*` tools (no memory writes; trail-capturing tools such as query_graph/graphify_find were deliberately not used):

| Call | Result |
|---|---|
| `list_workspaces` | 1 workspace, active, selected via token |
| `list_repositories` | 2 repos, both `ready`/queryable: the owner's `kosif-atlas` (146,926 nodes) and `kosif-tool` (1,255 nodes) |
| `graph_stats("kosif199022-jpg/kosif-tool")` | 1,255 nodes, 2,135 edges, 147 communities; index of commit `629a59b` (main), built ~29 min earlier |
| `graphify_callers("build_prompt")` | 2 resolved callers: cmd_prompt() call at tools/kosif.py:L498, cmd_scaffold() at L569 |
| `graphify_tests_for("build_prompt")` | tests/test_cli.py `.kosif()` L34 (matched by name) |
| `graphify_file_neighbors("tools/kosif.py")` | 77 symbols with signatures; 175 neighbour files (style SKILL.md files reference kosif.py) |
| `graphify_file_neighbors("tools/aspects.py")`, `graphify_callers("resolve")` | "no file matching" / "unresolved symbol" — **aspects.py exists only on the working branch, after the indexed commit** |

Endpoint check: `https://api.graphify.com/mcp` answers HTTP 401 without a token (OAuth required). Setup for other machines: `claude mcp add --transport http --scope user graphify https://api.graphify.com/mcp` or add it as a claude.ai connector (not run here; the connector was already attached).

Lesson: a hosted graph describes the indexed commit, not your working tree. Check the freshness block and use the local CLI for unindexed changes (GRAPH-15).

## 6. ما لم يُختبر / Not tested here
`/graphify` skill flow with subagents, semantic extraction of docs/PDFs/images, video transcription, `graphify install --project` in the real repo (it edits CLAUDE.md and settings — needs consent; an earlier session tested it in a sandbox HOME), `graphify update` and the export formats other than wiki (tested by an earlier session the same day), Neo4j push, HTTP MCP transport, `claude mcp add` registration, hosted `remember`/`recall`.

## 7. الملفات / Files
| File | What |
|---|---|
| run-log.txt | full CLI transcript (paths shortened to `$V`) |
| GRAPH_REPORT.md | report for the 13-file sample |
| LESSONS.md | output of `graphify reflect` |
| mcp-stdio-probe.txt | local MCP JSON-RPC probe output |
| graph_mindmap.py | graph → mind map script (ours, stdlib) |
| mindmap-tools.md, mindmap-repo.md | mind maps produced by it |

Large outputs (graph.json 200 KB, graph.html 235 KB, wiki/) were left in the scratch venv; rerun the commands above to regenerate them.

## 8. الرخص / Credits
Graphify — https://github.com/Graphify-Labs/graphify — Apache-2.0 (earlier contributions MIT), "Graphify, Copyright 2026 Safi Shamsi and the Graphify contributors". GRAPH_REPORT.md, LESSONS.md and the transcripts are tool output generated from this repo's own code. `graph_mindmap.py` and this README are original to kosif-superpowers. Not an official Graphify project.
