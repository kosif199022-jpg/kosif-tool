# أدوات المجال `sources` (24 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `atlas-audit-synthesis` — تحويل مراجعة الأطلس إلى بيان مُراجَع / Atlas audit to reviewed manifest

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_audit_synthesis.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
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

- `.claude/skills/kosif-superpowers/evals/test_atlas_audit_synthesis.py`
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
| الدليل | `tested-here` |
| العائلات | `video-download`, `photo-video-footage`, `formats-platforms` |

**ما تفعله:** غلاف لأداة yt-dlp ينزّل رابطًا أو عدة روابط فيديو أو صوت لاستخدامها في المونتاج، مع سلسلة بدائل للصيغ، ومحاكاة متصفح اختيارية، وملف كوكيز من المستخدم، وحدّ أقصى للجودة. ويمكنه إنشاء نسخة ‎.safe.mp4‎ بترميز H.264/AAC تقبلها برامج التحرير، وشيل صوت المقطع نفسه عند الاستلام (‎--strip-audio‎)، ويكتب ملف manifest.json فيه الملف والمدة والأبعاد ومعدل الإطارات والترميز والعنوان والناشر والترخيص إن كشفه الموقع. روابط Pinterest بتعدّي على المساعد المشترك scripts/_pinterest.py: طلب yt-dlp -J واحد يصنّف الـpin الأول (فيديو، صورة، GIF، يوتيوب مضمَّن، تضمين من موقع تاني، محذوف، سيرفر الفيديو رافض، محجوب) مع سبب في سطر، ومفيش تنزيل إلا للفيديو وفي فولدر مؤقت، والمقاس الحقيقي بيتقاس بـffprobe، وبيتكتب سجل نسب ‎.pin.json‎؛ و‎--classify‎ بيقول نوع كل pin بس.

**What it does:** Wraps yt-dlp to download one or many video or audio links for editing, with a format fallback chain, optional browser impersonation, a user cookies file and a quality cap. It can add an edit-safe H.264/AAC .safe.mp4 copy, can drop each clip's own audio on intake (--strip-audio), and writes a manifest.json with the file, duration, dimensions, frame rate, codecs, title, uploader and any license the site exposes. Pinterest pin links go through the shared helper scripts/_pinterest.py: one yt-dlp -J call classifies the pin first (video, image, GIF, embedded YouTube, other embed, deleted, CDN-refused, blocked) with a one-line reason, only a video pin is downloaded, in a temp folder, its real size is measured with ffprobe, and a .pin.json credit record is written; --classify only reports what each pin is.

#### متى تُستدعى

- «نزّل الفيديوهات دي من الروابط عشان المونتاج»
- «حمّل لي الصوت بس من هالرابط»
- «Download these video links at 1080p with an edit-safe MP4 copy»
- «Batch-download the URLs in links.txt into clips/»
- «Check whether yt-dlp and ffmpeg are ready for downloading»
- «نزّل فيديو الـpin ده من بنترست من غير المزيكا بتاعته»
- «Which of these Pinterest pins are videos and which are images or embedded YouTube?»

#### الأوامر

- **doctor**: Reports the yt-dlp version, ffmpeg presence and impersonation support (runs yt-dlp locally; no download). Exits 1 if yt-dlp is missing.
  - `python3 scripts/fetch_video.py --doctor`
- **download**: Downloads each URL (requested format, then a fallback format, then an impersonation retry if available; a Pinterest pin instead gets one classification and at most one download, with no retry), probes it, optionally writes <name>.safe.mp4, and writes ./out/clips/manifest.json.
  - `python3 scripts/fetch_video.py https://example.com/video -o ./out/clips --quality 1080 --safe`
- **batch**: Reads one URL per line (blank lines and lines starting with # are skipped) and downloads all of them. Non-HTTP(S) entries are skipped with a warning.
  - `python3 scripts/fetch_video.py --urls ./links.txt -o ./out/clips`
- **audio**: Extracts the best audio track as m4a (--safe is ignored).
  - `python3 scripts/fetch_video.py https://example.com/video --quality audio -o ./out/audio`
- **cookies**: Passes a Netscape cookies.txt exported from the user's own browser, for private or age-gated posts the user can access.
  - `python3 scripts/fetch_video.py https://example.com/video --cookies ./cookies.txt -o ./out/clips`
- **cookies-from-browser**: Passes --cookies-from-browser to yt-dlp so the user's own local browser login is used without exporting a cookies file.
  - `python3 scripts/fetch_video.py https://example.com/video --cookies-from-browser firefox -o ./out/clips`
- **strip-audio**: Drops each downloaded clip's own audio with ffmpeg (video stream copied, no re-encode) and records audio: stripped in the manifest; for Quran and other dignified jobs, since Pinterest video pins usually carry the creator's music. Refused with --quality audio.
  - `python3 scripts/fetch_video.py https://www.pinterest.com/pin/<id>/ -o ./out/clips --strip-audio`
- **classify**: Pinterest pins only: one yt-dlp -J call per pin (Pinterest extractor only, so an embedded YouTube video is named without contacting YouTube) prints kind, pin id and a one-line reason; nothing is downloaded or written. Exit 1 when a link is not a pin or a pin could not be classified.
  - `python3 scripts/fetch_video.py --classify https://www.pinterest.com/pin/<id>/ https://pin.it/<code>`
- **update**: Runs pip install --upgrade yt-dlp curl_cffi (network plus package install).
  - `python3 scripts/fetch_video.py --update`

#### المتطلبات والأمان

- binaries: ffmpeg
- network: true
- optional: bin:ffprobe, bin:node, bin:yt-dlp, pip:curl_cffi
- python: yt-dlp
- الأمان: network
- الموافقة: It downloads third-party media, so confirm the user has the right to use it. --cookies uses the user's own session (never store, print or commit it). --update pip-installs yt-dlp and curl_cffi.
- الحدود: It is only a yt-dlp wrapper: it does not bypass DRM or paywalls, does not verify licenses, and many platforms (YouTube 403, Vimeo login, Wikimedia 403) failed from cloud hosts. Pinterest is not a licence source: a pin is often a re-upload of unknown licence, its video is 720p at most whatever the 1080x1920 label says, and image, GIF, embedded-YouTube and deleted pins give no file (each is reported once, never retried; an embedded YouTube video is never fetched through the pin, use the YouTube link on your own computer).

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_pinterest.py`
- `.claude/skills/kosif-superpowers/evals/test_instagram_finder.py`
- `tests/test_download_deps.py`
- مرجع: `.claude/skills/kosif-superpowers/references/video-download.md`
- مرجع: `.claude/skills/kosif-superpowers/references/stock-media-100.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:fetch-video --evidence <ملف>`.

### `free-footage` — لقطات مجانية: قاعدة مواقع فيديو مفتوحة الترخيص مع بحث وتحميل وسطر نسب / Free footage: open-licence video sources with search, download and credits

| الحقل | القيمة |
|---|---|
| المسار | `scripts/free_footage.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `video-download`, `web-research` |

**ما تفعله:** قاعدة بيانات مفحوصة لـ17 موقع فيديو مجاني ومفتوح الترخيص (الترخيص ورابطه، هل لازم تكتب اسم صاحب الفيديو وصيغة السطر، الاستخدام التجاري، هل التعديل مسموح، نقاط قوة كل موقع، رابط البحث، الـAPI واسم متغير المفتاح، إزاي يتجاب رابط الملف، أكبر جودة، وهل الموقع بيرد من السيرفر)، وفيها Pinterest متعلَّم عليه إنه مش مصدر ترخيص. بيبحث في ويكيميديا كومنز وأرشيف الإنترنت (وبيعلّم على ترخيص الأغاني والأفلام المنسوخة من يوتيوب إنه مشكوك فيه) وناسا من غير مفتاح، وفي Pexels وPixabay لو مفاتيحهم موجودة في البيئة، وفي صفحات Mixkit (حتى اللقطات الجديدة اللي روابطها مشفّرة) وCoverr. كل نتيجة معاها صورة مصغّرة ورابط معاينة، والنتائج بتتجمّع في ملف واحد من غير ما تمسح القديم، وأمر preview بيعمل ورقة معاينة قبل ما تنزّل أي ملف كامل. أمر download بيحفظ اللقطة ومعاها ملف JSON فيه الترخيص وسطر النسب والحجم والبصمة ونوع الألوان، وبيحدّث ATTRIBUTION.md، وأمر probe بيقيس الوصول لكل موقع من جديد.

**What it does:** Keeps a checked database of 17 free and open-licence video sources (data/free_footage_sources.json: licence and its link, credit rule and template, commercial use, edits allowed, strengths, search URL, API and key variable, how a file URL is obtained, largest scripted size, measured reachability, with Pinterest marked not a licence source). It searches Wikimedia Commons (licence, author and attribution flag from imageinfo extmetadata), the Internet Archive (licenseurl plus the item's file list, with uploader claims on music videos, rips and YouTube re-uploads flagged suspicious) and NASA without keys, Pexels and Pixabay when PEXELS_API_KEY or PIXABAY_API_KEY is set, and the Mixkit and Coverr search pages (Mixkit's per-clip Free or Restricted notice and the sizes its clip page offers, including newer clips with hashed file links; Coverr's embedded state without premium clips). Results carry thumbnail and preview links and are merged into one results file; preview builds a contact sheet before any full download. download saves a clip with a sidecar JSON (licence, credit line, bytes, sha256, ffprobe size, pixel format and range) and rebuilds ATTRIBUTION.md; probe re-measures every source.

#### متى تُستدعى

- «اجمع لي فيديوهات مفتوحة المصدر للمونتاج عن البحر والمدينة بالليل»
- «عايز لقطات مجانية من غير حقوق لفيديو تيك توك طولي»
- «اعمل قاعدة مواقع فيها فيديوهات مفتوحة المصدر تساعدني في المونتاج»
- «ورّيني صور مصغّرة للقطات قبل ما أنزّلها عشان أشوف فيها ناس ولا كتابة»
- «Find free open-licence b-roll of a city at night for my montage»
- «Download CC0 or public-domain footage and record the licence and credit line»
- «Which free stock video sites allow commercial use and which need attribution?»
- «Make a contact sheet of the footage results so I can screen out people and text before downloading»

#### الأوامر

- **sources**: Offline: lists the sources with recorded reachability, search mode, key variable, commercial use, credit rule and licence; --id shows one full record, --find WORD, --status, --no-attribution and --commercial filter (paid stock such as Storyblocks only with --include-paid), --json prints records.
  - `python3 scripts/free_footage.py sources --searchable`
- **check**: Offline: validates data/free_footage_sources.json against the rules of schemas/free_footage_sources.schema.json (required keys, enums, unique ids and names, https links, template placeholders, key variables, Pinterest-style non-licence sources); exit 1 on any problem.
  - `python3 scripts/free_footage.py check`
- **probe**: Network: requests each source's probe URLs (files with a byte range), one per host per --delay seconds, and writes probe-<YYYYMMDD>.json with HTTP codes, the URL each probe landed on after redirects, a status per source (ok, partial, needs-key, blocked, timeout, paid, or moved when the site now answers from another domain) and whether it changed since the database was checked.
  - `python3 scripts/free_footage.py probe --out out/free-footage`
- **search**: Network: Wikimedia Commons, the Internet Archive and NASA by API, Mixkit and Coverr by page, Pexels and Pixabay only when their key variables are set (otherwise reported as skipped, with no request). ND licences are dropped by default (--allow-nd keeps them for reference); --commercial drops NC, Mixkit Restricted, suspicious Archive uploader claims, the retired CC Sampling/Sampling+/Developing Nations and other unconfirmed licences, and counts each reason apart (it reads Mixkit clip pages to decide, as --resolve does: licence, real sizes and file sizes; a plain search shows Mixkit sizes as ~thumbnail guesses); --match any\|all drops titles that share no query word; --no-people drops titles naming people; --no-ai drops AI-generated clips. Prints id, size, duration, licence and credit rule, and merges the results by id into out/free-footage/last_search.json (--replace overwrites), with thumb_url, preview_url and relevance per result. A 429 names its Retry-After; --wait-429 waits for up to 900 s and --retry-failed asks only the sources that failed last time. One failing source never stops the others; exit 3 only when every source failed.
  - `python3 scripts/free_footage.py search "night city" --orientation portrait --min-height 1280 --resolve --limit 6`
- **download**: Network: a result id from the results file or a page/file link of a supported source (a Pexels link works without a key through stock_fetch.py); any other link needs --licence and --licence-url from its page. Writes <source>-<id>.<ext>, a <file>.json sidecar (licence, credit line, bytes, sha256, ffprobe size, pixel format and range, a full-range warning for yuvj420p files) and ATTRIBUTION.md; --max-mb 300 cap and --quality / --max-height caps where sizes are listed (Mixkit, Archive, Pexels, Pixabay; the next smaller file is taken); a Mixkit Free clip comes at its largest listed size, a Restricted one at 720p, and newer Mixkit clips through the clip page's download route; --dry-run prints the size, resolution and file size (listed, or by HEAD); a Cloudflare browser check is reported and that host left alone (--retry-challenge waits once); one retry on an Archive data node's 500; refuses web pages served instead of video, ND licences and Pinterest; a failed target does not stop the others; exit 1 when any target failed.
  - `python3 scripts/free_footage.py download wikimedia:81916645 mixkit:100896 --quality 1080 --out out/free-footage/clips`
- **preview**: Network (thumbnails and small previews only): builds contact_sheet.html (and contact_sheet.jpg plus video stills with ffmpeg) and contact_sheet.json from each result's thumbnail, or a strip of --frames stills from its 360p preview file (capped at 25 MB, deleted after use), or from the clips already downloaded in a folder; --ids and --query pick results. It never fetches a full clip.
  - `python3 scripts/free_footage.py preview out/free-footage/last_search.json --frames 4`
- **credits**: Offline: rebuilds ATTRIBUTION.md (a table plus copy-ready credit lines) from the sidecars in the folder, for example after a clip was removed, and prints it.
  - `python3 scripts/free_footage.py credits out/free-footage/clips`

#### المتطلبات والأمان

- network: true
- optional: bin:ffprobe, env:PEXELS_API_KEY, env:PIXABAY_API_KEY
- الأمان: network
- الموافقة: search, preview and probe send the query and plain requests to the listed sites (preview fetches thumbnails and small preview files), and download fetches third-party clips: confirm the user wants that. Keep each sidecar and ATTRIBUTION.md with the project and follow the licence (credit where required, no edits of ND clips, NC and Mixkit Restricted clips only in non-commercial work, no reliance on a suspicious Archive licence). Keys are read only from PEXELS_API_KEY / PIXABAY_API_KEY in the environment and are never printed or stored; never ask the user to paste a key into chat. Pinterest is never downloaded, and a Cloudflare browser check is never worked around.
- الحدود: Licences are what each source declares (Commons extmetadata, the uploader's licenseurl on the Archive, the Mixkit clip page, the Pexels, Pixabay, Coverr and NASA terms); the tool records them but cannot verify or grant rights. Archive items are often re-uploads: the suspicious-licence flag catches only titles and identifiers that look like music videos, film or TV rips or YouTube downloads, so every Archive licence stays the uploader's claim. --match and --no-people read titles only (a clip can show people its title does not name): screen the contact sheet. The Mixkit and Coverr adapters read page markup and embedded JSON that can change without notice (that source then reports an error and the others continue), and the Mixkit download route can answer a Cloudflare browser check, which the tool reports and does not work around (retry later). Scripts get Mixkit Free clips at their largest listed size (1080p, 2160p on some) and Restricted clips at 720p, and Coverr's 1080p file (vertical Coverr files are upscaled to 1920 wide); --quality/--max-height apply only where a source lists sizes (not NASA, Coverr or Commons, which offer one file here). Pexels and Pixabay search needs the user's keys (on 2026-10-21 Pexels was not issuing new keys (field note); its docs on 2026-10-29 say keys are issued instantly); from this sandbox upload.wikimedia.org and the Commons API answered 429 (Retry-After 46 s and 600 s), and --wait-429 waits at most 900 s. Videezy, Vecteezy, Dareful, Life of Vids, ESA and Openverse are listed with their licences but not searched (no API, a login wall or 403); videvo.net and mazwai.com now redirect to Freepik (probe reports them as moved).

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_free_footage.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:free-footage --evidence <ملف>`.

### `github-pulse` — نبض GitHub: أهم 1000 مستودع نشط في آخر 30 يومًا حسب المجال، والأفكار المنقولة منها / GitHub 30-day pulse: the 1,000 most important repositories active in the last 30 days, by domain, with the ideas taken

| الحقل | القيمة |
|---|---|
| المسار | `scripts/github_pulse.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `self-discovery` |

**ما تفعله:** يرتب المستودعات بعدد الناس النشطين في 30 يومًا من أرشيف أحداث GitHub وبالنجوم الكلية، ويصنفها في 14 مجالًا، ويستبعد غير الآمن، ويسجل 24 فكرة منقولة ومكانها. التحديث بثلاثة أوامر شبكية في مجلد عمل.

**What it does:** Ranks repositories by distinct people active in a 30-day window (GH Archive hourly events) plus total stars (deps.dev), keeps only those pushed or released in the window, classifies them into 14 domains with a minimum share for creative ones, labels licence classes, keeps cheats, cracks and bot-detection bypasses out, and records 24 ideas restated in our own words with where each now lives. build writes data/github_pulse.json and references/github-pulse-30d.md; top, find, show and ideas query it; collect, enrich and select refresh it into a work folder (network, curl).

#### متى تُستدعى

- «إيه أهم المستودعات اللي اتحدثت في آخر شهر في التصميم والموشن؟»
- «هات أحدث أفكار GitHub ونستفيد منها»
- «What is trending on GitHub this month for agents?»
- «Refresh the 30-day GitHub list»

#### الأوامر

- **top**: Leaders of a domain.
  - `python3 scripts/github_pulse.py top --domain design-ui -n 15`
- **ideas**: Ideas taken and where they live.
  - `python3 scripts/github_pulse.py ideas --status transferred`
- **show**: One repository with its decision and ideas.
  - `python3 scripts/github_pulse.py show heygen-com/hyperframes`
- **build**: Rebuild or check the tracker and report.
  - `python3 scripts/github_pulse.py build --check`
- **collect**: Network: aggregate GH Archive hours into the work folder.
  - `python3 scripts/github_pulse.py collect --work /tmp/pulse --end 2026-10-26 --days 30`

#### المتطلبات والأمان

- binaries: curl
- network: true
- الأمان: writes-files
- الموافقة: Query commands are read-only; build writes the tracker and report; collect/enrich/select download public archives into --work only and refuse to overwrite the committed snapshot.
- الحدود: GH Archive captures far fewer events since 2026, so 30-day counts are a sample good for ranking; repositories deps.dev has not indexed show no total stars; domains are keyword rules fixed by hand in the review file.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_v58_mastery.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A38-v58-thinking-books-github-pulse.md`
- مرجع: `.claude/skills/kosif-superpowers/references/github-pulse-30d.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:github-pulse --evidence <ملف>`.

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

### `instagram-finder` — البحث عن فيديوهات إنستجرام لمنتج وتحميلها / Instagram product video finder

| الحقل | القيمة |
|---|---|
| المسار | `scripts/instagram_finder.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `video-download`, `photo-video-footage`, `formats-platforms` |

**ما تفعله:** يحفظ قائمة حسابات إنستجرام كمصادر (من غير باراميترات التتبع)، ويبني فهرسًا محليًا قابلًا للبحث من آخر بوستاتها (instaloader) ومن الهاشتاجات وروابط الريلز (yt-dlp)، ويرتّب الفيديوهات حسب منتج تكتبه بالعربي أو الإنجليزي بمرادفات ثنائية اللغة وتطبيع عربي والهاشتاجات والكابشن والوصف التلقائي للصورة. ويطلع خطة بحث ويب بدون شبكة، وينزّل الصور المصغّرة للمعاينة، ويحمّل المختار عبر fetch_video.py مع سجل حقوق.

**What it does:** Keeps a list of saved Instagram source accounts (tracking parameters stripped), builds a local searchable index of their recent posts (instaloader), hashtags and pasted reel links (yt-dlp), and ranks the indexed videos for a product query in Arabic or English using bilingual synonyms, Arabic normalisation, hashtags, captions and Instagram's automatic image description. It prints offline web-search plans, fetches thumbnails for a visual check, and downloads picked results through fetch_video.py with a rights log.

#### متى تُستدعى

- «دوّر لي في إنستجرام على فيديوهات تناسب منتج العطر ده ونزّلها»
- «احفظ حسابات الإنستجرام دي كمصادر عشان ننزّل منها بعدين»
- «Find Instagram reels from my saved accounts that fit a watch commercial»
- «Search the saved Instagram accounts for coffee product videos and download the best two»
- «نزّل لي الريل ده: https://www.instagram.com/reel/XXXX/»
- «Collect every video link from this Instagram account and download them»

#### الأوامر

- **accounts**: Lists the saved source accounts from data/instagram_sources.json (no network).
  - `python3 scripts/instagram_finder.py accounts`
- **add-account**: Normalises profile links or @handles (query strings removed, instagram.com only) and saves new ones.
  - `python3 scripts/instagram_finder.py add-account "https://www.instagram.com/name?igsh=xyz" --tag product`
- **plan**: Offline: expands the query with bilingual synonyms and prints hashtag ideas, site:instagram.com/reel web searches and the saved account URLs.
  - `python3 scripts/instagram_finder.py plan "عطر رجالي"`
- **index**: Reads recent posts of every saved account (or --accounts, --hashtag) with instaloader into out/instagram/index.json, incrementally, 8 s between accounts, at most 200 posts per account.
  - `python3 scripts/instagram_finder.py index --session-user MY_USERNAME --limit 40`
- **browser-login**: Uses the user's Instagram login from a local browser (instaloader for index, --cookies-from-browser for add-posts and download); the cookies stay on the machine and are never written by the tool.
  - `python3 scripts/instagram_finder.py index --browser firefox`
- **get**: One step for links you already have: cleans each reel or post link (or a --urls links.txt from the Chrome extension apps/instagram-link-collector), downloads it through fetch_video.py and logs the rights (default reference-only). No index needed; tested from the cloud on 2026-10-24.
  - `python3 scripts/instagram_finder.py get "https://www.instagram.com/reel/XXXX/"`
- **add-posts**: Indexes single post or reel links with yt-dlp metadata (no download), 4 s apart.
  - `python3 scripts/instagram_finder.py add-posts https://www.instagram.com/reel/XXXX/`
- **search**: Ranks indexed videos for the query and prints why each matched; filters by account, duration, date and photos.
  - `python3 scripts/instagram_finder.py search "perfume splash" --max-dur 30 --save out/instagram/hits.json`
- **thumbs**: Downloads the thumbnails of chosen results for a visual check before downloading videos.
  - `python3 scripts/instagram_finder.py thumbs out/instagram/hits.json --top 8`
- **download**: Downloads picked results through fetch_video.py (edit-safe copy by default), 5 s apart, at most 25 per run, and appends instagram_rights.jsonl. --rights is required; permission and licensed need --evidence.
  - `python3 scripts/instagram_finder.py download out/instagram/hits.json --pick 1,3 --rights owned --dry-run`
- **doctor**: Reports instaloader, yt-dlp, the saved account count and the index size.
  - `python3 scripts/instagram_finder.py doctor`

#### المتطلبات والأمان

- network: true
- optional: pip:instaloader, pip:yt-dlp, bin:ffmpeg
- الأمان: network
- الموافقة: It reads Instagram with the user's own session and downloads third-party media: confirm the user owns it, has permission or a licence, or keeps it as private reference only. Never store, print or commit the session or cookies. Keep the default rate limits. INSTAGRAM_SESSIONID is a login credential: doctor reports only whether it is set, and the temporary cookies file it becomes is mode 0600 and deleted at exit.
- الحدود: Instagram has no keyword search the tool may use, so it only searches what was indexed. Profiles and hashtags usually need a logged-in session, private accounts need an accepted follow, instaloader and yt-dlp break when Instagram changes, and instagram.com is blocked from the cloud container (proxy 403), so indexing and downloads run on the user's device.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_instagram_finder.py`
- مرجع: `.claude/skills/kosif-superpowers/references/instagram-finder.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/video-download.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:instagram-finder --evidence <ملف>`.

### `instagram-reference-discovery` — البحث عن مراجع فيديو إنستجرام وربطها بالمصفوفات اللانهائية / Instagram Reference Discovery → Infinite Matrices

| الحقل | القيمة |
|---|---|
| المسار | `scripts/instagram_reference_bridge.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `web-research`, `story-direction-ideas`, `creativity-engine` |

**ما تفعله:** يسجّل حسابين مرجعيين، وينشئ روابط بحث عامة حسب المحتوى، ويفهرس الروابط التي يتحقق منها الباحث مع وصف عربي/إنجليزي داخل SQLite محليًا، ثم يولّد مقترحات بحثية للبنات المصفوفات الست وأقرب أساليب الأطلس الـ86 دون ادعاء مشاهدة أو تنفيذ الفيديو.

**What it does:** Offline-first source registration for two user-specified Instagram creators. Produces public web-search links by topic, safely indexes researcher-confirmed reel permalinks and Arabic/English annotations in local SQLite, ranks metadata, and writes evidence-labelled six-brick research proposals referencing the existing KMX 86-style catalog. Does not scrape, visit or download Instagram.

#### متى تُستدعى

- «ابحث عن ريلز إنستجرام بتأثير معين»
- «حلّل مراجع موشن من asirgokerr و brkn.land وحوّلها لأفكار في المصفوفات»
- «Find Instagram motion references for glowing particles and propose causal bricks»
- «فهرس فيديوهات ريلز حسب الستايل والحركة»

#### الأوامر

- **doctor**: Show indexed count, local database and no-network policy.
  - `python3 scripts/instagram_reference_bridge.py doctor`
- **sources**: Show the two user-specified unreviewed creator accounts.
  - `python3 scripts/instagram_reference_bridge.py sources`
- **plan**: Generate public Google and Bing search links, not search results.
  - `python3 scripts/instagram_reference_bridge.py plan "جسيمات ضوئية"`
- **add**: Store an explicitly supplied permalink with evidence metadata, without downloading a reel.
  - `python3 scripts/instagram_reference_bridge.py add https://www.instagram.com/reel/REALCODE/ --topic "light particles" --state link_only`
- **search**: Rank locally indexed observations by normalized Arabic/English matching.
  - `python3 scripts/instagram_reference_bridge.py search "مؤثرات 3d"`
- **propose**: Write a non-executable, evidence-gated KMX proposal with causal bricks and matching operator tags.
  - `python3 scripts/instagram_reference_bridge.py propose https://www.instagram.com/reel/REALCODE/ --catalog ../kosif-infinite-matrices/data/86_style_research_database.json --out out/ideas.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes to caller's isolated local SQLite catalog and only user-selected proposal output; refuses overwriting proposals. No external requests or media downloads. Shared research ledger not modified.
- الحدود: The CLI cannot directly search inside all Instagram reels or verify a video's actual motion; web results must be discovered separately and manually checked. Source states only attest to submitted notes and evidence URI presence, not authenticity. Proposal is not a runnable KMX recipe.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_instagram_reference_bridge.py`
- مرجع: `.claude/skills/kosif-instagram-discovery/SKILL.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/instagram-discovery.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:instagram-reference-discovery --evidence <ملف>`.

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

### `source-finder` — البحث عن اللقطات الأصلية لكل مشهد في فيديو مرجعي / Source finder: the original clips behind each shot of a reference video

| الحقل | القيمة |
|---|---|
| المسار | `scripts/source_finder.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `video-download`, `web-research`, `transitions-cuts` |

**ما تفعله:** يقسم الفيديو المرجعي إلى مشاهد بفرق الإطارات في OpenCV، ويأخذ من كل مشهد صورًا للبحث بقصّ ffmpeg يشيل الكتابة المحروقة على الفيديو، ويبحث بكل صورة في Yandex بالرفع ويجمع روابط Pinterest، ثم يصنّف كل pin بالمساعد المشترك scripts/_pinterest.py (طلب yt-dlp -J واحد: فيديو، صورة، GIF، يوتيوب مضمَّن، تضمين تاني، محذوف، سيرفر الفيديو رافض، محجوب؛ من غير إعادة محاولة) وينزّل الفيديوهات بس (في فولدر مؤقت، ويقيس المقاس الحقيقي بـffprobe، ويشيل صوت الـpin نفسه إلا مع ‎--keep-audio‎، ويكتب سجل نسب ‎.pin.json‎ لكل pin)، ويتحقق من كل مرشح كل نصف ثانية بنقاط ORB ومطابقة RANSAC. أمر run يربط الخطوات ويكتب تقريرًا مرتبًا لكل مشهد: مطابق تمامًا (150 نقطة فأكثر) أو محتمل (40 فأكثر) أو لا شيء، مع الرابط والتوقيت وعدد الـpins من كل نوع وسبب استبعاد الباقي، ويستنى بين طلبات Yandex ويقف عند أول captcha.

**What it does:** Splits a reference video into shots with OpenCV frame differences, takes per-shot query frames through an ffmpeg crop that removes burned-in captions, reverse-searches each frame on Yandex Images by upload (sites and similar pages) and keeps the Pinterest pins it returns, then classifies each pin with the shared helper scripts/_pinterest.py (one yt-dlp -J call: video, image, GIF, embedded YouTube, other embed, deleted, CDN-refused, blocked; never retried), downloads only the video pins (temp folder, real size measured with ffprobe, the pin's own audio stripped unless --keep-audio, a .pin.json credit record per pin) and verifies every candidate every 0.5 s with ORB 3000 features, a 0.75 ratio test and RANSAC homography inliers. run chains the steps and writes a ranked report.json per shot: exact (150+ inliers), possible (40+) or none, with the pin link and timestamp, plus how many pins of each kind were found and why the others were skipped; it waits between Yandex calls and stops at the first captcha.

#### متى تُستدعى

- «طلّع لي المصادر الأصلية للقطات الفيديو ده»
- «الفيديو ده متجمّع من لقطات منين؟ دوّر على مصدر كل مشهد»
- «Find the original source clips of each shot in this reel»
- «Reverse search the shots of this edit and tell me where the footage came from»
- «Which Pinterest video is this shot taken from?»

#### الأوامر

- **doctor**: Offline: which parts can run here (OpenCV, numpy, ffmpeg, ffprobe, curl, yt-dlp).
  - `python3 scripts/source_finder.py doctor`
- **cuts**: Offline: hard cuts from the mean HSV change between frames (threshold 27, shortest shot 0.4 s) as boundaries and a shot list.
  - `python3 scripts/source_finder.py cuts reference.mp4 --out out/source-finder/cuts.json`
- **frames**: Offline (ffmpeg): three cropped query frames per shot kept away from the cuts, one full mid frame and frames.json. --crop accepts one ffmpeg crop filter only.
  - `python3 scripts/source_finder.py frames reference.mp4 --cuts out/source-finder/cuts.json --crop "crop=iw:ih*0.6:0:ih*0.2" --out out/source-finder/queries`
- **search**: Network: uploads each image to Yandex search-by-image, reads the sites and similar pages and lists Pinterest pin ids plus other video and stock leads; at least 2 s between calls, at most 40 images a run, exit 3 at a captcha.
  - `python3 scripts/source_finder.py search out/source-finder/queries/s003_1.jpg --delay 4 --out out/source-finder/s003.json`
- **match**: Classifies the pins first and downloads only the video pins (cached in <work>/cand with a p<id>.pin.json per pin; image, GIF, embedded-YouTube and deleted pins are never asked again, CDN-refused ones at most once per run; audio stripped unless --keep-audio) or reads a folder of clips, samples every 0.5 s and ranks candidates by RANSAC inliers with the best timestamp; a candidate that cannot be decoded scores 0 with an error and the rest are still checked; the output counts the pins of each kind; --no-download or a folder keeps it offline.
  - `python3 scripts/source_finder.py match out/source-finder/queries/s003_0.jpg out/source-finder/queries/s003_1.jpg --candidates out/source-finder/s003.json --work out/source-finder`
- **run**: The whole chain with cached searches and a partial report.json after every shot; a captcha stops it with exit 3 and a re-run continues. --candidates DIR skips the search and runs offline.
  - `python3 scripts/source_finder.py run reference.mp4 --work out/source-finder --crop "crop=iw:ih*0.6:0:ih*0.2"`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe, curl, yt-dlp
- network: true
- python: numpy, opencv-python-headless
- الأمان: network
- الموافقة: search and run upload frames of the user's reference video to Yandex (a third-party service), and match and run download third-party Pinterest videos: confirm the user wants both. Downloaded clips stay as private reference in the work folder; reusing one needs its creator's permission or a licence, and every found source is credited and linked. Keep the rate limit, and at a captcha stop rather than bypass it. No account, cookie or credential is used.
- الحدود: Finds a source only when it is posted on Pinterest as a video pin that Yandex indexes, so the hit rate depends on the reel: in this repository's runs it found 4 of 13 shots on one reel (514-1447 inliers against about 7-36 for unrelated clips), 1 of 4 on another and none on four more. Yandex and Pinterest pages can change or answer with a captcha, which stops the run. Hard cuts only (dissolves and fades are not split); mirrored, re-framed, re-graded or AI-redrawn footage scores lower. Most pins a search returns are not usable footage (in the 2026-10-29 scout run of about 140 pins, about 60% were images, and others were GIFs, embedded YouTube or deleted); Pinterest video is 720p at most whatever its 1080x1920 label says. Found clips belong to their creators: credit and link them.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_source_finder.py`
- `.claude/skills/kosif-superpowers/evals/test_pinterest.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:source-finder --evidence <ملف>`.

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
  - `python3 -I scripts/sources_index.py add charter.txt --dir ../../../out/demo`
- **list**: Lists indexed sources with counts.
  - `python3 -I scripts/sources_index.py list --dir ../../../out/demo`
- **show**: Prints one record (metadata, headings and flags, never body text).
  - `python3 -I scripts/sources_index.py show SRC-0123456789 --dir ../../../out/demo`
- **find**: Matches titles and headings and returns line ranges; --body also returns matching line numbers, never text.
  - `python3 -I scripts/sources_index.py find "الباب الرابع" --dir ../../../out/demo`

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

### `tiktok-photo` — تحميل بوست صور تيك توك (سلايد شو) / TikTok photo-post (slideshow) downloader

| الحقل | القيمة |
|---|---|
| المسار | `scripts/tiktok_photo.py` (جذر: skill) |
| المجال | `sources` |
| الدليل | `tested-here` |
| العائلات | `video-download`, `photo-video-footage`, `formats-platforms` |

**ما تفعله:** ينزّل بوست الصور في تيك توك اللي yt-dlp بيرفضه (Unsupported URL .../photo/): يفك الرابط المختصر vt.tiktok.com بتتبع التحويلات، ويفتح صفحة البوست بهوية متصفح سفاري للموبايل، ويقرأ بيانات JSON المضمّنة في الصفحة (الوصف والحساب والصوت وروابط الصور ومقاساتها)، ويحفظ كل صورة img00.jpg و img01.jpg وهكذا (كتابة آمنة واستكمال لو التحميل اتقطع)، ويجيب صوت البوست بـ yt-dlp من رابط /video/ المقابل، ويكتب meta.json فيه الحساب والوصف والصوت والرابط والمقاسات وسطر نسب الحقوق. وأمرا parse و url يشتغلوا من غير إنترنت على صفحة محفوظة أو رابط.

**What it does:** Downloads a TikTok photo post, which yt-dlp rejects with "Unsupported URL .../photo/<id>": it resolves a vt.tiktok.com or vm.tiktok.com short link by following redirects, fetches the /@user/photo/<id> page with a mobile Safari User-Agent, reads the JSON in <script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"> (itemStruct: desc, author, music, imagePost.images with sizes), saves every image as img00.jpg, img01.jpg ... (atomic writes, mirror links, resumable), gets the post's sound with yt-dlp -f ba on the rewritten /video/<id> link, and writes meta.json with author, desc, music, source link, image sizes and a credit line. parse and url work offline on a saved page or a link.

#### متى تُستدعى

- «نزّل صور البوست ده من تيك توك https://vt.tiktok.com/XXXXXXX/»
- «yt-dlp بيقول Unsupported URL على رابط تيك توك فيه /photo/»
- «عايز صور السلايد شو بتاعة تيك توك وصوتها»
- «Download the images of this TikTok photo slideshow»
- «yt-dlp says Unsupported URL for a TikTok /photo/ link»
- «Get the slides and the sound from a TikTok photo post»

#### الأوامر

- **fetch**: Network: resolves the link, saves img00.jpg ..., audio.<ext> (yt-dlp -f ba on the /video/ link) and meta.json; exit 2 on a partial download (rerun to resume), 3 for a video post (use yt-dlp), 4 when the page JSON is missing. --html uses a page saved on your device, --no-audio skips the sound.
  - `python3 scripts/tiktok_photo.py fetch "https://vt.tiktok.com/XXXXXXX/" --out out/tiktok/post`
- **parse**: Offline: prints the post JSON extracted from a saved page (author, desc, music, image links and sizes, the /photo/ and /video/ links).
  - `python3 scripts/tiktok_photo.py parse evals/fixtures/tiktok_photo_minimal.html`
- **url**: Offline: classifies a link (photo, video, short, other) and prints its /photo/ and /video/ forms without the tracking query.
  - `python3 scripts/tiktok_photo.py url "https://www.tiktok.com/@user/photo/7400000000000000001"`

#### المتطلبات والأمان

- network: true
- optional: pip:yt-dlp
- الأمان: network
- الموافقة: It downloads a third-party creator's post: confirm the user owns it, has the creator's permission or a licence, or keeps it as private reference only; keep the credit line and link the post. It sends no cookies or login and writes only into --out.
- الحدود: TikTok's page structure can change without notice (the tool then stops with a clear error, exit 4); private, removed, region-locked or login-walled posts fail, some networks block tiktok.com (save the page on your device and use --html), the sound needs yt-dlp and depends on its TikTok extractor, and the CDN image links are signed and expire, so meta.json keeps only their host. Respect creators: link and credit.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_tiktok_photo.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:tiktok-photo --evidence <ملف>`.

