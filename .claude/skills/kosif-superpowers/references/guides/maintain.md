# صيانة الكتالوج والمهارة — Maintaining the catalog and the skill

كل ملف مولَّد في المهارة له مصدر واحد وأمر واحد يعيد بناءه، وكل أمر بناء حتمي (تشغيلان متتاليان يعطيان الملف نفسه بايتًا ببايت)، ولكل منها وضع `--check` يستعمله CI. عدّل المصدر، ثم شغّل السلسلة بالترتيب أدناه.

Every generated file has one source and one command that rebuilds it. Every builder is deterministic (two runs give byte-identical output) and has a `--check` mode that CI runs. Edit the source, then run the chain below in order.

Commands are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless marked *(repo root)*.

<!-- hub:area:maintain:start -->

**الأدوات / tools (1)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `catalog-evidence-audit` | Statically audits every power record in data/powers/*.json for duplicate ids, malformed records and proof-link coverage, checks only whether local 'kosif-tool/...' references exist, and counts claimed statuses and proof scopes. | `python3 scripts/catalog_evidence_audit.py` | tested-here |

<!-- hub:area:maintain:end -->

## الفهرس / contents

1. [What to edit](#what-to-edit)
2. [The build chain](#the-build-chain)
3. [Adding a tool](#adding-a-tool)
4. [Adding or changing powers](#adding-or-changing-powers)
5. [What CI checks](#what-ci-checks)

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
python3 scripts/hub.py build                    # again: manifest.json, references/INDEX.md, SKILL.md and guide tool blocks
python3 scripts/boot.py --static --write        # CAPABILITIES.md + llms.txt at the repo root
python3 scripts/check_skill.py --print-counts   # paste the marker line into SKILL.md if any count changed
python3 scripts/check_skill.py --evals          # structure, links, proofs, counts, registry, secrets + routing evals
```

Then, from the repo root: `python3 tools/build.py && python3 tools/validate.py && python3 -m unittest discover -s tests`.

Check-only versions (what CI runs; they write nothing): `requirements.py derive --check`, `relabel_proofs.py --check`, `build_chapters.py --check`, `requirements.py index --check`, `capability_graph.py build --check`, `capability_atlas.py build --check`, `powers.py mindmap --html references/capability-map.html --update-md references/capability-map.md --check`, `hub.py build --check`, `boot.py --static --check`, `tools/build.py --check`.

The chapters (`build_chapters.py`) link related references but skip the generated ones (`INDEX.md`, `requirements.md`, `capability-atlas.md`, `capability-map.md`), so one pass of the chain converges whatever order those are rebuilt in.

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
