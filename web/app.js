// KOSIF TOOL website — hash-routed static app for GitHub Pages.
import { t, getLang, setLang, applyStatic } from './i18n.js';
import { buildRequest, cliCommand, defaultsFor, RESOLUTIONS, REPO_URL } from './generator.js';
import { renderMarkdown } from './md.js';

const BASE = new URL('.', import.meta.url.replace(/web\/app\.js.*$/, '')).href; // repo root as served
const S = {
  records: [], byId: new Map(), cats: [], catMap: {}, meta: {}, playbooks: [], briefs: null, briefsPromise: null,
  templates: {}, favs: new Set(), previews: 'hover', shown: 48, lastList: [], ready: false, error: null,
  filters: { q: '', cat: '', type: '', origin: '', aspect: '', sort: 'rank' },
};
const view = document.getElementById('view');
const toastEl = document.getElementById('toast');

/* ---------- utilities ---------- */
function el(tag, attrs = {}, ...children) {
  const n = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'class') n.className = v;
    else if (k === 'html') n.innerHTML = v;
    else if (k.startsWith('on') && typeof v === 'function') n.addEventListener(k.slice(2), v);
    else if (k === 'dataset') Object.assign(n.dataset, v);
    else if (k === 'style' && typeof v === 'object') Object.assign(n.style, v);
    else n.setAttribute(k, v === true ? '' : v);
  }
  for (const c of children.flat()) {
    if (c === null || c === undefined || c === false) continue;
    n.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return n;
}
function link(text, href, attrs = {}) {
  const external = /^https?:/.test(href);
  return el('a', { href, ...(external ? { target: '_blank', rel: 'noopener noreferrer' } : {}), ...attrs }, text);
}
let toastTimer;
function toast(msg) {
  toastEl.textContent = msg; toastEl.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => toastEl.classList.remove('show'), 1800);
}
async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch (e) {
    const ta = el('textarea', { style: { position: 'fixed', opacity: 0 } }, text); document.body.append(ta); ta.select();
    try { document.execCommand('copy'); return true; } catch (e2) { window.prompt('Copy:', text); return false; } finally { ta.remove(); }
  }
}
async function fetchJSON(path) { const r = await fetch(path, { cache: 'no-cache' }); if (!r.ok) throw new Error(`HTTP ${r.status} for ${path}`); return r.json(); }
async function fetchText(path) { const r = await fetch(path, { cache: 'no-cache' }); if (!r.ok) throw new Error(`HTTP ${r.status} for ${path}`); return r.text(); }
function store(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* ignore */ } }
function load(key, fallback) { try { const v = localStorage.getItem(key); return v === null ? fallback : JSON.parse(v); } catch (e) { return fallback; } }
function catLabel(key) { const c = S.catMap[key]; if (!c) return key === 'uncategorized' ? t('uncategorized') : key; return getLang() === 'ar' ? c.ar : c.en; }
function recordName(r) { return getLang() === 'ar' && r.name_ar ? r.name_ar : r.name; }
function recordAlt(r) { return getLang() === 'ar' ? r.name : (r.name_ar || ''); }
function summary(r) { return getLang() === 'ar' ? (r.summary_ar || r.summary_en || '') : (r.summary_en || r.summary_ar || ''); }
function githubBlob(path) { return `${REPO_URL}/blob/main/${path}`; }
function aspectStyle(r) { const a = r.aspect; return { aspectRatio: a ? `${a.w} / ${a.h}` : '16 / 9' }; }
function isFav(id) { return S.favs.has(id); }
function toggleFav(id) { if (S.favs.has(id)) S.favs.delete(id); else S.favs.add(id); store('kosif.favs', [...S.favs]); }

/* ---------- data ---------- */
async function boot() {
  S.favs = new Set(load('kosif.favs', []));
  S.previews = load('kosif.previews', 'hover');
  Object.assign(S.filters, load('kosif.filters', {}));
  try {
    const [records, cats, meta, playbooks] = await Promise.all([
      fetchJSON('catalog/styles.json'), fetchJSON('catalog/categories.json'),
      fetchJSON('catalog/meta.json').catch(() => ({})), fetchJSON('catalog/playbooks.json').catch(() => []),
    ]);
    S.records = records; S.byId = new Map(records.map(r => [r.id, r]));
    S.cats = cats; S.catMap = Object.fromEntries(cats.map(c => [c.key, c]));
    S.meta = meta; S.playbooks = playbooks; S.ready = true;
  } catch (e) { S.error = e; }
  route();
}
function briefs() {
  if (!S.briefsPromise) S.briefsPromise = fetchJSON('catalog/briefs.json').then(b => (S.briefs = b)).catch(() => (S.briefs = {}));
  return S.briefsPromise;
}
async function template(lang) {
  if (!S.templates[lang]) S.templates[lang] = await fetchText(`templates/claude_request.${lang}.txt`);
  return S.templates[lang];
}

/* ---------- previews ---------- */
const playing = new Set();
function playPreview(media, r) {
  if (!r.video || S.previews === 'off') return;
  let v = media.querySelector('video');
  if (!v) { v = el('video', { muted: true, loop: true, playsinline: true, preload: 'none', 'aria-hidden': 'true' }); v.muted = true; media.append(v); }
  if (!v.getAttribute('src')) v.src = r.video;
  media.classList.add('playing'); playing.add(v);
  v.play().catch(() => media.classList.remove('playing'));
}
function stopPreview(media) {
  const v = media.querySelector('video'); if (!v) return;
  v.pause(); v.removeAttribute('src'); v.load(); media.classList.remove('playing'); playing.delete(v);
}
let observer;
function observeAuto(media, r) {
  if (!observer) observer = new IntersectionObserver(entries => {
    for (const en of entries) {
      const m = en.target; const rec = S.byId.get(m.dataset.id);
      if (S.previews !== 'auto') { stopPreview(m); continue; }
      if (en.isIntersecting && en.intersectionRatio >= .55 && playing.size < 6) playPreview(m, rec); else stopPreview(m);
    }
  }, { threshold: [0, .55, 1] });
  observer.observe(media);
}

/* ---------- filtering ---------- */
function haystack(r) {
  if (!r._hay) {
    r._hay = [r.id, r.name, r.name_ar, r.creator, r.summary_ar, r.summary_en, ...(r.keywords || []), ...(r.tech || []), ...(r.stack || []),
      ...(r.category || []).flatMap(k => [k, S.catMap[k]?.en, S.catMap[k]?.ar])].filter(Boolean).join(' ').toLowerCase();
  }
  return r._hay;
}
function filtered(extra = {}) {
  const f = { ...S.filters, ...extra };
  const tokens = f.q.trim().toLowerCase().split(/\s+/).filter(Boolean);
  let list = S.records.filter(r => {
    if (f.fav && !S.favs.has(r.id)) return false;
    if (f.cat === 'uncategorized') { if ((r.category || []).length) return false; }
    else if (f.cat && !(r.category || []).includes(f.cat)) return false;
    if (f.type && r.type !== f.type) return false;
    if (f.origin === 'pm' && r.origin !== 'PromptsMotion') return false;
    if (f.origin === 'base' && r.origin === 'PromptsMotion') return false;
    if (f.aspect && (r.aspect_label || 'unknown') !== f.aspect) return false;
    if (tokens.length) { const h = haystack(r); if (!tokens.every(tk => h.includes(tk))) return false; }
    return true;
  });
  const big = 1e9;
  const sorters = {
    rank: (a, b) => (a.rank || big) - (b.rank || big) || a.id.localeCompare(b.id),
    newest: (a, b) => (b.published || '').localeCompare(a.published || '') || (a.rank || big) - (b.rank || big),
    name: (a, b) => recordName(a).localeCompare(recordName(b), getLang()),
    difficulty: (a, b) => (a.difficulty || 9) - (b.difficulty || 9) || (a.rank || big) - (b.rank || big),
  };
  list.sort(sorters[f.sort] || sorters.rank);
  return list;
}

/* ---------- components ---------- */
function card(r) {
  const media = el('div', { class: 'media', style: aspectStyle(r), dataset: { id: r.id }, role: 'link', tabindex: '0', 'aria-label': t('card.open') + ': ' + recordName(r) });
  if (r.poster) {
    const img = el('img', { src: r.poster, alt: '', loading: 'lazy', referrerpolicy: 'no-referrer', decoding: 'async' });
    img.onerror = () => { img.remove(); media.prepend(el('div', { class: 'fallback' }, recordName(r))); };
    media.append(img);
  } else media.append(el('div', { class: 'fallback' }, recordName(r)));
  media.append(el('span', { class: 'badge' }, r.aspect_label && r.aspect_label !== 'other' ? r.aspect_label : t('type.' + r.type)));
  if (r.video) media.append(el('span', { class: 'play', 'aria-hidden': 'true' }, '▶'));
  const go = () => { location.hash = `#/style/${r.id}`; };
  media.addEventListener('click', go);
  media.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  media.addEventListener('pointerenter', e => { if (e.pointerType !== 'touch' && S.previews === 'hover') playPreview(media, r); });
  media.addEventListener('pointerleave', () => { if (S.previews === 'hover') stopPreview(media); });
  if (S.previews === 'auto' && r.video) observeAuto(media, r);

  const fav = el('button', { class: 'fav-btn' + (isFav(r.id) ? ' on' : ''), title: t(isFav(r.id) ? 'card.unfav' : 'card.fav'), 'aria-label': t('card.fav'),
    onclick: () => { toggleFav(r.id); fav.classList.toggle('on', isFav(r.id)); fav.title = t(isFav(r.id) ? 'card.unfav' : 'card.fav'); } }, '♥');
  const body = el('div', { class: 'body' },
    el('h3', {}, el('a', { href: `#/style/${r.id}` }, recordName(r))),
    el('div', { class: 'sub' }, el('span', {}, r.creator || ''), el('span', { class: 'id' }, r.id)),
    el('div', { class: 'tags' }, el('span', { class: `tag type-${r.type}` }, t('type.' + r.type)), ...(r.category || []).slice(0, 3).map(k => el('span', { class: 'tag' }, catLabel(k)))),
    el('div', { class: 'actions' }, el('a', { class: 'btn small', href: `#/style/${r.id}` }, t('card.open')), fav));
  return el('article', { class: 'card' }, media, body);
}
function grid(list, mount) {
  mount.replaceChildren();
  const frag = document.createDocumentFragment();
  for (const r of list) frag.append(card(r));
  mount.append(frag);
}

/* ---------- views ---------- */
function setActiveNav(name) { document.querySelectorAll('#nav a[data-route]').forEach(a => a.classList.toggle('active', a.dataset.route === name)); }

function viewLibrary({ favOnly = false } = {}) {
  setActiveNav(favOnly ? 'favorites' : 'library');
  const m = S.meta;
  const hero = favOnly ? el('div', { class: 'panel' }, el('h1', {}, t('fav.title'))) : el('section', { class: 'hero' },
    el('div', {}, el('span', { class: 'kicker' }, t('hero.kicker')), el('h1', {}, t('hero.title')),
      el('p', {}, t('hero.sub', { total: m.total || S.records.length, pm: m.promptsmotion || '', base: m.base || '' })),
      el('div', { class: 'cta-row' }, el('a', { class: 'btn primary', href: '#library', onclick: e => { e.preventDefault(); document.getElementById('q')?.focus(); } }, t('hero.cta.library')), el('a', { class: 'btn', href: '#/generator' }, t('hero.cta.generator')))),
    el('div', { class: 'stats' },
      el('div', { class: 'stat' }, el('b', {}, m.total || S.records.length), el('span', {}, t('stat.styles'))),
      el('div', { class: 'stat' }, el('b', {}, m.with_briefs || 0), el('span', {}, t('stat.briefs'))),
      el('div', { class: 'stat' }, el('b', {}, m.playbooks || S.playbooks.length), el('span', {}, t('stat.playbooks'))),
      el('div', { class: 'stat' }, el('b', {}, m.creators || ''), el('span', {}, t('stat.creators')))));

  const f = S.filters;
  const q = el('input', { id: 'q', type: 'search', placeholder: t('search.placeholder'), value: f.q, autocomplete: 'off' });
  const sel = (key, options) => {
    const s = el('select', { 'aria-label': t('filter.' + key) }, ...options.map(([v, label]) => el('option', { value: v, selected: f[key] === v || null }, label)));
    s.onchange = () => { f[key] = s.value; S.shown = 48; persist(); refresh(); };
    return s;
  };
  const type = sel('type', [['', t('filter.type') + ': ' + t('filter.all')], ['Prompt', t('type.Prompt')], ['Skill', t('type.Skill')], ['Style', t('type.Style')]]);
  const origin = sel('origin', [['', t('filter.origin') + ': ' + t('filter.all')], ['pm', t('origin.pm')], ['base', t('origin.base')]]);
  const aspects = ['16:9', '9:16', '1:1', '4:5', '4:3', '21:9', 'other', 'unknown'].filter(a => S.records.some(r => (r.aspect_label || 'unknown') === a));
  const aspect = sel('aspect', [['', t('filter.aspect') + ': ' + t('filter.all')], ...aspects.map(a => [a, a === 'unknown' ? '—' : a])]);
  const sort = sel('sort', [['rank', t('sort.rank')], ['newest', t('sort.newest')], ['name', t('sort.name')], ['difficulty', t('sort.difficulty')]]);
  const prev = el('select', { 'aria-label': t('filter.previews') }, ...[['hover', t('previews.hover')], ['auto', t('previews.auto')], ['off', t('previews.off')]].map(([v, l]) => el('option', { value: v, selected: S.previews === v || null }, t('filter.previews') + ': ' + l)));
  prev.onchange = () => { S.previews = prev.value; store('kosif.previews', S.previews); refresh(); };
  const chips = el('div', { class: 'chips' });
  const counts = {}; for (const r of S.records) { const ks = r.category?.length ? r.category : ['uncategorized']; for (const k of ks) counts[k] = (counts[k] || 0) + 1; }
  const chipFor = (key, label) => { const c = el('button', { class: 'chip' + (f.cat === key ? ' active' : ''), onclick: () => { f.cat = f.cat === key ? '' : key; S.shown = 48; persist(); refresh(); } }, label, key ? el('b', {}, counts[key] || 0) : null); return c; };
  chips.append(chipFor('', t('filter.all')), ...S.cats.map(c => chipFor(c.key, catLabel(c.key))));
  if (counts.uncategorized) chips.append(chipFor('uncategorized', t('uncategorized')));
  const status = el('div', { class: 'status-row' });
  const mount = el('div', { class: 'grid' });
  const more = el('div', { class: 'load-more' });
  const toolbar = el('div', { class: 'toolbar' }, el('div', { class: 'search-row' }, q, type, origin, aspect, sort, prev), chips);
  let timer;
  q.oninput = () => { clearTimeout(timer); timer = setTimeout(() => { f.q = q.value; S.shown = 48; persist(); refresh(); }, 120); };
  function persist() { store('kosif.filters', { q: f.q, cat: f.cat, type: f.type, origin: f.origin, aspect: f.aspect, sort: f.sort }); }
  function refresh() {
    chips.querySelectorAll('.chip').forEach((c, i) => c.classList.toggle('active', i === 0 ? !f.cat : (c.textContent.startsWith(catLabel(S.cats[i - 1]?.key)) && f.cat === S.cats[i - 1]?.key) || (f.cat === 'uncategorized' && c.textContent === t('uncategorized'))));
    const list = filtered({ fav: favOnly }); S.lastList = list.map(r => r.id);
    const slice = list.slice(0, S.shown);
    status.replaceChildren(el('span', {}, list.length ? t('results', { shown: slice.length, count: list.length }) : (favOnly ? t('fav.empty') : t('results.none'))),
      el('span', {}, (f.q || f.cat || f.type || f.origin || f.aspect) ? el('button', { class: 'btn small', onclick: () => { Object.assign(f, { q: '', cat: '', type: '', origin: '', aspect: '' }); q.value = ''; type.value = origin.value = aspect.value = ''; S.shown = 48; persist(); refresh(); } }, t('clear.filters')) : null,
        favOnly && list.length ? el('button', { class: 'btn small', onclick: async () => { await copyText(list.map(r => r.id).join('\n')); toast(t('detail.copied')); } }, t('fav.copyIds')) : null));
    playing.forEach(v => { v.pause(); }); playing.clear();
    grid(slice, mount);
    more.replaceChildren(list.length > S.shown ? el('button', { class: 'btn', onclick: () => { S.shown += 48; refresh(); } }, t('load.more') + ` (${list.length - S.shown})`) : null);
  }
  view.replaceChildren(hero, toolbar, status, mount, more);
  refresh();
}

async function viewStyle(id) {
  setActiveNav('library');
  const r = S.byId.get(id);
  if (!r) { view.replaceChildren(el('div', { class: 'empty' }, t('detail.notfound'), ' ', link(t('detail.back'), '#/'))); return; }
  const L = getLang();
  const order = S.lastList.includes(id) ? S.lastList : S.records.map(x => x.id);
  const idx = order.indexOf(id);
  const prevId = idx > 0 ? order[idx - 1] : null, nextId = idx >= 0 && idx < order.length - 1 ? order[idx + 1] : null;

  const player = el('div', { class: 'player' });
  if (r.video) {
    const v = el('video', { controls: true, playsinline: true, preload: 'metadata', poster: r.poster || null, src: r.video, style: aspectStyle(r) });
    v.onerror = () => player.replaceChildren(el('div', { class: 'fallback' }, link(t('detail.watch') + ' ↗', r.page)));
    player.append(v);
  } else player.append(el('div', { class: 'fallback' }, r.poster ? el('img', { src: r.poster, alt: '', referrerpolicy: 'no-referrer' }) : null, el('p', {}, link(t('detail.watch') + ' ↗', r.page))));

  const row = (label, value) => value === null || value === undefined || value === '' || (Array.isArray(value) && !value.length) ? null : el('tr', {}, el('th', {}, label), el('td', {}, value));
  const metaTable = el('table', { class: 'meta-table' },
    row(t('detail.creator'), r.creator_url ? link(r.creator, r.creator_url) : r.creator),
    row(t('detail.source'), link(new URL(r.page).hostname + ' ↗', r.page)),
    row(t('detail.published'), r.published),
    row(t('detail.model'), r.model ? `${r.model}${r.effort ? ' · ' + t('detail.effort') + ' ' + r.effort : ''}` : null),
    row(t('detail.aspect'), r.aspect ? `${r.aspect_label} (${r.aspect.w}×${r.aspect.h})` : null),
    row(t('detail.rank'), r.rank ? `#${r.rank}` : null),
    row(t('detail.tech'), (r.tech || []).join(', ')),
    row(t('detail.promptWords'), r.source_prompt_words ? `≈ ${r.source_prompt_words} ${t('detail.words')}` : null),
    row(t('detail.difficulty'), r.difficulty ? '●'.repeat(r.difficulty) + '○'.repeat(5 - r.difficulty) + ` ${r.difficulty}/5` : null),
    row(t('detail.duration'), r.duration_s ? `${r.duration_s} s` : null),
    row(t('detail.stack'), (r.stack || []).join(', ')),
    row(t('detail.categories'), (r.category || []).length ? el('span', { class: 'tags' }, ...r.category.map(k => el('a', { class: 'tag', href: '#/', onclick: () => { S.filters.cat = k; store('kosif.filters', S.filters); } }, catLabel(k)))) : t('uncategorized')),
    row(t('detail.playbooks'), (r.playbooks || []).length ? el('span', {}, ...r.playbooks.map((p, i) => [i ? ' · ' : null, el('a', { href: `#/playbook/${p.replace(/^playbooks\//, '').replace(/\.md$/, '')}` }, p.replace(/^playbooks\//, '').replace(/\.md$/, ''))])) : null));

  const copyBtn = el('button', { class: 'btn primary', onclick: async () => {
    const tpl = await template(L); const b = S.briefs?.[id];
    const text = buildRequest({ template: tpl, record: r, categories: S.cats, options: { ...defaultsFor(r, b), reqLang: L }, hasBrief: !!r.brief });
    await copyText(text); copyBtn.textContent = t('detail.copied'); setTimeout(() => (copyBtn.textContent = t('detail.copy')), 1500);
  } }, t('detail.copy'));
  const fav = el('button', { class: 'btn' + (isFav(id) ? ' on' : ''), onclick: () => { toggleFav(id); fav.textContent = (isFav(id) ? '♥ ' : '♡ ') + t(isFav(id) ? 'card.unfav' : 'card.fav'); } }, (isFav(id) ? '♥ ' : '♡ ') + t(isFav(id) ? 'card.unfav' : 'card.fav'));
  const head = el('div', { class: 'panel' },
    el('div', { class: 'tags', style: { marginBottom: '8px' } }, el('span', { class: `tag type-${r.type}` }, t('type.' + r.type)), el('span', { class: 'tag' }, r.origin === 'PromptsMotion' ? t('origin.pm') : t('origin.base')), r.listed === false ? el('span', { class: 'tag' }, t('detail.unlisted')) : null),
    el('h1', {}, recordName(r)), recordAlt(r) && recordAlt(r) !== recordName(r) ? el('p', { class: 'lead', dir: 'auto' }, recordAlt(r)) : null,
    summary(r) ? el('p', { class: 'lead' }, summary(r)) : null,
    el('div', { class: 'id', style: { fontFamily: 'var(--mono)', direction: 'ltr', textAlign: 'start', color: 'var(--muted)', fontSize: '12px' } }, r.id),
    metaTable,
    el('div', { class: 'row-actions' }, copyBtn, el('a', { class: 'btn', href: `#/generator?style=${encodeURIComponent(id)}` }, t('detail.generator')), fav),
    el('div', { class: 'row-actions' }, link(t('detail.skill') + ' ↗', githubBlob(`styles/${id}/SKILL.md`), { class: 'btn small' }), r.brief ? link(t('detail.briefFile') + ' ↗', githubBlob(r.brief), { class: 'btn small' }) : null, link(t('detail.watch') + ' ↗', r.page, { class: 'btn small' })),
    el('p', { class: 'notice' }, t('detail.notice')));

  const briefPanel = el('div', { class: 'panel brief' }, el('h2', {}, t('detail.brief')), el('div', { class: 'skeleton', style: { height: '80px' } }));
  const relatedList = S.records.filter(x => x.id !== id && (x.category || []).some(k => (r.category || []).includes(k)))
    .sort((a, b) => ((b.category || []).filter(k => r.category.includes(k)).length - (a.category || []).filter(k => r.category.includes(k)).length) || ((a.rank || 1e9) - (b.rank || 1e9))).slice(0, 8);
  const related = el('div', { class: 'panel' }, el('h2', {}, t('detail.related')), el('div', { class: 'related' }, ...relatedList.map(x => el('a', { href: `#/style/${x.id}` }, recordName(x), el('small', {}, x.id)))));
  const pager = el('div', { class: 'pager' }, prevId ? el('a', { class: 'btn', href: `#/style/${prevId}` }, '‹ ' + t('detail.prev')) : el('span'), el('a', { class: 'btn', href: '#/' }, t('detail.back')), nextId ? el('a', { class: 'btn', href: `#/style/${nextId}` }, t('detail.next') + ' ›') : el('span'));

  view.replaceChildren(el('div', { class: 'detail' }, el('div', {}, player, pager, relatedList.length ? related : null), el('div', {}, head, briefPanel)));
  window.scrollTo({ top: 0 });

  const all = await briefs(); const b = all[id];
  if (!b) { briefPanel.replaceChildren(el('h2', {}, t('detail.brief')), el('p', { class: 'lead' }, t('detail.brief.none'))); return; }
  let bl = L;
  const render = () => {
    const ar = bl === 'ar';
    const list = items => el('ul', { dir: ar ? 'rtl' : 'ltr' }, ...items.map(x => el('li', {}, x)));
    briefPanel.replaceChildren(
      el('div', { style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '8px' } }, el('h2', {}, t('detail.brief')), el('button', { class: 'btn small', onclick: () => { bl = ar ? 'en' : 'ar'; render(); } }, ar ? 'EN' : 'AR')),
      el('div', { dir: ar ? 'rtl' : 'ltr', style: { textAlign: ar ? 'right' : 'left' } },
        el('h3', {}, t('detail.concept')), el('p', {}, ar ? b.concept_ar : b.concept_en),
        el('h3', {}, t('detail.scenes')), list(ar ? b.scenes_ar : b.scenes_en),
        el('h3', {}, t('detail.rules')), list(ar ? b.motion_rules_ar : b.motion_rules_en),
        (b.facts_from_source || []).length ? [el('h3', {}, t('detail.facts')), list(b.facts_from_source)] : null,
        el('h3', {}, t('detail.assumptions')), el('p', { dir: 'ltr', style: { textAlign: 'left' } }, b.assumptions_en),
        el('h3', {}, t('detail.keywords')), el('div', { class: 'tags' }, ...(b.keywords || []).map(k => el('span', { class: 'tag' }, k)))));
  };
  render();
}

function parseQuery(hash) { const i = hash.indexOf('?'); return i < 0 ? {} : Object.fromEntries(new URLSearchParams(hash.slice(i + 1))); }

async function viewGenerator(query) {
  setActiveNav('generator');
  const L = getLang();
  const saved = load('kosif.gen', {});
  const state = { styleId: query.style || saved.styleId || '', opts: { ...defaultsFor(null, null), reqLang: L, ...(saved.opts || {}) } };
  if (query.style) { const r = S.byId.get(query.style); if (r) { await briefs(); Object.assign(state.opts, { aspect: defaultsFor(r, S.briefs?.[r.id]).aspect, duration: defaultsFor(r, S.briefs?.[r.id]).duration }); } }
  await briefs();
  const o = state.opts;
  const field = (label, control, full = false) => el('label', { class: 'field' + (full ? ' full' : '') }, label, control);
  const select = (key, options) => { const s = el('select', {}, ...options.map(([v, l]) => el('option', { value: v, selected: String(o[key]) === String(v) || null }, l))); s.onchange = () => { o[key] = s.value; update(); }; return s; };
  const input = (key, attrs = {}) => { const i = el('input', { value: o[key] ?? '', ...attrs }); i.oninput = () => { o[key] = attrs.type === 'number' ? Number(i.value) : i.value; update(); }; return i; };
  const styleInput = el('input', { type: 'text', placeholder: t('gen.style.placeholder'), autocomplete: 'off', value: state.styleId ? `${state.styleId}` : '' });
  const suggest = el('div', { class: 'suggest' });
  const pick = el('div', { class: 'style-pick' }, styleInput, suggest);
  function showSuggest() {
    const qv = styleInput.value.trim().toLowerCase();
    const list = S.records.filter(r => !qv || haystack(r).includes(qv)).slice(0, 12);
    suggest.replaceChildren(...list.map(r => el('button', { type: 'button', onclick: () => { state.styleId = r.id; styleInput.value = r.id; suggest.classList.remove('open'); const d = defaultsFor(r, S.briefs?.[r.id]); o.aspect = d.aspect; o.duration = d.duration; aspectSel.value = o.aspect; durationIn.value = o.duration; update(); } }, recordName(r), el('small', {}, r.id))));
    suggest.classList.toggle('open', list.length > 0);
  }
  styleInput.oninput = () => { state.styleId = S.byId.has(styleInput.value.trim()) ? styleInput.value.trim() : ''; showSuggest(); update(); };
  styleInput.onfocus = showSuggest;
  document.addEventListener('click', e => { if (!pick.contains(e.target)) suggest.classList.remove('open'); });
  const reqLang = select('reqLang', [['ar', 'العربية'], ['en', 'English']]);
  const lang = select('lang', [['ar', t('gen.lang.ar')], ['en', t('gen.lang.en')], ['both', t('gen.lang.both')]]);
  const source = select('source', [['none', t('gen.source.none')], ['audio', t('gen.source.audio')], ['video', t('gen.source.video')], ['text', t('gen.source.text')]]);
  const detail = input('detail', { type: 'text', placeholder: 'voice.mp3 / clip.mp4 / …' });
  const aspectSel = input('aspect', { type: 'text', list: 'aspect-presets', placeholder: '9:16 · 21:9 · 2.35:1 · 1920x816 · reel' });
  const aspectList = el('datalist', { id: 'aspect-presets' }, ...Object.keys(RESOLUTIONS).map(a => el('option', { value: a }, `${a} (${RESOLUTIONS[a]})`)));
  document.getElementById('aspect-presets')?.remove(); document.body.append(aspectList);
  const durationIn = input('duration', { type: 'number', min: 3, max: 600, step: 1 });
  const fps = select('fps', [['30', '30'], ['24', '24'], ['25', '25'], ['60', '60']]);
  const stack = select('stack', [['auto', t('gen.stack.auto')], ['remotion', 'Remotion / React'], ['canvas', 'HTML Canvas'], ['svg', 'SVG + GSAP'], ['three', 'Three.js']]);
  const audio = select('audio', [['keep', t('gen.audio.keep')], ['music', t('gen.audio.music')], ['sfx', t('gen.audio.sfx')], ['silent', t('gen.audio.silent')]]);
  const brand = input('brand', { type: 'text', placeholder: t('gen.brand.placeholder') });
  const notes = el('textarea', { placeholder: t('gen.notes.placeholder') }, o.notes || ''); notes.oninput = () => { o.notes = notes.value; update(); };
  const out = el('div', { class: 'output', dir: o.reqLang === 'en' ? 'ltr' : 'rtl' });
  const cli = el('div', { class: 'cli' });
  const copyBtn = el('button', { class: 'btn primary', onclick: async () => { if (!out.dataset.text) return; await copyText(out.dataset.text); toast(t('detail.copied')); } }, t('gen.copy'));
  const dl = el('button', { class: 'btn', onclick: () => { if (!out.dataset.text) return; const blob = new Blob([out.dataset.text], { type: 'text/markdown' }); const a = el('a', { href: URL.createObjectURL(blob), download: `claude-request-${state.styleId || 'style'}.md` }); document.body.append(a); a.click(); a.remove(); } }, t('gen.download'));
  const openClaude = el('a', { class: 'btn', target: '_blank', rel: 'noopener noreferrer', href: '#' }, t('gen.open'));
  async function update() {
    store('kosif.gen', { styleId: state.styleId, opts: o });
    const r = S.byId.get(state.styleId);
    out.dir = o.reqLang === 'en' ? 'ltr' : 'rtl';
    if (!r) { out.textContent = t('gen.nostyle'); delete out.dataset.text; cli.textContent = ''; copyBtn.disabled = dl.disabled = true; openClaude.href = '#'; return; }
    const tpl = await template(o.reqLang === 'en' ? 'en' : 'ar');
    const text = buildRequest({ template: tpl, record: r, categories: S.cats, options: o, hasBrief: !!r.brief });
    out.textContent = text; out.dataset.text = text; cli.textContent = cliCommand(r, o);
    copyBtn.disabled = dl.disabled = false; openClaude.href = 'https://claude.ai/new?q=' + encodeURIComponent(text);
  }
  const form = el('div', { class: 'panel' }, el('div', { class: 'form-grid' },
    field(t('gen.style'), pick, true), field(t('gen.reqLang'), reqLang), field(t('gen.lang'), lang),
    field(t('gen.source'), source), field(t('gen.source.detail'), detail),
    field(t('gen.aspect'), aspectSel), field(t('gen.duration'), durationIn), field(t('gen.fps'), fps), field(t('gen.stack'), stack),
    field(t('gen.audio'), audio, true), field(t('gen.brand'), brand, true), field(t('gen.notes'), notes, true)));
  view.replaceChildren(el('div', { class: 'panel', style: { marginBottom: '16px' } }, el('h1', {}, t('gen.title')), el('p', { class: 'lead' }, t('gen.sub'))),
    el('div', { class: 'gen' }, form, el('div', { class: 'panel' }, el('h2', {}, t('gen.output')), el('div', { class: 'row-actions', style: { margin: '0 0 10px' } }, copyBtn, dl, openClaude), out, el('h2', { style: { marginTop: '16px' } }, t('gen.cli')), cli)));
  update();
}

function viewPlaybooks() {
  setActiveNav('playbooks');
  const counts = {}; for (const r of S.records) for (const k of r.category || []) counts[k] = (counts[k] || 0) + 1;
  const cards = S.playbooks.map(p => el('div', { class: 'pb-card' }, el('h3', {}, getLang() === 'ar' ? p.title_ar : p.title_en), el('p', { dir: 'ltr', style: { textAlign: 'left' } }, p.excerpt),
    counts[p.key] ? el('span', { class: 'count' }, `${counts[p.key]} ${t('stat.styles')}`) : null, el('a', { class: 'btn small', href: `#/playbook/${p.key}` }, t('pb.open'))));
  view.replaceChildren(el('div', { class: 'panel', style: { marginBottom: '16px' } }, el('h1', {}, t('pb.title')), el('p', { class: 'lead' }, t('pb.sub'))), cards.length ? el('div', { class: 'pb-grid' }, ...cards) : el('div', { class: 'empty' }, t('pb.none')));
}
async function viewPlaybook(key) {
  setActiveNav('playbooks');
  const safe = key.replace(/[^a-z0-9-]/g, '');
  view.replaceChildren(el('div', { class: 'skeleton' }));
  let md;
  try { md = await fetchText(`playbooks/${safe}.md`); } catch (e) { view.replaceChildren(el('div', { class: 'empty' }, t('pb.none'), ' ', link(t('pb.back'), '#/playbooks'))); return; }
  const { html, toc } = renderMarkdown(md);
  const article = el('article', { class: 'article', dir: 'ltr', html });
  article.querySelectorAll('p, li, h1, h2, h3, h4, blockquote, th, td').forEach(n => n.setAttribute('dir', 'auto'));
  article.querySelectorAll('a[href]').forEach(a => { const href = a.getAttribute('href'); if (!/^(https?:|#)/.test(href)) { a.href = githubBlob(href.replace(/^(\.\.\/)+/, '')); a.target = '_blank'; a.rel = 'noopener noreferrer'; } });
  const related = S.records.filter(r => (r.category || []).includes(safe)).slice(0, 12);
  const tocEl = el('nav', { class: 'toc' }, el('b', {}, t('pb.toc')), ...toc.map(x => el('a', { href: `#${x.id}`, class: x.level === 3 ? 'l3' : '', onclick: e => { e.preventDefault(); document.getElementById(x.id)?.scrollIntoView({ behavior: 'smooth' }); } }, x.text)),
    el('div', { class: 'row-actions' }, el('a', { class: 'btn small', href: '#/playbooks' }, t('pb.back')), link(t('pb.github') + ' ↗', githubBlob(`playbooks/${safe}.md`), { class: 'btn small' })));
  view.replaceChildren(el('div', { class: 'reader' }, tocEl, el('div', {}, article, related.length ? el('div', { class: 'panel', style: { marginTop: '16px', maxWidth: '920px' } }, el('h2', {}, t('detail.related')), el('div', { class: 'related' }, ...related.map(x => el('a', { href: `#/style/${x.id}` }, recordName(x), el('small', {}, x.id))))) : null)));
  window.scrollTo({ top: 0 });
}

const GUIDE = {
  ar: {
    steps: [
      ['١ · اختر الاستايل', 'تصفّح المكتبة، شاهد المرجع من مصدره، واقرأ الملف الإبداعي. كل استايل له ID ثابت مثل pm-ror-fly-9950f1.'],
      ['٢ · ولّد الطلب', 'من صفحة الاستايل اضغط «انسخ طلب Claude»، أو افتح المولّد لضبط المادة والنسبة والمدة والتقنية والهوية.'],
      ['٣ · الصق في Claude Code', 'افتح المستودع في Claude Code (أو شاركه)، الصق الطلب وأرفق الصوت/الفيديو/النص. سيقرأ CLAUDE.md وAGENTS.md وSKILL.md وBRIEF.md والدلائل.'],
      ['٤ · راجع المعاينة', 'يكتب Claude ملفي STYLE.md وPLAN.md ثم يبني الحركة ويعرض لوحة إطارات ومقطعًا قصيرًا قبل الرندر النهائي.'],
      ['٥ · الرندر والتسليم', 'بعد موافقتك يرندر MP4 ويتحقق من المدة وعدد الإطارات ومسار الصوت، ويسلّم الملفات المصدرية القابلة للتعديل.'],
    ],
    tools: [
      ['python3 tools/kosif.py search <كلمة>', 'بحث في الاستايلات بالعربية أو الإنجليزية'],
      ['python3 tools/kosif.py show <id>', 'عرض السجل والملف الإبداعي والدلائل'],
      ['python3 tools/kosif.py prompt <id> --aspect 9:16 --duration 15', 'توليد نفس الطلب من الطرفية'],
      ['python3 tools/kosif.py scaffold <id> <مجلد>', 'إنشاء مشروع إنتاج (STYLE.md, PLAN.md, TEST_REPORT.md, words.json, starter)'],
      ['node tools/render_html.cjs --in page.html --out film.mp4 --preview', 'معاينة لوحة إطارات ثم رندر MP4 حتمي عبر Chromium وffmpeg'],
      ['python3 tools/words_convert.py captions.srt words.json', 'تحويل ترجمة SRT/VTT أو مخرجات Whisper إلى توقيتات كلمات'],
      ['python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration 15 --audio voice.mp3', 'بوابة التسليم: الأبعاد والإطارات والمدة والصوت والجهارة -14 LUFS'],
      ['python3 tools/sync_catalog.py && python3 tools/build.py', 'مزامنة الفهرس مع المصدر وإعادة توليد كل الملفات المشتقة'],
      ['python3 tools/validate.py', 'فحص سلامة الفهرس والملفات'],
    ],
    faq: [
      ['كيف أكتب طلبًا يعطي حركة احترافية لا «شرائح»؟', 'حدّد خمسة أشياء: الدور (مخرج موشن)، السياق التقني (Remotion أو Canvas أو SVG)، المخرج (النسبة والمدة والإطارات)، خطة مشاهد موقّتة ثانية بثانية، ونظام بصري (ألوان، خط، منحنيات إيزنج بأرقام). المولّد يضيفها كلها، وتبقى عليك المادة والهوية.'],
      ['هل تُنسخ برومبتات PromptsMotion؟', 'لا. المستودع يحفظ روابط المراجع وبيانات وصفية (العنوان، التصنيفات، المبدع، النسبة، التاريخ) فقط، وكل ملفات SKILL.md وBRIEF.md والدلائل كتابة أصلية من KOSIF.'],
      ['كيف أزامن الحركة مع تعليق صوتي عربي؟', 'أرفق الصوت واختر «ملف صوت» في المولّد. يفرّغ Claude الكلمات مع توقيتها في words.json ويحرّك كل كلمة أو جملة على توقيتها، مع الحفاظ على اتصال الحروف العربية. راجع دليل audio-sync وarabic-typography.'],
      ['أي تقنية أختار؟', 'Remotion عندما تريد مشروعًا قابلًا للتعديل بالكامل ورندرًا موثوقًا؛ HTML Canvas أو SVG للرسوم الخفيفة والسريعة مع الرندر عبر tools/render_html.cjs؛ Three.js فقط عند الحاجة لكاميرا ثلاثية الأبعاد حقيقية.'],
      ['هل أستطيع العمل من الهاتف؟', 'نعم: انسخ الطلب من هذه الصفحة، الصقه في Claude (تطبيق أو موقع) مع إعطائه رابط المستودع، وأرفق الصوت أو النص. الرندر النهائي يحتاج بيئة Claude Code مع Chromium أو Remotion.'],
    ],
  },
  en: {
    steps: [
      ['1 · Pick a style', 'Browse the library, watch the reference at its source and read the creative brief. Every style has a stable ID such as pm-ror-fly-9950f1.'],
      ['2 · Generate the request', 'Press "Copy Claude request" on the style page, or open the generator to set material, aspect, duration, stack and brand.'],
      ['3 · Paste into Claude Code', 'Open the repository in Claude Code (or share it), paste the request and attach your audio, video or script. Claude reads CLAUDE.md, AGENTS.md, SKILL.md, BRIEF.md and the playbooks.'],
      ['4 · Review the preview', 'Claude writes STYLE.md and PLAN.md, builds the motion and shows a contact sheet plus a short clip before the final render.'],
      ['5 · Render and deliver', 'After your approval it renders the MP4, verifies duration, frame count and audio track, and delivers the editable sources.'],
    ],
    tools: [
      ['python3 tools/kosif.py search <word>', 'search styles in Arabic or English'],
      ['python3 tools/kosif.py show <id>', 'print the record, brief and playbooks'],
      ['python3 tools/kosif.py prompt <id> --aspect 9:16 --duration 15', 'generate the same request from the terminal'],
      ['python3 tools/kosif.py scaffold <id> <dir>', 'create a production project (STYLE.md, PLAN.md, TEST_REPORT.md, words.json, starter)'],
      ['node tools/render_html.cjs --in page.html --out film.mp4 --preview', 'contact-sheet preview, then a deterministic MP4 render through Chromium and ffmpeg'],
      ['python3 tools/words_convert.py captions.srt words.json', 'convert SRT/VTT subtitles or Whisper output into word timings'],
      ['python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration 15 --audio voice.mp3', 'delivery gate: dimensions, fps, duration, audio and -14 LUFS loudness'],
      ['python3 tools/sync_catalog.py && python3 tools/build.py', 'sync the catalog with the source and regenerate every derived file'],
      ['python3 tools/validate.py', 'integrity checks for the catalog and files'],
    ],
    faq: [
      ['How do I write a request that yields real motion, not slides?', 'State five things: the role (motion director), the technical context (Remotion, Canvas or SVG), the deliverable (aspect, duration, fps), a second-by-second scene plan, and a visual system (colors, type, easing curves with numbers). The generator adds all of them; you supply the material and the brand.'],
      ['Are PromptsMotion prompts copied?', 'No. The repository stores reference links and descriptive metadata only (title, categories, creator, aspect, date). Every SKILL.md, BRIEF.md and playbook is original KOSIF writing.'],
      ['How do I sync motion to an Arabic voice-over?', 'Attach the audio and pick "Audio file" in the generator. Claude transcribes word timings into words.json and animates each word or phrase on its timestamp while keeping Arabic letters joined. See the audio-sync and arabic-typography playbooks.'],
      ['Which stack should I choose?', 'Remotion for a fully editable project with reliable rendering; HTML Canvas or SVG for light, fast vector motion rendered through tools/render_html.cjs; Three.js only when a true 3D camera is needed.'],
      ['Can I work from my phone?', 'Yes: copy the request here, paste it into Claude (app or web) with the repository link, and attach your audio or script. The final render needs a Claude Code environment with Chromium or Remotion.'],
    ],
  },
};
function viewGuide() {
  setActiveNav('guide');
  const g = GUIDE[getLang()];
  view.replaceChildren(el('div', { class: 'guide' },
    el('div', { class: 'panel' }, el('h1', {}, t('guide.title')), el('div', { class: 'steps' }, ...g.steps.map(([b, p]) => el('div', { class: 'step' }, el('b', {}, b), p)))),
    el('div', { class: 'panel' }, el('h2', {}, getLang() === 'ar' ? 'أدوات المستودع' : 'Repository tools'), el('table', { class: 'meta-table' }, ...g.tools.map(([c, d]) => el('tr', {}, el('th', {}, el('code', { dir: 'ltr', style: { display: 'inline-block' } }, c)), el('td', {}, d))))),
    el('div', { class: 'panel faq' }, el('h2', {}, getLang() === 'ar' ? 'أسئلة شائعة' : 'FAQ'), ...g.faq.map(([q, a]) => el('details', {}, el('summary', {}, q), el('p', {}, a)))),
    el('div', { class: 'panel' }, el('h2', {}, getLang() === 'ar' ? 'الحقوق والمصادر' : 'Rights and sources'), el('p', { class: 'lead' }, t('footer.text')), el('div', { class: 'row-actions' }, link('README ↗', githubBlob('README.md'), { class: 'btn small' }), link('AGENTS.md ↗', githubBlob('AGENTS.md'), { class: 'btn small' }), link('PromptsMotion ↗', 'https://www.promptsmotion.com', { class: 'btn small' })))));
}

/* ---------- router ---------- */
function route() {
  if (S.error) { view.replaceChildren(el('div', { class: 'empty' }, t('error.load'), el('br'), el('code', {}, String(S.error.message)))); return; }
  if (!S.ready) return;
  playing.forEach(v => v.pause()); playing.clear();
  const hash = location.hash || '#/';
  const path = hash.replace(/^#/, '').split('?')[0];
  const m = path.match(/^\/(style|playbook)\/([^/]+)$/);
  if (m && m[1] === 'style') return viewStyle(decodeURIComponent(m[2]));
  if (m && m[1] === 'playbook') return viewPlaybook(decodeURIComponent(m[2]));
  if (path === '/generator') return viewGenerator(parseQuery(hash));
  if (path === '/playbooks') return viewPlaybooks();
  if (path === '/guide') return viewGuide();
  if (path === '/favorites') return viewLibrary({ favOnly: true });
  return viewLibrary();
}
window.addEventListener('hashchange', route);
document.getElementById('langToggle').addEventListener('click', () => { setLang(getLang() === 'ar' ? 'en' : 'ar'); applyStatic(); for (const r of S.records) delete r._hay; route(); });
document.getElementById('themeToggle').addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  const next = cur === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next); store('kosif.theme', next);
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', next === 'light' ? '#f5f7fb' : '#070b14');
});
document.addEventListener('keydown', e => {
  if (e.key === '/' && !/input|textarea|select/i.test(document.activeElement?.tagName || '')) { const q = document.getElementById('q'); if (q) { e.preventDefault(); q.focus(); } }
});
setLang(getLang()); applyStatic();
boot();
