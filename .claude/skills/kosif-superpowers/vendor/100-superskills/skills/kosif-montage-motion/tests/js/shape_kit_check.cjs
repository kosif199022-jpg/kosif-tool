/* Geometry checks for kit/shape-kit.js under Node (three.js from the kit bundle; no browser).
   Prints one JSON line the Python test asserts on. */
const path = require("path");
global.window = global; global.performance = require("perf_hooks").performance;
global.document = { createElementNS: () => ({ style: {} }), createElement: () => ({ getContext: () => null, style: {} }) };
const kit = path.resolve(__dirname, "../../scripts/kit");
require(path.join(kit, "three-kit.bundle.js"));
require(path.join(kit, "shape-kit.js"));
const S = window.K3S, THREE = window.K3.THREE;

function measure(geo) {
  const p = geo.attributes.position.array, idx = geo.index.array;
  let vol = 0, area = 0; const edges = new Map();
  for (let t = 0; t < idx.length; t += 3) {
    const a = idx[t] * 3, b = idx[t + 1] * 3, c = idx[t + 2] * 3;
    const ax = p[a], ay = p[a + 1], az = p[a + 2], bx = p[b], by = p[b + 1], bz = p[b + 2], cx = p[c], cy = p[c + 1], cz = p[c + 2];
    vol += (ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)) / 6;
    const ux = bx - ax, uy = by - ay, uz = bz - az, wx = cx - ax, wy = cy - ay, wz = cz - az;
    area += Math.hypot(uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx) / 2;
    for (const [i, j] of [[idx[t], idx[t + 1]], [idx[t + 1], idx[t + 2]], [idx[t + 2], idx[t]]]) {
      const k = i < j ? i + "," + j : j + "," + i; edges.set(k, (edges.get(k) || 0) + 1);
    }
  }
  let open = 0; for (const n of edges.values()) if (n !== 2) open++;
  return { vol, area, openEdges: open, edges: edges.size };
}

const r = 0.1, sphere = S.sculpt().sphere([0.02, 0.03, -0.01], r).mesh({ cells: 64 });
const ms = measure(sphere);
const p = sphere.attributes.position.array; let maxErr = 0;
for (let i = 0; i < p.length; i += 3) maxErr = Math.max(maxErr, Math.abs(Math.hypot(p[i] - 0.02, p[i + 1] - 0.03, p[i + 2] + 0.01) - r));
const k = 0.03, blob = S.sculpt().sphere([-0.05, 0, 0], 0.05).sphere([0.05, 0, 0], 0.05, { k });
const hard = S.sculpt().sphere([-0.05, 0, 0], 0.05).sphere([0.05, 0, 0], 0.05);
const carved = S.sculpt().box([0, 0, 0], [0.1, 0.1, 0.1], 0.01).sphere([0, 0, 0.1], 0.06, { op: "sub", k: 0.005, color: "#ff0000" });
const cg = carved.mesh({ cells: 72 }), cm = measure(cg);
const tinted = carved.colorAt(0, 0, 0.04 + 0.0), plain = carved.colorAt(0.1, 0, 0);
const t0 = performance.now(); const bun = S.bunny({ cells: 96 }); const bunnyMs = performance.now() - t0;
console.log(JSON.stringify({
  sphere: { volRatio: ms.vol / (4 / 3 * Math.PI * r ** 3), areaRatio: ms.area / (4 * Math.PI * r * r), maxRadiusErr: maxErr, openEdges: ms.openEdges,
            evals: sphere.userData.stats.evals, full: sphere.userData.stats.full },
  smoothUnionGap: blob.dist(0, 0, 0), hardUnionGap: hard.dist(0, 0, 0),
  carved: { openEdges: cm.openEdges, volume: cm.vol, tintRed: tinted[0] - tinted[1], plainRed: plain[0] - plain[1] },
  bunny: { triangles: bun.stats.triangles, parts: Object.keys(bun.parts).sort(), ms: Math.round(bunnyMs) },
  api: Object.keys(S).sort()
}));
