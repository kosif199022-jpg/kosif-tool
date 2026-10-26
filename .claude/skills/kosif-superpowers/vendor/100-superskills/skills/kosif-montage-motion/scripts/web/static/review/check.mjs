#!/usr/bin/env node
// Motion OS reel.json checker. Catches the mistakes that make the player misbehave (gaps between scenes,
// duplicate ids, boxes off the frame, a video that doesn't match the file) before the user sees them.
//   node check.mjs <project-dir> [--json]
//   node check.mjs --selftest
// Exit code 1 when there are errors; warnings alone exit 0. No dependencies (uses ffprobe when it is on PATH).
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const TYPES = new Set(['text', 'longtext', 'number', 'color', 'media', 'list', 'choice', 'motion']);
const ARABIC = /[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]/;
const TOL = 0.06;  // seconds; about two frames at 30 fps

export function check(reel, {exists = () => true, probe = null} = {}) {
  const err = [], warn = [], E = (m) => err.push(m), W = (m) => warn.push(m);
  const num = (v) => typeof v === 'number' && Number.isFinite(v);
  for (const k of ['id', 'title', 'src']) if (typeof reel[k] !== 'string' || !reel[k]) E(`"${k}" is missing or not a string`);
  for (const k of ['w', 'h', 'fps', 'duration']) if (!num(reel[k]) || reel[k] <= 0) E(`"${k}" must be a positive number`);
  if (reel.version != null && !Number.isInteger(reel.version)) E('"version" must be an integer');
  if (reel.src && !exists(reel.src)) E(`video "${reel.src}" not found next to reel.json`);
  if (reel.live && !exists(reel.live)) E(`live renderer "${reel.live}" not found`);
  if (reel.export && !reel.export.cmd && !reel.export.cmdWin) E('"export" needs a "cmd"');

  const brand = reel.brand || {}, colors = brand.colors || [], fonts = brand.fonts || [];
  if (!reel.brand) E('"brand" is missing (use {"colors": [], "fonts": [], "logo": null})');
  const colorIds = new Set(colors.map((c) => c.id));
  for (const c of colors) if (!/^#[0-9a-f]{6}$/i.test(c.v || '')) E(`brand color "${c.id}" must be #RRGGBB (the color picker needs it), got ${JSON.stringify(c.v)}`);
  for (const f of fonts) if (!f.id || !f.v) E('every brand font needs "id" and "v"');
  if (!reel.audio) E('"audio" is missing (use {"music": null, "bpm": null, "drop": 0, "musicVol": 0.6, "sfxVol": 0.8})');
  else if (reel.audio.bpm && !num(reel.audio.drop)) E('"audio.drop" must be a number when "audio.bpm" is set');
  if (!Array.isArray(reel.assets)) E('"assets" must be an array (can be empty)');
  const assetIds = new Set((reel.assets || []).map((a) => a.id));
  for (const a of reel.assets || []) {
    if (!['image', 'video', 'audio'].includes(a.type)) W(`asset "${a.id}" has type ${JSON.stringify(a.type)}; the player knows image, video, audio`);
    if (a.id && !/^(https?:|up-)/.test(a.id) && !exists(a.id)) W(`asset file "${a.id}" not found`);
  }
  const mediaOk = (v) => v == null || v === 'brand.logo' || assetIds.has(v) || exists(v);

  const scenes = reel.scenes;
  if (!Array.isArray(scenes) || !scenes.length) { E('"scenes" must be a non-empty array'); return {err, warn}; }
  const sids = new Set(), eids = new Set();
  let cursor = 0, hasArabic = false;
  scenes.forEach((s, i) => {
    const at = `scene ${s.id ?? i + 1}`;
    if (!s.id) E(`${at}: missing "id"`); else if (sids.has(s.id)) E(`${at}: duplicate scene id`); else sids.add(s.id);
    if (!Array.isArray(s.t) || s.t.length !== 2 || !s.t.every(num) || s.t[0] >= s.t[1]) { E(`${at}: "t" must be [start, end] with start < end`); return; }
    if (Math.abs(s.t[0] - cursor) > TOL) E(`${at}: starts at ${s.t[0]}s but the previous scene ends at ${cursor}s (scenes must cover the video with no gaps or overlaps)`);
    cursor = s.t[1];
    if (!Array.isArray(s.els)) { E(`${at}: "els" must be an array`); return; }
    for (const e of s.els) {
      const ea = `${at} / ${e.id || '?'}`;
      if (!e.id) E(`${ea}: element missing "id"`); else if (e.id.includes('.')) E(`${ea}: ids can't contain "." (edits are stored as id.prop)`);
      else if (eids.has(e.id)) E(`${ea}: duplicate element id (ids must be unique across the whole reel)`); else eids.add(e.id);
      if (!e.label) W(`${ea}: no "label"; the panel will show an empty name`);
      if (!Array.isArray(e.t) || e.t.length !== 2 || !e.t.every(num) || e.t[0] > e.t[1]) E(`${ea}: "t" must be [in, out]`);
      else if (e.t[0] < s.t[0] - TOL || e.t[1] > s.t[1] + TOL) W(`${ea}: visible ${e.t[0]}-${e.t[1]}s, outside its scene ${s.t[0]}-${s.t[1]}s (it can't be clicked outside the scene)`);
      if (e.box != null) {
        if (!Array.isArray(e.box) || e.box.length !== 4 || !e.box.every(num)) E(`${ea}: "box" must be [x, y, w, h] in % or null`);
        else {
          const [x, y, w, h] = e.box;
          if (w <= 0 || h <= 0) E(`${ea}: box width and height must be > 0`);
          if (x < -1 || y < -1 || x + w > 101 || y + h > 101) W(`${ea}: box ${JSON.stringify(e.box)} reaches off the frame (values are % of the frame, not pixels)`);
        }
      }
      if (!e.props || typeof e.props !== 'object') { E(`${ea}: "props" must be an object (can be empty)`); continue; }
      for (const [k, p] of Object.entries(e.props)) {
        const pa = `${ea}.${k}`;
        if (k.startsWith('@')) E(`${pa}: prop names can't start with "@"`);
        if (!TYPES.has(p.type)) { E(`${pa}: unknown type ${JSON.stringify(p.type)} (use ${[...TYPES].join(', ')})`); continue; }
        if (!('v' in p)) E(`${pa}: missing "v"`);
        if ((p.type === 'text' || p.type === 'longtext') && ARABIC.test(p.v || '')) hasArabic = true;
        if (p.type === 'color' && typeof p.v === 'string' && p.v.startsWith('brand.') && !colorIds.has(p.v.slice(6))) E(`${pa}: "${p.v}" is not a brand color`);
        if (p.type === 'media' && !mediaOk(p.v)) W(`${pa}: media "${p.v}" is not in assets and not a file`);
        if (p.type === 'choice' && (!Array.isArray(p.options) || !p.options.includes(p.v))) E(`${pa}: choice needs "options" containing the current value`);
        if (p.type === 'number' && !num(p.v)) E(`${pa}: number value must be a number`);
        if (p.type === 'list') {
          if (!Array.isArray(p.cols) || !p.cols.length) E(`${pa}: list needs "cols"`);
          if (!Array.isArray(p.v) || !p.v.length) E(`${pa}: list value must be a non-empty array of rows ("+ Add row" copies the last row)`);
          else for (const r of p.v) for (const c of p.cols || []) {
            if (!(c.k in r)) E(`${pa}: a row is missing column "${c.k}"`);
            if (c.type === 'text' && ARABIC.test(r[c.k] || '')) hasArabic = true;
          }
        }
      }
    }
  });
  if (Math.abs(cursor - reel.duration) > TOL) E(`scenes end at ${cursor}s but "duration" is ${reel.duration}s`);
  if (hasArabic && !reel.lang) W('copy is in Arabic but "lang" is not set; add "lang": "ar" so the player opens in Arabic and RTL');
  for (const n of reel.notes || []) if (!num(n.t) || !num(n.x) || !num(n.y)) E('every note needs numeric t, x, y');

  if (probe) {
    // Boxes are % of the frame, so only a different aspect ratio breaks them; a smaller encode of the same shape is fine.
    if (probe.w && (probe.w !== reel.w || probe.h !== reel.h)) (Math.abs(probe.w / probe.h - reel.w / reel.h) > 0.01 ? E : W)(`video is ${probe.w}x${probe.h} but reel.json says ${reel.w}x${reel.h}`);
    if (probe.fps && Math.abs(probe.fps - reel.fps) > 0.05) W(`video runs at ${probe.fps.toFixed(2)} fps but reel.json says ${reel.fps}`);
    if (probe.duration && Math.abs(probe.duration - reel.duration) > 0.25) E(`video is ${probe.duration.toFixed(2)}s long but reel.json says ${reel.duration}s`);
  }
  return {err, warn};
}

function ffprobe(file) {
  try {
    const j = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate:format=duration', '-of', 'json', file], {encoding: 'utf8', windowsHide: true}));
    const s = j.streams?.[0] || {}, [a, b] = String(s.r_frame_rate || '0/1').split('/').map(Number);
    return {w: s.width, h: s.height, fps: b ? a / b : 0, duration: Number(j.format?.duration) || 0};
  } catch { return null; }
}

if (process.argv[2] === '--selftest') {
  const ok = {id: 'x', title: 'X', version: 1, src: 'video.mp4', w: 1080, h: 1920, fps: 30, duration: 4, lang: 'ar',
    brand: {colors: [{id: 'a', name: 'A', v: '#112233'}], fonts: [], logo: null}, audio: {music: null, bpm: null, drop: 0, musicVol: 0.6, sfxVol: 0.8}, assets: [],
    scenes: [{id: 'S1', name: 'One', t: [0, 2], els: [{id: 'h', label: 'H', t: [0, 2], box: [10, 10, 80, 20], props: {text: {type: 'text', label: 'T', v: 'مرحبا'}, c: {type: 'color', label: 'C', v: 'brand.a'}}}]},
      {id: 'S2', name: 'Two', t: [2, 4], els: []}]};
  const r = check(ok);
  if (r.err.length || r.warn.length) throw new Error('clean reel flagged: ' + [...r.err, ...r.warn].join('; '));
  const bad = JSON.parse(JSON.stringify(ok));
  bad.scenes[1].t = [2.5, 4]; bad.scenes[0].els[0].props.c.v = 'brand.zz'; bad.scenes[1].els.push({...bad.scenes[0].els[0]}); delete bad.lang;
  const rb = check(bad, {probe: {w: 1920, h: 1080, fps: 30, duration: 4}});
  for (const want of ['gaps', 'not a brand color', 'duplicate element id', 'reel.json says 1080x1920']) if (!rb.err.some((m) => m.includes(want))) throw new Error('missed: ' + want);
  if (!rb.warn.some((m) => m.includes('"lang"'))) throw new Error('missed: lang hint');
  console.log('selftest ok');
  process.exit(0);
}

const asJson = process.argv.includes('--json');
const dir = path.resolve(process.argv.slice(2).find((a) => !a.startsWith('--')) || '.');
const file = path.join(dir, 'reel.json');
let reel;
try { reel = JSON.parse(fs.readFileSync(file, 'utf8').replace(/^﻿/, '')); }
catch (e) { console.error(`Motion OS check: can't read ${file}: ${e.message}`); process.exit(1); }
const exists = (p) => fs.existsSync(path.resolve(dir, p)) || fs.existsSync(path.resolve(dir, 'public', p));
const probe = reel.src && exists(reel.src) && !reel.live ? ffprobe(path.resolve(dir, reel.src)) : null;
const {err, warn} = check(reel, {exists, probe});
if (asJson) console.log(JSON.stringify({ok: !err.length, errors: err, warnings: warn, probed: !!probe}, null, 1));
else {
  err.forEach((m) => console.log('ERROR  ' + m));
  warn.forEach((m) => console.log('warn   ' + m));
  console.log(err.length ? `\n${err.length} error(s), ${warn.length} warning(s). Fix the errors before opening the player.` : `reel.json OK${warn.length ? ` (${warn.length} warning(s))` : ''}${probe ? '' : ' · video not probed (no ffprobe or live project)'}`);
}
process.exit(err.length ? 1 : 0);
