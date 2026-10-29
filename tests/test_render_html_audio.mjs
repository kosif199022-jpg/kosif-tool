// tools/render_html.cjs audio proof: the packet MD5 of a stream-copied --audio track against the
// output's, the audio_md5= token of the VERIFY line and the stderr explanation. The pure helpers need
// nothing; the encode tests need only ffmpeg/ffprobe (synthetic PNG frames and synthetic tones, no
// browser, no network) and skip without them. The last test runs the real CLI and skips unless
// Playwright and its Chromium are installed.
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const SCRIPT = join(ROOT, 'tools', 'render_html.cjs');
const require = createRequire(import.meta.url);
const R = require(SCRIPT);

const HASH = (c) => c.repeat(32);
const pk = (hash, pts = 0, duration = 1024, size = 300) => ({ hash, pts, duration, size });
const set = (md5, hashes, tb = [1, 48000]) => ({ md5, tb, packets: hashes.map((h, i) => pk(h, (i - 1) * 1024)) });

// ------------------------------------------------------------------ pure helpers

test('hash commands: first audio stream, stream copy, aac_adtstoasc for AAC only (as verify_video.py)', () => {
  assert.deepEqual(R.audioHashArgs('in.m4a', 'aac', 'md5'),
    ['-hide_banner', '-v', 'error', '-nostdin', '-i', 'in.m4a', '-map', '0:a:0', '-c', 'copy', '-bsf:a', 'aac_adtstoasc', '-f', 'md5', '-']);
  for (const codec of ['mp3', 'alac', null]) {
    const a = R.audioHashArgs('in.x', codec, 'framemd5');
    assert.ok(!a.includes('-bsf:a'), String(codec));
    assert.deepEqual(a.slice(-3), ['-f', 'framemd5', '-']);
  }
  const py = fs.readFileSync(join(ROOT, 'tools', 'verify_video.py'), 'utf8');
  assert.match(py, /"-map", "0:a:0", "-c", "copy", \*bsf, "-f", "md5"/, 'same hash recipe as verify_video.py --source-audio');
});

test('md5 and framemd5 output parsing (side data columns and headers ignored)', () => {
  assert.equal(R.parseMd5('MD5=46c8225519cd0e6cf62e96f75e74077f\n'), '46c8225519cd0e6cf62e96f75e74077f');
  assert.equal(R.parseMd5('garbage'), null);
  assert.equal(R.parseMd5(undefined), null);
  const text = [
    '#format: frame checksums', '#version: 2', '#hash: MD5',
    '#extradata 0,                               5, ff45c3a76898cdd565877d2f8752846e',
    '#tb 0: 1/44100', '#media_type 0: audio', '#codec_id 0: aac',
    '#stream#, dts,        pts, duration,     size, hash',
    '0,      -1024,      -1024,     1024,      477, 4a10b195d289c1d17df02f21bc3c339f, S=1,       10, f00904fd87b64e6bede38cfd77615dfc',
    '0,          0,          0,     1024,      380, 0123456789abcdef0123456789abcdef',
    '0,       1024,       1024,      512,      200, fedcba9876543210fedcba9876543210',
    '1,          0,          0,        1,        9, 0123456789abcdef0123456789abcdef',
    '',
  ].join('\n');
  const parsed = R.parseFrameMd5(text);
  assert.deepEqual(parsed.tb, [1, 44100]);
  assert.equal(parsed.packets.length, 3, 'stream 1 lines are not the audio stream');
  assert.deepEqual(parsed.packets[0], { pts: -1024, duration: 1024, size: 477, hash: '4a10b195d289c1d17df02f21bc3c339f' });
  assert.equal(R.packetsEndSeconds(parsed), 0.035); // (1024 + 512) / 44100
  assert.equal(R.packetsEndSeconds({ tb: null, packets: parsed.packets }), null);
  assert.equal(R.packetsEndSeconds({ tb: [1, 44100], packets: [] }), null);
});

test('compare: identical packets match', () => {
  const p = R.compareAudioPackets(set(HASH('a'), [HASH('1'), HASH('2')]), set(HASH('a'), [HASH('1'), HASH('2')]));
  assert.equal(p.verdict, 'match');
  assert.equal(p.relation, 'identical');
  assert.deepEqual([p.src_packets, p.out_packets, p.offset, p.cut_before, p.cut_after], [2, 2, 0, 0, 0]);
  assert.equal(R.audioMd5Token(p), 'match');
  assert.deepEqual(R.audioProofWarning(p), [], 'a match prints no warning');
});

test('compare: the output is the first M source packets (cut at the last video frame)', () => {
  const src = set(HASH('a'), ['1', '2', '3', '4', '5'].map(HASH));
  const out = set(HASH('b'), ['1', '2', '3'].map(HASH));
  const p = R.compareAudioPackets(src, out);
  assert.deepEqual([p.verdict, p.relation, p.offset, p.cut_before, p.cut_after], ['differs', 'prefix', 0, 0, 2]);
  assert.equal(R.audioMd5Token(p), 'differs (src 5 packets, out 3 packets)');
  const w = R.audioProofWarning(p, { source: '/v/voice.m4a', output: '/o/film.mp4', filmSeconds: 0.05 });
  assert.match(w[0], /^AUDIO NOT BYTE-IDENTICAL TO THE SOURCE: audio_md5=differs \(src 5 packets, out 3 packets\)$/);
  assert.match(w[1], /source md5 a{32} \(5 packets, ends at 0\.085s\): \/v\/voice\.m4a/);
  assert.match(w[2], /output md5 b{32} \(3 packets, ends at 0\.043s\): \/o\/film\.mp4/);
  assert.match(w.join('\n'), /byte-identical to source packets 1-3: nothing was re-encoded, packets were only cut/);
  assert.match(w.join('\n'), /cut: 2 packets after the last video frame \(the film is 0\.05s, the source audio ends at 0\.085s\)\. This trim is allowed/);
  assert.match(w.join('\n'), /never fails it/);
  assert.match(w.join('\n'), /-shortest drops the last packet/);
});

test('compare: a contiguous run from packet k (--start cut the head as well)', () => {
  const src = set(HASH('a'), ['1', '2', '3', '4', '5', '6'].map(HASH));
  const p = R.compareAudioPackets(src, set(HASH('b'), ['3', '4', '5'].map(HASH)));
  assert.deepEqual([p.relation, p.offset, p.cut_before, p.cut_after], ['run', 2, 2, 1]);
  const w = R.audioProofWarning(p, { start: 0.5, filmSeconds: 1 }).join('\n');
  assert.match(w, /source packets 3-5/);
  assert.match(w, /cut: 2 packets before --start 0\.5s and 1 packet after the last video frame/);
  const w0 = R.audioProofWarning(R.compareAudioPackets(src, set(HASH('b'), ['2', '3', '4', '5', '6'].map(HASH)))).join('\n');
  assert.match(w0, /cut: 1 packet before the first video frame\./, 'without --start the head cut is named by the frame');
});

test('compare: changed bytes are named, not explained away as a trim', () => {
  const src = set(HASH('a'), ['1', '2', '3', '4'].map(HASH));
  let p = R.compareAudioPackets(src, set(HASH('b'), ['1', '2', 'x', '4'].map(HASH)));
  assert.deepEqual([p.verdict, p.relation, p.offset, p.first_mismatch], ['differs', 'changed', 0, 2]);
  assert.equal(R.audioMd5Token(p), 'differs (src 4 packets, out 4 packets)');
  let w = R.audioProofWarning(p).join('\n');
  assert.match(w, /output packet 3 differs from source packet 3: the audio BYTES CHANGED, not just cut/);
  assert.match(w, /re-render from the untouched source file/);
  assert.doesNotMatch(w, /This trim is allowed/);
  p = R.compareAudioPackets(src, set(HASH('b'), ['y', 'z'].map(HASH))); // a re-encode: nothing lines up
  assert.deepEqual([p.relation, p.offset, p.first_mismatch], ['changed', 0, 0]);
  p = R.compareAudioPackets(src, set(HASH('b'), []));
  assert.equal(p.relation, 'changed');
  assert.equal(R.audioMd5Token(p), 'differs (src 4 packets, out 0 packets)');
  assert.match(R.audioProofWarning(p).join('\n'), /do not line up with the source/);
  // equal MD5 but a different packet count is not called a match
  assert.equal(R.compareAudioPackets(set(HASH('a'), [HASH('1')]), set(HASH('a'), [HASH('1'), HASH('2')])).verdict, 'differs');
});

test('audio_md5 tokens and the VERIFY line (token before file=, which may hold spaces)', () => {
  assert.equal(R.audioMd5Token(null), 'none');
  assert.equal(R.audioMd5Token({ verdict: 'none' }), 'none');
  assert.equal(R.audioMd5Token({ verdict: 'reencoded' }), 'reencoded');
  assert.equal(R.audioMd5Token({ verdict: 'unknown', reason: 'ffmpeg could not hash' }), 'unknown (ffmpeg could not hash)');
  const probe = { duration: 12, fps: 30, frames: 360, width: 1080, height: 1920, audio: true, audioCodec: 'aac' };
  assert.equal(R.verifyLine({ problems: [], probe, audioMd5: 'match', out: '/x/my film.mp4' }),
    'VERIFY OK duration=12.000s fps=30 frames=360 size=1080x1920 audio=aac audio_md5=match file=/x/my film.mp4');
  assert.equal(R.verifyLine({ problems: ['fps'], probe: { ...probe, audio: false }, audioMd5: 'none', out: 'o.mp4' }),
    'VERIFY FAIL duration=12.000s fps=30 frames=360 size=1080x1920 audio=none audio_md5=none file=o.mp4');
  assert.match(R.verifyLine({ problems: [], probe, audioMd5: 'differs (src 470 packets, out 469 packets)', out: 'o.mp4' }),
    / audio_md5=differs \(src 470 packets, out 469 packets\) file=o\.mp4$/);
});

test('proveAudio: no audio, a re-encoded track and a failed hash never throw', () => {
  assert.deepEqual(R.proveAudio({ audioInfo: null }), { verdict: 'none' });
  assert.deepEqual(R.proveAudio({ audioInfo: { handling: 'reencoded', codec: 'pcm_s16le' } }),
    { verdict: 'reencoded', codec_in: 'pcm_s16le', codec_out: 'aac' });
  assert.ok(R.MP4_COPY_AUDIO.has('aac') && R.MP4_COPY_AUDIO.has('mp3') && R.MP4_COPY_AUDIO.has('alac'));
});

// ------------------------------------------------- real encodes (ffmpeg only)

const HAVE_FFMPEG = ['ffmpeg', 'ffprobe'].every((b) => {
  const r = spawnSync(b, ['-version'], { encoding: 'utf8' });
  return !r.error && r.status === 0;
});
const ff = (args) => {
  const r = spawnSync('ffmpeg', ['-hide_banner', '-v', 'error', '-y', ...args], { encoding: 'utf8' });
  assert.equal(r.status, 0, `ffmpeg ${args.join(' ')}\n${r.stderr}`);
};

function workDir(t) {
  const dir = fs.mkdtempSync(join(os.tmpdir(), 'kosif-audio-test-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return dir;
}

// 30 PNG frames (1 s at 30 fps) named as the renderer writes them, and tones of the given lengths.
function fixture(t) {
  const dir = workDir(t);
  const frames = join(dir, 'frames');
  fs.mkdirSync(frames);
  ff(['-f', 'lavfi', '-i', 'testsrc=s=64x64:r=30:d=1', '-start_number', '0', join(frames, 'frame_%06d.png')]);
  const tone = (name, seconds, codecArgs) => {
    const file = join(dir, name);
    ff(['-f', 'lavfi', '-i', `sine=f=330:d=${seconds}:sample_rate=48000`, ...codecArgs, file]);
    return file;
  };
  return { dir, frames, tone };
}

function encode(fx, audio, { start = 0, name = 'film.mp4' } = {}) {
  const out = join(fx.dir, name);
  const enc = R.encodeVideo({ framesDir: fx.frames, frames: 30, fps: 30, out, crf: 17, audio, start, width: 64, height: 64, capWidth: 64, capHeight: 64 });
  return { out, enc, proof: R.proveAudio({ audioInfo: enc.audio, source: audio, output: out }) };
}

const AAC = ['-c:a', 'aac', '-b:a', '128k'];

test('a stream-copied AAC voice shorter than the film: audio_md5=match', { skip: !HAVE_FFMPEG && 'needs ffmpeg/ffprobe' }, (t) => {
  const fx = fixture(t);
  const { enc, proof } = encode(fx, fx.tone('short.m4a', 0.8, AAC));
  assert.deepEqual(enc.audio, { handling: 'copy', codec: 'aac' });
  assert.equal(proof.verdict, 'match', JSON.stringify(proof));
  assert.equal(proof.src_md5, proof.out_md5);
  assert.ok(proof.src_packets > 30);
  assert.equal(R.audioMd5Token(proof), 'match');
});

test('a voice longer than the film is cut at the last video frame: differs, every kept packet identical', { skip: !HAVE_FFMPEG && 'needs ffmpeg/ffprobe' }, (t) => {
  const fx = fixture(t);
  const { proof } = encode(fx, fx.tone('long.m4a', 1.5, AAC));
  assert.equal(proof.verdict, 'differs');
  assert.equal(proof.relation, 'prefix');
  assert.ok(proof.cut_after > 0 && proof.out_packets < proof.src_packets);
  assert.equal(proof.src_packets, proof.out_packets + proof.cut_after);
  assert.equal(R.audioMd5Token(proof), `differs (src ${proof.src_packets} packets, out ${proof.out_packets} packets)`);
  assert.match(R.audioProofWarning(proof, { filmSeconds: 1 }).join('\n'), /packets after the last video frame \(the film is 1s/);
});

test('--start cuts the head too: the kept packets are one contiguous run of the source', { skip: !HAVE_FFMPEG && 'needs ffmpeg/ffprobe' }, (t) => {
  const fx = fixture(t);
  const { proof } = encode(fx, fx.tone('long.m4a', 2, AAC), { start: 0.5 });
  assert.equal(proof.verdict, 'differs');
  assert.equal(proof.relation, 'run', JSON.stringify(proof));
  assert.ok(proof.cut_before > 0 && proof.cut_after > 0);
});

test('re-muxing the delivery with -shortest drops packets and re-encoding changes them: both are caught', { skip: !HAVE_FFMPEG && 'needs ffmpeg/ffprobe' }, (t) => {
  const fx = fixture(t);
  const voice = fx.tone('voice.m4a', 1.03, AAC);
  const video = encode(fx, null, { name: 'video_only.mp4' }).out;
  const remux = join(fx.dir, 'remux.mp4');
  ff(['-i', video, '-i', voice, '-map', '0:v', '-map', '1:a', '-c', 'copy', '-shortest', remux]);
  const hashes = (f) => R.audioPacketHashes(f, 'aac');
  let p = R.compareAudioPackets(hashes(voice), hashes(remux));
  assert.equal(p.verdict, 'differs', 'the -shortest re-mux is not byte-identical');
  assert.equal(p.relation, 'prefix');
  const reenc = join(fx.dir, 'reencoded.mp4');
  ff(['-i', video, '-i', voice, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '96k', reenc]);
  p = R.compareAudioPackets(hashes(voice), hashes(reenc));
  assert.equal(p.verdict, 'differs');
  assert.equal(p.relation, 'changed');
  assert.match(R.audioProofWarning(p).join('\n'), /BYTES CHANGED/);
});

test('raw ADTS .aac and MP3 are compared as the MP4 carries them; WAV says reencoded', { skip: !HAVE_FFMPEG && 'needs ffmpeg/ffprobe' }, (t) => {
  const fx = fixture(t);
  const adts = join(fx.dir, 'voice.aac');
  ff(['-i', fx.tone('src.m4a', 0.8, AAC), '-c', 'copy', '-f', 'adts', adts]);
  let r = encode(fx, adts, { name: 'adts.mp4' });
  assert.equal(r.proof.verdict, 'match', `the 7-byte ADTS headers the MP4 mux strips are not a difference: ${JSON.stringify(r.proof)}`);
  const mp3 = fx.tone('voice.mp3', 0.8, ['-c:a', 'libmp3lame', '-b:a', '128k']);
  r = encode(fx, mp3, { name: 'mp3.mp4' });
  assert.deepEqual(r.enc.audio, { handling: 'copy', codec: 'mp3' });
  assert.equal(r.proof.verdict, 'match', JSON.stringify(r.proof));
  r = encode(fx, fx.tone('voice.wav', 0.8, ['-c:a', 'pcm_s16le']), { name: 'wav.mp4' });
  assert.deepEqual(r.enc.audio, { handling: 'reencoded', codec: 'pcm_s16le' });
  assert.equal(R.audioMd5Token(r.proof), 'reencoded');
});

test("the skill's bundled copy encodes and proves the same way (resources/motion-runtime/render_html.cjs)", { skip: !HAVE_FFMPEG && 'needs ffmpeg/ffprobe' }, (t) => {
  const S = require(join(ROOT, '.claude', 'skills', 'kosif-superpowers', 'resources', 'motion-runtime', 'render_html.cjs'));
  assert.notEqual(S, R, 'a separate module instance');
  const fx = fixture(t);
  const voice = fx.tone('voice.m4a', 1.5, AAC);
  const out = join(fx.dir, 'skill.mp4');
  const enc = S.encodeVideo({ framesDir: fx.frames, frames: 30, fps: 30, out, crf: 17, audio: voice, start: 0, width: 64, height: 64, capWidth: 64, capHeight: 64 });
  const proof = S.proveAudio({ audioInfo: enc.audio, source: voice, output: out });
  assert.deepEqual([proof.verdict, proof.relation], ['differs', 'prefix']);
  assert.equal(S.audioMd5Token(proof), `differs (src ${proof.src_packets} packets, out ${proof.out_packets} packets)`);
  assert.deepEqual(S.probeVideo(out).frames, 30);
});

test('an unreadable source gives audio_md5=unknown with the reason, never an exception', { skip: !HAVE_FFMPEG && 'needs ffmpeg/ffprobe' }, (t) => {
  const dir = workDir(t);
  const bad = join(dir, 'not-audio.m4a');
  fs.writeFileSync(bad, 'not an audio file');
  const p = R.proveAudio({ audioInfo: { handling: 'copy', codec: 'aac' }, source: bad, output: bad });
  assert.equal(p.verdict, 'unknown');
  assert.match(R.audioMd5Token(p), /^unknown \(ffmpeg could not hash the audio packets of .*not-audio\.m4a/);
});

// ------------------------------------------- the real CLI (Playwright + Chromium)

function chromiumReady() {
  for (const spec of [() => require.resolve('playwright', { paths: [ROOT] }), () => '/opt/node-tools/node_modules/playwright', () => process.env.KOSIF_PLAYWRIGHT]) {
    try {
      const s = spec();
      if (!s) continue;
      const pw = require(s);
      if (pw.chromium && fs.existsSync(pw.chromium.executablePath())) return true;
    } catch (e) { /* try the next one */ }
  }
  return false;
}
const CAN_RENDER = HAVE_FFMPEG && chromiumReady();

test('CLI: a render prints audio_md5 in VERIFY and writes it to --report', { skip: !CAN_RENDER && 'needs Playwright Chromium and ffmpeg' }, (t) => {
  const fx = fixture(t);
  const voice = fx.tone('voice.m4a', 0.6, AAC);
  const out = join(fx.dir, 'film.mp4');
  const report = join(fx.dir, 'report.json');
  const r = spawnSync(process.execPath, [SCRIPT, '--in', join(ROOT, 'starters', 'html-canvas', 'index.html'), '--out', out,
    '--width', '128', '--height', '228', '--duration', '0.5', '--offline', '--audio', voice, '--report', report], { cwd: ROOT, encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
  assert.match(r.stdout, /^VERIFY OK duration=0\.500s fps=30 frames=15 size=128x228 audio=aac audio_md5=differs \(src \d+ packets, out \d+ packets\) file=/m);
  assert.match(r.stderr, /AUDIO NOT BYTE-IDENTICAL TO THE SOURCE/);
  assert.match(r.stderr, /This trim is allowed/);
  const rep = JSON.parse(fs.readFileSync(report, 'utf8'));
  assert.equal(rep.mode, 'render');
  assert.equal(rep.verify.ok, true);
  assert.match(rep.audio_md5, /^differs \(src \d+ packets, out \d+ packets\)$/);
  assert.equal(rep.audio.handling, 'copy');
  assert.equal(rep.audio.proof.relation, 'prefix');
  assert.ok(rep.verify_line.includes(`audio_md5=${rep.audio_md5} file=`));
});
