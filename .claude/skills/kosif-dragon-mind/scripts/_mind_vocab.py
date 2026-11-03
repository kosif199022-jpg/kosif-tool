"""Controlled vocabulary of the Dragon Mind: faculties, media kinds and the thinking cycle.

A *faculty* is one atomic thing the dragon can do (perceive media, transcribe,
animate, grade colour, verify, ...). Every catalog entry is decomposed into the
faculties its text names, so 7,000+ cards collapse into ~26 faculties that a
planner can reason about. Keywords are lower-case stems matched as substrings;
Arabic forms are given without diacritics.
"""
from __future__ import annotations

# The six-step cognitive cycle the mind runs for every task.
CYCLE = [
    {"id": "frame", "ar": "أطّر المشكلة", "en": "Frame the problem"},
    {"id": "explore", "ar": "استكشف البدائل", "en": "Explore options"},
    {"id": "decide", "ar": "قرّر", "en": "Decide"},
    {"id": "build", "ar": "ابنِ", "en": "Build"},
    {"id": "verify", "ar": "تحقّق", "en": "Verify"},
    {"id": "learn", "ar": "تعلّم وسلّم", "en": "Learn and deliver"},
]

# id, Arabic name, cycle stage, input kinds, output kinds, keywords
FACULTIES = [
    ("perceive-media", "افحص الوسائط", "frame", ["video", "audio", "image"], ["data"],
     ["ffprobe", "inspect", "probe", "detect", "scene", "measure", "analy", "loudness meter",
      "فحص", "تحليل", "كشف", "قياس"]),
    ("transcribe", "فرّغ الكلام", "frame", ["audio", "video"], ["text"],
     ["transcri", "whisper", "speech-to-text", "subtitle", "caption", "words.json",
      "تفريغ", "ترجمة", "سبتايتل"]),
    ("research", "ابحث واجمع المصادر", "frame", ["text"], ["data"],
     ["research", "search", "discover", "source", "fetch", "download", "scrape", "crawl",
      "بحث", "مصادر", "تحميل"]),
    ("reason-plan", "فكّر وخطّط", "explore", ["text", "data"], ["plan"],
     ["plan", "think", "reason", "strategy", "decid", "brief", "council", "option",
      "تخطيط", "تفكير", "خطة", "قرار", "مجلس"]),
    ("write-story", "اكتب السيناريو والنص", "explore", ["plan"], ["text"],
     ["script", "story", "copy", "hook", "narrat", "headline", "سيناريو", "قصة", "نص", "هوك"]),
    ("design-visual", "صمّم بصريًا", "build", ["plan", "text"], ["image"],
     ["design", "layout", "typograph", "palette", "poster", "font", "brand", "thumbnail",
      "تصميم", "خط", "ألوان", "بوستر", "غلاف"]),
    ("arabic-type", "اكتب بالعربي صح", "build", ["text"], ["image"],
     ["arabic", "rtl", "kashida", "harakat", "bidi", "عربي", "عربية", "تشكيل"]),
    ("generate-image", "ولّد صورًا", "build", ["text", "image"], ["image"],
     ["generate image", "text-to-image", "image generation", "diffusion", "flux", "midjourney",
      "توليد صور", "صورة"]),
    ("generate-video", "ولّد فيديو", "build", ["text", "image"], ["video"],
     ["generate video", "text-to-video", "image-to-video", "kling", "veo", "sora", "seedance",
      "توليد فيديو"]),
    ("generate-audio", "ولّد صوتًا وموسيقى", "build", ["text"], ["audio"],
     ["tts", "voice", "music", "song", "suno", "speech synth", "صوت", "موسيقى", "أغنية", "تعليق صوتي"]),
    ("animate-motion", "حرّك (موشن)", "build", ["plan", "image", "text"], ["video"],
     ["animat", "motion", "kinetic", "keyframe", "easing", "tween", "gsap", "lottie", "remotion",
      "تحريك", "موشن", "انميشن"]),
    ("three-d", "ابنِ ثلاثي الأبعاد", "build", ["plan", "image"], ["video", "3d"],
     ["blender", "3d", "mesh", "glb", "three.js", "camera orbit", "ثلاثي"]),
    ("edit-video", "اقطع ومنتج", "build", ["video", "audio"], ["video"],
     ["montage", "edit", "cut", "trim", "silence", "b-roll", "broll", "timeline", "reel", "video",
      "مونتاج", "قص", "ريلز", "فيديو"]),
    ("color-grade", "لوّن الصورة", "build", ["video", "image"], ["video", "image"],
     ["color", "colour", "grade", "lut", "tone", "bt.709", "تلوين", "لون"]),
    ("audio-mix", "امزج الصوت", "build", ["audio"], ["audio"],
     ["mix", "lufs", "duck", "beat", "bpm", "sync", "loudnorm", "مزج", "إيقاع", "مزامنة"]),
    ("render-encode", "ارندر وصدّر", "build", ["video", "plan"], ["video"],
     ["render", "encode", "ffmpeg", "export", "h.264", "x264", "mp4", "crf", "رندر", "تصدير"]),
    ("web-build", "ابنِ صفحات ومواقع", "build", ["plan", "text"], ["web"],
     ["html", "css", "website", "web page", "react", "site", "landing", "موقع", "صفحة"]),
    ("code-engineering", "برمج وهندس", "build", ["plan", "code"], ["code"],
     ["code", "refactor", "api", "python", "javascript", "library", "cli", "repository",
      "برمجة", "كود"]),
    ("data-analysis", "حلّل البيانات", "explore", ["data"], ["data"],
     ["dataset", "chart", "csv", "statistic", "metric", "dashboard", "graph", "بيانات", "إحصاء"]),
    ("verify-qa", "تحقّق واختبر", "verify", ["video", "audio", "image", "code", "web", "data"], ["receipt"],
     ["verify", "test", "check", "qa", "validat", "lint", "audit", "receipt", "proof", "gate",
      "تحقق", "اختبار", "جودة", "إيصال"]),
    ("safety-rights", "احمِ الحقوق والأمان", "verify", ["data", "text"], ["receipt"],
     ["rights", "licen", "privacy", "secret", "permission", "consent", "safety", "guard",
      "حقوق", "ترخيص", "خصوصية", "أمان"]),
    ("deliver-publish", "سلّم وانشر", "learn", ["video", "web", "code", "text"], ["delivery"],
     ["deliver", "publish", "upload", "share", "deploy", "package", "zip", "tiktok", "instagram",
      "youtube", "تسليم", "نشر", "رفع", "تيك توك", "انستجرام", "يوتيوب"]),
    ("memory-learn", "تذكّر وتعلّم", "learn", ["receipt", "data"], ["data"],
     ["memory", "recipe", "lesson", "learn", "ledger", "fusionforge", "remember", "ذاكرة", "درس", "تعلم"]),
    ("orchestrate", "نسّق الوكلاء", "decide", ["plan"], ["plan"],
     ["orchestr", "agent", "parallel", "pipeline", "workflow", "dispatch", "subagent",
      "تنسيق", "وكلاء", "توازي"]),
    ("protocol-govern", "التزم بالبروتوكول", "decide", ["plan"], ["plan"],
     ["protocol", "usip", "rule", "policy", "standard", "appendix", "بروتوكول", "قاعدة"]),
    ("visual-reference", "استلهم مرجعًا بصريًا", "explore", ["text"], ["plan"],
     ["style", "reference", "look", "aesthetic", "inspiration", "promptsmotion", "مرجع", "ستايل"]),
]

FACULTY_IDS = [f[0] for f in FACULTIES]
FACULTY = {f[0]: {"id": f[0], "ar": f[1], "stage": f[2], "inputs": f[3], "outputs": f[4],
                  "kw": f[5]} for f in FACULTIES}

# Readiness tiers: how the dragon can actually use an entry, strongest first.
TIERS = [
    ("T4-executable", "يتنفّذ بمحوّل مراجَع ويكتب إيصال SHA-256"),
    ("T3-runnable", "أداة CLI موجودة بـ argparse (تتشغّل؛ مش معناها اتنفذت على المهمة)"),
    ("T2-guided", "مهارة/بروتوكول/دليل ملفه موجود ويتقري ويتّبع"),
    ("T1-method", "كارت طريقة له وصف ومصدر موجود (معرفة، مش أداة)"),
    ("T0-broken", "مصدره مفقود أو بلا وصف — لازم يتصلّح"),
]
TIER_RANK = {t[0]: 4 - i for i, t in enumerate(TIERS)}

# Words in a task that make a step need the owner's explicit yes (no auto spend/publish).
CONSENT_WORDS = ["publish", "upload", "deploy", "pay", "buy", "credit", "spend", "tiktok", "post",
                 "انشر", "نشر", "ارفع", "رفع", "ادفع", "شراء", "رصيد", "كريدت"]

# Executors outside the catalog (MCP connectors). They always need the owner's yes
# because they spend credits or publish; the mind lists them, never calls them.
EXTERNAL = {
    "generate-video": ["mcp:Higgsfield.generate_video (credits, consent)"],
    "generate-image": ["mcp:Higgsfield.generate_image (credits, consent)"],
    "generate-audio": ["mcp:suno (credits:spend, consent)", "mcp:Higgsfield.generate_audio (credits, consent)"],
    "three-d": ["mcp:Higgsfield.generate_3d (credits, consent)"],
    "deliver-publish": ["mcp:Higgsfield.tiktok_prepare_publish (publishing, consent)"],
}

MIND_ADAPTER_KEY = "skill:kosif-dragon-mind"
MIND_ADAPTER = {
    "script": ".claude/skills/kosif-superpowers/scripts/_black_dragon_exec.py",
    "args": ["{artifact}", ".claude/skills/kosif-dragon-mind/scripts/dragon_mind.py", "think", "{task}"],
    "why": "Dragon Mind: six-step cognitive cycle, frameworks, patterns and typed faculty graph for the task (read-only)",
}

# The universal method applier: turns any catalog entry into a task-bound procedure artifact.
APPLIER_SCRIPT = ".claude/skills/kosif-dragon-mind/scripts/card_apply.py"

# Generated real-execution registries (proof runners for powers, style runners), loaded next to the
# reviewed file when present. Entries in them are real runners and never get the method applier.
GENERATED_ADAPTER_FILES = ["black_dragon_adapters_powers.json", "black_dragon_adapters_styles.json"]
