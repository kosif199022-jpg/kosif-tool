# الوصول إلى الجهاز المحلي — Local computer access (MCP)

خوادم MCP محلية: Remote Commander لملفات مساحة عمل يوافق عليها المستخدم، وخادم كتالوج KOSIF للقراءة فقط.

Local MCP servers: Remote Commander for a user-approved workspace, and the read-only KOSIF catalog server.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:local-computer:start -->

**الأدوات / tools (2)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `kosif-remote-commander` | A self-contained stdio MCP server (standard library only) that gives an MCP client 11 tools scoped to one approved workspace: health, system info, list, file info, read, search, plus create, write, replace, move and an allowlisted command runner. Writes and commands stay off until the user sets an environment flag. | `python3 scripts/kosif_remote_superpowers.py doctor` | tested-here |
| `adobe-mcp-bridges` | Vetted local MCP servers that let Claude drive Adobe apps on the user's own computer: Dakkshin/after-effects-mcp (compositions, layers, keyframes, expressions, ExtendScript), leancoderkavy/premiere-pro-mcp (timeline editing, effects, colour, export) and alisaitteke/photoshop-mcp (layers, text, masks, filters, retouch recipes), plus mikechambers/adb-mcp as a five-app alternative. The stdlib helper prints install steps, the Claude Code command or Claude Desktop JSON, and checks node/npm/git/python/uv. It installs nothing and needs no API key. | `python3 scripts/adobe_mcp.py list` | tested-here |

<!-- hub:area:local-computer:end -->

## الفهرس / contents

1. [KOSIF local computer MCP (verified prototype)](#kosif-local-computer-mcp-verified-prototype)
2. [KOSIF catalog MCP server (read-only discovery)](#kosif-catalog-mcp-server-read-only-discovery)
3. [Adobe apps: After Effects, Premiere Pro, Photoshop](#adobe-apps-after-effects-premiere-pro-photoshop)

## KOSIF local computer MCP (verified prototype)

For user-approved local computer work, use the self-contained **KOSIF Remote Commander** MCP server. It offers 11 workspace-scoped tools for files, search, metadata, and strictly allowlisted read-only commands. It runs **locally over stdio**, not on a cloud relay; it is not full remote desktop control. By default it **cannot write files or execute commands**.

From this skill directory:

~~~powershell
python scripts/kosif_remote_superpowers.py doctor
python scripts/kosif_remote_superpowers.py demo
python -m unittest discover -s scripts -p test_kosif_remote_superpowers.py -v
~~~

In a local MCP client, launch python with arguments `scripts/kosif_remote_superpowers.py serve` and set `KOSIF_REMOTE_ROOT` to the explicitly approved workspace. Only after separate user permission may `KOSIF_ALLOW_WRITES=1` be set for file changes or `KOSIF_ALLOW_EXEC=1` for a limited list of read-only commands. Do not connect this service directly to the internet or advertise cloud, UI, camera, or multi-device capabilities. See [Remote Commander operating guide and evidence](../remote-commander-mcp.md). The standalone test suite exercised 7 functional cases in an isolated workspace; it did not test actual remote device pairing.

## KOSIF catalog MCP server (read-only discovery)

`scripts/kosif_mcp.py` lets any MCP client discover what this skill can do without a shell or a copy of SKILL.md. It answers the same questions as `scripts/hub.py`: `kosif_find` (a task in the user's words → tools to run, catalog powers, guides, styles), `kosif_tool`, `kosif_list_tools`, `kosif_doctor`, `kosif_search_powers`, `kosif_power`, `kosif_family`, `kosif_guides` and `kosif_read_guide` (files inside the skill folder only). It also lists `SKILL.md`, `references/INDEX.md` and `manifest.json` as MCP resources.

It is **read-only**: it never runs a tool, installs anything, writes files or uses the network, so it needs no permission flags. Standard library only; MCP protocol versions 2025-06-18, 2025-03-26 and 2024-11-05.

```bash
python3 scripts/kosif_mcp.py --selftest      # full in-process session, prints PASS/FAIL per check
python3 scripts/hub.py mcp-config            # the `claude mcp add …` line and JSON config for this OS
```

- **Claude Code inside the kosif-tool repository:** the project file `.mcp.json` registers it as `kosif-superpowers`; approve it once when Claude Code asks.
- **Anywhere else / other clients:** run `hub.py mcp-config` and paste the command or JSON it prints (it uses `python` on Windows and `python3` elsewhere, with the absolute path of this copy).

Use Remote Commander (above) when the task needs the user's own files; use the catalog server when a client only needs to know which KOSIF tool or power fits.

## Adobe apps: After Effects, Premiere Pro, Photoshop

ربط Claude بأفتر إفكتس وبريمير وفوتوشوب على جهاز المستخدم (ويندوز أو ماك) عن طريق خوادم MCP مفتوحة المصدر تمت مراجعتها. السكربت يطبع الخطوات والإعداد فقط، والتسطيب نفسه بإذن المستخدم على جهازه.

Optional local tools for the computer that has the Adobe apps. `scripts/adobe_mcp.py` prints the vetted bridge for each app, its install steps and the MCP client config, and checks the runtimes; it installs nothing and needs no API key.

~~~bash
python3 scripts/adobe_mcp.py list
python3 scripts/adobe_mcp.py doctor
python3 scripts/adobe_mcp.py steps after-effects --os win
python3 scripts/adobe_mcp.py config premiere --client claude-code
python3 scripts/adobe_mcp.py config photoshop --os mac
~~~

After Effects: [Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp). Premiere Pro: [leancoderkavy/premiere-pro-mcp](https://github.com/leancoderkavy/premiere-pro-mcp). Photoshop: [alisaitteke/photoshop-mcp](https://github.com/alisaitteke/photoshop-mcp). Five apps in one (proof of concept): [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp). A cloud session can prepare the plan and config but cannot drive these apps. Full capabilities, limits and safety: [adobe-mcp-bridges.md](../adobe-mcp-bridges.md).
