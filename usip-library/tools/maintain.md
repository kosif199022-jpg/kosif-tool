# أدوات المجال `maintain` (12 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `build-chapters` — مولّد فصول العائلات / Family Chapter Generator

| الحقل | القيمة |
|---|---|
| المسار | `scripts/build_chapters.py` (جذر: skill) |
| المجال | `maintain` |
| الدليل | `untested` |
| العائلات | `self-discovery`, `verification-evals` |

**ما تفعله:** يعيد توليد الفصل ثنائي اللغة references/powers/<family>.md لكل عائلة قدرات عامة (غير عائلات الموشن) من ملف data/powers/<family>.json. ناتجه حتمي، ولا يمس فصول الموشن الثلاثين المكتوبة يدويًا. أما الخيار --check فيبلغ عن الفصول القديمة أو المفقودة أو اليتيمة دون أن يكتب شيئًا.

**What it does:** Regenerates the bilingual Markdown chapter references/powers/<family>.md for every general (non-motion) power family from data/powers/<family>.json. Output is deterministic, and it never touches the 30 hand-made motion chapters. --check reports stale, missing or orphaned chapters without writing.

#### متى تُستدعى

- «ولّد فصول العائلات من ملفات JSON بعد ما عدّلت القدرات»
- «وش فيها الفصول طالعة قديمة في check_skill؟ حدّثها»
- «حدّث ملف references/powers/thinking-core.md بس»
- «regenerate the general family chapters after editing data/powers»
- «check whether the generated power chapters are stale»

#### الأوامر

- **build**: Writes every general chapter whose rendered text changed. A chapter without the generated marker is refused, never overwritten. Prints 'wrote …' lines and a summary, and exits 1 if any chapter was refused or any family JSON failed to parse.
  - `python3 scripts/build_chapters.py`
- **--check**: Writes nothing. Lists missing, stale or orphaned generated chapters and exits 1 if there is any problem; otherwise prints 'N general chapter(s) up to date'.
  - `python3 scripts/build_chapters.py --check`
- **--family**: Limits the run (build or check) to one family stem; orphan detection and pruning are off. Exits 2 if no general family has that name.
  - `python3 scripts/build_chapters.py --family thinking-core --check`
- **--out**: Writes the chapters into another folder instead of references/powers/ (for tests and previews).
  - `python3 scripts/build_chapters.py --family thinking-core --out ./out/`
- **--force**: Overwrites a chapter even when it lacks the generated marker, which replaces a hand-written chapter.
  - `python3 scripts/build_chapters.py --family thinking-core --force`
- **--prune**: Also deletes generated chapters whose family JSON no longer exists. Off with --family; with --check orphans are only reported.
  - `python3 scripts/build_chapters.py --prune`
- **--quiet**: Suppresses the 'wrote …' lines and the summary in build mode, and the 'up to date' line in --check mode; problems are still printed.
  - `python3 scripts/build_chapters.py --check -q`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: A plain run rewrites the tracked generated chapters in references/powers/; --force overwrites hand-written chapters and --prune deletes files, so confirm before using either.
- الحدود: It only formats existing JSON records into Markdown, without checking the claims inside them, and it never regenerates the 30 motion chapters.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`
- مرجع: `.claude/skills/kosif-superpowers/references/verification.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:build-chapters --evidence <ملف>`.

### `catalog-evidence-audit` — تدقيق أدلة الكتالوج / Catalog Evidence Audit

| الحقل | القيمة |
|---|---|
| المسار | `scripts/catalog_evidence_audit.py` (جذر: skill) |
| المجال | `maintain` |
| الدليل | `tested-elsewhere` |
| العائلات | `verification-evals`, `qa-verification`, `self-discovery` |

**ما تفعله:** يفحص كل سجل قدرة في data/powers/*.json دون تشغيل أي شيء، بحثًا عن المعرّفات المكررة والسجلات المعطوبة ومدى تغطية روابط الإثبات. ويكتفي بالتحقق من وجود المراجع المحلية 'kosif-tool/...'، ويُحصي الحالات ونطاقات الإثبات المعلنة.

**What it does:** Statically audits every power record in data/powers/*.json for duplicate ids, malformed records and proof-link coverage. It checks only whether local 'kosif-tool/...' references exist and counts the claimed statuses and proof scopes.

#### متى تُستدعى

- «افحص كتالوج القدرات وشوف فيه سجلات مكررة أو روابط إثبات ناقصة»
- «كم قدرة في الكتالوج ليها دليل محلي فعلًا؟»
- «راجع صحة بيانات القدرات قبل ما ندمج الفرع»
- «audit the powers catalog for duplicate ids and broken proof links»
- «how many catalog entries have local evidence vs unverified links»
- «run a catalog health check before release»

#### الأوامر

- **audit**: Prints kosif.catalog.evidence-audit.v1 JSON for the skill that contains the script: records_examined, unique_ids, families_examined, statuses_claimed, proof_scopes_claimed, proof_links counts, record_integrity_errors (first 30), missing_local_samples (first 12), assessment, executes_external_code=false and downloads=false. Exits 1 if there are integrity errors, otherwise 0.
  - `python3 scripts/catalog_evidence_audit.py`
- **--skill**: Audits the skill folder at the given path (the repo root is taken as three levels above, i.e. skill.parents[2]).
  - `python3 scripts/catalog_evidence_audit.py --skill .`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Checks only that local reference paths exist, never runs a capability, and leaves every URL, sibling-repo or archive reference unverified, so a clean report does not prove that anything works.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_catalog_evidence_audit.py`
- مرجع: `.claude/skills/kosif-superpowers/references/claude-auto-local-first.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/discover.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:catalog-evidence-audit --evidence <ملف>`.

### `check-skill` — فحص سلامة المهارة / Skill Health Check

| الحقل | القيمة |
|---|---|
| المسار | `scripts/check_skill.py` (جذر: skill) |
| المجال | `maintain` |
| الدليل | `untested` |
| العائلات | `verification-evals`, `self-discovery`, `security-safety` |

**ما تفعله:** يفحص مهارة kosif-superpowers بأربعة عشر فحصًا لا تكتب شيئًا: ترويسة ملف SKILL.md، وسجلات القدرات، ومسارات الأدلة، وروابط Markdown النسبية، وعناوين المحتويات، والفصول المولَّدة، وعلامة العدّادات، وأسماء النماذج، والأسرار ومسارات الجلسات المسرَّبة، وملف evals/evals.json، وسجل الأدوات data/tools.json مع الملفات المولَّدة منه، وتطابق أعداد القدرات المذكورة في الوثائق الرئيسية، وبنية بروتوكول USIP (نواة PROTOCOL.md وملاحق references/protocol/)، وترتيب المراجع (كل ملف تحت references/ في قسم واحد من data/skill_layout.json). ويستطيع أيضًا تشغيل تقييمات التوجيه، ثم يطبع تقريرًا نصيًا أو بصيغة JSON ويخرج بالرمز 1 عند وجود أي خطأ.

**What it does:** Validates the kosif-superpowers skill with 14 read-only checks: SKILL.md frontmatter, power records, proof paths, relative Markdown links, contents headings, generated chapters, the counts marker, model names, secrets and leaked session paths, evals/evals.json, the data/tools.json registry with its generated hub files, power-count drift in the entry docs, the USIP protocol structure (PROTOCOL.md core and references/protocol/), and the reference layout (every file under references/ in exactly one section of data/skill_layout.json). It can also run the routing evals, then prints a text or JSON report and exits 1 on any error.

#### متى تُستدعى

- «افحص المهارة قبل ما نعمل commit»
- «شيك على المهارة وشوف فيه روابط مكسورة أو أعداد غلط»
- «تأكد إن عدادات القدرات في SKILL.md مطابقة للكتالوج»
- «validate the kosif-superpowers skill before packaging»
- «run the routing evals and tell me the pass rate»
- «print the counts marker line for SKILL.md»

#### الأوامر

- **check**: Runs all 14 checks and prints 'LEVEL [check] message' lines plus a summary such as 'check_skill: 14 checks · N error(s) · M warning(s) → OK/FAIL'. Exits 1 on any error.
  - `python3 scripts/check_skill.py`
- **--strict**: Same checks, but warnings also fail the run (exit 1).
  - `python3 scripts/check_skill.py --strict`
- **--json**: Prints one JSON object {ok, errors, warnings, checks, items[{level, check, message}]} instead of text lines.
  - `python3 scripts/check_skill.py --json`
- **--evals**: Runs all checks, then the routing evals: for each case in evals/evals.json with a routing block it calls powers.suggest in-process on the query and passes when one of expect_any's family prefixes is in the top K (plus expect_all, expect_domain and motion_output when set). Prints PASS/FAIL/SKIP per case and the pass rate; exits 1 if the checks fail or routing falls below --min-pass.
  - `python3 scripts/check_skill.py --evals`
- **--min-pass**: Sets the routing pass rate that --evals requires (default 0.8).
  - `python3 scripts/check_skill.py --evals --min-pass 0.9`
- **--print-counts**: Prints the '<!-- counts: powers=… families=… … -->' marker computed from the live catalog and exits 0 without running any checks.
  - `python3 scripts/check_skill.py --print-counts`
- **--verbose**: Also prints info lines: record, proof-path, link, chapter, eval and registry counts.
  - `python3 scripts/check_skill.py -v`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: It checks structure, links, counts and registry consistency only: the routing evals test search ranking, not whether any power works, and proofs outside this checkout are skipped rather than verified.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:check-skill --evidence <ملف>`.

### `package-skill` — تحزيم المهارة للرفع إلى claude.ai / Skill Packager for claude.ai

| الحقل | القيمة |
|---|---|
| المسار | `scripts/package_skill.py` (جذر: skill) |
| المجال | `maintain` |
| الدليل | `tested-here` |
| العائلات | `code-engineering`, `verification-evals` |

**ما تفعله:** يتحقق من المهارة بالأداة check_skill.py، ثم يضغطها ضغطًا حتميًا في ملف kosif-superpowers.skill لرفعه إلى claude.ai. يضم الأرشيف مجلدًا علويًا واحدًا وملف SKILL.md واحدًا يُستبدل وصفه بالوصف القصير claude_ai_description (200 حرف على الأكثر). يستبعد dist/ ومجلدات الذاكرة المؤقتة وvendor/ وevals/، ويستبعد الوسائط أيضًا مع الخيار --lite، ثم يتحقق من الأرشيف الناتج.

**What it does:** Validates the skill with check_skill.py, then zips it deterministically into kosif-superpowers.skill for upload to claude.ai. The archive has a single top folder and one SKILL.md, whose description is replaced by the ≤200-character claude_ai_description. dist/, caches, vendor/, evals/ and (with --lite) media are left out, and the finished archive is re-verified.

#### متى تُستدعى

- «حزّم المهارة عشان أرفعها على claude.ai»
- «اعمل ملف .skill خفيف من غير صور وفيديو»
- «أبي ملف zip للمهارة أرفعه في Claude»
- «package the skill for upload to claude.ai»
- «list which files would go into the skill zip»

#### الأوامر

- **package**: Runs check_skill.py in-process (stops on errors), then writes dist/kosif-superpowers.skill inside the skill (dist/ is git-ignored). Prints the file count, unpacked and zipped sizes, and an upload hint.
  - `python3 scripts/package_skill.py`
- **--lite**: Leaves out images, audio and video (all text and fonts stay) and writes kosif-superpowers-lite.skill.
  - `python3 scripts/package_skill.py --lite`
- **--out**: Writes to another folder or exact .skill/.zip file name. A destination inside the skill folder other than dist/ is refused (exit 1).
  - `python3 scripts/package_skill.py --lite -o ~/out/`
- **--with-evals**: Keeps evals/ in the package (normally excluded as dev-only).
  - `python3 scripts/package_skill.py --lite --with-evals -o ~/out/kosif-superpowers.skill`
- **--no-check**: Skips the check_skill.py validation step and packages anyway.
  - `python3 scripts/package_skill.py --lite --no-check -o ~/out/`
- **--list**: Prints every file that would be packed plus the skip counts by reason, and writes nothing.
  - `python3 scripts/package_skill.py --list`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes a .skill zip (default dist/ inside the skill; -o can write anywhere outside it). It packs every non-excluded file on disk, untracked ones included, so review --list before sharing the archive.
- الحدود: It only builds the upload zip and never uploads anything; no claude.ai size cap is documented, so whether claude.ai accepts a large package is untested.

#### الاختبارات والأدلة

- `tests/test_superpowers_unified.py`
- مرجع: `README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:package-skill --evidence <ملف>`.

### `rea-superpowers-map` — خريطة سوبر باور بمنهج REA / Superpowers map, REA approach

| الحقل | القيمة |
|---|---|
| المسار | `scripts/rea_superpowers_map.py` (جذر: skill) |
| المجال | `maintain` |
| الدليل | `tested-here` |
| العائلات | `self-discovery`, `software-investigation` |

**ما تفعله:** يرسم خريطة المهارة كما يرسم REA شجرة مصدر لا يشغّلها: جرد ببصمات المحتوى، وحواف الاستيراد والاستدعاء في بايثون، وحواف جافاسكربت من إيصال REA المحفوظ، وروابط كل سكربت بأداته واختباراته وخطوات CI والقدرات والعائلات، ثم الفجوات (سكربتات يتيمة أو بلا اختبار، ملفات أدوات مفقودة، مراجع خارج فهرس التخطيط، روابط مكسورة، عائلات بلا أداة قابلة للتشغيل) وتغطية الأطلس لكل موضوع.

**What it does:** Maps this skill the way REA maps a source tree it does not execute: a content-addressed inventory, Python import and invoke edges (ast), REA's JavaScript edges from its committed receipt, links from every script to its tools.json entry, tests, CI steps, powers and families, the gaps (orphan or untested scripts, missing tool files, unlisted references, broken links, families without a runnable tool) and Atlas safe-core coverage per theme.

#### متى تُستدعى

- «اعمل خريطة كاملة لسوبر باور: البنية والتبعيات والفجوات»
- «ايه السكربتات اللي ملهاش اختبار أو مش متسجلة؟»
- «Map the superpowers skill: structure, dependency graph, gaps and Atlas coverage»
- «Which scripts are orphaned or untested, and which families have no runnable tool?»

#### الأوامر

- **build**: Writes data/superpowers_rea_map.json, references/superpowers-rea-map.md and the self-contained references/superpowers-rea-map.html; --check exits 1 when they are stale.
  - `python3 scripts/rea_superpowers_map.py build`
- **stats**: Structure, counts, gap counts, Atlas coverage and the REA receipt summary.
  - `python3 scripts/rea_superpowers_map.py stats --json`
- **gaps**: Lists gap rows, optionally one kind.
  - `python3 scripts/rea_superpowers_map.py gaps --kind script_untested`
- **node**: One script, tool id, family or path with its edges, tools, tests, powers and gaps; unknown exits 2.
  - `python3 scripts/rea_superpowers_map.py node atlas_5000`
- **ingest-rea**: Turns `rea import-reference-source <skill dir> --format json` output (summary and full) into the trimmed receipt proofs/rea-superpowers-map/receipt.json; foreign JSON is refused.
  - `python3 scripts/rea_superpowers_map.py ingest-rea --summary sp_sum.json --graph sp_full.json`
- **self-test**: Offline synthetic tree with known roles, edges and gaps; prints pass or the failed checks.
  - `python3 scripts/rea_superpowers_map.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- optional: rea (only to refresh the receipt, run separately)
- الأمان: read-only
- الموافقة: None needed for build/stats/gaps/node; refreshing the receipt runs REA separately on the user's own tree.
- الحدود: Import edges are static (dynamic imports are invisible); a test reference is a name or import, not measured coverage; JavaScript edges are as of the receipt's git head; Atlas covered means cited, not run.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_rea_superpowers_map.py`
- مرجع: `.claude/skills/kosif-superpowers/references/superpowers-rea-map.md`
- مرجع: `.claude/skills/kosif-superpowers/references/rea-superpowers-frontier-20261023.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:rea-superpowers-map --evidence <ملف>`.

### `relabel-proofs` — إعادة تصنيف نطاق الأدلة / Proof Scope Relabeler

| الحقل | القيمة |
|---|---|
| المسار | `scripts/relabel_proofs.py` (جذر: skill) |
| المجال | `maintain` |
| الدليل | `untested` |
| العائلات | `verification-evals`, `self-discovery` |

**ما تفعله:** يعيد حساب الحقل proof_scope لكل سجل قدرة بحسب المكان الذي تشير إليه أدلته على هذا الجهاز (repo ثم session ثم archive ثم sibling ثم receipt ثم style ثم url ثم missing/none)، ويعيد كتابة ملفات data/powers/*.json في مكانها. أما مع الخيار --check فيكتفي بالإبلاغ عن عدد السجلات التي ستتغير.

**What it does:** Recomputes the proof_scope field of every power record from where its proof entries resolve on this machine (repo > session > archive > sibling > receipt > style > url > missing/none) and rewrites data/powers/*.json in place. With --check it only reports how many records would change.

#### متى تُستدعى

- «حدّث proof_scope لكل القدرات»
- «check_skill بيقول ✅ محتاج proof_scope، صلّحها»
- «كم قدرة مثبتة بدليل موجود داخل المستودع؟»
- «recompute proof_scope on every power record»
- «check whether any proof scope labels are out of date»

#### الأوامر

- **relabel**: Rewrites every data/powers/*.json that has a record whose proof_scope differs, inserting proof_scope right after proof and re-serialising the file with its detected indent. Prints the proven count by scope and 'relabelled N record(s)'; exit 0.
  - `python3 scripts/relabel_proofs.py`
- **--check**: Writes nothing. Prints the proven count by scope and 'would change N record(s)', and exits 1 when N > 0.
  - `python3 scripts/relabel_proofs.py --check`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: A run without --check rewrites data/powers/*.json in place: run --check first, and relabel only on a full kosif-tool checkout, because a partial copy relabels repo proofs as missing. --help and a mistyped flag only print usage.
- الحدود: It labels where a proof points, not whether the proof is valid: 'sibling' is assigned from the path shape alone without checking the other repository, and 'repo' only means the file exists.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:relabel-proofs --evidence <ملف>`.

### `repo-build` — مولّد ملفات أطلس الأساليب / Style Atlas Builder

| الحقل | القيمة |
|---|---|
| المسار | `tools/build.py` (جذر: repo) |
| المجال | `maintain` |
| الدليل | `untested` |
| العائلات | `self-discovery`, `story-direction-ideas` |

**ما تفعله:** يعيد توليد كل الملفات المشتقة في أطلس أساليب الموشن انطلاقًا من catalog/styles.json وcategories.json وbriefs.json: ملفي styles/<id>/SKILL.md وSTYLE.json لكل أسلوب، وملف STYLE_INDEX.md، وcatalog/playbooks.json وmeta.json وprompts_motion.json، والنسخة المنسَّقة من catalog/styles.json، وsitemap.xml، وكتلة الإحصاءات في README.md. أما الخيار --check فيكتفي بالإبلاغ عن الملفات غير المحدَّثة.

**What it does:** Regenerates every derived file of the motion style atlas from catalog/styles.json, categories.json and briefs.json: each style's styles/<id>/SKILL.md and STYLE.json, STYLE_INDEX.md, catalog/playbooks.json, meta.json, prompts_motion.json, the normalised catalog/styles.json, sitemap.xml and the stats block in README.md. --check only reports drift.

#### متى تُستدعى

- «بعد ما عدّلت catalog/styles.json ولّد ملفات الأساليب من جديد»
- «حدّث STYLE_INDEX.md وخريطة الموقع»
- «تأكد إن الملفات المشتقة للأطلس محدّثة»
- «regenerate the style SKILL.md files and STYLE_INDEX after a catalog change»
- «check that the derived atlas files are up to date before CI»

#### الأوامر

- **build**: Rewrites only the derived files whose content changed and prints 'regenerated N files (S styles, P playbooks, B briefs)'.
  - `python3 tools/build.py`
- **--check**: Writes nothing. Prints 'derived files up to date' (exit 0), or lists up to 20 out-of-date paths (exit 1).
  - `python3 tools/build.py --check`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: A plain run overwrites tracked files across the repo (catalog/styles.json, every styles/<id>/SKILL.md and STYLE.json, STYLE_INDEX.md, sitemap.xml and the README.md stats block); run --check first.
- الحدود: It generates text guides and indexes from catalog metadata only: it never fetches or inspects the referenced videos and does not validate the catalog (tools/validate.py does that).

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `AGENTS.md`
- مرجع: `README.md`
- مرجع: `CLAUDE.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-build --evidence <ملف>`.

### `repo-check-originality` — فاحص أصالة الملفات الإبداعية / Brief originality checker

| الحقل | القيمة |
|---|---|
| المسار | `tools/check_originality.py` (جذر: repo) |
| المجال | `maintain` |
| الدليل | `untested` |
| العائلات | `qa-verification`, `verification-evals` |

**ما تفعله:** يقارن النص الإنجليزي لكل ملف إبداعي يبدأ معرّفه بـ pm- في ملفات JSON بالوصف العام المحفوظ لصاحب المرجع (<slug>.txt)، ويبلّغ عن كل سلسلة مشتركة من N كلمات متتالية (6 افتراضيًا)، وينتهي برمز الخروج 1 إذا رُصد أي تطابق.

**What it does:** Compares the English text of each pm- brief in batch JSON files with the creator's saved public description (<slug>.txt), reports every shared run of N consecutive words (default 6) and exits 1 when any brief is flagged.

#### متى تُستدعى

- «تأكد إن البريفات مش منقولة من وصف المصدر»
- «افحص أصالة الملفات الإبداعية قبل الاستيراد»
- «Check briefs for wording copied from the source descriptions»
- «Flag 6-word overlaps between our briefs and the creator text»

#### الأوامر

- **check**: For each brief whose id starts with pm- and that has a matching <slug>.txt in --texts, it lists the distinct shared 6-word sequences and prints the first 5. The windows overlap, so one long copied passage gives many hits. It ends with a 'checked N briefs, flagged M' line and exits 1 if anything is flagged. Both flags are required (exit 2 without them).
  - `python3 tools/check_originality.py --briefs ./briefs/ --texts ./source-texts/`
- **--ngram**: Sets the shared-run length that counts as reuse.
  - `python3 tools/check_originality.py --briefs ./briefs/ --texts ./source-texts/ --ngram 8`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: It finds exact lower-case n-gram overlaps in the English fields only, joined into one string. It does not check paraphrase, the Arabic fields, briefs without a matching <slug>.txt or briefs whose id does not start with pm-, and a missing or misspelled folder passes silently.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/qa-verification.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-check-originality --evidence <ملف>`.

### `repo-import-briefs` — استيراد الملفات الإبداعية / Creative brief importer

| الحقل | القيمة |
|---|---|
| المسار | `tools/import_briefs.py` (جذر: repo) |
| المجال | `maintain` |
| الدليل | `untested` |
| العائلات | `qa-verification`, `story-direction-ideas` |

**ما تفعله:** يتحقق من ملفات JSON التي تضم دفعات من الملفات الإبداعية بصيغة {"briefs": [...]}، ويكتب styles/<id>/BRIEF.md لكل ملف مقبول، ويدمج حقول الملخص في catalog/styles.json وcatalog/prompts_motion.json وcatalog/briefs.json وفي ملف STYLE.json لكل أسلوب.

**What it does:** Validates batch JSON files of creative briefs ({"briefs": [...]}), writes styles/<id>/BRIEF.md for each accepted brief, and merges the brief summary fields into catalog/styles.json, catalog/prompts_motion.json, catalog/briefs.json and each STYLE.json.

#### متى تُستدعى

- «استورد ملفات البريف الجديدة للكتالوج»
- «عندي دفعة briefs بصيغة JSON، ضيفها للأطلس»
- «أبي أتحقق من صيغة البريفات قبل ما أدخلها»
- «Import a batch of creative briefs into the atlas»
- «Validate brief JSON files and write BRIEF.md for each style»

#### الأوامر

- **import**: Reads every *.json file in the folder and exits 2 if there are none. It skips unknown ids, briefs with missing keys or wrong types, and invalid JSON files. Briefs with only value issues (difficulty outside 1-5, unknown stack, keyword or scene count out of range, unreadable aspect) are still imported. Issues go to stderr and 'imported N briefs; M total' to stdout. It rewrites all catalog files, even when nothing was imported, and exits 0.
  - `python3 tools/import_briefs.py ./briefs/`
- **--strict**: Skips every brief that has any issue, still writes the valid ones, and exits 1 if any brief was invalid or had an unknown id. On an invalid JSON file it stops at once with exit 1. Briefs from earlier files already have BRIEF.md and STYLE.json written by then, but the catalog files have not been updated.
  - `python3 tools/import_briefs.py ./briefs/ --strict`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: Rewrites tracked catalog files in the repository (catalog/briefs.json, catalog/styles.json, catalog/prompts_motion.json, styles/<id>/BRIEF.md and STYLE.json). Briefs must be original writing, so run tools/check_originality.py on the batch first.
- الحدود: It checks only shape and simple ranges, not originality or accuracy; without --strict it imports briefs that fail the range checks, it accepts only ids already in the catalog, and it does not rebuild SKILL.md or STYLE_INDEX.md (run build.py).

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `README.md`
- مرجع: `AGENTS.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-import-briefs --evidence <ملف>`.

### `repo-sync-catalog` — مزامنة الكتالوج مع PromptsMotion / PromptsMotion catalog sync

| الحقل | القيمة |
|---|---|
| المسار | `tools/sync_catalog.py` (جذر: repo) |
| المجال | `maintain` |
| الدليل | `untested` |
| العائلات | `web-research`, `data-analysis` |

**ما تفعله:** يقرأ فهرس مكتبة PromptsMotion العامة وصفحات تفاصيلها ويخزّنها مؤقتًا في ‎.cache/promptsmotion/‎، ثم يستخرج البيانات الوصفية الواقعية فقط، ويعيد كتابة catalog/styles.json وcatalog/prompts_motion.json وملف STYLE.json لكل أسلوب، ويضع listed=false على الإدخالات التي خرجت من الفهرس.

**What it does:** Scrapes the public PromptsMotion library index and its detail pages (cached under .cache/promptsmotion/), extracts factual metadata only, rewrites catalog/styles.json, catalog/prompts_motion.json and every styles/<id>/STYLE.json, and flags entries that have left the index with listed=false.

#### متى تُستدعى

- «حدّث كتالوج الأساليب من مكتبة PromptsMotion»
- «فيه ستايلات جديدة نزلت في المكتبة؟ زامنها مع الأطلس»
- «أبغى أعيد بناء الكتالوج من الصفحات المخزنة بدون إنترنت»
- «Sync the style catalog with the PromptsMotion library»
- «Rebuild catalog/styles.json from cached pages offline»
- «Fetch at most 20 new reference pages this run»

#### الأوامر

- **sync**: Fetches the live index from www.promptsmotion.com (falling back to the cached index if the fetch fails) and every uncached detail page (3 retries each), then rewrites the catalog files and every STYLE.json. Exits 3 if fewer than 50 cards parse, and 2 if the index cannot be fetched and no cache exists.
  - `python3 tools/sync_catalog.py`
- **--offline**: Rebuilds the catalog from .cache/promptsmotion/home.html and pages/*.html without touching the network. Index entries with no cached detail page keep their old detail fields (date, model, effort, tech), but title, creator, poster, aspect and rank still come from the cached index. Exits 2 when no cached index exists, after it has already created .cache/promptsmotion/pages/.
  - `python3 tools/sync_catalog.py --offline`
- **--refetch**: Ignores cached detail pages and downloads all of them again. It has no effect together with --offline.
  - `python3 tools/sync_catalog.py --refetch`
- **--limit/--workers**: Caps how many new detail pages are fetched this run (0 means all) and sets the number of parallel fetch threads (default 3).
  - `python3 tools/sync_catalog.py --limit 20 --workers 3`

#### المتطلبات والأمان

- binaries: python3
- network: true
- الأمان: network
- الموافقة: Contacts www.promptsmotion.com to scrape its public index and detail pages, then rewrites tracked catalog files in the repository (catalog/styles.json, catalog/prompts_motion.json, every styles/<id>/STYLE.json). As written it also drops the 'dua' style from the catalog, so review git diff before committing.
- الحدود: It parses only the site's current markup with regexes, stores metadata and links only, does not regenerate SKILL.md, STYLE_INDEX.md or briefs (build.py does), and drops every non-PromptsMotion record that is missing from its hard-coded BASE list.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `README.md`
- مرجع: `AGENTS.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-sync-catalog --evidence <ملف>`.

### `repo-validate` — فاحص سلامة أطلس الأنماط / Style atlas repository validator

| الحقل | القيمة |
|---|---|
| المسار | `tools/validate.py` (جذر: repo) |
| المجال | `maintain` |
| الدليل | `tested-here` |
| العائلات | `qa-verification`, `verification-evals` |

**ما تفعله:** يُجري 14 فحصًا لسلامة أطلس الأنماط، ويطبع تقريرًا مرقّمًا بحالات النجاح أو التحذير أو الفشل، أو تقريرًا بصيغة JSON. يتحقق من صلاحية catalog/styles.json وتفرّد معرّفاته وصيغتها، ومن صحة تصنيف catalog/categories.json، ومن حقول السجلات وقيمها المسموحة وروابط https، ومن أن الفئات معروفة وأن aspect_label يطابق الأبعاد، ومن وجود styles/<id>/SKILL.md وتطابق STYLE.json مع السجل. ويفحص كذلك المجلدات اليتيمة، وذكر كل معرّف في STYLE_INDEX.md، واتساق prompts_motion وbriefs، ووجود ملفات الأدلة، وخلو styles/ وcatalog/ من ملفات وسائط مُعاد استضافتها، وتطابق متغيرات قالبي الطلب، وإجماليات meta.

**What it does:** Runs 14 integrity checks on the style atlas and prints a numbered PASS/WARN/FAIL report or JSON. It checks that catalog/styles.json parses with unique slug ids, that catalog/categories.json is a valid taxonomy, record fields, enums and https URLs, known categories, aspect_label against the pixel size, and that styles/<id>/SKILL.md exists and STYLE.json equals the record. It also checks for orphan folders, STYLE_INDEX.md coverage, prompts_motion and briefs consistency, playbook files, rehosted media under styles/ or catalog/, matching request-template placeholders and meta totals.

#### متى تُستدعى

- «افحص سلامة المستودع بعد ما عدّلت الكتالوج»
- «شغّل الفاحص وورّني الأخطاء والتحذيرات بس»
- «هل كل استايل له SKILL.md و STYLE.json مطابق للسجل؟»
- «validate the atlas after adding a new style»
- «give me a JSON integrity report of the catalog»

#### الأوامر

- **full**: Prints the full numbered report and a summary (OK or FAIL).
  - `python3 tools/validate.py`
- **quiet**: Hides PASS lines and shows only warnings, failures and the summary.
  - `python3 tools/validate.py --quiet`
- **json**: Prints a machine-readable report: {root, failed, warned, checks:[{status,title,details}]}.
  - `python3 tools/validate.py --json`
- **root**: Validates another checkout or a test fixture; a root without catalog/ exits 1 with an error.
  - `python3 tools/validate.py --root ./other-checkout --quiet`
- **help**: Shows the options.
  - `python3 tools/validate.py --help`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: It validates only the motion style atlas (catalog/, styles/, templates/, playbooks/); it does not check the skill's power catalog, data/tools.json, code behaviour or rendered media.

#### الاختبارات والأدلة

- `tests/test_validate.py`
- `tests/test_catalog.py`
- `tests/test_cli.py`
- مرجع: `README.md`
- مرجع: `AGENTS.md`
- مرجع: `CLAUDE.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`
- مرجع: `.claude/skills/kosif-superpowers/references/verification.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-validate --evidence <ملف>`.

### `skill-layout` — خريطة ترتيب المهارة / Skill Layout Map

| الحقل | القيمة |
|---|---|
| المسار | `scripts/skill_layout.py` (جذر: skill) |
| المجال | `maintain` |
| الدليل | `tested-here` |
| العائلات | `verification-evals`, `self-discovery` |

**ما تفعله:** يحفظ ترتيب ملفات المراجع في المهارة: الملف data/skill_layout.json يضع كل ملف تحت references/ (ومعه ملفات المدخل) في قسم واحد من أحد عشر قسمًا بترتيب القراءة. يبني الخريطة المقروءة references/LAYOUT.md، ويفحصها كميزان مراجعة (لا ملف بلا قسم ولا ملف في قسمين ولا ملف مفقود ولا خريطة قديمة)، ويخبرك في أي قسم يقع الملف، ويطبع أوامر git mv التي تنقل كل قسم إلى مجلده المخطط. ولا ينقل أي ملف بنفسه.

**What it does:** Keeps the skill's reference files in order: data/skill_layout.json puts every file under references/ (and the entry documents) into exactly one of eleven sections in reading order. It builds the readable map references/LAYOUT.md, checks it like a trial balance (no unlisted, doubly listed or missing file, no stale map), says which section holds a file, and prints the git mv commands that would move each section to its planned folder. It never moves a file itself.

#### متى تُستدعى

- «وين مكان ملف المرجع ده في المهارة؟»
- «رتّب ملفات المهارة وتأكد إن كل ملف له قسم»
- «which section does cognition.md belong to?»
- «check that every new reference file is classified in the skill layout»

#### الأوامر

- **build**: Writes references/LAYOUT.md from data/skill_layout.json
  - `python3 scripts/skill_layout.py build`
- **check**: Exits 1 when a reference file has no section or two, a listed or pinned file is missing, or LAYOUT.md is stale (the same check as check_skill.py layout)
  - `python3 scripts/skill_layout.py check`
- **where**: Prints each matching file with its section
  - `python3 scripts/skill_layout.py where cognition`
- **moves**: Prints the git mv commands that move every non-pinned file to its section's target folder (a deferred, separate step); prints only
  - `python3 scripts/skill_layout.py moves`
- **--self-test**: Runs the built-in checks on a temporary tree
  - `python3 scripts/skill_layout.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- الأمان: writes-files
- الموافقة: —
- الحدود: It checks where files are listed, not what they say; moving files and fixing the links that point at them is a separate, reviewed step.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_skill_layout.py`
- مرجع: `.claude/skills/kosif-superpowers/references/LAYOUT.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/maintain.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:skill-layout --evidence <ملف>`.

