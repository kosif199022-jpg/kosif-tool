"""Memory ops (scripts/memory_ops.py): add / update / delete / no-op decisions over a local memory file."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SK / "scripts"))
import memory_ops as M  # noqa: E402

CLI = [sys.executable, str(SK / "scripts" / "memory_ops.py")]


class MemoryOpsTest(unittest.TestCase):
    def test_self_test(self):
        p = subprocess.run(CLI + ["--self-test"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_secret_is_refused_and_never_written(self):
        with tempfile.TemporaryDirectory() as d:
            store, facts, plan = Path(d, "m.json"), Path(d, "f.json"), Path(d, "p.json")
            facts.write_text(json.dumps([{"text": "token: ghp_" + "a" * 36}, {"text": "Reels are 30 seconds long"}]), encoding="utf-8")
            subprocess.run(CLI + ["propose", "--store", str(store), "--facts", str(facts), "--out", str(plan)], check=True, capture_output=True, timeout=60)
            ops = [x["op"] for x in json.loads(plan.read_text(encoding="utf-8"))["plan"]]
            self.assertEqual(ops, ["REFUSE", "ADD"])
            subprocess.run(CLI + ["apply", "--store", str(store), "--plan", str(plan), "--when", "t"], check=True, capture_output=True, timeout=60)
            text = store.read_text(encoding="utf-8")
            self.assertNotIn("ghp_", text)
            self.assertEqual(len(json.loads(text)["memories"]), 1)

    def test_update_keeps_history(self):
        s = {"memories": [], "history": []}
        s = M.apply(s, M.propose(s, [{"text": "Brand colour is teal", "subject": "brand", "attribute": "colour", "value": "teal"}]), "1")
        s = M.apply(s, M.propose(s, [{"text": "Brand colour is navy", "subject": "brand", "attribute": "colour", "value": "navy"}]), "2")
        self.assertEqual([m["value"] for m in s["memories"]], ["navy"])
        self.assertEqual(s["history"][0]["old"]["value"], "teal")

    def test_arabic_retraction(self):
        s = {"memories": [], "history": []}
        s = M.apply(s, M.propose(s, [{"text": "المستخدم يحب موسيقى هادئة في الريلز"}]), "1")
        p = M.propose(s, [{"text": "المستخدم لم يعد يحب موسيقى هادئة في الريلز"}])
        self.assertEqual(p["plan"][0]["op"], "DELETE")


if __name__ == "__main__":
    unittest.main()
