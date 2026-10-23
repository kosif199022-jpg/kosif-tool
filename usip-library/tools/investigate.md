# أدوات المجال `investigate` (13 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `atlas-bulk-source-audit` — ????? ???? ?????? ???? / Atlas source-text audit

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_bulk_source_audit.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `untested` |
| العائلات | `software-investigation` |

**ما تفعله:** ????? ???? ?????? ????? ?????? ????? ?? ???? ????? ??? ???????.

**What it does:** Audits an authorized local Atlas source sample and records evidence without executing third-party skill code.

#### متى تُستدعى

- «Review documented Atlas or Blender capabilities»
- «Inspect relevant tool arguments before running»
- «????? ??????? ???????? ?? ???????»

#### الأوامر

- **--help**: Show documented options; inspect inputs and authorization requirements before running any non-help action.
  - `python3 scripts/atlas_bulk_source_audit.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: Require the user's authorization before analyzing third-party installations, invoking REA or Blender, writing files, or performing any external actions. --help is informational.
- الحدود: Registration describes discovery; verify CLI and run targeted tests. Do not infer that Atlas entries are runnable or that Blender/Ghidra work without installed binaries.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/SKILL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-bulk-source-audit --evidence <ملف>`.

### `atlas-deep-fusion` — ????? ??? ???? / Atlas read-only method selector

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_deep_fusion.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `untested` |
| العائلات | `software-investigation` |

**ما تفعله:** ????? ??? ????? ?????? ????? ?? ???? ????? ??? ???????.

**What it does:** Selects source-linked Atlas methods for review against an authorized local Atlas index.

#### متى تُستدعى

- «Review documented Atlas or Blender capabilities»
- «Inspect relevant tool arguments before running»
- «????? ??????? ???????? ?? ???????»

#### الأوامر

- **--help**: Show documented options; inspect inputs and authorization requirements before running any non-help action.
  - `python3 scripts/atlas_deep_fusion.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: Require the user's authorization before analyzing third-party installations, invoking REA or Blender, writing files, or performing any external actions. --help is informational.
- الحدود: Registration describes discovery; verify CLI and run targeted tests. Do not infer that Atlas entries are runnable or that Blender/Ghidra work without installed binaries.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/SKILL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-deep-fusion --evidence <ملف>`.

### `atlas-review-summary` — ???? ?????? ???? / Atlas review summary

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_review_summary.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `untested` |
| العائلات | `software-investigation` |

**ما تفعله:** ???? ?????? ????? ?????? ????? ?? ???? ????? ??? ???????.

**What it does:** Summarizes source-audit evidence and provenance for candidate Atlas methods.

#### متى تُستدعى

- «Review documented Atlas or Blender capabilities»
- «Inspect relevant tool arguments before running»
- «????? ??????? ???????? ?? ???????»

#### الأوامر

- **--help**: Show documented options; inspect inputs and authorization requirements before running any non-help action.
  - `python3 scripts/atlas_review_summary.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: Require the user's authorization before analyzing third-party installations, invoking REA or Blender, writing files, or performing any external actions. --help is informational.
- الحدود: Registration describes discovery; verify CLI and run targeted tests. Do not infer that Atlas entries are runnable or that Blender/Ghidra work without installed binaries.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/SKILL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-review-summary --evidence <ملف>`.

### `atlas-reviewed-methods-v3` — ??? ???? ???????? / Reviewed Atlas methods

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_reviewed_methods_v3.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `untested` |
| العائلات | `software-investigation` |

**ما تفعله:** ??? ???? ????????? ?????? ????? ?? ???? ????? ??? ???????.

**What it does:** Works with reviewed Atlas method records and their provenance.

#### متى تُستدعى

- «Review documented Atlas or Blender capabilities»
- «Inspect relevant tool arguments before running»
- «????? ??????? ???????? ?? ???????»

#### الأوامر

- **--help**: Show documented options; inspect inputs and authorization requirements before running any non-help action.
  - `python3 scripts/atlas_reviewed_methods_v3.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: Require the user's authorization before analyzing third-party installations, invoking REA or Blender, writing files, or performing any external actions. --help is informational.
- الحدود: Registration describes discovery; verify CLI and run targeted tests. Do not infer that Atlas entries are runnable or that Blender/Ghidra work without installed binaries.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/SKILL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-reviewed-methods-v3 --evidence <ملف>`.

### `atlas-transfer` — ??? ??? ???? / Atlas verified method transfer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_transfer.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `untested` |
| العائلات | `software-investigation` |

**ما تفعله:** ??? ??? ????? ?????? ????? ?? ???? ????? ??? ???????.

**What it does:** Converts reviewed Atlas records into KOSIF capability catalog data; writes files only when explicitly approved.

#### متى تُستدعى

- «Review documented Atlas or Blender capabilities»
- «Inspect relevant tool arguments before running»
- «????? ??????? ???????? ?? ???????»

#### الأوامر

- **--help**: Show documented options; inspect inputs and authorization requirements before running any non-help action.
  - `python3 scripts/atlas_transfer.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: Require the user's authorization before analyzing third-party installations, invoking REA or Blender, writing files, or performing any external actions. --help is informational.
- الحدود: Registration describes discovery; verify CLI and run targeted tests. Do not infer that Atlas entries are runnable or that Blender/Ghidra work without installed binaries.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/SKILL.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-transfer --evidence <ملف>`.

### `differential-exam` — مصحّح الامتحان الخفي التفاضلي / Differential hidden-exam scorer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/differential_exam.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `tested-here` |
| العائلات | `verification-evals`, `software-investigation` |

**ما تفعله:** يقارن تشغيلًا مرشحًا بتشغيل مرجعي سيناريو سيناريو وملفًا ملفًا (<run>/<scenario>/<files>)، فيقارن JSON وJSONL كبيانات وباقي الملفات كنص بعد إخفاء القيم المتغيرة (المعرّفات والأختام الزمنية والمسارات المؤقتة والأزمنة والمفاتيح المستبعدة). ويختم الامتحان ببصمات SHA-256 قبل بدء العمل ويتحقق من الختم لاحقًا، ولا يثق في المصحّح حتى يعطي المرجع ضد نفسه 100%. مكتبة Python القياسية فقط، ولا يشغّل شيئًا.

**What it does:** Scores a candidate run against a reference run folder by folder and file by file (<run>/<scenario>/<files>), comparing JSON and JSONL as data and other files as text after masking volatile values (UUIDs, timestamps, epochs, temp names, long hex ids, durations, named root paths and dropped keys). It seals an exam with SHA-256 hashes before the work starts and verifies the seal later, and its self-check refuses to trust the scorer until reference against reference scores 100%. Stdlib only; it runs nothing.

#### متى تُستدعى

- «قارن مخرجات النسخة المستنسخة بالأصل سيناريو سيناريو»
- «اختم الامتحان الخفي قبل ما يبدأ الشغل»
- «compare a clone's recorded requests and outputs with the original»
- «check my scorer gives 100% on the reference against itself»

#### الأوامر

- **seal**: Hashes every file under the exam folder into a seal JSON written outside it, before the builder starts.
  - `python3 scripts/differential_exam.py seal ./exam --out ./exam-seal.json`
- **verify-seal**: Lists changed, missing and added exam files; exits 1 when the seal is broken.
  - `python3 scripts/differential_exam.py verify-seal ./exam ./exam-seal.json`
- **self-check**: Scores reference against itself or a second reference run; exits 1 and prints the remaining differences until it reaches 100% (add --rule REGEX=>TOKEN, --root, --skip-key).
  - `python3 scripts/differential_exam.py self-check ./real-run-1 ./real-run-2 --root /tmp/work`
- **compare**: Prints per-scenario ok/total, the first difference of each failed file and TOTAL ok/total = percent; --min makes it exit 1 below that percentage.
  - `python3 scripts/differential_exam.py compare ./real-run ./clone-run --min 95 --json`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: seal writes only the --out file, which must be outside the exam folder.
- الحدود: It compares files that already exist: it does not run the reference or the candidate, does not build the mock model server, and cannot tell whether the scenarios cover enough behaviour. The default masks can hide a real difference in a long hex value or a duration; use --no-default-masks when those matter.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_differential_exam.py`
- مرجع: `.claude/skills/kosif-superpowers/references/codex-agent-harness.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/investigate.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:differential-exam --evidence <ملف>`.

### `installer-triage` — فرز المثبّتات / Installer Triage

| الحقل | القيمة |
|---|---|
| المسار | `scripts/installer_triage.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `tested-here` |
| العائلات | `software-investigation`, `app-feature-transfer` |

**ما تفعله:** فرز لمثبّتات ويندوز وتطبيقات سطح المكتب بالمكتبة القياسية قبل استخدام REA. يتعرّف على نوع المثبّت (NSIS وInno وWiX Burn وSquirrel وInstallShield وMSI) وضغط UPX وElectron و‎.NET وخانة التوقيع، ويكشف الحمولات المخبّأة في موارد PE. ويسرد كذلك محتوى حزم asar في Electron ويستخرج بصمة قدراتها، ويستخرج الحمولة بـ 7-Zip أو innoextract عند الإذن، ويحدّد لكل عنصر أمر REA المناسب.

**What it does:** Standard-library triage of Windows installers and desktop apps before REA. It identifies the installer family (NSIS, Inno, WiX Burn, Squirrel, InstallShield, MSI), UPX packing, Electron, .NET and the signature slot, and finds payloads hidden in PE resources. It also lists and fingerprints Electron asar bundles, unpacks payloads with 7-Zip or innoextract on request and maps each artifact to the matching REA command.

#### متى تُستدعى

- «افحص ملف setup.exe قبل الهندسة العكسية»
- «إيه المزايا اللي جوّه تطبيق Electron ده من ملف app.asar؟»
- «ما نوع هذا المثبّت وهل هو موقّع؟»
- «unpack this NSIS installer safely before analysis»
- «fingerprint an app.asar for its Electron features»
- «which REA command fits each file in this unpacked folder?»

#### الأوامر

- **scan**: Classifies a file, or the top-level .exe/.msi/.dll/.asar/.zip/.7z/.rar files in a folder. It reports installer family, packer, Electron, .NET, signature slot, version strings, embedded PE-resource payloads, encrypted RAR and Adobe offline packages, then proposes next steps (unpack or REA commands). Read-only.
  - `python3 scripts/installer_triage.py scan ./setup.exe`
- **unpack**: Extracts the payload into a folder that must not exist yet, using 7-Zip (innoextract for Inno Setup), and goes up to two nested archive levels deep. It never runs the target, needs --authorized and a 7-Zip binary, and returns a file manifest plus the target's sha256.
  - `python3 scripts/installer_triage.py unpack ./setup.exe --to ./unpacked --authorized`
- **asar**: Lists an Electron asar archive (files, largest entries, package.json, renderers) or prints one small text entry.
  - `python3 scripts/installer_triage.py asar ./app.asar package.json`
- **fingerprint**: Counts Electron capability anchors (screen capture, auto-update, deep links, safeStorage and more) in the main and preload bundles, plus file associations, renderer windows and RTL UI, as evidence that features exist.
  - `python3 scripts/installer_triage.py fingerprint ./app.asar`
- **route**: Walks an unpacked folder and maps each asar, large exe, managed dll, msi, zip/nupkg and sqlite file to the REA or triage commands that fit it. Nothing is run.
  - `python3 scripts/installer_triage.py route ./unpacked`

#### المتطلبات والأمان

- binaries: python3
- optional: bin:7z, bin:innoextract
- الأمان: runs-external-programs
- الموافقة: unpack runs a third-party extractor (7-Zip, or innoextract for Inno Setup) on a binary the user supplies and writes its contents into a new folder. It needs --authorized and the user's confirmation that they may inspect the binary; the target itself is never run. An encrypted RAR is refused: ask the owner for the password and never guess it. scan, asar, fingerprint and route are read-only.
- الحدود: Reports installer, packer and Electron structure and counts Electron API anchors. That shows code is present, not that a feature is reachable or enabled (verified is always false). It never runs the installer.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_installer_triage.py`
- مرجع: `.claude/skills/kosif-superpowers/references/rea-reverse-engineering.md`
- مرجع: `.claude/skills/kosif-superpowers/references/app-feature-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/software-investigation.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/app-feature-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/investigate.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/windows-installers-rea/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:installer-triage --evidence <ملف>`.

### `local-project-audit` — فحص المشروع المحلي دون تشغيل / Local project static audit

| الحقل | القيمة |
|---|---|
| المسار | `scripts/local_project_audit.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `tested-here` |
| العائلات | `software-investigation`, `security-safety` |

**ما تفعله:** يجري جردًا ساكنًا للقراءة فقط لمجلد محلي دون تشغيل أي شيء، ويعيد تقرير JSON يتضمّن أعداد الملفات وامتداداتها وتصنيف وجهتها (مراجعة الشيفرة، أو ملفات ثنائية مرشّحة للتحليل بـ Ghidra أو REA، أو أرشيفات، أو وسائط) ومؤشرات مطابقة الأنماط وبصمات SHA-256 وإحصاءات أمان ملفات zip.

**What it does:** Performs a read-only static inventory of a local folder without executing anything and returns a JSON report of file counts, extensions, routes (source review, Ghidra/REA binary candidates, archives, media), regex indicators, SHA-256 hashes and zip-safety stats.

#### متى تُستدعى

- «افحص مجلد المشروع هذا وقل لي محتواه بدون تشغيل أي شيء»
- «عايز جرد سريع للملفات وأي ملفات تنفيذية في الفولدر ده»
- «أبي تقرير عن امتدادات الملفات والمؤشرات الثابتة في المشروع»
- «Do a read-only triage of this local project folder»
- «Which files in this repo are binaries worth looking at with Ghidra or REA?»
- «Check this folder for zip files with path traversal entries»

#### الأوامر

- **scan**: Walks the folder read-only and prints a JSON summary: file and byte counts, extensions, routes, indicator counts and the unreadable count.
  - `python3 scripts/local_project_audit.py ./my-project`
- **scan-with-report**: Also writes the full report (per-file samples with sha256, indicators and zip stats, plus skipped items) to a path outside the audited folder, creating parent folders. It caps the walk at 20000 files.
  - `python3 scripts/local_project_audit.py ./my-project --output ./audit/report.json --limit 20000`
- **library**: Calls scan(root, limit) directly and returns the full report dict without writing anything.
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); import local_project_audit as a; print(a.scan('templates')['routes'])"`
- **help**: Shows the positional root and the --output and --limit options.
  - `python3 scripts/local_project_audit.py --help`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Reads and hashes every file under the chosen folder, which may hold private data: confirm the user wants that folder inspected. --output creates parent folders and silently overwrites an existing report file.
- الحدود: Static, file-level triage by extension and regex signatures only; it never executes or extracts anything and cannot prove runtime behavior, malware status or licensing.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_local_project_audit.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/investigate.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/3d.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:local-project-audit --evidence <ملف>`.

### `rea-bridge` — جسر أوامر REA / REA CLI Bridge

| الحقل | القيمة |
|---|---|
| المسار | `scripts/rea_bridge.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `tested-here` |
| العائلات | `software-investigation`, `self-discovery` |

**ما تفعله:** جسر اختياري إلى أداة REA للهندسة العكسية لا يتجاوز ما تثبته الأدلة. يفحص جاهزية Node وREA، ويسرد سجلات REA الـ241 في الكتالوج (153 أمرًا سطريًا و76 أداة MCP و6 قوالب أوامر و6 إضافات فرز من KOSIF)، ويخطّط للفحص دون تنفيذه. ولا يشغّل أحد فاحصات REA الساكنة المحلية الأربعة عشر إلا مع ‎--authorized، ويحفظ الناتج في ملف JSON جديد يسمّيه المستخدم.

**What it does:** Opt-in bridge to the REA reverse-engineering CLI that stays within what the evidence shows. It checks Node and REA readiness, lists the 241 REA power records in the catalog (153 CLI commands, 76 MCP tools, 6 prompts and 6 KOSIF installer-triage additions) and plans an inspection without running it. Only with --authorized does it run one of 14 static local REA inspectors, saving the output to a new JSON file named by the caller.

#### متى تُستدعى

- «شغّل فحص REA ساكنًا على تطبيق JavaScript واحفظ النتيجة في ملف»
- «اعرض قائمة أوامر REA المتاحة وحالة كل أمر»
- «هو REA متسطّب عندي ولا لأ؟ ونسخة Node مناسبة؟»
- «check if REA and Node are installed and compatible»
- «plan a .NET assembly inspection before running it»
- «run REA on this extracted Electron app and save the JSON evidence»

#### الأوامر

- **doctor**: Reports whether a REA launcher is found (REA_BIN or `rea` on PATH) and runs `node --version` to check against REA's supported range (22.19+, 24.11+ or 26+). Prints the result as a JSON report.
  - `python3 scripts/rea_bridge.py doctor`
- **catalog**: Lists the 241 REA power records from data/powers/software-investigation.json with their status, section and extra requirement. An optional text query filters the list. Nothing is run.
  - `python3 scripts/rea_bridge.py catalog sqlite`
- **plan**: Builds the exact REA argv for an existing target without running it. Kinds with no static command return a REA docs link (provider or manual workflow), and the 'installer' kind redirects to installer_triage.py scan.
  - `python3 scripts/rea_bridge.py plan javascript ./app --source-path ./app/main.js`
- **run**: Runs one of 14 static REA inspectors. It needs --authorized, an installed REA and a compatible Node. REA's JSON stdout goes to a new --output file (exclusive create, in an existing folder), and the tool returns the file's sha256 and byte count with verified=false.
  - `python3 scripts/rea_bridge.py run javascript ./app --authorized --output ./out/rea-evidence.json`

#### المتطلبات والأمان

- binaries: python3
- optional: bin:node, bin:rea
- الأمان: runs-external-programs
- الموافقة: run executes the third-party REA CLI (npm package rea-agents, which the user installs separately with approval) against a target the user names. It needs --authorized and the user's confirmation that they own the target or may inspect it. doctor only runs `node --version`, and catalog and plan run nothing, so they need no approval.
- الحدود: Runs only REA's 14 static local inspectors. It never installs REA, never runs native, dynamic or provider workflows (plan only links their docs) and never validates findings (verified is always false). Its Node gate does not account for per-command needs, such as Node 24.15+ for inspect-sqlite-database.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_rea_bridge.py`
- مرجع: `.claude/skills/kosif-superpowers/references/rea-reverse-engineering.md`
- مرجع: `.claude/skills/kosif-superpowers/references/rea-upstream-capabilities.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/software-investigation.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/investigate.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/windows-installers-rea/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:rea-bridge --evidence <ملف>`.

### `rea-family-router` — موجّه عائلات REA / REA Family Router

| الحقل | القيمة |
|---|---|
| المسار | `scripts/rea_family_router.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `tested-here` |
| العائلات | `software-investigation`, `self-discovery` |

**ما تفعله:** موجّه للقراءة فقط يربط كلمة واحدة تصف الهدف من قائمة ثابتة فيها 29 كلمة (مثل dotnet وapk وhar وfirmware وsqlite) بواحدة من 16 عائلة قدرات في REA، ويذكر اسم الأداة الأصلية وحالة توفّرها. ويبيّن كذلك هل rea وnode موجودان في PATH.

**What it does:** Read-only router that maps one target keyword from a fixed 29-word list (dotnet, apk, har, firmware, sqlite and others) to one of 16 REA capability families, giving the upstream tool name and availability status. It also reports whether rea and node are on PATH.

#### متى تُستدعى

- «أي أمر في REA يناسب ملف APK؟»
- «وجّه هدف dotnet إلى عائلة REA الصحيحة»
- «هو REA موجود على الجهاز ده؟»
- «which REA tool handles a HAR network capture?»
- «list the REA capability families»

#### الأوامر

- **list**: Prints all 16 REA capability families with examples, availability status and the upstream tool name.
  - `python3 scripts/rea_family_router.py list`
- **route**: Maps one exact intent keyword (case-insensitive) to its REA family and tool name without running anything. An unknown word returns not_an_rea_target.
  - `python3 scripts/rea_family_router.py route dotnet`
- **doctor**: Reports whether rea and node are on PATH (shutil.which only) and prints a suggested dry-run setup command, which it never runs.
  - `python3 scripts/rea_family_router.py doctor`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: Maps one exact keyword from a fixed list to a REA family and tool name. It does not understand free text, never runs or installs REA and never confirms the tool exists in the installed version (verified is always false; provider_version is always 'unknown').

#### الاختبارات والأدلة

- `tests/test_rea_family_router.py`
- مرجع: `.claude/skills/kosif-superpowers/references/rea-reverse-engineering.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/investigate.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:rea-family-router --evidence <ملف>`.

### `rea-owned-repo-batch` — تحليل REA لمستودعات المالك دفعةً واحدة / REA Owned-Repo Batch

| الحقل | القيمة |
|---|---|
| المسار | `scripts/rea_owned_repo_batch.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `untested` |
| العائلات | `software-investigation`, `code-engineering` |

**ما تفعله:** تحليل REA ساكن على دفعات لمستودعات المستخدم على GitHub المكتوبة بـ JavaScript أو TypeScript أو HTML. يقرأ جردًا خاصًا يُنشئه الأمر rea_creative_research_atlas.py own، ثم يستنسخ بـ git أصغر المستودعات المؤهَّلة ضمن حدّ الحجم استنساخًا سطحيًا (عمق 1 وblob:none)، ويشغّل عليها أمر REA analyze-javascript-application عبر node. تبقى النسخ والأدلة في مجلد خاص محلي، ولا يطبع إلا الأعداد.

**What it does:** Batch static REA analysis of the user's own JavaScript, TypeScript and HTML GitHub repositories. It reads a private inventory (made by rea_creative_research_atlas.py own), shallow-clones the smallest eligible repos under a size cap with git (depth 1, blob:none) and runs REA's analyze-javascript-application on each through node. Clones and evidence stay in a local private folder, and only counts are printed.

#### متى تُستدعى

- «حلّل مستودعاتي على GitHub بـ REA دفعة واحدة»
- «استخرج أدلة REA من مشاريع JavaScript اللي أملكها»
- «افحص شيفرة مستودعاتي الخاصة محليًا من غير ما تشغّلها»
- «run REA statically over all my owned JS repos»
- «batch-analyze the source of my GitHub repositories with REA»

#### الأوامر

- **run**: Picks JS, TS and HTML repos from the private inventory that are at or under --max-size-kb. It shallow-clones up to --max-repos of them over HTTPS, runs `node <rea-cli> analyze-javascript-application` on each, writes per-repo evidence and a results file, and prints a counts-only summary.
  - `python3 scripts/rea_owned_repo_batch.py --private-output "$HOME/kosif-private" --rea-cli ./node_modules/rea-agents/scripts/rea.mjs --max-repos 16 --max-size-kb 8000`

#### المتطلبات والأمان

- binaries: git, node, python3
- network: true
- node: rea-agents
- الأمان: network
- الموافقة: It clones the user's GitHub repositories over the network, using git with the user's credentials for private repos, and runs the third-party REA CLI on each clone. It needs the user's confirmation that they own or may analyze every repo in the inventory, a prepared private inventory and an output folder outside any git checkout (the script refuses a folder inside a git repository).
- الحدود: Analyzes only JS, TS and HTML repos under the size cap, using REA's static JavaScript analyzer. It does not verify runtime features, build the inventory or install REA.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/REA_CREATIVE_DISCOVERY_2000_20261019.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `docs/REA_CREATIVE_DISCOVERY_2000_20261019.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:rea-owned-repo-batch --evidence <ملف>`.

### `repository-capability-packer` — فحص المستودعات وحزمها / Repository Capability Packer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/repository_capability_packer.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `tested-here` |
| العائلات | `software-investigation`, `code-engineering` |

**ما تفعله:** يفحص مجلد مستودع محليًا أو ملف ZIP للشيفرة المصدرية بحثًا عن اللغات وإشارات القدرات وملفات التراخيص، ويبني بصمة SHA-256 لكل ملف. ثم يحزم الشيفرة في ملف ZIP مُرشَّح يتكرّر ناتجه حرفيًا، ويرفق به تقرير JSON لنقل القدرات. يستبعد مجلدات البناء والأرشيفات والملفات التنفيذية والصوت والفيديو والمفاتيح وقواعد البيانات والملفات التي توحي أسماؤها بأسرار، ولا يشغّل أي شيفرة ولا يستوردها ولا يثبّتها.

**What it does:** Inspects a local repository folder or source ZIP for languages, capability signals, license files and a per-file SHA-256 manifest. It packs a deterministic, filtered source ZIP plus a JSON capability-transfer report, leaving out build caches, archives, executables, audio and video, keys, databases and files whose names suggest secrets. Nothing is run, imported or installed.

#### متى تُستدعى

- «جهّز نسخة نظيفة من هذا المستودع لنقل قدراته»
- «احزم كود المشروع من غير أسرار ولا ملفات تنفيذية»
- «ما لغات هذا المستودع وما ملفات تراخيصه؟»
- «inspect a repo for reusable capabilities and licenses»
- «pack a downloaded GitHub ZIP into a sanitized source archive»

#### الأوامر

- **inspect**: Reports languages, capability signals, license files and excluded files on stdout, without the manifest. With --out it also writes the full report, including the sha256 manifest, to that path; the parent folder must already exist.
  - `python3 scripts/repository_capability_packer.py inspect ./repo --out ./repo-report.json`
- **pack**: Writes a deterministic filtered source ZIP (fixed timestamps, sorted entries) outside the input folder, creating parent folders as needed. With --report it also writes the capability-transfer report with package_sha256.
  - `python3 scripts/repository_capability_packer.py pack ./repo --out ./out/repo.zip --report ./out/report.json`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: pack and inspect --out write files to paths the user names. pack overwrites an existing --out file, and inspect --out is not stopped from writing inside the input folder, so choose fresh paths. Before reusing or sharing the ZIP, review licenses and any secrets inside files, because filtering goes by file name only (reuse_allowed is always false).
- الحدود: Infers candidate capabilities from file names and extensions only, and filters secrets by file name, not content. Images, fonts and PDFs stay in the ZIP. It never runs, imports, clones or licenses the code.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_repository_capability_packer.py`
- مرجع: `.claude/skills/kosif-superpowers/references/repository-capability-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/investigate.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repository-capability-packer --evidence <ملف>`.

### `web-app-study` — دراسة تطبيق ويب عام بـ REA (حقائق فقط) / Web app study (public frontend, REA, facts only)

| الحقل | القيمة |
|---|---|
| المسار | `scripts/web_app_study.py` (جذر: skill) |
| المجال | `investigate` |
| الدليل | `tested-here` |
| العائلات | `software-investigation`, `app-feature-transfer` |

**ما تفعله:** يدرس صفحة ويب عامة للقراءة فقط: متصفح بلا تسجيل دخول وملف شخصي جديد يُحذف بعد التشغيل، ثم يلتقط REA الصفحة وأدوات WebMCP المعلنة ولقطة شاشة والسكربتات العامة ببصمات SHA-256. التقرير حقائق فقط: الإطار وإصداره، ومكتبات اللوحة والمحرر والتزامن، والخدمات المستنتجة من أسماء مفاتيح التخزين، بدليل اسم ملف ومعرّف، وبلا أي كود.

**What it does:** Studies one public web page read-only: a logged-out headless Chromium with a fresh profile and background networking off (fresh profile, deleted afterwards), then REA captures the page, page-declared WebMCP tools, a screenshot and the public scripts, with SHA-256 receipts; optional bounded static JavaScript analysis. report turns a study folder into facts only: framework and versions, canvas/editor/realtime libraries, services inferred from storage key NAMES, WebMCP tools and page metrics, each with file-and-identifier evidence and never code. Written for the MagicPath study; runs on any desktop OS.

#### متى تُستدعى

- «حلل واجهة موقع MagicPath العامة بـ REA واعرف مبني بإيه»
- «Study a public web app's frontend stack and declared WebMCP tools without logging in»
- «اعمل تقرير تقني عن تطبيق ويب عشان نستلهم أفكاره بدون نسخ كوده»

#### الأوامر

- **doctor**: Finds REA and a Chromium/Chrome/Edge binary.
  - `python3 scripts/web_app_study.py doctor`
- **run (plan only)**: Prints the isolated browser command and every REA step without starting anything.
  - `python3 scripts/web_app_study.py run https://www.example.com --out ~/kosif-studies/example --dry-run`
- **run**: Isolated logged-out capture: targets, page (scripts, storage key names), WebMCP tools, screenshot, script export, receipts, then the report. Add --deep for REA's bounded static JavaScript analysis.
  - `python3 scripts/web_app_study.py run https://www.example.com --out ~/kosif-studies/example`
- **report**: Facts-only report.json and report.md from a study folder.
  - `python3 scripts/web_app_study.py report ~/kosif-studies/example`

#### المتطلبات والأمان

- binaries: chromium, rea
- network: true
- الأمان: network
- الموافقة: Visits the given public URL in a fresh, logged-out browser and saves its public scripts to a folder outside the repo. Only for sites the user may study; never log in, never commit the exported scripts, borrow ideas in your own words.
- الحدود: One page per run, logged out, so features behind sign-in are not observed; storage values, cookies and request bodies are never kept; library detection is identifier-based (a name can appear without the library being used — confidence is shown); the unbounded REA bundle analyzer is not used because it ran out of memory (about 8 GB, observed, not receipted) on MagicPath's 5.8 MB bundle. Exit code 2 when a required step failed or the profile could not be deleted.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_web_app_study.py`
- مرجع: `.claude/skills/kosif-superpowers/references/app-studies/magicpath.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:web-app-study --evidence <ملف>`.

