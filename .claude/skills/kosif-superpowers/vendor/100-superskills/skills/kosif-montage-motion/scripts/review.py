"""Review layer: any KOSIF film becomes a reel.json that the review page (scripts/web/static/review, the Motion OS
player by Jason Lee, MIT) opens scene by scene. The user edits copy, colours, timing and boxes, pins notes on the
frame, marks scenes approved and sends one prompt back. This script turns that feedback into changes.

    python scripts/kmotion.py review init  PROJECT_OR_SPEC [--video film.mp4] [--title T] [--name N]
    python scripts/kmotion.py review apply NAME [--feedback feedback.json]      edits with a binding → the source
    python scripts/kmotion.py review export NAME [--props props.json]           apply, re-render, bump the version
    python scripts/kmotion.py review feedback NAME                              the last prompt the user sent
    python scripts/kmotion.py review bump NAME [--video new.mp4]                version + 1 (the open page reloads)
    python scripts/kmotion.py review list

Where the scenes and elements come from:
  * HTML composition: a <script type="application/json" id="kosif-reel"> block ({"scenes":[{"id","name","t","els":[…]}]})
    whose element props bind to keys of <script type="application/json" id="kosif-props"> (the page reads its copy from
    there), plus every `--name: #hex` colour in :root as an editable brand colour. With no block, scenes come from
    cut detection on the rendered film.
  * Timeline spec (kmotion timeline): one scene per clip; every text / lower-third overlay is an element whose text,
    colour, timing and position are bound to the spec, so those edits apply exactly with no rewrite by hand.
  * Any video: scenes from cut detection; notes only.
Edits with a binding are applied by `review apply`; notes, motion requests and unbound edits are listed for Claude.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import motion  # noqa: E402  (PROJECTS and HOME follow KOSIF_MOTION_HOME)

REVIEWS = Path(os.environ.get("KOSIF_MOTION_HOME") or HERE.parent) / "reviews"
FF = shutil.which("ffmpeg") or "ffmpeg"
BLOCK = r'(<script[^>]*type="application/json"[^>]*id="{id}"[^>]*>)(.*?)(</script>)'


def _r(x: float, n: int = 3) -> float:
    return round(float(x), n)


def _probe(video: Path) -> dict:
    import qa
    try:
        return qa._probe(video)
    except Exception:  # noqa: BLE001
        return {}


def _cuts(video: Path, duration: float) -> list[list[float]]:
    try:
        import scenes as sc
        cuts = [c["t"] if isinstance(c, dict) else float(c) for c in (sc.detect(video).get("cuts") or [])]
    except Exception:  # noqa: BLE001
        cuts = []
    edges = [0.0] + [c for c in cuts if 0.4 < c < duration - 0.4] + [duration]
    return [[_r(a), _r(b)] for a, b in zip(edges, edges[1:]) if b - a > 0.05]


def _block(html: str, bid: str):
    m = re.search(BLOCK.format(id=bid), html, re.S)
    return (json.loads(m.group(2)), m) if m else (None, None)


def _set_block(html: str, bid: str, data: dict) -> str:
    _, m = _block(html, bid)
    body = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return html[:m.start(2)] + body + html[m.end(2):]


def _root_colors(html: str) -> list[dict]:
    m = re.search(r":root\s*\{([^}]*)\}", html)
    if not m:
        return []
    return [{"id": k, "name": k.replace("-", " ").strip().title(), "v": v}
            for k, v in re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\b", m.group(1))]


def _newest_video(folder: Path, stem: str, own: bool = False) -> Path | None:
    """The latest render of this film: any mp4 in a project's own out/renders (own=True), else only files named after it."""
    home_out = Path(os.environ.get("KOSIF_MOTION_HOME") or HERE.parent) / "out"
    cands = [p for d in (folder, folder / "out", folder / "renders", home_out) if d.exists() for p in d.glob("*.mp4")
             if stem.lower() in p.stem.lower() or (own and d in (folder / "out", folder / "renders"))]
    return max(cands, key=lambda p: p.stat().st_mtime) if cands else None


def _place_video(folder: Path, video: Path, rid: str, ver: int) -> str:
    """The film next to reel.json (the page serves its own folder); renders already inside are used as they are."""
    video = video.resolve()
    if folder.resolve() in video.parents:
        return video.relative_to(folder.resolve()).as_posix()
    (folder / "review").mkdir(parents=True, exist_ok=True)
    dst = folder / "review" / f"{rid}-v{ver}.mp4"
    if dst.exists():
        dst.unlink()
    try:
        os.link(video, dst)
    except OSError:
        shutil.copy2(video, dst)
    return dst.relative_to(folder).as_posix()


# ---------------------------------------------------------------------------------------------------- builders
def from_html(project: Path, video: Path | None) -> dict:
    html = (project / "index.html").read_text(encoding="utf-8")
    attr = lambda k, d: (re.search(rf'data-{k}="([^"]+)"', html) or [None, d])[1]  # noqa: E731
    W, H, fps, dur = int(attr("width", 1920)), int(attr("height", 1080)), int(float(attr("fps", 30))), float(attr("duration", 5))
    title = (re.search(r"<title>(.*?)</title>", html, re.S) or [None, project.name])[1].strip()
    spec, _ = _block(html, "kosif-reel")
    props, _ = _block(html, "kosif-props")
    props = props or {}
    scenes = []
    if spec and spec.get("scenes"):
        for s in spec["scenes"]:
            els = []
            for e in s.get("els", []):
                e = dict(e); pr = {}
                for k, p in (e.get("props") or {}).items():
                    p = dict(p)
                    if p.get("bind") in props:
                        p["v"] = props[p["bind"]]
                    p.setdefault("v", "")
                    pr[k] = p
                e["props"] = pr
                e.setdefault("box", [10, 10, 80, 20]); e.setdefault("t", s["t"]); e.setdefault("label", e["id"])
                e.setdefault("src", "index.html")
                els.append(e)
            scenes.append({"id": s["id"], "name": s.get("name", s["id"]), "t": s["t"], "els": els})
    elif video:
        scenes = [{"id": f"S{i + 1}", "name": f"Shot {i + 1}", "t": t, "els": []} for i, t in enumerate(_cuts(video, dur))]
    if not scenes:
        scenes = [{"id": "S1", "name": "Film", "t": [0, dur], "els": []}]
    return {"title": title, "w": W, "h": H, "fps": fps, "duration": dur, "scenes": scenes,
            "brand": {"colors": _root_colors(html), "fonts": [], "logo": None},
            "kosif": {"kind": "html", "project": str(project.resolve())}}


def _overlay_box(o: dict, W: int, H: int, captions: bool) -> list[float]:
    import timeline as tl
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "o.png"
        if o["type"] == "lower-third":
            info = tl.lower_third_png(o, W, H, png)
            o = {**o, "pos": o.get("pos") or ("lower-right" if info["rtl"] else "lower-left")}
        elif o["type"] == "text":
            info = tl.text_png(o, W, H, png)
        else:
            from PIL import Image
            im = Image.open(o["src"]); sc = float(o.get("scale", 1.0))
            tw = int(o.get("width") or round(im.width * sc * (W / 1080 if W <= H else H / 1080)))
            info = {"w": tw, "h": round(im.height * tw / im.width)}
        x, y = tl._place(o, W, H, info["w"], info["h"], captions)
    try:
        x, y = float(x), float(y)
    except ValueError:
        x, y = (W - info["w"]) / 2, (H - info["h"]) / 2
    return [_r(100 * x / W, 2), _r(100 * y / H, 2), _r(100 * info["w"] / W, 2), _r(100 * info["h"] / H, 2)]


def from_timeline(spec_path: Path, video: Path | None) -> dict:
    import timeline as tl
    raw = json.loads(spec_path.read_text(encoding="utf-8"))
    sp, sm = tl.load(raw, spec_path.parent), tl.summary(tl.load(raw, spec_path.parent))
    W, H = sp["W"], sp["H"]
    caps = any(o["type"] == "captions" for o in sp["overlays"])
    scenes = [{"id": f"S{c['i'] + 1}", "name": Path(str(c["src"])).name if c["kind"] != "color" else f"colour {c['src']}",
               "t": [_r(c["start"]), _r(c["start"] + c["dur"])], "els": []} for c in sm["clips"]]
    for k, o in enumerate(sp["overlays"]):
        if o["type"] not in ("text", "lower-third", "image"):
            continue
        b = f"overlays.{k}"
        if o["type"] == "text":
            props = {"text": {"type": "longtext", "label": "Text", "v": o.get("text", ""), "bind": f"{b}.text"},
                     "color": {"type": "color", "label": "Colour", "v": o.get("color", "#ffffff"), "bind": f"{b}.color"},
                     "size": {"type": "number", "label": "Size", "v": o.get("size", 72), "min": 16, "max": 300, "bind": f"{b}.size"}}
            label = (str(o.get("text", "")).split("\n")[0][:28] or "Text")
        elif o["type"] == "lower-third":
            props = {"title": {"type": "text", "label": "Name", "v": o.get("title", ""), "bind": f"{b}.title"},
                     "sub": {"type": "text", "label": "Role", "v": o.get("sub", ""), "bind": f"{b}.sub"},
                     "accent": {"type": "color", "label": "Accent", "v": o.get("accent", "#E7B65A"), "bind": f"{b}.accent"}}
            label = f"Lower third · {o.get('title', '')}"[:32]
        else:
            props = {"scale": {"type": "number", "label": "Scale", "v": o.get("scale", 1.0), "min": 0.05, "max": 1, "step": 0.01, "bind": f"{b}.scale"}}
            label = f"Image · {Path(o['src']).name}"
        props["anim"] = {"type": "motion", "label": "Motion", "v": o.get("anim", "")}
        el = {"id": f"ov{k}", "label": label, "t": [_r(o["start"]), _r(o["end"])], "box": _overlay_box(o, W, H, caps),
              "src": f"{spec_path.name}:overlays[{k}]", "props": props, "bind": b}
        host = next((s for s in scenes if s["t"][0] <= o["start"] < s["t"][1]), scenes[-1])
        host["els"].append(el)
    music = (raw.get("audio") or {}).get("music")
    return {"title": spec_path.stem, "w": W, "h": H, "fps": sp["fps"], "duration": sm["seconds"], "scenes": scenes,
            "brand": {"colors": [], "fonts": [], "logo": None},
            "audio": {"music": (music or {}).get("src") if isinstance(music, dict) else music},
            "kosif": {"kind": "timeline", "spec": str(spec_path.resolve())}}


def from_video(video: Path) -> dict:
    info = _probe(video)
    dur = float(info.get("duration") or 0)
    return {"title": video.stem, "w": info.get("width", 1920), "h": info.get("height", 1080), "fps": round(float(info.get("fps") or 30)),
            "duration": dur, "scenes": [{"id": f"S{i + 1}", "name": f"Shot {i + 1}", "t": t, "els": []} for i, t in enumerate(_cuts(video, dur))],
            "brand": {"colors": [], "fonts": [], "logo": None}, "kosif": {"kind": "video", "video": str(video.resolve())}}


# ---------------------------------------------------------------------------------------------------- folders
def folder_of(name: str) -> Path:
    for base in (motion.PROJECTS, REVIEWS):
        d = (base / name).resolve()
        if base.resolve() in d.parents and (d / "reel.json").exists():
            return d
    raise SystemExit(f"no review named {name!r} (run: kmotion review init …)")


def list_reels() -> list[dict]:
    out = []
    for base in (motion.PROJECTS, REVIEWS):
        if base.exists():
            for f in sorted(base.glob("*/reel.json")):
                try:
                    r = json.loads(f.read_text(encoding="utf-8"))
                except ValueError:
                    continue
                fb = sorted((f.parent / "review").glob("feedback-v*.json")) if (f.parent / "review").exists() else []
                out.append({"name": f.parent.name, "title": r.get("title"), "version": r.get("version", 1), "kind": (r.get("kosif") or {}).get("kind"),
                            "scenes": len(r.get("scenes", [])), "src": r.get("src"), "feedback": len(fb), "folder": str(f.parent)})
    return out


def init(target: Path, video: Path | None = None, title: str | None = None, name: str | None = None) -> dict:
    target = Path(target).resolve()
    if target.is_dir() and (target / "index.html").exists():
        video = video or _newest_video(target, target.name, own=True)
        reel, folder = from_html(target, video), target
    elif target.suffix.lower() == ".json":
        reel = from_timeline(target, video)
        folder = REVIEWS / (name or target.stem)
        video = video or _newest_video(target.parent, target.stem)
    elif target.suffix.lower() in (".mp4", ".mov", ".webm", ".mkv", ".m4v"):
        video, reel = target, from_video(target)
        folder = REVIEWS / (name or target.stem)
    else:
        raise SystemExit(f"{target}: give a project folder (index.html), a timeline spec (.json) or a video")
    folder.mkdir(parents=True, exist_ok=True)
    old = folder / "reel.json"
    prev = json.loads(old.read_text(encoding="utf-8")) if old.exists() else {}
    ver = int(prev.get("version", 0)) + 1
    rid = re.sub(r"[^a-z0-9-]+", "-", (name or folder.name).lower()).strip("-") or "reel"
    reel = {"id": rid, "title": title or prev.get("title") or reel["title"], "version": ver, "path": str(folder),
            "src": _place_video(folder, video, rid, ver) if video and Path(video).exists() else prev.get("src", ""), **{k: v for k, v in reel.items() if k != "title"}}
    reel["name"] = folder.name
    reel.setdefault("assets", [])
    reel.setdefault("audio", {"music": None, "bpm": None, "drop": 0, "musicVol": 0.6, "sfxVol": 0.8})
    if not isinstance(reel["audio"], dict) or "musicVol" not in reel["audio"]:
        reel["audio"] = {"music": (reel["audio"] or {}).get("music") if isinstance(reel["audio"], dict) else None, "bpm": None, "drop": 0, "musicVol": 0.6, "sfxVol": 0.8}
    if re.search(r"[؀-ۿ]", json.dumps([reel["title"], reel["scenes"]], ensure_ascii=False)):
        reel["lang"] = "ar"                                  # the page opens in Arabic (RTL), the prompt stays English
    reel["brand"]["colors"] = [c for c in reel["brand"]["colors"] if re.fullmatch(r"#[0-9a-fA-F]{6}", c["v"])]
    if reel["kosif"]["kind"] in ("html", "timeline"):
        reel["export"] = {"engine": "kosif", "cmd": f"kmotion review export {folder.name}"}
    reel["notes"] = prev.get("notes", [])
    reel["credit"] = "Review page: Motion OS player by Jason Lee (MIT). Engine: KOSIF Montage & Motion."
    old.write_text(json.dumps(reel, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"name": folder.name, "folder": str(folder), "version": ver, "scenes": len(reel["scenes"]),
            "elements": sum(len(s["els"]) for s in reel["scenes"]), "src": reel["src"], "kind": reel["kosif"]["kind"],
            "review_url": f"http://127.0.0.1:8766/review/{folder.name}/"}


def bump(name: str, video: Path | None = None) -> dict:
    folder = folder_of(name)
    reel = json.loads((folder / "reel.json").read_text(encoding="utf-8"))
    k = reel.get("kosif") or {}
    target = Path(k.get("project") or k.get("spec") or k.get("video") or folder)
    if k.get("kind") == "video" and video:
        target = video
    return init(target, video, reel.get("title"), None if k.get("kind") == "html" else name)


# ---------------------------------------------------------------------------------------------------- feedback
def save_feedback(name: str, fb: dict) -> dict:
    folder = folder_of(name)
    d = folder / "review"; d.mkdir(exist_ok=True)
    ver = int(fb.get("version") or json.loads((folder / "reel.json").read_text(encoding="utf-8")).get("version", 1))
    stamp = time.strftime("%Y%m%d-%H%M%S")
    fb = {**fb, "saved": stamp, "version": ver}
    (d / f"feedback-v{ver}-{stamp}.json").write_text(json.dumps(fb, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "feedback-latest.md").write_text(str(fb.get("text", "")), encoding="utf-8")
    return {"saved": f"review/feedback-v{ver}-{stamp}.json", "version": ver}


def latest_feedback(name: str) -> dict:
    folder = folder_of(name)
    files = sorted((folder / "review").glob("feedback-v*.json")) if (folder / "review").exists() else []
    if not files:
        return {"name": name, "feedback": None}
    return {"name": name, "file": str(files[-1]), **json.loads(files[-1].read_text(encoding="utf-8"))}


def _find_el(reel: dict, eid: str) -> dict | None:
    return next((e for s in reel["scenes"] for e in s["els"] if e["id"] == eid), None)


def _set_path(obj, dotted: str, value):
    keys = dotted.split(".")
    for k in keys[:-1]:
        obj = obj[int(k)] if isinstance(obj, list) else obj[k]
    last = keys[-1]
    if isinstance(obj, list):
        obj[int(last)] = value
    else:
        obj[last] = value


def apply(name: str, fb: dict | None = None) -> dict:
    """Write every bound edit into its source; return what was applied and what is left for Claude."""
    folder = folder_of(name)
    reel = json.loads((folder / "reel.json").read_text(encoding="utf-8"))
    fb = fb if fb is not None else latest_feedback(name)
    over = dict((fb or {}).get("over") or {})
    kind = (reel.get("kosif") or {}).get("kind")
    applied, left = [], []
    if kind == "html":
        index = Path(reel["kosif"]["project"]) / "index.html"
        html = index.read_text(encoding="utf-8"); props, m = _block(html, "kosif-props")
        for path, v in over.items():
            if path.endswith(".motion"):
                continue
            if path.startswith("brand.color."):
                cid = path[12:]
                new, n = re.subn(rf"(--{re.escape(cid)}\s*:\s*)#[0-9a-fA-F]{{3,8}}\b", lambda mm: mm.group(1) + str(v), html, count=1)
                if n:
                    html = new; applied.append(path)
                else:
                    left.append(path)
                continue
            eid, _, key = path.partition(".")
            el = _find_el(reel, eid)
            bind = el and (el.get("props", {}).get(key, {}).get("bind") if not key.startswith("@") else el.get(key[1:] + "Bind"))
            if bind and props is not None:
                props[bind] = v; applied.append(path)
            else:
                left.append(path)
        if props is not None and m:
            html = _set_block(html, "kosif-props", props)
        if applied:
            shutil.copy2(index, index.with_suffix(".html.bak")); index.write_text(html, encoding="utf-8")
    elif kind == "timeline":
        spec_path = Path(reel["kosif"]["spec"])
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        for path, v in over.items():
            if path.endswith(".motion"):
                continue
            eid, _, key = path.partition(".")
            el = _find_el(reel, eid)
            if not el:
                left.append(path); continue
            b = el["bind"]
            try:
                if key == "@time":
                    _set_path(spec, f"{b}.start", float(v[0])); _set_path(spec, f"{b}.end", float(v[1]))
                elif key == "@box":
                    x, y, w, h = (float(q) / 100 for q in v)
                    _set_path(spec, f"{b}.x", _r(x / (1 - w), 4) if w < 1 else 0); _set_path(spec, f"{b}.y", _r(y / (1 - h), 4) if h < 1 else 0)
                    if el["props"].get("size") and el["box"][3] > 0:
                        _set_path(spec, f"{b}.size", round(float(el["props"]["size"]["v"]) * (v[3] / el["box"][3])))
                elif el["props"].get(key, {}).get("bind"):
                    _set_path(spec, el["props"][key]["bind"], v)
                else:
                    left.append(path); continue
                applied.append(path)
            except (KeyError, IndexError, ValueError, TypeError):
                left.append(path)
        if applied:
            shutil.copy2(spec_path, spec_path.with_suffix(".json.bak"))
            spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        left = [p for p in over if not p.endswith(".motion")]
    notes = (fb or {}).get("notes") or []
    motion_req = {k: v for k, v in over.items() if k.endswith(".motion") and v}
    approved = [s for s, st in ((fb or {}).get("status") or {}).items() if st == "approved"]
    return {"name": name, "kind": kind, "applied": applied, "left_for_claude": {"edits": left, "notes": notes, "motion": motion_req,
            "links": (fb or {}).get("links") or []}, "approved_do_not_touch": approved,
            "next": "render, look at the sheet, then `kmotion review bump NAME --video NEW.mp4`" if applied or left or notes or motion_req else "nothing to do"}


def export(name: str, props: dict | None = None) -> dict:
    """The review page's Export button: apply the bound edits, render, re-open as the next version."""
    folder = folder_of(name)
    reel = json.loads((folder / "reel.json").read_text(encoding="utf-8"))
    rep = apply(name, {"over": props or {}} if props is not None else None)
    k = reel["kosif"]
    (folder / "exports").mkdir(exist_ok=True)
    out = folder / "exports" / f"{reel['id']}-v{reel.get('version', 1) + 1}.mp4"
    km = [sys.executable, str(HERE / "kmotion.py")]
    if k["kind"] == "timeline":
        cmd = km + ["timeline", k["spec"], "--out", str(out)]
    elif k["kind"] == "html":
        cmd = km + ["render", k["project"], "--out", str(out)]
    else:
        raise SystemExit("a plain video has nothing to re-render: send the notes to Claude")
    print("render:", subprocess.list2cmdline(cmd[1:]), flush=True)
    r = subprocess.run(cmd)
    if r.returncode != 0 or not out.exists():
        raise SystemExit(f"render failed (rc {r.returncode})")
    rep["bumped"] = bump(name, out)
    rep["out"] = str(out)
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("target"); p.add_argument("--video"); p.add_argument("--title"); p.add_argument("--name")
    p = sub.add_parser("apply"); p.add_argument("name"); p.add_argument("--feedback")
    p = sub.add_parser("export"); p.add_argument("name"); p.add_argument("--props")
    p = sub.add_parser("feedback"); p.add_argument("name")
    p = sub.add_parser("bump"); p.add_argument("name"); p.add_argument("--video")
    sub.add_parser("list")
    a = ap.parse_args()
    if a.cmd == "init":
        res = init(Path(a.target), Path(a.video) if a.video else None, a.title, a.name)
    elif a.cmd == "apply":
        res = apply(a.name, json.loads(Path(a.feedback).read_text(encoding="utf-8")) if a.feedback else None)
    elif a.cmd == "export":
        props = json.loads(Path(a.props or os.environ.get("PROPS", "")).read_text(encoding="utf-8")) if (a.props or os.environ.get("PROPS")) else None
        res = export(a.name, props.get("over", props) if isinstance(props, dict) else None)
    elif a.cmd == "feedback":
        fb = latest_feedback(a.name)
        if fb.get("text"):
            print(fb["text"]); return 0
        res = fb
    elif a.cmd == "bump":
        res = bump(a.name, Path(a.video) if a.video else None)
    else:
        res = {"reels": list_reels()}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
