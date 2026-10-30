#!/usr/bin/env python3
"""Join upload-page parts back into the original files.

  python3 -I join_parts.py --rows <dir of row .json files> --parts <dir of <id>.mp4 parts> --out <dest dir>

Each row is one uploaded file: name, size, parts, status, chunks=[{index, id, size}].
Only complete rows are joined; duplicates (same name and size) are joined once.
Exit code 1 if any file is missing a part or has the wrong size.
"""
import argparse, json, os, sys
from pathlib import Path

HIDDEN = dict.fromkeys(map(ord, "‎‏⁦⁧⁨⁩‪‫‬"))


def rows(path: Path):
    for f in sorted(path.glob("*.json")):
        r = json.loads(f.read_text(encoding="utf-8"))
        yield r.get("data", r)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True, type=Path)
    ap.add_argument("--parts", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    seen, bad, done = set(), 0, 0
    for r in rows(a.rows):
        name = os.path.basename(str(r.get("name", ""))).translate(HIDDEN).strip() or "file"
        chunks = sorted(r.get("chunks") or [], key=lambda c: c["index"])
        if r.get("status") != "done" or len(chunks) != r.get("parts"):
            print(f"skip   {name}: status={r.get('status')} {len(chunks)}/{r.get('parts')} {r.get('error') or ''}".rstrip())
            continue
        key = (name, r.get("size"))
        if key in seen:
            continue
        seen.add(key)
        missing = [c["id"] for c in chunks if not (a.parts / f"{c['id']}.mp4").exists()]
        if missing:
            print(f"MISSING {name}: download parts {' '.join(missing)}"); bad += 1; continue
        dest = a.out / name
        with open(dest, "wb") as w:
            for c in chunks:
                w.write((a.parts / f"{c['id']}.mp4").read_bytes())
        size = dest.stat().st_size
        if size != r.get("size"):
            print(f"BAD    {name}: {size} != {r.get('size')}"); bad += 1; continue
        done += 1
        print(f"ok     {name} ({size / 1048576:.1f} MB)")
    print(f"{done} joined, {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
