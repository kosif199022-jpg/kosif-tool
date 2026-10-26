"""KOSIF Studio tests:  python -m unittest discover -s tests   (from the kosif-studio folder)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE), str(HERE / "scenes")]
import render as R  # noqa: E402
import studio  # noqa: E402
import svg_import  # noqa: E402
import vector_scene  # noqa: E402
import vectorize  # noqa: E402


def sample_logo() -> np.ndarray:
    """A badge like a real logo: two rings, a white field, small antialiased text, a see-through outside."""
    im = Image.new("RGBA", (160, 190), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 155, 185], radius=60, fill=(170, 200, 55, 255))
    d.rounded_rectangle([9, 9, 150, 180], radius=56, fill=(255, 255, 255, 255))
    d.rounded_rectangle([13, 13, 146, 176], radius=52, fill=(240, 5, 12, 255))
    d.rounded_rectangle([24, 24, 135, 165], radius=44, fill=(255, 255, 255, 255))
    d.ellipse([55, 45, 105, 95], outline=(10, 10, 6, 255), width=4)
    d.rectangle([30, 120, 130, 145], fill=(240, 5, 12, 255))
    d.text((48, 125), "KOSIF 2026", fill=(255, 255, 255, 255))
    d.text((40, 100), "since", fill=(150, 150, 150, 255))
    return np.asarray(im).copy()


def px(img: Image.Image, x: float, y: float, scale: float):
    return img.getpixel((round(x * scale), round(y * scale)))


class Renderer(unittest.TestCase):
    def test_holes_cut_out(self):
        ring = [list(R.ellipse(600, 400, 200)[0]), R.Hole(R.ellipse(600, 400, 100)[0])]
        im = R.render_image([R.Step("bg", [R.fill(R.rect(0, 0, 1200, 800), "#ffffff")]),
                             R.Step("ring", [R.fill(ring, "#ff0000")])], .25, rolloff=1)
        self.assertEqual(px(im, 600, 400, .25), (255, 255, 255))
        self.assertEqual(px(im, 600, 250, .25), (255, 0, 0))

    def test_even_odd_compound(self):
        shape = R.compound(R.path("M0 0 H1200 V800 H0 Z M500 300 H700 V500 H500 Z"))
        im = R.render_image([R.Step("s", [R.fill(shape, "#0000ff")])], .25, rolloff=1)
        self.assertEqual(px(im, 600, 400, .25), (0, 0, 0))          # the hole shows the black sheet
        self.assertEqual(px(im, 100, 100, .25), (0, 0, 255))

    def test_path_arcs_and_smooth_curves_end_where_they_should(self):
        pts = R.path("M10 50 A40 40 0 0 1 90 50 S 50 100 10 50 Q30 20 50 50 T 90 50 a10 10 0 01 5 5")[0]
        self.assertAlmostEqual(pts[-1][0], 95, 3)
        self.assertAlmostEqual(pts[-1][1], 55, 3)

    def test_transparent_gradient_and_text(self):
        im = R.render_image([R.Step("bg", [R.fill(R.rect(0, 0, 1200, 800), "#000000")]),
                             R.Step("g", [R.fill(R.ellipse(600, 400, 300), R.rad((600, 400), 300,
                                                                                [(0, "#ffffffff"), (1, "#ffffff00")]))]),
                             R.Step("t", [R.text("سلام", 200, 200, 80, "#ff0000", anchor="mm")])], .5, rolloff=1)
        centre, edge = px(im, 600, 400, .5)[0], px(im, 600, 690, .5)[0]
        self.assertGreater(centre, 240)
        self.assertLess(edge, 40)
        reds = np.asarray(im)[50:150, 50:150]
        self.assertTrue(((reds[..., 0] > 200) & (reds[..., 1] < 60)).any(), "Arabic text was not drawn")

    def test_realism_primitives_change_a_flat_fill(self):
        base = [R.Step("b", [R.fill(R.ellipse(600, 400, 300, 200), "#808080")])]
        plain = np.asarray(R.render_image(base, .25, rolloff=1)).astype(int)
        for op in (R.shade(R.ellipse(600, 400, 300, 200), (200, 100), "#c0c0c0", "#202020"),
                   R.noise(R.ellipse(600, 400, 300, 200), .4, 20, 3),
                   R.scales(R.ellipse(600, 400, 300, 200), 16, "#000000", .5)):
            im = np.asarray(R.render_image(base + [R.Step("x", [op])], .25, rolloff=1)).astype(int)
            self.assertGreater(np.abs(im - plain).mean(), 1.0)
            self.assertGreater(len(np.unique(im[70:130, 100:200].reshape(-1, 3), axis=0)), 4)

    def test_camera_ops_run_and_change_the_picture(self):
        base = [R.Step("b", [R.fill(R.rect(0, 0, 1200, 800), R.lin((0, 0), (0, 800), [(0, "#102030"), (1, "#405060")])),
                             R.fill(R.ellipse(600, 400, 120, 120), "#ffffff")])]
        plain = np.asarray(R.render_image(base, .25, rolloff=1)).astype(int)
        for op in (R.defocus(3), R.motion_blur(R.rect(0, 0, 1200, 800), 8, 104), R.bloom(.6, 20, .8),
                   R.flare((600, 400), "#ffb070", 100, 300, .6), R.chroma(3), R.filmic(1.2, 1.1, 1.1)):
            im = np.asarray(R.render_image(base + [R.Step("c", [op])], .25, rolloff=1)).astype(int)
            self.assertGreater(np.abs(im - plain).mean(), 0.05)
        lit = R.render_image([R.Step("r", [R.relief(R.ellipse(600, 400, 300, 200), [(300, 100, 400, "#ffffff", 1.0)], "#808080",
                                                      bumps=[(2, 20), (.5, 4)], sss=4, roughness=.5)])], .25, rolloff=1)
        self.assertGreater(len(np.unique(np.asarray(lit)[70:130, 100:200].reshape(-1, 3), axis=0)), 30)

    def test_reveal_order_is_a_permutation_for_every_order(self):
        idx = np.arange(0, 12000, 7, dtype=np.int32)
        for order in ("sweep", "grow", "rise", "down", "left", "right", "sparkle"):
            out = R.reveal_order(idx, 300, R.Step("x", [], order, (100, 100)), .25)
            self.assertEqual(sorted(out.tolist()), idx.tolist(), order)

    def test_highlight_rolloff_is_per_picture(self):
        steps = [R.Step("w", [R.fill(R.rect(0, 0, 1200, 800), "#ffffff")])]
        self.assertEqual(px(R.render_image(steps, .1, rolloff=1.0), 10, 10, .1), (255, 255, 255))
        self.assertLess(px(R.render_image(steps, .1), 10, 10, .1)[0], 255)


class Svg(unittest.TestCase):
    def test_basic_shapes_styles_and_transforms(self):
        svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80">
          <style>.r{fill:#ff0000}</style>
          <rect width="120" height="80" fill="#0000ff"/>
          <g transform="translate(60 40)"><circle class="r" r="10"/></g>
          <rect x="5" y="5" width="20" height="10" rx="3" fill="rgb(0,255,0)" stroke="black" stroke-width="2"/>
        </svg>"""
        title, steps = svg_import.load_svg(svg)
        im = R.render_image(steps, .25, rolloff=1)
        self.assertEqual(px(im, 600, 400, .25), (255, 0, 0))        # the circle, moved to the centre
        self.assertEqual(px(im, 1100, 700, .25), (0, 0, 255))
        self.assertGreaterEqual(len(steps), 4)

    def test_the_example_rocket(self):
        title, steps = svg_import.load_svg((HERE / "examples" / "svg_rocket.svg").read_text(encoding="utf-8"))
        self.assertEqual(title, "صاروخ")
        R.render_image(steps, .25, rolloff=1)


class Vectorize(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_flat_logo_keeps_its_colours_and_its_hole(self):
        im = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse([10, 10, 110, 110], fill=(230, 20, 30, 255))
        d.ellipse([40, 40, 80, 80], fill=(255, 255, 255, 255))
        im.save(self.tmp / "logo.png")
        data = vectorize.trace(self.tmp / "logo.png")
        self.assertFalse(data["photo"])
        cols = {L["color"] for L in data["layers"]}
        self.assertTrue(any(c.startswith("#e6") for c in cols), cols)
        self.assertIn("#ffffff", cols)
        out = R.render_image(vector_scene.build(data), .5, rolloff=1)
        s = min(1080 / 120, 730 / 120)
        ox, oy = (1200 - 120 * s) / 2, (800 - 120 * s) / 2
        self.assertEqual(px(out, ox + 60 * s, oy + 60 * s, .5), (255, 255, 255))
        self.assertEqual(px(out, ox + 25 * s, oy + 60 * s, .5), (230, 20, 30))

    def test_noise_is_seen_as_a_photo(self):
        rng = np.random.default_rng(1)
        Image.fromarray(rng.integers(0, 255, (160, 160, 3), dtype=np.uint8)).save(self.tmp / "p.png")
        self.assertTrue(vectorize.looks_like_photo(np.asarray(Image.open(self.tmp / "p.png").convert("RGBA"))))
        data = vectorize.trace(self.tmp / "p.png", colors=6)
        self.assertEqual(len(data["layers"]) <= 6, True)


class Exact(unittest.TestCase):
    """An image redrawn from nothing must end identical to the original: every pixel, colour and transparency."""

    def check(self, rgba):
        import exact
        canvas = np.zeros_like(rgba).reshape(-1, 4)
        steps = 0
        for label, kind, origin, weight, order, cols in exact.plan(rgba):
            canvas[order] = cols
            steps += 1
        self.assertGreater(steps, 1)
        self.assertEqual(exact.mismatches(canvas.reshape(rgba.shape), rgba), 0)

    def test_a_logo_ends_identical(self):
        self.check(sample_logo())

    def test_a_photo_like_image_ends_identical(self):
        rng = np.random.default_rng(3)
        base = np.zeros((90, 120, 4), np.uint8)
        base[..., :3] = rng.integers(0, 255, (90, 120, 3), dtype=np.uint8)
        base[..., 3] = 255
        base[:10, :10, 3] = 0                                   # a see-through corner must stay see-through
        self.check(base)


class ImageToPython(unittest.TestCase):
    """📤: a standalone Pillow program that makes the image again, pixel for pixel, outside the studio."""

    def test_program_reproduces_the_image_with_plain_python(self):
        import to_python
        tmp = Path(tempfile.mkdtemp())
        Image.fromarray(sample_logo(), "RGBA").save(tmp / "logo.png")
        code = to_python.image_to_python(tmp / "logo.png", "logo")
        self.assertIn("draw.polygon(", code)
        (tmp / "logo.py").write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, "logo.py"], cwd=tmp, capture_output=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        out = np.asarray(Image.open(tmp / "logo.png").convert("RGBA"))
        self.assertEqual(int(np.any(out != sample_logo(), axis=2).sum()), 0)
        import runner
        self.assertEqual(runner.kind_of(code), "python")        # a real program: it runs and is recorded
        shutil.rmtree(tmp, ignore_errors=True)


class Judge(unittest.TestCase):
    """The realism gate tells a flat cartoon from a shaded picture, measured, not guessed."""

    def test_flat_cartoon_is_revised_and_shaded_scene_passes(self):
        import judge
        tmp = Path(tempfile.mkdtemp())
        flat = Image.new("RGB", (400, 300), "#ffffff")
        d = ImageDraw.Draw(flat)
        d.rectangle([0, 150, 400, 300], fill="#4caf50")
        d.ellipse([150, 40, 250, 140], fill="#ffd54f", outline="#000000", width=4)
        d.rectangle([100, 120, 300, 220], fill="#d7a86e", outline="#000000", width=4)
        flat.save(tmp / "flat.png")
        steps = [R.Step("bg", [R.fill(R.rect(0, 0, 1200, 800), R.lin((0, 0), (0, 800), [(0, "#102030"), (1, "#405060")])),
                               R.noise(R.rect(0, 0, 1200, 800), .3, 40, 1)]),
                 R.Step("ball", [R.shade(R.ellipse(600, 400, 250, 250), (300, 200), "#d0b090", "#301808", .4),
                                 R.noise(R.ellipse(600, 400, 250, 250), .3, 12, 2), R.grain(.02)])]
        R.render_image(steps, .5).save(tmp / "shaded.png")
        mf, ms = judge.measure(tmp / "flat.png"), judge.measure(tmp / "shaded.png")
        vf, rf = judge.verdict(mf)
        shutil.rmtree(tmp, ignore_errors=True)
        self.assertEqual(vf, "REVISE", rf)
        self.assertGreater(mf["flat_share"], judge.THRESH["flat_share"])          # the cartoon is caught by its flat fills
        self.assertLess(ms["flat_share"], judge.THRESH["flat_share"])             # shading leaves no flat fill
        self.assertLess(ms["hard_edge_share"], judge.THRESH["hard_edge_share"])   # and no outline look
        self.assertLess(ms["flat_share"], mf["flat_share"] / 5)

    def test_the_whale_scene_passes_the_gate(self):
        import judge
        _, steps, rolloff = studio.load("whale_dragon")
        tmp = Path(tempfile.mkdtemp())
        R.render_image(steps, 1.0, rolloff=rolloff).save(tmp / "whale.png")
        v, reasons = judge.verdict(judge.measure(tmp / "whale.png"))
        shutil.rmtree(tmp, ignore_errors=True)
        self.assertEqual(v, "PASS", reasons)


class JevPlan(unittest.TestCase):
    """Photos: the painting plan is chosen among measured candidates (by Jev, or by the rule when Jev is off)."""

    def photo(self):
        rng = np.random.default_rng(5)
        y, x = np.mgrid[:140, :180]
        img = np.zeros((140, 180, 4), np.uint8)
        img[..., 0] = (x * 1.3 + rng.integers(0, 40, x.shape)).clip(0, 255)
        img[..., 1] = (y * 1.6 + rng.integers(0, 40, x.shape)).clip(0, 255)
        img[..., 2] = ((x + y) * .6 + rng.integers(0, 40, x.shape)).clip(0, 255)
        img[..., 3] = 255
        return img

    def test_without_jev_the_rule_chooses_and_the_result_is_still_exact(self):
        import os
        import exact
        old = os.environ.get("KOSIF_JEV_URL")
        os.environ["KOSIF_JEV_URL"] = "off"
        try:
            rgba = self.photo()
            bk, fk, info = exact.choose_plan(rgba)
        finally:
            if old is None:
                os.environ.pop("KOSIF_JEV_URL", None)
            else:
                os.environ["KOSIF_JEV_URL"] = old
        self.assertEqual(info["by"], "rule")
        self.assertIn(info["choice"], exact.PLANS)
        self.assertEqual(set(info["candidates"]), set(exact.PLANS))
        canvas = np.zeros_like(rgba).reshape(-1, 4)
        for *_, order, cols in exact.plan(rgba, bk, fk):
            canvas[order] = cols
        self.assertEqual(exact.mismatches(canvas.reshape(rgba.shape), rgba), 0)

    def test_final_touches_go_from_visible_to_invisible(self):
        import exact
        labels = [(lb, w) for lb, kind, origin, w, o, c in exact.plan(self.photo(), 6, 32) if "اللمسات" in lb]
        weights = [w for _, w in labels]
        self.assertGreaterEqual(len(labels), 2)
        self.assertEqual(weights, sorted(weights, reverse=True), labels)


class Html(unittest.TestCase):
    """HTML pages render in headless Edge and are painted like an exact frame; skipped where no browser exists."""

    def test_html_kind_is_recognised(self):
        import runner
        self.assertEqual(runner.kind_of("<!doctype html><html><body><script>1</script></body></html>"), "html")
        self.assertEqual(runner.kind_of("<svg xmlns='x'><rect/></svg>"), "svg")

    def test_a_page_renders_to_the_pixels_it_draws(self):
        import html_render
        try:
            html_render.browser_path()
        except RuntimeError:
            self.skipTest("no Edge/Chrome")
        tmp = Path(tempfile.mkdtemp())
        (tmp / "p.html").write_text('<!doctype html><html><body style="margin:0;background:#102030">'
                                    '<div style="position:absolute;left:100px;top:50px;width:200px;height:100px;background:#ff3300"></div>'
                                    '<script>window.__ready=true</script></body></html>', encoding="utf-8")
        info = html_render.render_html(tmp / "p.html", tmp / "p.png", 400, 200)
        im = Image.open(tmp / "p.png").convert("RGB")
        self.assertEqual(im.size, (400, 200), info)
        self.assertEqual(im.getpixel((200, 100)), (255, 51, 0))
        self.assertEqual(im.getpixel((20, 20)), (16, 32, 48))
        shutil.rmtree(tmp, ignore_errors=True)


class Film(unittest.TestCase):
    def test_drawing_film_encodes(self):
        import film
        if not shutil.which("ffmpeg"):
            self.skipTest("no ffmpeg")
        tmp = Path(tempfile.mkdtemp())
        (tmp / "s.py").write_text("def build():\n    return [Step('a', [fill(rect(0, 0, 1200, 800), '#204060')]), Step('b', [fill(ellipse(600, 400, 200, 200), '#ffcc00')], 'grow', origin=(600, 400))]\n", encoding="utf-8")
        info = film.film_drawing(str(tmp / "s.py"), tmp / "s.mp4", fps=12, speed="fast", hold=0.2)
        self.assertTrue((tmp / "s.mp4").exists() and (tmp / "s.mp4").stat().st_size > 1000, info)
        self.assertGreater(info["frames"], 3)
        shutil.rmtree(tmp, ignore_errors=True)


class Runner(unittest.TestCase):
    """Code from any AI runs in its own process and comes back as paint jobs."""

    def run_code(self, name):
        out = Path(tempfile.mkdtemp())
        r = subprocess.run([sys.executable, str(HERE / "runner.py"), str(HERE / "examples" / name), str(out)],
                           capture_output=True, timeout=240)
        info = json.loads((out / "done.json").read_text(encoding="utf-8")) if (out / "done.json").exists() else None
        err = (out / "error.txt").read_text(encoding="utf-8") if (out / "error.txt").exists() else None
        jobs = len(list(out.glob("job_*.npz")))
        shutil.rmtree(out, ignore_errors=True)
        return r.returncode, info, err, jobs

    def test_pil_code_is_drawn_in_the_codes_own_order(self):
        rc, info, err, jobs = self.run_code("pil_house.py")
        self.assertEqual(rc, 0, err)
        self.assertEqual(info["kind"], "pil")
        self.assertGreater(jobs, 5)

    def test_raster_code_is_painted_at_its_own_size_and_matches_it(self):
        out = Path(tempfile.mkdtemp())
        subprocess.run([sys.executable, str(HERE / "runner.py"), str(HERE / "examples" / "pil_house.py"), str(out)],
                       capture_output=True, timeout=240)
        c = json.loads((out / "canvas.json").read_text(encoding="utf-8"))
        canvas = np.zeros((c["w"] * c["h"], 4), np.uint8)
        for f in sorted(out.glob("job_*.npz")):
            with np.load(f) as z:
                canvas[z["order"]] = z["cols"]
        final = np.asarray(Image.open(out / "final.png").convert("RGBA")).reshape(-1, 4)
        shutil.rmtree(out, ignore_errors=True)
        self.assertEqual((c["w"], c["h"]), (800, 600))
        self.assertEqual(int(np.any(canvas != final, axis=1).sum()), 0)

    def test_image_code_is_drawn_identical_to_the_original(self):
        tmp = Path(tempfile.mkdtemp())
        Image.fromarray(sample_logo(), "RGBA").save(tmp / "logo.png")
        (tmp / "logo_code.py").write_text(studio.image_code(tmp / "logo.png", "logo"), encoding="utf-8")
        out = tmp / "run"
        subprocess.run([sys.executable, str(HERE / "runner.py"), str(tmp / "logo_code.py"), str(out)],
                       capture_output=True, timeout=240)
        c = json.loads((out / "canvas.json").read_text(encoding="utf-8"))
        info = json.loads((out / "done.json").read_text(encoding="utf-8"))
        canvas = np.zeros((c["w"] * c["h"], 4), np.uint8)
        for f in sorted(out.glob("job_*.npz")):
            with np.load(f) as z:
                canvas[z["order"]] = z["cols"]
        original = np.asarray(Image.open(tmp / "logo.png").convert("RGBA")).reshape(-1, 4)
        shutil.rmtree(tmp, ignore_errors=True)
        self.assertEqual(info["kind"], "image")
        self.assertGreater(info["jobs"], 1)
        self.assertEqual(int(np.any(canvas != original, axis=1).sum()), 0)

    def test_image_code_is_read_as_data_and_never_executed(self):
        import base64
        import io
        import runner
        buf = io.BytesIO()
        Image.new("RGB", (4, 3), "red").save(buf, "PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        code = "\n".join(['import os', 'os.remove("nothing-here")', 'TITLE = "t"', f'IMAGE_B64 = "{b64}"', ''])
        self.assertEqual(runner.kind_of(code), "image")
        title, data = runner.read_image_code(code)              # would raise if os.remove had run
        self.assertEqual((title, Image.open(io.BytesIO(data)).size), ("t", (4, 3)))
        with self.assertRaises(ValueError):
            runner.read_image_code('IMAGE_B64 = open("x").read()')

    def test_broken_code_reports_the_real_error(self):
        rc, info, err, _ = self.run_code("broken_code.py")
        self.assertNotEqual(rc, 0)
        self.assertIn("bluee", err)


class EditPack(unittest.TestCase):
    """🧩: the package an AI edits, the key the studio restores, and an edit confined to its region."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        im = Image.new("RGB", (200, 120), "#204060")
        ImageDraw.Draw(im).rectangle([40, 30, 120, 90], fill="#8a8a8a")        # the grey shirt
        im.save(self.tmp / "me.png")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_package_has_instructions_description_request_and_program(self):
        import edit_pack
        pack = edit_pack.package(self.tmp / "me.png", "me", "غيّر لون القميص إلى الأحمر")
        for part in ("# EDITS START", "# EDITS END", "## وصف الصورة", "غيّر لون القميص إلى الأحمر", "<<KOSIF:ORIGINAL:",
                     "200×120", "recolor("):
            self.assertIn(part, pack)
        self.assertNotIn("iVBOR", pack)                                       # the image itself is not in the package

    def test_edit_program_is_restored_run_and_confined_to_the_region(self):
        import edit_pack
        import runner
        program, sha = edit_pack.edit_program(self.tmp / "me.png", "me")
        self.assertEqual(runner.kind_of(program), "python")                  # tools inside: it runs, not read as data
        self.assertEqual(studio.risky(program), [])
        edited = program.replace("\n# EDITS END", '\nrecolor(img, "#8a8a8a", "#c0392b", tolerance=30, region=(30, 20, 130, 100))\n# EDITS END')
        edited = edited.replace(f'IMAGE_B64 = "<<KOSIF:ORIGINAL:{sha}>>"', f"IMAGE_B64 = '<<KOSIF:ORIGINAL:{sha}>>'  # key")
        with self.assertRaises(SystemExit):                                   # the key alone cannot run
            exec(compile(edited, "<edit>", "exec"), {"__name__": "__main__"})
        code, restored = edit_pack.restore(edited)                            # however the AI quoted the key line
        self.assertTrue(restored)
        self.assertNotIn("<<KOSIF:ORIGINAL:" + sha, code)
        self.assertIn("IMAGE_B64 = (\n", code)
        (self.tmp / "e.py").write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, "e.py"], cwd=self.tmp, capture_output=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = np.asarray(Image.open(self.tmp / "me_edited.png").convert("RGB")).astype(int)
        self.assertLessEqual(int(np.abs(out[60, 80] - (0xc0, 0x39, 0x2b)).max()), 3)   # the shirt is red now (HSV rounding)
        self.assertEqual(tuple(out[10, 10]), (0x20, 0x40, 0x60))               # the background is untouched
        with self.assertRaises(FileNotFoundError):
            edit_pack.restore('IMAGE_B64 = "<<KOSIF:ORIGINAL:0000000000000000>>"')

    def test_code_is_extracted_from_an_ai_reply_or_the_whole_package(self):
        import edit_pack
        pack = edit_pack.package(self.tmp / "me.png", "me", "x")
        self.assertTrue(studio.extract_code(pack).startswith("# -*- coding: utf-8 -*-"))      # the package itself
        reply = "تفضل، هذا البرنامج بعد التعديل:\n\n```python\nimport io\nx = 1\n```\n\nغيّرت لون القميص."
        self.assertEqual(studio.extract_code(reply), "import io\nx = 1")                      # explanations around
        self.assertEqual(studio.extract_code("```\n<svg/>\n```"), "<svg/>")
        self.assertEqual(studio.extract_code("  print(1)\n"), "print(1)")                    # bare code

    def test_edited_program_is_painted_by_the_runner_original_first(self):
        import edit_pack
        program, _ = edit_pack.edit_program(self.tmp / "me.png", "me")
        code, _ = edit_pack.restore(program.replace("\n# EDITS END", '\nrecolor(img, "#8a8a8a", "#2ecc71", 30)\n# EDITS END'))
        (self.tmp / "e.py").write_text(code, encoding="utf-8")
        out = self.tmp / "run"
        subprocess.run([sys.executable, str(HERE / "runner.py"), str(self.tmp / "e.py"), str(out)], capture_output=True, timeout=240)
        jobs = sorted(out.glob("job_*.npz"))
        self.assertGreaterEqual(len(jobs), 2)                                 # the original, then the edit
        c = json.loads((out / "canvas.json").read_text(encoding="utf-8"))
        canvas = np.zeros((c["w"] * c["h"], 4), np.uint8)
        for f in jobs:
            with np.load(f) as z:
                canvas[z["order"]] = z["cols"]
        final = np.asarray(Image.open(out / "final.png").convert("RGBA")).reshape(-1, 4)
        self.assertEqual(int(np.any(canvas != final, axis=1).sum()), 0)
        px = final.reshape(c["h"], c["w"], 4)[60, 80, :3].astype(int)
        self.assertLessEqual(int(np.abs(px - (0x2e, 0xcc, 0x71)).max()), 3)


class LocalEditAndAi(unittest.TestCase):
    """Colour requests understood without an AI; the AI bridge's backends; a film from an image."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        im = Image.new("RGB", (160, 100), "#204060")
        ImageDraw.Draw(im).rectangle([30, 20, 110, 80], fill="#8a8a8a")
        im.save(self.tmp / "shirt.png")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_colour_requests_are_parsed_in_arabic_and_english(self):
        import edit_pack as E
        self.assertEqual(E.parse_colour_request("غيّر الذهبي إلى الأزرق"), ("#d4a53a", "#2f6fd6"))
        self.assertEqual(E.parse_colour_request("غيّر لون القميص الرمادي إلى الأحمر"), ("#8a8a8a", "#d62828"))
        self.assertEqual(E.parse_colour_request("اجعل الأبيض وردياً"), ("#f5f5f5", "#f06aa8"))
        self.assertEqual(E.parse_colour_request("change the grey shirt to red"), ("#8a8a8a", "#d62828"))
        self.assertEqual(E.parse_colour_request("make the gold blue"), ("#d4a53a", "#2f6fd6"))
        self.assertIsNone(E.parse_colour_request("غيّر لون القميص إلى الأحمر"))     # which thing is the shirt? an AI's job
        self.assertIsNone(E.parse_colour_request("make it brighter"))

    def test_local_edit_recolours_the_nearest_layer_and_runs(self):
        import edit_pack as E
        local = E.local_edit(self.tmp / "shirt.png", "غيّر الرمادي إلى الأحمر")
        self.assertIsNotNone(local)
        self.assertIn('recolor(img, "#8a8a8a", "#d62828"', local[0])
        program, _ = E.edit_program(self.tmp / "shirt.png", "shirt")
        code, ok = E.restore(E.with_edits(program, local[0]))
        self.assertTrue(ok)
        self.assertNotIn("مثال", code)                                            # the example comment is gone
        (self.tmp / "e.py").write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, "e.py"], cwd=self.tmp, capture_output=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = np.asarray(Image.open(self.tmp / "shirt_edited.png").convert("RGB")).astype(int)
        self.assertLessEqual(int(np.abs(out[50, 70] - (0xd6, 0x28, 0x28)).max()), 3)
        self.assertEqual(tuple(out[5, 5]), (0x20, 0x40, 0x60))
        self.assertIsNone(E.local_edit(self.tmp / "shirt.png", "غيّر البنفسجي إلى الأحمر"))   # no such colour here

    def test_ai_bridge_backends_and_fake_cli(self):
        import ai_bridge as A
        A._cache.clear()
        saved = A.SETTINGS
        A.SETTINGS = self.tmp / "settings.json"
        try:
            A.save_settings({"backend": "none"})
            self.assertIsNone(A.backend())
            with self.assertRaises(RuntimeError):
                A.ask("x")
            fake = self.tmp / "fake_claude.py"
            fake.write_text("import sys\nprint('```python\\nimport io\\nx = 1\\n```')\n", encoding="utf-8")
            A.save_settings({"backend": "cli"})
            A._cache["cli"] = (True, "fake", 1e12)
            real = A.claude_cli
            A.claude_cli = lambda: sys.executable
            try:
                A._run_cli_args = None
                orig = A._run_cli

                def run(cli, prompt, timeout):
                    return orig(sys.executable, prompt, timeout) if False else subprocess.run(
                        [sys.executable, str(fake)], capture_output=True, text=True, encoding="utf-8", timeout=timeout).stdout
                A._run_cli = run
                self.assertEqual(A.backend(), "cli")
                self.assertIn("x = 1", studio.extract_code(A.ask("anything")))
            finally:
                A._run_cli, A.claude_cli = orig, real
            A.save_settings({"backend": "api", "anthropic_api_key": ""})
            A._cache.clear()
            self.assertIsNone(A.backend())                                       # api chosen but no key
            self.assertIn("cli", A.status())
        finally:
            A.SETTINGS = saved
            A._cache.clear()

    def test_a_film_can_be_made_from_an_image(self):
        import film
        if not shutil.which("ffmpeg"):
            self.skipTest("ffmpeg not on PATH")
        Image.new("RGB", (48, 32), "#c03020").save(self.tmp / "tiny.png")
        info = film.film_drawing(str(self.tmp / "tiny.png"), self.tmp / "tiny.mp4", fps=10, speed="fast", hold=0.2)
        self.assertTrue((self.tmp / "tiny.mp4").exists() and (self.tmp / "tiny.mp4").stat().st_size > 500, info)


@unittest.skipUnless((HERE / "motion" / "motion.py").is_file(),
                     "scripts/motion/ is not shipped in this package (see hyperframes-animation-studio)")
class Motion(unittest.TestCase):
    """KOSIF Motion: a project from the template, the kit's contract, the ambience synth, the measure."""

    def test_new_project_has_the_hyperframes_contract_and_the_kit(self):
        sys.path.insert(0, str(HERE / "motion"))
        import motion
        tmp = Path(tempfile.mkdtemp())
        old = motion.PROJECTS
        motion.PROJECTS = tmp
        try:
            d = motion.new("demo", 5, 30, "1280x720", "تجربة")
            html = (d / "index.html").read_text(encoding="utf-8")
            for part in ('data-composition-id="root"', 'data-width="1280"', 'data-duration="5"', 'window.__timelines["root"] = tl',
                         '.shim("root", 5)', "assets/motion-kit.js"):
                self.assertIn(part, html)
            self.assertNotIn('<html lang="ar" dir', html)                      # dir=rtl on <html> breaks HyperFrames renders
            self.assertTrue((d / "assets" / "motion-kit.js").exists())
            self.assertEqual(motion.duration_of(d / "index.html"), 5.0)
        finally:
            motion.PROJECTS = old
            shutil.rmtree(tmp, ignore_errors=True)
        kit = (HERE / "motion" / "kit" / "motion-kit.js").read_text(encoding="utf-8")
        for name in ("revealWords", "drawPath", "rain", "vapour", "camera", "grain", "vignette", "shim", "register", "spring", "track", "zoomTrack", "beats", "clip-path"):
            self.assertIn(name, kit)
        self.assertNotIn("Math.random", kit)                                   # seeded only

    def test_ambience_is_deterministic_stereo_audio(self):
        sys.path.insert(0, str(HERE / "motion"))
        import ambience
        a = ambience.synth(2.0, [(0.5, 1.5)], [0.8], [0.2], [(0, "A"), (1, "F")], seed=3)
        b = ambience.synth(2.0, [(0.5, 1.5)], [0.8], [0.2], [(0, "A"), (1, "F")], seed=3)
        self.assertEqual(a.shape, (2 * ambience.SR, 2))
        self.assertTrue(np.array_equal(a, b))
        self.assertLessEqual(float(np.abs(a).max()), 0.86)
        tmp = Path(tempfile.mkdtemp())
        ambience.write_wav(tmp / "a.wav", a)
        self.assertGreater((tmp / "a.wav").stat().st_size, 100000)
        shutil.rmtree(tmp, ignore_errors=True)

    def test_bundle_and_audio_mux_are_wired(self):
        sys.path.insert(0, str(HERE / "motion"))
        import motion
        self.assertTrue(callable(motion.bundle) and callable(motion.mux_audio))
        tmp = Path(tempfile.mkdtemp())
        (tmp / "index.html").write_text('<div data-composition-id="root" data-duration="3"></div>', encoding="utf-8")
        (tmp / "v.mp4").write_bytes(b"")
        self.assertIsNone(motion.mux_audio(tmp / "index.html", tmp / "v.mp4"))       # no <audio>: nothing to do, no crash
        shutil.rmtree(tmp, ignore_errors=True)
        html = (HERE / "motion" / "projects" / "water_cycle_3d" / "index.html").read_text(encoding="utf-8")
        self.assertIn("assets/main.bundle.js", html)
        self.assertIn("window.__three.build", html)
        src = (HERE / "motion" / "projects" / "water_cycle_3d" / "src" / "main.js").read_text(encoding="utf-8")
        kit = (HERE / "motion" / "kit" / "three-kit.js").read_text(encoding="utf-8")
        self.assertIn("three-kit.js", src)
        for part in ("new Sky()", "new Water(", "UnrealBloomPass", "BokehPass", "composer.render(0)"):
            self.assertIn(part, kit)
        for text in (src, kit):
            self.assertNotIn("Math.random", text)
            self.assertNotIn("new THREE.Clock", text)

    def test_3d_template_scaffolds_and_bundles_on_the_three_kit(self):
        sys.path.insert(0, str(HERE / "motion"))
        import motion
        if not (HERE / "motion" / "node_modules" / "esbuild").exists():
            self.skipTest("esbuild not installed in motion/")
        tmp = Path(tempfile.mkdtemp(dir=str(HERE / "motion" / "projects")))     # inside projects/ so ../../../kit resolves
        old = motion.PROJECTS
        try:
            motion.PROJECTS = tmp
            d = motion.new("t3d", 5, 30, "1280x720", "اختبار", three_d=True)
            src = (d / "src" / "main.js").read_text(encoding="utf-8")
            self.assertIn("three-kit.js", src)
            self.assertIn("const SECONDS = 5", src)
            out = motion.bundle(str(d))
            self.assertGreater(out.stat().st_size, 300_000)                   # three.js + addons are inside
            kit = (HERE / "motion" / "kit" / "three-kit.js").read_text(encoding="utf-8")
            for name in ("makeSky", "makeTerrain", "makeForest", "coniferCrown", "makeFlock", "makeSea", "makeCloudSlab", "makePost", "makeFrameLoop", "cameraKeys", "makeRibbon"):
                self.assertIn(f"export function {name}", kit)
            self.assertNotIn("Math.random", kit)
        finally:
            motion.PROJECTS = old
            shutil.rmtree(tmp, ignore_errors=True)

    def test_water_cycle_composition_passes_the_static_rules(self):
        html = (HERE / "motion" / "projects" / "water_cycle" / "index.html").read_text(encoding="utf-8")
        self.assertIn('window.__timelines["root"] = tl', html)
        self.assertIn('<audio id="ambience"', html)
        self.assertNotIn('dir="rtl"', html.split("<body>")[0].split("<style>")[0])
        self.assertNotIn("marker-end", html)
        self.assertNotIn("Math.random", html)


class Studio(unittest.TestCase):
    def test_scenes_and_loading(self):
        self.assertIn("dragon_girl", studio.scenes())
        title, steps, rolloff = studio.load("dragon_girl")
        self.assertEqual(len(steps), 22)
        self.assertEqual(rolloff, 0.82)

    def test_a_traced_logo_loads_as_an_exact_colour_scene(self):
        tmp = Path(tempfile.mkdtemp())
        Image.fromarray(sample_logo(), "RGBA").save(tmp / "logo.png")
        data = vectorize.trace(tmp / "logo.png")
        shutil.rmtree(tmp, ignore_errors=True)
        self.assertFalse(data["photo"])
        self.assertGreaterEqual(len(data["layers"]), 4)
        R.render_image(vector_scene.build(data), .25, rolloff=1.0)

    def test_code_kinds_and_risk_check(self):
        import runner
        self.assertEqual(runner.kind_of("<svg viewBox='0 0 1 1'></svg>"), "svg")
        self.assertEqual(runner.kind_of("def build():\n    return []"), "scene")
        self.assertEqual(runner.kind_of("from PIL import Image"), "python")
        self.assertEqual(studio.risky("from PIL import Image, ImageDraw\nimg.save('a.png')"), [])
        self.assertTrue(studio.risky("import os\nos.remove('x')"))
        self.assertTrue(studio.risky("import requests"))
        self.assertEqual(studio.risky("<svg><text>os.remove</text></svg>"), [])


if __name__ == "__main__":
    unittest.main()
