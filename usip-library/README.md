# مكتبة بروتوكول USIP v5.5 الكاملة / the full USIP v5.5 protocol library

> مولّدة بـ `python3 .claude/skills/kosif-superpowers/scripts/smart_capabilities.py cards` من كتالوج KOSIF وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا، وتُفحص بـ `cards-check`. النواة المحمولة للصق: [USIP_PORTABLE.md](../.claude/skills/kosif-superpowers/USIP_PORTABLE.md).

## الفهرس / contents

- [ما هذه المكتبة](#ما-هذه-المكتبة)
- [بطاقات القدرات](#بطاقات-القدرات)
- [بطاقات الأدوات](#بطاقات-الأدوات)
- [المناهج](#المناهج)
- [الروابط الخام](#الروابط-الخام)

## ما هذه المكتبة

بطاقة بروتوكول لكل قدرة في الكتالوج (5,482) ولكل أداة قابلة للتشغيل (143)، في 78 ملفًا و408,409 سطرًا تقريبًا مع هذا الفهرس. كل بطاقة تجمع سجل القدرة نفسه (ما هي، متى، كيف، التثبيت، المتطلبات، الأدلة، الرخصة) مع قواعد البروتوكول مطبّقة عليها: خانات الاستقبال (A25)، والجاهزية والشارة الصادقة (A28)، وموضعها عقدةً منمّطة في الخطة (A26)، وبوابة التحقق لنوع مخرجها (A27)، وسلم التعافي لأخطائها المرجحة (A29). القواعد العامة تتكرر عمدًا في كل بطاقة لتُقرأ البطاقة وحدها؛ والمعرفة الفريدة في سجلات الكتالوج والملاحق. حالة الكتالوج ليست حالة الجلسة: افحص قبل أي شارة.

## بطاقات القدرات

| المجموعة | العائلة | البطاقات | الأسطر | الملف |
|---|---|---:|---:|---|
| الثري دي والمحاكاة والرندر | `3d-spatial` | 52 | 3,660 | [cards/3d/3d-spatial.md](cards/3d/3d-spatial.md) |
| الثري دي والمحاكاة والرندر | `engines-render-pipeline` | 443 | 30,775 | [cards/3d/engines-render-pipeline.md](cards/3d/engines-render-pipeline.md) |
| الثري دي والمحاكاة والرندر | `light-glow-bloom` | 87 | 6,191 | [cards/3d/light-glow-bloom.md](cards/3d/light-glow-bloom.md) |
| الثري دي والمحاكاة والرندر | `particles-fluids-physics` | 77 | 5,293 | [cards/3d/particles-fluids-physics.md](cards/3d/particles-fluids-physics.md) |
| الثري دي والمحاكاة والرندر | `texture-material` | 96 | 6,666 | [cards/3d/texture-material.md](cards/3d/texture-material.md) |
| الوكلاء والتوجيه الذكي | `agent-orchestration` | 46 | 3,169 | [cards/agents/agent-orchestration.md](cards/agents/agent-orchestration.md) |
| الوكلاء والتوجيه الذكي | `runnable-tools` | 69 | 4,912 | [cards/agents/runnable-tools.md](cards/agents/runnable-tools.md) |
| الوكلاء والتوجيه الذكي | `self-discovery` | 43 | 3,070 | [cards/agents/self-discovery.md](cards/agents/self-discovery.md) |
| الصوت والموسيقى والتعليق | `audio-sync-captions` | 61 | 4,404 | [cards/audio/audio-sync-captions.md](cards/audio/audio-sync-captions.md) |
| الصوت والموسيقى والتعليق | `music-beat-sound` | 306 | 21,436 | [cards/audio/music-beat-sound.md](cards/audio/music-beat-sound.md) |
| الصوت والموسيقى والتعليق | `voice-tts` | 55 | 3,931 | [cards/audio/voice-tts.md](cards/audio/voice-tts.md) |
| البيانات والرسوم والمواقع | `atlas-data` | 52 | 3,626 | [cards/data/atlas-data.md](cards/data/atlas-data.md) |
| البيانات والرسوم والمواقع | `charts-data-infographic` | 105 | 7,557 | [cards/data/charts-data-infographic.md](cards/data/charts-data-infographic.md) |
| البيانات والرسوم والمواقع | `data-analysis` | 39 | 2,742 | [cards/data/data-analysis.md](cards/data/data-analysis.md) |
| البيانات والرسوم والمواقع | `maps-geo` | 62 | 4,405 | [cards/data/maps-geo.md](cards/data/maps-geo.md) |
| المستندات والكتابة | `atlas-craft` | 26 | 1,807 | [cards/documents/atlas-craft.md](cards/documents/atlas-craft.md) |
| المستندات والكتابة | `atlas-docs` | 50 | 3,473 | [cards/documents/atlas-docs.md](cards/documents/atlas-docs.md) |
| المستندات والكتابة | `documents-office` | 34 | 2,363 | [cards/documents/documents-office.md](cards/documents/documents-office.md) |
| المستندات والكتابة | `writing-humanizer` | 28 | 1,947 | [cards/documents/writing-humanizer.md](cards/documents/writing-humanizer.md) |
| الرسم والأشكال والتصميم | `brand-logo-identity` | 43 | 3,143 | [cards/drawing/brand-logo-identity.md](cards/drawing/brand-logo-identity.md) |
| الرسم والأشكال والتصميم | `diagrams-explainers-code` | 67 | 4,805 | [cards/drawing/diagrams-explainers-code.md](cards/drawing/diagrams-explainers-code.md) |
| الرسم والأشكال والتصميم | `hand-drawn-draw-on` | 63 | 4,594 | [cards/drawing/hand-drawn-draw-on.md](cards/drawing/hand-drawn-draw-on.md) |
| الرسم والأشكال والتصميم | `pixel-retro-stylized` | 32 | 2,317 | [cards/drawing/pixel-retro-stylized.md](cards/drawing/pixel-retro-stylized.md) |
| الرسم والأشكال والتصميم | `shapes-morph-geometry` | 95 | 6,846 | [cards/drawing/shapes-morph-geometry.md](cards/drawing/shapes-morph-geometry.md) |
| الصور والتحرير والتوليد | `ai-generation` | 93 | 6,756 | [cards/images/ai-generation.md](cards/images/ai-generation.md) |
| الصور والتحرير والتوليد | `atlas-media` | 27 | 1,908 | [cards/images/atlas-media.md](cards/images/atlas-media.md) |
| الصور والتحرير والتوليد | `color-palette-grading` | 87 | 6,445 | [cards/images/color-palette-grading.md](cards/images/color-palette-grading.md) |
| الصور والتحرير والتوليد | `media-image-audio` | 41 | 2,892 | [cards/images/media-image-audio.md](cards/images/media-image-audio.md) |
| الصور والتحرير والتوليد | `photo-video-footage` | 71 | 5,194 | [cards/images/photo-video-footage.md](cards/images/photo-video-footage.md) |
| قدرات مساندة غير مصنفة | `other` | 27 | 1,904 | [cards/misc/other.md](cards/misc/other.md) |
| الموشن والمونتاج والسينما | `camera-composition-layout` | 425 | 32,479 | [cards/motion/camera-composition-layout.md](cards/motion/camera-composition-layout.md) |
| الموشن والمونتاج والسينما | `characters-rigs` | 51 | 4,026 | [cards/motion/characters-rigs.md](cards/motion/characters-rigs.md) |
| الموشن والمونتاج والسينما | `easing-timing-rhythm` | 102 | 8,061 | [cards/motion/easing-timing-rhythm.md](cards/motion/easing-timing-rhythm.md) |
| الموشن والمونتاج والسينما | `formats-platforms` | 70 | 5,549 | [cards/motion/formats-platforms.md](cards/motion/formats-platforms.md) |
| الموشن والمونتاج والسينما | `story-direction-ideas` | 95 | 7,557 | [cards/motion/story-direction-ideas.md](cards/motion/story-direction-ideas.md) |
| الموشن والمونتاج والسينما | `transitions-cuts` | 474 | 36,547 | [cards/motion/transitions-cuts.md](cards/motion/transitions-cuts.md) |
| الموشن والمونتاج والسينما | `video-download` | 11 | 856 | [cards/motion/video-download.md](cards/motion/video-download.md) |
| الاختبارات والجودة والأمان | `api-testing` | 22 | 1,577 | [cards/quality/api-testing.md](cards/quality/api-testing.md) |
| الاختبارات والجودة والأمان | `qa-verification` | 384 | 27,964 | [cards/quality/qa-verification.md](cards/quality/qa-verification.md) |
| الاختبارات والجودة والأمان | `security-safety` | 23 | 1,636 | [cards/quality/security-safety.md](cards/quality/security-safety.md) |
| الاختبارات والجودة والأمان | `verification-evals` | 35 | 2,548 | [cards/quality/verification-evals.md](cards/quality/verification-evals.md) |
| البحث والمعرفة | `atlas-research` | 11 | 757 | [cards/research/atlas-research.md](cards/research/atlas-research.md) |
| البحث والمعرفة | `knowledge-graph` | 21 | 1,507 | [cards/research/knowledge-graph.md](cards/research/knowledge-graph.md) |
| البحث والمعرفة | `web-research` | 24 | 1,655 | [cards/research/web-research.md](cards/research/web-research.md) |
| التحليل العكسي وفحص البرامج | `software-investigation` | 258 | 19,140 | [cards/reverse/software-investigation.md](cards/reverse/software-investigation.md) |
| البرمجة وبناء التطبيقات | `app-feature-transfer` | 139 | 10,422 | [cards/software/app-feature-transfer.md](cards/software/app-feature-transfer.md) |
| البرمجة وبناء التطبيقات | `apps-artifacts` | 23 | 1,649 | [cards/software/apps-artifacts.md](cards/software/apps-artifacts.md) |
| البرمجة وبناء التطبيقات | `atlas-build` | 52 | 3,767 | [cards/software/atlas-build.md](cards/software/atlas-build.md) |
| البرمجة وبناء التطبيقات | `atlas-code` | 237 | 17,013 | [cards/software/atlas-code.md](cards/software/atlas-code.md) |
| البرمجة وبناء التطبيقات | `code-engineering` | 24 | 1,726 | [cards/software/code-engineering.md](cards/software/code-engineering.md) |
| البرمجة وبناء التطبيقات | `ui-product-device` | 93 | 6,839 | [cards/software/ui-product-device.md](cards/software/ui-product-device.md) |
| التفكير والتخطيط والاستراتيجية | `atlas-mind` | 54 | 3,679 | [cards/thinking/atlas-mind.md](cards/thinking/atlas-mind.md) |
| التفكير والتخطيط والاستراتيجية | `atlas-strategy` | 72 | 4,908 | [cards/thinking/atlas-strategy.md](cards/thinking/atlas-strategy.md) |
| التفكير والتخطيط والاستراتيجية | `creativity-engine` | 29 | 2,024 | [cards/thinking/creativity-engine.md](cards/thinking/creativity-engine.md) |
| التفكير والتخطيط والاستراتيجية | `mental-models` | 63 | 4,414 | [cards/thinking/mental-models.md](cards/thinking/mental-models.md) |
| التفكير والتخطيط والاستراتيجية | `planning-execution` | 12 | 820 | [cards/thinking/planning-execution.md](cards/thinking/planning-execution.md) |
| التفكير والتخطيط والاستراتيجية | `prompt-craft` | 22 | 1,526 | [cards/thinking/prompt-craft.md](cards/thinking/prompt-craft.md) |
| التفكير والتخطيط والاستراتيجية | `strategy-finance` | 18 | 1,209 | [cards/thinking/strategy-finance.md](cards/thinking/strategy-finance.md) |
| التفكير والتخطيط والاستراتيجية | `thinking-core` | 46 | 3,214 | [cards/thinking/thinking-core.md](cards/thinking/thinking-core.md) |
| الخطوط والنصوص العربية واللاتينية | `arabic-language` | 22 | 1,525 | [cards/type/arabic-language.md](cards/type/arabic-language.md) |
| الخطوط والنصوص العربية واللاتينية | `typography-arabic` | 99 | 7,248 | [cards/type/typography-arabic.md](cards/type/typography-arabic.md) |
| الخطوط والنصوص العربية واللاتينية | `typography-latin` | 94 | 6,893 | [cards/type/typography-latin.md](cards/type/typography-latin.md) |

## بطاقات الأدوات

| المجال | الأدوات | الأسطر | الملف |
|---|---:|---:|---|
| `3d` | 11 | 521 | [tools/3d.md](tools/3d.md) |
| `audio` | 3 | 157 | [tools/audio.md](tools/audio.md) |
| `discover` | 24 | 1,247 | [tools/discover.md](tools/discover.md) |
| `draw` | 11 | 549 | [tools/draw.md](tools/draw.md) |
| `edit` | 13 | 661 | [tools/edit.md](tools/edit.md) |
| `image` | 9 | 495 | [tools/image.md](tools/image.md) |
| `investigate` | 13 | 597 | [tools/investigate.md](tools/investigate.md) |
| `local-computer` | 1 | 53 | [tools/local-computer.md](tools/local-computer.md) |
| `maintain` | 12 | 603 | [tools/maintain.md](tools/maintain.md) |
| `motion` | 18 | 978 | [tools/motion.md](tools/motion.md) |
| `sources` | 17 | 852 | [tools/sources.md](tools/sources.md) |
| `think` | 11 | 580 | [tools/think.md](tools/think.md) |

## المناهج

- [أنماط الاستدلال](methods/reasoning-modes.md)
- [النماذج الذهنية](methods/mental-models.md)
- [معايير الجودة وسلالم التعافي](methods/quality-and-recovery.md)

## الروابط الخام

- هذا الفهرس: <https://raw.githubusercontent.com/kosif199022-jpg/kosif-tool/main/usip-library/README.md>
- أي ملف: `https://raw.githubusercontent.com/kosif199022-jpg/kosif-tool/main/usip-library/<المسار>` (مثلًا `https://raw.githubusercontent.com/kosif199022-jpg/kosif-tool/main/usip-library/cards/motion/transitions-cuts.md`)
- النسخة المجمعة في ملف واحد: `smart_capabilities.py cards --single <الملف>`.

