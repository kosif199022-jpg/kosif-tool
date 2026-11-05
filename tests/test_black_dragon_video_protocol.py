"""Black Dragon mandatory video protocol: order, seals and measured color."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude/skills/kosif-black-dragon/scripts"


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


vp = load("bd_video_protocol", "video_protocol.py")
bd = load("bd_native_for_video", "black_dragon.py")


def poster(path, accent=None, bg=(4, 72, 83)):
    """Teal poster, light grey subject; the hero gets the accent if given."""
    img = Image.new("RGB", (400, 600), bg)
    d = ImageDraw.Draw(img)
    d.rectangle((60, 300, 340, 520), fill=(200, 205, 205))      # subject (support)
    d.rectangle((80, 60, 320, 120), fill=(240, 240, 240))       # title
    if accent:
        d.ellipse((170, 200, 250, 280), fill=accent)            # hero ~2.7%
        d.rectangle((140, 130, 260, 160), fill=accent)          # key word ~1.5%
    img.save(path)
    return path


class VideoProtocolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.job = self.dir / "job"

    def data(self, name, obj):
        p = self.dir / f"{name}.json"
        p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return json.loads(p.read_text(encoding="utf-8"))

    def brief(self):
        return self.data("brief", {"goal": "sell", "audience": "students", "platform": "instagram",
                                   "aspect": "9:16", "duration_s": 15, "message": "one idea lifts",
                                   "hero": "balloon"})

    def walk_to_produce(self, output):
        vp.start("ريل ١٥ ثانية", self.job)
        vp.record(self.job, "brief", self.brief())
        vp.record(self.job, "concept", {"idea": "heavy brand", "metaphor": "hippo + balloon",
                                        "hook": "براندك تقيل؟", "emotion": "قوة"})
        key = poster(self.dir / "key.png")
        r = vp.color(self.job, "color-design", key, rule="contrast")
        self.assertTrue(r["passed"], r)
        vp.record(self.job, "shots", {"shots": [
            {"duration_s": 7, "what": "hippo floats", "accent_on": "balloon"},
            {"duration_s": 8, "what": "title", "accent_on": "key word"}]})
        vp.record(self.job, "produce", {"outputs": [str(output)], "tool": "pil",
                                        "paid": False, "spend_approved": False})
        return r["accent"]

    def test_order_is_enforced(self):
        vp.start("ريل", self.job)
        with self.assertRaisesRegex(ValueError, "out of order"):
            vp.record(self.job, "concept", {"idea": "x", "metaphor": "y", "hook": "z"})
        with self.assertRaisesRegex(ValueError, "missing hero"):
            vp.record(self.job, "brief", {k: v for k, v in self.brief().items() if k != "hero"})

    def test_color_stage_cannot_be_typed_by_hand(self):
        vp.start("ريل", self.job)
        vp.record(self.job, "brief", self.brief())
        vp.record(self.job, "concept", {"idea": "x", "metaphor": "y", "hook": "z"})
        with self.assertRaisesRegex(ValueError, "measured from pixels"):
            vp.record(self.job, "color-design", {"passed": True})

    def test_analyze_finds_accent_only_when_present(self):
        plain = vp.analyze(poster(self.dir / "a.png"))
        self.assertIsNone(plain["accent"])
        lit = vp.analyze(poster(self.dir / "b.png", accent=(245, 108, 90)))
        self.assertIsNotNone(lit["accent"])
        self.assertLess(lit["accent_share"], 0.18)
        self.assertGreaterEqual(lit["accent_pop"], vp.MIN_POP)
        # contrast rule on teal proposes a warm red-orange, like the reference reels
        r, g, b = vp.hex_rgb(lit["suggestions"]["contrast"])
        self.assertGreater(r, g + 80)

    def test_full_path_passes_with_planned_accent(self):
        out = self.dir / "final.png"
        planned = self.walk_to_produce(poster(out, accent=None))
        # re-render the final with the planned accent, then re-record produce
        state = json.loads((self.job / "protocol.json").read_text(encoding="utf-8"))
        del state["stages"]["produce"]
        (self.job / "protocol.json").write_text(json.dumps(state), encoding="utf-8")
        poster(out, accent=vp.hex_rgb(planned))
        vp.record(self.job, "produce", {"outputs": [str(out)], "tool": "pil",
                                        "paid": False, "spend_approved": False})
        qa = vp.color(self.job, "qa-color", out)
        self.assertTrue(qa["passed"], qa)
        vp.record(self.job, "deliver", {"summary": "ok", "executed": ["pil render"],
                                        "not_executed": ["music"]})
        self.assertTrue(vp.check(self.job)["passed"])

    def test_output_without_accent_fails_qa_and_check(self):
        out = poster(self.dir / "flat.png")
        self.walk_to_produce(out)
        qa = vp.color(self.job, "qa-color", out)
        self.assertFalse(qa["passed"])
        vp.record(self.job, "deliver", {"summary": "x", "executed": ["a"], "not_executed": ["b"]})
        res = vp.check(self.job)
        self.assertFalse(res["passed"])
        self.assertTrue(any("qa-color did not pass" in p for p in res["problems"]))

    def test_tampering_and_paid_without_approval_fail(self):
        out = poster(self.dir / "o.png", accent=(245, 108, 90))
        vp.start("ريل", self.job)
        vp.record(self.job, "brief", self.brief())
        state = json.loads((self.job / "protocol.json").read_text(encoding="utf-8"))
        state["stages"]["brief"]["hero"] = "changed"
        (self.job / "protocol.json").write_text(json.dumps(state), encoding="utf-8")
        self.assertTrue(any("edited" in p for p in vp.check(self.job)["problems"]))
        errs = vp.validate("produce", {"outputs": [{"path": str(out), "sha256": vp.sha(out)}],
                                       "tool": "paid-api", "paid": True,
                                       "spend_approved": False}, {})
        self.assertTrue(any("without the owner's approval" in e for e in errs), errs)

    def test_shot_durations_must_match_brief(self):
        vp.start("ريل", self.job)
        vp.record(self.job, "brief", self.brief())
        vp.record(self.job, "concept", {"idea": "x", "metaphor": "y", "hook": "z"})
        vp.color(self.job, "color-design", poster(self.dir / "k.png"), rule="neon")
        with self.assertRaisesRegex(ValueError, "within 20%"):
            vp.record(self.job, "shots", {"shots": [{"duration_s": 40, "what": "a", "accent_on": "b"}]})

    def test_compose_flags_video_tasks_only(self):
        self.assertTrue(bd.video_protocol("اعمل ريل لمنتج قهوة")["mandatory"])
        self.assertTrue(bd.video_protocol("make a promo video"))
        self.assertIsNone(bd.video_protocol("اعمل جدول اكسل للمخزن"))


if __name__ == "__main__":
    unittest.main()
