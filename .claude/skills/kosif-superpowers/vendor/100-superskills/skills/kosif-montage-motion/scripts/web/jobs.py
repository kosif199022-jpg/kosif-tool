"""Jobs: every recipe runs as `python kmotion.py CMD …` in its own process, with its log streamed to the browser and
kept on disk (workbench/jobs/ID/log.txt + meta.json), so a long render survives a page reload and nothing shares
the server's process. One queue, N workers (default 2: renders already parallelise inside)."""
from __future__ import annotations

import json
import os
import queue
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
KMOTION = SCRIPTS / "kmotion.py"


class Job:
    def __init__(self, recipe: str, cmd: str, args: list[str], root: Path, cwd: Path, note: str = ""):
        self.id = time.strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:6]
        self.recipe, self.cmd, self.args, self.note = recipe, cmd, args, note
        self.dir = root / self.id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.cwd = cwd
        self.status = "queued"
        self.created = time.time(); self.started = None; self.ended = None
        self.rc: int | None = None
        self.proc: subprocess.Popen | None = None
        self.lines: list[str] = []
        self.lock = threading.Lock()
        self.cancel = threading.Event()
        self.outputs: list[str] = []
        self.save()

    @property
    def argv(self) -> list[str]:
        return [sys.executable, str(KMOTION), self.cmd, *self.args]

    def public(self) -> dict:
        return {"id": self.id, "recipe": self.recipe, "cmd": self.cmd, "args": self.args, "note": self.note, "status": self.status, "rc": self.rc,
                "created": self.created, "started": self.started, "ended": self.ended, "lines": len(self.lines), "outputs": self.outputs,
                "command": subprocess.list2cmdline(self.argv[1:])}

    def save(self):
        (self.dir / "meta.json").write_text(json.dumps(self.public(), ensure_ascii=False, indent=1), encoding="utf-8")

    def append(self, line: str):
        with self.lock:
            self.lines.append(line)
        with (self.dir / "log.txt").open("a", encoding="utf-8") as f:
            f.write(line)

    def run(self):
        self.status, self.started = "running", time.time(); self.save()
        env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
        env.pop("CLAUDECODE", None)
        self.append(f"▶ {subprocess.list2cmdline(self.argv[1:])}\n")
        try:
            self.proc = subprocess.Popen(self.argv, cwd=str(self.cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True,
                                         encoding="utf-8", errors="replace", env=env, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except OSError as e:
            self.append(f"✖ could not start: {e}\n"); self.status, self.rc, self.ended = "failed", -1, time.time(); self.save(); return
        assert self.proc.stdout
        for line in self.proc.stdout:
            self.append(line)
        self.rc = self.proc.wait()
        self.ended = time.time()
        self.status = "cancelled" if self.cancel.is_set() else ("done" if self.rc == 0 else "failed")
        self.append(f"■ {self.status} (exit {self.rc}, {self.ended - self.started:.1f} s)\n")
        self._collect_outputs()
        self.save()

    def _collect_outputs(self):
        """Paths the log mentions that exist on disk (the tools print their outputs), newest first, ≤ 20."""
        import re
        found: list[str] = []
        text = "".join(self.lines)

        def keep(raw: str):
            p = Path(raw.replace("\\\\", "\\"))
            if not p.is_absolute():
                p = self.cwd / p                                   # the tools print paths relative to the job's cwd
            s = str(p)
            if p.is_file() and s not in found:
                found.append(s)
        for m in re.finditer(r"(?:[A-Za-z]:[\\/]|/|\b(?:out|projects|deliver|workbench)[\\/])[^\s\"'<>|]+?\.(?:mp4|mov|webm|gif|webp|png|jpg|jpeg|wav|mp3|json|srt|ass|html|md|txt)", text):
            keep(m.group(0).rstrip(".,;:)"))
        for m in re.finditer(r"\"(?:file|sheet|poster|scenes_json|timeline|saved|written)\":\s*\"([^\"]+)\"", text):
            keep(m.group(1))
        self.outputs = found[-20:]

    def kill(self):
        self.cancel.set()
        if self.proc and self.proc.poll() is None:
            self.proc.kill()


class Runner:
    def __init__(self, root: Path, cwd: Path, workers: int = 2):
        self.root = root; self.cwd = cwd
        self.jobs: dict[str, Job] = {}
        self.q: queue.Queue[Job] = queue.Queue()
        self.threads = [threading.Thread(target=self._worker, daemon=True, name=f"kosif-job-{i}") for i in range(max(1, workers))]
        for t in self.threads:
            t.start()
        self._load_history()

    def _load_history(self, limit: int = 60):
        if not self.root.exists():
            return
        for d in sorted(self.root.iterdir())[-limit:]:
            meta = d / "meta.json"
            if meta.exists() and d.name not in self.jobs:
                try:
                    m = json.loads(meta.read_text(encoding="utf-8"))
                except ValueError:
                    continue
                j = Job.__new__(Job)
                j.id, j.recipe, j.cmd, j.args, j.note = m["id"], m["recipe"], m["cmd"], m["args"], m.get("note", "")
                j.dir, j.cwd = d, self.cwd
                j.status = m["status"] if m["status"] in ("done", "failed", "cancelled") else "failed"
                j.created, j.started, j.ended, j.rc = m.get("created"), m.get("started"), m.get("ended"), m.get("rc")
                j.proc, j.lock, j.cancel, j.outputs = None, threading.Lock(), threading.Event(), m.get("outputs", [])
                log = d / "log.txt"
                j.lines = log.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True) if log.exists() else []
                self.jobs[j.id] = j

    def _worker(self):
        while True:
            job = self.q.get()
            try:
                if job.cancel.is_set():
                    job.status, job.ended = "cancelled", time.time(); job.save(); continue
                job.run()
            except Exception as e:  # noqa: BLE001
                job.append(f"✖ {e}\n"); job.status, job.ended = "failed", time.time(); job.save()
            finally:
                self.q.task_done()

    def submit(self, recipe: str, cmd: str, args: list[str], note: str = "") -> Job:
        job = Job(recipe, cmd, args, self.root, self.cwd, note)
        self.jobs[job.id] = job
        self.q.put(job)
        return job

    def get(self, job_id: str) -> Job | None:
        return self.jobs.get(job_id)

    def list(self) -> list[dict]:
        return [j.public() for j in sorted(self.jobs.values(), key=lambda j: j.created or 0, reverse=True)]

    def cancel(self, job_id: str) -> bool:
        j = self.jobs.get(job_id)
        if not j:
            return False
        j.kill()
        if j.status == "queued":
            j.status, j.ended = "cancelled", time.time(); j.save()
        return True
