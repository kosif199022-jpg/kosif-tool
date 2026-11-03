"""Wave-2 "browser" power programs (Playwright Chromium, offline).

1) Every program in the *__browser.py modules passes through _black_dragon_power_program.run_program.
2) browser-done.json lists exactly those programs, every card is a wave-1 browser skip, and
   programmed + browser-skipped cover the wave's cards with no overlap.
3) Planted failures: breaking each module's technique (the page script, the PRNG, the clamp/easing,
   the pool, the fix loop, the focus trap, the page break, the boil step, the pitch ...) makes that
   card's own check fail. At least three per module.
"""
from __future__ import annotations

import importlib
import json
import shutil
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import power_programs as pp  # noqa: E402
import _black_dragon_power_program as bd  # noqa: E402

OUT = ROOT / "out" / "power-programs"
MODULES = ["engines_render_pipeline__browser", "atlas_build__browser", "documents_office__browser",
           "ai_generation__browser", "voice_tts__browser", "web_research__browser"]
_CARDS = pp.card_index()


def have_browser() -> bool:
    return shutil.which("node") is not None and shutil.which("ffmpeg") is not None


def mod(name):
    return importlib.import_module(f"power_programs.{name}")


def run(pid):
    with tempfile.TemporaryDirectory() as d:
        return bd.run_program(pid, Path(d) / "work")


def checks_failed(pid, fn, names):
    """Run fn (a patched program) directly; return which of the named checks failed (or 'raised')."""
    with tempfile.TemporaryDirectory() as d:
        w = Path(d) / "w"
        w.mkdir()
        try:
            res = {n: ok for n, ok, _ in fn(w)}
        except Exception as e:  # a broken technique may also make the program raise: still a failure
            return {"raised": str(e)[:200]}
    return {n: res.get(n) for n in names if res.get(n) is not True}


@unittest.skipUnless(have_browser(), "node/ffmpeg not available")
class AllProgramsPass(unittest.TestCase):
    def test_every_program_passes(self):
        ids = [pid for m in MODULES for pid in mod(m).PROGRAMS]
        with ThreadPoolExecutor(max_workers=6) as ex:
            results = list(ex.map(run, ids))
        bad = {r.get("power"): r.get("problems") or r.get("error") for r in results if not r.get("ok")}
        self.assertEqual(bad, {})
        self.assertEqual(len(results), len(ids))


class Bookkeeping(unittest.TestCase):
    def test_done_file_matches_modules(self):
        done = json.loads((OUT / "browser-done.json").read_text())
        progs = {pid: m for m in MODULES for pid in mod(m).PROGRAMS}
        self.assertEqual(done, progs)

    def test_cards_are_wave1_browser_skips_and_cover(self):
        wave1 = {}
        for g in ("engines", "data", "language"):
            wave1.update(json.loads((OUT / f"{g}-skipped.json").read_text()))
        done = json.loads((OUT / "browser-done.json").read_text())
        skipped = json.loads((OUT / "browser-skipped.json").read_text())
        self.assertFalse(set(done) & set(skipped))
        for pid in list(done) + list(skipped):
            self.assertIn(pid, wave1, pid)
            self.assertIn(pid, _CARDS, pid)
        for pid in done:
            self.assertNotIn("remotion", wave1[pid].lower(), pid)


def patched(module, pid, attr, value):
    m = mod(module)
    fn = m.PROGRAMS[pid]

    def go(w):
        with mock.patch.object(m, attr, value):
            return fn(w)
    return go


def replaced(module, attr, old, new):
    text = getattr(mod(module), attr)
    assert old in text, (attr, old)
    return text.replace(old, new)


E, A, D, G, V, W = MODULES
PLANTED = {
    E: [("ENG-382", "CHART_PAGE", lambda: replaced(E, "CHART_PAGE", "const ease=(x)=>x*x*(3-2*x);", "const ease=(x)=>x;"),
         ["t=0.8 heights match interpolate+easing"]),                                     # page loses its easing
        ("ENG-170", "ADAPTER_PAGE", lambda: replaced(E, "ADAPTER_PAGE", "paused both}", "paused}"), ["CSS adapter matches after backward seeks"]),
        ("ENG-161", "VLIB_PAGE", lambda: replaced(E, "VLIB_PAGE", "all.slice(30)", "all.slice(31)"), ["only the last 30 renders kept"]),
        ("ENG-G02", "SPRITE_PAGE", lambda: replaced(E, "SPRITE_PAGE", "if(pool.length)return pool.pop();", ""),
         ["recycling reuses the pooled object (created stays 2000)"])],
    A: [("ABUILD-39", "DNA_JS", lambda: replaced(A, "DNA_JS", "primary:btn.backgroundColor", "primary:b.backgroundColor"), ["primary colour #e7b65a"]),
        ("ABUILD-23", "QA_JS", lambda: replaced(A, "QA_JS", "f.push('overflow')", "0"), ["375 px: the 500 px table overflows"]),
        ("ABUILD-15", "build_clone", lambda: (lambda manifest, props: _boxes_only(manifest)),
         ["clone accepted (diff < 0.05) after adding background and radius"]),
        ("ABUILD-21", "UPLOAD", lambda: replaced(A, "UPLOAD", "f.name+' '+f.size", "f.name"), ["setting files directly fired change: page shows name and size"])],
    D: [("DOC-06", "DOC", lambda: replaced(D, "DOC", "page-break-after:always;", ""), ["one page per JS-built section (3)"]),
        ("DOC-06", "DOC", lambda: replaced(D, "DOC", "/lib/cairo-800.woff2", "/lib/missing.woff2"), ["Arabic Cairo face embedded as a subset"]),
        ("DOC-06", "DOC", lambda: replaced(D, "DOC", "background:#00ff80", "background:#0000ff"), ["printBackground:true paints the #00ff80 background"])],
    G: [("GEN-72", "FILM_JS", lambda: replaced(G, "FILM_JS", "Math.floor(t*12)", "Math.floor(t*100)"),
         ["same 1/12 s boil step -> identical frames (0.10 vs 0.12 s)"]),
        ("GEN-72", "FILM_JS", lambda: replaced(G, "FILM_JS", "s.side==='left'?'right':'left'", "s.side"),
         ["subject on the left -> big type block on the right"]),
        ("GEN-72", "FILM_JS", lambda: replaced(G, "FILM_JS", "g.fillRect(0,0,W,H);", "g.fillRect(0,0,W,H);g.fillStyle='rgb(128,128,128)';g.fillRect(0,0,9,9);"),
         ["only two inks on paper"])],
    V: [("VOICE-52", "REC", lambda: replaced(V, "REC", "o.frequency.value=440", "o.frequency.value=660"), ["recorded pitch is 440 Hz"]),
        ("VOICE-52", "REC", lambda: replaced(V, "REC", "},1000);window.__made", "},3000);window.__made"), ["object URL revoked after 1000 ms"]),
        ("VOICE-52", "REC", lambda: replaced(V, "REC", "downloadAudioBlob(blob,'kosif-response.webm')", "downloadAudioBlob(blob,'audio.bin')"),
         ["download saved as kosif-response.webm"])],
    W: [("WEB-07", "JS_PAGE", lambda: replaced(W, "JS_PAGE", "i<12", "i<11"), ["JS built the 12 result rows"]),
        ("WEB-07", "JS_PAGE", lambda: replaced(W, "JS_PAGE", '<script src="https://cdn.example.com/tracker.js"></script>', ""),
         ["remote tracker request refused"]),
        ("WEB-07", "JS_PAGE", lambda: replaced(W, "JS_PAGE", "i===11?'#ff0000'", "i===11?'#e0e0e0'"), ["last JS row (red) is in the full-page capture"])],
}


def _boxes_only(manifest):
    body = "".join(f"<div style='position:absolute;left:{e['x']}px;top:{e['y']}px;width:{e['w']}px;height:{e['h']}px'></div>"
                   for e in manifest["elements"] if e["id"] != "body")
    return f"<!doctype html><html><head><style>body{{margin:0}}</style></head><body>{body}</body></html>"


@unittest.skipUnless(have_browser(), "node/ffmpeg not available")
class PlantedFailures(unittest.TestCase):
    def test_at_least_three_per_module(self):
        for m in MODULES:
            self.assertGreaterEqual(len(PLANTED[m]), 3, m)

    def test_broken_techniques_fail_their_checks(self):
        def module_cases(m):
            out = []
            for pid, attr, make, names in PLANTED[m]:          # one module per thread: its patches never overlap
                value = make()
                out.append((m, pid, attr, checks_failed(pid, patched(m, pid, attr, value), names)))
            return out
        with ThreadPoolExecutor(max_workers=len(MODULES)) as ex:
            results = [r for rs in ex.map(module_cases, MODULES) for r in rs]
        not_caught = [(m, pid, attr, failed) for m, pid, attr, failed in results if not failed or "raised" in failed]
        self.assertEqual(not_caught, [])


if __name__ == "__main__":
    unittest.main()
