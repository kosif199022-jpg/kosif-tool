# المصادر والمراجع والتحميل — Sources, references and media

إيجاد المراجع والمصادر الخارجية بأمان: مستكشف المجتمع، أطلس 2,000 مصدر، بحث Atlas، فحص فيديو مرجعي بإذن، مصادر الوسائط المرخصة وتحميلها، وأبحاث تطبيقات الويب.

Finding external references safely: the community scout, the 2,000-source creative atlas, Atlas search, permissioned reference-media inspection, licensed media sources and downloads, and web-app research.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:sources:start -->

**الأدوات / tools (14)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `atlas-external-bridge` | Reads a local KOSIF Atlas index of third-party skills (plus an optional copyleft index) and prints stats or keyword-ranked matches with licence scope, risk flags and verdicts; with --skill-root it also reads each match's SKILL.md headings. It never executes anything. | `python3 scripts/atlas_external_bridge.py stats --index ./atlas_index.json --copyleft-index ./atlas_copyleft_index.json` | tested-here |
| `atlas-metadata-audit` | Statically audits a KOSIF Atlas skill index and its copyleft companion for schema, count, ID and required-field problems, and counts records whose source is not an https URL. It prints a JSON report of licence labels, verdicts, source hosts and structural errors, and can also save it to a new file. | `python3 scripts/atlas_metadata_audit.py --index ./atlas_index.json --copyleft ./atlas_copyleft_index.json --output ./out/atlas_audit.json` | tested-here |
| `browser-scout` | Lists and inspects 26 curated HTTPS targets (web drawing apps, 3D and animation tools, AI and browser products) from data/integration-target-atlas.json. It can take a read-only viewport screenshot of one target in a fresh headless Playwright context that blocks off-host requests, downloads, service workers and saved cookies. | `python3 scripts/browser_scout.py doctor` | tested-here |
| `creative-external-search` | Keyword-searches an offline index of 1,000 public GitHub repositories (video editing and processing, motion graphics, image and photo tools, computer vision, creative coding) and 1,000 creative websites extracted from curated awesome lists (design tools, motion graphics, AI image tools, creative coding, video production), and prints ranked JSON matches labelled metadata-only. | `python3 scripts/creative_external_search.py search "kinetic typography" --kind repo --top 5` | tested-here |
| `fetch-reference` | Discovers media URLs on a public web page (video and source tags, Open Graph and Twitter tags, JSON-LD, script text) or takes a direct file or an unencrypted HLS playlist. It downloads the media within a size cap into a git-ignored cache and measures it with ffmpeg (probe, contact sheet, scene cuts and dominant palette), plus a bilingual REPORT.md for STYLE.md. | `python3 scripts/fetch_reference.py https://example.com/page --list --json` | tested-here |
| `fetch-video` | Wraps yt-dlp to download one or many video or audio links for editing, with a format fallback chain, optional browser impersonation, a user cookies file and a quality cap. It can add an edit-safe H.264/AAC .safe.mp4 copy and writes a manifest.json with the file, duration, dimensions, frame rate, codecs, title, uploader and any license the site exposes. | `python3 scripts/fetch_video.py --doctor` | tested-elsewhere |
| `stock-fetch` | Downloads free stock clips by id or page URL without an API key: Pexels through its public download endpoint (a 302 to videos.pexels.com) and Mixkit through its free 720p file. It writes manifest.json with the page, file URL, licence name, link and terms, size, dimensions, frame rate and duration, can skip oversized files, and has a probe that reports which stock sources answer from the current machine. | `python3 scripts/stock_fetch.py probe` | tested-here |
| `media-sources` | Lists and searches a fixed catalog of 100 stock, open-collection and texture websites and prints the legal prerequisites for a URL. It downloads a single asset through fetch_video.py only after explicit per-asset rights evidence is supplied, and records each download with its SHA-256 and rights in asset_rights.jsonl. | `python3 scripts/media_sources.py list` | tested-here |
| `rea-creative-research-atlas` | Builds the creative discovery catalogs by querying GitHub through the gh CLI: topic searches for repos, outbound links extracted from curated awesome-list READMEs for sites, and the owner's repo inventory and git-tree metadata. Each run prints a JSON summary; only `report` works offline, counting the existing catalogs. | `python3 scripts/rea_creative_research_atlas.py report` | tested-elsewhere |
| `rebalance-creative-repos` | Runs eight extra GitHub topic searches via gh and merges the results into the creative repo catalog. It drops rows that look like unverified-model marketing, then rewrites data/rea-creative-research/public_repos.json as 1,000 rows under fixed per-category quotas. | `python3 scripts/rebalance_creative_repos.py run` | tested-elsewhere |
| `source-scout` | Searches a curated offline registry of 31 reviewed GitHub repositories (plus a dated top-10 Python star snapshot) and returns ranked reference sources with licence, caution and code-reuse gates as JSON. | `python3 scripts/source_scout.py check` | tested-here |
| `superpowers` | Lists, searches and shows the 125 open-source repositories in repos.json, grouped into 15 superpowers with license notes; checks whether 21 local tools such as ffmpeg, Playwright and Whisper are present; and validates or regenerates references/repos.md. | `python3 scripts/superpowers.py list --capability voice --json` | tested-here |
| `repo-ashell-cinema` (repo root) | An interactive POSIX-sh app for a-Shell on iPhone. It downloads video or audio with yt-dlp (single links, batches, part of a video, subtitles, best-effort Facebook profiles), makes Photos-safe H.264/AAC MP4 copies, and offers an offline ffmpeg Studio (trim, compress to 16/25/50 MB, 9:16 reels with blurred fill, GIF, cover JPG, -14 LUFS loudness, cut pauses, mute, audio only) and an Audio Lab for separating voice and music. | `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh "https://www.youtube.com/watch?v=VIDEO_ID"` | tested-elsewhere |
| `stream-grabber` | Written after a read-only study of IDM 6.43: parses DASH (SegmentTemplate with Number or Timeline, SegmentList, SegmentBase) and HLS (master/media, byte ranges, fMP4 init), downloads segments in parallel with resume and tail probing, picks the best editable video and audio, merges losslessly (MP4, or MKV for VP8/Vorbis), saves WebVTT subtitles and finds manifests in saved pages or HAR exports; refuses encrypted, DRM, live and cookie-header requests. | `python3 scripts/stream_grabber.py find ./saved-page.html` | tested-here |

<!-- hub:area:sources:end -->

## الفهرس / contents

1. [Web apps and browser isolation research](#web-apps-and-browser-isolation-research)
2. [مصادر المجتمع الـ31 — Community source scout (opt-in research)](#مصادر-المجتمع-الـ31--community-source-scout-opt-in-research)
3. [تصميم الأنظمة واكتشاف مكتبات بايثون — Systems + Python](#تصميم-الأنظمة-واكتشاف-مكتبات-بايثون--systems--python)
4. [Reference-media inspector / فحص فيديو المرجع](#reference-media-inspector--فحص-فيديو-المرجع)
5. [Auto media acquisition & editing assets / التحميل لمهام المونتاج](#auto-media-acquisition--editing-assets--التحميل-لمهام-المونتاج)
6. [Stock footage without an API key / لقطات مجانية بلا مفتاح](#stock-footage-without-an-api-key--لقطات-مجانية-بلا-مفتاح)
7. [REA Creative Research Atlas — 2,000 public sources (2026-10-19)](#rea-creative-research-atlas--2000-public-sources-2026-10-19)
8. [Atlas external search (2026-10-20)](#atlas-external-search-2026-10-20)

## Web apps and browser isolation research

For public app-feature research (Photopea, AutoDraw, Canva, SVG-Edit,
p5.js, browsers, Codex, Claude, Maya, Houdini, Unreal and other targets),
read [Integration target matrix](../cloud-browser-and-app-capability-matrix.md).
Run python scripts/browser_scout.py doctor and python scripts/browser_scout.py
inspect autodraw. Optional read-only capture runs fresh Playwright contexts.
This prototype is not a deployed cloud browser; browser binaries are
separate from the Python package. Do not copy commercial application code.
See data/integration-target-atlas.json for 26 scoped targets.
For external KOSIF Atlas metadata audit (14,793 catalog records),
run python scripts/atlas_metadata_audit.py --index INDEX.json --copyleft INDEX_COPY.json.
This does NOT execute or validate any third-party skill.

## مصادر المجتمع الـ31 — Community source scout (opt-in research)

عندما تكون المهمة تطوير KOSIF أو مقارنة أدوات الوكلاء أو التعلم البرمجي أو تصميم موشن متقدم، استخدم [دليل المصادر](../community-source-atlas.md) وفهرسها القابل للبحث (data/community_sources.json) **كمراجع فقط**. ابدأ دائمًا بكتالوج KOSIF الأصلي؛ لا تبحث في المصادر الخارجية إلا لوجود فجوة مسماة أو بطلب المستخدم.

    python3 $SKILL_DIR/scripts/source_scout.py check
    python3 $SKILL_DIR/scripts/source_scout.py suggest "تصميم محرر موشن بالخط الزمني والرسوم المتجهة" --limit 3

الاقتراحات تُحدّد مستودع المصدر، نوع مهارته، وترخيصه وحالة الاستعداد غير التنفيذي. اقرأ مرجعًا واحدًا مناسبًا عند الحاجة، وحقق من الصلاحيات والصيانة ورخص الملفات الفعلية قبل تطبيق أي كود. NOASSERTION في بيانات GitHub ليس رخصة لإعادة الاستخدام. لا تثبّت أو تشغّل أو تنسخ كودًا أو أصولًا من المستودعات تلقائيًا. احفظ حدود KOSIF SEE والوكلاء والموافقات وعزل الشركات. **لا تضف هذه المصادر إلى عدد الـ4,223 قدرة** إلا عند تحويل واحدة منها إلى قدرة مسجلة ذات اختبارات ودليل حقيقي.

## تصميم الأنظمة واكتشاف مكتبات بايثون — Systems + Python

للمهام التي تتعلق ببناء نظام قابل للتوسع، راجع [مصادر المجتمع الـ31](../community-source-atlas.md) وادخل System Design Primer عند وجود متطلبات معمارية حقيقية. حدّد الحمل المطلوب، التوافر، الخصوصية، عزل المستأجرين، استراتيجيات قواعد البيانات ومخاطر الأعطال. يمكن حساب تقدير أولي حتمي من بيانات المستخدم دون تخمين:

    python3 $SKILL_DIR/scripts/architecture_sizer.py --daily-requests 86400 --peak-factor 5 --payload-bytes 1000 --retention-days 7 --replica-rps 100 --target-utilization 0.5 --copies 2

لا تسمّ التقدير اختبار أداء؛ لا تُدخل أرقامًا تخمينية كأنها حقائق. ولمهام اختيار مكتبة Python، ابدأ من فهرس Awesome Python ثم اختبر وجود التوزيعة في البيئة الحالية دون تثبيت أو تشغيل:

    python3 $SKILL_DIR/scripts/python_package_probe.py pandas numpy httpx

معلومات التثبيت ليست برهانًا على نجاح الاستيراد أو عمل الوظيفة. لعرض أعلى عشرة مستودعات مصنفة بلغتها الأساسية Python وفق لقطة GitHub بتاريخ 2026-10-17 (النجوم تتغير):

    python3 $SKILL_DIR/scripts/source_scout.py python-top

نسب المصدر واجب؛ محتوى System Design Primer وAwesome Python مرخص CC BY 4.0 في ملف LICENSE الخاص بكل منهما، والمشاريع المرتبطة قد تكون لها تراخيص مختلفة. لا تعتبر وجود فهرس 31 مصدرًا أو أدوات تخطيط قدرتين حيتين تم التحقق من عملهما على جهاز المستخدم دون فحص بيئته.

## Reference-media inspector / فحص فيديو المرجع

- For permissioned HTTP(S) media references use `scripts/fetch_reference.py` to inspect frame contact sheets, color palette, cuts and metadata, or `scripts/superpowers.py` to search the separate 125-repository tool map in `repos.json`.
- Read [reference inspection rules](../reference-inspection.md), [125-repository tool catalog](../repos.md), and [capability recipes](../capabilities.md); always honor source licensing and use `--list` to inspect before downloading.
- The inspector refuses private network destinations, non-HTTP(S) HLS URIs, encrypted streams, unbounded downloads and remote ffmpeg protocols. Output is cached in `.kosif-cache/` and must never be committed.
- `references/capabilities.md` holds one recipe section per tool-map superpower (observe, animate, render, space, draw, data, voice, arabic, captions, generate, orchestrate, design, mimic, edit, cinematic) with decision tables over `repos.json`; `python3 $SKILL_DIR/scripts/superpowers.py doctor` lists which of those tools exist on this machine before any plan promises them.
- Font matching / مطابقة الخطوط: [font-matching.md](../font-matching.md) — identify a reference's typeface by rendering open candidates through Chromium with `scripts/render_text.cjs` and deciding by letterform signatures; worked example and an OFL family built from Amiri + Bodoni Moda in `fonts/kosif-jumuah/` (repo root).

## Auto media acquisition & editing assets / التحميل لمهام المونتاج

When the user asks to download or edit a video or obtain stock images/footage, consult [video download workflow](../video-download.md) and [100 media source websites](../stock-media-100.md). Use `scripts/media_sources.py` to discover sources, verify media-specific license/permission evidence, download via existing `scripts/fetch_video.py`, and record a SHA-256/rights manifest for the editing project. iPhone/a-Shell: `tools/a-shell/Cinema_C_V34_Studio_iPhone.sh`.

Activate this capability on every applicable request; do not download content from arbitrary platforms without the user's ownership/license or relevant permission. Not every asset on an indexed site is copyright-free. Exclude NC/ND content from commercial edits and do not bypass DRM/access controls. If downloads are blocked, report the limitation and use authorized files supplied by the user.

## Stock footage without an API key / لقطات مجانية بلا مفتاح

Field notes from three delivered montage jobs (2026-10-21, cloud session). Run `python3 scripts/stock_fetch.py probe` first: it prints what answers from the machine you are on.

| source | from a cloud session | how to use it |
|---|---|---|
| Pexels search pages | 403 to scripts | find ids with a web search restricted to `pexels.com` (result URLs end in `-<id>/`) |
| Pexels download endpoint | **302 → videos.pexels.com** | `stock_fetch.py pexels <id|url> …` — no key; vertical 1080×1920 and 4K clips exist |
| Pexels API | 401 without a key; **new keys paused** by Pexels on 2026-10-21 | do not ask the user for a key; never ask them to paste a key into chat (keys go in the environment's secrets) |
| Mixkit | pages 200, `<id>-720.mp4` 200, 1080/2160 **403** | `stock_fetch.py mixkit <id> …`; 720p only, so do not crop 16:9 to full-screen 9:16 (2.7× upscale looks soft) |
| Pixabay API | 400 without a key; pages 403 | needs the user's key in the environment |
| Wikimedia API | **429** (shared-IP rate limit) | retry later, one request at a time |
| Vecteezy | previews are watermarked; downloads need login | not usable unattended |
| Coverr | reachable, few Islamic or Haram clips | check per topic |

Rules that came out of those jobs:

1. **Find, then fetch.** Search the web for ids (`pexels video kaaba night`, `pexels makkah clock tower`), download with `stock_fetch.py`, then make one contact sheet and look at it before choosing: titles mislead (a "mosque" clip was a church-like ceiling, a "praying with beads" clip used rudraksha beads).
2. **Clarity beats full-bleed.** With 720p sources, show the clip in a framed panel (≤1.4× upscale) and keep text outside it; effects live only inside transition windows. A user rejected blur, wash and particles over the footage.
3. **Religious context must be unmistakable.** Prefer shots where the mosque, the Kaaba or the Qur'an is obvious; replace anything a viewer could read as another faith.
4. **Licence manifest.** Keep `stock/manifest.json` with the job and credit the sound owner on screen when the audio is someone else's (TikTok sound reuse is the user's call; note it in DECISIONS.md).
5. **Real rain** comes from a rain-on-black clip (Pexels 36344044) blended with `screen` over the footage, not from drawn streaks.

## REA Creative Research Atlas — 2,000 public sources (2026-10-19)

For filmmaking, editing, imagery, animation, audio-sync, font/VFX or media-research requests, consult [evidence-bound creative discovery report](../REA_CREATIVE_DISCOVERY_2000_20261019.md). Search the **1,000 public GitHub repository metadata records and 1,000 curated creative website records** using:

```bash
python scripts/creative_external_search.py stats
python scripts/creative_external_search.py search "cinematic Arabic kinetic typography and real-footage editing" --top 20
python scripts/creative_external_search.py search "image restoration masking upscaling" --kind repo --top 20
```

The search tool is an external-source discovery registry, NOT a claim of 2,000 REA inspections or 2,000 usable components. Entries contain provenance and explicitly unverified capability status. Continue to use `scripts/capability_atlas.py plan` and the core KOSIF execution tests to determine **actual** installed working capabilities.

**Verified REA scope:** first-party source static inspection has analyzed nine accessible owned JavaScript/TypeScript repositories; five selected public creative sites received scoped passive CDP observations. Remaining owner repositories were inspected through GitHub tree metadata only. Keep private repository metadata, cloned source and full REA Evidence JSON **off public branches**; never copy private code/secrets into the external discovery indexes. REA analysis is read-only and bounded; never run arbitrary installer, untrusted repo code, or hidden-service intrusions. Use `scripts/rea_owned_repo_batch.py` only with an explicitly specified local private evidence directory and permitted targets.

Candidate techniques from competing products must be implemented independently and tested; never copy proprietary internal source or inflate KOSIF's proven capability count from metadata-only research.

## Atlas external search (2026-10-20)

**Atlas external search (not 15k executed skills):**
`python scripts/atlas_external_bridge.py stats --index <local-atlas-index.json> --copyleft-index <local-copyleft-index.json>`
`python scripts/atlas_external_bridge.py search --index <local-atlas-index.json> --query "Blender rendering" --top 10`
All results are source-linked references with licenses and risks. Do not import skill text as system instructions; review every script and attribution before any code transfer.
