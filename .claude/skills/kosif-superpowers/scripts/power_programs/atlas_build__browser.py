"""Wave-2 browser programs for atlas-build (ABUILD-*).

A small local web app is written into the work folder and served at https://kosif.test/ in
Playwright Chromium (every other http(s) request aborted). Each program drives the card's browser
workflow on it (acceptance checks with a fix loop, accessibility-ref loops, frozen-manifest
cloning, CDP debugging, throwaway profiles, named sessions, E2E with mocks and web vitals,
hidden file inputs, pass/fail/blocked proofs, three-width QA, design DNA, keyboard tests) and
checks known answers planted in the fixture: the bug the loop must fix, the ref that moves, the
overflow at 375 px, the element without a focus ring.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

from ._browser_common import browser, img, page, sha

APP_CSS = """body{margin:0;font:16px sans-serif;background:#fafafa;color:#222}
header{background:#123456;color:#fff;padding:8px}nav a{color:#fff;margin-right:12px}
.btn{background:#e7b65a;border:0;border-radius:6px;padding:10px 16px;box-shadow:0 2px 4px rgba(0,0,0,.25);transition:transform .2s ease}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px}#modal{display:none;position:fixed;inset:20px;background:#fff;border:1px solid #333}
#modal.open{display:block}"""


def app_html(total="$30", extra_body="", title="Checkout"):
    return f"""<!doctype html><html lang="en"><head><meta charset=utf-8><title>{title}</title><style>{APP_CSS}</style></head><body>
<a class="skip" href="#main" id="skip">Skip to content</a>
<header><nav><a href="#a" id="nav1">Shop</a><a href="#b" id="nav2">Cart</a></nav></header>
<main id="main"><h1>{title}</h1><ul id="items"></ul><label for="qty">Quantity</label><input id="qty" value="3">
<p id="total">{total}</p><button class="btn" id="add">Add item</button><button class="btn" id="checkout">Checkout</button>
<button class="btn" id="open">Open dialog</button>
<div id="modal" role="dialog" aria-modal="true"><button id="m1">OK</button><button id="m2">Cancel</button></div>
{extra_body}</main>
<script>
document.getElementById('add').onclick=()=>{{const b=document.createElement('button');b.textContent='Remove '+(document.querySelectorAll('#items button').length+1);
const li=document.createElement('li');li.appendChild(b);document.getElementById('items').prepend(li);}};
const modal=document.getElementById('modal'),opener=document.getElementById('open');
opener.onclick=()=>{{modal.classList.add('open');document.getElementById('m1').focus();}};
modal.addEventListener('keydown',e=>{{const f=[...modal.querySelectorAll('button')];if(e.key==='Tab'){{e.preventDefault();const i=f.indexOf(document.activeElement);
f[(i+(e.shiftKey?-1:1)+f.length)%f.length].focus();}}if(e.key==='Escape'){{modal.classList.remove('open');opener.focus();}}}});
document.getElementById('checkout').onclick=()=>{{document.body.dataset.step='checkout';}};
</script></body></html>"""


def serve_app(work: Path, **kw) -> str:
    (work / "app").mkdir(exist_ok=True)
    (work / "app" / "index.html").write_text(app_html(**kw), encoding="utf-8")
    return "/app/index.html"


# ---------------------------------------------------------------- ABUILD-08

ACS = [("AC1", "title says Checkout", "document.querySelector('h1').textContent==='Checkout'"),
       ("AC2", "checkout button is enabled", "!document.getElementById('checkout').disabled"),
       ("AC3", "total for 3 x $10 shows $30", "document.getElementById('total').textContent==='$30'")]


def evaluate_prototype(work: Path, ticket: str, url: str, fix):
    if not ticket or not re.fullmatch(r"[A-Z]+-\d+", ticket):
        raise ValueError("a ticket key like KOS-12 is required")
    iterations = []
    for it in range(1, 4):
        r = browser(work, {"steps": [{"op": "goto", "url": url}] + [{"op": "eval", "js": js, "as": aid} for aid, _, js in ACS]}, name=f"ac{it}")
        verdict = {aid: ("PASS" if r["values"][aid] else "FAIL") for aid, _, _ in ACS}
        iterations.append(verdict)
        fails = [a for a, v in verdict.items() if v == "FAIL"]
        if not fails:
            break
        fix(fails)
    persona = [("first-time buyer", "I look for the button to add an item", "#add"), ("first-time buyer", "Now I go to checkout", "#checkout")]
    steps = [{"op": "goto", "url": url}]
    for i, (_, _, sel) in enumerate(persona):
        steps += [{"op": "click", "selector": sel}, {"op": "shot", "path": str(work / f"persona_{i + 1}.png")}]
    steps.append({"op": "eval", "js": "document.body.dataset.step||''", "as": "step"})
    pb = browser(work, {"steps": steps}, name="persona")
    with open(work / "evaluation-report.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ticket", "iteration", "criterion", "verdict"])
        for i, v in enumerate(iterations, 1):
            for a, s in v.items():
                w.writerow([ticket, i, a, s])
    rows = "".join(f"<tr><td>{a}</td><td>{d}</td><td>{iterations[-1][a]}</td></tr>" for a, d, _ in ACS)
    trace = "".join(f"<li>{p}: “{t}” <img src='persona_{i + 1}.png' width=160></li>" for i, (p, t, _) in enumerate(persona))
    (work / "evaluation-report.html").write_text(f"<html><body><h1>{ticket}</h1><table>{rows}</table><ol>{trace}</ol></body></html>")
    return iterations, pb


def abuild_08(work: Path):
    """Prototype evaluation vs acceptance criteria: AC verdicts with a fix loop, persona walkthrough, HTML + CSV evidence."""
    url = serve_app(work, total="$20")                       # planted bug: AC3 fails on the first pass
    def fix(fails):
        if "AC3" in fails:
            (work / "app" / "index.html").write_text(app_html(total="$30"), encoding="utf-8")
    its, pb = evaluate_prototype(work, "KOS-12", url, fix)
    try:
        evaluate_prototype(work, "", url, fix)
        refused = False
    except ValueError:
        refused = True
    rows = list(csv.DictReader(open(work / "evaluation-report.csv")))
    html = (work / "evaluation-report.html").read_text()
    return [("first pass: AC3 FAIL, AC1/AC2 PASS", its[0] == {"AC1": "PASS", "AC2": "PASS", "AC3": "FAIL"}, str(its[0])),
            ("fix loop: second pass all PASS", len(its) == 2 and set(its[1].values()) == {"PASS"}, str(its)),
            ("CSV logs 2 iterations x 3 criteria", len(rows) == 6 and rows[2]["verdict"] == "FAIL", str(len(rows))),
            ("persona walkthrough reached checkout", pb["values"]["step"] == "checkout", pb["values"]["step"]),
            ("report embeds 2 walkthrough screenshots", html.count("<img") == 2 and all((work / f"persona_{i}.png").stat().st_size > 0 for i in (1, 2)), ""),
            ("no ticket key -> refused", refused, str(refused))]


# ---------------------------------------------------------------- ABUILD-14

SNAP_JS = """((cap)=>{const els=[...document.querySelectorAll('a[href],button,input,select,textarea,[role=button]')].filter(e=>e.offsetParent!==null||e.getClientRects().length);
window.__refs={};const lines=els.map((e,i)=>{const r='e'+(i+1);window.__refs[r]=e;const name=(e.getAttribute('aria-label')||e.textContent||e.value||e.id||'').trim();
return `${r} ${e.tagName.toLowerCase()} "${name}"`});let out=lines.join('\\n');return out.length>cap?out.slice(0,cap)+'\\n[truncated]':out})"""


def abuild_14(work: Path):
    """Accessibility-ref loop: snapshot interactive elements with refs, act by ref, re-snapshot after DOM changes, capped output."""
    url = serve_app(work)
    act = "((ref)=>{const e=window.__refs[ref];const n=(e.textContent||e.id).trim();e.click();return n})"
    r = browser(work, {"steps": [
        {"op": "goto", "url": url},
        {"op": "eval", "js": SNAP_JS + "(2000)", "as": "s1"},
        {"op": "eval", "js": "(()=>{const k=Object.keys(window.__refs).find(k=>window.__refs[k].id==='add');return k})()", "as": "addRef"},
        {"op": "eval", "js": "(()=>{const k=Object.keys(window.__refs).find(k=>window.__refs[k].id==='add');window.__refs[k].click();window.__refs[k].click();return true})()"},
        {"op": "eval", "js": SNAP_JS + "(2000)", "as": "s2"},
        {"op": "eval", "js": SNAP_JS + "(60)", "as": "capped"},
        {"op": "text", "selector": "main", "cap": 40, "as": "txt"}]})
    v = r["values"]
    s1, s2 = v["s1"].splitlines(), v["s2"].splitlines()
    ref_of = lambda lines, word: next((l.split()[0] for l in lines if f'"{word}"' in l), None)
    # the planted move: two 'Remove' buttons were inserted, so refs after them shift by two
    return [("snapshot lists interactive elements with refs", s1[0].startswith("e1 a") and any('"Checkout"' in l for l in s1), s1[0]),
            ("Checkout ref moved after the DOM change", ref_of(s1, "Checkout") != ref_of(s2, "Checkout"), f"{ref_of(s1, 'Checkout')} -> {ref_of(s2, 'Checkout')}"),
            ("re-snapshot shows the two new buttons", sum('"Remove' in l for l in s2) == 2, str([l for l in s2 if 'Remove' in l])),
            ("old ref now names a different element", s2[int(ref_of(s1, "Checkout")[1:]) - 1] != s1[int(ref_of(s1, "Checkout")[1:]) - 1],
             s2[int(ref_of(s1, "Checkout")[1:]) - 1]),
            ("bounded output: capped at 60 chars + marker", len(v["capped"]) <= 60 + len("\n[truncated]") and v["capped"].endswith("[truncated]"), str(len(v["capped"]))),
            ("text read with a size cap (40)", len(v["txt"]) == 40, str(len(v["txt"])))]


# ---------------------------------------------------------------- ABUILD-15

SOURCE = """<!doctype html><html><head><meta charset=utf-8><style>body{margin:0;background:#f4efe6}
#hero{position:absolute;left:10px;top:10px;width:100px;height:40px;background:#c0392b;border-radius:8px}
#cta{position:absolute;left:10px;top:60px;width:60px;height:20px;background:#2c3e50}
#side{position:absolute;left:130px;top:10px;width:50px;height:70px;background:#16a085}</style></head>
<body><div id="hero"></div><div id="cta"></div><div id="side"></div></body></html>"""
EXTRACT_JS = """[...document.querySelectorAll('body *')].filter(e=>e.id).map(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);
return {id:e.id,x:r.x,y:r.y,w:r.width,h:r.height,bg:c.backgroundColor,radius:c.borderRadius}}).concat([{id:'body',bg:getComputedStyle(document.body).backgroundColor}])"""


def build_clone(manifest: dict, props: set) -> str:
    """Build the clone only from the frozen manifest, with the properties the gap loop has enabled."""
    css, body = [], []
    for el in manifest["elements"]:
        if el["id"] == "body":
            if "background" in props:
                css.append(f"body{{background:{el['bg']}}}")
            continue
        rule = f"#{el['id']}{{position:absolute;left:{el['x']}px;top:{el['y']}px;width:{el['w']}px;height:{el['h']}px"
        if "background" in props:
            rule += f";background:{el['bg']}"
        if "radius" in props:
            rule += f";border-radius:{el['radius']}"
        css.append(rule + "}")
        body.append(f"<div id='{el['id']}'></div>")
    return f"<!doctype html><html><head><style>body{{margin:0}}{''.join(css)}</style></head><body>{''.join(body)}</body></html>"


def abuild_15(work: Path):
    """Browser-evidence clone: capture with a real browser, freeze the manifest, build only from it, visual gap loop."""
    page(work, "source.html", SOURCE)
    vp = {"width": 200, "height": 100}
    r = browser(work, {"context": {"viewport": vp}, "steps": [{"op": "goto", "url": "/source.html"}, {"op": "eval", "js": EXTRACT_JS, "as": "m"},
                                                              {"op": "shot", "path": str(work / "first_viewport.png")}]}, name="capture")
    manifest = {"source": "/source.html", "viewport": vp, "elements": r["values"]["m"]}
    mf = work / "extraction_manifest.json"
    mf.write_text(json.dumps(manifest, indent=1, sort_keys=True))
    frozen = sha(mf)
    src = img(work / "first_viewport.png")
    props, diffs, plan = set(), [], ["background", "radius"]
    status = "done_with_gaps"
    for it in range(4):
        page(work, f"clone_{it}.html", build_clone(json.loads(mf.read_text()), props))
        browser(work, {"context": {"viewport": vp}, "steps": [{"op": "goto", "url": f"/clone_{it}.html"},
                                                              {"op": "shot", "path": str(work / f"clone_{it}.png")}]}, name=f"clone{it}")
        d = float(np.abs(img(work / f"clone_{it}.png") - src).mean())
        diffs.append(round(d, 3))
        if d < 0.05:
            status = "accepted"
            break
        if plan:
            props.add(plan.pop(0))
    return [("manifest captured 3 elements + body from the real browser", len(manifest["elements"]) == 4 and manifest["elements"][0]["bg"] == "rgb(192, 57, 43)", str(manifest["elements"][0])),
            ("frozen manifest unchanged by the build", sha(mf) == frozen, frozen[:12]),
            ("gap loop lowers the visual diff each round", all(a > b for a, b in zip(diffs, diffs[1:])), str(diffs)),
            ("clone accepted (diff < 0.05) after adding background and radius", status == "accepted" and props == {"background", "radius"}, f"{status} {sorted(props)}"),
            ("three rounds: boxes, colours, radii", len(diffs) == 3, str(diffs))]


# ---------------------------------------------------------------- ABUILD-16

BUGGY = """<!doctype html><html><body><button id="go">Go</button><p id="out"></p><script>
console.error('config missing: API_BASE');fetch('/api/missing').then(r=>document.getElementById('out').textContent='status '+r.status);
document.getElementById('go').onclick=()=>{const cfg=undefined;document.getElementById('out').textContent=cfg.name;};</script></body></html>"""
FIXED = """<!doctype html><html><body><button id="go">Go</button><p id="out"></p><script>
fetch('/api/ok.json').then(r=>r.json()).then(j=>document.getElementById('out').textContent=j.name);
document.getElementById('go').onclick=()=>{document.getElementById('out').textContent='clicked';};</script></body></html>"""


def cdp_debug(work: Path, name: str):
    r = browser(work, {"cdp": True, "context": {"viewport": {"width": 320, "height": 200}}, "steps": [
        {"op": "cdpSend", "method": "Emulation.setDeviceMetricsOverride", "params": {"width": 320, "height": 200, "deviceScaleFactor": 1, "mobile": False}},
        {"op": "goto", "url": "/debug.html"}, {"op": "eval", "js": "new Promise(r=>setTimeout(r,150))"},
        {"op": "shot", "path": str(work / f"{name}_before.png")},
        {"op": "click", "selector": "#go"}, {"op": "eval", "js": "new Promise(r=>setTimeout(r,100))"},
        {"op": "shot", "path": str(work / f"{name}_after.png")},
        {"op": "cdpSend", "method": "Runtime.evaluate", "params": {"expression": "innerWidth", "returnByValue": True}, "as": "w"}]}, name=name)
    ev = r["cdpEvents"]
    return {"console_errors": [e["text"] for e in ev if e["kind"] == "console" and e["level"] == "error"],
            "exceptions": [e["text"] for e in ev if e["kind"] == "exception"],
            "bad_responses": [(e["url"].rsplit("/", 1)[-1], e["status"]) for e in ev if e["kind"] == "response" and e["status"] >= 400],
            "width": r["values"]["w"]["result"]["value"]}


def abuild_16(work: Path):
    """Chrome DevTools Protocol debugging: console, network and exceptions via a CDP session; reproduce, fix, reload, re-verify."""
    (work / "api").mkdir()
    (work / "api" / "ok.json").write_text('{"name":"ok"}')
    page(work, "debug.html", BUGGY)
    before = cdp_debug(work, "buggy")
    page(work, "debug.html", FIXED)
    after = cdp_debug(work, "fixed")
    (work / "cdp_report.json").write_text(json.dumps({"before": before, "after": after}, indent=1))
    return [("CDP saw the planted console error", before["console_errors"] == ["config missing: API_BASE"], str(before["console_errors"])),
            ("CDP saw the 404 request", ("missing", 404) in before["bad_responses"], str(before["bad_responses"])),
            ("click reproduced the TypeError", any("TypeError" in (x or "") for x in before["exceptions"]), str(before["exceptions"])[:120]),
            ("viewport emulated through CDP (320)", before["width"] == 320, str(before["width"])),
            ("after the fix: no errors, no exceptions, no 4xx", not after["console_errors"] and not after["exceptions"] and not after["bad_responses"], str(after)),
            ("before/after screenshots differ", sha(work / "buggy_after.png") != sha(work / "fixed_after.png"), "")]


# ---------------------------------------------------------------- ABUILD-18

def driver(work: Path, inst: str, commands: list):
    """One-line commands -> steps in a throwaway profile (open/text/click/eval/wait/screenshot/close)."""
    prof = work / "profiles" / inst
    prof.mkdir(parents=True)
    steps = []
    for c in commands:
        op, _, arg = c.partition(" ")
        if op == "open":
            steps.append({"op": "goto", "url": arg})
        elif op == "text":
            steps.append({"op": "text", "selector": arg, "as": f"text:{arg}"})
        elif op == "click":
            steps.append({"op": "click", "selector": arg})
        elif op == "eval":
            steps.append({"op": "eval", "js": arg, "as": f"eval:{arg}"})
        elif op == "wait":
            steps.append({"op": "wait", "js": arg, "timeout": 3000})
        elif op == "screenshot":
            full = arg.endswith("--full")
            steps.append({"op": "shot", "path": str(work / arg.split()[0]), "fullPage": full})
        elif op == "close":
            pass
        else:
            raise ValueError(f"unknown command {op}")
    r = browser(work, {"persistent": str(prof), "context": {"viewport": {"width": 300, "height": 200}}, "steps": steps}, name=f"drv_{inst}")
    had_files = sum(1 for _ in prof.rglob("*"))
    if commands[-1] == "close":
        shutil.rmtree(prof)
    return r, had_files, prof


def abuild_18(work: Path):
    """Isolated headless Chrome over CDP with throwaway profiles: open/text/click/eval/wait/screenshot --full/close; --id instances."""
    url = serve_app(work, extra_body="<div style='height:900px'></div>")
    a, files_a, prof_a = driver(work, "a", [f"open {url}", "text h1", "click #add", "wait document.querySelectorAll('#items button').length===1", "eval document.querySelectorAll('#items button').length",
                                           "eval localStorage.setItem('k','A'), localStorage.getItem('k')", "screenshot full.png --full", "close"])
    b, files_b, prof_b = driver(work, "b", [f"open {url}", "eval localStorage.getItem('k')", "close"])
    full = Image.open(work / "full.png").size
    return [("text h1 = Checkout", a["values"]["text:h1"] == "Checkout", a["values"]["text:h1"]),
            ("click + wait expression saw the new item", a["values"]["eval:document.querySelectorAll('#items button').length"] == 1, ""),
            ("eval returned a value", a["values"]["eval:localStorage.setItem('k','A'), localStorage.getItem('k')"] == "A", ""),
            ("screenshot --full is taller than the 200 px viewport", full[1] > 900, str(full)),
            ("each instance got its own profile (--id): b does not see a's storage", b["values"]["eval:localStorage.getItem('k')"] is None, str(b["values"])),
            ("the profile was real (files written)", files_a > 3, str(files_a)),
            ("close deleted the throwaway profiles", not prof_a.exists() and not prof_b.exists(), "")]


# ---------------------------------------------------------------- ABUILD-19

def session(work: Path, name: str, url: str, actions: list) -> dict:
    """Named session writing snapshot YAML, screenshots and console log to .playwright-cli/<name>/, returning only paths."""
    d = work / ".playwright-cli" / name
    d.mkdir(parents=True, exist_ok=True)
    steps = [{"op": "goto", "url": url}, {"op": "aria", "selector": "body", "path": str(d / "snapshot.yml")}]
    for a in actions:
        steps.append({"op": "click", "selector": a})
    steps += [{"op": "aria", "selector": "body", "path": str(d / "snapshot-after.yml")},
              {"op": "shot", "path": str(d / f"{name}-after-clicks.png")}]
    r = browser(work, {"steps": steps}, name=f"sess_{name}")
    errors = [c["text"] for c in r["console"] if c["type"] == "error"] + r["pageErrors"]
    (d / "console.json").write_text(json.dumps({"errors": len(errors), "first": errors[:3]}))
    gi = work / ".gitignore"
    if ".playwright-cli/" not in (gi.read_text() if gi.exists() else ""):
        gi.write_text((gi.read_text() if gi.exists() else "") + ".playwright-cli/\n")
    return {"snapshot": str(d / "snapshot.yml"), "after": str(d / "snapshot-after.yml"), "screenshot": str(d / f"{name}-after-clicks.png"),
            "console": str(d / "console.json")}


def abuild_19(work: Path):
    """Named-session Playwright CLI: artifacts on disk, only paths returned; snapshot refs, descriptive screenshot names, console summary."""
    url = serve_app(work, extra_body="<script>console.error('planted: widget failed')</script>")
    out = session(work, "checkout-flow", url, ["#add", "#checkout"])
    snap = Path(out["snapshot"]).read_text()
    after = Path(out["after"]).read_text()
    con = json.loads(Path(out["console"]).read_text())
    return [("returned only file paths", all(isinstance(v, str) and Path(v).is_file() for v in out.values()), json.dumps(out)[:120]),
            ("snapshot YAML lists the buttons by role and name", 'button "Checkout"' in snap and 'button "Add item"' in snap, snap[:120]),
            ("after-click snapshot shows the new Remove 1 button", 'button "Remove 1"' in after and 'Remove 1' not in snap, ""),
            ("descriptive screenshot filename", Path(out["screenshot"]).name == "checkout-flow-after-clicks.png", Path(out["screenshot"]).name),
            ("console summary counted the planted error", con["errors"] == 1 and "planted" in con["first"][0], str(con)),
            (".playwright-cli/ gitignored", ".playwright-cli/" in (work / ".gitignore").read_text(), "")]


# ---------------------------------------------------------------- ABUILD-20

A11Y_JS = """(()=>{const v=[];document.querySelectorAll('img').forEach(i=>{if(!i.hasAttribute('alt'))v.push({rule:'image-alt',el:i.id})});
document.querySelectorAll('input:not([type=hidden])').forEach(i=>{const l=i.id&&document.querySelector(`label[for="${i.id}"]`);if(!l&&!i.getAttribute('aria-label'))v.push({rule:'label',el:i.id})});
document.querySelectorAll('button').forEach(b=>{if(!(b.textContent.trim()||b.getAttribute('aria-label')))v.push({rule:'button-name',el:b.id})});return v})()"""
CWV_INIT = """window.__cwv={lcp:0,cls:0};new PerformanceObserver(l=>{for(const e of l.getEntries())window.__cwv.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});
new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cwv.cls+=e.value}).observe({type:'layout-shift',buffered:true});"""
CWV_READ = "new Promise(r=>setTimeout(()=>{const n=performance.getEntriesByType('navigation')[0];r({lcp:window.__cwv.lcp,cls:Math.round(window.__cwv.cls*1000)/1000,ttfb:n?n.responseStart:null})},700))"


class CheckoutPage:
    """Page Object: selectors and actions for the checkout page in one place."""
    url = "/shop.html"
    name = "#user"

    @staticmethod
    def open_steps():
        return [{"op": "goto", "url": CheckoutPage.url}]


def scan(work: Path, name: str, state=None, save=None):
    ctx = {"viewport": {"width": 400, "height": 300}}
    if state:
        ctx["storageState"] = str(state)
    steps = CheckoutPage.open_steps() + [{"op": "wait", "js": f"document.querySelector('{CheckoutPage.name}').textContent!==''"},
                                         {"op": "text", "selector": CheckoutPage.name, "as": "user"},
                                         {"op": "eval", "js": A11Y_JS, "as": "a11y"}, {"op": "eval", "js": CWV_READ, "as": "cwv"}]
    if save:
        steps = [{"op": "goto", "url": "/login.html"}, {"op": "eval", "js": "localStorage.setItem('token','t-123'), true"},
                 {"op": "saveState", "path": str(save)}] + steps
    r = browser(work, {"initScripts": [CWV_INIT], "context": ctx, "steps": steps}, name=name)
    v = r["values"]
    poor = v["cwv"]["cls"] > 0.25 or v["cwv"]["lcp"] > 4000
    result = {"user": v["user"], "violations": v["a11y"], "cwv": v["cwv"], "exit": 1 if (v["a11y"] or poor) else 0}
    (work / f"{name}.json").write_text(json.dumps(result))
    return result, r


SHOP = """<!doctype html><html><body style="margin:0"><p id="user"></p>IMGS<input id="q"LABEL><button id="b">Buy</button><div id="late"></div><script>
fetch('/api/user').then(r=>r.json()).then(j=>{document.getElementById('user').textContent=(localStorage.getItem('token')?'signed-in ':'guest ')+j.name;});
SHIFT</script></body></html>"""


def abuild_20(work: Path):
    """Playwright E2E: Page Object, auth state reuse, API mocks, a scripted a11y rule scan and Core Web Vitals with fail-on-poor."""
    (work / "api").mkdir()
    (work / "api" / "user").write_text('{"name":"Mock Mona"}')   # the API mock served for /api/user
    page(work, "login.html", "<!doctype html><html><body>login</body></html>")
    bad = SHOP.replace("IMGS", "<img id='hero' src='data:image/gif;base64,R0lGODlhAQABAAAAACw='>").replace("LABEL", "") \
        .replace("SHIFT", "setTimeout(()=>{const d=document.getElementById('late');d.style.height='400px';document.body.prepend(d)},100);")
    page(work, "shop.html", bad)
    state = work / "auth.json"
    r1, _ = scan(work, "bad_run", save=state)
    good = SHOP.replace("IMGS", "<img id='hero' alt='Hero' src='data:image/gif;base64,R0lGODlhAQABAAAAACw='>") \
        .replace("<input id=\"q\"LABEL>", "<label for='q'>Search</label><input id='q'>").replace("SHIFT", "")
    page(work, "shop.html", good)
    r2, _ = scan(work, "good_run", state=state)
    return [("API mock answered the page (Mock Mona)", r1["user"].endswith("Mock Mona"), r1["user"]),
            ("stored auth state reused in a new context", r2["user"] == "signed-in Mock Mona", r2["user"]),
            ("a11y scan: missing alt and missing label found", sorted(x["rule"] for x in r1["violations"]) == ["image-alt", "label"], str(r1["violations"])),
            ("planted layout shift measured as poor CLS", r1["cwv"]["cls"] > 0.25, str(r1["cwv"])),
            ("fail-on-violations / poor vitals -> exit 1", r1["exit"] == 1, str(r1["exit"])),
            ("fixed page: no violations, good CLS (< 0.1), exit 0", r2["violations"] == [] and r2["cwv"]["cls"] < 0.1 and r2["exit"] == 0, str(r2)),
            ("LCP and TTFB measured", r2["cwv"]["lcp"] > 0 and r2["cwv"]["ttfb"] is not None, str(r2["cwv"]))]


# ---------------------------------------------------------------- ABUILD-21

UPLOAD = """<!doctype html><html><body><label>Upload<input type="file" id="f" style="display:none"></label><p id="name">none</p><script>
document.getElementById('f').addEventListener('change',e=>{const f=e.target.files[0];document.getElementById('name').textContent=f.name+' '+f.size;});</script></body></html>"""


def abuild_21(work: Path):
    """Hidden file-input upload: the input cannot be clicked; set files on it directly, change fires, the page shows the file."""
    page(work, "upload.html", UPLOAD)
    up = work / "report.csv"
    up.write_text("a,b\n1,2\n")
    r = browser(work, {"steps": [{"op": "goto", "url": "/upload.html"}, {"op": "tryClick", "selector": "#f", "as": "click"},
                                 {"op": "setFiles", "selector": "#f", "files": [str(up)]},
                                 {"op": "text", "selector": "#name", "as": "shown"},
                                 {"op": "eval", "js": "getComputedStyle(document.getElementById('f')).display", "as": "disp"}]})
    v = r["values"]
    return [("the input is hidden (display:none)", v["disp"] == "none", v["disp"]),
            ("a normal click on it fails/times out", v["click"] is not None, str(v["click"])[:100]),
            ("setting files directly fired change: page shows name and size", v["shown"] == f"report.csv {up.stat().st_size}", v["shown"])]


# ---------------------------------------------------------------- ABUILD-22

PROOF_PAGE = """<!doctype html><html><body><button>Toggle</button><div id="panel" hidden>Panel open</div><button>Save</button><p id="msg"></p><script>
document.querySelector('button').onclick=()=>{document.getElementById('panel').hidden=false};
document.querySelectorAll('button')[1].onclick=()=>{console.error('save failed: 500');fetch('/api/save',{method:'POST'})};</script></body></html>"""


def prove(work: Path, name: str, url: str, action: str, expect_js: str) -> dict:
    vp = {"width": 360, "height": 240}
    try:
        r = browser(work, {"context": {"viewport": vp}, "status": {"/api/save": 500}, "steps": [
            {"op": "goto", "url": url}, {"op": "eval", "js": "document.title||document.body.innerText.slice(0,20)", "as": "probe"},
            {"op": "click", "selector": action, "timeout": 800},
            {"op": "eval", "js": f"new Promise(r=>{{const t0=performance.now();const f=()=>{{if({expect_js})r(true);else if(performance.now()-t0>800)r(false);else requestAnimationFrame(f)}};f()}})", "as": "ok"},
            {"op": "shot", "path": str(work / f"{name}.png")}]}, name=name)
    except RuntimeError as e:
        m = {"claim": name, "verdict": "blocked", "reason": str(e).splitlines()[-1][:200], "viewport": vp}
        (work / f"{name}.json").write_text(json.dumps(m))
        return m
    failed = [q for q in r["requests"] if q["status"] >= 400]
    m = {"claim": name, "verdict": "pass" if r["values"]["ok"] else "fail", "viewport": vp,
         "console_errors": [c["text"] for c in r["console"] if c["type"] == "error"],
         "failed_network": [q["url"].replace("https://kosif.test", "") for q in failed], "status_ge_400": [q["status"] for q in failed]}
    (work / f"{name}.json").write_text(json.dumps(m))
    return m


def abuild_22(work: Path):
    """Rendered-behaviour proof: pass, fail or blocked with a JSON manifest (viewport, console errors, failed network, status>=400)."""
    page(work, "app.html", PROOF_PAGE)
    a = prove(work, "toggle_shows_panel", "/app.html", "role=button[name=\"Toggle\"]", "!document.getElementById('panel').hidden")
    b = prove(work, "save_shows_success", "/app.html", "role=button[name=\"Save\"]", "document.getElementById('msg').textContent==='Saved'")
    c = prove(work, "missing_page", "/nowhere.html", "role=button[name=\"Toggle\"]", "true")
    return [("toggle claim: pass (role locator, observable state)", a["verdict"] == "pass", str(a)),
            ("save claim: fail", b["verdict"] == "fail", b["verdict"]),
            ("fail manifest records the console error", "save failed: 500" in b["console_errors"], str(b["console_errors"])),
            ("fail manifest records POST /api/save with status 500", b["failed_network"] == ["/api/save"] and b["status_ge_400"] == [500], str(b["failed_network"])),
            ("no app at the URL: blocked, not pass", c["verdict"] == "blocked", c["verdict"]),
            ("manifests carry the viewport", a["viewport"] == {"width": 360, "height": 240}, "")]


# ---------------------------------------------------------------- ABUILD-23

QA_PAGE = """<!doctype html><html><head><meta name=viewport content="width=device-width"><style>body{margin:0;font:14px sans-serif}
.tbl{width:500px;height:20px;background:#ccc}.tiny{width:12px;height:12px;padding:0;border:0}
@media(min-width:768px){.mobile-only{display:none}}</style></head><body><nav id="nav"><a href="#">Home</a> <a href="#">Docs</a></nav>
<div class="tbl"></div><button class="tiny" id="x" aria-label="close"></button><img id="broken" src="/missing.png" alt="logo"></body></html>"""
QA_JS = """(()=>{const f=[];if(document.documentElement.scrollWidth>document.documentElement.clientWidth)f.push('overflow');
document.querySelectorAll('button,a').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&(r.width<24||r.height<24))f.push('tiny-tap:'+(e.id||e.textContent))});
document.querySelectorAll('img').forEach(i=>{if(i.complete&&i.naturalWidth===0)f.push('broken-img:'+i.id)});return f})()"""


def abuild_23(work: Path):
    """Three-width responsive QA at 375 (x2), 768 and 1280 px: overflow, tiny tap targets, broken images, failed requests, a table."""
    page(work, "page.html", QA_PAGE)
    widths = [(375, 812, 2), (768, 1024, 1), (1280, 800, 1)]
    table = {}
    for w, h, dpr in widths:
        r = browser(work, {"context": {"viewport": {"width": w, "height": h}, "deviceScaleFactor": dpr, "isMobile": w == 375},
                           "steps": [{"op": "goto", "url": "/page.html"}, {"op": "eval", "js": QA_JS, "as": "f"},
                                     {"op": "shot", "path": str(work / f"w{w}.png")}]}, name=f"w{w}")
        table[w] = {"findings": r["values"]["f"], "failed": [q["url"].rsplit("/", 1)[-1] for q in r["requests"] if q["status"] >= 400],
                    "shot": Image.open(work / f"w{w}.png").size}
    md = "| width | findings | failed requests |\n|---|---|---|\n" + "".join(
        f"| {w} | {', '.join(t['findings']) or 'none'} | {', '.join(t['failed']) or 'none'} |\n" for w, t in table.items())
    (work / "qa_table.md").write_text(md)
    return [("375 px: the 500 px table overflows", "overflow" in table[375]["findings"], str(table[375]["findings"])),
            ("768 and 1280 px: no overflow", "overflow" not in table[768]["findings"] and "overflow" not in table[1280]["findings"], ""),
            ("12 px close button flagged as a tiny tap target at every width", all("tiny-tap:x" in t["findings"] for t in table.values()), ""),
            ("broken image and its 404 found", all("broken-img:broken" in t["findings"] and "missing.png" in t["failed"] for t in table.values()), ""),
            ("375 emulated at 2x (750 px screenshot)", table[375]["shot"][0] == 750, str(table[375]["shot"])),
            ("page-by-width table written with 3 rows", md.count("\n| ") == 3, "")]


# ---------------------------------------------------------------- ABUILD-39

DNA_JS = """(()=>{const cs=(s)=>getComputedStyle(document.querySelector(s));const b=cs('body'),h=cs('h1'),btn=cs('.btn');
return {colors:{background:b.backgroundColor,text:b.color,primary:btn.backgroundColor,header:cs('header').backgroundColor},
fonts:{body:b.fontFamily,size:b.fontSize,h1Weight:h.fontWeight},spacing:{buttonPadding:btn.padding,headerPadding:cs('header').padding},
radii:{button:btn.borderRadius},shadows:{button:btn.boxShadow},motion:{button:btn.transitionDuration+' '+btn.transitionTimingFunction},
effects:{canvas:document.querySelectorAll('canvas').length,webgl:[...document.querySelectorAll('canvas')].some(c=>c.dataset.gl==='1')}}})()"""


def abuild_39(work: Path):
    """Design DNA from a live page: computed colours, fonts, spacing, radii, shadows, motion and canvas/WebGL use into JSON."""
    url = serve_app(work, extra_body="<canvas id='fx' data-gl='1'></canvas><script>document.getElementById('fx').getContext('webgl')</script>")
    r = browser(work, {"steps": [{"op": "goto", "url": url}, {"op": "eval", "js": DNA_JS, "as": "dna"}]})
    dna = r["values"]["dna"]
    (work / "design_dna.json").write_text(json.dumps(dna, indent=1))
    return [("primary colour #e7b65a", dna["colors"]["primary"] == "rgb(231, 182, 90)", dna["colors"]["primary"]),
            ("header colour #123456", dna["colors"]["header"] == "rgb(18, 52, 86)", dna["colors"]["header"]),
            ("body font sans-serif 16px", dna["fonts"]["body"] == "sans-serif" and dna["fonts"]["size"] == "16px", str(dna["fonts"])),
            ("button padding 10px 16px, radius 6px", dna["spacing"]["buttonPadding"] == "10px 16px" and dna["radii"]["button"] == "6px", str(dna["spacing"])),
            ("shadow 0 2px 4px rgba(0,0,0,.25)", dna["shadows"]["button"] == "rgba(0, 0, 0, 0.25) 0px 2px 4px 0px", dna["shadows"]["button"]),
            ("motion 0.2s ease", dna["motion"]["button"] == "0.2s ease", dna["motion"]["button"]),
            ("canvas/WebGL effect detected", dna["effects"] == {"canvas": 1, "webgl": True}, str(dna["effects"]))]


# ---------------------------------------------------------------- ABUILD-44

def abuild_44(work: Path):
    """Live keyboard test at 1440x900: tab order, skip link, visible focus, modal focus trap, Escape returns focus."""
    url = serve_app(work, extra_body="<style>#checkout:focus{outline:none;box-shadow:none}</style>")   # planted: no focus ring on Checkout
    r = browser(work, {"context": {"viewport": {"width": 1440, "height": 900}}, "steps": [
        {"op": "goto", "url": url}, {"op": "shot", "path": str(work / "baseline.png")},
        {"op": "focusWalk", "n": 7, "as": "order"},
        {"op": "click", "selector": "#open"}, {"op": "focusWalk", "n": 3, "as": "trap"},
        {"op": "press", "key": "Escape"}, {"op": "eval", "js": "[document.activeElement.id, document.getElementById('modal').classList.contains('open')]", "as": "esc"}]})
    order = [x["id"] for x in r["values"]["order"]]
    no_ring = [x["id"] for x in r["values"]["order"] if x["outline"].startswith("none") and x["shadow"] == "none"]
    trap = [x["id"] for x in r["values"]["trap"]]
    report = {"tab_order": order, "focus_not_visible": no_ring, "trap": trap, "escape": r["values"]["esc"]}
    (work / "keyboard_report.json").write_text(json.dumps(report, indent=1))
    return [("skip link is the first tab stop", order[0] == "skip", str(order)),
            ("tab order follows the DOM", order == ["skip", "nav1", "nav2", "qty", "add", "checkout", "open"], str(order)),
            ("the planted element without a focus ring is reported", no_ring == ["checkout"], str(no_ring)),
            ("modal traps focus (Tab cycles OK/Cancel)", trap == ["m2", "m1", "m2"], str(trap)),
            ("Escape closes the modal and returns focus to the opener", r["values"]["esc"] == ["open", False], str(r["values"]["esc"]))]


PROGRAMS = {
    "ABUILD-08": abuild_08, "ABUILD-14": abuild_14, "ABUILD-15": abuild_15, "ABUILD-16": abuild_16, "ABUILD-18": abuild_18,
    "ABUILD-19": abuild_19, "ABUILD-20": abuild_20, "ABUILD-21": abuild_21, "ABUILD-22": abuild_22, "ABUILD-23": abuild_23,
    "ABUILD-39": abuild_39, "ABUILD-44": abuild_44,
}
