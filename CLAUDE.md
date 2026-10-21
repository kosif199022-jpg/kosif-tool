# Claude entry point

**Universal Skill Intelligence Protocol (every substantial request):** read `.claude/skills/kosif-superpowers/PROTOCOL.md` and run `python3 .claude/skills/kosif-superpowers/scripts/skill_intelligence.py brief "<the request in the user's words>"`. It proves a 100% scan of the catalog (coverage receipt), ranks the groups, fused superpowers, powers and runnable tools that fit, and drafts three plans. Present the request analysis, the inventory numbers and plans A/B/C with a recommendation, then wait for the user's one-word answer (`موافق` / `تفاصيل` / `A` / `B` / `C` / `طوّر`) before executing.

**FusionForge v5.1 — self-learning composite workflows for L2/L3 tasks:** After the USIP brief, generate one local project-scoped recipe for every distinct substantive experiment with: python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py propose "<the user goal>" --project <safe_project_slug>. Before proposing, it automatically considers verified prior recipes ONLY within that same project. Review the proposed superpowers; invent actual compatible handoffs, input/output schemas, owners, tests and three genuinely different plans. After approval, use real executors. Document each actual step with fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --action "<observed action>" --tool <executor> --input "<inputs>" --output "<artifacts>" --observed "<measured result>" --evidence <file>; never paste credentials into trace. Record tested/failed with actual existing evidence files. Set verified only after genuine QA with --qa-pass and evidence. The private local index is under out/fusionforge/<project>/ and is gitignored; do not auto-publish it or promote project/client lessons to the global powers catalog. Never claim model-weight training, execution, Full Pro or learning persistence without receipts and file read-back. L0 and narrow follow-up edits do not need new candidate workflows.

First run `python3 .claude/skills/kosif-superpowers/scripts/boot.py` (one-second self-briefing; without a shell read `CAPABILITIES.md`), then load `.claude/skills/kosif-superpowers/SKILL.md` and run its power-up protocol: it shows what you can really do in this session (tools, connectors, installable libraries), how to think, create and verify better, and a catalog of 5,200+ powers in 10 domains, motion and montage included, each with evidence and proof.

For any task, ask the front door first: `python3 .claude/skills/kosif-superpowers/scripts/hub.py find "<the task in the user's words>"` returns the runnable tools (with a command and whether this machine can run them), the catalog powers and the guide to read; `hub.py tool <id>` gives a tool's exact commands. Everything is also on one page in `.claude/skills/kosif-superpowers/references/INDEX.md`.

Read AGENTS.md, then the selected style's `styles/<style-id>/SKILL.md`, `STYLE.json` and `BRIEF.md` (when present), then the playbooks that the SKILL.md lists (`playbooks/<category>.md`, plus `playbooks/arabic-typography.md` for Arabic text, `playbooks/audio-sync.md` when audio is supplied and `playbooks/render-pipeline.md` before rendering). Find IDs in `STYLE_INDEX.md` or with `python3 tools/kosif.py search <words>`.

Uploaded audio or video for montage or motion graphics: use the Montage Pro task force, `python3 .claude/skills/kosif-superpowers/scripts/montage_pro.py intake <file> --job <dir>` then `options` and `build` (guide: `.claude/skills/kosif-superpowers/montage-pro/README.md`).

Rules:
- Inspect the source video when your tools allow; never claim to have watched what you could not open.
- Produce editable, real motion graphics (timelines, easing, camera, draw-on), never static slides.
- Preserve the user's audio untouched and synchronize to word timing when provided (`words.json`).
- Scaffold with `python3 tools/kosif.py scaffold <id> <dir>`; preview with `node tools/render_html.cjs --preview` (or Remotion) before the final render; verify duration, fps and audio with `templates/TEST_REPORT.md`.
- Do not copy third-party videos, prompts, code or media without a compatible license; link and credit instead.
- After changing the catalog run `python3 tools/build.py` and `python3 tools/validate.py`; after changing the skill's catalog or tool registry follow `.claude/skills/kosif-superpowers/references/guides/maintain.md`.

## Smart capability index — Claude's 3-minute map

Before exploring thousands of individual power cards, read `.claude/skills/kosif-superpowers/references/CLAUDE_3_MINUTE_MAP.md`.
The deterministic index maps all 5,318 original powers (62 families) into 15 task-oriented groups; names, evidence, dependencies and original IDs are preserved.
Run `python .claude/skills/kosif-superpowers/scripts/smart_capabilities.py groups` for the overview, `find "<task>" --json` for matched groups and powers, and `verify` to check the source-to-index mapping. Follow with `hub.py find` and `hub.py doctor` before any action.
Grouping alone is not executable fusion: connect components only through tested workflows, and report missing runtime dependencies separately. Use REA/Ghidra only for suitable authorized executable targets, not catalog JSON.
