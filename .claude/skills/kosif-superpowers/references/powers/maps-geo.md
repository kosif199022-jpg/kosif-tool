# الخرائط — Maps & geo

> **ما تمنحك هذه القوة:** أنت تضع القصة على الأرض الحقيقية — تختار هل تحتاج خريطة أصلًا، أي إسقاط وأي خلفية، ثم ترسم الطرق على الدائرة العظمى، وتحرّك القوافل بطول القوس، وتضيء الدول حين يصلها النهر، وتدير الكوكب نقاطًا وأقواسًا — بإحداثيات [lng, lat] صحيحة وأسماء عربية مشكّلة وبلا ارتعاش في الرندر.  
> *You put the story on real ground — decide whether a map is warranted, pick projection and substrate, draw great-circle routes, walk caravans by arc length, light countries as a river reaches them, and spin the planet as dots and arcs — with correct [lng, lat], shaped Arabic names and shimmer-free renders.*
>
> **أقوى دليل / strongest proof:** ✅ خريطة المملكة التخطيطية بـ 13 منطقة وتعمّق حتى الأحياء — `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.test.ts` نجح 4/4 في هذه الحاوية؛ ✅ مولّد ممر الكاميرا `prep-cesium-path.mjs` شُغّل هنا (106 → 297 نقطة · 17.1 كم)؛ وأنت أنتجت رحلة الخريطة القديمة بالرقعة والقافلة في `style:map-journey` (34 ث، 7 محطات، عداد 100 → 6,230 كم).
>
> **62 قوة في 6 أقسام / 62 powers in 6 sections:** ✅ 4 · 🟢 3 · 📦 18 · 🔑 5 · 👁 12 · 📄 20. الخرائط بيانات أيضًا — اقرأ فصل الرسوم البيانية للأرقام والأساطير، وفصل ARAB لتسميات المدن. / Maps are data too — read the charts chapter for numbers and legends and the ARAB chapter for city labels.

**الشارات / badges:** ✅ مُثبت هنا / proven here · 🟢 جاهز / ready · 📦 بأمر تثبيت / one install · 🔑 مفتاح أو خدمة / needs key or service · 👁 شوهد في فيديو / seen in a reference video · 📄 موصوف / documented only · 💡 فكرة / idea

**المحرك الافتراضي / default engine:** خريطة متجهية تحريرية = D3 geo + TopoJSON داخل صفحة HTML قابلة للتقديم الإطاري (`npm i d3@7.9.0 topojson-client@3.1.0 world-atlas@2.0.2` → `node tools/render_html.cjs --preview` في kosif-tool). خريطة حقيقية = MapLibre بلا مفتاح على OpenFreeMap مع لوحة مجمّدة (MAP-13/14). كرة ثلاثية الأبعاد = three.js (`npm i three@0.186.1`). كتل جاهزة = `npx -y hyperframes@0.8.164 add <block>`. / Editorial vector map = D3 geo in a seekable HTML page; real basemap = keyless MapLibre on OpenFreeMap with a frozen plate; 3D globe = three.js; ready blocks via HyperFrames.

| # | القسم / section | powers |
|---|---|---|
| 1 | القرار والمنهج الخرائطي — Map decisions & cartographic method | MAP-01–MAP-10 (10) |
| 2 | المحركات والخلفيات واستقرار الرندر — Engines, basemaps & render stability | MAP-11–MAP-23 (13) |
| 3 | البيانات والتحضير الجغرافي — Geo data & preparation | MAP-24–MAP-31 (8) |
| 4 | المسارات والرحلات والرسم — Routes, journeys & draw-on | MAP-32–MAP-44 (13) |
| 5 | الخرائط الموضوعية وخرائط البيانات — Thematic & data maps | MAP-45–MAP-57 (13) |
| 6 | الكرات الأرضية والمنظر المداري — Globes & orbital views | MAP-58–MAP-62 (5) |

## الفهرس / contents
- [1. القرار والمنهج الخرائطي — Map decisions & cartographic method](#1-القرار-والمنهج-الخرائطي--map-decisions--cartographic-method)
- [2. المحركات والخلفيات واستقرار الرندر — Engines, basemaps & render stability](#2-المحركات-والخلفيات-واستقرار-الرندر--engines-basemaps--render-stability)
- [3. البيانات والتحضير الجغرافي — Geo data & preparation](#3-البيانات-والتحضير-الجغرافي--geo-data--preparation)
- [4. المسارات والرحلات والرسم — Routes, journeys & draw-on](#4-المسارات-والرحلات-والرسم--routes-journeys--draw-on)
- [5. الخرائط الموضوعية وخرائط البيانات — Thematic & data maps](#5-الخرائط-الموضوعية-وخرائط-البيانات--thematic--data-maps)
- [6. الكرات الأرضية والمنظر المداري — Globes & orbital views](#6-الكرات-الأرضية-والمنظر-المداري--globes--orbital-views)
- [توليفات قوية — Power combos](#توليفات-قوية--power-combos)
- [أخطاء ممنوعة — Never do](#أخطاء-ممنوعة--never-do)
- [أقوى 5 حركات توقيع — 5 signature moves](#أقوى-5-حركات-توقيع--5-signature-moves)

## 1. القرار والمنهج الخرائطي — Map decisions & cartographic method

قبل أي محرك: هل نحتاج خريطة، أي أساس، أي نوع موضوعي، أي إسقاط، وكيف نبقى أمناء للمصدر. / Before any engine: whether to map at all, which substrate, which thematic form, which projection, and how to stay honest to the source.

### MAP-01 · هل نحتاج خريطة أصلًا · Map or not · 📄 موصوف / documented only
- **ماذا / what:** الإحداثيات أو أسماء المناطق وحدها لا تبرر خريطة؛ ارسم خريطة فقط حين يكون الموقع أو الجوار أو الحركة جزءًا من الحجة. / Coordinates or region names alone do not justify a map; map only when position, adjacency or movement is part of the argument. · **متى / when:** أول سؤال في أي مشهد فيه دول أو مدن / the first question for any shot that names places.
- **كيف / how:** Ranking or precise comparison across named regions → sorted bar or dot plot, optionally with a tiny locator inset (≈15 % of frame) in the corner. Distance, neighbours, routes or spatial clustering carry the story → a real map. Write the choice and the reason into PLAN.md so the next shot does not drift back to a decorative map.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/map-or-not.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/references/chart-selection-patterns.md`

### MAP-02 · الخريطة الأساسية حسب الغرض · Basemap substrate by purpose · 📄 موصوف / documented only
- **ماذا / what:** اختر الطبقة الأساسية (طرق، تضاريس، حدود، صور فضائية، محايد، كرة) مما يجب أن يفكر فيه المشاهد، قبل اختيار المكتبة. / Choose the substrate from what the viewer must reason about, before choosing a library. · **متى / when:** عند كتابة خطة أي لقطة خريطة / when planning any map shot.
- **كيف / how:** Driving, delivery, traffic → road + city basemap. Hiking, flood, wildfire → topographic with hillshade, rivers, contours. Regional comparison → quiet admin boundaries only. Damage or land use → satellite imagery with transparent overlays. Dense events → quiet neutral (grey/dark) map. Globe or 3D only when curvature or depth changes the reading. Name contextual layers separately from thematic layers in the layer list.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/adaptive-basemaps-and-layer-stacks.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md`

### MAP-03 · اختيار نوع الخريطة الموضوعية · Thematic map family choice · 📄 موصوف / documented only
- **ماذا / what:** اختر بين التظليل والرموز النسبية والتجميع والتدفق والسداسيات والكثافة والرحلات المتحركة حسب طبيعة البيانات المكانية. / Pick choropleth, proportional symbol, cluster, flow, hex/tile, density or trip animation by the data's spatial nature. · **متى / when:** حين تتحول البيانات إلى خريطة / when data becomes a map.
- **كيف / how:** Normalised area rates → choropleth (MAP-05). Point magnitude → proportional symbols scaled by AREA (r = √v), not radius. Dense points → clusters, bins or heat. Real movement → flow map or animated trips. Noisy small areas → hex or tile grid (MAP-50). Continuous field → raster/density. One family per shot; switch families with a cut or morph, never overlay two.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/choropleths-symbols-and-flows.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md`

### MAP-04 · اختيار الإسقاط · Projection choice · 📄 موصوف / documented only
- **ماذا / what:** الإسقاط يقرر ما يتشوه (المساحة أو المسافة أو الاتجاه)، فاختره عمدًا للادعاء. / The projection decides what is distorted, so choose it deliberately for the claim. · **متى / when:** قبل رسم أي خريطة عالم أو قارة / before any world or continental map.
- **كيف / how:** Equal-area (d3.geoEqualEarth, geoConicEqualArea) for choropleths and area comparisons. Web Mercator only for tiled slippy context — it inflates high latitudes (Greenland looks like Africa). Orthographic for ‘whole planet’ globe moments (MAP-58…62). Conic conformal for mid-latitude countries (the spain-map block uses it). Note the projection in the source line. Engine: `npm i d3@7.9.0` (installable here).
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/projections-and-normalization.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/deckgl-d3-geo-stack-selection.md`

### MAP-05 · تطبيع خرائط التظليل · Choropleth normalization · 📄 موصوف / documented only
- **ماذا / what:** لوّن المناطق بالمعدلات أو النسب لا بالأعداد الخام، بمخطط تسلسلي مصنَّف. / Fill regions with rates or shares, never raw counts, with a classed sequential scheme. · **متى / when:** أي خريطة تظليل / every choropleth.
- **كيف / how:** Divide by population, area or the right denominator. ColorBrewer sequential at its supported class count, 5–7 classes; diverging only around a meaningful midpoint (0, national average). Compact legend with units beside the map. If huge empty regions dominate (Rub' al Khali, Sahara), consider a tile/hex cartogram (MAP-50). The owner's own 5-step blue ramp is MAP-46.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/projections-and-normalization.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/choropleths-symbols-and-flows.md` · `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/references/color_palettes.md`

### MAP-06 · استراتيجيات تداخل النقاط · Point overlap strategies · 📄 موصوف / documented only
- **ماذا / what:** تجميع بعدّاد للمعاينات الكثيفة، وتفريق (spiderfy) لنقاط قليلة متداخلة، ونقطة مرساة صغيرة داخل الهالات الكبيرة. / Count clusters for dense previews, spiderfy for a few overlaps, and a crisp anchor dot inside big halos. · **متى / when:** مدن متجاورة أو أحداث كثيرة في مكان واحد / neighbouring cities or many events at one place.
- **كيف / how:** Cluster badges that dissolve as the camera zooms; spiderfy when the overlap count is small (≤8); always keep a crisp exact-location dot drawn above rings and halos; draw smaller symbols above larger ones. For video, step through points one at a time with a moving highlight instead of showing all at once.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/point-overlap-strategies.md`

### MAP-07 · طبقات تتكبر مع الخريطة وأخرى ثابتة · Map-space vs screen-stable layers · 📄 موصوف / documented only
- **ماذا / what:** أثناء الزووم تتكبر الجغرافيا والمساحات الحقيقية، أما التسميات والدبابيس والحدود فتحافظ على حجمها على الشاشة. / During a zoom geography scales, but labels, pins, badges and outline strokes keep screen size. · **متى / when:** كل زووم أو دفع كاميرا على خريطة / every zoom or push-in on a map.
- **كيف / how:** Scale polygons, rivers, buffers and impact radii with the camera; keep city dots, labels, callouts and border strokes constant — SVG `vector-effect: non-scaling-stroke`, or a separate HTML overlay that only translates. Change label density in steps (country → region → city), never continuously.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/multiscale-symbols-and-zoom-behavior.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/references/svg-polish-and-crispness.md`

### MAP-08 · سجل الإحداثيات والمصادر · Coordinate & source ledger · 📄 موصوف / documented only
- **ماذا / what:** قبل بناء فيلم خريطة، اكتب لكل طبقة مصدرها وترخيصها وتاريخها ونظام إحداثياتها وهل هي مقاسة أم تخطيطية. / Before a map film, log each layer's source, license, date, CRS and whether it is measured or schematic. · **متى / when:** قبل أول إطار، وفي TEST_REPORT.md / before frame one and in TEST_REPORT.md.
- **كيف / how:** Per layer: source URL, license/attribution, update date, units, CRS, antimeridian policy, gaps. Per rendered layer: who owns the projection. Spot-check ≥3 known places (e.g. Mecca 39.83 E 21.42 N, Cairo 31.24 E 30.04 N, Casablanca −7.59 E 33.57 N) so markers and basemap align. GeoJSON/Turf order is ALWAYS [longitude, latitude].
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/source-method-and-coordinate-ledger.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md`

### MAP-09 · الخرائط الحساسة والبيانات الإنسانية · Sensitive maps & human data · 📄 موصوف / documented only
- **ماذا / what:** خرائط النزاع والنزوح والكوارث والحدود المتنازع عليها تحتاج حالات مؤرخة ومصادر وضبطًا للنبرة. / Conflict, displacement, disaster or disputed-border maps need dated states, sourcing and restraint. · **متى / when:** أي خريطة عن بشر متضررين أو حدود متنازع عليها / any map about harmed people or disputed borders.
- **كيف / how:** Show the date of each map state and the source hierarchy; style measured / estimated / schematic layers differently (solid / dashed / hatched). No particle flows and no team-colour framing for human harm. Keep caveats next to the numbers. Record source and effective date of any disputed border used; for Arab audiences, check which border convention the client expects before rendering.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/adaptive-basemaps-and-layer-stacks.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md`

### MAP-10 · توقيعات حركة الخرائط وضوابطها · Map motion signatures & restraint rules · 📄 موصوف / documented only
- **ماذا / what:** مفردات الحركة المعتمدة للخرائط: تعبئة الدول بالتتابع، إسقاط دبوس مع حلقة نبض، رسم القوس مع طائر يتبعه، كشف التظليل، وزووم عبر viewBox — بلا توهجات وجسيمات زخرفية. / The approved motion vocabulary: country fill stagger, pin drop + pulse ring, arc draw-on + flyer, choropleth reveal, viewBox zoom — no decorative glows or particles. · **متى / when:** عند تصميم حركة أي لقطة خريطة متجهية / when choreographing any vector map shot.
- **كيف / how:** Two lanes: vector (D3 + TopoJSON) or baked basemap (MapLibre, MAP-15). Signatures: country fill stagger 40–80 ms; pin drop + one pulse ring; arc `stroke-dashoffset` draw-on with a flyer riding the head; choropleth reveal; viewBox zoom. Rules: offset labels from their dots; filter far overseas territories out of the frame; no decorative glows, particles or lens flares; never use `tl.call()` for stateful updates (seek breaks) — tween a proxy value instead. Hand-author geo-highlight / geo-flow / flag-borders when the catalog lacks them.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/module.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/SKILL.md`
- **ترخيص / license:** Apache-2.0 (HyperFrames).

## 2. المحركات والخلفيات واستقرار الرندر — Engines, basemaps & render stability

محرك واحد لكل لقطة، وخلفية حقيقية تُرندر بلا ارتعاش. probe.md: `maplibre-gl@6.14.0`, `@turf/turf@7.4.0`, `d3@7.9.0`, `topojson-client`, `world-atlas`, `leaflet` قابلة للتثبيت، و`tile.openstreetmap.org` و`tiles.openfreemap.org` يمكن الوصول إليهما من هنا. / One engine per shot, and a real basemap that renders without shimmer. Per probe.md the GL/geo packages are installable and OSM + OpenFreeMap tile hosts are reachable here.

### MAP-11 · محرك واحد لكل لقطة · One map engine per shot (chooser) · 📄 موصوف / documented only
- **ماذا / what:** اختر تقنية خريطة واحدة لكل لقطة: صورة ثابتة، D3/SVG، MapLibre، Mapbox، MapTiler، أو Cesium. / Pick exactly one map technique per shot. · **متى / when:** عند تقسيم السكربت إلى لقطات / when breaking the script into shots.
- **كيف / how:**

| need | engine | cost here |
|---|---|---|
| location context only | static plate (MAP-12) | free, most deterministic |
| editorial vector map, Arabic labels, our HTML renderer | D3 geo + TopoJSON SVG | 📦 `npm i d3@7.9.0 topojson-client@3.1.0 world-atlas@2.0.2` |
| real vector/satellite basemap, free | MapLibre (MAP-13/14) | 📦 no key; OpenFreeMap reachable |
| globe when zoomed out, 3D buildings | Mapbox (MAP-16) | 🔑 token |
| draw over provider borders/rivers | MapTiler (MAP-17) | 🔑 key |
| terrain & city flyover | Cesium (MAP-18) | 🔑 ion token |
| GPU trips/arcs/hexagons | deck.gl | not probed |
| raster tiles + GeoJSON, simple | Leaflet | 📦 `leaflet@1.9.4` |
All are driven per frame (Remotion `useCurrentFrame` or our seekable HTML timeline), never by wall-clock animation.

- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/SKILL.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/static-map/TECHNIQUE.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10324-geospatial-and-cartographic-visualizatio/references/slippy-map-and-product-stack-selection.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/module.md`

### MAP-12 · لوحة خريطة ثابتة للموقع · Static locator map plate · 📄 موصوف / documented only
- **ماذا / what:** صورة خريطة مُصدَّرة مسبقًا بنسبة الإطار النهائية، فوقها دبابيس وتسميات وأسهم متحركة؛ أرخص لقطة خريطة وأكثرها حتمية. / A pre-exported map image at final aspect with animated pins, labels and arrows on top. · **متى / when:** حين تكفي «أين» بلا تنقل حقيقي / when ‘where’ is enough.
- **كيف / how:** Export the map at ≥ output size and exact aspect (1920×1080, or 3840×2160 if you push in), put it in public/ (Remotion) or next to the page (render_html.cjs), show it full-frame, then animate markers, route SVG paths and Arabic labels as normal layers (Arabic shaping stays in HTML — see ARAB chapter). Push-in 1.00→1.08 over 4–6 s. Keep the tile provider's attribution (‘© OpenStreetMap contributors’) in frame or credits; respect the OSM tile usage policy (a few tiles by hand, never bulk scraping).
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/static-map/TECHNIQUE.md`

### MAP-13 · MapLibre حتمي بلا واجهة · Deterministic headless MapLibre · 📦 بأمر تثبيت / one install
- **ماذا / what:** إعداد MapLibre ليعطي نفس الإطار في كل رندر داخل متصفح بلا واجهة. / MapLibre configured to give the same frame on every headless render. · **متى / when:** أي لقطة بخريطة GL حقيقية / any shot with a real GL basemap.
- **كيف / how:** `interactive:false, fadeDuration:0, preserveDrawingBuffer:true`; Chromium flag `--gl=angle` (Remotion: `chromiumOptions.gl='angle'`); on frame 0 `map.jumpTo(camera)` then wait for the `idle` event before capturing (Remotion: `delayRender`/`continueRender`). Coordinates `[lng,lat]`. Free styles: OpenFreeMap (`https://tiles.openfreemap.org/styles/liberty` — host reachable here). Never call `flyTo`/`easeTo` — they run on wall-clock time.

```js
const map = new maplibregl.Map({ container, style, interactive: false,
  fadeDuration: 0, preserveDrawingBuffer: true, ...cameraAt(0) });
const ready = new Promise(r => map.once('idle', r));   // capture only after this
```
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/SKILL.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/render-stability.md`
- **تثبيت / install:** `npm i maplibre-gl@6.14.0 @turf/turf@7.4.0`
- **ترخيص / license:** maplibre-gl BSD-3-Clause; Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier.

### MAP-14 · لوحة خريطة مجمّدة ضد الارتعاش · Frozen oversized plate (anti-shimmer) · 📦 بأمر تثبيت / one install
- **ماذا / what:** استدعاء jumpTo في كل إطار يجعل الصور الفضائية والظلال ترتعش في الرندر؛ ارندر الخريطة مرة واحدة كبيرة وحرّكها بـ CSS. / Per-frame jumpTo shimmers; render the map once oversized and move it with CSS. · **متى / when:** أي كاميرا متحركة فوق خريطة GL / any moving camera over a GL map.
- **كيف / how:** Render the basemap once at the largest zoom any waypoint reaches, centred on the route's extent midpoint, in an oversized container; keep pitch/bearing constant. Per frame: `scale = 2^(zoom − baseZoom)` (must stay ≤ 1) and translate so the target centre sits mid-frame; apply the identical transform to every HTML label. Keep animating GeoJSON data and paint properties inside the map. Plate sizes: 1920×1080 → 3840×2160; 1080×1920 → ~2700×3840; max side 4096 px. Split very long routes into two plates joined by an editorial transition.

```js
// plate rendered once at baseZoom (the deepest zoom of the shot)
const s = 2 ** (zoomAt(f) - baseZoom);            // ≤ 1
const [px, py] = project(centerAt(f));            // plate pixels
stage.style.transform =
  `translate(${W/2 - px*s}px, ${H/2 - py*s}px) scale(${s})`; // same for labels
```
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/references/render-stability.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/references/render-stability.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/SKILL.md`
- **تثبيت / install:** `npm i maplibre-gl@6.14.0`
- **ترخيص / license:** Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier.

### MAP-15 · خريطة حقيقية مخبوزة مع طبقة متجهات حية · Baked real basemap MP4 + live SVG overlay · 📦 بأمر تثبيت / one install
- **ماذا / what:** يقود MapLibre في Chrome بلا واجهة ليسجّل الخلفية الفضائية أو الداكنة وحدها كفيديو (زووم ثم ثبات)، ويصدّر حدود كل دولة كمسارات SVG لرسمها وتلوينها فوقه. / Bakes only the satellite/dark basemap to MP4 and exports each country's projected border as SVG coords for draw-on, fills, labels and pins. · **متى / when:** لقطة صور فضائية حقيقية مع حدود مرسومة / a real satellite shot with drawn borders.
- **كيف / how:** `NAME=br-ar STYLE=satellite COUNTRIES='Brazil:#22d3ee,Argentina:#f59e0b' CENTER='-60,-25' ZSTART=2.4 ZEND=3.4 FPS=30 DUR=5 node bake-basemap.mjs` → frames waited on map idle each frame, zoom→hold with easeInOutCubic; encode all-intra (`-g 1`) so seeking is exact; overlay `<NAME>-coords.json` borders with dashoffset draw-on, flag/colour fills, pins and callout cards in HTML. Raster tiles tileSize 256; world width = 512·2^zoom. Credit ‘Esri, Maxar, Earthstar Geographics’ (satellite) or ‘© CARTO, © OpenStreetMap’ (dark). The script looks for chrome-headless-shell; point it at the Playwright Chromium in /opt/pw-browsers or run `npx puppeteer browsers install chrome-headless-shell`. Esri/CARTO tile hosts were not probed here.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/bake-basemap.mjs` · `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/module.md`
- **تثبيت / install:** `npm i maplibre-gl@6.14.0 puppeteer@25.14.0`
- **ترخيص / license:** Apache-2.0 script; Esri World Imagery and CARTO tiles carry their own terms of use and mandatory attribution.

### MAP-16 · Mapbox: كرة وأبنية ثلاثية الأبعاد · Mapbox globe & 3D buildings · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** أجمل أنماط افتراضية، كرة أرضية عند الزووم البعيد، ومعالم وأبنية ثلاثية الأبعاد. / Nicer default styles, globe when zoomed out, 3D landmarks. · **متى / when:** لقطة تنتقل من الكوكب إلى شارع في مدينة / a planet-to-street dive.
- **كيف / how:** Same deterministic rules as MAP-13 (no flyTo; jumpTo + idle) and MAP-14 for shimmer. Projection `globe` at low zoom; `fill-extrusion` for buildings with pitch 45–60°. Route draw-on and markers per MAP-32/MAP-52.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/SKILL.md`
- **ترخيص / license:** Mapbox GL JS v2+ is proprietary (Mapbox Terms of Service); needs a Mapbox access token. Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier.

### MAP-17 · MapTiler: التحريك فوق طبقات المزود · MapTiler provider-layer animation · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** ارسم وظلّل فوق حدود وأنهار وتسميات المزود نفسه. / Draw and tint over the provider's own borders, rivers and labels. · **متى / when:** خريطة شرح تعتمد على حدود رسمية وأنهار حقيقية / an explainer built on official borders and real rivers.
- **كيف / how:** Load a MapTiler vector style; filter exact `source-layer`s (waterway, boundary, transportation) and animate only paint (opacity, colour, width) — tiles split features, so start-to-end draws need baked GeoJSON (MAP-23). Pair with decluttering (MAP-22) and the river-triggered reveal (MAP-44). Tokens and timings in `assets/tokens.ts`.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/assets/tokens.ts`
- **ترخيص / license:** Needs a MapTiler API key (free tier exists; commercial terms apply). Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier.

### MAP-18 · طيران فوق التضاريس بـ Cesium · Cesium terrain flyover · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** طيران سينمائي فوق تضاريس ثلاثية الأبعاد ومدن («محاكي طيران»). / Cinematic flight over 3D terrain and cities. · **متى / when:** وادٍ أو مضيق أو جبل يجب أن يُرى عمقه / a gorge, valley or mountain whose depth matters.
- **كيف / how:** Camera follows a pre-smoothed corridor (MAP-29 — proven here) at constant height; heading from the path tangent, small banking from curvature; wait for terrain tiles each frame before capture. Path assets: `assets/cesium-path.json`, `city-path.json`, `flight-path.ts`.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-troubleshooting.md`
- **ترخيص / license:** CesiumJS Apache-2.0, but world terrain / 3D Tiles stream from Cesium ion and need an ion access token. Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier.

### MAP-19 · صور خرائط ثابتة من AWS · Amazon Location static maps · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** صور خرائط مُرندرة مسبقًا أو أنماط جاهزة من خدمة مستضافة. / Pre-rendered map images or style descriptors from a hosted service. · **متى / when:** حين يملك العميل حساب AWS ويريد خرائطه الرسمية / when the client already has AWS and wants its maps.
- **كيف / how:** API key with geo-maps actions; pass `https://maps.geo.{region}.amazonaws.com/v2/styles/Standard/descriptor?key=…` straight to MapLibre with `validateStyle:false`, or call the static-image endpoint for a plate (MAP-12). Keep attribution.
- **الدليل / proof:** `kosif-atlas/skills/368-amazon-location-service/1365-amazon-location-service/SKILL.md`
- **ترخيص / license:** Apache-2.0 skill text; the service is paid AWS (API key).

### MAP-20 · أنماط VersaTiles المجانية · VersaTiles self-hosted styles · 📦 بأمر تثبيت / one install
- **ماذا / what:** مولّدات أنماط MapLibre مجانية بخيار لغة وخطوط SDF. / Free MapLibre style generators with a language option and SDF glyphs. · **متى / when:** حين تريد مظهرًا داكنًا أو رماديًا جاهزًا بلا مفتاح / a ready dark or grey look without a key.
- **كيف / how:** Styles: colorful, eclipse (dark), graybeard (grayscale), neutrino (minimal blueprint), shadow (hillshade-friendly), satellite overlay; each takes `{language}` (try `ar`). Glyphs `{fontstack}/{range}.pbf` (Fira Sans, Noto Sans, Roboto…). Default tiles at tiles.versatiles.org — that host was NOT probed here; OpenFreeMap (reachable) is the fallback. Verify Arabic glyph ranges and RTL shaping before trusting map-rendered Arabic labels (MAP-21).
- **الدليل / proof:** `kosif-atlas/skills/2761-charly-versa/10958-versatiles-style/SKILL.md` · `kosif-atlas/skills/2761-charly-versa/10956-versatiles-fonts/SKILL.md`
- **تثبيت / install:** `npm i maplibre-gl@6.14.0`

### MAP-21 · خطوط SDF والتسميات العربية على خرائط GL · SDF glyphs & Arabic labels on GL maps · 📦 بأمر تثبيت / one install
- **ماذا / what:** MapLibre يحتاج خطوط SDF مقطّعة، والعربية تحتاج إضافة النص من اليمين لليسار — وإلا فالتسميات في HTML. / MapLibre needs SDF glyph PBFs; Arabic needs the RTL text plugin — or put labels in HTML. · **متى / when:** أي تسمية عربية داخل خريطة GL / any Arabic label inside a GL map.
- **كيف / how:** `style.glyphs = '{fontstack}/{range}.pbf'` from the versatiles-fonts release; call `maplibregl.setRTLTextPlugin(url)` before map creation for Arabic shaping. Safer default for video: hide provider labels (MAP-22) and draw Arabic names as an HTML overlay that shares the plate transform (MAP-14) — full shaping, Ruqaa/Naskh fonts, halo via `text-shadow`.
- **الدليل / proof:** `kosif-atlas/skills/2761-charly-versa/10956-versatiles-fonts/SKILL.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md`
- **تثبيت / install:** `npm i maplibre-gl@6.14.0`

### MAP-22 · تنظيف الخريطة الأساسية · Basemap decluttering · 📦 بأمر تثبيت / one install
- **ماذا / what:** احذف تسميات المزود والحدود الداخلية لتبقى جغرافيا القصة وحدها. / Strip provider labels and inner admin borders so only the story geography reads. · **متى / when:** قبل إضافة تسمياتك / before adding your own labels.
- **كيف / how:** On `load`, remove every layer whose `type === 'symbol'` (place, road, water labels) and inner-border layers matched by id (e.g. `/other border/i`); keep country and disputed borders; add your own labels. Logos may be hidden with CSS, but required attribution stays in frame or credits.

```js
map.on('load', () => map.getStyle().layers
  .filter(l => l.type === 'symbol' || /other border/i.test(l.id))
  .forEach(l => map.removeLayer(l.id)));
```
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-geo-prep.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md`
- **تثبيت / install:** `npm i maplibre-gl@6.14.0`

### MAP-23 · طبقات المزود أم GeoJSON مخصص · Provider vectors vs custom GeoJSON · 📄 موصوف / documented only
- **ماذا / what:** معالم بلاطات المزود تصلح للتلاشي والتلوين لكنها لا تُرسم من البداية للنهاية لأن البلاطات تقطعها؛ اخبز GeoJSON مرتبًا للرسم. / Provider tile features can fade and tint but cannot draw start-to-end; bake ordered GeoJSON for meaningful draws. · **متى / when:** حين تخطط لرسم نهر أو حدود أو طريق / when planning to draw a river, border or road.
- **كيف / how:** Context → provider source-layer with an exact filter, paint-only animation. Proposed / historical / disputed / sequenced geometry → custom GeoJSON. Hybrid: provider context + custom evidence styled distinctly. Omit absent optional props — `filter: undefined` hides the layer silently.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-data-sources.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/TECHNIQUE.md`

## 3. البيانات والتحضير الجغرافي — Geo data & preparation

من أين تأتي الهندسة وكيف تُنظَّف قبل أن تتحرك. / Where geometry comes from and how it is cleaned before it moves.

### MAP-24 · متى GeoJSON ومتى البلاطات المتجهة · GeoJSON vs vector-tile threshold · 📄 موصوف / documented only
- **ماذا / what:** مجموعات صغيرة ثابتة كـ GeoJSON؛ الآلاف إلى الملايين أو البيانات المعتمدة على الزووم تحتاج بلاطات متجهة. / Small static sets ship as GeoJSON; large or zoom-dependent data needs vector tiles. · **متى / when:** عند تحميل طبقة بيانات / when loading a data layer.
- **كيف / how:** ≤ a few hundred features → GeoJSON source directly. Larger → MVT from Martin/pg_tileserv or a PMTiles file (MAP-25), reprojected to EPSG:3857, simplified per zoom. A wrong `source-layer` name renders nothing, silently. Simplify any GeoJSON over ~5 MB (mapshaper) before using it in a film.
- **الدليل / proof:** `kosif-atlas/skills/2307-geospatial-engineering/8857-serve-vector-tiles/SKILL.md` · `kosif-atlas/skills/1650-portaljs/4640-portaljs-add-map/SKILL.md`

### MAP-25 · خط PMTiles وGeoParquet · PMTiles & GeoParquet pipeline · 📄 موصوف / documented only
- **ماذا / what:** حوّل أي ملف جغرافي إلى أرشيف بلاطات بلا خادم للرندر وملف GeoParquet للاستعلام. / Turn any geo file into a serverless tile archive plus a GeoParquet file. · **متى / when:** بيانات ضخمة (مبانٍ، نقاط اهتمام) / big data (buildings, POIs).
- **كيف / how:** `ogr2ogr -t_srs EPSG:4326` → normalised GeoJSON; `tippecanoe -zg --drop-densest-as-needed` → `.pmtiles` (MapLibre reads it by range requests via the pmtiles protocol); DuckDB writes GeoParquet with a bbox struct and Hilbert ordering. Warn at ≥500 MB; above 2 GB keep parquet only. GDAL/tippecanoe were not probed here.
- **الدليل / proof:** `kosif-atlas/skills/1650-portaljs/4639-portaljs-add-geo/SKILL.md` · `kosif-atlas/skills/2761-charly-versa/10951-osm-tools-layer/SKILL.md`

### MAP-26 · التحليل المكاني بـ DuckDB · DuckDB spatial analysis · 📄 موصوف / documented only
- **ماذا / what:** SQL فوق GeoJSON وShapefile وGPX وGeoParquet للمسافات والاحتواء والكثافة قبل فيلم الخريطة. / SQL over geo files for distances, containment and density feeding a map film. · **متى / when:** حين يحتاج الرقم المعروض حسابًا جغرافيًا حقيقيًا / when an on-screen number needs real geo maths.
- **كيف / how:** `LOAD spatial; SET geometry_always_xy=true;` `ST_Point(lon,lat)` (longitude first); real metres with `ST_Distance_Spheroid` on POINT_2D; `ST_Contains` for point-in-polygon; H3 hex binning via the community extension; export with `COPY … (FORMAT GDAL, DRIVER 'GeoJSON')`. duckdb was not in the probe list.
- **الدليل / proof:** `kosif-atlas/skills/1366-duckdb-skills/3111-spatial/SKILL.md` · `kosif-atlas/skills/1366-duckdb-skills/3111-spatial/references/functions.md`

### MAP-27 · بيانات Overture Maps المفتوحة · Overture Maps open data · 📄 موصوف / documented only
- **ماذا / what:** بيانات عالمية مجانية بصيغة GeoParquet (أماكن، مبانٍ، طرق، حدود إدارية، يابسة وماء) بلا مفتاح. / Free global GeoParquet with no API key. · **متى / when:** نقاط اهتمام أو أعداد مبانٍ لمدن عربية / POI dots or building counts for Arab cities.
- **كيف / how:** Read `s3://overturemaps-us-west-2/release/<RELEASE>/theme=…/type=…/*` with httpfs; ALWAYS filter `bbox.xmin/xmax/ymin/ymax` first (predicate pushdown); find the latest release in the STAC catalog (mirror noted 2026-03-18.0). S3 reachability was not probed here.
- **الدليل / proof:** `kosif-atlas/skills/1366-duckdb-skills/3111-spatial/references/overture.md` · `kosif-atlas/skills/1366-duckdb-skills/3111-spatial/SKILL.md`
- **ترخيص / license:** Overture data mixes CDLA-Permissive-2.0 and ODbL by theme — attribute per theme.

### MAP-28 · OSM عبر Overpass لخطوط الأنهار والطرق · OSM via Overpass for centerlines · 📄 موصوف / documented only
- **ماذا / what:** طرق OpenStreetMap تعطي هندسة أنهار وطرق مفصلة (~0.3 كم بين الرؤوس) حيث Natural Earth خشن جدًا. / OSM ways give detailed river/road geometry where Natural Earth is too coarse. · **متى / when:** مضيق أو نهر أو طريق يُطار فوقه عن قرب / a close flight along a gorge, river or road.
- **كيف / how:** Query Overpass for the named way/relation and export GeoJSON; overpass-api.de is often busy — mirror overpass.kumi.systems (neither host probed here). Braided rivers must be routed into ONE source→mouth path by graph shortest path, never greedy nearest-endpoint chaining (it bounces between channels). Then feed MAP-29.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/scripts/prep-geo.mjs`
- **ترخيص / license:** OpenStreetMap data is ODbL — ‘© OpenStreetMap contributors’ attribution required.

### MAP-29 · تجهيز ممر الكاميرا · Camera corridor path preparation · ✅ مُثبت هنا / proven here
- **ماذا / what:** حوّل خط نهر أو طريق متعرج إلى ممر كاميرا ناعم قبل الطيران فوقه. / Turn a jagged river/road centerline into a smooth camera corridor. · **متى / when:** قبل أي طيران متتبع لمسار (Cesium، plate، three.js) / before any path-following flight.
- **كيف / how:** Clip a window of the source line → resample to even 0.1 km spacing → moving-average smooth ±2.8 km, 2 passes → dampen lateral deviation toward the straight chord (DAMP 0.45) → check heading deltas change gradually. Never Douglas-Peucker (it concentrates curvature into corners). Pure Node builtins, no install. Ran here on the shipped sample: `clip 106 → resample 297 → smooth → 297 pts · 17.1 km`, heading deltas every 1.5 km between −12° and +9°.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/scripts/prep-cesium-path.mjs` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/assets/sample-river.geojson` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-flyover-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/cesium/references/3d-troubleshooting.md`

### MAP-30 · مرساة التسمية في أبعد نقطة داخلية · Label anchor at pole of inaccessibility · 🟢 جاهز / ready
- **ماذا / what:** تسمية الدولة توضع في أعمق نقطة داخل المضلع (داخل صندوق القصة) لا في المركز الهندسي الذي قد يقع قرب الحافة أو خارجها. / Country labels sit at the most interior point, not the centroid. · **متى / when:** تسميات الدول على أي خريطة / country labels on any map.
- **كيف / how:** Grid-sample the polygon bbox (46×46), keep points inside, choose the one with maximum distance to the boundary; clip the search to a per-country story bbox; then a small operator nudge in degrees (e.g. [0, 0.6]). `prep-geo.mjs` uses only Node builtins but needs YOUR source geodata (polygons too large to ship; sample outputs are in `assets/sample-data/`).
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-geo-prep.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/scripts/prep-geo.mjs`

### MAP-31 · توحيد أسماء الأماكن العربية · Arabic place-name normalisation · ✅ مُثبت هنا / proven here
- **ماذا / what:** يطابق أسماء المدن المكتوبة بحرية بغض النظر عن الهمزة والتاء المربوطة والألف المقصورة وأل التعريف والتهجئة الإنجليزية. / Matches free-text city names regardless of hamza, taa marbuta, alif maqsura, the article or English spelling. · **متى / when:** ربط بيانات العميل (جداول مبيعات، قوائم) بنقاط الخريطة / joining client tables to map points.
- **كيف / how:** `norm()`: lowercase → أ/إ/آ→ا → ة→ه → ى→ي → strip leading ال → collapse spaces; then an alias index per city (عربي + English). Lives in the tested sales-geo engine; `npx vitest run src/engine/fusion/sales/sales-geo-engine.test.ts` passed 4/4 in this container.

```js
const norm = s => s.toLowerCase().trim()
  .replace(/[أإآ]/g, 'ا').replace(/ة/g, 'ه').replace(/ى/g, 'ي')
  .replace(/^ال/, '').replace(/\s+/g, ' ');
```
- **الدليل / proof:** `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts:51` · `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.test.ts`

## 4. المسارات والرحلات والرسم — Routes, journeys & draw-on

الخط الذي يتحرك عبر الخريطة: رحلة طيران، قافلة، نهر، مسار تقدم. / The line that travels: a flight, a caravan, a river, a progress path.

### MAP-32 · رسم مسار الدائرة العظمى · Great-circle route draw-on · 📦 بأمر تثبيت / one install
- **ماذا / what:** مسار طيران أو شحن يرسم نفسه على الجيوديسي بين مدينتين مع نقاط وأسماء المدن. / A flight or shipping route drawing itself along the geodesic. · **متى / when:** رحلة بين مدينتين بعيدتين / a long-distance hop.
- **كيف / how:** Turf: `greatCircle(from,to,{npoints:100})`; if it splits at the antimeridian keep the longest segment; `length()` in km; per frame `lineSliceAlong(route, 0, max(0.001, len*progress))` into a GeoJSON source. Travel window 20 %→82 % of the shot (ease-in-out), hold the rest. For a visually straight line use a plain 2-point LineString. Without Turf: slerp on the sphere, then project with D3 into an SVG path and use `stroke-dashoffset`.

```js
// slerp between two [lng,lat] points, t in 0..1 (no Turf needed)
const R = Math.PI / 180, v = ([lo, la]) =>
  [Math.cos(la*R)*Math.cos(lo*R), Math.cos(la*R)*Math.sin(lo*R), Math.sin(la*R)];
function gc(a, b, t) { const A = v(a), B = v(b);
  const w = Math.acos(A.reduce((s, x, i) => s + x*B[i], 0));
  const k1 = Math.sin((1-t)*w)/Math.sin(w), k2 = Math.sin(t*w)/Math.sin(w);
  const [x, y, z] = A.map((x, i) => k1*x + k2*B[i]);
  return [Math.atan2(y, x)/R, Math.asin(z)/R]; }
```
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md`
- **تثبيت / install:** `npm i @turf/turf@7.4.0`

### MAP-33 · رحلة على خريطة حبر قديمة · Parchment map journey · 📦 بأمر تثبيت / one install
- **ماذا / what:** خريطة ورقية قديمة بالحبر، طريق أحمر متقطع تمشي عليه قافلة، أعلام وكروت ورقية وعدّاد سنة ومسافة. / An ink-drawn parchment map, a red dashed route walked by a caravan, flags, paper cards and a year/distance HUD. · **متى / when:** رحلة تاريخية أو حج أو طريق تجارة / a historical journey, Hajj route or trade road.
- **كيف / how:** Owner canvas style `STY.mapjourney` (alias `map-journey`): 16:9, calm, 1.9 words/s; fonts Aref Ruqaa (titles, cities, seas) + Amiri (body, numbers); palette paper #EAD9B5, edge #C9AA72, sea #BFCDBE, ink #3B2716, route #9C2A1C, gold #B8862B, desk #24170E, card #F4E9D0; each line ‘المكان: ما حدث’ becomes a stop; route = Catmull-Rom through stops (24 samples/segment); sfx pop/swish/swell. The watched reference (34 s, 30 fps) adds: coastlines ink-draw in ~2 s, triple water lines, map tilts to rotateX ~50–60°, camel sprite follows by arc length (MAP-35) through 7 stops, flag springs up + paper card with dotted leader, HUD counts 100→6,230 km and year 1325→1326, cloud pass as the only transition, final pull-out.
- **الدليل / proof:** `app/public/js/10_studio.js:737` · `kosif-tool/styles/map-journey/SKILL.md` · `kosif-tool/styles/map-journey/STYLE.json` · `style:map-journey`
- **تثبيت / install:** `cd /home/user/app && npm install   # owner Basma studio app that hosts STY.mapjourney`
- **ترخيص / license:** Basma style is MIT-derived from motion-starter-kit styles/map-journey; keep its credit. kosif-tool scaffold: `python3 tools/kosif.py scaffold map-journey <dir>` (verified: writes STYLE/PLAN/REQUEST/TEST_REPORT/words.json, no map code).

### MAP-34 · إسقاط خطوط الطول والعرض على SVG · Equirectangular lon/lat → SVG with latitude squash · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** إسقاط بسيط يضع إحداثيات حقيقية على ورقة SVG، مع ضغط أفقي بجيب تمام خط عرض المنطقة. / A simple projection placing real coordinates on an SVG sheet with a cos(lat) horizontal squash. · **متى / when:** خريطة إقليمية مرسومة يدويًا (المتوسط والجزيرة) / a hand-styled regional map.
- **كيف / how:** `x = (lon + 18) · K · cos(30°)`, `y = (47 − lat) · K`, K chosen per frame width; draw sea polygons over the parchment; push synthetic polygon edges far outside the sheet so they clip cleanly. Choose the cos() latitude at the region's centre (≈24° for Saudi Arabia — the owner's MAP-45 uses exactly that).

```js
const K = W / 80, C = Math.cos(30 * Math.PI / 180);
const P = ([lon, lat]) => [(lon + 18) * K * C, (47 - lat) * K];
const d = 'M' + ring.map(P).map(p => p.join(',')).join('L') + 'Z';
```
- **الدليل / proof:** `style:map-journey`

### MAP-35 · متتبع مسار بطول القوس مع توقف · Arc-length route follower with dwell · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رأس المسار (جمل، طائرة، أفاتار) يتحرك بسرعة ثابتة على طول القوس ويتوقف عند كل محطة، والخط يُرسم خلفه. / The route head moves at constant arc-length speed, dwells at each stop, and the line draws behind it. · **متى / when:** أي رحلة متعددة المحطات / any multi-stop journey.
- **كيف / how:** Sample the Catmull-Rom route into a cumulative-length table; per stop store arrive/depart times; head position = lookup(length(t)); drawn path = dasharray up to the head; remainder dashed (6/4) in #9c2a1c. Camera zooms out on long legs, in on arrival. Basma's map-journey already has `catmull()` + `INK.at(route,u)` to build on.

```js
// lens[i] = cumulative length at sample i; stops[k] = {arrive, depart, s}
function headS(t) { let s = 0;
  for (const [k, st] of stops.entries()) {
    if (t < st.arrive) { const p = stops[k-1];
      const u = ease((t - p.depart) / (st.arrive - p.depart));
      return p.s + (st.s - p.s) * Math.max(0, u); }
    s = st.s; } return s; }        // dwell = clamp at st.s until depart
```
- **الدليل / proof:** `style:map-journey` · `app/public/js/10_studio.js:737`

### MAP-36 · كاميرا الخريطة المائلة 2.5D · Tilted 2.5D map camera · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الخريطة كلها تميل بمنظور (rotateX) والكاميرا الافتراضية تنزل من الأعلى إلى زاوية مائلة وتتبع الموضوع. / The whole map tilts in perspective and a virtual camera descends from top-down to oblique and tracks the subject. · **متى / when:** رحلة سينمائية بلا محرك ثلاثي الأبعاد / a cinematic journey without a 3D engine.
- **كيف / how:** Wrap the SVG map in a container with `perspective: 1600px`; tween `rotateX` 0 → 50–60° during the descent; pan/zoom happen INSIDE the SVG (viewBox or inner transform) so the tilt stays fixed; sprites billboard upright with `rotateX(-angle)` so they stand on the plane. Rhythm: zoom out on long legs, zoom in on arrival, ~4 s pulses; final pull-out to overview.
- **الدليل / proof:** `style:map-journey`

### MAP-37 · خط زمني بمحطات وخريطة رحلة · Milestone timeline & map route (MG-045/046) · 📄 موصوف / documented only
- **ماذا / what:** خط أفقي يتقدم ويفتح بطاقة مؤرخة عند كل محطة (MG-045)، وخط ينمو بين ثلاث نقاط على خريطة بأسماء المدن (MG-046). / A dated-milestone line and a three-city map route. · **متى / when:** قصة شركة أو سيرة أو رحلة قصيرة / a company story, biography or short trip.
- **كيف / how:** MG-045 (10 s): 0–1 s title, 1–7 s four stations, 7–10 s overview; equal spacing only when durations are not being represented. MG-046 (8 s): 0–1 s map, 1–5 s route, 5–8 s summary; distinguish an approximate path (dashed) from a true geographic route (solid). Local build: SVG/GeoJSON projected with d3-geo + dashoffset growth.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

### MAP-38 · رسم مسار بمحطات تنبثق · Route line with popping station dots · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مسار SVG يُرسم بإزاحة الشرطة، ونقاط المحطات تنبثق لحظة وصول الرأس. / An SVG route draws by dashoffset; station dots pop as the head reaches them. · **متى / when:** خريطة مترو، رحلة، أو خطوات منتج / a metro map, trip or product steps.
- **كيف / how:** 3 s total draw; station pop = scale 0→1.15→1 in ~250 ms back-out exactly when `drawn ≥ stationLength` (use `getPointAtLength` lengths precomputed once). Reference palette: ground #e6e6e0, ink #08090d, gold #c9a23a.
- **الدليل / proof:** `style:pm-ercankeskinx-ec2568`

### MAP-39 · مسار تقدم على جبل · Progress path up terrain with avatar · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مسار SVG بباقٍ متقطع، والجزء المقطوع خط صلب ليموني ينمو، وأفاتار عند رأسه. / A dashed remaining path, a solid lime travelled part growing, an avatar at the head. · **متى / when:** تقدم نحو هدف (خطوات، تحدٍّ، مراحل) / progress toward a goal.
- **كيف / how:** Two copies of the same path: bottom dashed (#485b62, 6/6), top solid lime #c8ff1a with dashoffset = L·(1−p); avatar placed with `getPointAtLength(L·p)` and rotated to the tangent; footprints stepping upward as accent. Ground #08070b, 4:5.
- **الدليل / proof:** `style:pm-marklaunches-3b9492`

### MAP-40 · خريطة وثائقية · Documentary map · 📄 موصوف / documented only
- **ماذا / what:** خريطة أرشيفية مع صور ومسارات وتسميات بنبرة وثائقية. / An archival map with photos, routes and labels in a documentary tone. · **متى / when:** تاريخ، تحقيق، قصة مكان / history, investigation, a place's story.
- **كيف / how:** 2.5D photo rig over a map plate (MAP-12); route draw-on; Ken Burns 1.00→1.06 over 4–6 s; grain 2–4 %, vignette 10–15 %. Scaffold verified here: `python3 tools/kosif.py scaffold documentary-map <dir>` (writes STYLE.md, PLAN.md, TEST_REPORT.md, words.json — map code is yours to write).
- **الدليل / proof:** `kosif-tool/styles/documentary-map/SKILL.md` · `kosif-tool/styles/documentary-map/STYLE.json` · `kosif-tool/playbooks/diagrams.md`

### MAP-41 · رحلة طيران نيويورك–باريس · NYC–Paris flight block · 📦 بأمر تثبيت / one install
- **ماذا / what:** خريطة واقعية بأسلوب أبل: طائرة تطير من مدينة إلى أخرى مع دائرة علامة ونبضة هبوط. / Apple-style realistic map: a plane flies city to city with a marker circle and a landing pop. · **متى / when:** أي «من هنا إلى هناك» قصير (6 ث) / any short ‘from here to there’.
- **كيف / how:** `npx -y hyperframes@0.8.164 add nyc-paris-flight` → swap `assets/map-nyc-paris.png` for your plate (e.g. Riyadh→Cairo from MAP-12), edit the inline city constants, `npx hyperframes preview`, `npx hyperframes render`. 1920×1080, 6 s. The local copy lacks the declared `assets/sfx-mix.wav` — add licensed SFX yourself.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/nyc-paris-flight/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/nyc-paris-flight/nyc-paris-flight.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/nyc-paris-flight.mdx`
- **تثبيت / install:** `npx -y hyperframes@0.8.164 add nyc-paris-flight`
- **ترخيص / license:** Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT.

### MAP-42 · أقواس ضوء ترسم بين المدن (3D) · 3D light arcs between cities · 📦 بأمر تثبيت / one install
- **ماذا / what:** أقواس مضيئة تنمو من مدينة مركزية إلى خمس مدن أخرى كأن شبكة تشتعل. / Glowing arcs grow from a hub city to five others, like a network lighting up. · **متى / when:** خاتمة «الاتصال»، شبكة توزيع، فروع شركة / a ‘connection’ finale, distribution network, branches.
- **كيف / how:** Per arc: `QuadraticBezierCurve3` with the control point lifted 90 units at the midpoint → `TubeGeometry(curve, 80, 1.1, 6)` with additive #FFC56B material, opacity .85; grow with `geometry.setDrawRange(0, indexCount · clamp(k·1.4 − i·0.08))` where k = segment progress (16.55–17.6 s in the source) — 0.08 stagger per arc. Bloom from the light family makes it sing.
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:185-201`
- **تثبيت / install:** `npm i three@0.186.1`

### MAP-43 · شريط نهر يُرسم ويجري · River ribbon reveal & flow · 🟢 جاهز / ready
- **ماذا / what:** أنبوب مسطّح على منحنى يكشف نفسه تدريجيًا ويجري ماؤه (إزاحة خريطة النورمال). / A flattened tube along a curve that draws on and flows. · **متى / when:** نهر على تضاريس أو خريطة ثلاثية الأبعاد / a river on 3D terrain or map.
- **كيف / how:** `K3.makeRibbon(curve, {radius:11, flatten:.3, segments:220, color:'#6fb4d6', emissive:'#1a5f85', repeat})` (emissive .55, opacity .94); per frame `mesh.userData.reveal(p)` (setDrawRange) and `.flow(t, .9)` (normal-map offset). Feed the curve from a smoothed corridor (MAP-29) for real rivers (Nile, Euphrates).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/three-kit.js:255` · `kosif-studio/motion/kit/three-kit.js:255`

### MAP-44 · إضاءة الدول عند وصول النهر · River-triggered country reveal · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** بينما يُرسم النهر أو الطريق، كل دولة يدخلها تشغّل تسلسلها: الحدود تُرسم، التعبئة تتوهج، والاسم يرتفع. / As a river draws on, each country it enters runs border draw → fill bloom → label rise. · **متى / when:** نهر عابر للدول (النيل، الفرات) أو طريق تجاري / a transnational river or trade road.
- **كيف / how:** Precompute per country the arc-length fraction where the line first enters it (point-in-polygon walk) → trigger = start + stop·(end − start). Per country, time since trigger drives: border draw 2.5 s (constant, so long borders do not flash by) → fill opacity overshoot 0 → 0.625 → 0.5 over 1.0 s → label 0.7 s. River window 0.3–8.0 s. Beat length = max(trigger + phases) + tail. Reference implementation is on MapTiler; the same timing ports to a D3/SVG map with `npm i d3@7.9.0 @turf/turf@7.4.0` (no key).
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-geo-prep.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/assets/tokens.ts`
- **ترخيص / license:** Reference build needs a MapTiler API key. Technique docs MIT; rendering through Remotion needs a Remotion company license for teams above the free tier.

## 5. الخرائط الموضوعية وخرائط البيانات — Thematic & data maps

مناطق وفقاعات وتدفقات ونقاط — بما فيها خريطة المملكة المختبرة هنا. / Regions, bubbles, flows and dots — including the Saudi map tested here.

**كتل HyperFrames للخرائط / HyperFrames map blocks** (`npx -y hyperframes@0.8.164 add <id>`, Apache-2.0 + GSAP Standard license):

| id | ماذا / what | المدة | الأطلس / data | قوة |
|---|---|---|---|---|
| `world-map` | تظليل عالمي + كرة صغيرة دوّارة / world choropleth + globe inset | 14 s | world-atlas@2 110m | MAP-47 |
| `us-map` | تظليل ولايات بكشف متتابع / staggered state choropleth | 12 s | us-atlas@3 10m | MAP-47 |
| `spain-map` | تظليل بإسقاط مخروطي / conic-conformal choropleth | 12 s | es-atlas@0.6.0 | MAP-47 |
| `us-map-bubble` | فقاعات متناسبة / proportional bubbles | 12 s | us-atlas | MAP-48 |
| `us-map-flow` | أقواس تدفق / OD flow arcs | 12 s | us-atlas | MAP-49 |
| `us-map-hex` | خريطة سداسية / hex tiles | 10 s | inline SVG | MAP-50 |
| `north-korea-locked-down` | زووم ودائرة حمراء / zoom + red scribble | 7 s | raster plate | MAP-51 |
| `nyc-paris-flight` | طائرة بين مدينتين / plane hop | 6 s | raster plate | MAP-41 |

*الدليل / proof:* `kosif-one/vendor/hyperframes/registry/blocks` · `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/maps/module.md`

### MAP-45 · خريطة المملكة التخطيطية بالمناطق · Schematic Saudi Arabia map — 13 regions, drill-down · ✅ مُثبت هنا / proven here
- **ماذا / what:** حدود المملكة مرسومة بالكود مع مقار المناطق الثلاث عشرة والمدن كفقاعات بحجم القيمة؛ نقرة على منطقة تفتح مدنها، ومدينة تفتح أحياءها، بزووم viewBox متحرك وترتيب جانبي. / Hand-coded Kingdom outline with 13 regional seats and cities as value-sized bubbles, drill-down by animated viewBox zoom. · **متى / when:** أي بيانات سعودية بالمناطق أو المدن (مبيعات، فروع، سكان) / any Saudi regional or city data.
- **كيف / how:** `project(lat, lon, {w:1000, h:820})`: lon scaled by cos(24°), bounds lon 34.4–56.2, lat 15.9–32.6; OUTLINE = 38 lon/lat points as one polygon; bubble r = max(6, √(v/max)·58) for regions, ·26 for cities, districts max(3.5, √·9); fill from the heat ramp MAP-46; 3 levels country → region → city with viewBox tween. Tests: `npx vitest run src/engine/fusion/sales/sales-geo-engine.test.ts` → 4/4 passed here. For video, drive the viewBox from the timeline instead of clicks.

```js
const project = (lat, lon, { w = 1000, h = 820 } = {}) => {
  const k = Math.cos(24 * Math.PI / 180), x0 = 34.4 * k, x1 = 56.2 * k;
  return [ (lon * k - x0) / (x1 - x0) * w, (32.6 - lat) / (32.6 - 15.9) * h ]; };
const r = (v, max) => Math.max(6, Math.sqrt(v / max) * 58);   // regions
```
- **الدليل / proof:** `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts` · `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.test.ts` · `kosif-earth-ci-fork/ui/features/sales-map.js:49`

### MAP-46 · تدرّج الخريطة الأزرق · Sequential blue map heat ramp · 🟢 جاهز / ready
- **ماذا / what:** تدرج أزرق أحادي اللون بخمس درجات لتلوين فقاعات الخريطة حسب القيمة. / A single-hue blue sequential ramp colouring map bubbles by value. · **متى / when:** أي تظليل أو فقاعات بهوية هادئة / any choropleth or bubbles in a calm identity.
- **كيف / how:** `heat(v,max) = clamp(ceil(v/max·5), 1, 5)`, 0 → line colour. Steps: #cfe3fb · #9cc5f5 · #5f9fea · #2f77d6 · #0b4fb0 (+ `var(--sk-line)` for zero). Matches the 5–7-class rule of MAP-05.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/features/sales-map.js:39` · `kosif-earth-ci-fork/app/src/engine/fusion/sales/sales-geo-engine.ts:87`

### MAP-47 · خرائط تظليل بكشف متتابع · Choropleth staggered-reveal blocks · 📦 بأمر تثبيت / one install
- **ماذا / what:** خرائط تظليل جاهزة (الولايات المتحدة، إسبانيا، العالم) تكشف المناطق واحدة تلو الأخرى مع أسطورة متدرجة وكرة دوّارة صغيرة. / Ready choropleths with staggered region reveals, gradient legend and (world) a rotating globe inset. · **متى / when:** خريطة بيانات بسرعة؛ استبدل الأطلس بحدود عربية / a fast data map; swap the atlas for Arab borders.
- **كيف / how:** `npx -y hyperframes@0.8.164 add world-map` (world-atlas@2 countries-110m, 14 s) · `add us-map` (us-atlas@3 states-10m, 12 s) · `add spain-map` (es-atlas@0.6.0, D3 conic conformal, 12 s). Engine D3 v7 + topojson-client via CDN, GSAP paused timeline (`window.__timelines`), Inter, 1920×1080. To localise: filter `world-atlas` to Arab League ISO codes, `fitExtent` the region, switch Inter → IBM Plex Sans Arabic, mirror the legend for RTL.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/world-map/world-map.html` · `kosif-one/vendor/hyperframes/registry/blocks/us-map/us-map.html` · `kosif-one/vendor/hyperframes/registry/blocks/spain-map/spain-map.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/world-map.mdx`
- **تثبيت / install:** `npx -y hyperframes@0.8.164 add world-map`
- **ترخيص / license:** Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT.

### MAP-48 · خريطة الفقاعات · Proportional bubble map · 📦 بأمر تثبيت / one install
- **ماذا / what:** مدن بفقاعات متناسبة ونداءات قيم وخطوط ربط؛ تتركب فوق خريطة التظليل. / Proportional city bubbles with value callouts and connection lines; composable with the choropleth. · **متى / when:** مقارنة مدن بقيم / comparing cities by magnitude.
- **كيف / how:** `npx -y hyperframes@0.8.164 add us-map-bubble` (12 s). Bubble area ∝ value (r = √v), grow 0→r with back-out, smaller bubbles on top, anchor dot inside each (MAP-06). For KSA reuse MAP-45 instead.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/us-map-bubble/us-map-bubble.html` · `kosif-one/vendor/hyperframes/registry/blocks/us-map-bubble/registry-item.json`
- **تثبيت / install:** `npx -y hyperframes@0.8.164 add us-map-bubble`
- **ترخيص / license:** Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT.

### MAP-49 · خريطة التدفق · Origin–destination flow map · 📦 بأمر تثبيت / one install
- **ماذا / what:** أقواس من الأصل إلى الوجهة بين المدن فوق خريطة أساسية. / Origin–destination arcs between cities over a basemap. · **متى / when:** تجارة، هجرة، شحن، مسافرون / trade, migration, shipping, travellers.
- **كيف / how:** `npx -y hyperframes@0.8.164 add us-map-flow` (12 s). Arcs as quadratic SVG paths (control point lifted ~20 % of chord), width ∝ volume, dashoffset draw-on in stagger, flyer dot on the head; never particle flows for human harm (MAP-09).
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/us-map-flow/us-map-flow.html` · `kosif-one/vendor/hyperframes/registry/blocks/us-map-flow/registry-item.json`
- **تثبيت / install:** `npx -y hyperframes@0.8.164 add us-map-flow`
- **ترخيص / license:** Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT.

### MAP-50 · خريطة سداسية · Hex tile map · 📦 بأمر تثبيت / one install
- **ماذا / what:** كل منطقة سداسي بوزن متساوٍ بتعبئة بيانات واختصار. / Each region an equal-weight hexagon with a data fill and abbreviation. · **متى / when:** حين تبتلع المناطق الكبيرة الفارغة الانتباه / when big empty regions would dominate.
- **كيف / how:** `npx -y hyperframes@0.8.164 add us-map-hex` (10 s, inline SVG, no CDN geo). For the Gulf or Arab world hand-author the hex grid (one hex per country/region, keep rough adjacency), fill with MAP-46, reveal in a diagonal stagger.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/us-map-hex/us-map-hex.html` · `kosif-one/vendor/hyperframes/registry/blocks/us-map-hex/registry-item.json`
- **تثبيت / install:** `npx -y hyperframes@0.8.164 add us-map-hex`
- **ترخيص / license:** Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT.

### MAP-51 · زووم دولة مع دائرة حمراء · Country zoom with red scribble circle · 📦 بأمر تثبيت / one install
- **ماذا / what:** زووم على خريطة واقعية نحو دولة، دائرة حمراء مخربشة، تسمية منبثقة وغسيل أحمر تحريري. / Realistic raster map zooms into a country, a red scribble circle, a pop-up label and a reddish editorial wash. · **متى / when:** خبر أو تحقيق عن بلد / a news or investigative beat about one country.
- **كيف / how:** `npx -y hyperframes@0.8.164 add north-korea-locked-down` (7 s, 1920×1080, `assets/korea-map.png`) → swap the plate and target; the scribble is a hand-jittered SVG ellipse drawn with dashoffset (~0.6 s) after the zoom settles; wash = red multiply layer at low opacity.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/north-korea-locked-down/north-korea-locked-down.html` · `kosif-one/vendor/hyperframes/registry/blocks/north-korea-locked-down/registry-item.json` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/north-korea-locked-down.mdx`
- **تثبيت / install:** `npx -y hyperframes@0.8.164 add north-korea-locked-down`
- **ترخيص / license:** Apache-2.0 block code; its timeline uses GSAP 3.14.2 under the GSAP Standard ‘no charge’ license (gsap.com/standard-license), not MIT.

### MAP-52 · علامات وتسميات داخل الخريطة · Map-native circle & symbol markers · 📦 بأمر تثبيت / one install
- **ماذا / what:** نقاط المدن وأسماؤها كطبقات circle وsymbol في GeoJSON بمقاسات للفيديو. / City dots and names as GeoJSON circle + symbol layers sized for video. · **متى / when:** تسميات لاتينية داخل خريطة GL / Latin labels inside a GL map.
- **كيف / how:** Circle: colour #f03b20, radius 12, white stroke 4. Symbol: `text-field` from properties, anchor top, offset [0, 0.9], size 28, dark text with 3 px white halo, `text-allow-overlap: true`. Scale sizes with output resolution (×2 at 4K). Arabic names → HTML overlay instead (MAP-21).
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/mapbox/TECHNIQUE.md` · `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maplibre/TECHNIQUE.md`
- **تثبيت / install:** `npm i maplibre-gl@6.14.0`

### MAP-53 · رسم خريطة شوارع وإسقاط دبابيس · SVG street map draw + pin drop · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شوارع مدينة SVG تُرسم بالخط، ثم تسقط الدبابيس بارتداد متتابع، ودبوس بطل بحلقة نبض وشريحة اسم. / City streets stroke-draw, pins drop with bounce stagger, one hero pin with pulse ring and label chip. · **متى / when:** تطبيق أماكن، فروع، توصيل / a places app, branches, delivery.
- **كيف / how:** Streets: dashoffset draw with 30–60 ms stagger per street; pins: y −40 px → 0 with bounce, stagger 60 ms; hero pin: pulse ring scale 1→2.4, opacity .6→0 over 900 ms, then label chip slides 8 px. Palette from the reference: #f7f7f7 ground, teal #1db394 accent, mint #e2f2ee, text #1a1a1a.
- **الدليل / proof:** `style:pm-danilowm-d3720d`

### MAP-54 · خريطة نقاط تجمعات المدن · Dot-cluster city map · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** جسيمات تتجمع في عناقيد عند مواقع المدن بلا خريطة أساسية، مع تسميات وأعداد تتصاعد. / Particles gather into clusters at city positions, no basemap, labels with ticking counts. · **متى / when:** حضور عالمي أو شبكة عملاء بأسلوب بسيط / global presence in a minimal look.
- **كيف / how:** ~800 dots; each assigned a city by weight; spring from random start to a disc of radius 40–80 px around the projected city; label + counter tick up when the cluster settles. Ink #08080a / #f5f6f8 with orange #ff5a1f accent.
- **الدليل / proof:** `style:pm-blushpetal795-0c85c2`

### MAP-55 · خريطة عالم نقطية بكبسولات صور · Dotted world map with avatar pills · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** يابسة العالم شبكة نقاط من قناع، وكبسولات بدوائر أحرف متداخلة وأعداد تنبثق عند المدن. / Land as a dot grid from a mask; pills with overlapping initial circles and counts pop at cities. · **متى / when:** مجتمع، مستخدمون، مؤسسون حول العالم / a community or user map.
- **كيف / how:** Dot 4 px, gap 8 px sampled from a land mask (world-atlas → canvas → `getImageData`); pills pop with 250 ms back-out in stagger; 2–3 overlapping initial circles (#3b6fe0, #22b55a, #f2b83a) + count. Ground #f5f6fa, text #111318.
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

### MAP-56 · خريطة أعمدة ضوئية · Spike map · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقاط بخطوط عمودية طولها يساوي القيمة مع توهج. / Points with vertical lines whose height is the value, with glow. · **متى / when:** كثافة أو مراجعات أو قيم كثيرة على خريطة / many values over a map.
- **كيف / how:** ~1,534 points; spike = thin triangle (base 4–6 px) from the projected point upward, height ∝ value, grow in a sweep from west to east (or by value rank); faint glow; orange #f05a0f on #14130f. Pairs with a slight perspective tilt (MAP-36).
- **الدليل / proof:** `style:pm-jesscaroline7-1ff7cb`

### MAP-57 · عناصر خرائط أرشيفية · Archival map-fragment collage props · ✅ مُثبت هنا / proven here
- **ماذا / what:** إكسسوارات كولاج توحي بالجغرافيا: قطعة خريطة قديمة مطوية، خريطة مصغرة، خيط أحمر يعبر الخريطة، شريط خط زمني مرسوم. / Collage props that suggest geography: folded era map fragment, map inset, red string across a map, hand-drawn timeline strip. · **متى / when:** فيديو تاريخي بأسلوب سكراب بوك أرشيفي / a vox-history scrapbook film.
- **كيف / how:** Part of the vox-history INVENTORY rotated through clips (sepia, grain, brass tacks, red string). What is proven: the planner places these props into clip prompts — `node --test tests/production-profiles.test.mjs` passed 10/10 here; the visuals themselves are generated per project.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/vox-history.mjs:15-18` · `fastify-motion-bro/tests/production-profiles.test.mjs`

## 6. الكرات الأرضية والمنظر المداري — Globes & orbital views

الكوكب كله: كرة واقعية بغلاف جوي، أضواء ليلية من المدار، وكرات نقطية بأقواس. / The whole planet: a realistic globe, night lights from orbit, and dotted globes with arcs.

### MAP-58 · كوكب الأرض مع غلاف جوي · Procedural Earth with atmosphere · 📦 بأمر تثبيت / one install
- **ماذا / what:** كرة بمزج نهار/ليل وأضواء مدن وغيوم متحركة وحافة غلاف جوي (فرينل). / A day/night globe with city lights, moving clouds and a fresnel atmosphere rim. · **متى / when:** افتتاحية «الكوكب» أو انتقال من الفضاء / a planet opener or space-to-ground transition.
- **كيف / how:** Sphere 64×64; `orientation = dot(normal, sun)·0.5 + 0.5`; `dayNight = smoothstep(0.4, 0.6, orientation)`; city lights × (1 − orientation)² × 1.5; clouds on a second sphere r = 1.01 with uv offset by time (speed 0.01); fresnel pow 4 × atmosphere colour × 0.3; bump 0.03. Sun (1, 0.2, 0.5); day #4db2ff, twilight #bd5f1b. Textures (day/night/clouds) must be licensed — NASA images host is blocked here (403); Wikimedia Commons is reachable.
- **الدليل / proof:** `kosif-atlas/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl/examples/earth-shader.js`
- **تثبيت / install:** `npm i three@0.186.1`

### MAP-59 · خريطة الأضواء من المدار · Orbit-at-night lights map · 📦 بأمر تثبيت / one install
- **ماذا / what:** منظر قمر صناعي ليلي منمّق: 26 ألف نقطة مضيئة على طول نهر ودلتا ومدن كثيفة وبلدات متناثرة وساحل أزرق خافت. / A stylised night satellite view: 26,000 glowing points along a river, a delta fan, dense cities, scattered towns and a faint coast. · **متى / when:** مصر/النيل، مدن الخليج ليلًا، «المستقبل» / Egypt & the Nile, Gulf cities at night, futurism.
- **كيف / how:** Nile `x(z) = 18·sin(z/95) + 9·sin(z/31)`; 9,000 points along it, 11,000 in a delta fan (angle ±0.75, distance pow(r, 0.7)·230), 2,600 Cairo, 1,400 Alexandria, 1,600 desert towns; 900-point coast. Colours gold #FFB65C, white #FFF1D6, cyan #7FE8FF 15–20 %, coast #5FA8FF; bloom 1.25 / 0.75 / 0.12. Camera dives y 1500 → 210 with ease and a slight roll.
- **الدليل / proof:** `kosif-one/projects/egypt-2120-animation/index.html:168-202`
- **تثبيت / install:** `npm i three@0.186.1`

### MAP-60 · كرة أرضية نقطية بإسقاط كروي · Orthographic dot / halftone globe · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** يابسة الأرض كشبكة نقاط على كرة تدور، بحجم وسطوع حسب العمق، مع شبكة خطوط عرض وطول أو محور مائل. / Land as a dot grid on a rotating orthographic sphere, size/brightness by depth, with graticule or a tilted axis. · **متى / when:** رقم عالمي (71 % ماء)، علامة تقنية، افتتاحية / a global stat, tech brand, opener.
- **كيف / how:** Rasterise continent polygons (world-atlas 110m) to a lat/lon dot grid ONCE (~2,000 dots, or a 2 px halftone with 15° graticule); each frame rotate (6–10 °/s) + tilt, project orthographically, cull back-facing (z < 0); dot size and alpha ∝ depth; add night shade and an atmosphere glow ring. Looks: navy keynote (#000 + glow #64d2ff, style:infographic), cream science-book (#efecdd, ink #1a1a18, red axis #c9452c, style:pm-hbcoop-de365c), black half-sphere with glowing rim and pings (style:pm-steventey-0d20e4). Build: `npm i d3@7.9.0 topojson-client@3.1.0 world-atlas@2.0.2`.

```js
// dots: [{lon,lat}] sampled once from the land mask
const R = Math.PI / 180;
function drawGlobe(ctx, dots, rot, tilt, cx, cy, r) {
  for (const d of dots) {
    const l = (d.lon + rot) * R, p = d.lat * R;
    let x = Math.cos(p) * Math.sin(l), y = Math.sin(p), z = Math.cos(p) * Math.cos(l);
    [y, z] = [y * Math.cos(tilt*R) - z * Math.sin(tilt*R), y * Math.sin(tilt*R) + z * Math.cos(tilt*R)];
    if (z < 0) continue;                                  // back-face cull
    ctx.globalAlpha = 0.25 + 0.75 * z;
    ctx.fillRect(cx + x * r, cy - y * r, 1 + 1.5 * z, 1 + 1.5 * z); } }
```
- **الدليل / proof:** `style:infographic` · `style:pm-hbcoop-de365c` · `style:pm-steventey-0d20e4`

### MAP-61 · كرة أرضية بأقواس اتصال · Globe with great-circle arcs (wireframe / particle) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كرة سلكية أو من جسيمات تدور، بنقاط مضيئة بهالات وأقواس دائرة عظمى متقطعة ترسم بين الأزواج. / A rotating wireframe or particle globe with haloed dots and dashed great-circle arcs drawing between pairs. · **متى / when:** لاعبون أو مستخدمون أو فروع متصلة حول العالم / connected players, users or offices worldwide.
- **كيف / how:** Orthographic lat/long grid (wireframe) or ~3,000 land-mask points (particle); rotate ~10 °/s; dots with ring halos; arcs: sample MAP-32's slerp at 64 steps, lift the middle by 10–20 % of r, cull hidden segments, draw-on 400 ms each with dashes; outer glow ring ~20 px. Looks: lime #d8f24a + white on navy #07131f (style:pm-deifosv-04e4d3); orange #e24b0f glow on light #f5f4f2 (style:pm-manuelogomigo-f33ca9); pings arcing over a black half-sphere (style:pm-steventey-0d20e4).
- **الدليل / proof:** `style:pm-deifosv-04e4d3` · `style:pm-manuelogomigo-f33ca9` · `style:pm-steventey-0d20e4`

### MAP-62 · كرة غبار مع تسميات · Dust point-cloud globe with leader labels · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كرة من سحابة نقاط تدور ببطء مع تسميات بنقطة قائدة تنبثق عند مواقع. / A slowly rotating point-cloud sphere with leader-dot labels popping at locations. · **متى / when:** تعريف شخصي أو شركة بـ «أين نعمل» / a personal or company ‘where we work’ beat.
- **كيف / how:** THREE.Points with additive blending + bloom; rotation 0.15 rad/s; 4–6 labels, stagger 200 ms: a dot on the surface, a 1 px leader line, a mono label in cyan #7fe3ff / amber #ffb070 on #05050a; hide a label when its anchor rotates behind (z < 0).
- **الدليل / proof:** `style:pm-madhav-xo-f97f20`

## توليفات قوية — Power combos

- **رحلة الحج على الرقعة / Hajj on parchment:** MAP-33 رحلة الحبر + MAP-35 متتبع القوس + MAP-36 الكاميرا المائلة + ARAB (رقعة وأميري) + عداد مسافة من TYPE + طبقة صوت المؤثرات من AUDIO — ثم MAP-08 لتثبيت مكة والمدينة بإحداثيات حقيقية.
- **من الفضاء إلى الحي / Space-to-street dive:** MAP-58 كوكب بغلاف جوي → قطع مطابق إلى MAP-14 لوحة MapLibre المجمّدة → MAP-45 خريطة المملكة لتعمّق المنطقة/المدينة؛ توهج الحافة من LIGHT وانتقال سحابي (cloud pass) من TRANS.
- **النيل يضيء الدول / The Nile lights its nations:** MAP-29 ممر ناعم + MAP-43 شريط النهر أو MAP-44 تسلسل الدول (2.5 / 1.0 / 0.7 ث) + MAP-30 مراسي التسميات + تسميات عربية HTML (MAP-21).
- **شبكة الفروع / Branch network finale:** MAP-42 أقواس ضوء ثلاثية الأبعاد من مقر الشركة + bloom من LIGHT + عدّاد عدد الفروع من TYPE، أو نسخة مسطحة بـ MAP-49 للرسائل الرسمية.
- **رقم عالمي واحد / One global stat:** MAP-60 كرة نقطية ترتفع وتدور + عداد نسبة ضخم (TYPE) + تحوّل النقاط إلى شبكة/دونات (CHART) كما في style:infographic.
- **خبر عاجل عن بلد / Breaking news country beat:** MAP-12 لوحة ثابتة + MAP-51 الدائرة الحمراء + شريط أسفل الشاشة وعنوان عربي (ARAB/TYPE) + MAP-09 تاريخ الحالة ومصدرها بجانب الرقم.
- **مبيعات المناطق / Regional sales story:** MAP-31 توحيد أسماء مدن العميل → MAP-45 فقاعات المملكة بتدرج MAP-46 → MAP-01 مخطط أعمدة مرتب للترتيب الدقيق، مع خريطة صغيرة كمؤشر موقع.
- **مسار تقدم المنتج / Product progress path:** MAP-39 مسار الجبل أو MAP-38 محطات تنبثق + بطاقات واجهة من UI + مؤثرات «تك» على كل محطة من AUDIO مضبوطة على words.json.

## أخطاء ممنوعة — Never do

- **ترتيب [lat, lng] في GeoJSON أو Turf** — GeoJSON/Turf/DuckDB كلها [longitude, latitude]؛ الخطأ يضع مكة في المحيط الهندي بصمت. افحص 3 أماكن معروفة (MAP-08).
- **flyTo / easeTo أو أي حركة بساعة الحائط** — تعمل بزمن حقيقي لا بالإطار، فيختلف كل رندر؛ استخدم jumpTo + idle أو لوحة مجمّدة (MAP-13/14).
- **jumpTo لكل إطار فوق صور فضائية** — ترتعش البلاطات والظلال؛ ارندر اللوحة مرة واحدة وحرّكها بـ CSS بمقياس ≤ 1.
- **تظليل بالأعداد الخام** — المناطق الكبيرة أو المكتظة تبتلع القصة؛ قسّم على السكان أو المساحة واستخدم 5–7 فئات (MAP-05).
- **Web Mercator لمقارنة المساحات** — يضخّم خطوط العرض العليا؛ استخدم إسقاطًا متساوي المساحة (MAP-04).
- **تسميات عربية داخل GL بلا إضافة RTL** — تتفكك الحروف وتنعكس؛ أخفِ تسميات المزود وضع العربية في طبقة HTML (MAP-21/22).
- **رسم معالم بلاطات المزود من البداية للنهاية** — البلاطات تقطع الخطوط فيظهر الرسم متقطعًا عشوائيًا؛ اخبز GeoJSON مرتبًا (MAP-23).
- **Douglas-Peucker لتبسيط مسار كاميرا** — يركّز الانحناء في زوايا حادة فتلتف الكاميرا فجأة؛ أعد التعيين ونعّم بالمتوسط المتحرك (MAP-29).
- **جسيمات متدفقة وألوان فرق لخرائط الأذى البشري** — تحوّل المأساة إلى مباراة؛ استخدم حالات مؤرخة وخطوطًا صلبة/متقطعة/مخططة (MAP-09).
- **حذف إسناد OSM أو Esri أو CARTO** — شرط ترخيص (ODbL وشروط الخدمات)؛ أبقه في الإطار أو في الشارة الختامية.
- **tl.call() لتحديثات الحالة في خط زمني قابل للتقديم** — يفشل عند القفز إلى إطار؛ احسب الحالة من الزمن مباشرة (MAP-10).
- **خريطة لأن البيانات فيها أسماء دول فقط** — الترتيب والمقارنة الدقيقة تُقرأ أسرع كأعمدة مرتبة (MAP-01).

## أقوى 5 حركات توقيع — 5 signature moves

1. **MAP-45 — خريطة المملكة بالمناطق والتعمّق / Saudi regions drill-down:** ✅ مختبرة هنا؛ حوّل النقر إلى خط زمني وستحصل على أقوى خريطة بيانات عربية فورًا.
2. **MAP-33 + MAP-35 — رحلة الرقعة والقافلة / parchment caravan journey:** كودها في استوديو بسمة وشكلها شوهد في style:map-journey — رحلة تاريخية كاملة بخط رقعة.
3. **MAP-32 — الدائرة العظمى ترسم نفسها / great-circle draw-on:** slerp من 6 أسطر أو Turf؛ رحلة بين أي مدينتين في دقائق.
4. **MAP-60 / MAP-61 — كرة نقطية بأقواس / dot globe with arcs:** افتتاحية عالمية أنيقة بلا محرك ثلاثي الأبعاد، من world-atlas وحده.
5. **MAP-44 — النهر يضيء الدول / river-triggered reveal:** أدق توقيت سردي في العائلة (2.5 / 1.0 / 0.7 ث) — قابل للنقل إلى D3 بلا مفتاح.
