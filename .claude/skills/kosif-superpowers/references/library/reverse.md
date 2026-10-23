# التحليل العكسي وفحص البرامج — Reverse engineering (`reverse`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: reverse engineering ghidra rea binary executable forensic تحليل عكسي جفرا ريش

لا خط عمل مسجّل لهذه المجموعة؛ ركّبه من الأدوات أدناه.

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 30 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `documented` | 180 | 📄 documented: a described method; needs building or wiring before it runs |
| `install` | 48 | 📦 install: needs a package, binary or model first |
| **المجموع** | **258** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `atlas-5000` | خريطة تغطية أطلس الـ5000 مهارة | `python3 scripts/atlas_5000.py stats --json` | tested-here |
| `atlas-bulk-source-audit` | ????? ???? ?????? ???? | `python3 scripts/atlas_bulk_source_audit.py --help` | untested |
| `atlas-capability-miner` | ???? ????? ???? | `python3 scripts/atlas_capability_miner.py --help` | tested-here |
| `atlas-deep-fusion` | ????? ??? ???? | `python3 scripts/atlas_deep_fusion.py --help` | untested |
| `atlas-review-summary` | ???? ?????? ???? | `python3 scripts/atlas_review_summary.py --help` | untested |
| `atlas-reviewed-methods-v3` | ??? ???? ???????? | `python3 scripts/atlas_reviewed_methods_v3.py --help` | untested |
| `atlas-task-method-router` | ????? ???? ???? | `python3 scripts/atlas_task_method_router.py --help` | untested |
| `atlas-transfer` | ??? ??? ???? | `python3 scripts/atlas_transfer.py --help` | untested |
| `blender-api-audit` | تدقيق واجهة بايثون في Blender | `python3 scripts/blender_api_audit.py --help` | tested-here |
| `differential-exam` | مصحّح الامتحان الخفي التفاضلي | `python3 scripts/differential_exam.py seal ./exam --out ./exam-seal.json` | tested-here |
| `installer-triage` | فرز المثبّتات | `python3 scripts/installer_triage.py scan ./setup.exe` | tested-here |
| `local-project-audit` | فحص المشروع المحلي دون تشغيل | `python3 scripts/local_project_audit.py ./my-project` | tested-here |
| `mosamem-rea-fusion` | تكامل مصمم وREA: فحص صور وتوليف مهارات آمن | `python3 scripts/mosamem_rea_fusion.py doctor` | tested-here |
| `rea-bridge` | جسر أوامر REA | `python3 scripts/rea_bridge.py doctor` | tested-here |
| `rea-creative-research-atlas` | باني فهرس البحث الإبداعي | `python3 scripts/rea_creative_research_atlas.py report` | tested-elsewhere |
| `rea-family-router` | موجّه عائلات REA | `python3 scripts/rea_family_router.py list` | tested-here |
| `rea-owned-repo-batch` | تحليل REA لمستودعات المالك دفعةً واحدة | `python3 scripts/rea_owned_repo_batch.py --private-output "$HOME/kosif-private" --rea-cli ./node_modules/rea-agents/scripts/rea.mjs --max-repos 16 --max-size-kb 8000` | untested |
| `rea-superpowers-map` | خريطة سوبر باور بمنهج REA | `python3 scripts/rea_superpowers_map.py build` | tested-here |
| `repository-capability-packer` | فحص المستودعات وحزمها | `python3 scripts/repository_capability_packer.py inspect ./repo --out ./repo-report.json` | tested-here |
| `web-app-study` | دراسة تطبيق ويب عام بـ REA (حقائق فقط) | `python3 scripts/web_app_study.py doctor` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `software-investigation` | 258 | [software-investigation.md](../powers/software-investigation.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `REA-003` | تحليل تطبيق جافاسكربت | Statically reconstruct a local JavaScript/Electron application | proven | chromium, npm:rea, engine:wakaru |
| `REA-004` | تحليل حزمة ويب | Capture and statically analyze a page bundle, defaulting to the selected target origin | proven | chromium, npm:rea, engine:wakaru |
| `REA-007` | قدرات المزودين | List provider capabilities and side effects | proven | npm:rea, os:macos |
| `REA-013` | التقاط لقطة شاشة ويب | Capture one visible page viewport within the supplied origin scope | proven | chromium, npm:rea, engine:wakaru |
| `REA-034` | فحص جاهزية REA | Check whether REA is ready | proven | npm:rea, engine:ghidra, engine:android |
| `REA-040` | استخراج قطعة | Extract all regular artifact contents safely | proven | npm:rea |
| `REA-047` | فحص عميل ADB | Inspect the caller-selected adb client without contacting devices | proven | chromium, npm:rea, engine:android |
| `REA-052` | فحص عرض التحليل | Project a selected view of completed binary-layout, JavaScript application, native function, artifact-inventory, WASM, Mach-O, Interface Builder, EVM, managed, Android package, Dart AOT, web network capture or pcap Evidence JSON | proven | npm:rea, engine:wireshark, os:macos |
| `REA-056` | فحص عميل apktool | Inspect the caller-selected apktool launcher without decoding anything | proven | chromium, npm:rea, engine:android |
| `REA-057` | فحص قطعة | Inspect one artifact and return all available observations and next probes | proven | npm:rea |
| `REA-061` | فحص fuses Electron | Inspect packaged Electron fuse bytes without launching the application | proven | npm:rea |
| `REA-064` | فحص واجهة EVM | Infer interface candidates from explicit local EVM bytecode | proven | npm:rea |
| `REA-066` | فحص ثنائي Go | Inspect embedded Go compiler, modules and build settings without target execution | proven | npm:rea |
| `REA-079` | فحص حقول الحزم | Search installed TShark protocol and field definitions | proven | npm:rea, engine:wireshark |
| `REA-081` | فحص عميل pcap | Inspect the caller-selected tshark and capinfos binaries without reading a capture | proven | npm:rea, engine:wireshark |
| `REA-085` | فحص ثنائي Rust | Inspect an embedded cargo-auditable Rust dependency list without target execution | proven | npm:rea |
| `REA-086` | فحص مفككات إشارة | Search installed sigrok decoders or selected decoder help | proven | npm:rea, engine:sigrok |
| `REA-090` | فحص مستمعات الأحداث الأحداث ويب | Inspect native listener source locations on the first main-document CSS match | proven | chromium, npm:rea, engine:wakaru |
| `REA-092` | فحص صفحة ويب | Passively inspect one page through CDP, defaulting to its current origin | proven | chromium, npm:rea, engine:wakaru |
| `REA-093` | فحص objdump بـ | Inspect a local artifact with GNU objdump and retain its raw output as Evidence | proven | npm:rea, engine:rizin |
| `REA-104` | سرد الأهداف المتصفح | List page targets from a selected loopback CDP browser, optionally filtered by origin | proven | chromium, npm:rea, engine:wakaru |
| `REA-111` | سرد المعماريات objdump | List BFD targets advertised by the installed GNU objdump | proven | npm:rea, engine:rizin |
| `REA-122` | المزودون المهيّأون | List configured analysis providers | proven | npm:rea |
| `REA-142` | تتبّع ميزة تطبيق | Trace a typed seed through authenticated application Evidence JSON | proven | chromium, npm:rea, engine:wakaru |
| `REA-236` | فرز المثبّت قبل REA | Installer triage scan | proven | python3, npm:rea |
| `REA-237` | فك حمولة المثبّت بلا تشغيل | Unpack an installer payload without running it | proven | python3, npm:rea, 7zip |
| `REA-238` | قراءة أرشيف asar | List an Electron app.asar | proven | python3, npm:rea |
| `REA-239` | بصمة قدرات Electron | Electron capability fingerprint | proven | python3, npm:rea |
| `REA-240` | توجيه المستخرجات إلى أوامر REA | Route unpacked artifacts to REA | proven | python3, npm:rea |
| `REA-241` | تشغيل REA على Windows بلا shell | Run REA on Windows without cmd.exe | proven | python3, npm:rea |
| `REA-001` | تحويل إزاحة ملف إلى | Resolve an analysis address to its original file byte offset | documented | npm:rea, engine:ghidra |
| `REA-002` | تحليل | Get an overview of an app | documented | npm:rea, engine:ghidra |
| `REA-005` | توصيف دالة أصلية | Edit function annotations and return refreshed analysis | documented | npm:rea, engine:ghidra |
| `REA-008` | التقاط screen ADB | Capture one screen frame as a digested PNG | documented | chromium, npm:rea, engine:android |
| `REA-011` | التقاط سيناريو الواجهة أصلية | Run declarative AX actions or waits in one exact native application window | documented | npm:rea, engine:ghidra, os:macos |
| `REA-014` | جمع تقرير أخطاء ADB | Collect and digest one device-generated bugreport archive | documented | chromium, npm:rea, engine:android |
| `REA-021` | مقارنة الواجهات WASM | Compare core WASM interfaces from two exact inspection Evidence records | documented | npm:rea, engine:wabt |
| `REA-024` | أمر Cutter command | Execute one Rizin command in a selected live Cutter instance | documented | python3, npm:rea, engine:rizin |
| `REA-025` | تنقيح GDB بـ | Run one unrestricted GDB console command in an ephemeral MI session; provide an inferior TTY so a live target can be safely detached | documented | npm:rea, engine:rizin |
| `REA-026` | تنقيح Rizin بـ | Run one unrestricted Rizin debugger command in an ephemeral session | documented | python3, npm:rea, engine:rizin |
| `REA-027` | فك ترميز الموارد أندرويد | Decode one APK's manifest, metadata, and string resources with apktool | documented | chromium, npm:rea, engine:android |
| `REA-028` | فك ترميز Interface Builder واجهة | Decode compiled storyboard and nib archives from an app bundle | documented | npm:rea, engine:ghidra, os:macos |
| `REA-029` | فك ترميز تسجيل إشارة | Decode an existing signal recording with caller-supplied sigrok | documented | npm:rea, engine:sigrok |
| `REA-030` | تفكيك | Read one part of an app as code | documented | npm:rea, engine:ghidra |
| `REA-031` | تفكيك عنصر JEB | Decompile one JEB type or method to engine pseudo-code | documented | npm:rea, engine:jeb |
| `REA-032` | فك تشويه Swift | Demangle Swift symbols without Hopper | documented | npm:rea, engine:ghidra, os:macos |
| `REA-038` | تنفيذ command Rizin | Execute one Rizin command against a local artifact | documented | python3, npm:rea, engine:rizin |
| `REA-041` | استخراج فيرموير | Extract selected firmware bytes and return verified files and provenance | documented | npm:rea, engine:binwalk |
| `REA-042` | تحليل دالة | Analyze one complete function with evidence | documented | npm:rea, engine:ghidra |
| `REA-046` | فحص | Inspect an app overview with evidence | documented | npm:rea, engine:ghidra |
| `REA-048` | فحص جهاز ADB | Inspect one device's build identity through a fixed getprop whitelist | documented | chromium, npm:rea, engine:android |
| `REA-049` | فحص الشاشة ADB | Report the display's declared size and density | documented | chromium, npm:rea, engine:android |
| `REA-050` | فحص حزمة ADB | Inspect one installed package's version, installer, and flags through dumpsys | documented | chromium, npm:rea, engine:android |
| `REA-051` | فحص النافذة ADB | Report the window manager's current focus declarations | documented | chromium, npm:rea, engine:android |
| `REA-053` | فحص صنف أندرويد | Inspect one exact APK class's member inventory | documented | chromium, npm:rea, engine:android |
| `REA-054` | فحص دالة أندرويد | Decompile one APK method with explicit overload selection | documented | chromium, npm:rea, engine:android |
| `REA-058` | فحص كتالوج الأصول | Inspect compiled Apple asset catalog metadata | documented | npm:rea, engine:ghidra, os:macos |
| `REA-059` | فحص تخطيط ثنائي | Inspect binary file/linked layout without executing the selected object | documented | npm:rea |
| `REA-065` | فحص المناطق فيرموير | Inspect firmware signature candidates without extracting them | documented | npm:rea, engine:binwalk |
| `REA-067` | فحص عميل JEB | Inspect the running JEB MCP client without opening a target | documented | npm:rea, engine:jeb |
| `REA-068` | فحص أرشيف مفاتيح | Inspect a Foundation keyed archive as an object-reference graph | documented | npm:rea, engine:ghidra, os:macos |
| `REA-069` | فحص Mach-O | Run inspect_macho without launching Hopper | documented | npm:rea, engine:ghidra, os:macos |
| `REA-073` | فحص واجهة برمجية أصلية | Reconstruct one native function API boundary with evidence | documented | npm:rea, engine:ghidra |
| `REA-074` | فحص نوع بيانات أصلية | Inspect one recovered database type or typed data object | documented | npm:rea, engine:ghidra |
| `REA-075` | فحص بيانات وصفية الإرسال أصلية | Inspect typed Objective-C and Swift dispatch metadata | documented | npm:rea, engine:ghidra, os:macos |
| `REA-076` | فحص تعليمة أصلية | Inspect one native instruction with decoded operand facts | documented | npm:rea, engine:ghidra |
| `REA-077` | فحص صورة تحميل أصلية | Verify loaded native bytes, source mappings, relocations and entry | documented | npm:rea, engine:ghidra |
| `REA-078` | فحص التقاط الحزم | Inspect an existing packet capture with caller-supplied TShark | documented | npm:rea, engine:wireshark |
| `REA-080` | فحص التقاط pcap | Inspect one pcap/pcapng capture: endpoints, DNS, TLS SNI, and protocol distribution | documented | npm:rea, engine:wireshark |
| `REA-083` | فحص plist | Parse app plist metadata without launching Hopper | documented | npm:rea, engine:ghidra, os:macos |
| `REA-087` | فحص التوقيع | Run inspect_signature without launching Hopper | documented | npm:rea, engine:ghidra, os:macos |
| `REA-089` | فحص قطعة WASM | Inspect an explicit local WASM artifact with WABT | documented | npm:rea, engine:wabt |
| `REA-094` | تثبيت حزمة ADB | Install one local APK; --replace requests reinstall mode to keep existing app data | documented | chromium, npm:rea, engine:android |
| `REA-095` | قراءة التعليمات | Read every raw instruction without decompiling | documented | npm:rea, engine:ghidra |
| `REA-096` | تجهيز Frida بـ | Run one Frida script against a selected process and detach | documented | npm:rea, engine:frida |
| `REA-097` | سرد الأجهزة ADB | List attached devices with serial, state, transport, and inferred kind | documented | chromium, npm:rea, engine:android |
| `REA-098` | سرد مجلد ADB | List one device directory with kinds, permissions, and sizes | documented | chromium, npm:rea, engine:android |
| `REA-099` | سرد الميزات ADB | List the device's declared hardware and software features | documented | chromium, npm:rea, engine:android |
| `REA-100` | سرد الحزم ADB | List installed packages on one device with base APK device paths | documented | chromium, npm:rea, engine:android |
| `REA-101` | سرد العمليات ADB | List running processes exactly as ps -A reports them | documented | chromium, npm:rea, engine:android |
| `REA-102` | سرد الخدمات ADB | List the device's binder services and interfaces | documented | chromium, npm:rea, engine:android |
| `REA-103` | سرد المعماريات | Run list_architectures without launching Hopper | documented | npm:rea, engine:ghidra, os:macos |
| `REA-105` | سرد الجلسات cutter | List live Cutter instances connected through the REA Python plugin bridge | documented | python3, npm:rea, engine:rizin |
| `REA-107` | سرد الأجهزة Frida | List local Frida devices and an optional remote endpoint | documented | npm:rea, engine:frida |
| `REA-108` | سرد العمليات Frida | List processes visible through a Frida device | documented | npm:rea, engine:frida |
| `REA-110` | سرد الوحدات JEB | List JEB project units by path and type with optional filter | documented | npm:rea, engine:jeb |
| `REA-113` | مراقبة calls أصلية | Launch a Mach-O under LLDB and record entries into selected functions or Objective-C methods | documented | npm:rea, engine:ghidra, os:macos |
| `REA-114` | مراقبة الواجهة أصلية | Observe one already-running native application window by PID and window ID | documented | npm:rea, engine:ghidra, os:macos |
| `REA-117` | فتح مشروع JEB | Open or create a JEB project from an artifact or .jdb2 database | documented | npm:rea, engine:jeb |
| `REA-119` | إسقاط مخطط تطبيق Apple | Project authenticated IPA or macOS app inventory Evidence into an Apple application graph | documented | npm:rea, engine:ghidra, os:macos |
| `REA-123` | سحب ملف ADB | Pull one device file to a local copy with a SHA-256 digest | documented | chromium, npm:rea, engine:android |
| `REA-124` | سحب حزمة ADB | Pull one installed package's complete APK set with SHA-256 digests | documented | chromium, npm:rea, engine:android |
| `REA-125` | دفع ملف ADB | Push one local file to the device; refuses existing targets without --overwrite | documented | chromium, npm:rea, engine:android |
| `REA-126` | قراءة سجل logcat ADB | Read a bounded dump of the device log for one buffer | documented | chromium, npm:rea, engine:android |
| `REA-127` | قراءة إعداد ADB | Read one settings value from system, secure, or global | documented | chromium, npm:rea, engine:android |
| `REA-128` | قراءة بايتات | Read exact provider memory bytes at one analysis address | documented | npm:rea, engine:ghidra |
| `REA-131` | تحديد الحزم ADB | Find installed packages by case-insensitive name substring | documented | chromium, npm:rea, engine:android |
| `REA-132` | تحديد الأهداف استدعاء أصلية | Resolve one static native call site | documented | npm:rea, engine:ghidra |
| `REA-133` | بحث في | Search every analyzed string or procedure name | documented | npm:rea, engine:ghidra |
| `REA-134` | بحث في الأصناف أندرويد | Search APK class names; empty query inventories all classes | documented | chromium, npm:rea, engine:android |
| `REA-135` | بحث في بايتات | Find masked byte patterns in initialized provider memory | documented | npm:rea, engine:ghidra |
| `REA-137` | تشغيل نشاط ADB | Start an intent with am start (action, URI, component, extras) | documented | chromium, npm:rea, engine:android |
| `REA-138` | تشغيل تطبيق ADB | Start one installed app by resolving and launching its launcher activity | documented | chromium, npm:rea, engine:android |
| `REA-139` | إيقاف تطبيق ADB | Force-stop every process of one package | documented | chromium, npm:rea, engine:android |
| `REA-140` | تتبّع | Trace a literal feature through analyzed references | documented | npm:rea, engine:ghidra |
| `REA-141` | تتبّع المراجع أندرويد | Trace incoming APK using nodes for a class or selected method | documented | chromium, npm:rea, engine:android |
| `REA-143` | تتبّع تحليل dylib | Trace dyld load-path resolution for a Mach-O or every executable in an app bundle | documented | npm:rea, engine:ghidra, os:macos |
| `REA-145` | تتبّع إجراء الواجهة أصلية | Trace a compiled UI action selector to its native handler and direct callees | documented | npm:rea, engine:ghidra, os:macos |
| `REA-146` | تتبّع القيم أصلية | Trace bounded native def-use and call dependencies | documented | npm:rea, engine:ghidra |
| `REA-150` | إزالة حزمة ADB | Uninstall one package and its data from the device | documented | chromium, npm:rea, engine:android |
| `REA-153` | المراجع المتقاطعة | List bounded references to an analyzed address | documented | npm:rea, engine:ghidra |
| `REA-154` | REA MCP: عنوان | REA MCP tool `address_name` | documented | chromium, npm:rea, engine:ghidra |
| `REA-155` | REA MCP: تعليق | REA MCP tool `comment` | documented | npm:rea, engine:ghidra |
| `REA-156` | REA MCP: عنوان | REA MCP tool `current_address` | documented | npm:rea, engine:ghidra |
| `REA-157` | REA MCP: دالة | REA MCP tool `current_procedure` | documented | npm:rea, engine:ghidra |
| `REA-158` | REA MCP: المستند الحالي | REA MCP tool `current_document` | documented | npm:rea, engine:ghidra |
| `REA-159` | REA MCP: عنوان | REA MCP tool `goto_address` | documented | npm:rea, engine:ghidra |
| `REA-160` | REA MCP: تعليق | REA MCP tool `inline_comment` | documented | npm:rea, engine:ghidra |
| `REA-161` | REA MCP: العلامات | REA MCP tool `list_bookmarks` | documented | npm:rea, engine:ghidra |
| `REA-162` | REA MCP: سرد المستندات المفتوحة | REA MCP tool `list_documents` | documented | chromium, npm:rea, engine:ghidra |
| `REA-163` | REA MCP: سرد الأسماء والرموز | REA MCP tool `list_names` | documented | npm:rea, engine:ghidra |
| `REA-164` | REA MCP: سرد الإجراءات المستعادة | REA MCP tool `list_procedures` | documented | npm:rea, engine:ghidra |
| `REA-165` | REA MCP: المقاطع | REA MCP tool `list_segments` | documented | npm:rea, engine:ghidra |
| `REA-166` | REA MCP: النصوص | REA MCP tool `list_strings` | documented | npm:rea, engine:ghidra |
| `REA-167` | REA MCP: عنوان | REA MCP tool `next_address` | documented | npm:rea, engine:ghidra |
| `REA-168` | REA MCP: عنوان | REA MCP tool `prev_address` | documented | npm:rea, engine:ghidra |
| `REA-169` | REA MCP: دالة | REA MCP tool `procedure_address` | documented | npm:rea, engine:ghidra |
| `REA-170` | REA MCP: دالة | REA MCP tool `procedure_assembly` | documented | npm:rea, engine:ghidra |
| `REA-171` | REA MCP: دالة | REA MCP tool `procedure_callees` | documented | npm:rea, engine:ghidra |
| `REA-172` | REA MCP: دالة | REA MCP tool `procedure_callers` | documented | npm:rea, engine:ghidra |
| `REA-173` | REA MCP: دالة | REA MCP tool `procedure_info` | documented | npm:rea, engine:ghidra |
| `REA-174` | REA MCP: دالة | REA MCP tool `read_function_instructions` | documented | npm:rea, engine:ghidra |
| `REA-175` | REA MCP: دالة | REA MCP tool `procedure_references` | documented | npm:rea, engine:ghidra |
| `REA-176` | REA MCP: دالة | REA MCP tool `procedure_pseudo_code` | documented | npm:rea, engine:ghidra |
| `REA-177` | REA MCP: دالة | REA MCP tool `resolve_containing_procedure` | documented | npm:rea, engine:ghidra |
| `REA-178` | REA MCP: البحث في الإجراءات | REA MCP tool `search_procedures` | documented | npm:rea, engine:ghidra |
| `REA-179` | REA MCP: النصوص | REA MCP tool `search_strings` | documented | npm:rea, engine:ghidra |
| `REA-180` | REA MCP: عنوان | REA MCP tool `set_address_name` | documented | npm:rea, engine:ghidra |
| `REA-181` | REA MCP: تسمية العناوين | REA MCP tool `set_addresses_names` | documented | npm:rea, engine:ghidra |
| `REA-182` | REA MCP: علامة | REA MCP tool `set_bookmark` | documented | npm:rea, engine:ghidra |
| `REA-183` | REA MCP: تعليق | REA MCP tool `set_comment` | documented | npm:rea, engine:ghidra |
| `REA-184` | REA MCP: تعليق | REA MCP tool `set_inline_comment` | documented | npm:rea, engine:ghidra |
| `REA-185` | REA MCP: علامة | REA MCP tool `unset_bookmark` | documented | npm:rea, engine:ghidra |
| `REA-186` | REA MCP: أصناف Objective-C | REA MCP tool `get_objc_classes` | documented | npm:rea, engine:ghidra |
| `REA-187` | REA MCP: أصناف Objective-C | REA MCP tool `get_objc_protocols` | documented | npm:rea, engine:ghidra |
| `REA-188` | REA MCP: فك تجميع دفعة إجراءات | REA MCP tool `batch_decompile` | documented | npm:rea, engine:ghidra |
| `REA-189` | REA MCP: الاستدعاء | REA MCP tool `get_call_graph` | documented | npm:rea, engine:ghidra |
| `REA-190` | REA MCP: أنواع Swift | REA MCP tool `analyze_swift_types` | documented | npm:rea, engine:ghidra |
| `REA-191` | REA MCP: المراجع المتقاطعة | REA MCP tool `find_xrefs_to_name` | documented | npm:rea, engine:ghidra |
| `REA-192` | REA MCP: الثنائي | REA MCP tool `binary_overview` | documented | npm:rea |
| `REA-193` | REA MCP: دالة | REA MCP tool `analyze_function` | documented | npm:rea, engine:ghidra |
| `REA-194` | REA MCP: ميزة | REA MCP tool `trace_feature` | documented | npm:rea, engine:ghidra |
| `REA-195` | REA MCP: الاستدعاء | REA MCP tool `trace_call_path` | documented | npm:rea, engine:ghidra |
| `REA-196` | REA MCP: بدء جلسة Frida | REA MCP tool `start_frida_session` | documented | npm:rea, engine:frida |
| `REA-197` | REA MCP: تحميل سكربت Frida | REA MCP tool `load_frida_script` | documented | npm:rea, engine:frida |
| `REA-198` | REA MCP: استئناف جلسة Frida | REA MCP tool `resume_frida_session` | documented | npm:rea, engine:frida |
| `REA-199` | REA MCP: إزالة سكربت Frida | REA MCP tool `unload_frida_script` | documented | npm:rea, engine:frida |
| `REA-200` | REA MCP: حالة جلسة Frida | REA MCP tool `frida_session_status` | documented | npm:rea, engine:frida |
| `REA-201` | REA MCP: إغلاق جلسة Frida | REA MCP tool `close_frida_session` | documented | npm:rea, engine:frida |
| `REA-202` | REA MCP: بدء جلسة GDB | REA MCP tool `start_gdb_session` | documented | npm:rea, engine:rizin |
| `REA-203` | REA MCP: وحدة أوامر GDB | REA MCP tool `gdb_console` | documented | npm:rea, engine:rizin |
| `REA-204` | REA MCP: حالة جلسة GDB | REA MCP tool `gdb_session_status` | documented | npm:rea, engine:rizin |
| `REA-205` | REA MCP: إغلاق جلسة GDB | REA MCP tool `close_gdb_session` | documented | npm:rea, engine:rizin |
| `REA-206` | REA MCP: بدء جلسة تصحيح Rizin | REA MCP tool `start_rizin_debug_session` | documented | npm:rea, engine:rizin |
| `REA-207` | REA MCP: أمر تصحيح Rizin | REA MCP tool `rizin_debug_command` | documented | npm:rea, engine:rizin |
| `REA-208` | REA MCP: حالة جلسة تصحيح Rizin | REA MCP tool `rizin_debug_session_status` | documented | npm:rea, engine:rizin |
| `REA-209` | REA MCP: إغلاق جلسة تصحيح Rizin | REA MCP tool `close_rizin_debug_session` | documented | npm:rea, engine:rizin |
| `REA-210` | REA MCP: الثنائي | REA MCP tool `open_binary` | documented | npm:rea, os:macos |
| `REA-211` | REA MCP: الثنائي | REA MCP tool `close_binary` | documented | npm:rea |
| `REA-212` | REA MCP: الثنائي | REA MCP tool `binary_session` | documented | npm:rea |
| `REA-213` | REA MCP: الأدلة | REA MCP tool `export_evidence_bundle` | documented | npm:rea |
| `REA-214` | REA MCP: الأدلة | REA MCP tool `import_evidence_bundle` | documented | npm:rea |
| `REA-215` | REA MCP: الأدلة | REA MCP tool `get_evidence_bundle` | documented | npm:rea |
| `REA-216` | REA MCP: عملية | REA MCP tool `capture_process_scenario` | documented | npm:rea |
| `REA-217` | REA MCP: القطع | REA MCP tool `compare_artifacts` | documented | npm:rea |
| `REA-218` | REA MCP: الدوال | REA MCP tool `compare_functions` | documented | npm:rea |
| `REA-219` | REA MCP: الحزم | REA MCP tool `compare_bundles` | documented | npm:rea |
| `REA-220` | REA MCP: كشف السلوك المتغير | REA MCP tool `find_changed_behavior` | documented | npm:rea |
| `REA-221` | REA MCP: الاستدعاء | REA MCP tool `build_call_path` | documented | npm:rea |
| `REA-222` | REA MCP: ربط التحليل الثابت بالتشغيل | REA MCP tool `correlate_static_and_runtime` | documented | npm:rea |
| `REA-223` | REA MCP: التحقق من إعادة البناء | REA MCP tool `verify_reconstruction` | documented | npm:rea |
| `REA-224` | REA MCP: سرد المجهولات | REA MCP tool `list_unknowns` | documented | npm:rea |
| `REA-225` | REA MCP: المجهول | REA MCP tool `record_unknown` | documented | npm:rea |
| `REA-226` | REA MCP: المجهول | REA MCP tool `update_unknown` | documented | npm:rea |
| `REA-227` | REA MCP: المجهول | REA MCP tool `verify_unknown_resolution` | documented | npm:rea |
| `REA-228` | REA MCP: سياق التنقل | REA MCP tool `get_navigation_context` | documented | npm:rea |
| `REA-229` | REA MCP: عنوان | REA MCP tool `inspect_address_context` | documented | npm:rea |
| `REA-230` | REA موجّه: investigate_feature | REA MCP prompt `investigate_feature` | documented | npm:rea |
| `REA-231` | REA موجّه: compare_application_versions | REA MCP prompt `compare_application_versions` | documented | npm:rea |
| `REA-232` | REA موجّه: verify_reconstruction | REA MCP prompt `verify_reconstruction` | documented | npm:rea |
| `REA-233` | REA موجّه: trace_crash | REA MCP prompt `trace_crash` | documented | npm:rea |
| `REA-234` | REA موجّه: audit_residual_unknowns | REA MCP prompt `audit_residual_unknowns` | documented | npm:rea |
| `REA-235` | REA موجّه: prepare_bounded_process_capture | REA MCP prompt `prepare_bounded_process_capture` | documented | npm:rea |
| `REA-242` | REA: تحسين أداء التحليل مع الحفاظ على الأدلة | REA skill: optimize analysis cost while preserving correctness and Evidence | documented | npm:rea, engine:ghidra |
| `REA-243` | REA: تصميم أداة تحقيق وعقد CLI/MCP | REA skill: design investigation tools, CLI/MCP contracts and Evidence semantics | documented | npm:rea |
| `REA-244` | REA: تدقيق CI والاختبارات (انحراف التجهيزات والنجاح الكاذب) | REA skill: audit CI and test suites for fixture drift, false passes and measured cost | documented | npm:rea |
| `REA-245` | REA: كتابة سجل التغييرات من تاريخ Git مثبت مع شكر موثق | REA skill: release changelog from pinned Git history with verified contributor thanks | documented | npm:rea |
| `REA-246` | REA: إنتروبيا البايتات لكشف المناطق المضغوطة أو المشفرة | REA MCP tool `inspect_byte_entropy`: Shannon byte entropy profile | documented | npm:rea, engine:binwalk |
| `REA-247` | REA: فحص تطبيق سطح مكتب ومعرفة محركه | REA MCP tool `inspect_desktop_application`: engine candidates for a desktop app folder | documented | npm:rea |
| `REA-248` | REA: ملاحظات ELF ومعرّف البناء | REA MCP tool `inspect_elf_notes`: GNU build-id and ABI-tag notes | documented | npm:rea |
| `REA-249` | REA: فحص ملفات BEAM لإرلانغ وإليكسير | REA MCP tool `inspect_erlang_beam`: BEAM atoms, exports and Code header | documented | npm:rea |
| `REA-250` | REA: كائنات كود GPU لـ CUDA وHIP | REA MCP tool `inspect_gpu_code_objects`: CUDA/HIP fatbins, CUBIN and PTX | documented | npm:rea, gpu |
| `REA-251` | REA: بيانات Unity IL2CPP الوصفية | REA MCP tool `inspect_il2cpp_metadata`: Unity IL2CPP metadata with optional binary link | documented | npm:rea, os:macos |
| `REA-252` | REA: فحص ملفات النماذج GGUF وsafetensors بلا تحميل | REA MCP tool `inspect_model_artifact`: GGUF and safetensors declarations without loading | documented | npm:rea, pip:llama-cpp |
| `REA-253` | REA: جدول تصدير مكتبة PE أو ELF | REA MCP tool `inspect_native_exports`: PE/ELF export table | documented | npm:rea |
| `REA-254` | REA: هويات شهادات Authenticode في PE | REA MCP tool `inspect_pe_certificates`: Authenticode certificate identities | documented | npm:rea |
| `REA-255` | REA: ترويسة pyc وكائنات الكود بلا بايثون | REA MCP tool `inspect_python_pyc`: CPython .pyc header and code objects | documented | python3, npm:rea |
| `REA-256` | REA: مطابقة الدوال بين نسختين من ثنائي | REA MCP tool `match_native_functions`: match functions across two binary versions | documented | npm:rea |
| `REA-257` | REA: فتح حزمة تطبيق لقراءة الموارد فقط | REA MCP tool `open_bundle_resources`: resource-only app bundle session | documented | npm:rea, os:macos |
| `REA-258` | REA: مهارة «اعكس هندسة أي شيء» ومتى لا تستخدم REA | REA skill: reverse-engineer-anything, and when to skip REA | documented | npm:rea |
| `REA-006` | بناء سجل الالتزامات إعادة البناء | Generate a deterministic Evidence-backed reconstruction obligation ledger page | install | npm:rea |
| `REA-009` | التقاط سيناريو المتصفح | Run one bounded Playwright browser scenario and return Evidence | install | chromium, npm:rea, engine:wakaru |
| `REA-010` | التقاط سيناريو Electron | Run one owned Electron scenario with cancellable actions | install | npm:rea |
| `REA-012` | التقاط عملية | Capture one caller-selected process scenario | install | npm:rea |
| `REA-015` | مقارنة | Compare two canonical Evidence bundles | install | npm:rea |
| `REA-016` | مقارنة الإصدارات تطبيق | Compare two authenticated JavaScript Application Graph versions | install | chromium, npm:rea, engine:wakaru |
| `REA-017` | مقارنة أشكال التصدير جافاسكربت | Compare exact static JavaScript export return shapes without execution | install | chromium, npm:rea, engine:wakaru |
| `REA-018` | مقارنة الأعضاء مُدار (.NET) | Compare managed PE/CLI member inventories by exact declared type, name, and signature; names alone never form a match | install | npm:rea |
| `REA-019` | مقارنة التقاطات عملية | Compare two process capture Evidence JSON files | install | npm:rea |
| `REA-020` | مقارنة حزمة إلى المصدر | Compare committed historical source with authenticated application Evidence | install | chromium, npm:rea, engine:wakaru |
| `REA-022` | مقارنة التقاطات ويب | Compare two normalized passive captures or recorded browser scenarios | install | chromium, npm:rea, engine:wakaru |
| `REA-023` | مقارنة لقطات الشاشة ويب | Compare two self-verifying PNG artifact JSON values | install | chromium, npm:rea, engine:wakaru |
| `REA-033` | اكتشاف أدوات WebMCP | Passively discover page-declared WebMCP tools | install | chromium, npm:rea, engine:wakaru |
| `REA-035` | تقييم التغطية إعادة البناء | Evaluate inline fail-closed reconstruction coverage | install | npm:rea |
| `REA-036` | تصدير حزمة أدلة | Validate and atomically export canonical Evidence JSON | install | npm:rea |
| `REA-037` | استيراد حزمة أدلة | Validate and import a bounded local Evidence bundle | install | npm:rea |
| `REA-039` | تصدير السكربتات ويب | Export retained website scripts into an absent directory for static JavaScript analysis | install | chromium, npm:rea, engine:wakaru |
| `REA-043` | تعريف build Flutter | Identify a Flutter build's Dart snapshot hash and engine facts by pure APK parsing | install | npm:rea, engine:android |
| `REA-044` | استيراد إعادة البناء مُدار (.NET) | Import decompiler-produced managed reconstruction against exact static member evidence | install | npm:rea |
| `REA-045` | استيراد المصدر مرجعي | Import a source tree as historical reference only | install | chromium, npm:rea, engine:wakaru |
| `REA-055` | فحص حزمة أندرويد | Inspect APK declarations and decoded manifest without executing it | install | npm:rea, engine:android |
| `REA-060` | فحص AOT Dart | Inspect one ABI's Dart AOT snapshot: sections, headers, and the string pool | install | npm:rea, engine:android |
| `REA-062` | فحص صفحة Electron | Passively inspect one Electron file page | install | npm:rea |
| `REA-063` | فحص حزمة الأدلة | Inspect complete or selected discovery metadata from a local Evidence bundle | install | npm:rea |
| `REA-070` | فحص قطعة مُدار (.NET) | Inspect PE/CLI identity without loading target code | install | npm:rea |
| `REA-071` | فحص الأعضاء مُدار (.NET) | Inspect PE/CLI metadata members, signatures, CIL anchors, and ldstr string literals without loading target code | install | npm:rea |
| `REA-072` | فحص الحدود أصلية مُدار (.NET) | Inspect PE/CLI PInvoke and native implementation boundary declarations without loading target code | install | npm:rea |
| `REA-082` | فحص الموارد PE | Inspect PE resource identities, payload ranges, hashes and icon-group relationships | install | npm:rea |
| `REA-084` | فحص انهيار مسجّل | Inspect supplied core registers/signals and optional debugger mapping evidence | install | npm:rea, engine:rizin |
| `REA-088` | فحص database SQLite | Inspect SQLite schema and optional ordinary-table rows from a local snapshot | install | npm:rea |
| `REA-091` | فحص التقاط الشبكة ويب | Inspect retained HAR, native mitmproxy, Fiddler SAZ or aioquic qlog records without fetching recorded URLs | install | chromium, npm:rea, engine:wakaru |
| `REA-106` | سرد الأهداف Electron | List local file pages exposed by the selected Electron CDP endpoint | install | chromium, npm:rea |
| `REA-109` | سرد الأهداف وقت التشغيل جافاسكربت | List Node/Electron V8 Inspector targets | install | npm:rea |
| `REA-112` | مراقبة وقت التشغيل جافاسكربت | Passively observe one exact Node/Electron Inspector target | install | npm:rea |
| `REA-115` | مراقبة التنفيذ ويب | Observe precise page execution; resets counters and temporarily disables optimization | install | chromium, npm:rea, engine:wakaru |
| `REA-116` | مراقبة جلسة ويب | Observe user-driven page navigation during a chosen window | install | chromium, npm:rea, engine:wakaru |
| `REA-118` | إسقاط مخطط تطبيق أندرويد | Project authenticated APK inventory Evidence into an Android application graph | install | npm:rea, engine:android |
| `REA-120` | إسقاط مخطط تطبيق HarmonyOS | Project authenticated HarmonyOS HAP, HSP, or App Pack inventory Evidence into an application graph | install | npm:rea |
| `REA-121` | إسقاط مخطط تطبيق مُدار (.NET) | Project authenticated managed static Evidence into an application graph | install | npm:rea |
| `REA-129` | توفيق وقت التشغيل جافاسكربت | Reconcile static application and passive runtime Evidence JSON | install | npm:rea |
| `REA-130` | استعادة sources جافاسكربت | Recover readable JavaScript modules with source provenance and verified files | install | chromium, npm:rea, engine:wakaru |
| `REA-136` | إعداد REA | Configure agent integrations and optional analysis providers | install | npm:rea |
| `REA-144` | تتبّع الدلالات جافاسكربت | Trace bounded static semantic relations through authenticated application Evidence | install | chromium, npm:rea, engine:wakaru |
| `REA-147` | تتبّع الاستيرادات وحدة ويب | Trace one captured script's native imports to URLs and captured source candidates | install | chromium, npm:rea, engine:wakaru |
| `REA-148` | تتبّع موقع المصدر ويب | Trace one retained script position through an explicitly selected local source map | install | chromium, npm:rea, engine:wakaru |
| `REA-149` | إزالة | Remove REA-owned agent configuration and skill files | install | npm:rea |
| `REA-151` | تحديث REA | Update this REA installation and verify the installed release | install | npm:rea |
| `REA-152` | تحقق من الحدود أصلية مُدار (.NET) | Verify managed P/Invoke declarations against authenticated native Evidence | install | npm:rea |
