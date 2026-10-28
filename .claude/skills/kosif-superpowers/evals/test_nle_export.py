"""Tests for scripts/nle_export.py: FCPXML, FCP7 XML, CMX3600 EDL, Blender VSE script, SRT and CapCut list.

Media files are placeholders (the exporter never decodes them); ffprobe failures fall back to timeline lengths.
When OpenTimelineIO (with its fcpx_xml, fcp_xml and cmx_3600 adapters) or Blender's bpy module is importable,
the written files are also read back by those independent implementations.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import nle_export as ne  # noqa: E402

REAL_PROBE = ne.probe

import importlib.util

HAVE_BPY = importlib.util.find_spec("bpy") is not None
try:
    import opentimelineio as otio  # noqa: F401
    HAVE_OTIO = True
except ImportError:
    HAVE_OTIO = False


def project(d):
    for name in ("لقطة 1.mp4", "logo.png", "music.wav"):
        (d / name).write_bytes(b"placeholder")
    doc = {"schema": ne.TIMELINE_SCHEMA, "name": "تجربة reel", "width": 1080, "height": 1920, "fps": 30, "duration": 5,
           "tracks": [
               {"id": "picture", "kind": "video", "layer": 0, "clips": [
                   {"id": "v1", "path": "لقطة 1.mp4", "start": 0, "in": 0.5, "duration": 2, "include_audio": True,
                    "fade_out": 0.3},
                   {"id": "v2", "path": "لقطة 1.mp4", "start": 2, "in": 1, "duration": 2.5}]},
               {"id": "logo", "kind": "image", "layer": 2, "clips": [
                   {"id": "g1", "path": "logo.png", "start": 1, "duration": 2, "x": 340, "y": 100, "width": 400,
                    "height": 200, "fade_in": 0.2}]},
               {"id": "music", "kind": "audio", "clips": [
                   {"id": "a1", "path": "music.wav", "start": 0, "in": 0.2, "duration": 5, "volume": 0.25,
                    "fade_in": 0.5}]}]}
    p = d / "project.json"
    p.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    (d / "words.json").write_text(json.dumps({"words": [
        {"word": "أهلا", "start": 0.1, "end": 0.4}, {"word": "بيكم", "start": 0.45, "end": 0.8},
        {"word": "في", "start": 1.5, "end": 1.6}, {"word": "KOSIF", "start": 1.65, "end": 2.1}]}, ensure_ascii=False),
        encoding="utf-8")
    return p


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory(prefix="kosif-nle-")
        self.d = Path(self.td.name)
        self.p = project(self.d)
        self.out = self.d / "out"
        ne.probe = lambda path: {}          # deterministic: no ffprobe on placeholders
        self.receipt = ne.export(ne.load(self.p), self.out, set(ne.FORMATS), self.d / "words.json")
        self.files = {f["file"] for f in self.receipt["files"]}

    def tearDown(self):
        ne.probe = REAL_PROBE
        self.td.cleanup()

    def read(self, suffix):
        name = next(n for n in self.files if n.endswith(suffix))
        return (self.out / name).read_text(encoding="utf-8")

    def test_every_format_written_with_receipt(self):
        for suffix in (".fcpxml", ".premiere.xml", ".picture.edl", ".music.edl", ".blender_vse.py", ".srt",
                       ".capcut.md", "HANDOFF.md"):
            self.assertTrue(any(n.endswith(suffix) for n in self.files), suffix)
        r = json.loads((self.out / "receipt.json").read_text(encoding="utf-8"))
        self.assertEqual((r["frames"], r["clips"], r["captions"]), (150, 4, 2))
        self.assertEqual(r["max_snap_drift_ms"], 0.0)
        self.assertTrue(any("fades" in g for g in r["not_carried"]))

    def test_fcpxml_lanes_times_and_paths(self):
        root = ET.fromstring(self.read(".fcpxml"))
        self.assertEqual(root.get("version"), "1.9")
        clips = {c.get("name"): c for c in root.iter() if c.tag in ("asset-clip", "clip")}
        self.assertEqual((clips["v1"].get("lane"), clips["v1"].get("start"), clips["v1"].get("duration")),
                         ("1", "1/2s", "2s"))
        self.assertEqual(clips["v1"].get("srcEnable"), "all")
        self.assertEqual(clips["v2"].get("srcEnable"), "video")
        self.assertEqual((clips["g1"].get("lane"), clips["g1"].get("offset")), ("2", "1s"))
        self.assertEqual(clips["a1"].get("lane"), "-1")
        self.assertEqual(clips["a1"].find("adjust-volume").get("amount"), "-12.04dB")
        srcs = [m.get("src") for m in root.iter("media-rep")]
        self.assertIn((self.d / "لقطة 1.mp4").resolve().as_uri(), srcs)

    def test_xmeml_tracks_and_frames(self):
        root = ET.fromstring(self.read(".premiere.xml"))
        vtracks = root.findall("./sequence/media/video/track")
        atracks = root.findall("./sequence/media/audio/track")
        self.assertEqual((len(vtracks), len(atracks)), (2, 2))
        v1 = vtracks[0].find("clipitem")
        self.assertEqual([v1.findtext(k) for k in ("start", "end", "in", "out")], ["0", "60", "15", "75"])
        level = atracks[1].find(".//parameter/value").text
        self.assertAlmostEqual(float(level), 0.25)

    def test_edl_events(self):
        edl = self.read(".picture.edl").splitlines()
        self.assertIn("FCM: NON-DROP FRAME", edl)
        self.assertIn("001  AX       V     C        00:00:00:15 00:00:02:15 00:00:00:00 00:00:02:00", edl)
        self.assertIn("002  AX       V     C        00:00:01:00 00:00:03:15 00:00:02:00 00:00:04:15", edl)
        self.assertIn(" AA ", self.read(".music.edl"))

    def test_blender_script_compiles_and_embeds_strips(self):
        src = self.read(".blender_vse.py")
        compile(src, "vse.py", "exec")
        data = json.loads(src.split('json.loads(r"""', 1)[1].split('""")', 1)[0])
        by = {s["name"]: s for s in data["strips"]}
        self.assertEqual((by["v1"]["channel"], by["g1"]["channel"], by["v1-audio"]["channel"], by["a1"]["channel"]),
                         (1, 2, 3, 4))
        self.assertEqual((by["v1"]["in"], by["v1"]["dur"], by["v1"]["fade_out"]), (15, 60, 9))

    def test_srt_and_capcut(self):
        srt = self.read(".srt")
        self.assertIn("00:00:00,100 --> 00:00:00,800\nأهلا بيكم", srt)
        self.assertIn("في KOSIF", srt)
        self.assertIn("| 1 | picture | v1 |", self.read(".capcut.md"))

    def test_refuses_overwrite_and_bad_input(self):
        with self.assertRaises(FileExistsError):
            ne.export(ne.load(self.p), self.out, {"fcpxml"})
        bad = self.d / "bad.json"
        bad.write_text(json.dumps({"schema": "nope"}), encoding="utf-8")
        with self.assertRaises(ValueError):
            ne.load(bad)
        doc = json.loads(self.p.read_text(encoding="utf-8"))
        doc["tracks"][0]["clips"][0]["path"] = "missing.mp4"
        self.p.write_text(json.dumps(doc), encoding="utf-8")
        with self.assertRaises(ValueError):
            ne.load(self.p)
        self.assertEqual(ne.load(self.p, allow_missing=True).frames, 150)

    def test_cut_plan_input(self):
        plan = {"schema": ne.EDL_SCHEMA, "video": {"fps": 30, "width": 1080, "height": 1920, "frame_count": 90},
                "scenes": [{"id": "SCENE-001", "start_frame": 0, "end_frame_exclusive": 45,
                            "footage_path": str(self.d / "لقطة 1.mp4"), "video_trim": {"in": 0, "out": 1.5}},
                           {"id": "SCENE-002", "start_frame": 45, "end_frame_exclusive": 90, "footage_path": None}]}
        pp = self.d / "plan.json"
        pp.write_text(json.dumps(plan), encoding="utf-8")
        tl = ne.load(pp, audio=self.d / "music.wav")
        self.assertEqual([t["id"] for t in tl.tracks], ["V1", "VO"])
        self.assertTrue(any("SCENE-002" in w for w in tl.warnings))

    def test_cli(self):
        res = subprocess.run([sys.executable, str(SCRIPTS / "nle_export.py"), "export", "--project", str(self.p),
                              "--out", str(self.d / "cli"), "--formats", "fcpxml,edl", "--words", str(self.d / "words.json")],
                             capture_output=True, text=True, timeout=60)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        out = json.loads(res.stdout)
        self.assertEqual(out["status"], "written")
        self.assertTrue(any(f.endswith(".srt") for f in out["files"]))

    @unittest.skipUnless(HAVE_OTIO, "opentimelineio not installed")
    def test_opentimelineio_reads_back(self):
        import opentimelineio as otio
        names = otio.adapters.available_adapter_names()
        checks = [(".fcpxml", "fcpx_xml", {}), (".premiere.xml", "fcp_xml", {}), (".picture.edl", "cmx_3600", {"rate": 30})]
        for suffix, adapter, kw in checks:
            if adapter not in names:
                continue
            path = self.out / next(n for n in self.files if n.endswith(suffix))
            tl = otio.adapters.read_from_file(str(path), adapter_name=adapter, **kw)
            if isinstance(tl, otio.schema.SerializableCollection):   # FCP readers wrap timelines in a collection
                tl = next(x for x in tl if isinstance(x, otio.schema.Timeline))
            frames = sorted((tr.range_of_child(c).start_time.to_frames(), c.source_range.start_time.to_frames())
                            for tr in tl.video_tracks() for c in tr if isinstance(c, otio.schema.Clip))
            self.assertIn((0, 15), frames, adapter)
            self.assertIn((60, 30), frames, adapter)


    @unittest.skipUnless(HAVE_BPY, "Blender's bpy module not installed")
    def test_blender_builds_the_sequencer(self):
        script = self.out / next(n for n in self.files if n.endswith(".blender_vse.py"))
        res = subprocess.run([sys.executable, "-W", "ignore", str(script)], capture_output=True, text=True, timeout=300)
        self.assertEqual(res.returncode, 0, res.stderr[-2000:])
        line = next(x for x in res.stdout.splitlines() if x.startswith("KOSIF_VSE "))
        got = {s["name"]: (s["channel"], s["start"], s["end"]) for s in json.loads(line[10:])["strips"]}
        self.assertEqual(got, {"v1": (1, 1, 61), "v2": (1, 61, 136), "g1": (2, 31, 91), "v1-audio": (3, 1, 61),
                               "a1": (4, 1, 151)})


if __name__ == "__main__":
    unittest.main()
