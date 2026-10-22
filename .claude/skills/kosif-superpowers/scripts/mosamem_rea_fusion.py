#!/usr/bin/env python3
"""KOSIF Superpowers: independent Mosamem + REA capability bridge.

Reads a source-informed capability matrix, inspects *headers* of authorized
local image assets, and routes REA through the existing consent-gated bridge.
It DOES NOT embed GPL Mosamem source, control its GUI, install executables,
download models, or claim an analysis was performed when it wasn't.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import struct
import sys

SOURCE_MOSAMEM = "https://github.com/motalim-ai/mosamem/tree/v0.1.0"
SOURCE_REA = "https://github.com/morluto/rea"
MAX_INPUT = 512 * 1024 * 1024
SKILL_ROOT = Path(__file__).resolve().parent.parent
CAPABILITIES = SKILL_ROOT / "data" / "mosamem_rea_capabilities.json"


def registry():
    data = json.loads(CAPABILITIES.read_text(encoding="utf-8"))
    if data.get("schema") != "kosif.mosamem_rea_capabilities.v1" or len(data.get("capabilities", [])) < 12:
        raise ValueError("capability manifest absent or malformed")
    ids = [c.get("id") for c in data["capabilities"]]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate capability ID")
    return data


def read_rea():
    path = Path(__file__).with_name("rea_bridge.py")
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("kosif_rea_bridge", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def environment():
    rea = read_rea()
    info = rea.environment() if rea else {"rea_installed": False, "node_compatible": False}
    # A non-running app can still be installed. Do not pretend to detect it.
    if os.name == "nt":
        candidates = [Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Mosamem" / "Mosamem.exe",
                      Path(os.environ.get("PROGRAMFILES", "")) / "Mosamem" / "Mosamem.exe"]
    elif sys.platform == "darwin":
        candidates = [Path("/Applications/Mosamem.app")]
    else:
        candidates = []
    present = [str(p) for p in candidates if p.is_file() or p.is_dir()]
    return {
        "status": "ENVIRONMENT_PROBE_ONLY",
        "mosamem_installed_at_known_path": bool(present),
        "mosamem_paths": present,
        "mosamem_headless_api": "NOT_DOCUMENTED_FOR_v0.1.0",
        "rea": info,
        "python": sys.version.split()[0],
        "feature_implementation": "INDEPENDENT_ROUTING_AND_HEADER_PREFLIGHT_ONLY",
        "analysis_executed": False,
    }


def _checked_file(path):
    p = Path(path).expanduser()
    if not p.is_file() or p.is_symlink():
        raise ValueError("input must be an existing regular non-symlink file")
    n = p.stat().st_size
    if not 1 <= n <= MAX_INPUT:
        raise ValueError("input size outside supported range")
    return p, n


def _sha256(p):
    d = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            d.update(block)
    return d.hexdigest()


def _psd_header(f):
    data = f.read(26)
    if len(data) != 26 or data[:4] != b"8BPS":
        raise ValueError("not PSD/PSB")
    version = struct.unpack(">H", data[4:6])[0]
    if version not in (1, 2) or data[6:12] != b"\0"*6:
        raise ValueError("invalid PSD header")
    channels, height, width, depth, mode = struct.unpack(">HIIHH", data[12:26])
    if not (1 <= channels <= 56 and 1 <= height <= 300000 and 1 <= width <= 300000 and depth in (1, 8, 16, 32)):
        raise ValueError("invalid PSD dimensions/depth")
    names = {0:"bitmap",1:"grayscale",2:"indexed",3:"RGB",4:"CMYK",7:"multichannel",8:"duotone",9:"Lab"}
    alerts = []
    if mode != 3:
        alerts.append("MOSAMEM_PSD_RGB_ONLY_FIDELITY_NOT_ASSURED")
    if depth != 8:
        alerts.append("PSD_8BIT_FIDELITY_NOT_ASSURED")
    if version == 2:
        alerts.append("PSB_COMPATIBILITY_NOT_VERIFIED")
    alerts.append("LAYER_EFFECTS_FONTS_MASKS_AND_ADVANCED_BLEND_MAY_DIFFER")
    return {"type":"PSB" if version == 2 else "PSD","width":width,"height":height,
            "channels":channels,"bits_per_channel":depth,"color_mode":names.get(mode,"unknown"),
            "color_mode_code":mode, "risk_flags":alerts,
            "limitations": "Header-only. NO layers were decoded or PSD compositing performed."}


def _png_header(f):
    h = f.read(26)
    if len(h) < 26 or h[:8] != b"\x89PNG\r\n\x1a\n" or h[12:16] != b"IHDR":
        raise ValueError("invalid PNG header")
    w, hgt, depth, ct = struct.unpack(">IIBB",h[16:26])
    if not (1 <= w <= 100000 and 1 <= hgt <= 100000 and depth in (1,2,4,8,16) and ct in (0,2,3,4,6)):
        raise ValueError("invalid PNG dimensions")
    return {"type":"PNG","width":w,"height":hgt,"bits_per_channel":depth,
            "alpha_possible":ct in (4,6),
            "risk_flags":[], "limitations":"Header-only. Transparency and actual pixel quality not verified."}


def _jpeg_header(f):
    if f.read(2) != b"\xff\xd8":
        raise ValueError("invalid JPEG SOI")
    checked=2
    while checked < 1048576:
        x=f.read(1)
        if not x: break
        checked+=1
        if x != b"\xff": continue
        marker=f.read(1)
        checked+=1
        while marker==b"\xff":
            marker=f.read(1);checked+=1
        if not marker: break
        code=marker[0]
        if code in (0xd8,0xd9,0x01) or 0xd0 <= code <= 0xd7: continue
        if code==0xda: break
        length_bytes=f.read(2);checked+=2
        if len(length_bytes)!=2: break
        length=struct.unpack(">H",length_bytes)[0]
        if length<2: break
        if code in (0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf):
            payload=f.read(5)
            if len(payload)!=5: break
            depth,height,width=struct.unpack(">BHH",payload)
            if width==0 or height==0: break
            return {"type":"JPEG","width":width,"height":height,"bits_per_channel":depth,
                    "risk_flags":["JPEG_NO_ALPHA_CHANNEL"],"limitations":"Header-only. Pixel quality and EXIF orientation not evaluated."}
        f.seek(length-2,1)
        checked+=length-2
    raise ValueError("no valid bounded JPEG frame header")


def inspect_asset(path):
    p, n = _checked_file(path)
    with p.open("rb") as f:
        magic=f.read(16)
        f.seek(0)
        if magic.startswith(b"8BPS"):
            report=_psd_header(f)
        elif magic.startswith(b"\x89PNG\r\n\x1a\n"):
            report=_png_header(f)
        elif magic.startswith(b"\xff\xd8"):
            report=_jpeg_header(f)
        elif magic.startswith(b"SQLite format 3"):
            report={"type":"SQLITE_UNCLASSIFIED","risk_flags":["DO_NOT_INFER_MOSAMEM_FROM_SQLITE"],
                    "limitations":"No database tables or private document content inspected."}
        else:
            report={"type":"UNKNOWN","risk_flags":["NO_PARSER_AVAILABLE"],
                    "limitations":"Only PNG/JPEG/PSD and SQLite file signature are recognized."}
    return {"schema":"kosif.asset_preflight.v1","status":"READ_ONLY_HEADER_INSPECTION",
            "file_name":p.name,"bytes":n,"sha256":_sha256(p),"asset":report,
            "source_limit":"Mosamem v0.1.0 PSD fidelity figures are the upstream project's own benchmark, NOT validation of this asset."}


def _route_for(category, reg):
    rows=[r for r in reg["capabilities"] if r["domain"]==category]
    return [{"id":r["id"],"feature":r["feature_ar"],"upstream_support":r["source_evidence"],
             "local_handoff":r["handoff"],"native_implementation":r["implementation"],
             "risks":r.get("risks",[])} for r in rows]


def plan(goal, domain="auto"):
    if not goal or len(goal)>1500:
        raise ValueError("goal must have 1–1500 characters")
    lower=goal.lower()
    if domain == "auto":
        if any(x in lower for x in ("rea","ghidra","هندسة عكسية","تحليل تطبيق","reverse","binary","تطبيق")):
            domain="investigation"
        elif any(x in lower for x in ("فيديو","مونتاج","motion","video","ريلز")):
            domain="motion"
        else:
            domain="image"
    if domain not in ("image","motion","investigation"):
        raise ValueError("unsupported domain")
    reg=registry()
    return {"schema":"kosif.mosamem_rea.fusion_plan.v1","status":"PLAN_ONLY_NO_EXECUTION",
        "goal":goal,"domain":domain,"sources":reg["sources"],"selected_capabilities":_route_for(domain,reg),
        "workflow":[
            {"node":"N1","action":"Audit authorized inputs and preserve source hashes","output":"asset manifest","verified":False},
            {"node":"N2","action":"Apply source-backed skills through existing KOSIF tools or user-operated Mosamem GUI","output":"editable creative artifact or plan","verified":False},
            {"node":"N3","action":"If needed, request explicit approval for bounded REA static analysis using existing rea_bridge.py","output":"local evidence packet","verified":False},
            {"node":"N4","action":"Compare pixel/PSD/Arabic QA and re-open exports in the target application","output":"measured and independently reviewed QA","verified":False},
            {"node":"N5","action":"Store only a tested, project-isolated FusionForge recipe","output":"eligible recipe, not model-weight training","verified":False},
        ],
        "limits":["Mosamem is GPL-3.0-or-later; NO source code included here.",
                  "Mosamem v0.1.0 desktop release has no proven remote/headless control API.",
                  "REA methods existing in KOSIF are already catalogued; registration is not runtime execution.",
                  "Do not run any native binaries or download models automatically.",
                  "Different companies/assets remain isolated; do not commit personal images or private REA evidence.",
                  "Katana remains analysis-only, no generation spend."],
        "executed":False,"verified":False}


def rea_plan(kind, target):
    rea = read_rea()
    if not rea:
        return {"status":"REA_BRIDGE_MISSING","analysis_executed":False}
    return rea.inspect_plan(kind,target)


def fresh_json(path,obj):
    p=Path(path)
    if p.exists() or p.is_symlink() or not p.parent.is_dir():
        raise ValueError("output exists or parent missing")
    with p.open("x",encoding="utf-8") as f:
        json.dump(obj,f,ensure_ascii=False,indent=2)
        f.write("\n")


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="cmd",required=True)
    sub.add_parser("doctor")
    sub.add_parser("catalog")
    ins=sub.add_parser("inspect");ins.add_argument("path")
    p=sub.add_parser("plan");p.add_argument("goal");p.add_argument("--domain",choices=("auto","image","motion","investigation"),default="auto")
    rp=sub.add_parser("rea-plan");rp.add_argument("kind");rp.add_argument("path")
    for x in (ins,p,rp): x.add_argument("--out")
    args=ap.parse_args(argv)
    try:
        if args.cmd=="doctor": result=environment()
        elif args.cmd=="catalog": result=registry()
        elif args.cmd=="inspect": result=inspect_asset(args.path)
        elif args.cmd=="plan": result=plan(args.goal,args.domain)
        else: result=rea_plan(args.kind,args.path)
        if getattr(args,"out",None): fresh_json(args.out,result)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,TypeError,ImportError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"ERROR","error":str(exc),"analysis_executed":False}),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
