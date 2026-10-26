# تثبيت «100 مهارة خارقة»

## Claude Code (كل شيء يعمل: المهارات + السكربتات)
```text
/plugin marketplace add kosif199022-jpg/100-superskills
/plugin install 100-superskills@superskills
```
تجربة بلا تثبيت دائم:
```text
claude --plugin-dir "PATH/TO/100-superskills"
```
بعدها اكتب طلبك بالعربية مباشرة («اعمل لي انميشن 10 ثوانٍ عن…»، «اكتب برومبت احترافي لـ…») وسيلتقط كلاود المهارة من وصفها،
أو اطلبها بالاسم: `/100-superskills:claude-animation-studio`.

### ما تحتاجه السكربتات
- Python 3.10+ (موجود عندك 3.13).
- للأنيميشن: `pip install playwright` ثم `python -m playwright install chromium` (أو استخدم Edge المثبت: السكربت يجرّبه أولاً)، وffmpeg في PATH (موجود عندك 9.0).
- للإكسل: `pip install openpyxl`.
- لاستوديو الرسم (109): `pip install pillow numpy opencv-python arabic-reshaper python-bidi` (وmatplotlib لكود matplotlib فقط).
- لباقي السكربتات: المكتبة القياسية فقط.

## Claude Desktop و claude.ai
Settings → Capabilities → Skills → ارفع ما تحتاجه من `dist/claude-ai-skills/<slug>.zip` (كل ملف مهارة واحدة).
ابدأ بـ `claude-animation-studio.zip` و`prompt-master-pro.zip` و`image-prompt-forge.zip`.

## ChatGPT (GPT مخصص)
الصق `dist/custom-gpt/instructions.md` في تعليمات الـ GPT، وارفع ملفات `dist/custom-gpt/knowledge/` (10 ملفات تجمع المئة مهارة
بحسب المجال). السكربتات لا تعمل داخل ChatGPT إلا في Code Interpreter؛ المهارات تعمل كمنهجيات.

## إعادة البناء
```text
python tools/build.py
```
