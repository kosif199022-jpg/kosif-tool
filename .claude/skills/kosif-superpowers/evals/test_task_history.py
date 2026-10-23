"""Task history (scripts/task_history.py): add, list, show, replay, compare, build and the privacy gate.

    python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_task_history.py' -v
"""
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SK / "scripts"))
import task_history as T  # noqa: E402

SCRIPT = SK / "scripts" / "task_history.py"


def entry(**over):
    rec = {
        "title": "Friday dua reel",
        "request": "اعمل لي فيديو دعاء الجمعة بنفس الخط",
        "kind": "video",
        "mode": "موافق",
        "level": "L2",
        "plan": "B",
        "status": "DONE_VERIFIED",
        "tools": ["montage-pro", "ffmpeg"],
        "params": {"fps": 30, "size": "1080x1920"},
        "inputs": [{"name": "voice", "path": "in/voice.wav", "kind": "audio"}],
        "steps": [
            {"what": "build the reel", "tool": "montage-pro", "command": "python3 build.py --fps 30"},
            {"what": "publish to TikTok", "command": "tiktok upload out/reel.mp4", "needs_permission": True},
        ],
        "outputs": [{"path": "out/reel.mp4", "kind": "video", "deterministic": True}],
        "reproduce": {"how": "run the steps in order", "prerequisites": ["ffmpeg 6"]},
    }
    rec.update(over)
    return rec


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name)
        self.root = self.work / "history"
        (self.work / "in").mkdir()
        (self.work / "out").mkdir()
        (self.work / "in" / "voice.wav").write_bytes(b"voice")
        (self.work / "out" / "reel.mp4").write_bytes(b"reel-v1")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args, stdin=None):
        out, err = io.StringIO(), io.StringIO()
        old = sys.stdin
        sys.stdin = io.StringIO(stdin or "")
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = T.main(["--root", str(self.root), *args])
        finally:
            sys.stdin = old
        return code, out.getvalue(), err.getvalue()

    def add(self, rec=None, *extra):
        f = self.work / "entry.json"
        f.write_text(json.dumps(rec or entry(), ensure_ascii=False), encoding="utf-8")
        return self.run_cli("add", "--from", str(f), "--base", str(self.work), "--date", "2026-10-23", *extra)


class AddAndIndex(Base):
    def test_add_writes_one_file_hashes_local_files_and_builds_the_index(self):
        code, out, err = self.add()
        self.assertEqual(code, 0, err)
        f = self.root / "tasks" / "20261023-friday-dua-reel.json"
        rec = json.loads(f.read_text(encoding="utf-8"))
        self.assertEqual(rec["schema"], T.SCHEMA)
        self.assertEqual(rec["outputs"][0]["bytes"], 7)
        self.assertEqual(len(rec["inputs"][0]["sha256"]), 64)
        self.assertEqual([s["n"] for s in rec["steps"]], [1, 2])
        self.assertIn("20261023-friday-dua-reel", (self.root / "INDEX.md").read_text(encoding="utf-8"))
        self.assertEqual(json.loads((self.root / "index.json").read_text(encoding="utf-8"))["count"], 1)
        self.assertEqual(self.run_cli("build", "--check")[0], 0)

    def test_the_same_title_twice_gets_a_new_id_not_an_overwrite(self):
        self.add()
        self.add()
        names = sorted(p.name for p in (self.root / "tasks").glob("*.json"))
        self.assertEqual(names, ["20261023-friday-dua-reel-2.json", "20261023-friday-dua-reel.json"])

    def test_an_explicit_id_is_not_overwritten_without_replace(self):
        self.add(entry(id="20261023-reel"))
        self.assertEqual(self.add(entry(id="20261023-reel"))[0], 1)
        self.assertEqual(self.add(entry(id="20261023-reel", title="v2"), "--replace")[0], 0)

    def test_build_is_deterministic_and_check_catches_a_stale_index(self):
        self.add()
        first = (self.root / "INDEX.md").read_bytes()
        self.run_cli("build")
        self.assertEqual((self.root / "INDEX.md").read_bytes(), first)
        (self.root / "INDEX.md").write_text("old", encoding="utf-8")
        self.assertEqual(self.run_cli("build", "--check")[0], 1)
        self.assertEqual(self.run_cli("validate")[0], 0)
        self.assertEqual(self.run_cli("validate", "--strict")[0], 1)

    def test_print_writes_nothing_and_gives_a_one_line_save_and_a_link(self):
        code, out, _ = self.add(None, "--print")
        self.assertEqual(code, 0)
        self.assertFalse((self.root / "tasks").exists())
        self.assertIn("FILE: history/tasks/20261023-friday-dua-reel.json", out)
        line = next(x for x in out.splitlines() if x.startswith("echo "))
        self.assertIn("base64 -d", line)
        self.assertIn("https://github.com/kosif199022-jpg/kosif-tool/new/main/history/tasks?filename=", out)

    def test_the_one_line_save_round_trips(self):
        _, out, _ = self.add(None, "--print")
        b64 = next(x for x in out.splitlines() if x.startswith("echo ")).split()[1]
        import base64
        rec = json.loads(base64.b64decode(b64))
        self.assertEqual(self.run_cli("add", "--from", "-", "--no-hash", stdin=json.dumps(rec))[0], 0)
        self.assertTrue((self.root / "tasks" / "20261023-friday-dua-reel.json").is_file())


class Gate(Base):
    def assertRefused(self, rec, needle):
        code, _out, err = self.add(rec)
        self.assertEqual(code, 1, err)
        self.assertIn(needle, err)
        self.assertFalse((self.root / "tasks").exists())

    def test_missing_fields_and_bad_enums_are_refused(self):
        rec = entry(kind="movie")
        del rec["reproduce"]
        self.assertRefused(rec, "reproduce")
        self.assertRefused(entry(kind="movie"), "kind must be one of")

    def test_a_step_that_cannot_be_repeated_is_refused(self):
        self.assertRefused(entry(steps=[{"what": "magic"}]), "needs a command, a tool or a manual")

    def test_unfilled_template_is_refused(self):
        rec = T.template("image")
        self.assertRefused(rec, "placeholders")

    def test_credentials_are_refused(self):
        self.assertRefused(entry(params={"api_key": "sk-" + "ant-api03-" + "A" * 43}),
                           "credential")

    def test_session_paths_and_personal_data_are_refused(self):
        self.assertRefused(entry(notes="file at /tmp/" + "claude-0/x/a.mp4"), "session, scratchpad")
        self.assertRefused(entry(notes="send to someone@example.com"), "e-mail")
        self.assertRefused(entry(notes="call +20 100 123 4567"), "phone")

    def test_saudi_iban_must_not_be_published(self):
        # Synthetic account number; privacy check does not depend on checksum validity.
        self.assertRefused(entry(notes="SA" + "0" * 22), "IBAN")
        self.assertRefused(entry(params={"payment_ref": "iban sa" + "9" * 22}), "IBAN")

    def test_git_remotes_and_versions_are_not_personal_data(self):
        rec = entry(notes="git clone git@github.com:o/r.git; npm i react@18.3.1; 2026-10-23 at 1080x1920")
        self.assertEqual(self.add(rec)[0], 0)

    def test_absolute_paths_only_warn(self):
        code, _out, err = self.add(entry(notes="rendered in /home/me/project"))
        self.assertEqual(code, 0)
        self.assertIn("absolute local path", err)

    def test_validate_reports_a_renamed_file(self):
        self.add()
        f = self.root / "tasks" / "20261023-friday-dua-reel.json"
        f.rename(f.with_name("20261023-other.json"))
        code, out, _ = self.run_cli("validate")
        self.assertEqual(code, 1)
        self.assertIn("must be 20261023-friday-dua-reel.json", out)


class ListShowReplay(Base):
    def setUp(self):
        super().setUp()
        self.add()
        self.add(entry(title="Lighthouse drawing", kind="image", request="ارسم فنار", mode="A",
                       outputs=[{"path": "out/reel.mp4", "kind": "image"}], inputs=[]), "--date", "2026-10-24")

    def test_list_filters_and_numbers_newest_first(self):
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        lines = [x for x in out.splitlines() if x.strip()[:2] in ("1.", "2.")]
        self.assertIn("lighthouse", lines[0])
        self.assertIn("friday", lines[1])
        _, out, _ = self.run_cli("list", "--kind", "image", "--json")
        self.assertEqual([r["kind"] for r in json.loads(out)], ["image"])
        _, out, _ = self.run_cli("list", "--q", "دعاء", "--json")
        self.assertEqual(len(json.loads(out)), 1)

    def test_show_by_number_prefix_and_last(self):
        for ref in ("2", "20261023-friday", "friday"):
            code, out, _ = self.run_cli("show", ref)
            self.assertEqual(code, 0)
            self.assertIn("Friday dua reel", out)
        self.assertIn("Lighthouse", self.run_cli("show", "last")[1])
        with self.assertRaises(SystemExit):
            self.run_cli("show", "2026")  # ambiguous prefix

    def test_replay_sh_checks_inputs_and_holds_back_permission_steps(self):
        _, out, _ = self.run_cli("replay", "friday", "--format", "sh")
        self.assertIn("sha256sum -c -", out)
        self.assertIn("python3 build.py --fps 30", out)
        self.assertIn("# tiktok upload out/reel.mp4", out)
        self.assertNotIn("\ntiktok upload", out)
        self.assertIn("compare 20261023-friday-dua-reel", out)

    def test_replay_md_and_json_carry_the_same_request_and_params(self):
        _, md, _ = self.run_cli("replay", "friday")
        self.assertIn("needs the user's explicit permission", md)
        self.assertIn('"fps": 30', md)
        _, js, _ = self.run_cli("replay", "friday", "--format", "json")
        self.assertEqual(json.loads(js)["params"]["size"], "1080x1920")

    def test_compare_says_same_or_different(self):
        code, out, _ = self.run_cli("compare", "friday", "--dir", str(self.work))
        self.assertEqual(code, 0, out)
        self.assertIn("identical", out)
        (self.work / "out" / "reel.mp4").write_bytes(b"reel-v2")
        code, out, _ = self.run_cli("compare", "friday", "--dir", str(self.work))
        self.assertEqual(code, 1)
        self.assertIn("DIFFERENT", out)
        (self.work / "out" / "reel.mp4").unlink()
        self.assertIn("missing", self.run_cli("compare", "friday", "--dir", str(self.work))[1])


class RepoHistory(unittest.TestCase):
    def test_the_committed_history_is_valid(self):
        if not T.HISTORY.is_dir():
            self.skipTest("no history folder in this checkout")
        r = subprocess.run([sys.executable, str(SCRIPT), "validate"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_help_works(self):
        r = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("replay", r.stdout)


if __name__ == "__main__":
    unittest.main()
