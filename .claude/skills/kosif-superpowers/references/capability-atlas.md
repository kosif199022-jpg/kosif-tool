# KOSIF Capability Atlas — Claude discovery index

Generated from real repository data. Catalog evidence is NOT a live execution receipt.

**5,601 powers / 62 families / 10 domains / 22 route descriptions.**

For a task in the user's words, `python3 scripts/hub.py find "<task>"` combines this atlas with the runnable tools and guides.

## الفهرس / contents

1. [Claude task protocol](#claude-task-protocol)
2. [Commands](#commands)
3. [Evidence model](#evidence-model)
4. [Families by domain](#families-by-domain)
5. [Decision flow](#decision-flow)

## Claude task protocol

1. Read this guide and the KOSIF master SKILL.md; do not load all power JSON files into context.
2. Run: python scripts/capability_atlas.py plan "<exact user task>" --json
3. Select matching capability IDs, process skills and candidate routes; inspect full entry with show ID.
4. Check requirements, local environment, authorization and licensing before running a tool.
5. Execute the actual task, test results, cite receipts, and report what remains unverified.

## Commands

    python scripts/capability_atlas.py stats --json
    python scripts/capability_atlas.py search "جرد مستودع قطع غيار" --top 10 --json
    python scripts/capability_atlas.py plan "Build a secure accounting app" --json
    python scripts/capability_atlas.py show DOC-05 --json
    python scripts/capability_atlas.py doctor --json
    python scripts/capability_atlas.py build

## Evidence model

- proven: recorded proof only, NOT proof of execution on this host.
- ready: catalog claims readiness; still verify environment.
- install/key: prerequisite or consent required; do not install or retrieve secrets automatically.
- seen/documented/idea: informational, not independently verified execution.
- Requirement detection is local and read-only; npm/API/remote services are not assumed available.
- Rebuild after source catalog edits; index freshness is verified by SHA-256.

## Families by domain

### build: 373 powers

- runnable-tools: 159
- app-feature-transfer: 139
- atlas-build: 52
- apps-artifacts: 23

### code: 595 powers

- software-investigation: 258
- atlas-code: 247
- code-engineering: 24
- security-safety: 23
- api-testing: 22
- knowledge-graph: 21

### craft: 119 powers

- prompt-craft: 41
- writing-humanizer: 28
- atlas-craft: 26
- arabic-language: 22
- typography-arabic: 2

### data: 91 powers

- atlas-data: 52
- data-analysis: 39

### docs: 84 powers

- atlas-docs: 50
- documents-office: 34

### media: 68 powers

- media-image-audio: 41
- atlas-media: 27

### mind: 328 powers

- mental-models: 63
- atlas-mind: 54
- agent-orchestration: 46
- thinking-core: 46
- self-discovery: 43
- verification-evals: 35
- creativity-engine: 29
- planning-execution: 12

### motion: 3,818 powers

- transitions-cuts: 474
- engines-render-pipeline: 443
- camera-composition-layout: 425
- qa-verification: 384
- music-beat-sound: 306
- charts-data-infographic: 105
- easing-timing-rhythm: 102
- typography-arabic: 97
- texture-material: 96
- shapes-morph-geometry: 95
- story-direction-ideas: 95
- typography-latin: 94
- ai-generation: 93
- ui-product-device: 93
- color-palette-grading: 87
- light-glow-bloom: 87
- particles-fluids-physics: 77
- photo-video-footage: 71
- formats-platforms: 70
- diagrams-explainers-code: 67
- hand-drawn-draw-on: 63
- maps-geo: 62
- audio-sync-captions: 61
- voice-tts: 55
- 3d-spatial: 52
- characters-rigs: 51
- brand-logo-identity: 43
- pixel-retro-stylized: 32
- other: 27
- video-download: 11

### research: 35 powers

- web-research: 24
- atlas-research: 11

### strategy: 90 powers

- atlas-strategy: 72
- strategy-finance: 18

## Decision flow

User task -> bilingual matching -> capability IDs -> exact source & proof -> prerequisites
-> obra Superpowers workflow SKILL.md -> authorized execution -> tests and output receipts.

Data: data/capability_atlas_index.json; originals: data/powers/*.json;
routes: data/capability_routes.json; workflows: vendor/obra-superpowers-v7/skills/
