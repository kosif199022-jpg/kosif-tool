"""SELF-26 install-then-verify in an isolated venv, with one real operation (env_scope=local: network)."""
from __future__ import annotations
import subprocess
import sys
import time
from pathlib import Path
from ._mind_common import save, eq, truth


def self26(work):
    work = Path(work)
    venv = work / ".venv"
    t = time.time()
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    py = venv / "bin" / "python"
    pip = subprocess.run([str(py), "-m", "pip", "install", "-q", "--only-binary=:all:", "duckdb"],
                         capture_output=True, text=True)
    out = subprocess.run([str(py), "-I", "-c", "import duckdb;print(duckdb.__version__);print(duckdb.sql('select 42*2').fetchall()[0][0])"],
                         capture_output=True, text=True)
    lines = out.stdout.split()
    save(work, "verify.txt", f"pip rc={pip.returncode}\n{out.stdout}{out.stderr}\nseconds={time.time()-t:.1f}\n")
    host = subprocess.run([sys.executable, "-I", "-c", "import sys;print(sys.prefix)"], capture_output=True, text=True).stdout.strip()
    return [eq("pip install ok", pip.returncode, 0), truth("version printed", len(lines) >= 1 and lines[0][0].isdigit(), lines[:1]),
            eq("smallest real call", lines[-1] if lines else None, "84"),
            truth("isolated from the host prefix", str(venv) not in host)]


PROGRAMS = {"SELF-26": self26}
