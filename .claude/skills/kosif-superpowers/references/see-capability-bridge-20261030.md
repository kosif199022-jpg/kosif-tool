# KOSIF SEE v1.7.6 → Superpowers — Capability Bridge

**Source verified:** Owned private `kosif-see` package version **1.7.6**, release `pluginrel_6ad4ee3c22fc8191b49c4301dae57833`, inspected 2026-10-30. **Target:** this repository's existing `kosif-superpowers` skill. This is a **public, safe, independent method/contract integration** — not a vendor of the private SEE source tree, packaged media, hidden backend, authentication, or credentials.

## Activate the integration

Use `python3 scripts/see_capability_bridge.py --catalog` to enumerate the methods and owners, then `python3 scripts/see_capability_bridge.py --task "طابق دفتر الحسابات" --mode deep` to obtain a read-only routing receipt. For a referenced video: add `--reference-video` **only if a real reference video was actually supplied**. Run `python3 scripts/see_capability_bridge.py --self-test` or `python3 -m unittest evals/test_see_capability_bridge.py` locally from the skill directory. This script never invokes a plugin or executes a side effect.

The canonical first entry remains **`scripts/hub.py find`** and the USIP pipeline; the new bridge adds specific SEE routing and guards, not a competing front door. Read [A12 Cognitive Fusion](protocol/A12-see-pro-cognitive-fusion.md) and canonical [PROTOCOL](../../PROTOCOL.md), open only matched materials.

## Eleven Stage-0 lenses carried over

1. Objective, constraints, output and success criteria.
2. Independent and adversarial perspectives.
3. Decision sensitivity and the assumptions that flip a recommendation.
4. Premortem / red-team failure hypotheses.
5. Fact, inference, unknown and cited evidence separation.
6. Forecasting ranges and calibrated uncertainty.
7. Explicit acceptance criteria and hard-fail tests.
8. PRD / business requirements and rollout.
9. Architecture, dependencies and failure boundaries.
10. Deterministic quantitative and financial checks.
11. Causal mechanism, alternative explanations and falsification.

Fast tasks use these compactly. Deep tasks expand only relevant lenses. **Full Pro requires request-bound service receipts, not just this checklist.**

## All nine stable SEE method domains

| SEE domain | Superpowers routing contract | Evidence/owner boundary |
|---|---|---|
| Research & Evidence | `kosif-research-evidence` → A6 | Sources, claim ledger and freshness checks |
| Agent Contracts | `kosif-agent-contracts` → A2 | Typed I/O, retries, permission/side-effect owner |
| Eval & Trust | `kosif-eval-trust` → A9 | Shadow evaluation, deterministic acceptance tests |
| Engineering Reliability | `kosif-engineering-reliability` → A16 | Reproduce/isolate/fix/regression; REA/Graphify only when exposed |
| Product Strategy | `kosif-product-strategy` → A18 | PRD, options, premortem, decision sensitivity |
| Finance & Data | `kosif-finance-data` → A6 | IFRS/Excel/SQL methods; exact numeric lock |
| Prompt Architecture | `kosif-prompt-architecture` → A33 | Source-safe prompts and injection boundaries |
| Media & Motion | `kosif-media-motion` → A8 | Video, audio, Suno, timing, render QA |
| Skill Orchestrator | `kosif-skill-orchestrator` → A10 | Baseline → shadow tests → guarded promotion |

**Loading cap:** normal 2 packs total with at most 1 dynamic specialist; Deep / Full Pro 4 packs total with at most 2 dynamic specialists; load one dynamic artifact at a time. A 15K skill catalog is candidate metadata, **not** 15K installed or executed skills.

## Specialist capabilities and collision guards

- **Images:** Visual Prompt Core takes precedence for image-only generation prompts; do not silently convert them to video.
- **Suno:** song/lyrics, title, style and exclusion sections; never claim audio generation from instructions.
- **Video imitation:** requires an actual reference video for verified fidelity; route to Media & Motion and external **KOSIF Montage & Motion** only when callable and authorized; FFmpeg/file checks prove output, not a prompt.
- **General cinematic production:** use current native media pipeline and source/asset rights with rendered MP4 QA.
- **Humanizer:** writing-specific rewrite with evidence retention, no fabricated facts.
- **Prompt optimization:** output prompt, not silently run another application.
- **Graphify/REA:** method and impact checks; never reverse-engineer absent binaries or imply a local tool is running.
- **Business & finances:** deterministic arithmetic and company isolation before synthesizing conclusions.
- **Dynamic specialists:** only when a **named gap** remains after local coverage; obtain current KOSIF Think or permissive Atlas evidence, then inspect the finalist. On stale metadata use local fallback.
- **Self-evolution:** baseline and hypothesis → reversible change → trigger/no-trigger/collision/fallback checks → integrity/license/security checks → measured comparison → guarded release → read-back → immutable repair log.
- **Cognitive Core / Council:** reviewer failures are isolated; an index of 500 expert cards is not 500 live reviewers.
- **ECC / project memory:** only opt-in, project-scoped evidence. No learning across company boundaries without separate approval.
- **Full Pro:** direct host tool → modern mobile bridge → fresh status-verified compatibility bridge → `FULL_PRO_BLOCKED / NOT_FULL_PRO`; never infer success from tool availability.

## Owner and execution truth

SEE's canonical owner map is **Think** (reasoning and Full Pro), **Computer** (browser/desktop), **WhatsApp** (messages), **Voice Director** (audio), **Jev Browser** (browser ambiguity), and **Release Bridge** (releases). For reference imitation, KOSIF Montage & Motion is a separate specialist owner.

Capability transitions: `candidate → selected → method_loaded → executor_exposed → configured/authorized → executed → verified`. Only observed **request-bound runtime receipts and artifact QA** justify executed/verified. The bridge intentionally emits `NOT_EXECUTED`. It neither changes the private SEE plugin's source nor turns Superpowers into these independent backends.

## Shadow coverage and deployment constraints

Regression checks cover simple task; research; engineering; self-improvement; image-only; Suno; reference-video positive and missing reference; text rewrite collision; general video; finance; WhatsApp; device; Full Pro no fake completion; dynamic-gap eligible but not activated; 11 lenses; 9 packs; limits and unexecuted receipts.

Never place private plugin `SYSTEM_REGISTRY.json`, private skill source, binary media, keys, emails, private user data or copyrighted third-party assets into this **public** repository merely because the user asked to merge capabilities. This bridge transfers *methodology and routing contracts*, not plugin source. For full code replication, use an owner-authorized private destination, audit licenses, and verify dependency/build/run behavior separately.
