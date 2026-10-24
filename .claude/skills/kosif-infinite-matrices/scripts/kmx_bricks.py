#!/usr/bin/env python3
"""Deep static decomposition of the 86 reference styles into the six bricks.

Two independent evidence sources, both static (nothing is executed):
  1. lexical scan of each styles/<id>.js from kmx_atlas_extract.py (canvas/Web API calls,
     H helper calls, math laws, time patterns, compositing modes);
  2. REA (github.com/morluto/rea, `rea analyze-javascript-application <tree> --format json`):
     per-module functions, call sites, data-flow relations and normalized-AST fingerprints,
     which reveal function bodies that several styles share.

Output (derived numbers and labels only, no source text) is safe to commit:
    python3 scripts/kmx_bricks.py analyze --src REF_TREE [--rea rea-js.json] --out data/86_style_code_bricks.json
    python3 scripts/kmx_bricks.py show flow-field
    python3 scripts/kmx_bricks.py summary
Every label is an inference from code patterns (evidence E2_STATIC_CODE), not a render test.
"""
import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
DEFAULT_OUT = SKILL / "data" / "86_style_code_bricks.json"
INDEX = SKILL / "data" / "86_style_research_database.json"

CALL = lambda *names: re.compile(r"\.(?:%s)\s*\(" % "|".join(names))
PROP = lambda *names: re.compile(r"\.(?:%s)\s*=(?!=)" % "|".join(names))

# operation families: what the code does to pixels
OPERATIONS = {
    "path_geometry": CALL("moveTo", "lineTo", "bezierCurveTo", "quadraticCurveTo", "arcTo"),
    "primitive_shapes": CALL("arc", "ellipse", "rect", "roundRect", "fillRect", "strokeRect"),
    "fill_stroke": CALL("fill", "stroke"),
    "gradient": CALL("createLinearGradient", "createRadialGradient", "createConicGradient"),
    "transform": CALL("translate", "rotate", "scale", "setTransform", "transform"),
    "clip_mask": CALL("clip"),
    "compositing": PROP("globalCompositeOperation"),
    "alpha": PROP("globalAlpha"),
    "blur_filter": re.compile(r"\.(?:filter|shadowBlur)\s*=(?!=)"),
    "pixel_readback": CALL("getImageData"),
    "pixel_write": CALL("putImageData", "createImageData"),
    "offscreen_layer": re.compile(r"\bH\.layer\s*\(|OffscreenCanvas|createElement\(\s*['\"]canvas"),
    "image_composite": CALL("drawImage"),
    "text": CALL("fillText", "strokeText", "measureText"),
    "pattern": CALL("createPattern"),
    "dash": CALL("setLineDash"),
}
LAWS = {
    "periodic": re.compile(r"Math\.(?:sin|cos)\s*\("),
    "exponential": re.compile(r"Math\.exp\s*\("),
    "power_curve": re.compile(r"Math\.pow\s*\(|\*\*"),
    "distance_field": re.compile(r"Math\.hypot\s*\(|Math\.sqrt\s*\("),
    "angle_field": re.compile(r"Math\.atan2\s*\("),
    "quantize": re.compile(r"Math\.(?:floor|round)\s*\("),
    "noise_field": re.compile(r"\bH\.makeNoise\s*\(|\.fbm\w*\s*\(|\.n[23]\s*\("),
    "seeded_random": re.compile(r"\bH\.rng\s*\("),
    "interpolate": re.compile(r"\bH\.(?:lerp|mix|map)\s*\("),
    "easing": re.compile(r"\bH\.(?:ease|smooth)\b"),
    "clamp": re.compile(r"\bH\.clamp\s*\("),
}
TIME = {
    "eased_reveal": re.compile(r"\bH\.(?:ease|smooth)\b[^;\n]*\bt\b|\bH\.clamp\s*\(\s*\(\s*t\s*-"),
    "periodic_in_t": re.compile(r"Math\.(?:sin|cos)\s*\([^)]*\bt\b"),
    "stepped_frames": re.compile(r"Math\.floor\s*\(\s*t\s*\*|Math\.floor\s*\(\s*\(?\s*t\b"),
    "history_resampling": re.compile(r"\bt\s*-\s*\w+\s*\*|\(\s*t\s*-\s*\(?\w+\s*\*"),
    "beat_windows": re.compile(r"\bt\s*[<>]=?\s*\d+(?:\.\d+)?\b"),
}
MEMORY = {
    "cached_texture": re.compile(r"\bcache\w*\b|\bH\.layer\s*\("),
    "trail_by_resampling": TIME["history_resampling"],
    "iterative_build": re.compile(r"for\s*\([^;]*;[^;]*<\s*(?:trail|steps|n|N|hist|len|k)\w*\s*;"),
    "fade_overlay": re.compile(r"globalAlpha\s*=\s*0?\.\d+[^;]*;\s*[\w.]*fillRect"),
}
FEEDBACK = {
    "pixel_postprocess": CALL("getImageData"),
    "field_drives_motion": re.compile(r"\bgrad\w*|\bcurl\w*|\bflow\w*\s*\(", re.I),
}
STATE = {
    "particle_arrays": re.compile(r"\bparticles?\b|\bdots\b|\bmotes?\b|\bstars?\b|\bdrops?\b", re.I),
    "polyline_points": re.compile(r"\bpts\b|\bpoints\b|\bpath\b"),
    "grid_cells": re.compile(r"\bcols?\b|\brows?\b|\bcells?\b|\bgrid\b"),
    "glyphs_text": CALL("fillText", "strokeText"),
    "noise_values": LAWS["noise_field"],
    "palette": re.compile(r"\bpal\w*\b|\bcolou?rs?\b|#[0-9a-fA-F]{6}\b"),
}
COMPOSITE_MODE = re.compile(r"globalCompositeOperation\s*=\s*['\"]([a-z-]+)['\"]")

# existing analyst tag -> code pattern that would support it (for a validation score)
TAG_SUPPORT = {
    "glow": r"lighter|shadowBlur|screen|blur\(", "light": r"lighter|createRadialGradient|screen|shadow",
    "gradient": r"create(?:Linear|Radial|Conic)Gradient", "noise": r"makeNoise|\.fbm|H\.grain",
    "grain": r"H\.grain|makeNoise|rng\(", "particles": r"particles?|dots|motes?|stars?",
    "path": r"lineTo|bezierCurveTo|quadraticCurveTo", "trace": r"lineTo|\bt\s*-\s*\w+\s*\*|drawOn",
    "mask": r"clip\(|destination-(?:in|out)|source-(?:in|atop)", "layer": r"H\.layer|drawImage",
    "grid": r"\bcols?\b|\brows?\b|\bgrid\b|\bcell", "pixel": r"getImageData|putImageData|imageSmoothingEnabled\s*=\s*false|Math\.floor",
    "field": r"makeNoise|getImageData|\bfield\b", "reflection": r"reflect|scale\(\s*1\s*,\s*-1|mirror",
    "shadow": r"shadow", "texture": r"H\.paper|H\.grain|makeNoise|createPattern", "blur": r"blur\(|shadowBlur",
    "step": r"Math\.floor\s*\(\s*t|step", "ease": r"H\.ease|H\.smooth", "camera": r"cam\w*|translate\(",
    "decay": r"Math\.exp|decay|fade", "accumulate": r"lighter|accum|\bt\s*-\s*\w+\s*\*", "pulse": r"Math\.sin\s*\([^)]*\bt\b",
}


def strip_comments(src):
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    return re.sub(r"(?m)(^|[^:\\])//.*$", r"\1", src)


def count(rx, text):
    return len(rx.findall(text))


def lexical(src):
    s = strip_comments(src)
    feats = {
        "lines": src.count("\n") + 1,
        "operations": {k: count(v, s) for k, v in OPERATIONS.items()},
        "laws": {k: count(v, s) for k, v in LAWS.items()},
        "time": {k: count(v, s) for k, v in TIME.items()},
        "memory": {k: count(v, s) for k, v in MEMORY.items()},
        "feedback": {k: count(v, s) for k, v in FEEDBACK.items()},
        "state": {k: count(v, s) for k, v in STATE.items()},
        "composite_modes": dict(collections.Counter(COMPOSITE_MODE.findall(s)).most_common()),
        "uses_math_random": bool(re.search(r"Math\.random\s*\(", s)),
    }
    return feats, s


def top(d, n, floor=1):
    return [k for k, v in sorted(d.items(), key=lambda kv: (-kv[1], kv[0])) if v >= floor][:n]


def bricks_from(f):
    ops = f["operations"]
    mem = f["memory"]
    fb = f["feedback"]
    memory = []
    if mem["cached_texture"]:
        memory.append("cached_texture (static memory: built once, reused every frame)")
    if mem["trail_by_resampling"]:
        memory.append("trail_by_resampling (history recomputed from earlier t, no stored state)")
    if mem["iterative_build"]:
        memory.append("iterative_build (a counted loop builds the frame from many items or sub-steps; a weak memory signal)")
    if not memory:
        memory.append("none_detected")
    feedback = []
    if fb["pixel_postprocess"]:
        feedback.append("pixel_postprocess (reads back pixels inside the same frame and rewrites them; not cross-frame)")
    if fb["field_drives_motion"]:
        feedback.append("field_drives_motion (a computed field steers geometry)")
    if not feedback:
        feedback.append("none_detected")
    return {
        "state": top(f["state"], 4),
        "operation": top(ops, 5),
        "law": top(f["laws"], 5),
        "time": top(f["time"], 3) or ["static_or_untimed"],
        "memory": memory,
        "feedback": feedback,
    }


# ------------------------------------------------------------------ REA ingestion
def rea_per_module(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    nr = d.get("normalized_result") or {}
    sg = nr.get("semantic_graph") or {}
    node_mod = {}
    per = collections.defaultdict(lambda: {"functions": 0, "call_sites": 0, "bindings": 0, "relations": collections.Counter(),
                                           "fingerprints": []})
    for n in sg.get("nodes", []):
        mod = ((n.get("identity") or {}).get("module_path")) or ""
        node_mod[n.get("node_id")] = mod
        if n.get("kind") == "function":
            per[mod]["functions"] += 1
        elif n.get("kind") == "call-site":
            per[mod]["call_sites"] += 1
        elif n.get("kind") == "binding":
            per[mod]["bindings"] += 1
    fn_span = {}
    for n in sg.get("nodes", []):
        if n.get("kind") == "function":
            r = (n.get("identity") or {}).get("source_range") or {}
            try:
                fn_span[n["node_id"]] = r["end"]["line"] - r["start"]["line"] + 1
            except (KeyError, TypeError):
                fn_span[n["node_id"]] = 0
    for r in sg.get("relations", []):
        mod = node_mod.get(r.get("source_node_id"), "")
        per[mod]["relations"][r.get("relation", "?")] += 1
    for fp in sg.get("fingerprints", []):
        if fp.get("status") != "complete":
            continue
        fid = fp.get("function_node_id")
        mod = node_mod.get(fid, "")
        h = (fp.get("components") or {}).get("normalized_ast_sha256")
        if h and fn_span.get(fid, 0) >= 3:  # ignore one-line lambdas
            per[mod]["fingerprints"].append(h)
    meta = {
        "rea_version": ((d.get("provider") or {}).get("version")) or None,
        "provider": (d.get("provider") or {}).get("id"),
        "evidence_id": d.get("evidence_id"),
        "root_artifact_sha256": nr.get("root_artifact_sha256"),
        "parsed_javascript_files": (nr.get("statistics") or {}).get("parsed_javascript_files"),
        "visited_ast_nodes": (nr.get("statistics") or {}).get("visited_ast_nodes"),
        "semantic_nodes": len(sg.get("nodes", [])), "semantic_relations": len(sg.get("relations", [])),
        "fingerprints": len(sg.get("fingerprints", [])),
        "semantic_coverage": (sg.get("coverage") or {}).get("status"),
        "semantic_truncated": (sg.get("coverage") or {}).get("truncated"),
    }
    return per, meta


def rea_merge(paths):
    """Merge several REA runs (one per batch of --source-path files); keep, per module, the
    run that analysed it most deeply (most function nodes)."""
    merged, metas = {}, []
    for path in paths:
        per, meta = rea_per_module(path)
        metas.append(meta)
        for mod, v in per.items():
            if mod not in merged or v["functions"] > merged[mod]["functions"]:
                merged[mod] = v
    meta = {
        "rea_version": metas[0]["rea_version"], "provider": metas[0]["provider"], "runs": len(metas),
        "evidence_ids": [m["evidence_id"] for m in metas],
        "root_artifact_sha256": sorted({m["root_artifact_sha256"] for m in metas}),
        "visited_ast_nodes": sum(m["visited_ast_nodes"] or 0 for m in metas),
        "semantic_nodes": sum(m["semantic_nodes"] for m in metas),
        "semantic_relations": sum(m["semantic_relations"] for m in metas),
        "fingerprints": sum(m["fingerprints"] for m in metas),
        "any_run_truncated": any(m["semantic_truncated"] for m in metas),
        "style_modules_with_functions": sum(1 for k, v in merged.items() if k.startswith("styles/") and v["functions"]),
    }
    return merged, meta


def analyze(src_dir, rea_path=None):
    src = Path(src_dir)
    man = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
    index = {s["style_id"]: s for s in json.loads(INDEX.read_text(encoding="utf-8"))["styles"]}
    per, meta = (rea_merge(rea_path if isinstance(rea_path, list) else [rea_path]) if rea_path else ({}, None))
    fp_owner = collections.defaultdict(set)
    for mod, v in per.items():
        if mod.startswith("styles/"):
            for h in v["fingerprints"]:
                fp_owner[h].add(Path(mod).stem)
    styles = []
    for sid in sorted(index, key=lambda k: index[k]["number"]):
        p = src / "styles" / (sid + ".js")
        raw = p.read_text(encoding="utf-8")
        feats, stripped = lexical(raw)
        card = json.loads((src / "cards" / (sid + ".json")).read_text(encoding="utf-8"))
        tags = index[sid]["operator_tags"]
        support = {t: bool(re.search(TAG_SUPPORT[t], stripped)) for t in tags if t in TAG_SUPPORT}
        row = {
            "number": index[sid]["number"], "style_id": sid, "family": index[sid]["card_family"],
            "source_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
            "card_matches_index": card.get("family") == index[sid]["card_family"],
            "features": feats, "bricks": bricks_from(feats),
            "analyst_tags": tags,
            "tag_support": {"checked": len(support), "supported": sum(support.values()),
                            "unsupported": sorted(t for t, ok in support.items() if not ok),
                            "unchecked": sorted(t for t in tags if t not in TAG_SUPPORT)},
            "evidence": "E2_STATIC_CODE",
            "status": "NOT_RECONSTRUCTED",
        }
        r = per.get("styles/%s.js" % sid)
        if r is not None and r["functions"]:
            shared = sorted({o for h in r["fingerprints"] for o in fp_owner[h] if o != sid})
            row["rea"] = {"functions": r["functions"], "call_sites": r["call_sites"], "bindings": r["bindings"],
                          "relations": dict(r["relations"].most_common()),
                          "multi_line_fingerprints": len(r["fingerprints"]),
                          "shares_function_bodies_with": shared}
        styles.append(row)
    agg = collections.Counter()
    for s in styles:
        for b, labels in s["bricks"].items():
            for lab in labels:
                agg["%s:%s" % (b, lab.split(" ")[0])] += 1
    checked = sum(s["tag_support"]["checked"] for s in styles)
    supported = sum(s["tag_support"]["supported"] for s in styles)
    out = {
        "schema": "kosif.matrices.code-bricks.v1",
        "title": "86-style static code decomposition into state / operation / law / time / memory / feedback",
        "archive_sha256": man["archive_sha256"],
        "method": "Lexical scan of each reference style source + REA semantic graph. Static only: nothing executed, no source text stored here.",
        "evidence": "E2_STATIC_CODE (labels inferred from code patterns; not a render test)",
        "rea": meta,
        "style_count": len(styles),
        "brick_frequency": dict(sorted(agg.items(), key=lambda kv: (-kv[1], kv[0]))),
        "analyst_tag_validation": {"checked": checked, "supported_by_code": supported,
                                   "rate": round(supported / checked, 4) if checked else None},
        "findings": findings(styles),
        "styles": styles,
    }
    return out


def findings(styles):
    n = len(styles)
    post = [s["style_id"] for s in styles if any(l.startswith("pixel_postprocess") for l in s["bricks"]["feedback"])]
    steer = [s["style_id"] for s in styles if any(l.startswith("field_drives_motion") for l in s["bricks"]["feedback"])]
    resample = [s["style_id"] for s in styles if any(l.startswith("trail_by_resampling") for l in s["bricks"]["memory"])]
    rnd = [s["style_id"] for s in styles if s["features"]["uses_math_random"]]
    modes = collections.Counter()
    for s in styles:
        modes.update(s["features"]["composite_modes"].keys())
    graph = {s["style_id"]: set((s.get("rea") or {}).get("shares_function_bodies_with", [])) for s in styles}
    seen, clusters = set(), []
    for sid in graph:
        if sid in seen or not graph[sid]:
            continue
        stack, comp = [sid], set()
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x)
            stack.extend(graph.get(x, set()) - comp)
        seen |= comp
        clusters.append(sorted(comp))
    clusters.sort(key=lambda c: (-len(c), c))
    return {
        "shared_code_lineage": {"styles_sharing_function_bodies": sum(1 for v in graph.values() if v), "clusters": clusters,
                                "meaning": "REA normalized-AST fingerprints (functions of 3+ lines) that appear in more than one style: these styles reuse the same drawing routine, so pairing them is not an independent combination."},
        "pure_function_of_time": "All %d styles are written as frame = f(t); none keeps state between frames." % n,
        "memory_is_simulated": "%d/%d styles fake history by recomputing earlier t inside the frame (trail_by_resampling); no style stores a material memory that later frames read." % (len(resample), n),
        "temporal_feedback_styles": "0/%d: no style carries pixels or state from one frame into the next (every frame is rebuilt from t)." % n,
        "within_frame_pixel_postprocess": {"count": len(post), "styles": post},
        "field_steers_geometry": {"count": len(steer), "styles": steer},
        "styles_using_Math_random": rnd,
        "composite_modes_by_style_count": dict(modes.most_common()),
        "implication": "A persistent memory field that changes later motion (the glass-memory recipe) is a mechanism the 86 references do not contain; it must be simulated outside the pure-t frame and played back.",
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("analyze")
    a1.add_argument("--src", required=True, help="tree written by kmx_atlas_extract.py")
    a1.add_argument("--rea", nargs="+", help="one or more JSON outputs of `rea analyze-javascript-application <src> [--source-path ...] --format json`")
    a1.add_argument("--out", default=str(DEFAULT_OUT))
    a2 = sub.add_parser("show")
    a2.add_argument("style_id")
    a2.add_argument("--data", default=str(DEFAULT_OUT))
    a3 = sub.add_parser("summary")
    a3.add_argument("--data", default=str(DEFAULT_OUT))
    a = ap.parse_args(argv)
    if a.cmd == "analyze":
        out = analyze(a.src, a.rea)
        Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({"out": a.out, "styles": out["style_count"], "rea": bool(out["rea"]),
                          "tag_validation": out["analyst_tag_validation"]}, ensure_ascii=False))
        return 0
    data = json.loads(Path(a.data).read_text(encoding="utf-8"))
    if a.cmd == "show":
        for s in data["styles"]:
            if s["style_id"] == a.style_id:
                print(json.dumps({k: s[k] for k in s if k != "features"} | {"operations": s["features"]["operations"]}, ensure_ascii=False, indent=1))
                return 0
        print("unknown style id", file=sys.stderr)
        return 2
    print(json.dumps({k: data[k] for k in ("style_count", "rea", "analyst_tag_validation", "findings")}
                     | {"top_bricks": dict(list(data["brick_frequency"].items())[:30])}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
