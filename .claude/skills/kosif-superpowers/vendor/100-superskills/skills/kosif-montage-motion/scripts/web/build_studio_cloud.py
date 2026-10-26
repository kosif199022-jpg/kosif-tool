"""Build KOSIF Studio Cloud: the browser montage editor (static/studio) as ONE self-contained page for a claude.ai
artifact — no server, no PC. Modules are wrapped in their own scopes (no name collisions), the vendored mp4-muxer is
loaded from jsDelivr at the same pinned version, and the Studio's file saves go through the artifact's `downloads`
capability (a sandboxed artifact cannot start <a download> itself).

    python scripts/web/build_studio_cloud.py --out studio-cloud.html [--home-url https://claude.ai/artifact/…]
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE / "static" / "studio"
MUXER_CDN = "https://cdn.jsdelivr.net/npm/mp4-muxer@5.2.1/build/mp4-muxer.min.js"
MODULES = ["model.mjs", "media.mjs", "offline.mjs"]

SAVE_SHIM = """<script>
/* KOSIF Studio Cloud: file saves through the artifact's downloads capability (the viewer confirms each save). */
(function () {
  let dl;  // undefined = not asked yet, null = unavailable
  const status = (msg, err) => { const s = document.getElementById('status'); if (s) { s.textContent = msg; s.classList.toggle('error', !!err); } };
  window.claude?.use?.('downloads').then((d) => { dl = d; }).catch(() => { dl = null; });
  globalThis.__kosifSave = async function (blob, name) {
    if (dl === undefined) { try { dl = await window.claude?.use?.('downloads'); } catch { dl = null; } }
    if (!dl) { status('الحفظ غير متاح في هذا العرض. افتح الصفحة من claude.ai لتحفظ الملف.', true); return; }
    try { const r = await dl.save({ filename: name, data: blob }); status(r.status === 'saved' ? `حُفظ ${name}` : `سُلّم ${name}`); }
    catch (e) {
      const m = { declined: 'ألغيتَ الحفظ.', too_large: 'الملف أكبر من المسموح هنا؛ قصّر المشروع.', rate_limited: 'نافذة حفظ مفتوحة بالفعل؛ انتظر ثم أعد المحاولة.', rejected_extension: 'هذا الامتداد غير مسموح.' };
      status(m[e?.code] || `تعذر الحفظ: ${e?.message || e?.code || e}`, e?.code !== 'declined');
    }
  };
})();
</script>"""


def strip_exports(src: str) -> tuple[str, list[str]]:
    names = re.findall(r"export\s+(?:async\s+)?(?:const|let|function)\s+([A-Za-z_$][\w$]*)", src)
    return re.sub(r"\bexport\s+(?=(?:async\s+)?(?:const|let|function)\b)", "", src), names


def build(home_url: str | None) -> str:
    css = (STUDIO / "style.css").read_text(encoding="utf-8")
    page = (STUDIO / "index.html").read_text(encoding="utf-8")
    body = page[page.index("<body>") + len("<body>"): page.index("</body>")]
    body = re.sub(r"<script\b[^>]*>\s*</script>\s*", "", body)                         # the module and muxer tags are rebuilt below
    home = html.escape(home_url or "#", quote=True)
    body = body.replace('<a class="brand" href="/"', f'<a class="brand" href="{home}" target="_blank" rel="noopener"')
    body = re.sub(r'<div class="examples">.*?</div>',
                  f'<div class="examples"><span class="subtle">التخطيط والعقل</span><a href="{home}" target="_blank" rel="noopener">KOSIF Motion Cloud <span>↗</span></a></div>',
                  body, flags=re.S)
    parts = []
    for m in MODULES:
        code, names = strip_exports((STUDIO / m).read_text(encoding="utf-8"))
        var = "__" + m.split(".")[0]
        parts.append(f"const {var} = (() => {{\n{code}\nreturn {{ {', '.join(names)} }};\n}})();")
    app = (STUDIO / "app.mjs").read_text(encoding="utf-8")
    for m in MODULES:
        var = "__" + m.split(".")[0]
        imp = re.search(r"import\s*\{([^}]*)\}\s*from\s*'\./" + re.escape(m) + r"';", app)
        if not imp:
            raise SystemExit(f"app.mjs does not import {m}")
        app = app.replace(imp.group(0), f"const {{{imp.group(1)}}} = {var};")
    if re.search(r"^\s*import\s", app, re.M) or "from './" in app:
        raise SystemExit("unresolved import left in app.mjs")
    hook = "function download(blob,name){"
    if app.count(hook) != 1:
        raise SystemExit("download() not found exactly once")
    app = app.replace(hook, hook + "if(globalThis.__kosifSave){globalThis.__kosifSave(blob,name);return;}")
    bundle = "\n".join(parts) + "\n" + app
    if "</script" in bundle.lower():
        raise SystemExit("a module contains </script>")
    return (f"<title>KOSIF Studio Cloud</title>\n<style>\n{css}\n</style>\n{body.strip()}\n"
            f'<script src="{MUXER_CDN}"></script>\n{SAVE_SHIM}\n<script type="module">\n{bundle}\n</script>\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True); ap.add_argument("--home-url")
    a = ap.parse_args()
    out = Path(a.out); out.write_text(build(a.home_url), encoding="utf-8")
    print(out, out.stat().st_size, "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
