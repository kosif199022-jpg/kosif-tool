#!/usr/bin/env python3
"""End-to-end check of the DEPLOYED gateway, with the token taken only from the environment.

    KOSIF_GATEWAY_TOKEN=... python3 services/kosif-media-gateway/live_check.py --out live-report.json

1. /health and /health?deep=1 (public)
2. MCP with the official SDK: initialize, tools/list, tools/call gateway_status and probe_youtube
3. A real download of a public-domain film from archive.org through the gateway, pulled back over
   HTTPS, SHA-256 and size re-checked, then probed and fully decoded here with ffmpeg
The report never contains the token. Exit 0 only when MCP works and the download is verified.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".claude" / "skills" / "kosif-superpowers" / "scripts"))

DEFAULT_URL = "https://kosif-media-gateway-free-20261030.onrender.com"
# Prelinger Archives, "Everyday Courtesy" (1948): public domain, 37 MB H.264/AAC.
PERMITTED_SOURCE = "https://archive.org/download/Everyday1948/Everyday1948_512kb.mp4"


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=180) as r:
        return json.load(r)


def _local_media_check(path: Path) -> dict:
    ff, fp = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not (ff and fp):
        return {"ok": None, "note": "ffmpeg/ffprobe not installed here"}
    probe = json.loads(subprocess.run([fp, "-v", "error", "-show_entries",
                                       "format=duration,size:stream=codec_type,codec_name,width,height",
                                       "-of", "json", str(path)], capture_output=True, text=True).stdout or "{}")
    dec = subprocess.run([ff, "-v", "error", "-xerror", "-nostdin", "-i", str(path), "-f", "null", "-"],
                         capture_output=True, text=True)
    return {"ok": dec.returncode == 0 and not dec.stderr.strip(), "full_decode_errors": dec.stderr.strip()[-300:],
            "ffprobe": probe}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default=os.environ.get("KOSIF_GATEWAY_URL", DEFAULT_URL))
    ap.add_argument("--source", default=PERMITTED_SOURCE)
    ap.add_argument("--rights", default="public-domain")
    ap.add_argument("--skip-download", action="store_true")
    ap.add_argument("--out", default="live-report.json")
    a = ap.parse_args()
    token = os.environ.get("KOSIF_GATEWAY_TOKEN", "")
    if not token:
        print("KOSIF_GATEWAY_TOKEN is not set; nothing authenticated can be checked", file=sys.stderr)
        return 3
    os.environ["KOSIF_GATEWAY_URL"] = a.url
    base = a.url.rstrip("/")
    report: dict = {"gateway": base, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    report["health"] = _get(base + "/health")
    report["health_deep"] = _get(base + "/health?deep=1").get("public_probe")

    from mcp_client_check import run_check
    report["mcp"] = asyncio.run(run_check(base + "/mcp", token, probe="dYrEeavC3cw"))
    bad = asyncio.run(run_check(base + "/mcp", "wrong-" + token[:0] + "token", probe=None))
    report["mcp_wrong_token_rejected"] = not bad["initialize"]["ok"]

    ok_download = True
    if not a.skip_download:
        import _media_gateway as client
        out = Path(tempfile.mkdtemp(prefix="kosif-live-"))
        t0 = time.time()
        try:
            rec = client.download(a.source, out, a.rights, 360)
        except client.GatewayError as exc:
            rec = {"file": None, "error": str(exc)}
        rec["seconds"] = round(time.time() - t0, 1)
        if rec.get("original_file"):
            orig = Path(rec["original_file"])
            rec["local_sha256"] = hashlib.sha256(orig.read_bytes()).hexdigest()
            rec["sha256_matches"] = rec["local_sha256"] == rec.get("sha256")
            rec["local_check"] = _local_media_check(orig)
            if rec.get("safe_file"):
                rec["compatible_local_check"] = _local_media_check(Path(rec["safe_file"]))
        for k in ("original_file", "safe_file", "file"):
            if rec.get(k):
                rec[k] = Path(rec[k]).name
        report["download"] = rec
        ok_download = bool(rec.get("verified") and rec.get("sha256_matches") and rec["local_check"].get("ok") is not False)
        shutil.rmtree(out, ignore_errors=True)

    mcp_ok = report["mcp"]["initialize"]["ok"] and "gateway_status" in report["mcp"]["calls"]
    report["result"] = {"mcp_ok": mcp_ok, "wrong_token_rejected": report["mcp_wrong_token_rejected"],
                        "download_verified": ok_download if not a.skip_download else None}
    text = json.dumps(report, ensure_ascii=False, indent=2).replace(token, "[token]")
    Path(a.out).write_text(text, encoding="utf-8")
    print(text)
    return 0 if mcp_ok and report["mcp_wrong_token_rejected"] and ok_download else 1


if __name__ == "__main__":
    sys.exit(main())
