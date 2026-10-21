# A3 — KOSIF Release Bridge وبرهان الإصدار / release proof (USIP v5.3)

> **متى تقرأه / when to read:** حين يُطلب دفع إلى مستودع أو دمج أو إصدار أو نشر موقع أو تحديث إنتاج. · [العودة إلى النواة / back to the core](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

> **الحالة هنا / backing:** إجراء موثَّق. Release Bridge وCloudflare خارجيان؛ هذا المستودع ينشر موقعه بـ GitHub Pages (`.github/workflows/pages.yml`) ويفحص نفسه بسير CI والحزمة — انظر الصف الخاص بعد -1.44.

نُقلت أقسام «المرحلة -1» هنا من `PROTOCOL.md` (v5.2) بنصها وبأرقامها؛ كل تعديل موسوم `(v5.3: …)`. معاني الخطط وكلمات الرد وسلالم الحالة المعتمدة في [مسرد النواة](../../PROTOCOL.md#المسرد--glossary)، وعند أي تعارض تغلب النواة. خريطة كل قسم قديم: [CHANGELOG](CHANGELOG.md).

### -1.44 KOSIF Release Bridge — برهان GitHub ↔ Cloudflare

المالك التنظيمي مستقل عن KOSIF Think وعن جهاز المستخدم. عندما يطلب المستخدم **إصدارًا أو دفعًا للمصدر** اتبع: النطاق والصلاحية → المستودع والفرع الحالي → مراجعة diff وHEAD → اختبار المصدر → commit/push عبر GitHub → انتظار Cloudflare المتصل → correlation بين deployed revision وcommit SHA نفسه → زيارة حية واختبار الوظيفة. الكتابة في GitHub وإطلاق الإنتاج حدثان مختلفان. لا يعتبر HTTP 200 ولا بدء build ولا الدمج وحده نجاح إصدار.

عقد إيصال الإصدار يحتوي: repository، source_branch، old_sha، intended_sha، tested_diff، authorized_action، cloudflare_project، deployment_id، deployed_sha، live_url، checked_at، acceptance_assertions، state. حالات (v5.3: وNOT_RELEASE_VERIFIED من R14 = أي حالة غير RELEASE_VERIFIED، وSOURCE_UPDATED_CI_FAILED في الصف الخاص أدناه): SOURCE_SCOPE_MISMATCH، SOURCE_CHANGED_CONCURRENTLY، BUILD_FAILED، DEPLOYMENT_COMMIT_MISMATCH، STALE_DEPLOYMENT، LIVE_CHECK_FAILED، POSTCONDITION_FAILED، RELEASE_VERIFIED. إن كان الملف دليلًا في المستودع بلا اعتماد تشغيل Cloudflare، اكتب SOURCE_UPDATED_DEPLOYMENT_NOT_APPLICABLE بدل ادعاء نشر. لا force push، لا تتجاوز حماية الفروع أو المصادقة أو الرصيد أو الفوترة، ولا تكتب أسرارًا في commit. عند تغيّر الـ SHA اعد المقارنة وتجنب تعديل عمل وكلاء آخرين.

### -1.44.أ — صف kosif-tool: GitHub Pages وCI (v5.3)

هذا المستودع لا ينشر على Cloudflare: الموقع يُنشر بسير `Deploy website` (`.github/workflows/pages.yml`)، والمهارة تُفحص بسير `CI` (`ci.yml`) و`Package KOSIF Superpowers for Claude` (`skill-package.yml`). الدفع إلى `main` نشر عام هنا (القانون 17). `RELEASE_VERIFIED` لـ kosif-tool = **كل سير أطلقه هذا الدفع** انتهى `conclusion=success` على **الـ headSha نفسه** الذي دفعته: `CI` و`Deploy website` دائمًا، و`Package KOSIF Superpowers for Claude` فقط حين مسّ الدفع `.claude/skills/kosif-superpowers/**` أو `skill-package.yml` (مرشّح `paths` فيه)؛ اقرأها بعد الدفع بـ `gh run list --branch main --commit <sha> --json name,headSha,conclusion`، ثم فحص حي للصفحة المتأثرة. نجاح `Deploy website` مع فشل أي سير آخر أطلقه الدفع = `SOURCE_UPDATED_CI_FAILED`، لا إصدار. ودفع فرع غير `main` = `SOURCE_UPDATED_DEPLOYMENT_NOT_APPLICABLE`: `CI` لا يعمل على دفع الفروع، فالمرجع نتيجة `CI` لطلب الدمج (PR) إن وُجد، وإلا فـ NOT_RUN. مسار Cloudflare أعلاه يُطبَّق فقط حين يوجد مشروع Cloudflare فعلي متصل.
