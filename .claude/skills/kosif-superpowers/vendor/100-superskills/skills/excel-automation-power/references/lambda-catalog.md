# كتالوج LAMBDA والمصفوفات الديناميكية (Excel 365/2024)

## لماذا LAMBDA
صيغة متكررة في 40 خلية = 40 نسخة لخطأ واحد. دالة مسمّاة تُعرَّف مرة (Formulas → Name Manager → New، أو `scripts/lambda_library.py`) وتُستدعى بالاسم، وتُوثَّق في ورقة Docs، وتُنقل بين المصنّفات بنسخ تعريفها.

## القالب
```excel
=LAMBDA(param1, [optional2],
  LET(
    step1, <expr>,
    step2, <expr using step1>,
    result, <expr>,
    result
  )
)
```
- `ISOMITTED(optional)` للافتراضات.
- اختبر بالاستدعاء المباشر قبل التسمية: `=LAMBDA(x,x*2)(5)` → 10.
- العودية مسموحة (الدالة تستدعي اسمها) لكن احذر العمق.

## المكتبة المضمّنة (lambda_library.py)
| الاسم | الغرض |
|---|---|
| SAFE_DIV(num,den,[alt]) | قسمة بلا #DIV/0! |
| PCT_CHANGE(old,new) | نسبة التغيّر |
| CAGR(start,end,years) | نمو سنوي مركّب |
| TRIM_ALL(txt) | مسافات + NBSP + كشيدة |
| ARABIC_DIGITS / LATIN_DIGITS | ٠-٩ ↔ 0-9 |
| BUCKET(x,edges,labels) | شرائح |
| CLAMP(x,lo,hi) | حصر |
| NPV_DATED(rate,cf,dates) | XNPV بتواريخ |
| WEEKDAY_AR / MONTH_AR | أسماء عربية |
| HIJRI_TEXT(d,[fmt]) | أم القرى كنص |
| SPLIT_NAME(full,part) | أول/أخير/أوسط |
| LAST_NONBLANK(rng) | آخر قيمة |
| RUNNING_TOTAL(rng) | تراكمي (SCAN) |
| RANK_DENSE(x,rng) | ترتيب كثيف |
| IS_BETWEEN, ROUND_TO | أدوات صغيرة |

## المصفوفات الديناميكية بدل الجداول الساكنة
```excel
=SORT(FILTER(tblSales,(tblSales[الفئة]="أ")*(tblSales[المبلغ]>1000)),3,-1)
=UNIQUE(tblSales[العميل])
=MAP(A2:A100,LAMBDA(x,IF(x>0,"موجب","سالب")))
=REDUCE(0,B2:B100,LAMBDA(acc,v,acc+MAX(0,v)))        -- مجموع الموجب فقط
=SCAN(0,B2:B100,LAMBDA(acc,v,acc+v))                  -- تراكمي
=BYROW(B2:F100,LAMBDA(r,MAX(r)))                      -- أقصى كل صف
=MAKEARRAY(5,5,LAMBDA(r,c,r*c))                       -- جدول ضرب
=LET(d,TEXTSPLIT(A2,","),TEXTJOIN("؛",TRUE,TRIM(d)))  -- تنظيف قائمة
=TOCOL(B2:F20,1)                                      -- تسطيح بلا فراغات
=VSTACK(Jan!A2:C50,Feb!A2:C50,Mar!A2:C50)             -- دمج أوراق
=GROUPBY(tbl[الفرع],tbl[المبلغ],SUM)                   -- (365 الأحدث) تجميع حي
```
- `#SPILL!` = خلايا مشغولة تحت الصيغة؛ أفرغها. مرجع المنسكب: `=SUM(A2#)`.
- لا دوال متقلبة (OFFSET/INDIRECT/NOW) في الملفات الكبيرة.
- للمشاركة مع Excel 2016/2019: لا FILTER/UNIQUE/SORT/LAMBDA؛ وثّق الحد الأدنى للإصدار في Docs.

## Office Scripts (TypeScript) عند الحاجة لتفاعل
```ts
function main(workbook: ExcelScript.Workbook) {
  const ws = workbook.getWorksheet("Data");
  const used = ws.getUsedRange();
  used.getFormat().autofitColumns();
  ws.getRange("A1").getEntireRow().getFormat().getFont().setBold(true);
}
```
يُشغَّل من Automate وفي Power Automate؛ لا يحتاج VBA ولا يُحظر كماكرو.

## VBA الأدنى (فقط حين لا بديل)
```vba
Sub RefreshAllAndSave()
    ThisWorkbook.RefreshAll
    Application.CalculateFull
    ThisWorkbook.Save
End Sub
```
احفظ كـ .xlsm، وقّع الماكرو، لا تخزّن كلمات مرور أو مسارات شخصية في الكود.

## Python في إكسل
`=PY(` ثم `df = xl("tblSales[#All]", headers=True); df.groupby("الفرع")["المبلغ"].sum()`؛ pandas/statsmodels للإحصاء؛ المخرج يعود كقيمة أو كائن. يحتاج 365 مع الميزة مفعّلة.
