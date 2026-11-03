"""Power programs of the media group: photo-video-footage, video-download, media-image-audio, atlas-media,
diagrams-explainers-code, maps-geo, 3d-spatial and characters-rigs.

Every program in the group's own modules runs through the real dispatcher (`run_program`) in its own
temp dir and must pass all its known-answer checks with a non-empty output. Planted-failure tests then
break one core function per case (a realistic bug: a dropped term, a wrong sign, a lost flag) and
require the program that depends on it to fail, which proves the checks measure the technique instead
of restating constants.
"""
from __future__ import annotations

import importlib
import math
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path
from unittest import mock

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _black_dragon_power_program as dispatcher  # noqa: E402
from power_programs import (  # noqa: E402
    atlas_media as am,
    characters_rigs as ch,
    diagrams_explainers_code as ex,
    maps_geo as mg,
    media_image_audio as mia,
    photo_video_footage as pvf,
    video_download as dl,
)

d3 = importlib.import_module("power_programs.3d_spatial")

MODULES = {"photo-video-footage": pvf, "video-download": dl, "media-image-audio": mia, "atlas-media": am,
           "diagrams-explainers-code": ex, "maps-geo": mg, "3d-spatial": d3, "characters-rigs": ch}
IDS = sorted(pid for mod in MODULES.values() for pid in mod.PROGRAMS)


def run(pid):
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        res = dispatcher.run_program(pid, work)
        res["_has_output"] = any(p.is_file() and p.stat().st_size > 0 for p in work.rglob("*")) if work.exists() else False
        return res


def failed(res):
    return [(c["name"], c["observed"]) for c in res.get("checks", []) if not c["passed"]]


def _ff_without(flag_pair):
    def factory(orig):
        def broken(*args):
            args = list(args)
            for i in range(len(args) - 1):
                if [str(args[i]), str(args[i + 1])] == flag_pair:
                    del args[i:i + 2]
                    break
            return orig(*args)
        return broken
    return factory


def _ff_replace(old, new):
    def factory(orig):
        return lambda *args: orig(*[new if str(a) == old else a for a in args])
    return factory


class _NoHost:
    def __init__(self, parsed):
        self._p = parsed

    def __getattr__(self, name):
        return None if name == "hostname" else getattr(self._p, name)


def _haversine_degrees_bug(a, b):
    """Classic bug: trigonometry on degrees, never converted to radians."""
    lon1, lat1, lon2, lat2 = (*a, *b)
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * mg.R_EARTH * math.asin(min(1.0, math.sqrt(abs(h))))


def _smin_hard(a, b, k=0.5):
    return np.minimum(a, b)


def _ik_no_bend(S, T, l1, l2, bend=1):
    S, T = np.asarray(S, float), np.asarray(T, float)
    J = S + (T - S) * l1 / (l1 + l2)  # knee on the straight line: bone lengths not kept
    return J, T


# Each case: (module, function name, factory(original) -> broken function, program that must fail).
PLANTED = {
    # photo-video-footage
    "foot-cuts-threshold-inverted": (pvf, "detect_cuts", lambda o: (lambda frames, fps, threshold=10.0, min_len=0.5:
                                                                    o(frames, fps, threshold=1e9, min_len=min_len)), "FOOT-08"),
    "foot-atempo-no-chain": (pvf, "atempo_chain", lambda o: (lambda f: f"atempo={f:g}"), "FOOT-16"),
    "foot-exposure-always-ok": (pvf, "exposure", lambda o: (lambda img: dict(o(img), verdict="ok")), "FOOT-12"),
    "foot-dom-freq-off-by-bin": (pvf, "dom_freq", lambda o: (lambda x, sr: o(x, sr) * 1.06), "FOOT-19"),
    # video-download (its programs live in photo_video_footage and use its ff/urlparse)
    "dl-no-faststart": (pvf, "ff", _ff_without(["-movflags", "+faststart"]), "DL-11"),
    "dl-wrong-pix-fmt": (pvf, "ff", _ff_replace("yuv420p", "yuv444p"), "DL-11"),
    "dl-host-not-parsed": (urllib.parse, "urlparse", lambda o: (lambda u, *a, **k: _NoHost(o(u, *a, **k))), "DL-08"),
    # media-image-audio
    "media-ean-weights-swapped": (mia, "ean_check", lambda o: (lambda d12: str((10 - sum(int(c) for c in d12) % 10) % 10)), "MEDIA-11"),
    "media-lufs-offset-dropped": (mia, "k_weight_lufs", lambda o: (lambda x, sr: o(x, sr) + 0.691 + 3.0), "MEDIA-18"),
    "media-yin-octave-error": (mia, "yin", lambda o: (lambda *a, **k: o(*a, **k) * 2), "MEDIA-16"),
    "media-deskew-sign-flipped": (mia, "deskew_angle", lambda o: (lambda *a, **k: -o(*a, **k)), "MEDIA-05"),
    # atlas-media
    "amedia-goertzel-wrong-bin": (am, "goertzel", lambda o: (lambda x, f, sr: o(x, f * 1.5, sr)), "AMEDIA-30"),
    "amedia-srgb-no-gamma": (am, "srgb_to_lin", lambda o: (lambda c: np.asarray(c, float)), "AMEDIA-26"),
    "amedia-spring-no-damping": (am, "spring_step", lambda o: (lambda zeta, omega, dt=1 / 1000, t_end=1.5: o(0.0, omega, dt, t_end)),
                                 "AMEDIA-15"),
    # diagrams-explainers-code
    "expl-crossings-ignored": (ex, "count_crossings", lambda o: (lambda pos, edges: 0), "EXPL-01"),
    "expl-truss-load-sign-flipped": (ex, "truss_solve", lambda o: (lambda nodes, members, supports, loads, E=200e9, A=1e-4:
                                                                   o(nodes, members, supports, {i: (fx, -fy) for i, (fx, fy) in loads.items()}, E, A)),
                                     "EXPL-50"),
    "expl-point-at-length-start": (ex, "point_at_length", lambda o: (lambda pts, cum, s: pts[0]), "EXPL-17"),
    # maps-geo
    "map-haversine-degrees": (mg, "haversine", lambda o: _haversine_degrees_bug, "MAP-32"),
    "map-pole-is-centroid": (mg, "pole_of_inaccessibility", lambda o: (lambda poly, grid=46: (0.0, (poly.centroid.x, poly.centroid.y))),
                             "MAP-30"),
    "map-arabic-norm-no-hamza": (mg, "norm_ar", lambda o: (lambda s: " ".join(s.lower().strip().split())), "MAP-31"),
    "map-heat-floor-not-ceil": (mg, "heat", lambda o: (lambda v, vmax: o(v - vmax / 5 + 1e-9, vmax) if v > vmax / 5 else o(v, vmax)), "MAP-46"),
    # 3d-spatial
    "3d-smin-hard-union": (d3, "smin", lambda o: _smin_hard, "3D-21"),
    "3d-aces-identity": (d3, "aces", lambda o: (lambda x: np.clip(x, 0, 1)), "3D-38"),
    "3d-fib-sphere-clustered": (d3, "fib_sphere", lambda o: (lambda n: o(n) * np.array([1, 1, 0.5]) /
                                                             np.linalg.norm(o(n) * np.array([1, 1, 0.5]), axis=1, keepdims=True)), "3D-20"),
    "3d-iso-cos60": (d3, "iso", lambda o: (lambda x, y, z, S=20, OX=200, OY=60: (OX + (x - y) * 0.5 * S, OY + (x + y) * 0.5 * S - z * S)),
                     "3D-05"),
    # characters-rigs
    "char-ik-straight-leg": (ch, "two_bone_ik", lambda o: _ik_no_bend, "CHAR-11"),
    "char-spring-overdamped": (ch, "spring", lambda o: (lambda t, f, z: o(t, f, 0.99)), "CHAR-37"),
    "char-back-out-no-overshoot": (ch, "back_out", lambda o: (lambda p, s=1.70158: 1 - (1 - p) ** 3), "CHAR-32"),
    "char-interp-linear": (ch, "interp", lambda o: (lambda frame, xs, ys, ease=None: o(frame, xs, ys, ease=lambda p: min(max(p, 0), 1))),
                           "CHAR-28"),
}


class MediaPowerPrograms(unittest.TestCase):
    def test_program_counts(self):
        counts = {fam: len(mod.PROGRAMS) for fam, mod in MODULES.items()}
        self.assertEqual(counts, {"photo-video-footage": 62, "video-download": 3, "media-image-audio": 21, "atlas-media": 23,
                                  "diagrams-explainers-code": 59, "maps-geo": 47, "3d-spatial": 35, "characters-rigs": 40})

    def test_every_program_passes(self):
        for pid in IDS:
            with self.subTest(pid=pid):
                res = run(pid)
                self.assertTrue(res["ok"], (failed(res), res.get("problems"), res.get("error", "")[-800:]))
                self.assertTrue(res["checks"] and all(c["passed"] for c in res["checks"]))
                self.assertTrue(res["_has_output"])

    def test_planted_failures_are_caught(self):
        per_family = {}
        fam_of = {pid: fam for fam, mod in MODULES.items() for pid in mod.PROGRAMS}
        for case, (mod, name, factory, pid) in sorted(PLANTED.items()):
            per_family[fam_of[pid]] = per_family.get(fam_of[pid], 0) + 1
            with self.subTest(case=case), mock.patch.object(mod, name, factory(getattr(mod, name))):
                res = run(pid)
                self.assertFalse(res["ok"], f"{case}: {pid} still passed with a broken {name}")
                self.assertTrue(failed(res) or res.get("error"), res)
        self.assertEqual(set(per_family), set(MODULES))
        self.assertTrue(all(n >= 3 for n in per_family.values()), per_family)


if __name__ == "__main__":
    unittest.main()
