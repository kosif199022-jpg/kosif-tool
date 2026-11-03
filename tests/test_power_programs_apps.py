"""Power programs of the apps group: app-feature-transfer, ui-product-device, apps-artifacts,
formats-platforms and brand-logo-identity.

Every registered program runs through the real dispatcher (`run_program`) in its own temp dir and must
pass all its known-answer checks. Planted-failure tests then break one core function per case (a
realistic bug: a dropped term, a wrong sign, a missing rule) and require the program that depends on
it to fail, which proves the checks measure the technique instead of restating constants.
"""
from __future__ import annotations

import math
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "kosif-superpowers" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import _black_dragon_power_program as dispatcher  # noqa: E402
import power_programs as pp  # noqa: E402
from power_programs import (  # noqa: E402
    app_feature_transfer as aft,
    apps_artifacts as apps,
    brand_logo_identity as brand,
    formats_platforms as fmt,
    ui_product_device as ui,
)

FAMILIES = ["app-feature-transfer", "ui-product-device", "apps-artifacts", "formats-platforms", "brand-logo-identity"]
IDS = sorted(pid for fam in FAMILIES for mod in pp.modules_for(fam) for pid in mod.PROGRAMS)


def run(pid):
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        res = dispatcher.run_program(pid, work)
        res["_has_output"] = any(p.is_file() and p.stat().st_size > 0 for p in work.rglob("*")) if work.exists() else False
        return res


def failed(res):
    return [(c["name"], c["observed"]) for c in res["checks"] if not c["passed"]]


def _contrast_gamma_encoded(a, b):
    """WCAG contrast with the classic bug: luminance from gamma-encoded sRGB, no linearisation."""
    la, lb = (0.2126 * r / 255 + 0.7152 * g / 255 + 0.0722 * bb / 255 for r, g, bb in (brand.hex2rgb(a), brand.hex2rgb(b)))
    return round((max(la, lb) + 0.05) / (min(la, lb) + 0.05), 2)


# Each case: (module, function name, factory(original) -> broken function, program that must fail).
PLANTED = {
    # brand-logo-identity
    "brand-contrast-no-linearisation": (brand, "contrast", lambda o: _contrast_gamma_encoded, "BRAND-05"),
    "brand-to_hex-no-short-expand": (brand, "to_hex", lambda o: (lambda s: s.strip().lower() if s.strip().startswith("#") else o(s)), "BRAND-08"),
    "brand-overshoot-missing-sqrt": (brand, "analytic_overshoot",
                                     lambda o: (lambda k, d, m=1.0: math.exp(-d / (2 * math.sqrt(k * m)) * math.pi)), "BRAND-26"),
    # formats-platforms
    "fmt-bar-height-not-halved": (fmt, "bar_height", lambda o: (lambda W, H, ratio=2.39: round(H - W / ratio)), "FMT-03"),
    "fmt-post-check-no-limits": (fmt, "post_check", lambda o: (lambda *a, **k: []), "FMT-34"),
    "fmt-chapters-no-spacing-rule": (fmt, "chapter_list",
                                     lambda o: (lambda m: (o(m)[0], [e for e in o(m)[1] if e != "closer than 10 s"])), "FMT-59"),
    # ui-product-device
    "ui-overshoot-zero": (ui, "overshoot", lambda o: (lambda k, c, m=1.0: 0.0), "UI-52"),
    "ui-graphemes-split-marks": (ui, "graphemes", lambda o: (lambda s: list(s)), "UI-25"),
    "ui-flip-wrong-sign": (ui, "flip", lambda o: (lambda f, l: {**o(f, l), "tx": -o(f, l)["tx"]}), "UI-41"),
    # apps-artifacts
    "apps-contrast-offset": (apps, "contrast", lambda o: (lambda a, b: o(a, b) + 1.0), "APP-19"),
    "apps-rubric-equal-weights": (apps, "rubric_score",
                                  lambda o: (lambda s: (_ for _ in ()).throw(ValueError("criteria mismatch")) if set(s) != set(apps.RUBRIC)
                                             else round(sum(s.values()) / len(s), 2)), "APP-18"),
    "apps-second-peak-one-bounce": (apps, "second_peak", lambda o: (lambda h, e: h * e ** 2), "APP-24"),
    # app-feature-transfer
    "aft-fuse-audit-blind": (aft, "fuse_audit", lambda o: (lambda blob: []), "APPX-24"),
    "aft-migrate-skips-steps": (aft, "migrate", lambda o: (lambda doc, latest=10: dict(doc, version=latest)), "APPX-52"),
    "aft-guard-no-host-check": (aft, "guard", lambda o: (lambda req, root, **k: (200, "ok")), "APPX-150"),
}


class AppsPowerPrograms(unittest.TestCase):
    def test_every_family_has_programs(self):
        counts = {fam: sum(len(m.PROGRAMS) for m in pp.modules_for(fam)) for fam in FAMILIES}
        self.assertEqual(counts, {"app-feature-transfer": 43, "ui-product-device": 82, "apps-artifacts": 10,
                                  "formats-platforms": 52, "brand-logo-identity": 35})

    def test_every_program_passes(self):
        for pid in IDS:
            with self.subTest(pid=pid):
                res = run(pid)
                self.assertTrue(res["ok"], (failed(res), res.get("error", "")[-800:]))
                self.assertTrue(res["checks"] and all(c["passed"] for c in res["checks"]))
                self.assertTrue(res["_has_output"])

    def test_planted_failures_are_caught(self):
        per_module = {}
        for case, (mod, name, factory, pid) in sorted(PLANTED.items()):
            per_module[mod.__name__] = per_module.get(mod.__name__, 0) + 1
            with self.subTest(case=case), mock.patch.object(mod, name, factory(getattr(mod, name))):
                res = run(pid)
                self.assertFalse(res["ok"], f"{case}: {pid} still passed with a broken {name}")
                self.assertTrue(failed(res) or res.get("error"), res)
        self.assertTrue(all(n >= 3 for n in per_module.values()) and len(per_module) == 5, per_module)


if __name__ == "__main__":
    unittest.main()
