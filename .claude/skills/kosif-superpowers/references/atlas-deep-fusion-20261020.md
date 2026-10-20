# KOSIF Atlas Deep Fusion — 2026-10-20

## Purpose and scope

Extend the **existing canonical KOSIF Superpowers** skill with safe, offline Atlas capability discovery, not by copying 14,793 third-party skills wholesale. This enhancement keeps the existing 4,751-power catalog intact and does not claim new model weights, native apps, binary decompilation, or 14,793 working tools.

- Atlas repository: https://github.com/kosif199022-jpg/kosif-atlas
- Source baseline: `99bb108d` on `main`
- Destination: `kosif199022-jpg/kosif-tool/.claude/skills/kosif-superpowers/`
- Destination baseline: `4ca36be` on `main`
- Audit time: 2026-10-20 (Asia/Riyadh)
- Atlas index count: 14,708 ordinary + 85 separate copyleft = **14,793** records
- Structural metadata errors reported by the existing `atlas_metadata_audit.py`: **0**
- Labels: **5,285 READ_ONLY_OK** vs **9,508 REVIEW_BEFORE_INSTALL**
- Additional cautious intersection (main index only, declared permissive license + no risk flags + READ_ONLY_OK): **5,114 metadata candidates**. This is **not** a security audit, execution receipt, or permission to install.
- Number of distinct `SKILL.md` files selected for source-level *static text* sampling: **34** (12 topic groups); see `../data/atlas-source-samples-20261020.json`. These 34 are **not** a full source scan of 14,793 skills.
- Static heuristic warning patterns occurred in 5 of 34 sampled documents; a text match is not itself proof of maliciousness. The review did not execute third-party code.

## What is newly available

`scripts/atlas_deep_fusion.py` is a **read-only** local index query and evidence router. It reads the user-supplied `index.json` and `index-copyleft.json`, validates index counts, searches by bilingual query and domain, ranks matching skills, tags uncertain or flagged records, optionally inspects only checked-out `SKILL.md` text, and returns reproducible JSON with the index SHA-256 digests and source metadata.

Supported topic routes: reasoning, agents, engineering, reverse_engineering, security, finance, media_motion, design, research, web_apps, documents, language. This is discovery capability, **not** live execution capability. The existing `capability_atlas.py` remains the first choice for KOSIF-native 4,751 powers.

## Use from the root of the kosif-tool checkout

~~~powershell
$atlas = 'C:\path\to\kosif-atlas'
$skill = '.claude/skills/kosif-superpowers'
python "$skill/scripts/atlas_deep_fusion.py" --index "$atlas/index.json" --copyleft "$atlas/index-copyleft.json" --query "agent orchestration" --domain agents --limit 8
python "$skill/scripts/atlas_deep_fusion.py" --index "$atlas/index.json" --copyleft "$atlas/index-copyleft.json" --domain media_motion --limit 10 --source-root "$atlas"
python -m unittest discover -s "$skill/scripts" -p test_atlas_deep_fusion.py -v
~~~

To inspect full source for a selected result, first make **only that exact skill path** available in the local Atlas checkout (for example, selective `git sparse-checkout add`). Read and verify the upstream license, its `SOURCE.md`, dependencies, attack surface, and any proposed scripts. Keep license notices and upstream URLs. Never treat license metadata alone as confirmation that code redistribution or execution is appropriate.

## Findings useful for KOSIF Superpowers

| Area | Sampled evidence | Proposed use | Boundary |
|---|---|---|---|
| Reasoning | doubt-driven-development, factor-of-safety-failure-margin, pre-mortem | hypothesis tracking, assumption sensitivity and failure criteria | Do not elevate third-party prompt instructions into system authority |
| Agent orchestration | agent-sdk-builder, agent-team-orchestration | distinguish agentic tool loops from plain completion APIs; add explicit budgets and checkpoints | Requires verified SDK version and permissions |
| Engineering / RE | architecture-optimization, binary-analysis-patterns | focused feature tracing and evidence IDs | REA/Ghidra analyze binaries when appropriate; do not use them to claim decompilation of Markdown |
| Security | security-basics group | use static flags to **queue review** | Flag-free is not safe-by-default |
| Finance | design-fx-and-interest-rate-hedge, fbt-prep | discover domain-specific checklists | Independently validate tax/regulatory jurisdiction, arithmetic, and applicability |
| Motion and design | remotion, awwwards-motion, akbun-draw-quiet-pencil | retrieve source-backed workflows for render/edit/draw | No proprietary model/implementation is imported |
| Research and web | goal-research, agent-browser | route to evidence/freshness and supported browser executor | No undocumented web or user credentials |
| Language/documents | humanize, carbone, 8d-report-writing | choose specialist methodology where useful | No wholesale transfer of third-party content |

## REA / Ghidra actual host diagnostics

On the authorized Windows laptop the REA CLI reported version **6.7.0**. `rea doctor --provider ghidra --json` returned `healthy=true` for the scoped Ghidra analysis engine, recognizing **Ghidra 12.1.4**, x64 native decompiler, headless analyzer and 64-bit **JDK 21**. Claude Code registration was reported aligned; Codex and several other registrations were reported missing, so **REA was not exposed as an MCP tool in this chat**, despite the installed local CLI. A static Markdown skill scan does not require Ghidra. Do not advertise installed-but-missing adapters as live.

## Explicit release acceptance

1. Existing `SKILL.md`, 4,751-power routing and old scripts retained.
2. 9 source-fusion regression tests pass; index check reports 14,793 records, zero index structural errors.
3. No third-party modules imported or executed, no network calls, no `curl | bash`, no installer, no copying copyleft code into Superpowers.
4. Uncertain, risky, ambiguous and copyleft records remain reference-only / manual review.
5. New selector return includes original metadata and provenance, never `verified=true`.
6. Compare checkout against current remote `main` before publish and read files back after publish.
