# دورة المياه — المثال المرجعي (17 ثانية، 1920×1080، 30 fps)

خمسة مشاهد على خط GSAP واحد: الفجر وطلوع الشمس والعنوان، التبخّر (بخار يصعد من البحر وسهمان يُرسمان)، التكاثف (سحب
تهبط بـ snap ثم تسافر وتغمق)، الهطول (دفعة كاميرا إلى القمة، مطر مبذور، برق، ثلج)، الجريان والتسرّب (نهر يُرسم إلى
البحر وأسهم جوفية)، ثم حلقة ذهبية تجمع المراحل الأربع. الصوت محيط مركّب بـ numpy مُفتاح إلى الثواني نفسها.

لتشغيله:

```bash
cd ../..                          # scripts/
npm install                        # hyperframes + gsap (مرة واحدة)
python motion.py sync examples/water_cycle                                   # ينسخ gsap.min.js والعدّة إلى assets/
python ambience.py examples/water_cycle/assets/ambience.wav --seconds 17 --rain 9.6:12.9 --thunder 10.6 --whoosh 0.6,15.25 --chords 0:A,6.2:F,12.6:C
python motion.py check examples/water_cycle                                  # صفر ✗
python motion.py render examples/water_cycle --out out/water_cycle.mp4
```

لوحة الإطارات المفتاحية في `../../../assets/water-cycle-frames.png`.
