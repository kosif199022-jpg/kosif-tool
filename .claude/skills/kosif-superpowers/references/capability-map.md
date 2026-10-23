# خريطة القدرات الذهنية — Capability mind map

> **ما هذه؟** خريطة ذهنية لكل قواك: 10 مجالات → 62 عائلة → 5,426 قدرة، مع أقوى شارة دليل في كل فرع. افتحها حين تبدأ مهمة كبيرة أو حين يسألك المستخدم «تقدر تعمل إيه؟»، ثم انزل من المجال إلى العائلة إلى القدرة.
> **What it gives you:** one picture of everything you can do, so you combine powers across domains instead of reaching for the first tool you remember. Regenerate after any catalog change: `python3 scripts/powers.py mindmap` (Mermaid text) or `--html references/capability-map.html` (standalone page). Drill into one domain with `--domain mind`.

> **الخريطة المترابطة / connected graph:** [capability-graph.html](capability-graph.html) تربط كل عائلة بمستلزماتها والسكربتات التي تنفذها والاختبارات التي تثبتها (طبقة الكود من Graphify + تحليل محلي). `python3 scripts/capability_graph.py build`

## الفهرس / contents
- [1. الخريطة / the map](#1-الخريطة--the-map)
- [2. كيف تقرأها / how to read it](#2-كيف-تقرأها--how-to-read-it)
- [3. خريطة طريقة العمل / the power-up flow](#3-خريطة-طريقة-العمل--the-power-up-flow)
- [4. جسور بين المجالات / cross-domain bridges](#4-جسور-بين-المجالات--cross-domain-bridges)
- [5. اصنع خريطة ذهنية لأي شيء / mind-map anything](#5-اصنع-خريطة-ذهنية-لأي-شيء--mind-map-anything)

## 1. الخريطة / the map
كل عقدة: البادئة · عدد القدرات · أقوى شارة متاحة فيها. Each node: prefix · count · strongest badge present.

```mermaid
mindmap
  root((Kosif superpowers · 5426))
    n1["`324 · ✅42
العقل والتفكير`"]
      n2["`MODEL · 63 · 📄63
النماذج الذهنية`"]
      n3["`AMIND · 50 · 📄50
أطلس: الوكلاء والتخطيط والمراجعة`"]
      n4["`AGENT · 46 · ✅1
تنسيق الوكلاء`"]
      n5["`THINK · 46 · ✅7
نواة التفكير`"]
      n6["`SELF · 43 · ✅26
اكتشاف القدرات`"]
      n7["`CHECK · 35 · ✅4
التحقق والتقييم`"]
      n8["`IDEA · 29 · ✅2
محرك الإبداع`"]
      n9["`PLAN · 12 · ✅2
التخطيط والتنفيذ`"]
    n10["`96 · ✅26
الكتابة واللغة`"]
      n11["`WRITE · 28 · ✅11
الكتابة الطبيعية`"]
      n12["`ACRAFT · 24 · 📄24
أطلس: الكتابة والبرومبت والترجمة`"]
      n13["`ARL · 22 · ✅14
اللغة العربية`"]
      n14["`PROMPT · 22 · ✅1
صناعة البرومبت`"]
    n15["`561 · ✅60
الهندسة والكود`"]
      n16["`REA · 245 · ✅30
فحص البرامج والهندسة العكسية`"]
      n17["`ACODE · 226 · 📄226
أطلس: الهندسة والكود`"]
      n18["`CODE · 24 · ✅3
هندسة البرمجيات`"]
      n19["`SEC · 23 · ✅1
الأمان والسلامة`"]
      n20["`API · 22 · ✅15
اختبار واجهات API`"]
      n21["`GRAPH · 21 · ✅11
الرسم المعرفي والخرائط الذهنية`"]
    n22["`86 · ✅36
البيانات`"]
      n23["`ADATA · 47 · 📄47
أطلس: البيانات والتعلم الآلي`"]
      n24["`ANLY · 39 · ✅36
تحليل البيانات`"]
    n25["`79 · ✅21
المستندات`"]
      n26["`ADOCS · 45 · 📄45
أطلس: المستندات والمخططات`"]
      n27["`DOC · 34 · ✅21
المستندات والمكتب`"]
    n28["`33 · ✅10
البحث والويب`"]
      n29["`WEB · 24 · ✅10
البحث على الويب`"]
      n30["`AWEB · 9 · 📄9
أطلس: البحث والمعرفة`"]
    n31["`279 · ✅159
التطبيقات والواجهات`"]
      n32["`APPX · 139 · ✅96
قدرات التطبيقات المحللة`"]
      n33["`TOOL · 67 · ✅57
الأدوات القابلة للتشغيل`"]
      n34["`ABUILD · 50 · 📄50
أطلس: التطبيقات والواجهات والتكاملات`"]
      n35["`APP · 23 · ✅6
التطبيقات والواجهات`"]
    n36["`68 · ✅24
الصور والصوت`"]
      n37["`MEDIA · 41 · ✅24
الصور والصوت`"]
      n38["`AMEDIA · 27 · 📄27
أطلس: الصور والصوت والفيديو`"]
    n39["`80 · ✅5
المنتج والمال`"]
      n40["`ASTRAT · 62 · 📄62
أطلس: المنتج والتسويق والأعمال`"]
      n41["`PROD · 18 · ✅5
المنتج والاستراتيجية والمال`"]
    n42["`3820 · ✅547
الموشن والمونتاج`"]
      n43("`193
النص والخط`")
        n44["`ARAB · 99 · ✅23
الخط العربي المتحرك`"]
        n45["`TYPE · 94 · ✅3
التايبوغرافي اللاتيني والحركي`"]
      n46("`302
اللون والضوء والملمس`")
        n47["`TEX · 96 · ✅18
الملمس والخامات`"]
        n48["`COLOR · 87 · ✅38
الألوان واللوحات والتلوين`"]
        n49["`GLOW · 87 · ✅29
التوهج والإضاءة`"]
        n50["`RETRO · 32 · ✅10
البكسل والريترو والأساليب الخاصة`"]
      n51("`388
الشكل والحركة`")
        n52["`EASE · 102 · ✅27
التوقيت والإيقاع والتسهيل`"]
        n53["`SHAPE · 95 · ✅16
الأشكال والتحوّل`"]
        n54["`PART · 77 · ✅18
الجسيمات والسوائل والفيزياء`"]
        n55["`DRAW · 63 · ✅17
الرسم اليدوي والرسم الحي`"]
        n56["`CHAR · 51 · ✅12
الشخصيات والتحريك الهيكلي`"]
      n57("`951
الكاميرا والقطع`")
        n58["`TRANS · 474 · ✅29
الانتقالات والقطعات`"]
        n59["`CAM · 425 · ✅13
الكاميرا والتكوين`"]
        n60["`3D · 52 · ✅2
الأبعاد الثلاثية`"]
      n61("`422
الصوت والتزامن`")
        n62["`BEAT · 306 · ✅27
الموسيقى والإيقاع والمؤثرات`"]
        n63["`SYNC · 61 · ✅20
التزامن مع الكلام والترجمة`"]
        n64["`VOICE · 55 · ✅12
الصوت المولّد والتعليق`"]
      n65("`441
المحتوى والشرح`")
        n66["`DATA · 105 · ✅9
البيانات والرسوم البيانية`"]
        n67["`UI · 93 · ✅6
الواجهات والمنتجات والأجهزة`"]
        n68["`FOOT · 71 · ✅20
الصور والفيديو الخام`"]
        n69["`EXPL · 67 · ✅2
المخططات والشرح والكود`"]
        n70["`MAP · 62 · ✅4
الخرائط`"]
        n71["`BRAND · 43 · ✅8
الهوية والشعار`"]
      n72("`165
القصة والمنصات`")
        n73["`STORY · 95 · ✅14
القصة والإخراج`"]
        n74["`FMT · 70 · ✅17
المقاسات والمنصات`"]
      n75("`958
الأدوات والجودة`")
        n76["`ENG · 443 · ✅55
المحركات وخط الرندر`"]
        n77["`QA · 384 · ✅74
الجودة والتحقق`"]
        n78["`GEN · 93 · ✅14
التوليد بالذكاء الاصطناعي`"]
        n79["`MISC · 27 · ✅5
قدرات مساندة`"]
        n80["`DL · 11 · ✅5
تحميل الفيديو من الروابط`"]
```

نسخة تُفتح في المتصفح: [capability-map.html](capability-map.html) (تحمّل Mermaid 11.4.1 من jsdelivr، وتعرض قائمة نصية إن لم يتوفر الإنترنت).

## 2. كيف تقرأها / how to read it
- **المجال** (العقل، الكتابة، الكود، البيانات، المستندات، البحث، التطبيقات، الصور والصوت، المنتج والمال، الموشن) يجيب عن «في أي عالم أعمل؟».
- **العائلة** (SELF, THINK, ANLY, DOC…) تجيب عن «أي صندوق أدوات أفتح؟». فصلها في `references/powers/<family>.md`.
- **القدرة** (مثل `DOC-07`) هي الوصفة: ماذا، متى، كيف، الأرقام، أمر التثبيت، الرخصة والدليل. `python3 scripts/powers.py show DOC-07`.
- **الشارات:** ✅ شُغّل فعلًا في حاوية Claude ومعه دليل · 🟢 كود جاهز · 📦 أمر تثبيت واحد · 🔑 مفتاح أو موصل · 👁 شوهد في فيديو مرجعي · 📄 طريقة موصوفة · 💡 فكرة. ✅ دليل بتاريخ، لا وعد دائم: أعد الفحص بـ`scripts/probe_env.py` قبل الادعاء.
- A branch with only 📄/💡 means "method or idea, not yet proven here"; a branch rich in ✅ means "done before in a Claude container, re-check and go".

## 3. خريطة طريقة العمل / the power-up flow
```mermaid
mindmap
  root((مهمة جديدة · new task))
    اعرف أين أنت
      قائمة أدواتك وToolSearch
      الموصلات والمهارات
      probe_env.py
    تذكّر قواك
      powers.py suggest
      هذه الخريطة
    فكّر
      THINK حلقة التفكير
      IDEA عوامل الإبداع
    ابنِ
      أصغر نسخة مرئية أولًا
      وكلاء متوازيون AGENT
    تحقّق
      CHECK حلقة التحقق
      افتح الناتج بعينك
    سلّم بصدق
      شارة كل ادعاء
      ما فُحص وما لم يُفحص
```

## 4. جسور بين المجالات / cross-domain bridges
The most creative results come from crossing branches. Proven or ready combinations (details in [creativity.md](creativity.md)):

| الجسر / bridge | ماذا يصنع / what it makes |
|---|---|
| ANLY → DATA/motion | تحليل CSV حقيقي ثم قصة بيانات متحركة بالعربية / a real analysis turned into an animated data story |
| WEB → DOC | بحث بمصادر موثّقة ثم تقرير Word أو PDF عربي / cited research delivered as an Arabic docx or PDF |
| WRITE → VOICE → SYNC | نص بلا علامات آلية، ثم صوت، ثم كلمات متزامنة / a clean script, then a voice, then synced words |
| REA → APPX | حلّل مثبّت تطبيق بلا تشغيله، ثم حوّل مزاياه إلى وصفات مفتوحة مثبتة / analyse an app's installer without running it, then turn its features into proven open recipes |
| GRAPH → mind map | رسم معرفي لمستودع أو مجموعة مهارات ثم خريطة ذهنية / a code or skills graph turned into a mind map |
| PROD + ANLY | تسعير ونقطة تعادل محسوبة بالكود لا بالتخمين / pricing and break-even computed in code |
| APP + MEDIA | لوحة تفاعلية أو صفحة Artifact بصور معالَجة / an interactive dashboard or artifact with processed media |
| SELF → any | قبل قول «لا أستطيع»: افحص، ثبّت، جرّب / before saying "I can't": probe, install, verify |

## 5. اصنع خريطة ذهنية لأي شيء / mind-map anything
- **لمهارة أو مستودع:** ابنِ رسمًا معرفيًا بـgraphify محليًا أو عبر Graphify MCP، ثم حوّل المجتمعات إلى فروع (الطريقة في [graphify.md](graphify.md) و`proofs/general-graphify/graph_mindmap.py`).
- **لفكرة أو مشروع:** جذر = الهدف، فروع = المجالات العشرة أعلاه، أوراق = القدرات المختارة. اكتبها Mermaid `mindmap` واعرضها في Artifact أو HTML.
- **For any topic:** root = goal; first ring = the questions (who, what, constraints, risks); second ring = the powers that answer each. Render with Mermaid; keep labels short and in the user's language.
