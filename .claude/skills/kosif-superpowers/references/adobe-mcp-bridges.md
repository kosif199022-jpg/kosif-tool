# Adobe MCP bridges — After Effects, Premiere Pro, Photoshop

**State:** optional local tools, installed by the user on the computer that has the Adobe apps (Windows or macOS). Nothing here runs in a cloud session, and nothing stores an API key. The helper `scripts/adobe_mcp.py` prints the steps, the config and a runtime check; it installs nothing. Reviewed on 2026-10-27 from each project's README; none of the bridges was run against a live Adobe app here.

ربط Claude ببرامج أدوبي على جهاز المستخدم: أفتر إفكتس وبريمير وفوتوشوب. كل جسر يتسطّب على الجهاز اللي عليه البرنامج، وClaude بيتحكم فيه من خلال MCP. السكربت `scripts/adobe_mcp.py` بيطلع الخطوات والإعداد ويفحص المتطلبات، ومش بيسطّب حاجة بنفسه.

## الفهرس / contents

1. [The choice per app](#the-choice-per-app)
2. [After Effects](#after-effects)
3. [Premiere Pro](#premiere-pro)
4. [Photoshop](#photoshop)
5. [One setup for five apps: adb-mcp](#one-setup-for-five-apps-adb-mcp)
6. [Not chosen](#not-chosen)
7. [Safety and consent](#safety-and-consent)
8. [How it fits USIP](#how-it-fits-usip)

## The choice per app

| app | bridge | licence | stars seen | needs |
|---|---|---|---|---|
| After Effects 2022+ | [Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp) | MIT | ~804 | Node 14+, git, a panel inside AE |
| Premiere Pro 2020–2026 | [leancoderkavy/premiere-pro-mcp](https://github.com/leancoderkavy/premiere-pro-mcp) | MIT | ~247 | Node 20.19+, a CEP connector panel |
| Photoshop CC | [alisaitteke/photoshop-mcp](https://github.com/alisaitteke/photoshop-mcp) | MIT | ~318 | Node 18+ (runs through npx) |
| PS, PR, ID, AE, AI (alternative) | [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) | MIT | ~710 | Python + uv, Node proxy, UXP Developer Tools |

~~~bash
python3 scripts/adobe_mcp.py list              # the table above, plus the rejected ones
python3 scripts/adobe_mcp.py doctor            # node / npm / git / python / uv on this machine
python3 scripts/adobe_mcp.py steps premiere --os win
python3 scripts/adobe_mcp.py config premiere --client claude-code
python3 scripts/adobe_mcp.py config after-effects --os win --path "C:\Users\me\after-effects-mcp"
~~~

## After Effects

What Claude can do: create compositions (size, fps, duration, background) and list them; add text, shape, solid/adjustment, camera and null layers; set position, scale, rotation, opacity, timing, 2D/3D, blend modes, track mattes and masks; add keyframes and expressions, batch-change properties, duplicate or delete layers; and run any ExtendScript with `run-script` + `get-results`.

Tools: `create-composition`, `run-script`, `get-results`, `get-help`, `setLayerKeyframe`, `setLayerExpression`, `setLayerProperties`, `batchSetLayerProperties`, `getLayerInfo`, `createCamera`, `createNullObject`, `duplicateLayer`, `deleteLayer`, `setLayerMask`.

Install:

~~~bash
git clone https://github.com/Dakkshin/after-effects-mcp.git
cd after-effects-mcp
npm install
npm run build
npm run install-bridge      # copies the mcp-bridge-auto.jsx panel into After Effects
~~~

Then in After Effects: if commands do not arrive, tick Edit › Preferences › Scripting & Expressions › *Allow Scripts to Write Files and Access Network*; restart AE, open Window › `mcp-bridge-auto.jsx`, tick **Auto-run commands** and keep the panel open. Add the server (`config after-effects`), restart Claude, and test with `get-help`.

Claude Desktop (`%APPDATA%\Claude\claude_desktop_config.json` on Windows):

~~~json
{ "mcpServers": { "AfterEffectsMCP": { "command": "node", "args": ["C:\\path\\to\\after-effects-mcp\\build\\index.js"] } } }
~~~

Claude Code: `claude mcp add AfterEffectsMCP -- node /path/to/after-effects-mcp/build/index.js`.

Limits: the panel polls every few seconds, so a command is not instant; macOS is not stated in the README (test it first).

## Premiere Pro

What Claude can do (about 369 core tools, ~93 more with the optional UXP panel): inspect the project, sequences and clips; open, save, import, bins; insert, overwrite, split, trim, move clips and tracks; effects, Lumetri colour, LUTs, stabilisation; keyframes; export through Media Encoder and frame capture; source monitor and 3-point editing; review-only editorial plans.

Install (version pinned to the one reviewed):

~~~bash
npm install -g premiere-pro-mcp@1.15.1
premiere-pro-mcp --install-cep      # installs the connector panel
# quit Premiere fully, reopen it, open Window > Extensions > the connector
premiere-pro-mcp --doctor
~~~

Claude Desktop: `{ "mcpServers": { "premiere-pro": { "command": "premiere-pro-mcp" } } }`. Claude Code: `claude mcp add premiere-pro -- premiere-pro-mcp`, or the plugin route `/plugin marketplace add leancoderkavy/premiere-pro-mcp` then `/plugin install premiere-pro@premiere-pro-mcp`. First call: `verify_premiere_connection`.

Limits: no supported API for speed or direction changes, raw text overlays or Render and Replace; QE-based tools are undocumented and some Premiere 26.x builds ignore them (the tools report this as an error). Premiere, the connector and Claude must run on the same computer.

## Photoshop

What Claude can do (102 tools, 23 prompts): documents and layers, layer styles, text, placed images, selections and masks, filters, colour adjustments, LUTs, actions, undo/redo and custom ExtendScript; state and preview tools so Claude sees the result; recipes such as background removal, portrait retouch, frequency separation, sky blend, colour grade, social export, mockups, batch watermark and carousel split; optional Firefly generative fill, expand and remove.

Install: Node 18+, open Photoshop, add the server and restart Claude.

~~~json
{ "mcpServers": { "photoshop": { "command": "npx", "args": ["-y", "@alisaitteke/photoshop-mcp"] } } }
~~~

Claude Code: `claude mcp add photoshop -- npx -y @alisaitteke/photoshop-mcp` (native Windows: `... -- cmd /c npx -y @alisaitteke/photoshop-mcp`).

Limits: it talks to Photoshop through AppleScript (macOS) or COM (Windows). Firefly tools spend the user's Adobe credits. The project also ships a web UI that takes API keys; KOSIF does not use it, Claude is the client.

## One setup for five apps: adb-mcp

[mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) covers Photoshop (strongest), Premiere (single sequence), InDesign, After Effects and Illustrator (ExtendScript runners). It is a proof of concept with more moving parts: a Python MCP server per app (`uv run mcp install ... ps-mcp.py`), a Node proxy that must stay running (`adb-proxy-socket/node proxy.js`) and UXP plugins loaded through Adobe UXP Developer Tools after enabling Developer Mode. Choose it only when one setup for several apps matters more than depth. `python3 scripts/adobe_mcp.py steps adb-mcp`.

## Not chosen

- [MauricePutinas/premiere-pro-mcp-claude-code](https://github.com/MauricePutinas/premiere-pro-mcp-claude-code): 0 stars and one commit, Windows and Premiere 2025 only. Its cinematic intro presets are interesting but unproven.
- The many `*/premiere-pro-mcp` repositories (marcelo-earth, bot202102, jameslashmar, dan0nchik, Utopai-Research and others) are forks of leancoderkavy's with 0–1 stars: use the original.
- [loonghao/photoshop-python-api-mcp-server](https://github.com/loonghao/photoshop-python-api-mcp-server): Windows only.

## Safety and consent

- These are third-party programs that run on the user's computer and can change open projects. Installing one, and adding it to an MCP client, each needs the user's explicit OK.
- `run-script` (After Effects) and the custom ExtendScript tools can run any script inside the app: work on a copy of the project, and save before a batch of changes.
- Firefly generative tools spend Adobe credits: ask before each use.
- Never put an API key, Adobe password or token in a config, a commit or a note. None of the recommended bridges needs one.

## How it fits USIP

These are **user-machine executors**: in a cloud session Claude can prepare the plan, scripts and config, but cannot drive the Adobe app. With the bridge installed locally, the motion and editing pipelines (A19, A8, A15) can end in an editable After Effects or Premiere project or a layered PSD instead of only a rendered MP4. Report honestly: a step is "done in After Effects" only when the bridge returned a result for it.
