# أفلام وإثباتات / Proofs

> **What this gives you:** the index of every proof folder in this skill: original motion films rendered in a Claude container, and the general proofs (data, documents, media, writing, code graphs, self-discovery) that back the ✅ badges outside motion.
> **Open it when:** you need to show that a power really ran, re-run a proof on a new machine, or copy a working starting point. Each folder's README holds the exact commands, numbers and limits.

## الفهرس / contents
1. أفلام الحركة — Motion proof films (15)
2. إثباتات عامة — General proofs (7)
3. تشغيلات إضافات الحركة v2 — Runs behind the v2 motion additions
4. ملاحظات — Notes

## 1. أفلام الحركة — Motion proof films

أفلام أصلية رُندرت في هذه الحاوية بـ `kosif-tool/tools/render_html.cjs` وفُحصت بـ `tools/verify_video.py`؛ نتيجة الفحص وأوامر إعادة الرندر في README كل مجلد. الـMP4 لا يُحفظ في المستودع.
Original films rendered with `render_html.cjs` and checked with `verify_video.py`; each folder's README gives the check result and the re-render commands. MP4s are not committed.

| الفيلم / film | ماذا يثبت / what it proves | المقاس / size |
|---|---|---|
| [arabic-voice-kinetic](arabic-voice-kinetic/README.md) | صوت عربي مولّد (Piper) ← كلمات تدخل على موعد نطقها (أقصى فرق 33 مللي ثانية)، ضوء فجر، Amiri، -14 LUFS | 1080×1920 |
| [audio-reactive-spectrum](audio-reactive-spectrum/README.md) | طيف دائري من تحليل FFT لكل إطار + كاريوكي عربي بقناع RTL | 1080×1080 |
| [neon-glow](neon-glow/README.md) | لافتة نيون عربية «قهوة» تشتعل، توهج بخمس طبقات، انعكاس أرض مبتلة، صوت طنين | 1080×1920 |
| [glass-luxury-logo](glass-luxury-logo/README.md) | بطاقات زجاجية بعمق، شعار عربي ذهبي بلمعة معدنية، رسم شعار حي | 1920×1080 |
| [particles-to-arabic](particles-to-arabic/README.md) | 6,000 جسيم في حقل curl-noise تتجمّع كلمة «إبداع» من صورتها المشكَّلة (الحروف متصلة) ثم تنفجر جمرات بسحب بصيغة مغلقة، صوت -14 LUFS | 1080×1920 |
| [data-story](data-story/README.md) | أعمدة بنابض وتتابع 75 ms، عدّاد ميكانيكي، تحوّل الأعمدة إلى حلقة، خط إشارة وتعليق، أرقام هندية عربية (بيانات توضيحية، صامت) | 1920×1080 |
| [map-route](map-route/README.md) | خريطة d3-geo من world-atlas، مسار القاهرة ← الإسكندرية ← سيوة بطول القوس، دبابيس مرتدة، عدّاد هافرسين ٦٥٧ كم (صامت) | 1080×1920 |
| [beat-sync](beat-sync/README.md) | حلقة طبول 120 BPM مولّدة ← كشف الضربات بـlibrosa ← كلمات عربية وأشكال تنبض 1.0→1.15→1.0 خلال 120 ms، قطع كل مازورة، شبكة إيقاع؛ قياس على الـMP4: 32/32، متوسط الفرق 6.5 ms، -14 LUFS | 1080×1080 |
| [ui-phone-demo](ui-phone-demo/README.md) | تطبيق عربي RTL على هاتف (العتاد غير معكوس): نقر بموجة لمس، لوحة سفلية بنابض، تمرير بقصور ذاتي، إشعار الجزيرة الديناميكية، بطاقة دعوة (صامت) | 1080×1920 |
| [pixel-art](pixel-art/README.md) | شبكة 160×160 ×6.75، لوحة 16 لونًا، حركة متدرجة 8 fps، دورة مشي 4 إطارات، دفعة عملات، كلمة «نور» نقطية مرسومة باليد بحروف متصلة (صامت) | 1080×1080 |
| [texture-lab](texture-lab/README.md) | تكوين متحرك واحد بأربع خامات مكتوبة يدويًا: حبيبات فيلم مبذورة، نقاط CMYK بشاشات تدور، ريزوغراف بحبرين وانزياح تسجيل، شاشة CRT بتحدّب وانحراف لوني (صامت) | 1920×1080 |
| [character-rig](character-rig/README.md) | شخصية مسطحة بـIK بعظمتين، مشية، تهيؤ وقفزة وهبوط، فقاعة كلام عربية، صوت مولّد؛ 13/13 | 1920×1080 |
| [transitions-reel](transitions-reel/README.md) | ثمانية انتقالات مسمّاة بين بطاقات عربية (iris، wipe، zoom-through، glitch، whip، light-leak…)؛ 13/13 | 1080×1920 |
| [three-bloom-scene](three-bloom-scene/README.md) | بلّورة ضوء ثلاثية الأبعاد بـThree.js: عقدة زجاج فيزيائي بخيط مضيء يُرسم، حلقات مدارية متوهجة، 2,600 جسيم، UnrealBloom، كاميرا تقترب وتدور وتفسح مكانًا لعنوان عربي (صامت، WebGL برمجي) | 1920×1080 |
| [whiteboard-draw](whiteboard-draw/README.md) | شرح على سبورة بقلم ماركر بترتيب يد إنسان: عنوان عربي يُكتب من اليمين، شمس وقطرة وأسهم سببية، تظليل مقصوص على الشكل، القلم يُرفع بين الضربات، صوت صرير مولّد من جدول الضربات؛ 13/13 | 1080×1920 |

الخطوط المشتركة في [`_shared/fonts`](_shared/fonts) (رخصة OFL: Amiri، Cairo، Reem Kufi، Aref Ruqaa، Tajawal، Lalezar، Space Grotesk، JetBrains Mono). / Shared fonts live in `_shared/fonts` (OFL); each family's licence travels next to it as `OFL-<Family>.txt`.

## 2. إثباتات عامة — General proofs

Proof folders for the non-motion domains, each run in a Claude Code cloud container on 2026-10-16. Versions and installed tools change per machine: re-run the folder's commands (and `scripts/probe_env.py`) before relying on a number.

| المجلد / folder | ماذا يثبت / what it proves | الفحص / checks |
|---|---|---|
| [general-discovery](general-discovery/README.md) | اكتشاف القدرات خطوة خطوة: الأدوات، المهارات، البيئة، الشبكة، الحزم، أسماء المفاتيح دون قيمها — the self-discovery steps (SELF-*) with observed results | 21 probes (P1–P21) |
| [general-data](general-data/README.md) | تحليل بيانات بأرقام مطابقة بثلاث طرق (pandas وDuckDB)، رسوم بتسميات عربية، رياضيات دقيقة ومحاكاة مخاطر، ولوحة RTL — data analysis, dashboards and strategy maths (ANLY-*, APP-*, PROD-*) | 17/17 |
| [general-docs](general-docs/README.md) | مستندات عربية وإنجليزية DOCX وXLSX وPPTX وPDF تُكتب وتُحوَّل وتُقرأ وتُصوَّر وتُقرأ آليًا، والتقاط الويب — office documents and web capture (DOC-*, WEB-*) | 24/24 + 3/3 |
| [general-media](general-media/README.md) | صور ونصوص عربية مقروءة آليًا (OCR)، ضغط وجودة، لوحة ألوان، رمز QR، وتحليل صوت وتوحيد جهارته وقصّه — images, OCR and audio (MEDIA-*) | 16/16 |
| [general-writing](general-writing/README.md) | سكربتات الكتابة (`tell_scan.py`، `anchor_gate.py`) وأدوات اللغة العربية على نصوص أصلية — writing and Arabic-language powers (WRITE, PROMPT-02, ARL) | 58/58 |
| [general-graphify](general-graphify/README.md) | خريطة معرفة للكود بلا مفتاح: تثبيت Graphify، رسم الكود، الاستعلام، أثر التغيير، خادم MCP محلي وموصل مستضاف — code knowledge graph (GRAPH-*, CODE-03, SEC-14) | run log in folder |
| [general-earlier-runs](general-earlier-runs/README.md) | سجل مشحون لتشغيلات جلسة سابقة كانت أدلتها في ملفات مؤقتة فقط (Hugging Face، torch للمعالج، تحديث Graphify وتكامله مع Claude Code) — shipped log of earlier-session runs (WEB-08, SELF-28, GRAPH-05, GRAPH-09) | HF re-run 2/2; rest marked not re-run |

## 3. تشغيلات إضافات الحركة v2 — Runs behind the v2 motion additions

The v2 motion additions (`*-X01…` IDs in the motion families) did not need a new film. Their runs (speed-shape maths, frame-diff and text-contrast ports, the owner's music, sound and lens scripts, a frame-accurate trim test and a Playwright UI recording) are logged with commands and numbers in [`references/external-skills.md` §15](../references/external-skills.md), and the two ported tools are printed in §10 of that file. Our own harnesses for V1, V2 and V8 ship in [motion-v2](motion-v2/README.md) with captured output. Records that rest on the owner's unvendored scripts (V4–V7, the song film's analyze.py) are 📄, not ✅.

## 4. ملاحظات — Notes
- Every film follows the `seek(t)` contract: each frame is a pure function of time with seeded randomness, so frames render in any order.
- Silent films say so; films with sound keep the generated or supplied audio untouched and land near −14 LUFS.
- Proof folders hold scripts, data, contact sheets and READMEs only; regenerate large outputs with the commands inside.
