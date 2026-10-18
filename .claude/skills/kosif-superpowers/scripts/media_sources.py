#!/usr/bin/env python3
"""KOSIF Licensed Media Gateway: discover 100 sources; acquire rights-cleared footage for editing.

This gateway does NOT grant a license. It requires asset-specific provenance supplied
by the operator and invokes the existing fetch_video.py extractor without DRM bypass.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "media_sources_100.json"
FETCHER = ROOT / "scripts" / "fetch_video.py"
RIGHTS = ("owned", "cc0", "public-domain", "cc-by", "cc-by-sa", "stock-license", "direct-permission")
MEDIA_TYPES = ("video_image", "image", "open_collections", "graphics_texture")

def load_sources() -> list[dict]:
    obj = json.loads(CATALOG.read_text(encoding="utf-8"))
    sites = obj["sources"]
    assert len(sites) == 100 and len({s["domain"] for s in sites}) == 100, "invalid stock source catalog"
    return sites

def source_for(url: str, sites: list[dict]) -> dict | None:
    host = (urlsplit(url).hostname or "").lower().rstrip(".")
    return next((s for s in sites if host == s["domain"] or host.endswith("." + s["domain"])), None)

def validate_license(url: str, rights: str | None, evidence_url: str | None,
                     creator: str | None, credit: str | None) -> list[str]:
    problems = []
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        problems.append("an HTTP(S) media URL without embedded credentials is required")
    if rights not in RIGHTS:
        problems.append("explicit --rights is required (not inferred from the website)")
    if rights != "owned":
        ev = urlsplit(evidence_url or "")
        if ev.scheme != "https" or not ev.hostname:
            problems.append("non-owned media requires an HTTPS --evidence-url proving asset rights")
    if rights in {"cc-by", "cc-by-sa"} and (not creator or not credit):
        problems.append("CC BY/SA media requires --creator and --credit")
    if rights == "stock-license" and not credit:
        problems.append("stock-license requires --credit (may say 'not required' if supported by terms)")
    return problems

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def safe_output_manifest(out: Path, url: str) -> dict | None:
    fp = out / "manifest.json"
    if not fp.exists():
        return None
    try:
        results = json.loads(fp.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None
    for item in reversed(results):
        if item.get("url") == url and item.get("file"):
            return item
    return None

def execute_download(args, sites: list[dict]) -> int:
    problems = validate_license(args.url, args.rights, args.evidence_url, args.creator, args.credit)
    if problems:
        for problem in problems:
            print("RIGHTS CHECK: " + problem, file=sys.stderr)
        return 2
    src = source_for(args.url, sites)
    if args.site and not any(s["domain"] == args.site for s in sites):
        print("unknown --site domain in 100-source catalog", file=sys.stderr)
        return 2
    if args.site and src and src["domain"] != args.site:
        print("the provided --site does not match the URL host", file=sys.stderr)
        return 2
    chosen = src or next((s for s in sites if s["domain"] == args.site), None)
    out = Path(args.out).expanduser().resolve()
    cmd = [sys.executable, str(FETCHER), args.url, "-o", str(out),
           "--quality", args.quality]
    if args.safe and args.quality != "audio":
        cmd.append("--safe")
    if args.dry_run:
        print(json.dumps({"action": "dry_run_no_download", "command": cmd,
                          "matched_source": chosen["name"] if chosen else None,
                          "rights_asserted": args.rights, "rights_evidence": args.evidence_url}, indent=2))
        return 0
    out.mkdir(parents=True, exist_ok=True)
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)
    except subprocess.TimeoutExpired:
        print("download timed out; no success asserted", file=sys.stderr)
        return 1
    if done.returncode:
        print("download failed: " + done.stderr[-1000:], file=sys.stderr)
        return done.returncode
    result = safe_output_manifest(out, args.url)
    if result is None:
        print("download returned no matching completed asset; refusing unverified success", file=sys.stderr)
        return 1
    chosen_path = Path(result.get("safe_file") or result["file"])
    if not chosen_path.is_file() or not chosen_path.stat().st_size:
        chosen_path = Path(result["file"])
    if not chosen_path.is_file() or not chosen_path.stat().st_size:
        print("missing media file; refusing unverified success", file=sys.stderr)
        return 1
    asset = {"downloaded_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
             "source_url": args.url, "catalog_site": chosen["name"] if chosen else None,
             "original_file": result["file"], "editing_file": str(chosen_path),
             "sha256": sha256_file(chosen_path), "rights": args.rights,
             "evidence_url": args.evidence_url, "creator": args.creator,
             "credit": args.credit, "verified_by": "user/operator rights assertion; not legal audit",
             "license_reviewed_for_this_asset": True}
    with (out / "asset_rights.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(asset, ensure_ascii=False) + "\n")
    print(json.dumps(asset, ensure_ascii=False, indent=2))
    return 0

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="action", required=True)
    sub.add_parser("list", help="list all 100 discovery sources")
    se = sub.add_parser("search", help="find sites by term, media type, rights hint")
    se.add_argument("term", nargs="?", default="")
    se.add_argument("--type", choices=MEDIA_TYPES)
    plan = sub.add_parser("plan", help="print workflow and legal prerequisites")
    plan.add_argument("url")
    down = sub.add_parser("download", help="retrieve a permitted URL for montage, recording provenance")
    down.add_argument("url")
    down.add_argument("--rights", choices=RIGHTS, required=True,
                      help="operator-verified per-asset rights; a site name alone is never sufficient")
    down.add_argument("--evidence-url", help="HTTPS link to item license or written permission")
    down.add_argument("--creator", help="creator attribution for CC BY/SA")
    down.add_argument("--credit", help="credit text or 'not required' under site terms")
    down.add_argument("--site", help="optional original 100-source catalog domain for CDN media URLs")
    down.add_argument("--quality", default="1080", choices=["best", "2160", "1080", "720", "480", "audio"])
    down.add_argument("-o", "--out", default="media_assets")
    down.add_argument("--safe", action=argparse.BooleanOptionalAction, default=True,
                      help="add edit-friendly H.264/AAC MP4 using ffmpeg (default on)")
    down.add_argument("--dry-run", action="store_true", help="verify rights and show command; no network or download")
    args = ap.parse_args(argv)
    sites = load_sources()
    if args.action == "list":
        for s in sites:
            print("%s  %-34s %-17s %s" % (s["id"], s["name"], s["type"], s["url"]))
        return 0
    if args.action == "search":
        matched = [s for s in sites if (not args.type or s["type"] == args.type)
                   and args.term.casefold() in (s["name"] + " " + s["domain"] +
                                                 " " + s["license_hint"]).casefold()]
        for s in matched:
            print("%s | %s | %s | %s | CHECK ITEM LICENSE" %
                  (s["id"], s["name"], s["type"], s["url"]))
        print("%s result(s)" % len(matched))
        return 0 if matched else 1
    if args.action == "plan":
        s = source_for(args.url, sites)
        print(json.dumps({"source": s, "requirement": "Confirm asset-specific commercial editing permission",
                          "accepted_rights": list(RIGHTS), "suggested_tool": "download",
                          "restrictions": "no DRM bypass, paywall bypass, bulk rehosting or license assumptions"}, indent=2))
        return 0
    return execute_download(args, sites)

if __name__ == "__main__":
    raise SystemExit(main())
