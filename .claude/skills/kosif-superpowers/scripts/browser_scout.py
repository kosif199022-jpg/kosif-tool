#!/usr/bin/env python3
"""Read-only KOSIF browser site survey with a fresh isolated Playwright context.

No credentials, clicks, uploads, installs, proxy tunneling, stored cookies or external code imports.
This is a LOCAL proof-of-concept, NOT a deployed cloud browser or hardened internet sandbox.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

SK=Path(__file__).resolve().parent.parent
CATALOG=SK/"data"/"integration-target-atlas.json"

def entries():
    data=json.loads(CATALOG.read_text(encoding="utf-8-sig"))
    if not isinstance(data,list) or len(data)<18:
        raise ValueError("incomplete source target atlas")
    ids=set()
    for row in data:
        if not isinstance(row,dict) or any(not row.get(k) for k in ("id","url","category","approach","feature")):
            raise ValueError("invalid target entry")
        if row["id"] in ids:
            raise ValueError("duplicate target id")
        ids.add(row["id"])
        check_url(row["url"], allow_host=urlsplit(row["url"]).hostname)
    return data

def check_url(value, allow_host):
    try:
        u=urlsplit(value)
        # Prevent credentials, arbitrary ports, query-based URL tricks, local files, and internal origins.
        if (not isinstance(value,str) or u.scheme != "https" or not u.hostname or u.username
            or u.password or u.port not in (None,443) or u.fragment or u.hostname != allow_host
            or "." not in u.hostname or u.hostname.startswith(("localhost.","127.","10.","192.168."))):
            raise ValueError("outside explicitly allowed HTTPS host")
    except (ValueError, TypeError) as exc:
        raise ValueError("blocked URL") from exc
    return u.hostname

def lookup(name):
    match=[x for x in entries() if x["id"] == name]
    if not match:
        raise ValueError("unknown target id")
    return match[0]

def survey(row, target_path, browser="chromium", seconds=20):
    if browser not in ("chromium","firefox","webkit"):
        raise ValueError("unsupported browser engine")
    if not 5 <= seconds <= 40:
        raise ValueError("timeout out of bounds")
    dest=Path(target_path)
    if dest.suffix.lower() != ".png" or dest.exists() or not dest.parent.is_dir():
        raise ValueError("output must be an unused PNG in an existing folder")
    host=check_url(row["url"],urlsplit(row["url"]).hostname)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise ValueError("Playwright not installed") from exc
    with sync_playwright() as p:
        engine=getattr(p,browser)
        instance=engine.launch(headless=True)
        context=instance.new_context(accept_downloads=False,service_workers="block",
                                     permissions=[],ignore_https_errors=False)
        try:
            page=context.new_page()
            def guard(route):
                try:
                    check_url(route.request.url,host)
                except (ValueError,TypeError):
                    route.abort()
                    return
                route.continue_()
            page.route("**/*",guard)
            response=page.goto(row["url"],wait_until="domcontentloaded",timeout=seconds*1000)
            page.screenshot(path=str(dest),full_page=False,timeout=seconds*1000)
            return {"target":row["id"],"engine":browser,"status":response.status if response else None,
                    "title":page.title()[:180],"screenshot":str(dest),
                    "sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),
                    "bytes":dest.stat().st_size,"cookies_saved":False,"network_host":host,
                    "cloud_deployed":False}
        finally:
            context.close()
            instance.close()

def main():
    ap=argparse.ArgumentParser(description="KOSIF local isolated read-only browser research")
    sub=ap.add_subparsers(dest="cmd",required=True)
    sub.add_parser("doctor")
    list_cmd=sub.add_parser("list")
    view=sub.add_parser("inspect");view.add_argument("id")
    run=sub.add_parser("capture")
    run.add_argument("id");run.add_argument("--output",required=True)
    run.add_argument("--engine",choices=("chromium","firefox","webkit"),default="chromium")
    args=ap.parse_args()
    try:
        if args.cmd=="doctor":
            out={"targets":len(entries()),"playwright_installed":bool(importlib.util.find_spec("playwright")),
                 "engines":["chromium","firefox","webkit"],"local_prototype":True,
                 "production_cloud_browser":False,"allows_auth":False}
        elif args.cmd=="list":
            out=[{"id":x["id"],"category":x["category"],"feature":x["feature"]} for x in entries()]
        elif args.cmd=="inspect":
            out=lookup(args.id)
        else:
            out=survey(lookup(args.id),args.output,args.engine)
        print(json.dumps(out,ensure_ascii=False,indent=2));return 0
    except (ValueError, OSError, TimeoutError) as e:
        print(json.dumps({"ok":False,"error":str(e)},ensure_ascii=False),file=sys.stderr);return 1

if __name__=="__main__":
    raise SystemExit(main())
