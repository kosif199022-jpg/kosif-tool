#!/usr/bin/env python3
"""Self-tests for the Living Site gate tools (KOSIF v5.11). Run: python3 tests/test_tools.py

Pure-Python tests always run. Media tests (cutscan, continuity gate, living loop) run only when
ffmpeg and zsh are on PATH, and say "skipped" otherwise: a skip is never reported as a pass.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, SKILL)
sys.path.insert(0, os.path.join(SKILL, 'tools'))
import check  # noqa: E402
import ledger  # noqa: E402
import kling_lint  # noqa: E402

GOOD = '''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>t</title></head><body>
<div id="flow" data-xray-tool="code" data-xray="مسار · SVG">x</div>
<p>علامة خيالية لعرض تجريبي</p>
<script>new IntersectionObserver(()=>{});window.__ready=true;</script>
<style>@media (prefers-reduced-motion: reduce){*{animation:none}}</style></body></html>'''


def page(tmp, body):
    p = os.path.join(tmp, 'index.html')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(body)
    return p


def names(r, status='FAIL'):
    return [t['name'] for t in r['tests'] if t['status'] == status]


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_level3_partial_build_passes(self):
        r = check.run(page(self.tmp, GOOD), (3,))
        self.assertTrue(r['pass'], r['fails'])
        self.assertTrue(all(n.startswith(('L1', 'L2')) for n in r['skipped']))

    def test_full_build_needs_all_levels(self):
        r = check.run(page(self.tmp, GOOD), (1, 2, 3))
        self.assertIn('L1 live 3D on the page', r['fails'])
        self.assertIn('L2 Higgsfield film or living loop', r['fails'])

    def test_attribute_order_does_not_matter(self):
        body = GOOD.replace('data-xray-tool="code" data-xray="مسار · SVG"', 'data-xray="مسار · SVG" class="a" data-xray-tool="code"')
        self.assertTrue(check.run(page(self.tmp, body), (3,))['pass'])

    def test_three_spline_scenes_fail(self):
        scenes = ''.join(f'<iframe src="https://my.spline.design/s{i}/"></iframe>' for i in range(3))
        r = check.run(page(self.tmp, GOOD.replace('<p>', scenes + '<script src="vendor/spline-shield.js"></script><p>')), (1, 3))
        self.assertIn('L1 at most two 3D showpieces', r['fails'])

    def test_two_spline_scenes_ok(self):
        scenes = ''.join(f'<iframe src="https://my.spline.design/s{i}/"></iframe>' for i in range(2))
        r = check.run(page(self.tmp, GOOD.replace('<p>', scenes + '<div class="sp-shield"></div><p>')), (1, 3))
        self.assertNotIn('L1 at most two 3D showpieces', r['fails'])

    def test_arabic_negative_letter_spacing_fails(self):
        r = check.run(page(self.tmp, GOOD.replace('</style>', 'h1{letter-spacing:-.03em}</style>')), (3,))
        self.assertIn('Arabic: no negative letter-spacing (breaks joining)', r['fails'])

    def test_guarded_latin_tracking_ok(self):
        js = "<script>if (!/[\\u0600-\\u06FF]/.test(s)) el.setAttribute('letter-spacing', '-0.4');</script>"
        r = check.run(page(self.tmp, GOOD.replace('<p>', js + '<p>')), (3,))
        self.assertTrue(r['pass'], r['fails'])

    def test_missing_charset_fails(self):
        r = check.run(page(self.tmp, GOOD.replace('<meta charset="utf-8">', '')), (3,))
        self.assertIn('charset declared (utf-8)', r['fails'])

    def test_dash_in_copy_fails(self):
        r = check.run(page(self.tmp, GOOD.replace('لعرض تجريبي', 'لعرض — تجريبي')), (3,))
        self.assertIn('no em or en dashes in visible copy', r['fails'])

    def test_generated_piece_needs_cost(self):
        vid = '<video src="loops/a.mp4" data-xray="loop" data-xray-tool="higgsfield"></video>'
        os.makedirs(os.path.join(self.tmp, 'loops'))
        open(os.path.join(self.tmp, 'loops', 'a.mp4'), 'w').close()
        r = check.run(page(self.tmp, GOOD.replace('<p>', vid + '<p>')), (2, 3))
        self.assertIn('L2 every generated piece shows its cost (data-xray-cost)', r['fails'])
        r = check.run(page(self.tmp, GOOD.replace('<p>', vid.replace('>', ' data-xray-cost="30">', 1) + '<p>')), (2, 3))
        self.assertTrue(r['pass'], r['fails'])

    def test_missing_asset_fails(self):
        r = check.run(page(self.tmp, GOOD.replace('<p>', '<img src="img/none.png"><p>')), (3,))
        self.assertIn('every local asset exists', r['fails'])

    def test_cli_rejects_bad_levels(self):
        self.assertEqual(check.main([page(self.tmp, GOOD), '--levels', '4']), 2)
        self.assertEqual(check.main([page(self.tmp, GOOD), '--levels']), 2)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.l = os.path.join(self.tmp, 'ledger.tsv')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_sum_and_quote(self):
        ledger.main(['add', self.l, 'nano_banana_2', '2', 'j1', 'kf/k1.png'])
        ledger.main(['add', self.l, 'seedance_2_0', '60', 'j2', 'film/c1.mp4'])
        self.assertEqual(ledger.main(['sum', self.l, '--quote', '62']), 0)
        self.assertEqual(ledger.main(['sum', self.l, '--quote', '50']), 1)
        self.assertEqual(ledger.main(['sum', self.l, '--budget', '61']), 1)

    def test_duplicate_job_refused(self):
        ledger.main(['add', self.l, 'm', '2', 'j1', 'a'])
        with self.assertRaises(SystemExit):
            ledger.main(['add', self.l, 'm', '2', 'j1', 'a'])

    def test_duplicate_in_file_fails_sum(self):
        with open(self.l, 'w') as fh:
            fh.write('t\tm\t2\tj1\ta\nt\tm\t2\tj1\ta\n')
        self.assertEqual(ledger.main(['sum', self.l]), 1)


class KlingLintTests(unittest.TestCase):
    """A41: the master-prompt gate. The recipe prompt passes; each break fails on its own check."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(SKILL, 'recipes', 'kling-master-prompt.txt'), encoding='utf-8') as fh:
            cls.good = fh.read()

    def fails(self, text, **kw):
        return [r['name'] for r in kling_lint.lint(text, **kw) if r['status'] == 'FAIL']

    def warns(self, text):
        return [r['name'] for r in kling_lint.lint(text) if r['status'] == 'warn']

    def test_recipe_passes(self):
        self.assertEqual(self.fails(self.good), [])
        self.assertEqual(self.warns(self.good), [])

    def test_timing_gap_and_wrong_end(self):
        self.assertIn('timing', self.fails(self.good.replace('4.0-8.0s', '5.0-8.0s')))
        self.assertIn('timing', self.fails(self.good.replace('12.0-15.0s', '12.0-14.0s')))

    def test_duration_limits(self):
        self.assertIn('duration', self.fails(self.good, duration=31))
        self.assertIn('duration', self.fails(self.good.replace('15 s, 21:9', '25 s, 21:9'), flash=True))

    def test_words_brands_and_mood(self):
        self.assertIn('polish', self.fails(self.good + '\nflawless skin, 8K'))
        self.assertIn('brands', self.fails(self.good.replace('Neo-noir,', 'Shot on ARRI Alexa, neo-noir,')))
        self.assertIn('mood-cam', self.fails(self.good + '\nDynamic cinematic camera.'))

    def test_references(self):
        self.assertIn('refs', self.fails(self.good.replace(' Do not render the storyboard itself.', '')))
        self.assertIn('refs', self.fails(self.good.replace('pose are not inherited', 'pose follow')))
        kf = self.good.replace('Controlled multi-shot', 'Keyframes mode. Controlled multi-shot') + '\n@Video1 as motion.'
        self.assertIn('limits', self.fails(kf))

    def test_arabic_dialogue_and_wide_face(self):
        self.assertIn('arabic-dlg', self.fails(self.good.replace('English, no dialogue.', 'Sami says: "يلا بسرعة".')))
        self.assertIn('wide-face', self.fails(self.good.replace('Medium close-up 47°', 'Close-up 24mm')))

    def test_negatives_warn_only(self):
        t = self.good.replace('Exactly one person visible;', 'Exactly one person visible; no people in the windows;')
        self.assertEqual(self.fails(t), [])
        self.assertIn('negatives', self.warns(t))

    def test_plan_and_cli(self):
        self.assertEqual(kling_lint.plan(90), [(0, 30), (30, 60), (60, 90)])
        self.assertEqual(kling_lint.plan(45), [(0, 23), (23, 45)])
        self.assertTrue(all(b - a <= 30 for a, b in kling_lint.plan(61)))
        self.assertEqual(kling_lint.main(['plan', '2']), 2)
        self.assertEqual(kling_lint.main(['x.txt', '--duration']), 2)


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('zsh'), 'needs ffmpeg and zsh')
class MediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        ff = ['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi']
        cls.smooth = os.path.join(cls.tmp, 'smooth.mp4')
        subprocess.run(ff + ['-i', 'testsrc2=size=640x360:rate=24', '-t', '3', cls.smooth], check=True)
        a, b = os.path.join(cls.tmp, 'a.mp4'), os.path.join(cls.tmp, 'b.mp4')
        subprocess.run(ff + ['-i', 'testsrc2=size=640x360:rate=24', '-t', '1.5', a], check=True)
        subprocess.run(ff + ['-i', 'mandelbrot=size=640x360:rate=24', '-t', '1.5', b], check=True)
        cls.cut = os.path.join(cls.tmp, 'cut.mp4')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a, '-i', b, '-filter_complex',
                        '[0:v][1:v]concat=n=2:v=1[v]', '-map', '[v]', cls.cut], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp)

    def tool(self, *a):
        return subprocess.run(list(a), capture_output=True, text=True)

    def frames(self, clip):
        d = tempfile.mkdtemp(dir=self.tmp)
        subprocess.run(['ffmpeg', '-v', 'error', '-i', clip, os.path.join(d, 'f_%04d.jpg')], check=True)
        return d

    def test_cutscan(self):
        cs = os.path.join(SKILL, 'tools', 'cutscan.py')
        self.assertEqual(self.tool(sys.executable, cs, self.smooth).returncode, 0)
        self.assertEqual(self.tool(sys.executable, cs, self.cut).returncode, 1)

    def test_continuity_gate(self):
        gate = os.path.join(SKILL, 'tools', 'continuity-gate.sh')
        self.assertEqual(self.tool('zsh', gate, self.frames(self.smooth), '4').returncode, 0)
        r = self.tool('zsh', gate, self.frames(self.cut), '4')
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_living_loop_doubles_length(self):
        out = os.path.join(self.tmp, 'loop.mp4')
        r = self.tool('zsh', os.path.join(SKILL, 'tools', 'living_loop.sh'), self.smooth, out)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        d = float(self.tool('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out).stdout)
        self.assertAlmostEqual(d, 6.0, delta=0.2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
