"""Regression: --probe-tools must never run module-level code (from PR #213).

Tests use synthetic fixtures only: no paid API, uploads or third-party media.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SUPER = ROOT / ".claude/skills/kosif-superpowers"
SCRIPTS = SUPER / "scripts"
sys.path.insert(0, str(SCRIPTS))
import black_dragon as dragon


class BlackDragonSafeProbe(unittest.TestCase):
    def test_probe_never_runs_import_time_code_even_for_argparse_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / "EXECUTED.txt"
            cli = root / "malicious.py"
            cli.write_text(
                "from pathlib import Path\n"
                + "Path(" + repr(str(marker)) + ").write_text('unsafe')\n"
                + "import argparse\n"
                + "p = argparse.ArgumentParser()\n"
                + "p.parse_args()\n", encoding="utf-8"
            )
            with patch.object(dragon, "REPO", root):
                result = dragon._probe(
                    "tool:untrusted", {"kind": "cli", "root": "repo", "path": "malicious.py"},
                    root / "job"
                )
            self.assertEqual(result["status"], "static-only", result)
            self.assertFalse(marker.exists(), "AST probe executed untrusted module-level code")
            receipt = json.loads(Path(result["output"]).read_text(encoding="utf-8"))
            self.assertFalse(receipt["executed"])



if __name__ == "__main__":
    unittest.main()
