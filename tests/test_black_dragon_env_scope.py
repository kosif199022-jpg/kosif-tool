import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".claude/skills/kosif-superpowers/scripts"))
import black_dragon as bd  # noqa: E402


class EnvScopeTests(unittest.TestCase):
    def test_any_keeps_everything(self):
        adapters = {"a": {"script": "x", "args": []}, "b": {"script": "y", "args": [], "env_scope": "local"}}
        kept, note = bd.scope_adapters(adapters, "any", {})
        self.assertEqual(kept, adapters)
        self.assertEqual(note["excluded"], 0)

    def test_ci_drops_local_by_entry_and_by_file_default(self):
        adapters = {"entry_local": {"script": "x", "args": [], "env_scope": "local"},
                    "file_local": {"script": "x", "args": []},
                    "entry_ci_in_local_file": {"script": "x", "args": [], "env_scope": "ci"},
                    "reviewed": {"script": "x", "args": []}}
        scopes = {"file_local": "local", "entry_ci_in_local_file": "local", "reviewed": "ci"}
        kept, note = bd.scope_adapters(adapters, "ci", scopes)
        self.assertEqual(set(kept), {"entry_ci_in_local_file", "reviewed"})
        self.assertEqual(note["excluded"], 2)

    def test_real_registry_scopes(self):
        scopes = bd.adapter_env_scopes()
        merged = bd._load_adapters(bd.REVIEWED_ADAPTERS)
        self.assertEqual(set(scopes), set(merged))
        for key in bd._load_one_adapter_file(bd.REVIEWED_ADAPTERS):
            self.assertEqual(scopes[key], "ci")


if __name__ == "__main__":
    unittest.main()
