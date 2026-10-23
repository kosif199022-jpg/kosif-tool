#!/usr/bin/env python3
"""جسيمات حتمية قابلة للقفز لأي إطار: انفجار بصيغة مغلقة، وفحص ميزانية الجسيمات، وإطار SVG للمراجعة.
Seekable deterministic particles: closed-form bursts, particle budget checks and one SVG frame for review.

Serves the particles-fluids-physics power family: "replace Math.random with an integer hash or a seeded
PRNG so every frame renders identically, in any order", "compute each particle from t directly (ballistic,
closed-form drag) so no state accumulates between frames", and the budget rule "sizes 4/8/14 px, <= 2
colours, 150-600 on Canvas 2D, <= 20,000 WebGL points, behind type, uneven density" plus the deterministic
burst rule (<= ~40 particles on a music hit). Python standard library only, offline, deterministic.

Physics (screen pixels, y grows downward, linear drag k per second, gravity g px/s^2):
  x(t) = cx + vx * (1 - e^(-k t)) / k
  y(t) = cy + vy * (1 - e^(-k t)) / k + (g / k) * (t - (1 - e^(-k t)) / k)       (k = 0: ballistic)
  opacity = 1 - easeInOutCubic(age / life) while 0 <= age < life, else 0 (age = t - per-particle delay)
Every random number is lowbias32(seed, particle index, channel) / 2^32, so frame t needs no earlier frame.

Commands
  burst --seed S --count N --t T [--size WxH --cx X --cy Y --speed LO,HI --drag K --gravity G
        --life LO,HI --stagger S --sizes 4,8,14 --colors "#fff,#ffcc00" --visible-only]
      every particle's x, y, opacity, size and colour at time T (JSON).
      e.g. python3 scripts/particles.py burst --seed 7 --count 40 --t 0.5
  budget SPEC.json
      budget violations of a particle spec {"engine": "canvas2d|webgl|svg|dom", "kind": "ambient|burst",
      "count": N, "sizes": [..], "colors": [..], "behind_text": true, "seeded": true, "density": "uneven"}.
      e.g. python3 scripts/particles.py budget spec.json
  svg --t T [same options as burst] [--bg "#0b0b10"] [--out FRAME.svg]
      one frame as SVG for a visual check (stdout unless --out is given).
      e.g. python3 scripts/particles.py svg --seed 7 --count 160 --t 0.4 --out /tmp/frame.svg
  --self-test   run a small offline check and exit 0

File arguments accept '-' for stdin. Bad input: exit 2 with one line on stderr. Writes only the --out path you pass.
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

MASK = 0xFFFFFFFF
HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def read_text(path):
    """Read a UTF-8 file, or stdin when path is '-'."""
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8-sig")


class BadInput(ValueError):
    pass


def lowbias32(x):
    """Chris Wellons' lowbias32 integer hash (public domain)."""
    x &= MASK
    x ^= x >> 16
    x = (x * 0x7FEB352D) & MASK
    x ^= x >> 15
    x = (x * 0x846CA68B) & MASK
    x ^= x >> 16
    return x


def rand01(seed, i, ch):
    """Uniform [0,1) for (seed, particle, channel) with no state."""
    return lowbias32((seed * 0x9E3779B1) ^ lowbias32((i * 16 + ch) ^ 0x5BD1E995)) / 4294967296.0


def ease_in_out_cubic(x):
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def _pair(text, what, positive=False):
    try:
        a, b = (float(v) for v in str(text).split(","))
    except ValueError:
        raise BadInput("%s must be LO,HI" % what)
    if not (math.isfinite(a) and math.isfinite(b)) or a > b or (positive and a <= 0):
        raise BadInput("%s needs LO <= HI%s" % (what, " and LO > 0" if positive else ""))
    return a, b


def _size(text):
    m = re.fullmatch(r"(\d+)[xX](\d+)", str(text).strip())
    if not m or int(m.group(1)) <= 0 or int(m.group(2)) <= 0:
        raise BadInput("--size must be WxH, e.g. 1080x1920")
    return int(m.group(1)), int(m.group(2))


def make_cfg(a):
    w, h = _size(a.size)
    if not 1 <= a.count <= 100000:
        raise BadInput("--count must be between 1 and 100000")
    for v, n in ((a.t, "--t"), (a.drag, "--drag"), (a.gravity, "--gravity"), (a.stagger, "--stagger")):
        if not math.isfinite(v):
            raise BadInput("%s must be finite" % n)
    if a.t < 0 or a.drag < 0 or a.stagger < 0:
        raise BadInput("--t, --drag and --stagger must be >= 0")
    sizes = [float(s) for s in a.sizes.split(",") if s.strip()]
    if not sizes or any(s <= 0 for s in sizes):
        raise BadInput("--sizes must be positive numbers")
    colors = [c.strip() for c in a.colors.split(",") if c.strip()]
    if not colors or not all(HEX.match(c) for c in colors):
        raise BadInput("--colors must be #rgb or #rrggbb values")
    return {"seed": a.seed, "count": a.count, "t": a.t, "w": w, "h": h,
            "cx": w / 2 if a.cx is None else a.cx, "cy": h / 2 if a.cy is None else a.cy,
            "speed": _pair(a.speed, "--speed"), "life": _pair(a.life, "--life", positive=True),
            "drag": a.drag, "gravity": a.gravity, "stagger": a.stagger, "sizes": sizes, "colors": colors}


def particle(cfg, i, t):
    s = cfg["seed"]
    theta = 2 * math.pi * rand01(s, i, 0)
    lo, hi = cfg["speed"]
    sp = lo + (hi - lo) * rand01(s, i, 1)
    llo, lhi = cfg["life"]
    life = llo + (lhi - llo) * rand01(s, i, 2)
    delay = cfg["stagger"] * rand01(s, i, 3)
    size = cfg["sizes"][int(rand01(s, i, 4) * len(cfg["sizes"]))]
    color = cfg["colors"][int(rand01(s, i, 5) * len(cfg["colors"]))]
    vx, vy = sp * math.cos(theta), sp * math.sin(theta)
    age = max(0.0, t - delay)
    k, g = cfg["drag"], cfg["gravity"]
    if k > 0:
        f = (1 - math.exp(-k * age)) / k
        x = cfg["cx"] + vx * f
        y = cfg["cy"] + vy * f + (g / k) * (age - f)
    else:
        x = cfg["cx"] + vx * age
        y = cfg["cy"] + vy * age + 0.5 * g * age * age
    if t < delay or age >= life:
        op = 0.0
    else:
        op = 1 - ease_in_out_cubic(age / life)
    return {"i": i, "x": round(x, 3), "y": round(y, 3), "opacity": round(op, 4), "size": size,
            "color": color, "age": round(age, 4), "life": round(life, 4), "delay": round(delay, 4)}


def burst(cfg, visible_only=False):
    ps = [particle(cfg, i, cfg["t"]) for i in range(cfg["count"])]
    vis = [p for p in ps if p["opacity"] > 0]
    on = [p for p in vis if 0 <= p["x"] <= cfg["w"] and 0 <= p["y"] <= cfg["h"]]
    return {"command": "burst", "seed": cfg["seed"], "t": cfg["t"], "count": cfg["count"],
            "canvas": [cfg["w"], cfg["h"]], "origin": [cfg["cx"], cfg["cy"]], "visible": len(vis),
            "visible_on_canvas": len(on), "rng": "lowbias32(seed, index, channel) — seekable, order-free",
            "particles": vis if visible_only else ps}


def svg(cfg, bg):
    if not HEX.match(bg):
        raise BadInput("--bg must be #rgb or #rrggbb")
    r = burst(cfg, visible_only=True)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
           % (cfg["w"], cfg["h"], cfg["w"], cfg["h"]),
           '<!-- particles.py seed=%s t=%s count=%s visible=%s -->' % (cfg["seed"], cfg["t"], cfg["count"], r["visible"]),
           '<rect width="100%%" height="100%%" fill="%s"/>' % bg]
    for p in r["particles"]:
        out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" fill-opacity="%.3f"/>'
                   % (p["x"], p["y"], p["size"] / 2, p["color"], p["opacity"]))
    out.append("</svg>")
    return "\n".join(out) + "\n", r


ENGINE_MAX = {"canvas2d": 600, "webgl": 20000, "svg": 300, "dom": 300}
ENGINE_MIN = {"canvas2d": 150}


def budget(spec):
    if not isinstance(spec, dict):
        raise BadInput("spec must be a JSON object")
    eng = spec.get("engine")
    if eng not in ENGINE_MAX:
        raise BadInput("engine must be one of: %s" % ", ".join(sorted(ENGINE_MAX)))
    cnt = spec.get("count")
    if isinstance(cnt, bool) or not isinstance(cnt, int) or cnt < 0:
        raise BadInput("count must be a non-negative integer")
    sizes = spec.get("sizes", [])
    colors = spec.get("colors", [])
    if not isinstance(sizes, list) or not all(isinstance(s, (int, float)) and not isinstance(s, bool) for s in sizes):
        raise BadInput("sizes must be a list of numbers")
    if not isinstance(colors, list) or not all(isinstance(c, str) for c in colors):
        raise BadInput("colors must be a list of strings")
    kind = spec.get("kind", "ambient")
    if kind not in ("ambient", "burst"):
        raise BadInput("kind must be ambient or burst")
    v, w = [], []

    def add(lst, rule, msg, src):
        lst.append({"rule": rule, "message": msg, "source": src})
    ds = sorted(set(float(s) for s in sizes))
    if len(ds) > 3:
        add(v, "sizes.max3", "%d distinct sizes; use at most three (e.g. 4/8/14 px)" % len(ds), "PART-04")
    elif ds and not set(ds) <= {4.0, 8.0, 14.0}:
        add(w, "sizes.scale", "sizes %s are off the 4/8/14 px scale" % ds, "PART-04")
    if any(s > 14 for s in ds):
        add(w, "sizes.large", "particles larger than 14 px read as objects, not particles", "PART-04")
    dc = sorted(set(c.strip().lower() for c in colors))
    if len(dc) > 2:
        add(v, "colors.max2", "%d colours; use at most two" % len(dc), "PART-04")
    if cnt > ENGINE_MAX[eng]:
        add(v, "count.engine", "%d particles exceed the %s budget of %d" % (cnt, eng, ENGINE_MAX[eng]),
            "PART-04" if eng in ("canvas2d", "webgl") else "tool heuristic (DOM/SVG nodes per frame)")
    if eng in ENGINE_MIN and 0 < cnt < ENGINE_MIN[eng] and kind == "ambient":
        add(w, "count.sparse", "%d ambient particles is below the 150-600 Canvas range; field may look sparse" % cnt, "PART-04")
    if kind == "burst" and cnt > 40:
        add(v, "burst.max40", "a deterministic hit burst should stay at about 40 particles or fewer (%d)" % cnt, "PART-09")
    if spec.get("seeded") is False:
        add(v, "seeded", "unseeded randomness (Math.random) makes frames differ between renders", "PART-01")
    elif "seeded" not in spec:
        add(w, "seeded.unknown", "spec does not state whether randomness is seeded/hashed", "PART-01")
    if spec.get("behind_text") is False:
        add(v, "layer.behind_text", "particles must sit behind type, never over it", "PART-04")
    if spec.get("density") == "uniform":
        add(w, "density.uniform", "uniform density looks like noise; vary density toward the subject", "PART-04")
    return {"command": "budget", "engine": eng, "kind": kind, "count": cnt, "distinct_sizes": ds,
            "distinct_colors": dc, "limit": ENGINE_MAX[eng], "violations": v, "warnings": w,
            "verdict": "pass" if not v else "fail"}


def _ns(**kw):
    d = dict(seed=1, count=40, t=0.5, size="1080x1080", cx=None, cy=None, speed="300,900", drag=2.5,
             gravity=300.0, life="0.8,1.6", stagger=0.0, sizes="4,8,14", colors="#ffffff,#ffcc00")
    d.update(kw)
    return argparse.Namespace(**d)


def self_test():
    c = make_cfg(_ns(t=0.0))
    assert all(p["x"] == 540 and p["y"] == 540 and p["opacity"] == 1 for p in burst(c)["particles"])
    c = make_cfg(_ns(t=0.7, count=50))
    a = burst(c)["particles"][37]
    assert a == particle(c, 37, 0.7)  # seek a single particle, no history needed
    assert budget({"engine": "canvas2d", "count": 900, "sizes": [4], "colors": ["#fff"]})["verdict"] == "fail"
    s, _ = svg(make_cfg(_ns(count=5)), "#000000")
    assert s.count("<circle") <= 5 and s.startswith("<svg")
    return {"self_test": "ok", "checks": 4}


def add_burst_opts(s):
    s.add_argument("--seed", type=int, default=1)
    s.add_argument("--count", type=int, default=160)
    s.add_argument("--t", type=float, required=True, help="time in seconds since the burst")
    s.add_argument("--size", default="1080x1080")
    s.add_argument("--cx", type=float)
    s.add_argument("--cy", type=float)
    s.add_argument("--speed", default="300,900", help="px/s LO,HI")
    s.add_argument("--drag", type=float, default=2.5, help="linear drag per second (0 = ballistic)")
    s.add_argument("--gravity", type=float, default=300.0, help="px/s^2, positive pulls down")
    s.add_argument("--life", default="0.8,1.6", help="seconds LO,HI")
    s.add_argument("--stagger", type=float, default=0.0, help="max random start delay in seconds")
    s.add_argument("--sizes", default="4,8,14")
    s.add_argument("--colors", default="#ffffff,#ffcc00")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--self-test", action="store_true", help="run a small offline check and exit 0")
    sub = p.add_subparsers(dest="cmd")
    b = sub.add_parser("burst"); add_burst_opts(b); b.add_argument("--visible-only", action="store_true")
    g = sub.add_parser("budget"); g.add_argument("spec")
    s = sub.add_parser("svg"); add_burst_opts(s); s.add_argument("--bg", default="#0b0b10"); s.add_argument("--out")
    args = p.parse_args(argv)
    try:
        if args.self_test:
            print(json.dumps(self_test()))
            return 0
        if args.cmd == "burst":
            r = burst(make_cfg(args), args.visible_only)
        elif args.cmd == "budget":
            try:
                spec = json.loads(read_text(args.spec))
            except FileNotFoundError:
                raise BadInput("spec file not found: %s" % args.spec)
            except json.JSONDecodeError as e:
                raise BadInput("spec is not valid JSON: %s" % e.msg)
            r = budget(spec)
        elif args.cmd == "svg":
            text, info = svg(make_cfg(args), args.bg)
            if args.out:
                Path(args.out).write_text(text, encoding="utf-8")
                print(json.dumps({"command": "svg", "out": args.out, "t": info["t"], "visible": info["visible"],
                                  "bytes": len(text.encode())}))
            else:
                sys.stdout.write(text)
            return 0
        else:
            p.print_help(sys.stderr)
            return 2
    except BadInput as e:
        print("particles: %s" % e, file=sys.stderr)
        return 2
    except AssertionError as e:
        print("particles: self-test failed: %s" % e, file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
