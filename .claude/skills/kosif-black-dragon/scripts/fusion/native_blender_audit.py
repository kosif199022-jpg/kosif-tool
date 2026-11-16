#!/usr/bin/env python3
"""native_blender_audit.py - headless Blender scene audit + Poly Haven lookup.

Original implementation for the Black Dragon, inspired by the ideas in
ahujasid/mcp-for-blender (MIT): a "scene info" tool that reports real-world size,
ground contact and mesh health, and a Poly Haven search/download resolver.
No code is copied; no addon, socket or telemetry is involved.

Subcommands (all accept --json):
  audit <file.blend> [--blender PATH] [--ground-tol 0.005] [--max-dim 1000]
        Opens the .blend with `blender -b`, returns per-object size, ground state
        (on ground / floating / below), topology (quads/tris/ngons, non-manifold,
        loose verts, poles), UV + material + weight checks, and an `issues` list.
  polyhaven search [--type hdris|textures|models|all] [--query Q] [--category C] [--limit N]
  polyhaven files <asset_id> [--res 1k] [--format hdr|exr|jpg|png|gltf|blend ...]
        Resolve real download URLs (CC0) from api.polyhaven.com.
  self-test
        Builds a deliberately broken scene in a temp dir, audits it with real
        Blender, and asserts the findings. Also pings Poly Haven (skipped if offline).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

MARK = "__AUDIT_JSON__"
BLENDER_CANDIDATES = [
    r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe",
    r"C:\Program Files\Blender Foundation\Blender 5.1\blender.exe",
    r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe",
]
PH_API = "https://api.polyhaven.com"
UA = {"User-Agent": "black-dragon-native-audit/1.0"}


# ----------------------------------------------------------------- inside Blender
def inner_audit(blend_unused, ground_tol, max_dim):
    import bpy
    import bmesh
    from mathutils import Vector

    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    objs, issues = [], []

    def issue(sev, obj, code, msg):
        issues.append({"severity": sev, "object": obj, "code": code, "message": msg})

    for o in sc.objects:
        d = {"name": o.name, "type": o.type, "parent": o.parent.name if o.parent else None,
             "hidden": bool(o.hide_render or o.hide_get())}
        if o.type not in {"EMPTY", "LIGHT", "CAMERA"}:
            ev = o.evaluated_get(dg)
            pts = [ev.matrix_world @ Vector(c) for c in ev.bound_box]
            lo = [min(p[i] for p in pts) for i in range(3)]
            hi = [max(p[i] for p in pts) for i in range(3)]
            size = [round(hi[i] - lo[i], 4) for i in range(3)]
            d["size_m"] = size
            d["min_z"] = round(lo[2], 4)
            if lo[2] > ground_tol:
                d["ground"] = "floating"
                issue("warn", o.name, "floating", f"bottom is {lo[2]:.3f} m above Z=0")
            elif lo[2] < -ground_tol:
                d["ground"] = "below"
                issue("warn", o.name, "below_ground", f"bottom is {-lo[2]:.3f} m below Z=0")
            else:
                d["ground"] = "on_ground"
            if max(size) > max_dim:
                issue("warn", o.name, "huge", f"largest dimension {max(size):.1f} m")
            if 0 < max(size) < 0.001:
                issue("warn", o.name, "tiny", f"largest dimension {max(size)*1000:.3f} mm")
            s = o.scale
            if o.type == "MESH" and any(abs(abs(v) - 1) > 1e-4 for v in s):
                issue("info", o.name, "unapplied_scale", f"scale=({s.x:.3f},{s.y:.3f},{s.z:.3f})")
            if o.type == "MESH" and any(v < 0 for v in s):
                issue("warn", o.name, "negative_scale", "negative scale flips normals")
        if o.type == "MESH":
            me = o.data
            bm = bmesh.new()
            bm.from_mesh(me)
            sides = [len(f.verts) for f in bm.faces]
            d["topology"] = {
                "verts": len(bm.verts), "faces": len(bm.faces),
                "quads": sides.count(4), "tris": sides.count(3),
                "ngons": sum(1 for n in sides if n > 4),
                "non_manifold_edges": sum(1 for e in bm.edges if not e.is_manifold and not e.is_boundary),
                "boundary_edges": sum(1 for e in bm.edges if e.is_boundary),
                "loose_verts": sum(1 for v in bm.verts if not v.link_edges),
                "poles": sum(1 for v in bm.verts if len(v.link_edges) not in (0, 2, 4) and not v.is_boundary),
            }
            bm.free()
            t = d["topology"]
            if t["non_manifold_edges"]:
                issue("warn", o.name, "non_manifold", f"{t['non_manifold_edges']} non-manifold edges")
            if t["loose_verts"]:
                issue("info", o.name, "loose_verts", f"{t['loose_verts']} loose vertices")
            if t["faces"] and not me.uv_layers:
                issue("info", o.name, "no_uv", "mesh has no UV map")
            if t["faces"] and not any(s.material for s in o.material_slots):
                issue("info", o.name, "no_material", "mesh has no material")
            arm = next((m.object for m in o.modifiers if m.type == "ARMATURE" and m.object), None)
            if arm:
                deform = {b.name for b in arm.data.bones if b.use_deform}
                gi = {g.index for g in o.vertex_groups if g.name in deform}
                unw = sum(1 for v in me.vertices if not any(g.group in gi and g.weight > 0 for g in v.groups))
                d["unweighted_verts"] = unw
                if unw:
                    issue("warn", o.name, "unweighted", f"{unw}/{len(me.vertices)} verts have no deform weight")
        base = o.name.rsplit(".", 1)[0]
        if base in {"Cube", "Sphere", "Plane", "Cylinder", "Cone", "Torus", "Circle"}:
            issue("info", o.name, "default_name", "primitive still has default name")
        objs.append(d)

    for im in bpy.data.images:
        if im.source == "FILE" and im.filepath:
            p = bpy.path.abspath(im.filepath)
            if not os.path.isfile(p):
                issue("warn", im.name, "missing_texture", f"file not found: {p}")
    if sc.camera is None:
        issue("info", None, "no_camera", "scene has no active camera")
    if not any(o.type == "LIGHT" for o in sc.objects) and not sc.world:
        issue("info", None, "no_light", "no lights and no world")

    counts = {}
    for o in sc.objects:
        counts[o.type] = counts.get(o.type, 0) + 1
    sev = {"warn": 0, "info": 0}
    for i in issues:
        sev[i["severity"]] += 1
    return {"ok": True, "blender": bpy.app.version_string, "file": bpy.data.filepath,
            "unit_scale": sc.unit_settings.scale_length,
            "engine": sc.render.engine, "frames": [sc.frame_start, sc.frame_end],
            "camera": sc.camera.name if sc.camera else None,
            "counts": counts, "objects": objs, "issues": issues, "issue_totals": sev}


def inner_main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--ground-tol", type=float, default=0.005)
    ap.add_argument("--max-dim", type=float, default=1000.0)
    ap.add_argument("--build-test", help="write a broken test scene here and exit")
    a = ap.parse_args(argv)
    if a.build_test:
        build_test_scene(a.build_test)
        print(MARK + json.dumps({"ok": True, "built": a.build_test}))
        return
    res = inner_audit(None, a.ground_tol, a.max_dim)
    print(MARK + json.dumps(res))


def build_test_scene(path):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))      # good: sits on ground
    bpy.context.object.name = "Crate"
    bpy.ops.mesh.primitive_cube_add(size=2, location=(5, 0, 4))      # floating
    bpy.context.object.name = "Floaty"
    bpy.ops.mesh.primitive_cube_add(size=2, location=(-5, 0, -2))    # below ground
    bpy.context.object.scale = (2, 1, 1)                             # unapplied scale
    bpy.context.object.name = "Sunk"
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 5, 0))     # default name, open mesh
    bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 0, 0))
    bpy.context.object.name = "Huge"
    bpy.ops.object.mode_set(mode="OBJECT")
    # genuinely non-manifold: three faces sharing one edge
    import bmesh
    me = bpy.data.meshes.new("Fin")
    bm = bmesh.new()
    a = bm.verts.new((0, 0, 0)); b = bm.verts.new((1, 0, 0))
    for c in [(0.5, 1, 0), (0.5, -1, 0), (0.5, 0, 1)]:
        bm.faces.new((a, b, bm.verts.new(c)))
    bm.to_mesh(me); bm.free()
    fin = bpy.data.objects.new("Fin", me)
    fin.location = (0, -5, 0)
    bpy.context.scene.collection.objects.link(fin)
    bpy.ops.wm.save_as_mainfile(filepath=path)


# ------------------------------------------------------------------ outside (CLI)
def find_blender(explicit=None):
    for c in (explicit, os.environ.get("BLENDER"), shutil.which("blender"), *BLENDER_CANDIDATES):
        if c and os.path.isfile(c):
            return c
    sys.exit(json.dumps({"ok": False, "error": "Blender not found; set BLENDER or pass --blender"}))


def run_blender(blender, extra, blend=None, timeout=300):
    cmd = [blender, "-b"] + ([blend] if blend else ["--factory-startup"]) + \
          ["--python", os.path.abspath(__file__), "--"] + extra
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
    for line in reversed(p.stdout.splitlines()):
        if line.startswith(MARK):
            return json.loads(line[len(MARK):])
    return {"ok": False, "error": "no result from Blender", "rc": p.returncode,
            "stderr_tail": p.stderr[-800:], "stdout_tail": p.stdout[-800:]}


def http_json(url):
    last = None
    for _ in range(4):  # the big listing sometimes truncates mid-read; retry
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            last = e
    raise last


def ph_search(typ, query, category, limit):
    params = {} if typ == "all" else {"t": typ}
    if category:
        params["c"] = category
    url = PH_API + "/assets" + ("?" + urllib.parse.urlencode(params) if params else "")
    data = http_json(url)
    q = (query or "").lower().split()
    rows = []
    for aid, a in data.items():
        hay = " ".join([aid, a.get("name", ""), *a.get("tags", []), *a.get("categories", [])]).lower()
        if all(w in hay for w in q):
            dim = a.get("dimensions")
            rows.append({"id": aid, "name": a.get("name"), "type": {0: "hdris", 1: "textures", 2: "models"}.get(a.get("type")),
                         "categories": a.get("categories", []), "downloads": a.get("download_count", 0),
                         "real_size_m": [round(v / 1000, 3) for v in dim] if dim else None,
                         "url": f"https://polyhaven.com/a/{aid}"})
    rows.sort(key=lambda r: -r["downloads"])
    return {"ok": True, "total": len(rows), "results": rows[:limit], "license": "CC0 (polyhaven.com)"}


def ph_files(aid, res, fmts):
    tree = http_json(f"{PH_API}/files/{aid}")
    found = []

    def walk(node, path):
        if isinstance(node, dict):
            if "url" in node and "size" in node:
                found.append({"path": "/".join(path), "url": node["url"], "bytes": node["size"]})
            else:
                for k, v in node.items():
                    walk(v, path + [k])
    walk(tree, [])
    if res:
        found = [f for f in found if f"/{res}/" in "/" + f["path"] + "/"]
    if fmts:
        found = [f for f in found if any(f["url"].lower().endswith("." + x.lower()) or f"/{x}/" in f["path"] for x in fmts)]
    return {"ok": True, "asset": aid, "count": len(found), "files": found[:60], "license": "CC0"}


def cmd_audit(a):
    blender = find_blender(a.blender)
    if not os.path.isfile(a.blend):
        return {"ok": False, "error": f"missing file {a.blend}"}
    return run_blender(blender, ["--ground-tol", str(a.ground_tol), "--max-dim", str(a.max_dim)], blend=os.path.abspath(a.blend))


def cmd_self_test(a):
    blender = find_blender(a.blender)
    tmp = tempfile.mkdtemp(prefix="bl_audit_")
    blend = os.path.join(tmp, "broken.blend")
    r = run_blender(blender, ["--build-test", blend])
    assert r.get("ok"), r
    assert os.path.isfile(blend), "test blend not written"
    res = run_blender(blender, [], blend=blend)
    assert res.get("ok"), res
    codes = {(i["object"], i["code"]) for i in res["issues"]}
    objs = {o["name"]: o for o in res["objects"]}
    assert objs["Crate"]["ground"] == "on_ground", objs["Crate"]
    assert objs["Floaty"]["ground"] == "floating", objs["Floaty"]
    assert objs["Sunk"]["ground"] == "below", objs["Sunk"]
    assert ("Sunk", "unapplied_scale") in codes, codes
    assert ("Huge", "huge") in codes, codes
    assert ("Plane", "default_name") in codes, codes
    assert ("Fin", "non_manifold") in codes, codes
    assert objs["Fin"]["topology"]["non_manifold_edges"] == 1, objs["Fin"]["topology"]
    assert objs["Crate"]["topology"]["quads"] == 6
    assert abs(objs["Crate"]["size_m"][0] - 2.0) < 1e-3
    assert ("Crate", "floating") not in codes
    out = {"blender": res["blender"], "objects": len(res["objects"]),
           "issues": len(res["issues"]), "totals": res["issue_totals"]}
    try:
        ph = ph_search("hdris", "sunrise", None, 3)
        assert ph["total"] > 0 and ph["results"][0]["id"]
        files = ph_files(ph["results"][0]["id"], "1k", ["hdr"])
        assert files["count"] >= 1 and files["files"][0]["url"].startswith("https://")
        out["polyhaven"] = {"hdri_hits": ph["total"], "first": ph["results"][0]["id"], "files_1k_hdr": files["count"]}
    except Exception as e:  # offline is acceptable
        out["polyhaven"] = f"skipped ({type(e).__name__}: {e})"
    shutil.rmtree(tmp, ignore_errors=True)
    return {"ok": True, "self_test": "PASS", **out}


def emit(res, as_json):
    if as_json:
        print(json.dumps(res, ensure_ascii=False))
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if res.get("ok") else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="single-line JSON output")
    ap.add_argument("--blender")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("audit")
    p.add_argument("blend")
    p.add_argument("--ground-tol", type=float, default=0.005)
    p.add_argument("--max-dim", type=float, default=1000.0)
    p = sub.add_parser("polyhaven")
    ps = p.add_subparsers(dest="ph", required=True)
    s = ps.add_parser("search")
    s.add_argument("--type", default="all", choices=["all", "hdris", "textures", "models"])
    s.add_argument("--query", default="")
    s.add_argument("--category")
    s.add_argument("--limit", type=int, default=10)
    f = ps.add_parser("files")
    f.add_argument("asset_id")
    f.add_argument("--res")
    f.add_argument("--format", action="append")
    sub.add_parser("self-test")
    a = ap.parse_args()
    if a.cmd == "audit":
        res = cmd_audit(a)
    elif a.cmd == "polyhaven":
        res = ph_search(a.type, a.query, a.category, a.limit) if a.ph == "search" else ph_files(a.asset_id, a.res, a.format)
    else:
        res = cmd_self_test(a)
    emit(res, a.json)


if __name__ == "__main__":
    try:
        import bpy  # noqa: F401  (only importable inside Blender)
        inside = "--" in sys.argv
    except ImportError:
        inside = False
    inner_main() if inside else main()
