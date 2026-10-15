# TEST_REPORT.md — {style_name}

> الاستايل: `{id}` · الهدف: {aspect} · {resolution} · {fps} fps · {duration} s · {frames} إطار · تاريخ الإنشاء: {date}
> Style: `{id}` · Target: {aspect} · {resolution} · {fps} fps · {duration} s · {frames} frames · Created: {date}

يُعبَّأ هذا التقرير بقيم **مقاسة** بالأوامر في القسم 3، لا بقيم مفترضة. أي سطر فيه FAIL يمنع التسليم حتى يُصلَّح أو يوافق المستخدم صراحةً على الاستثناء.
This report is filled with values **measured** by the commands in section 3, never assumed. Any FAIL blocks delivery until fixed or explicitly waived by the user.

## 1. الملف المُسلَّم / Delivered file

| البند / Item | القيمة / Value |
|---|---|
| المسار / Path | |
| الحجم / Size (MB) | |
| الحاوية / Container | MP4 |
| فيديو / Video codec | H.264 (yuv420p) |
| صوت / Audio codec | AAC |
| المصدر القابل للتعديل / Editable source | |
| المعاينة المعتمدة / Approved preview | |

## 2. الفحوص / Checks

| # | الفحص / Check | المستهدف / Target | المقاس / Measured | النتيجة / Result (PASS / FAIL) |
|---|---|---|---|---|
| 1 | المدة / Duration | {duration} s (± 0.1 s) | | |
| 2 | معدل الإطارات / Frame rate | {fps} fps ثابت / constant | | |
| 3 | عدد الإطارات / Frame count | {frames} | | |
| 4 | الدقة / Resolution | {resolution} ({aspect}) | | |
| 5 | وجود مسار صوت / Audio track present | AAC · 48 kHz · stereo | | |
| 6 | الصوت الأصلي دون تعديل / Supplied voice untouched | نفس المدة والتوقيت / same length and timing | | |
| 7 | مستوى الصوت / Loudness | -14 LUFS (± 1 LU) · true peak ≤ -1 dBTP | | |
| 8 | المقروئية على الهاتف / Legibility at phone size | أصغر نص ≥ 36 px عند عرض 1080 · مقروء بعرض 360 px / smallest text ≥ 36 px at 1080 width · readable at 360 px | | |
| 9 | تشكيل العربية / RTL shaping | حروف متصلة · اتجاه صحيح · ترقيم غير معكوس / joined letters · correct direction · punctuation not mirrored | | |
| 10 | تزامن الكلمات المفتاحية / Sync tolerance on key words | ≤ 100 ms (كل كلمة بـ emphasis) / (every emphasis word) | | |
| 11 | حركة في كل مشهد / Motion in every scene | لا شرائح ثابتة / no static slides | | |
| 12 | الهوامش الآمنة / Safe margins | 5% جانبيًا · 12% أعلى وأسفل في 9:16 / 5% sides · 12% top and bottom in 9:16 | | |
| 13 | التباين / Contrast | ≥ 4.5:1 للنص / for text | | |
| 14 | الإطار الأول والأخير / First and last frame | لا إطار أسود أو فارغ غير مقصود / no unintended black or empty frame | | |
| 15 | الأصول / Assets | أصلية أو مرخّصة · لا ميديا منسوخة من المرجع / original or licensed · no media copied from the reference | | |
| 16 | المعاينة قبل الرندر / Preview before final render | وافق المستخدم / user approved | | |

## 3. أوامر القياس / Measurement commands

```sh
# المدة / duration
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 final.mp4

# الفيديو: الترميز، الدقة، معدل الإطارات، عدد الإطارات / video: codec, size, frame rate, frame count
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames,pix_fmt -of default=nw=1 final.mp4

# الصوت: الترميز، التردد، القنوات / audio: codec, sample rate, channels
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels -of default=nw=1 final.mp4

# مستوى الصوت المتكامل والذروة الحقيقية / integrated loudness and true peak
ffmpeg -hide_banner -i final.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=summary -f null -

# لوحة إطارات للمراجعة البصرية (المقروئية، التشكيل، الهوامش) / contact sheet for visual review
ffmpeg -hide_banner -i final.mp4 -vf "fps=1,scale=360:-1,tile=4x4" -frames:v 1 contact_sheet.png

# تزامن الكلمات: قارن بداية كل كلمة مفتاحية في words.json بإطار ظهور حركتها / sync: compare each emphasis word start with its motion frame
# offset_ms = |word.start - motion_frame / {fps}| * 1000  → must be ≤ 100
```

## 4. مشاكل مفتوحة / Open issues

| # | الوصف / Description | الخطورة / Severity | الإجراء / Action |
|---|---|---|---|
| | | | |

## 5. الخلاصة / Verdict

- [ ] جاهز للتسليم / Ready to deliver
- [ ] يحتاج إصلاحًا / Needs fixes (see section 4)

الموقّع / Signed: ______ · التاريخ / Date: {date}
