# KOSIF TOOL Agent Guide

1. Identify the requested style ID with `STYLE_INDEX.md`, `catalog/styles.json` or `python3 tools/kosif.py search <words>`.
2. Read `styles/<id>/SKILL.md`, `STYLE.json` and `BRIEF.md` in full, then the category playbooks it lists. Follow the production runbook in SKILL.md.
3. Open the referenced source page and video if tools permit; never claim to have seen a video you could not access. The brief was written without watching the video: treat it as a director's proposal, verify against the reference.
4. Create fresh original assets and animation; no redistribution of external clips, prompts or music.
5. For user-supplied audio, transcribe to `words.json` and align actions to word timings (≤ 100 ms on key words). For a user video, study cuts, movement and voice first.
6. Scaffold a project with `python3 tools/kosif.py scaffold <id> <dir> --starter html-canvas|remotion`, fill `STYLE.md` (observed versus assumed) and `PLAN.md` (scene by scene), build the film in the starter, preview with `node tools/render_html.cjs --preview` or Remotion, and only then render.
7. Deliver: STYLE.md, PLAN.md, editable sources, a preview, the filled TEST_REPORT.md and the rendered MP4 after approval.
8. Preserve licenses, content rights, source attribution, secrets and platform terms.
9. If a style appears as an external-only example, use its brief as a creative direction, not proof of an existing tested implementation.
10. Catalog maintenance: `tools/sync_catalog.py` → `tools/import_briefs.py` (new briefs) → `tools/build.py` → `tools/validate.py`. Never store third-party prompt text in the repository.

11. Capabilities: `.claude/skills/kosif-superpowers/` lists every power with how-to and proof; search with `python3 .claude/skills/kosif-superpowers/scripts/powers.py suggest "<brief>"`.
