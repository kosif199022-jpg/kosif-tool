# KOSIF TOOL Agent Guide

This file is for any coding agent (Claude Code, Codex, Cursor, Copilot, Gemini CLI …). It has two parts: how to find and run
what this repository can do, and the motion-graphics production rules.

## A. Find and run a capability (any agent)

1. One front door: `python3 .claude/skills/kosif-superpowers/scripts/hub.py find "<the task in the user's words>"` (Arabic or English).
   It returns the runnable tools with a copy-paste command and whether this machine has their requirements, the catalog powers
   that apply (with evidence badges) and the guide to read. Add `--json` for machine output.
2. Details of one tool: `hub.py tool <tool-id>` (every command, requirements, safety, consent, tests, limits). What runs here:
   `hub.py doctor`. All tools: `hub.py list`. One catalog record: `hub.py power <ID>`.
3. Without a shell, read `.claude/skills/kosif-superpowers/references/INDEX.md` (every tool, guide and family on one page) or
   the JSON `.claude/skills/kosif-superpowers/manifest.json`. MCP clients can use the read-only server registered in `.mcp.json`
   (`scripts/kosif_mcp.py`; tools `kosif_find`, `kosif_tool`, `kosif_power`, `kosif_search_powers`, …).
4. Honesty: claim the lowest true evidence badge (✅ proven · 🟢 ready · 📦 install · 🔑 key · 👁 seen · 📄 documented · 💡 idea);
   a tool's `consent` field says what needs the user's approval first (downloads, installs, running third-party code).
5. Editing the catalog or the tool registry: follow `.claude/skills/kosif-superpowers/references/guides/maintain.md`.

## B. Motion-graphics production

1. Identify the requested style ID with `STYLE_INDEX.md`, `catalog/styles.json` or `python3 tools/kosif.py search <words>`.
2. Read `styles/<id>/SKILL.md`, `STYLE.json` and `BRIEF.md` in full, then the category playbooks it lists. Follow the production runbook in SKILL.md.
3. Open the referenced source page and video if tools permit; never claim to have seen a video you could not access. Unless its note says it was revised against frames sampled from the reference video, the brief was written without watching the video: treat it as a director's proposal and verify against the reference.
4. Create fresh original assets and animation; no redistribution of external clips, prompts or music.
5. For user-supplied audio, transcribe to `words.json` and align actions to word timings (≤ 100 ms on key words). For a user video, study cuts, movement and voice first.
6. Scaffold a project with `python3 tools/kosif.py scaffold <id> <dir> --starter html-canvas|remotion`, fill `STYLE.md` (observed versus assumed) and `PLAN.md` (scene by scene), build the film in the starter, preview with `node tools/render_html.cjs --in <scene.html> --out <film.mp4> --preview` or Remotion, and only then render.
7. Deliver: STYLE.md, PLAN.md, editable sources, a preview, the filled TEST_REPORT.md and the rendered MP4 after approval.
8. Preserve licenses, content rights, source attribution, secrets and platform terms.
9. If a style appears as an external-only example, use its brief as a creative direction, not proof of an existing tested implementation.
10. Catalog maintenance: `tools/sync_catalog.py` → `tools/import_briefs.py` (new briefs) → `tools/build.py` → `tools/validate.py`. Never store third-party prompt text in the repository.

11. Capabilities: `.claude/skills/kosif-superpowers/` maps every power (thinking, writing, code, data, documents, research, apps, media, strategy, motion) with how-to and proof. Probe the session with `python3 .claude/skills/kosif-superpowers/scripts/probe_env.py` and search with `python3 .claude/skills/kosif-superpowers/scripts/powers.py suggest "<brief>"`.
