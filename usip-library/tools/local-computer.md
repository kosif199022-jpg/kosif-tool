# أدوات المجال `local-computer` (3 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `adobe-mcp-bridges` — ربط Claude ببرامج أدوبي (أفتر إفكتس وبريمير وفوتوشوب) / Adobe MCP bridges (After Effects, Premiere Pro, Photoshop)

| الحقل | القيمة |
|---|---|
| المسار | `scripts/adobe_mcp.py` (جذر: skill) |
| المجال | `local-computer` |
| الدليل | `tested-here` |
| العائلات | `engines-render-pipeline`, `transitions-cuts`, `photo-video-footage`, `agent-orchestration` |

**ما تفعله:** خوادم MCP محلية تمت مراجعتها تخلّي Claude يتحكم في برامج أدوبي على جهاز المستخدم: after-effects-mcp للتكوينات والطبقات والكي فريمز والإكسبريشنز، وpremiere-pro-mcp للمونتاج على التايملاين والإفكتات والألوان والتصدير، وphotoshop-mcp للطبقات والنصوص والماسكات والفلاتر ووصفات الريتاتش، وadb-mcp بديل لخمسة برامج. السكربت يطبع خطوات التسطيب وأمر Claude Code أو إعداد Claude Desktop ويفحص المتطلبات، ولا يسطّب شيئًا ولا يحتاج مفتاح API.

**What it does:** Vetted local MCP servers that let Claude drive Adobe apps on the user's own computer: Dakkshin/after-effects-mcp (compositions, layers, keyframes, expressions, ExtendScript), leancoderkavy/premiere-pro-mcp (timeline editing, effects, colour, export) and alisaitteke/photoshop-mcp (layers, text, masks, filters, retouch recipes), plus mikechambers/adb-mcp as a five-app alternative. The stdlib helper prints install steps, the Claude Code command or Claude Desktop JSON, and checks node/npm/git/python/uv. It installs nothing and needs no API key.

#### متى تُستدعى

- «اربط كلاود بأفتر إفكتس على جهازي»
- «عايز Claude يقص ويمنتج في بريمير»
- «وصّل كلاود بفوتوشوب يعدّل الطبقات»
- «Connect Claude to Adobe Premiere Pro»
- «Let Claude animate layers in After Effects through MCP»
- «How do I install a Photoshop MCP server for Claude Desktop»

#### الأوامر

- **list**: Lists the vetted bridge per app (repo, licence, stars seen, status) and the repositories that were not chosen, with why. --json for machine output.
  - `python3 scripts/adobe_mcp.py list`
- **show**: Prints what Claude can do through one bridge, the supported app versions and its limits.
  - `python3 scripts/adobe_mcp.py show after-effects`
- **steps**: Prints the numbered install steps for one bridge (ids: after-effects, premiere, photoshop, adb-mcp).
  - `python3 scripts/adobe_mcp.py steps premiere --os win`
- **config**: Prints the claude mcp add command, or the Claude Desktop mcpServers JSON and where the config file lives; --path sets the clone folder for After Effects.
  - `python3 scripts/adobe_mcp.py config photoshop --client claude-code`
- **doctor**: Checks node, npm, git, python and uv versions on this machine and says which bridges are ready to install; notes that Adobe apps need Windows or macOS.
  - `python3 scripts/adobe_mcp.py doctor`

#### المتطلبات والأمان

- optional: bin:node, bin:npm, bin:git, bin:uv
- الأمان: read-only
- الموافقة: The helper only prints. Installing a bridge, adding it to an MCP client, enabling ExtendScript file/network access in After Effects, and any Firefly generative call (Adobe credits) each need the user's explicit approval; never write an API key or Adobe credential into a config.
- الحدود: It does not install or run any bridge, and no bridge was exercised against a live Adobe app here: the facts come from each project's README as of 2026-10-27, and Adobe apps run only on Windows or macOS, so a cloud session can prepare but not drive them.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_adobe_mcp.py`
- مرجع: `.claude/skills/kosif-superpowers/references/adobe-mcp-bridges.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/local-computer.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:adobe-mcp-bridges --evidence <ملف>`.

### `kosif-remote-commander` — خادم KOSIF Remote Commander / KOSIF Remote Commander MCP

| الحقل | القيمة |
|---|---|
| المسار | `scripts/kosif_remote_superpowers.py` (جذر: skill) |
| المجال | `local-computer` |
| الدليل | `tested-here` |
| العائلات | `agent-orchestration`, `code-engineering`, `security-safety` |

**ما تفعله:** خادم MCP مستقل يعمل عبر stdio بالمكتبة القياسية وحدها، ويمنح عميل MCP إحدى عشرة أداة محصورة في مساحة عمل واحدة يوافق عليها المستخدم: الحالة، ومعلومات النظام، وسرد المجلد، وبيانات الملف، والقراءة، والبحث، ثم الإنشاء والكتابة والاستبدال والنقل وتشغيل أوامر من قائمة مسموحة. وتبقى الكتابة وتشغيل الأوامر معطّلين حتى يفعّلهما المستخدم بمتغيرات بيئة.

**What it does:** A self-contained stdio MCP server (standard library only) that gives an MCP client 11 tools scoped to one approved workspace: health, system info, list, file info, read, search, plus create, write, replace, move and an allowlisted command runner. Writes and commands stay off until the user sets an environment flag.

#### متى تُستدعى

- «خلّي كلاود يقرأ ملفات مجلد مشروعي على جهازي»
- «Give my MCP client read-only access to one project folder»
- «ابحث في ملفات المشروع عن كلمة معيّنة عن طريق MCP محلي»
- «Run git status in my workspace through a local MCP server»
- «وصّل كلاود بمجلد على اللابتوب بدون ما يقدر يعدّل إلا بإذني»

#### الأوامر

- **doctor**: Prints the name, version, tool count, transport and current permissions (workspace, allow_writes, allow_exec) as one JSON line. It is also the default when no mode is given.
  - `python3 scripts/kosif_remote_superpowers.py doctor`
- **demo**: In a temporary folder, shows that writes are denied by default, enables them there only, then writes, searches and reads a sample. Prints PASS or FAIL and exits.
  - `python3 scripts/kosif_remote_superpowers.py demo`
- **serve**: Serves MCP over stdio with newline-delimited JSON-RPC 2.0 (initialize, ping, tools/list, tools/call) until stdin closes. Add KOSIF_ALLOW_WRITES=1 or KOSIF_ALLOW_EXEC=1 only with the user's approval.
  - `KOSIF_REMOTE_ROOT=./project python3 scripts/kosif_remote_superpowers.py serve`
- **tools/list (one-shot)**: Pipes one JSON-RPC request into the server, prints the 11 tool schemas and exits.
  - `printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \| KOSIF_REMOTE_ROOT=./project python3 scripts/kosif_remote_superpowers.py serve`

#### المتطلبات والأمان

- optional: bin:git, bin:node, bin:npm, bin:python
- الأمان: runs-external-programs
- الموافقة: The user must approve the folder set as KOSIF_REMOTE_ROOT. Setting KOSIF_ALLOW_WRITES=1 (create, write, replace, move inside it) and KOSIF_ALLOW_EXEC=1 (git status/diff/rev-parse with a few read-only flags, and exactly python/node/npm --version with no other arguments) each needs separate approval, as does adding the server to an MCP client config; do not enable exec on an untrusted repository, because git honours that repository's own config.
- الحدود: It gives bounded local stdio access to one workspace (UTF-8 text files up to 512 KB, 300 lines per read, 150 listed entries, 500 files and 35 hits per search) plus six allowlisted status and version commands, with no remote relay, pairing, desktop or UI control, or arbitrary shell.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/scripts/test_kosif_remote_superpowers.py`
- مرجع: `.claude/skills/kosif-superpowers/references/remote-commander-mcp.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/local-computer.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:kosif-remote-commander --evidence <ملف>`.

### `photocraft-mcp` — PhotoCraft MCP: محرر صور مفتوح المصدر يتحكم فيه Claude / PhotoCraft MCP (open-source Photoshop-style editor driven by Claude)

| الحقل | القيمة |
|---|---|
| المسار | `scripts/photocraft_mcp.py` (جذر: skill) |
| المجال | `local-computer` |
| الدليل | `tested-here` |
| العائلات | `engines-render-pipeline`, `transitions-cuts`, `photo-video-footage`, `agent-orchestration` |

**ما تفعله:** أداة الملحق A39 لـ storytold/photocraft، محرر صور بـ Rust (رخصة MIT/Apache) بأكثر من 500 أمر متاحة عبر MCP: جلسة بلا شاشة حتى في السحابة ولينكس، اكتشاف الأوامر وتنفيذها دفعات، فحص شجرة الطبقات، معاينة PNG، تصدير PSD وTIFF وWebP وEXR، طبقة لكل ملف، قوالب بيانات، دفعات مجلدات، تصدير LUT بصيغة cube، وجسر للبرنامج المفتوح. السكربت يطبع خطوات التسطيب وأمر Claude Code أو إعداد MCP بجذور مطلقة وأمثلة أكشنز ووصفات، ويفحص وجود photocraft-cli وcargo وffmpeg، ولا يسطّب شيئًا.

**What it does:** Annex A39 helper for storytold/photocraft, a clean-room Rust image editor (MIT/Apache) whose 500+ commands are exposed over MCP: headless sessions (also in cloud sessions and Linux), command discovery and batches, layer-tree inspection, bounded PNG previews, PSD/PSB/TIFF/WebP/EXR export, layers-to-files, data sets, folder batches, .cube LUT export and a loopback bridge to the running desktop app. The stdlib helper prints install steps, the Claude Code command or MCP JSON with absolute read/write roots, sample action files and recipes, and checks whether photocraft-cli, cargo and ffmpeg are present. It installs nothing.

#### متى تُستدعى

- «عدّل الصور دي من غير فوتوشوب في السحابة»
- «اربط Claude ببرنامج تعديل صور مفتوح المصدر»
- «طبّق نفس اللوك على كل صور المجلد»
- «Edit a PSD headlessly with an MCP server»
- «Export a .cube LUT from adjustment layers for my video»
- «Set up PhotoCraft MCP for Claude Code»

#### الأوامر

- **steps**: Prints numbered install/registration steps for headless, bridge or release installs; the first step is always to ask the user.
  - `python3 scripts/photocraft_mcp.py steps headless`
- **config**: Prints the claude mcp add command or the mcpServers JSON; refuses relative roots and a bridge without a token file.
  - `python3 scripts/photocraft_mcp.py config --client claude-code --read-root /abs/in --write-root /abs/out`
- **doctor**: Reports whether photocraft-cli (with its version), cargo and ffmpeg are on PATH.
  - `python3 scripts/photocraft_mcp.py doctor`
- **actions**: Prints a sample actions.json for photocraft-cli batch.
  - `python3 scripts/photocraft_mcp.py actions grade`
- **recipes**: Lists the six A39 recipes (thumbnail, photo+video LUT, product batch, data sets, PSD split, generated-then-finished).
  - `python3 scripts/photocraft_mcp.py recipes`

#### المتطلبات والأمان

- optional: bin:photocraft-cli, bin:cargo, bin:ffmpeg
- الأمان: read-only
- الموافقة: The helper only prints. Building or installing PhotoCraft runs third-party code, and opening the desktop control port, each need the user's explicit approval; keep the bearer token in a private file, never in a config, log or commit.
- الحدود: PhotoCraft itself was not built or run here (the build was not approved in this session); the tool list, limits and command ids come from the project's docs and engine source as of 2026-10-29, and it is an early-alpha editor, so check every output visually.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_photocraft_mcp.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A39-v59-photocraft-mcp.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/local-computer.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:photocraft-mcp --evidence <ملف>`.

