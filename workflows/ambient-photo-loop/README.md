# صورة ثابتة ← فيديو بحركة هادية (Ambient photo loop)

بيحوّل صورة واحدة لفيديو طويل من غير صوت (مثلًا 4 دقايق) عشان تحطه في برنامج المونتاج وتضيف عليه صوت. الصورة نفسها مبتتغيرش: الشخص بيتلقط بموديل تقسيم بشري (`rembg` / `u2net_human_seg`) وبيتنسخ من الصورة الأصلية في كل فريم زي ما هو. الحركة بس في:

- **السما:** السحاب بيزحف ببطء، واللي فوق أسرع من اللي تحت.
- **المية:** تموج خفيف ولمعة على الانعكاسات.
- **الأعلام:** رفرفة بسيطة بتبدأ من صفر عند العمود.
- **الضوء:** شريط ضوء دافي بيعدي بالراحة على الخلفية، والشمس بتتوهج وتهدى.

كل الحركات دورية بطول اللوب (`loop_seconds`)، فالفيديو بيلف من غير ما يبان مكان اللف، والفيديو النهائي هو اللوب متكرر بـ `ffmpeg concat -c copy`.

## المحتويات

| الملف | ما فيه |
|---|---|
| `config.json` | المقاس والـfps وطول اللوب والمدة، وأماكن السما والمية والأعلام والشمس بإحداثيات الصورة الأصلية، وقوة كل حركة |
| `scripts/ambient_loop.py` | الأداة: `masks` · `test` · `render` · `verify` · `all` |
| `TEST_REPORT.md` | قياس أول تشغيل فعلي |

## التشغيل

```bash
pip install opencv-python-headless rembg onnxruntime numpy pillow   # + ffmpeg
python3 workflows/ambient-photo-loop/scripts/ambient_loop.py masks  --image photo.png --config workflows/ambient-photo-loop/config.json --out out/ambient
# افتح out/ambient/mask_overlay.jpg: أحمر = سما، أزرق = مية، أخضر = الشخص المحمي
python3 workflows/ambient-photo-loop/scripts/ambient_loop.py test   --config workflows/ambient-photo-loop/config.json --out out/ambient
python3 workflows/ambient-photo-loop/scripts/ambient_loop.py render --config workflows/ambient-photo-loop/config.json --out out/ambient
python3 workflows/ambient-photo-loop/scripts/ambient_loop.py verify --config workflows/ambient-photo-loop/config.json --out out/ambient
```

النتيجة `out/ambient/final.mp4` (H.264، yuv420p، من غير صوت). الرندر بياخد حوالي 9 دقايق للوب 24 ثانية على 4 أنوية، والتكرار لـ4 دقايق ثواني.

## صورة جديدة

الإحداثيات في `config.json` معمولة لصورة 941×1672 (الراجل اللي بيأدي التحية قدام النيل والأهرامات). لصورة تانية عدّل:

1. `sky_skyline`: خط الأفق من الشمال لليمين؛ كل اللي فوقه سما.
2. `sky_exclude_boxes`: مستطيلات تتشال من السما (أعمدة الأعلام مثلًا) `[x0,y0,x1,y1]`.
3. `water_polygon`: مضلع المية، وبيتقاطع مع البكسلات الفاتحة (`water_min_brightness`).
4. `flags`: مستطيل كل علم و`pole_x` مكان العمود. ممكن تسيبها فاضية.
5. `sun`: مكان الشمس للتوهج.

بعدها شغّل `masks` واتأكد من `mask_overlay.jpg` قبل الرندر.

## حدود

- الصورة الأصلية والفيديو مش في الريبو (`*.mp4` متجاهل، والصورة شخصية). السجل بيحفظ البصمة بس.
- الحركة warp وتلاشي على بكسلات الصورة نفسها، مش توليد بالذكاء الاصطناعي، فمفيش تفاصيل جديدة بتتخترع.
