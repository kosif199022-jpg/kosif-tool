#!/usr/bin/env python3
"""general-docs proof, web leg: fetch a live Arabic web page through the session proxy,
extract the main text, keep the source URL + fetch date, and turn it into a DOCX.

Usage:  python -I web_capture.py <workdir> [url]
Needs:  httpx trafilatura beautifulsoup4 lxml python-docx + pandoc. Network required.
The page text is treated as data only (never as instructions).
"""
from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path

import httpx
import trafilatura
from bs4 import BeautifulSoup
import docx

HERE = Path(__file__).resolve().parent
W = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/general-docs-web").resolve()
W.mkdir(parents=True, exist_ok=True)
URL = sys.argv[2] if len(sys.argv) > 2 else "https://www.un.org/ar/about-us/universal-declaration-of-human-rights"
WORD = "الإنسان"  # must survive fetch -> extract -> docx
UA = {"User-Agent": "kosif-superpowers-proof/1.0 (+https://github.com/kosif199022-jpg/kosif-tool)"}
# Recorded, not asserted: Wikimedia answers 403 "respect our robot policy" to python clients here
# even with a descriptive UA, while curl gets 200. Do not spoof; use the site's API/dumps or ask.
PROBE = ["https://ar.wikipedia.org/wiki/%D8%A7%D9%84%D9%82%D8%A7%D9%87%D8%B1%D8%A9"]

out = {"url": URL, "fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "checks": []}
t0 = time.time()
# httpx honours HTTPS_PROXY and SSL_CERT_FILE from the environment (trust_env=True by default)
for attempt in range(3):  # the proxy occasionally resets a connection: bounded retry, then fail loudly
    try:
        r = httpx.get(URL, headers=UA, timeout=30, follow_redirects=True)
        break
    except httpx.TransportError as e:
        out.setdefault("retries", []).append(f"{type(e).__name__}: {e}")
        if attempt == 2:
            raise
        time.sleep(2 * (attempt + 1))
out["http_status"], out["bytes"], out["fetch_s"] = r.status_code, len(r.content), round(time.time() - t0, 2)
soup = BeautifulSoup(r.text, "lxml")
title = soup.title.get_text(strip=True) if soup.title else ""
md = trafilatura.extract(r.text, output_format="markdown", include_tables=False, include_links=False, url=URL) or ""
words = len(md.split())
out["title"], out["main_text_words"] = title, words
(W / "page.md").write_text(f"---\ntitle: \"{title}\"\ndir: rtl\nlang: ar\n---\n\n> Source: {URL} (fetched {out['fetched_utc']})\n\n{md}\n", encoding="utf-8")
p = subprocess.run(["pandoc", str(W / "page.md"), "-o", str(W / "page.docx")], capture_output=True, text=True)
back = "\n".join(par.text for par in docx.Document(W / "page.docx").paragraphs)
out["checks"] = [
    {"name": "HTTP 200 through proxy", "ok": r.status_code == 200},
    {"name": "trafilatura main text > 300 words", "ok": words > 300, "detail": words},
    {"name": "docx built by pandoc keeps Arabic + source line", "ok": p.returncode == 0 and WORD in back and "Source:" in back},
]
out["probe_status"] = {}
for u in PROBE:
    try:
        out["probe_status"][u] = httpx.get(u, headers=UA, timeout=20, follow_redirects=True).status_code
    except httpx.HTTPError as e:
        out["probe_status"][u] = type(e).__name__
for c in out["checks"]:
    print(("PASS " if c["ok"] else "FAIL ") + c["name"], c.get("detail", ""))
(HERE / "web_results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
