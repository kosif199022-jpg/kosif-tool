# `documents-office` — المستندات والكتابة (34 بطاقة)

> مكتبة بروتوكول USIP v5.6 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/documents-office.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/documents.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`DOC-01` مستند Word عربي من اليمين](#doc-01--مستند-word-عربي-من-اليمين--rtl-arabic-docx-with-python-docx)
- [`DOC-02` جدول Excel عربي بمعادلات ورسم](#doc-02--جدول-excel-عربي-بمعادلات-ورسم--arabic-xlsx-with-formulas-and-a-native-chart)
- [`DOC-03` إعادة حساب معادلات Excel بـ LibreOffice](#doc-03--إعادة-حساب-معادلات-excel-بـ-libreoffice--recalculate-xlsx-formulas-headless)
- [`DOC-04` عرض PowerPoint عربي برسم أصلي](#doc-04--عرض-powerpoint-عربي-برسم-أصلي--rtl-arabic-pptx-with-a-native-chart)
- [`DOC-05` PDF عربي من HTML وCSS](#doc-05--pdf-عربي-من-html-وcss--arabic-pdf-from-htmlcss-weasyprint)
- [`DOC-06` PDF من المتصفح الخفي](#doc-06--pdf-من-المتصفح-الخفي--html-to-pdf-with-headless-chromium)
- [`DOC-07` PDF برمجي بـ reportlab](#doc-07--pdf-برمجي-بـ-reportlab--programmatic-pdf-with-reportlab-shape-arabic-yourself)
- [`DOC-08` مكتبات JavaScript للمستندات](#doc-08--مكتبات-javascript-للمستندات--js-document-libraries-docx-pptxgenjs-exceljs-pdf-lib)
- [`DOC-09` تحويل Office إلى PDF دفعة واحدة](#doc-09--تحويل-office-إلى-pdf-دفعة-واحدة--batch-office-to-pdf-with-libreoffice)
- [`DOC-10` خطوط خاصة لـ LibreOffice دون تثبيت](#doc-10--خطوط-خاصة-لـ-libreoffice-دون-تثبيت--private-fontconfig-for-libreoffice-and-pango)
- [`DOC-11` ملاءمة الورقة عند تحويل Excel](#doc-11--ملاءمة-الورقة-عند-تحويل-excel--fit-to-page-before-xlsx-to-pdf)
- [`DOC-12` Markdown ↔ Word بـ pandoc](#doc-12--markdown--word-بـ-pandoc--markdown---docx-with-pandoc-rtl)
- [`DOC-13` دمج وتدوير وتشفير PDF](#doc-13--دمج-وتدوير-وتشفير-pdf--merge-rotate-and-encrypt-pdfs-pypdf)
- [`DOC-14` استخراج النص العربي من PDF بالطريقة الصحيحة](#doc-14--استخراج-النص-العربي-من-pdf-بالطريقة-الصحيحة--extract-arabic-from-pdfs-correctly)
- [`DOC-15` انتبه لربطة لا عند الاستخراج](#doc-15--انتبه-لربطة-لا-عند-الاستخراج--lam-alef-ligature-extraction-artefact)
- [`DOC-16` تحويل أي مستند إلى Markdown](#doc-16--تحويل-أي-مستند-إلى-markdown--any-office-file-to-markdown-markitdown)
- [`DOC-17` OCR لصفحات PDF الممسوحة](#doc-17--ocr-لصفحات-pdf-الممسوحة--ocr-for-scanned-pdf-pages)
- [`DOC-18` تصيير صفحات PDF للمراجعة البصرية](#doc-18--تصيير-صفحات-pdf-للمراجعة-البصرية--render-pdf-pages-to-png-for-visual-qa)
- [`DOC-19` pymupdf للنص والتصيير السريع](#doc-19--pymupdf-للنص-والتصيير-السريع--pymupdf-fast-text-and-render-agpl)
- [`DOC-20` جداول PDF بالمواقع (LTR)](#doc-20--جداول-pdf-بالمواقع-ltr--pdf-tables-with-positions-pdfplumber)
- [`DOC-21` تحليل PDF بالتخطيط (ثقيل)](#doc-21--تحليل-pdf-بالتخطيط-ثقيل--layout-aware-pdf-parsing-docling-camelot-tabula)
- [`DOC-22` اتجاه النص المختلط في المستندات](#doc-22--اتجاه-النص-المختلط-في-المستندات--mixed-direction-text-hygiene)
- [`DOC-23` من يشكّل العربية بنفسه ومن يحتاج تشكيلًا يدويًا](#doc-23--من-يشكّل-العربية-بنفسه-ومن-يحتاج-تشكيلًا-يدويًا--which-engines-need-manual-arabic-shaping)
- [`DOC-24` مراجعة المستند قبل التسليم](#doc-24--مراجعة-المستند-قبل-التسليم--document-delivery-gate)
- [`DOC-25` مهارات المستندات المدمجة في المضيف](#doc-25--مهارات-المستندات-المدمجة-في-المضيف--host-document-skills-docxxlsxpptxpdf)
- [`DOC-26` موصل المستندات الحية](#doc-26--موصل-المستندات-الحية--living-docs-connector-claude-docs)
- [`DOC-27` إنشاء الملفات في claude.ai](#doc-27--إنشاء-الملفات-في-claudeai--claudeai-file-creation-sandbox)
- [`DOC-28` ملفات Google عبر الموصل](#doc-28--ملفات-google-عبر-الموصل--google-docssheetsslides-via-connector)
- [`DOC-29` Docling: تحويل PDF وDOCX وPPTX إلى Markdown أو](#doc-29--docling-تحويل-pdf-وdocx-وpptx-إلى-markdown-أو--docling-convert-pdfdocxpptx-to-structured-markdownjson-with-tables-kept)
- [`DOC-30` Marker: تحويل ملفات PDF الأكاديمية أو الممسوحة إلى](#doc-30--marker-تحويل-ملفات-pdf-الأكاديمية-أو-الممسوحة-إلى--marker-turn-scanned-or-academic-pdfs-into-markdown-with-equations-in-latex)
- [`DOC-31` Slidev: كتابة عرض تقديمي بـMarkdown وتصديره PDF أو](#doc-31--slidev-كتابة-عرض-تقديمي-بـmarkdown-وتصديره-pdf-أو--slidev-author-a-markdown-deck-and-export-pdfpng)
- [`DOC-32` Marp CLI: تحويل Markdown إلى شرائح PDF أو PPTX](#doc-32--marp-cli-تحويل-markdown-إلى-شرائح-pdf-أو-pptx--marp-cli-markdown-to-pdfpptxhtml-decks-in-one-command)
- [`DOC-33` Mermaid: رسم مخططات انسيابية وتسلسلية وجانت من نص](#doc-33--mermaid-رسم-مخططات-انسيابية-وتسلسلية-وجانت-من-نص--mermaid-render-flowcharts-sequence-and-gantt-diagrams-from-text-to-svgpng)
- [`DOC-34` PlantUML: توليد مخططات UML من نص](#doc-34--plantuml-توليد-مخططات-uml-من-نص--plantuml-generate-uml-classsequencecomponent-diagrams-from-text)

## البطاقات / cards

### `DOC-01` — مستند Word عربي من اليمين / RTL Arabic DOCX with python-docx

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** أنشئ ملف Word بعناوين وفقرات وجداول عربية من اليمين إلى اليسار، ثم اقرأه مرة أخرى للتحقق. — Create a Word file with right-to-left Arabic headings, paragraphs and tables, then read it back to verify.

**متى:** عند طلب تقارير أو خطابات أو عقود أو نماذج بصيغة .docx / reports, letters, contracts or forms the user wants as .docx

**كيف:** python-docx has no RTL switch: add OxmlElement('w:bidi') to each paragraph's pPr; on each run add w:rtl, set w:rFonts w:cs='Amiri' (Arabic uses the complex-script font) and w:szCs; add w:bidiVisual to the table's tblPr so column 1 sits on the right. Read back with docx.Document(path) and check the XML for <w:bidi/>.

**المعاملات:** font size via both w:sz and w:szCs; heading level 1 = 20 pt in proof

**التثبيت:** pip install python-docx

**الوسوم:** docx · word · python-docx · rtl · arabic · وورد · مستند · تقرير · sales report · تقرير المبيعات · طلعلي تقرير

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `session-2026-10-16:general-arsenal.md#full-table`

#### 7. قدرات قريبة في العائلة

- `DOC-02` جدول Excel عربي بمعادلات ورسم / Arabic XLSX with formulas and a native chart (proven)
- `DOC-03` إعادة حساب معادلات Excel بـ LibreOffice / Recalculate XLSX formulas headless (proven)

### `DOC-02` — جدول Excel عربي بمعادلات ورسم / Arabic XLSX with formulas and a native chart

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** أنشئ مصنف Excel باتجاه ورقة من اليمين ومعادلات وتنسيقات أرقام ورسم بياني أصلي. — Build an Excel workbook with a right-to-left sheet, live formulas, number formats and a native chart.

**متى:** حين يكون المطلوب جدول بيانات سيواصل المستخدم تعديله / the deliverable is a spreadsheet the user will keep editing

**كيف:** openpyxl: ws.sheet_view.rightToLeft=True; Alignment(horizontal='right', readingOrder=2); formulas as strings ('=SUM(B2:B5)'); number_format '#,##0' / '0.0%'; BarChart + Reference(..., titles_from_data=True); ws.add_chart(ch,'E2'). Proof: 6.9 KB workbook, chart read back.

**التثبيت:** pip install openpyxl

**الوسوم:** xlsx · excel · openpyxl · formulas · chart · اكسل · جدول · معادلات

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `session-2026-10-16:general-arsenal.md#full-table`

#### 7. قدرات قريبة في العائلة

- `DOC-01` مستند Word عربي من اليمين / RTL Arabic DOCX with python-docx (proven)
- `DOC-03` إعادة حساب معادلات Excel بـ LibreOffice / Recalculate XLSX formulas headless (proven)
- `DOC-04` عرض PowerPoint عربي برسم أصلي / RTL Arabic PPTX with a native chart (proven)

### `DOC-03` — إعادة حساب معادلات Excel بـ LibreOffice / Recalculate XLSX formulas headless

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MPL-2.0 (LibreOffice) |

**ما هي:** openpyxl يكتب المعادلات ولا يحسبها؛ أعِد الحساب بتحويل LibreOffice ثم اقرأ القيم. — openpyxl writes formulas but never computes them; recalculate with a LibreOffice round trip, then read the values.

**متى:** قبل اقتباس أي رقم من مصنّف أنشأته، وقبل إرساله إلى من لا يملك Excel / before quoting any number from a workbook you generated; before sending it to someone without Excel

**كيف:** soffice --headless --norestore --convert-to xlsx --outdir recalc book.xlsx (1.2 s), then openpyxl.load_workbook('recalc/book.xlsx', data_only=True). Before recalculation data_only returns None; after it the proof read 3340 and 0.3593.

**التثبيت:** apt-get install libreoffice-calc (present in the cloud image 2026-10-16)

**الوسوم:** libreoffice · soffice · recalculate · formulas · openpyxl · حساب المعادلات

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `libreoffice` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-01` مستند Word عربي من اليمين / RTL Arabic DOCX with python-docx (proven)
- `DOC-02` جدول Excel عربي بمعادلات ورسم / Arabic XLSX with formulas and a native chart (proven)
- `DOC-04` عرض PowerPoint عربي برسم أصلي / RTL Arabic PPTX with a native chart (proven)
- `DOC-05` PDF عربي من HTML وCSS / Arabic PDF from HTML/CSS (weasyprint) (proven)

### `DOC-04` — عرض PowerPoint عربي برسم أصلي / RTL Arabic PPTX with a native chart

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** أنشئ عرضًا بمقاس 16:9 بعناوين ونقاط عربية من اليمين ورسم بياني قابل للتعديل. — Build a 16:9 deck with right-to-left Arabic titles and bullets and an editable chart.

**متى:** حين يطلب المستخدم ملف .pptx (وفي العرض بلا صيغة محددة يُفضَّل نوع الشرائح في المضيف إن وُجد) / the user asks for a .pptx file (for a deck without a named format, prefer the host's slides type if it exists)

**كيف:** prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5); per paragraph pPr.set('rtl','1'), pPr.set('algn','r'); per run rPr.set('lang','ar-SA') and add a:latin + a:cs typeface='Cairo'; chart: CategoryChartData + shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, ...). Read back the categories from chart.plots[0].categories.

**المعاملات:** title 36-40 pt, body 24 pt in proof

**التثبيت:** pip install python-pptx

**الوسوم:** pptx · powerpoint · python-pptx · slides · rtl · عرض تقديمي · شرائح

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `session-2026-10-16:general-arsenal.md#full-table`

#### 7. قدرات قريبة في العائلة

- `DOC-02` جدول Excel عربي بمعادلات ورسم / Arabic XLSX with formulas and a native chart (proven)
- `DOC-03` إعادة حساب معادلات Excel بـ LibreOffice / Recalculate XLSX formulas headless (proven)
- `DOC-05` PDF عربي من HTML وCSS / Arabic PDF from HTML/CSS (weasyprint) (proven)
- `DOC-06` PDF من المتصفح الخفي / HTML to PDF with headless Chromium (proven)

### `DOC-05` — PDF عربي من HTML وCSS / Arabic PDF from HTML/CSS (weasyprint)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | BSD-3-Clause |

**ما هي:** صمّم التقرير بـ HTML وCSS مع خطوط عربية مضمّنة، واطبعه PDF بحروف متصلة صحيحة. — Design the report in HTML/CSS with embedded Arabic fonts and print a PDF with correctly joined letters.

**متى:** لتقارير PDF أنيقة أو فواتير أو شهادات، وحيثما يتفوق تخطيط CSS على تخطيط معالج النصوص / polished PDF reports, invoices or certificates; anything where CSS layout beats word-processor layout

**كيف:** <html lang=ar dir=rtl>; @font-face { font-family: Amiri; src: url(file:///.../Amiri-Regular.ttf) }; @page { size: A4; margin: 16mm }; isolate English with a direction:ltr class; weasyprint.HTML(string=html, base_url=dir).write_pdf(out). Proof: 0.33 s, 17.9 KB, fonts embedded as subsets.

**التثبيت:** pip install weasyprint (needs pango; present in the cloud image)

**الوسوم:** weasyprint · pdf · html to pdf · css · arabic · تقرير PDF · طباعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `session-2026-10-16:general-arsenal.md#full-table`

#### 7. قدرات قريبة في العائلة

- `DOC-03` إعادة حساب معادلات Excel بـ LibreOffice / Recalculate XLSX formulas headless (proven)
- `DOC-04` عرض PowerPoint عربي برسم أصلي / RTL Arabic PPTX with a native chart (proven)
- `DOC-06` PDF من المتصفح الخفي / HTML to PDF with headless Chromium (proven)
- `DOC-07` PDF برمجي بـ reportlab / Programmatic PDF with reportlab (shape Arabic yourself) (proven)

### `DOC-06` — PDF من المتصفح الخفي / HTML to PDF with headless Chromium

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | Apache-2.0 |

**ما هي:** اطبع أي صفحة HTML (حتى المعتمدة على JavaScript) إلى PDF عبر Chromium الخفي. — Print any HTML page, including JavaScript-driven ones, to PDF through headless Chromium.

**متى:** حين تستخدم الصفحة رسومًا بـ JS أو CSS حديثًا لا يدعمه weasyprint / the page uses JS charts or modern CSS that weasyprint does not support

**كيف:** Playwright: page.goto(file URL); await document.fonts.ready; page.pdf({path, format:'A4', printBackground:true}). Proof snap.cjs printed the RTL dashboard; pdffonts shows Tajawal-Bold embedded.

**التثبيت:** npm i playwright && npx playwright install chromium (bundled at /opt/pw-browsers in the cloud image)

**الوسوم:** chromium · playwright · pdf · print · طباعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-data/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-04` عرض PowerPoint عربي برسم أصلي / RTL Arabic PPTX with a native chart (proven)
- `DOC-05` PDF عربي من HTML وCSS / Arabic PDF from HTML/CSS (weasyprint) (proven)
- `DOC-07` PDF برمجي بـ reportlab / Programmatic PDF with reportlab (shape Arabic yourself) (proven)
- `DOC-08` مكتبات JavaScript للمستندات / JS document libraries (docx, pptxgenjs, exceljs, pdf-lib) (proven)

### `DOC-07` — PDF برمجي بـ reportlab / Programmatic PDF with reportlab (shape Arabic yourself)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | BSD / MIT / LGPL-3.0 (python-bidi) |

**ما هي:** رسم PDF بالإحداثيات؛ reportlab لا يشكّل العربية فيجب تمريرها عبر reshaper وbidi. — Draw PDFs by coordinates; reportlab does not shape Arabic, so pass it through reshaper + bidi.

**متى:** للنماذج والملصقات والشهادات الدقيقة بالبكسل، وحين يكون HTML مبالغًا فيه / pixel-exact forms, labels or certificates; when HTML is overkill

**كيف:** pdfmetrics.registerFont(TTFont('Amiri', path)); c.setFont('Amiri',22); c.drawRightString(x,y,get_display(arabic_reshaper.reshape(text))). The raw string draws unjoined and reversed (see contact.png, last tile).

**التثبيت:** pip install reportlab arabic-reshaper python-bidi

**الوسوم:** reportlab · pdf · arabic_reshaper · bidi · شهادة · نموذج

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:arabic-reshaper` ← python3 -c "import arabic-reshaper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `session-2026-10-16:general-arsenal.md#full-table`

#### 7. قدرات قريبة في العائلة

- `DOC-05` PDF عربي من HTML وCSS / Arabic PDF from HTML/CSS (weasyprint) (proven)
- `DOC-06` PDF من المتصفح الخفي / HTML to PDF with headless Chromium (proven)
- `DOC-08` مكتبات JavaScript للمستندات / JS document libraries (docx, pptxgenjs, exceljs, pdf-lib) (proven)
- `DOC-09` تحويل Office إلى PDF دفعة واحدة / Batch Office to PDF with LibreOffice (proven)

### `DOC-08` — مكتبات JavaScript للمستندات / JS document libraries (docx, pptxgenjs, exceljs, pdf-lib)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** إنشاء docx وpptx وxlsx وPDF من Node دون Python. — Create docx, pptx, xlsx and PDF from Node without Python.

**متى:** في مشروع Node/TS أو زر تصدير داخل المتصفح / a Node/TS project or an in-browser export button

**كيف:** npm i docx pptxgenjs exceljs pdf-lib; Packer.toBuffer(doc); pptx.writeFile(); workbook.xlsx.writeFile(); PDFDocument.create(). All four produced files in the arsenal snapshot (Latin text only; RTL not tested).

**التثبيت:** npm i docx pptxgenjs exceljs pdf-lib

**الوسوم:** docx · pptxgenjs · exceljs · pdf-lib · node · javascript

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/arsenal-general.md`

#### 7. قدرات قريبة في العائلة

- `DOC-06` PDF من المتصفح الخفي / HTML to PDF with headless Chromium (proven)
- `DOC-07` PDF برمجي بـ reportlab / Programmatic PDF with reportlab (shape Arabic yourself) (proven)
- `DOC-09` تحويل Office إلى PDF دفعة واحدة / Batch Office to PDF with LibreOffice (proven)
- `DOC-10` خطوط خاصة لـ LibreOffice دون تثبيت / Private fontconfig for LibreOffice and pango (proven)

### `DOC-09` — تحويل Office إلى PDF دفعة واحدة / Batch Office to PDF with LibreOffice

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MPL-2.0 |

**ما هي:** حوّل docx وpptx وxlsx إلى PDF في أمر واحد دون واجهة. — Convert docx, pptx and xlsx to PDF in one headless command.

**متى:** حين يحتاج المستخدم PDF من ملف مكتبي، وللمراجعة البصرية لملف مكتبي مولَّد / the user needs a PDF of an office file; visual QA of a generated office file

**كيف:** soffice --headless --norestore --convert-to pdf --outdir out a.docx b.pptx c.xlsx (1.6 s for three files). For sheets set fitToPage first (DOC-11). Then render the pages to PNG and look at them (DOC-18).

**التثبيت:** apt-get install libreoffice (present in the cloud image)

**الوسوم:** libreoffice · soffice · docx to pdf · convert · تحويل

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `libreoffice` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-07` PDF برمجي بـ reportlab / Programmatic PDF with reportlab (shape Arabic yourself) (proven)
- `DOC-08` مكتبات JavaScript للمستندات / JS document libraries (docx, pptxgenjs, exceljs, pdf-lib) (proven)
- `DOC-10` خطوط خاصة لـ LibreOffice دون تثبيت / Private fontconfig for LibreOffice and pango (proven)
- `DOC-11` ملاءمة الورقة عند تحويل Excel / Fit-to-page before XLSX to PDF (proven)

### `DOC-10` — خطوط خاصة لـ LibreOffice دون تثبيت / Private fontconfig for LibreOffice and pango

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** وجّه LibreOffice وweasyprint إلى خطوط المشروع بملف fonts.conf خاص بدل تثبيتها في النظام. — Point LibreOffice and weasyprint at project fonts through a private fonts.conf instead of installing them.

**متى:** حين تعود العربية إلى DejaVu/FreeSerif في ملفات PDF المحوَّلة ولا يجوز تعديل النظام / Arabic falls back to DejaVu/FreeSerif in converted PDFs; you must not modify the system

**كيف:** Write fonts.conf: <include>/etc/fonts/fonts.conf</include><dir>/path/to/fonts</dir><cachedir>/tmp/fc</cachedir>; run soffice with env FONTCONFIG_FILE=that file (also set os.environ for weasyprint). Proof: pdffonts lists Amiri-Regular/Amiri-Bold in the LibreOffice PDF.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** fontconfig · fonts · libreoffice · arabic font · خطوط

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `libreoffice` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-08` مكتبات JavaScript للمستندات / JS document libraries (docx, pptxgenjs, exceljs, pdf-lib) (proven)
- `DOC-09` تحويل Office إلى PDF دفعة واحدة / Batch Office to PDF with LibreOffice (proven)
- `DOC-11` ملاءمة الورقة عند تحويل Excel / Fit-to-page before XLSX to PDF (proven)
- `DOC-12` Markdown ↔ Word بـ pandoc / Markdown <-> DOCX with pandoc (RTL) (proven)

### `DOC-11` — ملاءمة الورقة عند تحويل Excel / Fit-to-page before XLSX to PDF

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** بدون ضبط الملاءمة يقسم LibreOffice الرسم على صفحتين في الأوراق من اليمين. — Without fit-to-page, LibreOffice splits the chart of an RTL sheet across two pages.

**متى:** عند أي تحويل من xlsx إلى pdf / any xlsx -> pdf conversion

**كيف:** ws.page_setup.orientation='landscape'; ws.page_setup.fitToWidth=ws.page_setup.fitToHeight=1; ws.sheet_properties.pageSetUpPr.fitToPage=True. The first run produced 2 pages; after the fix, 1 page.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** xlsx · pdf · page setup · print · طباعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `libreoffice` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-09` تحويل Office إلى PDF دفعة واحدة / Batch Office to PDF with LibreOffice (proven)
- `DOC-10` خطوط خاصة لـ LibreOffice دون تثبيت / Private fontconfig for LibreOffice and pango (proven)
- `DOC-12` Markdown ↔ Word بـ pandoc / Markdown <-> DOCX with pandoc (RTL) (proven)
- `DOC-13` دمج وتدوير وتشفير PDF / Merge, rotate and encrypt PDFs (pypdf) (proven)

### `DOC-12` — Markdown ↔ Word بـ pandoc / Markdown <-> DOCX with pandoc (RTL)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | GPL-2.0-or-later (pandoc CLI) |

**ما هي:** اكتب بـ Markdown وأخرج Word عربيًا، أو حوّل Word إلى Markdown للقراءة. — Write in Markdown and output Arabic Word, or turn Word into Markdown for reading.

**متى:** حين يُكتب نص طويل بـ Markdown، وعند قراءة ملف .docx في السياق / long text drafted in Markdown; reading a .docx into context

**كيف:** front matter 'dir: rtl' and 'lang: ar'; pandoc note.md -o note.docx; pandoc note.docx -t gfm. Proof: the Arabic table survived md -> docx -> md. Use --reference-doc=style.docx for house styles (not tested).

**التثبيت:** apt-get install pandoc (3.1.3 present)

**الوسوم:** pandoc · markdown · docx · convert · تحويل

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pandoc` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-10` خطوط خاصة لـ LibreOffice دون تثبيت / Private fontconfig for LibreOffice and pango (proven)
- `DOC-11` ملاءمة الورقة عند تحويل Excel / Fit-to-page before XLSX to PDF (proven)
- `DOC-13` دمج وتدوير وتشفير PDF / Merge, rotate and encrypt PDFs (pypdf) (proven)
- `DOC-14` استخراج النص العربي من PDF بالطريقة الصحيحة / Extract Arabic from PDFs correctly (proven)

### `DOC-13` — دمج وتدوير وتشفير PDF / Merge, rotate and encrypt PDFs (pypdf)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | BSD-3-Clause |

**ما هي:** ادمج ملفات PDF ودوّر الصفحات واحمها بكلمة مرور AES-256. — Merge PDFs, rotate pages and protect them with an AES-256 password.

**متى:** عند تجميع حزمة ملفات أو تصحيح الاتجاه أو مشاركة ملف محمي / assembling a packet, fixing orientation, sharing a protected file

**كيف:** w=pypdf.PdfWriter(); w.append(f) per file; w.pages[0].rotate(90); w.encrypt(user_password=pw, algorithm='AES-256'); w.write(out); reopen: r.is_encrypted, r.decrypt(pw). Proof: 3 files -> 4 pages, /Rotate 90, the password works.

**التثبيت:** pip install pypdf

**الوسوم:** pypdf · merge · encrypt · rotate · دمج · تشفير

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `session-2026-10-16:general-arsenal.md#full-table`

#### 7. قدرات قريبة في العائلة

- `DOC-11` ملاءمة الورقة عند تحويل Excel / Fit-to-page before XLSX to PDF (proven)
- `DOC-12` Markdown ↔ Word بـ pandoc / Markdown <-> DOCX with pandoc (RTL) (proven)
- `DOC-14` استخراج النص العربي من PDF بالطريقة الصحيحة / Extract Arabic from PDFs correctly (proven)
- `DOC-15` انتبه لربطة لا عند الاستخراج / Lam-alef ligature extraction artefact (proven)

### `DOC-14` — استخراج النص العربي من PDF بالطريقة الصحيحة / Extract Arabic from PDFs correctly

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | BSD-3-Clause / GPL (poppler) |

**ما هي:** pypdf وpdftotext يعيدان العربية بالترتيب المنطقي، أما pdfplumber وpdfminer وmarkitdown فيعكسونها. — pypdf and pdftotext return Arabic in logical order; pdfplumber, pdfminer and markitdown return it reversed.

**متى:** عند قراءة أي PDF عربي أو مختلط، وبناء فهرس بحث، والاقتباس من PDF / reading any Arabic or mixed PDF; building a search index; quoting a PDF

**كيف:** Use pypdf.PdfReader(p).pages[i].extract_text() or `pdftotext -layout p -`; NFKC-normalise (undoes presentation forms) and strip U+202A..U+202E. Compare with a known phrase. Proof: pypdf and pdftotext gave 'تقرير المبيعات الربعي'; pdfplumber gave 'يعبرلا تاعيبملا ريرقت'.

**التثبيت:** pip install pypdf; apt-get install poppler-utils

**الوسوم:** pdf · extract text · arabic · pypdf · pdftotext · pdfplumber · استخراج · عكس النص

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-12` Markdown ↔ Word بـ pandoc / Markdown <-> DOCX with pandoc (RTL) (proven)
- `DOC-13` دمج وتدوير وتشفير PDF / Merge, rotate and encrypt PDFs (pypdf) (proven)
- `DOC-15` انتبه لربطة لا عند الاستخراج / Lam-alef ligature extraction artefact (proven)
- `DOC-16` تحويل أي مستند إلى Markdown / Any office file to Markdown (markitdown) (proven)

### `DOC-15` — انتبه لربطة لا عند الاستخراج / Lam-alef ligature extraction artefact

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قد يعيد pdftotext ربطة «لا» معكوسة («للاختبار» صارت «لالختبار») في ملفات Chromium. — pdftotext may reorder the lam-alef ligature in Chromium PDFs ('للاختبار' became 'لالختبار').

**متى:** عند مطابقة العربية المستخرجة بالمصدر والبحث داخل ملفات PDF / checking extracted Arabic against a source; searching inside PDFs

**كيف:** After extraction, diff against the source text with lam-alef-aware normalisation, or prefer the source HTML/DOCX when you have it. Seen on the dashboard PDF in the data proof.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** lam alef · ligature · pdf · arabic · ربطة لا

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-data/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-13` دمج وتدوير وتشفير PDF / Merge, rotate and encrypt PDFs (pypdf) (proven)
- `DOC-14` استخراج النص العربي من PDF بالطريقة الصحيحة / Extract Arabic from PDFs correctly (proven)
- `DOC-16` تحويل أي مستند إلى Markdown / Any office file to Markdown (markitdown) (proven)
- `DOC-17` OCR لصفحات PDF الممسوحة / OCR for scanned PDF pages (proven)

### `DOC-16` — تحويل أي مستند إلى Markdown / Any office file to Markdown (markitdown)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** حوّل docx وxlsx وpptx إلى Markdown لقراءتها في السياق؛ الحزمة تحتاج الإضافات. — Turn docx, xlsx and pptx into Markdown to read them into context; the package needs its extras.

**متى:** حين يرفع المستخدم ملفًا مكتبيًا ويسأل عن محتواه / the user uploads an office file and asks about its contents

**كيف:** pip install "markitdown[docx,pdf,xlsx,pptx]" (a bare install fails on docx with MissingDependencyException); MarkItDown().convert(path).text_content. Arabic is kept for docx/xlsx/pptx; for PDFs it comes out reversed (use DOC-14).

**التثبيت:** pip install "markitdown[docx,pdf,xlsx,pptx]"

**الوسوم:** markitdown · markdown · docx · xlsx · pptx · قراءة الملفات

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `session-2026-10-16:general-arsenal.md#full-table`

#### 7. قدرات قريبة في العائلة

- `DOC-14` استخراج النص العربي من PDF بالطريقة الصحيحة / Extract Arabic from PDFs correctly (proven)
- `DOC-15` انتبه لربطة لا عند الاستخراج / Lam-alef ligature extraction artefact (proven)
- `DOC-17` OCR لصفحات PDF الممسوحة / OCR for scanned PDF pages (proven)
- `DOC-18` تصيير صفحات PDF للمراجعة البصرية / Render PDF pages to PNG for visual QA (proven)

### `DOC-17` — OCR لصفحات PDF الممسوحة / OCR for scanned PDF pages

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | Apache-2.0 |

**ما هي:** حوّل صفحة PDF بلا طبقة نص إلى صورة 300 نقطة واقرأها بـ tesseract العربي. — Rasterise a PDF page with no text layer at 300 dpi and read it with Arabic tesseract.

**متى:** للمسوحات والصفحات المصوَّرة وملفات PDF التي لا يُخرج استخراج النص منها شيئًا / scans, photographed pages, PDFs where text extraction returns nothing

**كيف:** img=pypdfium2.PdfDocument(p)[i].render(scale=300/72).to_pil().convert('L'); pytesseract.image_to_string(img, lang='ara+eng', config='--oem 1 --psm 4'). Proof: title and English line recovered in 0.78 s. Validate digits (see MEDIA OCR findings).

**التثبيت:** apt-get install tesseract-ocr tesseract-ocr-ara; pip install pytesseract pypdfium2

**الوسوم:** ocr · scanned pdf · tesseract · arabic ocr · مسح ضوئي · تعرف ضوئي

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `tesseract` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-15` انتبه لربطة لا عند الاستخراج / Lam-alef ligature extraction artefact (proven)
- `DOC-16` تحويل أي مستند إلى Markdown / Any office file to Markdown (markitdown) (proven)
- `DOC-18` تصيير صفحات PDF للمراجعة البصرية / Render PDF pages to PNG for visual QA (proven)
- `DOC-19` pymupdf للنص والتصيير السريع / pymupdf fast text and render (AGPL) (proven)

### `DOC-18` — تصيير صفحات PDF للمراجعة البصرية / Render PDF pages to PNG for visual QA

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | Apache-2.0 / BSD-3-Clause (pypdfium2) |

**ما هي:** حوّل كل صفحة إلى صورة وقصّها حول الحبر واجمعها في ورقة اتصال، ثم انظر إليها قبل التسليم. — Render each page to an image, crop to the ink, tile a contact sheet, and look at it before delivery.

**متى:** بعد إنشاء أي مستند أو تحويله، ولفحص تشكيل العربية والفيض والخطوط المفقودة / after generating or converting any document; Arabic shaping, overflow or missing-font checks

**كيف:** pypdfium2: page.render(scale=2).to_pil(); crop with ImageChops.difference against white .getbbox(); tile with Pillow; quantize(128) to keep it < 300 KB; then open it with the Read tool and look. Proof contact.png: 50 KB, six documents.

**التثبيت:** pip install pypdfium2 pillow

**الوسوم:** pdf to png · contact sheet · visual qa · مراجعة بصرية

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-16` تحويل أي مستند إلى Markdown / Any office file to Markdown (markitdown) (proven)
- `DOC-17` OCR لصفحات PDF الممسوحة / OCR for scanned PDF pages (proven)
- `DOC-19` pymupdf للنص والتصيير السريع / pymupdf fast text and render (AGPL) (proven)
- `DOC-20` جداول PDF بالمواقع (LTR) / PDF tables with positions (pdfplumber) (install)

### `DOC-19` — pymupdf للنص والتصيير السريع / pymupdf fast text and render (AGPL)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | AGPL-3.0 or commercial |

**ما هي:** مكتبة سريعة لاستخراج النص وتصيير الصفحات وتعديل PDF؛ رخصتها AGPL. — A fast library for PDF text, page rendering and edits; licensed AGPL.

**متى:** لملفات PDF الكبيرة، أو حين تحتاج التعديل والتعليقات التوضيحية؛ أداةً فقط ولا تُدمج في شيفرة مغلقة / large PDFs, or when you need edits/annotations; only as a tool, never vendored into closed code

**كيف:** import pymupdf (not `import fitz`, which is deprecated); doc[0].get_text(); doc[0].get_pixmap().save('p.png'). Arabic order not tested; check it like DOC-14.

**التثبيت:** pip install pymupdf

**الوسوم:** pymupdf · fitz · pdf · agpl

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/references/arsenal-general.md`

#### 7. قدرات قريبة في العائلة

- `DOC-17` OCR لصفحات PDF الممسوحة / OCR for scanned PDF pages (proven)
- `DOC-18` تصيير صفحات PDF للمراجعة البصرية / Render PDF pages to PNG for visual QA (proven)
- `DOC-20` جداول PDF بالمواقع (LTR) / PDF tables with positions (pdfplumber) (install)
- `DOC-21` تحليل PDF بالتخطيط (ثقيل) / Layout-aware PDF parsing (docling, camelot, tabula) (install)

### `DOC-20` — جداول PDF بالمواقع (LTR) / PDF tables with positions (pdfplumber)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | MIT |

**ما هي:** pdfplumber يعطي إحداثيات الكلمات والجداول؛ ممتاز للإنجليزية ولكنه يعكس العربية. — pdfplumber gives word and table coordinates; excellent for English, but it reverses Arabic.

**متى:** عند استخراج الجداول من ملفات PDF من اليسار إلى اليمين (كشوف الحساب والفواتير) / extracting tables from left-to-right PDFs (statements, invoices)

**كيف:** page.extract_tables(); page.extract_words() for x/y. For Arabic cells reverse the string or re-read the region with pypdf/pdftotext -layout -x -y -W -H. Not run here: only pdfplumber extract_text was exercised (it returned Arabic reversed); extract_tables and extract_words are untested in this skill.

**التثبيت:** pip install pdfplumber

**الوسوم:** pdfplumber · tables · pdf · invoice · جداول

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/references/arsenal-general.md`

#### 7. قدرات قريبة في العائلة

- `DOC-18` تصيير صفحات PDF للمراجعة البصرية / Render PDF pages to PNG for visual QA (proven)
- `DOC-19` pymupdf للنص والتصيير السريع / pymupdf fast text and render (AGPL) (proven)
- `DOC-21` تحليل PDF بالتخطيط (ثقيل) / Layout-aware PDF parsing (docling, camelot, tabula) (install)
- `DOC-22` اتجاه النص المختلط في المستندات / Mixed-direction text hygiene (proven)

### `DOC-21` — تحليل PDF بالتخطيط (ثقيل) / Layout-aware PDF parsing (docling, camelot, tabula)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** أدوات أثقل لاستخراج التخطيط والجداول المعقدة. — Heavier tools for layout and complex tables.

**متى:** لملفات PDF العلمية متعددة الأعمدة أو الجداول المعقدة، بعد فشل الأدوات البسيطة / multi-column scientific PDFs or messy tables, after the simple tools fail

**كيف:** docling pulls torch and models; camelot needs ghostscript/opencv; tabula needs Java. None of them was installed or run here.

**التثبيت:** pip install docling \| camelot-py \| tabula-py

**الوسوم:** docling · camelot · tabula · layout · tables

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:opencv` ← python3 -c "import opencv" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:torch` ← python3 -c "import torch" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:docling` ← python3 -c "import docling" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-19` pymupdf للنص والتصيير السريع / pymupdf fast text and render (AGPL) (proven)
- `DOC-20` جداول PDF بالمواقع (LTR) / PDF tables with positions (pdfplumber) (install)
- `DOC-22` اتجاه النص المختلط في المستندات / Mixed-direction text hygiene (proven)
- `DOC-23` من يشكّل العربية بنفسه ومن يحتاج تشكيلًا يدويًا / Which engines need manual Arabic shaping (proven)

### `DOC-22` — اتجاه النص المختلط في المستندات / Mixed-direction text hygiene

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اعزل المقاطع اللاتينية والأرقام داخل النص العربي حتى لا تنقلب علامات الترقيم والأقواس. — Isolate Latin runs and numbers inside Arabic text so punctuation and brackets do not flip.

**متى:** حين يحتوي النص العربي أسماء إنجليزية أو رموزًا أو روابط أو إصدارات أو نسبًا مئوية / Arabic text containing English names, codes, URLs, versions or percentages

**كيف:** HTML: <span dir=ltr> or <bdi>, or a class with direction:ltr; DOCX: keep LTR runs without w:rtl; PPTX: separate runs. Choose one numeral system per document (Arabic-Indic ٠-٩ or Western 0-9) and keep it. The proof PDF holds an LTR English line inside an RTL page.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** bidi · rtl · ltr · mixed text · numerals · اتجاه النص · أرقام هندية

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-20` جداول PDF بالمواقع (LTR) / PDF tables with positions (pdfplumber) (install)
- `DOC-21` تحليل PDF بالتخطيط (ثقيل) / Layout-aware PDF parsing (docling, camelot, tabula) (install)
- `DOC-23` من يشكّل العربية بنفسه ومن يحتاج تشكيلًا يدويًا / Which engines need manual Arabic shaping (proven)
- `DOC-24` مراجعة المستند قبل التسليم / Document delivery gate (documented)

### `DOC-23` — من يشكّل العربية بنفسه ومن يحتاج تشكيلًا يدويًا / Which engines need manual Arabic shaping

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** weasyprint وLibreOffice وWord وPowerPoint وChromium وPillow 12 وmatplotlib 3.11 تشكّل بنفسها؛ reportlab وحده يحتاج reshaper وbidi. — weasyprint, LibreOffice, Word/PowerPoint XML, Chromium, Pillow 12 and matplotlib 3.11 shape Arabic themselves; only reportlab needs reshaper + bidi.

**متى:** عند اختيار مسار التصيير للعربية / choosing a rendering path for Arabic

**كيف:** Default to raw logical strings. Add arabic_reshaper.reshape + bidi.get_display only for engines without a shaper (reportlab, old PIL/matplotlib without raqm). Doing both reverses the text. All of these were exercised across the docs, data and media proofs.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** arabic shaping · raqm · harfbuzz · reshaper · تشكيل الحروف

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `libreoffice` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:pillow` ← python3 -c "import pillow" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:matplotlib` ← python3 -c "import matplotlib" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:arabic-reshaper` ← python3 -c "import arabic-reshaper" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-docs/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-data/README.md`
- `kosif-tool/.claude/skills/kosif-superpowers/proofs/general-media/README.md`

#### 7. قدرات قريبة في العائلة

- `DOC-21` تحليل PDF بالتخطيط (ثقيل) / Layout-aware PDF parsing (docling, camelot, tabula) (install)
- `DOC-22` اتجاه النص المختلط في المستندات / Mixed-direction text hygiene (proven)
- `DOC-24` مراجعة المستند قبل التسليم / Document delivery gate (documented)
- `DOC-25` مهارات المستندات المدمجة في المضيف / Host document skills (docx/xlsx/pptx/pdf) (key)

### `DOC-24` — مراجعة المستند قبل التسليم / Document delivery gate

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لا تسلّم مستندًا قبل قراءته آليًا والنظر إلى صفحاته والتأكد من تطابق أرقامه. — Never deliver a document before reading it back, looking at its pages and reconciling its numbers.

**متى:** عند كل ملف docx/xlsx/pptx/pdf مولَّد / every generated docx/xlsx/pptx/pdf

**كيف:** Checklist: 1) read back text with the format's own library; 2) recalc spreadsheets; 3) render pages to PNG and look (Arabic joined, right-aligned, nothing cut); 4) numbers come from the frozen results file (ANLY compute-freeze); 5) file size and page count are sensible; 6) state anything you could not verify (e.g., not opened in MS Office).

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** qa · delivery · checklist · مراجعة · تسليم

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-22` اتجاه النص المختلط في المستندات / Mixed-direction text hygiene (proven)
- `DOC-23` من يشكّل العربية بنفسه ومن يحتاج تشكيلًا يدويًا / Which engines need manual Arabic shaping (proven)
- `DOC-25` مهارات المستندات المدمجة في المضيف / Host document skills (docx/xlsx/pptx/pdf) (key)
- `DOC-26` موصل المستندات الحية / Living-docs connector (Claude Docs) (key)

### `DOC-25` — مهارات المستندات المدمجة في المضيف / Host document skills (docx/xlsx/pptx/pdf)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** في بعض الحسابات تظهر مهارات جاهزة للمستندات؛ حمّلها قبل العمل إن وُجدت. — Some accounts list ready-made document skills; load them before working when they exist.

**متى:** حين تعرض قائمة مهارات الجلسة مهارات docx/xlsx/pptx/pdf (مثل anthropic-skills:docx) / the session's skill list shows docx/xlsx/pptx/pdf skills (e.g. anthropic-skills:docx)

**كيف:** Read the skill listing; invoke the matching skill first. It carries tested recipes, such as tracked changes and templates. They require the account feature; this session listed them (2026-10-16) and they were not invoked here.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** skills · docx skill · xlsx skill · pptx skill · pdf skill · مهارات

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-23` من يشكّل العربية بنفسه ومن يحتاج تشكيلًا يدويًا / Which engines need manual Arabic shaping (proven)
- `DOC-24` مراجعة المستند قبل التسليم / Document delivery gate (documented)
- `DOC-26` موصل المستندات الحية / Living-docs connector (Claude Docs) (key)
- `DOC-27` إنشاء الملفات في claude.ai / claude.ai file creation sandbox (key)

### `DOC-26` — موصل المستندات الحية / Living-docs connector (Claude Docs)

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مستندات مشتركة قابلة للتعليق والتصدير إلى Word وPDF عبر موصل الطرف الأول عند وجوده. — Shared, commentable documents that export to Word/PDF through the first-party connector, when present.

**متى:** حين يريد المستخدم مستندًا يُشارَك أو يُحرَّر معًا ويوفّر المضيف الموصّل / the user wants a document to share or edit together, and the host exposes the connector

**كيف:** Follow the connector's own guide (create the skeleton first, then fill the sections). Only a host-designated first-party connector counts. Not exercised in this proof.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** docs connector · collaboration · export · مستند مشترك

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-24` مراجعة المستند قبل التسليم / Document delivery gate (documented)
- `DOC-25` مهارات المستندات المدمجة في المضيف / Host document skills (docx/xlsx/pptx/pdf) (key)
- `DOC-27` إنشاء الملفات في claude.ai / claude.ai file creation sandbox (key)
- `DOC-28` ملفات Google عبر الموصل / Google Docs/Sheets/Slides via connector (key)

### `DOC-27` — إنشاء الملفات في claude.ai / claude.ai file creation sandbox

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** في تطبيق claude.ai يمكن إنشاء docx وxlsx وpptx وpdf داخل بيئة تنفيذ؛ الشبكة يحددها المسؤول. — In the claude.ai app, docx/xlsx/pptx/pdf can be created in a code-execution sandbox; network access is set by the admin.

**متى:** عند العمل في واجهة محادثة claude.ai بدلًا من Claude Code / working in the claude.ai chat surface rather than Claude Code

**كيف:** Assume no apt and maybe no network: use preinstalled libraries and bundled fonts; verify with a quick import before promising. Per the help article (fetched 2026-10-16); not run from here.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** claude.ai · file creation · sandbox · إنشاء ملفات

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-25` مهارات المستندات المدمجة في المضيف / Host document skills (docx/xlsx/pptx/pdf) (key)
- `DOC-26` موصل المستندات الحية / Living-docs connector (Claude Docs) (key)
- `DOC-28` ملفات Google عبر الموصل / Google Docs/Sheets/Slides via connector (key)
- `DOC-29` Docling: تحويل PDF وDOCX وPPTX إلى Markdown أو / Docling: Convert PDF/DOCX/PPTX to structured Markdown/JSON with tables kept (install)

### `DOC-28` — ملفات Google عبر الموصل / Google Docs/Sheets/Slides via connector

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `none` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تعديل ملفات Google Drive يمر عبر موصل وحساب المستخدم. — Editing Google Drive files goes through a connector and the user's account.

**متى:** حين يذكر المستخدم Google Docs/Sheets/Slides أو يلصق رابط docs.google.com / the user names Google Docs/Sheets/Slides or pastes a docs.google.com link

**كيف:** Load the host's google-workspace skill if listed, and use the connector's tools. Without a connector, export the file locally (DOC-01..05) and say so.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** google docs · google sheets · drive · connector

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-26` موصل المستندات الحية / Living-docs connector (Claude Docs) (key)
- `DOC-27` إنشاء الملفات في claude.ai / claude.ai file creation sandbox (key)
- `DOC-29` Docling: تحويل PDF وDOCX وPPTX إلى Markdown أو / Docling: Convert PDF/DOCX/PPTX to structured Markdown/JSON with tables kept (install)
- `DOC-30` Marker: تحويل ملفات PDF الأكاديمية أو الممسوحة إلى / Marker: Turn scanned or academic PDFs into Markdown with equations in LaTeX (install)

### `DOC-29` — Docling: تحويل PDF وDOCX وPPTX إلى Markdown أو / Docling: Convert PDF/DOCX/PPTX to structured Markdown/JSON with tables kept

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** تحويل PDF وDOCX وPPTX إلى Markdown أو JSON منظم مع الحفاظ على الجداول. — Convert PDF/DOCX/PPTX to structured Markdown/JSON with tables kept. (Docling, ★69.1k, MIT).

**متى:** في مهام تحليل المستندات التي يحق للمستخدم تشغيلها / document parsing tasks the user has the right to run

**كيف:** `pip install docling (layout/table models download, a few hundred MB)`. Licence note: permissive.

**التثبيت:** pip install docling (layout/table models download, a few hundred MB)

**الوسوم:** Document parsing · Docling · toolbelt · توسعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `pip:docling` ← python3 -c "import docling" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-27` إنشاء الملفات في claude.ai / claude.ai file creation sandbox (key)
- `DOC-28` ملفات Google عبر الموصل / Google Docs/Sheets/Slides via connector (key)
- `DOC-30` Marker: تحويل ملفات PDF الأكاديمية أو الممسوحة إلى / Marker: Turn scanned or academic PDFs into Markdown with equations in LaTeX (install)
- `DOC-31` Slidev: كتابة عرض تقديمي بـMarkdown وتصديره PDF أو / Slidev: Author a Markdown deck and export PDF/PNG (install)

### `DOC-30` — Marker: تحويل ملفات PDF الأكاديمية أو الممسوحة إلى / Marker: Turn scanned or academic PDFs into Markdown with equations in LaTeX

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | Apache-2.0 code; model weights separate terms |

**ما هي:** تحويل ملفات PDF الأكاديمية أو الممسوحة إلى Markdown مع المعادلات LaTeX. — Turn scanned or academic PDFs into Markdown with equations in LaTeX. (Marker, ★40.5k, Apache-2.0 code; model weights separate terms).

**متى:** في مهام تحليل المستندات التي يحق للمستخدم تشغيلها / document parsing tasks the user has the right to run

**كيف:** `pip install marker-pdf (models ~1–2 GB)`. Licence note: custom: read before use.

**التثبيت:** pip install marker-pdf (models ~1–2 GB)

**الوسوم:** Document parsing · Marker · toolbelt · توسعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `latex` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `network` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `pip:marker` ← python3 -c "import marker" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-28` ملفات Google عبر الموصل / Google Docs/Sheets/Slides via connector (key)
- `DOC-29` Docling: تحويل PDF وDOCX وPPTX إلى Markdown أو / Docling: Convert PDF/DOCX/PPTX to structured Markdown/JSON with tables kept (install)
- `DOC-31` Slidev: كتابة عرض تقديمي بـMarkdown وتصديره PDF أو / Slidev: Author a Markdown deck and export PDF/PNG (install)
- `DOC-32` Marp CLI: تحويل Markdown إلى شرائح PDF أو PPTX / Marp CLI: Markdown to PDF/PPTX/HTML decks in one command (install)

### `DOC-31` — Slidev: كتابة عرض تقديمي بـMarkdown وتصديره PDF أو / Slidev: Author a Markdown deck and export PDF/PNG

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** كتابة عرض تقديمي بـMarkdown وتصديره PDF أو PNG. — Author a Markdown deck and export PDF/PNG. (Slidev, ★49.1k, MIT).

**متى:** في مهام الشرائح كشيفرة التي يحق للمستخدم تشغيلها / slides as code tasks the user has the right to run

**كيف:** `npm i -D @slidev/cli playwright-chromium`. Licence note: permissive.

**التثبيت:** npm i -D @slidev/cli playwright-chromium

**الوسوم:** Slides as code · Slidev · toolbelt · توسعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:slidev` ← npm ls slidev أو وجود node_modules/slidev
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-29` Docling: تحويل PDF وDOCX وPPTX إلى Markdown أو / Docling: Convert PDF/DOCX/PPTX to structured Markdown/JSON with tables kept (install)
- `DOC-30` Marker: تحويل ملفات PDF الأكاديمية أو الممسوحة إلى / Marker: Turn scanned or academic PDFs into Markdown with equations in LaTeX (install)
- `DOC-32` Marp CLI: تحويل Markdown إلى شرائح PDF أو PPTX / Marp CLI: Markdown to PDF/PPTX/HTML decks in one command (install)
- `DOC-33` Mermaid: رسم مخططات انسيابية وتسلسلية وجانت من نص / Mermaid: Render flowcharts, sequence and Gantt diagrams from text to SVG/PNG (install)

### `DOC-32` — Marp CLI: تحويل Markdown إلى شرائح PDF أو PPTX / Marp CLI: Markdown to PDF/PPTX/HTML decks in one command

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** تحويل Markdown إلى شرائح PDF أو PPTX أو HTML بأمر واحد. — Markdown to PDF/PPTX/HTML decks in one command. (Marp CLI, ★3.9k, MIT).

**متى:** في مهام الشرائح كشيفرة التي يحق للمستخدم تشغيلها / slides as code tasks the user has the right to run

**كيف:** `npm i -g @marp-team/marp-cli`. Licence note: permissive.

**التثبيت:** npm i -g @marp-team/marp-cli

**الوسوم:** Slides as code · Marp CLI · toolbelt · توسعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:office` ← python3 -c "import office" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- `npm:marp` ← npm ls marp أو وجود node_modules/marp
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-30` Marker: تحويل ملفات PDF الأكاديمية أو الممسوحة إلى / Marker: Turn scanned or academic PDFs into Markdown with equations in LaTeX (install)
- `DOC-31` Slidev: كتابة عرض تقديمي بـMarkdown وتصديره PDF أو / Slidev: Author a Markdown deck and export PDF/PNG (install)
- `DOC-33` Mermaid: رسم مخططات انسيابية وتسلسلية وجانت من نص / Mermaid: Render flowcharts, sequence and Gantt diagrams from text to SVG/PNG (install)
- `DOC-34` PlantUML: توليد مخططات UML من نص / PlantUML: Generate UML class/sequence/component diagrams from text (install)

### `DOC-33` — Mermaid: رسم مخططات انسيابية وتسلسلية وجانت من نص / Mermaid: Render flowcharts, sequence and Gantt diagrams from text to SVG/PNG

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | MIT |

**ما هي:** رسم مخططات انسيابية وتسلسلية وجانت من نص إلى SVG أو PNG. — Render flowcharts, sequence and Gantt diagrams from text to SVG/PNG. (Mermaid, ★90.7k, MIT).

**متى:** في مهام المخططات كشيفرة التي يحق للمستخدم تشغيلها / diagrams as code tasks the user has the right to run

**كيف:** `npm i -g @mermaid-js/mermaid-cli`. Licence note: permissive.

**التثبيت:** npm i -g @mermaid-js/mermaid-cli

**الوسوم:** Diagrams as code · Mermaid · toolbelt · توسعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:mermaid` ← npm ls mermaid أو وجود node_modules/mermaid
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-31` Slidev: كتابة عرض تقديمي بـMarkdown وتصديره PDF أو / Slidev: Author a Markdown deck and export PDF/PNG (install)
- `DOC-32` Marp CLI: تحويل Markdown إلى شرائح PDF أو PPTX / Marp CLI: Markdown to PDF/PPTX/HTML decks in one command (install)
- `DOC-34` PlantUML: توليد مخططات UML من نص / PlantUML: Generate UML class/sequence/component diagrams from text (install)

### `DOC-34` — PlantUML: توليد مخططات UML من نص / PlantUML: Generate UML class/sequence/component diagrams from text

| الحقل | القيمة |
|---|---|
| العائلة | `documents-office` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/documents-office.md)) |
| المجموعة | المستندات والكتابة (`documents`) |
| نوع المخرج (A25، A27) | مستند وكتابة ومحتوى (`document`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `none` |
| الرخصة | LGPL-3.0 (other editions exist) |

**ما هي:** توليد مخططات UML من نص. — Generate UML class/sequence/component diagrams from text. (PlantUML, ★13.4k, LGPL-3.0 (other editions exist)).

**متى:** في مهام المخططات كشيفرة التي يحق للمستخدم تشغيلها / diagrams as code tasks the user has the right to run

**كيف:** `apt-get install -y plantuml`. Licence note: weak copyleft.

**التثبيت:** apt-get install -y plantuml

**الوسوم:** Diagrams as code · PlantUML · toolbelt · توسعة

#### 1. الاستقبال (A25)

- الجمهور: افتراض مكتوب ← قارئ عام ذكي غير متخصص
- النبرة واللهجة: افتراض مكتوب ← لغة الطلب ولهجته
- الطول: افتراض مكتوب ← أقصر طول يحقق الغرض
- الصيغة: افتراض مكتوب ← نص في الرد، أو مستند إن طُلب ملف
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `plantuml` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `brief` ← المخرج `document`، والمنفّذ `method:DOC-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: الغرض والقارئ ← هيكل العناوين ← مسودة ← مراجعة الحقائق ← تحرير اللغة ← فتح الملف بصيغته ← تسليم.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: يحقق الغرض في أول فقرة ← قراءة الافتتاح
- إلزامي: عربية سليمة إملاءً ونحوًا ← مراجعة سطر بسطر
- جودة: بلا حشو ولا عبارات عامة بلا مضمون ← think.py critic
- إلزامي: كل رقم أو اسم أو تاريخ متحقق منه ← مصدر لكل حقيقة
- إلزامي: الملف المطلوب يُفتح فعلًا بصيغته ← فتح الملف
- أمر الحكم في الوضع 1: `think.py qa document --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- لا دليل مسجل: لا تُقدَّم أكثر من منهج.

#### 7. قدرات قريبة في العائلة

- `DOC-32` Marp CLI: تحويل Markdown إلى شرائح PDF أو PPTX / Marp CLI: Markdown to PDF/PPTX/HTML decks in one command (install)
- `DOC-33` Mermaid: رسم مخططات انسيابية وتسلسلية وجانت من نص / Mermaid: Render flowcharts, sequence and Gantt diagrams from text to SVG/PNG (install)

