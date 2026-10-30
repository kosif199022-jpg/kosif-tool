# Claude: understand KOSIF in under three minutes

## 30-second map
Full catalog: 5,857 power records, 62 families, 15 groups; 202 tool records in existing manifest.
Classification is NOT proof of runtime compatibility. Respect each power's status, requirements, proof.

## Commands (run from .claude/skills/kosif-superpowers)
```sh
python scripts/smart_capabilities.py groups
python scripts/smart_capabilities.py find "رسم خطوط وأشكال" --json
python scripts/hub.py find "<user task>" --json
python scripts/hub.py doctor --json
python scripts/smart_capabilities.py verify
```

## Group routing cheatsheet

- **البحث والمعرفة** (`research`, 60): atlas-research, web-research, knowledge-graph
- **التفكير والتخطيط والاستراتيجية** (`thinking`, 402): atlas-mind, atlas-strategy, creativity-engine, mental-models, planning-execution, prompt-craft, strategy-finance, thinking-core
- **الوكلاء والتوجيه الذكي** (`agents`, 276): agent-orchestration, runnable-tools, self-discovery
- **البرمجة وبناء التطبيقات** (`software`, 692): app-feature-transfer, apps-artifacts, atlas-build, atlas-code, code-engineering, ui-product-device
- **الرسم والأشكال والتصميم** (`drawing`, 306): brand-logo-identity, diagrams-explainers-code, hand-drawn-draw-on, pixel-retro-stylized, shapes-morph-geometry
- **الصور والتحرير والتوليد** (`images`, 323): ai-generation, atlas-media, color-palette-grading, media-image-audio, photo-video-footage
- **الثري دي والمحاكاة والرندر** (`3d`, 758): 3d-spatial, engines-render-pipeline, light-glow-bloom, particles-fluids-physics, texture-material
- **الموشن والمونتاج والسينما** (`motion`, 1,233): camera-composition-layout, characters-rigs, easing-timing-rhythm, formats-platforms, story-direction-ideas, transitions-cuts, video-download
- **الصوت والموسيقى والتعليق** (`audio`, 422): audio-sync-captions, music-beat-sound, voice-tts
- **الخطوط والنصوص العربية واللاتينية** (`type`, 215): arabic-language, typography-arabic, typography-latin
- **البيانات والرسوم والمواقع** (`data`, 268): atlas-data, charts-data-infographic, data-analysis, maps-geo
- **المستندات والكتابة** (`documents`, 148): atlas-craft, atlas-docs, documents-office, writing-humanizer
- **الاختبارات والجودة والأمان** (`quality`, 469): api-testing, qa-verification, security-safety, verification-evals
- **التحليل العكسي وفحص البرامج** (`reverse`, 258): software-investigation
- **قدرات مساندة غير مصنفة** (`misc`, 27): other

## Work without losing provenance

1. Route user task to a group using smart_capabilities.py find.
2. Inspect specific power IDs and actual tool cards with hub.py.
3. Check present requirements using hub.py doctor.
4. Use REA for legitimate source/metadata-assisted inspections, Ghidra for authorized binaries only.
5. Do not claim modules are interoperable until an end-to-end test passes.
6. Document executable pipelines with inputs, outputs, error handling and proofs.
