#!/usr/bin/env python3
"""KOSIF Native 3D: original Blender-free, stdlib-only animated GLB exporter.

Narrow first step toward a native 3D engine. Does NOT reproduce Blender.
Supported shapes: cube, sphere; properties: color, translation, scale;
animation: position keyframes. No external executable or arbitrary code runs.

kosif.blender.v1 scenes are Blender-style Z-up; glTF is Y-up (right-handed).
Like Blender's own glTF exporter, every position (mesh vertices, node
translation, keyframes) is written as (x, y, z) -> (x, z, -y) and scale as
(sx, sy, sz) -> (sx, sz, sy), so the scene schema itself is unchanged.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import sys


def _vec(v, n, low=-100, high=100):
    if (not isinstance(v, (tuple, list)) or len(v) != n or
            any(type(x) not in (int, float) or not math.isfinite(x)
                or not low <= x <= high for x in v)):
        raise ValueError(f"expected {n} finite numbers")
    return [float(x) for x in v]


def _y_up(v):
    """Blender Z-up (x, y, z) -> glTF Y-up (x, z, -y); `+ 0.0` avoids writing -0.0."""
    x, y, z = v
    return [float(x), float(z), -float(y) + 0.0]


def _cube():
    points = [(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1),
              (-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)]
    faces = [(0,1,2,3), (4,7,6,5), (0,4,5,1),
             (1,5,6,2), (2,6,7,3), (3,7,4,0)]
    return points, [i for a,b,c,d in faces for i in (a,b,c,a,c,d)]


def _sphere():
    points = [(0,0,1)]
    steps, rings = 12, 7
    for j in range(1, rings+1):
        polar = math.pi*j/(rings+1)
        for k in range(steps):
            theta = 2*math.pi*k/steps
            points.append((math.sin(polar)*math.cos(theta),
                           math.sin(polar)*math.sin(theta), math.cos(polar)))
    points.append((0,0,-1))
    faces = []
    for k in range(steps):
        faces.extend((0, 1+(k+1)%steps, 1+k))
    for j in range(rings-1):
        for k in range(steps):
            a = 1+j*steps+k
            b = 1+j*steps+(k+1)%steps
            c, d = a+steps, b+steps
            faces.extend((a,b,d,a,d,c))
    pole = len(points)-1
    for k in range(steps):
        faces.extend((pole, 1+(rings-1)*steps+k,
                      1+(rings-1)*steps+(k+1)%steps))
    return points, faces


def glb(scene):
    if not isinstance(scene, dict) or scene.get("schema") != "kosif.blender.v1":
        raise ValueError("expected KOSIF scene schema")
    objects = scene.get("objects")
    if not isinstance(objects, list) or not 1 <= len(objects) <= 12:
        raise ValueError("1-12 objects required")
    frames, fps = scene.get("frames", 1), scene.get("fps", 24)
    if (type(frames) is not int or not 1 <= frames <= 240 or
            type(fps) is not int or not 1 <= fps <= 60):
        raise ValueError("invalid timing")
    size = scene.get("size", [512, 512])
    if (not isinstance(size, list) or len(size) != 2 or
            any(type(x) is not int or not 128 <= x <= 1920 for x in size)):
        raise ValueError("invalid render-size metadata")

    document = {
        "asset": {"version": "2.0", "generator": "KOSIF native GLB 0.1"},
        "scene": 0, "scenes": [{"nodes": list(range(len(objects)))}],
        "nodes": [], "meshes": [], "materials": [], "bufferViews": [],
        "accessors": [], "buffers": [{"byteLength": 0}],
    }
    data = bytearray()
    animations = []

    def buffer(payload, target=None):
        offset = len(data)
        data.extend(payload)
        data.extend(b"\0" * ((-len(data)) % 4))
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(payload)}
        if target is not None:
            view["target"] = target
        document["bufferViews"].append(view)
        return len(document["bufferViews"])-1

    def accessor(values, kind, component, target=None):
        fmt = {"float": "f", "ushort": "H"}[component]
        payload = b"".join(
            struct.pack("<" + fmt*(1 if isinstance(v, (int,float)) else len(v)),
                        *([v] if isinstance(v,(int,float)) else v))
            for v in values
        )
        view = buffer(payload, target)
        item = {
            "bufferView": view,
            "componentType": {"float": 5126, "ushort": 5123}[component],
            "count": len(values), "type": kind,
        }
        if kind == "VEC3" and values and component == "float":
            item["min"] = [min(v[i] for v in values) for i in range(3)]
            item["max"] = [max(v[i] for v in values) for i in range(3)]
        document["accessors"].append(item)
        return len(document["accessors"])-1

    for i, obj in enumerate(objects):
        if not isinstance(obj, dict) or obj.get("shape") not in ("cube", "sphere"):
            raise ValueError("native exporter supports cube and sphere only")
        points, indices = _cube() if obj["shape"] == "cube" else _sphere()
        positions = accessor([_y_up(v) for v in points], "VEC3", "float", 34962)
        triangle_indices = accessor(indices, "SCALAR", "ushort", 34963)
        rgba = _vec(obj.get("color", [0.25, 0.6, 0.4, 1]), 4, 0, 1)
        material_id = len(document["materials"])
        document["materials"].append({
            "pbrMetallicRoughness": {
                "baseColorFactor": rgba, "metallicFactor": 0,
                "roughnessFactor": 0.78,
            },
            "doubleSided": True,
        })
        mesh_id = len(document["meshes"])
        document["meshes"].append({"primitives": [{
            "attributes": {"POSITION": positions},
            "indices": triangle_indices, "material": material_id,
        }]})
        location = _y_up(_vec(obj.get("location", [0, 0, 0]), 3))
        sx, sy, sz = _vec(obj.get("scale", [1, 1, 1]), 3, -20, 20)
        scale = [sx, sz, sy]
        document["nodes"].append({
            "name": f"KOSIF_{i}_{obj['shape']}",
            "mesh": mesh_id, "translation": location, "scale": scale,
        })
        keys = obj.get("keyframes", [])
        if not isinstance(keys, list) or len(keys) > 24:
            raise ValueError("invalid keyframes")
        if keys:
            previous, times, positions = 0, [], []
            for key in keys:
                if (not isinstance(key, dict) or type(key.get("frame")) is not int
                        or not previous < key["frame"] <= frames):
                    raise ValueError("keyframes must be ordered and in bounds")
                previous = key["frame"]
                times.append((previous-1)/fps)
                positions.append(_y_up(_vec(key.get("location"), 3)))
            times_accessor = accessor(times, "SCALAR", "float")
            translations_accessor = accessor(positions, "VEC3", "float")
            animations.append({
                "samplers": [{
                    "input": times_accessor, "output": translations_accessor,
                    "interpolation": "LINEAR",
                }],
                "channels": [{
                    "sampler": 0,
                    "target": {"node": i, "path": "translation"},
                }],
            })

    if animations:
        document["animations"] = animations
    document["buffers"][0]["byteLength"] = len(data)
    content = json.dumps(document, separators=(",", ":"), ensure_ascii=False).encode()
    content += b" " * ((-len(content)) % 4)
    total = 12 + 8 + len(content) + 8 + len(data)
    return (
        struct.pack("<4sII", b"glTF", 2, total)
        + struct.pack("<I4s", len(content), b"JSON") + content
        + struct.pack("<I4s", len(data), b"BIN\0") + data
    )


def main():
    parser = argparse.ArgumentParser(
        description="Export a bounded animated GLB scene without Blender"
    )
    parser.add_argument("--scene", required=True)
    parser.add_argument("--output", required=True)
    options = parser.parse_args()
    target = Path(options.output)
    if target.suffix.lower() != ".glb" or target.exists():
        parser.error("output must be a new .glb file")
    if not target.parent.is_dir():
        parser.error(f"output folder does not exist: {target.parent}")
    try:
        result = glb(json.loads(Path(options.scene).read_text(encoding="utf-8-sig")))
        with target.open("xb") as handle:
            handle.write(result)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps({
        "engine": "KOSIF native (no Blender required)",
        "path": str(target), "bytes": len(result),
        "sha256": hashlib.sha256(result).hexdigest(),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
