"""Real programs for catalog power cards, one module per family (power_programs/<family_with_underscores>.py).

Each module defines PROGRAMS = {"<POWER-ID>": function}. A function takes a work folder (Path),
really performs the card's technique on a fixture it builds itself (render frames, transform audio,
compute a model, parse a document ...), writes at least one output file there, and returns a list
of checks: (name, passed: bool, observed: str). Checks must be known answers the technique must
produce (e.g. the midpoint of a dip-to-black is black; a 120 BPM click track measures 120 BPM),
never "the function returned". The dispatcher _black_dragon_power_program.py runs one card and
refuses a pass without outputs or with any failed check.
"""
from __future__ import annotations
import functools
import importlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
POWERS = HERE.parent.parent / "data" / "powers"


@functools.lru_cache(maxsize=1)
def card_index() -> dict:
    """power id -> (family, card dict)."""
    out = {}
    for f in sorted(POWERS.glob("*.json")):
        for card in json.loads(f.read_text(encoding="utf-8")):
            out[card["id"]] = (card["family"], card)
    return out


def modules_for(family: str, local: bool = True) -> list:
    """The family's module <family>.py plus any wave modules <family>__<wave>.py.

    local=False leaves out <family>__local.py: programs that need a pip model or the network
    (env_scope=local), which a clean CI image cannot run."""
    name = family.replace("-", "_")
    paths = [HERE / f"{name}.py"] + sorted(p for p in HERE.glob(f"{name}__*.py") if local or p.stem != f"{name}__local")
    return [importlib.import_module(f"power_programs.{p.stem}") for p in paths if p.is_file()]


def program_for(family: str, pid: str):
    """(module, function) holding PROGRAMS[pid] for this family, or (None, None)."""
    for mod in modules_for(family):
        fn = getattr(mod, "PROGRAMS", {}).get(pid)
        if fn is not None:
            return mod, fn
    return None, None


def all_programs() -> dict:
    """power id -> (module file, function) for every program module present."""
    out = {}
    for path in sorted(HERE.glob("*.py")):
        if path.name.startswith("_"):
            continue
        mod = importlib.import_module(f"power_programs.{path.stem}")
        for pid, fn in getattr(mod, "PROGRAMS", {}).items():
            out[pid] = (path, fn)
    return out
