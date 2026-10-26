# أنماط DAX (Power Pivot / Power BI)

## القواعد
- **القياسات لا الأعمدة المحسوبة** للتجميعات (الأعمدة المحسوبة تُخزَّن وتُقيَّم صفاً صفاً؛ القياسات تُقيَّم في سياق التصفية).
- جدول تاريخ مُعلَّم (Mark as Date Table) متصل بكل جداول الحقائق؛ بلا فجوات.
- `VAR` لتسمية الخطوات والقراءة؛ `DIVIDE` بدل `/`؛ `CALCULATE` هو المحرّك.
- نموذج نجمي: حقائق في المنتصف وأبعاد حولها؛ علاقات واحد-إلى-كثير باتجاه واحد.

## المكتبة
```dax
Total Sales := SUM ( Sales[Amount] )
Orders := COUNTROWS ( Sales )
Avg Order := DIVIDE ( [Total Sales], [Orders] )

-- نسبة من الإجمالي (إزالة تصفية البُعد)
Sales % of Total := DIVIDE ( [Total Sales], CALCULATE ( [Total Sales], REMOVEFILTERS ( Product ) ) )

-- الزمن
Sales YTD := TOTALYTD ( [Total Sales], 'Date'[Date] )
Sales LY := CALCULATE ( [Total Sales], SAMEPERIODLASTYEAR ( 'Date'[Date] ) )
Sales YoY % := DIVIDE ( [Total Sales] - [Sales LY], [Sales LY] )
Sales Prev Month := CALCULATE ( [Total Sales], DATEADD ( 'Date'[Date], -1, MONTH ) )
Rolling 3M := CALCULATE ( [Total Sales], DATESINPERIOD ( 'Date'[Date], MAX ( 'Date'[Date] ), -3, MONTH ) )

-- عملاء نشطون (جدد ومتكررون)
Active Customers := DISTINCTCOUNT ( Sales[CustomerID] )
New Customers :=
VAR CurrentCustomers = VALUES ( Sales[CustomerID] )
VAR PastCustomers = CALCULATETABLE ( VALUES ( Sales[CustomerID] ), FILTER ( ALL ( 'Date' ), 'Date'[Date] < MIN ( 'Date'[Date] ) ) )
RETURN COUNTROWS ( EXCEPT ( CurrentCustomers, PastCustomers ) )

-- ترتيب وأعلى N
Product Rank := RANKX ( ALL ( Product[Name] ), [Total Sales], , DESC, DENSE )
Top 5 Sales := CALCULATE ( [Total Sales], TOPN ( 5, ALL ( Product[Name] ), [Total Sales] ) )

-- تجميع آمن مع شروط
Sales Riyadh := CALCULATE ( [Total Sales], Customer[City] = "الرياض" )
Sales High Value := CALCULATE ( [Total Sales], FILTER ( Sales, Sales[Amount] > 1000 ) )   -- FILTER على الجدول فقط عند الضرورة

-- التباين مقابل الموازنة
Budget := SUM ( Budget[Amount] )
Variance := [Total Sales] - [Budget]
Variance % := DIVIDE ( [Variance], [Budget] )
Variance Flag := IF ( ABS ( [Variance %] ) > 0.1, "⚠", "" )

-- ما-إذا (معامل من جدول What-If)
Price Uplift := SELECTEDVALUE ( 'Uplift'[Uplift], 0 )
Sales Scenario := SUMX ( Sales, Sales[Qty] * Sales[Price] * ( 1 + [Price Uplift] ) )
```

## أخطاء شائعة
| العرض | السبب | الحل |
|---|---|---|
| إجمالي الصفوف ≠ مجموع الصفوف | قياس بسياق تصفية غير جمعي (نسب، DISTINCTCOUNT) | `SUMX ( VALUES ( dim ), [measure] )` للإجمالي الجمعي |
| الزمن يعيد فراغاً | جدول التاريخ غير مُعلَّم أو به فجوات | أنشئ التقويم بـ Power Query واعلّمه |
| بطء | أعمدة محسوبة ثقيلة أو FILTER على جداول كبيرة | قياسات + CALCULATE بشروط أعمدة |
| علاقة غامضة | عدة مسارات | USERELATIONSHIP في القياس الذي يحتاج المسار البديل |
