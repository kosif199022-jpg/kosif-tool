# أدوات المجال `local-computer` (1 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

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

