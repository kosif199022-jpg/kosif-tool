/* KOSIF shape-kit — sculpted 3D shapes and characters from signed distance fields (window.K3S).

   Load after three-kit.bundle.js (it reads window.K3.THREE; a bare window.THREE works too). No npm, no bundling.
   Everything is deterministic and a function of its inputs, so frames render in any order.

   Sculpt:   const S = K3S.sculpt()
               .ellipsoid([0, .08, 0], [.07, .08, .065], { color: "#f6efe8" })
               .sphere([0, .06, -.07], .025, { k: .012 })                       // k = smooth-union radius (metres)
               .capsule([.05, .12, .03], [.035, .075, .06], .02, .017, { k: .012 })
               .ellipsoid([0, .07, .016], [.013, .05, .008], { op: "sub", k: .006, color: "#ffb3c6" })   // carve, tinted
               .paint([.045, .04, .05], .016, "#ffadc0", { soft: .012 });      // colour only, no geometry
           const geo = S.mesh({ cells: 120 });       // surface nets on a coarse-to-fine grid → BufferGeometry (normals, colours)
   Look:     K3S.plushMaterial(), K3S.glossMaterial(), K3S.eye(), K3S.tube(points, r, colour)
   Stage:    K3S.studioBackdrop(), K3S.stageDisc(), K3S.makeLitePost()  (bloom + grade only: the fast post stack)
   Twin:     K3S.trussOverlay(model, { nodeParts }) — 3D members + joints coloured by utilisation (structural_twin.py)
   Creature: K3S.bunny() — a cute plush rabbit with a rig (body, head, ears, tail) and named joints.

   Primitives (centre c, radii r, optional rot [rx, ry, rz] radians, options { op, k, color }):
     sphere(c, r) · ellipsoid(c, [rx, ry, rz]) · capsule(a, b, r1, r2) (a round cone; r2 defaults to r1)
     box(c, [hx, hy, hz], round) · torus(c, R, r) (ring in the local xz plane) · paint(c, r, colour, { soft, radii })
   Ops: "add" (smooth union, default) · "sub" (smooth subtraction) · "and" (smooth intersection)
*/
(function (root) {
  "use strict";
  const THREE = (root.K3 && root.K3.THREE) || root.THREE;
  if (!THREE) throw new Error("shape-kit.js needs three-kit.bundle.js (window.K3) or window.THREE loaded first");

  /* ───────── small vector helpers on plain arrays ───────── */
  const sub3 = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const dot3 = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const len3 = (a) => Math.hypot(a[0], a[1], a[2]);
  const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);
  const hex = (c) => { const col = new THREE.Color(c); return [col.r, col.g, col.b]; };   // linear-sRGB working colour

  /* rotation matrix (Euler XYZ) and its transpose for local-space evaluation */
  function rotM(r) {
    if (!r || (!r[0] && !r[1] && !r[2])) return null;
    const m = new THREE.Matrix4().makeRotationFromEuler(new THREE.Euler(r[0] || 0, r[1] || 0, r[2] || 0)).elements;
    // column-major 4x4 → row-major inverse (= transpose) 3x3: local = R^T (p - c)
    return [m[0], m[1], m[2], m[4], m[5], m[6], m[8], m[9], m[10]];
  }

  /* ───────── primitive distance functions (all return metres; < 0 inside) ───────── */
  function primitive(kind, a) {
    const c = a.c || [0, 0, 0], R = rotM(a.rot);
    const local = R ? (x, y, z) => { const px = x - c[0], py = y - c[1], pz = z - c[2];
      return [R[0] * px + R[1] * py + R[2] * pz, R[3] * px + R[4] * py + R[5] * pz, R[6] * px + R[7] * py + R[8] * pz]; }
      : (x, y, z) => [x - c[0], y - c[1], z - c[2]];
    let d, ext;
    if (kind === "sphere") {
      const r = a.r; d = (x, y, z) => Math.hypot(x - c[0], y - c[1], z - c[2]) - r; ext = r;
    } else if (kind === "ellipsoid") {                      // Inigo Quilez's bound: exact on the axes, close everywhere
      const [rx, ry, rz] = a.r;
      d = (x, y, z) => { const p = local(x, y, z); const k0 = Math.hypot(p[0] / rx, p[1] / ry, p[2] / rz);
        const k1 = Math.hypot(p[0] / (rx * rx), p[1] / (ry * ry), p[2] / (rz * rz)); return k1 > 1e-12 ? k0 * (k0 - 1) / k1 : -Math.min(rx, ry, rz); };
      ext = Math.max(rx, ry, rz);
    } else if (kind === "capsule") {                         // round cone between two points (IQ sdRoundCone)
      const A = a.a, B = a.b, r1 = a.r1, r2 = a.r2 == null ? a.r1 : a.r2;
      const ba = sub3(B, A), l2 = dot3(ba, ba), rr = r1 - r2, a2 = l2 - rr * rr, il2 = 1 / l2;
      d = (x, y, z) => {
        const pa = [x - A[0], y - A[1], z - A[2]], yy = dot3(pa, ba), zz = yy - l2;
        const xv = [pa[0] * l2 - ba[0] * yy, pa[1] * l2 - ba[1] * yy, pa[2] * l2 - ba[2] * yy];
        const x2 = dot3(xv, xv), y2 = yy * yy * l2, z2 = zz * zz * l2, k = Math.sign(rr) * rr * rr * x2;
        if (Math.sign(zz) * a2 * z2 > k) return Math.sqrt(x2 + z2) * il2 - r2;
        if (Math.sign(yy) * a2 * y2 < k) return Math.sqrt(x2 + y2) * il2 - r1;
        return (Math.sqrt(x2 * a2 * il2) + yy * rr) * il2 - r1;
      };
      const mid = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2, (A[2] + B[2]) / 2];
      return { d, box: boxAround(mid, len3(ba) / 2 + Math.max(r1, r2)) };
    } else if (kind === "box") {
      const h = a.h, rd = a.round || 0;
      d = (x, y, z) => { const p = local(x, y, z); const qx = Math.abs(p[0]) - h[0] + rd, qy = Math.abs(p[1]) - h[1] + rd, qz = Math.abs(p[2]) - h[2] + rd;
        return Math.hypot(Math.max(qx, 0), Math.max(qy, 0), Math.max(qz, 0)) + Math.min(Math.max(qx, qy, qz), 0) - rd; };
      ext = Math.hypot(h[0], h[1], h[2]);
    } else if (kind === "torus") {
      const Rr = a.R, r = a.r;
      d = (x, y, z) => { const p = local(x, y, z); return Math.hypot(Math.hypot(p[0], p[2]) - Rr, p[1]) - r; };
      ext = Rr + r;
    } else throw new Error("unknown primitive " + kind);
    return { d, box: boxAround(c, ext) };
  }
  const boxAround = (c, e) => [c[0] - e, c[1] - e, c[2] - e, c[0] + e, c[1] + e, c[2] + e];

  /* ───────── the sculpt: an ordered list of primitives combined with smooth CSG ───────── */
  class Sculpt {
    constructor() { this.items = []; this.base = hex("#ffffff"); }
    _push(kind, args, o = {}) {
      const p = primitive(kind, args);
      this.items.push({ op: o.op || "add", k: o.k == null ? 0.0 : o.k, color: o.color ? hex(o.color) : null, d: p.d, box: p.box, kind });
      return this;
    }
    color(c) { this.base = hex(c); return this; }
    sphere(c, r, o) { return this._push("sphere", { c, r }, o); }
    ellipsoid(c, r, o = {}) { return this._push("ellipsoid", { c, r, rot: o.rot }, o); }
    capsule(a, b, r1, r2, o) { return this._push("capsule", { a, b, r1, r2 }, o); }
    box(c, h, round, o = {}) { return this._push("box", { c, h, round, rot: o.rot }, o); }
    torus(c, R, r, o = {}) { return this._push("torus", { c, R, r, rot: o.rot }, o); }
    paint(c, r, color, o = {}) {                           // a colour stamp: soft sphere/ellipsoid of colour, no geometry
      const p = o.radii ? primitive("ellipsoid", { c, r: o.radii, rot: o.rot }) : primitive("sphere", { c, r });
      this.items.push({ op: "paint", soft: o.soft == null ? r * 0.5 : o.soft, amount: o.amount == null ? 1 : o.amount, color: hex(color), d: p.d, box: p.box });
      return this;
    }
    /* distance only (the hot path for meshing) */
    dist(x, y, z) {
      let D = 1e9;
      for (const it of this.items) {
        if (it.op === "paint") continue;
        const dn = it.d(x, y, z), k = it.k;
        if (it.op === "add") {
          if (k <= 0) D = Math.min(D, dn);
          else { const h = clamp(0.5 + 0.5 * (dn - D) / k, 0, 1); D = dn + (D - dn) * h - k * h * (1 - h); }
        } else if (it.op === "sub") {
          if (k <= 0) D = Math.max(D, -dn);
          else { const h = clamp(0.5 - 0.5 * (D + dn) / k, 0, 1); D = D + (-dn - D) * h + k * h * (1 - h); }
        } else if (it.op === "and") {
          if (k <= 0) D = Math.max(D, dn);
          else { const h = clamp(0.5 - 0.5 * (dn - D) / k, 0, 1); D = dn + (D - dn) * h + k * h * (1 - h); }
        }
      }
      return D;
    }
    /* colour at a surface point: blends follow the same smooth weights as the shape, paints stamp on top */
    colorAt(x, y, z) {
      let D = 1e9, c = this.base.slice();
      for (const it of this.items) {
        const dn = it.d(x, y, z);
        if (it.op === "paint") {
          const w = it.amount * (1 - smoothstep(-it.soft, it.soft, dn));
          if (w > 0) for (let j = 0; j < 3; j++) c[j] += (it.color[j] - c[j]) * w;
          continue;
        }
        const k = Math.max(it.k, 1e-5), col = it.color;
        if (it.op === "add") {
          const h = clamp(0.5 + 0.5 * (dn - D) / k, 0, 1);       // h = weight of what came before
          if (col) for (let j = 0; j < 3; j++) c[j] = col[j] + (c[j] - col[j]) * h;
          D = it.k <= 0 ? Math.min(D, dn) : dn + (D - dn) * h - it.k * h * (1 - h);
        } else if (it.op === "sub") {
          const h = clamp(0.5 - 0.5 * (D + dn) / k, 0, 1);
          if (col) for (let j = 0; j < 3; j++) c[j] += (col[j] - c[j]) * h;
          D = it.k <= 0 ? Math.max(D, -dn) : D + (-dn - D) * h + it.k * h * (1 - h);
        } else {
          const h = clamp(0.5 - 0.5 * (dn - D) / k, 0, 1);
          D = it.k <= 0 ? Math.max(D, dn) : dn + (D - dn) * h + it.k * h * (1 - h);
        }
      }
      return c;
    }
    grad(x, y, z, e) {
      const gx = this.dist(x + e, y, z) - this.dist(x - e, y, z), gy = this.dist(x, y + e, z) - this.dist(x, y - e, z),
        gz = this.dist(x, y, z + e) - this.dist(x, y, z - e);
      const l = Math.hypot(gx, gy, gz) || 1; return [gx / l, gy / l, gz / l];
    }
    bounds(pad = 0) {
      const b = [1e9, 1e9, 1e9, -1e9, -1e9, -1e9];
      for (const it of this.items) if (it.op === "add") for (let j = 0; j < 3; j++) { b[j] = Math.min(b[j], it.box[j] - it.k); b[j + 3] = Math.max(b[j + 3], it.box[j + 3] + it.k); }
      for (let j = 0; j < 3; j++) { b[j] -= pad; b[j + 3] += pad; }
      return b;
    }
    /* the closest surface point to p (Newton steps along the gradient) and its outward normal */
    project(p, steps = 8) {
      let q = p.slice(); const e = 1e-4;
      for (let i = 0; i < steps; i++) { const d = this.dist(q[0], q[1], q[2]); const g = this.grad(q[0], q[1], q[2], e); q = [q[0] - g[0] * d, q[1] - g[1] * d, q[2] - g[2] * d]; }
      return { point: q, normal: this.grad(q[0], q[1], q[2], e) };
    }
    /* a ray from `from` toward `dir` marched to the surface: where an eye or a button sits, seen from the front */
    hit(from, dir, maxDist = 2) {
      const l = len3(dir), u = [dir[0] / l, dir[1] / l, dir[2] / l]; let t = 0;
      for (let i = 0; i < 256 && t < maxDist; i++) {
        const p = [from[0] + u[0] * t, from[1] + u[1] * t, from[2] + u[2] * t], d = this.dist(p[0], p[1], p[2]);
        if (d < 1e-5) return this.project(p, 3);
        t += Math.max(d * 0.8, 1e-5);
      }
      return null;
    }
    mesh(o = {}) { return meshSculpt(this, o); }
  }
  const smoothstep = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };

  /* ───────── surface nets mesher, coarse-to-fine ─────────
     cells: grid resolution along the longest side (the cost is ~cells² near the surface, not cells³: only blocks the
     surface passes through are evaluated at full resolution). Vertices are projected onto the true surface and their
     normals come from the field's gradient, so even a moderate grid gives clean, smooth silhouettes. */
  function meshSculpt(S, o = {}) {
    const t0 = performance.now();
    const cells = o.cells || 96, B = 4;                      // B = coarse block size in cells
    const b0 = S.bounds(0), span = Math.max(b0[3] - b0[0], b0[4] - b0[1], b0[5] - b0[2]);
    const h = span / cells, b = S.bounds(h * 2.5);
    const nx = Math.ceil((b[3] - b[0]) / h) + 1, ny = Math.ceil((b[4] - b[1]) / h) + 1, nz = Math.ceil((b[5] - b[2]) / h) + 1;
    const N = nx * ny * nz, F = new Float32Array(N), done = new Uint8Array(N);
    const id = (i, j, k) => i + nx * (j + ny * k);
    const X = (i) => b[0] + i * h, Y = (j) => b[1] + j * h, Z = (k) => b[2] + k * h;
    let evals = 0;
    const ev = (i, j, k) => { const q = id(i, j, k); if (!done[q]) { F[q] = S.dist(X(i), Y(j), Z(k)); done[q] = 1; evals++; } return F[q]; };
    // coarse pass: block corners; a block is refined when the surface can pass through it
    const bx = Math.ceil((nx - 1) / B), by = Math.ceil((ny - 1) / B), bz = Math.ceil((nz - 1) / B);
    const thr = B * h * 1.75 + (o.slack || 0);
    for (let K = 0; K < bz; K++) for (let J = 0; J < by; J++) for (let I = 0; I < bx; I++) {
      const i0 = I * B, j0 = J * B, k0 = K * B, i1 = Math.min(i0 + B, nx - 1), j1 = Math.min(j0 + B, ny - 1), k1 = Math.min(k0 + B, nz - 1);
      let near = false; const ci = (i0 + i1) >> 1, cj = (j0 + j1) >> 1, ck = (k0 + k1) >> 1;
      if (Math.abs(ev(ci, cj, ck)) < thr) near = true;
      if (near) for (let k = k0; k <= k1; k++) for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) ev(i, j, k);
    }
    // points never evaluated are far from the surface: give them the sign of their block centre
    for (let K = 0; K < bz; K++) for (let J = 0; J < by; J++) for (let I = 0; I < bx; I++) {
      const i0 = I * B, j0 = J * B, k0 = K * B, i1 = Math.min(i0 + B, nx - 1), j1 = Math.min(j0 + B, ny - 1), k1 = Math.min(k0 + B, nz - 1);
      const c = F[id((i0 + i1) >> 1, (j0 + j1) >> 1, (k0 + k1) >> 1)];
      for (let k = k0; k <= k1; k++) for (let j = j0; j <= j1; j++) for (let i = i0; i <= i1; i++) { const q = id(i, j, k); if (!done[q]) F[q] = c; }
    }
    // one vertex per cell that the surface crosses
    const vIndex = new Int32Array(N).fill(-1), P = [];
    const corners = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1]];
    const edges = [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]];
    const v = new Float32Array(8);
    for (let k = 0; k < nz - 1; k++) for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
      let mask = 0;
      for (let c = 0; c < 8; c++) { v[c] = F[id(i + corners[c][0], j + corners[c][1], k + corners[c][2])]; if (v[c] < 0) mask |= 1 << c; }
      if (mask === 0 || mask === 255) continue;
      let sx = 0, sy = 0, sz = 0, n = 0;
      for (const [a, e] of edges) {
        if ((v[a] < 0) === (v[e] < 0)) continue;
        const t = v[a] / (v[a] - v[e]);
        sx += corners[a][0] + (corners[e][0] - corners[a][0]) * t; sy += corners[a][1] + (corners[e][1] - corners[a][1]) * t;
        sz += corners[a][2] + (corners[e][2] - corners[a][2]) * t; n++;
      }
      vIndex[id(i, j, k)] = P.length / 3;
      P.push(X(i) + (sx / n) * h, Y(j) + (sy / n) * h, Z(k) + (sz / n) * h);
    }
    // project onto the true surface (2 Newton steps), normals and colours from the field
    const nv = P.length / 3, pos = new Float32Array(nv * 3), nor = new Float32Array(nv * 3), col = new Float32Array(nv * 3);
    const eps = h * 0.35, proj = o.project == null ? 2 : o.project;
    for (let q = 0; q < nv; q++) {
      let x = P[q * 3], y = P[q * 3 + 1], z = P[q * 3 + 2];
      for (let s = 0; s < proj; s++) { const d = S.dist(x, y, z); if (Math.abs(d) > h * 1.5) break; const g = S.grad(x, y, z, eps); x -= g[0] * d; y -= g[1] * d; z -= g[2] * d; }
      const g = S.grad(x, y, z, eps), c = S.colorAt(x, y, z);
      pos[q * 3] = x; pos[q * 3 + 1] = y; pos[q * 3 + 2] = z; nor.set(g, q * 3); col.set(c, q * 3);
    }
    // quads around every grid edge with a sign change, split along the shorter diagonal, wound outward
    const idx = [];
    const quad = (a, b2, c, d, flip) => {
      if (a < 0 || b2 < 0 || c < 0 || d < 0) return;
      const dAC = (pos[a * 3] - pos[c * 3]) ** 2 + (pos[a * 3 + 1] - pos[c * 3 + 1]) ** 2 + (pos[a * 3 + 2] - pos[c * 3 + 2]) ** 2;
      const dBD = (pos[b2 * 3] - pos[d * 3]) ** 2 + (pos[b2 * 3 + 1] - pos[d * 3 + 1]) ** 2 + (pos[b2 * 3 + 2] - pos[d * 3 + 2]) ** 2;
      const tris = dAC < dBD ? [[a, b2, c], [a, c, d]] : [[a, b2, d], [b2, c, d]];
      for (let [p0, p1, p2] of tris) { if (flip) [p1, p2] = [p2, p1]; idx.push(p0, p1, p2); }
    };
    for (let k = 1; k < nz - 1; k++) for (let j = 1; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {      // x edges
      const a = F[id(i, j, k)] < 0, e = F[id(i + 1, j, k)] < 0; if (a === e) continue;
      quad(vIndex[id(i, j - 1, k - 1)], vIndex[id(i, j, k - 1)], vIndex[id(i, j, k)], vIndex[id(i, j - 1, k)], !a);
    }
    for (let k = 1; k < nz - 1; k++) for (let j = 0; j < ny - 1; j++) for (let i = 1; i < nx - 1; i++) {      // y edges
      const a = F[id(i, j, k)] < 0, e = F[id(i, j + 1, k)] < 0; if (a === e) continue;
      quad(vIndex[id(i - 1, j, k - 1)], vIndex[id(i - 1, j, k)], vIndex[id(i, j, k)], vIndex[id(i, j, k - 1)], !a);
    }
    for (let k = 0; k < nz - 1; k++) for (let j = 1; j < ny - 1; j++) for (let i = 1; i < nx - 1; i++) {      // z edges
      const a = F[id(i, j, k)] < 0, e = F[id(i, j, k + 1)] < 0; if (a === e) continue;
      quad(vIndex[id(i - 1, j - 1, k)], vIndex[id(i, j - 1, k)], vIndex[id(i, j, k)], vIndex[id(i - 1, j, k)], !a);
    }
    // safety: wind every triangle to agree with the field normal (robust whatever the edge orientation convention)
    for (let t = 0; t < idx.length; t += 3) {
      const a = idx[t], b2 = idx[t + 1], c = idx[t + 2];
      const ux = pos[b2 * 3] - pos[a * 3], uy = pos[b2 * 3 + 1] - pos[a * 3 + 1], uz = pos[b2 * 3 + 2] - pos[a * 3 + 2];
      const wx = pos[c * 3] - pos[a * 3], wy = pos[c * 3 + 1] - pos[a * 3 + 1], wz = pos[c * 3 + 2] - pos[a * 3 + 2];
      const fx = uy * wz - uz * wy, fy = uz * wx - ux * wz, fz = ux * wy - uy * wx;
      const s = fx * (nor[a * 3] + nor[b2 * 3] + nor[c * 3]) + fy * (nor[a * 3 + 1] + nor[b2 * 3 + 1] + nor[c * 3 + 1]) + fz * (nor[a * 3 + 2] + nor[b2 * 3 + 2] + nor[c * 3 + 2]);
      if (s < 0) { idx[t + 1] = c; idx[t + 2] = b2; }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    geo.setAttribute("normal", new THREE.BufferAttribute(nor, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(col, 3));
    geo.setIndex(nv > 65535 ? new THREE.Uint32BufferAttribute(idx, 1) : new THREE.Uint16BufferAttribute(idx, 1));
    geo.computeBoundingSphere();
    geo.userData.stats = { grid: [nx, ny, nz], cell_m: +h.toFixed(5), evals, full: N, vertices: nv, triangles: idx.length / 3,
      ms: Math.round(performance.now() - t0) };
    return geo;
  }

  /* ───────── materials ───────── */
  const NOISE3 = `
    float ks_h(vec3 p){ p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
    float ks_n(vec3 x){ vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);
      return mix(mix(mix(ks_h(i), ks_h(i + vec3(1,0,0)), f.x), mix(ks_h(i + vec3(0,1,0)), ks_h(i + vec3(1,1,0)), f.x), f.y),
                 mix(mix(ks_h(i + vec3(0,0,1)), ks_h(i + vec3(1,0,1)), f.x), mix(ks_h(i + vec3(0,1,1)), ks_h(i + vec3(1,1,1)), f.x), f.y), f.z); }`;
  /* plush / felt: vertex colours, velvet sheen, a fuzz rim that takes the fabric's own colour, and micro fibre noise
     in object space (no UVs needed). o.fibre = normal jitter, o.fibreScale = fibres per metre, o.fuzz = rim glow. */
  function plushMaterial(o = {}) {
    const m = new THREE.MeshPhysicalMaterial({ vertexColors: true, color: o.color || 0xffffff, roughness: o.roughness == null ? 0.82 : o.roughness,
      metalness: 0, sheen: o.sheen == null ? 1.0 : o.sheen, sheenRoughness: o.sheenRoughness == null ? 0.42 : o.sheenRoughness,
      sheenColor: new THREE.Color(o.sheenColor || 0xfff4f6), transparent: !!o.transparent });
    const U = { uFuzz: { value: o.fuzz == null ? 0.38 : o.fuzz }, uFibre: { value: o.fibre == null ? 0.22 : o.fibre },
      uFibreScale: { value: o.fibreScale == null ? 520 : o.fibreScale }, uFuzzTint: { value: new THREE.Color(o.fuzzTint || 0xffffff) } };
    m.userData.uniforms = U;
    m.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, U);
      sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vKsObj;")
        .replace("#include <begin_vertex>", "#include <begin_vertex>\nvKsObj = position;");
      sh.fragmentShader = sh.fragmentShader.replace("#include <common>", `#include <common>
        uniform float uFuzz, uFibre, uFibreScale; uniform vec3 uFuzzTint; varying vec3 vKsObj; ${NOISE3}`)
        .replace("#include <normal_fragment_maps>", `#include <normal_fragment_maps>
        { vec3 q = vKsObj * uFibreScale; float n0 = ks_n(q), e = 0.35;
          vec3 g = vec3(ks_n(q + vec3(e,0,0)) - n0, ks_n(q + vec3(0,e,0)) - n0, ks_n(q + vec3(0,0,e)) - n0);
          vec3 gv = (viewMatrix * vec4(g, 0.0)).xyz; normal = normalize(normal + uFibre * (gv - dot(gv, normal) * normal) * 2.5); }`)
        .replace("#include <emissivemap_fragment>", `#include <emissivemap_fragment>
        { float fr = pow(1.0 - clamp(dot(normal, normalize(vViewPosition)), 0.0, 1.0), 2.2);
          float fib = 0.75 + 0.5 * ks_n(vKsObj * uFibreScale * 2.0);
          totalEmissiveRadiance += diffuseColor.rgb * uFuzzTint * fr * uFuzz * fib; }`);
    };
    m.customProgramCacheKey = () => "kosif-plush";
    return m;
  }
  function glossMaterial(color = 0x15100f, o = {}) {
    return new THREE.MeshPhysicalMaterial({ color, roughness: o.roughness == null ? 0.08 : o.roughness, metalness: 0, clearcoat: 1,
      clearcoatRoughness: 0.04, ior: 1.5, envMapIntensity: o.env == null ? 1.6 : o.env });
  }
  /* a cute eye: glossy dark sphere, a warm iris ring and two catch-lights that face +z (toward the camera) */
  function eye(o = {}) {
    const r = o.r || 0.012, g = new THREE.Group();
    const ball = new THREE.Mesh(new THREE.SphereGeometry(r, 40, 28), glossMaterial(o.color || 0x1a1113));
    ball.scale.set(1, o.tall || 1.12, 0.78); g.add(ball);
    const iris = new THREE.Mesh(new THREE.TorusGeometry(r * 0.55, r * 0.09, 10, 40),
      new THREE.MeshBasicMaterial({ color: o.iris || 0x5a3a2c, transparent: true, opacity: 0.55 }));
    iris.position.set(0, -r * 0.18, r * 0.72); iris.scale.set(1, 1.1, 1); g.add(iris);
    const spark = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
    const s1 = new THREE.Mesh(new THREE.SphereGeometry(r * 0.3, 16, 12), spark); s1.position.set(r * 0.32, r * 0.42, r * 0.66); s1.scale.set(1, 1, 0.35); g.add(s1);
    const s2 = new THREE.Mesh(new THREE.SphereGeometry(r * 0.14, 12, 8), spark); s2.position.set(-r * 0.3, -r * 0.3, r * 0.72); s2.scale.set(1, 1, 0.35); g.add(s2);
    g.userData.ball = ball;
    return g;
  }
  function tube(points, r, color, o = {}) {
    const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(...p)));
    return new THREE.Mesh(new THREE.TubeGeometry(curve, o.segments || 32, r, 8, false),
      new THREE.MeshStandardMaterial({ color, roughness: 0.6 }));
  }

  /* ───────── stage: a studio backdrop, a measuring disc, and the fast post stack ───────── */
  function studioBackdrop(o = {}) {
    const W = 512, cv = document.createElement("canvas"); cv.width = cv.height = W; const x = cv.getContext("2d");
    const g = x.createRadialGradient(W * 0.5, W * (o.cy || 0.42), 0, W * 0.5, W * 0.5, W * 0.75);
    g.addColorStop(0, o.inner || "#1e4a44"); g.addColorStop(0.55, o.mid || "#0c2224"); g.addColorStop(1, o.outer || "#050c0d");
    x.fillStyle = g; x.fillRect(0, 0, W, W);
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; return tex;
  }
  function stageDisc(o = {}) {
    const R = o.radius || 0.32, g = new THREE.Group();
    const mat = new THREE.ShaderMaterial({ transparent: true, depthWrite: false,
      uniforms: { uColor: { value: new THREE.Color(o.color || 0x9dffb4) }, uScan: { value: 0 }, uAlpha: { value: 1 } },
      vertexShader: `varying vec2 vP; void main(){ vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
      fragmentShader: `uniform vec3 uColor; uniform float uScan, uAlpha; varying vec2 vP;
        void main(){ float r = length(vP) / ${R.toFixed(4)}; if (r > 1.0) discard;
          vec2 gp = vP / ${(R / 8).toFixed(5)}; vec2 gr = abs(fract(gp - 0.5) - 0.5) / fwidth(gp);
          float grid = 1.0 - min(min(gr.x, gr.y), 1.0);
          float ring = smoothstep(0.012, 0.0, abs(r - 0.985)) + 0.6 * smoothstep(0.008, 0.0, abs(r - 0.62));
          float ang = atan(vP.y, vP.x); float ticks = step(0.94, r) * step(0.5, fract(ang * 36.0 / 6.2831853)) * 0.5;
          float a = (grid * 0.16 * (1.0 - r * 0.6) + ring * 0.85 + ticks) * uAlpha;
          float sweep = smoothstep(0.08, 0.0, abs(r - uScan)) * 0.9 * uAlpha;
          gl_FragColor = vec4(uColor * (1.0 + sweep * 2.0), clamp(a + sweep, 0.0, 1.0)); }` });
    const disc = new THREE.Mesh(new THREE.CircleGeometry(R, 96), mat); disc.rotation.x = -Math.PI / 2; disc.position.y = 0.0006; g.add(disc);
    const shadow = new THREE.Mesh(new THREE.CircleGeometry(R * 1.6, 64), new THREE.ShadowMaterial({ opacity: o.shadow == null ? 0.42 : o.shadow }));
    shadow.rotation.x = -Math.PI / 2; shadow.receiveShadow = true; g.add(shadow);
    g.userData.mat = mat;
    return g;
  }
  /* RenderPass → bloom → grade/vignette → output. A fraction of makePost's cost (no 64-tap rays, no DOF, no grain pass);
     returns the same shape ({ composer, bloom, grade, film }) so K3.makeFrameLoop can drive it. */
  function makeLitePost(renderer, scene, camera, W, H, o = {}) {
    const ex = root.K3 || {};
    const { EffectComposer, RenderPass, UnrealBloomPass, ShaderPass, OutputPass } = ex.POST || {};
    if (!EffectComposer) {                                   // no post classes exported: plain render, same interface
      const film = { uniforms: { time: { value: 0 } } };
      const composer = { renderToScreen: true, readBuffer: null, render: () => renderer.render(scene, camera) };
      return { composer, film, bloom: null, grade: null, plain: true };
    }
    const composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    const bloom = new UnrealBloomPass(new THREE.Vector2(W, H), o.bloom == null ? 0.55 : o.bloom, o.radius == null ? 0.5 : o.radius, o.threshold == null ? 0.82 : o.threshold);
    composer.addPass(bloom);
    const grade = new ShaderPass({ uniforms: { tDiffuse: { value: null }, uVig: { value: o.vignette == null ? 0.38 : o.vignette }, uSeed: { value: 0 }, uGrain: { value: o.grain == null ? 0.025 : o.grain } },
      vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
      fragmentShader: `uniform sampler2D tDiffuse; uniform float uVig, uSeed, uGrain; varying vec2 vUv;
        float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233)) + uSeed) * 43758.5453); }
        void main(){ vec3 c = texture2D(tDiffuse, vUv).rgb; vec2 d = vUv - 0.5;
          c *= 1.0 - uVig * smoothstep(0.3, 0.95, length(d) * 1.35); c += (h(gl_FragCoord.xy) - 0.5) * uGrain;
          gl_FragColor = vec4(c, 1.0); }` });
    composer.addPass(grade);
    composer.addPass(new OutputPass());
    const film = { uniforms: { time: { value: 0 } } };       // makeFrameLoop writes the time here; the grain seeds from it
    Object.defineProperty(film.uniforms.time, "value", { get: () => grade.uniforms.uSeed.value, set: (v) => { grade.uniforms.uSeed.value = (v * 37.0) % 101; } });
    return { composer, bloom, grade, film };
  }

  /* ───────── structural twin overlay: the truss model drawn in 3D ─────────
     model: the `model` of a structural_twin.py report (nodes [x, y, z] in metres, elements). Each node may be bound to
     a rig part (o.nodeParts[id] = Object3D) so joints ride along when an ear bends. update(utilOf(id) → 0..∞) colours
     members green → yellow → red; hide/break/swap per member id. */
  function utilColor(u, out) {
    const stops = [[0, [0.35, 1.0, 0.72]], [0.5, [0.75, 1.0, 0.45]], [0.8, [1.0, 0.86, 0.35]], [1.0, [1.0, 0.36, 0.28]]];
    let i = 0; while (i < stops.length - 2 && u > stops[i + 1][0]) i++;
    const a = stops[i], b = stops[i + 1], t = clamp((u - a[0]) / (b[0] - a[0]), 0, 1);
    return out.setRGB(a[1][0] + (b[1][0] - a[1][0]) * t, a[1][1] + (b[1][1] - a[1][1]) * t, a[1][2] + (b[1][2] - a[1][2]) * t);
  }
  function trussOverlay(model, o = {}) {
    const g = new THREE.Group(), parts = o.nodeParts || {}, rest = {};
    for (const [id, p] of Object.entries(model.nodes)) rest[id] = new THREE.Vector3(p[0], p[1], p[2] || 0);
    const R = o.radius || 0.0022, jointR = o.jointRadius || 0.0042;
    const memberGeo = new THREE.CylinderGeometry(1, 1, 1, 10, 1, false); memberGeo.translate(0, 0.5, 0);
    const members = {}, joints = {};
    for (const e of model.elements) {
      const mat = new THREE.MeshBasicMaterial({ color: 0x9dffb4, transparent: true, opacity: 0, toneMapped: false, depthWrite: false });
      const m = new THREE.Mesh(memberGeo, mat); m.userData = { id: e.id, a: e.a, b: e.b, thick: 1, grow: 1, gap: 0 }; m.renderOrder = 5;
      g.add(m); members[e.id] = m;
    }
    const jGeo = new THREE.SphereGeometry(1, 16, 12), ringGeo = new THREE.TorusGeometry(1, 0.16, 8, 32);
    for (const id of Object.keys(model.nodes)) {
      const j = new THREE.Group();
      const core = new THREE.Mesh(jGeo, new THREE.MeshBasicMaterial({ color: 0xeaffd0, transparent: true, opacity: 0, toneMapped: false, depthWrite: false }));
      const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ color: 0xd0ff6a, transparent: true, opacity: 0, toneMapped: false, depthWrite: false }));
      core.scale.setScalar(jointR); ring.scale.setScalar(jointR * 2.0); j.add(core, ring); j.renderOrder = 6;
      j.userData = { core, ring, pop: 1 }; g.add(j); joints[id] = j;
    }
    const tmpA = new THREE.Vector3(), tmpB = new THREE.Vector3(), dir = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0), col = new THREE.Color();
    const world = (id, out) => { out.copy(rest[id]); const p = parts[id]; if (p) { p.updateWorldMatrix(true, false); out.applyMatrix4(p.matrixWorld); }
      if (g.parent) { g.parent.updateWorldMatrix(true, false); out.applyMatrix4(tmpInv.copy(g.parent.matrixWorld).invert()); } return out; };
    const tmpInv = new THREE.Matrix4();
    /* state: { alpha, jointAlpha, utilOf(id), camera (rings face it), flash(id) → 0..1 } */
    function update(s = {}) {
      const alpha = s.alpha == null ? 1 : s.alpha, ja = s.jointAlpha == null ? alpha : s.jointAlpha;
      for (const [id, j] of Object.entries(joints)) {
        world(id, j.position);
        const pop = j.userData.pop; j.scale.setScalar(Math.max(1e-4, pop));
        j.userData.core.material.opacity = ja; j.userData.ring.material.opacity = ja * 0.85;
        if (s.camera) j.userData.ring.quaternion.copy(s.camera.quaternion);
      }
      for (const m of Object.values(members)) {
        const u = m.userData; world(u.a, tmpA); world(u.b, tmpB);
        dir.subVectors(tmpB, tmpA); const L = dir.length(); dir.normalize();
        const grow = clamp(u.grow, 0, 1), gap = u.gap || 0;
        m.position.copy(tmpA).addScaledVector(dir, L * gap * 0.5);
        m.quaternion.setFromUnitVectors(up, dir);
        const r = R * u.thick; m.scale.set(r, Math.max(1e-5, L * grow * (1 - gap)), r);
        const util = s.utilOf ? s.utilOf(u.id) : 0; utilColor(util, col);
        const fl = s.flash ? s.flash(u.id) : 0; if (fl > 0) col.lerp(new THREE.Color(1, 1, 1), fl * 0.6);
        m.material.color.copy(col).multiplyScalar(1.05 + 0.9 * clamp(util - 0.7, 0, 1));
        m.material.opacity = alpha * (u.hidden ? 0 : 1) * (grow > 0 ? 1 : 0);
        m.visible = m.material.opacity > 0.002;
      }
    }
    return { group: g, members, joints, update, worldOf: (id, out = new THREE.Vector3()) => world(id, out), rest };
  }

  /* ───────── a cute plush bunny, rigged: body · head (on the neck) · ears (on their bases) · tail ─────────
     Metres, standing on y = 0 and facing +z, ~0.33 m to the ear tips. Returns { group, parts, joints (world-rest
     positions of the anatomy, for a structural twin), stats }. o.cells sets mesh density (default 132). */
  function bunny(o = {}) {
    const fur = o.fur || "#f2e4d8", belly = o.belly || "#fbf3ea", pink = o.pink || "#ff9fb8", nose = o.nose || "#ff7c9c", cells = o.cells || 132;
    const scarf = o.scarf || "#7fe7b4";
    const mat = o.material || plushMaterial({ fuzz: 0.16, fibre: 0.22, fibreScale: 560, sheen: 0.7, sheenColor: 0xfff0f2 });
    const group = new THREE.Group(), parts = {}, stats = {};
    const NECK = [0, 0.152, 0.004], EAR_L = [-0.03, 0.123, -0.014], EAR_R = [0.03, 0.123, -0.014];   // pivots (EAR in head space)

    // body: pear torso, thighs, feet, arms, belly patch
    const body = new Sculpt().color(fur)
      .ellipsoid([0, 0.088, 0], [0.071, 0.082, 0.064])
      .ellipsoid([0, 0.138, 0.004], [0.05, 0.035, 0.046], { k: 0.03 })
      .ellipsoid([-0.044, 0.046, 0.012], [0.04, 0.042, 0.048], { k: 0.022 })
      .ellipsoid([0.044, 0.046, 0.012], [0.04, 0.042, 0.048], { k: 0.022 })
      .ellipsoid([-0.04, 0.017, 0.05], [0.027, 0.018, 0.04], { k: 0.014 })
      .ellipsoid([0.04, 0.017, 0.05], [0.027, 0.018, 0.04], { k: 0.014 })
      .capsule([-0.052, 0.128, 0.022], [-0.03, 0.082, 0.062], 0.02, 0.017, { k: 0.014 })
      .capsule([0.052, 0.128, 0.022], [0.03, 0.082, 0.062], 0.02, 0.017, { k: 0.014 })
      .box([0, -0.05, 0], [0.2, 0.05, 0.2], 0, { op: "sub", k: 0.004 })                    // flat underside: it sits
      .paint([0, 0.075, 0.062], 0.034, belly, { radii: [0.042, 0.05, 0.03], soft: 0.012 })
      .paint([-0.04, 0.006, 0.084], 0.012, pink, { radii: [0.014, 0.01, 0.01], soft: 0.004, amount: 0.85 })
      .paint([0.04, 0.006, 0.084], 0.012, pink, { radii: [0.014, 0.01, 0.01], soft: 0.004, amount: 0.85 });
    const bodyGeo = body.mesh({ cells }); stats.body = bodyGeo.userData.stats;
    parts.body = new THREE.Mesh(bodyGeo, mat); parts.body.castShadow = true; group.add(parts.body);

    // scarf: a soft torus around the neck (the one splash of the HUD's mint)
    const sc = new Sculpt().color(scarf).torus([0, 0.152, 0.004], 0.047, 0.0125, { rot: [0.12, 0, 0] })
      .ellipsoid([0.026, 0.13, 0.052], [0.012, 0.022, 0.007], { k: 0.008, rot: [0.3, 0, -0.35] });
    const scGeo = sc.mesh({ cells: 90 }); stats.scarf = scGeo.userData.stats;
    parts.scarf = new THREE.Mesh(scGeo, plushMaterial({ fuzz: 0.14, fibre: 0.28, fibreScale: 700, sheenColor: 0xd8fff0, sheen: 0.6 })); parts.scarf.castShadow = true; group.add(parts.scarf);

    // tail
    const tl = new Sculpt().color(belly).sphere([0, 0, 0], 0.024).sphere([0.008, 0.008, -0.006], 0.016, { k: 0.01 }).sphere([-0.008, 0.004, -0.008], 0.015, { k: 0.01 });
    parts.tail = new THREE.Group(); parts.tail.position.set(0, 0.052, -0.066);
    const tailMesh = new THREE.Mesh(tl.mesh({ cells: 60 }), plushMaterial({ fuzz: 0.3, fibre: 0.35, fibreScale: 800 }));
    tailMesh.castShadow = true; parts.tail.add(tailMesh); group.add(parts.tail);

    // head on a neck pivot: round skull, chubby cheeks, muzzle, nose, blush
    parts.head = new THREE.Group(); parts.head.position.set(...NECK); group.add(parts.head);
    const hs = new Sculpt().color(fur)
      .ellipsoid([0, 0.072, 0.004], [0.08, 0.07, 0.07])
      .ellipsoid([-0.036, 0.046, 0.034], [0.04, 0.034, 0.036], { k: 0.022 })
      .ellipsoid([0.036, 0.046, 0.034], [0.04, 0.034, 0.036], { k: 0.022 })
      .ellipsoid([0, 0.042, 0.058], [0.027, 0.02, 0.019], { k: 0.014, color: belly })
      .ellipsoid([0, 0.0545, 0.0755], [0.0095, 0.0065, 0.0055], { k: 0.0035, color: nose })
      .paint([-0.047, 0.041, 0.053], 0.015, "#ff8fab", { radii: [0.017, 0.011, 0.012], soft: 0.009, amount: 0.8 })
      .paint([0.047, 0.041, 0.053], 0.015, "#ff8fab", { radii: [0.017, 0.011, 0.012], soft: 0.009, amount: 0.8 });
    const headGeo = hs.mesh({ cells }); stats.head = headGeo.userData.stats;
    const headMesh = new THREE.Mesh(headGeo, mat); headMesh.castShadow = true; parts.head.add(headMesh);
    // eyes sit where rays from the front meet the face
    for (const sx of [-1, 1]) {
      const hit = hs.hit([sx * 0.031, 0.07, 0.2], [0, -0.06, -1]);
      if (!hit) continue;
      const e = eye({ r: 0.0128 }); const p = hit.point, n = hit.normal;
      e.position.set(p[0] - n[0] * 0.0046, p[1] - n[1] * 0.0046, p[2] - n[2] * 0.0046);
      e.lookAt(e.position.x + n[0] * 0.6 + sx * -0.02, e.position.y + n[1] * 0.6, e.position.z + n[2] * 0.6 + 0.35); parts.head.add(e);
      parts[sx < 0 ? "eyeL" : "eyeR"] = e;
    }
    // a small "w" mouth laid onto the muzzle
    const mouthPts = [[-0.011, 0.043], [-0.0055, 0.0385], [0, 0.0425], [0.0055, 0.0385], [0.011, 0.043]].map(([x, y]) => {
      const h = hs.hit([x, y, 0.2], [0, 0, -1]); return h ? [h.point[0] + h.normal[0] * 0.0006, h.point[1] + h.normal[1] * 0.0006, h.point[2] + h.normal[2] * 0.0006] : [x, y, 0.07]; });
    parts.mouth = tube(mouthPts, 0.0011, 0x6b3540); parts.head.add(parts.mouth);
    const noseTop = hs.hit([0, 0.05, 0.2], [0, 0, -1]);
    if (noseTop) { const nl = tube([[0, 0.049, noseTop.point[2] - 0.001], [0, 0.0435, noseTop.point[2] - 0.004]], 0.0009, 0x6b3540); parts.head.add(nl); }

    // ears on their own pivots (in head space): long, soft, a pink carved inner, a gentle outward tilt
    for (const side of [-1, 1]) {
      const es = new Sculpt().color(fur)
        .capsule([0, -0.004, 0], [0, 0.03, 0], 0.0145, 0.017)
        .ellipsoid([0, 0.07, 0], [0.023, 0.066, 0.0125], { k: 0.016 })
        .ellipsoid([0, 0.07, 0.0135], [0.0125, 0.05, 0.0085], { op: "sub", k: 0.005, color: pink })
        .paint([0, 0.068, 0.009], 0.04, pink, { radii: [0.013, 0.052, 0.008], soft: 0.004 });
      const pivot = new THREE.Group(); pivot.position.set(side * 0.03, 0.123, -0.014);
      pivot.rotation.set(-0.12, 0, -side * 0.2);
      const em = new THREE.Mesh(es.mesh({ cells: 110 }), mat); em.castShadow = true; pivot.add(em);
      parts.head.add(pivot); parts[side < 0 ? "earL" : "earR"] = pivot;
    }
    stats.triangles = 0; group.traverse((m) => { if (m.isMesh && m.geometry.index) stats.triangles += m.geometry.index.count / 3; });
    return { group, parts, stats, pivots: { neck: NECK, earL: EAR_L, earR: EAR_R }, sculpts: { body, head: hs } };
  }

  root.K3S = { Sculpt, sculpt: () => new Sculpt(), meshSculpt, plushMaterial, glossMaterial, eye, tube, studioBackdrop, stageDisc,
    makeLitePost, trussOverlay, utilColor, bunny, version: "1.0" };
})(typeof window !== "undefined" ? window : globalThis);
