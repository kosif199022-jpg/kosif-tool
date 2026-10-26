# The timeline spec (v6) — `kmotion timeline SPEC.json --out film.mp4`

One JSON file is the whole edit. The same spec and sources give the same film. `kmotion timeline --example edit.json`
writes a starting point; `kmotion transitions` lists what this FFmpeg build offers (57 here).

```json
{
  "size": "1080x1920",            // or "ratio": "9:16" | "16:9" | "1:1" | "4:5" | "4:3" | "21:9"
  "fps": 30, "background": "#0d1b2a",
  "clips": [
    {"src": "a.mp4", "in": 2.0, "out": 6.5, "speed": 1.0, "fit": "cover", "grade": "teal_orange",
     "zoom": {"from": 1.0, "to": 1.08}, "volume": 1.0, "mute": false,
     "transition": {"type": "circleopen", "dur": 0.6}},
    {"src": "b.mp4", "in": 0, "out": 4, "ramp": [[0, 1.0], [1.5, 0.25], [3.0, 1.0]], "interpolate": false},
    {"image": "photo.jpg", "dur": 3, "zoom": {"from": 1.0, "to": 1.15}},
    {"color": "#000000", "dur": 0.8}
  ],
  "overlays": [
    {"type": "text", "text": "عنوان\nسطر ثانٍ", "start": 0.5, "end": 3.5, "pos": "center", "size": 96, "color": "#ffffff",
     "box": "#00000099", "stroke": 6, "anim": "rise", "align": "center", "font": "optional path"},
    {"type": "lower-third", "title": "محمود", "sub": "مخرج", "start": 4, "end": 8, "accent": "#E7B65A"},
    {"type": "image", "src": "logo.png", "start": 0, "end": 12, "pos": "upper-right", "scale": 0.22, "anim": "fade"},
    {"type": "progress", "color": "#E7B65A", "height": 10, "from": "right", "y": "bottom"},
    {"type": "captions", "spec": "caps.json", "style": "tiktok", "max_words": 4}
  ],
  "audio": {"music": {"src": "track.mp3", "gain": -6, "start": 0, "fade_in": 1.0, "fade_out": 2.0, "loop": true},
            "voice": {"src": "vo.wav", "start": 0.5, "gain": 0},
            "keep_clip_audio": true, "duck": "auto", "lufs": -14}
}
```

## Clips
- `src` (video) with `in`/`out` seconds; `image` + `dur`; `color` + `dur`. Paths resolve against the spec's folder.
- `fit`: `cover` (fill + crop) · `contain` (letterbox on `background`) · `blur` (blurred copy behind).
- `speed` 0.1–10 (audio kept, pitch-preserved through `atempo`) or `ramp` `[[t_in_clip, speed], …]` — the speed is
  linear between keys and the time map is its exact integral (a 0.25× stretch really lasts 4×); audio is dropped under
  a ramp. `interpolate: true` uses `minterpolate` for smooth slow motion (slow).
- `zoom` {from, to} 1–3: a Ken-Burns push eased with a raised cosine over the clip, rendered at 2× for half-pixel steps.
- `grade`: any `kmotion grade` preset (`restore`, `teal_orange`, `golden_hour`, `blue_hour`, `sodium_night`, `cyberpunk`,
  `vintage_film`, `matrix_tech`, `clean_commercial`, `magma_night`, `none`).
- `transition` into the next clip: `{type, dur 0.05–5}` or a name (`"slideup"`), `"cut"` for none. The picture uses
  `xfade`, the sound `acrossfade` of the same length; a transition is clamped to half of either clip.

## Overlays (drawn by Pillow, shaped Arabic, placed by expressions)
- `pos`: `center` · `top` · `bottom` · `lower-left` · `lower-right` · `upper-left` · `upper-right` · `lower-third`, or `x`/`y`
  as fractions (0–1), pixels, or FFmpeg expressions (`W`, `H`, `w`, `h`, `t`). Vertical safe areas: 14–80 % for 9:16.
- `anim`: `fade` (default 0.35 s) · `rise` · `drop` · `slide-left` · `slide-right` · `none`; `fade` sets the length.
- `lower-third` picks the right side and a slide-in from the right when the text is Arabic.
- `progress`: a bar growing from the right (`from: "left"` to flip), `y: top|bottom|px`.
- `captions`: the karaoke styles of `kmotion captions` (`reels`, `tiktok`, `hormozi`, `boxed`, `minimal`, `cinema`, `punchy`).

## Audio
- `keep_clip_audio` keeps the footage's own sound (level 1.0 → amix).
- `duck`: `auto` → under the voice when there is one, else under the clips' speech when music is present; `voice` ·
  `clips` · `none`. Sidechain: threshold 0.02, ratio 12, attack 20 ms, release 300 ms (≈ −18 dB under speech).
- Master: two-stage `loudnorm` to `lufs` (default −14, TP −1.5) + a limiter.

## What `kmotion timeline` reports
`film.timeline.json` next to the output: per-clip measured durations, the transitions used (type, at, dur), the
overlays placed (x/y expressions), the audio decisions and the gate (`--inspect`). `--dry-run` prints the FFmpeg
graph without rendering; `kmotion scenes CLIP --timeline edit.json` writes a spec with one clip per detected shot.
