#!/usr/bin/env python3
"""native_rapier_bake.py - deterministic 2D rigid-body baker for frame-exact video.

Idea ported (own code) from pmndrs/react-three-rapier (MIT) Physics.tsx:
fixed-timestep accumulator ("fix your timestep"), previous/current state
interpolation (lerp position, slerp rotation -> angle lerp in 2D), sleeping,
collision-started events. Difference: wall-clock dt is replaced by the video
frame clock (frame/fps), so output is bit-identical on every run.

Bodies: dynamic circles; static boxes (AABB) and static circles as colliders.
Output: per-frame transforms JSON + contact events with frame numbers.
Subcommands: bake, example, self-test.
"""
import argparse, hashlib, json, math, os, sys, tempfile

SLOP = 0.001          # allowed linear error (same default as R3R)
BETA = 0.2            # position-correction rate
REST_THRESHOLD = 0.5  # m/s: below this approach speed there is no bounce


class Body:
    def __init__(s, d, idx):
        s.id = d.get("id", "body%d" % idx)
        s.kind = d.get("kind", "circle")          # circle | box
        s.static = bool(d.get("static", s.kind == "box"))
        s.x, s.y = d.get("pos", [0.0, 0.0])
        s.vx, s.vy = d.get("vel", [0.0, 0.0])
        s.a = math.radians(d.get("angle_deg", 0.0))
        s.w = math.radians(d.get("spin_deg_s", 0.0))
        s.r = float(d.get("radius", 0.5))
        s.hw, s.hh = d.get("half", [0.5, 0.5])
        s.e = float(d.get("restitution", 0.5))
        s.mu = float(d.get("friction", 0.5))
        dens = float(d.get("density", 1.0))
        if s.static:
            s.im = s.ii = 0.0
        else:
            m = dens * math.pi * s.r ** 2
            s.im = 1.0 / m
            s.ii = 1.0 / (0.5 * m * s.r ** 2)
        s.sleeping = False
        s.rest_t = 0.0
        s.prev = (s.x, s.y, s.a)

    def state(s):
        return (s.x, s.y, s.a)


def contact(A, B):
    """Return (nx, ny, pen, px, py) with normal pointing from A to B, or None."""
    if A.kind == "circle" and B.kind == "circle":
        dx, dy = B.x - A.x, B.y - A.y
        d = math.hypot(dx, dy)
        rs = A.r + B.r
        if d >= rs:
            return None
        if d < 1e-12:
            return (0.0, 1.0, rs, A.x, A.y)
        nx, ny = dx / d, dy / d
        return (nx, ny, rs - d, A.x + nx * A.r, A.y + ny * A.r)
    if A.kind == "box" and B.kind == "circle":
        cx = min(max(B.x, A.x - A.hw), A.x + A.hw)
        cy = min(max(B.y, A.y - A.hh), A.y + A.hh)
        dx, dy = B.x - cx, B.y - cy
        d = math.hypot(dx, dy)
        if d > 1e-12:
            if d >= B.r:
                return None
            return (dx / d, dy / d, B.r - d, cx, cy)
        ox, oy = A.hw - abs(B.x - A.x), A.hh - abs(B.y - A.y)   # centre inside box
        if ox < oy:
            sx = 1.0 if B.x >= A.x else -1.0
            return (sx, 0.0, ox + B.r, B.x - sx * ox, B.y)
        sy = 1.0 if B.y >= A.y else -1.0
        return (0.0, sy, oy + B.r, B.x, B.y - sy * oy)
    if A.kind == "circle" and B.kind == "box":
        c = contact(B, A)
        return None if c is None else (-c[0], -c[1], c[2], c[3], c[4])
    return None


class World:
    def __init__(s, spec):
        s.g = spec.get("gravity", [0.0, -9.81])
        s.dt = 1.0 / float(spec.get("physics_hz", 120))
        s.iters = int(spec.get("solver_iterations", 8))
        s.bodies = [Body(b, i) for i, b in enumerate(spec["bodies"])]
        s.touching = set()
        s.events = []
        s.time = 0.0
        s.sleep_enabled = bool(spec.get("sleep", True))

    def step(s):
        dt = s.dt
        B = s.bodies
        for b in B:
            if not b.static and not b.sleeping:
                b.vx += s.g[0] * dt
                b.vy += s.g[1] * dt
        pairs = []
        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                A, C = B[i], B[j]
                if A.static and C.static:
                    continue
                if (A.sleeping or A.static) and (C.sleeping or C.static):
                    continue
                c = contact(A, C)
                if c is None:
                    continue
                nx, ny, pen, px, py = c
                vn0 = (C.vx - A.vx) * nx + (C.vy - A.vy) * ny
                pairs.append([A, C, nx, ny, pen, px, py, vn0, 0.0, 0.0])
        cur = set()
        for p in pairs:
            A, C = p[0], p[1]
            key = (A.id, C.id)
            cur.add(key)
            if key not in s.touching:
                s.events.append({"time": round(s.time, 6), "a": A.id, "b": C.id,
                                 "speed": round(max(0.0, -p[7]), 4),
                                 "point": [round(p[5], 4), round(p[6], 4)]})
        s.touching = cur
        for _ in range(s.iters):
            for p in pairs:
                A, C, nx, ny, pen, px, py, vn0 = p[:8]
                if A.static:
                    e = C.e
                elif C.static:
                    e = A.e
                else:
                    e = (A.e + C.e) / 2.0
                rax, ray = px - A.x, py - A.y
                rbx, rby = px - C.x, py - C.y
                vx = (C.vx - C.w * rby) - (A.vx - A.w * ray)
                vy = (C.vy + C.w * rbx) - (A.vy + A.w * rax)
                vn = vx * nx + vy * ny
                rnA = rax * ny - ray * nx
                rnB = rbx * ny - rby * nx
                kn = A.im + C.im + A.ii * rnA ** 2 + C.ii * rnB ** 2
                if kn == 0:
                    continue
                target = BETA / dt * max(pen - SLOP, 0.0)
                if vn0 < -REST_THRESHOLD:
                    target = max(target, -e * vn0)
                jn = (target - vn) / kn
                new = max(p[8] + jn, 0.0)
                jn = new - p[8]
                p[8] = new
                A.vx -= jn * nx * A.im; A.vy -= jn * ny * A.im; A.w -= A.ii * rnA * jn
                C.vx += jn * nx * C.im; C.vy += jn * ny * C.im; C.w += C.ii * rnB * jn
                tx, ty = -ny, nx
                vx = (C.vx - C.w * rby) - (A.vx - A.w * ray)
                vy = (C.vy + C.w * rbx) - (A.vy + A.w * rax)
                vt = vx * tx + vy * ty
                rtA = rax * ty - ray * tx
                rtB = rbx * ty - rby * tx
                kt = A.im + C.im + A.ii * rtA ** 2 + C.ii * rtB ** 2
                jt = -vt / kt
                mx = math.sqrt(A.mu * C.mu) * p[8]
                newt = max(-mx, min(mx, p[9] + jt))
                jt = newt - p[9]
                p[9] = newt
                A.vx -= jt * tx * A.im; A.vy -= jt * ty * A.im; A.w -= A.ii * rtA * jt
                C.vx += jt * tx * C.im; C.vy += jt * ty * C.im; C.w += C.ii * rtB * jt
        for b in B:
            if b.sleeping and not b.static:
                # wake if pushed by a moving body
                for (ka, kb) in cur:
                    other = kb if ka == b.id else ka if kb == b.id else None
                    if other is not None:
                        o = next(x for x in B if x.id == other)
                        if not o.static and math.hypot(o.vx, o.vy) > 0.2:
                            b.sleeping = False
                            b.rest_t = 0.0
        for b in B:
            if b.static or b.sleeping:
                continue
            b.x += b.vx * dt
            b.y += b.vy * dt
            b.a += b.w * dt
            if s.sleep_enabled:
                touching = any(b.id in k for k in cur)
                if touching and math.hypot(b.vx, b.vy) < 0.05 and abs(b.w) < 0.1:
                    b.rest_t += dt
                    if b.rest_t > 0.5:
                        b.sleeping = True
                        b.vx = b.vy = b.w = 0.0
                else:
                    b.rest_t = 0.0
        s.time += dt


def frame_of(t, fps):
    return int(math.ceil(t * fps - 1e-9))


def bake(spec):
    fps = float(spec.get("fps", 30))
    frames = int(spec.get("frames", round(fps * spec.get("seconds", 3))))
    w = World(spec)
    acc = 0.0
    last_t = 0.0
    out = []
    seen = 0
    for f in range(frames):
        t = f / fps                       # frame clock, never wall-clock
        acc += t - last_t
        last_t = t
        while acc >= w.dt - 1e-12:        # fixed-step accumulator
            for b in w.bodies:
                b.prev = b.state()
            w.step()
            acc -= w.dt
        alpha = max(0.0, min(1.0, acc / w.dt))
        rec = {}
        for b in w.bodies:
            if b.static:
                x, y, a = b.x, b.y, b.a
            else:
                px, py, pa = b.prev
                x = px + (b.x - px) * alpha
                y = py + (b.y - py) * alpha
                a = pa + (b.a - pa) * alpha     # 2D slerp == angle lerp
            rec[b.id] = {"x": round(x, 6), "y": round(y, 6),
                         "rot_deg": round(math.degrees(a), 4), "sleeping": b.sleeping}
        evs = [dict(e, frame=frame_of(e["time"], fps)) for e in w.events[seen:]]
        seen = len(w.events)
        out.append({"frame": f, "t": round(t, 6), "bodies": rec, "events": evs})
    return {"fps": fps, "frames": frames, "physics_hz": round(1.0 / w.dt, 6),
            "frames_data": out,
            "events": [dict(e, frame=frame_of(e["time"], fps)) for e in w.events],
            "sha256": hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()}


EXAMPLE = {
    "fps": 30, "seconds": 3, "physics_hz": 120, "gravity": [0, -9.81],
    "bodies": [
        {"id": "ground", "kind": "box", "pos": [0, -0.5], "half": [10, 0.5], "restitution": 0.5},
        {"id": "ball", "kind": "circle", "pos": [0, 2.5], "radius": 0.5, "restitution": 0.75},
        {"id": "ball2", "kind": "circle", "pos": [0.3, 5], "radius": 0.3, "restitution": 0.4},
    ]}


def self_test():
    ok = []

    def check(name, cond, info=""):
        assert cond, "FAIL %s %s" % (name, info)
        ok.append("%s: OK %s" % (name, info))

    spec = {"fps": 60, "seconds": 3, "physics_hz": 240, "bodies": [
        {"id": "ground", "kind": "box", "pos": [0, -0.5], "half": [10, 0.5], "restitution": 0.5},
        {"id": "ball", "kind": "circle", "pos": [0, 2.5], "radius": 0.5, "restitution": 0.5}]}
    r = bake(spec)
    t_hit = math.sqrt(2 * 2.0 / 9.81)
    first = r["events"][0]
    check("first impact time", abs(first["time"] - t_hit) < 0.02,
          "%.3fs vs analytic %.3fs" % (first["time"], t_hit))
    check("event frame", first["frame"] == frame_of(first["time"], 60), "frame %d" % first["frame"])
    ys = [fd["bodies"]["ball"]["y"] for fd in r["frames_data"]]
    fi = first["frame"]
    apex = max(ys[fi + 2: fi + 40]) - 0.5
    check("rebound height (e^2*h)", abs(apex - 0.5) < 0.08, "apex %.3f vs 0.500" % apex)
    r2 = bake(json.loads(json.dumps(spec)))
    check("deterministic sha256", r["sha256"] == r2["sha256"], r["sha256"][:12])
    a = bake(dict(spec, fps=24, seconds=2, physics_hz=100))["frames_data"][24]["bodies"]["ball"]["y"]
    b = bake(dict(spec, fps=60, seconds=2, physics_hz=100))["frames_data"][60]["bodies"]["ball"]["y"]
    check("render-fps independent sim", abs(a - b) < 1e-6, "y(1s)=%.4f/%.4f" % (a, b))
    r5 = bake(dict(spec, seconds=8))
    last = r5["frames_data"][-1]["bodies"]["ball"]
    check("settles and sleeps", last["sleeping"] and abs(last["y"] - 0.5) < 0.01, "y=%.4f" % last["y"])
    sp = {"fps": 30, "seconds": 2, "gravity": [0, 0], "physics_hz": 240, "bodies": [
        {"id": "L", "pos": [-2, 0], "vel": [2, 0], "radius": 0.5, "restitution": 1.0, "friction": 0},
        {"id": "R", "pos": [2, 0], "vel": [-1, 0], "radius": 0.5, "restitution": 1.0, "friction": 0}]}
    w = World(sp)
    p0 = sum(x.vx / x.im for x in w.bodies)
    for _ in range(480):
        w.step()
    p1 = sum(x.vx / x.im for x in w.bodies)
    L, R = w.bodies
    check("momentum conserved", abs(p0 - p1) < 1e-6, "%.4f->%.4f" % (p0, p1))
    check("elastic velocity swap", abs(L.vx + 1) < 0.05 and abs(R.vx - 2) < 0.05,
          "vL=%.3f vR=%.3f" % (L.vx, R.vx))
    sp7 = dict(spec, seconds=4)
    sp7["bodies"] = [spec["bodies"][0], {"id": "ball", "pos": [0, 0.5], "vel": [3, 0],
                                         "radius": 0.5, "restitution": 0, "friction": 0.8}]
    rot = bake(sp7)["frames_data"][-1]["bodies"]["ball"]["rot_deg"]
    check("rolling spin (clockwise)", rot < -90, "rot=%.1f deg" % rot)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "s.json")
        o = os.path.join(d, "o.json")
        json.dump(EXAMPLE, open(p, "w", encoding="utf-8"))
        main(["bake", p, "--out", o])
        data = json.load(open(o, encoding="utf-8"))
        check("bake file round-trip", len(data["frames_data"]) == 90 and len(data["events"]) >= 2,
              "%d frames, %d events" % (len(data["frames_data"]), len(data["events"])))
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("bake")
    b.add_argument("spec")
    b.add_argument("--out")
    b.add_argument("--json", action="store_true", help="(output is always JSON)")
    e = sp.add_parser("example")
    e.add_argument("--json", action="store_true")
    t = sp.add_parser("self-test")
    t.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "example":
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    if a.cmd == "self-test":
        res = self_test()
        if a.json:
            print(json.dumps({"ok": True, "checks": res}, ensure_ascii=False))
        else:
            print("\n".join(res))
            print("SELF-TEST PASS (%d checks)" % len(res))
        return 0
    spec = json.load(open(a.spec, encoding="utf-8"))
    r = bake(spec)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False)
        print(json.dumps({"frames": r["frames"], "events": r["events"], "sha256": r["sha256"],
                          "out": a.out}, ensure_ascii=False))
    else:
        print(json.dumps(r, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
