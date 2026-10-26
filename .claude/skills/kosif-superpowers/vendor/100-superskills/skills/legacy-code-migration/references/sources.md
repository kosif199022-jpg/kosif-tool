# مصادر «تحديث الكود القديم والترحيل» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## strangler-fig-migration (2325-legacy-modernization)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/legacy-modernization
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2325-legacy-modernization/8928-strangler-fig-migration
- الوصف: Plan an incremental strangler-fig migration off a legacy system — a facade routing one capability at a time to a new implementation behind an anti-corruption layer. Reach for this instead of a big-bang rewrite.

```markdown
# Skill: Strangler-fig migration

Replace the old system one capability at a time, value landing continuously, rollback always a route-flip away (§2 #4).

## Step 1 — Place the facade
Put an interception point (gateway / facade / abstraction) in front of the legacy system so requests can be routed to old *or* new per capability.

## Step 2 — Pick the first capability
Choose a slice that is high-value or high-risk-to-learn and has a clean seam (from `codebase-archaeologist`). Small enough to ship; meaningful enough to prove the pattern.

## Step 3 — Build behind an anti-corruption layer
Implement the new version with an ACL translating between the legacy model and the new model (§2 #5), so the old quirks don't leak into the new design.

## Step 4 — Route incrementally
Shift traffic for that capability gradually (canary / cohort), watching SLOs and reconciliation. Keep the old path live as the rollback.

## Step 5 — Repeat, then remove the facade
Migrate capabilities one by one until the legacy system is dead, then retire the facade. Branch-by-abstraction is the in-process variant of the same idea.

> Decision support: the cutover-strategy tree in [`../../knowledge/legacy-modernization-decision-trees.md`](../../knowledge/legacy-modernization-decision-trees.md) and the pattern catalog in [`../../knowledge/modernization-patterns-reference.md`](../../knowledge/modernization-patterns-reference.md).
```

## assemblyai-upgrade-migration (1828-assemblyai-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/assemblyai-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1828-assemblyai-pack/5108-assemblyai-upgrade-migration
- الوصف: Migrate legacy AssemblyAI Streaming v2 and LeMUR integrations to Streaming v3 and LLM Gateway with parity evidence. Use when removing deprecated contracts. Trigger with "migrate AssemblyAI", "LeMUR migration", or "Streaming v3 upgrade".

```markdown
# AssemblyAI v3 and LLM Gateway Migration

## Overview

Migrate legacy AssemblyAI Streaming v2 and LeMUR integrations to Streaming v3 and LLM Gateway with parity evidence. Treat live audio, transcript content, credentials, spend, and destructive state as separately governed boundaries.

## Prerequisites

- The target repository or integration path and the requested operator outcome.
- The AssemblyAI project, environment, region, data classification, and accountable owner.
- Current first-party documentation plus credentials only for a narrowly approved live check.

## Current Contract

Streaming v2 used `/v2/realtime/ws`; v3 uses `/v3/ws` with different messages, turns, configuration, and termination. LeMUR sunset on March 31, 2026; LLM Gateway is the current analysis path. Deprecated transcript summary parameters must not anchor new designs.

## Authentication

For live work, inject `ASSEMBLYAI_API_KEY` from an approved secret manager and send the raw value only in the AssemblyAI `Authorization` header to the configured first-party host. Never print, commit, place in a URL, or expose it to an untrusted client. Callback secrets and temporary streaming tokens are separate credentials.

## Instructions

1. Inventory endpoints, SDK methods, handlers, fixtures, dashboards, and legacy credentials.
2. Capture approved legacy behavior with synthetic golden cases.
3. Map v2 messages and shutdown to v3 begin, turns, configuration, and termination.
4. Map LeMUR prompts and outputs to schema-constrained LLM Gateway requests.
5. Compare quality, latency, structured results, privacy, and cost.
6. Canary the new route, test rollback, then remove legacy code and secrets.

## Tool Discipline

Use Read, Glob, and Grep to inspect repository code, configuration, fixtures, and evidence. Use Write and Edit only for approved implementation or documentation changes. Do not call AssemblyAI, upload audio, open a streaming session, mint a token, replay a callback, deploy, rotate a key, or delete a transcript merely because this skill was invoked.

## Approval Boundaries

Require an accountable owner before live audio processing, production credential or endpoint changes, paid model or capacity changes, content retention, callback replay, deployment, or deletion. Read-only repository inspection and synthetic offline validation do not authorize live vendor actions.

## Failure Modes

- Changing only the WebSocket URL leaves v2 handlers broken.
- LeMUR calls after sunset are a hard migration defect.
- LLM parity needs semantic and schema assertions, not byte equality.

## Output
```

## bamboohr-upgrade-migration (1830-bamboohr-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/bamboohr-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1830-bamboohr-pack/5144-bamboohr-upgrade-migration
- الوصف: Migrate a BambooHR integration across SDK, OpenAPI, auth, dataset, or endpoint changes with pinned evidence, dual-read comparison, and rollback. Use when replacing legacy report/dataset calls or upgrading an official SDK. Trigger with "upgrade BambooHR", "BambooHR migration", or "BambooHR deprecated API".

```markdown
# BambooHR Upgrade and Migration

## Overview

Move one contract boundary at a time and prove semantic parity on authorized
data. A repository default branch is not a released package; a README install
line is not registry evidence; and a `v1` URL does not mean the operation is
free from deprecation.

## Prerequisites

- The target repository or integration path and the requested operator outcome.
- The tenant, identity, and data scope only when approved live work is in scope.
- The current evidence register plus customer-specific permissions and agreements.

## Current Contract

- Dataset v1 data retrieval is deprecated in favor of
  `POST /api/v2/datasets/{datasetName}/data`.
- Saved/custom report operations carry replacement notices in the current SDK docs.
- Official Python and PHP SDK repositories were updated 2026-08-31. PHP package
  `bamboohr/api` 2.0.1 is on Packagist. Python `bamboohr-sdk` 1.0.0 is described
  in source but was absent from public PyPI and had no tag/release on 2026-09-11.

## Authentication

Preserve the existing identity during endpoint/SDK migration unless auth change
is the explicit workstream. If migrating API key to OAuth, treat registration,
state validation, token storage, refresh, permission equivalence, and revocation
as a separate staged migration with independent rollback.

## Instructions

1. Freeze the current adapter, dependency lock, endpoint inventory, auth mode,
   fields, filters, pagination, error mapping, retry policy, and production metrics.
2. Pin target OpenAPI/SDK evidence to an immutable commit, tag, or registry
   artifact. Verify package availability, integrity, license, and runtime support.
3. Diff operations, required parameters, auth scopes, status codes, response
   shapes, deprecations, pagination, retry behavior, and model return types.
4. Put old and new implementations behind the same application adapter. Keep
   writes on the old path while dual-reading a minimized approved cohort.
5. Compare record identities, field semantics, null/absent/redacted values,
   inactive/future cases, ordering, page completion, and error behavior. Do not
   log differing employee values; report aliases and counts.
6. Canary the new read path, then separately stage any idempotent write path with
   before/after verification and explicit approval.
7. Maintain checkpoints that both versions understand or define a reversible
   conversion. Do not let rollback replay completed HR mutations.
8. Remove old code only after the observation window, reconciliation, dependency
   scan, runbook update, and rollback retirement approval.

## Tool Discipline

Use Read, Glob, and Grep to inventory current contracts and versions. Use
Write/Edit only for approved adapters, migrations, tests, and docs. This skill
```

## techsmith-upgrade-migration (1909-techsmith-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/techsmith-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1909-techsmith-pack/6889-techsmith-upgrade-migration
- الوصف: Upgrade Snagit or Camtasia with entitlement checks, immutable backups, canaries, project-format boundaries, and reversible endpoint rollout. Use when changing product versions or retiring legacy media. Trigger with "upgrade TechSmith", "migrate Camtasia project", or "convert Snagit library".

```markdown
# TechSmith Versioned Upgrade and Media Migration

## Overview

This skill treats application upgrade and content conversion as separate transactions. It preserves original libraries/projects, pins the tools needed for legacy formats, validates copies on a canary, and never assumes backward compatibility.

## Prerequisites

- Source and target product/version, platform, license eligibility, and installer hashes
- Immutable backup of Snagit library or standalone/zipped Camtasia projects plus checksums
- Representative canary assets and acceptance criteria
- Rollback endpoint/package and owners for content conversion

## Tool Discipline

Use `Read`, `Glob`, and `Grep` to inspect local scripts, manifests, logs, and tests. Use `WebFetch` only for current primary TechSmith documentation. Use `Write` or `Edit` only after confirming the target repository file and approval boundary.

## Current Contract

- Camtasia projects are not backward-compatible; collaborators must align on the same version.
- Camtasia 2020+ does not open CAMPROJ or CAMREC directly; CAMPROJ requires an intermediate 9/2018/2019 save to TSCPROJ, while CAMREC must be produced in an older version.
- Snagit 2022 introduced SNAGX; export to standard formats while a usable Snagit entitlement is available when long-term portability is required.
- Never overwrite originals during canary conversion or uninstall user data as part of application rollback.

## Licensing and Authentication

TechSmith desktop activation is not API authentication. Resolve individual sign-in versus business-key or approved offline activation before execution. Redact all keys, account identifiers, activation artifacts, and sensitive endpoint details.

## Instructions

1. Inventory endpoints, entitlements, integrations, COM clients, project/library formats, share outputs, and collaborators.
2. Back up original content immutably, record hashes, and verify restore before installing the target version.
3. Read target release and deployment guidance; identify removed exporter, executable, codec, project, and policy changes.
4. Upgrade one canary endpoint and test launch, activation, COM creation, recorder discovery, representative open/edit/export, and rollback.
5. Convert copies through the documented intermediate versions or batch-export path; retain original-to-result mapping and validation.
6. Promote by endpoint ring, monitor failures, and retire legacy tooling only after recovery and audit windows expire.

## Approval Boundaries

Do not bulk-convert the only copy, open a project in a newer version before preserving a rollback copy, or assume a subscription unlocks every historical version.

## Output
```

## together-upgrade-migration (1910-together-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/together-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1910-together-pack/6905-together-upgrade-migration
- الوصف: Migrate Together AI Python SDK v1, OpenAI-compatible clients, deprecated models, or legacy dedicated endpoints with inventory, contract tests, canaries, and rollback. Use when upgrading Together dependencies or provider resources. Trigger with "upgrade Together SDK", "Together model migration", or "migrate Together endpoint v1".

```markdown
# Together AI Upgrade and Migration

## Overview

This skill moves one Together contract at a time while preserving response, model-quality, cost, and rollback evidence.

## Prerequisites

- An inventory of SDK versions, API calls, model IDs, and dedicated resources
- Current migration, model lifecycle, and deprecation documentation
- Golden requests/evaluations plus latency and cost baselines
- A rollback target and owners for traffic, data, billing, and teardown

## Tool Discipline

Use `Read`, `Glob`, and `Grep` to locate dependencies, direct calls, model constants, response assumptions, and endpoint management. Use `WebFetch` for current migration and deprecation contracts. Use `Write` or `Edit` only after scope and rollback are agreed.

## Current Contract

- Python v1 is maintenance-only; new features target `together>=2.0.0` and may use changed method/response shapes.
- OpenAI-compatible migration requires Together's base URL, project key, and Together model IDs.
- Same-lineage model upgrades may redirect after notice; materially new models require explicit migration and evaluation.
- New dedicated capacity uses v2 DMI; legacy v1 create/restart paths are retired.

## Authentication

Preserve project-scoped `TOGETHER_API_KEY` injection while changing clients or endpoints. Never reuse development keys in production or expose a key during dual-run comparison.

## Instructions

1. Classify the migration as SDK, model, compatibility layer, or dedicated endpoint and freeze the baseline.
2. Inventory every call, parameter, response field, model, job, retry, and management resource in scope.
3. Build contract and golden-quality tests before changing dependencies or routing.
4. Implement the target behind a reversible configuration or traffic boundary.
5. Canary with sanitized requests; compare behavior, latency, usage, errors, limits, and cost.
6. Promote explicitly, monitor, remove obsolete resources only after retention/rollback approval, and update the runbook.

## Approval Boundaries

Do not accept silent model substitution, delete legacy endpoints, revoke keys, or shift production traffic without evaluated behavior and an executable rollback.

## Output

Return source/target contracts, inventory, test delta, canary metrics, model/deprecation evidence, traffic state, rollback proof, obsolete-resource disposition, and owners.

## Error Handling

| Condition | Response |
|---|---|
| SDK response shape changes | Adapt at the provider boundary and keep caller contracts stable. |
| Model quality regresses | Roll back routing and revisit the candidate. |
| Legacy endpoint cannot restart | Move to v2 DMI; do not rely on v1 recovery. |
| Redirect is detected | Record the effective model and run migration evaluations. |

## Examples
```

## adobe-upgrade-migration (1819-adobe-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/adobe-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1819-adobe-pack/4916-adobe-upgrade-migration
- الوصف: Migrate Adobe integrations away from Service Account JWT, Photoshop v1, retired Lightroom Firefly Services, or drifting SDK/API contracts with canaries and rollback. Use when the task requires adobe end-of-life and contract migration. Trigger with "upgrade Adobe integration", "migrate Adobe JWT", or "Photoshop v2 migration".

```markdown
# Adobe End-of-Life and Contract Migration

## Overview

Migrate Adobe integrations away from Service Account JWT, Photoshop v1, retired Lightroom Firefly Services, or drifting SDK/API contracts with canaries and rollback. This workflow produces a reviewable artifact and evidence before any live side effect.

## Prerequisites

- Current first-party Adobe documentation for every selected service, API version, auth flow, limit, and lifecycle.
- Named product, identity, security, data, budget, release, and operations owners appropriate to the scope.
- Synthetic or approved non-production fixtures with secret and content canaries.

## Current Contract

Service Account JWT is deprecated. Photoshop API v1 and the Firefly Services Lightroom API are already end-of-life; Remove Background uses Photoshop v2. Do not conflate the retired Lightroom service with separate Lightroom consumer APIs; confirm the dated retirement evidence in the reference map. Recheck the dated evidence map before relying on mutable product behavior.

## Authentication

Preserve current and target credential, organization, scopes, profiles, and last-use evidence during auth migration. Old-secret or old-credential deletion is irreversible and happens only after verified cutover.

## Instructions

1. Inventory JWT code/configuration, endpoint versions, Lightroom service calls, SDK locks, fixtures, dashboards, and runbooks.
2. Trace every behavior to current first-party docs and classify supported, deprecated, retired, undocumented, or environment-observed.
3. Define target OAuth, Photoshop v2, replacement/retirement, adapter, data, and rollback contracts.
4. Build parity fixtures and dual-run or shadow-read comparisons where they do not duplicate spend or writes.
5. Canary the target, verify outputs and observability, then cut traffic under declared thresholds.
6. Remove obsolete paths and approved credentials, scan for residue, and publish cutover plus rollback receipts.

## Tool Discipline

Use Read, Glob, and Grep to inspect current documentation, configuration, code, fixtures, and evidence. Use Write and Edit only for approved repository artifacts. Skill invocation alone does not authorize network access, credentials, Adobe content, consent, uploads, generation, spend, deployment, registration changes, replay, cancellation, or deletion.

## Approval Boundaries

Identity/security owners approve auth changes and deletions; product/data owners approve API replacement and live comparisons; release owner approves cutover and rollback.

## Error Handling

- Do not leave JWT or v1 as a production fallback.
- Do not substitute a similarly named Lightroom API without contract proof.
- Roll back on output, authorization, storage, spend, or event drift.

## Output
```
