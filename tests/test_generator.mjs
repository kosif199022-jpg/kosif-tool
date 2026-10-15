import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { buildRequest, cliCommand, defaultsFor, RESOLUTIONS } from '../web/generator.js';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const catalog = JSON.parse(readFileSync(join(ROOT, 'catalog/styles.json'), 'utf8'));
const categories = JSON.parse(readFileSync(join(ROOT, 'catalog/categories.json'), 'utf8'));
const tpl = { ar: readFileSync(join(ROOT, 'templates/claude_request.ar.txt'), 'utf8'), en: readFileSync(join(ROOT, 'templates/claude_request.en.txt'), 'utf8') };

test('templates share the same placeholder set', () => {
  const ph = s => new Set([...s.matchAll(/\{(\w+)\}/g)].map(m => m[1]));
  assert.deepEqual([...ph(tpl.ar)].sort(), [...ph(tpl.en)].sort());
});

test('every record builds a request with no unfilled placeholders in both languages', () => {
  for (const r of catalog) {
    for (const lang of ['ar', 'en']) {
      const text = buildRequest({ template: tpl[lang], record: r, categories, options: { ...defaultsFor(r, null), reqLang: lang }, hasBrief: !!r.brief });
      assert.ok(text.includes(r.id), `${r.id} missing in ${lang}`);
      assert.ok(text.includes(r.page), `${r.id} page missing`);
      assert.equal(text.match(/\{\w+\}/), null, `${r.id} has placeholder in ${lang}`);
      assert.ok(text.includes(RESOLUTIONS[defaultsFor(r, null).aspect]), `${r.id} resolution missing`);
    }
  }
});

test('options are reflected in the output', () => {
  const r = catalog.find(x => x.id === 'pm-ror-fly-9950f1') || catalog[0];
  const text = buildRequest({ template: tpl.en, record: r, categories, options: { reqLang: 'en', source: 'audio', detail: 'voice.mp3', aspect: '9:16', duration: 22, fps: 24, stack: 'remotion', audio: 'music', brand: '#123456', notes: 'keep it calm', lang: 'both' }, hasBrief: true });
  for (const s of ['voice.mp3', '1080x1920', '22 seconds', '24 fps', 'Remotion/React', '-14 LUFS', '#123456', 'keep it calm', 'BRIEF.md', 'Arabic and English']) assert.ok(text.includes(s), `missing ${s}`);
});

test('cli command mirrors the options', () => {
  const r = catalog[0];
  const cmd = cliCommand(r, { reqLang: 'ar', aspect: '1:1', duration: 10, fps: 30, stack: 'canvas', source: 'text', detail: 'script.txt', audio: 'sfx' });
  assert.ok(cmd.startsWith('python3 tools/kosif.py prompt ' + r.id));
  for (const s of ['--aspect 1:1', '--duration 10', '--stack canvas', '"text script.txt"', '--audio sfx']) assert.ok(cmd.includes(s), `missing ${s}`);
});
