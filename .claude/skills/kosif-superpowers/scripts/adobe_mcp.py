#!/usr/bin/env python3
"""Adobe MCP bridges: vetted local MCP servers that let Claude drive After Effects,
Premiere Pro and Photoshop on the user's own computer.

This script does not install or run any bridge. It prints the vetted choice for each
app, the exact install steps, the MCP client config, and checks whether this machine
has the runtimes each bridge needs (node, npm, git, python, uv). Standard library only.

Usage:
  python3 scripts/adobe_mcp.py list [--json]
  python3 scripts/adobe_mcp.py show <id> [--json]
  python3 scripts/adobe_mcp.py steps <id> [--os win|mac]
  python3 scripts/adobe_mcp.py config <id> [--client claude-code|claude-desktop] [--path DIR] [--os win|mac]
  python3 scripts/adobe_mcp.py doctor [--json]

ids: after-effects, premiere, photoshop, adb-mcp (multi-app alternative)
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import subprocess
import sys

REVIEWED = "2026-10-27"

BRIDGES: dict[str, dict] = {
    "after-effects": {
        "app": "Adobe After Effects",
        "app_ar": "أدوبي أفتر إفكتس",
        "repo": "https://github.com/Dakkshin/after-effects-mcp",
        "license": "MIT",
        "stars_seen": 804,
        "status": "recommended",
        "app_versions": "After Effects 2022+",
        "os": ["win", "mac"],
        "os_note": "README examples use Windows paths; macOS is not stated, test it first.",
        "needs": {"node": 14, "npm": True, "git": True},
        "server_name": "AfterEffectsMCP",
        "capabilities": [
            "create compositions (size, fps, duration, background) and list them; project info",
            "text, shape (rectangle/ellipse/polygon/star), solid/adjustment, camera and null layers",
            "layer position, scale, rotation, opacity, timing, 2D/3D, blend modes, track mattes, masks",
            "keyframes, expressions and batch property changes across layers",
            "duplicate/delete layers; run-script + get-results for any ExtendScript",
        ],
        "tools": [
            "create-composition", "run-script", "get-results", "get-help", "setLayerKeyframe",
            "setLayerExpression", "setLayerProperties", "batchSetLayerProperties", "getLayerInfo",
            "createCamera", "createNullObject", "duplicateLayer", "deleteLayer", "setLayerMask",
        ],
        "steps": [
            "git clone https://github.com/Dakkshin/after-effects-mcp.git",
            "cd after-effects-mcp",
            "npm install",
            "npm run build",
            "npm run install-bridge   # copies the mcp-bridge-auto.jsx panel into After Effects",
            "In After Effects: Edit > Preferences > Scripting & Expressions > tick 'Allow Scripts to Write Files and Access Network' (if the panel cannot exchange commands)",
            "Restart After Effects, open Window > mcp-bridge-auto.jsx and tick 'Auto-run commands' (keep the panel open)",
            "Add the server to Claude (see: config after-effects), then restart Claude",
            "Test: ask Claude to run get-help, then create a 1080x1920 30fps composition",
        ],
        "entry": "build/index.js",
        "limits": "The panel polls every few seconds, so commands are not instant; the panel must stay open with Auto-run on. run-script executes any ExtendScript inside After Effects.",
    },
    "premiere": {
        "app": "Adobe Premiere Pro",
        "app_ar": "أدوبي بريمير برو",
        "repo": "https://github.com/leancoderkavy/premiere-pro-mcp",
        "license": "MIT",
        "stars_seen": 247,
        "status": "recommended",
        "app_versions": "Premiere Pro 2020-2026 (CEP bridge); 25.6+ for the optional UXP panel",
        "os": ["win", "mac"],
        "os_note": "",
        "needs": {"node": 20, "npm": True},
        "npm_package": "premiere-pro-mcp",
        "pinned": "1.15.1",
        "server_name": "premiere-pro",
        "capabilities": [
            "inspect project, sequences and clips; state snapshots",
            "open/save projects, import media, bins",
            "timeline: insert, overwrite, split, trim, move, track operations",
            "effects, Lumetri colour, LUTs, stabilisation; keyframes",
            "export through Media Encoder, frame capture",
            "source monitor, 3-point editing, playback; editorial plans for review",
        ],
        "tools": ["~369 core tools (+~93 with the UXP panel); start with verify_premiere_connection"],
        "steps": [
            "Install Node.js 20.19 or newer (nodejs.org, LTS)",
            "npm install -g premiere-pro-mcp@1.15.1",
            "premiere-pro-mcp --install-cep   # installs the Premiere connector panel",
            "Fully quit and reopen Premiere Pro, then open the panel from Window > Extensions",
            "premiere-pro-mcp --doctor",
            "Add the server to Claude (see: config premiere), then restart Claude",
            "Test: ask Claude to run verify_premiere_connection before any edit",
        ],
        "alt_claude_code": [
            "/plugin marketplace add leancoderkavy/premiere-pro-mcp",
            "/plugin install premiere-pro@premiere-pro-mcp",
        ],
        "limits": "No supported API for speed/direction changes, text overlays or Render and Replace; QE-based tools are undocumented and some Premiere 26.x builds ignore them (reported as errors). Premiere, the connector and Claude must be on the same computer.",
    },
    "photoshop": {
        "app": "Adobe Photoshop",
        "app_ar": "أدوبي فوتوشوب",
        "repo": "https://github.com/alisaitteke/photoshop-mcp",
        "license": "MIT",
        "stars_seen": 318,
        "status": "recommended",
        "app_versions": "Photoshop CC (ExtendScript); WebP/AVIF export needs 23.2+; neural filters need its optional UXP plugin",
        "os": ["win", "mac"],
        "os_note": "",
        "needs": {"node": 18, "npm": True},
        "npm_package": "@alisaitteke/photoshop-mcp",
        "server_name": "photoshop",
        "capabilities": [
            "documents and layers, layer styles, text, placing images, selections and masks",
            "filters, colour adjustments, LUTs, actions, undo/redo, custom ExtendScript",
            "state + preview image tools so Claude can see the result",
            "recipes: background removal, portrait retouch, frequency separation, sky blend, colour grade, social export, mockups, batch watermark, carousel split",
            "optional Firefly generative fill/expand/remove (uses the user's Adobe credits)",
        ],
        "tools": ["102 tools (86 photoshop_* + 16 photoshop_recipe_*) and 23 prompts"],
        "steps": [
            "Install Node.js 18+ (LTS)",
            "Open Photoshop",
            "Add the server to Claude (see: config photoshop); npx downloads it on first run",
            "Restart Claude",
            "Test: ask Claude for the Photoshop state/capabilities, then a small edit on a copy of a file",
        ],
        "limits": "Talks to Photoshop through AppleScript (mac) or COM (Windows). Firefly tools spend Adobe credits: ask first. Do not use its optional web UI with API keys; Claude itself is the client.",
    },
    "adb-mcp": {
        "app": "Photoshop, Premiere, InDesign, After Effects, Illustrator",
        "app_ar": "فوتوشوب وبريمير وإن ديزاين وأفتر إفكتس وإليستريتور",
        "repo": "https://github.com/mikechambers/adb-mcp",
        "license": "MIT",
        "stars_seen": 710,
        "status": "alternative",
        "app_versions": "Photoshop 26.0+; Premiere Beta 25.3+; InDesign UXP; AE and Illustrator via CEP",
        "os": ["win", "mac"],
        "os_note": "Proof of concept, not supported by Adobe.",
        "needs": {"node": 18, "npm": True, "git": True, "python": True, "uv": True},
        "server_name": "adb-mcp",
        "capabilities": [
            "one project for five Adobe apps (Photoshop strongest, Premiere single-sequence)",
            "Photoshop: create files, layers, text by font, effects, renders shown back to Claude",
            "AE/Illustrator: low-level ExtendScript runner",
        ],
        "tools": ["per-app servers: ps-mcp.py, pr-mcp.py, id-mcp.py, ae-mcp.py, ai-mcp.py"],
        "steps": [
            "git clone https://github.com/mikechambers/adb-mcp.git && cd adb-mcp",
            "Photoshop server: uv run mcp install --with fonttools --with python-socketio --with mcp --with requests --with websocket-client --with numpy ps-mcp.py",
            "Start the proxy and keep it running: cd adb-proxy-socket && node proxy.js",
            "Install Adobe UXP Developer Tools (Creative Cloud), enable Developer Mode in the app (Settings > Plugins), restart",
            "UXP Developer Tools > File > Add Plugin > uxp/ps/manifest.json (pr / id for the others), load it, open the panel, Connect",
            "Restart Claude Desktop; in a chat choose + > Add from Adobe Photoshop > config://get_instructions",
        ],
        "limits": "More moving parts (Python server + Node proxy + UXP plugin); plugins must be reloaded after each app restart. Use it only when one setup for several apps matters more than depth.",
    },
}

REJECTED = [
    {"repo": "https://github.com/MauricePutinas/premiere-pro-mcp-claude-code",
     "why": "0 stars and a single commit, Windows and Premiere 2025 only; interesting intro presets but unproven."},
    {"repo": "marcelo-earth, bot202102, jameslashmar, dan0nchik, Utopai-Research and others /premiere-pro-mcp",
     "why": "forks of leancoderkavy/premiere-pro-mcp with ~0-1 stars; use the original."},
    {"repo": "https://github.com/loonghao/photoshop-python-api-mcp-server",
     "why": "Windows-only (Photoshop COM via photoshop-python-api); alisaitteke covers Windows and macOS."},
]


def _os_key(value: str | None) -> str:
    if value:
        return value
    return "mac" if sys.platform == "darwin" else "win"


def _get(bridge_id: str) -> dict:
    if bridge_id not in BRIDGES:
        raise SystemExit(f"unknown id '{bridge_id}'. ids: {', '.join(BRIDGES)}")
    return BRIDGES[bridge_id]


def server_entry(bridge_id: str, os_key: str, path: str | None = None) -> dict:
    b = _get(bridge_id)
    if bridge_id == "after-effects":
        base = path or ("C:\\path\\to\\after-effects-mcp" if os_key == "win" else "/path/to/after-effects-mcp")
        sep = "\\" if os_key == "win" else "/"
        return {"command": "node", "args": [base.rstrip("\\/") + sep + b["entry"].replace("/", sep)]}
    if bridge_id == "premiere":
        return {"command": "premiere-pro-mcp"}
    if bridge_id == "photoshop":
        return {"command": "npx", "args": ["-y", b["npm_package"]]}
    raise SystemExit(ADB_NOTE)


ADB_NOTE = ("adb-mcp has no hand-written config: `uv run mcp install ... ps-mcp.py` (see: steps adb-mcp) "
            "registers the server in Claude Desktop itself. If Claude cannot start it, put the absolute path of uv in that entry.")


def claude_code_command(bridge_id: str, os_key: str, path: str | None = None) -> str:
    b = _get(bridge_id)
    entry = server_entry(bridge_id, os_key, path)
    parts = [entry["command"], *entry.get("args", [])]
    if os_key == "win" and entry["command"] == "npx":
        parts = ["cmd", "/c", *parts]  # native Windows needs cmd /c to start npx
    quoted = " ".join(f'"{p}"' if (" " in p or "\\" in p) else p for p in parts)
    return f"claude mcp add {b['server_name']} -- {quoted}"


def desktop_config(bridge_id: str, os_key: str, path: str | None = None) -> dict:
    entry = {k: v for k, v in server_entry(bridge_id, os_key, path).items() if k != "note"}
    return {"mcpServers": {_get(bridge_id)["server_name"]: entry}}


DESKTOP_CONFIG_PATH = {
    "win": "%APPDATA%\\Claude\\claude_desktop_config.json",
    "mac": "~/Library/Application Support/Claude/claude_desktop_config.json",
}


def _version(cmd: str, flag: str = "--version") -> str | None:
    exe = shutil.which(cmd)
    if not exe:
        return None
    try:
        out = subprocess.run([exe, flag], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    text = (out.stdout or out.stderr).strip().splitlines()
    return text[0] if text else ""


def _major(version: str | None) -> int | None:
    if not version:
        return None
    m = re.search(r"(\d+)\.", version)
    return int(m.group(1)) if m else None


def doctor() -> dict:
    found = {
        "node": _version("node"),
        "npm": _version("npm"),
        "git": _version("git"),
        "python": _version("python3") or _version("python"),
        "uv": _version("uv"),
    }
    os_name = platform.system()
    ready = {}
    for bid, b in BRIDGES.items():
        missing = []
        for need, req in b["needs"].items():
            if not found.get(need):
                missing.append(need)
            elif need == "node" and isinstance(req, int) and (_major(found["node"]) or 0) < req:
                missing.append(f"node>={req} (have {found['node']})")
        ready[bid] = {"ready_to_install": not missing, "missing": missing}
    supported_os = os_name in ("Windows", "Darwin")
    return {
        "os": os_name,
        "adobe_apps_possible_here": supported_os,
        "note": "Adobe apps run only on Windows or macOS; run this on the computer that has them."
        if not supported_os else "Runtimes checked; Adobe apps themselves are not detected by this script.",
        "found": found,
        "bridges": ready,
    }


def _print_list(as_json: bool) -> None:
    if as_json:
        print(json.dumps({"reviewed": REVIEWED, "bridges": {k: {x: v[x] for x in ("app", "repo", "license", "stars_seen", "status", "app_versions")} for k, v in BRIDGES.items()}, "rejected": REJECTED}, ensure_ascii=False, indent=1))
        return
    print(f"Adobe MCP bridges (reviewed {REVIEWED})")
    for k, b in BRIDGES.items():
        print(f"- {k:14} {b['status']:11} {b['app']}  ({b['repo']}, {b['license']}, ~{b['stars_seen']} stars)")
    print("Not chosen:")
    for r in REJECTED:
        print(f"  x {r['repo']}: {r['why']}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Vetted MCP bridges for Adobe After Effects, Premiere Pro and Photoshop: steps, config and a runtime check. Installs nothing.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list", help="the vetted bridges and the ones not chosen")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("show", help="everything about one bridge")
    s.add_argument("id")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("steps", help="install steps for one bridge")
    s.add_argument("id")
    s.add_argument("--os", choices=["win", "mac"])
    s = sub.add_parser("config", help="Claude Code command or Claude Desktop JSON")
    s.add_argument("id")
    s.add_argument("--client", choices=["claude-code", "claude-desktop"], default="claude-desktop")
    s.add_argument("--path", help="folder where you cloned the bridge (After Effects, adb-mcp)")
    s.add_argument("--os", choices=["win", "mac"])
    s = sub.add_parser("doctor", help="check node/npm/git/python/uv on this machine")
    s.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    if a.cmd == "list":
        _print_list(a.json)
    elif a.cmd == "show":
        b = _get(a.id)
        if a.json:
            print(json.dumps({"id": a.id, **b}, ensure_ascii=False, indent=1))
        else:
            print(f"{b['app']} — {b['repo']} ({b['license']}, {b['status']})")
            print(f"versions: {b['app_versions']}")
            print("can do:")
            for c in b["capabilities"]:
                print(f"  - {c}")
            print(f"limits: {b['limits']}")
    elif a.cmd == "steps":
        b = _get(a.id)
        os_key = _os_key(a.os)
        print(f"{b['app']} — install ({os_key}); nothing here stores an API key")
        for i, step in enumerate(b["steps"], 1):
            print(f"{i}. {step}")
        if b.get("os_note"):
            print(f"note: {b['os_note']}")
        if b.get("alt_claude_code"):
            print("Claude Code plugin route instead:")
            for line in b["alt_claude_code"]:
                print(f"  {line}")
    elif a.cmd == "config":
        os_key = _os_key(a.os)
        _get(a.id)
        if a.id == "adb-mcp":
            print(ADB_NOTE)
            return 0
        if a.client == "claude-code":
            print(claude_code_command(a.id, os_key, a.path))
        else:
            print(f"// merge into {DESKTOP_CONFIG_PATH[os_key]}")
            print(json.dumps(desktop_config(a.id, os_key, a.path), indent=2))
    elif a.cmd == "doctor":
        r = doctor()
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        else:
            print(f"OS: {r['os']} — {r['note']}")
            for k, v in r["found"].items():
                print(f"  {k:6} {v or 'missing'}")
            for k, v in r["bridges"].items():
                state = "ready" if v["ready_to_install"] else "missing " + ", ".join(v["missing"])
                print(f"  {k:14} {state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
