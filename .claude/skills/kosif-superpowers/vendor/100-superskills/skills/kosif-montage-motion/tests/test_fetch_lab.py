"""v6.2 fetch (yt-dlp, the Cinema C method) and Audio Lab, offline: a local HTTP server stands in for the site."""
from __future__ import annotations

import functools
import http.server
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
FF = shutil.which("ffmpeg")
try:
    import yt_dlp  # noqa: F401
    HAVE_YTDLP = True
except ImportError:
    HAVE_YTDLP = False


def streams(f: Path) -> list[str]:
    r = subprocess.run([shutil.which("ffprobe") or "ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(f)],
                       capture_output=True, text=True)
    return r.stdout.split()


@unittest.skipUnless(FF, "ffmpeg")
class Lab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="kosif_lab_"))
        cls.st = cls.tmp / "st.mp4"                          # a centred tone (the "voice") over a wide stereo bed
        subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=220:d=3", "-f", "lavfi", "-i", "anoisesrc=d=3:c=pink:a=0.3",
                        "-f", "lavfi", "-i", "anoisesrc=d=3:c=pink:a=0.3:seed=7", "-f", "lavfi", "-i", "testsrc2=s=320x180:r=25:d=3",
                        "-filter_complex", "[0:a]volume=0.5,asplit=2[v1][v2];[v1][v2]amerge=inputs=2[vc];[1:a][2:a]amerge=inputs=2[m];[vc][m]amix=inputs=2:normalize=0[a]",
                        "-map", "3:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ac", "2", str(cls.st)], check=True)
        cls.mono = cls.tmp / "mono.wav"
        subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=220:d=2", "-ac", "1", str(cls.mono)], check=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_music_and_video_modes(self):
        import audiolab
        r = audiolab.run(self.st, "novoice", self.tmp / "o1")
        self.assertTrue(r["stereo"]); self.assertIn("music_method", r)
        self.assertEqual(sorted(streams(Path(r["video"]))), ["audio", "video"])
        def band(f):
            e = subprocess.run([FF, "-hide_banner", "-nostdin", "-i", str(f), "-af", "bandpass=f=220:width_type=q:w=30,volumedetect", "-f", "null", "-"],
                               capture_output=True, text=True).stderr
            return float(e.split("mean_volume:")[1].split("dB")[0])
        self.assertLess(band(r["music"]), band(self.st) - 4)          # the centre is cancelled

    def test_mono_refused_for_music(self):
        import audiolab
        with self.assertRaises(SystemExit):
            audiolab.run(self.mono, "music", self.tmp / "o2")


@unittest.skipUnless(FF and HAVE_YTDLP, "ffmpeg + yt-dlp")
class Fetch(unittest.TestCase):
    def test_local_download_edit_copy_credits(self):
        import fetch
        tmp = Path(tempfile.mkdtemp(prefix="kosif_fetch_"))
        src = tmp / "srv"; src.mkdir()
        subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=320x180:r=25:d=2", "-f", "lavfi", "-i", "sine=d=2",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(src / "clip.mp4")], check=True)
        subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=teal:s=64x64", "-frames:v", "1", str(src / "still.png")], check=True)
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(src)))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        try:
            out = tmp / "media"
            r = fetch.fetch([f"{base}/clip.mp4"], out)
            self.assertEqual(len(r["fetched"]), 1, r)
            row = r["fetched"][0]
            self.assertEqual(sorted(streams(Path(row["edit"]))), ["audio", "video"])   # the edit copy keeps the sound
            cred = json.loads((out / "fetch-credits.json").read_text(encoding="utf-8"))
            self.assertEqual(cred[0]["source"], f"{base}/clip.mp4")
            self.assertEqual(fetch.fetch([f"{base}/clip.mp4"], out)["skipped"][0]["why"], "already fetched")
            img = fetch._download_image(f"{base}/still.png", out / "img")
            self.assertEqual(img.suffix, ".png"); self.assertGreater(img.stat().st_size, 0)
        finally:
            srv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)


@unittest.skipUnless(FF, "ffmpeg")
class MixedMontage(unittest.TestCase):
    def test_folder_photos_and_fit(self):
        import montage
        tmp = Path(tempfile.mkdtemp(prefix="kosif_mix_"))
        m = tmp / "media"; m.mkdir()
        subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=1280x720:r=30:d=4", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(m / "a.mp4")], check=True)
        shutil.copy2(m / "a.mp4", m / "a.edit.mp4")
        subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=navy:s=720x1280", "-frames:v", "1", str(m / "p.png")], check=True)
        got = [p.name for p in montage.gather([m])]
        self.assertEqual(got, ["a.edit.mp4", "p.png"])                     # the edit copy replaces its original
        self.assertTrue(montage._fit_chain(m / "a.mp4", 1080, 1920)[0].startswith("split=2"))   # landscape in 9:16: whole, over a blur
        self.assertTrue(montage._fit_chain(m / "p.png", 1080, 1920)[0].startswith("scale="))     # same shape: filled
        subprocess.run([FF, "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=110:d=6", "-af", "volume=0.6", str(tmp / "m.wav")], check=True)
        r = montage.cut([m], tmp / "m.wav", tmp / "out.mp4", ratio="9:16", punch=False)
        self.assertGreaterEqual(r["shots"], 1)
        self.assertEqual(streams(tmp / "out.mp4"), ["video", "audio"])
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
