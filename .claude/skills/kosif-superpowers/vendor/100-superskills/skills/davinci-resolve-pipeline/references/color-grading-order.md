# ترتيب التلوين وقياسه (خلاصة akbun-davinciresolve-workflow + mas-video-lab/davinci-resolve + ثلاثة دروس عملية)

## المبدأ
تصحيح تقني أولاً في عقد مسمّاة، ثم لوك إبداعي في عقدة منفصلة فقط عند الطلب. لا تخلط «يبدو جميلاً» مع «صحيح تقنياً».

## ترتيب العقد (مسار LUT واحد Log→Rec.709)
| # | العقدة | ماذا | أين تُقاس |
|---|---|---|---|
| 1 | `EXPOSURE` | Offset في فضاء Log | على مخرج LUT (Waveform) |
| 2 | `WB` | Offset قنوات R/G/B في Log | Vectorscope + بكسل محايد حقيقي |
| 3 | `CST` | LUT تحويل الكاميرا (Apple Log، I-Log، S-Log3…) | يُطبَّق أولاً زمنياً لأن القياس بعده |
| 4 | `CONTRAST` | Contrast/Pivot بعد التحويل | Waveform: لا قصّ |
| 5 | `SAT` | تشبّع معتدل (سقف ≈ 1.25) مع rolloff للظلال والإضاءات | Vectorscope |
| 6 | `LOOK` (اختياري) | الدفء/البرودة، split-tone، حبيبات | عقدة Serial جديدة بعد التصحيح |

**ترتيب التنفيذ** يختلف عن ترتيب الإشارة: طبّق CST أولاً، ثم قِس وعدّل EXPOSURE وWB (تقعان قبله في السلسلة لكن تُقاسان على مخرجه)، ثم CONTRAST وSAT.
**المقاطع غير Log** بلا CST وبقية العقد كما هي.

## مسار DWG/Intermediate (يدوي)
Input CST → HDR Global Exposure → HDR Global WB → Contrast/Pivot → Color Slice للتشبّع → تصحيحات انتقائية → Output CST → LOOK/LUT إبداعي. القيم مثل Contrast 1.3 وPivot 0.336 أمثلة لمدخل DaVinci Intermediate فقط، لا قيماً ثابتة. تأكد من 3D LUT interpolation = Tetrahedral لتقليل الـ banding عند LUT منخفض العمق.

## القياس لا الانطباع
- API بلا Scopes: `Timeline.SetCurrentTimecode(منتصف المقطع)` ثم `Project.ExportCurrentFrameAsStill(path)` واحسب هيستوغرام الإضاءة والقنوات بـ Pillow. الهدف حسب الوقت من اليوم (الليل مظلم؛ «context is important»).
- توازن الأبيض: عيّنة محايدة حقيقية فقط (لا أسطح تعكس ضوءاً ملوّناً)؛ فرق القنوات بعد التصحيح ≤ 20/255.
- بين لقطتين متجاورتين: فرق قيم Scopes tail→head ضمن عتبة الإرهاق البصري؛ وإلا علامة `EXPOSURE_CHECK`/`WB_CHECK`.
- هواتف وكاميرات 360 مشبّعة ومتباينة أصلاً: تصحيح أخف.

## ما تملكه الواجهة وما لا تملكه
| العملية | API | البديل |
|---|---|---|
| تكرار خط زمني | `Timeline.DuplicateTimeline(name)` (19+) | UI |
| إضافة/تسمية عقدة | **لا** | Color → Nodes → Append a Node → Label Selected Node (لكل مقطع؛ Alt+S لا يعمم) |
| CDL (Slope/Offset/Power/Sat) | `TimelineItem.SetCDL({NodeIndex,…})` | — (لا قراءة؛ استخدم فقط على عقدك) |
| LUT | `TimelineItem.SetLUT(nodeIndex, path)` | — |
| تعطيل عقدة للمقارنة | `GetNodeGraph().SetNodeEnabled(idx, False)` + Still | — |
| نسخ تدرّج | `TimelineItem.CopyGrades(targets)` (19+) أو `ApplyGradeFromDRX` | — |
| درجة حرارة/Tint | **لا** | UI |
| تثبيت | `TimelineItem.Stabilize()` بقيم Inspector الحالية | المعاملات UI |
| نقل/قصّ مقاطع | **لا** | `CreateTimelineFromClips` بـ startFrame/endFrame أو UI |
| علامات | `Timeline.AddMarker(frame, color, name, note, dur)` / `TimelineItem.AddMarker` | 16 لوناً فقط |
| Text+ | `AppendToTimeline` لقالب من Media Pool ثم `GetFusionCompByIndex(1)`؛ **لا** `InsertFusionTitleIntoTimeline` (يقطع V1 ويزيح كل شيء) | — |
| Loudness | **لا** | Fairlight meter أو `ffmpeg -af ebur128` على الرندر |
| رندر | `SetCurrentRenderFormatAndCodec`, `SetRenderSettings`, `AddRenderJob`, `StartRendering`, `GetRenderJobStatus` | ffprobe للتحقق |

## سجل العلامات
| اللون | الاسم | الهدف |
|---|---|---|
| Blue | `CHAPTER <اسم>` | خط زمني، بداية المشهد؛ الأولى عند الإطار 0 |
| Purple / Pink | `PRIVACY_MOSAIC` / `PRIVACY_CHECK` | مقطع |
| Red / Yellow | `CUT_DONE` / `CUT_REVIEW` | مقطع |
| Lemon / Sky | `EXPOSURE_CHECK` / `WB_CHECK` | مقطع |
| Sand | `AUDIO_REVIEW <cue>` | خط زمني |
| Cyan | `GFX <نوع>` | خط زمني |
إطار واحد = علامة واحدة؛ الإزاحات (+0..+6) تمنع التصادم.

## التحقق قبل الرندر (كلها أو لا رندر)
الدقة والمعدل = إعدادات الخط الزمني · لا وسائط offline ولا إطارات سوداء · قمة ≤ −1 dBTP وفروق المشاهد ≤ 6 dB · لا قفزات إضاءة/لون بين القطع · كل وجه مُموّه أو معلَّم · الترجمة داخل المنطقة الآمنة · ملف الرندر يعمل ومدته ضمن إطار واحد.
