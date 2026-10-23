#!/usr/bin/env python3
"""Lesson integrity checks: cited numbers, placeholder rendering, conservation ledgers, gauge scales, sound sprites.

Every number a lesson, explainer or infographic shows should come from one registry entry that names
its source and quotes the sentence that supports it, or says plainly that it is a gap. The text then
refers to numbers by id ({v:id}, {v:id|2}, {n:id}) so that a missing value or an unknown unit stops the
build instead of printing a guess. Methods restated in our own words from a study of the public
every-joule-lesson1 build (no licence: nothing copied); see references/lesson-integrity-methods.md.

Stdlib only. Read-only except `render --out`. Runs nothing it reads.

  values   --registry values.json               check every entry (source+quote or gap, range, derived sums)
  render   --registry values.json --content f   fill placeholders, fail closed; --strict flags bare numbers
  ledger   --file ledger.json                   energy (or any quantity) in = out within tolerance, with shares
  scale    VALUE [--headroom 0.9]               smallest 1-2-5 x 10^n gauge capacity that holds the value
  sprite   --manifest sounds.json [--credits CREDITS.md] [--duration S]   sound sprite regions and licences
  --self-test                                   run the built-in checks on synthetic data
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

SCHEMA = "kosif.lesson-integrity.v1"

# Print forms for units; a value whose unit is not here cannot be rendered with its unit.
UNIT_PRINT = {
    "J": " J", "kJ": " kJ", "MJ": " MJ", "kWh": " kWh", "W": " W", "kW": " kW",
    "m": " m", "cm": " cm", "mm": " mm", "km": " km", "kg": " kg", "g": " g",
    "s": " s", "min": " min", "h": " h", "m/s": " m/s", "N": " N", "N/m": " N/m",
    "°C": " °C", "K": " K", "J/(kg °C)": " J/(kg °C)", "W/(m^2 K)": " W/(m² K)",
    "%": "%", "": "",
}
SPRITE_LICENCES = {"CC0 1.0", "CC0", "CC-BY 4.0", "CC BY 4.0", "owner", "original"}
PLACEHOLDER = re.compile(r"\{(v|n):([A-Za-z0-9_]+)(?:\|(\d))?\}")
BARE_NUMBER = re.compile(r"(?<![\w{|.])\d+(?:[.,]\d+)?\s?(?:%|°C|kWh|kJ|MJ|J|kW|W|kg|g|km|cm|mm|m/s|m|s)\b")


def fmt_number(value, dp=None):
    if dp is not None:
        return f"{value:.{dp}f}"
    if float(value).is_integer():
        return f"{int(value):,}"
    return f"{float(f'{value:.3g}'):g}"


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def number_in_quote(value, quote):
    """True when the quote contains the value as printed (1210, 1,210, 0.75, 75%...)."""
    text = quote.replace(" ", "").replace(" ", " ")
    forms = {fmt_number(value), str(value), f"{value:g}"}
    if float(value).is_integer():
        forms.add(str(int(value)))
    if 0 < value < 1:
        forms.add(f"{value * 100:g}")
    found = [float(m.replace(",", "")) for m in re.findall(r"\d[\d,]*(?:\.\d+)?", text)]
    return any(f in text for f in forms) or any(math.isclose(f, value, rel_tol=1e-9) or
                                                (0 < value < 1 and math.isclose(f, value * 100, rel_tol=1e-9))
                                                for f in found)


def check_values(reg):
    """Return (errors, warnings, summary) for a registry {"sources": {...}, "values": {...}}."""
    errors, warnings = [], []
    sources = reg.get("sources", {})
    values = reg.get("values", {})
    for sid, src in sources.items():
        if not src.get("title") or not (src.get("url") or src.get("citation")):
            errors.append(f"source '{sid}': needs a title and a url or citation")
    counts = {"sourced": 0, "gap": 0, "derived": 0}
    for vid, v in values.items():
        where = f"value '{vid}'"
        if not isinstance(v.get("value"), (int, float)) or isinstance(v.get("value"), bool):
            if "gap" in v and v.get("value") is None:
                counts["gap"] += 1
                continue
            errors.append(f"{where}: value must be a number (or null with a gap note)")
            continue
        if "unit" not in v:
            errors.append(f"{where}: no unit (use \"\" for a pure number)")
        if not v.get("what"):
            errors.append(f"{where}: says nothing about what it measures ('what')")
        rng = v.get("range")
        if rng is not None and not (len(rng) == 2 and rng[0] <= v["value"] <= rng[1]):
            errors.append(f"{where}: {v['value']} lies outside its range {rng}")
        if "derived" in v:
            counts["derived"] += 1
            d = v["derived"]
            op, parts = d.get("op"), d.get("of", [])
            missing = [p for p in parts if not isinstance(values.get(p, {}).get("value"), (int, float))]
            if missing or op not in ("sum", "product", "difference", "ratio"):
                errors.append(f"{where}: derived {op} of unknown or unset values {missing or parts}")
                continue
            nums = [values[p]["value"] for p in parts]
            want = {"sum": sum(nums), "product": math.prod(nums),
                    "difference": nums[0] - sum(nums[1:]),
                    "ratio": nums[0] / nums[1] if len(nums) == 2 and nums[1] else float("nan")}[op]
            tol = d.get("tolerance", 1e-9)
            if not math.isclose(v["value"], want, rel_tol=tol, abs_tol=tol):
                errors.append(f"{where}: says {v['value']} but the {op} of {parts} is {want:g}")
            continue
        src = v.get("source")
        if src:
            counts["sourced"] += 1
            if src.get("ref") not in sources:
                errors.append(f"{where}: source ref '{src.get('ref')}' is not in sources")
            quote = src.get("quote", "")
            if not quote:
                errors.append(f"{where}: cites a source but quotes no supporting sentence")
            elif not number_in_quote(v["value"], quote) and not v.get("note"):
                warnings.append(f"{where}: {v['value']} does not appear in its quote; add a note saying how it follows")
        elif v.get("gap"):
            counts["gap"] += 1
            warnings.append(f"{where}: shown with no source (gap: {v['gap']})")
        else:
            errors.append(f"{where}: no source and no gap note; a number nobody can trace must not be shown")
    summary = {"sources": len(sources), "values": len(values), **counts}
    return errors, warnings, summary


def render(reg, text, strict=False):
    """Fill {v:id}, {v:id|dp} (with unit) and {n:id} (number only). Returns (text, errors)."""
    values = reg.get("values", {})
    errors = []

    def sub(m):
        kind, vid, dp = m.group(1), m.group(2), m.group(3)
        v = values.get(vid)
        if v is None or v.get("value") is None:
            errors.append(f"no value '{vid}' in the registry" if v is None else f"value '{vid}' is a gap and cannot be shown")
            return m.group(0)
        dp = int(dp) if dp is not None else None
        unit = v.get("unit", "")
        if unit == "fraction":
            return fmt_number(v["value"] * 100, dp) + "%"
        num = fmt_number(v["value"], dp)
        if kind == "n":
            return num
        if unit not in UNIT_PRINT:
            errors.append(f"no print form for unit '{unit}' (value '{vid}')")
            return m.group(0)
        return num + UNIT_PRINT[unit]

    out = PLACEHOLDER.sub(sub, text)
    if strict:
        for line_no, line in enumerate(text.splitlines(), 1):
            for m in BARE_NUMBER.finditer(PLACEHOLDER.sub("", line)):
                errors.append(f"line {line_no}: bare number '{m.group(0)}' is not taken from the registry")
    return out, errors


def check_ledger(led):
    """A conservation ledger: {"quantity","unit","in":{store:amount},"out":{store:amount},"tolerance"}."""
    unit = led.get("unit", "")
    total_in = sum(led.get("in", {}).values())
    total_out = sum(led.get("out", {}).values())
    tol = led.get("tolerance", 1e-6 * max(abs(total_in), 1))
    errors = []
    if total_in <= 0:
        errors.append("nothing goes in: the ledger needs at least one positive starting amount")
    for side in ("in", "out"):
        for store, amount in led.get(side, {}).items():
            if amount < 0:
                errors.append(f"{side} '{store}' is negative ({amount}); record a transfer on the other side instead")
    gap = total_in - total_out
    if abs(gap) > tol:
        errors.append(f"{abs(gap):g} {unit} {'unaccounted for' if gap > 0 else 'appeared from nowhere'} "
                      f"(in {total_in:g}, out {total_out:g}, tolerance {tol:g})")
    shares = {k: (a / total_in if total_in else 0.0) for k, a in led.get("out", {}).items()}
    useful = [k for k in led.get("useful", []) if k in shares]
    report = {"quantity": led.get("quantity", "energy"), "unit": unit, "in": total_in, "out": total_out,
              "gap": gap, "shares": shares}
    if useful:
        report["efficiency"] = sum(shares[k] for k in useful)
    return errors, report


def nice_scale(value, headroom=0.9):
    """Smallest capacity from 1, 2, 5 x 10^n so that value fills at most `headroom` of it."""
    if not (value > 0 and math.isfinite(value)):
        raise ValueError("value must be a positive finite number")
    if not 0 < headroom <= 1:
        raise ValueError("headroom must be in (0, 1]")
    need = value / headroom
    exp = math.floor(math.log10(need))
    for e in (exp, exp + 1):
        for step in (1, 2, 5):
            cap = step * 10 ** e
            if cap >= need * (1 - 1e-12):
                return {"value": value, "capacity": cap, "fill": value / cap, "headroom": headroom}
    raise AssertionError("unreachable")


def check_sprite(manifest, credits_text=None, duration=None):
    """Regions must not overlap, must fit the file, and every cue must be credited with an allowed licence."""
    errors, regions = [], []
    for cue, spec in manifest.get("sounds", {}).items():
        spans = list(spec.get("variants", []))
        for layer in (spec.get("layers") or {}).values():
            spans.extend(layer if layer and isinstance(layer[0], list) else [layer])
        if not spans:
            errors.append(f"cue '{cue}' has no regions")
        for start, length in spans:
            if length <= 0 or start < 0:
                errors.append(f"cue '{cue}': bad region [{start}, {length}]")
            regions.append((start, start + length, cue))
    regions.sort()
    for (a0, a1, ca), (b0, b1, cb) in zip(regions, regions[1:]):
        if b0 < a1 - 1e-6:
            errors.append(f"regions overlap: '{ca}' ends at {a1:g}s after '{cb}' starts at {b0:g}s")
    if duration is not None and regions and max(r[1] for r in regions) > duration + 1e-6:
        errors.append(f"a region ends at {max(r[1] for r in regions):g}s, past the file's {duration:g}s")
    credited = {}
    if credits_text is not None:
        for line in credits_text.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or set(cells[0]) <= set("-: "):
                continue
            cues = re.findall(r"`([^`]+)`", cells[0])
            for c in cues:
                credited[c] = cells[-1]
        for cue in manifest.get("sounds", {}):
            if cue not in credited:
                errors.append(f"cue '{cue}' has no row in the credits table")
            elif credited[cue] not in SPRITE_LICENCES:
                errors.append(f"cue '{cue}' is credited under '{credited[cue]}', which is not on the allowed list")
    return errors, {"cues": len(manifest.get("sounds", {})), "regions": len(regions),
                    "end": max((r[1] for r in regions), default=0.0), "credited": len(credited)}


def emit(args, payload, errors, warnings=()):
    payload = {"schema": SCHEMA, "ok": not errors, "errors": list(errors), "warnings": list(warnings), **payload}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for e in errors:
            print(f"ERROR {e}")
        for w in warnings:
            print(f"WARN  {w}")
        rest = {k: v for k, v in payload.items() if k not in ("schema", "errors", "warnings", "text")}
        print(json.dumps(rest, ensure_ascii=False))
    return 0 if not errors else 1


def self_test():
    reg = {"sources": {"spec": {"title": "Exam specification", "url": "https://example.org/spec.pdf"}},
           "values": {
               "g": {"value": 9.8, "unit": "N/kg", "what": "gravitational field strength",
                     "source": {"ref": "spec", "quote": "take g as 9.8 N/kg"}},
               "heater": {"value": 30, "unit": "W", "range": [30, 110], "what": "practical heater",
                          "source": {"ref": "spec", "quote": "heaters from 30 W to 110 W"}},
               "a": {"value": 2, "unit": "J", "what": "a", "gap": "teacher estimate"},
               "b": {"value": 3, "unit": "J", "what": "b", "gap": "teacher estimate"},
               "ab": {"value": 5, "unit": "J", "what": "a+b", "derived": {"op": "sum", "of": ["a", "b"]}}}}
    errs, warns, summary = check_values(reg)
    assert not errs and summary["derived"] == 1 and len(warns) == 2, (errs, warns)
    reg["values"]["ab"]["value"] = 6
    assert any("sum" in e for e in check_values(reg)[0])
    text, errs = render(reg, "{v:heater} heater, {n:g} and {v:nope}")
    assert text.startswith("30 W heater, 9.8") and errs == ["no value 'nope' in the registry"], (text, errs)
    assert render(reg, "{v:g}")[1] == ["no print form for unit 'N/kg' (value 'g')"]
    assert render(reg, "it fell 2 m", strict=True)[1]
    led_errs, rep = check_ledger({"unit": "J", "in": {"gravitational": 10}, "out": {"kinetic": 7, "thermal": 2.5}})
    assert led_errs and rep["gap"] == 0.5
    assert nice_scale(4.4)["capacity"] == 5 and nice_scale(4.6)["capacity"] == 10 and nice_scale(170)["capacity"] == 200
    sp = {"sounds": {"turn": {"variants": [[0.05, 0.6], [0.7, 0.4]]}, "thud": {"variants": [[1.2, 0.3]]}}}
    errs, info = check_sprite(sp, "| Cue | Used | Source | Licence |\n|---|---|---|---|\n| `turn` | x | y | CC0 1.0 |\n", 2.0)
    assert errs == ["cue 'thud' has no row in the credits table"] and info["regions"] == 3, errs
    sp["sounds"]["thud"]["variants"] = [[0.6, 0.3]]
    assert any("overlap" in e for e in check_sprite(sp)[0])
    print("lesson_integrity self-test: 11 checks passed")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--self-test", action="store_true", help="run the built-in checks and exit")
    sub = p.add_subparsers(dest="cmd")
    v = sub.add_parser("values", help="check every registry entry")
    v.add_argument("--registry", required=True)
    r = sub.add_parser("render", help="fill {v:id}/{n:id} placeholders, failing on unknown values or units")
    r.add_argument("--registry", required=True)
    r.add_argument("--content", required=True)
    r.add_argument("--out", help="write the rendered text here (nothing is written on error)")
    r.add_argument("--strict", action="store_true", help="also flag numbers with units typed into the text")
    led = sub.add_parser("ledger", help="check that a conservation ledger balances")
    led.add_argument("--file", required=True)
    s = sub.add_parser("scale", help="1-2-5 gauge capacity for a value")
    s.add_argument("value", type=float)
    s.add_argument("--headroom", type=float, default=0.9)
    sp = sub.add_parser("sprite", help="check a sound sprite manifest and its credits")
    sp.add_argument("--manifest", required=True)
    sp.add_argument("--credits")
    sp.add_argument("--duration", type=float, help="length of the sprite file in seconds")
    for q in (v, r, led, s, sp):
        q.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return self_test()
    if args.cmd == "values":
        errs, warns, summary = check_values(load_json(args.registry))
        return emit(args, summary, errs, warns)
    if args.cmd == "render":
        text, errs = render(load_json(args.registry), Path(args.content).read_text(encoding="utf-8"), args.strict)
        if not errs:
            if args.out:
                Path(args.out).write_text(text, encoding="utf-8")
            elif not args.json:
                sys.stdout.write(text if text.endswith("\n") else text + "\n")
        return emit(args, {"text": text} if args.json and not errs else {"written": args.out}, errs)
    if args.cmd == "ledger":
        errs, report = check_ledger(load_json(args.file))
        return emit(args, report, errs)
    if args.cmd == "scale":
        try:
            return emit(args, nice_scale(args.value, args.headroom), [])
        except ValueError as e:
            return emit(args, {}, [str(e)])
    if args.cmd == "sprite":
        credits = Path(args.credits).read_text(encoding="utf-8") if args.credits else None
        errs, info = check_sprite(load_json(args.manifest), credits, args.duration)
        return emit(args, info, errs)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
