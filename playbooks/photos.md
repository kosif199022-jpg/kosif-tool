# Photos and parallax — الصور والبارالاكس

This playbook covers films built from still photographs: layered camera rigs, 2.5D depth, planar parallax, dynamic masks, Ken Burns moves and the handoff from a photo into a graphic treatment. It gives Claude concrete numbers so that a photo sequence reads as one deliberate camera operator reframing, not as a slideshow with a zoom. It also fixes the licensing discipline for every image that enters a project.

يغطي هذا الدليل الأفلام المبنية من صور ثابتة: منصّات الكاميرا الطبقية، العمق 2.5D، البارالاكس المستوي، الأقنعة الديناميكية، حركات كين بيرنز، والانتقال من الصورة إلى المعالجة الجرافيكية. يعطي أرقامًا محددة حتى تُقرأ سلسلة الصور كحركة مصوّر واحد يعيد التأطير، لا كعرض شرائح مع تكبير. ويثبّت أيضًا انضباط الترخيص لكل صورة تدخل المشروع.

## 1. When to use / متى تستخدمه

Use this playbook when the user supplies photographs (a personal archive, product shots, documentary stills, portraits) or when the narration needs real-world evidence that vector graphics cannot carry. It fits documentary explainers, anniversary and memorial pieces, real-estate and travel reels, founder stories, and mixed-media ads where one photo anchors a claim. Do not use it to hide a lack of motion: if the only available motion is a zoom on a stock image, build the scene with kinetic type or a diagram and keep the photo as a short insert. Skip the parallax rig when the long side of a photo is under 1600 px, or when the subject fills the frame with no separable background; a clean Ken Burns hold beats a parallax that tears.

**Licensing of imagery.** Usable: the user's own photos; client-supplied images with written confirmation of rights; public-domain and CC0 files; CC BY material with the attribution line kept in the film description and in `ASSETS.md`; stock images with a saved license receipt and ID. Not usable: frames from the reference video, images scraped from search results, CC BY-ND files (the treatment here is a derivative) and NC licenses on commercial work, editorial-only stock in ads. Identifiable faces in advertising need a model release. AI-generated images are allowed only when the user asked for them, are declared in STYLE.md and the delivery note, and are never presented as documentary evidence. Every file gets a row in `ASSETS.md`: path, source URL, author, license, attribution text, date, modifications.

**بالعربية:** استخدم الدليل عندما يقدّم المستخدم صورًا حقيقية أو عندما يحتاج السرد إلى دليل من الواقع: الوثائقي، قصص المؤسسين، العقارات، السفر، الإعلانات المختلطة. لا تستخدمه لتغطية غياب الحركة؛ إن كانت الحركة الوحيدة تكبيرًا على صورة ستوك فابنِ المشهد بالتايبوغرافي أو المخطط واجعل الصورة لقطة قصيرة. تجاوز البارالاكس إذا كان الضلع الأطول أقل من 1600 بكسل أو إذا لم يكن الموضوع قابلًا للفصل عن الخلفية. الترخيص: صور المستخدم، أو صور العميل بإذن مكتوب، أو CC0، أو CC BY مع سطر النسبة، أو ستوك بإيصال ترخيص محفوظ. ممنوع: إطارات من الفيديو المرجعي، صور من نتائج البحث، تراخيص ND أو NC في عمل تجاري. الوجوه في الإعلانات تحتاج إذن نموذج. الصور المولّدة بالذكاء الاصطناعي فقط بطلب المستخدم ومع التصريح بها. كل ملف له صف في `ASSETS.md`.

## 2. Visual grammar / القواعد البصرية

- One camera per sequence. Every photo in a scene lives inside a single rig transform (translate, scale, rotate ≤ 1°), so cuts between photos feel like one operator reframing rather than a new engine starting.
- Fixed depth order: background plate, mid-ground, subject cut-out, then graphics (titles, pills, arrows). When a cut-out exists, the title sits between the background and the subject; this one rule produces most of the "premium" feel.
- Three layers are enough. Five or more parallax layers read as a pop-up book.
- Edges never show. Oversize each layer by at least twice its maximum travel plus 4%, and put a blurred 1.3× copy of the background (blur 24 px) behind it so a worst-case drift reveals bokeh, not transparency.
- Unify the stack: one shared grade (a single LUT or curves preset applied to the whole composition), 2–4% film grain over everything, a 10–15% vignette. A cut-out gets a contact shadow (blur 24 px, offset 0, opacity 0.35) so it belongs to the plate.
- Depth-of-field cue: about 1 px of blur per 100 px of simulated distance behind the focal layer, never on the subject.
- Text on a busy photo sits on a gradient scrim (opacity 0.6 → 0 over 35% of the frame height), never on a flat black box.
- Portraits keep the eyes in the top third; never push into a face past 1.08×.
- In 9:16, lock the subject on a vertical third; horizontal pans travel at most 6% of frame width, pushes at most 12% of scale.
- Source resolution: the long side must be at least 1.5× the displayed size at the maximum scale, so a 1080×1920 output pushed to 1.12 needs roughly a 2400 px long side.

**بالعربية:** كاميرا واحدة لكل تسلسل. ترتيب الطبقات ثابت: خلفية، وسط، موضوع مقصوص، ثم الجرافيك، والعنوان بين الخلفية والموضوع. ثلاث طبقات تكفي. لا تظهر الحواف: كل طبقة أكبر من أقصى حركتها بمرتين زائد 4٪، ونسخة مموّهة 1.3× خلف الخلفية. وحّد الطبقات بتدرج لوني واحد وحبيبات 2–4٪ وفينييت 10–15٪ وظل تلامس تحت المقصوص. تمويه نحو 1 بكسل لكل 100 بكسل عمق خلف طبقة التركيز. النص فوق صورة مزدحمة على تدرج شفاف لا مربع أسود. العيون في الثلث الأعلى ولا تكبير على وجه فوق 1.08×. دقة المصدر 1.5× حجم العرض عند أقصى تكبير.

## 3. Motion mechanics / ميكانيكا الحركة

**Ken Burns done well.** Scale travels 1.00 → 1.06 over a 4–6 s hold (about 1–1.5% per second) with a hard ceiling of 1.12; the pan in the same hold stays under 6% of frame width. Velocity is constant: `linear`, or `cubic-bezier(0.37, 0, 0.63, 1)` only when the move must visibly settle before a cut. A visible eased stop at the end of every photo is the loudest slideshow tell. Alternate the move across cuts (push-in, lateral pan, slow pull-out); never two identical push-ins in a row. The pan follows the reading direction of the scene, so Arabic narration defaults to right → left.

**Planar parallax.** Give each layer a depth factor `d`: background 0.15, mid 0.45, subject 1.0, foreground occluder 1.4. Layer offset = camera offset × d, so a 40 px camera pan moves the background 6 px, the mid 18 px, the subject 40 px and the occluder 56 px. Push-ins scale the same way: layer scale = 1 + (zoom − 1) × d, with camera zoom ≤ 1.10. All layers move in the same direction; opposing layers "swim". A hold is one intentional move of 1200–2400 ms with `cubic-bezier(0.45, 0, 0.55, 1)` plus a drift that never stops: `x = 6·sin(2πt/7) + 4·sin(2πt/11)` px and `y` on periods of 9 s and 13 s, total amplitude ≤ 12 px. Speed limits at 1080 px width: pans 30–60 px/s, pushes 1.5–3% of scale per second, rotation ≤ 0.3°/s.

**2.5D depth.** Use `perspective: 1200px` on the rig and `translateZ` per layer: background −400 px, mid −120 px, subject 0, occluder +200 px. Pre-scale distant layers by `(1200 − z) / 1200` so the composition looks normal at rest, and give the background 1.5× cover. Rotation budget: rotateY ≤ 6°, rotateX ≤ 4°; an 8° orbit takes 2000–3000 ms with easeInOutSine.

**Dynamic masks.** Wipes last 500–700 ms with `cubic-bezier(0.65, 0, 0.35, 1)` and a feather of 1–2% of frame width. The mask leads the photo motion by 60–90 ms so the shape appears to reveal the image rather than carry it. Shape masks animate their geometry, not only their position: a circle grows from r = 0 to full in 450 ms while the photo inside counter-scales 1.15 → 1.00. A cut-out that pops through a title uses a spring with damping 14, stiffness 120, mass 1 (settles in about 600 ms) from scale 0.92.

**Entrances, exits, stagger.** Entrance: opacity 0 → 1 and scale 1.04 → 1.00 over 400 ms, `cubic-bezier(0.22, 1, 0.36, 1)`. Exit: 250–300 ms, `cubic-bezier(0.55, 0, 1, 0.45)`; the next photo starts 2 frames before the previous one is gone. Stacks and grids stagger 80–120 ms (60 ms for grids of six or more), with at most six photos on screen and no more than one photo arriving every 2 frames. Holds: 2.5–5 s per photo under narration, 1.2–2 s in a beat-driven montage, never under 8 frames.

**Photo-to-graphic transitions.** Tracing: an outline path draws over the subject for 900 ms (stroke-dashoffset, easeInOutCubic); the photo fades over 300 ms starting at 700 ms; the line remains and the vector fill arrives 150 ms later. Treatment ladder: full colour → duotone (300 ms) → halftone or posterised (300 ms) → flat vector (400 ms), each step landing on a beat or word boundary; luma threshold 0.5, halftone dot pitch 8–12 px at 1080 width.

**بالعربية:** كين بيرنز: تكبير 1.00 إلى 1.06 خلال 4–6 ثوانٍ بسرعة ثابتة (`linear`)، السقف 1.12، التحريك الجانبي أقل من 6٪ من العرض، ولا توقف مُنعَّم في نهاية كل صورة، ولا حركتين متطابقتين متتاليتين. البارالاكس: معامل عمق لكل طبقة (0.15 خلفية، 0.45 وسط، 1.0 موضوع، 1.4 أمامي)، الإزاحة = إزاحة الكاميرا × المعامل، الجميع في اتجاه واحد، حركة مقصودة 1200–2400 مللي ثانية زائد انجراف دائم بجيبين (7 ثوانٍ و11 ثانية) بسعة ≤ 12 بكسل. حدود السرعة: 30–60 بكسل/ثانية تحريكًا، 1.5–3٪ تكبيرًا في الثانية. العمق 2.5D: perspective 1200، translateZ من −400 إلى +200، دوران ≤ 6° أفقيًا و4° رأسيًا. الأقنعة: 500–700 مللي ثانية، تنعيم 1–2٪، القناع يسبق الصورة بـ 60–90 مللي ثانية. دخول 400 مللي ثانية، خروج 250–300، تدرج 80–120 بين الصور، ستة صور كحد أقصى. التحول إلى جرافيك: رسم الخط 900 مللي ثانية ثم تلاشي الصورة 300 ثم تعبئة المتجه.

## 4. Scene recipes / وصفات المشاهد

**A. Documentary hold** — one photo under narration, lower-third title.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 400 ms | photo enters: opacity 0 → 1, scale 1.04 → 1.00 | cubic-bezier(0.22, 1, 0.36, 1) |
| 0 ms | 4500 ms | push-in 1.00 → 1.055, pan right → left 4% of width | linear |
| 600 ms | 1100 ms | lower-third wipes in from the right edge, feather 1.5% | cubic-bezier(0.65, 0, 0.35, 1) |
| 4200 ms | 4500 ms | exit; the next photo is already entering at 4433 ms | cubic-bezier(0.55, 0, 1, 0.45) |

**B. Three-layer parallax reveal** — background, mid, cut-out subject, title between them.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 600 ms | background fades in at scale 1.15, mid at 1.06 | easeOutCubic |
| 200 ms | 800 ms | subject pops from scale 0.92 with its contact shadow | spring, damping 14, stiffness 120 |
| 400 ms | 2600 ms | camera pans 40 px right → left; depths 0.15 / 0.45 / 1.0 | cubic-bezier(0.45, 0, 0.55, 1) |
| 900 ms | 1400 ms | right-aligned title slides in between background and subject | cubic-bezier(0.22, 1, 0.36, 1) |
| 2600 ms | 5000 ms | drift only, push 1.5% per second | linear |

**C. Collage to hero** — a 2×3 grid collapses to one photo.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 700 ms | six tiles enter from the top-right cell, 60 ms stagger, 400 ms each | cubic-bezier(0.22, 1, 0.36, 1) |
| 700 ms | 2200 ms | grid drifts 20 px upward; each tile has a micro push 1.00 → 1.03 | linear |
| 2200 ms | 2800 ms | five tiles exit toward their nearest edge (250 ms, 40 ms stagger); the hero tile grows to full frame | cubic-bezier(0.65, 0, 0.35, 1) |
| 2800 ms | 6000 ms | hero hold, push-in 1.00 → 1.06 | linear |

**D. Photo to vector** — a traced outline hands the scene to graphics.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 2000 ms | photo hold, push 1.00 → 1.03 | linear |
| 2000 ms | 2900 ms | outline draws over the subject, stroke-dashoffset 1 → 0 | easeInOutCubic |
| 2700 ms | 3000 ms | photo fades to 0 (optional duotone pass at 2000–2300 ms) | easeInCubic |
| 3050 ms | 3400 ms | flat vector fill wipes in behind the line, right → left | cubic-bezier(0.65, 0, 0.35, 1) |
| 3400 ms | 5000 ms | the vector scene continues on the same camera drift, so the handoff is invisible | linear |

**E. 2.5D orbit card** — product or portrait with a foreground occluder.

| start | end | action | easing |
|---|---|---|---|
| 0 ms | 500 ms | rig at rotateY −4°; layers fade in back to front, 100 ms stagger | easeOutCubic |
| 500 ms | 3000 ms | rotateY −4° → +4°, translateZ fixed; the occluder passes in front | easeInOutSine |
| 1200 ms | 1700 ms | caption pill attached to the subject plane (same transform) | spring, damping 16, stiffness 140 |
| 3000 ms | 4500 ms | settle at +2°, push-in 1.00 → 1.04 | linear |

**بالعربية:** خمس وصفات قابلة لإعادة الاستخدام: (أ) ثبات وثائقي بصورة واحدة مع عنوان سفلي يدخل من اليمين؛ (ب) كشف بارالاكس بثلاث طبقات والعنوان بين الخلفية والموضوع؛ (ج) شبكة ست صور تنهار إلى صورة بطل؛ (د) صورة تتحول إلى متجه عبر خط يُرسم فوقها؛ (هـ) بطاقة 2.5D تدور 8° مع عنصر أمامي يمر. الجداول أعلاه تعطي البداية والنهاية والفعل والإيزنج لكل خطوة؛ انسخ الأرقام إلى PLAN.md وعدّل الأزمنة على توقيت الكلمات.

## 5. Implementation / التنفيذ

Both snippets express the same idea: the frame is a pure function of time, the camera is one path, and each layer multiplies that path by its depth factor. Oversizing hides edges; the entrance is 400 ms; the drift never stops.

**Remotion / React.** Drop this scene inside a `<Sequence>` in `starters/remotion/src/Film.tsx`, nested in the starter's `CameraRig`; images live in `public/` and load through `staticFile`. The easing helpers in `src/easing.ts` can replace the inline functions.

```tsx
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

type Layer = { src: string; depth: number; blur?: number };

// One camera: a 2 s intentional pan plus a two-sine drift that never stops.
const camera = (t: number, holdS: number) => {
  const pan = interpolate(t, [0.4, 2.4], [0, -40], {
    extrapolateLeft: "clamp", extrapolateRight: "clamp",
    easing: (u) => -(Math.cos(Math.PI * u) - 1) / 2,
  });
  const drift = 6 * Math.sin((2 * Math.PI * t) / 7) + 4 * Math.sin((2 * Math.PI * t) / 11);
  const zoom = 1 + 0.06 * Math.min(t / holdS, 1); // 1.00 -> 1.06, linear
  return { x: pan + drift, y: 3 * Math.sin((2 * Math.PI * t) / 9), zoom };
};

export const ParallaxPhoto: React.FC<{ layers: Layer[]; holdS?: number }> = ({ layers, holdS = 5 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const cam = camera(frame / fps, holdS);
  const enter = interpolate(frame, [0, 0.4 * fps], [0, 1], {
    extrapolateRight: "clamp", easing: (u) => 1 - Math.pow(1 - u, 5),
  });
  return (
    <AbsoluteFill style={{ background: "#0b0b0d", opacity: enter }}>
      {layers.map((l) => {
        const scale = (1 + (cam.zoom - 1) * l.depth) * (1.04 + 0.12 * l.depth); // oversize hides edges
        return (
          <Img key={l.src} src={staticFile(l.src)} style={{
            position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover",
            filter: l.blur ? `blur(${l.blur}px)` : undefined,
            transform: `translate(${cam.x * l.depth}px, ${cam.y * l.depth}px) scale(${scale})`,
          }} />
        );
      })}
    </AbsoluteFill>
  );
};
```

**Canvas (seek mode).** This is the shape `starters/html-canvas` expects: load assets, then expose `window.__kosif = { duration, seek(t) }` and resolve `window.__kosifReady`. Render with `node tools/render_html.cjs --in index.html --out film.mp4 --mode seek --audio voice.mp3`; the renderer calls `seek` once per frame, so nothing may depend on wall-clock time.

```js
// parallax.js — deterministic: every frame is a pure function of t (seconds).
const W = 1080, H = 1920, DURATION = 5;
const canvas = document.getElementById("film"); canvas.width = W; canvas.height = H;
const ctx = canvas.getContext("2d");
const LAYERS = [ // depth: 0 = infinitely far, 1 = subject plane, > 1 = in front
  { src: "assets/bg.jpg", depth: 0.15, blur: 3 },
  { src: "assets/mid.png", depth: 0.45, blur: 1 },
  { src: "assets/subject.png", depth: 1.0, blur: 0 },
];
const load = (src) => new Promise((ok, err) => { const i = new Image(); i.onload = () => ok(i); i.onerror = err; i.src = src; });
const easeInOut = (u) => -(Math.cos(Math.PI * u) - 1) / 2;
const clamp01 = (u) => Math.max(0, Math.min(1, u));

function camera(t) {
  const pan = -40 * easeInOut(clamp01((t - 0.4) / 2));            // 40 px, right -> left, over 2 s
  const drift = 6 * Math.sin(2 * Math.PI * t / 7) + 4 * Math.sin(2 * Math.PI * t / 11);
  return { x: pan + drift, y: 3 * Math.sin(2 * Math.PI * t / 9), zoom: 1 + 0.06 * clamp01(t / DURATION) };
}

function seek(t, imgs) {
  const cam = camera(t);
  ctx.clearRect(0, 0, W, H);
  ctx.globalAlpha = 1 - Math.pow(1 - clamp01(t / 0.4), 5);         // 400 ms entrance
  LAYERS.forEach((l, i) => {
    const s = (1 + (cam.zoom - 1) * l.depth) * (1.04 + 0.12 * l.depth); // oversize hides edges
    const img = imgs[i], cover = Math.max(W / img.width, H / img.height) * s;
    const w = img.width * cover, h = img.height * cover;
    ctx.save();
    ctx.filter = l.blur ? `blur(${l.blur}px)` : "none";
    ctx.translate(W / 2 + cam.x * l.depth, H / 2 + cam.y * l.depth);
    ctx.drawImage(img, -w / 2, -h / 2, w, h);
    ctx.restore();
  });
  ctx.globalAlpha = 1;
}

window.__kosifReady = Promise.all(LAYERS.map((l) => load(l.src))).then((imgs) => {
  window.__kosif = { duration: DURATION, seek: (t) => seek(t, imgs) };
});
```

For a 2.5D rig in HTML, wrap the layers in a `perspective: 1200px` container and drive `rotateY`/`translateZ` from the same `camera(t)`; the renderer's virtual mode handles CSS transforms if you prefer DOM layers over Canvas. Masks are `clip-path` (DOM) or `ctx.clip()` with a feathered gradient (Canvas). Cut-outs are PNGs with alpha prepared outside the film; the film never attempts background removal.

**بالعربية:** المقطعان يعبّران عن الفكرة نفسها: الإطار دالة خالصة للزمن، الكاميرا مسار واحد، وكل طبقة تضرب هذا المسار في معامل عمقها. في Remotion ضع المشهد داخل `Sequence` في `Film.tsx` تحت `CameraRig` وحمّل الصور من `public/` عبر `staticFile`. في Canvas اتبع شكل `starters/html-canvas`: حمّل الأصول ثم عرّف `window.__kosif = { duration, seek }` وارندر بـ `render_html.cjs --mode seek`. الأقنعة بـ `clip-path` أو `ctx.clip()`، والمقصوصات ملفات PNG بشفافية تُجهَّز خارج الفيلم.

## 6. Arabic and RTL notes / ملاحظات العربية

- Reveal and pan direction default right → left; mask wipes start at the right edge; grids fill from the top-right cell.
- Layout: subject on the left half, right-aligned text block on the right half, so reading begins where the eye lands.
- Never mirror a photo to fix a composition when it contains writing, numerals, clocks, flags, logos, wristwatches or a vehicle's steering side; flipped Arabic signage is instantly wrong.
- Titles over photos use `direction: rtl` and `unicode-bidi: isolate`; animate words or lines, never individual letters of a joined word (see `playbooks/arabic-typography.md`).
- Smallest text 36 px at 1080 width, contrast ≥ 4.5:1 against the scrim, captions below the subject's chin line and inside 5% side and 12% top/bottom margins for 9:16.
- Pick one numeral system per film; mixed Arabic-English captions usually read better with Western digits for years and prices.
- Lower-thirds and caption pills attached to a parallax layer inherit that layer's transform, so Arabic text drifts with the plane it labels rather than floating in screen space.

**بالعربية:** الاتجاه الافتراضي للكشف والتحريك من اليمين إلى اليسار، والأقنعة تبدأ من الحافة اليمنى، والشبكات تمتلئ من الخلية العليا اليمنى. الموضوع في النصف الأيسر والنص في النصف الأيمن بمحاذاة يمينية. لا تعكس صورة فيها كتابة أو أرقام أو ساعات أو أعلام أو شعارات. العناوين بـ `direction: rtl` و `unicode-bidi: isolate` وتُحرَّك كلماتٍ أو أسطرًا لا حروفًا. أصغر نص 36 بكسل عند عرض 1080، تباين ≥ 4.5:1، وهوامش 5٪ جانبيًا و12٪ أعلى وأسفل. نظام أرقام واحد في الفيلم. الترجمات المثبتة على طبقة ترث تحويلها.

## 7. Audio sync / المزامنة مع الصوت

- The supplied voice is master time and stays untouched. Cut to a new photo 2 frames (about 67 ms at 30 fps) before the start of the emphasis word that names it; the image must already be there when the word lands.
- Camera direction changes and mask reveals start on phrase boundaries from `words.json`, never mid-word.
- A sentence end gets a settle: the drift continues, the intentional move finishes within 300 ms after the last word, and the cut comes on the next phrase start.
- Music-driven montage: cut on the beat, keep the push-in velocity continuous across the cut, change pan direction every 2 or 4 bars.
- Never modulate scale or parallax amplitude with the audio envelope; "breathing" photos read as a glitch.
- Verification: list every `emphasis: true` word and the frame at which its photo or mask is ≥ 50% visible. Tolerance ≤ 100 ms, and aim for a consistent small lead of 40–70 ms rather than a mix of early and late.
- SFX for wipes (a soft whoosh at or below −18 dBFS) go on a separate stem; the voice stem is never re-encoded.

**بالعربية:** الصوت المقدَّم هو الساعة الرئيسية ولا يُمسّ. اقطع إلى الصورة الجديدة قبل بداية الكلمة المفتاحية بإطارين (نحو 67 مللي ثانية عند 30 إطارًا). تغييرات اتجاه الكاميرا والأقنعة على حدود العبارات من `words.json` لا في منتصف كلمة. نهاية الجملة استقرار: الحركة المقصودة تنتهي خلال 300 مللي ثانية بعد آخر كلمة. في المونتاج الإيقاعي اقطع على النبضة وأبقِ سرعة التكبير مستمرة عبر القطع. لا تربط التكبير أو سعة البارالاكس بغلاف الصوت. تحقق من كل كلمة `emphasis` بتسامح ≤ 100 مللي ثانية وتقدّم ثابت 40–70. المؤثرات على مسار منفصل.

## 8. Quality checklist / قائمة الفحص

1. Does every photo move for its whole hold, with no still frame longer than 8 frames?
2. Do all layers move in the same direction with ratios that match their depth factors?
3. At the extreme of every camera move (first and last frame of each hold), is every edge, stretched pixel and transparent corner hidden?
4. Is the maximum scale ≤ 1.12, and is the source long side ≥ 1.5× the displayed size at that scale?
5. Do cut-outs have clean edges (no halo wider than 1 px) and a contact shadow?
6. Is one shared grade plus grain applied to the whole stack so the layers read as a single photograph?
7. Do reveals and pans default right → left for Arabic, with no mirrored photo that contains writing?
8. Does each photo cut land within 100 ms of, and slightly before, its narration word?
9. Do no two consecutive photos use the identical camera move?
10. Is every image listed in `ASSETS.md` with source, license and attribution, and none taken from the reference video?

**بالعربية:** عشرة أسئلة بنعم أو لا: كل صورة تتحرك طوال مدتها؟ الطبقات في اتجاه واحد وبنسب العمق؟ لا حواف أو زوايا شفافة عند أقصى حركة؟ التكبير ≤ 1.12 والدقة كافية؟ المقصوصات نظيفة ولها ظل؟ تدرج وحبيبات موحّدة؟ الاتجاه من اليمين ولا صور معكوسة فيها كتابة؟ القطع خلال 100 مللي ثانية من الكلمة وقبلها قليلًا؟ لا حركتان متطابقتان متتاليتان؟ كل صورة مسجّلة في `ASSETS.md` بترخيصها ولا شيء من الفيديو المرجعي؟

## 9. Anti-patterns / أخطاء شائعة

The generic "AI look" in photo work comes from treating every image the same way and from parallax built without a camera model:

- The same slow push-in with an eased stop on every photo (screensaver cadence), or a one-second crossfade between everything.
- Parallax that reveals stretched edges or transparent corners, layers sliding in opposite directions, or five-plus layers like a pop-up book.
- Jagged, haloed cut-outs with no contact shadow, floating in front of an unrelated plate.
- The glossy "photo card in 3D space" with a reflective floor, a lens flare and a slow turntable.
- A warm, over-sharpened, HDR-style grade applied per layer so the stack never fuses.
- Random tilt, float and bob on every element, including the background.
- Pushing into a face until skin texture fills the frame, or cropping through foreheads.
- Text centred over the busiest region on a flat black box.
- Stock imagery that illustrates the word rather than the story (a handshake for "partnership").
- Mirrored photos with flipped Arabic text, numerals or logos.
- Undisclosed AI-generated images presented as documentary evidence.
- Audio-reactive scaling of photos, or an infinite parallax loop with no narrative reason to be there.

**بالعربية:** المظهر الآلي يأتي من معاملة كل صورة بالطريقة نفسها ومن بارالاكس بلا نموذج كاميرا: تكبير بطيء مُنعَّم النهاية على كل صورة، تلاشي متقاطع لثانية بين كل شيء، حواف مشدودة أو زوايا شفافة، طبقات في اتجاهين، خمس طبقات فأكثر، مقصوصات مسنّنة بلا ظل، بطاقة صور لامعة بأرضية عاكسة وتوهج عدسة، تدرج دافئ مبالغ لكل طبقة على حدة، اهتزاز وطفو عشوائي على كل عنصر، تكبير على الوجه حتى المسام، نص على مربع أسود فوق أزحم منطقة، ستوك يصوّر الكلمة لا القصة، صور معكوسة بنص عربي مقلوب، صور مولّدة غير مصرّح بها، تكبير متفاعل مع الصوت.

## 10. Related styles / استايلات ذات صلة

- parallax-2d — بارالاكس
- fake3d — عمق 2.5D
- documentary-map — خريطة وثائقية
- higgsfield-journey — جولة سينمائية
- editorial — مونتاج تحريري
- viral-mixed-media — مونتاج مختلط
- stop-motion — ستوب موشن
- pm-koldo2k-5cff87 — Infinite-zoom landscape loop
