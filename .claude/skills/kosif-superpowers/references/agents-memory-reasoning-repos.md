# الوكلاء والذاكرة والاستدلال من أكبر المستودعات / Agents, memory and reasoning from the top repositories

Batch 2 of the GitHub top-1000 review ([github-top-1000.md](github-top-1000.md)): methods from the most-starred agent, memory, retrieval and planning projects, restated in our own words as power records, plus two runnable tools. Nothing was copied; each record's `source` names the repository and its licence.

## الفهرس / contents

1. [How to choose](#how-to-choose)
2. [Runnable tools](#runnable-tools)
3. [Records by repository](#records-by-repository)
4. [What this does not claim](#what-this-does-not-claim)

## How to choose

| you need | method | id |
|---|---|---|
| a long job that may break or needs approval mid-way | checkpointed state graph with interrupts | AGENT-47 |
| work split across subagents | role-goal crew with written expected outputs | AGENT-48 |
| idea → delivery with clean handoffs | SOP assembly line with document handoffs | AGENT-49 |
| memory that does not pile up contradictions | add / update / delete / no-op decision | AGENT-50 (`memory_ops.py`) |
| an agent that works across many sessions | tiered self-editing memory; session capture and injection | AGENT-51, AGENT-52 |
| loops, arithmetic or many tool calls | code-as-action agent in a sandbox | AGENT-53 |
| a public-facing assistant | tripwire guardrails and specialist handoffs | AGENT-54 |
| an agent you must audit or resume | replayable event stream | AGENT-55 |
| questions about a whole corpus | graph RAG with community summaries; dual-level retrieval | GRAPH-22, GRAPH-23 |
| a cited report | perspective-guided research; planner + parallel researchers | WEB-25, WEB-26 |
| a feature from scratch | spec-driven development; brainstorm → plan → test-first subagents | PLAN-13, PLAN-14 |
| an unfamiliar codebase | ranked repository map; search/replace edit blocks | CODE-25 (`repo_map.py`), CODE-26 |
| a hard question that deserves several views | anonymous peer-ranked council | THINK-47 (`council.py`) |

## Runnable tools

```bash
python3 scripts/repo_map.py map <dir> --budget 6000 --focus render   # ranked files and their definition lines
python3 scripts/repo_map.py defs <dir> load_scene                    # where a name is defined, who mentions it
python3 scripts/memory_ops.py propose --store memory.json --facts facts.json --out plan.json
python3 scripts/memory_ops.py apply --store memory.json --plan plan.json
python3 scripts/memory_ops.py search --store memory.json "dialect"
```

`repo_map.py` only parses text (Python through `ast`, other languages through line patterns); it never imports, runs or builds the target. `memory_ops.py` decides with word overlap and subject/attribute keys instead of a model, refuses facts that contain a secret, and keeps every replaced or deleted memory in `history`.

## Records by repository

- langchain-ai/langgraph (MIT): AGENT-47 · crewAIInc/crewAI (MIT): AGENT-48 · FoundationAgents/MetaGPT (MIT): AGENT-49
- mem0ai/mem0 (Apache-2.0): AGENT-50 · letta-ai/letta (Apache-2.0, outside the top 1,000): AGENT-51 · thedotmack/claude-mem (Apache-2.0): AGENT-52
- huggingface/smolagents (Apache-2.0): AGENT-53 · openai/openai-agents-python (MIT): AGENT-54 · All-Hands-AI/OpenHands (MIT): AGENT-55
- microsoft/graphrag (MIT): GRAPH-22 · HKUDS/LightRAG (MIT): GRAPH-23
- stanford-oval/storm (MIT): WEB-25 · assafelovic/gpt-researcher (Apache-2.0): WEB-26
- github/spec-kit (MIT): PLAN-13 · obra/superpowers (MIT): PLAN-14
- Aider-AI/aider (Apache-2.0): CODE-25, CODE-26 · karpathy/llm-council (no licence detected; idea only): THINK-47

## What this does not claim

These are methods Claude applies and two small tools; none of the frameworks is installed or run here, and no model was trained. A record marked `documented` is a described method; only `repo_map.py` and `memory_ops.py` are code in this skill, with tests in `evals/test_repo_map.py` and `evals/test_memory_ops.py`.
