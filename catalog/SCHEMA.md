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
| `aspect_label` | string\|null | `16:9`, `9:16`, `1:1`, `4:5`, `4:3`, `21:9`, `other`. |
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

## Brief objects (`tools/import_briefs.py`, `catalog/briefs.json`)

`tools/import_briefs.py <dir>` reads every `*.json` file in `<dir>`; each file must be an object `{"briefs": [ <brief>, ... ]}`. `catalog/briefs.json` stores the accepted briefs as `{ "<id>": <brief> }`. `tools/check_originality.py` reads the same batch files.

| key | type | rule |
|---|---|---|
| `id` | string | Must already exist in `catalog/styles.json`; unknown ids are skipped. |
| `title_ar` | string | Arabic title, at most 80 characters. Becomes the record's `name_ar`. |
| `summary_ar` / `summary_en` | string | One-sentence summaries copied into the style record. |
| `concept_ar` / `concept_en` | string | The creative idea (BRIEF.md "الفكرة" / "Concept"). |
| `scenes_ar` / `scenes_en` | string[] | Proposed scene beats; `scenes_en` should have 3–8 items. |
| `motion_rules_ar` / `motion_rules_en` | string[] | Motion rules (BRIEF.md "قواعد الحركة" / "Motion rules"). |
| `stack` | string[] | Each one of `Remotion`, `React`, `HTML Canvas`, `SVG`, `CSS`, `GSAP`, `Three.js`, `WebGL`, `Web Audio`, `Lottie`. |
| `keywords` | string[] | 6–20 Arabic + English search terms. |
| `facts_from_source` | string[] | Facts the source states, rewritten in our words (may be empty). |
| `assumptions_en` | string | What was assumed rather than observed. |
| `aspect` | string | A readable ratio: `W:H` (e.g. `9:16`, `2.35:1`), `WxH` or a name (see `tools/aspects.py`). |
| `duration_s` | number\|null | Suggested duration in seconds; `null` means "per material". |
| `difficulty` | int 1–5 | Estimated implementation difficulty. |
| `revised_from_video` | string (optional) | `YYYY-MM-DD` when the brief was revised against frames of the reference video; changes the provenance note in BRIEF.md. |

All keys except `revised_from_video` are required. Without `--strict`, a brief with a missing key, a wrong type or an unreadable `aspect` is skipped, while a brief that only breaks a value rule (difficulty range, stack names, keyword or scene count, `duration_s` type, `revised_from_video` format, `title_ar` length) is imported and its issues are printed. With `--strict`, any issue skips the brief and the run exits 1, and a file that is not valid JSON shaped `{"briefs": [...]}` stops the run before anything is written. Briefs must be original writing: run `tools/check_originality.py --briefs <dir> --texts <dir>` on the batch before importing.

Policy: no third-party prompt text, video, poster, music or voice is stored in this repository. Links point to the owners' pages.
