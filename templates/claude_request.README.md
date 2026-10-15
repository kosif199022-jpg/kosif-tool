# Claude request template

`claude_request.ar.txt` and `claude_request.en.txt` are the single source of truth for the request that the website generator and `tools/kosif.py prompt` produce. Placeholders:

| placeholder | filled with |
|---|---|
| `{repo}` | `https://github.com/kosif199022-jpg/kosif-tool` |
| `{id}`, `{name}`, `{page}` | from the style record |
| `{brief_line}` | ` و styles/<id>/BRIEF.md` / ` and styles/<id>/BRIEF.md` when a brief exists, else empty |
| `{playbooks}` | comma-separated playbook paths for the record's categories |
| `{source}` | user's material: audio file, video file, text script, or "none — write a short narration" |
| `{aspect}`, `{resolution}`, `{fps}`, `{duration}` | output format |
| `{stack}` | Remotion/React, HTML Canvas, SVG + GSAP, Three.js, or "choose the best fit" |
| `{lang}` | Arabic / English / both |
| `{brand}` | colors, fonts, logo notes or "none" |
| `{audio}` | keep provided voice, add licensed music, SFX only, or silent |
| `{notes}` | free text |
