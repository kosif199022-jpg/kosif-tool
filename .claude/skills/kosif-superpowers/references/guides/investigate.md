# فحص البرامج والهندسة العكسية — Software investigation and reverse engineering

فحص قانوني لتطبيقات وملفات تنفيذية ومثبّتات بـ REA وGhidra، وفرز مثبّتات Windows، وفحص المستودعات وضغطها بأمان.

Lawful inspection of apps, binaries and installers with REA and Ghidra, Windows installer triage, and safe repository inspection and packing.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:investigate:start -->

**الأدوات / tools (12)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `installer-triage` | Standard-library triage of Windows installers and desktop apps before REA. It identifies the installer family (NSIS, Inno, WiX Burn, Squirrel, InstallShield, MSI), UPX packing, Electron, .NET and the signature slot, and finds payloads hidden in PE resources. It also lists and fingerprints Electron asar bundles, unpacks payloads with 7-Zip or innoextract on request and maps each artifact to the matching REA command. | `python3 scripts/installer_triage.py scan ./setup.exe` | tested-here |
| `local-project-audit` | Performs a read-only static inventory of a local folder without executing anything and returns a JSON report of file counts, extensions, routes (source review, Ghidra/REA binary candidates, archives, media), regex indicators, SHA-256 hashes and zip-safety stats. | `python3 scripts/local_project_audit.py ./my-project` | tested-here |
| `rea-bridge` | Opt-in bridge to the REA reverse-engineering CLI that stays within what the evidence shows. It checks Node and REA readiness, lists the 241 REA power records in the catalog (153 CLI commands, 76 MCP tools, 6 prompts and 6 KOSIF installer-triage additions) and plans an inspection without running it. Only with --authorized does it run one of 14 static local REA inspectors, saving the output to a new JSON file named by the caller. | `python3 scripts/rea_bridge.py doctor` | tested-here |
| `web-app-study` | Studies one public web page read-only: an isolated, logged-out headless Chromium (fresh profile, deleted afterwards), then REA captures the page, page-declared WebMCP tools, a screenshot and the public scripts, with SHA-256 receipts; optional bounded static JavaScript analysis. report turns a study folder into facts only: framework and versions, canvas/editor/realtime libraries, services inferred from storage key NAMES, WebMCP tools and page metrics, each with file-and-identifier evidence and never code. Written for the MagicPath study; works on Windows, macOS and Linux. | `python3 scripts/web_app_study.py doctor` | tested-here |
| `rea-family-router` | Read-only router that maps one target keyword from a fixed 29-word list (dotnet, apk, har, firmware, sqlite and others) to one of 16 REA capability families, giving the upstream tool name and availability status. It also reports whether rea and node are on PATH. | `python3 scripts/rea_family_router.py list` | tested-here |
| `rea-owned-repo-batch` | Batch static REA analysis of the user's own JavaScript, TypeScript and HTML GitHub repositories. It reads a private inventory (made by rea_creative_research_atlas.py own), shallow-clones the smallest eligible repos under a size cap with git (depth 1, blob:none) and runs REA's analyze-javascript-application on each through node. Clones and evidence stay in a local private folder, and only counts are printed. | `python3 scripts/rea_owned_repo_batch.py --private-output "$HOME/kosif-private" --rea-cli ./node_modules/rea-agents/scripts/rea.mjs --max-repos 16 --max-size-kb 8000` | untested |
| `repository-capability-packer` | Inspects a local repository folder or source ZIP for languages, capability signals, license files and a per-file SHA-256 manifest. It packs a deterministic, filtered source ZIP plus a JSON capability-transfer report, leaving out build caches, archives, executables, audio and video, keys, databases and files whose names suggest secrets. Nothing is run, imported or installed. | `python3 scripts/repository_capability_packer.py inspect ./repo --out ./repo-report.json` | tested-here |
| `atlas-bulk-source-audit` | Audits an authorized local Atlas source sample and records evidence without executing third-party skill code. | `python3 scripts/atlas_bulk_source_audit.py --help` | untested |
| `atlas-deep-fusion` | Selects source-linked Atlas methods for review against an authorized local Atlas index. | `python3 scripts/atlas_deep_fusion.py --help` | untested |
| `atlas-review-summary` | Summarizes source-audit evidence and provenance for candidate Atlas methods. | `python3 scripts/atlas_review_summary.py --help` | untested |
| `atlas-reviewed-methods-v3` | Works with reviewed Atlas method records and their provenance. | `python3 scripts/atlas_reviewed_methods_v3.py --help` | untested |
| `atlas-transfer` | Converts reviewed Atlas records into KOSIF capability catalog data; writes files only when explicitly approved. | `python3 scripts/atlas_transfer.py --help` | untested |

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
