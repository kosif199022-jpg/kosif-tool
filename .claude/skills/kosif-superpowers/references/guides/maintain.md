# صيانة الكتالوج والمهارة — Maintaining the catalog and the skill

كل ملف مولَّد في المهارة له مصدر واحد وأمر واحد يعيد بناءه، وكل أمر بناء حتمي (تشغيلان متتاليان يعطيان الملف نفسه بايتًا ببايت)، ولكل منها وضع `--check` يستعمله CI. عدّل المصدر، ثم شغّل السلسلة بالترتيب أدناه.

Every generated file has one source and one command that rebuilds it. Every builder is deterministic (two runs give byte-identical output) and has a `--check` mode that CI runs. Edit the source, then run the chain below in order.

Commands are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless marked *(repo root)*.

<!-- hub:area:maintain:start -->

**الأدوات / tools (14)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `build-chapters` | Regenerates the bilingual Markdown chapter references/powers/<family>.md for every general (non-motion) power family from data/powers/<family>.json. Output is deterministic, and it never touches the 30 hand-made motion chapters. --check reports stale, missing or orphaned chapters without writing. | `python3 scripts/build_chapters.py` | untested |
| `catalog-evidence-audit` | Statically audits every power record in data/powers/*.json for duplicate ids, malformed records and proof-link coverage. It checks only whether local 'kosif-tool/...' references exist and counts the claimed statuses and proof scopes. | `python3 scripts/catalog_evidence_audit.py` | tested-elsewhere |
| `check-skill` | Validates the kosif-superpowers skill with 14 read-only checks: SKILL.md frontmatter, power records, proof paths, relative Markdown links, contents headings, generated chapters, the counts marker, model names, secrets and leaked session paths, evals/evals.json, the data/tools.json registry with its generated hub files, power-count drift in the entry docs, the USIP protocol structure (PROTOCOL.md core and references/protocol/), and the reference layout (every file under references/ in exactly one section of data/skill_layout.json). It can also run the routing evals, then prints a text or JSON report and exits 1 on any error. | `python3 scripts/check_skill.py` | untested |
| `skill-layout` | Keeps the skill's reference files in order: data/skill_layout.json puts every file under references/ (and the entry documents) into exactly one of eleven sections in reading order. It builds the readable map references/LAYOUT.md, checks it like a trial balance (no unlisted, doubly listed or missing file, no stale map), says which section holds a file, and prints the git mv commands that would move each section to its planned folder. It never moves a file itself. | `python3 scripts/skill_layout.py build` | tested-here |
| `package-skill` | Validates the skill with check_skill.py, then zips it deterministically into kosif-superpowers.skill for upload to claude.ai. The archive has a single top folder and one SKILL.md, whose description is replaced by the ≤200-character claude_ai_description. dist/, caches, vendor/, evals/ and (with --lite) media are left out, and the finished archive is re-verified. | `python3 scripts/package_skill.py` | tested-here |
| `relabel-proofs` | Recomputes the proof_scope field of every power record from where its proof entries resolve on this machine (repo > session > archive > sibling > receipt > style > url > missing/none) and rewrites data/powers/*.json in place. With --check it only reports how many records would change. | `python3 scripts/relabel_proofs.py` | untested |
| `repo-build` (repo root) | Regenerates every derived file of the motion style atlas from catalog/styles.json, categories.json and briefs.json: each style's styles/<id>/SKILL.md and STYLE.json, STYLE_INDEX.md, catalog/playbooks.json, meta.json, prompts_motion.json, the normalised catalog/styles.json, sitemap.xml and the stats block in README.md. --check only reports drift. | `python3 tools/build.py` | untested |
| `repo-check-originality` (repo root) | Compares the English text of each pm- brief in batch JSON files with the creator's saved public description (<slug>.txt), reports every shared run of N consecutive words (default 6) and exits 1 when any brief is flagged. | `python3 tools/check_originality.py --briefs ./briefs/ --texts ./source-texts/` | untested |
| `repo-import-briefs` (repo root) | Validates batch JSON files of creative briefs ({"briefs": [...]}), writes styles/<id>/BRIEF.md for each accepted brief, and merges the brief summary fields into catalog/styles.json, catalog/prompts_motion.json, catalog/briefs.json and each STYLE.json. | `python3 tools/import_briefs.py ./briefs/` | untested |
| `repo-sync-catalog` (repo root) | Scrapes the public PromptsMotion library index and its detail pages (cached under .cache/promptsmotion/), extracts factual metadata only, rewrites catalog/styles.json, catalog/prompts_motion.json and every styles/<id>/STYLE.json, and flags entries that have left the index with listed=false. | `python3 tools/sync_catalog.py` | untested |
| `repo-validate` (repo root) | Runs 14 integrity checks on the style atlas and prints a numbered PASS/WARN/FAIL report or JSON. It checks that catalog/styles.json parses with unique slug ids, that catalog/categories.json is a valid taxonomy, record fields, enums and https URLs, known categories, aspect_label against the pixel size, and that styles/<id>/SKILL.md exists and STYLE.json equals the record. It also checks for orphan folders, STYLE_INDEX.md coverage, prompts_motion and briefs consistency, playbook files, rehosted media under styles/ or catalog/, matching request-template placeholders and meta totals. | `python3 tools/validate.py` | tested-here |
| `rea-superpowers-map` | Maps this skill the way REA maps a source tree it does not execute: a content-addressed inventory, Python import and invoke edges (ast), REA's JavaScript edges from its committed receipt, links from every script to its tools.json entry, tests, CI steps, powers and families, the gaps (orphan or untested scripts, missing tool files, unlisted references, broken links, families without a runnable tool) and Atlas safe-core coverage per theme. | `python3 scripts/rea_superpowers_map.py build` | tested-here |
| `agent-guard` | Checks a shell command before an agent runs it against a documented 13-rule table (recursive rm of / ~ * or outside the folder, curl\|bash, force push, world-writable chmod, credentials in argv, disk-destroying commands, writes to system paths or outside cwd, history-rewriting git, sudo) and returns GREEN, YELLOW or RED with redacted findings; scans a transcript or log line by line for credential-shaped strings with the shared detector and prints only redacted excerpts; and plans parallel agent work as deterministic branch/worktree names, waves and a dependency-respecting merge order with the git commands. | `python3 scripts/agent_guard.py rules` | tested-here |
| `self-council` | Inventories every reviewable unit of the repository with a stable id (skills, this skill's scripts, apps, tools, playbooks, workflows) and cheap static signals (direct or indirect test, docstring and usage line, line count, tools.json registration, SKILL.md description, last CHANGELOG mention). It plans the next batch of the weakest unreviewed units, writes prompts for five fixed personas (Strict Engineer, New Egyptian User, Devil's Advocate, Architect, Innovator), validates each persona's review (severity, an evidence path that exists, proposed change, effort, confidence, a persona-specific field), refuses secrets, merges and dedupes the findings, and ranks proposals by severity, confidence, agreement and effort into an implement-next list. A ledger in data/self_council_ledger.json records which units were reviewed and at which content hash, so successive runs cover the whole app and changed units come back as stale. It never calls a model: Claude runs the personas as parallel subagents, or the report says SELF_COUNCIL_SIMULATED. | `python3 scripts/self_council.py inventory --summary` | tested-here |

<!-- hub:area:maintain:end -->

## الفهرس / contents

1. [What to edit](#what-to-edit)
2. [The build chain](#the-build-chain)
3. [Adding a tool](#adding-a-tool)
4. [Adding or changing powers](#adding-or-changing-powers)
5. [What CI checks](#what-ci-checks)
6. [Mapping the skill the REA way](#mapping-the-skill-the-rea-way)

## What to edit

| you want to change | edit this (source) | never edit (generated) |
|---|---|---|
| a runnable tool's description, commands, requirements, safety | `data/tools.json` (schema: `schemas/tools.schema.json`) | `manifest.json`, `references/INDEX.md`, the `hub:` blocks in `SKILL.md` and `references/guides/*.md` |
| a power (capability record) | `data/powers/<family>.json` (schema: `schemas/power.schema.json`) | `references/powers/<family>.md` for general families, `references/requirements.md`, `data/capability_atlas_index.json`, `references/capability-atlas.md` |
| a requirement (binary, package, key) | `data/requirements.json` | the `requires` field is derived by `requirements.py derive` |
| how a task is routed to a runnable route | `data/capability_routes.json` | — |
| the repo-root self-model for a bare link | nothing — `boot.py --static --write` rebuilds it | `CAPABILITIES.md`, `llms.txt` *(repo root)* |
| the motion style atlas | `catalog/styles.json` *(repo root)* | `STYLE_INDEX.md`, `styles/<id>/SKILL.md`, `catalog/*.json` indexes, `sitemap.xml` |

## The build chain

```bash
python3 scripts/hub.py build                    # data/powers/runnable-tools.json (TOOL records) from data/tools.json, + the files below
python3 scripts/requirements.py derive          # fill `requires` on every power from its install/how/tags text
python3 scripts/relabel_proofs.py               # recompute proof_scope (repo / sibling / session …)
python3 scripts/build_chapters.py               # general family chapters references/powers/*.md
python3 scripts/requirements.py index           # references/requirements.md (requirement → powers it unlocks)
python3 scripts/capability_graph.py build       # data/capability_graph.json + references/capability-graph.html
python3 scripts/capability_atlas.py build       # data/capability_atlas_index.json + references/capability-atlas.md
python3 scripts/powers.py mindmap --html references/capability-map.html
python3 scripts/powers.py mindmap --update-md references/capability-map.md   # map block + counts, prose kept
python3 scripts/smart_capabilities.py build     # data/smart_capability_index.json + the group maps
python3 scripts/superpower_fusion.py build      # data/superpowers.json + references/superpowers.md (fused superpowers)
python3 scripts/kosif_hubs.py build             # data/hubs_index.json, references/hubs.md, START.md
python3 scripts/capability_mindmap.py build     # data/capability_mindmap.json + references/capability-mindmap.md
python3 scripts/owned_repos.py render           # references/owned-repos-map.md (its counts follow the catalog)
python3 scripts/smart_capabilities.py library   # references/library/: one routing chapter per group (USIP v5.5, A28)
python3 scripts/smart_capabilities.py cards     # usip-library/ (repo root): a protocol card per power and tool
python3 scripts/superpower_fusion.py build      # data/superpowers.json + references/superpowers.md (fused superpowers; ids shift when powers are added)
python3 scripts/kosif_hubs.py build             # data/hubs_index.json, references/hubs.md, START.md (the 15 hubs over the superpowers)
python3 scripts/capability_mindmap.py build     # data/capability_mindmap.json + references/capability-mindmap.md
python3 scripts/owned_repos.py render           # references/owned-repos-map.md (its catalog proof counts move with the powers)
python3 scripts/github_top_repos.py build       # data/github_top1000.json + references/github-top-1000.md (it lists the powers that cite each repository)
python3 scripts/micro_index.py build            # data/micro_index.json + references/micro-index/ (one line per power, tool, superpower)
python3 scripts/hub.py build                    # again: manifest.json, references/INDEX.md, SKILL.md and guide tool blocks
python3 scripts/boot.py --static --write        # CAPABILITIES.md + llms.txt at the repo root
python3 scripts/rea_superpowers_map.py build    # data/superpowers_rea_map.json + references/superpowers-rea-map.{md,html} (not CI-checked)
python3 scripts/atlas_ledger.py build           # data/atlas_ledger.json.gz, after powers that cite Atlas folders change (not CI-checked)
python3 scripts/check_skill.py --print-counts   # paste the marker line into SKILL.md if any count changed
python3 scripts/check_skill.py --evals          # structure, links, proofs, counts, registry, secrets + routing evals
```

Then, from the repo root: `python3 tools/build.py && python3 tools/validate.py && python3 -m unittest discover -s tests`.

Check-only versions (what CI runs in its "Generated skill files are current" step, plus `tools/build.py --check`; they write nothing): `requirements.py derive --check`, `relabel_proofs.py --check`, `build_chapters.py --check`, `requirements.py index --check`, `capability_graph.py build --check`, `capability_atlas.py build --check`, `powers.py mindmap --html references/capability-map.html --update-md references/capability-map.md --check`, `hub.py build --check`, `boot.py --static --check`, `smart_capabilities.py library-check`, `smart_capabilities.py cards-check`, `github_top_repos.py build --check`, `micro_index.py build --check`, `tools/build.py --check`.

The chapters (`build_chapters.py`) link related references but skip the generated ones (`INDEX.md`, `LAYOUT.md`, `requirements.md`, `capability-atlas.md`, `capability-map.md`), so one pass of the chain converges whatever order those are rebuilt in.

## Adding a tool

1. Write the script under `scripts/` with `argparse` and a `--help` that works without optional dependencies (import heavy packages inside the commands that need them).
2. Add a test under `evals/` (skill) or `tests/` (repo) and add it to `.github/workflows/ci.yml`.
3. Add one entry to `data/tools.json`: a kebab-case `id`, its `area` (one of the 12), bilingual titles and summaries, at least two `use_when` requests in the user's words (Arabic and English), search `keywords`, every subcommand with a runnable `example`, `requires` (pip distributions, binaries, npm packages, optional extras, network), `safety`, `consent`, an honest `limits` sentence, `tests`, `docs` and `families`. Set `evidence` to `tested-here` only after the test passed on this checkout.
4. Document the how-to in the area guide `references/guides/<area>.md` (the guide's tool table is generated; write the prose below it).
5. Run `python3 scripts/hub.py build` and `python3 scripts/check_skill.py --evals`; `python3 scripts/hub.py find "<a request it should answer>"` should list it.

## Adding or changing powers

- Keep IDs stable (`<PREFIX>-<n>`); a new family needs a `FAMILY_META` entry in `scripts/powers.py` for general domains.
- Fill `what`, `how`, `when` (a bilingual trigger: "<Arabic> / <English>") and `tags` (Arabic and English words users type). `when` and `tags` feed the search directly.
- Claim the lowest true `status`; `proof` paths must resolve (checked by `check_skill.py`).
- Add a routing case to `evals/evals.json` when a new kind of request should reach the new records.

## What CI checks

`.github/workflows/ci.yml` runs the repo validators and tests, `check_skill.py --evals`, every skill eval suite, the Node tests, the determinism checks above, the tool registry tests (`evals/test_hub.py`) and the MCP server self-test (`python3 scripts/kosif_mcp.py --selftest`).

## Mapping the skill the REA way

`python3 scripts/rea_superpowers_map.py build` writes [superpowers-rea-map.md](../superpowers-rea-map.md), its interactive page [superpowers-rea-map.html](../superpowers-rea-map.html) and `data/superpowers_rea_map.json`: a content-addressed inventory, the Python import and invoke graph between scripts and tests, links from each script to its `data/tools.json` entry, tests, CI steps and powers, and the gaps (`gaps --kind <kind>` lists them). Run it after the chain above when scripts, tools or tests changed; CI runs only its `--self-test` and `evals/test_rea_superpowers_map.py`, so a concurrent edit elsewhere never makes it fail.

The JavaScript edges and the tree identity come from REA itself. To refresh them, run REA on the skill folder (it reads the tree as historical reference only and executes nothing), then ingest the two outputs:

```bash
rea import-reference-source .claude/skills/kosif-superpowers --detail summary --outline-depth 1 --format json > /tmp/sp_sum.json
rea import-reference-source .claude/skills/kosif-superpowers --format json > /tmp/sp_full.json
python3 scripts/rea_superpowers_map.py ingest-rea --summary /tmp/sp_sum.json --graph /tmp/sp_full.json
python3 scripts/rea_superpowers_map.py build
```

`family_without_tool` rows are informational: most method families are documented guidance with no script, which is expected; the row says where a runnable tool would help most.
