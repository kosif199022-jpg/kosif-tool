/*
 * KOSIF photo_cover — keep a photo covering the whole frame through any camera move.
 *
 * One rule for every photo film: the frame never shows an edge of the photo,
 * whatever the photo's aspect ratio, zoom, pan, shake, rotation or blur.
 *
 *   1. Cover: the base scale is max(W / iw, H / ih), so the shorter side fills.
 *   2. Minimum scale: zoom is floored (default 1 = exact cover). Rotation and blur
 *      raise the floor: a rotated frame needs a bigger photo, and a blur pulls
 *      empty pixels in from outside the photo, so the photo must reach further.
 *   3. Clamp: the camera centre is clamped so the (rotated) frame stays inside
 *      the photo. mode 'zoom' instead zooms in just enough to reach the requested
 *      centre, so a long pan keeps moving instead of sticking at the edge.
 *
 * Usage in a page (classic script, no build step):
 *   <script src="photo_cover.js"></script>
 *   const cam = KosifCover.camera({ W: 1080, H: 1920, iw: img.width, ih: img.height,
 *                                   zoom: 1.1, fx: 0.5, fy: 0.35, ox: shakeX, oy: shakeY,
 *                                   rot: 1.5, blur: 6 });
 *   KosifCover.draw(ctx, img, cam);            // or KosifCover.drawPhoto(ctx, img, opts)
 *
 * Parameters (all optional except W, H, iw, ih):
 *   zoom     1 = cover. Values below minZoom are raised to minZoom.
 *   minZoom  floor for zoom (default 1).
 *   fx, fy   the photo point (0..1) placed at the frame centre (default 0.5, 0.5).
 *   ox, oy   extra offset in frame pixels (shake, whip, parallax drift).
 *   rot      rotation in degrees.
 *   blur     blur radius in frame pixels applied when drawing (ctx.filter).
 *   bleed    extra frame pixels kept covered on every side (default 2), so
 *            resampling at the border never mixes in transparent pixels.
 *   mode     'clamp' (default) or 'zoom'.
 *
 * camera() returns { s, cx, cy, rot, zoom, minZoom, clamped } where s is frame
 * pixels per photo pixel and (cx, cy) is the photo pixel drawn at the frame centre.
 *
 * License: MIT (part of KOSIF TOOL).
 */
(function (root) {
  'use strict';

  const DEG = Math.PI / 180;

  // Half extents (frame px) of the axis-aligned box around the rotated, bled, blurred frame.
  function frameExtents(W, H, rotDeg, pad) {
    const r = Math.abs((rotDeg || 0) * DEG), c = Math.abs(Math.cos(r)), s = Math.abs(Math.sin(r));
    const hw = W / 2 + pad, hh = H / 2 + pad;
    return [hw * c + hh * s, hw * s + hh * c];
  }

  // Smallest scale (frame px per photo px) at which the frame fits inside the photo.
  function minScale(o) {
    const pad = (o.bleed == null ? 2 : o.bleed) + 2 * Math.max(0, o.blur || 0);
    const [ex, ey] = frameExtents(o.W, o.H, o.rot, pad);
    return Math.max((2 * ex) / o.iw, (2 * ey) / o.ih);
  }

  function camera(o) {
    if (!(o && o.W > 0 && o.H > 0 && o.iw > 0 && o.ih > 0)) throw new Error('KosifCover.camera needs W, H, iw, ih > 0');
    const base = Math.max(o.W / o.iw, o.H / o.ih);
    const minZoom = Math.max(1, o.minZoom == null ? 1 : o.minZoom);
    const pad = (o.bleed == null ? 2 : o.bleed) + 2 * Math.max(0, o.blur || 0);
    const [ex, ey] = frameExtents(o.W, o.H, o.rot, pad);
    const sFit = Math.max((2 * ex) / o.iw, (2 * ey) / o.ih);
    let s = Math.max(base * Math.max(o.zoom == null ? 1 : o.zoom, minZoom), sFit);
    const fx = o.fx == null ? 0.5 : o.fx, fy = o.fy == null ? 0.5 : o.fy;
    const ox = o.ox || 0, oy = o.oy || 0;
    // requested centre in photo px (an offset moves the photo, so the centre moves the other way)
    const want = (sc) => [fx * o.iw - ox / sc, fy * o.ih - oy / sc];
    let [cx, cy] = want(s);
    if (o.mode === 'zoom') {
      // zoom in until the requested centre is reachable: need |c - i/2| <= i/2 - e/s on each axis
      const need = (c, i, e) => { const d = Math.abs(c - i / 2); return d >= i / 2 ? Infinity : e / (i / 2 - d); };
      for (let k = 0; k < 6; k++) {
        const sNeed = Math.max(need(cx, o.iw, ex), need(cy, o.ih, ey));
        if (!(sNeed > s) || !isFinite(sNeed)) break;
        s = sNeed * 1.0005;
        [cx, cy] = want(s);
      }
    }
    const hx = ex / s, hy = ey / s;
    const ccx = Math.min(Math.max(cx, hx), o.iw - hx), ccy = Math.min(Math.max(cy, hy), o.ih - hy);
    return {
      s, cx: ccx, cy: ccy, rot: o.rot || 0, zoom: s / base, minZoom: Math.max(minZoom, sFit / base),
      clamped: Math.abs(ccx - cx) > 1e-6 || Math.abs(ccy - cy) > 1e-6, W: o.W, H: o.H, iw: o.iw, ih: o.ih,
    };
  }

  // Draw the photo with a camera from camera(). blur is applied here so the margin matches.
  function draw(ctx, img, cam, opts) {
    const blur = opts && opts.blur;
    ctx.save();
    if (blur > 0.3) ctx.filter = `blur(${blur.toFixed(2)}px)`;
    ctx.translate(cam.W / 2, cam.H / 2);
    if (cam.rot) ctx.rotate(cam.rot * DEG);
    ctx.scale(cam.s, cam.s);
    ctx.translate(-cam.cx, -cam.cy);
    ctx.drawImage(img, 0, 0, cam.iw, cam.ih);
    ctx.restore();
    return cam;
  }

  function drawPhoto(ctx, img, o) {
    const iw = o.iw || img.naturalWidth || img.videoWidth || img.width;
    const ih = o.ih || img.naturalHeight || img.videoHeight || img.height;
    const cam = camera(Object.assign({}, o, { iw, ih }));
    return draw(ctx, img, cam, o);
  }

  // Where a frame point lands on the photo (photo px). Used by tests and the checker.
  function frameToPhoto(cam, x, y) {
    const r = -cam.rot * DEG, dx = x - cam.W / 2, dy = y - cam.H / 2;
    return [cam.cx + (dx * Math.cos(r) - dy * Math.sin(r)) / cam.s, cam.cy + (dx * Math.sin(r) + dy * Math.cos(r)) / cam.s];
  }

  // True when every frame pixel (plus margin) maps inside the photo.
  function covers(cam, margin) {
    const m = margin || 0;
    const pts = [[-m, -m], [cam.W + m, -m], [-m, cam.H + m], [cam.W + m, cam.H + m]];
    return pts.every(([x, y]) => {
      const [u, v] = frameToPhoto(cam, x, y);
      return u >= -1e-6 && v >= -1e-6 && u <= cam.iw + 1e-6 && v <= cam.ih + 1e-6;
    });
  }

  const api = { camera, draw, drawPhoto, minScale, frameToPhoto, covers, version: 1 };
  root.KosifCover = api;
  if (typeof module === 'object' && module && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
