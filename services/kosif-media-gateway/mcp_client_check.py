#!/usr/bin/env python3
"""Check the gateway's MCP endpoint with the official MCP Python SDK (a real client, not raw JSON).

    KOSIF_GATEWAY_TOKEN=... python3 services/kosif-media-gateway/mcp_client_check.py \
        https://kosif-media-gateway-free-20261030.onrender.com/mcp [--probe dYrEeavC3cw] [--out report.json]

Runs initialize, tools/list, tools/call gateway_status and (optionally) probe_youtube. The token is read
from the environment and never printed or written to the report. Works with mcp SDK 1.x and 2.x.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time


def _client_streams(url: str, token: str):
    headers = {"Authorization": "Bearer " + token}
    try:  # SDK 2.x
        from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client
        return streamable_http_client(url, http_client=create_mcp_http_client(headers=headers))
    except ImportError:  # SDK 1.x
        from mcp.client.streamable_http import streamablehttp_client
        return streamablehttp_client(url, headers=headers)


def _attr(obj, *names):
    """SDK 1.x uses camelCase attributes, SDK 2.x snake_case."""
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return None


def _dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json", exclude_none=True)
    return obj


async def run_check(url: str, token: str, probe: str | None = None, download: bool = False) -> dict:
    from mcp import ClientSession
    report: dict = {"url": url, "client": "mcp-python-sdk", "at": int(time.time()),
                    "initialize": {"ok": False}, "tools": [], "calls": {}}
    try:
        async with _client_streams(url, token) as streams:
            read, write = streams[0], streams[1]
            async with ClientSession(read, write) as session:
                init = await session.initialize()
                report["initialize"] = {"ok": True, "protocolVersion": _attr(init, "protocolVersion", "protocol_version"),
                                        "server": _dump(_attr(init, "serverInfo", "server_info"))}
                tools = await session.list_tools()
                report["tools"] = [t.name for t in tools.tools]
                calls = [("gateway_status", {})]
                if probe:
                    calls.append(("probe_youtube", {"video": probe}))
                if download:
                    calls.append(("download_permitted_video", {"video": probe or "dYrEeavC3cw", "rights": "owned"}))
                for name, args in calls:
                    res = await session.call_tool(name, args)
                    payload = _attr(res, "structuredContent", "structured_content")
                    if payload is None:
                        payload = json.loads(res.content[0].text)
                    report["calls"][name] = {"isError": bool(_attr(res, "isError", "is_error")), **payload}
    except BaseException as exc:  # noqa: BLE001 - anyio wraps failures in exception groups
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        msg = repr(exc)
        report["error"] = (msg.replace(token, "[token]") if token else msg)[:400]
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--probe", help="also call probe_youtube with this video id/URL")
    ap.add_argument("--out", help="write the JSON report here (never contains the token)")
    a = ap.parse_args()
    token = os.environ.get("KOSIF_GATEWAY_TOKEN", "")
    if not token:
        ap.error("set KOSIF_GATEWAY_TOKEN in the environment")
    report = asyncio.run(run_check(a.url, token, a.probe))
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fp:
            fp.write(text)
    return 0 if report["initialize"]["ok"] and "gateway_status" in report["calls"] else 1


if __name__ == "__main__":
    sys.exit(main())
