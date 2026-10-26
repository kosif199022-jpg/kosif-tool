# مرجع صيغ إكسل الحديثة (Excel 2021 / 365؛ لِـ 2016 وما قبل انظر البدائل)

## البحث
| المهمة | الحديثة | البديل القديم |
|---|---|---|
| قيمة مقابل مفتاح | `=XLOOKUP(المفتاح, عمود_المفاتيح, عمود_القيم, "غير موجود")` | `=IFERROR(INDEX(القيم, MATCH(المفتاح, المفاتيح, 0)), "غير موجود")` |
| بحث بشرطين | `=XLOOKUP(1, (A:A=x)*(B:B=y), C:C)` | `=INDEX(C:C, MATCH(1, (A:A=x)*(B:B=y), 0))` بـ Ctrl+Shift+Enter |
| آخر قيمة في عمود | `=XLOOKUP(TRUE, A:A<>"", A:A, , 0, -1)` | `=LOOKUP(2, 1/(A:A<>""), A:A)` |

## التجميع
- `=SUMIFS(المبالغ, الفئة, "مبيعات", التاريخ, ">="&DATE(2026,1,1))` — دائماً SUMIFS لا SUMIF للتوسع.
- `=COUNTIFS(...)`، `=AVERAGEIFS(...)`، `=MAXIFS(...)`، `=MINIFS(...)`.
- مجموع فريد: `=SUM(FILTER(المبالغ, (الفئة="أ")*(الحالة="مدفوع")))`.

## المصفوفات الديناميكية
- `=FILTER(الجدول, الشرط, "لا نتائج")`، `=SORT(FILTER(...), 2, -1)`، `=UNIQUE(العمود)`، `=SEQUENCE(12)`.
- `=LET(x, A2*B2, y, x*0.15, x+y)` للوضوح؛ `=LAMBDA(a,b, a*b)` تُسمّى في Name Manager كدالة مخصصة.
- `=TEXTSPLIT(A2, "،")`، `=TEXTJOIN("، ", TRUE, B2:B9)`، `=TEXTBEFORE/TEXTAFTER`.

## التواريخ والنصوص والعربية
- `=TEXT(A2, "[$-ar-SA]dd mmmm yyyy")` اسم الشهر بالعربية. الهجري: `=TEXT(A2, "[$-ar-SA,16]dd/mm/yyyy")` (التقويم 16 = أم القرى) أو `=TEXT(A2,"B2dd/mm/yyyy")`.
- أرقام عربية-هندية مخزّنة كنص: `=VALUE(SUBSTITUTE(... ))` أو `=NUMBERVALUE(A2)` بعد تحويل الأرقام؛ الأبسط: Power Query → Transform → Data Type.
- تنظيف: `=TRIM(CLEAN(A2))`، إزالة التشكيل: Power Query أو دالة LAMBDA بـ SUBSTITUTE متسلسلة.
- نهاية الشهر: `=EOMONTH(A2, 0)`؛ فرق بالأيام العملية: `=NETWORKDAYS.INTL(بداية, نهاية, "0000011")` (الجمعة والسبت عطلة).

## الأخطاء وتصحيحها
| الخطأ | السبب الشائع | الحل |
|---|---|---|
| #N/A | المفتاح غير موجود أو مسافة زائدة | TRIM المفاتيح، وif_not_found في XLOOKUP |
| #REF! | حُذف عمود/ورقة مُشار إليه | أعد الربط؛ استخدم جداول منظّمة بأسماء |
| #VALUE! | نص في حساب | VALUE/NUMBERVALUE، وفحص الأرقام كنص |
| #DIV/0! | قاسم صفر | `=IF(B2=0, "", A2/B2)` |
| #SPILL! | مصفوفة ديناميكية تصادم خلايا | أفرغ المنطقة أسفل الصيغة |

## قواعد الملف الاحترافي
1. البيانات في **جدول منظّم** (Ctrl+T) باسم ذي معنى؛ الصيغ تشير إلى `الجدول[العمود]`.
2. المدخلات بالأزرق في ورقة Assumptions؛ الحسابات بالأسود؛ لا رقم مدفون في صيغة.
3. ورقة Checks: المجاميع تطابق، ولا أخطاء (`=SUMPRODUCT(--ISERROR(النطاق))=0`)، والميزانية تتوازن.
4. التنسيق الشرطي للاستثناءات فقط؛ التحقق من البيانات للقوائم والتواريخ.
5. تجنّب الدوال المتقلبة (OFFSET، INDIRECT، NOW) في الملفات الكبيرة؛ وتجنّب الأعمدة الكاملة A:A في SUMPRODUCT.
6. ورقة «كيف يعمل» بالعربية: الغرض، والمدخلات، والمخرجات، وكل صيغة مهمة بجملة.

## python/openpyxl (توليد الملف)
```python
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
wb = Workbook(); ws = wb.active; ws.title = "Data"; ws.sheet_view.rightToLeft = True
ws.append(["التاريخ", "الفئة", "المبلغ"]); ws.append(["2026-01-05", "مبيعات", 1200])
ws.add_table(Table(displayName="tblData", ref="A1:C2", tableStyleInfo=TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)))
ws["E1"] = "إجمالي المبيعات"; ws["F1"] = '=SUMIFS(tblData[المبلغ], tblData[الفئة], "مبيعات")'
wb.save("out.xlsx")
```
ثم `python xlsx_check.py out.xlsx`. القيم المحسوبة تظهر بعد فتح الملف في إكسل (openpyxl لا يحسب).
