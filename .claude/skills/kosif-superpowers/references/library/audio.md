# الصوت والموسيقى والتعليق — Audio & voice (`audio`)

> مكتبة بروتوكول USIP v5.6، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: audio music voice speech tts subtitles beat sync caption صوت موسيقى تعليق ترجمة توقيت

خط العمل المقترح (هدف تصميم، لم يُختبر كوحدة واحدة): المعالجة → المزامنة → التعليق والترجمة → التحقق

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 59 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 74 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 117 | 📄 documented: a described method; needs building or wiring before it runs |
| `seen` | 42 | 👁 seen: observed in a reference or demo, not executed here |
| `install` | 82 | 📦 install: needs a package, binary or model first |
| `key` | 36 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 12 | 💡 idea: not built |
| **المجموع** | **422** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `audio-cue-mapper` | مستخرج إشارات التوقيت من الصوت | `python3 scripts/audio_cue_mapper.py ./voice.wav --out ./out/cues.json` | tested-here |
| `blender-cinematic-bridge` | دمج رندر Blender Cycles مع مونتاج KOSIF والصوت | `python3 scripts/blender_cinematic_bridge.py doctor` | tested-here |
| `caption-lines` | سطور الترجمة: من توقيت الكلمات إلى ترجمة مقروءة | `python3 scripts/caption_lines.py group words.json -o captions.srt --rlm` | tested-here |
| `character-fullbody` | تحريك الشخصية بكامل الجسم | `python3 scripts/character_fullbody.py doctor` | tested-here |
| `character-ik` | تحريك ذراع الشخصية بالحركية العكسية | `python3 scripts/character_ik.py doctor` | tested-here |
| `cinematic-cut-planner` | مُخطِّط قطعات اللقطات الحقيقية | `python3 scripts/cinematic_cut_planner.py --words ./words.json --clips ./clips.json --duration 48.5 --fps 30 --out ./out/edl.json` | tested-here |
| `code-drawing-master` | رسم الشخصيات والمشاهد بالكود | `python3 scripts/code_drawing_master.py --cast human+cat --expression happy --location street --action walk --out ./story.json --html ./story.html` | tested-here |
| `creative-quality-gate` | بوابة جودة خطة المونتاج | `python3 scripts/creative_quality_gate.py ./my-project/src/plan.json --out ./out/quality-audit.json` | tested-here |
| `creative-reasoning-bridge` | جسر الصوت إلى لوحة القصة | `python3 scripts/creative_reasoning_bridge.py ./cues.json --style auto --out ./out/scene.json --report ./out/decision.json` | tested-here |
| `dua-wednesday` | دعاء يوم الأربعاء — محرك ريل دعاء موشن جرافيك 9:16 | `python3 scripts/dua_wednesday.py doctor` | tested-here |
| `fast-edit` | التعديل السريع: قص فوري يعرف الإطارات المفتاحية، مغيّر صوت، تفتيح الفيديو المظلم، استخراج الصوت | `python3 scripts/fast_edit.py doctor` | tested-here |
| `kosif-timeline` | محرر KOSIF Timeline: مونتاج متعدد المسارات مع تراجع وإعادة | `python3 scripts/kosif_timeline.py doctor` | tested-here |
| `montage-pro` | فريق مونتاج برو (صوت أو فيديو إلى مونتاج أو موشن) | `python3 scripts/montage_pro.py doctor` | tested-here |
| `motion-director` | مُصرِّف حركة SVG المتزامنة مع الصوت | `python3 scripts/motion_director.py doctor` | tested-here |
| `motion-engine-js` | محرك حركة SVG | `python3 scripts/motion_director.py compile ./scene.json --out ./out/film.html` | tested-here |
| `motion-kit-bridge` | جسر توقيتات Motion Starter Kit | `python3 scripts/motion_kit_bridge.py styles` | tested-here |
| `music-rhythm-engine` | فرضيات إيقاع الموسيقى | `python3 scripts/music_rhythm_engine.py ./out/cues.json --out ./out/rhythm.json` | tested-here |
| `reel-factory` | مصنع الريلز: صوت وتوقيت كلمات ولقطات مرخصة ← ريلز 9:16 مفحوص | `python3 scripts/reel_factory.py plan --audio ./voice.m4a --audio-rights owned --words ./words.json --shots-manifest ./stock/manifest.json --shot-ids 17928486,8165467,20382699 --title "دعاء يوم الخميس" --handle @kosif` | tested-here |
| `reference-edit-engine` | محرك إعادة بناء المونتاج المرجعي | `python3 scripts/reference_edit_engine.py --probe ./cuts.json --out ./new-edit` | tested-here |
| `repo-words-convert` | محوّل الترجمات إلى توقيت الكلمات | `python3 tools/words_convert.py ./captions.srt ./words.json` | tested-here |
| `starter-html-canvas` | قالب فيلم HTML Canvas | `python3 tools/kosif.py scaffold kinetic-arabic ./my-film --starter html-canvas` | tested-elsewhere |
| `starter-remotion` | قالب فيلم Remotion | `python3 tools/kosif.py scaffold product ./my-film --starter remotion` | tested-elsewhere |
| `tts-script` | تجهيز نص التعليق الصوتي: تقطيع آمن وتقدير المدة وSSML | `printf 'مرحبا بكم في KOSIF Studio. هذا اختبار، قصير جدا!\n\nفقرة ثانية؟ نعم.\n' \| python3 scripts/tts_script.py chunk - --max-chars 30` | tested-here |
| `unified-cinematic` | السينما الموحدة: مونتاج الفيديو مع الصوت وحركة الكاميرا | `python3 scripts/unified_cinematic.py doctor` | tested-here |
| `video-workflow-bridge` | جسر سير عمل الفيديو | `python3 scripts/video_workflow_bridge.py paper-edit templates/ik-wave-words.json --keep "1-3,5" --fps 30 --out ./out/paper-edit.json` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `audio-sync-captions` | 61 | [audio-sync-captions.md](../powers/audio-sync-captions.md) |
| `music-beat-sound` | 306 | [music-beat-sound.md](../powers/music-beat-sound.md) |
| `voice-tts` | 55 | [voice-tts.md](../powers/voice-tts.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `SYNC-01` | الصوت هو الساعة الرئيسية | Audio is the master clock | proven | ffmpeg, chromium, npm:remotion |
| `SYNC-02` | ملف توقيت الكلمات kosif-words/1 | words.json master timing schema | proven | python3 |
| `SYNC-03` | محوّل الترجمات والتفريغ إلى words.json | Subtitle/transcript → words.json converter | proven | pip:faster-whisper |
| `SYNC-04` | حدود تسامح التزامن | Sync tolerances | proven |  |
| `SYNC-05` | قياس التزامن إطارًا بإطار | Frame-by-frame sync probe | proven | node |
| `SYNC-07` | تفريغ عربي محلي بتوقيت الكلمات | Local Arabic word-timed transcription (faster-whisper) | proven | pip:faster-whisper, network |
| `SYNC-09` | توقيت حقيقي من فونيمات Piper | True word timing from Piper phonemes | proven | pip:faster-whisper, pip:piper |
| `SYNC-10` | محاذاة النص الصحيح على التفريغ | True-text alignment onto ASR | proven |  |
| `SYNC-18` | توقيت الكلمات حسب الطول | Word timing by length | proven | imagemagick |
| `SYNC-20` | سكريبت بتوقيت مكتوب | Timestamped script parser | proven | node |
| `SYNC-27` | كاريوكي ASS عربي بحدث لكل كلمة | Arabic ASS karaoke, one event per word | proven | ffmpeg, python3, imagemagick |
| `SYNC-28` | سبعة ستايلات ترجمة جاهزة | Seven named caption styles | proven | imagemagick |
| `SYNC-29` | صفحات ترجمة + SRT/VTT/ASS | Caption pages → JSON/SRT/VTT/ASS | proven | pip:faster-whisper |
| `SYNC-32` | دخول الكلمة على بداية نطقها | Word enters on its spoken start | proven |  |
| `SYNC-33` | تعبئة كاريوكي من اليمين بقناع كامل الكلمة | RTL karaoke fill with whole-word clip-path | proven | fonts:arabic |
| `SYNC-34` | كاريوكي الكبسولة في starter الكانفس | Canvas karaoke pill (html-canvas starter) | proven | node, chromium |
| `SYNC-45` | فيلم كلمات من صوت (أغنية، شعر، دعاء) | Verse film from sound | proven | pip:faster-whisper, network |
| `SYNC-46` | Voice2Motion: موشن بالمعنى من الصوت | Voice2Motion semantic scenes | proven | python3 |
| `SYNC-47` | إخراج تلقائي لمقطع متكلم | Editor-style auto direction of a talking clip | proven |  |
| `SYNC-53` | كشف الصمت الثابت والتكيفي | Fixed & adaptive silence detection | proven | ffmpeg, python3 |
| `BEAT-01` | توحيد الجهارة بمرورين | Two-pass loudness normalisation | proven | ffmpeg |
| `BEAT-02` | مؤثرات صوتية مصممة على الإشارات | Designed SFX on picture cues | proven |  |
| `BEAT-03` | توقف الشريط وإقلاعه | Tape-stop / tape-start | proven |  |
| `BEAT-04` | مؤثرات وحوار الرجل العصوي | Stickman foley + dialogue pacing | proven |  |
| `BEAT-05` | تصميم مؤثرات ميكانيكية | Mechanical foley design (car) | proven |  |
| `BEAT-06` | مؤثرات الطعام الملموسة | Tactile food foley + tasting sounds | proven |  |
| `BEAT-07` | سياسات الصمت وعدم الموسيقى | Silent / no-music sound policies | proven |  |
| `BEAT-08` | مخطط ريلز الأغاني | Song reel planner (sections, excerpt, shot grid) | proven |  |
| `BEAT-09` | معايرة الصوت −14 LUFS | Loudness: −14 LUFS and BS.1770 meter | proven | node |
| `BEAT-10` | خفض الموسيقى تحت الصوت | Music ducking under voice (sidechain) | proven | ffmpeg |
| `BEAT-11` | إزالة الصوت البشري بإلغاء المركز | Centre-cancel vocal removal (Audio Lab) | proven |  |
| `BEAT-12` | مكتبة مؤثرات CC0 داخل التايملاين | CC0 SFX kit in timelines | proven |  |
| `BEAT-13` | مسار الموسيقى | Soundtrack track | proven |  |
| `BEAT-14` | كاشف الإيقاع | Beat tracker (numpy) | proven | pip:numpy |
| `BEAT-15` | نبضة الضربة | hitPulse punch envelope | proven |  |
| `BEAT-16` | شبكة الإيقاع | Beat grid clock (beats) | proven | python3 |
| `BEAT-17` | كاشف الموسيقى الخلفية | Music-bed detector | proven |  |
| `BEAT-18` | ضبط الجهارة | Loudness mastering (−14 LUFS) | proven | ffmpeg, imagemagick |
| `BEAT-19` | قنوات الصوت لكل إطار | Per-frame sound channels | proven | python3 |
| `BEAT-20` | متتبع الإيقاع | Beat tracker (numpy only) | proven | pip:numpy |
| `BEAT-21` | مؤلف موسيقى على شبكة الإيقاع | Beat-grid score synthesiser | proven | python3 |
| `BEAT-22` | وصفات الآلات المركبة | Synth instrument recipes | proven |  |
| `BEAT-23` | قناة المزج | Score mix bus | proven |  |
| `BEAT-24` | مواصفات موسيقى المشاريع | Project score specs (templates) | proven | python3 |
| `BEAT-25` | مولد الأصوات المحيطة | Ambience synthesiser | proven | python3 |
| `BEAT-26` | سياسات الصوت والموسيقى | Music/SFX policy presets | proven | python3 |
| `BEAT-27` | قياس الجهارة EBU R128 | EBU R128 loudness measurement | proven | ffmpeg |
| `VOICE-01` | تعليق عربي محلي بـ Piper | Piper offline Arabic TTS | proven | ffmpeg, pip:piper, pip:onnxruntime, network |
| `VOICE-19` | السرعة حسب المحتوى — أعد التوليد ولا تمطّ | Read speed by content — regenerate, never stretch | proven | pip:piper |
| `VOICE-27` | صوت الراوي الوثائقي المقفل | Locked documentary narrator voice | proven |  |
| `VOICE-28` | جمل صوت المدرب | Coach voice cue lines | proven |  |
| `VOICE-31` | مدة المشهد = طول التعليق + هامش | Scene duration from voice length | proven | ffmpeg, npm:remotion |
| `VOICE-32` | توقيت كلمات التعليق المولد بـ faster-whisper | Word timings from the generated voice (faster-whisper) | proven | pip:numpy, pip:faster-whisper |
| `VOICE-39` | سلسلة تنظيف الصوت البشري | Voice clean-up chain | proven | ffmpeg, python3, imagemagick |
| `VOICE-41` | أزياء صوتية للشخصيات | Character voice costumes | proven | ffmpeg, pip:piper |
| `VOICE-42` | مختبر الصوت: عزل الصوت وفصل الموسيقى | Audiolab voice isolation & stem split | proven | python3 |
| `VOICE-43` | خفض الموسيقى تحت التعليق | Music ducking under the voice | proven | ffmpeg |
| `VOICE-44` | التسليم بجهارة −14 LUFS وفحص البوابة | −14 LUFS delivery + gate | proven | ffmpeg, python3 |
| `VOICE-48` | موجه نوايا صوتي عربي حتمي | Deterministic Arabic voice intent router | proven | node |
| `SYNC-06` | التحقق من توقيت جاهز | Pre-timed transcript validation | ready | pip:faster-whisper |
| `SYNC-11` | تصحيح الكلمات مع حفظ التوقيت | Transcript fixes that keep timing | ready |  |
| `SYNC-17` | توزيع النص على مقاطع الصوت | Text over voiced spans (estimated) | ready |  |
| `SYNC-26` | إبراز تلقائي للكلمات المهمة | Automatic emphasis words | ready |  |
| `SYNC-31` | كاريوكي \k بشرائح متساوية | Even-slice \k karaoke (omni) | ready | python3, fonts:arabic |
| `SYNC-36` | كلمات على مقاطعها مع كلمات ذهبية | Syllable-timed speech captions with gold keywords | ready |  |
| `SYNC-48` | الريل التلقائي من الكلام | Automatic talking-clip reel | ready | pip:faster-whisper |
| `SYNC-56` | دمج المشاهد مع الصوت الأصلي بلا تعديل | Concat + untouched original audio mux | ready | ffmpeg, python3 |
| `SYNC-57` | غلاف الجهارة وقنوات الصوت للحركة | Loudness envelope & sound channels for motion | ready | python3 |
| `BEAT-28` | أرض من طيف الصوت | Spectrogram canyon ground | ready | python3 |
| `BEAT-29` | استخراج طاقة الترددات لكل إطار | Per-frame FFT band extraction | ready | ffmpeg, pip:numpy |
| `BEAT-30` | عناصر تتفاعل مع الصوت | Audio-reactive UI accents | ready | ffmpeg, pip:numpy, npm:gsap |
| `BEAT-31` | قائمة قطع تلقائية من المازورات وذروات الحركة | Auto edit list from bars and motion peaks | ready | ffmpeg, pip:numpy |
| `BEAT-32` | القص على حدود المازورة | Bar-grid cutting | ready |  |
| `BEAT-33` | مستويات علو المؤثرات | SFX loudness tiers | ready |  |
| `BEAT-34` | حلقات سلسة بالرندر الثلاثي | Seamless loops render-three-keep-middle | ready | pip:numpy |
| `BEAT-35` | تنفس الإيقاع مع الطبلة | Kick-pump duck | ready |  |
| `BEAT-36` | توهج متفاعل مع الصوت | Audio-reactive glow and scale | ready |  |
| `BEAT-37` | قص تريلر على البار | Beat-mapped trailer cuts | ready |  |
| `BEAT-38` | أعمدة الطيف الصوتي | Audio spectrum bars | ready | ffmpeg |
| `BEAT-39` | أهداف ارتفاع الصوت للموسيقى المولدة | Loudness mastering targets for generated music | ready | ffmpeg |
| `BEAT-40` | حلقة موسيقية سلسة على حدود الموازير | Bar-aligned seamless music loop | ready |  |
| `BEAT-41` | موجة أعمدة تتفاعل مع الميكروفون | Mic-reactive bar waveform (canvas) | ready |  |
| `BEAT-42` | مقياس مستوى الميكروفون | Mic level meter (AnalyserNode RMS) | ready |  |
| `BEAT-43` | صفارة تأكيد Web Audio | Web Audio confirmation beep | ready |  |
| `BEAT-44` | مسار إشارات المؤثرات | SFX cue track (cues only) | ready |  |
| `BEAT-45` | كوسف: توليد موسيقى ومحيط صوتي إجرائيا | KOSIF: procedural score and ambience synthesis | ready | pip:numpy |
| `BEAT-46` | مونتاج على الإيقاع | Beat-planned montage | ready | python3, imagemagick |
| `BEAT-47` | موسيقى مولدة على الإيقاع | score synthesised music on beat grid | ready | python3 |
| `BEAT-48` | أجواء صوتية مولدة | ambience synthesis | ready | python3 |
| `BEAT-49` | تحليل الإيقاع والقنوات | beats / channels analysis | ready | python3 |
| `BEAT-50` | مكتبة المؤثرات | SFX kit 20 CC0 cues | ready | python3 |
| `BEAT-51` | تحليل الصوت | Audio analysis | ready | python3 |
| `BEAT-52` | شبكة الإيقاع | Beat grid (beats) | ready | python3 |
| `BEAT-53` | قنوات الصوت كمحرك للحركة | Audio channels as animation drivers | ready | python3 |
| `BEAT-54` | مكتبة مؤثرات صوتية | CC0 UI sound-effects kit (20 sounds) | ready | python3 |
| `BEAT-55` | مواصفة موسيقى إجرائية على شبكة الإيقاع | Procedural score spec (beat-grid music) | ready |  |
| `BEAT-56` | ورقة مؤثرات صوتية متزامنة مع الصورة | SFX cue sheet synced to picture | ready |  |
| `BEAT-57` | قنوات تحليل الصوت لكل إطار | Per-frame audio analysis channels | ready |  |
| `BEAT-58` | ملفات صوت الخلفية والموسيقى | Ambient bed and score audio files | ready |  |
| `BEAT-59` | مقام minor | Score scale minor | ready | pip:numpy |
| `BEAT-60` | مقام major | Score scale major | ready | pip:numpy |
| `BEAT-61` | مقام dorian | Score scale dorian | ready | pip:numpy |
| `BEAT-62` | مقام hijaz | Score scale hijaz | ready | pip:numpy |
| `BEAT-63` | مقام pentatonic | Score scale pentatonic | ready | pip:numpy |
| `BEAT-64` | مقام lydian | Score scale lydian | ready | pip:numpy |
| `BEAT-65` | كشف الإيقاع | Beat grid detection | ready | pip:numpy |
| `BEAT-66` | مونتاج على الإيقاع | Beat-cut montage | ready | python3, imagemagick |
| `BEAT-67` | أجواء مولدة | Synth ambience | ready | pip:numpy |
| `BEAT-68` | موسيقى أصلية مولدة | Original score synth | ready | python3 |
| `BEAT-69` | ريل أغنية | Songreel lyric montage | ready | python3, imagemagick |
| `BEAT-70` | المراجعة: شبكة الإيقاع مع علامة الذروة | Review: beat grid with drop marker | ready |  |
| `BEAT-71` | المراجعة: تبديل الموسيقى ومستوى الصوت | Review: music swap and music/effects volume | ready |  |
| `BEAT-72` | تقدير الإيقاع BPM | Tempo (BPM) estimate from spectral flux | ready |  |
| `BEAT-73` | معايرة الصوت إلى -14 LUFS | Loudness master to -14 LUFS (loudnorm) | ready | ffmpeg |
| `BEAT-74` | ساعة الإيقاع للصورة | Beat clock for picture (MOTION.beats) | ready | python3 |
| `BEAT-75` | موسيقى مولدة على الإيقاع | Synthesised score on the beat grid | ready | pip:numpy |
| `BEAT-76` | أصوات أجواء مولدة | Synthesised ambience | ready | python3 |
| `BEAT-77` | ضبط علو الصوت للنشر | Broadcast loudness master | ready | ffmpeg, imagemagick |
| `BEAT-78` | خفض الموسيقى تحت الصوت | Voice-over sidechain ducking | ready | ffmpeg, imagemagick |
| `BEAT-79` | موسيقى تحت الكلام | Music bed under speech (static) | ready |  |
| `BEAT-80` | استخراج بيانات الصوت لكل إطار | Per-frame audio feature extraction | ready | ffmpeg, python3 |
| `BEAT-81` | قالب مرئي صوتي | Two-canvas audio visualiser template | ready | fonts:arabic |
| `BEAT-82` | قنوات الصوت كمحرّك | Sound channels as animation drivers | ready | python3 |
| `BEAT-83` | خلط صوت التركيب مع خفض الموسيقى تحت الصوت | Composition audio mux with voice ducking | ready | ffmpeg |
| `BEAT-84` | إعدادات خفض الموسيقى تحت الكلام | Sidechain ducking presets | ready | ffmpeg, imagemagick |
| `BEAT-85` | ترتيبات جاهزة | Default arrangements launch / calm | ready | python3 |
| `BEAT-86` | موسيقى خلفية أصلية تلقائية | Auto underscore when no bed | ready |  |
| `VOICE-04` | نطق المتصفح العربي ar-SA | Browser Web Speech fallback (ar-SA) | ready | chromium |
| `VOICE-25` | اختيار اللغة واللهجة في المقابلة | Language & dialect intake field | ready | pip:piper |
| `VOICE-49` | كرة الصوت بحالاتها | Voice orb state animation | ready |  |
| `VOICE-50` | نبض حلقة زر الميكروفون العائم | Live mic FAB ring pulse | ready |  |
| `VOICE-51` | التقاط ميكروفون نظيف | Clean mic capture constraints | ready |  |
| `VOICE-52` | تسجيل الصوت وتنزيله | MediaRecorder capture + download | ready | ffmpeg |
| `SYNC-08` | فخ نماذج .en | The .en model trap | documented | pip:faster-whisper, npm:hyperframes |
| `SYNC-12` | ضبط بداية الكلمة على النطق | Onset snapping of word stamps | documented | pip:faster-whisper |
| `SYNC-13` | تجهيز الصوت للتفريغ وفخ التوقيت | STT audio prep & its timing trap | documented | ffmpeg |
| `SYNC-16` | كشف الإعادات وتجميع المونتاج من النص | Retake detection & transcript-driven assembly | documented |  |
| `SYNC-19` | ميزانية الكلمات حسب الزمن | Narration word budgets | documented |  |
| `SYNC-21` | تجميع الكلمات حسب الطاقة | Word grouping by energy | documented | npm:remotion |
| `SYNC-22` | موضع آمن وضمان الاختفاء | Safe placement & exit guarantee | documented |  |
| `SYNC-23` | ستايل الترجمة حسب نبرة الكلام | Caption style by tone | documented |  |
| `SYNC-24` | وضوح الترجمة العربية | Arabic caption legibility | documented | fonts:arabic |
| `SYNC-25` | لا تغيّر كلام المتحدث، والحرق عند الطلب | Verbatim words; burn only when asked | documented |  |
| `SYNC-30` | معايرة حجم ASS | ASS PlayRes calibration | documented | ffmpeg, fonts:arabic |
| `SYNC-49` | إيقاع التلاوة والدعاء | Recitation & dua pacing | documented |  |
| `SYNC-50` | توقيت سطر الأغنية | Lyric line timing | documented |  |
| `SYNC-52` | لكل جملة منطوقة دليل بصري | One visual proof per spoken claim | documented |  |
| `SYNC-54` | إصلاح انزياح الصوت المدموج | Joined-audio drift fix | documented | ffmpeg |
| `SYNC-58` | مزامنة الفم بستة أشكال | Six-shape lip sync | documented | pip:piper |
| `SYNC-U01` | وسم مصدر التوقيت: عرض أم صوت أم تقديري | Timing provenance labels (display / voice / estimated) | documented | pip:faster-whisper |
| `SYNC-X01` | تحليل أغنية لفيلم كلمات | Song analysis for a lyric film (bands, kicks, word times) | documented |  |
| `SYNC-X02` | قفل موضع مقطع الترجمة | Caption chunk position lock | documented |  |
| `BEAT-213` | ربط الترددات بخصائص بصرية | Audio-to-visual property mapping | documented |  |
| `BEAT-214` | ترجمة تتفاعل مع الصوت | Audio-reactive captions at build time | documented |  |
| `BEAT-215` | مونتاج على شبكة الإيقاع | Beat-grid trailer edit | documented |  |
| `BEAT-216` | أطوال أصوات واجهة الاستخدام | UI sound feedback lengths | documented |  |
| `BEAT-217` | مقطع دعائي مقصوص على الإيقاع | Beat-grid trailer from a capture | documented | ffmpeg, pip:numpy, pip:librosa |
| `BEAT-218` | توجيه الموسيقى مقطعًا بمقطع | Section-by-section music direction | documented | ffmpeg |
| `BEAT-219` | مزامنة المؤثرات وترتيب المكساج | Sound design sync and mix order | documented | ffmpeg, pip:numpy |
| `BEAT-220` | جدول تحويل الإيقاع إلى إطارات | Tempo-to-frame grid table | documented | pip:numpy, pip:librosa |
| `BEAT-221` | ربط ضربات المونتاج بنبضات الموسيقى | Edit hits married to music transients | documented |  |
| `BEAT-222` | MG-028 توقيع صوتي موجز | MG-028 Sonic-logo pulses | documented | ffmpeg |
| `BEAT-223` | MG-091/099 نص على الضربات وتقطيع على الجملة الموسيقية | MG-091/099 Beat-locked words and phrase cuts | documented | ffmpeg, imagemagick, pip:librosa |
| `BEAT-224` | MG-094/098 مسار الكرة وخطوط السرعة | MG-094/098 Trajectory path and local speed lines | documented | ffmpeg |
| `BEAT-225` | MG-096 موجة صوت حول الغلاف | MG-096 Amplitude-reactive bars around cover art | documented | ffmpeg, npm:react |
| `BEAT-226` | جدول سرعات تناسب شبكة الإيقاع | Beat-grid friendly BPM table | documented |  |
| `BEAT-227` | عزل الصوت وتنظيفه | Audio isolation / voice cleanup | documented | ffmpeg, key:elevenlabs |
| `BEAT-228` | أدوار طبقات الصوت | Sound layer roles | documented | ffmpeg |
| `BEAT-229` | إيقاف الموسيقى وعودتها | Music stop/re-entry grammar | documented | ffmpeg |
| `BEAT-230` | خفض الموسيقى تحت الكلام | Speech-first ducking | documented | ffmpeg |
| `BEAT-231` | تجهيز الموسيقى قبل الميكس | Hero music premaster | documented | ffmpeg |
| `BEAT-232` | صوت كتابة تحت ظهور النص | Typing SFX under caption reveal | documented |  |
| `BEAT-233` | الموجة والطيف كعنصر بصري | Waveform/spectrum as a visual asset | documented | ffmpeg |
| `BEAT-234` | لوحات الأنواع الموسيقية | Genre palettes (BPM/swing/instrument) | documented |  |
| `BEAT-235` | ألحان أصلية فقط | Original melodies only | documented |  |
| `BEAT-236` | تشريح المؤثر بثلاث طبقات | SFX three-layer anatomy | documented | pip:numpy |
| `BEAT-237` | دلالات النغمة | Pitch/interval semantics | documented |  |
| `BEAT-238` | وضوح الصوت على سماعة الهاتف | Phone-speaker audibility | documented |  |
| `BEAT-239` | تنويع لتجنب الملل | Anti-fatigue variants | documented |  |
| `BEAT-240` | بداية المؤثر بلا تأخير | Zero-latency transient start | documented | ffmpeg |
| `BEAT-241` | ورقة توزيع أدوار الصوت | Sound-role cue sheet | documented |  |
| `BEAT-242` | ملء الصمت بنبرة الغرفة | Room tone fills | documented |  |
| `BEAT-243` | تعديل طول الموسيقى على الجمل | Edit music to length on phrases | documented |  |
| `BEAT-244` | خفض الموسيقى تحت الصوت | Ducking music under voice | documented | ffmpeg |
| `BEAT-245` | عرض ستيريو آمن للمونو | Mono-safe stereo width | documented | ffmpeg |
| `BEAT-246` | سلسلة ماسترينج | Music mastering chain | documented | ffmpeg, pip:numpy |
| `BEAT-247` | انحناء النغمة بتكامل الطور | Phase-integrated pitch bends | documented |  |
| `BEAT-248` | توحيد الجهارة للنشر | Publish loudness normalization | documented | ffmpeg |
| `BEAT-249` | كثافة المؤثرات | Sound design density | documented |  |
| `BEAT-250` | معادلة زمن النبضة | Beat interval formula | documented |  |
| `BEAT-251` | رايزر قبل القطع | Riser/whoosh before cut | documented |  |
| `BEAT-252` | ضربة على القطع | Impact/sub-drop on cut | documented |  |
| `BEAT-253` | مونتاج لقطات على إيقاع الموسيقى | Beat-cut montage to music | documented | python3, imagemagick |
| `BEAT-254` | موسيقى أصلية على شبكة الإيقاع | Original beat-grid score (WAV) | documented | python3 |
| `BEAT-255` | مؤثر صاعد قبل القطع وضربة عنده | Riser/whoosh before cut, impact on cut | documented |  |
| `BEAT-256` | سلسلة المكساج والماستر | Mix/master processing chain with numbers | documented | ffmpeg |
| `BEAT-257` | لوحة المقامات العربية | Arabic maqam palette | documented |  |
| `BEAT-258` | الإيقاعات العربية | Arabic rhythm (iqa') patterns | documented |  |
| `BEAT-259` | الآلات العربية | Arabic instrument palette | documented |  |
| `BEAT-260` | موجز الأغنية ومدد الإيقاع | Song brief spec + beat durations | documented |  |
| `BEAT-261` | أهداف الجهارة | Loudness targets per platform | documented | ffmpeg |
| `BEAT-262` | ducking حقيقي | Sidechain ducking | documented |  |
| `BEAT-263` | سلسلة ماسترينغ | Audio mastering chain | documented | ffmpeg, python3 |
| `BEAT-264` | ربط الحركة بالصوت | Audio-reactive mapping rules | documented |  |
| `BEAT-265` | القطع على الإيقاع | Beat-cut rules | documented |  |
| `BEAT-266` | قطع على الإيقاع | Beat/sentence cut points from BPM | documented |  |
| `BEAT-267` | قواعد صوت الإعلان | Ad audio rules | documented |  |
| `BEAT-268` | خفض الموسيقى تحت الصوت | Music ducking under voice | documented | ffmpeg |
| `BEAT-269` | تطبيع الجهارة -14 LUFS | Loudness normalisation -14 LUFS | documented | ffmpeg |
| `BEAT-270` | أصوات مفاتيح خافتة | Soft key-click SFX | documented |  |
| `BEAT-271` | مستوى صوت الرسم | Drawing SFX level | documented |  |
| `BEAT-272` | خريطة بنية المقطوعة | Song structure map | documented |  |
| `BEAT-273` | تأكيد الضربات القوية والضعيفة | Strong/weak beat accents | documented |  |
| `BEAT-274` | حساب طول الضربة | Beat period math | documented |  |
| `BEAT-275` | قيم متفاعلة منعّمة | Smoothed audio-reactive values | documented | ffmpeg, python3, npm:remotion |
| `BEAT-276` | وصفة التصاعد والذروة | Build and drop recipe | documented |  |
| `BEAT-277` | أعمدة المعادل | Equalizer bars | documented |  |
| `BEAT-278` | ترخيص الموسيقى | Music licensing rule | documented |  |
| `BEAT-279` | مستويات مؤثرات النقر والسحب | Tap/swipe SFX levels | documented |  |
| `BEAT-280` | تصميم صوت شحيح للواجهة | Sparse UI sound design | documented |  |
| `BEAT-281` | مكتبة مؤثرات Kenney | Kenney CC0 SFX library | documented |  |
| `BEAT-282` | إشارات الموسيقى الجاهزة | Music cue presets | documented |  |
| `BEAT-P01` | نقرات صوتية مولّدة على لحظات الحركة | Code-synthesised chirp ticks on motion events | documented | pip:numpy |
| `BEAT-U01` | لوحة مؤثرات بلا whoosh وفراش صوت اللقطات | Subtle SFX palette without whooshes | documented |  |
| `BEAT-X01` | أفضل نافذة موسيقية للفيلم | Best music window finder | documented | ffmpeg, python3 |
| `BEAT-X02` | لصق أزمنة السيناريو على الضربات | Snap scenario times to real hits | documented | python3 |
| `BEAT-X03` | تحقق الضربات على المزج النهائي | Verify picture hits on the final mix | documented | python3 |
| `BEAT-X04` | قص مقطع الموسيقى بلا نقرة | Click-free music cut with a shaped fade-out | documented | ffmpeg, python3, os:macos |
| `BEAT-X05` | القطعات هي الإيقاع | Cuts are the rhythm: synthesized launch-film score | documented | pip:numpy |
| `BEAT-X06` | ملخص الأغنية والخطاف أولًا | Song brief and hook-first writing | documented |  |
| `BEAT-X07` | بوابات اللهجة العربية في الأغاني | Arabic dialect gates for song lyrics | documented |  |
| `BEAT-X10` | تسليم الأغنية بأربع كتل ومعيار النجاح | Four-block song hand-off and PASS rubric | documented |  |
| `VOICE-02` | صوت ويندوز العربي (نايف) بالجدول الزمني | Windows OneCore Arabic narration (Naayf) | documented | python3 |
| `VOICE-05` | أصوات Edge العصبية والمولدات المبنية عليها | Edge neural voices & scene-file generators | documented | ffmpeg, python3, chromium, docker |
| `VOICE-17` | أوضاع مخرج الصوت الخارجي | KOSIF Voice Director provider modes | documented |  |
| `VOICE-18` | ميزانية الكلمات في الثانية | Words-per-second budget | documented | pip:piper |
| `VOICE-20` | نص النطق غير نص الشاشة | Spoken form vs on-screen form | documented |  |
| `VOICE-21` | قواعد كتابة التعليق للمشهد | Scene narration writing rules | documented |  |
| `VOICE-22` | سكربت تعليق بوسوم أداء SSML | VO script with performance tags (SSML) | documented | pip:piper, key:elevenlabs |
| `VOICE-23` | نص التعليق المقفل SCRIPT.md | Locked narration file (SCRIPT.md) | documented |  |
| `VOICE-24` | توجيه الصوت باللهجات العربية | Arabic dialect voice-direction workflow | documented |  |
| `VOICE-26` | شخصية اليوتيوبر المصري | Egyptian YouTuber voice persona | documented |  |
| `VOICE-29` | مواصفات تسجيل الصوت البشري | Human VO recording spec | documented |  |
| `VOICE-30` | مدرب اللغة الثنائي | Language Coach (AR/EN) skill | documented |  |
| `VOICE-33` | إعادة لصق النص المعروف على توقيت ويسبر | Re-attach the known script to Whisper timings | documented | pip:faster-whisper |
| `VOICE-40` | وصفات إصلاح الصوت بالأعراض | Voice repair presets by symptom | documented | ffmpeg, npm:hyperframes |
| `VOICE-45` | وصل المقاطع كـ WAV لا MP3 | Join chunks as PCM, not MP3 copy | documented |  |
| `VOICE-53` | لا تقليد لأصوات حقيقية | Never imitate real voices | documented |  |
| `VOICE-54` | لا ادعاء بلا ملف | No audio claim without a receipt | documented | ffmpeg |
| `VOICE-55` | نظافة تكلفة الحروف | TTS character-cost hygiene | documented |  |
| `SYNC-37` | سطر شبحي يضيء كلمة بكلمة | Ghost-to-lit line | seen |  |
| `SYNC-38` | صندوق ينتقل للكلمة النشطة | Word-hop highlight box | seen | npm:hyperframes |
| `SYNC-39` | ترجمة تُكتب لحظة النطق | Voice-timed typewriter captions | seen |  |
| `SYNC-40` | عداد كلمة مفتاحية ودائرة على الكلمة | Keyword counter & on-word annotations | seen |  |
| `SYNC-55` | ذروة المؤثر على الحدث | SFX peak-offset alignment | seen | pip:numpy |
| `BEAT-181` | قطع متزامن مع الإيقاع | Beat-locked cuts | seen |  |
| `BEAT-182` | صوت خربشة طباشير مولّد | Procedural chalk scratch sound | seen |  |
| `BEAT-183` | مونتاج كلمات خاطفة على الإيقاع | Flash-word beat montage | seen | imagemagick |
| `BEAT-184` | انفجار ذروة متزامن مع الموسيقى | Explosion climax on beat | seen |  |
| `BEAT-185` | قطع على شبكة الإيقاع | Beat-grid cuts | seen |  |
| `BEAT-186` | دفعة لقطات على الإيقاع مع شارة اسم الصانع | Beat-cut reel burst with handle chips | seen |  |
| `BEAT-187` | مخطط أعمدة يتزامن مع الإيقاع | Beat-synced bar chart | seen |  |
| `BEAT-188` | إطار HUD بعداد المقاطع ونصوص مشفرة تتفكك | Beat-bar HUD with scramble labels | seen |  |
| `BEAT-189` | مسار قفز مربوط بالإيقاع | Beat-mapped bounce path | seen |  |
| `BEAT-190` | حروف مفرغة تمتلئ مع موجة صوتية | Outline-to-fill letters with waveform | seen |  |
| `BEAT-191` | مونتاج إيقاعي | Beat montage | seen | imagemagick |
| `BEAT-192` | جدولة النغمات بمقذوفات عكسية | Inverse-ballistic note scheduling | seen |  |
| `BEAT-193` | كل ارتداد يعزف النغمة التالية | Bounce-to-note sonification | seen |  |
| `BEAT-194` | كشف كلمة مع موجة صوتية | Waveform word reveal | seen |  |
| `BEAT-195` | لحظة سواد قبل الذروة | Silence-before-drop black beat | seen |  |
| `BEAT-196` | قطعات حادة مضبوطة على الإيقاع | Beat-locked hard cuts | seen |  |
| `BEAT-197` | كلمة بين أعمدة موجة صوتية | Waveform-flanked word | seen |  |
| `BEAT-198` | موسيقى مولّدة بالكود ومقفلة على القطعات | Code-synthesized beat-locked soundtrack | seen | pip:numpy |
| `BEAT-199` | شيفرة تتوهج مع الإيقاع | Beat-highlighted code | seen |  |
| `BEAT-200` | بطاقة نتيجة تتبدل أسلوبها على إيقاع النوتات | Style-roll result card on 16th notes | seen |  |
| `BEAT-201` | واجهة عداد البارات الإيقاعية | Bar-counter HUD | seen |  |
| `BEAT-202` | قطع الفصول على المازورة | Bar-locked chapter cuts | seen |  |
| `BEAT-203` | شريط موجة الإيقاع | Beat waveform bar strip | seen |  |
| `BEAT-204` | قطع على الإيقاع | BPM beat cuts | seen |  |
| `BEAT-205` | عدّاد مازورة وضربة في الواجهة | Beat/bar HUD counter | seen |  |
| `BEAT-206` | خط زمني مقفل على الإيقاع | BPM beat grid timeline | seen |  |
| `BEAT-207` | كلمات تتبدل على الإيقاع | BPM beat-cut word flashes | seen |  |
| `BEAT-208` | أعمدة إيقاع تحت كلمة | Equaliser under word | seen |  |
| `BEAT-209` | شبكة تنبض مع الإيقاع | Beat grid pulse | seen |  |
| `BEAT-210` | قطع على إيقاع البار | BPM bar cut grid | seen |  |
| `BEAT-211` | قطع على شبكة الإيقاع | Beat-grid cutting | seen |  |
| `BEAT-212` | صوت ماركر مولد بالكود | Procedural marker squeak | seen |  |
| `VOICE-34` | إيقاع يقوده التعليق | Voice-led pacing | seen |  |
| `VOICE-35` | قراءة صوتية بتظليل الكلمة المنطوقة | Read-aloud karaoke highlight | seen |  |
| `VOICE-36` | ترجمة تُكتب على توقيت الصوت | Typewriter captions on voice word times | seen | key:elevenlabs |
| `VOICE-37` | موجة الصوت ومؤشر التشغيل | Voice waveform with playhead | seen | ffmpeg |
| `VOICE-38` | محاضرة مروية: رسم يتقدم مع الجمل | Narrated lecture: draw-on paced to sentences | seen |  |
| `SYNC-15` | تفريغ HyperFrames | HyperFrames transcribe CLI | install | pip:faster-whisper, npm:hyperframes, key:openai |
| `SYNC-35` | ترجمة Remotion بالكلمة مع كشف الاتجاه | Remotion word captions with bidi detection | install | npm:remotion |
| `SYNC-41` | مكوّنات ترجمة HyperFrames | HyperFrames caption components | install | npm:hyperframes |
| `SYNC-42` | ترجمة مدمجة: شريط وكلمة ذروة خلف المتحدث | Embedded captions: rail + peak word behind the subject | install | npm:hyperframes |
| `SYNC-43` | الأشرطة السفلية | Lower thirds | install | npm:hyperframes |
| `SYNC-44` | ستايلات وحركات ترجمة بصمة | Basma caption presets, animations & highlight modes | install | node, fonts:arabic |
| `SYNC-51` | ريل كلمات أغنية | Songreel lyric reel | install | yt-dlp, pip:faster-whisper, network |
| `BEAT-100` | تحسين الكلام التلقائي | Automatic speech enhancement chain | install |  |
| `BEAT-101` | بوابة ضوضاء بين الكلمات | Downward expander between words | install |  |
| `BEAT-102` | موجات الصوت | Audio visualiser (bars / circle) | install |  |
| `BEAT-103` | النبض مع الإيقاع | Beat-reactive pulse | install |  |
| `BEAT-104` | فيديو لملف صوت فقط | Audio-only clip visuals | install | npm:react |
| `BEAT-105` | أمر: استخراج الإيقاع | CLI: beats | install | npm:hyperframes |
| `BEAT-106` | أمر: تسوية الصوت | CLI: normalize-audio | install | npm:hyperframes |
| `BEAT-107` | سلسلة مؤثرات صوتية | Audio fx chain (WebAudio-style) | install |  |
| `BEAT-108` | أتمتة الصوت | Audio automation lanes | install |  |
| `BEAT-109` | مونتاج على الإيقاع | Music-to-video beat grid | install | npm:hyperframes |
| `BEAT-110` | لسعة الإيقاع | Beat Accent | install | chromium, npm:hyperframes |
| `BEAT-111` | خلفية نابضة على الإيقاع | Beat Pulse Background | install | npm:hyperframes |
| `BEAT-112` | تجميد على الإيقاع | Beat Freeze Cut | install | npm:gsap, npm:hyperframes |
| `BEAT-113` | موجة صوتية | Waveform | install | chromium, npm:hyperframes |
| `BEAT-114` | التلاشي وخفض الموسيقى عبر مسار الأتمتة | Volume fades and ducking via automation lane | install | npm:gsap |
| `BEAT-115` | مزامنة مؤثر صوتي مع حدث مرئي | Align a sound to an on-screen event | install |  |
| `BEAT-116` | مرئيات تتفاعل مع الصوت | Audio-reactive visuals from precomputed bands | install | python3, npm:gsap |
| `BEAT-117` | سلسلة المؤثرات الصوتية على المسار | Audio FX chain on any track (data-fx-chain) | install | chromium |
| `BEAT-118` | سجل معاملات المؤثرات | Effect parameter registry (ranges and defaults) | install |  |
| `BEAT-119` | نحت الموسيقى تحت التعليق الصوتي | Voiceover carve (spectral sidechain ducking) | install | npm:hyperframes |
| `BEAT-120` | حافلة المزج الفرعي | Submix bus <hf-audio-group> | install |  |
| `BEAT-121` | منحنيات الأتمتة للصوت والمؤثرات | Automation envelopes on volume or any effect param | install |  |
| `BEAT-122` | إعدادات الفضاء والصدى | Space / reverb presets | install |  |
| `BEAT-123` | ملفات المقبض الواحد للمؤثرات | One-knob effect profiles | install |  |
| `BEAT-124` | مفردات نطاقات التردد | Frequency band vocabulary | install |  |
| `BEAT-125` | شبكة الإيقاع لاستوديو | Studio beat grid (beats command) | install | python3, chromium, npm:hyperframes |
| `BEAT-126` | خفض تلقائي من بيانات الصوت | Auto-duck lane from audio_meta | install | node |
| `BEAT-127` | مكتبة المؤثرات الصوتية المرفقة | Bundled SFX library (19 files) | install |  |
| `BEAT-128` | فيديو متزامن مع إيقاع الموسيقى | Music-to-video beat-synced workflow | install | npm:hyperframes |
| `BEAT-129` | محلل شبكة الإيقاع | Beat-grid analyzer (audiomap.json) | install | pip:numpy, pip:librosa, pip:soundfile |
| `BEAT-130` | حركات إيقاعية موثقة فقط | Beat motion primitives without demo folders | install |  |
| `BEAT-131` | مساعدات مدة الإطار ومستوى الموسيقى | Pad frame duration and BGM volume helpers | install | node |
| `BEAT-132` | الصوت يحرك الصورة | Sound-driven picture | install | npm:three |
| `BEAT-133` | وادٍ من المخطط الطيفي | Spectrogram canyon (sound as terrain) | install |  |
| `BEAT-134` | ساعة شبكة إيقاع لفيلم كامل | Beat-grid clock for a whole film | install |  |
| `BEAT-135` | توقف الشريط ووقت الرصاصة ولمسات الخلل | Tape-stop bullet time and glitch accents | install |  |
| `BEAT-136` | مرئيات تتفاعل مع الصوت | Audio-reactive visuals (kick/bass mapping) | install |  |
| `BEAT-137` | خفض الموسيقى تحت الصوت | Sidechain auto-ducking | install |  |
| `BEAT-138` | ساعة الإيقاع | Beat clock MOTION.beats | install | python3 |
| `BEAT-139` | صوت محيطي مُركّب | Synth ambience fallback | install | python3 |
| `BEAT-140` | موسيقى أصلية | Original music score | install |  |
| `BEAT-141` | قنوات الصوت | Audio channels + tape-stop | install | python3 |
| `BEAT-142` | كاشف الإيقاع وسرعة BPM | Kick-band beat & BPM detector | install | ffmpeg, python3 |
| `BEAT-143` | خفض الموسيقى تحت الصوت | Music ducking under voice (spec vs code) | install | ffmpeg |
| `BEAT-144` | موسيقى حجاز مركّبة بلا عينات | Hijaz synth soundtrack (numpy/scipy, no samples) | install | pip:numpy, pip:scipy, npm:d3, fonts:arabic |
| `BEAT-145` | سلسلة ماسترنج ذاتية | Self-mastering chain (reverb, shelf, loudness, true-peak guard) | install |  |
| `BEAT-146` | تنفس الهالة على ضربات الإيقاع | Downbeat-synced halo breathing | install |  |
| `BEAT-147` | قنوات الصوت لكل إطار | Audio channels JSON (per-frame features) | install | python3 |
| `BEAT-148` | مواصفة موسيقى خلفية للكلام | Talking-voice score spec (90 BPM D minor) | install | pip:numpy |
| `BEAT-149` | قائمة مؤثرات صوتية مصممة | Designed SFX cue sheet | install | python3 |
| `BEAT-150` | شبكة الإيقاع | Beat grid helper | install |  |
| `BEAT-151` | نقاط قطع على الإيقاع | Beat/onset cut points | install | ffmpeg, pip:numpy |
| `BEAT-152` | مستويات الصوت | Loudness targets | install | ffmpeg |
| `BEAT-153` | طيف على ساعة الشريط | Spectrum on tape clock | install |  |
| `BEAT-154` | هالة وجسيمات تتفاعل مع الصوت | Sound-reactive halo, motes and kick rings | install |  |
| `BEAT-155` | فيلم يستمع بالرياضيات | Listen-with-math music film | install | python3 |
| `BEAT-156` | موجة صوت | Style: Audio wave (audio-wave) | install | ffmpeg, python3, npm:remotion |
| `BEAT-157` | موسيقى | Category: Music | install | python3, npm:remotion |
| `BEAT-158` | خفض الموسيقى والجهارة | Music ducking and loudness | install | ffmpeg, python3 |
| `BEAT-159` | كشف الإيقاع بالقياس | Measured beat detection | install | pip:librosa |
| `BEAT-160` | غلاف التأكيد | Accent envelope / BeatPulse | install | npm:remotion |
| `BEAT-87` | أعمدة طيف وموجة صوتية في ريموشن | Remotion spectrum bars & waveform | install | npm:remotion |
| `BEAT-88` | موسيقى إجرائية بملف JSON | Procedural music score in JSON | install | ffmpeg, pip:numpy |
| `BEAT-89` | مكتبة توليف بايثون | Python synthesis toolkit (numpy/scipy) | install | pip:numpy, pip:scipy, pip:soundfile |
| `BEAT-90` | كتابة اللحن بالخطوات | Step-notation melody writing | install |  |
| `BEAT-91` | توافق المؤثرات النغمية مع المقام | Tonal SFX key check | install |  |
| `BEAT-92` | تتبع الإيقاع في المتصفح | Browser beat tracker (spectral flux + autocorrelation) | install |  |
| `BEAT-93` | نمط مونتاج سريع سريع نَفَس | Editor's beat pattern (hook-quick-quick-breathe) | install |  |
| `BEAT-94` | توطية الموسيقى وقت الكلام | Music ducking under speech | install | imagemagick |
| `BEAT-95` | مكتبة المؤثرات الصوتية المولدة | Synthesised SFX library (16) | install |  |
| `BEAT-96` | تركيب طبقة المؤثرات | SFX stem compositor | install |  |
| `BEAT-97` | مؤلف موسيقى خلفية محلي | Procedural music bed composer | install |  |
| `BEAT-98` | توزيع المؤثرات على كلمات الفيلم | Film SFX auto-placement | install |  |
| `BEAT-99` | مؤثرات المونتاج على القطعات | Montage SFX rules | install | imagemagick |
| `VOICE-03` | Kokoro المحلي (بلا عربية) | Kokoro local TTS (no Arabic voice) | install | pip:kokoro, pip:soundfile, npm:hyperframes, network |
| `SYNC-14` | تفريغ سحابي مع فصل المتحدثين | Cloud STT with diarisation | key | pip:faster-whisper, key:elevenlabs, key:unspecified, pip:pyannote |
| `BEAT-161` | توليد مؤثرات صوتية من وصف نصي | Text-to-sound-effects generation | key | key:elevenlabs |
| `BEAT-162` | مكتبة مؤثرات صوتية | SFX library by URL | key | npm:remotion, key:unspecified |
| `BEAT-163` | توليد مؤثرات صوتية من نص | Text-to-SFX generation | key | pip:numpy, key:elevenlabs |
| `BEAT-164` | خطة تأليف موسيقى ElevenLabs | ElevenLabs Music composition plan | key | key:elevenlabs |
| `BEAT-165` | الكلمات داخل أقسام الخطة فقط | Lyrics only via plan sections | key | key:unspecified |
| `BEAT-166` | برومبت الأسلوب السداسي في Suno | Suno six-layer style prompt | key | key:video-gen |
| `BEAT-167` | تجاوز الأسلوب لكل مقطع في Suno | Suno per-section style overrides | key | key:video-gen |
| `BEAT-168` | تصنيف وسوم Suno والتلميحات المضمنة | Suno tag taxonomy and inline cues | key | key:video-gen |
| `BEAT-169` | حيل الأداء الصوتي في Suno | Suno vocal performance tricks | key | key:video-gen |
| `BEAT-170` | أخطاء Suno الشائعة وحلولها | Suno anti-patterns and fixes | key | key:video-gen |
| `BEAT-171` | تحرير Suno: الغلاف والتمديد واستبدال المقطع | Suno editing: Cover, Extend, Replace Section, Personas | key | key:video-gen |
| `BEAT-172` | تقسيم Suno إلى مسارات وملفات بإيقاع مقفل | Suno stems, tempo-locked WAV and MIDI for editing | key | key:video-gen |
| `BEAT-173` | اللغة والأنماط العربية في Suno | Suno language and Arabic-flavoured genres | key | key:video-gen |
| `BEAT-174` | قوالب الأنماط الموسيقية في Suno | Suno genre templates | key | key:video-gen |
| `BEAT-175` | خطة تأليف ElevenLabs بالموازير | ElevenLabs Music composition plan in whole bars | key | key:elevenlabs |
| `BEAT-176` | عزل الحوار بالذكاء الاصطناعي قبل المونتاج | AI dialogue isolation before editing | key | key:elevenlabs |
| `BEAT-177` | تنظيف الصوت محلياً | Local voice cleaning via bridge (audiolab.py) | key | python3, key:unspecified |
| `BEAT-178` | حزمة أغنية لـ Suno/Udio | Suno/Udio song package | key | key:video-gen |
| `BEAT-179` | جدول تصميم المؤثرات الصوتية | SFX design sheet | key | key:elevenlabs |
| `BEAT-180` | حزمة الأطلس للصوت والقصة | Atlas skill pack: audio/voice/story skills | key | npm:hyperframes, key:elevenlabs |
| `BEAT-X08` | حقل الأسلوب والاستبعاد في Suno | Suno Style field order and Exclude rules | key | key:video-gen |
| `BEAT-X09` | خريطة الإصلاح الجراحي للأغنية | Surgical song iteration map | key | key:video-gen |
| `VOICE-06` | تعليق ElevenLabs بإعدادات جاهزة | ElevenLabs narration presets | key | npm:remotion, key:elevenlabs |
| `VOICE-07` | اختيار النموذج والصيغة حسب الاستخدام | Model & output-format choice | key | key:elevenlabs |
| `VOICE-08` | تقسيم النص الطويل مع حفظ النبرة | Long-script chunking with prosody context | key | key:unspecified |
| `VOICE-09` | استنساخ صوت بموافقة صاحبه | Consented voice cloning | key | node, key:elevenlabs |
| `VOICE-10` | تحويل صوت إلى صوت | Speech-to-speech re-voice | key | key:unspecified |
| `VOICE-11` | Gemini TTS بثلاثين صوتًا | Gemini TTS with 30 prebuilt voices | key | key:unspecified |
| `VOICE-12` | إخراج أداء الصوت بواسطة Claude | Claude-directed voice performance | key | pip:piper, fonts:arabic, key:unspecified |
| `VOICE-13` | حوار بأكثر من متكلم | Multi-speaker dialogue production | key | imagemagick, key:unspecified |
| `VOICE-14` | HeyGen Starfish بطوابع زمنية للكلمات | HeyGen Starfish TTS with word timestamps | key | node, pip:kokoro, key:elevenlabs |
| `VOICE-15` | محرك الصوت الموحد audio_meta.json | Unified audio engine (voice + words + BGM + SFX) | key | npm:hyperframes, key:unspecified |
| `VOICE-16` | كتالوج Together للصوت | Together AI TTS catalog | key | pip:kokoro, key:unspecified |
| `VOICE-46` | محادثة صوتية عربية لحظية عبر WebRTC | Realtime Arabic speech-to-speech (WebRTC) | key | key:openai |
| `VOICE-47` | مقاطعة المساعد بالكلام | Barge-in interruption | key | key:unspecified |
| `BEAT-283` | أوديوجرام للبودكاست | Podcast audiogram | idea | ffmpeg, pip:faster-whisper, npm:gsap, npm:remotion |
| `BEAT-284` | مؤثرات صوتية مولدة | Synthesized Web Audio SFX on frame clock | idea |  |
| `BEAT-285` | مؤثر واحد لكل عنصر | One soft SFX per element | idea |  |
| `BEAT-286` | شبكة 110 نبضة | 110 BPM beat grid derivation | idea |  |
| `BEAT-287` | كشف الإيقاع | BPM-detect beat grid | idea | pip:librosa |
| `BEAT-288` | ضربات على النبض | Beat-locked punch-ins | idea |  |
| `BEAT-289` | موسيقى مع خفض | Arc-scored music with typing duck | idea |  |
| `BEAT-290` | قطع على الصوت | Sound-first cuts with held silence | idea |  |
| `BEAT-291` | نغمة متصاعدة | Rising pitch per pass | idea |  |
| `BEAT-292` | تفاعل على الإيقاع | Frame-accurate beat reactions | idea |  |
| `BEAT-293` | نبض على الكيك | Kick pulse exponential decay | idea |  |
| `BEAT-294` | أصوات مولدة | Event-synthesized UI tones | idea |  |
