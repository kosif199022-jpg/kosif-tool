# أدوات المجال `sources` (18 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `atlas-audit-synthesis` — تحويل مراجعة الأطلس إلى بيان مُراجَع / Atlas audit to reviewed manifest

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_audit_synthesis.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `untested` |
| العائلات | `web-research`, `security-safety` |

**ما تفعله:** يحوّل ملف records.json الخاص الناتج من atlas_body_audit.py ومجلد نتائج تحليل REA الساكن إلى بيان مُراجَع من البيانات الوصفية فقط (لكل مهارة: بصمة SHA-256 لـSKILL.md، وعدد ملفات الكود المقروءة، والمؤشرات، وادعاء الرخصة) وتقرير نتائج قصير. لا يُنسخ أي نص لطرف ثالث، فيمكن حفظ البيان في data/atlas-reviewed/manifest.json ليقرأه atlas_external_bridge.py ويعلّم نتائج البحث.

**What it does:** Turns the private records.json from atlas_body_audit.py and a folder of REA static-analysis results into a metadata-only reviewed manifest (per skill: SKILL.md SHA-256, code files read, indicators, licence claim) and a short findings report. No third-party text is copied into the outputs, so the manifest can be committed as data/atlas-reviewed/manifest.json, which atlas_external_bridge.py reads to annotate search results.

#### متى تُستدعى

- «حوّل نتائج مراجعة الأطلس إلى بيان نقدر نحفظه في الريبو»
- «اعمل تقرير ملخص لمراجعة مهارات الأطلس»
- «build the committed reviewed manifest from my private Atlas audit records»
- «summarise the Atlas audit and REA results without copying third-party text»

#### الأوامر

- **synthesize**: Groups the records by skill, attaches REA results from --rea-dir, and writes the metadata-only manifest and the Markdown findings report.
  - `python3 scripts/atlas_audit_synthesis.py --records ./out/atlas-audit-private/records.json --rea-dir ./out/rea --manifest-out ./out/manifest.json --report-out ./out/atlas-reviewed-audit.md`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only the two output paths given; review the manifest for private paths before committing it.
- الحدود: Only summarises what the audit and REA already recorded, so it adds no new verification; the counts describe the sample, not the whole Atlas.

#### الاختبارات والأدلة

- `tests/test_atlas_body_audit.py`
- مرجع: `.claude/skills/kosif-superpowers/references/atlas-reviewed-audit.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-audit-synthesis --evidence <ملف>`.

### `atlas-body-audit` — مراجعة ساكنة لنصوص مهارات الأطلس / Atlas skill-body static audit

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_body_audit.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `security-safety` |

**ما تفعله:** يختار عيّنة محدودة موزّعة على المواضيع من فهرس أطلس KOSIF (ومن فهرس copyleft اختياري)، ويجلب نص SKILL.md لكل مهارة وحتى N من ملفات سكربتاتها من مستودع kosif-atlas، ويفحصها بحثًا عن مؤشرات مراجعة (تنفيذ سكربت عن بُعد، أوامر حذف، جمع أسرار، تجاوز التعليمات، تثبيت حزم). لا ينفّذ شيئًا، ويكتب النصوص المجلوبة وrecords.json وsummary.json في مجلد --out خاص فقط.

**What it does:** Picks a bounded, topic-stratified sample of skills from a KOSIF Atlas index (plus an optional copyleft index), fetches each raw SKILL.md and up to N of its script files from the kosif-atlas repository, and scans them for review indicators (remote script execution, destructive shell, secret collection, prompt override, installs). It never executes anything and writes the fetched text, records.json and summary.json only to a private --out directory.

#### متى تُستدعى

- «راجع لي نصوص مهارات الأطلس قبل ما نستخدمها»
- «افحص عيّنة من مهارات Atlas بحثًا عن أوامر خطرة»
- «statically review a sample of Atlas skill bodies before using them»
- «audit the next 200 Atlas skills for risky instructions»

#### الأوامر

- **audit**: Fetches the selected skills' SKILL.md and up to --scripts-per-skill code files (default 2), scans them for indicators, and writes source/, records.json and summary.json under --out; prints the summary.
  - `python3 scripts/atlas_body_audit.py --index ./atlas-index.json --out ./out/atlas-audit-private --limit 200`

#### المتطلبات والأمان

- network: true
- الأمان: network
- الموافقة: Downloads third-party text from raw.githubusercontent.com into a private folder; keep it out of the repository and do not run or merge any fetched code without the owner's task-specific approval.
- الحدود: A sample, not full coverage, and static only: an indicator is a prompt for human review, not a malware verdict, and nothing proves a skill works; fetching needs network access to the kosif-atlas repository.

#### الاختبارات والأدلة

- `tests/test_atlas_body_audit.py`
- مرجع: `.claude/skills/kosif-superpowers/references/atlas-reviewed-audit.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-body-audit --evidence <ملف>`.

### `atlas-external-bridge` — بحث مهارات أطلس الخارجية / Atlas external skill search

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_external_bridge.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `security-safety` |

**ما تفعله:** يقرأ فهرس KOSIF Atlas المحلي لمهارات الجهات الخارجية (مع فهرس اختياري للمهارات ذات تراخيص الحقوق المتروكة copyleft)، ويطبع إحصاءات أو نتائج مرتبة بالكلمات المفتاحية مع نطاق الترخيص وعلامات الخطر وحكم المراجعة؛ ومع الخيار --skill-root يقرأ أيضًا عناوين ملف SKILL.md لكل نتيجة. ولا يشغّل أي شيء.

**What it does:** Reads a local KOSIF Atlas index of third-party skills (plus an optional copyleft index) and prints stats or keyword-ranked matches with licence scope, risk flags and verdicts; with --skill-root it also reads each match's SKILL.md headings. It never executes anything.

#### متى تُستدعى

- «دوّر في أطلس المهارات على مهارة رندر بلندر»
- «search the Atlas index for Blender rendering skills»
- «كم مهارة في الأطلس عليها علامات خطر؟»
- «which Atlas skills are copyleft and reference-only?»

#### الأوامر

- **stats**: Counts entries by licence scope, licence label, verdict and heuristic domain, plus how many are risk-flagged.
  - `python3 scripts/atlas_external_bridge.py stats --index ./atlas_index.json --copyleft-index ./atlas_copyleft_index.json`
- **search**: Ranks entries by query words found in the skill name (x5) or else in description/plugin (x1), keeping only positive scores. With --skill-root it reads the matching SKILL.md read-only (≤256 KB, paths that resolve outside the root return INVALID_PATH) and reports its line count and up to 12 headings.
  - `python3 scripts/atlas_external_bridge.py search --index ./atlas_index.json --query "Blender render" --top 10 --skill-root ./atlas_skills/`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: Reads a private local Atlas index the user supplies; keep its contents out of public commits. Installing or running any listed skill needs separate user approval and review.
- الحدود: Needs an external Atlas index JSON that this repo does not ship. It only ranks metadata (optionally reading SKILL.md headings) and never runs, installs or vets the listed skills.

#### الاختبارات والأدلة

- `tests/test_atlas_cycles_integration.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `docs/KOSIF_TAJRIBA_ATLAS_REALISTIC_RENDER_20261020.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-external-bridge --evidence <ملف>`.

### `atlas-metadata-audit` — تدقيق بيانات أطلس الوصفية / Atlas metadata audit

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_metadata_audit.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `qa-verification`, `security-safety` |

**ما تفعله:** يدقّق، دون تشغيل أي كود، فهرس مهارات KOSIF Atlas وفهرسه المرافق للمهارات ذات تراخيص الحقوق المتروكة (copyleft)، بحثًا عن مشكلات البنية والعدد والمعرّفات والحقول الإلزامية، ويعدّ السجلات التي لا يكون مصدرها رابط https. ويطبع تقرير JSON عن تسميات التراخيص والأحكام ونطاقات المصادر والأخطاء البنيوية، ويمكنه أيضًا حفظه في ملف جديد.

**What it does:** Statically audits a KOSIF Atlas skill index and its copyleft companion for schema, count, ID and required-field problems, and counts records whose source is not an https URL. It prints a JSON report of licence labels, verdicts, source hosts and structural errors, and can also save it to a new file.

#### متى تُستدعى

- «افحص فهرس الأطلس وتأكد إن مفيش أخطاء في البنية»
- «audit the Atlas index metadata before importing any skills»
- «كم سجل في الأطلس حكمه REVIEW_BEFORE_INSTALL؟»
- «validate atlas_index.json counts, IDs and source URLs»

#### الأوامر

- **audit**: Checks both indexes (count field matches, unique non-empty IDs per index, required plugin/skill/description/license/source/path/verdict fields) and tallies licences, verdicts, risk flags, REVIEW_BEFORE_INSTALL/READ_ONLY_OK records and source hosts; non-https sources are counted, not treated as structural errors. Prints the report and, with --output, also writes it to a new file (refuses to overwrite or to create folders).
  - `python3 scripts/atlas_metadata_audit.py --index ./atlas_index.json --copyleft ./atlas_copyleft_index.json --output ./out/atlas_audit.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: --output writes a new report file (it never overwrites). The Atlas indexes are the user's private local files: keep them and the report out of public commits.
- الحدود: Checks index structure, labels, source URLs and verdict counts only; it does not read skill source code or verify licences, safety or behaviour.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_atlas_metadata_audit.py`
- مرجع: `.claude/skills/kosif-superpowers/references/cloud-browser-and-app-capability-matrix.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-metadata-audit --evidence <ملف>`.

### `browser-scout` — مستكشف المواقع بالمتصفح / Browser scout site survey

| الحقل | القيمة |
|---|---|
| المسار | `scripts/browser_scout.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `app-feature-transfer` |

**ما تفعله:** يعرض 26 هدفًا منتقًى عبر HTTPS ويفحص سجلاتها، منها تطبيقات رسم على الويب وأدوات ثلاثية الأبعاد ورسوم متحركة ومنتجات ذكاء اصطناعي ومتصفحات، من الملف data/integration-target-atlas.json. ويستطيع أن يلتقط، دون أي تفاعل، صورةً لإطار العرض في هدف واحد داخل سياق Playwright جديد بلا واجهة، يحجب الطلبات إلى النطاقات الأخرى والتنزيلات وعمّال الخدمة (service workers) ولا يحفظ ملفات تعريف الارتباط.

**What it does:** Lists and inspects 26 curated HTTPS targets (web drawing apps, 3D and animation tools, AI and browser products) from data/integration-target-atlas.json. It can take a read-only viewport screenshot of one target in a fresh headless Playwright context that blocks off-host requests, downloads, service workers and saved cookies.

#### متى تُستدعى

- «صوّر لي واجهة Photopea عشان أدرس ميزاتها»
- «Which web drawing apps are in the integration target atlas?»
- «Take a read-only screenshot of the AutoDraw homepage»
- «وش المواقع المعتمدة لدراسة ميزات تطبيقات الرسم؟»
- «Show me the approach recorded for the canva-draw target»

#### الأوامر

- **doctor**: Reports the target count, whether Playwright is installed, the supported engines and the flags for local prototype, no cloud browser and no auth. Uses no network.
  - `python3 scripts/browser_scout.py doctor`
- **list**: Prints every target's id, category and feature as JSON.
  - `python3 scripts/browser_scout.py list`
- **inspect**: Prints one target's full record: URL, category, feature and the recommended lawful approach.
  - `python3 scripts/browser_scout.py inspect autodraw`
- **capture**: Opens the target in a fresh headless context with a 20 s timeout and saves one viewport PNG. The output must be an unused .png in an existing folder. Prints status, title, sha256 and bytes.
  - `python3 scripts/browser_scout.py capture autodraw --output ./out/autodraw.png --engine chromium`

#### المتطلبات والأمان

- network: true
- optional: bin:chromium, pip:playwright
- الأمان: network
- الموافقة: capture visits the target website and needs 'pip install playwright' plus a separately installed browser engine ('playwright install chromium'). Ask before installing either and before visiting the site.
- الحدود: It captures only a viewport screenshot of one of 26 curated HTTPS targets (no arbitrary URLs, logins, clicks or crawling), and because off-host requests are blocked, pages that load assets from CDNs may render incomplete.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_browser_scout.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/cloud-browser-and-app-capability-matrix.md`
- مرجع: `.claude/skills/kosif-superpowers/references/native-primitives-and-research-v2.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:browser-scout --evidence <ملف>`.

### `creative-external-search` — بحث المصادر الإبداعية دون اتصال / Creative sources offline search

| الحقل | القيمة |
|---|---|
| المسار | `scripts/creative_external_search.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `photo-video-footage` |

**ما تفعله:** يبحث بالكلمات المفتاحية في فهرس محلي يضم 1,000 مستودع عام على GitHub (تحرير الفيديو ومعالجته، والموشن جرافيك، وأدوات الصور، والرؤية الحاسوبية، والبرمجة الإبداعية) و1,000 موقع إبداعي مستخرَج من قوائم awesome منتقاة (أدوات التصميم، والموشن جرافيك، وأدوات الصور بالذكاء الاصطناعي، والبرمجة الإبداعية، وإنتاج الفيديو)، ويطبع نتائج JSON مرتبة موسومة بأنها بيانات وصفية فقط.

**What it does:** Keyword-searches an offline index of 1,000 public GitHub repositories (video editing and processing, motion graphics, image and photo tools, computer vision, creative coding) and 1,000 creative websites extracted from curated awesome lists (design tools, motion graphics, AI image tools, creative coding, video production), and prints ranked JSON matches labelled metadata-only.

#### متى تُستدعى

- «دورلي على أدوات مفتوحة المصدر للمونتاج وإزالة الخلفية»
- «find open-source repos for kinetic typography»
- «أبغى مواقع تساعدني في تصحيح الألوان والتلوين»
- «list creative websites for motion graphics inspiration»
- «how many creative repos and sites are in the discovery index?»

#### الأوامر

- **search**: Scores repos and/or sites by query terms found in the name (x6) and in description/category/topic (x2), plus a star bonus of at most 1.2; Arabic words such as مونتاج/صور/تلوين and topic names such as image-editing are expanded to English terms; --top is clamped to 1–100.
  - `python3 scripts/creative_external_search.py search "kinetic typography" --kind repo --top 5`
- **stats**: Prints repo and website counts, repo category counts, and flags stating no REA analysis or implemented features.
  - `python3 scripts/creative_external_search.py stats`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Plain substring keyword scoring over a frozen offline index of public metadata and curated links; no entry was code-analysed, licence-verified, checked for availability or tested, and nothing is fetched live.

#### الاختبارات والأدلة

- `tests/test_creative_external_research.py`
- مرجع: `.claude/skills/kosif-superpowers/references/REA_CREATIVE_DISCOVERY_2000_20261019.md`
- مرجع: `docs/REA_CREATIVE_DISCOVERY_2000_20261019.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:creative-external-search --evidence <ملف>`.

### `fetch-reference` — جلب المرجع المسموح وقياسه / Permitted reference fetch and measure

| الحقل | القيمة |
|---|---|
| المسار | `scripts/fetch_reference.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `video-download`, `photo-video-footage`, `transitions-cuts`, `color-palette-grading` |

**ما تفعله:** يكتشف روابط الوسائط في صفحة ويب عامة (وسوم video وsource، ووسوم Open Graph وTwitter، وJSON-LD، ونصوص السكربت)، أو يأخذ رابط ملف مباشرًا أو قائمة HLS غير مشفّرة. ثم ينزّل الوسيط ضمن حدّ أقصى للحجم إلى ذاكرة مؤقتة مستثناة من git، ويقيسه بأداة ffmpeg: خصائص الملف، ولوحة إطارات، والقطعات المشهدية، والألوان الغالبة، مع تقرير REPORT.md ثنائي اللغة يُستخدم في STYLE.md.

**What it does:** Discovers media URLs on a public web page (video and source tags, Open Graph and Twitter tags, JSON-LD, script text) or takes a direct file or an unencrypted HLS playlist. It downloads the media within a size cap into a git-ignored cache and measures it with ffmpeg (probe, contact sheet, scene cuts and dominant palette), plus a bilingual REPORT.md for STYLE.md.

#### متى تُستدعى

- «هات الفيديو المرجعي من الرابط ده وقيس القطعات والألوان»
- «شوف الصفحة دي فيها روابط فيديو إيه»
- «حمّل المرجع من رابط m3u8 وحلّل مدته وأبعاده»
- «Fetch this reference video and give me a contact sheet, cuts and palette»
- «List the media URLs on this page before downloading»

#### الأوامر

- **list**: Fetches the page and lists the discovered media URLs (direct first, then HLS, then untyped) without downloading media. The list goes to stderr and, with --json, also to stdout as a JSON array. A direct media or .m3u8 URL is echoed back without any network access.
  - `python3 scripts/fetch_reference.py https://example.com/page --list --json`
- **fetch-and-analyse**: Downloads (cap --max-mb, default 400), remuxes to reference.mp4 and writes probe.json, contact.png, cuts.json, palette.json and REPORT.md. Prints the output directory.
  - `python3 scripts/fetch_reference.py https://example.com/clip.mp4 --out ./out/ref --frames 8 --scene 0.3`
- **pick**: Fetches the Nth media URL found on a page (default 1) and prints a JSON summary (probe, cuts_s, colors, files).
  - `python3 scripts/fetch_reference.py https://example.com/page --pick 2 --out ./out/ref --json`
- **hls**: Takes the highest-bandwidth variant (plus a separate audio rendition if present), fetches its segments one by one within the size cap, and refuses EXT-X-KEY encrypted streams.
  - `python3 scripts/fetch_reference.py https://example.com/stream/master.m3u8 --out ./out/ref --max-mb 200`
- **download-only**: Downloads without the ffmpeg measurements. The same happens automatically when ffmpeg or ffprobe is missing.
  - `python3 scripts/fetch_reference.py https://example.com/clip.mp4 --out ./out/ref --no-analyse`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- network: true
- الأمان: network
- الموافقة: Downloads third-party media: confirm the user has the right to analyse it. The output is working material in a git-ignored cache and must never be committed, rehosted or cut into the deliverable.
- الحدود: It cannot reach media behind logins, JavaScript-only players, DRM or encrypted HLS, and it measures only technical facts (duration, fps, size, cuts, palette, contact sheet), not easing, camera motion or typography.

#### الاختبارات والأدلة

- `tests/test_reference_fetch_security.py`
- `tests/test_superpowers_catalog.py`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-inspection.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capabilities.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:fetch-reference --evidence <ملف>`.

### `fetch-video` — تنزيل الفيديو من الروابط للمونتاج / Video link downloader for montage

| الحقل | القيمة |
|---|---|
| المسار | `scripts/fetch_video.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-elsewhere` |
| العائلات | `video-download`, `photo-video-footage`, `formats-platforms` |

**ما تفعله:** غلاف لأداة yt-dlp ينزّل رابطًا أو عدة روابط فيديو أو صوت لاستخدامها في المونتاج، مع سلسلة بدائل للصيغ، ومحاكاة متصفح اختيارية، وملف كوكيز من المستخدم، وحدّ أقصى للجودة. ويمكنه إنشاء نسخة ‎.safe.mp4‎ بترميز H.264/AAC تقبلها برامج التحرير، ويكتب ملف manifest.json فيه الملف والمدة والأبعاد ومعدل الإطارات والترميز والعنوان والناشر والترخيص إن كشفه الموقع.

**What it does:** Wraps yt-dlp to download one or many video or audio links for editing, with a format fallback chain, optional browser impersonation, a user cookies file and a quality cap. It can add an edit-safe H.264/AAC .safe.mp4 copy and writes a manifest.json with the file, duration, dimensions, frame rate, codecs, title, uploader and any license the site exposes.

#### متى تُستدعى

- «نزّل الفيديوهات دي من الروابط عشان المونتاج»
- «حمّل لي الصوت بس من هالرابط»
- «Download these video links at 1080p with an edit-safe MP4 copy»
- «Batch-download the URLs in links.txt into clips/»
- «Check whether yt-dlp and ffmpeg are ready for downloading»

#### الأوامر

- **doctor**: Reports the yt-dlp version, ffmpeg presence and impersonation support (runs yt-dlp locally; no download). Exits 1 if yt-dlp is missing.
  - `python3 scripts/fetch_video.py --doctor`
- **download**: Downloads each URL (requested format, then a fallback format, then an impersonation retry if available), probes it, optionally writes <name>.safe.mp4, and writes ./out/clips/manifest.json.
  - `python3 scripts/fetch_video.py https://example.com/video -o ./out/clips --quality 1080 --safe`
- **batch**: Reads one URL per line (blank lines and lines starting with # are skipped) and downloads all of them. Non-HTTP(S) entries are skipped with a warning.
  - `python3 scripts/fetch_video.py --urls ./links.txt -o ./out/clips`
- **audio**: Extracts the best audio track as m4a (--safe is ignored).
  - `python3 scripts/fetch_video.py https://example.com/video --quality audio -o ./out/audio`
- **cookies**: Passes a Netscape cookies.txt exported from the user's own browser, for private or age-gated posts the user can access.
  - `python3 scripts/fetch_video.py https://example.com/video --cookies ./cookies.txt -o ./out/clips`
- **update**: Runs pip install --upgrade yt-dlp curl_cffi (network plus package install).
  - `python3 scripts/fetch_video.py --update`

#### المتطلبات والأمان

- binaries: ffmpeg
- network: true
- optional: bin:ffprobe, bin:node, bin:yt-dlp, pip:curl_cffi
- python: yt-dlp
- الأمان: network
- الموافقة: It downloads third-party media, so confirm the user has the right to use it. --cookies uses the user's own session (never store, print or commit it). --update pip-installs yt-dlp and curl_cffi.
- الحدود: It is only a yt-dlp wrapper: it does not bypass DRM or paywalls, does not verify licenses, and many platforms (YouTube 403, Vimeo login, Wikimedia 403) failed from cloud hosts.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/video-download.md`
- مرجع: `.claude/skills/kosif-superpowers/references/stock-media-100.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:fetch-video --evidence <ملف>`.

### `github-top-repos` — متابعة أشهر 1000 مستودع / GitHub Top-1000 Tracker

| الحقل | القيمة |
|---|---|
| المسار | `scripts/github_top_repos.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `self-discovery` |

**ما تفعله:** يحفظ مراجعة أشهر 1000 مستودع عام على GitHub: لقطة حقائق (الترتيب والنجوم واللغة والترخيص والوصف، مدموجة من فهرس gitstar-ranking وسجلات deps.dev لقائمة مكملة لما يفوته)، وتصنيف آلي حسب الموضوع والترخيص، ومراجعة يدوية للاستبعادات والنقل. build يكتب data/github_top1000.json والجدول references/github-top-1000.md بقرار لكل مستودع (نُقل، قابل للتعدين، مرجع، لا يُنقل) ومعرّفات القدرات أو الأدوات التي تحمل طرقه؛ find وshow للبحث؛ refresh يجلب لقطة جديدة إلى ملف منفصل للمراجعة.

**What it does:** Keeps the review of the 1,000 most-starred public GitHub repositories: a facts snapshot (rank, stars, language, licence id, description, merged from the gitstar-ranking index and deps.dev records for a supplement list it misses), an automatic topic and licence classification, and a hand review of exclusions and transfers. build writes data/github_top1000.json and the table references/github-top-1000.md with a decision per repository (transferred, mine, reference, skip) and the power or tool ids that carry its methods; find and show search it; refresh fetches a new snapshot to a separate file for review.

#### متى تُستدعى

- «وريني أشهر مستودعات جيت هاب اللي ليها علاقة بالموشن»
- «هل راجعت مستودع langchain ونقلت منه إيه؟»
- «which top GitHub repos about agents are still unmined?»
- «show the licence and decision for stanfordnlp/dspy»

#### الأوامر

- **build**: Writes data/github_top1000.json and references/github-top-1000.md; --check reports drift only
  - `python3 scripts/github_top_repos.py build`
- **stats**: Counts by decision, topic and licence class; --json
  - `python3 scripts/github_top_repos.py stats`
- **find**: Repositories whose name, description, topic or decision match every word
  - `python3 scripts/github_top_repos.py find motion`
- **show**: One repository's full record
  - `python3 scripts/github_top_repos.py show stanfordnlp/dspy`
- **refresh**: Network: fetches a new snapshot to --out (refuses to overwrite the committed one)
  - `python3 scripts/github_top_repos.py refresh --out /tmp/top1000-new.json`
- **--self-test**: Runs the built-in checks on a small fixture
  - `python3 scripts/github_top_repos.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: refresh reads two public websites (gitstar-ranking.com, api.deps.dev); nothing is sent but repository names.
- الحدود: The top 1,000 is cut from a merged pool, not a census of GitHub: a repository neither source lists is missing; the topic rules are keyword based and corrected by hand where noticed; licence ids are what GitHub detects ('non-standard' means read the licence yourself).

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_github_top_repos.py`
- مرجع: `.claude/skills/kosif-superpowers/references/github-top-1000.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:github-top-repos --evidence <ملف>`.

### `media-sources` — بوابة الوسائط المرخّصة / Licensed stock media gateway

| الحقل | القيمة |
|---|---|
| المسار | `scripts/media_sources.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `video-download`, `photo-video-footage`, `media-image-audio` |

**ما تفعله:** يعرض فهرسًا ثابتًا من 100 موقع للوسائط الجاهزة والمجموعات المفتوحة والخامات ويبحث فيه، ويطبع المتطلبات القانونية لأي رابط. ولا ينزّل أي ملف عبر fetch_video.py إلا بعد تقديم إثبات صريح لحقوق ذلك الملف بعينه، ويسجّل كل تنزيل مع بصمته SHA-256 وحقوقه في ملف asset_rights.jsonl.

**What it does:** Lists and searches a fixed catalog of 100 stock, open-collection and texture websites and prints the legal prerequisites for a URL. It downloads a single asset through fetch_video.py only after explicit per-asset rights evidence is supplied, and records each download with its SHA-256 and rights in asset_rights.jsonl.

#### متى تُستدعى

- «فين ألاقي لقطات ستوك مجانية للمونتاج؟»
- «ابحث في مواقع الصور والفيديو المرخّصة عن pexels»
- «أبي أنزّل مقطع من Pixabay وأسجّل ترخيصه»
- «Find free stock video sites for B-roll»
- «Download this licensed clip and record its rights and SHA-256»

#### الأوامر

- **list**: Prints all 100 catalog sites (id, name, type, URL). Offline.
  - `python3 scripts/media_sources.py list`
- **search**: Filters by an optional term (matched against name, domain and license hint) and --type (video_image, image, open_collections, graphics_texture). Exits 1 when nothing matches. Offline.
  - `python3 scripts/media_sources.py search pexels --type video_image`
- **plan**: Prints JSON with the matched catalog entry (domain, license_url, license_hint, policy) or null, the requirement, the accepted --rights values and restrictions. Offline.
  - `python3 scripts/media_sources.py plan https://www.pexels.com/video/123/`
- **download-dry-run**: Validates the rights fields and prints the fetch_video.py command it would run, with no network, download or folder creation.
  - `python3 scripts/media_sources.py download https://www.pexels.com/video/123/ --rights stock-license --evidence-url https://www.pexels.com/license/ --credit "Pexels" -o ./out/media --dry-run`
- **download**: Runs fetch_video.py (default --quality 1080 --safe), checks that the file arrived via its manifest.json, and appends a record (sha256, rights, evidence, creator, credit) to ./out/media/asset_rights.jsonl.
  - `python3 scripts/media_sources.py download https://example.org/my-video.mp4 --rights owned -o ./out/media`

#### المتطلبات والأمان

- network: true
- optional: bin:ffmpeg, pip:curl_cffi, pip:yt-dlp
- الأمان: network
- الموافقة: download fetches media through fetch_video.py/yt-dlp. The user must assert per-asset rights with evidence; a site being in the catalog is never a license.
- الحدود: The rights check only confirms that evidence fields were supplied in the right shape; it does not open or verify the license page, grants no license, and real downloads need yt-dlp, which is missing here.

#### الاختبارات والأدلة

- `tests/test_media_sources_gateway.py`
- مرجع: `.claude/skills/kosif-superpowers/references/stock-media-100.md`
- مرجع: `.claude/skills/kosif-superpowers/references/video-download.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:media-sources --evidence <ملف>`.

### `rea-creative-research-atlas` — باني فهرس البحث الإبداعي / Creative research catalog builder

| الحقل | القيمة |
|---|---|
| المسار | `scripts/rea_creative_research_atlas.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-elsewhere` |
| العائلات | `web-research`, `software-investigation` |

**ما تفعله:** يبني فهارس الاكتشاف الإبداعي باستعلام GitHub عبر أداة gh: بحث المستودعات حسب الموضوع، واستخراج روابط المواقع من ملفات README لقوائم awesome منتقاة، وجرد مستودعات المالك وبيانات أشجارها في git. ويطبع ملخصًا بصيغة JSON في كل تشغيل، والأمر report وحده يعمل دون اتصال فيكتفي بعدّ الفهارس الموجودة.

**What it does:** Builds the creative discovery catalogs by querying GitHub through the gh CLI: topic searches for repos, outbound links extracted from curated awesome-list READMEs for sites, and the owner's repo inventory and git-tree metadata. Each run prints a JSON summary; only `report` works offline, counting the existing catalogs.

#### متى تُستدعى

- «حدّث فهرس المستودعات الإبداعية من GitHub»
- «rebuild the 1,000 creative websites list from the awesome lists»
- «show how many creative repos and sites are cataloged»
- «اعمل جرد لمستودعاتي على GitHub واحفظه في مجلد خاص»

#### الأوامر

- **report**: Offline: counts cataloged repos and sites and how many were REA-inspected (currently 1,000 / 1,000 and 0 / 0).
  - `python3 scripts/rea_creative_research_atlas.py report`
- **repos**: Runs up to 21 GitHub topic searches via gh (up to --pages pages of 100 each, ~2.1 s sleeps), stops at --limit unique public non-archived repos, and overwrites data/rea-creative-research/public_repos.json and repository_discovery_errors.json. When discovery errors would shrink the catalog it writes nothing and exits 1 unless --force is given.
  - `python3 scripts/rea_creative_research_atlas.py repos --limit 1000 --pages 2`
- **sites**: Fetches up to 15 curated awesome-list READMEs via gh until --limit unique hosts are found (the current catalog came from the first 9), keeps outbound links near creative keywords (dropping GitHub, social, Wikipedia, badge/CI hosts, image files and licence/donate/privacy links) and overwrites creative_websites.json and website_discovery_errors.json. When discovery errors would shrink the catalog it writes nothing and exits 1 unless --force is given.
  - `python3 scripts/rea_creative_research_atlas.py sites --limit 1000`
- **own**: Lists up to 100 of the authenticated user's own repos (private ones included) plus up to 100 public repos of the hard-coded elkosif0-cmd account, and writes owner_repositories_PRIVATE_LOCAL.json into the private folder (created if missing).
  - `python3 scripts/rea_creative_research_atlas.py own --private-output ~/kosif-private/`
- **trees**: Needs the inventory written by own. For each listed repo it fetches metadata and the recursive git tree via gh and writes extension counts and media-related path examples to owner_tree_inspection_PRIVATE_LOCAL.json (rewritten after each repo).
  - `python3 scripts/rea_creative_research_atlas.py trees --private-output ~/kosif-private/`

#### المتطلبات والأمان

- binaries: gh
- network: true
- الأمان: network
- الموافقة: Contacts GitHub through the user's authenticated gh CLI. repos and sites overwrite tracked catalog files in data/rea-creative-research/ (no backup; review the git diff), but refuse to shrink a catalog after discovery errors unless --force is given. own and trees read the user's private repository metadata, and --private-output must be outside every git repository (the script refuses otherwise).
- الحدود: Collects GitHub search metadata and links scraped from awesome-list READMEs only; despite its name it does not run REA, analyse code, or verify licences or site availability, and only `report` works offline.

#### الاختبارات والأدلة

- `tests/test_creative_external_research.py`
- مرجع: `.claude/skills/kosif-superpowers/references/REA_CREATIVE_DISCOVERY_2000_20261019.md`
- مرجع: `docs/REA_CREATIVE_DISCOVERY_2000_20261019.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:rea-creative-research-atlas --evidence <ملف>`.

### `rebalance-creative-repos` — إعادة موازنة فهرس المستودعات الإبداعية / Rebalance creative repo catalog

| الحقل | القيمة |
|---|---|
| المسار | `scripts/rebalance_creative_repos.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-elsewhere` |
| العائلات | `web-research`, `photo-video-footage` |

**ما تفعله:** ينفّذ ثمانية استعلامات بحث إضافية حسب الموضوع على GitHub عبر أداة gh، ويدمج نتائجها في فهرس المستودعات الإبداعية. ثم يستبعد الصفوف التي تبدو ترويجًا لنماذج غير موثّقة، ويعيد كتابة الملف data/rea-creative-research/public_repos.json في 1,000 صف وفق حصص ثابتة لكل فئة.

**What it does:** Runs eight extra GitHub topic searches via gh and merges the results into the creative repo catalog. It drops rows that look like unverified-model marketing, then rewrites data/rea-creative-research/public_repos.json as 1,000 rows under fixed per-category quotas.

#### متى تُستدعى

- «الفهرس فيه فيديو كتير وصور قليل، وازنه»
- «rebalance the creative repo index so image tools are represented»
- «refresh the image-editing repos in the discovery catalog»
- «زوّد مستودعات تحرير الصور في فهرس الاكتشاف»

#### الأوامر

- **run**: Merges the existing catalog with 8 GitHub topic searches, filters out 'fable/opus/claude 5.5' marketing rows, applies the quotas (video-film 380, motion-vfx 260, image-photo 320, computer-vision-creative 40, speech-typography 40), fills up to 1,000 rows by stars and cuts anything beyond 1,000. It overwrites public_repos.json and rebalance_errors.json, and writes nothing when every GitHub query fails. --help (or no argument) only prints usage.
  - `python3 scripts/rebalance_creative_repos.py run`

#### المتطلبات والأمان

- binaries: gh
- network: true
- الأمان: network
- الموافقة: Contacts GitHub through the user's authenticated gh CLI and overwrites the tracked data/rea-creative-research/public_repos.json and rebalance_errors.json. Run it only when the user wants the catalog regenerated: there is no dry-run or backup (review the git diff).
- الحدود: Rewrites the catalog from GitHub search metadata using fixed quotas. It has no dry-run, no backup and no tests, and it analyses no code.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/REA_CREATIVE_DISCOVERY_2000_20261019.md`
- مرجع: `docs/REA_CREATIVE_DISCOVERY_2000_20261019.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:rebalance-creative-repos --evidence <ملف>`.

### `repo-ashell-cinema` — استوديو التنزيل Cinema C للآيفون / Cinema C iPhone downloader studio

| الحقل | القيمة |
|---|---|
| المسار | `tools/a-shell/Cinema_C_V34_Studio_iPhone.sh` (جذر: repo) |
| المجال | `sources` |
| الدليل | `tested-elsewhere` |
| العائلات | `video-download`, `photo-video-footage`, `formats-platforms`, `media-image-audio` |

**ما تفعله:** تطبيق تفاعلي مكتوب بلغة sh يعمل في a-Shell على الآيفون. ينزّل الفيديو أو الصوت عبر yt-dlp (رابط مفرد، أو دفعة روابط، أو جزء من فيديو، أو مع الترجمة، أو من صفحات فيسبوك بأفضل جهد ممكن)، وينشئ نسخ MP4 بترميز H.264/AAC متوافقة مع تطبيق الصور. ويوفّر استوديو ffmpeg يعمل دون اتصال (قص، وضغط إلى 16 أو 25 أو 50 ميغابايت، ومقاطع ريلز 9:16 بخلفية مموّهة، وGIF، وصورة غلاف، وضبط الجهارة على ‎-14 LUFS، وحذف فترات الصمت، وكتم الصوت، واستخراج الصوت وحده)، ومعملًا صوتيًا لفصل الصوت البشري عن الموسيقى.

**What it does:** An interactive POSIX-sh app for a-Shell on iPhone. It downloads video or audio with yt-dlp (single links, batches, part of a video, subtitles, best-effort Facebook profiles), makes Photos-safe H.264/AAC MP4 copies, and offers an offline ffmpeg Studio (trim, compress to 16/25/50 MB, 9:16 reels with blurred fill, GIF, cover JPG, -14 LUFS loudness, cut pauses, mute, audio only) and an Audio Lab for separating voice and music.

#### متى تُستدعى

- «نزّل الفيديو ده على الآيفون من a-Shell»
- «أبي أحمّل ريل إنستغرام وأحفظه في الصور»
- «افصل صوت المتكلم عن الموسيقى من فيديو على الجوال»
- «Download a TikTok on my iPhone with a-Shell and save it to Photos»
- «Trim and compress a downloaded video to 16 MB on iPhone»
- «Make a 9:16 reel with a blurred background from a file on my iPhone»

#### الأوامر

- **download (interactive)**: Takes a URL or a whole share text (an empty Enter uses the clipboard), then shows a menu: best, 2160p to 480p, fast MP4, M4A or MP3, exact site formats (10), Audio Lab (11), part start-end (12), with subtitles (13) and Studio (14). Saves to Photos SAFE or Files and offers a yt-dlp update and one retry when a download fails.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh "https://www.youtube.com/watch?v=VIDEO_ID"`
- **--photos/--files/-N/--output**: Presets the destination (photos or files), sets 1-16 parallel connections (default 8 or CINEMA_CONNECTIONS) and chooses the download folder.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --files -N 4 --output ./downloads "https://www.youtube.com/watch?v=VIDEO_ID"`
- **--batch**: Downloads many links in one go and saves the failed ones for a retry. Without a file it reads pasted links until an empty line.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --batch ./links.txt`
- **--studio**: Opens the offline ffmpeg Studio menu on a local file (or a file picked from Cinema_Downloads): fast or exact trim, compress to 16/25/50 MB or a custom size, 9:16 reels, GIF up to 15 MB, cover JPG, two-pass -14 LUFS, cut pauses, mute, audio only and Audio Lab. Results go to Cinema_Downloads/Studio.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --studio ./in.mp4`
- **--safe**: Builds a Photos-safe H.264/AAC yuv420p +faststart MP4 from a file already downloaded. It remuxes losslessly when the video is already H.264 or HEVC, and otherwise re-encodes with the first encoder that works.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --safe ./in.mp4`
- **--lab**: Opens the Audio Lab on a local file: voice only, music only, both, video with the music or the voice muted, AI STEMS (online Demucs on Replicate) or the original audio. Voice isolation may download the arnndn model once.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --lab ./in.mp4`
- **--doctor**: Reports yt-dlp (and its impersonation targets, checked locally), the clipboard and ffmpeg, lists the encoders present, runs a 1-second synthetic encode test for each video encoder present and lists the Studio filters. It writes only to ~/Documents/.cinema.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --doctor`
- **--lab-doctor**: Checks the Audio Lab ffmpeg filters, the Replicate token and curl. If the arnndn voice model is missing, it downloads it from GitHub with curl.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --lab-doctor`
- **--update**: Runs pip install --upgrade yt-dlp (or python3 -m pip).
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --update`
- **--setup-ai**: Prompts for a Replicate API token and saves it to ~/Documents/replicate_token.txt (chmod 600). An empty answer saves nothing.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --setup-ai`
- **--install**: Copies the script to ~/Documents/bin/c and makes it executable, so typing 'c' runs it.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --install`
- **--history**: Prints the last 20 lines of Cinema_Downloads/history.txt, or 'No downloads recorded yet.'
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --history`
- **--setup-facebook-cookies**: Prints instructions for providing a Netscape-format cookies file for Facebook profiles.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --setup-facebook-cookies`
- **--cookies**: Passes the user's Netscape cookies file to yt-dlp for the download. It exits 1 at parse time if the file is missing or lacks the Netscape header. Without this flag, Facebook profile URLs use ~/Documents/facebook_cookies.txt automatically when it is valid. Profile enumeration is best-effort.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --cookies ./facebook_cookies.txt "https://www.facebook.com/profile.php?id=NUMERIC_ID"`
- **--fb-doctor/--fb-debug**: --fb-doctor diagnoses Facebook profile access (impersonation targets, login redirects). --fb-debug runs the normal flow with verbose logs. Both need yt-dlp.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --fb-debug "https://www.facebook.com/profile.php?id=NUMERIC_ID"`
- **--version/--help**: Prints the version (Cinema C 34.0-Studio-iPhone) or the usage text.
  - `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh --help`

#### المتطلبات والأمان

- binaries: ffmpeg, sh, yt-dlp
- network: true
- optional: bin:curl, bin:open, bin:pbpaste, bin:pip
- الأمان: network
- الموافقة: Downloads third-party media, so confirm the user owns it or has the rights first. It uses the user's cookies file, which is a login credential. --update runs pip install --upgrade yt-dlp. AI STEMS uploads the audio to api.replicate.com with the user's paid token. The Audio Lab and --lab-doctor may download an arnndn model from GitHub. --install copies the script to ~/Documents/bin/c, and --setup-ai stores a secret token in ~/Documents.
- الحدود: It is built for a-Shell on iPhone and has never been run on a real iPhone (only container simulations are recorded); most flows are interactive menus rather than scriptable flags, and Facebook profile enumeration is best-effort.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/video-download.md`
- مرجع: `.claude/skills/kosif-superpowers/references/stock-media-100.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-ashell-cinema --evidence <ملف>`.

### `source-scout` — مستكشف مصادر المجتمع / Community source scout

| الحقل | القيمة |
|---|---|
| المسار | `scripts/source_scout.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `app-feature-transfer`, `security-safety` |

**ما تفعله:** يبحث في سجلٍّ محلي منسَّق يضم 31 مستودعًا على GitHub جرت مراجعتها (مع لقطة مؤرَّخة لأعلى عشرة مستودعات Python من حيث عدد النجوم)، ويعيد بصيغة JSON مصادر مرجعية مرتبة مع ترخيص كلٍّ منها وتحذيراته وضوابط إعادة استخدام الكود.

**What it does:** Searches a curated offline registry of 31 reviewed GitHub repositories (plus a dated top-10 Python star snapshot) and returns ranked reference sources with licence, caution and code-reuse gates as JSON.

#### متى تُستدعى

- «عايز مستودع مرجعي أتعلم منه إزاي أعمل محرر موشن بتايملاين»
- «find a reference repo for persistent agent memory before we build it»
- «وش أفضل مصادر GitHub لتصميم الأنظمة والتوسع؟»
- «can I reuse code from GraphiteEditor/Graphite? check the licence gate»
- «اعرض أعلى عشرة مستودعات بايثون حسب النجوم»

#### الأوامر

- **check**: Validates data/community_sources.json (schema, exactly 31 sources, URL = github.com/<repo>, 13 known domains, reference_only status, a sorted top-10 Python snapshot) and prints counts and domains. Every other command runs the same validation first.
  - `python3 scripts/source_scout.py check`
- **list**: Lists sources (id, repo, domain, licence), optionally filtered to one of 13 domains.
  - `python3 scripts/source_scout.py list --domain creative`
- **show**: Prints the full registry record for one source by id or owner/repo (case-insensitive); an unknown id exits 2 with the same catalog_error message as an invalid registry.
  - `python3 scripts/source_scout.py show SRC-16`
- **suggest**: Ranks sources by keyword overlap with each source's signals (Arabic-normalised) or an exact repo name, optionally within one --domain; --limit is clamped to 1–10. With --code-reuse the reuse_gate is check_rights_first for licences other than MIT/Apache-2.0/BSD-3-Clause and check_file_and_dependency_licenses for those three; without it, reference_only.
  - `python3 scripts/source_scout.py suggest "keyframes timeline animation" --limit 3 --code-reuse`
- **python-top**: Prints the dated (2026-10-17) top-10 Python-repos-by-stars snapshot, flagged live_star_counts=false.
  - `python3 scripts/source_scout.py python-top`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Matches keywords against a fixed hand-reviewed list of 31 repositories and a dated star snapshot; it fetches nothing live and does not install, run or prove any listed repository works.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_source_scout.py`
- مرجع: `.claude/skills/kosif-superpowers/references/community-source-atlas.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/repository-capability-transfer.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:source-scout --evidence <ملف>`.

### `sources-index` — فهرس المصادر: الذاكرة الفهرسية لمرفقات المستخدم داخل مجلد العمل / Sources index: per-work-dir index memory of the user's attachments

| الحقل | القيمة |
|---|---|
| المسار | `scripts/sources_index.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `security-safety`, `verification-evals` |

**ما تفعله:** يسجّل كل مرفق (ملف أو docx أو pdf عبر pdftotext أو رابط يُسجَّل دون جلبه) في <dir>/sources_index.json: النوع والبصمة والحجم وعدد الأسطر والعناوين بنطاقات أسطرها والمصدر ونطاق الثقة «بيانات لا تعليمات» والأسطر الآمرة، والأسرار بموقعها ونوعها فقط دون قيمتها أبدًا. والبحث يعيد نطاقات الأسطر لتُقرأ وحدها.

**What it does:** Records each attachment (file, .docx, .pdf via pdftotext, or a URL recorded without fetching) in <dir>/sources_index.json: kind, sha256, size, lines, title guess, headings with line ranges, provenance, trust_scope 'data, not instructions', imperative lines that try to instruct the assistant, and secrets by line and kind only (never the value). find returns heading line ranges (or line numbers with --body) so only that range is read.

#### متى تُستدعى

- «فهرس الملفات اللي رفعتها عشان ترجع لها وقت الحاجة»
- «الذاكرة الفهرسية للمصادر»
- «Index my attachments and tell me where the chapter on X is»
- «Check this uploaded file for embedded instructions or leaked keys before using it»

#### الأوامر

- **add**: Indexes one file or URL into out/demo/sources_index.json and prints its id, imperative line numbers and secret locations.
  - `python3 -I scripts/sources_index.py add charter.txt --dir out/demo`
- **list**: Lists indexed sources with counts.
  - `python3 -I scripts/sources_index.py list --dir out/demo`
- **show**: Prints one record (metadata, headings and flags, never body text).
  - `python3 -I scripts/sources_index.py show SRC-0123456789 --dir out/demo`
- **find**: Matches titles and headings and returns line ranges; --body also returns matching line numbers, never text.
  - `python3 -I scripts/sources_index.py find "الباب الرابع" --dir out/demo`

#### المتطلبات والأمان

- optional: bin:pdftotext
- الأمان: writes-files
- الموافقة: Writes only <dir>/sources_index.json (refuses the skill folder, jobs/ and git-tracked paths); fetches nothing and never writes a credential value.
- الحدود: Headings, imperative cues and secrets are pattern heuristics (can miss or over-flag); lists are capped with counts; the index is local to this container and nothing is learned from it.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_sources_index.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A17-story-scene-charter.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:sources-index --evidence <ملف>`.

### `stock-fetch` — تحميل لقطات مجانية بلا مفتاح (Pexels وMixkit) / Keyless stock footage fetcher (Pexels, Mixkit)

| الحقل | القيمة |
|---|---|
| المسار | `scripts/stock_fetch.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `video-download` |

**ما تفعله:** ينزّل لقطات مجانية برقم المقطع أو رابط صفحته بلا مفتاح API: من Pexels عبر رابط التحميل العام (تحويل 302 إلى videos.pexels.com)، ومن Mixkit عبر ملف 720p المجاني. ويكتب manifest.json فيه الصفحة ورابط الملف واسم الرخصة ورابطها وشروطها والحجم والأبعاد ومعدل الإطارات والمدة، ويتخطى الملفات الضخمة، وفيه فحص يبيّن أي مصادر اللقطات تستجيب من الجهاز الحالي.

**What it does:** Downloads free stock clips by id or page URL without an API key: Pexels through its public download endpoint (a 302 to videos.pexels.com) and Mixkit through its free 720p file. It writes manifest.json with the page, file URL, licence name, link and terms, size, dimensions, frame rate and duration, can skip oversized files, and has a probe that reports which stock sources answer from the current machine.

#### متى تُستدعى

- «هات لقطات مجانية للحرم من Pexels من غير مفتاح»
- «مفتاح Pexels مش متاح، نزّل الفيديوهات دي بأرقامها»
- «Download these Pexels clips by id without an API key»
- «Which stock footage sites can this cloud machine reach?»

#### الأوامر

- **probe**: Prints the HTTP status of Mixkit pages and files, the Pexels search page, download endpoint and API, the Pixabay API, the Wikimedia API and Coverr from this machine.
  - `python3 scripts/stock_fetch.py probe`
- **pexels**: Resolves each id through https://www.pexels.com/download/video/<id>/ (302), downloads the file, probes it and merges the rows into ./stock/manifest.json. --dry-run only resolves and sizes.
  - `python3 scripts/stock_fetch.py pexels 35155732 https://www.pexels.com/video/people-walking-around-the-kaaba-9112700/ -o ./stock --max-mb 120`
- **mixkit**: Downloads https://assets.mixkit.co/videos/<id>/<id>-720.mp4 (the free size; 1080 and 2160 return 403) and records it in the manifest.
  - `python3 scripts/stock_fetch.py mixkit 4312 9998 -o ./stock`

#### المتطلبات والأمان

- network: true
- optional: bin:ffprobe
- الأمان: network
- الموافقة: It downloads third-party stock media; keep the manifest with the project and follow each licence (no resale of unaltered clips, no implied endorsement). Find ids with a web search restricted to pexels.com or mixkit.co; the tool does not search or log in.
- الحدود: It works only while the Pexels download endpoint keeps answering with a 302 and Mixkit keeps its 720p file public; it cannot search Pexels (search pages return 403 to scripts and new API keys were paused on 2026-10-21) and gives Mixkit clips at 720p only.

#### الاختبارات والأدلة

- `tests/test_stock_fetch.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/stock-media-100.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:stock-fetch --evidence <ملف>`.

### `stream-grabber` — ملتقط بث DASH وHLS للمونتاج / DASH/HLS stream grabber for editing

| الحقل | القيمة |
|---|---|
| المسار | `scripts/stream_grabber.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `video-download`, `photo-video-footage` |

**ما تفعله:** ملتقط بث كُتب بعد دراسة IDM 6.43: يقرأ DASH وHLS، وينزل المقاطع بالتوازي مع الاستئناف، ويختار أفضل فيديو وصوت صالحين للمونتاج، ويدمجهما بلا إعادة ترميز، ويحفظ الترجمات، ويجد روابط البث في صفحة محفوظة أو ملف HAR؛ ويرفض المحمي والمشفر والبث الحي.

**What it does:** Written after a read-only study of IDM 6.43: parses DASH (SegmentTemplate with Number or Timeline, SegmentList, SegmentBase) and HLS (master/media, byte ranges, fMP4 init), downloads segments in parallel with resume and tail probing, picks the best editable video and audio, merges losslessly (MP4, or MKV for VP8/Vorbis), saves WebVTT subtitles and finds manifests in saved pages or HAR exports; refuses encrypted, DRM, live and cookie-header requests.

#### متى تُستدعى

- «نزّل البث ده m3u8 وجهزه للمونتاج»
- «Grab this licensed DASH manifest as an MP4»
- «طلّع روابط الفيديو من الصفحة المحفوظة دي»

#### الأوامر

- **find**: Lists manifests and media links in a page, HAR export or URL.
  - `python3 scripts/stream_grabber.py find ./saved-page.html`
- **list**: Tracks with quality labels.
  - `python3 scripts/stream_grabber.py list https://example.com/master.m3u8`
- **grab**: Downloads and merges the best editable tracks plus subtitles.
  - `python3 scripts/stream_grabber.py grab https://example.com/manifest.mpd -o ./clip.mp4 --max-height 1080`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- network: true
- الأمان: network
- الموافقة: downloads from the given URL: only content the user owns or is licensed to use; encrypted, DRM and live streams are refused
- الحدود: No DRM, no live streams, no cookie headers; servers that ignore Range are read once and sliced in memory.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_stream_grabber.py`
- مرجع: `.claude/skills/kosif-superpowers/montage-pro/README.md`
- مرجع: `.claude/skills/kosif-superpowers/montage-pro/IDM_STUDY.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:stream-grabber --evidence <ملف>`.

### `superpowers` — خريطة المستودعات الخارجية / External repository tool map

| الحقل | القيمة |
|---|---|
| المسار | `scripts/superpowers.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `engines-render-pipeline` |

**ما تفعله:** يعرض المستودعات المفتوحة المصدر المسجلة في repos.json وعددها 125، ويبحث فيها ويعرض تفاصيلها، وهي موزعة على 15 قدرة مع ملاحظات الترخيص. ويفحص وجود 21 أداة محلية مثل ffmpeg وPlaywright وWhisper، ويتحقق من حداثة ملف references/repos.md أو يعيد توليده.

**What it does:** Lists, searches and shows the 125 open-source repositories in repos.json, grouped into 15 superpowers with license notes; checks whether 21 local tools such as ffmpeg, Playwright and Whisper are present; and validates or regenerates references/repos.md.

#### متى تُستدعى

- «أي مكتبة مفتوحة المصدر تنفع لمحاذاة الكلمات مع الصوت؟»
- «إيه الأدوات المتسطبة على الجهاز ده قبل ما أوعد بالرندر؟»
- «List the voice repositories in the KOSIF tool map»
- «Show the record for ggml-org/whisper.cpp with its license note»
- «Is references/repos.md up to date with repos.json?»

#### الأوامر

- **list**: Lists repositories, optionally filtered by --capability, --domain or a --license-note substring, as a table or as JSON.
  - `python3 scripts/superpowers.py list --capability voice --json`
- **search**: Searches owner/repo, name, Arabic and English summaries and KOSIF uses, invocation, capability, domain and license, requiring every word to match. Exits with code 1 when nothing matches.
  - `python3 scripts/superpowers.py search whisper --json`
- **show**: Shows one record with its URL, license note, KOSIF use, invocation, caveats and playbooks; when the repository is not found it suggests close matches and exits with code 1.
  - `python3 scripts/superpowers.py show ggml-org/whisper.cpp`
- **doctor**: Probes 21 tools on PATH, in node_modules folders, under PLAYWRIGHT_BROWSERS_PATH and by Python import spec, printing install hints for missing ones. With --strict it exits 1 if a core render tool (node, ffmpeg, ffprobe, playwright or chromium) is missing.
  - `python3 scripts/superpowers.py doctor --json --strict`
- **stats**: Counts repositories and total stars by superpower, domain and license note.
  - `python3 scripts/superpowers.py stats`
- **check**: Validates repos.json (125 entries, required fields, GitHub URLs, Arabic text, existing playbooks) and verifies that references/repos.md is up to date. Read-only, suitable for CI.
  - `python3 scripts/superpowers.py check`
- **build**: Without --check it validates repos.json and rewrites references/repos.md. With --check it only verifies the file is current (exit 1 if stale).
  - `python3 scripts/superpowers.py build --check`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: build without --check overwrites the tracked file references/repos.md. doctor prints install hints such as pip or npm commands; never run them without user approval and a license review.
- الحدود: Catalogs and links third-party repositories but never installs, fetches or tests them; doctor checks presence only, not that a tool works.

#### الاختبارات والأدلة

- `tests/test_superpowers_catalog.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capabilities.md`
- مرجع: `.claude/skills/kosif-superpowers/references/repos.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/engines-render-pipeline.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:superpowers --evidence <ملف>`.

