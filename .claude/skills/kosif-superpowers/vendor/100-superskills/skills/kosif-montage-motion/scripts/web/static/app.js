/* KOSIF Motion Web — the studio UI. Plain JS, no build step. Everything goes through /api/… */
const $ = (s) => document.querySelector(s), $$ = (s) => Array.from(document.querySelectorAll(s));
const state = { recipes: null, recipe: null, media: [], projects: [], jobs: [], job: null, es: null, wb: { plan: null, manifest: null, html: null }, env: null, transitions: [] };

async function api(path, opts = {}) {
  const r = await fetch(path, { headers: opts.body && !(opts.body instanceof FormData) ? { "Content-Type": "application/json" } : {}, ...opts,
    body: opts.body && !(opts.body instanceof FormData) ? JSON.stringify(opts.body) : opts.body });
  const text = await r.text();
  let data; try { data = JSON.parse(text); } catch { data = { raw: text }; }
  if (!r.ok) throw new Error(data.error || data.detail || `${r.status}`);
  return data;
}
function toast(msg, err = false) { const t = $("#toast"); t.textContent = msg; t.className = "toast" + (err ? " err" : ""); t.style.display = "block"; clearTimeout(t._h); t._h = setTimeout(() => (t.style.display = "none"), err ? 7000 : 3500); }
function fmtBytes(b) { return b > 1e9 ? (b / 1e9).toFixed(2) + " GB" : b > 1e6 ? (b / 1e6).toFixed(1) + " MB" : Math.round(b / 1e3) + " KB"; }
function fileUrl(p, dl = false) { return `/api/file?path=${encodeURIComponent(p)}${dl ? "&download=1" : ""}`; }
function esc(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }

/* ── navigation ── */
$$("#nav button").forEach((b) => b.addEventListener("click", () => show(b.dataset.view)));
function show(v) {
  $$("#nav button").forEach((b) => b.classList.toggle("active", b.dataset.view === v));
  $$(".view").forEach((s) => s.classList.toggle("active", s.id === "view-" + v));
  ({ media: loadMedia, recipes: loadRecipes, projects: loadProjects, timeline: initTimeline, jobs: loadJobs, review: loadReviews, claude: loadClaude, env: loadEnv }[v] || (() => {}))();
}

/* ── status / env ── */
async function loadEnv() {
  try {
    state.env = await api("/api/env");
    const e = state.env.env || {};
    $("#status").innerHTML = `<span class="pill ${e.route === "A" ? "ok" : e.route === "B" ? "warn" : "bad"}">المسار ${e.route || "?"}</span>` +
      `<span class="pill ${e.ffmpeg ? "ok" : "bad"}">FFmpeg</span><span class="pill ${e.browser ? "ok" : "bad"}">متصفح</span>` +
      `<span class="pill ${(e.libs || {}).faster_whisper ? "ok" : "warn"}">Whisper</span><span class="pill">${e.cpus || "?"} أنوية</span>` +
      `<span class="pill">${e.face_detector || "—"}</span><span class="pill">${e.xfade_transitions || 0} انتقال</span>`;
    $("#envJson").textContent = JSON.stringify(state.env, null, 1);
  } catch (err) { $("#status").innerHTML = `<span class="pill bad">${esc(err.message)}</span>`; }
}

/* ── media ── */
async function loadMedia() {
  const d = await api("/api/media"); state.media = d.media; $("#mediaDir").textContent = d.dir;
  $("#mediaGrid").innerHTML = d.media.map((m) => `<div class="media-item">${m.kind === "video" ? `<video src="${m.url}" controls preload="metadata"></video>` : m.kind === "image" ? `<img src="${m.url}" />` : m.kind === "audio" ? `<audio src="${m.url}" controls style="width:100%"></audio>` : `<div class="muted">📄</div>`}
    <div class="name">${esc(m.name)}</div><div class="muted">${fmtBytes(m.bytes)}${m.probe ? ` · ${m.probe.duration}s${m.probe.video ? ` · ${m.probe.video.w}×${m.probe.video.h}` : ""}` : ""}</div>
    <div class="row" style="margin-top:6px"><button data-copy="${esc(m.path)}">📋 المسار</button><button data-del="${esc(m.name)}" class="danger">🗑</button></div></div>`).join("") || `<div class="muted">لا وسائط بعد.</div>`;
  $$("#mediaGrid [data-copy]").forEach((b) => b.onclick = () => { navigator.clipboard.writeText(b.dataset.copy); toast("نُسخ المسار"); });
  $$("#mediaGrid [data-del]").forEach((b) => b.onclick = async () => { if (confirm("حذف " + b.dataset.del + "؟")) { await api("/api/media/" + encodeURIComponent(b.dataset.del), { method: "DELETE" }); loadMedia(); } });
}
const drop = $("#drop"), fileInput = $("#file");
drop.onclick = () => fileInput.click();
drop.ondragover = (e) => { e.preventDefault(); drop.classList.add("over"); }; drop.ondragleave = () => drop.classList.remove("over");
drop.ondrop = (e) => { e.preventDefault(); drop.classList.remove("over"); upload(e.dataTransfer.files); };
fileInput.onchange = () => upload(fileInput.files);
async function upload(files) {
  if (!files.length) return;
  const fd = new FormData(); for (const f of files) fd.append("file", f, f.name);
  drop.textContent = "جارٍ الرفع…";
  try { const r = await api("/api/media", { method: "POST", body: fd }); toast(`رُفع ${r.saved.filter((s) => !s.error).length} ملف`); } catch (err) { toast(err.message, true); }
  drop.textContent = "اسحب فيديو / صوت / صور هنا، أو اضغط للاختيار. الملفات تبقى على جهازك في مجلد workbench/media.";
  loadMedia();
}

/* ── recipes ── */
async function loadRecipes() {
  if (!state.recipes) state.recipes = (await api("/api/recipes")).groups;
  if (!state.media.length) try { state.media = (await api("/api/media")).media; } catch {}
  $("#recipeGroups").innerHTML = state.recipes.map((g) => `<h3>${esc(g.ar)}</h3>` + g.recipes.map((r) => `<div><button data-recipe="${r.id}" style="width:100%;text-align:right;margin-bottom:4px">${esc(r.ar)}</button></div>`).join("")).join("");
  $$("#recipeGroups [data-recipe]").forEach((b) => b.onclick = () => showRecipe(b.dataset.recipe));
}
function findRecipe(id) { for (const g of state.recipes) for (const r of g.recipes) if (r.id === id) return r; return null; }
function showRecipe(id, preset = {}) {
  const r = findRecipe(id); if (!r) return; state.recipe = r;
  $("#recipeTitle").textContent = r.ar;
  const mediaOpts = state.media.map((m) => `<option value="${esc(m.path)}">${esc(m.name)}</option>`).join("");
  $("#recipeForm").innerHTML = r.fields.map((f) => {
    const v = preset[f.arg] ?? f.default;
    let input;
    if (f.kind === "bool") input = `<input type="checkbox" data-arg="${f.arg}" ${v === "1" ? "checked" : ""} style="width:auto" />`;
    else if (f.kind === "choice") input = `<select data-arg="${f.arg}">${f.choices.map((c) => `<option ${c === v ? "selected" : ""}>${esc(c)}</option>`).join("")}</select>`;
    else input = `<input data-arg="${f.arg}" value="${esc(v)}" ${f.kind === "set" || f.kind === "text" ? "" : 'dir="ltr" style="text-align:left"'} />`;
    const picker = (f.kind === "file" || f.kind === "files") && mediaOpts ? `<select data-pick="${f.arg}" style="width:160px"><option value="">من المكتبة…</option>${mediaOpts}</select>` : `<span></span>`;
    return `<div class="field"><label>${esc(f.label)}</label>${input}${picker}</div>`;
  }).join("") || `<div class="muted">بلا معاملات.</div>`;
  $$("#recipeForm [data-pick]").forEach((s) => s.onchange = () => { const inp = $(`#recipeForm [data-arg="${s.dataset.pick}"]`); const f = r.fields.find((x) => x.arg === s.dataset.pick); inp.value = f.kind === "files" && inp.value ? inp.value + "|" + s.value : s.value; s.value = ""; cmdPreview(); });
  $$("#recipeForm [data-arg]").forEach((i) => i.oninput = cmdPreview);
  $("#recipeActions").style.display = "flex"; cmdPreview();
}
function recipeValues() { const v = {}; $$("#recipeForm [data-arg]").forEach((i) => { v[i.dataset.arg] = i.type === "checkbox" ? (i.checked ? "1" : "0") : i.value; }); return v; }
function cmdPreview() { const v = recipeValues(); $("#recipeCmd").textContent = `kmotion ${state.recipe.cmd} ` + Object.entries(v).filter(([k, x]) => x && x !== "0").map(([k, x]) => (k.startsWith("--") ? (x === "1" ? k : `${k} ${x}`) : x)).join(" "); }
$("#runRecipe").onclick = async () => {
  try { const j = await api("/api/jobs", { method: "POST", body: { recipe: state.recipe.id, args: recipeValues() } }); toast("بدأت المهمة " + j.id); show("jobs"); selectJob(j.id); }
  catch (err) { toast(err.message, true); }
};

/* ── jobs ── */
async function loadJobs() {
  const d = await api("/api/jobs"); state.jobs = d.jobs;
  $("#jobList").innerHTML = d.jobs.map((j) => `<div class="job ${state.job === j.id ? "active" : ""}" data-job="${j.id}"><span class="st ${j.status}">●</span><span><b>${esc(j.recipe)}</b> <span class="muted">${esc(j.note || "")}</span><div class="mono muted">${esc(j.command).slice(0, 110)}</div></span><span class="muted">${new Date((j.created || 0) * 1000).toLocaleTimeString("ar-EG")}</span></div>`).join("") || `<div class="muted">لا مهام بعد.</div>`;
  $$("#jobList [data-job]").forEach((el) => el.onclick = () => selectJob(el.dataset.job));
  if (state.job && !d.jobs.find((j) => j.id === state.job)) state.job = null;
}
function selectJob(id) {
  state.job = id; if (state.es) { state.es.close(); state.es = null; }
  $("#jobLog").textContent = ""; $("#jobOutputs").innerHTML = ""; $("#jobPreview").innerHTML = "";
  const j = state.jobs.find((x) => x.id === id); $("#jobTitle").textContent = j ? j.command : id;
  const es = new EventSource(`/api/jobs/${id}/log`); state.es = es;
  es.onmessage = (e) => { $("#jobLog").textContent += JSON.parse(e.data); $("#jobLog").scrollTop = $("#jobLog").scrollHeight; };
  es.addEventListener("end", (e) => { es.close(); state.es = null; const jj = JSON.parse(e.data); showOutputs(jj); loadJobs(); if (jj.status === "done") toast("انتهت المهمة ✓"); else toast("المهمة " + jj.status, true); });
  es.onerror = () => { es.close(); state.es = null; };
  $$("#jobList .job").forEach((el) => el.classList.toggle("active", el.dataset.job === id));
}
function showOutputs(j) {
  $("#jobOutputs").innerHTML = (j.outputs || []).map((o) => `<a href="${fileUrl(o, true)}">⬇ ${esc(o.split(/[\\/]/).pop())}</a>`).join("");
  const vid = (j.outputs || []).find((o) => /\.(mp4|webm|mov)$/i.test(o)), img = (j.outputs || []).find((o) => /\.(png|jpg|jpeg|webp|gif)$/i.test(o));
  $("#jobPreview").innerHTML = vid ? `<video class="preview" controls src="${fileUrl(vid)}"></video>` : img ? `<img src="${fileUrl(img)}" style="max-width:100%;border-radius:10px" />` : "";
}
$("#jobCancel").onclick = async () => { if (state.job) { await api(`/api/jobs/${state.job}/cancel`, { method: "POST" }); toast("أُرسل طلب الإيقاف"); } };

/* ── projects ── */
async function loadProjects() {
  const d = await api("/api/projects"); state.projects = d.projects;
  if (!$("#newTemplate").options.length) { const t = await api("/api/templates"); $("#newTemplate").innerHTML = t.motion_templates.map((m) => `<option value="${m.id}">${esc(m.id)} — ${esc(m.ar)}</option>`).join(""); }
  $("#projectGrid").innerHTML = d.projects.map((p) => `<div class="proj" data-proj="${esc(p.name)}"><div class="name">${esc(p.name)}</div><div class="muted">${p.kind || ""} ${p.size || ""} ${p.seconds ? p.seconds + "s" : ""}</div>
    <div class="frames">${(p.frames || []).slice(0, 4).map((f) => `<img src="${f}" />`).join("")}</div><div class="muted">${(p.outputs || []).length} تصيير</div></div>`).join("") || `<div class="muted">لا مشاريع: أنشئ واحداً أو شغّل وصفة direct/verse/template.</div>`;
  $$("#projectGrid [data-proj]").forEach((el) => el.onclick = () => showProject(el.dataset.proj));
}
$("#newKind").onchange = () => { $("#newTemplate").style.display = $("#newKind").value === "template" ? "" : "none"; };
$("#createProject").onclick = async () => {
  const kind = $("#newKind").value, name = $("#newName").value.trim(); if (!name) return toast("اكتب اسم المشروع", true);
  const body = { name, seconds: parseFloat($("#newSeconds").value) || 6, size: $("#newSize").value, fps: 30 };
  if (kind === "template") { body.kind = "template"; body.template = $("#newTemplate").value; body.params = Object.fromEntries(($("#newTitle").value.match(/(\w+)=("[^"]*"|\S+)/g) || []).map((kv) => { const [k, ...v] = kv.split("="); return [k, v.join("=").replace(/^"|"$/g, "")]; })); }
  else { body.kind = "new"; body.title = $("#newTitle").value; body.three_d = kind === "3d"; body.lab = kind === "lab"; body.canvas = kind === "canvas"; }
  try { const p = await api("/api/projects", { method: "POST", body }); toast("أُنشئ " + p.name); loadProjects(); showProject(p.name); } catch (err) { toast(err.message, true); }
};
async function showProject(name) {
  const d = await api(`/api/projects/${encodeURIComponent(name)}/files`); const p = d.info;
  $("#projectPanel").innerHTML = `<div class="row" style="justify-content:space-between"><b class="mono">${esc(p.name)}</b><span class="muted">${p.size || ""} · ${p.seconds || "?"}s · ${p.kind || ""}</span></div>
    ${p.preview ? `<iframe class="preview" src="${p.preview}"></iframe>` : ""}
    <div class="row" style="margin-top:8px"><button data-act="frames">🖼 إطارات 1,3,5</button><button data-act="preview">⚡ مسودة</button><button class="primary" data-act="render">🎬 تصيير</button><button data-act="lint">🔍 lint</button><button data-act="ask">🧠 Claude</button></div>
    <div class="row" style="margin-top:8px"><select id="projFile">${d.files.map((f) => `<option>${esc(f.path)}</option>`).join("")}</select><button id="projOpen">فتح</button><button id="projSave" class="primary">💾 حفظ</button></div>
    <textarea id="projCode" class="code" spellcheck="false"></textarea>
    <div class="outputs">${(p.outputs || []).map((o) => `<a href="${fileUrl(o, true)}">⬇ ${esc(o.split(/[\\/]/).pop())}</a>`).join("")}</div>
    ${(p.outputs || [])[0] ? `<video class="preview" controls src="${fileUrl(p.outputs[0])}"></video>` : ""}`;
  const proj = `projects/${p.name}`;
  $$("#projectPanel [data-act]").forEach((b) => b.onclick = async () => {
    const act = b.dataset.act;
    if (act === "ask") { show("claude"); $("#ctxProject").value = p.name; return; }
    const map = { frames: ["frames", { project: proj, "--times": "1,3,5" }], preview: ["preview", { project: proj }], render: ["render", { project: proj, "--engine": "studio", "--blur": "4", "--workers": "0" }], lint: ["lint", { project: proj }] };
    const [rid, args] = map[act];
    try { const j = await api("/api/jobs", { method: "POST", body: { recipe: rid, args, note: p.name } }); toast("بدأت " + rid); show("jobs"); selectJob(j.id); } catch (err) { toast(err.message, true); }
  });
  const open = async () => { const f = await api(`/api/projects/${encodeURIComponent(p.name)}/file?path=${encodeURIComponent($("#projFile").value)}`); $("#projCode").value = f.content; };
  $("#projOpen").onclick = open; if (d.files.length) open();
  $("#projSave").onclick = async () => { try { await api(`/api/projects/${encodeURIComponent(p.name)}/file`, { method: "POST", body: { path: $("#projFile").value, content: $("#projCode").value } }); toast("حُفظ (نسخة .bak من القديم)"); } catch (err) { toast(err.message, true); } };
}

/* ── timeline ── */
let tlInit = false;
async function initTimeline() {
  const [ex, list, media] = await Promise.all([api("/api/timeline/example"), api("/api/timeline/list"), api("/api/media")]);
  state.transitions = ex.transitions;
  $("#transitions").innerHTML = ex.transitions.map((t) => `<span class="pill" style="margin:2px">${t}</span>`).join(" ");
  $("#tlList").innerHTML = `<option value="">— المحفوظة —</option>` + list.timelines.map((t) => `<option value="${esc(t.name)}">${esc(t.name)}</option>`).join("");
  $("#tlMedia").innerHTML = media.media.map((m) => `<div data-copy="${esc(m.path)}" style="cursor:pointer">${esc(m.path)}</div>`).join("");
  $$("#tlMedia [data-copy]").forEach((el) => el.onclick = () => { navigator.clipboard.writeText(el.dataset.copy); toast("نُسخ"); });
  if (!tlInit) { if (!$("#tlSpec").value) $("#tlSpec").value = JSON.stringify(ex.spec, null, 1); tlInit = true; }
}
function tlSpec() { try { return JSON.parse($("#tlSpec").value); } catch (e) { toast("JSON غير صالح: " + e.message, true); return null; } }
$("#tlExample").onclick = async () => { const ex = await api("/api/timeline/example"); $("#tlSpec").value = JSON.stringify(ex.spec, null, 1); };
$("#tlLoad").onclick = async () => { const n = $("#tlList").value; if (!n) return; const t = await api(`/api/timeline/${encodeURIComponent(n)}`); $("#tlSpec").value = JSON.stringify(t.spec, null, 1); $("#tlName").value = t.name; checkTimeline(); };
$("#tlCheck").onclick = checkTimeline;
async function checkTimeline() {
  const spec = tlSpec(); if (!spec) return null;
  try { const s = await api("/api/timeline/validate", { method: "POST", body: { spec } }); drawStrip(s); $("#tlInfo").textContent = `✔ ${s.seconds}s · ${s.size} · ${s.fps} fps · ${s.clips.length} مقطع · ${s.transitions.length} انتقال · ${s.overlays.length} طبقة`; return s; }
  catch (err) { $("#tlInfo").textContent = "✖ " + err.message; $("#strip").innerHTML = ""; toast(err.message, true); return null; }
}
function drawStrip(s) {
  const total = Math.max(0.1, s.seconds), W = $("#strip").clientWidth || 800, px = (t) => (t / total) * W;
  let html = "";
  s.clips.forEach((c, i) => html += `<div class="clip" style="left:${px(c.start)}px;width:${Math.max(6, px(c.dur) - 2)}px" title="${esc(c.src)}">${i + 1} · ${esc(String(c.src).split(/[\\/]/).pop())} · ${c.dur}s${c.speed && c.speed !== 1 ? ` ×${c.speed}` : ""}${c.ramp ? " ramp" : ""}</div>`);
  s.transitions.forEach((t) => html += `<div class="tr" style="left:${px(t.at)}px;width:${Math.max(3, px(t.dur))}px" title="${t.type}"></div>`);
  s.overlays.forEach((o) => { if (o.start != null) html += `<div class="ov" style="left:${px(o.start)}px;width:${Math.max(6, px(o.end - o.start))}px">${esc(o.type)} ${esc(o.text || o.title || "")}</div>`; });
  html += `<div class="ruler"></div>`; $("#strip").innerHTML = html;
}
$("#tlSave").onclick = async () => { const spec = tlSpec(); if (!spec) return; try { const r = await api("/api/timeline/save", { method: "POST", body: { name: $("#tlName").value || "timeline", spec } }); toast("حُفظ " + r.saved); initTimeline(); } catch (err) { toast(err.message, true); } };
$("#tlRender").onclick = async () => {
  const spec = tlSpec(); if (!spec) return; if (!(await checkTimeline())) return;
  try { const r = await api("/api/timeline/save", { method: "POST", body: { name: $("#tlName").value || "timeline", spec } });
    const j = await api("/api/jobs", { method: "POST", body: { recipe: "timeline", args: { spec: r.saved, "--out": `out/${($("#tlName").value || "timeline")}.mp4`, "--inspect": "1" }, note: "timeline" } });
    toast("بدأ التصيير"); show("jobs"); selectJob(j.id); } catch (err) { toast(err.message, true); }
};
$("#tlStudio").onclick = () => $("#tlStudioFile").click();
$("#tlStudioFile").onchange = async () => {
  const f = $("#tlStudioFile").files[0]; $("#tlStudioFile").value = ""; if (!f) return;
  try {
    const project = JSON.parse(await f.text());
    const r = await api("/api/studio/import", { method: "POST", body: { project, name: f.name.replace(/\.kosif\.json$|\.json$/i, "") } });
    $("#tlSpec").value = JSON.stringify(r.spec, null, 1); $("#tlName").value = r.saved.split(/[\\/]/).pop().replace(/\.json$/, "");
    const rep = r.report, miss = rep.missing_media.length, skip = rep.skipped.length;
    toast(`استُورد «${rep.name}»: ${rep.clips.length} مقطع، ${rep.overlays.length} نص` + (miss ? ` · ${miss} ملف غير موجود في المكتبة (ارفعه ثم أعد الاستيراد)` : "") + (skip ? ` · ${skip} عنصر لم يُنقل` : ""), miss > 0);
    checkTimeline(); initTimeline();
  } catch (err) { toast("تعذّر الاستيراد: " + err.message, true); }
};
$("#tlAsk").onclick = () => { show("claude"); $("#ctxTimeline").checked = true; $("#claudeTask").value ||= "حسّن هذا التايملاين: انتقالات مناسبة، نص عنوان في البداية، ومدد متوازنة."; };

/* ── workbench ── */
function wbDraw() { if (state.wb.manifest) drawFrame($("#wbCanvas"), state.wb.manifest, parseFloat($("#wbTime").value)); $("#wbT").textContent = parseFloat($("#wbTime").value).toFixed(2); }
$("#wbTime").oninput = wbDraw;
let wbTimer = null;
$("#wbPlay").onclick = () => { if (wbTimer) { clearInterval(wbTimer); wbTimer = null; $("#wbPlay").textContent = "▶"; return; } const t0 = performance.now() - parseFloat($("#wbTime").value) * 1000; $("#wbPlay").textContent = "⏸"; wbTimer = setInterval(() => { const t = (performance.now() - t0) / 1000; if (t > parseFloat($("#wbTime").max)) { $("#wbTime").value = 0; clearInterval(wbTimer); wbTimer = null; $("#wbPlay").textContent = "▶"; } else $("#wbTime").value = t; wbDraw(); }, 33); };
$("#wbPlan").onclick = async () => { try { state.wb.plan = await api("/api/plan", { method: "POST", body: { task: $("#wbTask").value, seconds: parseFloat($("#wbSeconds").value), fps: parseInt($("#wbFps").value), aspect: $("#wbAspect").value } }); $("#wbJson").textContent = JSON.stringify(state.wb.plan, null, 1); $("#wbInfo").textContent = `خطة: ${state.wb.plan.intent} · ${state.wb.plan.timeline.shots.length} لقطات · ${state.wb.plan.timeline.total_frames} إطار`; } catch (err) { toast(err.message, true); } };
$("#wbValidate").onclick = async () => { if (!state.wb.plan) return toast("اعمل خطة أولاً", true); const v = await api("/api/validate", { method: "POST", body: { plan: state.wb.plan } }); $("#wbJson").textContent = JSON.stringify(v, null, 1); $("#wbInfo").textContent = v.valid ? "✔ الخطة صالحة" : "✖ " + v.errors.join(" "); };
$("#wbCompile").onclick = async () => { if (!state.wb.plan) return toast("اعمل خطة أولاً", true); try { const c = await api("/api/compile", { method: "POST", body: { plan: state.wb.plan } }); state.wb.manifest = c.manifest; state.wb.html = c.project_html; $("#wbJson").textContent = JSON.stringify(c.manifest, null, 1); $("#wbTime").max = c.manifest.duration; $("#wbTime").value = 0; wbDraw(); $("#wbInfo").textContent = `manifest: ${c.manifest.width}×${c.manifest.height} · ${c.manifest.duration}s · ${c.manifest.scenes.length} مشاهد` + (c.project_html ? " · معاينة HTML جاهزة" : " · (لا HTML لهذا النوع)"); } catch (err) { toast(err.message, true); } };
$("#wbRender").onclick = async () => {
  if (!state.wb.manifest) return toast("اعمل manifest أولاً", true);
  const m = { ...state.wb.manifest }; delete m.frames;
  try {
    const j = await api("/api/render/jobs", { method: "POST", body: { manifest: m } }); $("#wbInfo").textContent = "رندر محلي… 0%";
    const h = { "X-Job-Token": j.job_token };
    for (;;) { await new Promise((r) => setTimeout(r, 700)); const s = await (await fetch(`/api/render/jobs/${j.job_id}`, { headers: h })).json(); $("#wbInfo").textContent = `رندر محلي… ${Math.round((s.progress || 0) * 100)}% (${s.status})`; if (s.status === "succeeded") { const blob = await (await fetch(`/api/render/jobs/${j.job_id}/video`, { headers: h })).blob(); const url = URL.createObjectURL(blob); $("#wbVideo").innerHTML = `<video class="preview" controls src="${url}"></video><div class="muted">${JSON.stringify(s.metadata)}</div><a href="${url}" download="kosif-motion.mp4">⬇ تنزيل MP4</a>`; break; } if (s.status === "failed" || s.status === "cancelled") { toast(s.error || s.status, true); break; } }
  } catch (err) { toast(err.message, true); }
};
$("#wbProject").onclick = async () => { if (!state.wb.manifest) return toast("اعمل manifest أولاً", true); const name = prompt("اسم المشروع", "wb_" + Date.now().toString(36)); if (!name) return; const m = { ...state.wb.manifest }; delete m.frames; try { const p = await api("/api/projects", { method: "POST", body: { name, kind: "manifest", manifest: m } }); toast("أُنشئ المشروع " + p.name + " — صيّره بالمحرك الكامل من المشاريع"); show("projects"); } catch (err) { toast(err.message, true); } };

/* ── claude ── */
async function loadClaude() {
  try { const s = await api("/api/claude/status"); $("#claudeStatus").innerHTML = `الطريقة الفعلية: <b>${s.backend}</b> · ${esc(s.cli.message)}`; $("#mcpUrl").textContent = s.mcp; $("#setBackend").value = s.settings.backend; $("#setModel").value = s.settings.model; $("#setKey").placeholder = s.settings.api_key_set ? "مفتاح محفوظ " + s.settings.api_key_hint : "sk-ant-… (اختياري)"; } catch (err) { $("#claudeStatus").textContent = err.message; }
}
function claudeContext() { return { media: $("#ctxMedia").checked, projects: $("#ctxProjects").checked, timeline: $("#ctxTimeline").checked ? tlSpec() : null, project: $("#ctxProject").value.trim() || null }; }
$("#claudeAsk").onclick = async () => {
  const task = $("#claudeTask").value.trim(); if (!task) return toast("اكتب الطلب", true);
  $("#claudeMsg").textContent = "…"; try { const r = await api("/api/claude/ask", { method: "POST", body: { task, context: claudeContext() } });
    if (r.reply) { $("#claudeReply").value = r.reply; $("#claudePlan").textContent = JSON.stringify(r.plan, null, 1); $("#claudeMsg").textContent = `رد عبر ${r.backend}`; }
    else { $("#claudeReply").value = ""; $("#claudePlan").textContent = r.package; $("#claudeMsg").textContent = r.message; await navigator.clipboard.writeText(r.package).catch(() => {}); toast("نُسخت الحزمة: ألصقها في Claude ثم ألصق الرد هنا"); } }
  catch (err) { $("#claudeMsg").textContent = err.message; toast(err.message, true); }
};
$("#claudePackage").onclick = async () => { const task = $("#claudeTask").value.trim() || "اقترح خطة مونتاج"; const r = await api("/api/claude/package", { method: "POST", body: { task, context: claudeContext() } }); $("#claudePlan").textContent = r.package; await navigator.clipboard.writeText(r.package).catch(() => {}); toast("نُسخت الحزمة إلى الحافظة"); };
$("#claudeReply").oninput = () => { const m = $("#claudeReply").value.match(/```json\s*([\s\S]*?)```/); try { $("#claudePlan").textContent = JSON.stringify(JSON.parse(m ? m[1] : $("#claudeReply").value), null, 1); } catch { } };
$("#claudeApply").onclick = async () => { try { const d = await api("/api/claude/apply", { method: "POST", body: { plan: $("#claudeReply").value } }); $("#claudePlan").textContent = JSON.stringify(d, null, 1); toast(`طُبّق: ${d.files.length} ملف، ${d.jobs.length} مهمة${d.timeline ? "، تايملاين" : ""}`); if (d.jobs.length) { show("jobs"); await loadJobs(); if (d.jobs[0].id) selectJob(d.jobs[0].id); } } catch (err) { toast(err.message, true); } };
$("#saveSettings").onclick = async () => { const body = { backend: $("#setBackend").value, model: $("#setModel").value }; if ($("#setKey").value) body.anthropic_api_key = $("#setKey").value; await api("/api/claude/settings", { method: "POST", body }); $("#setKey").value = ""; toast("حُفظت الإعدادات محلياً"); loadClaude(); };

/* ── review (the Motion OS page on the KOSIF engine) ── */
async function loadReviews() {
  const d = await api("/api/reviews");
  $("#rvList").innerHTML = d.reviews.map((r) => `<div class="row" style="justify-content:space-between;border-bottom:1px solid var(--line,#333);padding:6px 0">
    <span><b>${esc(r.title || r.name)}</b> <span class="muted mono">${esc(r.name)} · v${r.version} · ${r.kind} · ${r.scenes} مشاهد · ${r.feedback} ملاحظات مرسلة</span></span>
    <a class="navlink" href="/review/${encodeURIComponent(r.name)}/" target="_blank" rel="noopener">فتح ↗</a></div>`).join("") || `<div class="muted">لا مراجعات بعد.</div>`;
}
$("#rvInit").onclick = async () => {
  const target = $("#rvTarget").value.trim(); if (!target) return toast("اكتب المسار", true);
  try { const r = await api("/api/reviews", { method: "POST", body: { target, video: $("#rvVideo").value.trim() || null, name: $("#rvName").value.trim() || null } });
    toast(`v${r.version}: ${r.scenes} مشاهد، ${r.elements} عناصر`); loadReviews(); window.open(`/review/${encodeURIComponent(r.name)}/`, "_blank", "noopener"); }
  catch (err) { toast(err.message, true); }
};

/* ── boot ── */
loadEnv(); loadMedia();
setInterval(() => { if ($("#view-jobs").classList.contains("active")) loadJobs(); }, 5000);
