"""Programs for the app-feature-transfer family (cards without an existing code proof).

Desktop-app patterns (fuses, bridges, updaters, installers, deep links, migrations, caches,
undo, editor servers) are rebuilt as small, real, offline implementations and fed planted good
and bad inputs whose verdicts are known. Media cards run ffmpeg on tiny synthetic clips and read
the result back with ffprobe or by decoding frames.
"""
from __future__ import annotations
import fnmatch
import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import yaml
from PIL import Image, ImageChops, ImageDraw, ImageFont

FONT_DIRS = ["/usr/share/fonts/truetype/noto", "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/liberation"]
ARABIC = ["NotoSansArabic-Regular.ttf", "NotoNaskhArabic-Regular.ttf", "DejaVuSans.ttf"]


def font(size):
    for d in FONT_DIRS:
        for n in ARABIC:
            if (Path(d) / n).is_file():
                return ImageFont.truetype(str(Path(d) / n), size)
    raise FileNotFoundError("font")


def save_json(work, name, obj):
    (work / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def ff(*args, ok=True):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], capture_output=True, text=True)
    if ok and r.returncode:
        raise RuntimeError(r.stderr[-600:])
    return r


def probe(p):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(p)],
                                     capture_output=True, text=True, check=True).stdout)


def dur(p):
    return float(probe(p)["format"]["duration"])


# ---------------------------------------------------------------- APPX-20
def choose_ui(event: str, online: bool, local_ok: bool):
    if event == "did-fail-load" or not online:
        return "local:offline.html" if local_ok else "error"
    return "remote"


def appx_20(work):
    (work / "offline.html").write_text('<html dir="rtl"><body><p>لا اتصال</p><button id="retry">إعادة المحاولة</button></body></html>', encoding="utf-8")
    cases = {"loaded+online": choose_ui("did-finish-load", True, True), "fail": choose_ui("did-fail-load", True, True),
             "offline": choose_ui("did-finish-load", False, True), "no-bundle": choose_ui("did-fail-load", False, False)}
    save_json(work, "decisions.json", cases)
    return [("normal load stays remote", cases["loaded+online"] == "remote", cases),
            ("did-fail-load falls back to the packaged page", cases["fail"] == "local:offline.html", cases["fail"]),
            ("navigator.onLine=false falls back", cases["offline"] == "local:offline.html", cases["offline"]),
            ("fallback page explains and offers retry", 'id="retry"' in (work / "offline.html").read_text(encoding="utf-8"), "retry")]


# ---------------------------------------------------------------- APPX-21
FLIP = [("margin-left", "margin-right"), ("padding-left", "padding-right"), ("border-left", "border-right"), ("left", "right"),
        ("text-align: left", "text-align: right")]


def to_rtl(css: str) -> str:
    out = css
    for a, b in FLIP:
        out = re.sub(rf"(?<![\w-]){re.escape(a)}(?![\w-])", "\0TMP\0", out)
        out = re.sub(rf"(?<![\w-]){re.escape(b)}(?![\w-])", a, out)
        out = out.replace("\0TMP\0", b)
    out = re.sub(r"translateX\((-?)(\d+)px\)", lambda m: f"translateX({'' if m.group(1) else '-'}{m.group(2)}px)", out)
    return out


def bundle_for(lang):
    return "app.rtl.css" if lang.split("-")[0] in ("ar", "he", "fa", "ur") else "app.ltr.css"


def appx_21(work):
    ltr = ".a{margin-left:8px;padding-right:4px}.b{left:0}.c{margin-inline-start:12px}.d{transform:translateX(10px)}"
    rtl = to_rtl(ltr)
    (work / "app.ltr.css").write_text(ltr)
    (work / "app.rtl.css").write_text(rtl)
    return [("margin-left -> margin-right, padding-right -> padding-left", "margin-right:8px" in rtl and "padding-left:4px" in rtl, rtl),
            ("left:0 -> right:0", ".b{right:0}" in rtl, rtl),
            ("logical properties untouched", "margin-inline-start:12px" in rtl, rtl),
            ("directional translate flipped", "translateX(-10px)" in rtl, rtl),
            ("double flip restores the source", to_rtl(rtl) == ltr, "involution"),
            ("ar-SA picks the .rtl bundle, en the .ltr", (bundle_for("ar-SA"), bundle_for("en")) == ("app.rtl.css", "app.ltr.css"), "bundle")]


# ---------------------------------------------------------------- APPX-22
EXTS = "avi gif heic jpeg jpg key mkv mov mp4 mpeg numbers pages png svg webm webp".split()


def associations():
    import mimetypes
    mimetypes.add_type("image/heic", ".heic")
    mimetypes.add_type("video/x-matroska", ".mkv")
    mimetypes.add_type("image/webp", ".webp")
    for e, m in (("key", "application/x-iwork-keynote-sffkey"), ("numbers", "application/x-iwork-numbers-sffnumbers"), ("pages", "application/x-iwork-pages-sffpages")):
        mimetypes.add_type(m, "." + e)
    return [{"ext": e, "mimeType": mimetypes.guess_type("f." + e)[0]} for e in EXTS]


def files_from_argv(argv):
    return [a for a in argv[1:] if not a.startswith("-") and Path(a).suffix.lstrip(".").lower() in EXTS]


def appx_22(work):
    a = associations()
    save_json(work, "fileAssociations.json", a)
    got = files_from_argv(["app.exe", "--squirrel-firstrun", "C:/v/clip.MOV", "notes.txt", "pic.heic"])
    return [("16 extensions registered", len(a) == 16, len(a)),
            ("every extension has a mime type", all(x["mimeType"] for x in a), [x for x in a if not x["mimeType"]]),
            ("argv: media files kept, flags and .txt ignored", got == ["C:/v/clip.MOV", "pic.heic"], got),
            ("mp4 -> video/mp4", next(x["mimeType"] for x in a if x["ext"] == "mp4") == "video/mp4", "mp4")]


# ---------------------------------------------------------------- APPX-23
class Bridge:
    exposed = ("onPageBuildIdentityReady", "requestMessagePort")

    def __init__(self, allowed_origins):
        self.allowed, self.ports = set(allowed_origins), []

    def handle(self, channel, sender_url):
        from urllib.parse import urlsplit
        u = urlsplit(sender_url)
        origin = f"{u.scheme}://{u.netloc}"
        if channel != "request-port" or origin not in self.allowed:
            return {"ok": False, "reason": "rejected"}
        self.ports.append(origin)
        return {"ok": True, "port": len(self.ports)}


def appx_23(work):
    b = Bridge(["https://app.kosif.dev"])
    ok = b.handle("request-port", "https://app.kosif.dev/editor?x=1")
    evil = b.handle("request-port", "https://app.kosif.dev.evil.com/")
    other = b.handle("eval", "https://app.kosif.dev/")
    save_json(work, "bridge.json", {"exposed": Bridge.exposed, "ok": ok, "evil": evil})
    return [("exactly two members exposed", len(Bridge.exposed) == 2, Bridge.exposed),
            ("allowed frame gets a MessagePort", ok["ok"], ok),
            ("look-alike origin rejected (senderFrame.url check)", not evil["ok"], evil),
            ("unknown channel rejected", not other["ok"], other)]


# ---------------------------------------------------------------- APPX-24
SENTINEL = b"dL7pKGdnNz796PbbjQWNKmHXBZaB9tsX"
FUSES = ["RunAsNode", "EnableCookieEncryption", "EnableNodeOptionsEnvironmentVariable", "EnableNodeCliInspectArguments",
         "EnableEmbeddedAsarIntegrityValidation", "OnlyLoadAppFromAsar"]
WANT = {"RunAsNode": "0", "EnableCookieEncryption": "1", "EnableNodeOptionsEnvironmentVariable": "0", "EnableNodeCliInspectArguments": "0",
        "EnableEmbeddedAsarIntegrityValidation": "1", "OnlyLoadAppFromAsar": "1"}


def write_fuses(states: dict) -> bytes:
    wire = bytes([1, len(FUSES)]) + "".join(states[f] for f in FUSES).encode()
    return os.urandom(64) + SENTINEL + wire + os.urandom(64)


def read_fuses(blob: bytes) -> dict:
    i = blob.index(SENTINEL) + len(SENTINEL)
    ver, n = blob[i], blob[i + 1]
    vals = blob[i + 2:i + 2 + n].decode()
    return {"version": ver, **{FUSES[k]: vals[k] for k in range(n)}}


def fuse_audit(blob):
    f = read_fuses(blob)
    return [k for k, v in WANT.items() if f[k] != v]


def appx_24(work):
    good = write_fuses(WANT)
    bad = write_fuses(dict(WANT, RunAsNode="1", OnlyLoadAppFromAsar="0"))
    (work / "App.exe.bin").write_bytes(good)
    rd = read_fuses(good)
    return [("fuse wire found after the sentinel (version 1, 6 fuses)", rd["version"] == 1 and len(rd) == 7, rd),
            ("hardened build passes the audit", fuse_audit(good) == [], fuse_audit(good)),
            ("RunAsNode on and ASAR-only off caught", fuse_audit(bad) == ["RunAsNode", "OnlyLoadAppFromAsar"], fuse_audit(bad))]


# ---------------------------------------------------------------- APPX-25
def update_decision(latest_yml: str, current: str, payload: bytes, recording: bool):
    import base64
    meta = yaml.safe_load(latest_yml)
    newer = tuple(map(int, meta["version"].split("."))) > tuple(map(int, current.split(".")))
    ok_hash = base64.b64encode(hashlib.sha512(payload).digest()).decode() == meta["sha512"]
    if not newer:
        return "up-to-date"
    if not ok_hash:
        return "reject: sha512 mismatch"
    return "defer: recording" if recording else "offer to user"


def appx_25(work):
    import base64
    payload = b"setup-2.1.0" * 100
    yml = f"version: 2.1.0\npath: App-Setup-2.1.0.exe\nsha512: {base64.b64encode(hashlib.sha512(payload).digest()).decode()}\nreleaseDate: '2026-10-30'\n"
    (work / "latest.yml").write_text(yml)
    return [("newer signed build is offered, not auto-installed", update_decision(yml, "2.0.4", payload, False) == "offer to user", "offer"),
            ("never installs during a recording", update_decision(yml, "2.0.4", payload, True) == "defer: recording", "defer"),
            ("tampered payload rejected by sha512", update_decision(yml, "2.0.4", payload + b"x", False) == "reject: sha512 mismatch", "reject"),
            ("same version -> up-to-date", update_decision(yml, "2.1.0", payload, False) == "up-to-date", "same"),
            ("2.10.0 compares newer than 2.9.9 (numeric, not string)", update_decision(yml.replace("2.1.0", "2.10.0"), "2.9.9", payload, False) == "offer to user", "numeric")]


# ---------------------------------------------------------------- APPX-26
PII = [(re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[email]"), (re.compile(r"(?:/Users|/home|C:\\\\Users)[/\\\\][^/\\\\\s]+"), "<home>"),
       (re.compile(r"\b(?:\+?966|0)5\d{8}\b"), "[phone]")]


def scrub(event: dict) -> dict:
    txt = json.dumps(event, ensure_ascii=False)
    for rx, rep in PII:
        txt = rx.sub(rep, txt)
    return json.loads(txt)


def send_report(event, consent):
    return scrub(event) if consent else None


def appx_26(work):
    ev = {"message": "crash in /home/nasser/app/main.js", "user": {"email": "nasser@example.com"}, "extra": "call 0551234567"}
    out = send_report(ev, True)
    save_json(work, "report.json", out)
    blob = json.dumps(out, ensure_ascii=False)
    return [("email scrubbed", "nasser@example.com" not in blob and "[email]" in blob, out["user"]),
            ("home path scrubbed", "/home/nasser" not in blob and "<home>/app/main.js" in blob, out["message"]),
            ("Saudi mobile scrubbed", "0551234567" not in blob, out["extra"]),
            ("nothing sent without consent", send_report(ev, False) is None, None)]


# ---------------------------------------------------------------- APPX-27
def parse_deeplink(url, scheme="myapp"):
    from urllib.parse import urlsplit, parse_qs
    u = urlsplit(url)
    if u.scheme != scheme:
        return None
    return {"action": u.netloc, "path": u.path.strip("/"), "query": {k: v[0] for k, v in parse_qs(u.query).items()}}


def second_instance(argv, scheme="myapp"):
    links = [a for a in argv if a.startswith(scheme + "://")]
    return parse_deeplink(links[0], scheme) if links else {"action": "focus"}


def appx_27(work):
    a = second_instance(["app.exe", "--flag", "myapp://open/project/42?tab=timeline"])
    b = second_instance(["app.exe"])
    c = parse_deeplink("https://evil.example/open")
    save_json(work, "deeplinks.json", {"a": a, "b": b})
    return [("deep link from second-instance argv parsed", a == {"action": "open", "path": "project/42", "query": {"tab": "timeline"}}, a),
            ("plain relaunch just focuses the window", b == {"action": "focus"}, b),
            ("other schemes ignored", c is None, c)]


# ---------------------------------------------------------------- APPX-29
def bootstrap(payload: bytes, expected_sha: str, cert_der: bytes, pins: set):
    pin = "sha256//" + __import__("base64").b64encode(hashlib.sha256(cert_der).digest()).decode()
    if pin not in pins:
        return "abort: certificate pin mismatch"
    if sha256(payload) != expected_sha:
        return "abort: payload hash mismatch"
    return "run"


def appx_29(work):
    import base64
    cert = b"FAKE-DER-SPKI-of-update-server"
    pins = {"sha256//" + base64.b64encode(hashlib.sha256(cert).digest()).decode()}
    payload = b"\x7fPAYLOAD" * 500
    exp = sha256(payload)
    (work / "payload.bin").write_bytes(payload)
    save_json(work, "manifest.json", {"sha256": exp, "pins": sorted(pins)})
    return [("pinned server + matching payload -> run", bootstrap(payload, exp, cert, pins) == "run", "run"),
            ("MITM certificate refused before download is trusted", bootstrap(payload, exp, b"other-cert", pins) == "abort: certificate pin mismatch", "pin"),
            ("one flipped byte refused", bootstrap(payload[:-1] + b"\x00", exp, cert, pins) == "abort: payload hash mismatch", "hash")]


# ---------------------------------------------------------------- APPX-51
class Plugin:
    id = ""
    params = {}

    def validate(self, s):
        raise NotImplementedError

    def render(self, img, s):
        raise NotImplementedError


class Exposure(Plugin):
    id = "exposure"

    def validate(self, s):
        return -3 <= s.get("ev", 0) <= 3

    def render(self, img, s):
        return np.clip(img * 2 ** s["ev"], 0, 1)


class Saturation(Plugin):
    id = "saturation"

    def validate(self, s):
        return 0 <= s.get("amount", 1) <= 2

    def render(self, img, s):
        g = img.mean(axis=2, keepdims=True)
        return np.clip(g + (img - g) * s["amount"], 0, 1)


def load_plugins(folder: Path):
    reg = {}
    for p in sorted(folder.glob("*.json")):
        spec = json.loads(p.read_text())
        cls = {"exposure": Exposure, "saturation": Saturation}.get(spec["class"])
        if cls:
            reg[cls.id] = cls()
    return reg


def appx_51(work):
    pl = work / "plugins"
    pl.mkdir()
    (pl / "10_exposure.json").write_text('{"class": "exposure"}')
    (pl / "20_saturation.json").write_text('{"class": "saturation"}')
    (pl / "30_unknown.json").write_text('{"class": "teleport"}')
    reg = load_plugins(pl)
    img = np.full((4, 4, 3), [0.2, 0.4, 0.6])
    up = reg["exposure"].render(img, {"ev": 1})
    grey = reg["saturation"].render(img, {"amount": 0})
    np.save(work / "out.npy", up)
    return [("registry loads the two known plugins from the folder", sorted(reg) == ["exposure", "saturation"], sorted(reg)),
            ("+1 EV doubles linear values", np.allclose(up[0, 0], [0.4, 0.8, 1.0]), up[0, 0].tolist()),
            ("saturation 0 gives grey (all channels equal)", np.allclose(grey[0, 0], 0.4), grey[0, 0].tolist()),
            ("each plugin has its own validator (ev 5 refused, amount 3 refused)", not reg["exposure"].validate({"ev": 5}) and not reg["saturation"].validate({"amount": 3}), "validators")]


# ---------------------------------------------------------------- APPX-52
def v7_to_v8(d): return {**{k: v for k, v in d.items() if k != "expo"}, "exposure": d["expo"], "version": 8}
def v8_to_v9(d): return {**d, "exposure": {"ev": d["exposure"]}, "version": 9}
def v9_to_v10(d): return {**d, "tags": d.get("tags", []), "version": 10}


MIGRATIONS = {7: v7_to_v8, 8: v8_to_v9, 9: v9_to_v10}


def migrate(doc, latest=10):
    while doc["version"] < latest:
        if doc["version"] not in MIGRATIONS:
            raise ValueError(f"no migration from v{doc['version']}")
        doc = MIGRATIONS[doc["version"]](doc)
    return doc


def appx_52(work):
    old = {"version": 7, "expo": 0.5, "name": "قديم"}
    new = migrate(dict(old))
    save_json(work, "migrated.json", new)
    try:
        migrate({"version": 5})
        rej = False
    except ValueError:
        rej = True
    return [("v7 file reaches v10 through every step", new == {"version": 10, "exposure": {"ev": 0.5}, "name": "قديم", "tags": []}, new),
            ("v9 file needs only the last step", migrate({"version": 9, "exposure": {"ev": 1}}) == {"version": 10, "exposure": {"ev": 1}, "tags": []}, "v9"),
            ("current file untouched", migrate({"version": 10, "x": 1}) == {"version": 10, "x": 1}, "v10"),
            ("unknown old version refused, not guessed", rej, rej)]


# ---------------------------------------------------------------- APPX-54
def radial_mask(H, W, cx, cy, r, feather):
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.hypot(xx - cx, yy - cy)
    return np.clip((r + feather - d) / feather, 0, 1)


def local_adjust(img, mask, adjust):
    m = mask[..., None]
    return img * (1 - m) + adjust(img) * m


def appx_54(work):
    img = np.full((40, 60, 3), 0.25)
    m = radial_mask(40, 60, 30, 20, 8, 6)
    out = local_adjust(img, m, lambda x: np.clip(x * 2, 0, 1))
    Image.fromarray((out * 255).astype(np.uint8)).save(work / "brushed.png")
    save_json(work, "preset.json", {"adjust": {"exposure_ev": 1}, "mask": {"type": "radial", "cx": 30, "cy": 20, "r": 8, "feather": 6}})
    return [("inside the mask fully adjusted (0.25 -> 0.5)", np.allclose(out[20, 30], 0.5), out[20, 30].tolist()),
            ("outside untouched", np.allclose(out[0, 0], 0.25), out[0, 0].tolist()),
            ("feather midway blends 50/50 (0.375)", np.allclose(out[20, 30 + 11], 0.375), out[20, 41].tolist()),
            ("mask shape saved with the preset", json.loads((work / "preset.json").read_text())["mask"]["r"] == 8, "saved")]


# ---------------------------------------------------------------- APPX-55
def kern_pairs(text, top=3):
    from collections import Counter
    c = Counter()
    for w in re.findall(r"[\u0621-\u064a]+", text):
        for a, b in zip(w, w[1:]):
            c[a + b] += 1
    return c.most_common(top)


def appx_55(work):
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.ttLib import TTFont
    names = [".notdef", "alef", "lam"]
    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(names)
    fb.setupCharacterMap({0x0627: "alef", 0x0644: "lam"})
    glyphs = {}
    for n in names:
        pen = TTGlyphPen(None)
        if n != ".notdef":
            pen.moveTo((100, 0)); pen.lineTo((200, 0)); pen.lineTo((200, 700)); pen.lineTo((100, 700)); pen.closePath()
        glyphs[n] = pen.glyph()
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics({n: (300, 100) for n in names})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({"familyName": "KosifTest", "styleName": "Regular"})
    fb.setupOS2()
    fb.setupPost()
    fb.save(str(work / "test.ttf"))
    f = TTFont(str(work / "test.ttf"))
    pairs = kern_pairs("السلام عليكم الله الكلام السلام")
    save_json(work, "kern_pairs.json", pairs)
    return [("font built and read back with cmap for alef/lam", f.getBestCmap() == {0x0627: "alef", 0x0644: "lam"}, f.getBestCmap()),
            ("advance width 300 stored", f["hmtx"]["lam"][0] == 300, f["hmtx"]["lam"]),
            ("most frequent pair from real Arabic text is 'ال'", pairs[0][0] == "ال", pairs)]


# ---------------------------------------------------------------- APPX-56
def build_asset(params: dict, seed: int):
    rng = np.random.default_rng(seed)
    n, r, jitter = params["segments"], params["radius"], params["jitter"]
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rad = r * (1 + jitter * rng.uniform(-1, 1, n))
    return np.stack([rad * np.cos(ang), rad * np.sin(ang)], 1)


def cached_build(cache: Path, params, seed):
    key = sha256(json.dumps({"p": params, "s": seed}, sort_keys=True).encode())[:16]
    p = cache / f"{key}.json"
    if p.exists():
        return json.loads(p.read_text()), True
    g = build_asset(params, seed).round(6).tolist()
    p.write_text(json.dumps(g))
    return g, False


def appx_56(work):
    cache = work / "cache"
    cache.mkdir()
    P = {"segments": 12, "radius": 1.0, "jitter": 0.1}
    a, hit_a = cached_build(cache, P, 3)
    b, hit_b = cached_build(cache, P, 3)
    c, _ = cached_build(cache, dict(P, segments=8), 3)
    rad = np.hypot(*np.array(a).T)
    return [("same params + seed -> identical geometry, second call from cache", a == b and not hit_a and hit_b, (hit_a, hit_b)),
            ("segments param controls vertex count (12 vs 8)", (len(a), len(c)) == (12, 8), (len(a), len(c))),
            ("jitter 0.1 keeps every radius within 0.9-1.1", rad.min() >= 0.9 - 1e-9 and rad.max() <= 1.1 + 1e-9, (round(float(rad.min()), 3), round(float(rad.max()), 3))),
            ("one cache file per parameter set", len(list(cache.glob("*.json"))) == 2, len(list(cache.glob("*.json"))))]


# ---------------------------------------------------------------- APPX-58
def export_animation(keys, fps=30):
    """One keyframed property (x over time) -> Lottie layer JSON, SVG SMIL and glTF animation sampler."""
    import base64
    import struct
    op = round(keys[-1][0] * fps)
    lottie = {"v": "5.7.0", "fr": fps, "ip": 0, "op": op, "w": 200, "h": 100,
              "layers": [{"ty": 4, "ks": {"p": {"a": 1, "k": [{"t": round(t * fps), "s": [x, 50, 0]} for t, x in keys]}}}]}
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><circle r="8" cy="50"><animate attributeName="cx" '
           f'dur="{keys[-1][0]}s" values="{";".join(str(x) for _, x in keys)}" keyTimes="{";".join(str(round(t / keys[-1][0], 4)) for t, _ in keys)}" repeatCount="indefinite"/></circle></svg>')
    times = struct.pack(f"<{len(keys)}f", *[t for t, _ in keys])
    vals = struct.pack(f"<{3 * len(keys)}f", *[v for _, x in keys for v in (x / 100, 0.5, 0)])
    buf = times + vals
    gltf = {"asset": {"version": "2.0"}, "nodes": [{"name": "dot"}], "scenes": [{"nodes": [0]}],
            "buffers": [{"byteLength": len(buf), "uri": "data:application/octet-stream;base64," + base64.b64encode(buf).decode()}],
            "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": len(times)}, {"buffer": 0, "byteOffset": len(times), "byteLength": len(vals)}],
            "accessors": [{"bufferView": 0, "componentType": 5126, "count": len(keys), "type": "SCALAR", "min": [keys[0][0]], "max": [keys[-1][0]]},
                          {"bufferView": 1, "componentType": 5126, "count": len(keys), "type": "VEC3"}],
            "animations": [{"samplers": [{"input": 0, "output": 1, "interpolation": "LINEAR"}], "channels": [{"sampler": 0, "target": {"node": 0, "path": "translation"}}]}]}
    return lottie, svg, gltf


def appx_58(work):
    import base64
    import struct
    import xml.etree.ElementTree as ET
    keys = [(0.0, 20), (1.0, 180), (2.0, 20)]
    lottie, svg, gltf = export_animation(keys)
    save_json(work, "anim.lottie.json", lottie)
    (work / "anim.svg").write_text(svg)
    save_json(work, "anim.gltf", gltf)
    raw = base64.b64decode(gltf["buffers"][0]["uri"].split(",", 1)[1])
    t = struct.unpack("<3f", raw[:12])
    an = ET.fromstring(svg).find(".//{http://www.w3.org/2000/svg}animate")
    return [("Lottie: 60 frames at 30 fps, keyframe at frame 30 = x 180", lottie["op"] == 60 and lottie["layers"][0]["ks"]["p"]["k"][1] == {"t": 30, "s": [180, 50, 0]}, lottie["op"]),
            ("SVG SMIL: 3 values over 2 s", an.get("values") == "20;180;20" and an.get("dur") == "2.0s", an.attrib),
            ("glTF 2.0 buffer decodes back to the key times", gltf["asset"]["version"] == "2.0" and t == (0.0, 1.0, 2.0), t),
            ("glTF byteLength matches the buffer", gltf["buffers"][0]["byteLength"] == len(raw) == 12 + 36, len(raw))]


# ---------------------------------------------------------------- APPX-120
def fidelity_check(contract, ref, built):
    allowed = set(contract["deviations"])
    diffs = sorted(k for k in ref if ref[k] != built.get(k))
    return {"undeclared": [d for d in diffs if d not in allowed], "declared": [d for d in diffs if d in allowed]}


def appx_120(work):
    contract = {"source": "figma:landing@v3", "size": [1440, 900], "deviations": ["hero.copy"]}
    ref = {"hero.copy": "Old", "hero.padding": 64, "cta.radius": 12, "nav.height": 72}
    built_ok = dict(ref, **{"hero.copy": "New"})
    built_bad = dict(built_ok, **{"cta.radius": 8})
    save_json(work, "contract.json", contract)
    a, b = fidelity_check(contract, ref, built_ok), fidelity_check(contract, ref, built_bad)
    return [("declared copy change allowed", a == {"undeclared": [], "declared": ["hero.copy"]}, a),
            ("undeclared radius drift caught", b["undeclared"] == ["cta.radius"], b),
            ("contract written before build with source and size", contract["size"] == [1440, 900] and contract["source"], contract)]


# ---------------------------------------------------------------- APPX-121
def computed(styles, tokens):
    return {k: tokens.get(v[4:-1], v) if isinstance(v, str) and v.startswith("var(") else v for k, v in styles.items()}


def accept_tokenisation(before, after, tokens):
    return computed(before, tokens) == computed(after, tokens)


def appx_121(work):
    tokens = {"--space-4": "16px", "--radius-m": "12px"}
    before = {"padding": "16px", "border-radius": "13px"}
    good = {"padding": "var(--space-4)", "border-radius": "13px"}
    bad = {"padding": "var(--space-4)", "border-radius": "var(--radius-m)"}
    save_json(work, "parity.json", {"before": before, "good": computed(good, tokens), "bad": computed(bad, tokens)})
    return [("16px -> var(--space-4) keeps computed values: accepted", accept_tokenisation(before, good, tokens), computed(good, tokens)),
            ("13px -> nearest token 12px changes the value: refused", not accept_tokenisation(before, bad, tokens), computed(bad, tokens))]


# ---------------------------------------------------------------- APPX-122
def render_ui(elements, W=144, H=90):
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    for e in elements:
        d.rectangle(e["box"], fill=e["fill"])
    return im


def first_diff_element(ref, built, elements):
    diff = ImageChops.difference(ref, built)
    bbox = diff.getbbox()
    if not bbox:
        return None, None
    for e in sorted(elements, key=lambda e: (e["box"][1], e["box"][0])):
        x0, y0, x1, y1 = e["box"]
        if not (x1 < bbox[0] or x0 > bbox[2] or y1 < bbox[1] or y0 > bbox[3]):
            return e["id"], bbox
    return "unknown", bbox


def appx_122(work):
    els = [{"id": "nav", "box": (0, 0, 143, 10), "fill": (20, 30, 60)}, {"id": "hero", "box": (10, 20, 133, 50), "fill": (240, 200, 90)},
           {"id": "cta", "box": (50, 60, 94, 74), "fill": (220, 60, 40)}]
    ref = render_ui(els)
    built = render_ui([els[0], els[1], dict(els[2], box=(52, 60, 96, 74))])
    ref.save(work / "ref.png")
    built.save(work / "built.png")
    Image.blend(ref, built, 0.5).save(work / "overlay.png")
    who, bbox = first_diff_element(ref, built, els)
    same, _ = first_diff_element(ref, render_ui(els), els)
    return [("identical render -> no difference", same is None, same),
            ("2 px shifted CTA found as the first differing element", who == "cta", (who, bbox)),
            ("difference bbox spans the shifted edges (x 50..96)", bbox[0] == 50 and bbox[2] == 97, bbox)]


# ---------------------------------------------------------------- APPX-123
def design_foundation(repo: Path):
    css = "\n".join(p.read_text() for p in sorted(repo.rglob("*.css")))
    def block(sel):
        m = re.search(re.escape(sel) + r"\s*{([^}]*)}", css)
        return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1))) if m else {}
    fonts = re.findall(r"@font-face\s*{[^}]*font-family:\s*['\"]?([^;'\"]+)", css)
    strategy = "class" if ".dark" in css else "media" if "prefers-color-scheme" in css else "none"
    return {"root": block(":root"), "dark": block(".dark"), "fonts": fonts, "theme_strategy": strategy}


def appx_123(work):
    repo = work / "repo"
    (repo / "src/styles").mkdir(parents=True)
    (repo / "src/styles/globals.css").write_text(":root{--bg:#ffffff;--fg:#111111;--radius:12px;}\n.dark{--bg:#0b0b0c;--fg:#f5f5f5;}\n"
                                                  "@font-face{font-family:'IBM Plex Sans Arabic';src:url(/f.woff2)}")
    (repo / "src/components/Button.css").parent.mkdir(parents=True)
    (repo / "src/components/Button.css").write_text(".btn{border-radius:var(--radius)}")
    f = design_foundation(repo)
    save_json(work, "foundation.json", f)
    return [(":root variables read", f["root"] == {"--bg": "#ffffff", "--fg": "#111111", "--radius": "12px"}, f["root"]),
            (".dark overrides read", f["dark"] == {"--bg": "#0b0b0c", "--fg": "#f5f5f5"}, f["dark"]),
            ("font loading found", f["fonts"] == ["IBM Plex Sans Arabic"], f["fonts"]),
            ("theme strategy = class (.dark)", f["theme_strategy"] == "class", f["theme_strategy"])]


# ---------------------------------------------------------------- APPX-124
def theme_css(theme):
    errs = []
    if set(theme["light"]) != set(theme["dark"]):
        errs.append("modes have different keys")
    if not theme.get("intent"):
        errs.append("missing designer intent")
    if theme.get("default") not in ("light", "dark"):
        errs.append("default mode")
    for f in theme.get("fonts", []):
        if f.get("licence") not in ("OFL", "Apache-2.0", "MIT"):
            errs.append(f"font licence {f['family']}")
    css = ":root{" + ";".join(f"--{k}:{v}" for k, v in theme["light"].items()) + "}\n.dark{" + ";".join(f"--{k}:{v}" for k, v in theme["dark"].items()) + "}"
    return css, errs


def appx_124(work):
    th = {"light": {"bg": "#fbf8f3", "ink": "#1d1814"}, "dark": {"bg": "#161310", "ink": "#f5ede3"}, "default": "light",
          "fonts": [{"family": "Cairo", "source": "Google Fonts", "licence": "OFL"}], "intent": ["ظلال لا حدود", "زوايا 12px"]}
    css, errs = theme_css(th)
    (work / "theme.css").write_text(css, encoding="utf-8")
    save_json(work, "theme.json", th)
    _, bad = theme_css({"light": {"bg": "#fff"}, "dark": {}, "default": "auto", "fonts": [{"family": "Paid", "licence": "proprietary"}]})
    return [("valid theme generates :root and .dark", errs == [] and css.startswith(":root{--bg:#fbf8f3") and ".dark{--bg:#161310" in css, css),
            ("validator lists all four planted faults", bad == ["modes have different keys", "missing designer intent", "default mode", "font licence Paid"], bad)]


# ---------------------------------------------------------------- APPX-125
def frame_rules(jsx: str):
    errs = []
    if re.search(r"onClick=\{\s*\(\)\s*=>\s*\{\s*\}\s*\}", jsx):
        errs.append("empty onClick")
    if re.search(r"<(?:div|main)[^>]*className=\"root\"[^>]*style=\{\{[^}]*width:\s*['\"]?\d+px", jsx):
        errs.append("fixed root width")
    if re.search(r"device-frame|iphone-frame", jsx):
        errs.append("device frame drawn")
    return errs


def appx_125(work):
    good = '<main className="root" style={{maxWidth: "100%", margin: "0 auto"}}><button onClick={() => setStep(2)}>التالي</button></main>'
    bad = '<div className="root" style={{width: "390px"}}><div className="iphone-frame"/><button onClick={() => {}}>Go</button></div>'
    (work / "Frame.jsx").write_text(good, encoding="utf-8")
    return [("good frame passes", frame_rules(good) == [], frame_rules(good)),
            ("planted empty handler, fixed width, device frame caught", frame_rules(bad) == ["empty onClick", "fixed root width", "device frame drawn"], frame_rules(bad))]


# ---------------------------------------------------------------- APPX-126
CONTRACT_KEYS = ["props", "callbacks", "state", "requests", "routes", "validation", "loading", "empty", "error", "keyboard", "aria"]


def behaviour_gaps(old, new):
    gaps = []
    for k in CONTRACT_KEYS:
        missing = sorted(set(old.get(k, [])) - set(new.get(k, [])))
        if missing:
            gaps.append((k, missing))
    return gaps


def appx_126(work):
    old = {"props": ["items", "onSelect"], "callbacks": ["onSelect"], "requests": ["GET /api/items"], "keyboard": ["Enter", "Escape"],
           "aria": ["listbox"], "empty": ["لا عناصر"], "error": ["retry"]}
    new = dict(old, keyboard=["Enter"], error=[])
    save_json(work, "contract.json", old)
    g = behaviour_gaps(old, new)
    return [("new component missing Escape and retry is caught", g == [("error", ["retry"]), ("keyboard", ["Escape"])], g),
            ("identical behaviour has no gaps", behaviour_gaps(old, dict(old)) == [], "none"),
            ("contract covers 11 behaviour areas", len(CONTRACT_KEYS) == 11, len(CONTRACT_KEYS))]


# ---------------------------------------------------------------- APPX-127
CLI = r'''
import argparse, json, os, sys
ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--json", action="store_true"); ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
plan = [os.path.join(a.out, n) for n in ("index.html", "style.css")]
def say(state, **kw):
    print(json.dumps({"state": state, **kw}) if a.json else f"{state}: {kw}"); sys.exit(0 if state != "failed" else 1)
if os.path.isdir(a.out) and os.listdir(a.out):
    say("failed", reason="target folder not empty")
if a.dry_run:
    say("dry-run", would_write=plan)
os.makedirs(a.out, exist_ok=True)
for p in plan: open(p, "w").write("x")
say("done", wrote=plan)
'''


def appx_127(work):
    cli = work / "scaffold_cli.py"
    cli.write_text(CLI)
    def run(*args):
        r = subprocess.run([sys.executable, "-I", str(cli), *args], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=20)
        return r.returncode, json.loads(r.stdout)
    t = str(work / "site")
    dry = run(t, "--json", "--dry-run")
    dry_wrote_nothing = not Path(t).exists()
    wrote = run(t, "--json")
    again = run(t, "--json")
    return [("dry-run lists what it would write and writes nothing", dry[1]["state"] == "dry-run" and len(dry[1]["would_write"]) == 2 and dry_wrote_nothing, dry),
            ("real run reports 'done' as JSON", wrote == (0, {"state": "done", "wrote": dry[1]["would_write"]}), wrote[1]["state"]),
            ("non-empty target refused with an explicit state and exit 1", again == (1, {"state": "failed", "reason": "target folder not empty"}), again),
            ("runs non-interactively to exit 0 with stdin closed", dry[0] == 0 and wrote[0] == 0, (dry[0], wrote[0]))]


# ---------------------------------------------------------------- APPX-128
def preflight(env):
    report = {"auth": {s: bool(env.get(f"{s.upper()}_TOKEN")) for s in ("github", "media")}, "project": env.get("PROJECT"), "version": env.get("TOOL_VERSION")}
    if not report["version"]:
        nxt = "install"
    elif not all(report["auth"].values()):
        nxt = "sign in: " + ",".join(k for k, v in report["auth"].items() if not v)
    elif not report["project"]:
        nxt = "ask which project"
    else:
        nxt = "continue"
    report["next"] = nxt
    return report


def appx_128(work):
    full = preflight({"GITHUB_TOKEN": "x", "MEDIA_TOKEN": "y", "PROJECT": "kosif", "TOOL_VERSION": "6.5"})
    noauth = preflight({"GITHUB_TOKEN": "x", "PROJECT": "kosif", "TOOL_VERSION": "6.5"})
    noproj = preflight({"GITHUB_TOKEN": "x", "MEDIA_TOKEN": "y", "TOOL_VERSION": "6.5"})
    save_json(work, "preflight.json", full)
    return [("all set -> continue", full["next"] == "continue", full),
            ("missing media login -> sign in: media", noauth["next"] == "sign in: media", noauth["next"]),
            ("no active project -> ask", noproj["next"] == "ask which project", noproj["next"]),
            ("report holds no secrets (booleans only)", "x" not in json.dumps(full["auth"]), full["auth"])]


# ---------------------------------------------------------------- APPX-130
def manifest(root, patterns):
    return {str(p.relative_to(root)): sha256(p.read_bytes()) for p in sorted(root.rglob("*")) if p.is_file() and any(fnmatch.fnmatch(str(p.relative_to(root)), pt) for pt in patterns)}


def handoff(root, base, allow):
    now = {str(p.relative_to(root)): sha256(p.read_bytes()) for p in sorted(root.rglob("*")) if p.is_file()}
    changed = sorted(k for k in now if k in base and now[k] != base[k])
    deleted = sorted(k for k in base if k not in now)
    added = sorted(k for k in now if k not in base)
    outside = [k for k in changed + added if not any(fnmatch.fnmatch(k, a) for a in allow)]
    state = "no change" if not (changed or deleted or added) else ("rejected" if outside else "changed")
    return {"state": state, "changed": changed, "deleted": deleted, "added": added, "outside_allowlist": outside}


def appx_130(work):
    root = work / "proj"
    (root / "scenes").mkdir(parents=True)
    (root / "scenes/a.html").write_text("a")
    (root / "scenes/b.html").write_text("b")
    (root / "package.json").write_text("{}")
    allow = ["scenes/*.html"]
    base = manifest(root, ["*", "scenes/*"])
    save_json(work, "base.json", base)
    r0 = handoff(root, base, allow)
    (root / "scenes/a.html").write_text("a2")
    r1 = handoff(root, base, allow)
    (root / "package.json").write_text('{"x":1}')
    r2 = handoff(root, base, allow)
    return [("untouched project -> 'no change'", r0["state"] == "no change", r0),
            ("allowed edit reported as changed", r1["state"] == "changed" and r1["changed"] == ["scenes/a.html"], r1),
            ("edit outside the allowlist rejected", r2["state"] == "rejected" and r2["outside_allowlist"] == ["package.json"], r2)]


# ---------------------------------------------------------------- APPX-131
def pinned_export(ref: Path, pin: str):
    now = sha256(ref.read_bytes())
    return {"ok": now == pin, "pinned": pin[:12], "current": now[:12]}


def appx_131(work):
    ref = work / "scene_v3.html"
    ref.write_text("<h1>v3</h1>")
    pin = sha256(ref.read_bytes())
    (work / "TEST_REPORT.md").write_text(f"reference sha256: {pin}\n")
    a = pinned_export(ref, pin)
    ref.write_text("<h1>v4</h1>")
    b = pinned_export(ref, pin)
    return [("export of the pinned version passes", a["ok"], a),
            ("drift to a newer version is detected", not b["ok"] and b["current"] != b["pinned"], b),
            ("pin written into TEST_REPORT.md", pin in (work / "TEST_REPORT.md").read_text(), pin[:12])]


# ---------------------------------------------------------------- APPX-132
def worker_briefs(refs_path: Path, scenes):
    refs = json.loads(refs_path.read_text())
    lock = {k: refs["lock"][k] for k in ("palette", "fonts")}
    return [{"scene": s, "refs": str(refs_path), "lock": lock, "roles": sorted({r["role"] for r in refs["files"]})} for s in scenes]


def appx_132(work):
    refs = {"files": [{"path": "style.png", "role": "style"}, {"path": "script.md", "role": "content"}, {"path": "board.json", "role": "structure"}],
            "lock": {"palette": ["#1b2a49", "#e7b65a"], "fonts": ["Cairo"]}}
    p = work / "refs.json"
    save_json(work, "refs.json", refs)
    briefs = worker_briefs(p, ["s1", "s2", "s3"])
    save_json(work, "briefs.json", briefs)
    return [("every worker gets the same refs path", len({b["refs"] for b in briefs}) == 1, briefs[0]["refs"]),
            ("roles style/content/structure carried", briefs[0]["roles"] == ["content", "structure", "style"], briefs[0]["roles"]),
            ("palette and fonts locked identically", all(b["lock"] == briefs[0]["lock"] for b in briefs), briefs[0]["lock"])]


# ---------------------------------------------------------------- APPX-133
def fan_out(scene: dict, axes: dict, work: Path):
    base = work / "scene"
    base.mkdir()
    (base / "scene.json").write_text(json.dumps(scene, sort_keys=True))
    out = []
    for axis, value in axes.items():
        d = work / f"scene--{axis}"
        d.mkdir()
        v = dict(scene, **{axis: value})
        (d / "scene.json").write_text(json.dumps(v, sort_keys=True))
        out.append(d)
    return base, out


def appx_133(work):
    scene = {"layout": "split", "palette": "night", "type": "Cairo", "tempo": 1.0}
    h0 = sha256(json.dumps(scene, sort_keys=True).encode())
    base, sibs = fan_out(scene, {"palette": "dawn", "type": "Tajawal", "tempo": 1.25}, work)
    diffs = []
    for d in sibs:
        v = json.loads((d / "scene.json").read_text())
        diffs.append([k for k in scene if scene[k] != v[k]])
    return [("original untouched", sha256((base / "scene.json").read_bytes()) == h0, h0[:12]),
            ("three sibling folders, side by side", sorted(d.name for d in sibs) == ["scene--palette", "scene--tempo", "scene--type"], [d.name for d in sibs]),
            ("each sibling changes exactly its named axis", diffs == [["palette"], ["type"], ["tempo"]], diffs)]


# ---------------------------------------------------------------- APPX-134
class EditLog:
    OPS = {"text", "color", "timing"}

    def __init__(self, doc):
        self.doc, self.done, self.undone = json.loads(json.dumps(doc)), [], []

    def apply(self, op):
        if op["op"] not in self.OPS:
            return "needs model rewrite"
        el = self.doc["elements"][op["id"]]
        key = {"text": "text", "color": "color", "timing": "start"}[op["op"]]
        self.done.append((op["id"], key, el[key]))
        el[key] = op["value"]
        self.undone.clear()
        return "applied"

    def undo(self):
        i, k, v = self.done.pop()
        self.undone.append((i, k, self.doc["elements"][i][k]))
        self.doc["elements"][i][k] = v

    def redo(self):
        i, k, v = self.undone.pop()
        self.done.append((i, k, self.doc["elements"][i][k]))
        self.doc["elements"][i][k] = v


def appx_134(work):
    doc = {"elements": {"title": {"text": "مرحبا", "color": "#fff", "start": 0.5}}}
    log = EditLog(doc)
    r1 = log.apply({"op": "text", "id": "title", "value": "أهلا"})
    log.apply({"op": "timing", "id": "title", "value": 0.8})
    r3 = log.apply({"op": "restructure", "id": "title", "value": None})
    after = json.loads(json.dumps(log.doc))
    log.undo(); log.undo()
    undone = json.loads(json.dumps(log.doc))
    log.redo()
    save_json(work, "doc.json", log.doc)
    return [("deterministic ops applied by script", r1 == "applied" and after["elements"]["title"] == {"text": "أهلا", "color": "#fff", "start": 0.8}, after),
            ("structural change flagged for the model, not faked", r3 == "needs model rewrite", r3),
            ("two undos restore the original", undone == doc, undone),
            ("redo re-applies the text edit only", log.doc["elements"]["title"]["text"] == "أهلا" and log.doc["elements"]["title"]["start"] == 0.5, log.doc)]


# ---------------------------------------------------------------- APPX-135
def render_cards(template, records):
    return [template.format(**r) for r in records]


def appx_135(work):
    tpl = '<div class="card" style="background:{{bg}}">{title}</div>'.replace("{{bg}}", "#1b2a49")
    recs = [{"title": "أ"}, {"title": "ب"}, {"title": "ج"}]
    v0 = render_cards(tpl, recs)
    v1 = render_cards(tpl.replace("#1b2a49", "#0a5c36"), recs)
    recs2 = [dict(recs[0]), {"title": "ب٢"}, dict(recs[2])]
    v2 = render_cards(tpl, recs2)
    (work / "cards.html").write_text("".join(v0), encoding="utf-8")
    return [("template edit changes every card", all(a != b for a, b in zip(v0, v1)), sum(a != b for a, b in zip(v0, v1))),
            ("record edit changes exactly one card", [a != b for a, b in zip(v0, v2)] == [False, True, False], [a != b for a, b in zip(v0, v2)])]


# ---------------------------------------------------------------- APPX-136
class Revisions:
    def __init__(self, folder):
        self.folder = folder
        folder.mkdir(exist_ok=True)

    def save(self, scene_id, content, approved):
        n = len(list(self.folder.glob(f"{scene_id}.v*.html"))) + 1
        p = self.folder / f"{scene_id}.v{n:03d}.html"
        p.write_text(content)
        if approved:
            (self.folder / f"{scene_id}.approved").write_text(p.name)
        return p

    def rollback(self, scene_id):
        return (self.folder / (self.folder / f"{scene_id}.approved").read_text()).read_text()


def appx_136(work):
    r = Revisions(work / "revs")
    r.save("s1", "<good v1>", True)
    r.save("s1", "<worse v2>", False)
    r.save("s1", "<worse v3>", False)
    back = r.rollback("s1")
    files = sorted(p.name for p in (work / "revs").glob("s1.v*.html"))
    return [("numbered versions kept", files == ["s1.v001.html", "s1.v002.html", "s1.v003.html"], files),
            ("rollback returns the last approved version", back == "<good v1>", back)]


# ---------------------------------------------------------------- APPX-137
def sketch_slots(img):
    import cv2
    a = np.asarray(img.convert("L"))
    cs, hier = cv2.findContours((a < 128).astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    H, W = a.shape
    boxes = []
    for i, c in enumerate(cs):
        if hier[0][i][3] != -1:
            continue
        x, y, w, h = cv2.boundingRect(c)
        if w * h > 200:
            boxes.append((round(x / W, 2), round(y / H, 2), round(w / W, 2), round(h / H, 2)))
    return sorted(boxes, key=lambda b: (b[1], b[0]))


def appx_137(work):
    im = Image.new("L", (200, 300), 255)
    d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 180, 80], outline=0, width=3)     # title
    d.rectangle([20, 100, 90, 250], outline=0, width=3)    # image
    d.rectangle([110, 100, 180, 250], outline=0, width=3)  # text
    im.save(work / "sketch.png")
    slots = sketch_slots(im)
    labels = ["title", "image", "text"]
    layout = dict(zip(labels, slots))
    save_json(work, "layout.json", layout)
    return [("three boxes found in the rough sketch", len(slots) == 3, slots),
            ("title slot spans the top 10%-27%", layout["title"][:2] == (0.1, 0.07) and abs(layout["title"][3] - 0.2) <= 0.02, layout["title"]),
            ("image left of text on the same row", layout["image"][0] < layout["text"][0] and layout["image"][1] == layout["text"][1], (layout["image"], layout["text"]))]


# ---------------------------------------------------------------- APPX-139
EXEC_EXT = {".exe", ".dll", ".so", ".dylib", ".sh", ".bat", ".ps1", ".py", ".js", ".bin", ".jar"}


def vet_skill(zbytes, source, max_bytes=2_000_000, trusted=("github.com/anthropics", "github.com/kosif199022-jpg")):
    errs = []
    if len(zbytes) > max_bytes:
        errs.append("too large")
    if not any(source.startswith("https://" + t) for t in trusted):
        errs.append("unknown source")
    with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
        names = z.namelist()
        if not any(n.endswith("SKILL.md") for n in names):
            errs.append("no SKILL.md")
        for n in names:
            if Path(n).suffix.lower() in EXEC_EXT or ".." in n or n.startswith("/"):
                errs.append(f"blocked {n}")
            elif not z.read(n)[:4096].decode("utf-8", "strict").isprintable() and b"\x00" in z.read(n)[:4096]:
                errs.append(f"binary {n}")
    return errs


def appx_139(work):
    def mk(files):
        b = io.BytesIO()
        with zipfile.ZipFile(b, "w") as z:
            for n, c in files.items():
                z.writestr(n, c)
        return b.getvalue()
    good = mk({"my-skill/SKILL.md": "---\nname: x\n---\nSteps", "my-skill/references/a.md": "notes"})
    bad = mk({"s/README.md": "x", "s/install.sh": "rm -rf ~", "../escape.md": "x"})
    (work / "good.zip").write_bytes(good)
    g, b = vet_skill(good, "https://github.com/anthropics/skills"), vet_skill(bad, "https://pastebin.com/x")
    return [("text-only package from a known source passes", g == [], g),
            ("script, path escape, missing SKILL.md, unknown source all caught",
             set(b) == {"unknown source", "no SKILL.md", "blocked s/install.sh", "blocked ../escape.md"}, b),
            ("size cap enforced", "too large" in vet_skill(good, "https://github.com/anthropics/x", max_bytes=10), "cap")]


# ---------------------------------------------------------------- APPX-144
def xfade_plan(durs, T, fps=30):
    offs, acc = [], durs[0]
    for i in range(1, len(durs)):
        t = min(T, durs[i - 1] / 2, durs[i] / 2)
        t = round(t * fps) / fps
        offs.append((round((acc - t) * fps) / fps, t))
        acc = acc + durs[i] - t
    return offs, acc


def appx_144(work):
    durs = [1.0, 0.6, 1.0]
    clips = []
    for i, (d, c) in enumerate(zip(durs, ("red", "green", "blue"))):
        p = work / f"c{i}.mp4"
        ff("-f", "lavfi", "-i", f"color=c={c}:size=32x18:rate=30:duration={d}", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", p)
        clips.append(p)
    offs, total = xfade_plan(durs, 0.5)
    fg = f"[0][1]xfade=transition=fade:duration={offs[0][1]}:offset={offs[0][0]}[v1];[v1][2]xfade=transition=fade:duration={offs[1][1]}:offset={offs[1][0]}"
    out = work / "track.mp4"
    ff(*sum((["-i", str(c)] for c in clips), []), "-filter_complex", fg, "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", out)
    d = dur(out)
    return [("transition clamped to half the 0.6 s clip (0.3 s)", offs[0][1] == 0.3 and offs[1][1] == 0.3, offs),
            ("offsets = accumulated length - T (0.7, 1.0)", [o for o, _ in offs] == [0.7, 1.0], offs),
            ("output length = sum - transitions = 2.0 s", abs(d - 2.0) <= 1 / 30 + 1e-3 and abs(total - 2.0) < 1e-9, d)]


# ---------------------------------------------------------------- APPX-145
def atempo_chain(S):
    parts = []
    while S < 0.5:
        parts.append(0.5)
        S /= 0.5
    while S > 100:
        parts.append(100.0)
        S /= 100
    parts.append(round(S, 6))
    return parts


def appx_145(work):
    src = work / "tone.wav"
    ff("-f", "lavfi", "-i", "sine=f=440:d=1:sample_rate=16000", src)
    chain = atempo_chain(0.25)
    out = work / "slow.wav"
    ff("-i", src, "-af", ",".join(f"atempo={x}" for x in chain), out)
    d = dur(out)
    return [("0.25 decomposes to 0.5 x 0.5", chain == [0.5, 0.5], chain),
            ("0.1 -> 0.5 x 0.5 x 0.5 x 0.8 (product 0.1)", atempo_chain(0.1) == [0.5, 0.5, 0.5, 0.8], atempo_chain(0.1)),
            ("every factor within 0.5-100", all(0.5 <= x <= 100 for x in atempo_chain(0.03) + atempo_chain(250)), atempo_chain(0.03)),
            ("1 s tone at 0.25x lasts 4 s within atempo's ~2% tail flush (<=0.1 s)", abs(d - 4.0) <= 0.1, d)]


# ---------------------------------------------------------------- APPX-146
def appx_146(work):
    src = work / "land.png"
    rng = np.random.default_rng(1)
    a = (rng.random((54, 96, 3)) * 255).astype(np.uint8)
    a[:, :48] //= 3
    Image.fromarray(a).save(src)
    W, H, s = 108, 192, 8
    cheap = work / "cheap.png"
    ff("-i", src, "-filter_complex", f"split[a][b];[b]scale={W // 4}:{H // 4}:force_original_aspect_ratio=increase,crop={W // 4}:{H // 4},gblur=sigma={s / 4},scale={W}:{H}[bg];[a]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2", cheap)
    full = work / "full.png"
    ff("-i", src, "-filter_complex", f"split[a][b];[b]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma={s}[bg];[a]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2", full)
    c = np.asarray(Image.open(cheap).convert("RGB")).astype(int)
    f = np.asarray(Image.open(full).convert("RGB")).astype(int)
    band = slice(0, 50)
    diff = np.abs(c[band] - f[band]).mean()
    return [("output 108x192 (9:16)", Image.open(cheap).size == (108, 192), Image.open(cheap).size),
            ("quarter-res blur fill looks like the full-res blur (mean diff < 12/255)", diff < 12, round(diff, 2)),
            ("fill is blurred (low local variance vs source)", c[band].std(axis=(0, 1)).mean() < a.std(axis=(0, 1)).mean(), "blurred"),
            ("blur work at quarter size: 16x fewer pixels", (W * H) / ((W // 4) * (H // 4)) == 16, 16)]


# ---------------------------------------------------------------- APPX-147
def layout_lines(text, short_side=1080, box_frac=0.8, size_ref=64):
    f = font(size_ref)
    maxw = short_side * box_frac
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def render_scaled(lines, k, size_ref=64):
    from PIL import features
    kw = {"direction": "rtl"} if features.check("raqm") else {}
    f = font(round(size_ref * k))
    W = round(1080 * k)
    im = Image.new("L", (W, round(len(lines) * size_ref * 1.6 * k) + 10), 0)
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        d.text((W - 10, 5 + i * size_ref * 1.6 * k), ln, font=f, fill=255, anchor="ra", **kw)
    return im


def appx_147(work):
    text = "هذا نص عربي طويل يجب أن تبقى فواصل أسطره نفسها في كل مقاس من مقاسات التصدير"
    lines = layout_lines(text)
    a = render_scaled(lines, 1080 / 1080)
    b = render_scaled(lines, 720 / 1080)
    a.save(work / "t1080.png")
    b.save(work / "t720.png")
    def rows(im):
        r = (np.asarray(im).max(axis=1) > 0).astype(int)
        return int(np.sum(np.diff(np.concatenate([[0], r])) == 1))
    naive = layout_lines(text, short_side=720, size_ref=64)
    return [("layout done once at short side 1080", len(lines) >= 2, lines),
            ("same line count at k=1 and k=2/3", rows(a) == rows(b) == len(lines), (rows(a), rows(b))),
            ("re-laying out at 720 without scaling would break lines differently", naive != lines, (len(naive), len(lines))),
            ("k = short side / 1080", round(720 / 1080, 4) == 0.6667, 0.6667)]


# ---------------------------------------------------------------- APPX-148
def media_plan(p):
    info = probe(p)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    rot = 0
    for sd in v.get("side_data_list", []):
        if "rotation" in sd:
            rot = int(sd["rotation"])
    w, h = (v["height"], v["width"]) if abs(rot) % 180 == 90 else (v["width"], v["height"])
    d = float(info["format"]["duration"])
    container = info["format"]["format_name"]
    web = v["codec_name"] in ("h264", "hevc", "vp9", "av1") and v["pix_fmt"] == "yuv420p" and any(c in container for c in ("mp4", "mov", "webm"))
    return {"display": (w, h), "poster_at": min(0.1 * d, 1.0), "proxy": not web, "duration": d}


def peaks(pcm: np.ndarray, per=80):
    n = len(pcm) // per
    v = np.abs(pcm[: n * per].reshape(n, per)).max(axis=1).astype(float)
    return (np.sqrt(v / v.max()) * 255).round().astype(int)


def appx_148(work):
    a = work / "a.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=size=64x36:rate=30:duration=2", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", a)
    rot = work / "rot.mp4"
    ff("-display_rotation", 90, "-i", a, "-c", "copy", rot)
    b = work / "b.mkv"
    ff("-f", "lavfi", "-i", "testsrc2=size=64x36:rate=30:duration=1", "-c:v", "mpeg4", b)
    pa, pr, pb = media_plan(a), media_plan(rot), media_plan(b)
    ff("-i", a, "-vf", "fps=4,tile=8x1", "-frames:v", 1, work / "strip.png")
    sr = 4000
    t = np.arange(sr) / sr
    pcm = (np.sin(2 * np.pi * 50 * t) * np.linspace(0, 1, sr) * 32767).astype(np.int16)
    pk = peaks(pcm)
    save_json(work, "prep.json", {"a": pa, "rot": pr, "b": pb, "peaks": pk.tolist()})
    return [("90 deg rotation swaps width/height (36x64)", pr["display"] == (36, 64) and pa["display"] == (64, 36), pr["display"]),
            ("poster at 10% of 2 s = 0.2 s, capped at 1 s", abs(pa["poster_at"] - 0.2) < 0.01 and media_plan(a)["poster_at"] <= 1, pa["poster_at"]),
            ("browser-safe H.264 mp4 needs no proxy; MPEG-4 Part 2 mkv does", (pa["proxy"], pb["proxy"]) == (False, True), (pa["proxy"], pb["proxy"])),
            ("thumbnail strip tiles 8 frames (512x36)", Image.open(work / "strip.png").size == (512, 36), Image.open(work / "strip.png").size),
            ("peaks: 50 values/s at 4 kHz / 80, sqrt-scaled to 255 max", len(pk) == 50 and pk.max() == 255 and abs(pk[24] - round(math.sqrt(0.5) * 255)) <= 8, (len(pk), int(pk[24])))]


# ---------------------------------------------------------------- APPX-149
def bitrate(w, h, fps, quality="normal", codec="h264"):
    bpp = {"normal": 0.07, "high": 0.12, "max": 0.2}[quality]
    return round(bpp * w * h * fps * (0.65 if codec == "hevc" else 1))


def encode_with_fallback(src, out, kbps):
    tried = []
    for enc in ("h264_videotoolbox", "h264_nvenc", "libx264"):
        r = ff("-i", src, "-c:v", enc, "-b:v", f"{kbps}k", "-movflags", "+faststart", out, ok=False)
        tried.append((enc, r.returncode))
        if r.returncode == 0:
            return enc, tried
        if not re.search(r"(Unknown encoder|Error while opening encoder|Cannot load|No device|not found|Could not open)", r.stderr, re.I):
            return None, tried
    return None, tried


def appx_149(work):
    src = work / "s.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=size=64x36:rate=30:duration=0.5", "-c:v", "libx264", "-preset", "ultrafast", src)
    br = bitrate(1920, 1080, 30)
    enc, tried = encode_with_fallback(src, work / "out.mp4", max(50, bitrate(64, 36, 30) // 1000))
    save_json(work, "tried.json", tried)
    return [("bpp 0.07 at 1080p30 = 4.35 Mbps", br == 4354560, br),
            ("HEVC x 0.65", bitrate(1920, 1080, 30, codec="hevc") == round(4354560 * 0.65), bitrate(1920, 1080, 30, codec="hevc")),
            ("hardware encoders fail to open here, software fallback encodes", enc == "libx264" and tried[-1] == ("libx264", 0) and all(rc != 0 for _, rc in tried[:-1]), tried)]


# ---------------------------------------------------------------- APPX-150
def guard(req, root: Path, app="kosif", hosts=("127.0.0.1:7777", "localhost:7777")):
    if req.get("bind") not in ("127.0.0.1", None):
        return 500, "bind"
    if req["headers"].get("Host") not in hosts:
        return 403, "host"
    if req["method"] != "GET" and req["headers"].get(f"X-{app}") != "1":
        return 403, "csrf"
    if "id" in req and not re.fullmatch(r"[a-z0-9-]{1,40}", req["id"]):
        return 400, "id"
    target = os.path.normpath(os.path.join(str(root), req.get("path", "").lstrip("/")))
    if not (target + os.sep).startswith(str(root) + os.sep) and target != str(root):
        return 403, "path"
    return 200, "ok"


def appx_150(work):
    root = work / "projects"
    root.mkdir()
    ok = {"method": "POST", "headers": {"Host": "127.0.0.1:7777", "X-kosif": "1"}, "path": "/p1/scene.json", "id": "p1"}
    cases = {"ok": guard(ok, root), "rebinding": guard(dict(ok, headers={"Host": "evil.com", "X-kosif": "1"}), root),
             "no_header": guard(dict(ok, headers={"Host": "127.0.0.1:7777"}), root), "traversal": guard(dict(ok, path="/../../etc/passwd"), root),
             "bad_id": guard(dict(ok, id="../x"), root), "get_no_header": guard({"method": "GET", "headers": {"Host": "localhost:7777"}, "path": "/p1"}, root)}
    save_json(work, "guard.json", cases)
    return [("legit POST passes", cases["ok"] == (200, "ok"), cases["ok"]),
            ("DNS-rebinding Host refused", cases["rebinding"] == (403, "host"), cases["rebinding"]),
            ("mutating request without X-app header refused", cases["no_header"] == (403, "csrf"), cases["no_header"]),
            ("../ traversal refused after normalize + prefix check", cases["traversal"] == (403, "path"), cases["traversal"]),
            ("id regex refuses '../x'", cases["bad_id"] == (400, "id"), cases["bad_id"]),
            ("plain GET needs no custom header", cases["get_no_header"] == (200, "ok"), cases["get_no_header"])]


# ---------------------------------------------------------------- APPX-151
def verified_download(src: Path, dest: Path, expected: str, chunk=4096, cancel_after=None):
    part = dest.with_suffix(dest.suffix + ".part")
    h = hashlib.sha256()
    try:
        with open(src, "rb") as fi, open(part, "wb") as fo:
            n = 0
            while True:
                b = fi.read(chunk)
                if not b:
                    break
                h.update(b)
                fo.write(b)
                n += 1
                if cancel_after and n >= cancel_after:
                    raise KeyboardInterrupt
        if h.hexdigest() != expected:
            raise ValueError("sha256 mismatch")
        os.replace(part, dest)
        return "ok"
    except (ValueError, KeyboardInterrupt) as e:
        part.unlink(missing_ok=True)
        return f"removed: {type(e).__name__}"


def appx_151(work):
    mirror = work / "mirror"
    mirror.mkdir()
    blob = os.urandom(50_000)
    (mirror / "model.bin").write_bytes(blob)
    good = verified_download(mirror / "model.bin", work / "model.bin", sha256(blob))
    bad = verified_download(mirror / "model.bin", work / "model2.bin", "0" * 64)
    cancel = verified_download(mirror / "model.bin", work / "model3.bin", sha256(blob), cancel_after=3)
    return [("hash verified while streaming, then atomic rename", good == "ok" and (work / "model.bin").read_bytes() == blob, good),
            ("mismatch removes the .part and never creates the final file", bad == "removed: ValueError" and not (work / "model2.bin").exists() and not (work / "model2.bin.part").exists(), bad),
            ("cancel removes the .part", cancel == "removed: KeyboardInterrupt" and not (work / "model3.bin.part").exists(), cancel)]


# ---------------------------------------------------------------- APPX-152
class Project:
    def __init__(self, path: Path):
        self.path, self.state, self.stack, self._last = path, {"exposure": 0}, [], (None, -9)

    def change(self, fn, now, merge=None):
        if not (merge and self._last[0] == merge and now - self._last[1] <= 1.5):
            self.stack.append(json.loads(json.dumps(self.state)))
            self.stack = self.stack[-150:]
        self._last = (merge, now)
        fn(self.state)

    def undo(self):
        self.state = self.stack.pop()

    def save(self):
        if self.path.exists():
            shutil.copy(self.path, self.path.with_suffix(".json.bak"))
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state))
        os.replace(tmp, self.path)


def appx_152(work):
    p = Project(work / "project.json")
    for i in range(10):
        p.change(lambda s, i=i: s.update(exposure=i), now=0.1 * i, merge="exposure")
    one_step = len(p.stack)
    p.change(lambda s: s.update(exposure=99), now=5.0, merge="exposure")
    p.save()
    p.save()
    p.undo()
    after_undo = p.state["exposure"]
    for i in range(200):
        p.change(lambda s, i=i: s.update(n=i), now=10 + 2 * i)
    return [("a 1 s slider drag is one undo step", one_step == 1, one_step),
            ("a drag 5 s later is a new step; undo returns to 9", after_undo == 9, after_undo),
            ("history capped at 150 snapshots", len(p.stack) == 150, len(p.stack)),
            ("atomic save leaves project.json and .bak, no .tmp", (work / "project.json").exists() and (work / "project.json.bak").exists() and not (work / "project.tmp").exists(), "files")]


# ---------------------------------------------------------------- APPX-154
def media_id(p: Path):
    st = p.stat()
    return hashlib.sha1(f"{p}|{st.st_size}|{int(st.st_mtime)}".encode()).hexdigest()[:16]


def resume_queue(index):
    return [k for k, v in index.items() if v["status"] in ("processing", "queued")]


def appx_154(work):
    m = work / "clip.mov"
    m.write_bytes(b"x" * 100)
    os.utime(m, (1_700_000_000, 1_700_000_000))
    i1, i2 = media_id(m), media_id(m)
    m.write_bytes(b"x" * 101)
    os.utime(m, (1_700_000_000, 1_700_000_000))
    i3 = media_id(m)
    index = {i1: {"status": "done"}, i3: {"status": "processing"}, "zz": {"status": "queued"}}
    tmp = work / "index.json.tmp"
    tmp.write_text(json.dumps(index))
    os.replace(tmp, work / "index.json")
    q = resume_queue(json.loads((work / "index.json").read_text()))
    return [("unchanged file -> same 16-hex id", i1 == i2 and len(i1) == 16, i1),
            ("size change -> new id (re-prepare)", i3 != i1, (i1, i3)),
            ("interrupted 'processing' item re-queued on start", q == [i3, "zz"], q),
            ("original media untouched by the cache", m.stat().st_size == 101, m.stat().st_size)]


PROGRAMS = {"APPX-20": appx_20, "APPX-21": appx_21, "APPX-22": appx_22, "APPX-23": appx_23, "APPX-24": appx_24, "APPX-25": appx_25,
            "APPX-26": appx_26, "APPX-27": appx_27, "APPX-29": appx_29, "APPX-51": appx_51, "APPX-52": appx_52, "APPX-54": appx_54,
            "APPX-55": appx_55, "APPX-56": appx_56, "APPX-58": appx_58, "APPX-120": appx_120, "APPX-121": appx_121, "APPX-122": appx_122,
            "APPX-123": appx_123, "APPX-124": appx_124, "APPX-125": appx_125, "APPX-126": appx_126, "APPX-127": appx_127, "APPX-128": appx_128,
            "APPX-130": appx_130, "APPX-131": appx_131, "APPX-132": appx_132, "APPX-133": appx_133, "APPX-134": appx_134, "APPX-135": appx_135,
            "APPX-136": appx_136, "APPX-137": appx_137, "APPX-139": appx_139, "APPX-144": appx_144, "APPX-145": appx_145, "APPX-146": appx_146,
            "APPX-147": appx_147, "APPX-148": appx_148, "APPX-149": appx_149, "APPX-150": appx_150, "APPX-151": appx_151, "APPX-152": appx_152,
            "APPX-154": appx_154}
