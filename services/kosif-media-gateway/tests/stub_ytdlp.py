#!/usr/bin/env python3
"""Offline stand-in for yt-dlp used by the gateway tests.

Behaviour comes from STUB_MODE: ok | mpeg4 | corrupt | short | login | 429 | proxy502 | 403 | big | slow.
In ok/mpeg4/corrupt/short modes it writes a real MP4 made by ffmpeg (portrait 360x640, 3 s).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

args = sys.argv[1:]
mode = os.environ.get("STUB_MODE", "ok")
if mode == "probe_only_403" and "--test" not in args and "-J" not in args:
    mode = "403"
ff = os.environ.get("KOSIF_FFMPEG", "ffmpeg")
if "--version" in args:
    print("2026.10.26-stub")
    sys.exit(0)
counter = os.environ.get("STUB_COUNTER")
if counter:
    with open(counter, "a") as fp:
        fp.write("call\n")
errors = {
    "login": "ERROR: [youtube] abc: Sign in to confirm you’re not a bot. Use --cookies-from-browser",
    "429": "ERROR: [youtube] abc: Unable to download webpage: HTTP Error 429: Too Many Requests",
    "proxy502": "ERROR: Unable to download: Tunnel connection failed: 502 Bad Gateway (proxy) https://rr1.googlevideo.com/x",
    "403": "ERROR: unable to download video data: HTTP Error 403: Forbidden",
    "big": "ERROR: File is larger than max-filesize (99999999 bytes > 47185920 bytes). Aborting.",
}
if mode in errors:
    print(errors[mode], file=sys.stderr)
    sys.exit(1)
if mode == "slow":
    time.sleep(float(os.environ.get("STUB_SLEEP", "30")))
if "--test" in args:
    if mode == "probe_only_403":
        print("ERROR: unable to download video data: HTTP Error 403: Forbidden", file=sys.stderr)
        sys.exit(1)
    Path(args[args.index("-o") + 1].replace("%(ext)s", "mp4")).write_bytes(b"\0" * 10240)
    sys.exit(0)
if "-J" in args:
    print(json.dumps({"id": "dYrEeavC3cw", "title": "stub", "duration": 3, "width": 360, "height": 640,
                      "formats": [{"vcodec": "avc1.4d401e"}, {"vcodec": "vp09"}, {"vcodec": "none"}]}))
    sys.exit(0)
out = Path(args[args.index("-o") + 1].replace("%(ext)s", "mp4"))
vcodec = ["-c:v", "mpeg4"] if mode == "mpeg4" else ["-c:v", "libx264", "-pix_fmt", "yuv420p"]
dur = "1" if mode == "short" else "3"
subprocess.run([ff, "-y", "-v", "error", "-f", "lavfi", "-i", f"testsrc2=s=360x640:r=25:d={dur}",
                "-f", "lavfi", "-i", f"sine=f=440:d={dur}", *vcodec, "-c:a", "aac", "-shortest", str(out)], check=True)
if mode == "corrupt":
    data = out.read_bytes()
    out.write_bytes(data[: len(data) // 2])
(out.parent / "source.info.json").write_text(json.dumps({"title": "stub clip", "duration": 3,
                                                         "webpage_url": args[-1], "license": "stub"}))
print(out)
