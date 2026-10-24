// Copy to lyrics.js and fill with the song's lines (kept local: derived from another account's audio).
// p = panel 0-5, y = baseline, size = max font px (auto-shrinks to 900 px wide), c = pink|cyan|warm|violet|green|white,
// font = kufi (Marhey, default) | ruqaa, w = [[word, start seconds, 'strike'|'fail'?]], final = stays lit at the end.
// Regenerate timing: python3 .claude/skills/kosif-superpowers/scripts/montage_pro.py transcribe <audio> --out words.json
window.LYRICS = {
  duration: 45.533, audio: 'audio.m4a',
  env30: [], // per-frame loudness 0..1 at 30 fps (optional; drives the glow pulse)
  lines: [
    { p: 0, y: 880, size: 112, c: 'warm', w: [['كلمة', 0.1], ['كلمة', 0.8]] },
    { p: 5, y: 1330, size: 210, font: 'ruqaa', c: 'pink', final: true, w: [['كلمة', 43.8]] },
  ],
};
