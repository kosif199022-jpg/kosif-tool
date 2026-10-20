# KOSIF Capability Atlas — Claude discovery index

Generated from real repository data. Catalog evidence is NOT a live execution receipt.

**4,751 powers / 52 families / 10 domains / 22 route descriptions.**

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

### build: 142 powers

- app-feature-transfer: 119
- apps-artifacts: 23

### code: 327 powers

- software-investigation: 241
- code-engineering: 24
- api-testing: 22
- knowledge-graph: 21
- security-safety: 19

### craft: 72 powers

- writing-humanizer: 28
- arabic-language: 22
- prompt-craft: 22

### data: 39 powers

- data-analysis: 39

### docs: 34 powers

- documents-office: 34

### media: 34 powers

- media-image-audio: 34

### mind: 260 powers

- mental-models: 63
- thinking-core: 46
- self-discovery: 43
- agent-orchestration: 38
- creativity-engine: 29
- verification-evals: 29
- planning-execution: 12

### motion: 3,801 powers

- transitions-cuts: 473
- engines-render-pipeline: 443
- camera-composition-layout: 424
- qa-verification: 383
- music-beat-sound: 305
- charts-data-infographic: 105
- easing-timing-rhythm: 102
- texture-material: 96
- typography-arabic: 96
- shapes-morph-geometry: 95
- story-direction-ideas: 94
- ai-generation: 93
- ui-product-device: 93
- typography-latin: 92
- color-palette-grading: 87
- light-glow-bloom: 87
- particles-fluids-physics: 76
- formats-platforms: 70
- photo-video-footage: 68
- diagrams-explainers-code: 65
- hand-drawn-draw-on: 62
- maps-geo: 62
- audio-sync-captions: 60
- voice-tts: 55
- 3d-spatial: 52
- characters-rigs: 51
- brand-logo-identity: 43
- pixel-retro-stylized: 32
- other: 27
- video-download: 10

### research: 24 powers

- web-research: 24

### strategy: 18 powers

- strategy-finance: 18

## Decision flow

User task -> bilingual matching -> capability IDs -> exact source & proof -> prerequisites
-> obra Superpowers workflow SKILL.md -> authorized execution -> tests and output receipts.

Data: data/capability_atlas_index.json; originals: data/powers/*.json;
routes: data/capability_routes.json; workflows: vendor/obra-superpowers-v7/skills/
