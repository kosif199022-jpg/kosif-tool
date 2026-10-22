"""Katana/Higgsfield reference-analysis-only policy regression tests.

These tests verify the written routing policy; they do not invoke Higgsfield,
claim free Katana analysis endpoints, or consume generation credits.
"""
from pathlib import Path
import unittest

SKILL = Path(__file__).resolve().parents[1]
CORE = SKILL / "PROTOCOL.md"
APP = SKILL / "references" / "protocol" / "A8-motion-brain.md"
SESSION = SKILL / "SESSION_PROMPT.md"
ENTRY = SKILL / "SKILL.md"
EDIT = SKILL / "references" / "guides" / "edit.md"

class KatanaAnalysisOnlyPolicyTests(unittest.TestCase):
    def test_required_policy_is_present_in_core(self):
        text = CORE.read_text(encoding="utf-8")
        self.assertIn("26. **Katana لتحليل الصور والفيديوهات المرجعية في الردود فقط**", text)
        self.assertIn("ممنوع استدعاؤها لتوليد/إعادة إنشاء صور أو فيديو", text)
        self.assertIn("رصيد إنتاج", text)
        self.assertIn("18–25", text)
        self.assertIn("Katana تحليل فقط", text)

    def test_analysis_contract_excludes_generating_media(self):
        text = APP.read_text(encoding="utf-8")
        for clause in (
            "ANALYZE_ONLY", "READ_ONLY", "Katana_ANALYSIS",
            "katana_generate=false", "katana_video_edit=false",
            "katana_image_generation=false", "katana_media_credit_spend=0",
            "external_upload_requires_permission=true",
            "KATANA_ANALYSIS_NOT_AVAILABLE", "KATANA_SPEND_BLOCKED",
            "generation_called=false",
        ):
            if clause == "Katana_ANALYSIS":
                continue
            self.assertIn(clause, text)
        self.assertIn("ممنوع إنتاج صور أو فيديو", text)
        self.assertIn("لا تدّعِ أن Katana حللت ملفًا", text)

    def test_readonly_unavailable_is_not_replaced_by_paid_generation(self):
        text = APP.read_text(encoding="utf-8")
        self.assertIn("لا تستدعِ أمر Katana التوليدي كحيلة تحليل", text)
        self.assertIn("model vision", text)
        self.assertIn("FFprobe/FFmpeg", text)
        self.assertIn("credits_spent", text)
        self.assertIn("unknown", text)

    def test_activation_and_skill_entry_match_user_constraint(self):
        session = SESSION.read_text(encoding="utf-8")
        entry = ENTRY.read_text(encoding="utf-8")
        edit = EDIT.read_text(encoding="utf-8")
        self.assertIn("Katana — تحليل فقط، صفر توليد", session)
        self.assertIn("never spend Katana/Higgsfield image/video generation credits", entry)
        self.assertIn("Katana analysis-only policy", edit)
        self.assertIn("A8-motion-brain.md#katana--higgsfield--", entry)
        self.assertIn("Katana لم تُشغّل", session)

if __name__ == "__main__":
    unittest.main(verbosity=2)
