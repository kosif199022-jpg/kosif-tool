#!/usr/bin/env python3
"""KOSIF One planner: one request -> ranked routes, add-on modules and a ready Jev packet.

Usage:
    python plan.py "اعمل ريل من بنترست عن البحر بالليل"
    python plan.py --json "..."                                # machine-readable only
    python plan.py --json --main ROUTE [--extra R1,R2] "..."   # combo packets around Jev's main route
    python plan.py --combine ROUTE [ROUTE ...]                 # one merged, ordered pipeline

The keyword ranking is the offline fallback and the evidence Jev judges; Jev (kosif_jev_decide,
mode=choice) makes the final route choice. Explicit words from the user always win over both.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HOME = Path.home()
SKILLS = HOME / ".claude" / "skills"
_SIBLINGS = Path(__file__).resolve().parents[2]
SUPER = Path(os.environ.get("KOSIF_SUPERSKILLS") or (
    _SIBLINGS if (_SIBLINGS / "kosif-social" / "SKILL.md").is_file()
    else HOME / "Desktop" / "الاداة" / "100-superskills" / "skills"))

# ---------------------------------------------------------------- text normalisation
_TASHKEEL = re.compile(r"[ً-ْـ]")


def norm(text: str) -> str:
    t = _TASHKEEL.sub("", text.lower())
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي"), ("ؤ", "و"), ("ئ", "ي")):
        t = t.replace(a, b)
    return t


# ---------------------------------------------------------------- routes (Jev's closed set)
# Each route: Arabic label for the user, a one-line description for Jev, keywords, and the
# ordered steps (skill or tool per step). Keywords are written already normalised.
ROUTES: dict[str, dict] = {
    "reel_from_web": {
        "ar": "ريل من مواد الإنترنت",
        "desc": "Download clips/photos from Pinterest, TikTok, Instagram or YouTube links, then cut them into a reel.",
        "kw": ["بنترست", "pinterest", "تيك توك", "تيكتوك", "tiktok", "انستا", "instagram", "يوتيوب", "youtube",
               "رابط", "لينك", "link", "http", "نزل", "حمل", "تحميل", "download", "fetch", "من النت", "من الانترنت"],
        "steps": ["fetch", "montage", "captions?", "audio_master", "gate", "post_pack?"],
    },
    "edit_my_footage": {
        "ar": "مونتاج فيديوهاتي/صوري",
        "desc": "Edit the user's own clips or photos: beat-synced montage, JSON timeline, transitions, colour grade.",
        "kw": ["مونتاج", "montage", "قص", "قطع", "اقطع", "edit", "فيديوهاتي", "صوري", "لقطات", "clips", "footage",
               "انتقالات", "transition", "تلوين", "color grade", "ايقاع", "beat", "تايم لاين", "timeline", "دمج"],
        "steps": ["inspect", "montage_or_timeline", "grade?", "captions?", "audio_master", "gate", "post_pack?"],
    },
    "talking_reel": {
        "ar": "ريل فيديو كلام",
        "desc": "A talking-head/speech clip: cut silences, transcribe, karaoke captions, punch zooms, smart 9:16.",
        "kw": ["بيتكلم", "كلام", "متكلم", "talking", "بودكاست", "podcast", "لقاء", "مقابله", "interview", "صمت",
               "silence", "تفريغ", "transcribe", "ترجمه", "سبتايتل", "subtitle", "كاريوكي", "karaoke", "خطبه", "درس"],
        "steps": ["audiolab?", "transcribe", "reel", "captions", "audio_master", "gate", "post_pack?"],
    },
    "motion_2d": {
        "ar": "موشن جرافيك 2D",
        "desc": "2D motion graphics: kinetic Arabic text, infographic/data animation, explainer, cartoon characters, trend styles.",
        "kw": ["موشن", "motion", "موشن جرافيك", "انميشن", "انيميشن", "animation", "نص متحرك", "كلمات متحركه",
               "kinetic", "بتتحرك", "تتحرك", "متحركه", "تايبوجرافي", "typography", "انفوجراف", "infographic", "رسم بياني", "chart", "ارقام",
               "شرح", "explainer", "كرتون", "cartoon", "شخصيه", "character", "اقتباس", "quote", "لوتي", "lottie", "2d"],
        "steps": ["direct", "motion_build_2d", "review?", "render", "audio_master", "gate", "post_pack?"],
    },
    "cinematic_3d": {
        "ar": "مشهد سينمائي ثلاثي الأبعاد",
        "desc": "Realistic cinematic 3D film rendered in code (Three.js): landscapes, sea, creatures, light, camera moves.",
        "kw": ["3d", "ثلاثي", "ثري دي", "واقعي", "realistic", "سينمائي", "cinematic", "threejs", "three.js", "مشهد",
               "scene", "بحر", "غابه", "جبال", "سما", "قمر", "تنين", "dragon", "حوت", "مركب", "فلوكه"],
        "steps": ["direct", "motion_build_3d", "review?", "render", "audio_master", "gate"],
    },
    "launch_video": {
        "ar": "فيديو إطلاق/إعلان",
        "desc": "Product launch or promo/ad video for a brand, app or store, with sound effects, poster frame and review.",
        "kw": ["اطلاق", "launch", "اعلان", "اعلاني", "ad ", "promo", "برومو", "منتج", "product",
               "تطبيق جديد", "براند", "brand", "عرض", "خصم", "offer", "تسويق", "marketing"],
        "steps": ["direct", "brag", "review", "final", "gate", "post_pack?"],
    },
    "sound_to_film": {
        "ar": "فيلم من صوت/أغنية/قصيدة",
        "desc": "A film driven by audio: song lyrics, poem, Quran verse, dua or voice-over turned into synced motion (Voice2Motion).",
        "kw": ["اغنيه", "song", "قصيده", "poem", "شعر", "ايه", "ايات", "قران", "سوره", "دعاء", "dua", "تلاوه",
               "صوتي", "voice2motion", "كلمات الاغنيه", "lyrics", "نشيد", "على الصوت", "مع الصوت", "audio reactive"],
        "steps": ["audio_analyze", "transcribe", "verse_or_audio2motion", "render", "audio_master", "gate"],
    },
    "song_reel": {
        "ar": "أغنية → ريل من بنترست بكلمات متحركة",
        "desc": "A song (audio) understood line by line, the strongest excerpt chosen, Pinterest clips searched per section by the meaning of its words, cut on the beats, the lyrics animated over the footage (songreel).",
        "kw": ["مونتاج للاغنيه", "على الاغنيه", "للاغنيه", "فيديوهات على", "كليب", "فيديو كليب", "song reel", "lyric reel",
               "lyric video", "music video", "اغنيه من بنترست", "مقطع صوت لاغنيه", "كلمات الاغنيه على", "لاغنيه"],
        "steps": ["songreel_analyze", "fetch", "songreel_cut", "songreel_build", "gate", "post_pack?"],
    },
    "mimic_reel": {
        "ar": "محاكاة ريل بلقطات جديدة",
        "desc": "Imitate someone's reel shot for shot with NEW footage (usually from Pinterest): same cut times, transitions, on-screen words, lettering and sound — only the pictures change.",
        "kw": ["محاكاه", "المحاكاه", "تقليد", "التقليد", "قلد", "حاكي", "mimic", "imitate", "replicate", "بلقطات تانيه", "بلقطات جديده", "نفس الفيديو", "فيديو شبهه", "زي الفيديو", "remake", "زيه بالظبط",
               "شبهه بالظبط", "نفس الانتقالات", "نفس الكتابه", "نفس الصوت", "فيديوهات شبه", "شبيهه", "بنفس الطريقه",
               "اعمل زيه", "نسخه منه"],
        "steps": ["mimic_study", "fetch", "mimic_build", "gate", "post_pack?"],
    },
    "analyze_reference": {
        "ar": "تحليل فيديو مرجعي",
        "desc": "Break down a reference video (shots, beats, style) and turn it into per-shot generation prompts.",
        "kw": ["حلل", "تحليل", "analyze", "analyse", "breakdown", "فكك", "تفكيك", "زي الفيديو ده", "نفس الستايل",
               "مرجع", "reference", "استخرج البرومبت", "زيه", "مثله"],
        "steps": ["fetch?", "analyze", "omniprompt", "report"],
    },
    "ai_video_prompts": {
        "ar": "برومبتات فيديو وسينما",
        "desc": "Write AI video/scene prompts for Veo, Sora, Kling, Runway, Higgsfield: shot lists, 7-layer cinema prompts, lighting.",
        "kw": ["برومبت فيديو", "video prompt", "veo", "sora", "kling", "runway", "higgsfield", "هيجزفيلد", "luma",
               "hailuo", "شوت ليست", "shot list", "ستوري بورد", "storyboard", "لقطات", "سيناريو", "اضاءه", "lighting",
               "7 طبقات", "سبع طبقات"],
        "steps": ["cinema_director", "video_prompts", "lighting?", "report"],
    },
    "image_graphics": {
        "ar": "صور وتصميم جرافيك",
        "desc": "Still graphics: image prompts, thumbnails, social posts, logo/brand identity, product photos, pixel art, image critique.",
        "kw": ["صوره", "image", "برومبت صوره", "midjourney", "ميدجورني", "flux", "غلاف", "thumbnail", "ثمبنيل",
               "بوست", "post", "ستوري", "story", "لوجو", "logo", "شعار", "هويه", "identity", "موك اب", "mockup",
               "تصوير منتج", "بكسل ارت", "pixel art", "سبرايت", "sprite", "قيم الصوره", "انتقد", "critique", "بوستر", "poster"],
        "steps": ["image_route", "report"],
    },
    "pixel_redraw": {
        "ar": "رسم/تعديل صورة بيكسل ببيكسل",
        "desc": "Draw a given image or AI code pixel by pixel, redraw an uploaded image exactly, vectorise, or edit colours in it.",
        "kw": ["بيكسل ببيكسل", "pixel by pixel", "ارسم الصوره", "ارسم الكود", "اعد رسم", "redraw", "عدل الصوره",
               "غير لون", "change the colour", "change the color", "متجه", "vector", "svg", "مطابق"],
        "steps": ["pixel_studio", "report"],
    },
    "audio_only": {
        "ar": "صوت فقط",
        "desc": "Audio-only work: denoise, master to platform loudness, analyse a track, voice-over script/TTS direction, song brief.",
        "kw": ["صوت", "audio", "ضوضاء", "noise", "نضف الصوت", "ماستر", "master", "mastering", "lufs", "تعليق صوتي",
               "voice over", "voiceover", "tts", "موسيقى", "music", "بيت", "مقام", "suno", "سونو"],
        "steps": ["audio_route", "report"],
    },
    "ui_web_motion": {
        "ar": "حركة مواقع وتطبيقات",
        "desc": "Motion for websites and app UIs: microinteractions, page transitions, scroll animation, web design systems.",
        "kw": ["موقع", "website", "صفحه", "landing", "واجهه", "ui", "ux", "زرار", "button", "سكرول", "scroll",
               "framer", "gsap", "تطبيق", "app", "microinteraction", "هوفر", "hover"],
        "steps": ["ui_motion", "report"],
    },
    "social_content": {
        "ar": "سوشيال ميديا: بوستات وخطة نشر",
        "desc": "Social-media words and plans around content: per-platform captions/hashtags/YouTube titles, carousels, a content calendar, best posting time from the account's export, A/B tests. Never posts.",
        "kw": ["سوشيال", "سوشال", "social media", "هاشتاج", "هاشتاجات", "hashtag", "كاروسيل", "carousel", "سلايدات",
               "خطه محتوى", "خطه المحتوى", "content plan", "content calendar", "جدول نشر", "جدول النشر", "وقت للنشر",
               "وقت النشر", "مواعيد النشر", "best time to post", "وصف البوست", "وصف للبوست", "كابشن للبوست",
               "وصف يوتيوب", "عنوان ووصف", "a/b", "تجربه نسختين", "بوستات", "منشورات", "استراتيجيه محتوى",
               "قناه يوتيوب", "افكار محتوى", "المنافسين"],
        "steps": ["social_strategy?", "social_copy", "carousel?", "calendar?", "post_pack?", "ab_test?", "report"],
    },
    "not_media": {
        "ar": "طلب غير بصري",
        "desc": "Anything that is not video, motion, image or audio (code, accounting, research, decisions, Excel...).",
        "kw": ["كود", "code", "برمجه", "bug", "خطا", "محاسبه", "قيد", "ضريبه", "vat", "ifrs", "مراجعه", "audit",
               "اكسل", "excel", "شيت", "بحث", "research", "قرار", "استراتيجيه", "واتساب", "github", "جيت هب"],
        "steps": ["kosif_omni"],
    },
}

# ---------------------------------------------------------------- add-on modules (any route)
ADDONS: dict[str, dict] = {
    "captions": {"ar": "ترجمة/نص على الفيديو", "kw": ["ترجمه", "سبتايتل", "subtitle", "caption", "كابشن", "نص عربي", "كتابه على"]},
    "voice": {"ar": "تعليق صوتي", "kw": ["تعليق صوتي", "voice over", "voiceover", "صوت راوي", "راوي", "tts"]},
    "music": {"ar": "موسيقى", "kw": ["موسيقى", "music", "مزيكا", "اغنيه", "بيت", "soundtrack"]},
    "vertical": {"ar": "طولي 9:16", "kw": ["9:16", "طولي", "عمودي", "vertical", "ريل", "reel", "ريلز", "reels", "شورتس", "shorts", "تيك توك", "tiktok", "ستوري"]},
    "wide": {"ar": "عرضي 16:9", "kw": ["16:9", "عرضي", "يوتيوب", "youtube", "landscape"]},
    "review": {"ar": "صفحة مراجعة مشهد بمشهد", "kw": ["مراجعه", "review", "اعدل بنفسي", "motion os", "موشن او اس", "ملاحظات"]},
    "poster": {"ar": "غلاف/صورة مصغّرة", "kw": ["غلاف", "poster", "thumbnail", "ثمبنيل", "صوره مصغره", "كفر", "cover"]},
    "privacy": {"ar": "تمويه الوجوه", "kw": ["امسح الوجوه", "تمويه", "blur face", "اخفي الوجوه", "privacy"]},
    "grade": {"ar": "تلوين", "kw": ["تلوين", "color grade", "colour grade", "الوان سينمائيه", "lut", "teal"]},
    "prompts": {"ar": "برومبتات توليد", "kw": ["برومبت", "prompt", "برومت"]},
    "cloud": {"ar": "بدون الكمبيوتر (claude.ai)", "kw": ["من غير الجهاز", "بدون الكمبيوتر", "claude.ai", "على السحابه", "cloud"]},
    "social_pack": {"ar": "بوست جاهز للنشر (كابشن ووسوم لكل منصة)",
                    "kw": ["هاشتاج", "hashtag", "للنشر", "وصف البوست", "وصف للبوست", "كابشن للبوست", "عنوان ووصف",
                           "وصف يوتيوب", "انشره", "post pack"]},
}

# ---------------------------------------------------------------- where each step lives
K = "kosif-montage-motion"
STEP_SKILLS: dict[str, list[str]] = {
    "fetch": [f"{K}: kmotion fetch (yt-dlp; Pinterest via the browser pane, the user signs in themselves)"],
    "montage": [f"{K}: kmotion montage FOLDER (beats, photos+folders, credits)"],
    "montage_or_timeline": [f"{K}: kmotion montage / timeline JSON", "super:pro-video-editor-ffmpeg",
                            "super:davinci-resolve-pipeline"],
    "inspect": [f"{K}: kmotion inspect / scenes"],
    "grade": [f"{K}: grade presets", "super:video-editing-captions"],
    "captions": ["embedded-captions: cinematic captions behind the subject (35 styles)", f"{K}: karaoke captions", "super:audio-reactive-captions-studio", "super:video-editing-captions"],
    "audiolab": [f"{K}: kmotion audiolab (RNNoise)"],
    "transcribe": [f"{K}: transcribe (faster-whisper)"],
    "reel": ["talking-head-recut: talking-head recut (HyperFrames)", f"{K}: kmotion reel", "super:reels-shorts-factory", "super:podcast-production"],
    "audio_master": ["hyperframes-audio: ducking, fades, EQ/compressor/limiter on composition audio", f"{K}: -14 LUFS master", "super:audio-mastering-analysis"],
    "gate": [f"{K}: delivery gate (black/freeze/LUFS/peak)", "tool:kosif_delivery_gate"],
    "direct": ["hyperframes-creative: palettes, typography, beat planning, design spec", "faceless-explainer: narrated explainer without a presenter", "super:motion-director-pro", "hyperframes-animation-studio: references/motion-director",
               "super:storyboard-shotlist", "super:storytelling-scripts"],
    "motion_build_2d": ["motion-graphics: kinetic type, stat count-ups, lower thirds, maps (HyperFrames)", "hyperframes-animation: 24 text effects, scene blueprints", "hyperframes-registry: ~400 ready effects (grain, glitch, shimmer, charts) — search before hand-building", "hyperframes-animation-studio (flat SVG/GSAP)", "super:kinetic-typography-arabic",
                        "super:data-in-motion", "super:explainer-edu-animation", "super:character-animation-2d",
                        "super:trend-animation-styles", "super:claude-animation-studio"],
    "motion_build_3d": ["hyperframes-keyframes: 3D depth, camera moves, punch-ins", "hyperframes-animation: Three.js adapter", "hyperframes-animation-studio (three-kit 3D)", "ultra-motion-montage", "super:cinematic-3d-scene"],
    "review": ["motion-os", f"{K}: kmotion review"],
    "render": [f"{K}: film/final render (≥1080, poster frame 0)"],
    "brag": ["brag: /brag launch video from the project code (brag-slim on Opus 5.5)", "product-launch-video: URL/brief → launch promo (HyperFrames)", f"{K}: kmotion brag init|deliver + sfx", f"{K}: references/launch-video.md", "super:ad-creative-30s"],
    "final": [f"{K}: kmotion final"],
    "audio_analyze": ["tool:kosif_audio_analyze", "super:audio-mastering-analysis"],
    "verse_or_audio2motion": ["music-to-video: beat-synced lyric video / kinetic promo (HyperFrames)", f"{K}: verse / audio2motion (Voice2Motion)", "super:audio-reactive-captions-studio"],
    "analyze": [f"{K}: kmotion analyze (references/video-breakdown.md)"],
    "songreel_analyze": [f"{K}: kmotion songreel analyze SONG --lyrics → excerpt + per-section Pinterest queries by meaning (references/operating-manual.md)"],
    "songreel_cut": [f"{K}: kmotion songreel cut --media MEDIA (look at every clip first; sNN folders per section)"],
    "songreel_build": ["music-to-video: alternative lyric engine on the same beat grid", "hyperframes-registry: finishing effects (film grain, light leaks, shimmer)", f"{K}: kmotion songreel build --draft → look → --render (lyrics over footage, verse engine)"],
    "mimic_study": [f"{K}: kmotion mimic study → texts/text_style/layer/fonts (references/mimic.md)", "kosif-mimic: mm_analyze + mm_fonts.match (transition re-synthesis, text alpha/pose curves, font ranking)"],
    "mimic_build": [f"{K}: kmotion mimic match --pool → mimic build (compare.json gate)", "kosif-mimic: mm_build (per-shot LUT, measured transition progress, text replay, original audio copied)"],
    "omniprompt": [f"{K}: kmotion omniprompt / aiprompts"],
    "cinema_director": ["kosif-omni:kosif-cinema-director", "super:cinema-director-7layers"],
    "video_prompts": ["super:video-prompt-director", f"{K}: kmotion aiprompts", "super:storyboard-shotlist"],
    "lighting": ["kosif-omni:kosif-lighting", "super:photo-lighting-plan"],
    "image_route": ["super:image-prompt-forge", "super:thumbnail-social-graphics", "super:brand-identity-logo",
                    "super:product-photo-mockups", "super:pixel-art-game-assets", "super:image-critique-reverse-prompt",
                    "kosif-omni:kosif-image-studio", "super:ai-art-style-library", "super:svg-illustration-icons"],
    "pixel_studio": ["pixel-studio-painter"],
    "audio_route": [f"{K}: kmotion audiolab", "super:audio-mastering-analysis", "kosif-omni:kosif-audio",
                    "kosif-omni:kosif-voice", "super:voiceover-tts-direction", "super:music-song-brief",
                    "super:podcast-production"],
    "ui_motion": ["super:ui-motion-microinteractions", "super:website-design-system", "kosif-omni:kosif-web-design"],
    "social_strategy": ["super:youtube-channel-strategy", "super:market-competitor-research", "super:ideation-100-ideas",
                        "super:seo-content-architecture"],
    "social_copy": ["kosif-social: references/copy-guide.md", "super:arabic-copywriting", "super:storytelling-scripts",
                    "super:ecommerce-store-listings", "super:newsletter-email-marketing"],
    "carousel": ["kosif-social: social.py carousel (PNG + PDF + contact sheet)", "super:thumbnail-social-graphics"],
    "calendar": ["kosif-social: social.py calendar (+ besttime from the account's own export)", "super:reels-shorts-factory"],
    "post_pack": ["kosif-social: social.py pack → write per platform → check (never posts)"],
    "ab_test": ["kosif-social: social.py abplan / abread", "super:ab-testing-experiments"],
    "kosif_omni": ["kosif-omni:kosif-omni (front door: kosif_route → kosif_skill_auto)"],
    "report": ["Arabic report with measured numbers and output paths"],
}


def resolve(ref: str) -> dict:
    """Turn a step reference into {ref, how, path?, exists?}."""
    if ref.startswith("super:"):
        name = ref[6:]
        p = SUPER / name / "SKILL.md"
        return {"ref": name, "how": "Read playbook file", "path": str(p), "exists": p.exists()}
    if ref.startswith("tool:"):
        return {"ref": ref[5:], "how": "MCP tool"}
    if ref.startswith("kosif-omni:"):
        return {"ref": ref.split(" ")[0], "how": "Skill tool"}
    name = ref.split(":")[0].split(" ")[0]
    p = SKILLS / name / "SKILL.md"
    if not p.exists() and (SUPER / name / "SKILL.md").exists():
        p = SUPER / name / "SKILL.md"
        return {"ref": ref, "how": "Skill tool", "path": str(p), "exists": True}
    return {"ref": ref, "how": "Skill tool", "exists": p.exists()}


def _hit(text: str, k: str) -> bool:
    # short words (قص، ui، 3d…) must be whole words — «قص» must not fire inside «قصيده»;
    # Arabic clitics و/ب/ل/ف/ال in front are allowed.
    if len(k) > 3 or " " in k:
        return k in text
    return re.search(r"(?<![\w])(?:و|ب|ل|ف)?(?:ال)?" + re.escape(k) + r"(?![\w])", text) is not None


def score(text: str, kws: list[str]) -> tuple[int, list[str]]:
    hits = [k for k in kws if _hit(text, k)]
    # longer phrases are stronger evidence than single short words
    return sum(2 if " " in k or len(k) >= 7 else 1 for k in hits), hits


# Production order used when several routes are combined: gather -> design -> build -> finish -> gate.
PHASE = ["songreel_analyze", "mimic_study", "fetch", "inspect", "audio_analyze", "audiolab", "transcribe", "analyze", "social_strategy",
         "direct", "cinema_director", "lighting",
         "motion_build_3d", "motion_build_2d", "pixel_studio", "image_route", "audio_route", "ui_motion",
         "montage", "montage_or_timeline", "songreel_cut", "songreel_build", "mimic_build", "reel", "verse_or_audio2motion", "brag",
         "omniprompt", "video_prompts", "social_copy", "carousel",
         "grade", "captions", "review", "render", "final", "audio_master",
         "gate", "post_pack", "ab_test", "calendar", "kosif_omni", "report"]
MAX_ROUTES = 4  # main + up to 3 helpers; more than that is a sign the request should be split


def _rank(request: str) -> tuple[list[dict], list[dict]]:
    t = " " + norm(request) + " "
    ranked = []
    for rid, r in ROUTES.items():
        s, hits = score(t, [norm(k) for k in r["kw"]])
        ranked.append({"route": rid, "ar": r["ar"], "score": s, "hits": hits})
    ranked.sort(key=lambda x: (-x["score"], list(ROUTES).index(x["route"])))
    addons = [{"addon": a, "ar": d["ar"]} for a, d in ADDONS.items() if score(t, [norm(k) for k in d["kw"]])[0]]
    return ranked, addons


def combo_packets(request: str, main: str, extra: list[str] | None = None,
                  ranked: list[dict] | None = None) -> list[dict]:
    """Jev yes/no packets: does the request ALSO need route X next to the main one?
    Candidates = routes with keyword hits + routes Claude proposes (`extra`); never not_media."""
    if ranked is None:
        ranked, _ = _rank(request)
    cands = [r["route"] for r in ranked if r["score"] > 0 and r["route"] != main]
    for e in extra or []:
        if e in ROUTES and e != main and e not in cands:
            cands.append(e)
    cands = [c for c in cands if c != "not_media"][:MAX_ROUTES + 1]
    hits = {r["route"]: r["hits"] for r in ranked}
    return [{
        "route": c,
        "mode": "noul",
        "question": f"Besides its main route '{main}', does this request also need the '{c}' capability to be fully delivered?",
        "evidence": {"request": request, "main_route": main, "main_does": ROUTES[main]["desc"],
                     "candidate": c, "candidate_does": ROUTES[c]["desc"], "keyword_hits": hits.get(c, [])},
        "true_criteria": "The request explicitly or clearly asks for something only this candidate route produces.",
        "false_criteria": "The main route already covers it, or the link to this candidate is only a loose word match.",
        "stability": True,
    } for c in cands]


def combine(routes: list[str]) -> list[dict]:
    """Merge the steps of several routes into one ordered, de-duplicated pipeline.
    A step is optional only if it is optional in every route that has it."""
    merged: dict[str, dict] = {}
    for rid in routes:
        for s in ROUTES[rid]["steps"]:
            key, opt = s.rstrip("?"), s.endswith("?")
            if key in merged:
                merged[key]["optional"] = merged[key]["optional"] and opt
                if rid not in merged[key]["from"]:
                    merged[key]["from"].append(rid)
            else:
                merged[key] = {"step": key, "optional": opt, "from": [rid],
                               "use": [resolve(x) for x in STEP_SKILLS[key]]}
    return sorted(merged.values(), key=lambda d: PHASE.index(d["step"]))


def plan(request: str, main: str | None = None, extra: list[str] | None = None) -> dict:
    ranked, addons = _rank(request)
    top = ranked[0]
    second = ranked[1]
    confident = top["score"] >= 2 and top["score"] >= 2 * max(second["score"], 1)
    if top["score"] == 0:
        top = {"route": "not_media", "ar": ROUTES["not_media"]["ar"], "score": 0, "hits": []}
    main = main or top["route"]
    # Jev packet: closed set = the strongest candidates plus a generic escape, so Jev is never forced.
    cands = [r["route"] for r in ranked if r["score"] > 0][:6]
    for extra_c in ("motion_2d", "edit_my_footage", "not_media"):
        if len(cands) < 4 and extra_c not in cands:
            cands.append(extra_c)
    options = {c: ROUTES[c]["desc"] for c in cands}
    packet = {
        "mode": "choice",
        "question": "Which single production route best fulfils this user request as its main pipeline?",
        "evidence": {
            "request": request,
            "keyword_ranking": [{"route": r["route"], "score": r["score"], "hits": r["hits"]} for r in ranked[:5]],
            "requested_addons": [a["addon"] for a in addons],
        },
        "options": options,
        "stability": True,
    }
    return {
        "request": request,
        "fallback_route": top["route"],
        "fallback_route_ar": ROUTES[top["route"]]["ar"],
        "fallback_confident": bool(confident and top["score"] > 0),
        "main_route": main,
        "ranking": ranked[:5],
        "addons": addons,
        "steps": combine([main]),
        "jev_packet": packet,
        "combo_packets": combo_packets(request, main, extra, ranked),
    }


def steps_for(route: str) -> list[dict]:
    """Steps for a single route. Optional steps run when the request, add-ons or material need them."""
    return combine([route])


def _opt(args: list[str], flag: str) -> tuple[str | None, list[str]]:
    if flag in args:
        i = args.index(flag)
        return args[i + 1], args[:i] + args[i + 2:]
    return None, args


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    if args and args[0] in ("--route", "--combine"):
        routes = list(dict.fromkeys(args[1:]))
        bad = [r for r in routes if r not in ROUTES]
        if bad or not routes:
            print("unknown route(s): " + ", ".join(bad) + "\nknown: " + ", ".join(ROUTES), file=sys.stderr)
            return 2
        if len(routes) > MAX_ROUTES:
            print(f"warning: {len(routes)} routes — consider splitting the request", file=sys.stderr)
        print(json.dumps(combine(routes), ensure_ascii=False, indent=2))
        return 0
    main_r, args = _opt(args, "--main")
    extra, args = _opt(args, "--extra")
    if main_r is not None and main_r not in ROUTES:
        print(f"unknown route: {main_r}", file=sys.stderr)
        return 2
    if not args:
        print(__doc__)
        return 2
    out = plan(" ".join(args), main_r, extra.split(",") if extra else None)
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print(f"المسار المبدئي: {out['fallback_route_ar']} ({out['fallback_route']})"
          f"{' — واضح' if out['fallback_confident'] else ' — غير محسوم، يقرره Jev'}")
    print("الإضافات:", "، ".join(a["ar"] for a in out["addons"]) or "—")
    print("مسارات مساعدة محتملة:", "، ".join(ROUTES[c["route"]]["ar"] for c in out["combo_packets"]) or "—")
    for i, s in enumerate(out["steps"], 1):
        print(f" {i}. {s['step']}{' (اختياري)' if s['optional'] else ''}: " + " | ".join(u["ref"] for u in s["use"]))
    print("\nJEV_PACKET=" + json.dumps(out["jev_packet"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
