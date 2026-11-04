"""Wave-2 browser program for web-research: WEB-07, headless Chromium for JavaScript pages and screenshots.

The page is local (served at https://kosif.test/, remote requests aborted, as on a site that
refuses bots): its content only exists after JavaScript runs. page.screenshot({fullPage:true})
must capture the whole JS-built document and the PDF must print it, while a raw HTML read sees
none of it.
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

from ._browser_common import browser, img, near, page

JS_PAGE = """<!doctype html><html><head><meta charset=utf-8><script src="https://cdn.example.com/tracker.js"></script></head>
<body style="margin:0;background:#fff"><div id="app"></div><script>
const app=document.getElementById('app');for(let i=0;i<12;i++){const d=document.createElement('div');d.className='row';d.textContent='Result '+(i+1);
d.style.cssText='height:100px;background:'+(i===11?'#ff0000':'#e0e0e0')+';margin:0';app.appendChild(d);}window.__built=12;</script></body></html>"""


def web_07(work: Path):
    """Headless Chromium for JS pages: what a user sees (JS-built), full-page screenshot, print to PDF; remote requests refused."""
    page(work, "results.html", JS_PAGE)
    r = browser(work, {"context": {"viewport": {"width": 320, "height": 240}}, "steps": [
        {"op": "goto", "url": "/results.html"}, {"op": "count", "selector": ".row", "as": "rows"},
        {"op": "shot", "path": str(work / "full.png"), "fullPage": True}, {"op": "shot", "path": str(work / "viewport.png")},
        {"op": "pdf", "path": str(work / "results.pdf"), "options": {"format": "A4"}}]})
    raw_rows = len(re.findall(r"class=['\"]row", JS_PAGE))
    full = Image.open(work / "full.png").size
    a = img(work / "full.png")
    return [("JS built the 12 result rows", r["values"]["rows"] == 12, str(r["values"]["rows"])),
            ("raw HTML has none of them (needs a browser)", raw_rows == 0, str(raw_rows)),
            ("full-page screenshot is 12 x 100 px tall", full == (320, 1200), str(full)),
            ("viewport screenshot is only 240 px", Image.open(work / "viewport.png").size == (320, 240), ""),
            ("last JS row (red) is in the full-page capture", a.shape[0] > 1150 and near(a[1150, 10], (255, 0, 0), 3), str(a[min(1150, a.shape[0] - 1), 10].tolist())),
            ("PDF printed", (work / "results.pdf").read_bytes()[:5] == b"%PDF-", ""),
            ("remote tracker request refused", any("cdn.example.com" in u for u in r["blocked"]), str(r["blocked"]))]


PROGRAMS = {"WEB-07": web_07}
