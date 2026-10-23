#!/usr/bin/env python3
"""لوح الخرائط: إسقاط الإحداثيات إلى بكسلات، وتصنيف الخرائط الملوّنة بفحص التطبيع، وسجل المصادر والترخيص.
Map plate: project coordinates to pixels, classify choropleth data with a normalization check, and audit a
coordinate/source ledger.

Serves the maps-geo power family: "the projection decides what is distorted, so choose it deliberately",
"a simple projection placing real coordinates on an SVG sheet with a cos(lat) horizontal squash", "fill
regions with rates or shares, never raw counts, with a classed sequential scheme", and "log each layer's
source, licence, date, CRS and whether it is measured or schematic". Python standard library only, offline,
deterministic.

Commands
  project --proj mercator|equirect --size WxH [--bbox W,S,E,N] [--ref-lat DEG] LON,LAT [LON,LAT ...]
      pixel x,y of each point on a WxH plate. The world (or --bbox) is fitted inside the plate with its aspect
      kept and centred. mercator = spherical Web Mercator (lat clamped to +-85.05113, flagged);
      equirect = plate carree, with --ref-lat giving the cos(lat) horizontal squash for local sheets.
      e.g. python3 scripts/geo_plate.py project --proj equirect --size 2000x1000 31.2357,30.0444 -0.1276,51.5072
  classify DATA.csv --value COL [--name COL] --method quantile|equal|jenks --classes K
           [--per-capita POP_COL --scale 100000]
      class breaks (K+1 bounds), each row's class, class counts and goodness of variance fit (GVF);
      warns when raw counts would be mapped without --per-capita.
      e.g. python3 scripts/geo_plate.py classify regions.csv --value cases --per-capita pop --method jenks --classes 5
  ledger POINTS.json
      validates {"crs": "EPSG:4326", "source": ..., "licence": ..., "points": [{"id", "lon", "lat", "source",
      "licence", "date", "kind": "measured|schematic"}]}: coordinate ranges, likely lat/lon swaps, null island,
      duplicate ids, CRS, and source+licence present for every point (ledger-level values are defaults).
      e.g. python3 scripts/geo_plate.py ledger points.json
  --self-test   run a small offline check and exit 0

Output is JSON on stdout. File arguments accept '-' for stdin. Bad input: exit 2 with one line on stderr. Never touches the network.
"""
import argparse
import csv
import io
import json
import math
import re
import sys
from pathlib import Path

MERC_MAX_LAT = 85.05112878
COORD = re.compile(r"^\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*$")


def read_text(path):
    """Read a UTF-8 file, or stdin when path is '-'."""
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8-sig")


class BadInput(ValueError):
    pass


# ---------------------------------------------------------------- project
def _size(text):
    m = re.fullmatch(r"(\d+)[xX](\d+)", str(text).strip())
    if not m or int(m.group(1)) <= 0 or int(m.group(2)) <= 0:
        raise BadInput("--size must be WxH, e.g. 1920x1080")
    return int(m.group(1)), int(m.group(2))


def _parse_ll(text):
    if not COORD.match(text):
        raise BadInput("point must be LON,LAT in decimal degrees: %r" % text)
    lon, lat = (float(v) for v in text.split(","))
    if not -180 <= lon <= 180:
        raise BadInput("longitude out of range [-180, 180]: %s" % text)
    if not -90 <= lat <= 90:
        raise BadInput("latitude out of range [-90, 90]: %s (is it LON,LAT?)" % text)
    return lon, lat


def _unit(proj, lon, lat, ref_lat):
    """Projected unit coordinates (X east, Y north) and whether lat was clamped."""
    lam = math.radians(lon)
    if proj == "mercator":
        c = abs(lat) > MERC_MAX_LAT
        phi = math.radians(max(-MERC_MAX_LAT, min(MERC_MAX_LAT, lat)))
        return lam, math.log(math.tan(math.pi / 4 + phi / 2)), c
    return lam * math.cos(math.radians(ref_lat)), math.radians(lat), False


def project(proj, size, points, bbox=None, ref_lat=0.0):
    if proj not in ("mercator", "equirect"):
        raise BadInput("--proj must be mercator or equirect")
    if not -89 <= ref_lat <= 89:
        raise BadInput("--ref-lat must be between -89 and 89")
    if proj == "mercator" and ref_lat:
        raise BadInput("--ref-lat applies to equirect only")
    w, h = _size(size)
    if not points:
        raise BadInput("give at least one LON,LAT point")
    pts = [_parse_ll(p) for p in points]
    if bbox:
        try:
            west, south, east, north = (float(v) for v in bbox.split(","))
        except ValueError:
            raise BadInput("--bbox must be W,S,E,N")
        if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
            raise BadInput("--bbox needs -180 <= W < E <= 180 and -90 <= S < N <= 90")
    else:
        west, south, east, north = -180.0, -90.0, 180.0, 90.0
    x0, y0, _ = _unit(proj, west, south, ref_lat)
    x1, y1, _ = _unit(proj, east, north, ref_lat)
    dx, dy = x1 - x0, y1 - y0
    scale = min(w / dx, h / dy)
    ox, oy = (w - dx * scale) / 2, (h - dy * scale) / 2
    out = []
    for (lon, lat), raw in zip(pts, points):
        X, Y, clamped = _unit(proj, lon, lat, ref_lat)
        px, py = ox + (X - x0) * scale, oy + (y1 - Y) * scale
        rec = {"lon": lon, "lat": lat, "x": round(px, 3), "y": round(py, 3),
               "inside": bool(-1e-9 <= px <= w + 1e-9 and -1e-9 <= py <= h + 1e-9)}
        if clamped:
            rec["clamped_lat"] = True
        out.append(rec)
    note = {"mercator": "conformal: shapes/angles kept locally, area grows toward the poles (Greenland ~ Africa)",
            "equirect": "neither equal-area nor conformal; distances true along meridians%s"
                        % (" and along %.4g deg" % ref_lat if ref_lat else " and the equator")}[proj]
    return {"command": "project", "proj": proj, "size": [w, h], "extent": [west, south, east, north],
            "ref_lat": ref_lat, "px_per_unit": round(scale, 6), "offset": [round(ox, 3), round(oy, 3)],
            "distortion": note, "points": out}


# ---------------------------------------------------------------- classify
def _lin_pct(xs, p):
    pos = (len(xs) - 1) * p
    i = int(math.floor(pos))
    j = min(i + 1, len(xs) - 1)
    return xs[i] + (xs[j] - xs[i]) * (pos - i)


def breaks_quantile(xs, k):
    s = sorted(xs)
    return [s[0]] + [_lin_pct(s, i / k) for i in range(1, k)] + [s[-1]]


def breaks_equal(xs, k):
    lo, hi = min(xs), max(xs)
    return [lo + (hi - lo) * i / k for i in range(k)] + [hi]


def breaks_jenks(xs, k):
    """Exact Fisher-Jenks natural breaks (Jenks 1977 dynamic programme). Returns K+1 bounds."""
    d = sorted(xs)
    n = len(d)
    inf = float("inf")
    lower = [[0] * (k + 1) for _ in range(n + 1)]
    var = [[0.0] * (k + 1) for _ in range(n + 1)]
    for j in range(1, k + 1):
        lower[1][j] = 1
        for i in range(2, n + 1):
            var[i][j] = inf
    for l in range(2, n + 1):
        s1 = s2 = 0.0
        v = 0.0
        for m in range(1, l + 1):
            i3 = l - m + 1
            val = d[i3 - 1]
            s2 += val * val
            s1 += val
            v = s2 - s1 * s1 / m
            i4 = i3 - 1
            if i4:
                for j in range(2, k + 1):
                    if var[l][j] >= v + var[i4][j - 1]:
                        lower[l][j] = i3
                        var[l][j] = v + var[i4][j - 1]
        lower[l][1] = 1
        var[l][1] = v
    br = [0.0] * (k + 1)
    br[0], br[k] = d[0], d[-1]
    kk = n
    for c in range(k, 1, -1):
        idx = lower[kk][c] - 2
        br[c - 1] = d[idx]
        kk = lower[kk][c] - 1
    return br


def assign(v, br):
    for c in range(1, len(br)):
        if v <= br[c] + 1e-12:
            return c
    return len(br) - 1


def gvf(xs, br):
    mean = sum(xs) / len(xs)
    sdam = sum((x - mean) ** 2 for x in xs)
    groups = {}
    for x in xs:
        groups.setdefault(assign(x, br), []).append(x)
    sdcm = sum(sum((x - sum(g) / len(g)) ** 2 for x in g) for g in groups.values())
    return 1.0 if sdam == 0 else 1 - sdcm / sdam


RATE_WORDS = re.compile(r"(rate|pct|percent|per|share|ratio|density|avg|mean|median|index|نسبة|معدل|كثافة|متوسط)", re.I)


def classify(path, value, method, k, name=None, per_capita=None, scale=100000.0):
    if method not in ("quantile", "equal", "jenks"):
        raise BadInput("--method must be quantile, equal or jenks")
    if not 2 <= k <= 12:
        raise BadInput("--classes must be between 2 and 12")
    if not math.isfinite(scale) or scale <= 0:
        raise BadInput("--scale must be > 0")
    try:
        rows = list(csv.DictReader(io.StringIO(read_text(path))))
    except FileNotFoundError:
        raise BadInput("data file not found: %s" % path)
    if not rows:
        raise BadInput("data CSV has no rows")
    cols = list(rows[0].keys())
    for c in [value] + ([per_capita] if per_capita else []) + ([name] if name else []):
        if c not in cols:
            raise BadInput("column not found: %s (have: %s)" % (c, ", ".join(cols)))
    name = name or cols[0]
    recs, raw = [], []
    for i, r in enumerate(rows, 2):
        try:
            v = float(r[value])
        except (TypeError, ValueError):
            raise BadInput("line %d: %s is not a number" % (i, value))
        raw.append(v)
        if per_capita:
            try:
                pop = float(r[per_capita])
            except (TypeError, ValueError):
                raise BadInput("line %d: %s is not a number" % (i, per_capita))
            if pop <= 0:
                raise BadInput("line %d: population must be > 0" % i)
            v = v / pop * scale
        if not math.isfinite(v):
            raise BadInput("line %d: value is not finite" % i)
        recs.append({"name": r[name], "value": v})
    xs = [x["value"] for x in recs]
    if len(set(xs)) < k:
        raise BadInput("only %d distinct values for %d classes" % (len(set(xs)), k))
    if method == "jenks" and len(xs) > 5000:
        raise BadInput("jenks is O(k n^2); use at most 5000 rows or quantile")
    br = {"quantile": breaks_quantile, "equal": breaks_equal, "jenks": breaks_jenks}[method](xs, k)
    warnings = []
    if per_capita:
        norm = {"normalized": True, "by": per_capita, "scale": scale, "unit": "%s per %g %s" % (value, scale, per_capita)}
    else:
        counts_like = all(v >= 0 and float(v).is_integer() for v in raw) and not RATE_WORDS.search(value)
        norm = {"normalized": False, "looks_like_raw_counts": counts_like}
        if counts_like:
            warnings.append("'%s' looks like raw counts: a choropleth of counts mostly maps population or area; "
                            "pass --per-capita <population column> or map counts as proportional symbols" % value)
    if len(set(round(b, 12) for b in br)) < len(br):
        warnings.append("duplicate break values (many ties); some classes are empty — try fewer classes or jenks")
    counts = [0] * k
    for x in recs:
        c = assign(x["value"], br)
        x["class"] = c
        x["value"] = round(x["value"], 6)
        counts[c - 1] += 1
    if any(c == 0 for c in counts):
        warnings.append("empty classes: %s" % [i + 1 for i, c in enumerate(counts) if c == 0])
    return {"command": "classify", "method": method, "classes": k, "n": len(recs), "value": value,
            "normalization": norm, "breaks": [round(b, 6) for b in br], "class_counts": counts,
            "gvf": round(gvf(xs, br), 6), "rule": "class c holds breaks[c-1] < v <= breaks[c] (class 1 includes the minimum)",
            "warnings": warnings, "rows": recs}


# ---------------------------------------------------------------- ledger
DEG_CRS = {"EPSG:4326", "CRS84", "OGC:CRS84", "WGS84", "EPSG:4979"}
M_CRS = {"EPSG:3857", "EPSG:900913"}
WEB_MERC_MAX = 20037508.342789244


def _decimals(v):
    s = repr(float(v))
    return len(s.split(".")[1]) if "." in s and "e" not in s else 0


def ledger(d):
    if isinstance(d, list):
        d = {"points": d}
    if not isinstance(d, dict) or not isinstance(d.get("points"), list):
        raise BadInput("ledger must be an object with a 'points' list (or a list of points)")
    errors, warns = [], []
    crs = str(d.get("crs") or "").strip().upper()
    if not crs:
        errors.append({"point": None, "rule": "crs.missing", "message": "ledger does not state its CRS"})
        unit = "deg"
    elif crs in DEG_CRS:
        unit = "deg"
    elif crs in M_CRS:
        unit = "m"
    else:
        warns.append({"point": None, "rule": "crs.unknown", "message": "CRS %s is not checked by this tool; ranges skipped" % crs})
        unit = None
    dsrc = d.get("source")
    dlic = d.get("licence", d.get("license"))
    seen = set()
    ok_pts = 0
    for n, p in enumerate(d["points"]):
        before = len(errors)
        if not isinstance(p, dict):
            errors.append({"point": n, "rule": "point.type", "message": "point is not an object"}); continue
        pid = p.get("id", n)
        if "id" not in p:
            warns.append({"point": pid, "rule": "id.missing", "message": "point has no id (index used)"})
        elif pid in seen:
            errors.append({"point": pid, "rule": "id.duplicate", "message": "duplicate id"})
        seen.add(pid)
        xk, yk = ("x", "y") if unit == "m" and "x" in p else ("lon", "lat")
        x, y = p.get(xk, p.get("lng")), p.get(yk)
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in (x, y)):
            errors.append({"point": pid, "rule": "coord.type", "message": "%s/%s must be finite numbers" % (xk, yk)})
        elif unit == "deg":
            if not -90 <= y <= 90 or not -180 <= x <= 180:
                msg = "lon %s / lat %s out of range" % (x, y)
                if -90 <= x <= 90 and -180 <= y <= 180:
                    msg += " — likely swapped (lat,lon given as lon,lat)"
                errors.append({"point": pid, "rule": "coord.range", "message": msg})
            if x == 0 and y == 0:
                warns.append({"point": pid, "rule": "coord.null_island", "message": "0,0 is usually a missing value"})
            if max(_decimals(x), _decimals(y)) > 7:
                warns.append({"point": pid, "rule": "coord.precision", "message": "more than 7 decimals (sub-cm) is false precision"})
        elif unit == "m":
            if abs(x) > WEB_MERC_MAX or abs(y) > WEB_MERC_MAX:
                errors.append({"point": pid, "rule": "coord.range", "message": "x/y outside the Web Mercator square (+-20037508.34 m)"})
            elif abs(x) <= 180 and abs(y) <= 90:
                warns.append({"point": pid, "rule": "coord.units", "message": "values look like degrees but CRS is in metres"})
        src = p.get("source", dsrc)
        lic = p.get("licence", p.get("license", dlic))
        if not (isinstance(src, str) and src.strip()):
            errors.append({"point": pid, "rule": "source.missing", "message": "no source for this point or the ledger"})
        if not (isinstance(lic, str) and lic.strip()):
            errors.append({"point": pid, "rule": "licence.missing", "message": "no licence for this point or the ledger"})
        if not (p.get("date") or d.get("date")):
            warns.append({"point": pid, "rule": "date.missing", "message": "no date (when was it measured/published?)"})
        kind = p.get("kind", d.get("kind"))
        if kind not in ("measured", "schematic"):
            warns.append({"point": pid, "rule": "kind.unstated", "message": "state kind: measured or schematic"})
        if len(errors) == before:
            ok_pts += 1
    return {"command": "ledger", "crs": crs or None, "points": len(d["points"]), "points_ok": ok_pts,
            "errors": errors, "warnings": warns, "verdict": "pass" if not errors else "fail"}


def self_test():
    r = project("equirect", "2000x1000", ["0,0", "-180,90", "180,-90"])
    assert [(p["x"], p["y"]) for p in r["points"]] == [(1000, 500), (0, 0), (2000, 1000)], r
    r = project("mercator", "1024x1024", ["0,0", "180,85.05112878"])
    assert abs(r["points"][0]["x"] - 512) < 1e-6 and abs(r["points"][1]["y"]) < 1e-3
    assert breaks_jenks([1, 2, 3, 10, 11, 12, 20, 21, 22], 3) == [1, 3, 12, 22]
    lg = ledger({"crs": "EPSG:4326", "points": [{"id": 1, "lon": 31.2, "lat": 30.0}]})
    assert lg["verdict"] == "fail" and {e["rule"] for e in lg["errors"]} == {"source.missing", "licence.missing"}
    return {"self_test": "ok", "checks": 4}


def main(argv=None):
    raw = list(sys.argv[1:] if argv is None else argv)
    coords = []
    if "project" in raw:  # "-73.98,40.75" starts with '-' and would be read as an option
        k = raw.index("project")
        keep, rest, j = raw[:k + 1], raw[k + 1:], 0
        while j < len(rest):
            tok = rest[j]
            if tok == "--bbox" and j + 1 < len(rest):
                keep.append("--bbox=" + rest[j + 1]); j += 2
                continue
            (coords if COORD.match(tok) else keep).append(tok)
            j += 1
        raw = keep
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--self-test", action="store_true", help="run a small offline check and exit 0")
    sub = p.add_subparsers(dest="cmd")
    a = sub.add_parser("project")
    a.add_argument("--proj", required=True, choices=["mercator", "equirect"])
    a.add_argument("--size", required=True)
    a.add_argument("--bbox")
    a.add_argument("--ref-lat", type=float, default=0.0)
    a.add_argument("points", nargs="*", help="LON,LAT pairs")
    c = sub.add_parser("classify")
    c.add_argument("data")
    c.add_argument("--value", required=True)
    c.add_argument("--name")
    c.add_argument("--method", required=True, choices=["quantile", "equal", "jenks"])
    c.add_argument("--classes", type=int, default=5)
    c.add_argument("--per-capita")
    c.add_argument("--scale", type=float, default=100000.0)
    g = sub.add_parser("ledger")
    g.add_argument("points")
    args = p.parse_args(raw)
    try:
        if args.self_test:
            print(json.dumps(self_test()))
            return 0
        if args.cmd == "project":
            r = project(args.proj, args.size, coords + list(args.points), args.bbox, args.ref_lat)
        elif args.cmd == "classify":
            r = classify(args.data, args.value, args.method, args.classes, args.name, args.per_capita, args.scale)
        elif args.cmd == "ledger":
            try:
                d = json.loads(read_text(args.points))
            except FileNotFoundError:
                raise BadInput("ledger file not found: %s" % args.points)
            except json.JSONDecodeError as e:
                raise BadInput("ledger is not valid JSON: %s" % e.msg)
            r = ledger(d)
        else:
            p.print_help(sys.stderr)
            return 2
    except BadInput as e:
        print("geo_plate: %s" % e, file=sys.stderr)
        return 2
    except AssertionError as e:
        print("geo_plate: self-test failed: %s" % e, file=sys.stderr)
        return 1
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
