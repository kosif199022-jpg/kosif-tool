# `maps-geo` — البيانات والرسوم والمواقع (62 بطاقة)

> مكتبة بروتوكول USIP v5.5 الكاملة، مولّدة بـ `smart_capabilities.py cards` من `data/powers/maps-geo.json` وقواعد الملاحق A25–A29؛ لا تُحرَّر يدويًا. [الفهرس الرئيسي](../../README.md) · [فصل المجموعة](../../../.claude/skills/kosif-superpowers/references/library/data.md) · [النواة](../../../.claude/skills/kosif-superpowers/PROTOCOL.md)

## الفهرس / contents

- [`MAP-01` هل نحتاج خريطة أصلًا](#map-01--هل-نحتاج-خريطة-أصلًا--map-or-not)
- [`MAP-02` الخريطة الأساسية حسب الغرض](#map-02--الخريطة-الأساسية-حسب-الغرض--basemap-substrate-by-purpose)
- [`MAP-03` اختيار نوع الخريطة الموضوعية](#map-03--اختيار-نوع-الخريطة-الموضوعية--thematic-map-family-choice)
- [`MAP-04` اختيار الإسقاط](#map-04--اختيار-الإسقاط--projection-choice)
- [`MAP-05` تطبيع خرائط التظليل](#map-05--تطبيع-خرائط-التظليل--choropleth-normalization)
- [`MAP-06` استراتيجيات تداخل النقاط](#map-06--استراتيجيات-تداخل-النقاط--point-overlap-strategies)
- [`MAP-07` طبقات تتكبر مع الخريطة وأخرى ثابتة](#map-07--طبقات-تتكبر-مع-الخريطة-وأخرى-ثابتة--map-space-vs-screen-stable-layers)
- [`MAP-08` سجل الإحداثيات والمصادر](#map-08--سجل-الإحداثيات-والمصادر--coordinate--source-ledger)
- [`MAP-09` الخرائط الحساسة والبيانات الإنسانية](#map-09--الخرائط-الحساسة-والبيانات-الإنسانية--sensitive-maps--human-data)
- [`MAP-10` توقيعات حركة الخرائط وضوابطها](#map-10--توقيعات-حركة-الخرائط-وضوابطها--map-motion-signatures--restraint-rules)
- [`MAP-11` محرك واحد لكل لقطة](#map-11--محرك-واحد-لكل-لقطة--one-map-engine-per-shot-chooser)
- [`MAP-12` لوحة خريطة ثابتة للموقع](#map-12--لوحة-خريطة-ثابتة-للموقع--static-locator-map-plate)
- [`MAP-13` MapLibre حتمي بلا واجهة](#map-13--maplibre-حتمي-بلا-واجهة--deterministic-headless-maplibre)
- [`MAP-14` لوحة خريطة مجمّدة ضد الارتعاش](#map-14--لوحة-خريطة-مجمّدة-ضد-الارتعاش--frozen-oversized-plate-anti-shimmer)
- [`MAP-15` خريطة حقيقية مخبوزة مع طبقة متجهات حية](#map-15--خريطة-حقيقية-مخبوزة-مع-طبقة-متجهات-حية--baked-real-basemap-mp4--live-svg-overlay)
- [`MAP-16` Mapbox: كرة وأبنية ثلاثية الأبعاد](#map-16--mapbox-كرة-وأبنية-ثلاثية-الأبعاد--mapbox-globe--3d-buildings)
- [`MAP-17` MapTiler: التحريك فوق طبقات المزود](#map-17--maptiler-التحريك-فوق-طبقات-المزود--maptiler-provider-layer-animation)
- [`MAP-18` طيران فوق التضاريس بـ Cesium](#map-18--طيران-فوق-التضاريس-بـ-cesium--cesium-terrain-flyover)
- [`MAP-19` صور خرائط ثابتة من AWS](#map-19--صور-خرائط-ثابتة-من-aws--amazon-location-static-maps)
- [`MAP-20` أنماط VersaTiles المجانية](#map-20--أنماط-versatiles-المجانية--versatiles-self-hosted-styles)
- [`MAP-21` خطوط SDF والتسميات العربية على خرائط GL](#map-21--خطوط-sdf-والتسميات-العربية-على-خرائط-gl--sdf-glyphs--arabic-labels-on-gl-maps)
- [`MAP-22` تنظيف الخريطة الأساسية](#map-22--تنظيف-الخريطة-الأساسية--basemap-decluttering)
- [`MAP-23` طبقات المزود أم GeoJSON مخصص](#map-23--طبقات-المزود-أم-geojson-مخصص--provider-vectors-vs-custom-geojson)
- [`MAP-24` متى GeoJSON ومتى البلاطات المتجهة](#map-24--متى-geojson-ومتى-البلاطات-المتجهة--geojson-vs-vector-tile-threshold)
- [`MAP-25` خط PMTiles وGeoParquet](#map-25--خط-pmtiles-وgeoparquet--pmtiles--geoparquet-pipeline)
- [`MAP-26` التحليل المكاني بـ DuckDB](#map-26--التحليل-المكاني-بـ-duckdb--duckdb-spatial-analysis)
- [`MAP-27` بيانات Overture Maps المفتوحة](#map-27--بيانات-overture-maps-المفتوحة--overture-maps-open-data)
- [`MAP-28` OSM عبر Overpass لخطوط الأنهار والطرق](#map-28--osm-عبر-overpass-لخطوط-الأنهار-والطرق--osm-via-overpass-for-centerlines)
- [`MAP-29` تجهيز ممر الكاميرا](#map-29--تجهيز-ممر-الكاميرا--camera-corridor-path-preparation)
- [`MAP-30` مرساة التسمية في أبعد نقطة داخلية](#map-30--مرساة-التسمية-في-أبعد-نقطة-داخلية--label-anchor-at-pole-of-inaccessibility)
- [`MAP-31` توحيد أسماء الأماكن العربية](#map-31--توحيد-أسماء-الأماكن-العربية--arabic-place-name-normalisation)
- [`MAP-32` رسم مسار الدائرة العظمى](#map-32--رسم-مسار-الدائرة-العظمى--great-circle-route-draw-on)
- [`MAP-33` رحلة على خريطة حبر قديمة](#map-33--رحلة-على-خريطة-حبر-قديمة--parchment-map-journey)
- [`MAP-34` إسقاط خطوط الطول والعرض على SVG](#map-34--إسقاط-خطوط-الطول-والعرض-على-svg--equirectangular-lonlat--svg-with-latitude-squash)
- [`MAP-35` متتبع مسار بطول القوس مع توقف](#map-35--متتبع-مسار-بطول-القوس-مع-توقف--arc-length-route-follower-with-dwell)
- [`MAP-36` كاميرا الخريطة المائلة 2.5D](#map-36--كاميرا-الخريطة-المائلة-25d--tilted-25d-map-camera)
- [`MAP-37` خط زمني بمحطات وخريطة رحلة](#map-37--خط-زمني-بمحطات-وخريطة-رحلة--milestone-timeline--map-route-mg-045046)
- [`MAP-38` رسم مسار بمحطات تنبثق](#map-38--رسم-مسار-بمحطات-تنبثق--route-line-with-popping-station-dots)
- [`MAP-39` مسار تقدم على جبل](#map-39--مسار-تقدم-على-جبل--progress-path-up-terrain-with-avatar)
- [`MAP-40` خريطة وثائقية](#map-40--خريطة-وثائقية--documentary-map)
- [`MAP-41` رحلة طيران نيويورك–باريس](#map-41--رحلة-طيران-نيويوركباريس--nycparis-flight-block)
- [`MAP-42` أقواس ضوء ترسم بين المدن (3D)](#map-42--أقواس-ضوء-ترسم-بين-المدن-3d--3d-light-arcs-between-cities)
- [`MAP-43` شريط نهر يُرسم ويجري](#map-43--شريط-نهر-يُرسم-ويجري--river-ribbon-reveal--flow)
- [`MAP-44` إضاءة الدول عند وصول النهر](#map-44--إضاءة-الدول-عند-وصول-النهر--river-triggered-country-reveal)
- [`MAP-45` خريطة المملكة التخطيطية بالمناطق](#map-45--خريطة-المملكة-التخطيطية-بالمناطق--schematic-saudi-arabia-map--13-regions-drill-down)
- [`MAP-46` تدرّج الخريطة الأزرق](#map-46--تدرّج-الخريطة-الأزرق--sequential-blue-map-heat-ramp)
- [`MAP-47` خرائط تظليل بكشف متتابع](#map-47--خرائط-تظليل-بكشف-متتابع--choropleth-staggered-reveal-blocks)
- [`MAP-48` خريطة الفقاعات](#map-48--خريطة-الفقاعات--proportional-bubble-map)
- [`MAP-49` خريطة التدفق](#map-49--خريطة-التدفق--origindestination-flow-map)
- [`MAP-50` خريطة سداسية](#map-50--خريطة-سداسية--hex-tile-map)
- [`MAP-51` زووم دولة مع دائرة حمراء](#map-51--زووم-دولة-مع-دائرة-حمراء--country-zoom-with-red-scribble-circle)
- [`MAP-52` علامات وتسميات داخل الخريطة](#map-52--علامات-وتسميات-داخل-الخريطة--map-native-circle--symbol-markers)
- [`MAP-53` رسم خريطة شوارع وإسقاط دبابيس](#map-53--رسم-خريطة-شوارع-وإسقاط-دبابيس--svg-street-map-draw--pin-drop)
- [`MAP-54` خريطة نقاط تجمعات المدن](#map-54--خريطة-نقاط-تجمعات-المدن--dot-cluster-city-map)
- [`MAP-55` خريطة عالم نقطية بكبسولات صور](#map-55--خريطة-عالم-نقطية-بكبسولات-صور--dotted-world-map-with-avatar-pills)
- [`MAP-56` خريطة أعمدة ضوئية](#map-56--خريطة-أعمدة-ضوئية--spike-map)
- [`MAP-57` عناصر خرائط أرشيفية](#map-57--عناصر-خرائط-أرشيفية--archival-map-fragment-collage-props)
- [`MAP-58` كوكب الأرض مع غلاف جوي](#map-58--كوكب-الأرض-مع-غلاف-جوي--procedural-earth-with-atmosphere)
- [`MAP-59` خريطة الأضواء من المدار](#map-59--خريطة-الأضواء-من-المدار--orbit-at-night-lights-map)
- [`MAP-60` كرة أرضية نقطية بإسقاط كروي](#map-60--كرة-أرضية-نقطية-بإسقاط-كروي--orthographic-dot--halftone-globe)
- [`MAP-61` كرة أرضية بأقواس اتصال](#map-61--كرة-أرضية-بأقواس-اتصال--globe-with-great-circle-arcs-wireframe--particle)
- [`MAP-62` كرة غبار مع تسميات](#map-62--كرة-غبار-مع-تسميات--dust-point-cloud-globe-with-leader-labels)

## البطاقات / cards

### `MAP-01` — هل نحتاج خريطة أصلًا / Map or not

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الإحداثيات أو أسماء المناطق وحدها لا تبرر خريطة؛ ارسم خريطة فقط حين يكون الموقع أو الجوار أو الحركة جزءًا من الحجة. / Coordinates or region names alone do not justify a map; map only when position, adjacency or movement is part of the argument.

**متى:** أول سؤال في أي مشهد فيه دول أو مدن / the first question for any shot that names places.

**كيف:** Ranking or precise comparison across named regions → sorted bar or dot plot, optionally with a tiny locator inset (≈15 % of frame) in the corner. Distance, neighbours, routes or spatial clustering carry the story → a real map. Write the choice and the reason into PLAN.md so the next shot does not drift back to a decorative map.

**المعاملات:** map only if position/adjacency/movement matters; else bar + locator inset

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** map or chart · locator inset · هل نحتاج خريطة · مخطط أم خريطة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-01` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/map-or-not.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/references/chart-selection-patterns.md`

#### 7. قدرات قريبة في العائلة

- `MAP-02` الخريطة الأساسية حسب الغرض / Basemap substrate by purpose (documented)
- `MAP-03` اختيار نوع الخريطة الموضوعية / Thematic map family choice (documented)

### `MAP-02` — الخريطة الأساسية حسب الغرض / Basemap substrate by purpose

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر الطبقة الأساسية (طرق، تضاريس، حدود، صور فضائية، محايد، كرة) مما يجب أن يفكر فيه المشاهد، قبل اختيار المكتبة. / Choose the substrate from what the viewer must reason about, before choosing a library.

**متى:** عند كتابة خطة أي لقطة خريطة / when planning any map shot.

**كيف:** Driving, delivery, traffic → road + city basemap. Hiking, flood, wildfire → topographic with hillshade, rivers, contours. Regional comparison → quiet admin boundaries only. Damage or land use → satellite imagery with transparent overlays. Dense events → quiet neutral (grey/dark) map. Globe or 3D only when curvature or depth changes the reading. Name contextual layers separately from thematic layers in the layer list.

**المعاملات:** 6 substrates: road · topo · admin · imagery · neutral · globe

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** basemap · substrate · hillshade · satellite · خريطة أساسية · تضاريس

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-02` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/adaptive-basemaps-and-layer-stacks.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-01` هل نحتاج خريطة أصلًا / Map or not (documented)
- `MAP-03` اختيار نوع الخريطة الموضوعية / Thematic map family choice (documented)
- `MAP-04` اختيار الإسقاط / Projection choice (documented)

### `MAP-03` — اختيار نوع الخريطة الموضوعية / Thematic map family choice

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر بين التظليل والرموز النسبية والتجميع والتدفق والسداسيات والكثافة والرحلات المتحركة حسب طبيعة البيانات المكانية. / Pick choropleth, proportional symbol, cluster, flow, hex/tile, density or trip animation by the data's spatial nature.

**متى:** حين تتحول البيانات إلى خريطة / when data becomes a map.

**كيف:** Normalised area rates → choropleth (MAP-05). Point magnitude → proportional symbols scaled by AREA (r = √v), not radius. Dense points → clusters, bins or heat. Real movement → flow map or animated trips. Noisy small areas → hex or tile grid (MAP-50). Continuous field → raster/density. One family per shot; switch families with a cut or morph, never overlay two.

**المعاملات:** r = sqrt(value) for symbols

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** choropleth · proportional symbol · flow · hex · تظليل · رموز نسبية · تدفق

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-03` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/choropleths-symbols-and-flows.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-01` هل نحتاج خريطة أصلًا / Map or not (documented)
- `MAP-02` الخريطة الأساسية حسب الغرض / Basemap substrate by purpose (documented)
- `MAP-04` اختيار الإسقاط / Projection choice (documented)
- `MAP-05` تطبيع خرائط التظليل / Choropleth normalization (documented)

### `MAP-04` — اختيار الإسقاط / Projection choice

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الإسقاط يقرر ما يتشوه (المساحة أو المسافة أو الاتجاه)، فاختره عمدًا للادعاء. / The projection decides what is distorted, so choose it deliberately for the claim.

**متى:** قبل رسم أي خريطة عالم أو قارة / before any world or continental map.

**كيف:** Equal-area (d3.geoEqualEarth, geoConicEqualArea) for choropleths and area comparisons. Web Mercator only for tiled slippy context — it inflates high latitudes (Greenland looks like Africa). Orthographic for ‘whole planet’ globe moments (MAP-58…62). Conic conformal for mid-latitude countries (the spain-map block uses it). Note the projection in the source line. Engine: `npm i d3@7.9.0` (installable here).

**المعاملات:** equal-area for areas; Mercator only for tiles; orthographic for globes

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** projection · equal earth · mercator · orthographic · إسقاط

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-04` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/projections-and-normalization.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/deckgl-d3-geo-stack-selection.md`

#### 7. قدرات قريبة في العائلة

- `MAP-02` الخريطة الأساسية حسب الغرض / Basemap substrate by purpose (documented)
- `MAP-03` اختيار نوع الخريطة الموضوعية / Thematic map family choice (documented)
- `MAP-05` تطبيع خرائط التظليل / Choropleth normalization (documented)
- `MAP-06` استراتيجيات تداخل النقاط / Point overlap strategies (documented)

### `MAP-05` — تطبيع خرائط التظليل / Choropleth normalization

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** لوّن المناطق بالمعدلات أو النسب لا بالأعداد الخام، بمخطط تسلسلي مصنَّف. / Fill regions with rates or shares, never raw counts, with a classed sequential scheme.

**متى:** أي خريطة تظليل / every choropleth.

**كيف:** Divide by population, area or the right denominator. ColorBrewer sequential at its supported class count, 5–7 classes; diverging only around a meaningful midpoint (0, national average). Compact legend with units beside the map. If huge empty regions dominate (Rub' al Khali, Sahara), consider a tile/hex cartogram (MAP-50). The owner's own 5-step blue ramp is MAP-46.

**المعاملات:** 5–7 classes; sequential; legend with units

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** normalization · colorbrewer · classes · تطبيع · تظليل

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-05` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/projections-and-normalization.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/choropleths-symbols-and-flows.md`
- `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/references/color_palettes.md`

#### 7. قدرات قريبة في العائلة

- `MAP-03` اختيار نوع الخريطة الموضوعية / Thematic map family choice (documented)
- `MAP-04` اختيار الإسقاط / Projection choice (documented)
- `MAP-06` استراتيجيات تداخل النقاط / Point overlap strategies (documented)
- `MAP-07` طبقات تتكبر مع الخريطة وأخرى ثابتة / Map-space vs screen-stable layers (documented)

### `MAP-06` — استراتيجيات تداخل النقاط / Point overlap strategies

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تجميع بعدّاد للمعاينات الكثيفة، وتفريق (spiderfy) لنقاط قليلة متداخلة، ونقطة مرساة صغيرة داخل الهالات الكبيرة. / Count clusters for dense previews, spiderfy for a few overlaps, and a crisp anchor dot inside big halos.

**متى:** مدن متجاورة أو أحداث كثيرة في مكان واحد / neighbouring cities or many events at one place.

**كيف:** Cluster badges that dissolve as the camera zooms; spiderfy when the overlap count is small (≤8); always keep a crisp exact-location dot drawn above rings and halos; draw smaller symbols above larger ones. For video, step through points one at a time with a moving highlight instead of showing all at once.

**المعاملات:** spiderfy ≤ ~8; small above large; anchor dot on top

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cluster · spiderfy · overlap · تجميع · تداخل

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-06` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/point-overlap-strategies.md`

#### 7. قدرات قريبة في العائلة

- `MAP-04` اختيار الإسقاط / Projection choice (documented)
- `MAP-05` تطبيع خرائط التظليل / Choropleth normalization (documented)
- `MAP-07` طبقات تتكبر مع الخريطة وأخرى ثابتة / Map-space vs screen-stable layers (documented)
- `MAP-08` سجل الإحداثيات والمصادر / Coordinate & source ledger (documented)

### `MAP-07` — طبقات تتكبر مع الخريطة وأخرى ثابتة / Map-space vs screen-stable layers

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أثناء الزووم تتكبر الجغرافيا والمساحات الحقيقية، أما التسميات والدبابيس والحدود فتحافظ على حجمها على الشاشة. / During a zoom geography scales, but labels, pins, badges and outline strokes keep screen size.

**متى:** كل زووم أو دفع كاميرا على خريطة / every zoom or push-in on a map.

**كيف:** Scale polygons, rivers, buffers and impact radii with the camera; keep city dots, labels, callouts and border strokes constant — SVG `vector-effect: non-scaling-stroke`, or a separate HTML overlay that only translates. Change label density in steps (country → region → city), never continuously.

**المعاملات:** vector-effect: non-scaling-stroke; label density in steps

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** zoom · non-scaling-stroke · labels · زووم · تسميات ثابتة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-07` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/multiscale-symbols-and-zoom-behavior.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/references/svg-polish-and-crispness.md`

#### 7. قدرات قريبة في العائلة

- `MAP-05` تطبيع خرائط التظليل / Choropleth normalization (documented)
- `MAP-06` استراتيجيات تداخل النقاط / Point overlap strategies (documented)
- `MAP-08` سجل الإحداثيات والمصادر / Coordinate & source ledger (documented)
- `MAP-09` الخرائط الحساسة والبيانات الإنسانية / Sensitive maps & human data (documented)

### `MAP-08` — سجل الإحداثيات والمصادر / Coordinate & source ledger

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** قبل بناء فيلم خريطة، اكتب لكل طبقة مصدرها وترخيصها وتاريخها ونظام إحداثياتها وهل هي مقاسة أم تخطيطية. / Before a map film, log each layer's source, license, date, CRS and whether it is measured or schematic.

**متى:** قبل أول إطار، وفي TEST_REPORT.md / before frame one and in TEST_REPORT.md.

**كيف:** Per layer: source URL, license/attribution, update date, units, CRS, antimeridian policy, gaps. Per rendered layer: who owns the projection. Spot-check ≥3 known places (e.g. Mecca 39.83 E 21.42 N, Cairo 31.24 E 30.04 N, Casablanca −7.59 E 33.57 N) so markers and basemap align. GeoJSON/Turf order is ALWAYS [longitude, latitude].

**المعاملات:** [lng, lat]; ≥3 spot checks

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** ledger · CRS · lng lat · attribution · مصادر · إحداثيات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-08` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/source-method-and-coordinate-ledger.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md`

#### 7. قدرات قريبة في العائلة

- `MAP-06` استراتيجيات تداخل النقاط / Point overlap strategies (documented)
- `MAP-07` طبقات تتكبر مع الخريطة وأخرى ثابتة / Map-space vs screen-stable layers (documented)
- `MAP-09` الخرائط الحساسة والبيانات الإنسانية / Sensitive maps & human data (documented)
- `MAP-10` توقيعات حركة الخرائط وضوابطها / Map motion signatures & restraint rules (documented)

### `MAP-09` — الخرائط الحساسة والبيانات الإنسانية / Sensitive maps & human data

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خرائط النزاع والنزوح والكوارث والحدود المتنازع عليها تحتاج حالات مؤرخة ومصادر وضبطًا للنبرة. / Conflict, displacement, disaster or disputed-border maps need dated states, sourcing and restraint.

**متى:** أي خريطة عن بشر متضررين أو حدود متنازع عليها / any map about harmed people or disputed borders.

**كيف:** Show the date of each map state and the source hierarchy; style measured / estimated / schematic layers differently (solid / dashed / hatched). No particle flows and no team-colour framing for human harm. Keep caveats next to the numbers. Record source and effective date of any disputed border used; for Arab audiences, check which border convention the client expects before rendering.

**المعاملات:** solid=measured, dashed=estimated, hatched=schematic

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** sensitive · disputed border · conflict · حدود متنازع عليها · نزوح

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-09` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/adaptive-basemaps-and-layer-stacks.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md`

#### 7. قدرات قريبة في العائلة

- `MAP-07` طبقات تتكبر مع الخريطة وأخرى ثابتة / Map-space vs screen-stable layers (documented)
- `MAP-08` سجل الإحداثيات والمصادر / Coordinate & source ledger (documented)
- `MAP-10` توقيعات حركة الخرائط وضوابطها / Map motion signatures & restraint rules (documented)
- `MAP-11` محرك واحد لكل لقطة / One map engine per shot (chooser) (documented)

### `MAP-10` — توقيعات حركة الخرائط وضوابطها / Map motion signatures & restraint rules

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 (HyperFrames). |

**ما هي:** مفردات الحركة المعتمدة للخرائط: تعبئة الدول بالتتابع، إسقاط دبوس مع حلقة نبض، رسم القوس مع طائر يتبعه، كشف التظليل، وزووم عبر viewBox — بلا توهجات وجسيمات زخرفية. / The approved motion vocabulary: country fill stagger, pin drop + pulse ring, arc draw-on + flyer, choropleth reveal, viewBox zoom — no decorative glows or particles.

**متى:** عند تصميم حركة أي لقطة خريطة متجهية / when choreographing any vector map shot.

**كيف:** Two lanes: vector (D3 + TopoJSON) or baked basemap (MapLibre, MAP-15). Signatures: country fill stagger 40–80 ms; pin drop + one pulse ring; arc `stroke-dashoffset` draw-on with a flyer riding the head; choropleth reveal; viewBox zoom. Rules: offset labels from their dots; filter far overseas territories out of the frame; no decorative glows, particles or lens flares; never use `tl.call()` for stateful updates (seek breaks) — tween a proxy value instead. Hand-author geo-highlight / geo-flow / flag-borders when the catalog lacks them.

**المعاملات:** stagger 40–80 ms; dashoffset arcs; no tl.call

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** signatures · pin drop · stagger · restraint · توقيعات حركة · دبوس

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-10` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/module.md`
- `kosif-one/vendor/hyperframes/skills/motion-graphics/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-08` سجل الإحداثيات والمصادر / Coordinate & source ledger (documented)
- `MAP-09` الخرائط الحساسة والبيانات الإنسانية / Sensitive maps & human data (documented)
- `MAP-11` محرك واحد لكل لقطة / One map engine per shot (chooser) (documented)
- `MAP-12` لوحة خريطة ثابتة للموقع / Static locator map plate (documented)

### `MAP-11` — محرك واحد لكل لقطة / One map engine per shot (chooser)

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** اختر تقنية خريطة واحدة لكل لقطة: صورة ثابتة، D3/SVG، MapLibre، Mapbox، MapTiler، أو Cesium. / Pick exactly one map technique per shot.

**متى:** عند تقسيم السكربت إلى لقطات / when breaking the script into shots.

**كيف:** \| need \| engine \| cost here \| \|---\|---\|---\| \| location context only \| static plate (MAP-12) \| free, most deterministic \| \| editorial vector map, Arabic labels, our HTML renderer \| D3 geo + TopoJSON SVG \| 📦 `npm i d3@7.9.0 topojson-client@3.1.0 world-atlas@2.0.2` \| \| real vector/satellite basemap, free \| MapLibre (MAP-13/14) \| 📦 no key; OpenFreeMap reachable \| \| globe when zoomed out, 3D buildings \| Mapbox (MAP-16) \| 🔑 token \| \| draw over provider borders/rivers \| MapTiler (MAP-17) \| 🔑 key \| \| terrain & city flyover \| Cesium (MAP-18) \| 🔑 ion token \| \| GPU trips/arcs/hexagons \| deck.gl \| not probed \| \| raster tiles + GeoJSON, simple \| Leaflet \| 📦 `leaflet@1.9.4` \| All are driven per frame (Remotion `useCurrentFrame` or our seekable HTML timeline), never by wall-clock animation.

**المعاملات:** 1 engine/shot

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** engine · maplibre · mapbox · cesium · d3 · محرك خرائط

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-11` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/SKILL.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/static-map/TECHNIQUE.md`
- `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/slippy-map-and-product-stack-selection.md`
- `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/module.md`

#### 7. قدرات قريبة في العائلة

- `MAP-09` الخرائط الحساسة والبيانات الإنسانية / Sensitive maps & human data (documented)
- `MAP-10` توقيعات حركة الخرائط وضوابطها / Map motion signatures & restraint rules (documented)
- `MAP-12` لوحة خريطة ثابتة للموقع / Static locator map plate (documented)
- `MAP-13` MapLibre حتمي بلا واجهة / Deterministic headless MapLibre (install)

### `MAP-12` — لوحة خريطة ثابتة للموقع / Static locator map plate

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** صورة خريطة مُصدَّرة مسبقًا بنسبة الإطار النهائية، فوقها دبابيس وتسميات وأسهم متحركة؛ أرخص لقطة خريطة وأكثرها حتمية. / A pre-exported map image at final aspect with animated pins, labels and arrows on top.

**متى:** حين تكفي «أين» بلا تنقل حقيقي / when ‘where’ is enough.

**كيف:** Export the map at ≥ output size and exact aspect (1920×1080, or 3840×2160 if you push in), put it in public/ (Remotion) or next to the page (render_html.cjs), show it full-frame, then animate markers, route SVG paths and Arabic labels as normal layers (Arabic shaping stays in HTML — see ARAB chapter). Push-in 1.00→1.08 over 4–6 s. Keep the tile provider's attribution (‘© OpenStreetMap contributors’) in frame or credits; respect the OSM tile usage policy (a few tiles by hand, never bulk scraping).

**المعاملات:** plate ≥ output px; push-in 1.00→1.08

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** static map · plate · locator · خريطة ثابتة · لوحة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-12` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/static-map/TECHNIQUE.md`

#### 7. قدرات قريبة في العائلة

- `MAP-10` توقيعات حركة الخرائط وضوابطها / Map motion signatures & restraint rules (documented)
- `MAP-11` محرك واحد لكل لقطة / One map engine per shot (chooser) (documented)
- `MAP-13` MapLibre حتمي بلا واجهة / Deterministic headless MapLibre (install)
- `MAP-14` لوحة خريطة مجمّدة ضد الارتعاش / Frozen oversized plate (anti-shimmer) (install)

### `MAP-13` — MapLibre حتمي بلا واجهة / Deterministic headless MapLibre

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | maplibre-gl BSD-3-Clause; Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier. |

**ما هي:** إعداد MapLibre ليعطي نفس الإطار في كل رندر داخل متصفح بلا واجهة. / MapLibre configured to give the same frame on every headless render.

**متى:** أي لقطة بخريطة GL حقيقية / any shot with a real GL basemap.

**كيف:** `interactive:false, fadeDuration:0, preserveDrawingBuffer:true`; Chromium flag `--gl=angle` (Remotion: `chromiumOptions.gl='angle'`); on frame 0 `map.jumpTo(camera)` then wait for the `idle` event before capturing (Remotion: `delayRender`/`continueRender`). Coordinates `[lng,lat]`. Free styles: OpenFreeMap (`https://tiles.openfreemap.org/styles/liberty` — host reachable here). Never call `flyTo`/`easeTo` — they run on wall-clock time. const map = new maplibregl.Map({ container, style, interactive: false, fadeDuration: 0, preserveDrawingBuffer: true, ...cameraAt(0) }); const ready = new Promise(r => map.once('idle', r)); // capture only after this

**المعاملات:** fadeDuration 0; --gl=angle; wait 'idle'

**التثبيت:** npm i maplibre-gl@6.14.0 @turf/turf@7.4.0

**الوسوم:** maplibre · headless · deterministic · idle · حتمي

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:remotion` ← npm ls remotion أو وجود node_modules/remotion
- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-13` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/SKILL.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/render-stability.md`

#### 7. قدرات قريبة في العائلة

- `MAP-11` محرك واحد لكل لقطة / One map engine per shot (chooser) (documented)
- `MAP-12` لوحة خريطة ثابتة للموقع / Static locator map plate (documented)
- `MAP-14` لوحة خريطة مجمّدة ضد الارتعاش / Frozen oversized plate (anti-shimmer) (install)
- `MAP-15` خريطة حقيقية مخبوزة مع طبقة متجهات حية / Baked real basemap MP4 + live SVG overlay (install)

### `MAP-14` — لوحة خريطة مجمّدة ضد الارتعاش / Frozen oversized plate (anti-shimmer)

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier. |

**ما هي:** استدعاء jumpTo في كل إطار يجعل الصور الفضائية والظلال ترتعش في الرندر؛ ارندر الخريطة مرة واحدة كبيرة وحرّكها بـ CSS. / Per-frame jumpTo shimmers; render the map once oversized and move it with CSS.

**متى:** أي كاميرا متحركة فوق خريطة GL / any moving camera over a GL map.

**كيف:** Render the basemap once at the largest zoom any waypoint reaches, centred on the route's extent midpoint, in an oversized container; keep pitch/bearing constant. Per frame: `scale = 2^(zoom − baseZoom)` (must stay ≤ 1) and translate so the target centre sits mid-frame; apply the identical transform to every HTML label. Keep animating GeoJSON data and paint properties inside the map. Plate sizes: 1920×1080 → 3840×2160; 1080×1920 → ~2700×3840; max side 4096 px. Split very long routes into two plates joined by an editorial transition. // plate rendered once at baseZoom (the deepest zoom of the shot) const s = 2 ** (zoomAt(f) - baseZoom); // ≤ 1 const [px, py] = project(centerAt(f)); // plate pixels stage.style.transform = `translate(${W/2 - px*s}px, ${H/2 - py*s}px) scale(${s})`; // same for labels

**المعاملات:** scale = 2^(zoom−baseZoom) ≤ 1; plate 3840×2160; max 4096 px

**التثبيت:** npm i maplibre-gl@6.14.0

**الوسوم:** shimmer · plate · css transform · ارتعاش · لوحة مجمدة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-14` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/references/render-stability.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/references/render-stability.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-12` لوحة خريطة ثابتة للموقع / Static locator map plate (documented)
- `MAP-13` MapLibre حتمي بلا واجهة / Deterministic headless MapLibre (install)
- `MAP-15` خريطة حقيقية مخبوزة مع طبقة متجهات حية / Baked real basemap MP4 + live SVG overlay (install)
- `MAP-16` Mapbox: كرة وأبنية ثلاثية الأبعاد / Mapbox globe & 3D buildings (key)

### `MAP-15` — خريطة حقيقية مخبوزة مع طبقة متجهات حية / Baked real basemap MP4 + live SVG overlay

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 script; Esri World Imagery and CARTO tiles carry their own terms of use and mandatory attribution. |

**ما هي:** يقود MapLibre في Chrome بلا واجهة ليسجّل الخلفية الفضائية أو الداكنة وحدها كفيديو (زووم ثم ثبات)، ويصدّر حدود كل دولة كمسارات SVG لرسمها وتلوينها فوقه. / Bakes only the satellite/dark basemap to MP4 and exports each country's projected border as SVG coords for draw-on, fills, labels and pins.

**متى:** لقطة صور فضائية حقيقية مع حدود مرسومة / a real satellite shot with drawn borders.

**كيف:** `NAME=br-ar STYLE=satellite COUNTRIES='Brazil:#22d3ee,Argentina:#f59e0b' CENTER='-60,-25' ZSTART=2.4 ZEND=3.4 FPS=30 DUR=5 node bake-basemap.mjs` → frames waited on map idle each frame, zoom→hold with easeInOutCubic; encode all-intra (`-g 1`) so seeking is exact; overlay `<NAME>-coords.json` borders with dashoffset draw-on, flag/colour fills, pins and callout cards in HTML. Raster tiles tileSize 256; world width = 512·2^zoom. Credit ‘Esri, Maxar, Earthstar Geographics’ (satellite) or ‘© CARTO, © OpenStreetMap’ (dark). The script looks for chrome-headless-shell; point it at the Playwright Chromium in /opt/pw-browsers or run `npx puppeteer browsers install chrome-headless-shell`. Esri/CARTO tile hosts were not probed here.

**المعاملات:** ZSTART 2.4 → ZEND 3.4; FPS 30; DUR 5; -g 1

**التثبيت:** npm i maplibre-gl@6.14.0 puppeteer@25.14.0

**الوسوم:** satellite · bake · basemap · border draw · صور فضائية · حدود

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `chromium` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-15` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/bake-basemap.mjs`
- `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/module.md`

#### 7. قدرات قريبة في العائلة

- `MAP-13` MapLibre حتمي بلا واجهة / Deterministic headless MapLibre (install)
- `MAP-14` لوحة خريطة مجمّدة ضد الارتعاش / Frozen oversized plate (anti-shimmer) (install)
- `MAP-16` Mapbox: كرة وأبنية ثلاثية الأبعاد / Mapbox globe & 3D buildings (key)
- `MAP-17` MapTiler: التحريك فوق طبقات المزود / MapTiler provider-layer animation (key)

### `MAP-16` — Mapbox: كرة وأبنية ثلاثية الأبعاد / Mapbox globe & 3D buildings

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Mapbox GL JS v2+ is proprietary (Mapbox Terms of Service); needs a Mapbox access token. Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier. |

**ما هي:** أجمل أنماط افتراضية، كرة أرضية عند الزووم البعيد، ومعالم وأبنية ثلاثية الأبعاد. / Nicer default styles, globe when zoomed out, 3D landmarks.

**متى:** لقطة تنتقل من الكوكب إلى شارع في مدينة / a planet-to-street dive.

**كيف:** Same deterministic rules as MAP-13 (no flyTo; jumpTo + idle) and MAP-14 for shimmer. Projection `globe` at low zoom; `fill-extrusion` for buildings with pitch 45–60°. Route draw-on and markers per MAP-32/MAP-52.

**المعاملات:** pitch 45–60°; globe projection

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** mapbox · globe · 3d buildings · مباني ثلاثية

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-16` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-14` لوحة خريطة مجمّدة ضد الارتعاش / Frozen oversized plate (anti-shimmer) (install)
- `MAP-15` خريطة حقيقية مخبوزة مع طبقة متجهات حية / Baked real basemap MP4 + live SVG overlay (install)
- `MAP-17` MapTiler: التحريك فوق طبقات المزود / MapTiler provider-layer animation (key)
- `MAP-18` طيران فوق التضاريس بـ Cesium / Cesium terrain flyover (key)

### `MAP-17` — MapTiler: التحريك فوق طبقات المزود / MapTiler provider-layer animation

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Needs a MapTiler API key (free tier exists; commercial terms apply). Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier. |

**ما هي:** ارسم وظلّل فوق حدود وأنهار وتسميات المزود نفسه. / Draw and tint over the provider's own borders, rivers and labels.

**متى:** خريطة شرح تعتمد على حدود رسمية وأنهار حقيقية / an explainer built on official borders and real rivers.

**كيف:** Load a MapTiler vector style; filter exact `source-layer`s (waterway, boundary, transportation) and animate only paint (opacity, colour, width) — tiles split features, so start-to-end draws need baked GeoJSON (MAP-23). Pair with decluttering (MAP-22) and the river-triggered reveal (MAP-44). Tokens and timings in `assets/tokens.ts`.

**المعاملات:** paint-only animation on provider layers

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** maptiler · vector tiles · borders · rivers

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-17` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/assets/tokens.ts`

#### 7. قدرات قريبة في العائلة

- `MAP-15` خريطة حقيقية مخبوزة مع طبقة متجهات حية / Baked real basemap MP4 + live SVG overlay (install)
- `MAP-16` Mapbox: كرة وأبنية ثلاثية الأبعاد / Mapbox globe & 3D buildings (key)
- `MAP-18` طيران فوق التضاريس بـ Cesium / Cesium terrain flyover (key)
- `MAP-19` صور خرائط ثابتة من AWS / Amazon Location static maps (key)

### `MAP-18` — طيران فوق التضاريس بـ Cesium / Cesium terrain flyover

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | CesiumJS Apache-2.0, but world terrain / 3D Tiles stream from Cesium ion and need an ion access token. Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier. |

**ما هي:** طيران سينمائي فوق تضاريس ثلاثية الأبعاد ومدن («محاكي طيران»). / Cinematic flight over 3D terrain and cities.

**متى:** وادٍ أو مضيق أو جبل يجب أن يُرى عمقه / a gorge, valley or mountain whose depth matters.

**كيف:** Camera follows a pre-smoothed corridor (MAP-29 — proven here) at constant height; heading from the path tangent, small banking from curvature; wait for terrain tiles each frame before capture. Path assets: `assets/cesium-path.json`, `city-path.json`, `flight-path.ts`.

**المعاملات:** camera on smoothed 0.1 km corridor

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** cesium · terrain · flyover · 3d tiles · تضاريس · طيران

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-18` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/TECHNIQUE.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-troubleshooting.md`

#### 7. قدرات قريبة في العائلة

- `MAP-16` Mapbox: كرة وأبنية ثلاثية الأبعاد / Mapbox globe & 3D buildings (key)
- `MAP-17` MapTiler: التحريك فوق طبقات المزود / MapTiler provider-layer animation (key)
- `MAP-19` صور خرائط ثابتة من AWS / Amazon Location static maps (key)
- `MAP-20` أنماط VersaTiles المجانية / VersaTiles self-hosted styles (install)

### `MAP-19` — صور خرائط ثابتة من AWS / Amazon Location static maps

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 skill text; the service is paid AWS (API key). |

**ما هي:** صور خرائط مُرندرة مسبقًا أو أنماط جاهزة من خدمة مستضافة. / Pre-rendered map images or style descriptors from a hosted service.

**متى:** حين يملك العميل حساب AWS ويريد خرائطه الرسمية / when the client already has AWS and wants its maps.

**كيف:** API key with geo-maps actions; pass `https://maps.geo.{region}.amazonaws.com/v2/styles/Standard/descriptor?key=…` straight to MapLibre with `validateStyle:false`, or call the static-image endpoint for a plate (MAP-12). Keep attribution.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** aws · amazon location · static map

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-19` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/368-amazon-location-service/1365-amazon-location-service/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-17` MapTiler: التحريك فوق طبقات المزود / MapTiler provider-layer animation (key)
- `MAP-18` طيران فوق التضاريس بـ Cesium / Cesium terrain flyover (key)
- `MAP-20` أنماط VersaTiles المجانية / VersaTiles self-hosted styles (install)
- `MAP-21` خطوط SDF والتسميات العربية على خرائط GL / SDF glyphs & Arabic labels on GL maps (install)

### `MAP-20` — أنماط VersaTiles المجانية / VersaTiles self-hosted styles

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مولّدات أنماط MapLibre مجانية بخيار لغة وخطوط SDF. / Free MapLibre style generators with a language option and SDF glyphs.

**متى:** حين تريد مظهرًا داكنًا أو رماديًا جاهزًا بلا مفتاح / a ready dark or grey look without a key.

**كيف:** Styles: colorful, eclipse (dark), graybeard (grayscale), neutrino (minimal blueprint), shadow (hillshade-friendly), satellite overlay; each takes `{language}` (try `ar`). Glyphs `{fontstack}/{range}.pbf` (Fira Sans, Noto Sans, Roboto…). Default tiles at tiles.versatiles.org — that host was NOT probed here; OpenFreeMap (reachable) is the fallback. Verify Arabic glyph ranges and RTL shaping before trusting map-rendered Arabic labels (MAP-21).

**المعاملات:** styles: colorful · eclipse · graybeard · neutrino · shadow · satellite

**التثبيت:** npm i maplibre-gl@6.14.0

**الوسوم:** versatiles · dark map · eclipse · graybeard · نمط خريطة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-20` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2761-charly-versa/10958-versatiles-style/SKILL.md`
- `kosif-atlas/skills/2761-charly-versa/10956-versatiles-fonts/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-18` طيران فوق التضاريس بـ Cesium / Cesium terrain flyover (key)
- `MAP-19` صور خرائط ثابتة من AWS / Amazon Location static maps (key)
- `MAP-21` خطوط SDF والتسميات العربية على خرائط GL / SDF glyphs & Arabic labels on GL maps (install)
- `MAP-22` تنظيف الخريطة الأساسية / Basemap decluttering (install)

### `MAP-21` — خطوط SDF والتسميات العربية على خرائط GL / SDF glyphs & Arabic labels on GL maps

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** MapLibre يحتاج خطوط SDF مقطّعة، والعربية تحتاج إضافة النص من اليمين لليسار — وإلا فالتسميات في HTML. / MapLibre needs SDF glyph PBFs; Arabic needs the RTL text plugin — or put labels in HTML.

**متى:** أي تسمية عربية داخل خريطة GL / any Arabic label inside a GL map.

**كيف:** `style.glyphs = '{fontstack}/{range}.pbf'` from the versatiles-fonts release; call `maplibregl.setRTLTextPlugin(url)` before map creation for Arabic shaping. Safer default for video: hide provider labels (MAP-22) and draw Arabic names as an HTML overlay that shares the plate transform (MAP-14) — full shaping, Ruqaa/Naskh fonts, halo via `text-shadow`.

**المعاملات:** glyphs {fontstack}/{range}.pbf; RTL plugin

**التثبيت:** npm i maplibre-gl@6.14.0

**الوسوم:** sdf · glyphs · rtl · arabic labels · تسميات عربية · خطوط

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-21` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2761-charly-versa/10956-versatiles-fonts/SKILL.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md`

#### 7. قدرات قريبة في العائلة

- `MAP-19` صور خرائط ثابتة من AWS / Amazon Location static maps (key)
- `MAP-20` أنماط VersaTiles المجانية / VersaTiles self-hosted styles (install)
- `MAP-22` تنظيف الخريطة الأساسية / Basemap decluttering (install)
- `MAP-23` طبقات المزود أم GeoJSON مخصص / Provider vectors vs custom GeoJSON (documented)

### `MAP-22` — تنظيف الخريطة الأساسية / Basemap decluttering

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** احذف تسميات المزود والحدود الداخلية لتبقى جغرافيا القصة وحدها. / Strip provider labels and inner admin borders so only the story geography reads.

**متى:** قبل إضافة تسمياتك / before adding your own labels.

**كيف:** On `load`, remove every layer whose `type === 'symbol'` (place, road, water labels) and inner-border layers matched by id (e.g. `/other border/i`); keep country and disputed borders; add your own labels. Logos may be hidden with CSS, but required attribution stays in frame or credits. map.on('load', () => map.getStyle().layers .filter(l => l.type === 'symbol' \|\| /other border/i.test(l.id)) .forEach(l => map.removeLayer(l.id)));

**المعاملات:** remove type==='symbol' layers

**التثبيت:** npm i maplibre-gl@6.14.0

**الوسوم:** declutter · labels · تنظيف · خريطة نظيفة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-22` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-geo-prep.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md`

#### 7. قدرات قريبة في العائلة

- `MAP-20` أنماط VersaTiles المجانية / VersaTiles self-hosted styles (install)
- `MAP-21` خطوط SDF والتسميات العربية على خرائط GL / SDF glyphs & Arabic labels on GL maps (install)
- `MAP-23` طبقات المزود أم GeoJSON مخصص / Provider vectors vs custom GeoJSON (documented)
- `MAP-24` متى GeoJSON ومتى البلاطات المتجهة / GeoJSON vs vector-tile threshold (documented)

### `MAP-23` — طبقات المزود أم GeoJSON مخصص / Provider vectors vs custom GeoJSON

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** معالم بلاطات المزود تصلح للتلاشي والتلوين لكنها لا تُرسم من البداية للنهاية لأن البلاطات تقطعها؛ اخبز GeoJSON مرتبًا للرسم. / Provider tile features can fade and tint but cannot draw start-to-end; bake ordered GeoJSON for meaningful draws.

**متى:** حين تخطط لرسم نهر أو حدود أو طريق / when planning to draw a river, border or road.

**كيف:** Context → provider source-layer with an exact filter, paint-only animation. Proposed / historical / disputed / sequenced geometry → custom GeoJSON. Hybrid: provider context + custom evidence styled distinctly. Omit absent optional props — `filter: undefined` hides the layer silently.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** geojson · vector tiles · draw-on · طبقات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-23` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-data-sources.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md`

#### 7. قدرات قريبة في العائلة

- `MAP-21` خطوط SDF والتسميات العربية على خرائط GL / SDF glyphs & Arabic labels on GL maps (install)
- `MAP-22` تنظيف الخريطة الأساسية / Basemap decluttering (install)
- `MAP-24` متى GeoJSON ومتى البلاطات المتجهة / GeoJSON vs vector-tile threshold (documented)
- `MAP-25` خط PMTiles وGeoParquet / PMTiles & GeoParquet pipeline (documented)

### `MAP-24` — متى GeoJSON ومتى البلاطات المتجهة / GeoJSON vs vector-tile threshold

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مجموعات صغيرة ثابتة كـ GeoJSON؛ الآلاف إلى الملايين أو البيانات المعتمدة على الزووم تحتاج بلاطات متجهة. / Small static sets ship as GeoJSON; large or zoom-dependent data needs vector tiles.

**متى:** عند تحميل طبقة بيانات / when loading a data layer.

**كيف:** ≤ a few hundred features → GeoJSON source directly. Larger → MVT from Martin/pg_tileserv or a PMTiles file (MAP-25), reprojected to EPSG:3857, simplified per zoom. A wrong `source-layer` name renders nothing, silently. Simplify any GeoJSON over ~5 MB (mapshaper) before using it in a film.

**المعاملات:** ≤ few hundred features; >5 MB simplify; EPSG:3857

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** geojson · mvt · simplify · بلاطات متجهة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-24` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2307-geospatial-engineering/8857-serve-vector-tiles/SKILL.md`
- `kosif-atlas/skills/1650-portaljs/4640-portaljs-add-map/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-22` تنظيف الخريطة الأساسية / Basemap decluttering (install)
- `MAP-23` طبقات المزود أم GeoJSON مخصص / Provider vectors vs custom GeoJSON (documented)
- `MAP-25` خط PMTiles وGeoParquet / PMTiles & GeoParquet pipeline (documented)
- `MAP-26` التحليل المكاني بـ DuckDB / DuckDB spatial analysis (documented)

### `MAP-25` — خط PMTiles وGeoParquet / PMTiles & GeoParquet pipeline

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حوّل أي ملف جغرافي إلى أرشيف بلاطات بلا خادم للرندر وملف GeoParquet للاستعلام. / Turn any geo file into a serverless tile archive plus a GeoParquet file.

**متى:** بيانات ضخمة (مبانٍ، نقاط اهتمام) / big data (buildings, POIs).

**كيف:** `ogr2ogr -t_srs EPSG:4326` → normalised GeoJSON; `tippecanoe -zg --drop-densest-as-needed` → `.pmtiles` (MapLibre reads it by range requests via the pmtiles protocol); DuckDB writes GeoParquet with a bbox struct and Hilbert ordering. Warn at ≥500 MB; above 2 GB keep parquet only. GDAL/tippecanoe were not probed here.

**المعاملات:** warn ≥500 MB; >2 GB parquet only

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** pmtiles · geoparquet · tippecanoe · ogr2ogr

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- `pip:duckdb` ← python3 -c "import duckdb" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-25` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/1650-portaljs/4639-portaljs-add-geo/SKILL.md`
- `kosif-atlas/skills/2761-charly-versa/10951-osm-tools-layer/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-23` طبقات المزود أم GeoJSON مخصص / Provider vectors vs custom GeoJSON (documented)
- `MAP-24` متى GeoJSON ومتى البلاطات المتجهة / GeoJSON vs vector-tile threshold (documented)
- `MAP-26` التحليل المكاني بـ DuckDB / DuckDB spatial analysis (documented)
- `MAP-27` بيانات Overture Maps المفتوحة / Overture Maps open data (documented)

### `MAP-26` — التحليل المكاني بـ DuckDB / DuckDB spatial analysis

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** SQL فوق GeoJSON وShapefile وGPX وGeoParquet للمسافات والاحتواء والكثافة قبل فيلم الخريطة. / SQL over geo files for distances, containment and density feeding a map film.

**متى:** حين يحتاج الرقم المعروض حسابًا جغرافيًا حقيقيًا / when an on-screen number needs real geo maths.

**كيف:** `LOAD spatial; SET geometry_always_xy=true;` `ST_Point(lon,lat)` (longitude first); real metres with `ST_Distance_Spheroid` on POINT_2D; `ST_Contains` for point-in-polygon; H3 hex binning via the community extension; export with `COPY … (FORMAT GDAL, DRIVER 'GeoJSON')`. duckdb was not in the probe list.

**المعاملات:** lon first; ST_Distance_Spheroid in metres

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** duckdb · spatial sql · h3 · مسافات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `pip:duckdb` ← python3 -c "import duckdb" (اسم الاستيراد قد يختلف عن اسم الحزمة)
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-26` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/1366-duckdb-skills/3111-spatial/SKILL.md`
- `kosif-atlas/skills/1366-duckdb-skills/3111-spatial/references/functions.md`

#### 7. قدرات قريبة في العائلة

- `MAP-24` متى GeoJSON ومتى البلاطات المتجهة / GeoJSON vs vector-tile threshold (documented)
- `MAP-25` خط PMTiles وGeoParquet / PMTiles & GeoParquet pipeline (documented)
- `MAP-27` بيانات Overture Maps المفتوحة / Overture Maps open data (documented)
- `MAP-28` OSM عبر Overpass لخطوط الأنهار والطرق / OSM via Overpass for centerlines (documented)

### `MAP-27` — بيانات Overture Maps المفتوحة / Overture Maps open data

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | Overture data mixes CDLA-Permissive-2.0 and ODbL by theme — attribute per theme. |

**ما هي:** بيانات عالمية مجانية بصيغة GeoParquet (أماكن، مبانٍ، طرق، حدود إدارية، يابسة وماء) بلا مفتاح. / Free global GeoParquet with no API key.

**متى:** نقاط اهتمام أو أعداد مبانٍ لمدن عربية / POI dots or building counts for Arab cities.

**كيف:** Read `s3://overturemaps-us-west-2/release/<RELEASE>/theme=…/type=…/*` with httpfs; ALWAYS filter `bbox.xmin/xmax/ymin/ymax` first (predicate pushdown); find the latest release in the STAC catalog (mirror noted 2026-03-18.0). S3 reachability was not probed here.

**المعاملات:** release 2026-03-18.0 (as of mirror)

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** overture · open data · buildings · poi · بيانات مفتوحة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-27` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/1366-duckdb-skills/3111-spatial/references/overture.md`
- `kosif-atlas/skills/1366-duckdb-skills/3111-spatial/SKILL.md`

#### 7. قدرات قريبة في العائلة

- `MAP-25` خط PMTiles وGeoParquet / PMTiles & GeoParquet pipeline (documented)
- `MAP-26` التحليل المكاني بـ DuckDB / DuckDB spatial analysis (documented)
- `MAP-28` OSM عبر Overpass لخطوط الأنهار والطرق / OSM via Overpass for centerlines (documented)
- `MAP-29` تجهيز ممر الكاميرا / Camera corridor path preparation (proven)

### `MAP-28` — OSM عبر Overpass لخطوط الأنهار والطرق / OSM via Overpass for centerlines

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | OpenStreetMap data is ODbL — ‘© OpenStreetMap contributors’ attribution required. |

**ما هي:** طرق OpenStreetMap تعطي هندسة أنهار وطرق مفصلة (~0.3 كم بين الرؤوس) حيث Natural Earth خشن جدًا. / OSM ways give detailed river/road geometry where Natural Earth is too coarse.

**متى:** مضيق أو نهر أو طريق يُطار فوقه عن قرب / a close flight along a gorge, river or road.

**كيف:** Query Overpass for the named way/relation and export GeoJSON; overpass-api.de is often busy — mirror overpass.kumi.systems (neither host probed here). Braided rivers must be routed into ONE source→mouth path by graph shortest path, never greedy nearest-endpoint chaining (it bounces between channels). Then feed MAP-29.

**المعاملات:** ~0.3 km vertex spacing

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** osm · overpass · river · centerline · أنهار

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-28` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/scripts/prep-geo.mjs`

#### 7. قدرات قريبة في العائلة

- `MAP-26` التحليل المكاني بـ DuckDB / DuckDB spatial analysis (documented)
- `MAP-27` بيانات Overture Maps المفتوحة / Overture Maps open data (documented)
- `MAP-29` تجهيز ممر الكاميرا / Camera corridor path preparation (proven)
- `MAP-30` مرساة التسمية في أبعد نقطة داخلية / Label anchor at pole of inaccessibility (ready)

### `MAP-29` — تجهيز ممر الكاميرا / Camera corridor path preparation

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حوّل خط نهر أو طريق متعرج إلى ممر كاميرا ناعم قبل الطيران فوقه. / Turn a jagged river/road centerline into a smooth camera corridor.

**متى:** قبل أي طيران متتبع لمسار (Cesium، plate، three.js) / before any path-following flight.

**كيف:** Clip a window of the source line → resample to even 0.1 km spacing → moving-average smooth ±2.8 km, 2 passes → dampen lateral deviation toward the straight chord (DAMP 0.45) → check heading deltas change gradually. Never Douglas-Peucker (it concentrates curvature into corners). Pure Node builtins, no install. Ran here on the shipped sample: `clip 106 → resample 297 → smooth → 297 pts · 17.1 km`, heading deltas every 1.5 km between −12° and +9°.

**المعاملات:** resample 0.1 km; smooth ±2.8 km ×2; DAMP 0.45

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** camera path · smoothing · corridor · flyover · ممر كاميرا · تنعيم

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-29` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/scripts/prep-cesium-path.mjs`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/assets/sample-river.geojson`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-troubleshooting.md`

#### 7. قدرات قريبة في العائلة

- `MAP-27` بيانات Overture Maps المفتوحة / Overture Maps open data (documented)
- `MAP-28` OSM عبر Overpass لخطوط الأنهار والطرق / OSM via Overpass for centerlines (documented)
- `MAP-30` مرساة التسمية في أبعد نقطة داخلية / Label anchor at pole of inaccessibility (ready)
- `MAP-31` توحيد أسماء الأماكن العربية / Arabic place-name normalisation (proven)

### `MAP-30` — مرساة التسمية في أبعد نقطة داخلية / Label anchor at pole of inaccessibility

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تسمية الدولة توضع في أعمق نقطة داخل المضلع (داخل صندوق القصة) لا في المركز الهندسي الذي قد يقع قرب الحافة أو خارجها. / Country labels sit at the most interior point, not the centroid.

**متى:** تسميات الدول على أي خريطة / country labels on any map.

**كيف:** Grid-sample the polygon bbox (46×46), keep points inside, choose the one with maximum distance to the boundary; clip the search to a per-country story bbox; then a small operator nudge in degrees (e.g. [0, 0.6]). `prep-geo.mjs` uses only Node builtins but needs YOUR source geodata (polygons too large to ship; sample outputs are in `assets/sample-data/`).

**المعاملات:** grid 46×46; nudge ≈[0,0.6]°

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** label placement · polylabel · centroid · تسمية الدول · مرساة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-30` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-geo-prep.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/scripts/prep-geo.mjs`

#### 7. قدرات قريبة في العائلة

- `MAP-28` OSM عبر Overpass لخطوط الأنهار والطرق / OSM via Overpass for centerlines (documented)
- `MAP-29` تجهيز ممر الكاميرا / Camera corridor path preparation (proven)
- `MAP-31` توحيد أسماء الأماكن العربية / Arabic place-name normalisation (proven)
- `MAP-32` رسم مسار الدائرة العظمى / Great-circle route draw-on (install)

### `MAP-31` — توحيد أسماء الأماكن العربية / Arabic place-name normalisation

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يطابق أسماء المدن المكتوبة بحرية بغض النظر عن الهمزة والتاء المربوطة والألف المقصورة وأل التعريف والتهجئة الإنجليزية. / Matches free-text city names regardless of hamza, taa marbuta, alif maqsura, the article or English spelling.

**متى:** ربط بيانات العميل (جداول مبيعات، قوائم) بنقاط الخريطة / joining client tables to map points.

**كيف:** `norm()`: lowercase → أ/إ/آ→ا → ة→ه → ى→ي → strip leading ال → collapse spaces; then an alias index per city (عربي + English). Lives in the tested sales-geo engine; `npx vitest run src/engine/fusion/sales/sales-geo-engine.test.ts` passed 4/4 in this container. const norm = s => s.toLowerCase().trim() .replace(/[أإآ]/g, 'ا').replace(/ة/g, 'ه').replace(/ى/g, 'ي') .replace(/^ال/, '').replace(/\s+/g, ' ');

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** arabic · normalization · geocoding · aliases · توحيد الأسماء · همزة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-31` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts:51`
- `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.test.ts`

#### 7. قدرات قريبة في العائلة

- `MAP-29` تجهيز ممر الكاميرا / Camera corridor path preparation (proven)
- `MAP-30` مرساة التسمية في أبعد نقطة داخلية / Label anchor at pole of inaccessibility (ready)
- `MAP-32` رسم مسار الدائرة العظمى / Great-circle route draw-on (install)
- `MAP-33` رحلة على خريطة حبر قديمة / Parchment map journey (install)

### `MAP-32` — رسم مسار الدائرة العظمى / Great-circle route draw-on

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مسار طيران أو شحن يرسم نفسه على الجيوديسي بين مدينتين مع نقاط وأسماء المدن. / A flight or shipping route drawing itself along the geodesic.

**متى:** رحلة بين مدينتين بعيدتين / a long-distance hop.

**كيف:** Turf: `greatCircle(from,to,{npoints:100})`; if it splits at the antimeridian keep the longest segment; `length()` in km; per frame `lineSliceAlong(route, 0, max(0.001, len*progress))` into a GeoJSON source. Travel window 20 %→82 % of the shot (ease-in-out), hold the rest. For a visually straight line use a plain 2-point LineString. Without Turf: slerp on the sphere, then project with D3 into an SVG path and use `stroke-dashoffset`. // slerp between two [lng,lat] points, t in 0..1 (no Turf needed) const R = Math.PI / 180, v = ([lo, la]) => [Math.cos(la*R)*Math.cos(lo*R), Math.cos(la*R)*Math.sin(lo*R), Math.sin(la*R)]; function gc(a, b, t) { const A = v(a), B = v(b); const w = Math.acos(A.reduce((s, x, i) => s + x*B[i], 0)); const k1 = Math.sin((1-t)*w)/Math.sin(w), k2 = Math.sin(t*w)/Math.sin(w); const [x, y, z] = A.map((x, i) => k1*x + k2*B[i]); return [Math.atan2(y, x)/R, Math.asin(z)/R]; }

**المعاملات:** npoints 100; min slice 0.001 km; travel 20–82 % of shot

**التثبيت:** npm i @turf/turf@7.4.0

**الوسوم:** great circle · geodesic · flight route · turf · دائرة عظمى · رحلة طيران

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-32` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md`

#### 7. قدرات قريبة في العائلة

- `MAP-30` مرساة التسمية في أبعد نقطة داخلية / Label anchor at pole of inaccessibility (ready)
- `MAP-31` توحيد أسماء الأماكن العربية / Arabic place-name normalisation (proven)
- `MAP-33` رحلة على خريطة حبر قديمة / Parchment map journey (install)
- `MAP-34` إسقاط خطوط الطول والعرض على SVG / Equirectangular lon/lat → SVG with latitude squash (seen)

### `MAP-33` — رحلة على خريطة حبر قديمة / Parchment map journey

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `repo` |
| الرخصة | Basma style is MIT-derived from motion-starter-kit styles/map-journey; keep its credit. kosif-tool scaffold: `python3 tools/kosif.py scaffold map-journey <dir>` (verified: writes STYLE/PLAN/REQUEST/TEST_REPORT/words.json, no map code). |

**ما هي:** خريطة ورقية قديمة بالحبر، طريق أحمر متقطع تمشي عليه قافلة، أعلام وكروت ورقية وعدّاد سنة ومسافة. / An ink-drawn parchment map, a red dashed route walked by a caravan, flags, paper cards and a year/distance HUD.

**متى:** رحلة تاريخية أو حج أو طريق تجارة / a historical journey, Hajj route or trade road.

**كيف:** Owner canvas style `STY.mapjourney` (alias `map-journey`): 16:9, calm, 1.9 words/s; fonts Aref Ruqaa (titles, cities, seas) + Amiri (body, numbers); palette paper #EAD9B5, edge #C9AA72, sea #BFCDBE, ink #3B2716, route #9C2A1C, gold #B8862B, desk #24170E, card #F4E9D0; each line ‘المكان: ما حدث’ becomes a stop; route = Catmull-Rom through stops (24 samples/segment); sfx pop/swish/swell. The watched reference (34 s, 30 fps) adds: coastlines ink-draw in ~2 s, triple water lines, map tilts to rotateX ~50–60°, camel sprite follows by arc length (MAP-35) through 7 stops, flag springs up + paper card with dotted leader, HUD counts 100→6,230 km and year 1325→1326, cloud pass as the only transition, final pull-out.

**المعاملات:** 16:9; 1.9 wps; Aref Ruqaa + Amiri; route #9C2A1C; 7 stops; 34 s

**التثبيت:** cd /home/user/app && npm install # owner Basma studio app that hosts STY.mapjourney

**الوسوم:** map journey · parchment · caravan · hajj · ruqaa · رحلة · خريطة قديمة · قافلة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-33` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `app/public/js/10_studio.js:737`
- `kosif-tool/styles/map-journey/SKILL.md`
- `kosif-tool/styles/map-journey/STYLE.json`
- `style:map-journey`

#### 7. قدرات قريبة في العائلة

- `MAP-31` توحيد أسماء الأماكن العربية / Arabic place-name normalisation (proven)
- `MAP-32` رسم مسار الدائرة العظمى / Great-circle route draw-on (install)
- `MAP-34` إسقاط خطوط الطول والعرض على SVG / Equirectangular lon/lat → SVG with latitude squash (seen)
- `MAP-35` متتبع مسار بطول القوس مع توقف / Arc-length route follower with dwell (seen)

### `MAP-34` — إسقاط خطوط الطول والعرض على SVG / Equirectangular lon/lat → SVG with latitude squash

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إسقاط بسيط يضع إحداثيات حقيقية على ورقة SVG، مع ضغط أفقي بجيب تمام خط عرض المنطقة. / A simple projection placing real coordinates on an SVG sheet with a cos(lat) horizontal squash.

**متى:** خريطة إقليمية مرسومة يدويًا (المتوسط والجزيرة) / a hand-styled regional map.

**كيف:** `x = (lon + 18) · K · cos(30°)`, `y = (47 − lat) · K`, K chosen per frame width; draw sea polygons over the parchment; push synthetic polygon edges far outside the sheet so they clip cleanly. Choose the cos() latitude at the region's centre (≈24° for Saudi Arabia — the owner's MAP-45 uses exactly that). const K = W / 80, C = Math.cos(30 * Math.PI / 180); const P = ([lon, lat]) => [(lon + 18) * K * C, (47 - lat) * K]; const d = 'M' + ring.map(P).map(p => p.join(',')).join('L') + 'Z';

**المعاملات:** K per frame width; cos(30°) squash; origin lon −18, lat 47

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** projection · equirectangular · svg · إسقاط

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-34` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:map-journey`

#### 7. قدرات قريبة في العائلة

- `MAP-32` رسم مسار الدائرة العظمى / Great-circle route draw-on (install)
- `MAP-33` رحلة على خريطة حبر قديمة / Parchment map journey (install)
- `MAP-35` متتبع مسار بطول القوس مع توقف / Arc-length route follower with dwell (seen)
- `MAP-36` كاميرا الخريطة المائلة 2.5D / Tilted 2.5D map camera (seen)

### `MAP-35` — متتبع مسار بطول القوس مع توقف / Arc-length route follower with dwell

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** رأس المسار (جمل، طائرة، أفاتار) يتحرك بسرعة ثابتة على طول القوس ويتوقف عند كل محطة، والخط يُرسم خلفه. / The route head moves at constant arc-length speed, dwells at each stop, and the line draws behind it.

**متى:** أي رحلة متعددة المحطات / any multi-stop journey.

**كيف:** Sample the Catmull-Rom route into a cumulative-length table; per stop store arrive/depart times; head position = lookup(length(t)); drawn path = dasharray up to the head; remainder dashed (6/4) in #9c2a1c. Camera zooms out on long legs, in on arrival. Basma's map-journey already has `catmull()` + `INK.at(route,u)` to build on. // lens[i] = cumulative length at sample i; stops[k] = {arrive, depart, s} function headS(t) { let s = 0; for (const [k, st] of stops.entries()) { if (t < st.arrive) { const p = stops[k-1]; const u = ease((t - p.depart) / (st.arrive - p.depart)); return p.s + (st.s - p.s) * Math.max(0, u); } s = st.s; } return s; } // dwell = clamp at st.s until depart

**المعاملات:** dash 6/4; #9c2a1c; 7 stops

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** arc length · follow · dwell · caravan · متتبع مسار · محطات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-35` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:map-journey`
- `app/public/js/10_studio.js:737`

#### 7. قدرات قريبة في العائلة

- `MAP-33` رحلة على خريطة حبر قديمة / Parchment map journey (install)
- `MAP-34` إسقاط خطوط الطول والعرض على SVG / Equirectangular lon/lat → SVG with latitude squash (seen)
- `MAP-36` كاميرا الخريطة المائلة 2.5D / Tilted 2.5D map camera (seen)
- `MAP-37` خط زمني بمحطات وخريطة رحلة / Milestone timeline & map route (MG-045/046) (documented)

### `MAP-36` — كاميرا الخريطة المائلة 2.5D / Tilted 2.5D map camera

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** الخريطة كلها تميل بمنظور (rotateX) والكاميرا الافتراضية تنزل من الأعلى إلى زاوية مائلة وتتبع الموضوع. / The whole map tilts in perspective and a virtual camera descends from top-down to oblique and tracks the subject.

**متى:** رحلة سينمائية بلا محرك ثلاثي الأبعاد / a cinematic journey without a 3D engine.

**كيف:** Wrap the SVG map in a container with `perspective: 1600px`; tween `rotateX` 0 → 50–60° during the descent; pan/zoom happen INSIDE the SVG (viewBox or inner transform) so the tilt stays fixed; sprites billboard upright with `rotateX(-angle)` so they stand on the plane. Rhythm: zoom out on long legs, zoom in on arrival, ~4 s pulses; final pull-out to overview.

**المعاملات:** rotateX 50–60°; ~4 s per leg

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** tilt · perspective · 2.5d · camera · كاميرا مائلة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-36` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:map-journey`

#### 7. قدرات قريبة في العائلة

- `MAP-34` إسقاط خطوط الطول والعرض على SVG / Equirectangular lon/lat → SVG with latitude squash (seen)
- `MAP-35` متتبع مسار بطول القوس مع توقف / Arc-length route follower with dwell (seen)
- `MAP-37` خط زمني بمحطات وخريطة رحلة / Milestone timeline & map route (MG-045/046) (documented)
- `MAP-38` رسم مسار بمحطات تنبثق / Route line with popping station dots (seen)

### `MAP-37` — خط زمني بمحطات وخريطة رحلة / Milestone timeline & map route (MG-045/046)

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خط أفقي يتقدم ويفتح بطاقة مؤرخة عند كل محطة (MG-045)، وخط ينمو بين ثلاث نقاط على خريطة بأسماء المدن (MG-046). / A dated-milestone line and a three-city map route.

**متى:** قصة شركة أو سيرة أو رحلة قصيرة / a company story, biography or short trip.

**كيف:** MG-045 (10 s): 0–1 s title, 1–7 s four stations, 7–10 s overview; equal spacing only when durations are not being represented. MG-046 (8 s): 0–1 s map, 1–5 s route, 5–8 s summary; distinguish an approximate path (dashed) from a true geographic route (solid). Local build: SVG/GeoJSON projected with d3-geo + dashoffset growth.

**المعاملات:** 10 s / 8 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** timeline · milestones · route · خط زمني · محطات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-37` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`
- `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### 7. قدرات قريبة في العائلة

- `MAP-35` متتبع مسار بطول القوس مع توقف / Arc-length route follower with dwell (seen)
- `MAP-36` كاميرا الخريطة المائلة 2.5D / Tilted 2.5D map camera (seen)
- `MAP-38` رسم مسار بمحطات تنبثق / Route line with popping station dots (seen)
- `MAP-39` مسار تقدم على جبل / Progress path up terrain with avatar (seen)

### `MAP-38` — رسم مسار بمحطات تنبثق / Route line with popping station dots

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مسار SVG يُرسم بإزاحة الشرطة، ونقاط المحطات تنبثق لحظة وصول الرأس. / An SVG route draws by dashoffset; station dots pop as the head reaches them.

**متى:** خريطة مترو، رحلة، أو خطوات منتج / a metro map, trip or product steps.

**كيف:** 3 s total draw; station pop = scale 0→1.15→1 in ~250 ms back-out exactly when `drawn ≥ stationLength` (use `getPointAtLength` lengths precomputed once). Reference palette: ground #e6e6e0, ink #08090d, gold #c9a23a.

**المعاملات:** 3 s draw; pop 250 ms back-out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** route · dashoffset · stations · مسار · محطات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-38` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:pm-ercankeskinx-ec2568`

#### 7. قدرات قريبة في العائلة

- `MAP-36` كاميرا الخريطة المائلة 2.5D / Tilted 2.5D map camera (seen)
- `MAP-37` خط زمني بمحطات وخريطة رحلة / Milestone timeline & map route (MG-045/046) (documented)
- `MAP-39` مسار تقدم على جبل / Progress path up terrain with avatar (seen)
- `MAP-40` خريطة وثائقية / Documentary map (documented)

### `MAP-39` — مسار تقدم على جبل / Progress path up terrain with avatar

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** مسار SVG بباقٍ متقطع، والجزء المقطوع خط صلب ليموني ينمو، وأفاتار عند رأسه. / A dashed remaining path, a solid lime travelled part growing, an avatar at the head.

**متى:** تقدم نحو هدف (خطوات، تحدٍّ، مراحل) / progress toward a goal.

**كيف:** Two copies of the same path: bottom dashed (#485b62, 6/6), top solid lime #c8ff1a with dashoffset = L·(1−p); avatar placed with `getPointAtLength(L·p)` and rotated to the tangent; footprints stepping upward as accent. Ground #08070b, 4:5.

**المعاملات:** lime #c8ff1a on #08070b; 4:5

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** progress path · mountain · avatar · مسار تقدم

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-39` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:pm-marklaunches-3b9492`

#### 7. قدرات قريبة في العائلة

- `MAP-37` خط زمني بمحطات وخريطة رحلة / Milestone timeline & map route (MG-045/046) (documented)
- `MAP-38` رسم مسار بمحطات تنبثق / Route line with popping station dots (seen)
- `MAP-40` خريطة وثائقية / Documentary map (documented)
- `MAP-41` رحلة طيران نيويورك–باريس / NYC–Paris flight block (install)

### `MAP-40` — خريطة وثائقية / Documentary map

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📄 `documented`: منهج موصوف يحتاج بناءً أو ربطًا قبل التشغيل |
| سقف التحقق قبل العمل (A27) | V1 حتى تُبنى وتُشغَّل؛ لا تقدَّم جاهزة أبدًا |
| نطاق الدليل | `repo` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** خريطة أرشيفية مع صور ومسارات وتسميات بنبرة وثائقية. / An archival map with photos, routes and labels in a documentary tone.

**متى:** تاريخ، تحقيق، قصة مكان / history, investigation, a place's story.

**كيف:** 2.5D photo rig over a map plate (MAP-12); route draw-on; Ken Burns 1.00→1.06 over 4–6 s; grain 2–4 %, vignette 10–15 %. Scaffold verified here: `python3 tools/kosif.py scaffold documentary-map <dir>` (writes STYLE.md, PLAN.md, TEST_REPORT.md, words.json — map code is yours to write).

**المعاملات:** Ken Burns 1.00→1.06 / 4–6 s; grain 2–4 %; vignette 10–15 %

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** documentary · archival map · ken burns · وثائقي · خريطة أرشيفية

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `python3` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📄 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📄 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-40` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-tool/styles/documentary-map/SKILL.md`
- `kosif-tool/styles/documentary-map/STYLE.json`
- `kosif-tool/playbooks/diagrams.md`

#### 7. قدرات قريبة في العائلة

- `MAP-38` رسم مسار بمحطات تنبثق / Route line with popping station dots (seen)
- `MAP-39` مسار تقدم على جبل / Progress path up terrain with avatar (seen)
- `MAP-41` رحلة طيران نيويورك–باريس / NYC–Paris flight block (install)
- `MAP-42` أقواس ضوء ترسم بين المدن (3D) / 3D light arcs between cities (install)

### `MAP-41` — رحلة طيران نيويورك–باريس / NYC–Paris flight block

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT. |

**ما هي:** خريطة واقعية بأسلوب أبل: طائرة تطير من مدينة إلى أخرى مع دائرة علامة ونبضة هبوط. / Apple-style realistic map: a plane flies city to city with a marker circle and a landing pop.

**متى:** أي «من هنا إلى هناك» قصير (6 ث) / any short ‘from here to there’.

**كيف:** `npx -y hyperframes@0.8.164 add nyc-paris-flight` → swap `assets/map-nyc-paris.png` for your plate (e.g. Riyadh→Cairo from MAP-12), edit the inline city constants, `npx hyperframes preview`, `npx hyperframes render`. 1920×1080, 6 s. The local copy lacks the declared `assets/sfx-mix.wav` — add licensed SFX yourself.

**المعاملات:** 6 s; 1920×1080

**التثبيت:** npx -y hyperframes@0.8.164 add nyc-paris-flight

**الوسوم:** flight · plane · block · طائرة · رحلة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-41` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/blocks/nyc-paris-flight/registry-item.json`
- `kosif-one/vendor/hyperframes/registry/blocks/nyc-paris-flight/nyc-paris-flight.html`
- `kosif-one/vendor/hyperframes/docs/catalog/blocks/nyc-paris-flight.mdx`

#### 7. قدرات قريبة في العائلة

- `MAP-39` مسار تقدم على جبل / Progress path up terrain with avatar (seen)
- `MAP-40` خريطة وثائقية / Documentary map (documented)
- `MAP-42` أقواس ضوء ترسم بين المدن (3D) / 3D light arcs between cities (install)
- `MAP-43` شريط نهر يُرسم ويجري / River ribbon reveal & flow (ready)

### `MAP-42` — أقواس ضوء ترسم بين المدن (3D) / 3D light arcs between cities

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أقواس مضيئة تنمو من مدينة مركزية إلى خمس مدن أخرى كأن شبكة تشتعل. / Glowing arcs grow from a hub city to five others, like a network lighting up.

**متى:** خاتمة «الاتصال»، شبكة توزيع، فروع شركة / a ‘connection’ finale, distribution network, branches.

**كيف:** Per arc: `QuadraticBezierCurve3` with the control point lifted 90 units at the midpoint → `TubeGeometry(curve, 80, 1.1, 6)` with additive #FFC56B material, opacity .85; grow with `geometry.setDrawRange(0, indexCount · clamp(k·1.4 − i·0.08))` where k = segment progress (16.55–17.6 s in the source) — 0.08 stagger per arc. Bloom from the light family makes it sing.

**المعاملات:** lift 90; tube 80/1.1/6; #FFC56B; stagger .08

**التثبيت:** npm i three@0.186.1

**الوسوم:** arcs · three.js · network · hub · أقواس ضوء · شبكة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-42` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/projects/egypt-2120-animation/index.html:185-201`

#### 7. قدرات قريبة في العائلة

- `MAP-40` خريطة وثائقية / Documentary map (documented)
- `MAP-41` رحلة طيران نيويورك–باريس / NYC–Paris flight block (install)
- `MAP-43` شريط نهر يُرسم ويجري / River ribbon reveal & flow (ready)
- `MAP-44` إضاءة الدول عند وصول النهر / River-triggered country reveal (key)

### `MAP-43` — شريط نهر يُرسم ويجري / River ribbon reveal & flow

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** أنبوب مسطّح على منحنى يكشف نفسه تدريجيًا ويجري ماؤه (إزاحة خريطة النورمال). / A flattened tube along a curve that draws on and flows.

**متى:** نهر على تضاريس أو خريطة ثلاثية الأبعاد / a river on 3D terrain or map.

**كيف:** `K3.makeRibbon(curve, {radius:11, flatten:.3, segments:220, color:'#6fb4d6', emissive:'#1a5f85', repeat})` (emissive .55, opacity .94); per frame `mesh.userData.reveal(p)` (setDrawRange) and `.flow(t, .9)` (normal-map offset). Feed the curve from a smoothed corridor (MAP-29) for real rivers (Nile, Euphrates).

**المعاملات:** r 11; flatten .3; 220 segs; #6fb4d6 / #1a5f85; flow .9

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** river · ribbon · three.js · draw-on · نهر · شريط

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-43` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:255`
- `kosif-studio/motion/kit/three-kit.js:255`

#### 7. قدرات قريبة في العائلة

- `MAP-41` رحلة طيران نيويورك–باريس / NYC–Paris flight block (install)
- `MAP-42` أقواس ضوء ترسم بين المدن (3D) / 3D light arcs between cities (install)
- `MAP-44` إضاءة الدول عند وصول النهر / River-triggered country reveal (key)
- `MAP-45` خريطة المملكة التخطيطية بالمناطق / Schematic Saudi Arabia map — 13 regions, drill-down (proven)

### `MAP-44` — إضاءة الدول عند وصول النهر / River-triggered country reveal

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🔑 `key`: تحتاج حسابًا أو مفتاحًا أو خدمة مدفوعة |
| سقف التحقق قبل العمل (A27) | لا استدعاء قبل إذن صريح ومعرفة التكلفة |
| نطاق الدليل | `sibling` |
| الرخصة | Reference build needs a MapTiler API key. Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier. |

**ما هي:** بينما يُرسم النهر أو الطريق، كل دولة يدخلها تشغّل تسلسلها: الحدود تُرسم، التعبئة تتوهج، والاسم يرتفع. / As a river draws on, each country it enters runs border draw → fill bloom → label rise.

**متى:** نهر عابر للدول (النيل، الفرات) أو طريق تجاري / a transnational river or trade road.

**كيف:** Precompute per country the arc-length fraction where the line first enters it (point-in-polygon walk) → trigger = start + stop·(end − start). Per country, time since trigger drives: border draw 2.5 s (constant, so long borders do not flash by) → fill opacity overshoot 0 → 0.625 → 0.5 over 1.0 s → label 0.7 s. River window 0.3–8.0 s. Beat length = max(trigger + phases) + tail. Reference implementation is on MapTiler; the same timing ports to a D3/SVG map with `npm i d3@7.9.0 @turf/turf@7.4.0` (no key).

**المعاملات:** river 0.3–8.0 s; border 2.5 s; fill 1.0 s (peak .625 → .5); label 0.7 s

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** river · country reveal · trigger · nile · النيل · إضاءة الدول

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- `key:unspecified` ← حساب أو مفتاح: لا تطلب لصقه في المحادثة، واسأل قبل أي صرف
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🔑 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🔑 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-44` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام
- `permission_denied` (صلاحية مرفوضة، ميزانية 1): من رفض: نظام الملفات أم الخدمة أم المستخدم في نافذة الإذن ← اكتب في مسار مسموح (مجلد مؤقت أو مجلد العمل) · البديل: سلّم الأمر جاهزًا ليشغّله المستخدم بنفسه · تصعيد: لا تتجاوز أي رفض بحيلة؛ اشرح ما يلزم وانتظر

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-geo-prep.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/assets/tokens.ts`

#### 7. قدرات قريبة في العائلة

- `MAP-42` أقواس ضوء ترسم بين المدن (3D) / 3D light arcs between cities (install)
- `MAP-43` شريط نهر يُرسم ويجري / River ribbon reveal & flow (ready)
- `MAP-45` خريطة المملكة التخطيطية بالمناطق / Schematic Saudi Arabia map — 13 regions, drill-down (proven)
- `MAP-46` تدرّج الخريطة الأزرق / Sequential blue map heat ramp (ready)

### `MAP-45` — خريطة المملكة التخطيطية بالمناطق / Schematic Saudi Arabia map — 13 regions, drill-down

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** حدود المملكة مرسومة بالكود مع مقار المناطق الثلاث عشرة والمدن كفقاعات بحجم القيمة؛ نقرة على منطقة تفتح مدنها، ومدينة تفتح أحياءها، بزووم viewBox متحرك وترتيب جانبي. / Hand-coded Kingdom outline with 13 regional seats and cities as value-sized bubbles, drill-down by animated viewBox zoom.

**متى:** أي بيانات سعودية بالمناطق أو المدن (مبيعات، فروع، سكان) / any Saudi regional or city data.

**كيف:** `project(lat, lon, {w:1000, h:820})`: lon scaled by cos(24°), bounds lon 34.4–56.2, lat 15.9–32.6; OUTLINE = 38 lon/lat points as one polygon; bubble r = max(6, √(v/max)·58) for regions, ·26 for cities, districts max(3.5, √·9); fill from the heat ramp MAP-46; 3 levels country → region → city with viewBox tween. Tests: `npx vitest run src/engine/fusion/sales/sales-geo-engine.test.ts` → 4/4 passed here. For video, drive the viewBox from the timeline instead of clicks. const project = (lat, lon, { w = 1000, h = 820 } = {}) => { const k = Math.cos(24 * Math.PI / 180), x0 = 34.4 * k, x1 = 56.2 * k; return [ (lon * k - x0) / (x1 - x0) * w, (32.6 - lat) / (32.6 - 15.9) * h ]; }; const r = (v, max) => Math.max(6, Math.sqrt(v / max) * 58); // regions

**المعاملات:** 1000×820; cos(24°); r=max(6,√(v/max)·58); 3 levels

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** saudi · ksa · regions · bubbles · drill-down · المملكة · المناطق · فقاعات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-45` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts`
- `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.test.ts`
- `kosif-earth-ci-fork/ui/features/sales-map.js:49`

#### 7. قدرات قريبة في العائلة

- `MAP-43` شريط نهر يُرسم ويجري / River ribbon reveal & flow (ready)
- `MAP-44` إضاءة الدول عند وصول النهر / River-triggered country reveal (key)
- `MAP-46` تدرّج الخريطة الأزرق / Sequential blue map heat ramp (ready)
- `MAP-47` خرائط تظليل بكشف متتابع / Choropleth staggered-reveal blocks (install)

### `MAP-46` — تدرّج الخريطة الأزرق / Sequential blue map heat ramp

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 🟢 `ready`: جاهزة حسب الكتالوج بلا إعداد |
| سقف التحقق قبل العمل (A27) | V2 بعد تشغيلها، وV3 بعد قياس معيار |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** تدرج أزرق أحادي اللون بخمس درجات لتلوين فقاعات الخريطة حسب القيمة. / A single-hue blue sequential ramp colouring map bubbles by value.

**متى:** أي تظليل أو فقاعات بهوية هادئة / any choropleth or bubbles in a calm identity.

**كيف:** `heat(v,max) = clamp(ceil(v/max·5), 1, 5)`, 0 → line colour. Steps: #cfe3fb · #9cc5f5 · #5f9fea · #2f77d6 · #0b4fb0 (+ `var(--sk-line)` for zero). Matches the 5–7-class rule of MAP-05.

**المعاملات:** #cfe3fb #9cc5f5 #5f9fea #2f77d6 #0b4fb0

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** palette · sequential · blue · heat · تدرج أزرق · ألوان

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 🟢 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 🟢 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-46` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-earth-ci-fork/ui/features/sales-map.js:39`
- `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts:87`

#### 7. قدرات قريبة في العائلة

- `MAP-44` إضاءة الدول عند وصول النهر / River-triggered country reveal (key)
- `MAP-45` خريطة المملكة التخطيطية بالمناطق / Schematic Saudi Arabia map — 13 regions, drill-down (proven)
- `MAP-47` خرائط تظليل بكشف متتابع / Choropleth staggered-reveal blocks (install)
- `MAP-48` خريطة الفقاعات / Proportional bubble map (install)

### `MAP-47` — خرائط تظليل بكشف متتابع / Choropleth staggered-reveal blocks

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT. |

**ما هي:** خرائط تظليل جاهزة (الولايات المتحدة، إسبانيا، العالم) تكشف المناطق واحدة تلو الأخرى مع أسطورة متدرجة وكرة دوّارة صغيرة. / Ready choropleths with staggered region reveals, gradient legend and (world) a rotating globe inset.

**متى:** خريطة بيانات بسرعة؛ استبدل الأطلس بحدود عربية / a fast data map; swap the atlas for Arab borders.

**كيف:** `npx -y hyperframes@0.8.164 add world-map` (world-atlas@2 countries-110m, 14 s) · `add us-map` (us-atlas@3 states-10m, 12 s) · `add spain-map` (es-atlas@0.6.0, D3 conic conformal, 12 s). Engine D3 v7 + topojson-client via CDN, GSAP paused timeline (`window.__timelines`), Inter, 1920×1080. To localise: filter `world-atlas` to Arab League ISO codes, `fitExtent` the region, switch Inter → IBM Plex Sans Arabic, mirror the legend for RTL.

**المعاملات:** world 14 s; us/spain 12 s; 1920×1080

**التثبيت:** npx -y hyperframes@0.8.164 add world-map

**الوسوم:** choropleth · world map · stagger · legend · خريطة العالم · تظليل

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:gsap` ← npm ls gsap أو وجود node_modules/gsap
- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-47` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/blocks/world-map/world-map.html`
- `kosif-one/vendor/hyperframes/registry/blocks/us-map/us-map.html`
- `kosif-one/vendor/hyperframes/registry/blocks/spain-map/spain-map.html`
- `kosif-one/vendor/hyperframes/docs/catalog/blocks/world-map.mdx`

#### 7. قدرات قريبة في العائلة

- `MAP-45` خريطة المملكة التخطيطية بالمناطق / Schematic Saudi Arabia map — 13 regions, drill-down (proven)
- `MAP-46` تدرّج الخريطة الأزرق / Sequential blue map heat ramp (ready)
- `MAP-48` خريطة الفقاعات / Proportional bubble map (install)
- `MAP-49` خريطة التدفق / Origin–destination flow map (install)

### `MAP-48` — خريطة الفقاعات / Proportional bubble map

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT. |

**ما هي:** مدن بفقاعات متناسبة ونداءات قيم وخطوط ربط؛ تتركب فوق خريطة التظليل. / Proportional city bubbles with value callouts and connection lines; composable with the choropleth.

**متى:** مقارنة مدن بقيم / comparing cities by magnitude.

**كيف:** `npx -y hyperframes@0.8.164 add us-map-bubble` (12 s). Bubble area ∝ value (r = √v), grow 0→r with back-out, smaller bubbles on top, anchor dot inside each (MAP-06). For KSA reuse MAP-45 instead.

**المعاملات:** 12 s; r ∝ √v

**التثبيت:** npx -y hyperframes@0.8.164 add us-map-bubble

**الوسوم:** bubble map · proportional · فقاعات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-48` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/blocks/us-map-bubble/us-map-bubble.html`
- `kosif-one/vendor/hyperframes/registry/blocks/us-map-bubble/registry-item.json`

#### 7. قدرات قريبة في العائلة

- `MAP-46` تدرّج الخريطة الأزرق / Sequential blue map heat ramp (ready)
- `MAP-47` خرائط تظليل بكشف متتابع / Choropleth staggered-reveal blocks (install)
- `MAP-49` خريطة التدفق / Origin–destination flow map (install)
- `MAP-50` خريطة سداسية / Hex tile map (install)

### `MAP-49` — خريطة التدفق / Origin–destination flow map

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT. |

**ما هي:** أقواس من الأصل إلى الوجهة بين المدن فوق خريطة أساسية. / Origin–destination arcs between cities over a basemap.

**متى:** تجارة، هجرة، شحن، مسافرون / trade, migration, shipping, travellers.

**كيف:** `npx -y hyperframes@0.8.164 add us-map-flow` (12 s). Arcs as quadratic SVG paths (control point lifted ~20 % of chord), width ∝ volume, dashoffset draw-on in stagger, flyer dot on the head; never particle flows for human harm (MAP-09).

**المعاملات:** 12 s; lift ≈20 % chord

**التثبيت:** npx -y hyperframes@0.8.164 add us-map-flow

**الوسوم:** flow map · arcs · origin destination · تدفق · أقواس

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-49` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/blocks/us-map-flow/us-map-flow.html`
- `kosif-one/vendor/hyperframes/registry/blocks/us-map-flow/registry-item.json`

#### 7. قدرات قريبة في العائلة

- `MAP-47` خرائط تظليل بكشف متتابع / Choropleth staggered-reveal blocks (install)
- `MAP-48` خريطة الفقاعات / Proportional bubble map (install)
- `MAP-50` خريطة سداسية / Hex tile map (install)
- `MAP-51` زووم دولة مع دائرة حمراء / Country zoom with red scribble circle (install)

### `MAP-50` — خريطة سداسية / Hex tile map

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT. |

**ما هي:** كل منطقة سداسي بوزن متساوٍ بتعبئة بيانات واختصار. / Each region an equal-weight hexagon with a data fill and abbreviation.

**متى:** حين تبتلع المناطق الكبيرة الفارغة الانتباه / when big empty regions would dominate.

**كيف:** `npx -y hyperframes@0.8.164 add us-map-hex` (10 s, inline SVG, no CDN geo). For the Gulf or Arab world hand-author the hex grid (one hex per country/region, keep rough adjacency), fill with MAP-46, reveal in a diagonal stagger.

**المعاملات:** 10 s

**التثبيت:** npx -y hyperframes@0.8.164 add us-map-hex

**الوسوم:** hex map · tile cartogram · سداسية

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-50` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/blocks/us-map-hex/us-map-hex.html`
- `kosif-one/vendor/hyperframes/registry/blocks/us-map-hex/registry-item.json`

#### 7. قدرات قريبة في العائلة

- `MAP-48` خريطة الفقاعات / Proportional bubble map (install)
- `MAP-49` خريطة التدفق / Origin–destination flow map (install)
- `MAP-51` زووم دولة مع دائرة حمراء / Country zoom with red scribble circle (install)
- `MAP-52` علامات وتسميات داخل الخريطة / Map-native circle & symbol markers (install)

### `MAP-51` — زووم دولة مع دائرة حمراء / Country zoom with red scribble circle

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT. |

**ما هي:** زووم على خريطة واقعية نحو دولة، دائرة حمراء مخربشة، تسمية منبثقة وغسيل أحمر تحريري. / Realistic raster map zooms into a country, a red scribble circle, a pop-up label and a reddish editorial wash.

**متى:** خبر أو تحقيق عن بلد / a news or investigative beat about one country.

**كيف:** `npx -y hyperframes@0.8.164 add north-korea-locked-down` (7 s, 1920×1080, `assets/korea-map.png`) → swap the plate and target; the scribble is a hand-jittered SVG ellipse drawn with dashoffset (~0.6 s) after the zoom settles; wash = red multiply layer at low opacity.

**المعاملات:** 7 s; 1920×1080

**التثبيت:** npx -y hyperframes@0.8.164 add north-korea-locked-down

**الوسوم:** zoom · scribble circle · news · دائرة حمراء · أخبار

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:hyperframes` ← npm ls hyperframes أو وجود node_modules/hyperframes
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-51` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/vendor/hyperframes/registry/blocks/north-korea-locked-down/north-korea-locked-down.html`
- `kosif-one/vendor/hyperframes/registry/blocks/north-korea-locked-down/registry-item.json`
- `kosif-one/vendor/hyperframes/docs/catalog/blocks/north-korea-locked-down.mdx`

#### 7. قدرات قريبة في العائلة

- `MAP-49` خريطة التدفق / Origin–destination flow map (install)
- `MAP-50` خريطة سداسية / Hex tile map (install)
- `MAP-52` علامات وتسميات داخل الخريطة / Map-native circle & symbol markers (install)
- `MAP-53` رسم خريطة شوارع وإسقاط دبابيس / SVG street map draw + pin drop (seen)

### `MAP-52` — علامات وتسميات داخل الخريطة / Map-native circle & symbol markers

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط المدن وأسماؤها كطبقات circle وsymbol في GeoJSON بمقاسات للفيديو. / City dots and names as GeoJSON circle + symbol layers sized for video.

**متى:** تسميات لاتينية داخل خريطة GL / Latin labels inside a GL map.

**كيف:** Circle: colour #f03b20, radius 12, white stroke 4. Symbol: `text-field` from properties, anchor top, offset [0, 0.9], size 28, dark text with 3 px white halo, `text-allow-overlap: true`. Scale sizes with output resolution (×2 at 4K). Arabic names → HTML overlay instead (MAP-21).

**المعاملات:** circle r12 stroke 4 #f03b20; text 28 px halo 3

**التثبيت:** npm i maplibre-gl@6.14.0

**الوسوم:** markers · labels · circle layer · symbol layer · علامات

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:maplibre` ← npm ls maplibre أو وجود node_modules/maplibre
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-52` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md`
- `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md`

#### 7. قدرات قريبة في العائلة

- `MAP-50` خريطة سداسية / Hex tile map (install)
- `MAP-51` زووم دولة مع دائرة حمراء / Country zoom with red scribble circle (install)
- `MAP-53` رسم خريطة شوارع وإسقاط دبابيس / SVG street map draw + pin drop (seen)
- `MAP-54` خريطة نقاط تجمعات المدن / Dot-cluster city map (seen)

### `MAP-53` — رسم خريطة شوارع وإسقاط دبابيس / SVG street map draw + pin drop

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** شوارع مدينة SVG تُرسم بالخط، ثم تسقط الدبابيس بارتداد متتابع، ودبوس بطل بحلقة نبض وشريحة اسم. / City streets stroke-draw, pins drop with bounce stagger, one hero pin with pulse ring and label chip.

**متى:** تطبيق أماكن، فروع، توصيل / a places app, branches, delivery.

**كيف:** Streets: dashoffset draw with 30–60 ms stagger per street; pins: y −40 px → 0 with bounce, stagger 60 ms; hero pin: pulse ring scale 1→2.4, opacity .6→0 over 900 ms, then label chip slides 8 px. Palette from the reference: #f7f7f7 ground, teal #1db394 accent, mint #e2f2ee, text #1a1a1a.

**المعاملات:** pin stagger 60 ms; ring 900 ms; teal #1db394

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** street map · pin drop · pulse ring · دبابيس · خريطة مدينة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-53` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:pm-danilowm-d3720d`

#### 7. قدرات قريبة في العائلة

- `MAP-51` زووم دولة مع دائرة حمراء / Country zoom with red scribble circle (install)
- `MAP-52` علامات وتسميات داخل الخريطة / Map-native circle & symbol markers (install)
- `MAP-54` خريطة نقاط تجمعات المدن / Dot-cluster city map (seen)
- `MAP-55` خريطة عالم نقطية بكبسولات صور / Dotted world map with avatar pills (seen)

### `MAP-54` — خريطة نقاط تجمعات المدن / Dot-cluster city map

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** جسيمات تتجمع في عناقيد عند مواقع المدن بلا خريطة أساسية، مع تسميات وأعداد تتصاعد. / Particles gather into clusters at city positions, no basemap, labels with ticking counts.

**متى:** حضور عالمي أو شبكة عملاء بأسلوب بسيط / global presence in a minimal look.

**كيف:** ~800 dots; each assigned a city by weight; spring from random start to a disc of radius 40–80 px around the projected city; label + counter tick up when the cluster settles. Ink #08080a / #f5f6f8 with orange #ff5a1f accent.

**المعاملات:** ~800 dots; cluster r 40–80 px; #ff5a1f

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dot cluster · particles · cities · تجمعات · نقاط

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-54` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:pm-blushpetal795-0c85c2`

#### 7. قدرات قريبة في العائلة

- `MAP-52` علامات وتسميات داخل الخريطة / Map-native circle & symbol markers (install)
- `MAP-53` رسم خريطة شوارع وإسقاط دبابيس / SVG street map draw + pin drop (seen)
- `MAP-55` خريطة عالم نقطية بكبسولات صور / Dotted world map with avatar pills (seen)
- `MAP-56` خريطة أعمدة ضوئية / Spike map (seen)

### `MAP-55` — خريطة عالم نقطية بكبسولات صور / Dotted world map with avatar pills

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يابسة العالم شبكة نقاط من قناع، وكبسولات بدوائر أحرف متداخلة وأعداد تنبثق عند المدن. / Land as a dot grid from a mask; pills with overlapping initial circles and counts pop at cities.

**متى:** مجتمع، مستخدمون، مؤسسون حول العالم / a community or user map.

**كيف:** Dot 4 px, gap 8 px sampled from a land mask (world-atlas → canvas → `getImageData`); pills pop with 250 ms back-out in stagger; 2–3 overlapping initial circles (#3b6fe0, #22b55a, #f2b83a) + count. Ground #f5f6fa, text #111318.

**المعاملات:** dot 4 px gap 8 px; pill 250 ms back-out

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dotted map · avatars · pills · خريطة نقطية

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-55` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:pm-ratheejaisal-1f4538`

#### 7. قدرات قريبة في العائلة

- `MAP-53` رسم خريطة شوارع وإسقاط دبابيس / SVG street map draw + pin drop (seen)
- `MAP-54` خريطة نقاط تجمعات المدن / Dot-cluster city map (seen)
- `MAP-56` خريطة أعمدة ضوئية / Spike map (seen)
- `MAP-57` عناصر خرائط أرشيفية / Archival map-fragment collage props (proven)

### `MAP-56` — خريطة أعمدة ضوئية / Spike map

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** نقاط بخطوط عمودية طولها يساوي القيمة مع توهج. / Points with vertical lines whose height is the value, with glow.

**متى:** كثافة أو مراجعات أو قيم كثيرة على خريطة / many values over a map.

**كيف:** ~1,534 points; spike = thin triangle (base 4–6 px) from the projected point upward, height ∝ value, grow in a sweep from west to east (or by value rank); faint glow; orange #f05a0f on #14130f. Pairs with a slight perspective tilt (MAP-36).

**المعاملات:** 1534 pts; #f05a0f on #14130f

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** spike map · 3d bars · أعمدة

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-56` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:pm-jesscaroline7-1ff7cb`

#### 7. قدرات قريبة في العائلة

- `MAP-54` خريطة نقاط تجمعات المدن / Dot-cluster city map (seen)
- `MAP-55` خريطة عالم نقطية بكبسولات صور / Dotted world map with avatar pills (seen)
- `MAP-57` عناصر خرائط أرشيفية / Archival map-fragment collage props (proven)
- `MAP-58` كوكب الأرض مع غلاف جوي / Procedural Earth with atmosphere (install)

### `MAP-57` — عناصر خرائط أرشيفية / Archival map-fragment collage props

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | ✅ `proven`: مثبتة في الكتالوج؛ افحص متطلباتها هنا قبل كتابة ✅ في الخطة |
| سقف التحقق قبل العمل (A27) | V3 بعد تشغيلها هنا وقياس معيار، لا قبل ذلك |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** إكسسوارات كولاج توحي بالجغرافيا: قطعة خريطة قديمة مطوية، خريطة مصغرة، خيط أحمر يعبر الخريطة، شريط خط زمني مرسوم. / Collage props that suggest geography: folded era map fragment, map inset, red string across a map, hand-drawn timeline strip.

**متى:** فيديو تاريخي بأسلوب سكراب بوك أرشيفي / a vox-history scrapbook film.

**كيف:** Part of the vox-history INVENTORY rotated through clips (sepia, grain, brass tacks, red string). What is proven: the planner places these props into clip prompts — `node --test tests/production-profiles.test.mjs` passed 10/10 here; the visuals themselves are generated per project.

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** archival · collage · red string · vox · أرشيف · خيط أحمر

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `node` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا ✅ الكتالوج تلقائيًا · الوضع 2: `كتالوج: ✅ · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-57` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `fastify-motion-bro/scripts/profiles/vox-history.mjs:15-18`
- `fastify-motion-bro/tests/production-profiles.test.mjs`

#### 7. قدرات قريبة في العائلة

- `MAP-55` خريطة عالم نقطية بكبسولات صور / Dotted world map with avatar pills (seen)
- `MAP-56` خريطة أعمدة ضوئية / Spike map (seen)
- `MAP-58` كوكب الأرض مع غلاف جوي / Procedural Earth with atmosphere (install)
- `MAP-59` خريطة الأضواء من المدار / Orbit-at-night lights map (install)

### `MAP-58` — كوكب الأرض مع غلاف جوي / Procedural Earth with atmosphere

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرة بمزج نهار/ليل وأضواء مدن وغيوم متحركة وحافة غلاف جوي (فرينل). / A day/night globe with city lights, moving clouds and a fresnel atmosphere rim.

**متى:** افتتاحية «الكوكب» أو انتقال من الفضاء / a planet opener or space-to-ground transition.

**كيف:** Sphere 64×64; `orientation = dot(normal, sun)·0.5 + 0.5`; `dayNight = smoothstep(0.4, 0.6, orientation)`; city lights × (1 − orientation)² × 1.5; clouds on a second sphere r = 1.01 with uv offset by time (speed 0.01); fresnel pow 4 × atmosphere colour × 0.3; bump 0.03. Sun (1, 0.2, 0.5); day #4db2ff, twilight #bd5f1b. Textures (day/night/clouds) must be licensed — NASA images host is blocked here (403); Wikimedia Commons is reachable.

**المعاملات:** sun (1,.2,.5); #4db2ff / #bd5f1b; clouds .01; lights 1.5; fresnel^4 ×.3

**التثبيت:** npm i three@0.186.1

**الوسوم:** earth · globe · atmosphere · fresnel · three.js · tsl · الأرض · غلاف جوي

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-58` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/examples/earth-shader.js`

#### 7. قدرات قريبة في العائلة

- `MAP-56` خريطة أعمدة ضوئية / Spike map (seen)
- `MAP-57` عناصر خرائط أرشيفية / Archival map-fragment collage props (proven)
- `MAP-59` خريطة الأضواء من المدار / Orbit-at-night lights map (install)
- `MAP-60` كرة أرضية نقطية بإسقاط كروي / Orthographic dot / halftone globe (seen)

### `MAP-59` — خريطة الأضواء من المدار / Orbit-at-night lights map

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 📦 `install`: تحتاج حزمة أو برنامجًا أو نموذجًا أولًا |
| سقف التحقق قبل العمل (A27) | V1 حتى تُثبَّت (التثبيت النظامي بإذن) |
| نطاق الدليل | `sibling` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** منظر قمر صناعي ليلي منمّق: 26 ألف نقطة مضيئة على طول نهر ودلتا ومدن كثيفة وبلدات متناثرة وساحل أزرق خافت. / A stylised night satellite view: 26,000 glowing points along a river, a delta fan, dense cities, scattered towns and a faint coast.

**متى:** مصر/النيل، مدن الخليج ليلًا، «المستقبل» / Egypt & the Nile, Gulf cities at night, futurism.

**كيف:** Nile `x(z) = 18·sin(z/95) + 9·sin(z/31)`; 9,000 points along it, 11,000 in a delta fan (angle ±0.75, distance pow(r, 0.7)·230), 2,600 Cairo, 1,400 Alexandria, 1,600 desert towns; 900-point coast. Colours gold #FFB65C, white #FFF1D6, cyan #7FE8FF 15–20 %, coast #5FA8FF; bloom 1.25 / 0.75 / 0.12. Camera dives y 1500 → 210 with ease and a slight roll.

**المعاملات:** 26k pts; bloom 1.25/.75/.12; camera y 1500→210

**التثبيت:** npm i three@0.186.1

**الوسوم:** night lights · orbit · nile · points · bloom · أضواء ليلية · النيل · مدار

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- `fonts:arabic` ← افحص وجوده بأمر واحد قبل كتابة الشارة
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 📦 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 📦 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-59` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `kosif-one/projects/egypt-2120-animation/index.html:168-202`

#### 7. قدرات قريبة في العائلة

- `MAP-57` عناصر خرائط أرشيفية / Archival map-fragment collage props (proven)
- `MAP-58` كوكب الأرض مع غلاف جوي / Procedural Earth with atmosphere (install)
- `MAP-60` كرة أرضية نقطية بإسقاط كروي / Orthographic dot / halftone globe (seen)
- `MAP-61` كرة أرضية بأقواس اتصال / Globe with great-circle arcs (wireframe / particle) (seen)

### `MAP-60` — كرة أرضية نقطية بإسقاط كروي / Orthographic dot / halftone globe

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** يابسة الأرض كشبكة نقاط على كرة تدور، بحجم وسطوع حسب العمق، مع شبكة خطوط عرض وطول أو محور مائل. / Land as a dot grid on a rotating orthographic sphere, size/brightness by depth, with graticule or a tilted axis.

**متى:** رقم عالمي (71 % ماء)، علامة تقنية، افتتاحية / a global stat, tech brand, opener.

**كيف:** Rasterise continent polygons (world-atlas 110m) to a lat/lon dot grid ONCE (~2,000 dots, or a 2 px halftone with 15° graticule); each frame rotate (6–10 °/s) + tilt, project orthographically, cull back-facing (z < 0); dot size and alpha ∝ depth; add night shade and an atmosphere glow ring. Looks: navy keynote (#000 + glow #64d2ff, style:infographic), cream science-book (#efecdd, ink #1a1a18, red axis #c9452c, style:pm-hbcoop-de365c), black half-sphere with glowing rim and pings (style:pm-steventey-0d20e4). Build: `npm i d3@7.9.0 topojson-client@3.1.0 world-atlas@2.0.2`. // dots: [{lon,lat}] sampled once from the land mask const R = Math.PI / 180; function drawGlobe(ctx, dots, rot, tilt, cx, cy, r) { for (const d of dots) { const l = (d.lon + rot) * R, p = d.lat * R; let x = Math.cos(p) * Math.sin(l), y = Math.sin(p), z = Math.cos(p) * Math.cos(l); [y, z] = [y * Math.cos(tilt*R) - z * Math.sin(tilt*R), y * Math.sin(tilt*R) + z * Math.cos(tilt*R)]; if (z < 0) continue; // back-face cull ctx.globalAlpha = 0.25 + 0.75 * z; ctx.fillRect(cx + x * r, cy - y * r, 1 + 1.5 * z, 1 + 1.5 * z); } }

**المعاملات:** ~2000 dots; 6–10 °/s; dot 2 px; graticule 15°; glow #64d2ff

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** dot globe · halftone · orthographic · كرة نقطية · كوكب

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:d3` ← npm ls d3 أو وجود node_modules/d3
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-60` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:infographic`
- `style:pm-hbcoop-de365c`
- `style:pm-steventey-0d20e4`

#### 7. قدرات قريبة في العائلة

- `MAP-58` كوكب الأرض مع غلاف جوي / Procedural Earth with atmosphere (install)
- `MAP-59` خريطة الأضواء من المدار / Orbit-at-night lights map (install)
- `MAP-61` كرة أرضية بأقواس اتصال / Globe with great-circle arcs (wireframe / particle) (seen)
- `MAP-62` كرة غبار مع تسميات / Dust point-cloud globe with leader labels (seen)

### `MAP-61` — كرة أرضية بأقواس اتصال / Globe with great-circle arcs (wireframe / particle)

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرة سلكية أو من جسيمات تدور، بنقاط مضيئة بهالات وأقواس دائرة عظمى متقطعة ترسم بين الأزواج. / A rotating wireframe or particle globe with haloed dots and dashed great-circle arcs drawing between pairs.

**متى:** لاعبون أو مستخدمون أو فروع متصلة حول العالم / connected players, users or offices worldwide.

**كيف:** Orthographic lat/long grid (wireframe) or ~3,000 land-mask points (particle); rotate ~10 °/s; dots with ring halos; arcs: sample MAP-32's slerp at 64 steps, lift the middle by 10–20 % of r, cull hidden segments, draw-on 400 ms each with dashes; outer glow ring ~20 px. Looks: lime #d8f24a + white on navy #07131f (style:pm-deifosv-04e4d3); orange #e24b0f glow on light #f5f4f2 (style:pm-manuelogomigo-f33ca9); pings arcing over a black half-sphere (style:pm-steventey-0d20e4).

**المعاملات:** ~10 °/s; arc draw 400 ms; ~3000 pts; glow 20 px

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** globe arcs · wireframe globe · particle globe · connections · كرة أرضية · أقواس

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- لا متطلبات مسجلة؛ افحص المسار والأداة بـ `hub.py doctor` قبل الشارة.
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-61` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:pm-deifosv-04e4d3`
- `style:pm-manuelogomigo-f33ca9`
- `style:pm-steventey-0d20e4`

#### 7. قدرات قريبة في العائلة

- `MAP-59` خريطة الأضواء من المدار / Orbit-at-night lights map (install)
- `MAP-60` كرة أرضية نقطية بإسقاط كروي / Orthographic dot / halftone globe (seen)
- `MAP-62` كرة غبار مع تسميات / Dust point-cloud globe with leader labels (seen)

### `MAP-62` — كرة غبار مع تسميات / Dust point-cloud globe with leader labels

| الحقل | القيمة |
|---|---|
| العائلة | `maps-geo` ([فصل العائلة](../../../.claude/skills/kosif-superpowers/references/powers/maps-geo.md)) |
| المجموعة | البيانات والرسوم والمواقع (`data`) |
| نوع المخرج (A25، A27) | بيانات وجداول ورسوم (`data`) |
| الحالة في الكتالوج | 👁 `seen`: شوهدت في مرجع أو عرض ولم تُنفّذ هنا |
| سقف التحقق قبل العمل (A27) | V0 هنا؛ أعد بناءها أو اذكرها مرجعًا فقط |
| نطاق الدليل | `style` |
| الرخصة | غير مذكورة في السجل: تُؤكَّد من المصدر قبل التسليم |

**ما هي:** كرة من سحابة نقاط تدور ببطء مع تسميات بنقطة قائدة تنبثق عند مواقع. / A slowly rotating point-cloud sphere with leader-dot labels popping at locations.

**متى:** تعريف شخصي أو شركة بـ «أين نعمل» / a personal or company ‘where we work’ beat.

**كيف:** THREE.Points with additive blending + bloom; rotation 0.15 rad/s; 4–6 labels, stagger 200 ms: a dot on the surface, a 1 px leader line, a mono label in cyan #7fe3ff / amber #ffb070 on #05050a; hide a label when its anchor rotates behind (z < 0).

**المعاملات:** 0.15 rad/s; 4–6 labels; stagger 200 ms

**التثبيت:** لا خطوة تثبيت مسجلة

**الوسوم:** point cloud · globe · labels · hud · كرة غبار

#### 1. الاستقبال (A25)

- مصدر البيانات: مدخل حاجب ← لا يُفترض: البيانات مطلوبة أو مصدر عام مسمى
- السؤال الذي تجيب عنه البيانات: سؤال بإجابة مقترحة ← وصف عام: توزيع واتجاه وأعلى خمس فئات
- الفترة والوحدات: افتراض مكتوب ← كل الفترة الموجودة في الملف، مع ذكرها
- لا تُفترض أبدًا: مادة الإنتاج نفسها، والإذن بخطوة مدفوعة أو منشورة أو لا رجعة فيها، والهوية والحقوق.

#### 2. الجاهزية والشارة (A28)

- `npm:three` ← npm ls three أو وجود node_modules/three
- الوضع 1: شارة «هنا الآن» بعد الفحص، لا 👁 الكتالوج تلقائيًا · الوضع 2: `كتالوج: 👁 · هنا: غير مفحوص` · الوضع 3: بلا شارة ولا معرّف.

#### 3. موضعها في الخطة (A26)

- عقدة منمّطة: المدخل `dataset` ← المخرج `report`، والمنفّذ `method:MAP-62` حتى تُربط بأداة مختبرة (`fusionforge.py bind`).
- لا أداة مسجلة تخدم عائلتها: التنفيذ بالمكتبات أو بأداة من مجموعة أخرى.
- مراحل النوع: فحص الملف ← تنظيف موثق ← حساب بسكربت ← تسوية المجاميع ← رسم يناسب السؤال ← تسليم مع السكربت.
- إن اختلف نوع مدخلها عن مخرج العقدة السابقة فمحوّل صريح بينهما، والخط ينتهي بعقدة تحقق قبل التسليم.

#### 4. بوابة التحقق (A27)

- إلزامي: المجاميع تطابق المصدر (تسوية) ← حساب بالكود
- إلزامي: الوحدات والفترات مكتوبة على كل رقم ورسم ← مراجعة المحاور
- إلزامي: كل رقم من حساب حتمي لا من تقدير النموذج ← سكربت قابل لإعادة التشغيل
- جودة: نوع الرسم يناسب السؤال ولا يشوّه المقياس ← المحور يبدأ من الصفر للأعمدة
- جودة: القيم المفقودة والشاذة معالجة ومذكورة ← عدّ القيم الفارغة
- أمر الحكم في الوضع 1: `think.py qa data --answers qa.json` (PASS / FAIL / INCOMPLETE).

#### 5. التعافي (A29)

- `missing_dependency` (اعتمادية مفقودة، ميزانية 2): سمِّ الاعتمادية بالضبط (حزمة، برنامج، خط، نموذج) ← ثبّت محليًا في بيئة العمل إن كان مجانيًا ومسموحًا (pip --user أو venv أو npm محلي) · البديل: مسار المكتبة القياسية أو أداة أخرى من نفس المجموعة · تصعيد: تثبيت نظامي أو مدفوع أو يحتاج مفتاحًا: توقف واسأل
- `wrong_input_kind` (نوع مدخل خاطئ، ميزانية 2): افحص المدخل الفعلي (file، ffprobe، أول بايتات، ترميز النص) ← أضف محوّلًا صريحًا بين العقدتين (مثلًا ffmpeg لتحويل الصيغة) واحفظ الأصل كما هو · البديل: اطلب المدخل بالصيغة الصحيحة مع أمر تحويل جاهز · تصعيد: إن كان التحويل يفقد جودة أو بيانات: اسأل قبل التحويل
- `quality_below_threshold` (جودة دون العتبة، ميزانية 3): أي معيار فشل وبكم (المقيس مقابل العتبة) ← عالج السبب الأكبر وحده ثم أعد القياس · البديل: المنهج البديل المكتوب للمرحلة في الخطة · تصعيد: معيار إلزامي لا يتحقق بعد البديل: توقف وأبلغ بالأرقام

#### 6. الأدلة

- `style:pm-madhav-xo-f97f20`

#### 7. قدرات قريبة في العائلة

- `MAP-60` كرة أرضية نقطية بإسقاط كروي / Orthographic dot / halftone globe (seen)
- `MAP-61` كرة أرضية بأقواس اتصال / Globe with great-circle arcs (wireframe / particle) (seen)

