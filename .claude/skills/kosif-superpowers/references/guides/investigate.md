# فحص البرامج والهندسة العكسية — Software investigation and reverse engineering

فحص قانوني لتطبيقات وملفات تنفيذية ومثبّتات بـ REA وGhidra، وفرز مثبّتات Windows، وفحص المستودعات وضغطها بأمان.

Lawful inspection of apps, binaries and installers with REA and Ghidra, Windows installer triage, and safe repository inspection and packing.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:investigate:start -->

**الأدوات / tools (1)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `local-project-audit` | Performs a read-only static inventory of a local folder and returns it as a JSON report, without executing anything. The report covers file counts, extensions, routing (source review, Ghidra/REA binary candidates, archives, media), regex indicators, SHA-256 hashes and zip safety stats. | `python3 scripts/local_project_audit.py ./my-project` | tested-here |

<!-- hub:area:investigate:end -->

## الفهرس / contents

1. [فحص البرامج والهندسة العكسية / REA optional integration](#فحص-البرامج-والهندسة-العكسية--rea-optional-integration)
2. [Repository Capability Transfer — فحص وضغط المستودعات للكود](#repository-capability-transfer--فحص-وضغط-المستودعات-للكود)
3. [REA v6.7 family router](#rea-v67-family-router)
4. [REA + Ghidra on an authorized binary (2026-10-20)](#rea--ghidra-on-an-authorized-binary-2026-10-20)

## فحص البرامج والهندسة العكسية / REA optional integration

إذا طلب المستخدم فحص تطبيق أو برنامج، فهم سلوك تطبيق دون مصدر، تحليل Electron/JavaScript أو APK أو .NET أو ملفات تنفيذية، أو بناء وظيفة مشابهة بناءً على أدلة؛ افتح [REA investigation guide](../rea-reverse-engineering.md) فقط لهذه المهمة. ابحث أولًا عن الكود الأصلي المتاح وعن الإذن القانوني؛ هذا مسار هندسة عكسية **اختياري** وليس بديلًا عن مهارات CODE وCHECK.

1. ابدأ بقراءة القدرات الفعلية: `python3 $SKILL_DIR/scripts/rea_bridge.py doctor`؛ لا تخلط بين وجود Node وبين تثبيت أو تشغيل REA.
2. للأنواع الثابتة المدعومة، اطلب خطة بلا تنفيذ: `python3 $SKILL_DIR/scripts/rea_bridge.py plan javascript /absolute/path/to/app`.
3. لا تثبّت REA أو الأدوات التجارية تلقائيًا. بعد تفويض المستخدم صراحةً، يمكن استخدام `run` في الجسر لنطاقات التحليل الثابت المسموحة فقط، مع ملف دليل محلي وعدم الكتابة فوق النتائج.
4. لا تعتبر `executed_not_verified` دليلًا على استنساخ الوظيفة. التحقق يتطلب أدلة ذات عناوين، ومقارنة سلوك مستقلة، واختبارات.
5. إذا كان المطلوب صورة أو فيديو أو بحثًا عاديًا أو كان المصدر متاحًا، لا تستدعِ REA لمجرد ورود كلمة «تقليد» أو «عكس». لا تنفّذ كودًا خارجيًا مسترجعًا من المستودعات.

**مثبّتات Windows وتطبيقات سطح المكتب (جديد):** REA يرى مثبّت NSIS/Inno/UPX ملفًا واحدًا بلا محتوى، فابدأ بـ `python $SKILL_DIR/scripts/installer_triage.py scan <المجلد>` ثم `unpack <ملف> --to <مجلد جديد> --authorized` (7-Zip، بلا تشغيل) ثم `fingerprint <app.asar>` و`route <المجلد>` لتعرف أمر REA لكل ملف. على Windows استخدم `python` بدل `python3`، والجسر يشغّل REA عبر node بلا cmd.exe (`REA_BIN`، `--timeout`، `--source-path`). الدروس والدليل: [proofs/windows-installers-rea](../../proofs/windows-installers-rea/README.md). **الفرز يكشف أيضًا** Inno Setup (ثم `innoextract -l`)، وحمولات MSI/CAB المخبأة داخل موارد PE (مثل DxO)، وRAR مشفّر العناوين (اطلب كلمة السر من المالك ولا تخمّنها)، وحزم Adobe دون اتصال (`products/driver.xml`). REA يرفض كل ملف أكبر من 64 MiB في `inspect-pe-resources`، فاستخرج قبل الفحص. لا تشغّل ولا تفتح Crack أو Patch أو KeyGen أبدًا ([الدفعة الثانية](../../proofs/windows-installers-rea/BATCH_2026-10-19.md)).

مرجع المصدر: [morluto/rea](https://github.com/morluto/rea) (MIT لكوده الأصلي؛ تبعياته لها شروطها). أوامر REA v6.7.0 الـ153 كلها مسجّلة قدراتٍ في عائلة [software-investigation](../powers/software-investigation.md) (REA-001…REA-153): 19 منها ✅ شُغّلت هنا فعلًا ([الدليل](../../proofs/rea-static-runs/README.md))، والباقي 📦 أو 📄 حسب المحرك الخارجي المطلوب؛ `python3 $SKILL_DIR/scripts/rea_bridge.py catalog <كلمة>` يسردها بلا تنفيذ. أدوات MCP وموجّهاته مسجّلة REA-154…REA-235، ومعها 6 إضافات KOSIF لفرز مثبّتات Windows (REA-236…REA-241، ✅ شُغّلت على Windows 11).

## Repository Capability Transfer — فحص وضغط المستودعات للكود

**نفّذ بدل جمع الروابط:** اقرأ [دليل نقل القدرات القابل للاختبار](../repository-capability-transfer.md) ثم استخدم `scripts/repository_capability_packer.py` على مستودع محلي أو ZIP مصدر مرخَّص للفحص. الأداة تحسب بصمات SHA256، تحدد اللغات والملفات والقدرات المرشحة من البنية، وتجهز ZIP حتميًا بعد رفض المسارات الخطرة واستبعاد ملفات البناء والأسرار المعروفة *بالأسماء*. لا تنفذ كود المصدر، ولا تثبت المكتبات، ولا ترفع أية قدرة إلى ✅ لمجرد وجود ZIP.

    python3 $SKILL_DIR/scripts/repository_capability_packer.py inspect ./repository --out ./repo-report.json
    python3 $SKILL_DIR/scripts/repository_capability_packer.py pack ./repository --out ./repo-safe.zip --report ./transfer-report.json
    python3 -m unittest discover -s $SKILL_DIR/evals -p test_repository_capability_packer.py -v

قبل نسخ أي كود: اقرأ رخص الملفات والتبعيات والأصول، صمّم Adapter ضيقًا واختبار قبول، ثم تحقّق من تشغيله فعليًا. الفلترة بالاسم لا تُعتبر ماسح أسرار شاملًا؛ افحص ZIP وتقرير البصمات قبل مشاركته.

## REA v6.7 family router

For authorized reverse engineering, keep the existing `scripts/rea_bridge.py` security gates and use `scripts/rea_family_router.py` and [upstream REA v6.7 capability families](../rea-upstream-capabilities.md) to discover supported routes. Read the **installed version-matched upstream REA skill** before exercising the executable. Do not auto-install, run native providers, attach to browsers/devices or claim successful agent investigations without authorization and real evidence.

## REA + Ghidra on an authorized binary (2026-10-20)

For licensed local application investigation, use REA with the Ghidra provider only after a live `rea doctor` and a controlled proof on an authorized binary. REA 6.7.0 plus Ghidra 12.1.4 successfully analyzed an OS test executable on the owner's Windows computer (341 recovered procedures; this does not mean source recovered). Never open Crack/KeyGen/Patch samples or copy proprietary implementation.
