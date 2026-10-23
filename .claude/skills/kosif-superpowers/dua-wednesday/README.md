# دعاء يوم الأربعاء — Wednesday-morning dua reel

ريل دعاء عمودي 9:16 بأسلوب موشن جرافيك كامل: كل عبارة دعاء على لقطة مختارة بانتقال مختلف، والنص يظهر كلمة كلمة مع
الصوت بخطوط عربية ذهبية، تحت محراب ذهبي يعلوه هلال. الصوت الأصلي لا يُمس.

A vertical 9:16 dua reel in full motion graphics: one phrase per chosen shot with a different transition each cut,
word-by-word Arabic text timed to the voice in gold calligraphic fonts, under a gold mihrab crowned by a crescent.
The original voice is stream-copied untouched.

| | |
|---|---|
| المحرك / engine | `scripts/dua_wednesday.py` (+ `dua-wednesday/sprites.cjs` للنصوص في Chromium) |
| سير العمل الكامل / full workflow | [WORKFLOW.md](WORKFLOW.md) — اقرأه قبل أي ريل جديد بهذا الأسلوب |
| المشروع المرجعي / reference project | [project.example.json](project.example.json) — ريل الأربعاء 21.10.2026 بالقيم المعتمدة |
| الخطوط / fonts | `fonts/` (Gulzar, Rakkas, El Messiri — SIL OFL 1.1) + Aref Ruqaa من `proofs/_shared/fonts/` |
| الاختبار / test | `evals/test_dua_wednesday.py` |

## الاستعمال السريع / quick use

```bash
python3 scripts/dua_wednesday.py fetch "<رابط الفيديو>" --job JOB
python3 scripts/dua_wednesday.py asr --job JOB
python3 scripts/dua_wednesday.py init --job JOB          # ثم عدّل project.json
python3 scripts/dua_wednesday.py prep --job JOB clip1.mp4 clip2.mp4:556 ...
python3 scripts/dua_wednesday.py sprites --job JOB
python3 scripts/dua_wednesday.py stills --job JOB --t 1.6,5.4,20
python3 scripts/dua_wednesday.py render --job JOB
```

Needs ffmpeg, Python with numpy + opencv-python-headless, Node with Playwright (Chromium); faster-whisper for `asr`,
yt-dlp for `fetch`. `doctor` lists what is missing.
