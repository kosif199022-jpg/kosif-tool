# Claude entry point

First run `python3 .claude/skills/kosif-superpowers/scripts/boot.py` (one-second self-briefing; without a shell read `CAPABILITIES.md`), then load `.claude/skills/kosif-superpowers/SKILL.md` and run its power-up protocol: it shows what you can really do in this session (tools, connectors, installable libraries), how to think, create and verify better, and a catalog of 4,700+ powers in 10 domains, motion and montage included, each with evidence and proof.

For any task, ask the front door first: `python3 .claude/skills/kosif-superpowers/scripts/hub.py find "<the task in the user's words>"` returns the runnable tools (with a command and whether this machine can run them), the catalog powers and the guide to read; `hub.py tool <id>` gives a tool's exact commands. Everything is also on one page in `.claude/skills/kosif-superpowers/references/INDEX.md`.

Read AGENTS.md, then the selected style's `styles/<style-id>/SKILL.md`, `STYLE.json` and `BRIEF.md` (when present), then the playbooks that the SKILL.md lists (`playbooks/<category>.md`, plus `playbooks/arabic-typography.md` for Arabic text, `playbooks/audio-sync.md` when audio is supplied and `playbooks/render-pipeline.md` before rendering). Find IDs in `STYLE_INDEX.md` or with `python3 tools/kosif.py search <words>`.

Rules:
- Inspect the source video when your tools allow; never claim to have watched what you could not open.
- Produce editable, real motion graphics (timelines, easing, camera, draw-on), never static slides.
- Preserve the user's audio untouched and synchronize to word timing when provided (`words.json`).
- Scaffold with `python3 tools/kosif.py scaffold <id> <dir>`; preview with `node tools/render_html.cjs --preview` (or Remotion) before the final render; verify duration, fps and audio with `templates/TEST_REPORT.md`.
- Do not copy third-party videos, prompts, code or media without a compatible license; link and credit instead.
- After changing the catalog run `python3 tools/build.py` and `python3 tools/validate.py`; after changing the skill's catalog or tool registry follow `.claude/skills/kosif-superpowers/references/guides/maintain.md`.
