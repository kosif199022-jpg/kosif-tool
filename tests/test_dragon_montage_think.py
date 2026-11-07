"""Dragon Montage stations 2+3 (dm_think.py, build_mind_registry.py, editor_mind.json)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".claude" / "skills" / "kosif-dragon-montage" / "scripts"
DATA = SCRIPTS.parent / "data"
sys.path.insert(0, str(SCRIPTS))

import build_mind_registry as BMR  # noqa: E402
import dm_common as C  # noqa: E402
import dm_think as T  # noqa: E402

SENTENCES = [
    "اهلا بيكم في فيديو جديد",
    "خسرت ٤٠٠٠ جنيه في عقد ناقصه سطر واحد.",
    "محدش بيقولك إن العقد الشفهي مالوش قيمة.",
    "متمضيش على أي عقد قبل ما تقرا البند ده.",
    "الكل بيمضي بسرعة. الصح إنك تسأل محامي.",
    "وده كان درس غالي جدا عليا.",
    "لو انت فريلانسر الفيديو ده ليك.",
]


def fake_analysis(speech: bool = True) -> dict:
    words, t = [], 0.4
    if speech:
        for s in SENTENCES:
            for w in s.split():
                words.append({"w": w, "start": round(t, 2), "end": round(t + 0.32, 2), "conf": 0.92})
                t += 0.38
            t += 0.9
    dur = 40.0
    shots = [{"id": f"c01-s{i + 1:03d}", "start": i * 5.0, "end": (i + 1) * 5.0,
              "quality": {"sharpness": 0.7, "exposure": 0.55, "shake": 0.1 if i != 3 else 0.7, "score": 0.6 + 0.03 * i},
              "faces": 1 if speech else 0, "motion_energy": 0.2 + 0.05 * i,
              "color": {"mean_rgb": [0.4, 0.4, 0.4], "saturation": 0.4}, "thumb": None} for i in range(8)]
    return C.new("analysis", clips=[{"id": "c01", "path": "/abs/in.mp4", "duration": dur, "width": 1080,
                                     "height": 1920, "fps": 30, "has_audio": True, "loudness_lufs": -19.0,
                                     "shots": shots, "words": words, "silences": [], "energy": []}],
                 music={"path": None, "bpm": None, "beats": [], "downbeats": []}, contact_sheet=None,
                 tools_used=["test-fixture"], missing=[])


def make_job(tmp: str, speech: bool = True) -> Path:
    j = Path(tmp) / "job"
    j.mkdir()
    C.write(j, "analysis", fake_analysis(speech))
    return j


# ------------------------------------------------------------------ registry
def _registry_dedupes_and_maps_every_entry_to_a_stage():
    reg = BMR.build()
    c = reg["counts"]
    assert c["after"] < c["before_total"] == sum(c["before"].values())
    assert set(c["before"]) == {"dragon-mind", "thinking-books", "book-methods", "mental-models"}
    keys = [e["key"] for e in reg["frameworks"]]
    assert len(keys) == len(set(keys))
    for e in reg["frameworks"]:
        assert e["stage"] in BMR.STAGES
        assert e["sources"]
        assert set(e["video"]["tags"]) <= set(BMR.TAGS)
    by = {e["key"]: e for e in reg["frameworks"]}
    pm = by["pre mortem"]
    assert {s["source"] for s in pm["sources"]} >= {"dragon-mind", "thinking-books", "mental-models"}
    assert pm["video"]["tags"]["critique"] >= 0.9


def _registry_file_is_current():
    on_disk = json.loads((DATA / "mind_registry.json").read_text(encoding="utf-8"))
    assert on_disk == json.loads(json.dumps(BMR.build(), ensure_ascii=False))


def _editor_mind_covers_contract_enums():
    em = json.loads((DATA / "editor_mind.json").read_text(encoding="utf-8"))
    assert set(em["feelings"]) == {"tense", "warm", "epic", "playful", "calm", "inspiring", "sad", "funny"}
    assert set(em["content_types"]) == {"talking-head", "travel", "product", "interview", "event", "montage"}
    assert set(em["platforms"]) == {"reel", "story", "youtube", "square", "landscape"}
    assert set(em["rhythms"]) == {"on-beat", "speech-led", "slow-burn"}
    for arc in em["arcs"].values():
        assert abs(sum(b["share"] for b in arc["beats"]) - 1.0) < 1e-6
        roles = [b["role"] for b in arc["beats"]]
        assert len(roles) == len(set(roles))
        assert set(arc["sources"]) <= set(em["sources"])


# ------------------------------------------------------------------ brief
def _brief_from_speech_analysis_is_talking_head(job):
    br = T.build_brief(job, "التنين الأسود، مونتاج ريل 30 ثانية")
    C.validate("brief", br)
    assert br["content_type"] == "talking-head"
    assert br["platform"] == "reel" and br["aspect"] == "9:16"
    assert br["target_seconds"] == 30
    assert br["language"] == "ar-eg"
    assert br["frameworks"] and all(f["output"] and f["stage"] == "frame" for f in br["frameworks"])
    assert br["hook_candidates"][0]["hook_score"] >= br["hook_candidates"][-1]["hook_score"]
    assert any("c01-s004" in a for a in br["avoid"])          # the shaky shot


def _brief_without_analysis_and_task_words():
    with tempfile.TemporaryDirectory() as d:
        br = T.build_brief(Path(d), "التنين الأسود، مونتاج لرحلتي لدهب بإحساس ملحمي، من غير موسيقى حزينة",
                           platform="story")
        C.validate("brief", br)
        assert br["content_type"] == "travel" and br["feeling"] == "epic"
        assert br["platform"] == "story" and br["target_seconds"] <= 15
        assert any("موسيقى حزينة" in a for a in br["avoid"])


# ------------------------------------------------------------------ concepts
def _run_cli(job: Path, *args) -> None:
    subprocess.run([sys.executable, str(SCRIPTS / "dm_think.py"), *args, "--job", str(job)], check=True,
                   capture_output=True, text=True, timeout=120)


def _concepts_three_distinct_with_decision_and_council(job):
    _run_cli(job, "brief", "--task", "التنين الأسود، مونتاج ريل 30 ثانية")
    _run_cli(job, "concepts")
    cc = C.read(job, "concepts")
    cs = cc["concepts"]
    assert len(cs) == 3
    assert len({tuple(c["arc"]) for c in cs}) == 3                 # three different arcs
    assert len({c["rhythm"] for c in cs}) >= 2                     # and not one shared rhythm
    ids = [c["id"] for c in cs]
    assert cc["decision"]["chosen"] in ids
    assert {m["id"] for m in cc["decision"]["matrix"]} == set(ids)
    assert "robust" in cc["decision"]["sensitivity"]
    texts = [c["hook"]["text"] for c in cs]
    assert len(set(texts)) == 3
    assert all(c["hook"]["src"] for c in cs)                      # built from real transcript sentences
    assert all(t.replace(" ", "") in "".join(SENTENCES).replace(" ", "") for t in texts)
    for c in cs:
        assert [f["stage"] for f in c["frameworks"]] == T.STAGES
        assert all(f["output"] for f in c["frameworks"])
        assert abs(c["beats"][-1]["end"] - 30) < 0.01
        assert c["hook"]["first_seconds"] <= 3
    assert len(cc["premortem"]) == 5
    assert cc["decision"]["council"]["prompt"] == "council_prompt.md"
    pack = (job / "council_prompt.md").read_text(encoding="utf-8")
    assert "المعارض" in pack and "Outsider" in pack


def _concepts_without_speech_use_formulas_not_speech_led(job):
    j = job
    C.write(j, "brief", T.build_brief(j, "التنين الأسود، مونتاج"))
    cc = T.build_concepts(j)
    C.validate("concepts", cc)
    assert all(c["rhythm"] != "speech-led" for c in cc["concepts"])
    assert all(c["hook"]["formula"].startswith("hooks_ar#") for c in cc["concepts"])
    assert len({tuple(c["arc"]) for c in cc["concepts"]}) == 3


def _concepts_are_deterministic(job):
    C.write(job, "brief", T.build_brief(job, "التنين الأسود، مونتاج ريل"))
    a = T.build_concepts(job)
    b = T.build_concepts(job)
    assert a == b


class DragonMontageThinkTests(unittest.TestCase):
    def test_registry_dedupes_and_maps_every_entry_to_a_stage(self):
        _registry_dedupes_and_maps_every_entry_to_a_stage()

    def test_registry_file_is_current(self):
        _registry_file_is_current()

    def test_editor_mind_covers_contract_enums(self):
        _editor_mind_covers_contract_enums()

    def test_brief_from_speech_analysis_is_talking_head(self):
        with tempfile.TemporaryDirectory() as d:
            _brief_from_speech_analysis_is_talking_head(make_job(d, True))

    def test_brief_without_analysis_and_task_words(self):
        _brief_without_analysis_and_task_words()

    def test_concepts_three_distinct_with_decision_and_council(self):
        with tempfile.TemporaryDirectory() as d:
            _concepts_three_distinct_with_decision_and_council(make_job(d, True))

    def test_concepts_without_speech_use_formulas_not_speech_led(self):
        with tempfile.TemporaryDirectory() as d:
            _concepts_without_speech_use_formulas_not_speech_led(make_job(d, False))

    def test_concepts_are_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            _concepts_are_deterministic(make_job(d, True))


if __name__ == "__main__":
    unittest.main()
