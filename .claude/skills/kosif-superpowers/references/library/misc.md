# قدرات مساندة غير مصنفة — Other supporting capabilities (`misc`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: other legacy مساعد إضافي متنوع

لا خط عمل مسجّل لهذه المجموعة؛ ركّبه من الأدوات أدناه.

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 5 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 7 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 11 | 📄 documented: a described method; needs building or wiring before it runs |
| `install` | 2 | 📦 install: needs a package, binary or model first |
| `key` | 2 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| **المجموع** | **27** | |

## الأدوات القابلة للتشغيل / runnable tools

لا أداة مسجلة تخدم عائلات هذه المجموعة مباشرة؛ التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `other` | 27 | [other.md](../powers/other.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `MISC-01` | البحث في كتالوج الأساليب | Style catalogue search · list · show | proven | python3 |
| `MISC-04` | اختيار المهارة تلقائيًا والموجّه الحتمي | Auto skill selection & deterministic capability router | proven |  |
| `MISC-05` | خادم MCP للاستوديو (22 أداة) | Studio MCP server for Claude Code (22 tools) | proven |  |
| `MISC-06` | جسر Claude بأربعة طرق وعقد الرد | Claude bridge (CLI · API · MCP · copy-paste) & gated apply | proven |  |
| `MISC-11` | بوابة نقطة التفتيش البشرية | Human-checkpoint action gate | proven |  |
| `MISC-07` | ملف المشروع المحمول وإعادة الربط | Portable project file (.kosif.json) with media re-link | ready |  |
| `MISC-13` | تسمية آمنة وتهريب النصوص | Safe naming & escaping | ready |  |
| `MISC-14` | سجل مصادر المعرفة | Knowledge provenance registry | ready | python3 |
| `MISC-17` | أفضل وقت للنشر من بيانات الحساب | Best time to post from own analytics | ready | python3 |
| `MISC-18` | مشاريع الأمثلة الجاهزة للمونتاج والموشن | Ready example projects (night_boat … water_cycle_3d) | ready | node, python3 |
| `MISC-19` | تطبيقات المالك كمراجع تصميم | Owner apps as design references (Audit Pro, Audit Studio, KOSIF Earth) | ready | python3, npm:react |
| `MISC-20` | تذييل المشهد وشريط التقدم | Scene footer label & progress bar | ready |  |
| `MISC-08` | عقود الدخول لعدة وكلاء | Multi-agent entry contracts | documented |  |
| `MISC-10` | المدخلات غير الموثوقة | Untrusted-input safety rule | documented | python3 |
| `MISC-12` | تدقيق تراخيص المصادر وحدود إعادة الاستخدام | Source licence audit & reuse allowlist | documented | pip:higgsfield, npm:gsap, npm:hyperframes |
| `MISC-15` | حدود التكامل مع KOSIF SEE | KOSIF SEE routing limits | documented | imagemagick |
| `MISC-21` | مهارات المالك المساندة (31 كتيب) | Owner supporting playbooks (31) | documented | pip:chromadb, npm:axe |
| `MISC-P01` | سُلَّم اختيار سطح التشغيل وحزمة التنفيذ | Capability-surface ladder + execution packet | documented | ffmpeg, python3 |
| `MISC-P02` | حارس تصادم المسارات بعشر حالات ظل | Route-collision guard with 10 shadow cases | documented | key:video-gen |
| `MISC-P03` | اقتراح درس مشروعي بموافقة صريحة | Consent-gated, project-scoped lesson proposal | documented | python3, key:unspecified |
| `MISC-P04` | كتالوج 60 معاينة مفهومية مولّدة بالكود | 60-card concept-preview catalog generator (A01–A60) | documented | python3 |
| `MISC-X01` | أدوات نص الويب: حكم الطرق الخمسمئة | Web text utilities: the 500-methods verdict | documented |  |
| `MISC-X02` | تنسيق الوكلاء لبناء فيلم متوازٍ | Agent orchestration rules for parallel film builds | documented |  |
| `MISC-03` | فهرس نصي كامل لمهارات الأطلس | Atlas full-text index (FTS5) | install | python3 |
| `MISC-16` | قراءة النصوص من المسوحات والإطارات | OCR of scans and video frames | install | ffmpeg, tesseract |
| `MISC-02` | مكتبة KOSIF Atlas | KOSIF Atlas library access | key | npm:remotion, key:unspecified |
| `MISC-09` | التحكم بسطح مكتب ويندوز (KOSIF Mouse) | Windows desktop control with Live View (KOSIF Mouse) | key | tesseract, key:unspecified |
