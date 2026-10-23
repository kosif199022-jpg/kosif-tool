# REA superpowers map and frontier mining — 2026-10-23

خريطة سوبر باور بمنهج REA، وقدرات جديدة من الأطلس وREA ومستودعَي الاستنساخ وCodex. هذا إيصال دراسة: ما قُرئ، وما أُضيف، وما لم يُفعل.

This is a study receipt: what was read, what was added, and what was not done. Third-party text was read as inert data and paraphrased in our own words; nothing from the sources was executed except REA itself on this skill's own folder.

## الفهرس / contents

1. [REA on this skill](#rea-on-this-skill)
2. [The map tool](#the-map-tool)
3. [Gaps found and closed](#gaps-found-and-closed)
4. [Atlas frontier powers](#atlas-frontier-powers)
5. [REA capabilities that were missing](#rea-capabilities-that-were-missing)
6. [Lessons from the Codex clone kit and openai/codex](#lessons-from-the-codex-clone-kit-and-openaicodex)
7. [Boundaries](#boundaries)

## REA on this skill

REA 6.7.0 (`rea-agents`, MIT, source checked at morluto/rea 45a411e8 and against the user's `rea-main.zip` upload, same version) ran `import-reference-source` on `.claude/skills/kosif-superpowers`. REA's own skill says to skip REA for ordinary source-repository analysis; `import-reference-source` is the one command meant for a source tree, because it marks it as historical reference only and executes nothing. Its trimmed output is the receipt `proofs/rea-superpowers-map/receipt.json` (counts, languages, the 71 JavaScript require/import edges, the graph and root SHA-256, and REA's stated limitation about path races). REA reports no Python edges, so the map adds them from `ast`.

## The map tool

`scripts/rea_superpowers_map.py` (tool `rea-superpowers-map`, guide section in [maintain.md](guides/maintain.md#mapping-the-skill-the-rea-way)) builds [superpowers-rea-map.md](superpowers-rea-map.md) and [superpowers-rea-map.html](superpowers-rea-map.html): structure, Python import and invoke edges, script to tool to test to CI to power links, families, gaps and Atlas safe-core coverage per theme with the next candidates. `stats`, `gaps --kind`, `node <id>`, `ingest-rea` and `--self-test` work offline. Tests: `evals/test_rea_superpowers_map.py`.

## Gaps found and closed

- Eight scripts had no test, CI step or tools.json test at all (`atlas_bulk_source_audit`, `atlas_deep_fusion`, `atlas_review_summary`, `atlas_task_method_router`, `atlas_transfer`, `probe_env`, `rea_owned_repo_batch`, `rebalance_creative_repos`). `evals/test_script_smoke.py` now checks that each parses its arguments offline, and checks the Atlas method router's behaviour on its shipped manifest.
- Every one of REA's 153 CLI commands already had a power. Twelve MCP-only tools and REA's main `reverse-engineer-anything` skill did not; they are REA-246 to REA-258.
- The fusion step renamed one superpower's medoid (the Electron inspection group is now named after "Passively inspect one Electron file page"; same members), so routing case R06 now accepts either name, as was done for R07 in the Atlas-5000 batch.
- Left for a decision, not changed: 22 power families have no runnable tool in `data/tools.json` (most are documented method families, which is expected); `tools.json` marks `check-skill`, `build-chapters` and `relabel-proofs` as `untested` although CI runs them with `--check`.

## Atlas frontier powers

41 new documented powers from 55 safe-core SKILL.md files (READ_ONLY_OK, permissive license, no risk flags, re-checked with `atlas_5000.is_safe`), chosen from the least-covered themes. Evidence file: `data/atlas-frontier-mining-20261023.json` (atlas commit 99bb108d, SKILL.md SHA-256 per source).

| Power | Name | Atlas source | License | Read |
|---|---|---|---|---|
| ABUILD-51 | What/Why/How ticket and PR drafting | [communication-plugin/ticket-drafting-guidelines #7664](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2143-communication-plugin/7664-ticket-drafting-guidelines) | MIT | full |
| ABUILD-52 | Fault-domain connectivity triage without touching config | [incident-response/connectivity-triage #14217](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3494-incident-response/14217-connectivity-triage) | MIT | full |
| ACODE-227 | ruff lint and format without the select trap | [ruff/ruff #2942](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1262-ruff/2942-ruff) | MIT | first 12k chars |
| ACODE-228 | Python projects, scripts and tools with uv | [uv/uv #2951](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1273-uv/2951-uv) | MIT | first 12k chars |
| AWEB-10 | Database views over notes with Obsidian Bases | [obsidian-bases/obsidian-bases #2927](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1247-obsidian-bases/2927-obsidian-bases) | MIT | first 12k chars |
| AWEB-11 | Recognition over recall in pickers and menus | [universal-design-principles/recognition-over-recall #3771](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1503-universal-design-principles/3771-recognition-over-recall) | MIT | first 12k chars |
| ADOCS-46 | JSON-to-document templating (DOCX/XLSX/PPTX/PDF) | [carbone-skill/carbone #2177](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/931-carbone-skill/2177-carbone) | Apache-2.0 | first 12k chars |
| ADOCS-47 | True redaction and a sha256 delivery manifest | [carrel-documents/redaction-and-provenance #2838](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1195-carrel-documents/2838-redaction-and-provenance) | MIT | full |
| ADOCS-48 | Developer slide decks in Markdown with Slidev | [slidev/slidev #12191](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2938-slidev/12191-slidev) | MIT | full |
| ASTRAT-63 | One-question interview to extract real intent | [interview-me/interview-me #13638](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3225-interview-me/13638-interview-me) | MIT | first 12k chars |
| ASTRAT-64 | Tailored cover letter without AI tells | [career-tools/cover-letter-builder #13964](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3410-career-tools/13964-cover-letter-builder) | MIT | first 12k chars |
| ASTRAT-65 | Negotiation with tactical empathy and calibrated questions | [product-strategy/negotiation #14097](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3433-product-strategy/14097-negotiation) | MIT | first 12k chars |
| ASTRAT-66 | Team Topologies: four team types, three interaction modes | [systems-architecture/team-topologies #14113](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3436-systems-architecture/14113-team-topologies) | MIT | first 12k chars |
| ASTRAT-67 | Gated 8D investigation coach | [quality-engineering-skills/8d-coach #12639](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2989-quality-engineering-skills/12639-8d-coach) | MIT | full |
| ASTRAT-68 | Closable corrective action report (CAR/CAPA) | [quality-engineering-skills/car-corrective-action #12651](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2989-quality-engineering-skills/12651-car-corrective-action) | MIT | full |
| ADATA-48 | Fine-tuning dataset curation and dataset card | [llm-finetuning/dataset-curation #13287](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13287-dataset-curation) | MIT | full |
| ASTRAT-69 | LoRA and QLoRA fine-tuning recipe | [llm-finetuning/lora-qlora-recipes #13291](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13291-lora-qlora-recipes) | MIT | full |
| ADATA-49 | Anomaly detection with baseline, calibration and explained flags | [majestic-data/anomaly-detection #8242](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2207-majestic-data/8242-anomaly-detection) | MIT | full |
| ACODE-229 | Choosing DPO, ORPO, KTO or SimPO for preference tuning | [llm-finetuning/preference-optimization #13292](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3104-llm-finetuning/13292-preference-optimization) | MIT | full |
| ASTRAT-70 | Customer-support system ladder: self-service to contact center | [twilio-developer-kit/twilio-customer-support-architect #10479](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2721-twilio-developer-kit/10479-twilio-customer-support-architect) | MIT | first 12k chars |
| ASTRAT-71 | Action-first response shape for an ADHD reader | [adhd/shape #9350](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2411-adhd/9350-shape) | MIT | full |
| AMIND-51 | Plant the defect to prove a check can fail | [plant-defects/plant-defects #2243](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/959-plant-defects/2243-plant-defects) | MIT | full |
| AMIND-52 | Resumable numbered manual verification plan | [write-manual-verification-plan/write-manual-verification-plan #2276](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/992-write-manual-verification-plan/2276-write-manual-verification-plan) | MIT | full |
| ACODE-230 | MCP server design: deployment model and tool pattern before code | [mcp-server-dev/build-mcp-server #911](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/297-mcp-server-dev/911-build-mcp-server) | Apache-2.0 | full |
| ACODE-231 | Upgrade-everything audit with a risk/reward matrix | [upgrade-everything/upgrade-everything #2267](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/983-upgrade-everything/2267-upgrade-everything) | MIT | full |
| AMIND-53 | Shadow mode (dark launch) to validate a replacement under real load | [migration-patterns-plugin/shadow-mode #7804](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2160-migration-patterns-plugin/7804-shadow-mode) | MIT | full |
| ACODE-232 | False-green test detection | [falsegreen-skill/falsegreen-skill #13769](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3258-falsegreen-skill/13769-falsegreen-skill) | MIT | first 12k chars |
| ACODE-233 | Reduced-space test: decompose the equivalence claim first | [epistemic-cooperative/reduced-space-test #7155](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1990-epistemic-cooperative/7155-reduced-space-test) | MIT | first 12k chars |
| ACODE-234 | Exploratory web-app QA with full repro evidence | [agent-browser/dogfood #11671](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2887-agent-browser/11671-dogfood) | Apache-2.0 | full |
| ACODE-235 | GDPR review built on a personal-data inventory | [gdpr-review/gdpr-review #9825](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2528-gdpr-review/9825-gdpr-review) | MIT | first 12k chars |
| ACODE-236 | Narrative codebase guide for newcomers | [codebase-mapper/map-codebase-workflow #97](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/60-codebase-mapper/97-map-codebase-workflow) | MIT | full |
| ACODE-237 | Pin every version surface for supply-chain hardening | [pin-everything/pin-everything #2242](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/958-pin-everything/2242-pin-everything) | MIT | first 12k chars |
| ACRAFT-25 | Prompt governance: registry, evals, promotion and rollback | [prompt-governance/prompt-governance #548](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/179-prompt-governance/548-prompt-governance) | MIT | full |
| ACRAFT-26 | Extract a writing style into a reusable style guide | [style-extractor/style-extractor #2946](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1268-style-extractor/2946-style-extractor) | MIT | full |
| AMIND-54 | Specification refinement: gap analysis and ranked one-at-a-time questions | [specification-refiner/specification-refiner #1403](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/376-specification-refiner/1403-specification-refiner) | MIT | first 12k chars |
| ASTRAT-72 | Session report for a non-technical stakeholder | [dev-report/dev-report #2383](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1074-dev-report/2383-dev-report) | MIT | first 12k chars |
| ADOCS-49 | README that hooks in 3 seconds and runs in 60 | [docs/readme-craft #36](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/26-docs/36-readme-craft) | MIT | full |
| ADOCS-50 | Appropriate code comments: information the code cannot carry | [appropriate-comments-code/appropriate-comments-code #11563](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2854-appropriate-comments-code/11563-appropriate-comments-code) | MIT | first 12k chars |
| ADATA-50 | Pre-mortem: define success and failure before starting | [pre-mortem/pre-mortem #7548](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2123-pre-mortem/7548-pre-mortem) | MIT | full |
| ADATA-51 | Statistical process control: chart choice and capability | [quality-engineering-skills/spc-control-charts #12654](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2989-quality-engineering-skills/12654-spc-control-charts) | MIT | full |
| ADATA-52 | Trustworthy numbers from a client-rendered dashboard | [client-rendered-dashboard-data-blob/client-rendered-dashboard-data-blob #13800](https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3286-client-rendered-dashboard-data-blob/13800-client-rendered-dashboard-data-blob) | MIT | full |

Skipped after checking against main:

- #2957: method overlaps existing ADOCS-02
- #7507: already cited by ACODE-221
- #14110: already cited by ACODE-223
- #9949: already cited by ACODE-220
- #9413: method overlaps existing WEB-10
- #13862: method overlaps existing ACODE-83
- #14093: already cited by ASTRAT-58
- #2907: method overlaps existing ANLY-33
- #9828: already cited by ACODE-88
- #2934: method overlaps existing ADATA-40
- #2899: already cited by ASTRAT-54
- #8244: already cited by ACODE-85,ACODE-86,ADATA-34
- #2925: already cited by ADOCS-21
- #14283: already cited by ACODE-174

## REA capabilities that were missing

| Power | Name |
|---|---|
| REA-246 | REA MCP tool `inspect_byte_entropy`: Shannon byte entropy profile |
| REA-247 | REA MCP tool `inspect_desktop_application`: engine candidates for a desktop app folder |
| REA-248 | REA MCP tool `inspect_elf_notes`: GNU build-id and ABI-tag notes |
| REA-249 | REA MCP tool `inspect_erlang_beam`: BEAM atoms, exports and Code header |
| REA-250 | REA MCP tool `inspect_gpu_code_objects`: CUDA/HIP fatbins, CUBIN and PTX |
| REA-251 | REA MCP tool `inspect_il2cpp_metadata`: Unity IL2CPP metadata with optional binary link |
| REA-252 | REA MCP tool `inspect_model_artifact`: GGUF and safetensors declarations without loading |
| REA-253 | REA MCP tool `inspect_native_exports`: PE/ELF export table |
| REA-254 | REA MCP tool `inspect_pe_certificates`: Authenticode certificate identities |
| REA-255 | REA MCP tool `inspect_python_pyc`: CPython .pyc header and code objects |
| REA-256 | REA MCP tool `match_native_functions`: match functions across two binary versions |
| REA-257 | REA MCP tool `open_bundle_resources`: resource-only app bundle session |
| REA-258 | REA skill: reverse-engineer-anything, and when to skip REA |

## Lessons from the Codex clone kit and openai/codex

Both repositories were studied here too, but a parallel batch (PR #104) already added their lessons to the catalog, so this batch adds no duplicate cards. Use those records:

- softsweb/codex-clone-hidden-test-kit (no license file, summarised only): CHECK-31 exam sealed before the work, CHECK-32 recording mock model server, CHECK-33 observable-surface checklist, CHECK-34 scorer must score 100% on itself first, CHECK-35 honest recovery notes, and the runnable `differential-exam` tool. The kit's own numbers show why REA matters for clone work: the hard test scored 245/325 (75.4%) without mandatory REA and 320/325 (98.5%) with it.
- openai/codex (Apache-2.0, ideas only): AGENT-39 instruction layering and AGENTS.md scope, AGENT-45 tool result envelope and typed event stream, SEC-20 approval ladder, SEC-21 command segmentation and tested prefix rules.

## Boundaries

- No Atlas script, package or instruction was executed; nothing came from kosif-atlas-private; copyleft skills were excluded.
- Status of every new power is `documented`: the method was read, not run here.
- PROTOCOL.md and the protocol appendices were not touched.
- The REA receipt is a snapshot of the tree at its git head; `ingest-rea` refreshes it.
