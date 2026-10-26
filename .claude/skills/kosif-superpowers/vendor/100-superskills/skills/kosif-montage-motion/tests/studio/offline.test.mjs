// KOSIF Studio offline exporter (v6.1): plans, codec choice and the encode loop with mocked WebCodecs + muxer.
import test from 'node:test';
import assert from 'node:assert/strict';
import { framePlan, audioPlan, pickVideoCodec, pickAudioCodec, mixAudio, encodeOffline, offlineSupported } from '../../scripts/web/static/studio/offline.mjs';

test('framePlan counts frames and timestamps exactly', () => {
  const p = framePlan(8, 30);
  assert.equal(p.frames, 240);
  assert.equal(p.timestampUs(0), 0);
  assert.equal(p.timestampUs(30), 1_000_000);
  assert.equal(framePlan(0.01, 30).frames, 1);
});

test('audioPlan places clip sound on the timeline and the soundtrack from zero', () => {
  const project = { clips: [{ type: 'demo', duration: 2 }, { type: 'video', assetId: 'v', trim: 1.5, duration: 3, volume: 0.8 }, { type: 'video', assetId: 'm', duration: 1, volume: 0 }],
    soundtrack: { assetId: 's', trim: 4, volume: 0.5 } };
  const plan = audioPlan(project);
  assert.equal(plan.total, 6);
  assert.deepEqual(plan.items.map((i) => [i.assetId, i.when, i.offset, i.duration, i.volume]), [['v', 2, 1.5, 3, 0.8], ['s', 0, 4, 6, 0.5]]);
});

test('codec choice falls back across profiles and to Opus', async () => {
  const VE = { isConfigSupported: async (c) => ({ supported: c.codec.startsWith('avc1.42') }) };
  assert.match(await pickVideoCodec(VE, 1280, 720, 30), /^avc1\.42/);
  assert.equal(await pickVideoCodec({ isConfigSupported: async () => ({ supported: false }) }, 1280, 720, 30), null);
  const AE = { isConfigSupported: async (c) => ({ supported: c.codec === 'opus' }) };
  assert.deepEqual(await pickAudioCodec(AE), { codec: 'opus', mux: 'opus' });
  assert.equal(await pickAudioCodec(null), null);
});

test('mixAudio schedules each source once, skips undecodable assets, renders the full length', async () => {
  const started = [];
  class OC {
    constructor(ch, len, sr) { this.len = len; this.sr = sr; this.destination = {}; }
    createBufferSource() { return { connect() {}, start: (...a) => started.push(a) }; }
    createGain() { return { gain: { value: 1 }, connect() {} }; }
    async startRendering() { return { length: this.len, sampleRate: this.sr, duration: this.len / this.sr }; }
  }
  const plan = { total: 4, items: [{ assetId: 'a', when: 0, offset: 0, duration: 4, volume: 1 }, { assetId: 'bad', when: 1, offset: 0, duration: 1, volume: 1 }, { assetId: 'a', when: 2, offset: 9, duration: 1, volume: 1 }] };
  const r = await mixAudio(plan, async (id) => (id === 'a' ? { duration: 5 } : null), 48000, OC);
  assert.equal(r.buffer.length, 192000);
  assert.deepEqual(r.skipped, ['bad']);
  assert.equal(started.length, 1);                       // the second use of 'a' starts past its end
  assert.deepEqual(started[0], [0, 0, 4]);
});

test('encodeOffline drives every frame, keyframes every 2 s, muxes video + audio, honours cancel', async () => {
  const chunks = { video: 0, audio: 0 }, frames = [], keys = [];
  class VE {
    static async isConfigSupported() { return { supported: true }; }
    constructor(o) { this.o = o; this.encodeQueueSize = 0; }
    configure(c) { this.cfg = c; }
    encode(f, opt) { frames.push(f.timestamp); keys.push(!!opt.keyFrame); this.o.output({ type: 'chunk' }, {}); }
    async flush() {} close() {}
  }
  class AE {
    static async isConfigSupported(c) { return { supported: c.codec === 'mp4a.40.2' }; }
    constructor(o) { this.o = o; } configure() {} encode() { this.o.output({}, {}); } async flush() {} close() {}
  }
  class VF { constructor(src, o) { this.timestamp = o.timestamp; } close() {} }
  class AD { constructor(o) { this.o = o; } close() {} }
  const Mp4Muxer = { ArrayBufferTarget: class { constructor() { this.buffer = new ArrayBuffer(16); } },
    Muxer: class { constructor(o) { this.target = o.target; this.opts = o; } addVideoChunk() { chunks.video++; } addAudioChunk() { chunks.audio++; } finalize() { this.done = true; } } };
  const audioBuffer = { sampleRate: 48000, length: 48000, numberOfChannels: 2, getChannelData: () => new Float32Array(48000) };
  let rendered = 0;
  const res = await encodeOffline({ width: 640, height: 360, fps: 30, frames: 90, source: {}, renderFrame: async () => { rendered++; }, audioBuffer,
    VideoEncoder: VE, VideoFrame: VF, AudioEncoder: AE, AudioData: AD, Mp4Muxer });
  assert.equal(rendered, 90); assert.equal(frames.length, 90); assert.equal(chunks.video, 90);
  assert.equal(frames[30], 1_000_000);
  assert.deepEqual(keys.map((k, i) => (k ? i : -1)).filter((i) => i >= 0), [0, 60]);
  assert.equal(res.audio, 'aac'); assert.ok(chunks.audio >= 12);
  assert.equal(res.blob.type, 'video/mp4');
  let n = 0;
  const cancelled = await encodeOffline({ width: 640, height: 360, fps: 30, frames: 90, source: {}, renderFrame: async () => { n++; }, isAlive: () => n < 5,
    VideoEncoder: VE, VideoFrame: VF, Mp4Muxer });
  assert.equal(cancelled, null); assert.equal(n, 5);
  await assert.rejects(encodeOffline({ width: 64, height: 64, fps: 30, frames: 1, source: {}, renderFrame: async () => {}, VideoEncoder: VE, VideoFrame: VF, Mp4Muxer: null }), /mp4-muxer/);
});

test('loudness meter follows BS.1770 and normalisation respects the peak ceiling', async () => {
  const { measureLoudness, normalizeLoudness } = await import('../../scripts/web/static/studio/offline.mjs');
  const sr = 48000, n = sr * 4, sine = (amp, f = 997) => { const s = new Float32Array(n); for (let i = 0; i < n; i++) s[i] = amp * Math.sin(2 * Math.PI * f * i / sr); return s; };
  assert.ok(Math.abs(measureLoudness([sine(1), new Float32Array(n)], sr).lufs - -3.01) < 0.05);   // the standard's calibration
  assert.ok(Math.abs(measureLoudness([sine(1), sine(1)], sr).lufs - 0) < 0.05);
  assert.equal(measureLoudness([new Float32Array(n), new Float32Array(n)], sr).lufs, -Infinity);  // silence is gated out
  const quiet = [sine(0.05), sine(0.05)];
  const r = normalizeLoudness(quiet, sr, -14, -1.5);
  assert.ok(Math.abs(r.after - -14) < 0.01); assert.equal(r.limitedByPeak, false);
  assert.ok(Math.abs(measureLoudness(quiet, sr).lufs - -14) < 0.05);
  const loud = [sine(0.9), sine(0.9)];                                                              // already ~-0.9 LUFS: must go down
  const r2 = normalizeLoudness(loud, sr, -14, -1.5);
  assert.ok(r2.gainDb < -12);
  const crest = [new Float32Array(n), new Float32Array(n)]; crest[0][1000] = 0.5; for (let i = 0; i < n; i++) crest[1][i] = 0.001 * Math.sin(i / 7);
  const r3 = normalizeLoudness(crest, sr, -14, -1.5);                                              // a spike: the peak ceiling wins
  assert.equal(r3.limitedByPeak, true); assert.ok(Math.abs(r3.peakDb - -1.5) < 0.01);
  assert.equal(normalizeLoudness([new Float32Array(10)], sr).gainDb, 0);
});

test('offlineSupported needs VideoEncoder, VideoFrame and the muxer', () => {
  assert.equal(offlineSupported({}), false);
  assert.equal(offlineSupported({ VideoEncoder: function () {}, VideoFrame: function () {}, Mp4Muxer: {} }), true);
});
