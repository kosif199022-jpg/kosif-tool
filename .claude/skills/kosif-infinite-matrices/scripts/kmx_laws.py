#!/usr/bin/env python3
"""Four typed causal laws ported from the owner's Infinite Matrices v0.2 causal studio (SRC-024).

The v1 engine (kmx_engine.py) runs one mechanism: light written into glass steers motes
(memory -> dynamics). This module adds the four small particle laws of v0.2, each with a typed
contract (input port -> output port) and one causal edge that the control arm switches off:

  trajectory_memory  ScalarField2D.grad   -> ParticleVelocity2D      stored light -> velocity
  material_memory    ScalarField2D.sample -> MaterialOpacity         stored light -> material luminance
  elastic_memory     ScalarField2D.grad   -> ParticleDisplacement2D  stored light -> elastic displacement
  self_imprinting    ParticlePositions2D  -> ScalarField2D           particle history -> memory field -> velocity

self_imprinting is the "memory written by the motes themselves" adapter that engine.md listed as
missing: both arms keep the same field -> motion law; only the particle -> field write is removed.

Arithmetic is kept identical to v0.2 so the owner's four demo receipts reproduce exactly
(tests/test_kmx_laws.py). Added on top of v0.2: a dose sweep (gain x 0, .25, .5, 1) with a
Spearman rho, so a law is CONFIRMED_IN_MODEL only when the effect is 0 at gain 0, positive at
full gain and rises with the dose (the repo's A/B/C + dose standard). SVG frames are written only
when asked (--render) and never committed. Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
RECIPES = SKILL / "recipes" / "laws"
ATOMS = SKILL / "data" / "197_mechanism_atoms.json"
VERSION = "kmx-laws-1 (from causal_studio 0.2.0)"

LAWS = {
    "trajectory_memory": {"input": "ScalarField2D.grad", "output": "ParticleVelocity2D", "edge": "stored light → velocity"},
    "material_memory": {"input": "ScalarField2D.sample", "output": "MaterialOpacity", "edge": "stored light → material luminance"},
    "elastic_memory": {"input": "ScalarField2D.grad", "output": "ParticleDisplacement2D", "edge": "stored light → elastic displacement"},
    "self_imprinting": {"input": "ParticlePositions2D", "output": "ScalarField2D", "edge": "particle history → memory field → velocity"},
}
GEOMETRIES = ("rings", "spiral", "lattice")
DOSE = (0.0, 0.25, 0.5, 1.0)


def canonical(data):
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(data):
    return hashlib.sha256(canonical(data).encode("utf8")).hexdigest()


@dataclass
class Particle:
    x: float
    y: float
    material: float = 0.55


class ScalarField:
    N = 35

    def __init__(self):
        self.a = [[0.0] * self.N for _ in range(self.N)]

    @staticmethod
    def clamp(v):
        return max(-.999, min(.999, v))

    def coord(self, x, y):
        return (max(0, min(self.N - 1, round((self.clamp(x) + 1) * (self.N - 1) / 2))),
                max(0, min(self.N - 1, round((self.clamp(y) + 1) * (self.N - 1) / 2))))

    def sample(self, x, y):
        i, j = self.coord(x, y)
        return self.a[j][i]

    def grad(self, x, y):
        h = 2 / (self.N - 1)
        return ((self.sample(x + h, y) - self.sample(x - h, y)) / (2 * h),
                (self.sample(x, y + h) - self.sample(x, y - h)) / (2 * h))

    def advance(self, t, light_steps, decay):
        cx = 0.34 * math.sin(t * .31)
        cy = 0.24 * math.cos(t * .27)
        for j in range(self.N):
            y = -1 + 2 * j / (self.N - 1)
            for i in range(self.N):
                x = -1 + 2 * i / (self.N - 1)
                excitation = 0.33 * math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / .055) if t < light_steps else 0
                self.a[j][i] = min(4, decay * self.a[j][i] + excitation)

    def imprint(self, particles):
        for p in particles:
            i, j = self.coord(p.x, p.y)
            self.a[j][i] = min(4, self.a[j][i] + .035)


def initial(geometry, n=120):
    out = []
    for i in range(n):
        q = i / max(n - 1, 1)
        if geometry == "spiral":
            theta = 6 * math.pi * q
            radius = .1 + .72 * math.sqrt(q)
            x, y = radius * math.cos(theta), radius * math.sin(theta)
        elif geometry == "lattice":
            k = math.ceil(math.sqrt(n))
            row, col = divmod(i, k)
            x, y = -.82 + 1.64 * col / (k - 1), -.82 + 1.64 * row / (k - 1)
        elif geometry == "rings":
            theta = 2.3999632 * i
            radius = .10 + .75 * (i % 11) / 10
            x, y = radius * math.cos(theta), radius * math.sin(theta)
        else:
            raise ValueError("unsupported geometry " + geometry)
        out.append(Particle(x, y))
    return out


def validate_plan(plan):
    errs = []
    law = plan.get("law")
    par = plan.get("parameters") or {}
    if law not in LAWS:
        errs.append("law not registered: %r (known: %s)" % (law, ", ".join(LAWS)))
    gain, decay = par.get("gain"), par.get("decay")
    if not isinstance(gain, (int, float)) or isinstance(gain, bool) or not 0 <= gain <= 1:
        errs.append("gain must be a number in 0..1")
    if not isinstance(decay, (int, float)) or isinstance(decay, bool) or not 0 < decay < 1:
        errs.append("decay must be a number in (0, 1)")
    if par.get("geometry") not in GEOMETRIES:
        errs.append("geometry must be one of %s" % (GEOMETRIES,))
    contract = plan.get("causal_contract")
    if law in LAWS and contract is not None and {k: contract.get(k) for k in ("input", "output", "edge")} != LAWS[law]:
        errs.append("causal_contract does not match the typed ports of law %s" % law)
    return errs


def simulate(plan, frames=32, n=120):
    """Run arm A (edge on) and arm B (edge off) from identical inputs. Returns (histA, histB, metrics)."""
    errs = validate_plan(plan)
    if errs:
        raise ValueError("; ".join(errs))
    if not 8 <= frames <= 120 or not 16 <= n <= 300:
        raise ValueError("simulation outside safe bounds (frames 8..120, n 16..300)")
    law = plan["law"]
    gain = plan["parameters"]["gain"]
    decay = plan["parameters"]["decay"]
    geom = plan["parameters"]["geometry"]
    lit = max(1, int(frames * .36))
    histories = [[], []]
    fields = [ScalarField(), ScalarField()]
    states = [initial(geom, n), initial(geom, n)]
    metrics = []
    for t in range(frames):
        for side in range(2):
            enabled = (side == 0)
            field = fields[side]
            points = states[side]
            field.advance(t, lit, decay)
            # self_imprinting: ONLY the particle -> field write differs; both arms keep field -> motion.
            if law == "self_imprinting" and enabled:
                field.imprint(points)
            new = []
            for p in points:
                x, y = p.x, p.y
                vx = -.31 * y + .07 * math.sin(t * .14)
                vy = .31 * x + .07 * math.cos(t * .16)
                gradx, grady = field.grad(x, y)
                if law == "trajectory_memory" and enabled:
                    vx += gain * gradx
                    vy += gain * grady
                if law == "self_imprinting":
                    vx += gain * gradx
                    vy += gain * grady
                if law == "elastic_memory" and enabled:
                    x += .012 * gain * gradx
                    y += .012 * gain * grady
                base = p.material
                if law == "material_memory" and enabled:
                    base = min(1, .55 + .43 * gain * field.sample(x, y))
                new.append(Particle(max(-.97, min(.97, x + .10 * vx)), max(-.97, min(.97, y + .10 * vy)), base))
            states[side] = new
            histories[side].append(new)
        a, b = states
        position = sum(math.hypot(p.x - q.x, p.y - q.y) for p, q in zip(a, b)) / n
        material = sum(abs(p.material - q.material) for p, q in zip(a, b)) / n
        metrics.append({"frame": t, "pos": position, "material": material})
    final = metrics[-1]
    post = metrics[lit:]
    result = {"law": law, "coupling_edge": LAWS[law]["edge"], "frames": frames, "light_off_frame": lit,
              "same_exogenous_light": True, "same_initial_positions": True, "only_one_channel_disabled": True,
              "final_pos_difference": round(final["pos"], 9),
              "final_material_difference": round(final["material"], 9),
              "mean_post_light_effect": round(sum(x["pos"] + x["material"] for x in post) / len(post), 9),
              "effect_detected": (final["pos"] + final["material"]) > 1e-7,
              "metric": "mean particle position displacement + absolute normalized material difference"}
    return histories[0], histories[1], result


def _spearman(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def experiment(plan, frames=32, n=120, dose=DOSE):
    """A/B run plus a dose sweep of the coupling gain. Verdict follows the repo's evidence rules."""
    _, _, main = simulate(plan, frames, n)
    sweep = []
    for f in dose:
        p = json.loads(json.dumps(plan))
        p["parameters"]["gain"] = plan["parameters"]["gain"] * f
        sweep.append({"factor": f, "gain": round(p["parameters"]["gain"], 9),
                      "mean_post_light_effect": simulate(p, frames, n)[2]["mean_post_light_effect"]})
    effects = [s["mean_post_light_effect"] for s in sweep]
    rho = _spearman(list(dose), effects)
    checks = {"effect_at_full_gain": main["effect_detected"] and main["mean_post_light_effect"] > 0,
              "zero_gain_zero_effect": effects[0] == 0.0,
              "dose_monotonic": rho > 0.9}
    return {"schema": "kosif.matrices.law-experiment.v1", "engine": VERSION, "recipe_id": plan.get("id"),
            "recipe_sha256": digest(plan), "law": plan["law"], "contract": LAWS[plan["law"]],
            "metrics": main, "dose": sweep, "dose_spearman_rho": round(rho, 6), "checks": checks,
            "verdict": "CONFIRMED_IN_MODEL" if all(checks.values()) else "NOT_CONFIRMED",
            "status": "NUMERIC_TESTED",
            "limits": ["causal claim holds inside this toy particle model only",
                       "no visual or human review yet; a numeric pass is not a visual pass",
                       "the 197 mechanism atoms are concepts, not executors"]}


def frame_svg(history, frame, law, enabled):
    p = history[frame]
    title = "KOSIF · %s · %s" % (law, "A: COUPLED" if enabled else "B: CONTROL")
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 740" width="740" height="740">',
           '<rect width="740" height="740" fill="#091525"/>',
           '<text x="36" y="48" fill="#f0f5ff" font-size="19" font-family="sans-serif">%s</text>' % html.escape(title),
           '<text x="36" y="72" fill="#a6bed4" font-size="12" font-family="monospace">FRAME %02d/%02d</text>' % (frame + 1, len(history)),
           '<rect x="25" y="94" width="690" height="604" rx="9" fill="none" stroke="#2c5668"/>']
    for i, particle in enumerate(p):
        past = history[max(0, frame - 7):frame + 1]
        trail = " ".join("%.2f,%.2f" % (370 + s[i].x * 302, 397 + s[i].y * 259) for s in past)
        out.append('<polyline points="%s" fill="none" stroke="#56c8d0" stroke-width="1" opacity=".26"/>' % trail)
        m = particle.material
        out.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" opacity="%.3f"/>' % (
            370 + 302 * particle.x, 397 + 259 * particle.y, 1.3 + 3 * m, "#efd4a0" if i % 7 == 0 else "#8aecf1", max(.1, min(1, m))))
    out.append("</svg>")
    return "\n".join(out)


def render(plan, dest, frames=32, n=120):
    """Write A/B SVG frame folders, plan.json, report.json with per-file sha256. Local output only."""
    dest = Path(dest)
    a, b, _ = simulate(plan, frames, n)
    rep = experiment(plan, frames, n)
    files = {}
    for label, hist, flag in (("a_coupled", a, True), ("b_control", b, False)):
        folder = dest / label
        folder.mkdir(parents=True, exist_ok=True)
        files[label] = {}
        for k in range(len(hist)):
            data = frame_svg(hist, k, plan["law"], flag)
            (folder / ("%03d.svg" % k)).write_text(data, encoding="utf8")
            files[label]["%03d.svg" % k] = hashlib.sha256(data.encode("utf8")).hexdigest()
    rep["files_sha256"] = files
    rep["status"] = "RENDER_TESTED_PENDING_REVIEW"
    (dest / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf8")
    (dest / "report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf8")
    return rep


def verify_render(report_path):
    report_path = Path(report_path)
    rep = json.loads(report_path.read_text(encoding="utf8"))
    base = report_path.parent
    if digest(json.loads((base / "plan.json").read_text(encoding="utf8"))) != rep.get("recipe_sha256"):
        return False
    files = rep.get("files_sha256") or {}
    if not files:
        return False
    for folder, entries in files.items():
        for name, sha in entries.items():
            f = base / folder / name
            if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != sha:
                return False
    return True


def load_plan(path):
    doc = json.loads(Path(path).read_text(encoding="utf8"))
    return doc["recipes"][0] if "recipes" in doc else doc


def atoms():
    return json.loads(ATOMS.read_text(encoding="utf8"))["atoms"]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    p = sub.add_parser("run"); p.add_argument("recipe"); p.add_argument("--frames", type=int, default=32); p.add_argument("--n", type=int, default=120)
    p.add_argument("--render", metavar="DIR", help="also write A/B SVG frames + report.json here (keep out of git)")
    p = sub.add_parser("verify"); p.add_argument("report")
    p = sub.add_parser("atoms"); p.add_argument("--axis")
    a = ap.parse_args(argv)
    if a.cmd == "list":
        out = {"laws": LAWS, "recipes": sorted(str(x.relative_to(SKILL)) for x in RECIPES.glob("*.json"))}
    elif a.cmd == "run":
        plan = load_plan(a.recipe)
        try:
            out = render(plan, a.render, a.frames, a.n) if a.render else experiment(plan, a.frames, a.n)
        except ValueError as e:
            out = {"error": str(e)}
            print(json.dumps(out, ensure_ascii=False, indent=1))
            return 2
        if a.render:
            out = {k: v for k, v in out.items() if k != "files_sha256"}
            out["report"] = str(Path(a.render) / "report.json")
    elif a.cmd == "verify":
        ok = verify_render(a.report)
        out = {"verified": ok}
        print(json.dumps(out))
        return 0 if ok else 1
    else:
        rows = atoms()
        out = [r for r in rows if r["axis"] == a.axis] if a.axis else {"count": len(rows), "axes": sorted({r["axis"] for r in rows})}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
