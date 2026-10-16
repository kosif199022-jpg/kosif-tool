# خريطة القدرات الذهنية — Capability mind map

> **ما هذه؟** خريطة ذهنية لكل قواك: 10 مجالات → 47 عائلة → 4,223 قدرة، مع أقوى شارة دليل في كل فرع. افتحها حين تبدأ مهمة كبيرة أو حين يسألك المستخدم «تقدر تعمل إيه؟»، ثم انزل من المجال إلى العائلة إلى القدرة.
> **What it gives you:** one picture of everything you can do, so you combine powers across domains instead of reaching for the first tool you remember. Regenerate after any catalog change: `python3 scripts/powers.py mindmap` (Mermaid text) or `--html references/capability-map.html` (standalone page). Drill into one domain with `--domain mind`.

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
  root((Kosif superpowers · 4223))
    n1["`166 · ✅31
العقل والتفكير`"]
      n2["`SELF · 43 · ✅26
اكتشاف القدرات`"]
      n3["`AGENT · 35 · 🟢1
تنسيق الوكلاء`"]
      n4["`THINK · 34 · ✅1
نواة التفكير`"]
      n5["`CHECK · 29 · ✅4
التحقق والتقييم`"]
      n6["`IDEA · 25 · 📄25
محرك الإبداع`"]
    n7["`69 · ✅25
الكتابة واللغة`"]
      n8["`WRITE · 28 · ✅11
الكتابة الطبيعية`"]
      n9["`PROMPT · 22 · ✅1
صناعة البرومبت`"]
      n10["`ARL · 19 · ✅13
اللغة العربية`"]
    n11["`58 · ✅12
الهندسة والكود`"]
      n12["`CODE · 22 · ✅1
هندسة البرمجيات`"]
      n13["`GRAPH · 20 · ✅10
الرسم المعرفي والخرائط الذهنية`"]
      n14["`SEC · 16 · ✅1
الأمان والسلامة`"]
    n15["`29 · ✅27
البيانات`"]
      n16["`ANLY · 29 · ✅27
تحليل البيانات`"]
    n17["`28 · ✅22
المستندات`"]
      n18["`DOC · 28 · ✅22
المستندات والمكتب`"]
    n19["`20 · ✅10
البحث والويب`"]
      n20["`WEB · 20 · ✅10
البحث على الويب`"]
    n21["`19 · ✅6
التطبيقات والواجهات`"]
      n22["`APP · 19 · ✅6
التطبيقات والواجهات`"]
    n23["`30 · ✅23
الصور والصوت`"]
      n24["`MEDIA · 30 · ✅23
الصور والصوت`"]
    n25["`15 · ✅4
المنتج والمال`"]
      n26["`PROD · 15 · ✅4
المنتج والاستراتيجية والمال`"]
    n27["`3789 · ✅545
الموشن والمونتاج`"]
      n28("`185
النص والخط`")
        n29["`ARAB · 93 · ✅19
الخط العربي المتحرك`"]
        n30["`TYPE · 92 · ✅2
التايبوغرافي اللاتيني والحركي`"]
      n31("`302
اللون والضوء والملمس`")
        n32["`TEX · 96 · ✅18
الملمس والخامات`"]
        n33["`COLOR · 87 · ✅38
الألوان واللوحات والتلوين`"]
        n34["`GLOW · 87 · ✅31
التوهج والإضاءة`"]
        n35["`RETRO · 32 · ✅10
البكسل والريترو والأساليب الخاصة`"]
      n36("`386
الشكل والحركة`")
        n37["`EASE · 102 · ✅27
التوقيت والإيقاع والتسهيل`"]
        n38["`SHAPE · 95 · ✅16
الأشكال والتحوّل`"]
        n39["`PART · 76 · ✅17
الجسيمات والسوائل والفيزياء`"]
        n40["`DRAW · 62 · ✅18
الرسم اليدوي والرسم الحي`"]
        n41["`CHAR · 51 · ✅12
الشخصيات والتحريك الهيكلي`"]
      n42("`948
الكاميرا والقطع`")
        n43["`TRANS · 472 · ✅27
الانتقالات والقطعات`"]
        n44["`CAM · 424 · ✅13
الكاميرا والتكوين`"]
        n45["`3D · 52 · ✅2
الأبعاد الثلاثية`"]
      n46("`420
الصوت والتزامن`")
        n47["`BEAT · 305 · ✅33
الموسيقى والإيقاع والمؤثرات`"]
        n48["`SYNC · 60 · ✅21
التزامن مع الكلام والترجمة`"]
        n49["`VOICE · 55 · ✅12
الصوت المولّد والتعليق`"]
      n50("`432
المحتوى والشرح`")
        n51["`DATA · 105 · ✅9
البيانات والرسوم البيانية`"]
        n52["`UI · 93 · ✅6
الواجهات والمنتجات والأجهزة`"]
        n53["`EXPL · 65 · ✅2
المخططات والشرح والكود`"]
        n54["`FOOT · 64 · ✅17
الصور والفيديو الخام`"]
        n55["`MAP · 62 · ✅4
الخرائط`"]
        n56["`BRAND · 43 · ✅8
الهوية والشعار`"]
      n57("`164
القصة والمنصات`")
        n58["`STORY · 94 · ✅14
القصة والإخراج`"]
        n59["`FMT · 70 · ✅17
المقاسات والمنصات`"]
      n60("`952
الأدوات والجودة`")
        n61["`ENG · 441 · ✅54
المحركات وخط الرندر`"]
        n62["`QA · 381 · ✅72
الجودة والتحقق`"]
        n63["`GEN · 93 · ✅14
التوليد بالذكاء الاصطناعي`"]
        n64["`MISC · 27 · ✅7
قدرات مساندة`"]
        n65["`DL · 10 · ✅5
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
| GRAPH → mind map | رسم معرفي لمستودع أو مجموعة مهارات ثم خريطة ذهنية / a code or skills graph turned into a mind map |
| PROD + ANLY | تسعير ونقطة تعادل محسوبة بالكود لا بالتخمين / pricing and break-even computed in code |
| APP + MEDIA | لوحة تفاعلية أو صفحة Artifact بصور معالَجة / an interactive dashboard or artifact with processed media |
| SELF → any | قبل قول «لا أستطيع»: افحص، ثبّت، جرّب / before saying "I can't": probe, install, verify |

## 5. اصنع خريطة ذهنية لأي شيء / mind-map anything
- **لمهارة أو مستودع:** ابنِ رسمًا معرفيًا بـgraphify محليًا أو عبر Graphify MCP، ثم حوّل المجتمعات إلى فروع (الطريقة في [graphify.md](graphify.md) و`proofs/general-graphify/graph_mindmap.py`).
- **لفكرة أو مشروع:** جذر = الهدف، فروع = المجالات العشرة أعلاه، أوراق = القدرات المختارة. اكتبها Mermaid `mindmap` واعرضها في Artifact أو HTML.
- **For any topic:** root = goal; first ring = the questions (who, what, constraints, risks); second ring = the powers that answer each. Render with Mermaid; keep labels short and in the user's language.
