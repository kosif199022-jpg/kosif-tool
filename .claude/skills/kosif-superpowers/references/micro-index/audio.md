# الصوت والموسيقى والتعليق — Audio & voice

[← الفهرس الدقيق / micro index](README.md) · 422 powers

## الفهرس / contents

- [audio-sync-captions (motion)](#audio-sync-captions-motion)
- [music-beat-sound (motion)](#music-beat-sound-motion)
- [voice-tts (motion)](#voice-tts-motion)


## audio-sync-captions (motion)

chapter: [audio-sync-captions](../powers/audio-sync-captions.md) · card: `usip-library/cards/audio/audio-sync-captions.md` · tools: `audio-cue-mapper` · `blender-cinematic-bridge` · `caption-lines` · `character-fullbody` · `character-ik` · `cinematic-cut-planner` · `code-drawing-master` · `creative-quality-gate` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| SYNC-02 | ✅ | ملف توقيت الكلمات kosif-words/1 · words.json master timing schema | SP-0176 Word timing by length | python3 |
| SYNC-09 | ✅ | توقيت حقيقي من فونيمات Piper · True word timing from Piper phonemes | SP-0176 Word timing by length | pip:faster-whisper, pip:piper |
| SYNC-18 | ✅ | توقيت الكلمات حسب الطول · Word timing by length | SP-0176 Word timing by length | imagemagick |
| SYNC-20 | ✅ | سكريبت بتوقيت مكتوب · Timestamped script parser | SP-0176 Word timing by length | node |
| SYNC-27 | ✅ | كاريوكي ASS عربي بحدث لكل كلمة · Arabic ASS karaoke, one event per word | SP-0176 Word timing by length | ffmpeg, python3, imagemagick |
| SYNC-28 | ✅ | سبعة ستايلات ترجمة جاهزة · Seven named caption styles | SP-0176 Word timing by length | imagemagick |
| SYNC-29 | ✅ | صفحات ترجمة + SRT/VTT/ASS · Caption pages → JSON/SRT/VTT/ASS | SP-0176 Word timing by length | pip:faster-whisper |
| SYNC-32 | ✅ | دخول الكلمة على بداية نطقها · Word enters on its spoken start | SP-0176 Word timing by length | — |
| SYNC-33 | ✅ | تعبئة كاريوكي من اليمين بقناع كامل الكلمة · RTL karaoke fill with whole-word clip-path | SP-0176 Word timing by length | fonts:arabic |
| SYNC-47 | ✅ | إخراج تلقائي لمقطع متكلم · Editor-style auto direction of a talking clip | SP-0176 Word timing by length | — |
| SYNC-11 | 🟢 | تصحيح الكلمات مع حفظ التوقيت · Transcript fixes that keep timing | SP-0176 Word timing by length | — |
| SYNC-26 | 🟢 | إبراز تلقائي للكلمات المهمة · Automatic emphasis words | SP-0176 Word timing by length | — |
| SYNC-31 | 🟢 | كاريوكي \k بشرائح متساوية · Even-slice \k karaoke (omni) | SP-0176 Word timing by length | python3, fonts:arabic |
| SYNC-35 | 📦 | ترجمة Remotion بالكلمة مع كشف الاتجاه · Remotion word captions with bidi detection | SP-0176 Word timing by length | npm:remotion |
| SYNC-41 | 📦 | مكوّنات ترجمة HyperFrames · HyperFrames caption components | SP-0176 Word timing by length | npm:hyperframes |
| SYNC-44 | 📦 | ستايلات وحركات ترجمة بصمة · Basma caption presets, animations & highlight modes | SP-0176 Word timing by length | node, fonts:arabic |
| SYNC-37 | 👁 | سطر شبحي يضيء كلمة بكلمة · Ghost-to-lit line | SP-0176 Word timing by length | — |
| SYNC-38 | 👁 | صندوق ينتقل للكلمة النشطة · Word-hop highlight box | SP-0176 Word timing by length | npm:hyperframes |
| SYNC-40 | 👁 | عداد كلمة مفتاحية ودائرة على الكلمة · Keyword counter & on-word annotations | SP-0176 Word timing by length | — |
| SYNC-12 | 📄 | ضبط بداية الكلمة على النطق · Onset snapping of word stamps | SP-0176 Word timing by length | pip:faster-whisper |
| SYNC-19 | 📄 | ميزانية الكلمات حسب الزمن · Narration word budgets | SP-0176 Word timing by length | — |
| SYNC-21 | 📄 | تجميع الكلمات حسب الطاقة · Word grouping by energy | SP-0176 Word timing by length | npm:remotion |
| SYNC-22 | 📄 | موضع آمن وضمان الاختفاء · Safe placement & exit guarantee | SP-0176 Word timing by length | — |
| SYNC-23 | 📄 | ستايل الترجمة حسب نبرة الكلام · Caption style by tone | SP-0176 Word timing by length | — |
| SYNC-24 | 📄 | وضوح الترجمة العربية · Arabic caption legibility | SP-0176 Word timing by length | fonts:arabic |
| SYNC-25 | 📄 | لا تغيّر كلام المتحدث، والحرق عند الطلب · Verbatim words; burn only when asked | SP-0176 Word timing by length | — |
| SYNC-30 | 📄 | معايرة حجم ASS · ASS PlayRes calibration | SP-0176 Word timing by length | ffmpeg, fonts:arabic |
| SYNC-52 | 📄 | لكل جملة منطوقة دليل بصري · One visual proof per spoken claim | SP-0176 Word timing by length | — |
| SYNC-U01 | 📄 | وسم مصدر التوقيت: عرض أم صوت أم تقديري · Timing provenance labels (display / voice / estimated) | SP-0176 Word timing by length | pip:faster-whisper |
| SYNC-X02 | 📄 | قفل موضع مقطع الترجمة · Caption chunk position lock | SP-0176 Word timing by length | — |
| SYNC-03 | ✅ | محوّل الترجمات والتفريغ إلى words.json · Subtitle/transcript → words.json converter | SP-0177 The .en model trap | pip:faster-whisper |
| SYNC-07 | ✅ | تفريغ عربي محلي بتوقيت الكلمات · Local Arabic word-timed transcription (faster-whisper) | SP-0177 The .en model trap | pip:faster-whisper, network |
| SYNC-06 | 🟢 | التحقق من توقيت جاهز · Pre-timed transcript validation | SP-0177 The .en model trap | pip:faster-whisper |
| SYNC-17 | 🟢 | توزيع النص على مقاطع الصوت · Text over voiced spans (estimated) | SP-0177 The .en model trap | — |
| SYNC-15 | 📦 | تفريغ HyperFrames · HyperFrames transcribe CLI | SP-0177 The .en model trap | pip:faster-whisper, npm:hyperframes, key:openai |
| SYNC-14 | 🔑 | تفريغ سحابي مع فصل المتحدثين · Cloud STT with diarisation | SP-0177 The .en model trap | pip:faster-whisper, key:elevenlabs, key:unspecified, pip:pyannote |
| SYNC-39 | 👁 | ترجمة تُكتب لحظة النطق · Voice-timed typewriter captions | SP-0177 The .en model trap | — |
| SYNC-08 | 📄 | فخ نماذج .en · The .en model trap | SP-0177 The .en model trap | pip:faster-whisper, npm:hyperframes |
| SYNC-13 | 📄 | تجهيز الصوت للتفريغ وفخ التوقيت · STT audio prep & its timing trap | SP-0177 The .en model trap | ffmpeg |
| SYNC-10 | ✅ | محاذاة النص الصحيح على التفريغ · True-text alignment onto ASR | SP-0178 Verse film from sound | — |
| SYNC-45 | ✅ | فيلم كلمات من صوت (أغنية، شعر، دعاء) · Verse film from sound | SP-0178 Verse film from sound | pip:faster-whisper, network |
| SYNC-36 | 🟢 | كلمات على مقاطعها مع كلمات ذهبية · Syllable-timed speech captions with gold keywords | SP-0178 Verse film from sound | — |
| SYNC-48 | 🟢 | الريل التلقائي من الكلام · Automatic talking-clip reel | SP-0178 Verse film from sound | pip:faster-whisper |
| SYNC-51 | 📦 | ريل كلمات أغنية · Songreel lyric reel | SP-0178 Verse film from sound | yt-dlp, pip:faster-whisper, network |
| SYNC-55 | 👁 | ذروة المؤثر على الحدث · SFX peak-offset alignment | SP-0178 Verse film from sound | pip:numpy |
| SYNC-49 | 📄 | إيقاع التلاوة والدعاء · Recitation & dua pacing | SP-0178 Verse film from sound | — |
| SYNC-50 | 📄 | توقيت سطر الأغنية · Lyric line timing | SP-0178 Verse film from sound | — |
| SYNC-X01 | 📄 | تحليل أغنية لفيلم كلمات · Song analysis for a lyric film (bands, kicks, word times) | SP-0178 Verse film from sound | — |
| SYNC-01 | ✅ | الصوت هو الساعة الرئيسية · Audio is the master clock | SP-0179 Concat + untouched original audio mux | ffmpeg, chromium, npm:remotion |
| SYNC-04 | ✅ | حدود تسامح التزامن · Sync tolerances | SP-0179 Concat + untouched original audio mux | — |
| SYNC-05 | ✅ | قياس التزامن إطارًا بإطار · Frame-by-frame sync probe | SP-0179 Concat + untouched original audio mux | node |
| SYNC-46 | ✅ | Voice2Motion: موشن بالمعنى من الصوت · Voice2Motion semantic scenes | SP-0179 Concat + untouched original audio mux | python3 |
| SYNC-56 | 🟢 | دمج المشاهد مع الصوت الأصلي بلا تعديل · Concat + untouched original audio mux | SP-0179 Concat + untouched original audio mux | ffmpeg, python3 |
| SYNC-57 | 🟢 | غلاف الجهارة وقنوات الصوت للحركة · Loudness envelope & sound channels for motion | SP-0179 Concat + untouched original audio mux | python3 |
| SYNC-54 | 📄 | إصلاح انزياح الصوت المدموج · Joined-audio drift fix | SP-0179 Concat + untouched original audio mux | ffmpeg |
| SYNC-58 | 📄 | مزامنة الفم بستة أشكال · Six-shape lip sync | SP-0179 Concat + untouched original audio mux | pip:piper |
| SYNC-34 | ✅ | كاريوكي الكبسولة في starter الكانفس · Canvas karaoke pill (html-canvas starter) | SP-0180 Lower thirds | node, chromium |
| SYNC-42 | 📦 | ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث · Embedded captions: rail + peak word behind the subject | SP-0180 Lower thirds | npm:hyperframes |
| SYNC-43 | 📦 | الأشرطة السفلية · Lower thirds | SP-0180 Lower thirds | npm:hyperframes |
| SYNC-53 | ✅ | كشف الصمت الثابت والتكيفي · Fixed & adaptive silence detection | SP-0441 Genre-aware silence trimming | ffmpeg, python3 |
| SYNC-16 | 📄 | كشف الإعادات وتجميع المونتاج من النص · Retake detection & transcript-driven assembly | SP-0441 Genre-aware silence trimming | — |

## music-beat-sound (motion)

chapter: [music-beat-sound](../powers/music-beat-sound.md) · card: `usip-library/cards/audio/music-beat-sound.md` · tools: `audio-cue-mapper` · `music-rhythm-engine`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| BEAT-146 | 📦 | تنفس الهالة على ضربات الإيقاع · Downbeat-synced halo breathing | SP-0307 Painted moon with halo | — |
| BEAT-154 | 📦 | هالة وجسيمات تتفاعل مع الصوت · Sound-reactive halo, motes and kick rings | SP-0307 Painted moon with halo | — |
| BEAT-07 | ✅ | سياسات الصمت وعدم الموسيقى · Silent / no-music sound policies | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-10 | ✅ | خفض الموسيقى تحت الصوت · Music ducking under voice (sidechain) | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-13 | ✅ | مسار الموسيقى · Soundtrack track | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-17 | ✅ | كاشف الموسيقى الخلفية · Music-bed detector | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-21 | ✅ | مؤلف موسيقى على شبكة الإيقاع · Beat-grid score synthesiser | SP-0318 Music ducking under voice (sidechain) | python3 |
| BEAT-24 | ✅ | مواصفات موسيقى المشاريع · Project score specs (templates) | SP-0318 Music ducking under voice (sidechain) | python3 |
| BEAT-26 | ✅ | سياسات الصوت والموسيقى · Music/SFX policy presets | SP-0318 Music ducking under voice (sidechain) | python3 |
| BEAT-35 | 🟢 | تنفس الإيقاع مع الطبلة · Kick-pump duck | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-40 | 🟢 | حلقة موسيقية سلسة على حدود الموازير · Bar-aligned seamless music loop | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-47 | 🟢 | موسيقى مولدة على الإيقاع · score synthesised music on beat grid | SP-0318 Music ducking under voice (sidechain) | python3 |
| BEAT-55 | 🟢 | مواصفة موسيقى إجرائية على شبكة الإيقاع · Procedural score spec (beat-grid music) | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-71 | 🟢 | المراجعة: تبديل الموسيقى ومستوى الصوت · Review: music swap and music/effects volume | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-75 | 🟢 | موسيقى مولدة على الإيقاع · Synthesised score on the beat grid | SP-0318 Music ducking under voice (sidechain) | pip:numpy |
| BEAT-78 | 🟢 | خفض الموسيقى تحت الصوت · Voice-over sidechain ducking | SP-0318 Music ducking under voice (sidechain) | ffmpeg, imagemagick |
| BEAT-79 | 🟢 | موسيقى تحت الكلام · Music bed under speech (static) | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-83 | 🟢 | خلط صوت التركيب مع خفض الموسيقى تحت الصوت · Composition audio mux with voice ducking | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-84 | 🟢 | إعدادات خفض الموسيقى تحت الكلام · Sidechain ducking presets | SP-0318 Music ducking under voice (sidechain) | ffmpeg, imagemagick |
| BEAT-85 | 🟢 | ترتيبات جاهزة · Default arrangements launch / calm | SP-0318 Music ducking under voice (sidechain) | python3 |
| BEAT-86 | 🟢 | موسيقى خلفية أصلية تلقائية · Auto underscore when no bed | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-114 | 📦 | التلاشي وخفض الموسيقى عبر مسار الأتمتة · Volume fades and ducking via automation lane | SP-0318 Music ducking under voice (sidechain) | npm:gsap |
| BEAT-119 | 📦 | نحت الموسيقى تحت التعليق الصوتي · Voiceover carve (spectral sidechain ducking) | SP-0318 Music ducking under voice (sidechain) | npm:hyperframes |
| BEAT-121 | 📦 | منحنيات الأتمتة للصوت والمؤثرات · Automation envelopes on volume or any effect param | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-126 | 📦 | خفض تلقائي من بيانات الصوت · Auto-duck lane from audio_meta | SP-0318 Music ducking under voice (sidechain) | node |
| BEAT-131 | 📦 | مساعدات مدة الإطار ومستوى الموسيقى · Pad frame duration and BGM volume helpers | SP-0318 Music ducking under voice (sidechain) | node |
| BEAT-137 | 📦 | خفض الموسيقى تحت الصوت · Sidechain auto-ducking | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-140 | 📦 | موسيقى أصلية · Original music score | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-143 | 📦 | خفض الموسيقى تحت الصوت · Music ducking under voice (spec vs code) | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-148 | 📦 | مواصفة موسيقى خلفية للكلام · Talking-voice score spec (90 BPM D minor) | SP-0318 Music ducking under voice (sidechain) | pip:numpy |
| BEAT-157 | 📦 | موسيقى · Category: Music | SP-0318 Music ducking under voice (sidechain) | python3, npm:remotion |
| BEAT-158 | 📦 | خفض الموسيقى والجهارة · Music ducking and loudness | SP-0318 Music ducking under voice (sidechain) | ffmpeg, python3 |
| BEAT-88 | 📦 | موسيقى إجرائية بملف JSON · Procedural music score in JSON | SP-0318 Music ducking under voice (sidechain) | ffmpeg, pip:numpy |
| BEAT-94 | 📦 | توطية الموسيقى وقت الكلام · Music ducking under speech | SP-0318 Music ducking under voice (sidechain) | imagemagick |
| BEAT-97 | 📦 | مؤلف موسيقى خلفية محلي · Procedural music bed composer | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-218 | 📄 | توجيه الموسيقى مقطعًا بمقطع · Section-by-section music direction | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-229 | 📄 | إيقاف الموسيقى وعودتها · Music stop/re-entry grammar | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-230 | 📄 | خفض الموسيقى تحت الكلام · Speech-first ducking | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-231 | 📄 | تجهيز الموسيقى قبل الميكس · Hero music premaster | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-235 | 📄 | ألحان أصلية فقط · Original melodies only | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-243 | 📄 | تعديل طول الموسيقى على الجمل · Edit music to length on phrases | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-244 | 📄 | خفض الموسيقى تحت الصوت · Ducking music under voice | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-246 | 📄 | سلسلة ماسترينج · Music mastering chain | SP-0318 Music ducking under voice (sidechain) | ffmpeg, pip:numpy |
| BEAT-254 | 📄 | موسيقى أصلية على شبكة الإيقاع · Original beat-grid score (WAV) | SP-0318 Music ducking under voice (sidechain) | python3 |
| BEAT-262 | 📄 | ducking حقيقي · Sidechain ducking | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-268 | 📄 | خفض الموسيقى تحت الصوت · Music ducking under voice | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| BEAT-278 | 📄 | ترخيص الموسيقى · Music licensing rule | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-282 | 📄 | إشارات الموسيقى الجاهزة · Music cue presets | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-X04 | 📄 | قص مقطع الموسيقى بلا نقرة · Click-free music cut with a shaped fade-out | SP-0318 Music ducking under voice (sidechain) | ffmpeg, python3, os:macos |
| BEAT-289 | 💡 | موسيقى مع خفض · Arc-scored music with typing duck | SP-0318 Music ducking under voice (sidechain) | — |
| BEAT-02 | ✅ | مؤثرات صوتية مصممة على الإشارات · Designed SFX on picture cues | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-04 | ✅ | مؤثرات وحوار الرجل العصوي · Stickman foley + dialogue pacing | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-05 | ✅ | تصميم مؤثرات ميكانيكية · Mechanical foley design (car) | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-06 | ✅ | مؤثرات الطعام الملموسة · Tactile food foley + tasting sounds | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-12 | ✅ | مكتبة مؤثرات CC0 داخل التايملاين · CC0 SFX kit in timelines | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-50 | 🟢 | مكتبة المؤثرات · SFX kit 20 CC0 cues | SP-0319 SFX kit 20 CC0 cues | python3 |
| BEAT-54 | 🟢 | مكتبة مؤثرات صوتية · CC0 UI sound-effects kit (20 sounds) | SP-0319 SFX kit 20 CC0 cues | python3 |
| BEAT-56 | 🟢 | ورقة مؤثرات صوتية متزامنة مع الصورة · SFX cue sheet synced to picture | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-115 | 📦 | مزامنة مؤثر صوتي مع حدث مرئي · Align a sound to an on-screen event | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-127 | 📦 | مكتبة المؤثرات الصوتية المرفقة · Bundled SFX library (19 files) | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-149 | 📦 | قائمة مؤثرات صوتية مصممة · Designed SFX cue sheet | SP-0319 SFX kit 20 CC0 cues | python3 |
| BEAT-95 | 📦 | مكتبة المؤثرات الصوتية المولدة · Synthesised SFX library (16) | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-98 | 📦 | توزيع المؤثرات على كلمات الفيلم · Film SFX auto-placement | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-99 | 📦 | مؤثرات المونتاج على القطعات · Montage SFX rules | SP-0319 SFX kit 20 CC0 cues | imagemagick |
| BEAT-161 | 🔑 | توليد مؤثرات صوتية من وصف نصي · Text-to-sound-effects generation | SP-0319 SFX kit 20 CC0 cues | key:elevenlabs |
| BEAT-162 | 🔑 | مكتبة مؤثرات صوتية · SFX library by URL | SP-0319 SFX kit 20 CC0 cues | npm:remotion, key:unspecified |
| BEAT-163 | 🔑 | توليد مؤثرات صوتية من نص · Text-to-SFX generation | SP-0319 SFX kit 20 CC0 cues | pip:numpy, key:elevenlabs |
| BEAT-216 | 📄 | أطوال أصوات واجهة الاستخدام · UI sound feedback lengths | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-228 | 📄 | أدوار طبقات الصوت · Sound layer roles | SP-0319 SFX kit 20 CC0 cues | ffmpeg |
| BEAT-232 | 📄 | صوت كتابة تحت ظهور النص · Typing SFX under caption reveal | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-236 | 📄 | تشريح المؤثر بثلاث طبقات · SFX three-layer anatomy | SP-0319 SFX kit 20 CC0 cues | pip:numpy |
| BEAT-241 | 📄 | ورقة توزيع أدوار الصوت · Sound-role cue sheet | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-270 | 📄 | أصوات مفاتيح خافتة · Soft key-click SFX | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-271 | 📄 | مستوى صوت الرسم · Drawing SFX level | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-279 | 📄 | مستويات مؤثرات النقر والسحب · Tap/swipe SFX levels | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-281 | 📄 | مكتبة مؤثرات Kenney · Kenney CC0 SFX library | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-U01 | 📄 | لوحة مؤثرات بلا whoosh وفراش صوت اللقطات · Subtle SFX palette without whooshes | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-284 | 💡 | مؤثرات صوتية مولدة · Synthesized Web Audio SFX on frame clock | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-285 | 💡 | مؤثر واحد لكل عنصر · One soft SFX per element | SP-0319 SFX kit 20 CC0 cues | — |
| BEAT-29 | 🟢 | استخراج طاقة الترددات لكل إطار · Per-frame FFT band extraction | SP-0320 Audio channels as animation drivers | ffmpeg, pip:numpy |
| BEAT-30 | 🟢 | عناصر تتفاعل مع الصوت · Audio-reactive UI accents | SP-0320 Audio channels as animation drivers | ffmpeg, pip:numpy, npm:gsap |
| BEAT-36 | 🟢 | توهج متفاعل مع الصوت · Audio-reactive glow and scale | SP-0320 Audio channels as animation drivers | — |
| BEAT-43 | 🟢 | صفارة تأكيد Web Audio · Web Audio confirmation beep | SP-0320 Audio channels as animation drivers | — |
| BEAT-53 | 🟢 | قنوات الصوت كمحرك للحركة · Audio channels as animation drivers | SP-0320 Audio channels as animation drivers | python3 |
| BEAT-57 | 🟢 | قنوات تحليل الصوت لكل إطار · Per-frame audio analysis channels | SP-0320 Audio channels as animation drivers | — |
| BEAT-80 | 🟢 | استخراج بيانات الصوت لكل إطار · Per-frame audio feature extraction | SP-0320 Audio channels as animation drivers | ffmpeg, python3 |
| BEAT-81 | 🟢 | قالب مرئي صوتي · Two-canvas audio visualiser template | SP-0320 Audio channels as animation drivers | fonts:arabic |
| BEAT-82 | 🟢 | قنوات الصوت كمحرّك · Sound channels as animation drivers | SP-0320 Audio channels as animation drivers | python3 |
| BEAT-104 | 📦 | فيديو لملف صوت فقط · Audio-only clip visuals | SP-0320 Audio channels as animation drivers | npm:react |
| BEAT-108 | 📦 | أتمتة الصوت · Audio automation lanes | SP-0320 Audio channels as animation drivers | — |
| BEAT-116 | 📦 | مرئيات تتفاعل مع الصوت · Audio-reactive visuals from precomputed bands | SP-0320 Audio channels as animation drivers | python3, npm:gsap |
| BEAT-124 | 📦 | مفردات نطاقات التردد · Frequency band vocabulary | SP-0320 Audio channels as animation drivers | — |
| BEAT-147 | 📦 | قنوات الصوت لكل إطار · Audio channels JSON (per-frame features) | SP-0320 Audio channels as animation drivers | python3 |
| BEAT-180 | 🔑 | حزمة الأطلس للصوت والقصة · Atlas skill pack: audio/voice/story skills | SP-0320 Audio channels as animation drivers | npm:hyperframes, key:elevenlabs |
| BEAT-193 | 👁 | كل ارتداد يعزف النغمة التالية · Bounce-to-note sonification | SP-0320 Audio channels as animation drivers | — |
| BEAT-213 | 📄 | ربط الترددات بخصائص بصرية · Audio-to-visual property mapping | SP-0320 Audio channels as animation drivers | — |
| BEAT-214 | 📄 | ترجمة تتفاعل مع الصوت · Audio-reactive captions at build time | SP-0320 Audio channels as animation drivers | — |
| BEAT-222 | 📄 | MG-028 توقيع صوتي موجز · MG-028 Sonic-logo pulses | SP-0320 Audio channels as animation drivers | ffmpeg |
| BEAT-264 | 📄 | ربط الحركة بالصوت · Audio-reactive mapping rules | SP-0320 Audio channels as animation drivers | — |
| BEAT-267 | 📄 | قواعد صوت الإعلان · Ad audio rules | SP-0320 Audio channels as animation drivers | — |
| BEAT-31 | 🟢 | قائمة قطع تلقائية من المازورات وذروات الحركة · Auto edit list from bars and motion peaks | SP-0321 BPM beat cuts | ffmpeg, pip:numpy |
| BEAT-46 | 🟢 | مونتاج على الإيقاع · Beat-planned montage | SP-0321 BPM beat cuts | python3, imagemagick |
| BEAT-66 | 🟢 | مونتاج على الإيقاع · Beat-cut montage | SP-0321 BPM beat cuts | python3, imagemagick |
| BEAT-109 | 📦 | مونتاج على الإيقاع · Music-to-video beat grid | SP-0321 BPM beat cuts | npm:hyperframes |
| BEAT-112 | 📦 | تجميد على الإيقاع · Beat Freeze Cut | SP-0321 BPM beat cuts | npm:gsap, npm:hyperframes |
| BEAT-130 | 📦 | حركات إيقاعية موثقة فقط · Beat motion primitives without demo folders | SP-0321 BPM beat cuts | — |
| BEAT-151 | 📦 | نقاط قطع على الإيقاع · Beat/onset cut points | SP-0321 BPM beat cuts | ffmpeg, pip:numpy |
| BEAT-181 | 👁 | قطع متزامن مع الإيقاع · Beat-locked cuts | SP-0321 BPM beat cuts | — |
| BEAT-183 | 👁 | مونتاج كلمات خاطفة على الإيقاع · Flash-word beat montage | SP-0321 BPM beat cuts | imagemagick |
| BEAT-184 | 👁 | انفجار ذروة متزامن مع الموسيقى · Explosion climax on beat | SP-0321 BPM beat cuts | — |
| BEAT-191 | 👁 | مونتاج إيقاعي · Beat montage | SP-0321 BPM beat cuts | imagemagick |
| BEAT-196 | 👁 | قطعات حادة مضبوطة على الإيقاع · Beat-locked hard cuts | SP-0321 BPM beat cuts | — |
| BEAT-204 | 👁 | قطع على الإيقاع · BPM beat cuts | SP-0321 BPM beat cuts | — |
| BEAT-207 | 👁 | كلمات تتبدل على الإيقاع · BPM beat-cut word flashes | SP-0321 BPM beat cuts | — |
| BEAT-223 | 📄 | MG-091/099 نص على الضربات وتقطيع على الجملة الموسيقية · MG-091/099 Beat-locked words and phrase cuts | SP-0321 BPM beat cuts | ffmpeg, imagemagick, pip:librosa |
| BEAT-250 | 📄 | معادلة زمن النبضة · Beat interval formula | SP-0321 BPM beat cuts | — |
| BEAT-253 | 📄 | مونتاج لقطات على إيقاع الموسيقى · Beat-cut montage to music | SP-0321 BPM beat cuts | python3, imagemagick |
| BEAT-266 | 📄 | قطع على الإيقاع · Beat/sentence cut points from BPM | SP-0321 BPM beat cuts | — |
| BEAT-274 | 📄 | حساب طول الضربة · Beat period math | SP-0321 BPM beat cuts | — |
| BEAT-16 | ✅ | شبكة الإيقاع · Beat grid clock (beats) | SP-0322 Beat grid clock (beats) | python3 |
| BEAT-52 | 🟢 | شبكة الإيقاع · Beat grid (beats) | SP-0322 Beat grid clock (beats) | python3 |
| BEAT-70 | 🟢 | المراجعة: شبكة الإيقاع مع علامة الذروة · Review: beat grid with drop marker | SP-0322 Beat grid clock (beats) | — |
| BEAT-74 | 🟢 | ساعة الإيقاع للصورة · Beat clock for picture (MOTION.beats) | SP-0322 Beat grid clock (beats) | python3 |
| BEAT-129 | 📦 | محلل شبكة الإيقاع · Beat-grid analyzer (audiomap.json) | SP-0322 Beat grid clock (beats) | pip:numpy, pip:librosa, pip:soundfile |
| BEAT-134 | 📦 | ساعة شبكة إيقاع لفيلم كامل · Beat-grid clock for a whole film | SP-0322 Beat grid clock (beats) | — |
| BEAT-138 | 📦 | ساعة الإيقاع · Beat clock MOTION.beats | SP-0322 Beat grid clock (beats) | python3 |
| BEAT-150 | 📦 | شبكة الإيقاع · Beat grid helper | SP-0322 Beat grid clock (beats) | — |
| BEAT-185 | 👁 | قطع على شبكة الإيقاع · Beat-grid cuts | SP-0322 Beat grid clock (beats) | — |
| BEAT-206 | 👁 | خط زمني مقفل على الإيقاع · BPM beat grid timeline | SP-0322 Beat grid clock (beats) | — |
| BEAT-209 | 👁 | شبكة تنبض مع الإيقاع · Beat grid pulse | SP-0322 Beat grid clock (beats) | — |
| BEAT-211 | 👁 | قطع على شبكة الإيقاع · Beat-grid cutting | SP-0322 Beat grid clock (beats) | — |
| BEAT-215 | 📄 | مونتاج على شبكة الإيقاع · Beat-grid trailer edit | SP-0322 Beat grid clock (beats) | — |
| BEAT-217 | 📄 | مقطع دعائي مقصوص على الإيقاع · Beat-grid trailer from a capture | SP-0322 Beat grid clock (beats) | ffmpeg, pip:numpy, pip:librosa |
| BEAT-226 | 📄 | جدول سرعات تناسب شبكة الإيقاع · Beat-grid friendly BPM table | SP-0322 Beat grid clock (beats) | — |
| BEAT-286 | 💡 | شبكة 110 نبضة · 110 BPM beat grid derivation | SP-0322 Beat grid clock (beats) | — |
| BEAT-292 | 💡 | تفاعل على الإيقاع · Frame-accurate beat reactions | SP-0322 Beat grid clock (beats) | — |
| BEAT-14 | ✅ | كاشف الإيقاع · Beat tracker (numpy) | SP-0323 Beat grid detection | pip:numpy |
| BEAT-15 | ✅ | نبضة الضربة · hitPulse punch envelope | SP-0323 Beat grid detection | — |
| BEAT-20 | ✅ | متتبع الإيقاع · Beat tracker (numpy only) | SP-0323 Beat grid detection | pip:numpy |
| BEAT-65 | 🟢 | كشف الإيقاع · Beat grid detection | SP-0323 Beat grid detection | pip:numpy |
| BEAT-72 | 🟢 | تقدير الإيقاع BPM · Tempo (BPM) estimate from spectral flux | SP-0323 Beat grid detection | — |
| BEAT-103 | 📦 | النبض مع الإيقاع · Beat-reactive pulse | SP-0323 Beat grid detection | — |
| BEAT-105 | 📦 | أمر: استخراج الإيقاع · CLI: beats | SP-0323 Beat grid detection | npm:hyperframes |
| BEAT-111 | 📦 | خلفية نابضة على الإيقاع · Beat Pulse Background | SP-0323 Beat grid detection | npm:hyperframes |
| BEAT-125 | 📦 | شبكة الإيقاع لاستوديو · Studio beat grid (beats command) | SP-0323 Beat grid detection | python3, chromium, npm:hyperframes |
| BEAT-142 | 📦 | كاشف الإيقاع وسرعة BPM · Kick-band beat & BPM detector | SP-0323 Beat grid detection | ffmpeg, python3 |
| BEAT-159 | 📦 | كشف الإيقاع بالقياس · Measured beat detection | SP-0323 Beat grid detection | pip:librosa |
| BEAT-92 | 📦 | تتبع الإيقاع في المتصفح · Browser beat tracker (spectral flux + autocorrelation) | SP-0323 Beat grid detection | — |
| BEAT-220 | 📄 | جدول تحويل الإيقاع إلى إطارات · Tempo-to-frame grid table | SP-0323 Beat grid detection | pip:numpy, pip:librosa |
| BEAT-287 | 💡 | كشف الإيقاع · BPM-detect beat grid | SP-0323 Beat grid detection | pip:librosa |
| BEAT-288 | 💡 | ضربات على النبض · Beat-locked punch-ins | SP-0323 Beat grid detection | — |
| BEAT-01 | ✅ | توحيد الجهارة بمرورين · Two-pass loudness normalisation | SP-0324 Loudness normalisation -14 LUFS | ffmpeg |
| BEAT-09 | ✅ | معايرة الصوت −14 LUFS · Loudness: −14 LUFS and BS.1770 meter | SP-0324 Loudness normalisation -14 LUFS | node |
| BEAT-18 | ✅ | ضبط الجهارة · Loudness mastering (−14 LUFS) | SP-0324 Loudness normalisation -14 LUFS | ffmpeg, imagemagick |
| BEAT-27 | ✅ | قياس الجهارة EBU R128 · EBU R128 loudness measurement | SP-0324 Loudness normalisation -14 LUFS | ffmpeg |
| BEAT-39 | 🟢 | أهداف ارتفاع الصوت للموسيقى المولدة · Loudness mastering targets for generated music | SP-0324 Loudness normalisation -14 LUFS | ffmpeg |
| BEAT-73 | 🟢 | معايرة الصوت إلى -14 LUFS · Loudness master to -14 LUFS (loudnorm) | SP-0324 Loudness normalisation -14 LUFS | ffmpeg |
| BEAT-77 | 🟢 | ضبط علو الصوت للنشر · Broadcast loudness master | SP-0324 Loudness normalisation -14 LUFS | ffmpeg, imagemagick |
| BEAT-106 | 📦 | أمر: تسوية الصوت · CLI: normalize-audio | SP-0324 Loudness normalisation -14 LUFS | npm:hyperframes |
| BEAT-152 | 📦 | مستويات الصوت · Loudness targets | SP-0324 Loudness normalisation -14 LUFS | ffmpeg |
| BEAT-248 | 📄 | توحيد الجهارة للنشر · Publish loudness normalization | SP-0324 Loudness normalisation -14 LUFS | ffmpeg |
| BEAT-261 | 📄 | أهداف الجهارة · Loudness targets per platform | SP-0324 Loudness normalisation -14 LUFS | ffmpeg |
| BEAT-263 | 📄 | سلسلة ماسترينغ · Audio mastering chain | SP-0324 Loudness normalisation -14 LUFS | ffmpeg, python3 |
| BEAT-269 | 📄 | تطبيع الجهارة -14 LUFS · Loudness normalisation -14 LUFS | SP-0324 Loudness normalisation -14 LUFS | ffmpeg |
| BEAT-283 | 💡 | أوديوجرام للبودكاست · Podcast audiogram | SP-0324 Loudness normalisation -14 LUFS | ffmpeg, pip:faster-whisper, npm:gsap, npm:remotion |
| BEAT-38 | 🟢 | أعمدة الطيف الصوتي · Audio spectrum bars | SP-0325 Remotion spectrum bars & waveform | ffmpeg |
| BEAT-41 | 🟢 | موجة أعمدة تتفاعل مع الميكروفون · Mic-reactive bar waveform (canvas) | SP-0325 Remotion spectrum bars & waveform | — |
| BEAT-102 | 📦 | موجات الصوت · Audio visualiser (bars / circle) | SP-0325 Remotion spectrum bars & waveform | — |
| BEAT-113 | 📦 | موجة صوتية · Waveform | SP-0325 Remotion spectrum bars & waveform | chromium, npm:hyperframes |
| BEAT-156 | 📦 | موجة صوت · Style: Audio wave (audio-wave) | SP-0325 Remotion spectrum bars & waveform | ffmpeg, python3, npm:remotion |
| BEAT-87 | 📦 | أعمدة طيف وموجة صوتية في ريموشن · Remotion spectrum bars & waveform | SP-0325 Remotion spectrum bars & waveform | npm:remotion |
| BEAT-190 | 👁 | حروف مفرغة تمتلئ مع موجة صوتية · Outline-to-fill letters with waveform | SP-0325 Remotion spectrum bars & waveform | — |
| BEAT-194 | 👁 | كشف كلمة مع موجة صوتية · Waveform word reveal | SP-0325 Remotion spectrum bars & waveform | — |
| BEAT-197 | 👁 | كلمة بين أعمدة موجة صوتية · Waveform-flanked word | SP-0325 Remotion spectrum bars & waveform | — |
| BEAT-203 | 👁 | شريط موجة الإيقاع · Beat waveform bar strip | SP-0325 Remotion spectrum bars & waveform | — |
| BEAT-208 | 👁 | أعمدة إيقاع تحت كلمة · Equaliser under word | SP-0325 Remotion spectrum bars & waveform | — |
| BEAT-225 | 📄 | MG-096 موجة صوت حول الغلاف · MG-096 Amplitude-reactive bars around cover art | SP-0325 Remotion spectrum bars & waveform | ffmpeg, npm:react |
| BEAT-233 | 📄 | الموجة والطيف كعنصر بصري · Waveform/spectrum as a visual asset | SP-0325 Remotion spectrum bars & waveform | ffmpeg |
| BEAT-277 | 📄 | أعمدة المعادل · Equalizer bars | SP-0325 Remotion spectrum bars & waveform | — |
| BEAT-11 | ✅ | إزالة الصوت البشري بإلغاء المركز · Centre-cancel vocal removal (Audio Lab) | SP-0326 Audio isolation / voice cleanup | — |
| BEAT-42 | 🟢 | مقياس مستوى الميكروفون · Mic level meter (AnalyserNode RMS) | SP-0326 Audio isolation / voice cleanup | — |
| BEAT-51 | 🟢 | تحليل الصوت · Audio analysis | SP-0326 Audio isolation / voice cleanup | python3 |
| BEAT-100 | 📦 | تحسين الكلام التلقائي · Automatic speech enhancement chain | SP-0326 Audio isolation / voice cleanup | — |
| BEAT-89 | 📦 | مكتبة توليف بايثون · Python synthesis toolkit (numpy/scipy) | SP-0326 Audio isolation / voice cleanup | pip:numpy, pip:scipy, pip:soundfile |
| BEAT-176 | 🔑 | عزل الحوار بالذكاء الاصطناعي قبل المونتاج · AI dialogue isolation before editing | SP-0326 Audio isolation / voice cleanup | key:elevenlabs |
| BEAT-177 | 🔑 | تنظيف الصوت محلياً · Local voice cleaning via bridge (audiolab.py) | SP-0326 Audio isolation / voice cleanup | python3, key:unspecified |
| BEAT-227 | 📄 | عزل الصوت وتنظيفه · Audio isolation / voice cleanup | SP-0326 Audio isolation / voice cleanup | ffmpeg, key:elevenlabs |
| BEAT-238 | 📄 | وضوح الصوت على سماعة الهاتف · Phone-speaker audibility | SP-0326 Audio isolation / voice cleanup | — |
| BEAT-245 | 📄 | عرض ستيريو آمن للمونو · Mono-safe stereo width | SP-0326 Audio isolation / voice cleanup | ffmpeg |
| BEAT-275 | 📄 | قيم متفاعلة منعّمة · Smoothed audio-reactive values | SP-0326 Audio isolation / voice cleanup | ffmpeg, python3, npm:remotion |
| BEAT-290 | 💡 | قطع على الصوت · Sound-first cuts with held silence | SP-0326 Audio isolation / voice cleanup | — |
| BEAT-294 | 💡 | أصوات مولدة · Event-synthesized UI tones | SP-0326 Audio isolation / voice cleanup | — |
| BEAT-166 | 🔑 | برومبت الأسلوب السداسي في Suno · Suno six-layer style prompt | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-167 | 🔑 | تجاوز الأسلوب لكل مقطع في Suno · Suno per-section style overrides | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-168 | 🔑 | تصنيف وسوم Suno والتلميحات المضمنة · Suno tag taxonomy and inline cues | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-169 | 🔑 | حيل الأداء الصوتي في Suno · Suno vocal performance tricks | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-170 | 🔑 | أخطاء Suno الشائعة وحلولها · Suno anti-patterns and fixes | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-171 | 🔑 | تحرير Suno: الغلاف والتمديد واستبدال المقطع · Suno editing: Cover, Extend, Replace Section, Personas | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-172 | 🔑 | تقسيم Suno إلى مسارات وملفات بإيقاع مقفل · Suno stems, tempo-locked WAV and MIDI for editing | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-173 | 🔑 | اللغة والأنماط العربية في Suno · Suno language and Arabic-flavoured genres | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-174 | 🔑 | قوالب الأنماط الموسيقية في Suno · Suno genre templates | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-178 | 🔑 | حزمة أغنية لـ Suno/Udio · Suno/Udio song package | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-X08 | 🔑 | حقل الأسلوب والاستبعاد في Suno · Suno Style field order and Exclude rules | SP-0327 Suno six-layer style prompt | key:video-gen |
| BEAT-234 | 📄 | لوحات الأنواع الموسيقية · Genre palettes (BPM/swing/instrument) | SP-0327 Suno six-layer style prompt | — |
| BEAT-08 | ✅ | مخطط ريلز الأغاني · Song reel planner (sections, excerpt, shot grid) | SP-0328 Song brief spec + beat durations | — |
| BEAT-69 | 🟢 | ريل أغنية · Songreel lyric montage | SP-0328 Song brief spec + beat durations | python3, imagemagick |
| BEAT-164 | 🔑 | خطة تأليف موسيقى ElevenLabs · ElevenLabs Music composition plan | SP-0328 Song brief spec + beat durations | key:elevenlabs |
| BEAT-165 | 🔑 | الكلمات داخل أقسام الخطة فقط · Lyrics only via plan sections | SP-0328 Song brief spec + beat durations | key:unspecified |
| BEAT-175 | 🔑 | خطة تأليف ElevenLabs بالموازير · ElevenLabs Music composition plan in whole bars | SP-0328 Song brief spec + beat durations | key:elevenlabs |
| BEAT-X09 | 🔑 | خريطة الإصلاح الجراحي للأغنية · Surgical song iteration map | SP-0328 Song brief spec + beat durations | key:video-gen |
| BEAT-186 | 👁 | دفعة لقطات على الإيقاع مع شارة اسم الصانع · Beat-cut reel burst with handle chips | SP-0328 Song brief spec + beat durations | — |
| BEAT-260 | 📄 | موجز الأغنية ومدد الإيقاع · Song brief spec + beat durations | SP-0328 Song brief spec + beat durations | — |
| BEAT-272 | 📄 | خريطة بنية المقطوعة · Song structure map | SP-0328 Song brief spec + beat durations | — |
| BEAT-X01 | 📄 | أفضل نافذة موسيقية للفيلم · Best music window finder | SP-0328 Song brief spec + beat durations | ffmpeg, python3 |
| BEAT-X06 | 📄 | ملخص الأغنية والخطاف أولًا · Song brief and hook-first writing | SP-0328 Song brief spec + beat durations | — |
| BEAT-X10 | 📄 | تسليم الأغنية بأربع كتل ومعيار النجاح · Four-block song hand-off and PASS rubric | SP-0328 Song brief spec + beat durations | — |
| BEAT-110 | 📦 | لسعة الإيقاع · Beat Accent | SP-0329 Impact/sub-drop on cut | chromium, npm:hyperframes |
| BEAT-160 | 📦 | غلاف التأكيد · Accent envelope / BeatPulse | SP-0329 Impact/sub-drop on cut | npm:remotion |
| BEAT-195 | 👁 | لحظة سواد قبل الذروة · Silence-before-drop black beat | SP-0329 Impact/sub-drop on cut | — |
| BEAT-221 | 📄 | ربط ضربات المونتاج بنبضات الموسيقى · Edit hits married to music transients | SP-0329 Impact/sub-drop on cut | — |
| BEAT-251 | 📄 | رايزر قبل القطع · Riser/whoosh before cut | SP-0329 Impact/sub-drop on cut | — |
| BEAT-252 | 📄 | ضربة على القطع · Impact/sub-drop on cut | SP-0329 Impact/sub-drop on cut | — |
| BEAT-255 | 📄 | مؤثر صاعد قبل القطع وضربة عنده · Riser/whoosh before cut, impact on cut | SP-0329 Impact/sub-drop on cut | — |
| BEAT-265 | 📄 | القطع على الإيقاع · Beat-cut rules | SP-0329 Impact/sub-drop on cut | — |
| BEAT-276 | 📄 | وصفة التصاعد والذروة · Build and drop recipe | SP-0329 Impact/sub-drop on cut | — |
| BEAT-X02 | 📄 | لصق أزمنة السيناريو على الضربات · Snap scenario times to real hits | SP-0329 Impact/sub-drop on cut | python3 |
| BEAT-X03 | 📄 | تحقق الضربات على المزج النهائي · Verify picture hits on the final mix | SP-0329 Impact/sub-drop on cut | python3 |
| BEAT-X05 | 📄 | القطعات هي الإيقاع · Cuts are the rhythm: synthesized launch-film score | SP-0329 Impact/sub-drop on cut | pip:numpy |
| BEAT-33 | 🟢 | مستويات علو المؤثرات · SFX loudness tiers | SP-0330 Sound design density | — |
| BEAT-44 | 🟢 | مسار إشارات المؤثرات · SFX cue track (cues only) | SP-0330 Sound design density | — |
| BEAT-117 | 📦 | سلسلة المؤثرات الصوتية على المسار · Audio FX chain on any track (data-fx-chain) | SP-0330 Sound design density | chromium |
| BEAT-118 | 📦 | سجل معاملات المؤثرات · Effect parameter registry (ranges and defaults) | SP-0330 Sound design density | — |
| BEAT-91 | 📦 | توافق المؤثرات النغمية مع المقام · Tonal SFX key check | SP-0330 Sound design density | — |
| BEAT-96 | 📦 | تركيب طبقة المؤثرات · SFX stem compositor | SP-0330 Sound design density | — |
| BEAT-179 | 🔑 | جدول تصميم المؤثرات الصوتية · SFX design sheet | SP-0330 Sound design density | key:elevenlabs |
| BEAT-219 | 📄 | مزامنة المؤثرات وترتيب المكساج · Sound design sync and mix order | SP-0330 Sound design density | ffmpeg, pip:numpy |
| BEAT-249 | 📄 | كثافة المؤثرات · Sound design density | SP-0330 Sound design density | — |
| BEAT-23 | ✅ | قناة المزج · Score mix bus | SP-0331 Score mix bus | — |
| BEAT-34 | 🟢 | حلقات سلسة بالرندر الثلاثي · Seamless loops render-three-keep-middle | SP-0331 Score mix bus | pip:numpy |
| BEAT-107 | 📦 | سلسلة مؤثرات صوتية · Audio fx chain (WebAudio-style) | SP-0331 Score mix bus | — |
| BEAT-120 | 📦 | حافلة المزج الفرعي · Submix bus <hf-audio-group> | SP-0331 Score mix bus | — |
| BEAT-122 | 📦 | إعدادات الفضاء والصدى · Space / reverb presets | SP-0331 Score mix bus | — |
| BEAT-123 | 📦 | ملفات المقبض الواحد للمؤثرات · One-knob effect profiles | SP-0331 Score mix bus | — |
| BEAT-145 | 📦 | سلسلة ماسترنج ذاتية · Self-mastering chain (reverb, shelf, loudness, true-peak guard) | SP-0331 Score mix bus | — |
| BEAT-256 | 📄 | سلسلة المكساج والماستر · Mix/master processing chain with numbers | SP-0331 Score mix bus | ffmpeg |
| BEAT-22 | ✅ | وصفات الآلات المركبة · Synth instrument recipes | SP-0332 Synth instrument recipes | — |
| BEAT-68 | 🟢 | موسيقى أصلية مولدة · Original score synth | SP-0332 Synth instrument recipes | python3 |
| BEAT-136 | 📦 | مرئيات تتفاعل مع الصوت · Audio-reactive visuals (kick/bass mapping) | SP-0332 Synth instrument recipes | — |
| BEAT-90 | 📦 | كتابة اللحن بالخطوات · Step-notation melody writing | SP-0332 Synth instrument recipes | — |
| BEAT-198 | 👁 | موسيقى مولّدة بالكود ومقفلة على القطعات · Code-synthesized beat-locked soundtrack | SP-0332 Synth instrument recipes | pip:numpy |
| BEAT-259 | 📄 | الآلات العربية · Arabic instrument palette | SP-0332 Synth instrument recipes | — |
| BEAT-P01 | 📄 | نقرات صوتية مولّدة على لحظات الحركة · Code-synthesised chirp ticks on motion events | SP-0332 Synth instrument recipes | pip:numpy |
| BEAT-293 | 💡 | نبض على الكيك · Kick pulse exponential decay | SP-0332 Synth instrument recipes | — |
| BEAT-03 | ✅ | توقف الشريط وإقلاعه · Tape-stop / tape-start | SP-0333 Tape-stop bullet time and glitch accents | — |
| BEAT-49 | 🟢 | تحليل الإيقاع والقنوات · beats / channels analysis | SP-0333 Tape-stop bullet time and glitch accents | python3 |
| BEAT-132 | 📦 | الصوت يحرك الصورة · Sound-driven picture | SP-0333 Tape-stop bullet time and glitch accents | npm:three |
| BEAT-135 | 📦 | توقف الشريط ووقت الرصاصة ولمسات الخلل · Tape-stop bullet time and glitch accents | SP-0333 Tape-stop bullet time and glitch accents | — |
| BEAT-141 | 📦 | قنوات الصوت · Audio channels + tape-stop | SP-0333 Tape-stop bullet time and glitch accents | python3 |
| BEAT-155 | 📦 | فيلم يستمع بالرياضيات · Listen-with-math music film | SP-0333 Tape-stop bullet time and glitch accents | python3 |
| BEAT-273 | 📄 | تأكيد الضربات القوية والضعيفة · Strong/weak beat accents | SP-0333 Tape-stop bullet time and glitch accents | — |
| BEAT-128 | 📦 | فيديو متزامن مع إيقاع الموسيقى · Music-to-video beat-synced workflow | SP-0334 Arabic rhythm (iqa') patterns | npm:hyperframes |
| BEAT-93 | 📦 | نمط مونتاج سريع سريع نَفَس · Editor's beat pattern (hook-quick-quick-breathe) | SP-0334 Arabic rhythm (iqa') patterns | — |
| BEAT-187 | 👁 | مخطط أعمدة يتزامن مع الإيقاع · Beat-synced bar chart | SP-0334 Arabic rhythm (iqa') patterns | — |
| BEAT-199 | 👁 | شيفرة تتوهج مع الإيقاع · Beat-highlighted code | SP-0334 Arabic rhythm (iqa') patterns | — |
| BEAT-257 | 📄 | لوحة المقامات العربية · Arabic maqam palette | SP-0334 Arabic rhythm (iqa') patterns | — |
| BEAT-258 | 📄 | الإيقاعات العربية · Arabic rhythm (iqa') patterns | SP-0334 Arabic rhythm (iqa') patterns | — |
| BEAT-X07 | 📄 | بوابات اللهجة العربية في الأغاني · Arabic dialect gates for song lyrics | SP-0334 Arabic rhythm (iqa') patterns | — |
| BEAT-25 | ✅ | مولد الأصوات المحيطة · Ambience synthesiser | SP-0335 ambience synthesis | python3 |
| BEAT-45 | 🟢 | كوسف: توليد موسيقى ومحيط صوتي إجرائيا · KOSIF: procedural score and ambience synthesis | SP-0335 ambience synthesis | pip:numpy |
| BEAT-48 | 🟢 | أجواء صوتية مولدة · ambience synthesis | SP-0335 ambience synthesis | python3 |
| BEAT-58 | 🟢 | ملفات صوت الخلفية والموسيقى · Ambient bed and score audio files | SP-0335 ambience synthesis | — |
| BEAT-67 | 🟢 | أجواء مولدة · Synth ambience | SP-0335 ambience synthesis | pip:numpy |
| BEAT-76 | 🟢 | أصوات أجواء مولدة · Synthesised ambience | SP-0335 ambience synthesis | python3 |
| BEAT-139 | 📦 | صوت محيطي مُركّب · Synth ambience fallback | SP-0335 ambience synthesis | python3 |
| BEAT-59 | 🟢 | مقام minor · Score scale minor | SP-0336 Score scale lydian | pip:numpy |
| BEAT-60 | 🟢 | مقام major · Score scale major | SP-0336 Score scale lydian | pip:numpy |
| BEAT-61 | 🟢 | مقام dorian · Score scale dorian | SP-0336 Score scale lydian | pip:numpy |
| BEAT-62 | 🟢 | مقام hijaz · Score scale hijaz | SP-0336 Score scale lydian | pip:numpy |
| BEAT-63 | 🟢 | مقام pentatonic · Score scale pentatonic | SP-0336 Score scale lydian | pip:numpy |
| BEAT-64 | 🟢 | مقام lydian · Score scale lydian | SP-0336 Score scale lydian | pip:numpy |
| BEAT-144 | 📦 | موسيقى حجاز مركّبة بلا عينات · Hijaz synth soundtrack (numpy/scipy, no samples) | SP-0336 Score scale lydian | pip:numpy, pip:scipy, npm:d3, fonts:arabic |
| BEAT-32 | 🟢 | القص على حدود المازورة · Bar-grid cutting | SP-0337 Bar-counter HUD | — |
| BEAT-188 | 👁 | إطار HUD بعداد المقاطع ونصوص مشفرة تتفكك · Beat-bar HUD with scramble labels | SP-0337 Bar-counter HUD | — |
| BEAT-201 | 👁 | واجهة عداد البارات الإيقاعية · Bar-counter HUD | SP-0337 Bar-counter HUD | — |
| BEAT-202 | 👁 | قطع الفصول على المازورة · Bar-locked chapter cuts | SP-0337 Bar-counter HUD | — |
| BEAT-205 | 👁 | عدّاد مازورة وضربة في الواجهة · Beat/bar HUD counter | SP-0337 Bar-counter HUD | — |
| BEAT-210 | 👁 | قطع على إيقاع البار · BPM bar cut grid | SP-0337 Bar-counter HUD | — |
| BEAT-200 | 👁 | بطاقة نتيجة تتبدل أسلوبها على إيقاع النوتات · Style-roll result card on 16th notes | SP-0338 Rising pitch per pass | — |
| BEAT-237 | 📄 | دلالات النغمة · Pitch/interval semantics | SP-0338 Rising pitch per pass | — |
| BEAT-239 | 📄 | تنويع لتجنب الملل · Anti-fatigue variants | SP-0338 Rising pitch per pass | — |
| BEAT-240 | 📄 | بداية المؤثر بلا تأخير · Zero-latency transient start | SP-0338 Rising pitch per pass | ffmpeg |
| BEAT-247 | 📄 | انحناء النغمة بتكامل الطور · Phase-integrated pitch bends | SP-0338 Rising pitch per pass | — |
| BEAT-291 | 💡 | نغمة متصاعدة · Rising pitch per pass | SP-0338 Rising pitch per pass | — |
| BEAT-19 | ✅ | قنوات الصوت لكل إطار · Per-frame sound channels | SP-0339 Spectrogram canyon (sound as terrain) | python3 |
| BEAT-28 | 🟢 | أرض من طيف الصوت · Spectrogram canyon ground | SP-0339 Spectrogram canyon (sound as terrain) | python3 |
| BEAT-133 | 📦 | وادٍ من المخطط الطيفي · Spectrogram canyon (sound as terrain) | SP-0339 Spectrogram canyon (sound as terrain) | — |
| BEAT-153 | 📦 | طيف على ساعة الشريط · Spectrum on tape clock | SP-0339 Spectrogram canyon (sound as terrain) | — |
| BEAT-280 | 📄 | تصميم صوت شحيح للواجهة · Sparse UI sound design | SP-0339 Spectrogram canyon (sound as terrain) | — |
| BEAT-101 | 📦 | بوابة ضوضاء بين الكلمات · Downward expander between words | SP-0340 Procedural chalk scratch sound | — |
| BEAT-182 | 👁 | صوت خربشة طباشير مولّد · Procedural chalk scratch sound | SP-0340 Procedural chalk scratch sound | — |
| BEAT-212 | 👁 | صوت ماركر مولد بالكود · Procedural marker squeak | SP-0340 Procedural chalk scratch sound | — |
| BEAT-242 | 📄 | ملء الصمت بنبرة الغرفة · Room tone fills | SP-0340 Procedural chalk scratch sound | — |
| BEAT-37 | 🟢 | قص تريلر على البار · Beat-mapped trailer cuts | SP-0341 Beat-mapped bounce path | — |
| BEAT-189 | 👁 | مسار قفز مربوط بالإيقاع · Beat-mapped bounce path | SP-0341 Beat-mapped bounce path | — |
| BEAT-192 | 👁 | جدولة النغمات بمقذوفات عكسية · Inverse-ballistic note scheduling | SP-0341 Beat-mapped bounce path | — |
| BEAT-224 | 📄 | MG-094/098 مسار الكرة وخطوط السرعة · MG-094/098 Trajectory path and local speed lines | SP-0341 Beat-mapped bounce path | ffmpeg |

## voice-tts (motion)

chapter: [voice-tts](../powers/voice-tts.md) · card: `usip-library/cards/audio/voice-tts.md` · tools: `tts-script`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| VOICE-43 | ✅ | خفض الموسيقى تحت التعليق · Music ducking under the voice | SP-0318 Music ducking under voice (sidechain) | ffmpeg |
| VOICE-01 | ✅ | تعليق عربي محلي بـ Piper · Piper offline Arabic TTS | SP-0472 Character voice costumes | ffmpeg, pip:piper, pip:onnxruntime, network |
| VOICE-27 | ✅ | صوت الراوي الوثائقي المقفل · Locked documentary narrator voice | SP-0472 Character voice costumes | — |
| VOICE-39 | ✅ | سلسلة تنظيف الصوت البشري · Voice clean-up chain | SP-0472 Character voice costumes | ffmpeg, python3, imagemagick |
| VOICE-41 | ✅ | أزياء صوتية للشخصيات · Character voice costumes | SP-0472 Character voice costumes | ffmpeg, pip:piper |
| VOICE-42 | ✅ | مختبر الصوت: عزل الصوت وفصل الموسيقى · Audiolab voice isolation & stem split | SP-0472 Character voice costumes | python3 |
| VOICE-48 | ✅ | موجه نوايا صوتي عربي حتمي · Deterministic Arabic voice intent router | SP-0472 Character voice costumes | node |
| VOICE-04 | 🟢 | نطق المتصفح العربي ar-SA · Browser Web Speech fallback (ar-SA) | SP-0472 Character voice costumes | chromium |
| VOICE-49 | 🟢 | كرة الصوت بحالاتها · Voice orb state animation | SP-0472 Character voice costumes | — |
| VOICE-03 | 📦 | Kokoro المحلي (بلا عربية) · Kokoro local TTS (no Arabic voice) | SP-0472 Character voice costumes | pip:kokoro, pip:soundfile, npm:hyperframes, network |
| VOICE-09 | 🔑 | استنساخ صوت بموافقة صاحبه · Consented voice cloning | SP-0472 Character voice costumes | node, key:elevenlabs |
| VOICE-10 | 🔑 | تحويل صوت إلى صوت · Speech-to-speech re-voice | SP-0472 Character voice costumes | key:unspecified |
| VOICE-12 | 🔑 | إخراج أداء الصوت بواسطة Claude · Claude-directed voice performance | SP-0472 Character voice costumes | pip:piper, fonts:arabic, key:unspecified |
| VOICE-13 | 🔑 | حوار بأكثر من متكلم · Multi-speaker dialogue production | SP-0472 Character voice costumes | imagemagick, key:unspecified |
| VOICE-15 | 🔑 | محرك الصوت الموحد audio_meta.json · Unified audio engine (voice + words + BGM + SFX) | SP-0472 Character voice costumes | npm:hyperframes, key:unspecified |
| VOICE-16 | 🔑 | كتالوج Together للصوت · Together AI TTS catalog | SP-0472 Character voice costumes | pip:kokoro, key:unspecified |
| VOICE-46 | 🔑 | محادثة صوتية عربية لحظية عبر WebRTC · Realtime Arabic speech-to-speech (WebRTC) | SP-0472 Character voice costumes | key:openai |
| VOICE-47 | 🔑 | مقاطعة المساعد بالكلام · Barge-in interruption | SP-0472 Character voice costumes | key:unspecified |
| VOICE-36 | 👁 | ترجمة تُكتب على توقيت الصوت · Typewriter captions on voice word times | SP-0472 Character voice costumes | key:elevenlabs |
| VOICE-37 | 👁 | موجة الصوت ومؤشر التشغيل · Voice waveform with playhead | SP-0472 Character voice costumes | ffmpeg |
| VOICE-02 | 📄 | صوت ويندوز العربي (نايف) بالجدول الزمني · Windows OneCore Arabic narration (Naayf) | SP-0472 Character voice costumes | python3 |
| VOICE-05 | 📄 | أصوات Edge العصبية والمولدات المبنية عليها · Edge neural voices & scene-file generators | SP-0472 Character voice costumes | ffmpeg, python3, chromium, docker |
| VOICE-17 | 📄 | أوضاع مخرج الصوت الخارجي · KOSIF Voice Director provider modes | SP-0472 Character voice costumes | — |
| VOICE-22 | 📄 | سكربت تعليق بوسوم أداء SSML · VO script with performance tags (SSML) | SP-0472 Character voice costumes | pip:piper, key:elevenlabs |
| VOICE-26 | 📄 | شخصية اليوتيوبر المصري · Egyptian YouTuber voice persona | SP-0472 Character voice costumes | — |
| VOICE-40 | 📄 | وصفات إصلاح الصوت بالأعراض · Voice repair presets by symptom | SP-0472 Character voice costumes | ffmpeg, npm:hyperframes |
| VOICE-53 | 📄 | لا تقليد لأصوات حقيقية · Never imitate real voices | SP-0472 Character voice costumes | — |
| VOICE-31 | ✅ | مدة المشهد = طول التعليق + هامش · Scene duration from voice length | SP-0473 Words-per-second budget | ffmpeg, npm:remotion |
| VOICE-32 | ✅ | توقيت كلمات التعليق المولد بـ faster-whisper · Word timings from the generated voice (faster-whisper) | SP-0473 Words-per-second budget | pip:numpy, pip:faster-whisper |
| VOICE-08 | 🔑 | تقسيم النص الطويل مع حفظ النبرة · Long-script chunking with prosody context | SP-0473 Words-per-second budget | key:unspecified |
| VOICE-14 | 🔑 | HeyGen Starfish بطوابع زمنية للكلمات · HeyGen Starfish TTS with word timestamps | SP-0473 Words-per-second budget | node, pip:kokoro, key:elevenlabs |
| VOICE-34 | 👁 | إيقاع يقوده التعليق · Voice-led pacing | SP-0473 Words-per-second budget | — |
| VOICE-35 | 👁 | قراءة صوتية بتظليل الكلمة المنطوقة · Read-aloud karaoke highlight | SP-0473 Words-per-second budget | — |
| VOICE-38 | 👁 | محاضرة مروية: رسم يتقدم مع الجمل · Narrated lecture: draw-on paced to sentences | SP-0473 Words-per-second budget | — |
| VOICE-18 | 📄 | ميزانية الكلمات في الثانية · Words-per-second budget | SP-0473 Words-per-second budget | pip:piper |
| VOICE-20 | 📄 | نص النطق غير نص الشاشة · Spoken form vs on-screen form | SP-0473 Words-per-second budget | — |
| VOICE-21 | 📄 | قواعد كتابة التعليق للمشهد · Scene narration writing rules | SP-0473 Words-per-second budget | — |
| VOICE-23 | 📄 | نص التعليق المقفل SCRIPT.md · Locked narration file (SCRIPT.md) | SP-0473 Words-per-second budget | — |
| VOICE-33 | 📄 | إعادة لصق النص المعروف على توقيت ويسبر · Re-attach the known script to Whisper timings | SP-0473 Words-per-second budget | pip:faster-whisper |
| VOICE-19 | ✅ | السرعة حسب المحتوى — أعد التوليد ولا تمطّ · Read speed by content — regenerate, never stretch | SP-0474 Model & output-format choice | pip:piper |
| VOICE-44 | ✅ | التسليم بجهارة −14 LUFS وفحص البوابة · −14 LUFS delivery + gate | SP-0474 Model & output-format choice | ffmpeg, python3 |
| VOICE-06 | 🔑 | تعليق ElevenLabs بإعدادات جاهزة · ElevenLabs narration presets | SP-0474 Model & output-format choice | npm:remotion, key:elevenlabs |
| VOICE-07 | 🔑 | اختيار النموذج والصيغة حسب الاستخدام · Model & output-format choice | SP-0474 Model & output-format choice | key:elevenlabs |
| VOICE-11 | 🔑 | Gemini TTS بثلاثين صوتًا · Gemini TTS with 30 prebuilt voices | SP-0474 Model & output-format choice | key:unspecified |
| VOICE-24 | 📄 | توجيه الصوت باللهجات العربية · Arabic dialect voice-direction workflow | SP-0474 Model & output-format choice | — |
| VOICE-45 | 📄 | وصل المقاطع كـ WAV لا MP3 · Join chunks as PCM, not MP3 copy | SP-0474 Model & output-format choice | — |
| VOICE-54 | 📄 | لا ادعاء بلا ملف · No audio claim without a receipt | SP-0474 Model & output-format choice | ffmpeg |
| VOICE-55 | 📄 | نظافة تكلفة الحروف · TTS character-cost hygiene | SP-0474 Model & output-format choice | — |
| VOICE-50 | 🟢 | نبض حلقة زر الميكروفون العائم · Live mic FAB ring pulse | SP-0475 Clean mic capture constraints | — |
| VOICE-51 | 🟢 | التقاط ميكروفون نظيف · Clean mic capture constraints | SP-0475 Clean mic capture constraints | — |
| VOICE-52 | 🟢 | تسجيل الصوت وتنزيله · MediaRecorder capture + download | SP-0475 Clean mic capture constraints | ffmpeg |
| VOICE-29 | 📄 | مواصفات تسجيل الصوت البشري · Human VO recording spec | SP-0475 Clean mic capture constraints | — |
| VOICE-28 | ✅ | جمل صوت المدرب · Coach voice cue lines | SP-0476 Language Coach (AR/EN) skill | — |
| VOICE-25 | 🟢 | اختيار اللغة واللهجة في المقابلة · Language & dialect intake field | SP-0476 Language Coach (AR/EN) skill | pip:piper |
| VOICE-30 | 📄 | مدرب اللغة الثنائي · Language Coach (AR/EN) skill | SP-0476 Language Coach (AR/EN) skill | — |
