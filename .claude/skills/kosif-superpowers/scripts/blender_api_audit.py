#!/usr/bin/env python3
"""Blender source-tree AST catalog. Never imports or executes inspected files."""
import argparse
import ast
from collections import Counter
import json
import os
from pathlib import Path

MAX_FILE = 2_000_000
MAX_FILES = 3000
GROUPS = {
    "animation_rig": ("anim", "rig", "keyfram", "bone", "pose", "ik", "motion"),
    "drawing_strokes": ("grease", "pencil", "draw", "stroke", "brush", "paint"),
    "3d_geometry": ("mesh", "modifier", "curve", "geometry", "sculpt"),
    "video_composite": ("video", "sequenc", "composit", "render", "camera", "track"),
    "materials": ("material", "shader", "texture", "color", "light"),
}
def dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return dotted(node.value) + "." + node.attr
    return ""

def audit(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("source root must be a directory")
    files, parsable, skipped = 0, 0, []
    classes, operators, groups = Counter(), Counter(), Counter()
    sample = []
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not (Path(base)/d).is_symlink() and d != "__pycache__")
        for name in sorted(names):
            file = Path(base) / name
            if file.suffix.lower() != ".py" or file.is_symlink():
                continue
            files += 1
            if files > MAX_FILES:
                raise ValueError("file count exceeds limit")
            rel = file.relative_to(root).as_posix()
            try:
                if file.stat().st_size > MAX_FILE:
                    skipped.append({"file": rel, "why": "too_large"})
                    continue
                tree = ast.parse(file.read_text(encoding="utf-8-sig"), filename=rel)
            except (SyntaxError, UnicodeError, OSError) as err:
                skipped.append({"file": rel, "why": type(err).__name__})
                continue
            parsable += 1
            lower = rel.lower()
            tags = [g for g, keys in GROUPS.items() if any(k in lower for k in keys)]
            for tag in tags:
                groups[tag] += 1
            ops = set()
            class_names = []
            for item in ast.walk(tree):
                if isinstance(item, ast.ClassDef):
                    bases = [dotted(b) for b in item.bases]
                    typ = next((b for b in bases if b in {
                        "bpy.types.Operator", "bpy.types.Panel", "bpy.types.Menu",
                        "bpy.types.PropertyGroup", "bpy.types.GizmoGroup"}), None)
                    if typ:
                        classes[typ] += 1
                        class_names.append(item.name)
                elif isinstance(item, ast.Call):
                    api = dotted(item.func)
                    if api.startswith("bpy.ops.") and len(api) < 180:
                        operators[api] += 1
                        ops.add(api)
            if (tags or class_names or ops) and len(sample) < 45:
                sample.append({"path": rel, "groups": tags[:4],
                               "operator_classes": class_names[:7], "bpy_ops": sorted(ops)[:8]})
    return {"schema": "kosif.blender-api-audit.v1", "files_found": files,
            "parsed_files": parsable, "skipped": skipped[:35],
            "operator_class_types": dict(classes.most_common()),
            "bpy_ops_calls": dict(operators.most_common(120)),
            "topic_file_counts": dict(groups.most_common()), "samples": sample,
            "source_not_executed": True,
            "caveat": "Only bundled Python AST; no C/C++ behavior inferred."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("--output")
    a = p.parse_args()
    result = audit(a.source)
    if a.output:
        path = Path(a.output).resolve()
        if path.exists() or Path(a.source).resolve() in path.parents:
            p.error("output exists or is inside inspected tree")
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in {"samples", "bpy_ops_calls"}},
                     ensure_ascii=False))
if __name__ == "__main__":
    main()
