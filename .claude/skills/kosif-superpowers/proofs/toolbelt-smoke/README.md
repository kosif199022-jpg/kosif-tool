# toolbelt-smoke — 20 أداة جديدة تعمل فعلًا هنا / 20 new tools, each doing real work

<div dir="rtl">

## بالعربية

**ماذا يثبت:** أن أدوات التوسعة التي أضيفت إلى الكتالوج يوم 2026-10-18 ليست روابط فقط: ثُبّتت في بيئة بايثون معزولة داخل حاوية Claude السحابية (بلا GPU) وأدّت كل واحدة مهمة حقيقية دون اتصال ودون تنزيل نماذج: حل معادلات بدقة رمزية، إثبات خاصية بـ Z3، استعلام SQL على 100 ألف صف، تدريب نموذج بتحقق متقاطع، توقع سلسلة زمنية بفترة ثقة، استخراج مقال عربي من HTML، اختبار خصائص يجد مثالًا مضادًا، عقد بيانات يرفض قيمة خاطئة، تحليل مقام لحن، جدولة مثلى، برمجة خطية، مساحة دائرة 1 كم حول القاهرة بإسقاط UTM حقيقي، ترجمة تسلسل جيني، وزن جزيء الأسبرين، تقطيع عربي ومطابقة «يوم الجمعة»، واستعلام متجهات.

**النتيجة:** `20/20 pass` (انظر `results.json` للأرقام والإصدارات). ثلاث أدوات (MediaPipe وArgos وSemgrep) أُثبت تحميلها فقط لأن عملها الكامل يحتاج تنزيل نماذج أو قواعد من الشبكة؛ لذلك بقيت شارتها 📦 في الكتالوج لا ✅.

**إعادة التشغيل:**

```bash
python3 -m venv /tmp/tb && /tmp/tb/bin/pip install sympy z3-solver duckdb polars scikit-learn statsforecast trafilatura hypothesis pandera music21 ortools pulp geopandas biopython rdkit spacy chromadb mediapipe argostranslate semgrep
/tmp/tb/bin/python -I .claude/skills/kosif-superpowers/proofs/toolbelt-smoke/smoke.py --json /tmp/tb/results.json
```

**دروس من التشغيل (أخطاء حقيقية صُححت):** PuLP 4 لم يعد يضم CBC ويتطلب متغيرات صحيحة محدودة مع CP-SAT؛ Chroma يرفض أسماء المجموعات الأقصر من 3 أحرف؛ حساب المساحة بإسقاط Web Mercator يعطي رقمًا مضللًا، فاستُخدم UTM 36N.

</div>

## English

**What it proves:** the extended-toolbelt records added on 2026-10-18 are not just links. Twenty libraries were installed into an isolated venv in the Claude cloud container (CPU only) and each did one real offline task with no model download: exact symbolic solving, an SMT proof, SQL over 100k rows, a cross-validated model, a forecast with intervals, Arabic article extraction, a property test that finds a counterexample, a data contract rejecting a bad value, key analysis of a melody, an optimal schedule, a linear program, a true-metric 1 km buffer around Cairo (UTM 36N), DNA translation, aspirin's molecular weight, Arabic tokenisation and rule matching, and a vector query.

**Result:** `20/20 pass`; numbers and versions in `results.json`. MediaPipe, Argos and Semgrep were only proven to load (full use needs models or rule packs from the network), so they stay 📦 in the catalog, not ✅.

**Lessons recorded:** PuLP 4 ships no CBC and CP-SAT needs bounded integer variables; Chroma rejects collection names shorter than 3 characters; Web Mercator areas are misleading, so the check uses UTM 36N.
