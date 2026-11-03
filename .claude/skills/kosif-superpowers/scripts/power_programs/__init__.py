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
import importlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
POWERS = HERE.parent.parent / "data" / "powers"


def card_index() -> dict:
    """power id -> (family, card dict)."""
    out = {}
    for f in sorted(POWERS.glob("*.json")):
        for card in json.loads(f.read_text(encoding="utf-8")):
            out[card["id"]] = (card["family"], card)
    return out


def module_for(family: str):
    name = family.replace("-", "_")
    if not (HERE / f"{name}.py").is_file():
        return None
    return importlib.import_module(f"power_programs.{name}")


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
