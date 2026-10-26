# وصفات Power Query (M) للأتمتة

## المبادئ
- كل خطوة مسمّاة بما تفعله (بالعربية أو الإنجليزية الواضحة) لا `Changed Type1`.
- المعاملات في جدول `Parameters` (مسار الملف، السنة، الفرع) تُقرأ بـ `Excel.CurrentWorkbook(){[Name="Parameters"]}[Content]`؛ لا مسارات مكتوبة داخل الكود.
- الاستعلامات الوسيطة بلا تحميل (Enable load = off) وتُجمَّع في مجلد `Staging`.
- اجعل العمليات القابلة للطيّ (تصفية، اختيار أعمدة) أولاً عند الاتصال بقواعد بيانات لتُدفع إلى المصدر (View Native Query لا يكون رمادياً).
- الأنواع تُحدَّد مرة واحدة في النهاية؛ `Table.TransformColumnTypes` بثقافة `"ar-SA"` أو `"en-US"` حسب تنسيق الأرقام.
- لا تعتمد على ترتيب الأعمدة؛ اختر بالاسم.

## الوصفات
```m
// 1) قراءة كل ملفات مجلد ودمجها (نفس البنية)
let
  Params = Excel.CurrentWorkbook(){[Name="Parameters"]}[Content],
  Folder = Params{0}[FolderPath],
  Files = Folder.Files(Folder),
  Xlsx = Table.SelectRows(Files, each Text.EndsWith([Name], ".xlsx") and not Text.StartsWith([Name], "~$")),
  Data = Table.AddColumn(Xlsx, "Data", each Excel.Workbook([Content], true){[Item="Data", Kind="Sheet"]}[Data]),
  Expanded = Table.ExpandTableColumn(Table.SelectColumns(Data, {"Name", "Data"}), "Data", Table.ColumnNames(Data{0}[Data])),
  Typed = Table.TransformColumnTypes(Expanded, {{"التاريخ", type date}, {"المبلغ", type number}}, "ar-SA")
in Typed

// 2) إلغاء التدوير (جدول عريض بأشهر أعمدة → طويل)
let
  Src = Excel.CurrentWorkbook(){[Name="tblWide"]}[Content],
  Unpivoted = Table.UnpivotOtherColumns(Src, {"الفرع", "البند"}, "الشهر", "القيمة"),
  Typed = Table.TransformColumnTypes(Unpivoted, {{"القيمة", type number}})
in Typed

// 3) دمج بمفاتيح منظّفة (TRIM/UPPER) ومطابقة غير حسّاسة
let
  A = Table.TransformColumns(tblCustomers, {{"الاسم", each Text.Upper(Text.Trim(_)), type text}}),
  B = Table.TransformColumns(tblOrders, {{"العميل", each Text.Upper(Text.Trim(_)), type text}}),
  Joined = Table.NestedJoin(B, {"العميل"}, A, {"الاسم"}, "Cust", JoinKind.LeftOuter),
  Expanded = Table.ExpandTableColumn(Joined, "Cust", {"المدينة", "الفئة"}),
  Unmatched = Table.SelectRows(Expanded, each [المدينة] = null)   // راجع غير المطابق قبل التسليم
in Expanded

// 4) أرقام عربية-هندية وفواصل عربية → أرقام
let
  Fix = (t as nullable text) as nullable number =>
    let digits = List.Zip({{"٠","١","٢","٣","٤","٥","٦","٧","٨","٩","٬","٫"}, {"0","1","2","3","4","5","6","7","8","9","",""}}),
        s = List.Accumulate(digits, t ?? "", (acc, p) => Text.Replace(acc, p{0}, p{1}))
    in try Number.From(s, "en-US") otherwise null,
  Out = Table.TransformColumns(Src, {{"المبلغ", Fix, type number}})
in Out

// 5) تقويم التواريخ (جدول تاريخ لـ DAX)
let
  Start = #date(2024,1,1), End = #date(2026,12,31),
  Dates = List.Dates(Start, Duration.Days(End - Start) + 1, #duration(1,0,0,0)),
  T = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}),
  T1 = Table.AddColumn(T, "Year", each Date.Year([Date]), Int64.Type),
  T2 = Table.AddColumn(T1, "Month", each Date.Month([Date]), Int64.Type),
  T3 = Table.AddColumn(T2, "MonthName", each Date.ToText([Date], "MMMM", "ar-SA"), type text),
  T4 = Table.AddColumn(T3, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
  T5 = Table.TransformColumnTypes(T4, {{"Date", type date}})
in T5

// 6) إزالة التكرار بذكاء: الأحدث لكل مفتاح
let
  Sorted = Table.Sort(Src, {{"UpdatedAt", Order.Descending}}),
  Buffered = Table.Buffer(Sorted),            // يثبّت الترتيب قبل Distinct
  Dedup = Table.Distinct(Buffered, {"CustomerID"})
in Dedup

// 7) دالة مخصصة قابلة لإعادة الاستخدام
(tbl as table, col as text) as table =>
  Table.AddColumn(tbl, col & "_Clean", each Text.Proper(Text.Trim(Record.Field(_, col))), type text)
```

## التحديث والنشر
- Data → Queries & Connections → Properties: تحديث عند الفتح، وكل N دقيقة، وتعطيل التحديث بالخلفية للتسلسل.
- تحويل ملف .xlsx الناتج إلى قالب: احذف البيانات واحتفظ بالاستعلامات؛ غيّر Parameters فقط.
- الأخطاء: `Expression.Error: The column 'X' wasn't found` = تغيّر اسم عمود في المصدر؛ أضف خطوة إعادة تسمية مرنة أو `Table.ColumnNames` ديناميكياً. `DataFormat.Error` = نوع بيانات؛ حوّل بالثقافة الصحيحة. بطء = لا طيّ؛ انقل التصفية قبل الدمج و`Table.Buffer` للجداول الصغيرة المرجعية.

## متى لا Power Query
- حسابات صفّية بسيطة → صيغة/LAMBDA.
- تجميعات على نموذج بيانات بعلاقات → DAX.
- تفاعل مستخدم (أزرار، نماذج) → Office Scripts/VBA.
- إحصاء وتعلّم آلة → Python في إكسل أو دفتر خارجي.
