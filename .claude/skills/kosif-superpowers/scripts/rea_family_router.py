#!/usr/bin/env python3
"""KOSIF REA capability router — full upstream family discovery; no automatic execution.

This does not copy REA or install it. For supported installed versions, consult the
package-matched upstream skill and MCP tool schema, not this mapping alone.
"""
from __future__ import annotations
import argparse
import json
import shutil

FAMILIES={
    "native":{"examples":["Mach-O","ELF","PE","xrefs","function pseudocode"],"status":"provider_required","tool":"open_binary"},
    "managed":{"examples":["CIL","P/Invoke",".NET assembly"],"status":"static_plan","tool":"inspect-managed-artifact"},
    "javascript":{"examples":["ASAR","Electron bundle","sourcemap"],"status":"static_plan","tool":"analyze-javascript-application"},
    "android":{"examples":["APK","classes","manifest"],"status":"provider_required","tool":"inspect_android_package"},
    "packages":{"examples":["ZIP","IPA","MSIX","AppX","archive"],"status":"inspect_with_approval","tool":"open_binary"},
    "browser":{"examples":["Chrome","CDP","DOM","network timeline"],"status":"live_permission_required","tool":"list_browser_targets"},
    "electron":{"examples":["Electron renderer","file URL"],"status":"scoped_permission_required","tool":"passive_electron_observation"},
    "node":{"examples":["V8 Inspector","scriptParsed","execution context"],"status":"live_permission_required","tool":"inspect_node_target"},
    "captures":{"examples":["HAR","SAZ","qlog","network capture"],"status":"scoped_permission_required","tool":"inspect_web_network_capture"},
    "process":{"examples":["process behavior","runtime compare"],"status":"execution_permission_required","tool":"controlled_process_capture"},
    "firmware":{"examples":["firmware regions","Binwalk","Unblob"],"status":"provider_required","tool":"inspect_firmware_regions"},
    "sqlite":{"examples":["SQLite","schema","indexes"],"status":"static_plan","tool":"inspect-sqlite-database"},
    "go":{"examples":["Go executable metadata"],"status":"static_plan","tool":"inspect-go-binary"},
    "rust":{"examples":["Rust executable metadata"],"status":"static_plan","tool":"inspect-rust-binary"},
    "apple":{"examples":["plist","app signing","Mach-O metadata"],"status":"platform_required","tool":"native_macos_utilities"},
    "evidence":{"examples":["Evidence v2","application graph","comparison"],"status":"requires_upstream_result","tool":"inspect_analysis_view"},
}
INTENT={
    "application-binary":"native","native":"native","binary":"native",
    "dotnet":"managed","c#":"managed","javascript":"javascript","asar":"javascript","source-map":"javascript",
    "apk":"android","android":"android","zip":"packages","ios-package":"packages",
    "chrome":"browser","website":"browser","electron":"electron","v8":"node","node":"node",
    "har":"captures","saz":"captures","qlog":"captures","network-capture":"captures",
    "process":"process","firmware":"firmware","sqlite":"sqlite","go":"go","rust":"rust",
    "plist":"apple","app-graph":"evidence","evidence":"evidence"
}
def route(intent):
    family=INTENT.get(intent.strip().lower())
    if not family:
        return {"status":"not_an_rea_target","verified":False,
                "instruction":"Use ordinary source search, KOSIF motion/typography tools or ask for artifact type"}
    profile=FAMILIES[family]
    return {"status":"route_only_not_executed","family":family,**profile,
            "requires":["authorized target","compatible installed REA version","exposed current CLI or MCP tool"],
            "verified":False,"executed":False,"provider_version":"unknown"}

def doctor():
    return {"status":"probe_only","rea_executable":bool(shutil.which("rea")),
            "node_present":bool(shutil.which("node")),
            "mcp_connected":"unknown_not_measured",
            "install":"npx -y rea-agents@latest setup --client claude_code --dry-run --json",
            "installation_authorized":False,"version_verified":False}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("action",choices=["list","route","doctor"])
    p.add_argument("intent",nargs="?")
    a=p.parse_args(argv)
    if a.action=="list":v={"families":FAMILIES,"count":len(FAMILIES),"status":"guidance_only"}
    elif a.action=="doctor":v=doctor()
    else:
        if not a.intent:p.error("route requires an intent keyword")
        v=route(a.intent)
    print(json.dumps(v,ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__":raise SystemExit(main())
