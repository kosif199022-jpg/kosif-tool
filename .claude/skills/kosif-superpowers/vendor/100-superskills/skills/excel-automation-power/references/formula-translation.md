# ترجمة الصيغ بين Excel وGoogle Sheets وLark (خلاصة lark-sheets-formula-translation + خبرة Sheets)

## المبدأ الحاكم
Excel 365 **ينسكب** (spill) افتراضياً؛ Sheets وLark **يُسقطان** (project) الصيغة العادية على الصف/العمود الحالي، وتحتاج `ARRAYFORMULA` أو دالة مصفوفات أصلية لتتوسع عنصراً عنصراً.

## قرار سريع
1. النتيجة قيمة واحدة → لا ARRAYFORMULA.
2. النتيجة مصفوفة:
   - الصيغة تحوي دالة مصفوفات أصلية (FILTER، XLOOKUP، MAP، UNIQUE، SORT، SEQUENCE، SUMPRODUCT، VSTACK…) → لا حاجة؛ دلالة المصفوفة تنتشر إلى العمليات القياسية الخارجية (`=FILTER(...)+1` ✓، `=XLOOKUP(E2:E10,...)*100` ✓).
   - بلا دالة أصلية وعمليات قياسية على نطاقات → `ARRAYFORMULA(التعبير كله)` (`=A2:A100*B2:B100` → `=ARRAYFORMULA(A2:A100*B2:B100)`).
3. Excel يعتمد على `ROW(range)` لقيادة SUBTOTAL/INDIRECT/OFFSET عنصراً عنصراً → `MAP(ARRAYFORMULA(ROW(...)),LAMBDA(r, ...))`.
4. INDEX/INDIRECT/OFFSET داخلية تعيد نطاقاً وخارجها SUMIF/COUNTIF/SUMIFS → `MAP`/`REDUCE` صراحةً (لا توسّع ثانٍ تلقائي).
5. «احسب لعدة نطاقات ثم جمّع» → لا قائمة نطاقات؛ خفّض الأبعاد: `VSTACK`/`HSTACK`/`TOCOL`/`TOROW` أو `REDUCE` إلى قيمة.
6. فرق التواريخ → `DAYS(b,a)` أو `DATEDIF(a,b,"D"|"M"|"Y")` أو `b-a`؛ **لا** `DAY(b-a)`.

## ما لا يُنسخ آلياً
| Excel | Sheets/Lark |
|---|---|
| `=@A1:A10` | احذف `@` (الإسقاط افتراضي) |
| `=A1#` | نطاق صريح أو TAKE/DROP/ARRAY_CONSTRAIN |
| `=SUM(Table1[Amount])` | `=SUM(A2:A100)` (لا مراجع هيكلية) |
| `{=A1:A10*B1:B10}` (CSE) | `=ARRAYFORMULA(A1:A10*B1:B10)` |
| `LET`, LAMBDA مسمّاة، `=LAMBDA(x,x+1)(5)` | Lark: `#NAME?` → IF متداخلة أو عمود مساعد؛ LAMBDA **مدعومة فقط** كمعامل داخل MAP/REDUCE/BYROW/BYCOL/SCAN/MAKEARRAY. Sheets: LET وLAMBDA المسمّاة مدعومتان |
| `TEXTBEFORE/TEXTAFTER` | Sheets: REGEXEXTRACT؛ Lark: SPLIT/INDEX أو LEFT/MID+FIND |
| `STOCKHISTORY`, `WEBSERVICE`, CUBE*, `FORECAST.ETS`, `INFO`, `RTD`, `PHONETIC` | غير مدعومة في Lark؛ استيراد يدوي |
| PIVOT كصيغة | Lark: كائن جدول محوري حقيقي (`+pivot-create`)، ممنوع تقليده بـ SUMIFS |
| `H2:H`, `2:2` داخل صيغة Lark | ممنوعة؛ `H:H` أو نطاق صريح (`$A2:$Z2`) |

## المراجع المطلقة قبل التعبئة
حدّد ما يُقفل قبل السحب: ثابت `$C$3`، نطاق بيانات `$A$2:$B$5`، عمود مقفل `$A2`، صف مقفل `B$1`. راجع أسعار الصرف والضرائب وجداول البحث والأوزان.

## الدوال الأصلية للمصفوفات في Lark
ARRAYFORMULA ARRAY_CONSTRAIN BYCOL BYROW CHOOSECOLS CHOOSEROWS DROP EXPAND FILTER FLATTEN FREQUENCY GROWTH HSTACK IMPORT* LINEST LOGEST LOOKUP MAKEARRAY MAP MINVERSE MMULT MUNIT QUERY RANDARRAY REDUCE REGEXEXTRACT SCAN SEQUENCE SORT SORTBY SORTN SPLIT SUMPRODUCT **SWITCH** TAKE TEXTSPLIT TOCOL TOROW TRANSPOSE TREND UNIQUE VSTACK WRAPCOLS WRAPROWS XLOOKUP. (IMPORTRANGE: ≤ 5 تداخلات و≤ 100 مرجع لكل ورقة.)

## التحقق الثلاثي (إلزامي بعد الترجمة)
1. اختر 3-5 صفوف ممثّلة (أول، وسط، أخير، فارغ، شاذ).
2. احسب دلالة الصيغة الأصلية بـ Python (ما أراده المستخدم).
3. اكتب الترجمة في المنصة واقرأ القيم الفعلية.
4. تطابق الثلاثة = تسليم؛ الاختلاف يدل على دلالة مصفوفات أو تواريخ أو نطاقات.
ثم بوابة التحقق من الصيغ في المنصة (`status=success` لا `partial`).

## أمثلة
| Excel | Lark/Sheets |
|---|---|
| `=A2:A100*B2:B100` | `=ARRAYFORMULA(A2:A100*B2:B100)` |
| `=IF(A2:A100>0,B2:B100,"")` | `=ARRAYFORMULA(IF(A2:A100>0,B2:B100,""))` |
| `=INDEX(A1:D2,{2,1},0)` | `=ARRAYFORMULA(INDEX(A1:D2,{2,1},0))` |
| `=SUMPRODUCT(SUBTOTAL(103,INDIRECT("E"&ROW($E$16:$E$387))))` | `=SUMPRODUCT(MAP(ARRAYFORMULA(ROW($E$16:$E$387)),LAMBDA(row,SUBTOTAL(103,INDIRECT("E"&row)))))` |
| `=SUMIF(INDIRECT("E"&ROW($E$16:$E$387)),">0")` (خاطئ أصلاً) | `=MAP(ARRAYFORMULA(ROW($E$16:$E$387)),LAMBDA(r,SUMIF(INDIRECT("E"&r),">0")))` |
