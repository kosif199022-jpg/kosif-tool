# KOSIF Capability Atlas — Claude discovery index

Generated from real repository data. Catalog evidence is NOT a live execution receipt.

**5,727 powers / 62 families / 10 domains / 22 route descriptions.**

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

### build: 401 powers

- runnable-tools: 167
- app-feature-transfer: 155
- atlas-build: 52
- apps-artifacts: 27

### code: 629 powers

- atlas-code: 277
- software-investigation: 258
- code-engineering: 26
- knowledge-graph: 23
- security-safety: 23
- api-testing: 22

### craft: 119 powers

- prompt-craft: 41
- writing-humanizer: 28
- atlas-craft: 26
- arabic-language: 22
- typography-arabic: 2

### data: 95 powers

- atlas-data: 56
- data-analysis: 39

### docs: 89 powers

- atlas-docs: 55
- documents-office: 34

### media: 68 powers

- media-image-audio: 41
- atlas-media: 27

### mind: 351 powers

- mental-models: 63
- atlas-mind: 60
- agent-orchestration: 55
- thinking-core: 47
- self-discovery: 43
- verification-evals: 40
- creativity-engine: 29
- planning-execution: 14

### motion: 3,833 powers

- transitions-cuts: 475
- engines-render-pipeline: 445
- camera-composition-layout: 425
- qa-verification: 384
- music-beat-sound: 306
- easing-timing-rhythm: 106
- charts-data-infographic: 105
- shapes-morph-geometry: 97
- typography-arabic: 97
- texture-material: 96
- story-direction-ideas: 95
- ai-generation: 94
- typography-latin: 94
- ui-product-device: 93
- color-palette-grading: 87
- light-glow-bloom: 87
- particles-fluids-physics: 77
- photo-video-footage: 71
- formats-platforms: 70
- diagrams-explainers-code: 69
- hand-drawn-draw-on: 65
- maps-geo: 62
- audio-sync-captions: 61
- voice-tts: 55
- 3d-spatial: 53
- characters-rigs: 51
- brand-logo-identity: 43
- pixel-retro-stylized: 32
- other: 27
- video-download: 11

### research: 37 powers

- web-research: 26
- atlas-research: 11

### strategy: 105 powers

- atlas-strategy: 87
- strategy-finance: 18

## Decision flow

User task -> bilingual matching -> capability IDs -> exact source & proof -> prerequisites
-> obra Superpowers workflow SKILL.md -> authorized execution -> tests and output receipts.

Data: data/capability_atlas_index.json; originals: data/powers/*.json;
routes: data/capability_routes.json; workflows: vendor/obra-superpowers-v7/skills/
