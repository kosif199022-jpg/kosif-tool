# Claude entry point

First load `.claude/skills/kosif-superpowers/SKILL.md` — your catalog of motion/montage superpowers (6,400+ powers with proof, libraries arsenal, 253 watched styles).

Read AGENTS.md, then the selected style's `styles/<style-id>/SKILL.md`, `STYLE.json` and `BRIEF.md` (when present), then the playbooks that the SKILL.md lists (`playbooks/<category>.md`, plus `playbooks/arabic-typography.md` for Arabic text, `playbooks/audio-sync.md` when audio is supplied and `playbooks/render-pipeline.md` before rendering). Find IDs in `STYLE_INDEX.md` or with `python3 tools/kosif.py search <words>`.

Rules:
- Inspect the source video when your tools allow; never claim to have watched what you could not open.
- Produce editable, real motion graphics (timelines, easing, camera, draw-on), never static slides.
- Preserve the user's audio untouched and synchronize to word timing when provided (`words.json`).
- Scaffold with `python3 tools/kosif.py scaffold <id> <dir>`; preview with `node tools/render_html.cjs --preview` (or Remotion) before the final render; verify duration, fps and audio with `templates/TEST_REPORT.md`.
- Do not copy third-party videos, prompts, code or media without a compatible license; link and credit instead.
- After changing the catalog run `python3 tools/build.py` and `python3 tools/validate.py`.
