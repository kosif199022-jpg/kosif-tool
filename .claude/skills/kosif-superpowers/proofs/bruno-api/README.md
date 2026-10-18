# bruno-api — اختبار API كامل بـ Bruno CLI (مُثبت هنا)

<div dir="rtl">

## بالعربية

**ماذا يثبت:** أن Claude يستطيع بناء مجموعة طلبات API كملفات نصية قابلة للمراجعة في git (صيغة Bru)، وتشغيلها آليًا كاختبارات قبول، وإخراج تقارير CI، دون أي حساب أو خدمة سحابية. شُغّل كل شيء في حاوية Claude السحابية يوم 2026-10-18 مع Bruno CLI 4.2.1 على API صغير مملوك (`server.py`، مكتبة بايثون القياسية فقط).

| الخطوة | النتيجة |
|---|---|
| تشغيل المجموعة كاملة (6 طلبات) | 6/6 طلبات · 3/3 اختبارات Chai · 8/8 تأكيدات |
| تسلسل الطلبات | `login` يحفظ الرمز بـ `bru.setVar` ثم تستخدمه الطلبات بـ Bearer |
| تقارير CI | JSON وJUnit وHTML |
| تشغيل مدفوع بالبيانات من CSV | 3 تكرارات أنشأت «فيديو إعلان» و«موشن شعار» و«ريل دعاء» |
| بوابة الفشل | كلمة مرور خاطئة مع `--bail` ← رمز خروج 1 (يوقف خط CI) |
| استيراد OpenAPI | 10 ملفات .bru مجمعة حسب الوسوم |
| توليد التوثيق | صفحة HTML مستقلة بكل البيئات |
| تحويل Postman | `@usebruno/converters` ترجم `pm.*` إلى `bru.*` بلا أخطاء |

**إعادة التشغيل:** `bash .claude/skills/kosif-superpowers/proofs/bruno-api/run.sh` (المخرجات في `/tmp/bruno-proof`، خارج المستودع). كلمة المرور سرّية في `environments/local.bru` وتمرَّر بـ `--env-var` ولا تُكتب في الملفات.

**حدود:** خوادم المحاكاة (Mock Servers) والذكاء المدمج و Bruno Apps تعمل من تطبيق Bruno المكتبي لا من CLI، فلم تُشغَّل هنا. بروتوكولات gRPC وWebSocket وGraphQL وSOAP موثقة ولم تُختبر في هذا الدليل.

</div>

## English

**What it proves:** Claude can author an API collection as reviewable plain-text files (Bru), run it as automated acceptance tests and emit CI reports with no account or cloud service. Run in the Claude cloud container on 2026-10-18 with Bruno CLI 4.2.1 against a small owned API (`server.py`, stdlib only).

The table above lists the results. In short: 6/6 requests with 3/3 Chai tests and 8/8 assertions; token chaining via `bru.setVar`; JSON, JUnit and HTML reports; a 3-row CSV data-driven run; a deliberate failure exiting 1 under `--bail`; OpenAPI import into 10 `.bru` files; standalone HTML docs; and a Postman collection converted with `pm.*` translated to `bru.*`. Summary in `results.json`.

**Limits:** mock servers, Bruno AI and Bruno Apps run inside the desktop app, not the CLI, so they were not run here. gRPC, WebSocket, GraphQL and SOAP requests are documented but not exercised in this proof.
