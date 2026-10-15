# Catalog schema (catalog/styles.json, styles/<id>/STYLE.json)

Every style record has these fields. Optional fields may be `null` or absent in older records; code must tolerate that.

| field | type | meaning |
|---|---|---|
| `id` | string | Unique style ID. PromptsMotion entries are `pm-<slug>`; KOSIF base styles are plain slugs. Use verbatim with Claude. |
| `name` | string | Display title (English for PromptsMotion entries, Arabic for base styles). |
| `name_ar` | string\|null | Arabic title (from the brief). |
| `origin` | `"PromptsMotion"` \| `"KOSIF original style"` | Where the reference lives. |
| `type` | `"Prompt"` \| `"Skill"` \| `"Style"` | PromptsMotion labels each entry Prompt or Skill; base styles are `Style`. |
| `category` | string[] | Canonical category keys from `catalog/categories.json` (e.g. `charts`, `kinetic-type`). |
| `creator` | string | Credited creator handle (`@name`) or `KOSIF + attributed sources`. |
| `creator_url` | string\|null | Creator's source post. |
| `page` | string | Public reference page (never rehosted). |
| `video` | string\|null | External reference video URL (never rehosted). |
| `poster` | string\|null | External poster image URL. |
| `aspect` | `{w:int,h:int}`\|null | Reference video pixel aspect, e.g. `{"w":1920,"h":1080}`. |
| `aspect_label` | string\|null | `16:9`, `9:16`, `1:1`, `4:5`, `other`. |
| `rank` | int\|null | Popularity rank on the source library (1 = most popular). |
| `published` | string\|null | ISO date the reference was published on the source. |
| `model` | string\|null | Model credited by the source for the reference (e.g. `Opus 5.5`). |
| `effort` | string\|null | Effort level credited by the source (`Max`, `High`, `Medium`). |
| `tech` | string[] | Implementation technologies named by the source (Remotion, Canvas, SVG, CSS, Three.js, ...). May be empty. |
| `source_prompt_words` | int\|null | Length in words of the creator's public prompt. Stored as a number only; prompt text is never stored here. |
| `difficulty` | int 1–5\|null | Estimated implementation difficulty (from the brief). |
| `duration_s` | number\|null | Stated or recommended duration in seconds. |
| `stack` | string[] | Recommended implementation stack (from the brief). |
| `keywords` | string[] | Arabic + English search terms (from the brief). |
| `summary_ar` / `summary_en` | string\|null | One-sentence summary (from the brief). |
| `brief` | string\|null | Repo-relative path to `styles/<id>/BRIEF.md` when present. |
| `skill` | string | Repo-relative path to `styles/<id>/SKILL.md`. |
| `playbooks` | string[] | Repo-relative playbook paths for the record's categories. |

Derived files:
- `catalog/styles.json` — all records. `catalog/prompts_motion.json` — PromptsMotion subset.
- `catalog/briefs.json` — `{ "<id>": { full brief object } }`, loaded lazily by the website.
- `catalog/playbooks.json` — `[ {key, title_ar, title_en, path, excerpt} ]` for the website.
- `catalog/categories.json` — taxonomy (key, en, ar, legacy labels, playbook path).
- `STYLE_INDEX.md` — one line per record.

Policy: no third-party prompt text, video, poster, music or voice is stored in this repository. Links point to the owners' pages.
