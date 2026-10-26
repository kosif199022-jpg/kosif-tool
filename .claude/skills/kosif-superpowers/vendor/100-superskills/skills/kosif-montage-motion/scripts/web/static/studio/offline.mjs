// KOSIF Studio — offline, frame-accurate MP4 export (KOSIF Montage & Motion v6.1).
// Each frame is drawn by the Studio's own draw() after the media are sought to that exact time, then encoded with
// WebCodecs (H.264) and muxed with mp4-muxer; the sound is mixed once with an OfflineAudioContext and encoded as AAC
// (Opus when AAC is unavailable). Nothing here needs requestAnimationFrame, real time or a visible tab, so no frame
// is dropped and a short project renders faster than it plays. Pure helpers are exported for the tests.

export const FPS = 30;

/** Frames of a film: count and the timestamp (µs) of each, from the total seconds. */
export function framePlan(totalSeconds, fps = FPS) {
  const frames = Math.max(1, Math.round(totalSeconds * fps));
  return { frames, fps, frameUs: 1e6 / fps, timestampUs: (i) => Math.round(i * 1e6 / fps) };
}

/** What sounds play when: the video clips' own sound at their place on the timeline, and the soundtrack from 0. */
export function audioPlan(project) {
  const out = [];
  let start = 0;
  for (const c of project.clips || []) {
    if (c.type === 'video' && c.assetId && (c.volume ?? 1) > 0) out.push({ assetId: c.assetId, when: start, offset: c.trim || 0, duration: c.duration, volume: c.volume ?? 1, kind: 'clip' });
    start += c.duration;
  }
  const st = project.soundtrack;
  if (st && st.assetId && (st.volume ?? 0.6) > 0) out.push({ assetId: st.assetId, when: 0, offset: st.trim || 0, duration: start, volume: st.volume ?? 0.6, kind: 'soundtrack' });
  return { items: out, total: start };
}

/** Integrated loudness (LUFS) per ITU-R BS.1770-4: K-weighting (48 kHz coefficients; other rates are resampled
 *  conceptually by recomputing the filters), 400 ms blocks every 100 ms, −70 LUFS absolute gate, −10 LU relative gate.
 *  channels: Float32Array[] (L, R …, each weighted 1.0). Returns {lufs, samplePeak} (−Infinity for silence). */
export function measureLoudness(channels, sampleRate = 48000) {
  const [shelfB, hpB, shelfA] = kWeights(sampleRate), hpA = kHighPassA(sampleRate);
  const n = channels[0]?.length || 0;
  const block = Math.round(0.4 * sampleRate), hop = Math.round(0.1 * sampleRate);
  let peak = 0;
  const weighted = channels.map((x) => {
    const y = biquad(biquad(x, shelfB, shelfA), hpB, hpA);
    for (let i = 0; i < x.length; i++) { const v = Math.abs(x[i]); if (v > peak) peak = v; }
    return y;
  });
  const blocks = [];
  for (let s = 0; s + block <= n; s += hop) {
    let z = 0;
    for (const y of weighted) { let acc = 0; for (let i = s; i < s + block; i++) acc += y[i] * y[i]; z += acc / block; }
    blocks.push(z);
  }
  if (!blocks.length) return { lufs: -Infinity, samplePeak: peak };
  const L = (z) => -0.691 + 10 * Math.log10(z);
  const abs = blocks.filter((z) => z > 0 && L(z) > -70);
  if (!abs.length) return { lufs: -Infinity, samplePeak: peak };
  const rel = L(abs.reduce((a, b) => a + b, 0) / abs.length) - 10;
  const gated = abs.filter((z) => L(z) > rel);
  return { lufs: L(gated.reduce((a, b) => a + b, 0) / gated.length), samplePeak: peak };
}

/** Bring a buffer to `target` LUFS without letting the sample peak pass `ceilingDb` dBFS (gain is the smaller of the
 *  two); modifies the channels in place and reports what was reached. Not a true-peak limiter: the margin below the
 *  −1 dBTP delivery ceiling absorbs encoder overshoot. */
export function normalizeLoudness(channels, sampleRate = 48000, target = -14, ceilingDb = -1.5) {
  const before = measureLoudness(channels, sampleRate);
  if (!Number.isFinite(before.lufs) || before.samplePeak <= 0) return { before: before.lufs, after: before.lufs, gainDb: 0, peakDb: -Infinity, limitedByPeak: false };
  const wantDb = target - before.lufs;
  const peakDb = 20 * Math.log10(before.samplePeak);
  const gainDb = Math.min(wantDb, ceilingDb - peakDb);
  const g = 10 ** (gainDb / 20);
  for (const x of channels) for (let i = 0; i < x.length; i++) x[i] *= g;
  return { before: before.lufs, after: before.lufs + gainDb, gainDb, peakDb: peakDb + gainDb, limitedByPeak: gainDb < wantDb - 1e-9 };
}

function kWeights(sr) {
  // BS.1770 stage 1 (high shelf, +4 dB above ~1.5 kHz) designed at sr with the standard analog prototype.
  const f0 = 1681.974450955533, G = 3.999843853973347, Q = 0.7071752369554196;
  const K = Math.tan(Math.PI * f0 / sr), Vh = 10 ** (G / 20), Vb = Vh ** 0.4996667741545416;
  const a0 = 1 + K / Q + K * K;
  const b = [(Vh + Vb * K / Q + K * K) / a0, 2 * (K * K - Vh) / a0, (Vh - Vb * K / Q + K * K) / a0];
  const a = [2 * (K * K - 1) / a0, (1 - K / Q + K * K) / a0];
  return [b, [1, -2, 1], a];
}
function kHighPassA(sr) {
  // BS.1770 stage 2 (RLB high-pass, ~38 Hz).
  const f0 = 38.13547087602444, Q = 0.5003270373238773, K = Math.tan(Math.PI * f0 / sr);
  const d = 1 + K / Q + K * K;
  return [2 * (K * K - 1) / d, (1 - K / Q + K * K) / d];
}
function biquad(x, b, a) {
  const y = new Float32Array(x.length);
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  for (let i = 0; i < x.length; i++) {
    const v = b[0] * x[i] + b[1] * x1 + b[2] * x2 - a[0] * y1 - a[1] * y2;
    x2 = x1; x1 = x[i]; y2 = y1; y1 = v; y[i] = v;
  }
  return y;
}

/** The first H.264 profile this browser can encode at this size and rate (High → Main → Baseline). */
export async function pickVideoCodec(VideoEncoderImpl, width, height, fps) {
  const level = width * height > 1280 * 720 || fps > 30 ? '2A' : '1F';
  for (const codec of [`avc1.6400${level}`, `avc1.4D40${level}`, `avc1.42E0${level}`, 'avc1.42E01F']) {
    try {
      const r = await VideoEncoderImpl.isConfigSupported({ codec, width, height, bitrate: 8_000_000, framerate: fps, avc: { format: 'avc' } });
      if (r?.supported) return codec;
    } catch { /* try the next profile */ }
  }
  return null;
}

/** AAC when the browser can encode it, else Opus; null when neither (the film is then silent and the report says so). */
export async function pickAudioCodec(AudioEncoderImpl, sampleRate = 48000, channels = 2) {
  if (!AudioEncoderImpl) return null;
  for (const [codec, mux] of [['mp4a.40.2', 'aac'], ['opus', 'opus']]) {
    try {
      const r = await AudioEncoderImpl.isConfigSupported({ codec, sampleRate, numberOfChannels: channels, bitrate: 192000 });
      if (r?.supported) return { codec, mux };
    } catch { /* next */ }
  }
  return null;
}

/** Mix the plan into one stereo buffer (OfflineAudioContext: exact, not real time). decode(assetId) → AudioBuffer|null. */
export async function mixAudio(plan, decode, sampleRate, OfflineCtx) {
  if (!plan.items.length || !OfflineCtx) return { buffer: null, skipped: [] };
  const length = Math.max(1, Math.ceil(plan.total * sampleRate));
  const ctx = new OfflineCtx(2, length, sampleRate);
  const skipped = [];
  const cache = new Map();
  for (const it of plan.items) {
    let buf = cache.get(it.assetId);
    if (buf === undefined) { try { buf = await decode(it.assetId); } catch { buf = null; } cache.set(it.assetId, buf); }
    if (!buf) { skipped.push(it.assetId); continue; }
    if (it.offset >= buf.duration) continue;
    const src = ctx.createBufferSource(); src.buffer = buf;
    const gain = ctx.createGain(); gain.gain.value = it.volume;
    src.connect(gain); gain.connect(ctx.destination);
    src.start(it.when, it.offset, Math.min(it.duration, buf.duration - it.offset));
  }
  return { buffer: await ctx.startRendering(), skipped };
}

/** Encode frames (+ an optional AudioBuffer) into an MP4 Blob. renderFrame(i) must leave the picture on `source`. */
export async function encodeOffline(o) {
  const { width, height, fps, frames, source, renderFrame, audioBuffer, onProgress = () => {}, isAlive = () => true } = o;
  const VE = o.VideoEncoder ?? globalThis.VideoEncoder, VF = o.VideoFrame ?? globalThis.VideoFrame;
  const AE = o.AudioEncoder ?? globalThis.AudioEncoder, AD = o.AudioData ?? globalThis.AudioData;
  const M = o.Mp4Muxer ?? globalThis.Mp4Muxer;
  if (!VE || !VF) throw new Error('هذا المتصفح لا يدعم WebCodecs (VideoEncoder)');
  if (!M) throw new Error('مكتبة mp4-muxer غير محمّلة');
  const vcodec = await pickVideoCodec(VE, width, height, fps);
  if (!vcodec) throw new Error(`لا يوجد ترميز H.264 مدعوم لمقاس ${width}×${height}`);
  const acodec = audioBuffer ? await pickAudioCodec(AE, audioBuffer.sampleRate, 2) : null;
  const muxer = new M.Muxer({
    target: new M.ArrayBufferTarget(),
    video: { codec: 'avc', width, height, frameRate: fps },
    ...(acodec ? { audio: { codec: acodec.mux, numberOfChannels: 2, sampleRate: audioBuffer.sampleRate } } : {}),
    fastStart: 'in-memory', firstTimestampBehavior: 'offset',
  });
  let failure = null;
  const venc = new VE({ output: (chunk, meta) => muxer.addVideoChunk(chunk, meta), error: (e) => { failure = e; } });
  venc.configure({ codec: vcodec, width, height, bitrate: Math.min(16_000_000, Math.round(width * height * fps * 0.15)), framerate: fps, avc: { format: 'avc' }, latencyMode: 'quality' });
  const frameUs = 1e6 / fps;
  for (let i = 0; i < frames; i++) {
    if (!isAlive()) { try { venc.close(); } catch { /* closed */ } return null; }
    if (failure) throw failure;
    await renderFrame(i);
    const vf = new VF(source, { timestamp: Math.round(i * frameUs), duration: Math.round(frameUs) });
    venc.encode(vf, { keyFrame: i % (fps * 2) === 0 });
    vf.close();
    while (venc.encodeQueueSize > 8) await new Promise((r) => setTimeout(r, 2));
    onProgress((i + 1) / frames, i + 1);
  }
  await venc.flush(); venc.close();
  if (failure) throw failure;
  let audioNote = audioBuffer ? (acodec ? acodec.mux : 'no-encoder') : 'none';
  if (acodec) {
    let aerr = null;
    const aenc = new AE({ output: (chunk, meta) => muxer.addAudioChunk(chunk, meta), error: (e) => { aerr = e; } });
    aenc.configure({ codec: acodec.codec, sampleRate: audioBuffer.sampleRate, numberOfChannels: 2, bitrate: 192000 });
    const sr = audioBuffer.sampleRate, n = audioBuffer.length, block = 4096;
    const L = audioBuffer.getChannelData(0), R = audioBuffer.numberOfChannels > 1 ? audioBuffer.getChannelData(1) : L;
    for (let p = 0; p < n; p += block) {
      if (!isAlive()) { try { aenc.close(); } catch { /* closed */ } return null; }
      const len = Math.min(block, n - p), data = new Float32Array(len * 2);
      data.set(L.subarray(p, p + len), 0); data.set(R.subarray(p, p + len), len);
      const ad = new AD({ format: 'f32-planar', sampleRate: sr, numberOfFrames: len, numberOfChannels: 2, timestamp: Math.round(p * 1e6 / sr), data });
      aenc.encode(ad); ad.close();
    }
    await aenc.flush(); aenc.close();
    if (aerr) { audioNote = 'failed'; throw aerr; }
  }
  muxer.finalize();
  const blob = new Blob([muxer.target.buffer], { type: 'video/mp4' });
  return { blob, videoCodec: vcodec, audio: audioNote, frames, fps, width, height };
}

/** Is an offline export possible in this browser at all? */
export function offlineSupported(g = globalThis) {
  return typeof g.VideoEncoder === 'function' && typeof g.VideoFrame === 'function' && !!g.Mp4Muxer;
}
