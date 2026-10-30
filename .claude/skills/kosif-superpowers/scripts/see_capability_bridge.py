#!/usr/bin/env python3
"""KOSIF SEE -> Superpowers read-only, deterministic capability router.

Routes methods; never invokes tools, claims Full Pro execution or installs plugins.
Source: owned KOSIF SEE v1.7.6 (2026-10-30), USIP A12. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
from typing import Any

VERSION = "1.0.0"
SOURCE = "kosif-see 1.7.6 (private plugin; method-level integration)"
STAGE0 = (
    "objective_contract", "independent_perspectives", "decision_sensitivity",
    "premortem", "evidence_classification", "forecast_ranges",
    "acceptance_tests", "requirements_prd", "architecture_dependencies",
    "deterministic_numbers", "causal_falsification",
)
PACKS = (
    "kosif-research-evidence", "kosif-agent-contracts", "kosif-eval-trust",
    "kosif-engineering-reliability", "kosif-product-strategy",
    "kosif-finance-data", "kosif-prompt-architecture",
    "kosif-media-motion", "kosif-skill-orchestrator",
)
OWNERS = {
    "reasoning": "KOSIF Think",
    "full_pro": "KOSIF Think",
    "device": "KOSIF Computer",
    "browser": "KOSIF Computer",
    "whatsapp": "KOSIF WhatsApp",
    "voice": "KOSIF Voice Director",
    "browser_ambiguity": "KOSIF Jev Browser",
    "release": "KOSIF Release Bridge",
    "video_imitation": "KOSIF Montage & Motion",
}
# Order is intentional: narrow branches win over generic media/research.
ROUTES = (
    ("self_evolution", ("طور see", "تطوير see", "دمج قدرات see",
                        "طور مهارات", "تطوير المهارات", "self evolution",
                        "improve the skill", "merge see capabilities"),
     ("kosif-skill-orchestrator", "kosif-eval-trust"),
     "references/protocol/A10-self-evolution.md", None),
    ("suno_songwriting", ("suno", "كلمات أغنية", "اكتب اغنية", "اكتب أغنية",
                          "lyrics", "songwriting"),
     ("kosif-media-motion",),
     "references/protocol/A8-motion-brain.md", None),
    ("video_imitation", ("قلد مونتاج", "قلّد مونتاج", "محاكاة فيديو",
                         "نفس المونتاج", "reference video", "تقليد مونتاج",
                         "نفس الانتقالات"),
     ("kosif-media-motion",),
     "references/protocol/A8-motion-brain.md", "video_imitation"),
    ("image_prompt", ("صمم صورة", "اصنع صورة", "اعمل صورة", "ارسم صورة",
                      "image prompt", "generate image", "visual prompt"),
     (), "references/protocol/A8-motion-brain.md", None),
    ("humanize", ("صياغة بشرية", "خلي الكلام طبيعي", "humanize",
                  "أعد صياغة", "قلد صياغة", "قلّد صياغة", "rewrite"),
     ("kosif-research-evidence",),
     "references/protocol/A6-evidence-security-numbers.md", None),
    ("prompt_optimization", ("حسن البرومبت", "حسّن البرومبت",
                             "optimize prompt", "تحسين البرومبت"),
     ("kosif-prompt-architecture",),
     "references/protocol/A33-open-source-mining-prompts.md", None),
    ("whatsapp", ("واتساب", "whatsapp", "ارسال رسالة واتس", "أرسل واتس"),
     ("kosif-agent-contracts",),
     "references/protocol/A2-executors-fullpro.md", "whatsapp"),
    ("device", ("تحكم في الكمبيوتر", "تحكم في الجهاز", "remote desktop",
                "شاشة الكمبيوتر", "device control", "فتح ملف على الجهاز"),
     ("kosif-agent-contracts",),
     "references/protocol/A2-executors-fullpro.md", "device"),
    ("voice", ("توليد صوت", "تعليق صوتي", "تحويل نص لصوت",
               "voice director", "text to speech", "tts"),
     ("kosif-media-motion",),
     "references/protocol/A2-executors-fullpro.md", "voice"),
    ("release", ("انشر github", "نشر الإصدار", "release bridge",
                 "نشر cloudflare", "deploy github"),
     ("kosif-agent-contracts",),
     "references/protocol/A3-release-bridge.md", "release"),
    ("finance", ("المحاسبة", "قيد محاسبي", "دفتر الحسابات", "ميزان المراجعة",
                 "المخزون", "ضريبة", "finance", "ifrs", "reconcile",
                 "financial", "excel"),
     ("kosif-finance-data",),
     "references/protocol/A6-evidence-security-numbers.md", None),
    ("engineering", ("صلح خطأ", "أصلح كود", "debug", "fix bug", "python error",
                     "graphify", "ghidra", "reverse engineering", "rea"),
     ("kosif-engineering-reliability",),
     "references/protocol/A16-mosamem-rea-capability-fusion.md", None),
    ("media_motion", ("مونتاج", "فيديو", "موشن", "reel", "motion", "video",
                      "animation", "ffmpeg"),
     ("kosif-media-motion",),
     "references/protocol/A8-motion-brain.md", None),
    ("product", ("خطة عمل", "منتج", "استراتيجية المنتج", "business plan",
                 "product strategy", "roadmap", "prd"),
     ("kosif-product-strategy",),
     "references/protocol/A18-futurepedia-business-workflows.md", None),
    ("research", ("ابحث", "بحث معمق", "تحقق من المصادر", "مصادر",
                  "research", "fact check", "citations"),
     ("kosif-research-evidence",),
     "references/protocol/A6-evidence-security-numbers.md", None),
)
SPECIALIST_GAPS = ("fpga", "robotics", "روبوتات", "شبكات متخصصة",
                   "specialist gap", "uncovered specialist")
NUMERIC = ("ضريبة", "حساب", "مطابقة", "reconcile", "ifrs", "financial",
           "excel", "ميزان", "مخزون", "تسعير", "optimization")
FULL_PRO = ("full pro", "وضع البرو", "برو الكامل", "فعّل البرو",
            "فعل البرو", "c500", "council 500")
MODES = ("fast", "standard", "deep", "full_pro")


def _contains(text: str, phrases: tuple[str, ...]) -> bool:
    return any(term.casefold() in text for term in phrases)


def route(task: str, mode: str = "standard",
          has_reference_video: bool = False) -> dict[str, Any]:
    """Select SEE methods without pretending to execute them."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be a non-empty string")
    if mode not in MODES:
        raise ValueError("Unsupported mode")
    q = re.sub(r"\s+", " ", task.casefold()).strip()
    if _contains(q, FULL_PRO):
        mode = "full_pro"
    name, packs, reference, owner = "general", (), "references/protocol/A12-see-pro-cognitive-fusion.md", None
    for entry in ROUTES:
        if _contains(q, entry[1]):
            name, packs, reference, owner = entry[0], entry[2], entry[3], entry[4]
            if name == "video_imitation" and not has_reference_video:
                # No original video means imitation execution cannot be verified.
                name = "video_reference_missing"
                owner = "video_imitation"
            break
    if name == "general" and _contains(q, ("متصفح", "browser", "website automation")):
        name, packs, reference, owner = ("browser", ("kosif-agent-contracts",),
            "references/protocol/A2-executors-fullpro.md", "browser")
    dynamic_gap = _contains(q, SPECIALIST_GAPS) and name == "general"
    cap = 4 if mode in ("deep", "full_pro") else 2
    assert len(packs) <= cap and all(p in PACKS for p in packs)
    externally_owned = owner is not None
    fullpro_requested = mode == "full_pro"
    return {
        "schema": "kosif.see-capability-route.v1",
        "router_version": VERSION,
        "source": SOURCE,
        "task": task,
        "mode": mode,
        "branch": name,
        "stage0_lenses_available": len(STAGE0),
        "selected_method_packs": list(packs),
        "method_pack_limit": cap,
        "dynamic_specialist_lookup": {
            "eligible": dynamic_gap, "activated": False,
            "named_gap": "specialist capability not in local packs" if dynamic_gap else None,
            "max_dynamic": 2 if cap == 4 else 1,
            "requires_fresh_metadata_and_source_review": dynamic_gap,
        },
        "primary_reference": reference,
        "execution": {
            "owner": OWNERS.get(owner) if owner else None,
            "requires_live_exposure_and_authorization": externally_owned,
            "status": "NOT_EXECUTED",
            "verified": False,
        },
        "full_pro": {
            "requested": fullpro_requested,
            "state": "NOT_FULL_PRO" if fullpro_requested else "NOT_REQUESTED",
            "requires_request_bound_receipts": fullpro_requested,
        },
        "deterministic_numeric_verification": _contains(q, NUMERIC),
        "evidence": {
            "source_methods_inspected": True,
            "host_exposure_checked": False,
            "executed": False,
            "postcondition_verified": False,
        },
        "next_step": "Resolve live executor and QA receipts" if externally_owned
                     else ("Verify specialist provenance; stay on local fallback" if dynamic_gap
                           else "Load referenced method and run task-specific acceptance tests"),
    }


def self_test() -> int:
    cases = (
        ("٢ + ٢", "general", {}),
        ("ابحث في المصادر", "research", {}),
        ("صلح خطأ في بايثون", "engineering", {}),
        ("طور مهارات SEE", "self_evolution", {}),
        ("اصنع صورة", "image_prompt", {}),
        ("اكتب كلمات أغنية Suno", "suno_songwriting", {}),
        ("قلد مونتاج الفيديو", "video_imitation", {"has_reference_video": True}),
        ("قلد مونتاج الفيديو", "video_reference_missing", {}),
        ("قلّد صياغة البريد", "humanize", {}),
        ("اعمل مونتاج فيديو", "media_motion", {}),
        ("طابق دفتر الحسابات", "finance", {}),
        ("ارسل رسالة واتساب", "whatsapp", {}),
        ("تحكم في الكمبيوتر", "device", {}),
        ("استخدم Full Pro", "general", {}),
        ("احتاج مهندس FPGA", "general", {}),
    )
    for q, expected, opts in cases:
        result = route(q, **opts)
        assert result["branch"] == expected, (q, result["branch"], expected)
        assert result["execution"]["status"] == "NOT_EXECUTED"
        assert not result["execution"]["verified"]
        assert len(result["selected_method_packs"]) <= result["method_pack_limit"]
    assert route("استخدم Full Pro")["full_pro"]["state"] == "NOT_FULL_PRO"
    assert route("احتاج مهندس FPGA")["dynamic_specialist_lookup"]["eligible"]
    assert not route("اعمل صورة")["dynamic_specialist_lookup"]["activated"]
    assert len(PACKS) == 9 and len(STAGE0) == 11
    return len(cases) + 4


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", help="Task to route without executing tools")
    parser.add_argument("--mode", choices=MODES, default="standard")
    parser.add_argument("--reference-video", action="store_true")
    parser.add_argument("--catalog", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        print(json.dumps({"passed": self_test(), "router_version": VERSION}))
    elif args.catalog:
        print(json.dumps({"source": SOURCE, "stage0": STAGE0, "packs": PACKS,
            "specialized_branches": [x[0] for x in ROUTES],
            "owners": OWNERS}, ensure_ascii=False, indent=2))
    elif args.task:
        print(json.dumps(route(args.task, args.mode, args.reference_video),
                         ensure_ascii=False, indent=2))
    else:
        parser.error("Use --task, --catalog or --self-test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
