"""Wave-2 browser program for documents-office: DOC-06, HTML (JavaScript-driven, RTL Arabic) to PDF via headless Chromium.

The page builds its sections with JavaScript, waits for document.fonts.ready (vendored Cairo
woff2 served at https://kosif.test/), then page.pdf({format:'A4', printBackground:true}). The PDF
is parsed with the stdlib: A4 MediaBox, one page per JS-built section, the embedded Cairo subset,
and the background fill present only when printBackground is on.
"""
from __future__ import annotations

import re
import zlib
from pathlib import Path

from ._browser_common import browser, page

DOC = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset=utf-8><style>
@font-face{font-family:Cairo;src:url(/lib/cairo-800.woff2) format('woff2');font-weight:800}
body{margin:0;font:800 28px Cairo;background:#00ff80}section{page-break-after:always;padding:40px}</style></head><body><script>
for(const t of ['لوحة المبيعات','الإيرادات الشهرية','الخلاصة']){const s=document.createElement('section');s.textContent=t;document.body.appendChild(s);}
document.fonts.ready.then(()=>{window.__font=document.fonts.check("800 28px Cairo");window.__ready=true});</script></body></html>"""


def pdf_facts(path: Path) -> dict:
    data = path.read_bytes()
    streams = []
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        try:
            streams.append(zlib.decompress(m.group(1)))
        except zlib.error:
            pass
    text = data + b"".join(streams)
    boxes = re.findall(rb"/MediaBox\s*\[\s*0 0 ([\d.]+) ([\d.]+)\s*\]", text)
    return {"pages": len(re.findall(rb"/Type\s*/Page\b", text)), "box": [(float(a), float(b)) for a, b in boxes][:1],
            "fonts": sorted(set(m.decode() for m in re.findall(rb"/FontName\s*/([A-Z]{6}\+[\w-]+)", text))),
            "bg_fill": any(abs(float(g) - 1) < 0.01 and abs(float(b_) - 0.502) < 0.01 and float(r_) < 0.01
                           for r_, g, b_ in re.findall(rb"([\d.]+) ([\d.]+) ([\d.]+) rg", text))}


def doc_06(work: Path):
    """HTML to PDF with headless Chromium: A4, printBackground, fonts.ready, JS-built content, RTL Arabic font embedded."""
    page(work, "dashboard.html", DOC)
    steps = [{"op": "goto", "url": "/dashboard.html"}, {"op": "wait", "js": "window.__ready===true"},
             {"op": "eval", "js": "window.__font", "as": "font"},
             {"op": "pdf", "path": str(work / "dashboard.pdf"), "options": {"format": "A4", "printBackground": True}},
             {"op": "pdf", "path": str(work / "no_background.pdf"), "options": {"format": "A4", "printBackground": False}}]
    r = browser(work, {"steps": steps})
    a, b = pdf_facts(work / "dashboard.pdf"), pdf_facts(work / "no_background.pdf")
    w, h = a["box"][0] if a["box"] else (0, 0)
    return [("fonts.ready awaited: Cairo 800 loaded before printing", r["values"]["font"] is True, str(r["values"]["font"])),
            ("PDF starts with %PDF", (work / "dashboard.pdf").read_bytes()[:5] == b"%PDF-", ""),
            ("A4 MediaBox 595 x 842 pt", abs(w - 595.3) < 1.5 and abs(h - 841.9) < 1.5, str(a["box"])),
            ("one page per JS-built section (3)", a["pages"] == 3, str(a["pages"])),
            ("Arabic Cairo face embedded as a subset", any(f.split("+")[1].startswith("Cairo") for f in a["fonts"]), str(a["fonts"])),
            ("printBackground:true paints the #00ff80 background", a["bg_fill"] is True, str(a["bg_fill"])),
            ("printBackground:false leaves it out", b["bg_fill"] is False, str(b["bg_fill"])),
            ("no network used", not r["blocked"], str(r["blocked"]))]


PROGRAMS = {"DOC-06": doc_06}
