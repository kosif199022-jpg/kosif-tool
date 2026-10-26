# دورة المياه — الفيلم السينمائي ثلاثي الأبعاد (17 ثانية، 1920×1080، 30 fps)

مشهد Three.js كامل مُفتاح إلى الزمن: شروق أمام العدسة فوق بحر عاكس، تضاريس بظلال، بخار يصعد من الخليج، سحب حجمية
تتشكّل وتغمق، مطر وبرق فوق القمم، نهر يمتد في الوادي إلى البحر، ولقطة ختامية واسعة. النص العربي طبقة HTML فوق
اللوحة بأقنعة الكلمات. الصوت من `ambience.py`.

```bash
cd ../..                           # scripts/
npm install                         # hyperframes + gsap + three + esbuild (مرة واحدة)
python motion.py sync examples/water_cycle_3d
python motion.py bundle examples/water_cycle_3d                     # src/main.js → assets/main.bundle.js
python ambience.py examples/water_cycle_3d/assets/ambience.wav --seconds 17 --rain 9.7:13.2 --thunder 10.6 --whoosh 0.5,15.6 --chords 0:A,6.5:F,12.8:C --seed 11
python motion.py frames examples/water_cycle_3d --times 0.8,4.5,8,10.9,13.6,16.5   # بوابة الإطارات
python motion.py render examples/water_cycle_3d --engine studio --out out/water_cycle_3d.mp4   # على GPU الجهاز، مع الصوت
```

لوحة الإطارات في `../../../assets/water-cycle-3d-frames.png`. المسار الثلاثي الأبعاد يُصيَّر بمحرّك الاستوديو
(يحتاج scripts/ المهارة 109 بجواره أو `html_render.py` في المجلد الأب).
