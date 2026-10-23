#!/usr/bin/env python3
"""KOSIF UI beat — cursor keyframes, RTL layout mirroring and seamless-loop checks for product UI motion.

إيقاع الواجهات: مسار مؤشر بمنحنى بيزييه وتوقيتات النقر، وعكس تخطيط الواجهة للعربية، وفحص الحلقات المتصلة.
UI beat: eased Bezier cursor keyframes with click/ripple timings, RTL mirroring of a layout, and a check
that a loop's first and last states are identical. Standard library only, no network, deterministic.

Subcommands (run from the skill root):
  cursor --from x,y --to x,y --dur s --fps n [--ease ease-in-out|ease-out|ease-in|linear|cubic-bezier:a,b,c,d]
         [--arc 0.12] [--no-click] [--press-ms 90] [--response-ms 80] [--ripple-ms 300] [--ripple-px 64]
      one keyframe per frame (frame 0..round(dur*fps)) along a quadratic Bezier bowed by --arc times the
      distance (positive bows to the right of travel on screen, y down), timed by a CSS-style cubic-bezier easing solved exactly by
      bisection; then press/release frames, UI response time and ripple (radius 0 -> px, opacity 0.6 -> 0)
      e.g. python3 scripts/ui_beat.py cursor --from 900,1700 --to 540,960 --dur 0.8 --fps 30
  rtl-mirror layout.json --width W
      x' = W - x - w for every element, text-align/align left<->right (start/end kept), and the list of
      directional icons that must flip (arrows, chevrons, back/forward, undo/redo, send, reply ...) versus
      icons that must not (play, checkmark, clock, search, media ...)
      e.g. python3 scripts/ui_beat.py rtl-mirror layout.json --width 1080
  loop-check states.json [--tol 0.000001]
      flattens the first and last state (dotted keys) and lists every key that differs, is missing or has
      a different type; seamless only when none differ; warns when a given duration is outside 3-6 s
      e.g. python3 scripts/ui_beat.py loop-check states.json
  --self-test   offline check, exits 0 on success

All output is JSON on stdout; nothing is written. Bad input exits 2 with one line on stderr.
"""
import argparse
import json
import math
import re
import sys

EASES = {"linear": (0.0, 0.0, 1.0, 1.0), "ease": (0.25, 0.1, 0.25, 1.0), "ease-in": (0.42, 0.0, 1.0, 1.0),
         "ease-out": (0.0, 0.0, 0.58, 1.0), "ease-in-out": (0.42, 0.0, 0.58, 1.0),
         "expressive": (0.65, 0.0, 0.35, 1.0)}
FLIP = ["arrow-left", "arrow-right", "arrow-back", "arrow-forward", "chevron-left", "chevron-right", "caret-left",
        "caret-right", "back", "forward", "next", "previous", "prev", "undo", "redo", "send", "reply", "reply-all",
        "forward-mail", "exit", "logout", "login", "first-page", "last-page", "skip-next", "skip-previous",
        "list-bullet", "indent", "outdent", "text-left", "text-right", "sort-left", "trending", "redo-arrow",
        "open-in-new", "external-link", "keyboard-tab", "subdirectory", "comment", "chat-bubble", "rotate-left",
        "rotate-right", "volume", "help", "label", "bike", "car", "cart", "shopping-cart"]
KEEP = ["play", "pause", "stop", "fast-forward", "rewind", "check", "checkmark", "clock", "time", "search",
        "close", "plus", "minus", "add", "remove", "settings", "gear", "home", "user", "person", "heart", "star",
        "camera", "image", "music", "phone", "mail", "lock", "bell", "download", "upload", "share", "refresh",
        "media", "slash", "circle", "dot", "menu", "more", "logo", "brand", "graph", "chart", "battery"]
ALIGN = {"left": "right", "right": "left", "start": "start", "end": "end", "center": "center",
         "justify": "justify", "flex-start": "flex-start", "flex-end": "flex-end"}


class Bad(Exception):
    pass


def point(s, name):
    try:
        x, y = (float(v) for v in str(s).split(","))
    except ValueError:
        raise Bad("--%s must be x,y (got %r)" % (name, s))
    return x, y


def parse_ease(s):
    if s in EASES:
        return EASES[s]
    m = re.match(r"^cubic-bezier[:(]\s*([^)]*)\)?$", s or "")
    if not m:
        raise Bad("unknown --ease %r (use %s or cubic-bezier:a,b,c,d)" % (s, ", ".join(EASES)))
    try:
        v = tuple(float(x) for x in m.group(1).split(","))
    except ValueError:
        raise Bad("bad cubic-bezier numbers %r" % s)
    if len(v) != 4 or not (0 <= v[0] <= 1 and 0 <= v[2] <= 1):
        raise Bad("cubic-bezier needs 4 numbers with x1 and x2 in [0,1]")
    return v


def bez1(p1, p2, t):
    u = 1 - t
    return 3 * u * u * t * p1 + 3 * u * t * t * p2 + t ** 3


def ease_value(e, x):
    """y of a CSS cubic-bezier timing function at progress x (bisection on the monotonic x(t))."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if bez1(e[0], e[2], mid) < x:
            lo = mid
        else:
            hi = mid
    return bez1(e[1], e[3], (lo + hi) / 2)


def cursor(frm, to, dur, fps, ease="ease-in-out", arc=0.12, click=True, press_ms=90, response_ms=80,
           ripple_ms=300, ripple_px=64):
    if dur <= 0 or fps <= 0:
        raise Bad("--dur and --fps must be positive")
    e = parse_ease(ease)
    n = round(dur * fps)
    if n < 1:
        raise Bad("duration shorter than one frame")
    (x0, y0), (x1, y1) = frm, to
    dx, dy = x1 - x0, y1 - y0
    dist = math.hypot(dx, dy)
    # control point: midpoint pushed perpendicular (right of travel on screen, y down) by arc*dist
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if dist:
        cx += -dy / dist * arc * dist
        cy += dx / dist * arc * dist
    keys = []
    for f in range(n + 1):
        t = f / n
        s = ease_value(e, t)
        u = 1 - s
        x = u * u * x0 + 2 * u * s * cx + s * s * x1
        y = u * u * y0 + 2 * u * s * cy + s * s * y1
        tx = 2 * u * (cx - x0) + 2 * s * (x1 - cx)
        ty = 2 * u * (cy - y0) + 2 * s * (y1 - cy)
        keys.append({"frame": f, "t": round(f / fps, 4), "progress": round(s, 6), "x": round(x, 3),
                     "y": round(y, 3), "angle_deg": round(math.degrees(math.atan2(ty, tx)), 2) if (tx or ty) else 0.0})
    keys[-1]["x"], keys[-1]["y"] = round(x1, 3), round(y1, 3)
    out = {"kind": "kosif.ui_beat.cursor.v1", "from": [x0, y0], "to": [x1, y1], "duration_s": dur, "fps": fps,
           "frames": n + 1, "ease": ease, "cubic_bezier": list(e), "arc": arc,
           "control_point": [round(cx, 3), round(cy, 3)], "distance_px": round(dist, 3), "keyframes": keys}
    if click:
        press_s = n / fps
        rel_s = press_s + press_ms / 1000
        resp_s = press_s + response_ms / 1000
        out["click"] = {"press_s": round(press_s, 4), "press_frame": n,
                        "release_s": round(rel_s, 4), "release_frame": n + round(press_ms / 1000 * fps),
                        "ui_response_s": round(resp_s, 4), "ui_response_frame": n + round(response_ms / 1000 * fps),
                        "cursor_scale": {"down": 0.88, "up": 1.0},
                        "ripple": {"start_s": round(press_s, 4), "end_s": round(press_s + ripple_ms / 1000, 4),
                                   "start_frame": n, "end_frame": n + round(ripple_ms / 1000 * fps),
                                   "radius_px": [0, ripple_px], "opacity": [0.6, 0.0], "ease": "ease-out"},
                        "note": "UI response 60-120 ms after the press; 0 ms reads as a slideshow, >200 ms as a bug"}
        if not 60 <= response_ms <= 120:
            out["click"]["warning"] = "response %d ms is outside 60-120 ms" % response_ms
    return out


def icon_kind(name):
    k = str(name).lower().replace("_", "-").replace(" ", "-")
    for f in FLIP:
        if k == f or k.startswith(f + "-") or k.endswith("-" + f) or ("-" + f + "-") in k:
            return "flip"
    for f in KEEP:
        if k == f or k.startswith(f + "-") or k.endswith("-" + f) or ("-" + f + "-") in k:
            return "keep"
    if re.search(r"(left|right|back|forward|next|prev)", k):
        return "flip"
    return "keep"


def rtl_mirror(layout, width):
    if width <= 0:
        raise Bad("--width must be positive")
    els = layout.get("elements") if isinstance(layout, dict) else layout
    if not isinstance(els, list):
        raise Bad("layout needs an 'elements' list")
    out, flip, keep, warn = [], [], [], []
    for i, el in enumerate(els):
        if not isinstance(el, dict):
            raise Bad("element %d is not an object" % (i + 1))
        try:
            x, w = float(el["x"]), float(el.get("w", el.get("width", 0)))
        except (KeyError, TypeError, ValueError):
            raise Bad("element %d needs numeric 'x' (and 'w')" % (i + 1))
        eid = el.get("id", "el%d" % (i + 1))
        m = dict(el)
        nx = width - x - w
        m["x"] = int(nx) if nx == int(nx) else round(nx, 3)
        if x < 0 or x + w > width:
            warn.append("%s lies outside 0..%s" % (eid, width))
        for key in ("align", "text_align", "textAlign", "justify"):
            if key in el:
                v = str(el[key])
                if v not in ALIGN:
                    raise Bad("element %s has unknown %s %r" % (eid, key, v))
                m[key] = ALIGN[v]
        if "anchor" in el:
            m["anchor"] = {"left": "right", "right": "left"}.get(el["anchor"], el["anchor"])
        if "dir" in el or el.get("text"):
            m["dir"] = "rtl"
        icon = el.get("icon")
        if icon:
            if icon_kind(icon) == "flip":
                m["icon_transform"] = "scaleX(-1)"
                flip.append({"id": eid, "icon": icon})
            else:
                keep.append({"id": eid, "icon": icon})
        out.append(m)
    return {"kind": "kosif.ui_beat.rtl_mirror.v1", "width": width, "elements": out, "icons_flip": flip,
            "icons_keep": keep, "container": {"dir": "rtl", "note": "set dir=rtl on the UI container, use logical "
                                              "CSS (margin-inline-start, inset-inline-end)"}, "warnings": warn}


def flatten(v, prefix="", out=None):
    out = {} if out is None else out
    if isinstance(v, dict):
        if not v and prefix:
            out[prefix] = {}
        for k in sorted(v):
            flatten(v[k], "%s.%s" % (prefix, k) if prefix else str(k), out)
    elif isinstance(v, list):
        if not v and prefix:
            out[prefix] = []
        for i, x in enumerate(v):
            flatten(x, "%s[%d]" % (prefix, i), out)
    else:
        out[prefix] = v
    return out


def loop_check(data, tol=1e-6):
    dur = None
    if isinstance(data, dict) and "start" in data and "end" in data:
        a, b, dur = data["start"], data["end"], data.get("duration")
    elif isinstance(data, dict) and isinstance(data.get("states"), list):
        st, dur = data["states"], data.get("duration")
        if len(st) < 2:
            raise Bad("need at least two states")
        a, b = st[0], st[-1]
    elif isinstance(data, list) and len(data) >= 2:
        a, b = data[0], data[-1]
    else:
        raise Bad("states.json needs {start,end}, {states:[...]} or a list of 2+ states")
    fa, fb = flatten(a), flatten(b)
    diffs = []
    for k in sorted(set(fa) | set(fb)):
        if k not in fa or k not in fb:
            diffs.append({"key": k, "start": fa.get(k), "end": fb.get(k),
                          "reason": "missing at start" if k not in fa else "missing at end"})
            continue
        va, vb = fa[k], fb[k]
        num = lambda v: isinstance(v, (int, float)) and not isinstance(v, bool)  # noqa: E731
        if num(va) and num(vb):
            if abs(va - vb) > tol:
                diffs.append({"key": k, "start": va, "end": vb, "reason": "delta %g" % (vb - va)})
        elif type(va) is not type(vb):
            diffs.append({"key": k, "start": va, "end": vb, "reason": "type differs"})
        elif va != vb:
            diffs.append({"key": k, "start": va, "end": vb, "reason": "value differs"})
    warn = []
    if dur is not None:
        try:
            d = float(dur)
        except (TypeError, ValueError):
            raise Bad("duration must be a number")
        if not 3 <= d <= 6:
            warn.append("loop duration %g s is outside the 3-6 s range for seamless UI loops" % d)
    return {"kind": "kosif.ui_beat.loop_check.v1", "keys_compared": len(set(fa) | set(fb)),
            "seamless": not diffs, "differing": diffs, "warnings": warn}


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        raise Bad("cannot read JSON %s: %s" % (path, e))


def self_test():
    c = cursor((0, 0), (100, 0), 1, 10, "linear", 0)
    assert c["frames"] == 11 and c["keyframes"][5]["x"] == 50.0 and c["keyframes"][-1]["x"] == 100
    assert abs(ease_value(EASES["ease-in-out"], 0.5) - 0.5) < 1e-9
    m = rtl_mirror({"elements": [{"id": "b", "x": 20, "w": 100, "align": "left", "icon": "chevron-left"}]}, 1080)
    assert m["elements"][0]["x"] == 960 and m["elements"][0]["align"] == "right" and m["icons_flip"]
    assert loop_check({"start": {"a": 1}, "end": {"a": 1}})["seamless"]
    assert not loop_check([{"a": 1}, {"a": 2}])["seamless"]
    print("self-test: OK")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(prog="ui_beat.py",
                                 description="إيقاع الواجهات — KOSIF UI beat: cursor paths, RTL mirror, loop check")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cursor")
    c.add_argument("--from", dest="frm", required=True)
    c.add_argument("--to", required=True)
    c.add_argument("--dur", type=float, required=True)
    c.add_argument("--fps", type=float, required=True)
    c.add_argument("--ease", default="ease-in-out")
    c.add_argument("--arc", type=float, default=0.12)
    c.add_argument("--no-click", action="store_true")
    c.add_argument("--press-ms", type=int, default=90)
    c.add_argument("--response-ms", type=int, default=80)
    c.add_argument("--ripple-ms", type=int, default=300)
    c.add_argument("--ripple-px", type=int, default=64)
    r = sub.add_parser("rtl-mirror")
    r.add_argument("layout")
    r.add_argument("--width", type=float, required=True)
    lc = sub.add_parser("loop-check")
    lc.add_argument("states")
    lc.add_argument("--tol", type=float, default=1e-6)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "cursor":
            fps = int(args.fps) if args.fps == int(args.fps) else args.fps
            res = cursor(point(args.frm, "from"), point(args.to, "to"), args.dur, fps, args.ease, args.arc,
                         not args.no_click, args.press_ms, args.response_ms, args.ripple_ms, args.ripple_px)
        elif args.cmd == "rtl-mirror":
            w = int(args.width) if args.width == int(args.width) else args.width
            res = rtl_mirror(load_json(args.layout), w)
        else:
            res = loop_check(load_json(args.states), args.tol)
    except Bad as e:
        print("ui_beat: " + str(e), file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
