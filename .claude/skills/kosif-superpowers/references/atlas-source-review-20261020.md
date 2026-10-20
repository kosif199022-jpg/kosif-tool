# KOSIF Atlas — source-inspection receipt (20 October 2026)

## Scope and limitations

* Atlas pinned commit: `99bb108dff169880dd531359f474a01b73c4b233`.
* Catalog records inspected structurally: **14,793** (14,708 regular and 85 copyleft).
* Source `SKILL.md` files actually read: **395/395** in the stratified plan.
* Files with one or more heuristic warning signals: **39**. Warnings are not proof of maliciousness; absence is not a safety guarantee.
* Source frontmatter present: **394**; name matching metadata: **379**.
* Candidate records meeting review metadata gates: **258**. Neither live execution nor licensing authenticity verified.
* Newly routed original method summaries: **24** across **12** domains.
* No external skill scripts, packages, or instructions were executed. Copyleft reference skills were not merged.

## Warning patterns observed

- credential_reference: 19 file(s)
- data_upload_instruction: 2 file(s)
- destructive_shell: 3 file(s)
- disable_protection: 1 file(s)
- one_liner_install: 6 file(s)
- prompt_override_language: 7 file(s)
- remote_command: 2 file(s)

## Reviewed method guidance (non-executable)

### reasoning (32 sampled sources)
- **causal-root-review** from [5why-root-cause](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/2989-quality-engineering-skills/12659-5why-root-cause/SKILL.md), source SHA-256 `492a3f50c07ede34...` — Define the observed failure; distinguish symptoms from causes; challenge each causal link; verify a corrective action.
- **external-factor-matrix** from [pestle-analysis](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/2883-pm-product-strategy/11656-pestle-analysis/SKILL.md), source SHA-256 `6b264055b74a8632...` — Separate political, economic, social, technology, legal and environmental drivers; score impact; record supporting evidence.

### agents (32 sampled sources)
- **bounded-agent-orchestration** from [agent-team-orchestration](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3263-agent-team-orchestration/13774-agent-team-orchestration/SKILL.md), source SHA-256 `9c880067ee743349...` — Break work into independent tasks; assign explicit boundaries; require evidence receipts; reconcile overlapping outputs.
- **agent-permission-gates** from [agent-runtime-guardrails](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3045-adlc-agent-engineering/13086-agent-runtime-guardrails/SKILL.md), source SHA-256 `d366e800e6b887d5...` — Identify trusted boundaries; allowlist available tools; request confirmation for side effects; log rejected actions.

### engineering (32 sampled sources)
- **code-quality-review** from [improve-code-quality](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3431-metaskills/14084-improve-code-quality/SKILL.md), source SHA-256 `bb4ec46eadb0e1aa...` — Establish tests; identify hotspots; make minimal changes; compare behavior and maintainability.
- **architecture-tradeoff-review** from [architecture-optimization](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3431-metaskills/14073-architecture-optimization/SKILL.md), source SHA-256 `f52ac42637adf012...` — Measure constraints; compare architectures; estimate migration risk; test a reversible pilot.

### reverse_engineering (28 sampled sources)
- **native-evidence-tracing** from [binary-analysis-patterns](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3512-reverse-engineering/14279-binary-analysis-patterns/SKILL.md), source SHA-256 `895c49228f3ed121...` — Hash authorized artifact; identify sections and imports; trace functions and references; document uncertainty before implementing original code.
- **forensic-memory-boundary** from [memory-forensics](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3512-reverse-engineering/14280-memory-forensics/SKILL.md), source SHA-256 `051546e6887f9143...` — Preserve chain of custody; inventory memory images; correlate process indicators; report evidence and limits.

### security (32 sampled sources)
- **code-review-security-gates** from [coderabbit-security-basics](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/1840-coderabbit-pack/5385-coderabbit-security-basics/SKILL.md), source SHA-256 `14981a3849dd829c...` — Enumerate input and trust boundaries; inspect secret handling; review authorization paths; require tests before approving.
- **media-credential-boundaries** from [runway-security-basics](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/1900-runway-pack/6672-runway-security-basics/SKILL.md), source SHA-256 `92cfa43ba9e044be...` — Map content and credential flows; protect tokens and user assets; evaluate retention and permissions; verify policy compliance.

### finance (32 sampled sources)
- **month-end-close-checklist** from [fondo-core-workflow-a](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/1857-fondo-pack/5748-fondo-core-workflow-a/SKILL.md), source SHA-256 `015e798393d829ea...` — Collect ledgers and supporting evidence; reconcile accounts; record adjustments and approvals; review reports before closing.
- **runway-finance-scenarios** from [bootstrapped-finance](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/2209-majestic-founder/8265-bootstrapped-finance/SKILL.md), source SHA-256 `de29492e6ccb8455...` — Identify cash constraints; model revenue and cost scenarios; stress-test assumptions; monitor runway triggers.

### media_motion (32 sampled sources)
- **cinematic-motion-design** from [awwwards-motion](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md), source SHA-256 `e08b590217f823c4...` — Define design language; plan timed shots and eased motion; render reference frames; inspect motion continuity.
- **render-performance-profiling** from [fix-web-rendering-performance](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/1530-webcraft/4192-fix-web-rendering-performance/SKILL.md), source SHA-256 `f5b00c2437618115...` — Measure frame time; locate layout, paint or GPU bottlenecks; optimize only measured causes; regress-test frames.

### design (32 sampled sources)
- **interface-heuristic-audit** from [web-design-guidelines](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/1434-react-skills/3420-web-design-guidelines/SKILL.md), source SHA-256 `633dd3e7fc44b1df...` — Audit hierarchy, contrast and accessibility; inspect density at mobile and desktop widths; repair defects; validate usability.
- **app-improvement-loop** from [improve-app](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3431-metaskills/14082-improve-app/SKILL.md), source SHA-256 `c2843b034b11593c...` — Identify the primary user journey; measure friction; prototype prioritized changes; compare usability and errors.

### research (32 sampled sources)
- **claim-source-verification** from [ai-citation-verification](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/229-mas-ai-workflows/715-ai-citation-verification/SKILL.md), source SHA-256 `1f10b26b5a9aca2b...` — Separate claims from sources; check links and original context; resolve contradictions; retain provenance.
- **premortem-counterfactual** from [pre-mortem](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/2123-pre-mortem/7548-pre-mortem/SKILL.md), source SHA-256 `d67f70acc7b87afd...` — Define success criteria; imagine project failure; rank causes; add mitigation gates.

### web_apps (32 sampled sources)
- **browser-compat-qa** from [browser-compat](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3165-browser-compat/13494-browser-compat/SKILL.md), source SHA-256 `9927a0cb1472c8f7...` — Define browser matrix; test critical flows; inspect incompatibilities; retest fixes in representative environments.
- **frontend-review-protocol** from [review-frontend-workflow](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/67-frontend-review/117-review-frontend-workflow/SKILL.md), source SHA-256 `606ae7e25dfa5aad...` — Inventory routes and states; exercise interactions; inspect responsive layouts; document failures with reproduction.

### documents (32 sampled sources)
- **source-document-structured-reading** from [deepread](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/219-deepread/696-deepread/SKILL.md), source SHA-256 `d36bb7b98610b4cf...` — Identify document scope; extract arguments and evidence; check gaps and ambiguities; summarize with references.
- **structured-8d-report** from [8d-problem-solving](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/2989-quality-engineering-skills/12660-8d-problem-solving/SKILL.md), source SHA-256 `69fc87e295f05f59...` — Record incident and containment; diagnose causes; validate corrective action; document prevention and effectiveness.

### language (32 sampled sources)
- **natural-voice-editing** from [anti-ai-writing-patterns](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/50-text-humanizer/72-anti-ai-writing-patterns/SKILL.md), source SHA-256 `385684c9addc0ddb...` — Identify generic phrasing; preserve factual meaning; tighten voice and rhythm; verify clarity and naturalness.
- **human-centered-language-review** from [humanize](https://github.com/kosif199022-jpg/kosif-atlas/blob/99bb108dff169880dd531359f474a01b73c4b233/skills/3536-humanize/14319-humanize/SKILL.md), source SHA-256 `5de2daf064902f89...` — Match audience and dialect; edit repetitive phrases; protect technical accuracy; compare before and after.

## Integration

Use `python scripts/atlas_reviewed_methods_v3.py --doctor` or the `--task` option within the skill directory.
The selector only returns provenance-backed guidance, not executable external tooling, and does not bypass permission requirements.

## Machine-readable sampled-source evidence

The [395-record source-audit receipt](../data/atlas-source-evidence-395-20261020.json) publishes per-file source hashes, warning-category flags, path, scope and metadata verdict; it deliberately excludes third-party source bodies and any private machine secrets.

## Evidence location

Full local review: `C:\KOSIF\atlas-superpowers-audit\source_audit.json` (local evidence, not published because of size).
Catalog index SHA-256: `cc34646fdb2654d5505416d13ecc9155dd667db857c26ea14214f4a4272fc4b4` (main).
