#!/usr/bin/env python3
"""Split the user's ai-style-atlas-prompts-FULL archive into a local reference tree.

Reads the single .txt inside the zip (or the .txt itself) and writes, into an EMPTY output
folder that stays outside git:
    lib/harness.js            the shared H helper library (first copy; later copies are hashed)
    lib/sound.js              the shared SOUND kit
    styles/<style_id>.js      the reference style source of each of the 86 entries
    cards/<style_id>.json     the STYLE CARD fields (name, family, look, motion, how it explains)
    manifest.json             sha256 of every file + the archive hash

Nothing is executed. The third-party text stays local: never commit the output folder; commit
only derived measurements (see kmx_bricks.py). Stdlib only.
"""
import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ENTRY = re.compile(r"^#(\d\d) — (.+)$")
FENCE_TITLE = re.compile(r"^(H HELPER LIBRARY|SOUND KIT|REFERENCE STYLE SOURCE)\b.*?(?:\(([^)]*)\))?\s*$")


def read_text(path):
    p = Path(path)
    if p.suffix.lower() == ".zip":
        with zipfile.ZipFile(p) as z:
            names = [n for n in z.namelist() if n.lower().endswith(".txt")]
            if len(names) != 1:
                raise SystemExit("expected exactly one .txt in the archive, found %d" % len(names))
            return z.read(names[0]).decode("utf-8"), hashlib.sha256(p.read_bytes()).hexdigest()
    data = p.read_bytes()
    return data.decode("utf-8"), hashlib.sha256(data).hexdigest()


def parse(text):
    lines = text.splitlines()
    entries, cur = [], None
    i = 0
    while i < len(lines):
        line = lines[i]
        m = ENTRY.match(line)
        if m:
            cur = {"number": int(m.group(1)), "title": m.group(2).strip(), "card": {}, "blocks": {}}
            entries.append(cur)
            i += 1
            continue
        if cur is not None:
            if line.startswith("Style ID:"):
                cur["style_id"] = line.split(":", 1)[1].strip()
            elif line.startswith("Category:"):
                cur["family"] = line.split(":", 1)[1].strip()
            for key in ("Look", "Motion", "How it explains"):
                if line.startswith(key + ":"):
                    cur["card"][key.lower().replace(" ", "_")] = line.split(":", 1)[1].strip()
            t = FENCE_TITLE.match(line)
            if t and i + 1 < len(lines) and lines[i + 1].startswith("```"):
                j = i + 2
                while j < len(lines) and not lines[j].startswith("```"):
                    j += 1
                kind = {"H HELPER LIBRARY": "harness", "SOUND KIT": "sound", "REFERENCE STYLE SOURCE": "style"}[t.group(1)]
                cur["blocks"][kind] = "\n".join(lines[i + 2:j]) + "\n"
                i = j + 1
                continue
        i += 1
    return entries


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--archive", required=True, help="ai-style-atlas-prompts-FULL.zip or its .txt")
    ap.add_argument("--out", required=True, help="empty folder outside the repository")
    a = ap.parse_args(argv)
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit("refusing to write into a non-empty folder: %s" % out)
    text, archive_sha = read_text(a.archive)
    entries = parse(text)
    ids = [e.get("style_id") for e in entries]
    if len(entries) != 86 or len(set(ids)) != 86 or None in ids:
        raise SystemExit("expected 86 distinct entries, parsed %d (%d ids)" % (len(entries), len(set(ids))))
    (out / "lib").mkdir(parents=True)
    (out / "styles").mkdir()
    (out / "cards").mkdir()
    files = {}
    shared = {"harness": set(), "sound": set()}

    def write(rel, body):
        p = out / rel
        p.write_text(body, encoding="utf-8")
        files[rel] = hashlib.sha256(body.encode("utf-8")).hexdigest()

    missing = []
    for e in entries:
        for kind in ("harness", "sound"):
            body = e["blocks"].get(kind)
            if body:
                h = hashlib.sha256(body.encode()).hexdigest()
                if not shared[kind]:
                    write("lib/%s.js" % kind, body)
                shared[kind].add(h)
        style = e["blocks"].get("style")
        if not style:
            missing.append(e["style_id"])
            continue
        write("styles/%s.js" % e["style_id"], style)
        write("cards/%s.json" % e["style_id"], json.dumps(
            {"number": e["number"], "style_id": e["style_id"], "title": e["title"], "family": e.get("family"), **e["card"]},
            ensure_ascii=False, indent=1) + "\n")
    manifest = {"schema": "kosif.matrices.atlas-extract.v1", "archive_sha256": archive_sha, "entries": len(entries),
                "styles_with_source": 86 - len(missing), "missing_source": missing,
                "shared_variants": {k: len(v) for k, v in shared.items()}, "files": files,
                "rights": "Third-party text (Futurepedia AI Style Atlas). Local analysis only; do not commit or redistribute."}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in manifest.items() if k != "files"}, ensure_ascii=False))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
