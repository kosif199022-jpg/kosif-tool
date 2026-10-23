#!/usr/bin/env python3
"""KOSIF brand tokens — SVG palette extraction, 3-tier design tokens and a WCAG 2.x contrast matrix.

رموز الهوية: استخراج ألوان الشعار وبناء رموز بثلاث طبقات ومصفوفة تباين WCAG — Brand palette, tokens and contrast.

Commands (JSON on stdout; FILE may be "-" for stdin)
  palette FILE.svg
        every colour used in fill / stroke / stop-color / flood-color / lighting-color / color (attributes,
        style="" and <style> CSS), normalised to lowercase #rrggbb (alpha reported apart), with use counts,
        share and roles; none/transparent/currentColor/url(#…) are skipped; unknown values are listed.
        e.g. python3 scripts/brand_tokens.py palette logo.svg
  tokens PALETTE.json [--css]
        3-tier tokens in DTCG shape ($value/$type): core (100–900 scale per colour, mixed with white/black in
        sRGB), semantic (aliases such as {core.color.primary.600}, chosen so white text on the action colour,
        and muted/link text on the subtle background, pass AA), component (button/card/link/input aliases to semantic). Also a resolved map and CSS custom
        properties. PALETTE.json is the palette output, a {"name": "#hex"} map (or {"colors": {...}}), or a
        list of hex strings. --css prints only the CSS.
        e.g. python3 scripts/brand_tokens.py tokens palette.json --css
  contrast TOKENS.json
        WCAG 2.x contrast ratio for text/background pairs (names with text/fg/on-/link/icon versus
        bg/background/surface/action), with AA (4.5, large 3) and AAA (7, large 4.5) verdicts. Intended pairs
        first: siblings (button.primary.text on button.primary.bg), semantic text.* on bg.* and text.on-action
        on action.*; else every text x background pair; when no names say which is which, every pair of
        distinct colours. Accepts the tokens output or a flat name -> hex map.
        e.g. python3 scripts/brand_tokens.py contrast tokens.json
  --self-test   runs a small offline check and exits 0.

Never uses the network and never writes files. Bad input: exit 2 with one line on stderr.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import re
import sys
from pathlib import Path

NAMED = {  # CSS named colours most often found in exported SVGs (CSS Level 2 + common Level 3)
    "black": "#000000", "silver": "#c0c0c0", "gray": "#808080", "grey": "#808080", "white": "#ffffff",
    "maroon": "#800000", "red": "#ff0000", "purple": "#800080", "fuchsia": "#ff00ff", "magenta": "#ff00ff",
    "green": "#008000", "lime": "#00ff00", "olive": "#808000", "yellow": "#ffff00", "navy": "#000080",
    "blue": "#0000ff", "teal": "#008080", "aqua": "#00ffff", "cyan": "#00ffff", "orange": "#ffa500",
    "gold": "#ffd700", "pink": "#ffc0cb", "brown": "#a52a2a", "beige": "#f5f5dc", "ivory": "#fffff0",
    "indigo": "#4b0082", "violet": "#ee82ee", "crimson": "#dc143c", "coral": "#ff7f50", "salmon": "#fa8072",
    "tomato": "#ff6347", "khaki": "#f0e68c", "turquoise": "#40e0d0", "skyblue": "#87ceeb", "steelblue": "#4682b4",
    "royalblue": "#4169e1", "darkblue": "#00008b", "darkgreen": "#006400", "darkred": "#8b0000",
    "lightgray": "#d3d3d3", "lightgrey": "#d3d3d3", "darkgray": "#a9a9a9", "darkgrey": "#a9a9a9",
    "dimgray": "#696969", "dimgrey": "#696969", "gainsboro": "#dcdcdc", "whitesmoke": "#f5f5f5",
    "slategray": "#708090", "slategrey": "#708090", "orangered": "#ff4500", "chocolate": "#d2691e",
    "tan": "#d2b48c", "goldenrod": "#daa520", "seagreen": "#2e8b57", "forestgreen": "#228b22",
    "limegreen": "#32cd32", "hotpink": "#ff69b4", "deeppink": "#ff1493", "plum": "#dda0dd", "lavender": "#e6e6fa",
}
SKIP = {"none", "transparent", "currentcolor", "inherit", "initial", "unset", "context-fill", "context-stroke"}
_PROP = re.compile(r"(?i)(?<![\w-])(fill|stroke|stop-color|flood-color|lighting-color|color)\s*(?:=\s*[\"']|:\s*)([^\"';}<>]+)")
_HEX = re.compile(r"#([0-9a-fA-F]{3,8})")
_FUNC = re.compile(r"(?i)(rgba?|hsla?)\(\s*([^)]*)\)")
STEPS = {100: ("w", .80), 200: ("w", .60), 300: ("w", .40), 400: ("w", .20), 500: (None, 0),
         600: ("k", .20), 700: ("k", .40), 800: ("k", .60), 900: ("k", .80)}
ROLE_NAMES = ["primary", "secondary", "accent"]
FG_HINT = ("text", "fg", "foreground", "on-", "link", "icon")
BG_HINT = ("bg", "background", "surface", "action", "fill")


class Bad(ValueError):
    pass


def _read(path) -> str:
    if path == "-":
        return sys.stdin.read().lstrip("\ufeff")
    p = Path(path)
    if not p.is_file():
        raise Bad(f"file not found: {path}")
    return p.read_text(encoding="utf-8-sig")


def _h(x):
    return int(math.floor(x + 0.5))


def to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, _h(c))):02x}" for c in rgb)


def from_hex(h):
    h = h.strip().lower()
    m = re.fullmatch(r"#?([0-9a-f]{3}|[0-9a-f]{6})", h)
    if not m:
        raise Bad(f"not a #rgb/#rrggbb colour: {h!r}")
    s = m.group(1)
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def _num(tok, scale):
    tok = tok.strip()
    if tok.endswith("%"):
        return float(tok[:-1]) * scale / 100
    return float(tok)


def parse_color(value):
    """(hex, alpha) or None to skip; raises Bad for an unknown value."""
    v = value.strip().strip("\"'").strip()
    lv = v.lower()
    if not lv or lv in SKIP or lv.startswith("url(") or lv.startswith("var("):
        return None
    m = _HEX.fullmatch(v)
    if m:
        s = m.group(1).lower()
        if len(s) in (3, 4):
            s = "".join(c * 2 for c in s)
        if len(s) not in (6, 8):
            raise Bad(v)
        a = int(s[6:8], 16) / 255 if len(s) == 8 else 1.0
        return "#" + s[:6], round(a, 3)
    m = _FUNC.fullmatch(v)
    if m:
        kind, args = m.group(1).lower(), m.group(2)
        parts = [p for p in re.split(r"[\s,/]+", args.strip()) if p]
        if len(parts) not in (3, 4):
            raise Bad(v)
        a = _num(parts[3], 1) if len(parts) == 4 else 1.0
        if kind.startswith("rgb"):
            rgb = [_num(p, 255) for p in parts[:3]]
        else:
            hue = float(parts[0].rstrip("deg")) % 360 / 360
            s, l = _num(parts[1], 1) / (100 if not parts[1].endswith("%") else 1), _num(parts[2], 1) / (100 if not parts[2].endswith("%") else 1)
            rgb = [c * 255 for c in colorsys.hls_to_rgb(hue, l, s)]
        return to_hex(rgb), round(max(0.0, min(1.0, a)), 3)
    if lv in NAMED:
        return NAMED[lv], 1.0
    raise Bad(v)


def palette(path):
    text = _read(path)
    if "<svg" not in text:
        raise Bad(f"{path} is not an SVG (no <svg> element)")
    found, unparsed, total = {}, [], 0
    for m in _PROP.finditer(text):
        prop, val = m.group(1).lower(), m.group(2).split("!")[0].strip()
        try:
            c = parse_color(val)
        except (Bad, ValueError):
            if val not in unparsed:
                unparsed.append(val)
            continue
        if c is None:
            continue
        hx, a = c
        e = found.setdefault(hx, {"hex": hx, "count": 0, "roles": {}, "alpha_values": []})
        e["count"] += 1
        e["roles"][prop] = e["roles"].get(prop, 0) + 1
        if a < 1 and a not in e["alpha_values"]:
            e["alpha_values"].append(a)
        total += 1
    colors = sorted(found.values(), key=lambda e: (-e["count"], e["hex"]))
    for e in colors:
        e["share"] = round(e["count"] / total, 4)
        e["roles"] = dict(sorted(e["roles"].items()))
        e["alpha_values"].sort()
        r, g, b = from_hex(e["hex"])
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        e["hsl"] = [round(h * 360, 1), round(s, 3), round(l, 3)]
    return {"file": str(path), "distinct": len(colors), "total_uses": total, "colors": colors, "unparsed": unparsed,
            "note": "Elements with no fill paint black by SVG default; those implicit uses are not counted."}


def _mix(rgb, target, t):
    return tuple(c * (1 - t) + target * t for c in rgb)


def scale(hx):
    rgb = from_hex(hx)
    out = {}
    for step, (to, t) in STEPS.items():
        out[str(step)] = to_hex(rgb if to is None else _mix(rgb, 255 if to == "w" else 0, t))
    return out


def luminance(hx):
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = from_hex(hx)
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _sat_light(hx):
    r, g, b = from_hex(hx)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return s, l


def _load_palette(path):
    d = json.loads(_read(path))
    named, unnamed = {}, []
    src = d.get("colors", d) if isinstance(d, dict) else d
    if isinstance(src, dict):
        for k, v in src.items():
            if not re.fullmatch(r"[a-z][a-z0-9-]*", str(k)):
                raise Bad(f"colour name {k!r} must be lowercase kebab-case")
            named[k] = to_hex(from_hex(v if isinstance(v, str) else v.get("hex", "")))
    elif isinstance(src, list):
        for v in src:
            unnamed.append(to_hex(from_hex(v if isinstance(v, str) else v.get("hex", ""))))
    else:
        raise Bad("palette JSON must be a palette output, a name->hex map or a list of hex strings")
    if not named and not unnamed:
        raise Bad("the palette holds no colours")
    return named, unnamed


def tokens(path):
    named, unnamed = _load_palette(path)
    synthesized = False
    seen = set(named.values())
    pool = [h for h in dict.fromkeys(unnamed) if h not in seen]
    if "neutral" not in named:
        cands = [h for h in pool if _sat_light(h)[0] < 0.15 and 0.2 <= _sat_light(h)[1] <= 0.8]
        if cands:
            named["neutral"] = min(cands, key=lambda h: (_sat_light(h)[0], pool.index(h)))
            pool.remove(named["neutral"])
        else:
            named["neutral"] = "#737373"
            synthesized = True
    # brand colours: skip near-white/near-black/greys from an unnamed palette; they live in core white/black/neutral
    brand = [h for h in pool if not (_sat_light(h)[0] < 0.15 or _sat_light(h)[1] > 0.95 or _sat_light(h)[1] < 0.05)]
    for i, h in enumerate(brand):
        name = ROLE_NAMES[i] if i < len(ROLE_NAMES) else f"accent-{i - 1}"
        while name in named:
            name += "-x"
        named[name] = h
    if "primary" not in named:
        first = next((k for k in named if k != "neutral"), "neutral")
        named["primary"] = named[first]
    core = {"white": "#ffffff", "black": "#000000"}
    for name in sorted(named):
        for step, hx in scale(named[name]).items():
            core[f"{name}.{step}"] = hx

    def first_aa(name, start=500, on="#ffffff"):
        for st in range(start, 1000, 100):
            if ratio(core[f"{name}.{st}"], on) >= 4.5:
                return st
        return 900

    sem = {"bg.default": "white", "bg.subtle": "neutral.100", "text.default": "neutral.900",
           "text.muted": f"neutral.{first_aa('neutral', 500, core['neutral.100'])}", "border.default": "neutral.300",
           "text.on-action": "white"}
    for role in ("primary", "secondary"):
        if role in named:
            st = first_aa(role)
            sem[f"action.{role}"] = f"{role}.{st}"
            sem[f"action.{role}-hover"] = f"{role}.{min(900, st + 100)}"
    sem["text.link"] = f"primary.{first_aa('primary', 500, core['neutral.100'])}"  # readable on bg.default and bg.subtle
    if "accent" in named:
        sem["accent.default"] = "accent.500"
    comp = {"button.primary.bg": "action.primary", "button.primary.bg-hover": "action.primary-hover",
            "button.primary.text": "text.on-action", "card.bg": "bg.default", "card.text": "text.default",
            "card.border": "border.default", "link.text": "text.link", "input.bg": "bg.default",
            "input.text": "text.default", "input.border": "border.default"}
    if "action.secondary" in sem:
        comp.update({"button.secondary.bg": "action.secondary", "button.secondary.bg-hover": "action.secondary-hover",
                     "button.secondary.text": "text.on-action"})

    def nest(flat, ref=None):
        out = {}
        for k, v in flat.items():
            node = out
            parts = k.split(".")
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = {"$value": v if ref is None else "{" + f"{ref}.{v}" + "}", "$type": "color"}
        return out

    resolved = {f"core.color.{k}": v for k, v in core.items()}
    resolved.update({f"semantic.color.{k}": core[v] for k, v in sem.items()})
    resolved.update({f"component.{k}": core[sem[v]] for k, v in comp.items()})
    css = [":root {"]
    css += [f"  --core-color-{k.replace('.', '-')}: {v};" for k, v in core.items()]
    css += [f"  --color-{k.replace('.', '-')}: var(--core-color-{v.replace('.', '-')});" for k, v in sem.items()]
    css += [f"  --{k.replace('.', '-')}: var(--color-{v.replace('.', '-')});" for k, v in comp.items()]
    css.append("}")
    return {"$schema_note": "DTCG-style tokens: core -> semantic -> component; themes swap the semantic tier only",
            "sources": dict(sorted(named.items())), "neutral_synthesized": synthesized,
            "core": {"color": nest(core)}, "semantic": {"color": nest(sem, "core.color")},
            "component": nest(comp, "semantic.color"), "resolved": resolved, "css": "\n".join(css) + "\n"}


def _flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict) and "$value" in v:
            out[key] = v["$value"]
        elif isinstance(v, dict):
            out.update(_flatten(v, key))
        elif isinstance(v, str):
            out[key] = v
    return out


def _resolve(flat):
    res = {}
    for k in flat:
        v, hops = flat[k], 0
        while isinstance(v, str) and v.startswith("{") and v.endswith("}"):
            v, hops = flat.get(v[1:-1]), hops + 1
            if v is None or hops > 10:
                raise Bad(f"token {k} has an unresolved or circular alias")
        res[k] = v
    return res


def contrast(path):
    d = json.loads(_read(path))
    if not isinstance(d, dict):
        raise Bad("tokens JSON must be an object")
    if isinstance(d.get("resolved"), dict):
        flat = d["resolved"]
    else:
        flat = _resolve(_flatten({k: v for k, v in d.items() if not k.startswith("$")}))
    colors = {}
    for k, v in flat.items():
        if isinstance(v, str) and re.fullmatch(r"#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?", v.strip()):
            colors[k] = to_hex(from_hex(v))
    if len(colors) < 2:
        raise Bad("need at least two #hex colour tokens")
    tail = lambda k: ".".join(k.split(".")[-2:]).lower()  # noqa: E731
    fg = [k for k in colors if any(h in tail(k) for h in FG_HINT) and not k.startswith("core.")]
    bg = [k for k in colors if any(h in tail(k) for h in BG_HINT) and k not in fg and not k.startswith("core.")]
    grp = lambda k: k.rsplit(".", 1)[0]  # noqa: E731

    def intended(f, b):
        if grp(f) == grp(b):  # component.button.primary.text on component.button.primary.bg
            return True
        if ".text." in f and f.startswith("semantic.") and b.startswith("semantic."):
            return (".bg." in b) if not f.endswith("on-action") else (".action." in b)
        return False

    pairs = [(f, b) for f in fg for b in bg if intended(f, b)]
    if pairs:
        mode = "intended-pairs"
    elif fg and bg:
        pairs, mode = [(f, b) for f in fg for b in bg], "text-on-background"
    else:
        ks = sorted(colors)
        pairs, mode = [(a, b) for i, a in enumerate(ks) for b in ks[i + 1:] if colors[a] != colors[b]], "all-pairs"
    rows = []
    for f, b in pairs:
        r = ratio(colors[f], colors[b])
        rows.append({"fg": f, "fg_hex": colors[f], "bg": b, "bg_hex": colors[b], "ratio": round(r, 2),
                     "AA": r >= 4.5, "AA_large": r >= 3, "AAA": r >= 7, "AAA_large": r >= 4.5})
    rows.sort(key=lambda x: (x["ratio"], x["fg"], x["bg"]))
    return {"file": str(path), "mode": mode, "pairs": len(rows), "pass_AA": sum(r["AA"] for r in rows),
            "pass_AAA": sum(r["AAA"] for r in rows), "fail_AA": [f"{r['fg']} on {r['bg']} ({r['ratio']})" for r in rows if not r["AA"]],
            "matrix": rows, "method": "WCAG 2.x relative luminance (sRGB, 0.03928 threshold); verdicts use the unrounded ratio"}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        print(f"BRAND_TOKENS_ERROR: {message}", file=sys.stderr)
        raise SystemExit(2)


def self_test() -> int:
    import tempfile
    assert round(ratio("#000000", "#ffffff"), 2) == 21.0
    assert ratio("#777777", "#ffffff") < 4.5 <= ratio("#767676", "#ffffff")
    assert parse_color("rgb(100%, 0%, 0%)") == ("#ff0000", 1.0) and parse_color("#3366cc80") == ("#3366cc", 0.502)
    assert scale("#3366cc")["100"] == "#d6e0f5"
    with tempfile.TemporaryDirectory() as t:
        pj = Path(t) / "p.json"
        pj.write_text(json.dumps({"primary": "#3366cc"}), encoding="utf-8")
        tk = tokens(pj)
        assert ratio(tk["resolved"]["component.button.primary.bg"], "#ffffff") >= 4.5
        tj = Path(t) / "t.json"
        tj.write_text(json.dumps(tk), encoding="utf-8")
        assert contrast(tj)["mode"] == "intended-pairs" and not contrast(tj)["fail_AA"]
    print("self-test: OK")
    return 0


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = _Parser(prog="brand_tokens.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true", help="run the offline check")
    sub = ap.add_subparsers(dest="cmd", required=True, parser_class=_Parser)
    sub.add_parser("palette").add_argument("file")
    s = sub.add_parser("tokens"); s.add_argument("file"); s.add_argument("--css", action="store_true", help="print only the CSS")
    sub.add_parser("contrast").add_argument("file")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "palette":
            r = palette(a.file)
        elif a.cmd == "tokens":
            r = tokens(a.file)
            if a.css:
                sys.stdout.write(r["css"])
                return 0
        else:
            r = contrast(a.file)
    except (Bad, OSError, UnicodeDecodeError, json.JSONDecodeError, AttributeError, TypeError) as e:
        print(f"BRAND_TOKENS_ERROR: {e}".replace("\n", " "), file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
