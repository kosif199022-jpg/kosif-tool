/* drawFrame(canvas, manifest, time) — the kosif.motion.manifest.v1 canvas picture (ported from site/lib/motion.ts v3).
   Pure in t: the same manifest and time give the same frame. No eval, no remote assets. */
function drawFrame(canvas, m, time) {
  const c = canvas.getContext("2d"); if (!c) return;
  if (canvas.width !== m.width) canvas.width = m.width;
  if (canvas.height !== m.height) canvas.height = m.height;
  const w = m.width, h = m.height, f = Math.min(Math.floor(Math.max(0, time) * m.fps), Math.ceil(m.duration * m.fps) - 1);
  const i = Math.max(0, m.scenes.findIndex((s) => f >= s.start_frame && f < s.end_frame_exclusive)), s = m.scenes[i];
  if (!s) return;
  const u = Math.min(1, Math.max(0, (f - s.start_frame) / Math.max(1, s.end_frame_exclusive - s.start_frame))), e = 1 - Math.pow(1 - Math.min(1, u * 4), 3), unit = Math.min(w, h);
  c.fillStyle = "#11171b"; c.fillRect(0, 0, w, h);
  const g = c.createRadialGradient(w * .28, h * .25, 0, w * .5, h * .5, w * .8); g.addColorStop(0, s.accent + "32"); g.addColorStop(1, "#11171b");
  c.fillStyle = g; c.fillRect(0, 0, w, h);
  c.strokeStyle = "#ffffff0c"; c.lineWidth = 1;
  for (let x = 0; x < w; x += unit / 12) { c.beginPath(); c.moveTo(x, 0); c.lineTo(x, h); c.stroke(); }
  for (let y = 0; y < h; y += unit / 12) { c.beginPath(); c.moveTo(0, y); c.lineTo(w, y); c.stroke(); }
  c.save(); c.translate(w * .5, h * .43); c.rotate(time * .12 + i * .3);
  for (let k = 0; k < 3; k++) { c.strokeStyle = s.accent; c.globalAlpha = .12 + k * .13; c.lineWidth = unit * .003; c.beginPath(); c.ellipse(0, 0, unit * (.17 + k * .045) * (0.7 + e * .3), unit * (.17 + k * .045), k * .7, 0, Math.PI * 2); c.stroke(); }
  c.restore(); c.globalAlpha = e; c.fillStyle = s.accent; c.beginPath(); c.arc(w * .5, h * .42, unit * .03, 0, Math.PI * 2); c.fill();
  c.textAlign = "center"; c.direction = "rtl"; c.fillStyle = "#f2f4f3"; c.font = `600 ${unit * .066}px Tahoma, Arial, sans-serif`;
  c.fillText(s.title, w * .5, h * .69 + (1 - e) * unit * .05, w * .84);
  c.font = `${unit * .023}px Tahoma, Arial, sans-serif`; c.fillStyle = "#bbc7c9"; c.fillText(s.subtitle, w * .5, h * .76, w * .84);
  c.globalAlpha = 1; c.textAlign = "left"; c.direction = "ltr"; c.font = `${unit * .022}px monospace`; c.fillStyle = s.accent; c.fillText("KOSIF / MOTION", w * .07, h * .09);
  c.textAlign = "right"; c.fillStyle = "#829195"; c.fillText(String(i + 1).padStart(2, "0") + " / " + String(m.scenes.length).padStart(2, "0"), w * .93, h * .09);
  c.fillStyle = s.accent; c.fillRect(0, h - unit * .006, w * Math.min(1, time / m.duration), unit * .006);
}
