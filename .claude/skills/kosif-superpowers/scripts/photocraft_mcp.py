#!/usr/bin/env python3
"""PhotoCraft MCP helper for KOSIF (annex A39, USIP v5.10).

Prints install steps, MCP client config, a doctor report, sample action files
and recipes. It never installs, builds or registers anything by itself.

  python3 photocraft_mcp.py steps headless|bridge|release
  python3 photocraft_mcp.py config --client claude-code|claude-desktop|json \
          --read-root /abs/in --write-root /abs/out [--bridge 127.0.0.1:7878 --token-file /private/pc.token]
  python3 photocraft_mcp.py doctor
  python3 photocraft_mcp.py actions grade|resize-webp
  python3 photocraft_mcp.py recipes
  python3 photocraft_mcp.py lut <look.cube> <in.mp4> <out.mp4>     # recipe R2, printed not run
  python3 photocraft_mcp.py selftest

v5.10: shell-safe quoting (shlex), root flags with --bridge are refused (the app owns the roots),
a config with no write root warns (no write permission at all), a write root that is / or $HOME is
refused, doctor --json, and the LUT command for recipe R2.
"""
import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys

REPO = "https://github.com/storytold/photocraft"

STEPS = {
    "headless": [
        "Ask the user first: building or installing runs third-party code.",
        f"git clone --depth 1 {REPO} && cd photocraft",
        "cargo install --path apps/photocraft-cli --locked   # needs Rust >= 1.95",
        'export PATH="${CARGO_HOME:-$HOME/.cargo}/bin:$PATH"',
        "photocraft-cli --version && photocraft-cli mcp --help",
        "mkdir -p /abs/out   # a dedicated output folder as the write root",
        "claude mcp add photocraft -- photocraft-cli mcp --automation-read-root /abs/in --automation-write-root /abs/out",
        "Restart the MCP client, then call command_list with a filter to confirm.",
    ],
    "bridge": [
        "Ask the user first. Only for a trusted local session; never keep the port open.",
        "Create a private token file readable only by you (chmod 600 on POSIX).",
        "photocraft --control 7878 --control-token-file /private/pc.token "
        "--automation-read-root /abs/in --automation-write-root /abs/out",
        "claude mcp add photocraft-live -- photocraft-cli mcp --bridge 127.0.0.1:7878 "
        "--control-token-file /private/pc.token",
        "Root flags are rejected with --bridge; the desktop app owns the roots.",
        "Never proxy or tunnel the loopback port; never log or commit the token.",
    ],
    "release": [
        "Linux deb/rpm: /usr/bin/photocraft-cli",
        r"Windows MSI: %LOCALAPPDATA%\Programs\ArtCraft\PhotoCraft\photocraft-cli.exe (not on PATH)",
        "macOS: separate photocraft-cli-<version>-macos-<arch>.zip release asset",
        f"Releases: {REPO}/releases",
        "Then register with: photocraft_mcp.py config --client claude-code ...",
    ],
}

ACTIONS = {
    "grade": [
        {"command": "layer.newAdjustmentLayer.curves",
         "params": {"points": [[0, 0], [64, 48], [192, 212], [255, 255]]}},
        {"command": "filter.sharpen.smartSharpen", "params": {"amount": 80}},
    ],
    "resize-webp": [
        {"command": "image.imageSize", "params": {"width": 1600}},
    ],
}

RECIPES = [
    ("R1 Arabic thumbnail", "doc_new 1280x720 -> doc_place frame -> curves -> Arabic type layer -> render_preview -> doc_export"),
    ("R2 one look for photos+video", "grade a still -> file.export.colorLookupTables {size:33,path:look.cube} -> ffmpeg -vf lut3d=look.cube"),
    ("R3 product batch", "photocraft-cli batch --actions a.json --in raw --out done --format webp"),
    ("R4 data-set template", "doc_import_data_sets (CSV) -> doc_export_data_sets"),
    ("R5 split a PSD", "doc_open x.psd -> doc_export_layers"),
    ("R6 generated then finished", "Higgsfield image (paid, ask) -> PhotoCraft grade/type/crop -> render_preview"),
]


def args_for(ns):
    if ns.bridge:
        if not ns.token_file:
            sys.exit("--bridge needs --token-file (never pass the token itself)")
        if ns.read_root or ns.write_root:
            sys.exit("root flags are rejected with --bridge: set the roots on the desktop app (photocraft --control ...)")
        host = ns.bridge.rsplit(":", 1)[0]
        if host not in ("127.0.0.1", "localhost", "[::1]"):
            sys.exit("--bridge must be a loopback address (127.0.0.1:<port>): never proxy or tunnel the control port")
        return ["mcp", "--bridge", ns.bridge, "--control-token-file", ns.token_file]
    for name in ("read_root", "write_root"):
        val = getattr(ns, name)
        if val and not os.path.isabs(val):
            sys.exit(f"--{name.replace('_', '-')} must be an absolute path")
    if ns.write_root:
        wr = os.path.normpath(ns.write_root)
        if wr in ("/", os.path.expanduser("~")) or (len(wr) <= 3 and wr.endswith(":\\")):
            sys.exit("--write-root must be a dedicated output folder, not / or the home folder (rule 1)")
    else:
        print("# warning: no --write-root, so the server can save nothing (that is safe, but probably not what you want)",
              file=sys.stderr)
    out = ["mcp"]
    if ns.read_root:
        out += ["--automation-read-root", ns.read_root]
    if ns.write_root:
        out += ["--automation-write-root", ns.write_root]
    return out


def cmd_config(ns):
    a = args_for(ns)
    name = "photocraft-live" if ns.bridge else "photocraft"
    exe = ns.command
    if ns.client == "claude-code":
        print("claude mcp add " + name + " -- " + shlex.join([exe] + a))
    else:
        cfg = {"mcpServers": {name: {"command": exe, "args": a}}}
        print(json.dumps(cfg, indent=2))
        if ns.client == "claude-desktop":
            print("# merge into claude_desktop_config.json, then restart Claude Desktop", file=sys.stderr)


def cmd_doctor(_ns):
    report = {"photocraft-cli": shutil.which("photocraft-cli"),
              "cargo": shutil.which("cargo"),
              "ffmpeg (for LUT recipe R2)": shutil.which("ffmpeg")}
    exe = report["photocraft-cli"]
    if exe:
        try:
            r = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=20)
            report["version"] = (r.stdout or r.stderr).strip()
        except (OSError, subprocess.SubprocessError) as e:
            report["version"] = f"error: {e}"
    if getattr(_ns, "json", False):
        print(json.dumps({k: v for k, v in report.items()}, indent=2))
        return 0
    for k, v in report.items():
        print(f"{k:28} {v or 'MISSING'}")
    if not exe:
        print("\nNot installed. Run: photocraft_mcp.py steps headless (and ask the user first).")
    return 0


def cmd_lut(ns):
    """Recipe R2: print (never run) the ffmpeg line that applies a PhotoCraft .cube to a clip,
    keeping the KOSIF export standard: H.264 High CRF 17 slow, BT.709 tags, audio copied, faststart."""
    if not ns.cube.lower().endswith(".cube"):
        sys.exit("the LUT must be a .cube file (file.export.colorLookupTables)")
    vf = "lut3d=file=" + ns.cube.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    cmd = ["ffmpeg", "-i", ns.input, "-vf", vf, "-c:v", "libx264", "-profile:v", "high", "-crf", "17",
           "-preset", "slow", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
           "-color_trc", "bt709", "-c:a", "copy", "-movflags", "+faststart", ns.output]
    print(shlex.join(cmd))
    print("# then compare one frame before/after (A31): masks and crops are not part of a LUT", file=sys.stderr)
    return 0


def cmd_selftest(_ns):
    import contextlib
    import io
    cases = [
        (["config", "--client", "claude-code", "--read-root", "/abs/my in", "--write-root", "/abs/out"], 0, "'/abs/my in'"),
        (["config", "--client", "json", "--read-root", "/abs/in", "--write-root", "/abs/out"], 0, '"mcpServers"'),
        (["config", "--bridge", "127.0.0.1:7878", "--token-file", "/p/t"], 0, "--control-token-file"),
        (["config", "--bridge", "127.0.0.1:7878", "--token-file", "/p/t", "--write-root", "/abs/out"], "exit", ""),
        (["config", "--bridge", "10.0.0.5:7878", "--token-file", "/p/t"], "exit", ""),
        (["config", "--bridge", "127.0.0.1:7878"], "exit", ""),
        (["config", "--read-root", "rel/in"], "exit", ""),
        (["config", "--write-root", "/"], "exit", ""),
        (["lut", "look.cube", "in.mp4", "out.mp4"], 0, "lut3d=file=look.cube"),
        (["lut", "look.png", "in.mp4", "out.mp4"], "exit", ""),
        (["actions", "grade"], 0, "layer.newAdjustmentLayer.curves"),
    ]
    bad = 0
    for argv, want, needle in cases:
        out, err = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                got = main(argv)
        except SystemExit:
            got = "exit"
        ok = got == want and needle in out.getvalue()
        bad += not ok
        print(("ok   " if ok else "FAIL ") + " ".join(argv))
    print("PASS" if not bad else f"FAIL ({bad})")
    return 1 if bad else 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("steps"); s.add_argument("mode", choices=sorted(STEPS))
    c = sub.add_parser("config")
    c.add_argument("--client", choices=["claude-code", "claude-desktop", "json"], default="claude-code")
    c.add_argument("--command", default="photocraft-cli", help="absolute path if not on the client's PATH")
    c.add_argument("--read-root"); c.add_argument("--write-root")
    c.add_argument("--bridge"); c.add_argument("--token-file")
    d = sub.add_parser("doctor"); d.add_argument("--json", action="store_true")
    lt = sub.add_parser("lut"); lt.add_argument("cube"); lt.add_argument("input"); lt.add_argument("output")
    sub.add_parser("selftest")
    a = sub.add_parser("actions"); a.add_argument("name", choices=sorted(ACTIONS))
    sub.add_parser("recipes")
    ns = p.parse_args(argv)
    if ns.cmd == "steps":
        for i, line in enumerate(STEPS[ns.mode], 1):
            print(f"{i}. {line}")
    elif ns.cmd == "config":
        cmd_config(ns)
    elif ns.cmd == "doctor":
        return cmd_doctor(ns)
    elif ns.cmd == "actions":
        print(json.dumps(ACTIONS[ns.name], indent=2))
    elif ns.cmd == "lut":
        return cmd_lut(ns)
    elif ns.cmd == "selftest":
        return cmd_selftest(ns)
    elif ns.cmd == "recipes":
        for name, flow in RECIPES:
            print(f"{name}: {flow}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
