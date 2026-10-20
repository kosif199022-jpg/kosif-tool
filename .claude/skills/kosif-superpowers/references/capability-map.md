# خريطة القدرات الذهنية — Capability mind map

> **ما هذه؟** خريطة ذهنية لكل قواك: 10 مجالات → 61 عائلة → 5,185 قدرة، مع أقوى شارة دليل في كل فرع. افتحها حين تبدأ مهمة كبيرة أو حين يسألك المستخدم «تقدر تعمل إيه؟»، ثم انزل من المجال إلى العائلة إلى القدرة.
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
  root((Kosif superpowers · 5185))
    n1["`300 · ✅42
العقل والتفكير`"]
      n2["`MODEL · 63 · 📄63
النماذج الذهنية`"]
      n3["`THINK · 46 · ✅7
نواة التفكير`"]
      n4["`SELF · 43 · ✅26
اكتشاف القدرات`"]
      n5["`AMIND · 40 · 📄40
أطلس: الوكلاء والتخطيط والمراجعة`"]
      n6["`AGENT · 38 · ✅1
تنسيق الوكلاء`"]
      n7["`IDEA · 29 · ✅2
محرك الإبداع`"]
      n8["`CHECK · 29 · ✅4
التحقق والتقييم`"]
      n9["`PLAN · 12 · ✅2
التخطيط والتنفيذ`"]
    n10["`72 · ✅26
الكتابة واللغة`"]
      n11["`WRITE · 28 · ✅11
الكتابة الطبيعية`"]
      n12["`ARL · 22 · ✅14
اللغة العربية`"]
      n13["`PROMPT · 22 · ✅1
صناعة البرومبت`"]
    n14["`503 · ✅60
الهندسة والكود`"]
      n15["`REA · 241 · ✅30
فحص البرامج والهندسة العكسية`"]
      n16["`ACODE · 176 · 📄176
أطلس: الهندسة والكود`"]
      n17["`CODE · 24 · ✅3
هندسة البرمجيات`"]
      n18["`API · 22 · ✅15
اختبار واجهات API`"]
      n19["`GRAPH · 21 · ✅11
الرسم المعرفي والخرائط الذهنية`"]
      n20["`SEC · 19 · ✅1
الأمان والسلامة`"]
    n21["`86 · ✅36
البيانات`"]
      n22["`ADATA · 47 · 📄47
أطلس: البيانات والتعلم الآلي`"]
      n23["`ANLY · 39 · ✅36
تحليل البيانات`"]
    n24["`50 · ✅21
المستندات`"]
      n25["`DOC · 34 · ✅21
المستندات والمكتب`"]
      n26["`ADOCS · 16 · 📄16
أطلس: المستندات والمخططات`"]
    n27["`32 · ✅10
البحث والويب`"]
      n28["`WEB · 24 · ✅10
البحث على الويب`"]
      n29["`AWEB · 8 · 📄8
أطلس: البحث والمعرفة`"]
    n30["`232 · ✅152
التطبيقات والواجهات`"]
      n31["`APPX · 119 · ✅96
قدرات التطبيقات المحللة`"]
      n32["`TOOL · 60 · ✅50
الأدوات القابلة للتشغيل`"]
      n33["`ABUILD · 30 · 📄30
أطلس: التطبيقات والواجهات والتكاملات`"]
      n34["`APP · 23 · ✅6
التطبيقات والواجهات`"]
    n35["`45 · ✅24
الصور والصوت`"]
      n36["`MEDIA · 34 · ✅24
الصور والصوت`"]
      n37["`AMEDIA · 11 · 📄11
أطلس: الصور والصوت والفيديو`"]
    n38["`64 · ✅5
المنتج والمال`"]
      n39["`ASTRAT · 46 · 📄46
أطلس: المنتج والتسويق والأعمال`"]
      n40["`PROD · 18 · ✅5
المنتج والاستراتيجية والمال`"]
    n41["`3801 · ✅542
الموشن والمونتاج`"]
      n42("`188
النص والخط`")
        n43["`ARAB · 96 · ✅22
الخط العربي المتحرك`"]
        n44["`TYPE · 92 · ✅2
التايبوغرافي اللاتيني والحركي`"]
      n45("`302
اللون والضوء والملمس`")
        n46["`TEX · 96 · ✅18
الملمس والخامات`"]
        n47["`COLOR · 87 · ✅38
الألوان واللوحات والتلوين`"]
        n48["`GLOW · 87 · ✅29
التوهج والإضاءة`"]
        n49["`RETRO · 32 · ✅10
البكسل والريترو والأساليب الخاصة`"]
      n50("`386
الشكل والحركة`")
        n51["`EASE · 102 · ✅27
التوقيت والإيقاع والتسهيل`"]
        n52["`SHAPE · 95 · ✅16
الأشكال والتحوّل`"]
        n53["`PART · 76 · ✅17
الجسيمات والسوائل والفيزياء`"]
        n54["`DRAW · 62 · ✅17
الرسم اليدوي والرسم الحي`"]
        n55["`CHAR · 51 · ✅12
الشخصيات والتحريك الهيكلي`"]
      n56("`949
الكاميرا والقطع`")
        n57["`TRANS · 473 · ✅28
الانتقالات والقطعات`"]
        n58["`CAM · 424 · ✅13
الكاميرا والتكوين`"]
        n59["`3D · 52 · ✅2
الأبعاد الثلاثية`"]
      n60("`420
الصوت والتزامن`")
        n61["`BEAT · 305 · ✅27
الموسيقى والإيقاع والمؤثرات`"]
        n62["`SYNC · 60 · ✅20
التزامن مع الكلام والترجمة`"]
        n63["`VOICE · 55 · ✅12
الصوت المولّد والتعليق`"]
      n64("`436
المحتوى والشرح`")
        n65["`DATA · 105 · ✅9
البيانات والرسوم البيانية`"]
        n66["`UI · 93 · ✅6
الواجهات والمنتجات والأجهزة`"]
        n67["`FOOT · 68 · ✅20
الصور والفيديو الخام`"]
        n68["`EXPL · 65 · ✅2
المخططات والشرح والكود`"]
        n69["`MAP · 62 · ✅4
الخرائط`"]
        n70["`BRAND · 43 · ✅8
الهوية والشعار`"]
      n71("`164
القصة والمنصات`")
        n72["`STORY · 94 · ✅14
القصة والإخراج`"]
        n73["`FMT · 70 · ✅17
المقاسات والمنصات`"]
      n74("`956
الأدوات والجودة`")
        n75["`ENG · 443 · ✅55
المحركات وخط الرندر`"]
        n76["`QA · 383 · ✅73
الجودة والتحقق`"]
        n77["`GEN · 93 · ✅14
التوليد بالذكاء الاصطناعي`"]
        n78["`MISC · 27 · ✅5
قدرات مساندة`"]
        n79["`DL · 10 · ✅5
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
