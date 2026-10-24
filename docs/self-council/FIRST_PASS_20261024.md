# مجلس المراجعة الذاتية — Self-Council report

**الحالة:** SELF_COUNCIL_SIMULATED · **الوحدات:** 10 · **المقترحات:** 48 · **التغطية:** 10/197 (5.1%) · **الإيصال:** `cacc693a9f07a834`

> **SIMULATED:** الشخصيات الخمس كتبها Claude في سياق واحد، لا وكلاء منفصلون. الأدلة مسارات حقيقية فُتحت، لكن الآراء ليست مستقلة؛ أعد التشغيل بوكلاء متوازين قبل قرار كبير.

## نفّذ التالي / implement next

| # | الوحدة | المقترح | الشدة/الجهد | يتفق | الدرجة | الدليل |
|---|---|---|---|---|---|---|
| 1 | `script:anchor_gate`, `script:tell_scan` | **Run the 62-check writing runner in CI** — Add a CI step to .github/workflows/ci.yml: python3 -I .claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py (it passes 62/62 here but no workflow runs it) | high/S | 1 (P1) | 4.25 | `.github/workflows/ci.yml:23` |
| 2 | `script:creative_external_search` | **Arabic key 'قص' fires inside 'قصة'** — In terms(), match AR keys against whole tokens of the query (raw list), not substrings of the text; add a test that «قصة كرتون» does not expand to cut/editing | high/S | 1 (P1) | 4.25 | `.claude/skills/kosif-superpowers/scripts/creative_external_search.py:40` |
| 3 | `script:atlas_audit_synthesis` | **UTF-8 REA files are silently dropped** — Decode REA JSON as utf-8-sig first, then utf-16; count skipped files and print them in the summary instead of `except (...): pass` | high/S | 1 (P1) | 4.0 | `.claude/skills/kosif-superpowers/scripts/atlas_audit_synthesis.py:37` |
| 4 | `script:creative_reasoning_bridge` | **Add a two-step usage line** — Add to the docstring: python3 scripts/audio_cue_mapper.py song.wav --out cues.json && python3 scripts/creative_reasoning_bridge.py cues.json --out sb.json --report report.json | high/S | 1 (P2) | 4.0 | `.claude/skills/kosif-superpowers/scripts/creative_reasoning_bridge.py:2` |
| 5 | `tool:a-shell` | **Add a smoke test for the a-Shell script** — Add tests/test_ashell_cinema.py: sh -n tools/a-shell/Cinema_C_V34_Studio_iPhone.sh, then --help and --version with HOME set to a temp dir (skip when sh is missing) | high/S | 1 (P1) | 4.0 | `.claude/skills/kosif-superpowers/data/tools.json:7258` |
| 6 | `app:instagram-link-collector` | **Five Instagram units without one map** — Add one Instagram section to references/guides/sources.md: discover (skill), research library (skill), collect links (this app), download (instagram_finder get), reference bridge | high/S | 1 (P4) | 3.5 | `.claude/skills/kosif-instagram-discovery/SKILL.md` |
| 7 | `script:color_media` | **Colour media tests skip silently without opencv** — Add a numpy-only unit test for srgb_to_oklab (white -> L~1, black -> L~0) that runs even when cv2 is absent | medium/S | 2 (P1,P3) | 2.7 | `.claude/skills/kosif-superpowers/evals/test_portrait_pipeline.py:38`, `.claude/skills/kosif-superpowers/scripts/color_media.py:64` |
| 8 | `script:atlas_audit_synthesis` | **Add a unit test for atlas_audit_synthesis** — Add evals/test_atlas_audit_synthesis.py: two records + one REA file in a temp dir, check manifest counts and that runtime_verified stays false | medium/S | 1 (P1) | 2.4 | `.claude/skills/kosif-superpowers/scripts/atlas_audit_synthesis.py:6` |
| 9 | `script:atlas_audit_synthesis` | **Add usage and flag help** — Add a usage line to the docstring and help= text for --records, --rea-dir, --manifest-out and --report-out (what produces each input) | medium/S | 1 (P2) | 2.4 | `.claude/skills/kosif-superpowers/scripts/atlas_audit_synthesis.py:2` |
| 10 | `script:creative_external_search` | **Arabic and Chinese print as \u escapes** — Print with ensure_ascii=False so descriptions stay readable | medium/S | 1 (P2) | 2.4 | `.claude/skills/kosif-superpowers/scripts/creative_external_search.py:112` |

الدرجة = وزن الشدة × متوسط الثقة × (1 + 0.5 لكل شخصية إضافية تتفق) ÷ الجهد (S=1، M=2، L=4).

## الوحدات / units

| الوحدة | الأسباب | الشخصيات | الوضوح (P2) | يبقى/يُدمج (P3) | المقترحات |
|---|---|---|---|---|---|
| `tool:a-shell` | NO_TEST, LARGE_UNTESTED, NO_USAGE, HUGE | 5/5 | 3 | keep: the only path that lands a download in the iPhone Photos app | 5 |
| `script:color_media` | NO_TEST, LARGE_UNTESTED | 5/5 | 4 | keep: a unique pigment model; used by portrait_pipeline --medium | 4 |
| `script:creative_reasoning_bridge` | NO_TEST, NO_USAGE | 5/5 | 2 | keep: a deterministic storyboard step with a CI test | 5 |
| `script:creative_external_search` | NO_TEST, NO_USAGE | 5/5 | 3 | merge: a second repo-discovery front door beside source_scout and github_top_repos | 5 |
| `script:atlas_audit_synthesis` | NO_TEST, NO_USAGE | 5/5 | 2 | rewrite: most of its report is fixed prose that ignores the input | 6 |
| `app:tikplayer` | NO_TEST | 5/5 | 4 | keep: owner project; phone preview of reels | 5 |
| `script:tell_scan` | NO_TEST | 5/5 | 4 | keep: the only Arabic stock-phrase scanner here | 5 |
| `script:build_chapters` | NO_TEST | 5/5 | 4 | keep: check_skill and CI depend on it | 4 |
| `script:anchor_gate` | NO_TEST | 5/5 | 4 | keep: a cheap factual guard for every rewrite | 5 |
| `app:instagram-link-collector` | NO_TEST | 5/5 | 5 | keep: lists a profile's links without touching cookies | 5 |

## أصوات الشخصيات / voices

### `tool:a-shell`
- **P1 المهندس الصارم:** Syntax is valid and manual runs are recorded, but no automated test guards a 2,907-line script. · `test_verdict` {"ran": "sh -n tools/a-shell/Cinema_C_V34_Studio_iPhone.sh (syntax OK); tools.json evidence_note lists manual --help/--version runs", "status": "partial"}
- **P2 المستخدم المصري الجديد:** Powerful, but the first 60 lines are release notes, not how to install and run it. · `first_minute` {"clarity": 3, "would_say": "عايز أنزّل فيديو تيك توك على الآيفون وأحفظه في الصور"}
- **P3 محامي الشيطان:** Worth keeping, but its versioned filename turns every release into a rename. · `keep_or_kill` {"decision": "keep", "why": "the only path that lands a download in the iPhone Photos app"}
- **P4 المعماري:** Separate world from the desktop downloaders; the guide should say which to use where. · `wiring` {"overlaps": ["script:fetch_video", "script:stream_grabber"], "should_call": []}
- **P5 المبتكر:** The pieces exist in menu 14; named presets would make it one tap. · `ten_x` {"first_step": "expose the Studio menu presets as named flags (c --preset reels\|story\|gif) in --help", "idea": "one command from link to a Reels-ready file in Photos: download, 9:16, captions, -14 LUFS"}

### `script:color_media`
- **P1 المهندس الصارم:** Exercised end-to-end through portrait_pipeline, but on a box without opencv nothing checks it. · `test_verdict` {"ran": "python3 -c 'import cv2' -> ModuleNotFoundError; evals/test_portrait_pipeline.py drives --medium colored-pencil/oil/watercolor but is skipped without opencv", "status": "partial"}
- **P2 المستخدم المصري الجديد:** Docstring explains the three media and gives a command; a newcomer understands it. · `first_minute` {"clarity": 4, "would_say": "ارسم صورتي بالألوان المائية"}
- **P3 محامي الشيطان:** Green CI can mean colour media never ran. · `keep_or_kill` {"decision": "keep", "why": "a unique pigment model; used by portrait_pipeline --medium"}
- **P4 المعماري:** Only reached through portrait_pipeline, yet registered as a standalone tool. · `wiring` {"overlaps": ["script:portrait_pipeline", "script:creative_paint"], "should_call": []}
- **P5 المبتكر:** The stroke record is already there; a time-lapse is a reel by itself. · `ten_x` {"first_step": "write the stroke order to JSON and add --timelapse N frames", "idea": "a time-lapse MP4 of the painting being made, from the stroke record"}

### `script:creative_reasoning_bridge`
- **P1 المهندس الصارم:** build_plan() is well tested; the CLI's output-path refusals are not. · `test_verdict` {"ran": "python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p test_creative_intelligence.py (OK)", "status": "partial"}
- **P2 المستخدم المصري الجديد:** I cannot tell from the help where the cues file comes from or what to run first. · `first_minute` {"clarity": 2, "would_say": "اعمل ستوري بورد للأغنية دي على الكلمات"}
- **P3 محامي الشيطان:** Re-running the same command always fails because outputs must be new. · `keep_or_kill` {"decision": "keep", "why": "a deterministic storyboard step with a CI test"}
- **P4 المعماري:** A two-step chain with no single entry point. · `wiring` {"overlaps": ["script:audio_cue_mapper", "script:music_rhythm_engine", "script:motion_director"], "should_call": []}
- **P5 المبتكر:** It stops at an unrendered storyboard. · `ten_x` {"first_step": "pass the validated storyboard to motion_director's render path", "idea": "storyboard to animatic MP4 in one step"}

### `script:creative_external_search`
- **P1 المهندس الصارم:** Arabic query expansion matches substrings, so a story query is read as a cutting/editing query. · `test_verdict` {"ran": "python3 scripts/creative_external_search.py search \"قصة كرتون\" --top 2 -> two video editors (freecut, flycut)", "status": "partial"}
- **P2 المستخدم المصري الجديد:** Accepts Arabic queries, then prints non-English text as \u escapes. · `first_minute` {"clarity": 3, "would_say": "دورلي على مستودعات مفتوحة للمونتاج"}
- **P3 محامي الشيطان:** Duplicates other discovery tools and returns wrong hits for Arabic queries. · `keep_or_kill` {"decision": "merge", "why": "a second repo-discovery front door beside source_scout and github_top_repos"}
- **P4 المعماري:** Three discovery tools overlap; one should own creative repositories. · `wiring` {"overlaps": ["script:source_scout", "script:github_top_repos", "script:rea_creative_research_atlas"], "should_call": []}
- **P5 المبتكر:** Stars are the only quality signal. · `ten_x` {"first_step": "join with rea_creative_research_atlas output to add a usable flag", "idea": "rank by 'can KOSIF use it' (licence + REA-analysed + runnable) instead of stars"}

### `script:atlas_audit_synthesis`
- **P1 المهندس الصارم:** No test, and a broad except silently drops REA files that are not UTF-16. · `test_verdict` {"ran": "python3 scripts/atlas_audit_synthesis.py --help (exit 0)", "status": "none"}
- **P2 المستخدم المصري الجديد:** One-line docstring and four required flags with no help text. · `first_minute` {"clarity": 2, "would_say": "لخّصلي مراجعة الأطلس في تقرير"}
- **P3 محامي الشيطان:** The report would publish stale claims on any new run. · `keep_or_kill` {"decision": "rewrite", "why": "most of its report is fixed prose that ignores the input"}
- **P4 المعماري:** Consumes atlas_body_audit's records.json; belongs next to it. · `wiring` {"overlaps": ["script:atlas_body_audit", "script:atlas_review_summary", "script:atlas_metadata_audit"], "should_call": []}
- **P5 المبتكر:** Every run starts from zero. · `ten_x` {"first_step": "skip records whose sha256 already sits in data/atlas-reviewed/manifest.json", "idea": "incremental audits keyed by SKILL.md SHA-256"}

### `app:tikplayer`
- **P1 المهندس الصارم:** Never built: there is no wrapper and no CI job, so nobody knows whether it compiles. · `test_verdict` {"ran": "not run (no JDK/Android SDK here, and the folder has no Gradle wrapper)", "status": "none"}
- **P2 المستخدم المصري الجديد:** README is clear; the app itself opens on demo videos from the internet. · `first_minute` {"clarity": 4, "would_say": "عايز أشوف الريلز بتاعتي على الموبايل زي تيك توك"}
- **P3 محامي الشيطان:** Low risk, but carries an INTERNET permission only for demo clips. · `keep_or_kill` {"decision": "keep", "why": "owner project; phone preview of reels"}
- **P4 المعماري:** Apps are discoverable only through a catalog card. · `wiring` {"overlaps": ["app:virtualcam"], "should_call": []}
- **P5 المبتكر:** It can show how a reel looks; it cannot show what the Reels UI will cover. · `ten_x` {"first_step": "add a safe-zone overlay toggle to item_video.xml", "idea": "a KOSIF preview player: open a render from the desktop on the phone with Reels safe-zone overlays"}

### `script:tell_scan`
- **P1 المهندس الصارم:** Well covered by a script-style runner, but that runner is not in CI. · `test_verdict` {"ran": "python3 -I .claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py -> 62/62 passed", "status": "covered"}
- **P2 المستخدم المصري الجديد:** Clear output, but its label says 'overused AI word', which reads as an authorship verdict the docstring forbids. · `first_minute` {"clarity": 4, "would_say": "شوف النص ده فيه كلام شكله مكتوب بالذكاء الاصطناعي؟"}
- **P3 محامي الشيطان:** Its rule list mirrors references/humanizer.md by hand. · `keep_or_kill` {"decision": "keep", "why": "the only Arabic stock-phrase scanner here"}
- **P4 المعماري:** Scan -> rewrite -> gate is one loop split over two tools. · `wiring` {"overlaps": ["script:anchor_gate"], "should_call": ["script:anchor_gate"]}
- **P5 المبتكر:** It finds; it does not help fix. · `ten_x` {"first_step": "emit a 'suggest' field for strong tells in --json output", "idea": "suggest the rewrite for each strong tell and verify it with anchor_gate"}

### `script:build_chapters`
- **P1 المهندس الصارم:** Determinism is checked by check_skill, but the never-overwrite guard is not. · `test_verdict` {"ran": "check_skill.py chapters check (imports build_chapters and compares output)", "status": "partial"}
- **P2 المستخدم المصري الجديد:** Usage is clear for maintainers; the examples assume you are inside scripts/. · `first_minute` {"clarity": 4, "would_say": "حدّث فصول القدرات بعد ما ضفت أداة"}
- **P3 محامي الشيطان:** Three manual follow-up steps after hub.py build are easy to forget. · `keep_or_kill` {"decision": "keep", "why": "check_skill and CI depend on it"}
- **P4 المعماري:** Part of a four-step build chain run by hand. · `wiring` {"overlaps": ["script:hub", "script:capability_graph", "script:capability_atlas"], "should_call": []}
- **P5 المبتكر:** Committed generated files are churn. · `ten_x` {"first_step": "measure which references/powers/*.md files are actually opened", "idea": "no committed chapters: render them on demand from the JSON"}

### `script:anchor_gate`
- **P1 المهندس الصارم:** Covered with exit codes, by a runner that CI never runs. · `test_verdict` {"ran": "python3 -I .claude/skills/kosif-superpowers/proofs/general-writing/test_writing.py -> 62/62 passed (incl. exit codes 0/2/64)", "status": "covered"}
- **P2 المستخدم المصري الجديد:** Excellent docstring with exit codes; the --help description is English only. · `first_minute` {"clarity": 4, "would_say": "اتأكد إن الأرقام والأسماء ما اتغيرتش بعد ما عدّلت النص"}
- **P3 محامي الشيطان:** Ambiguous Arabic words are skipped by design, so a dropped 'نص ساعة' passes silently. · `keep_or_kill` {"decision": "keep", "why": "a cheap factual guard for every rewrite"}
- **P4 المعماري:** Shares a test runner and a loop with tell_scan. · `wiring` {"overlaps": ["script:tell_scan"], "should_call": []}
- **P5 المبتكر:** The same anchors matter in translation. · `ten_x` {"first_step": "add --mode translate that ignores month/weekday language but keeps numbers and names", "idea": "a translation gate: numbers, names and quotes survive EN<->AR translation"}

### `app:instagram-link-collector`
- **P1 المهندس الصارم:** Parses, but its link parser is buried in DOM code and untested. · `test_verdict` {"ran": "node --check apps/instagram-link-collector/collector.js (OK)", "status": "none"}
- **P2 المستخدم المصري الجديد:** Best README in the batch: Egyptian Arabic, steps, limits and privacy. · `first_minute` {"clarity": 5, "would_say": "عايز كل روابط الريلز من حساب إنستجرام"}
- **P3 محامي الشيطان:** When Instagram changes its DOM, it finishes with an empty list and no explanation. · `keep_or_kill` {"decision": "keep", "why": "lists a profile's links without touching cookies"}
- **P4 المعماري:** Five Instagram units and no single map of which does what. · `wiring` {"overlaps": ["skill:kosif-instagram-discovery", "skill:kosif-instagram-video-research", "script:instagram_finder", "script:instagram_reference_bridge"], "should_call": ["script:instagram_finder"]}
- **P5 المبتكر:** The collected links stop at a text file. · `ten_x` {"first_step": "save a .json next to the .txt with handle, page and collected_at", "idea": "one click from a profile to the research library"}

## كل المقترحات / all proposals

| # | الوحدة | المقترح | الفئة | الشدة/الجهد | يتفق | الدرجة |
|---|---|---|---|---|---|---|
| 1 | `script:anchor_gate`, `script:tell_scan` | Run the 62-check writing runner in CI | test | high/S | 1 | 4.25 |
| 2 | `script:creative_external_search` | Arabic key 'قص' fires inside 'قصة' | bug | high/S | 1 | 4.25 |
| 3 | `script:atlas_audit_synthesis` | UTF-8 REA files are silently dropped | bug | high/S | 1 | 4.0 |
| 4 | `script:creative_reasoning_bridge` | Add a two-step usage line | docs | high/S | 1 | 4.0 |
| 5 | `tool:a-shell` | Add a smoke test for the a-Shell script | test | high/S | 1 | 4.0 |
| 6 | `app:instagram-link-collector` | Five Instagram units without one map | duplicate | high/S | 1 | 3.5 |
| 7 | `script:color_media` | Colour media tests skip silently without opencv | test | medium/S | 2 | 2.7 |
| 8 | `script:atlas_audit_synthesis` | Add a unit test for atlas_audit_synthesis | test | medium/S | 1 | 2.4 |
| 9 | `script:atlas_audit_synthesis` | Add usage and flag help | docs | medium/S | 1 | 2.4 |
| 10 | `script:creative_external_search` | Arabic and Chinese print as \u escapes | arabic | medium/S | 1 | 2.4 |
| 11 | `app:instagram-link-collector` | Extract and test the link parser | test | medium/S | 1 | 2.1 |
| 12 | `script:creative_reasoning_bridge` | CLI refusal paths are untested | test | medium/S | 1 | 2.1 |
| 13 | `script:tell_scan` | Label 'overused AI word' contradicts the disclaimer | ux | medium/S | 1 | 2.1 |
| 14 | `tool:a-shell` | Top of the script is a changelog, not a how-to | ux | medium/S | 1 | 2.1 |
| 15 | `script:atlas_audit_synthesis` | Report hard-codes date, totals and reviewed examples | docs | high/M | 1 | 2.0 |
| 16 | `app:tikplayer` | Opens on network demo videos with fake comments | ux | medium/S | 1 | 1.8 |
| 17 | `script:creative_reasoning_bridge` | No --force: re-running the same command fails | ux | medium/S | 1 | 1.8 |
| 18 | `app:tikplayer` | TikPlayer has never been built | test | high/M | 1 | 1.75 |
| 19 | `script:build_chapters` | Chain hub build with chapters, graph and atlas | architecture | medium/M | 2 | 1.57 |
| 20 | `app:instagram-link-collector` | Export JSON for the research library | feature | medium/S | 1 | 1.5 |
| 21 | `app:instagram-link-collector` | Silent empty result after a DOM change | ux | medium/S | 1 | 1.5 |
| 22 | `script:anchor_gate` | Say which words were not checked | ux | medium/S | 1 | 1.5 |
| 23 | `script:creative_reasoning_bridge` | Document the audio -> storyboard chain in one place | architecture | medium/S | 1 | 1.5 |
| 24 | `tool:a-shell` | Say when to use a-Shell vs desktop downloaders | duplicate | medium/S | 1 | 1.5 |
| 25 | `script:creative_external_search` | Merge creative_external_search into source_scout | duplicate | medium/M | 2 | 1.19 |
| 26 | `script:build_chapters` | Test the never-overwrite guard | test | medium/M | 1 | 0.9 |
| 27 | `tool:a-shell` | Versioned filename breaks every link on release | architecture | medium/M | 1 | 0.9 |
| 28 | `app:tikplayer` | Reels safe-zone overlay | feature | medium/M | 1 | 0.75 |
| 29 | `script:anchor_gate` | One command for the scan-rewrite-gate loop | architecture | medium/M | 1 | 0.75 |
| 30 | `script:anchor_gate` | Translation mode | feature | medium/M | 1 | 0.75 |
| 31 | `script:atlas_audit_synthesis` | Make it a subcommand of atlas_body_audit | architecture | medium/M | 1 | 0.75 |
| 32 | `script:color_media` | Time-lapse export from the stroke record | feature | medium/M | 1 | 0.75 |
| 33 | `script:creative_external_search` | Rank by usability, not stars | feature | medium/M | 1 | 0.75 |
| 34 | `script:tell_scan` | One command for the scan-rewrite-gate loop | architecture | medium/M | 1 | 0.75 |
| 35 | `script:creative_external_search` | No usage line in the docstring | docs | low/S | 1 | 0.7 |
| 36 | `app:tikplayer` | Add an apps/README.md index | docs | low/S | 1 | 0.6 |
| 37 | `script:build_chapters` | Examples assume cwd = scripts/ | docs | low/S | 1 | 0.6 |
| 38 | `script:color_media` | Say opencv is needed in --help | docs | low/S | 1 | 0.6 |
| 39 | `app:instagram-link-collector` | Give the download command from the repo root | ux | low/S | 1 | 0.5 |
| 40 | `app:tikplayer` | INTERNET permission only for demo clips | security | low/S | 1 | 0.5 |
| 41 | `script:anchor_gate` | Arabic line in --help | arabic | low/S | 1 | 0.5 |
| 42 | `script:color_media` | Register color_media as a library of portrait_pipeline | architecture | low/S | 1 | 0.5 |
| 43 | `script:tell_scan` | Rule list duplicated with humanizer.md | duplicate | low/M | 1 | 0.25 |
| 44 | `tool:a-shell` | Named Studio presets | feature | low/M | 1 | 0.25 |
| 45 | `script:atlas_audit_synthesis` | Incremental audit by SHA-256 | feature | low/M | 1 | 0.2 |
| 46 | `script:creative_reasoning_bridge` | Render an animatic | feature | low/M | 1 | 0.2 |
| 47 | `script:tell_scan` | Suggestions per tell | feature | low/M | 1 | 0.2 |
| 48 | `script:build_chapters` | Render chapters on demand | architecture | low/L | 1 | 0.07 |

## التغطية / coverage

راجع المجلس 10 من 197 وحدة (5.1%): skill 0/5 · script 7/159 · app 2/3 · tool 1/11 · playbook 0/17 · workflow 0/2. لم تُراجع بعد 187، وتغيّرت بعد مراجعتها 0، ومحجوزة لتشغيل مفتوح 0. الدفعة التالية: `python3 .claude/skills/kosif-superpowers/scripts/self_council.py plan --batch 10 --dir out/self-council/<run>`.

## ملاحظات المشغّل / operator notes (written by hand after the generated report)

**How this pass ran.** `inventory` → `plan --batch 10 --dir out/self-council/first-pass-20261024` → five reviews ingested with `--simulated` → `report`. This session had no subagent tool, so Claude wrote all five voices in one context. Every finding cites a file that was opened, and the commands it quotes (`sh -n`, `--help`, `node --check`, the unittest runs, the `قصة كرتون` search) were really run. The voices are still not independent. Re-run this batch with five parallel agents before acting on the L-effort ideas.

**Implemented from the top list (3 of 10).** Each is small and each was verified:
1. #3 `script:atlas_audit_synthesis`: REA files that were not UTF-16 were silently dropped. `scripts/atlas_audit_synthesis.py` now reads UTF-16 first, as before, and falls back to UTF-8 (`_read_rea`), so existing UTF-16 files behave exactly as they did.
2. #8 `script:atlas_audit_synthesis`: new `evals/test_atlas_audit_synthesis.py`, with UTF-16, UTF-8 and broken REA files. It fails on the old script (`(1, 1, 1, 2) != (1, 1, 2, 5)`) and passes on the new one. It matches CI's `test_*atlas_*.py` step.
3. #4 `script:creative_reasoning_bridge`: the docstring (and so `--help`) now shows the two-step chain `audio_cue_mapper.py … --out cues.json` → `creative_reasoning_bridge.py cues.json --out … --report …`. `test_creative_intelligence.py` still passes.

These two units now show as `stale` in the ledger because their content changed, and the next `plan` will offer them for re-review.

**Not implemented (needs the owner, or touches protected files).**
- #1 adds a CI step to `.github/workflows/ci.yml`.
- #2 (the Arabic substring match in `creative_external_search.py`) changes search results, and prefixed forms such as «للمونتاج» need care.
- #5, #6, #9 and #10 are safe follow-ups for the next session.

**What the pass found in the self-council tool itself.** Five of the ten units were picked as `NO_TEST` but do have tests:
- `tell_scan` and `anchor_gate` are covered by `proofs/general-writing/test_writing.py`.
- `creative_reasoning_bridge` and `creative_external_search` are tested through `import x as y`.
- `color_media` is tested through `portrait_pipeline.py`.

Two more signals were wrong: `a-shell` showed as unregistered (a folder tool), and as `NO_USAGE` because its usage lines are `c --studio`. `scripts/self_council.py` now does four things differently:
- parses `import x as y`;
- scans `proofs/**/test_*.py`;
- counts the tests that `data/tools.json` names (a new `has_test: registered` value);
- matches folder tools to the registry and reads `cmd --flag` lines as usage.

`evals/test_self_council.py` covers each of these fixes. The batch itself was not re-picked: all ten units still had real weaknesses (no CI run, no usage line, silent data loss, never built), and the ledger records them as reviewed.
