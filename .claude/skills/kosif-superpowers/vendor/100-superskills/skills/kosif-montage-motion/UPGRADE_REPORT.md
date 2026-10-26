# KOSIF Montage & Motion — tested upgrade (2026-10-08)

Original ZIP: 86 entries, 2,136,157 bytes uncompressed. Upgraded in a separate reversible directory without deleting the original.

## Changes
- Added offline read-only `kmotion proplan` with intent mapping, method cap, frame-accurate 5-beat storyboard, environment preflight and requested-Full-Pro fail-closed behavior.
- Added timestamped `--transcript` fallback for reel creation without the `faster_whisper` dependency.
- Added explicit transcript timing bounds/monotonicity, finite-number and input-size validation.
- Replaced Windows-specific `credit` font assumption and interpolated FFmpeg text with UTF-8 file-based overlay.
- Added `reel_with_transcript` to the environment capability report; original commands remain.
- Added KOSIF SEE routing and bounded 15K Atlas policy documentation, plus offline unit regression tests.

## Observations
- Baseline env route A on the test Linux machine: FFmpeg, Chromium and Playwright present; no faster_whisper/voice.
- Source compile passed before modification; no prior committed unit-test suite in the uploaded archive.
- Candidate unit suite: six tests passed; guarded Full Pro request exited 3 as designed.
- Candidate FFmpeg smoke: actual 160x288 MP4 produced using a timed Arabic transcript and credit overlay, QA `ok:true`, LUFS -14.0, true peak -9.7 dBTP.

## Truth limits
- Full Pro runtime not proven by a local script or KOSIF Think's ordinary fast council. Status: `NOT_FULL_PRO` for this environment.
- 15,122 graded Atlas skill entries observed in the packaged 2026-10-07 registry, not 15,122 individual executable skills activated.
- Platform-specific ASR, voice synthesizer and full-scale 3D performance not independently E2E tested here.
- Plugin publication to KOSIF SEE is a separate guarded mutation, not implied by producing this ZIP.

# v1.3 — faster, 3D shapes, 3D twin (2026-10-08)

## Changes
- `film.py`: parallel studio renderer (contiguous chunks → per-chunk H.264 segments → lossless concat), CDP
  `optimizeForSpeed` capture piped to FFmpeg undecoded, `--workers/--capture/--preset`, worker processes launched
  as plain subprocesses (safe from any caller).
- `kit/shape-kit.js` (new): SDF sculpting + coarse-to-fine surface nets + plush/gloss/eye/tube + stage disc + lite
  post + 3D truss overlay + rigged `bunny()`. `references/shape-kit.md` (new).
- `kit/three-kit.js`: exports `POST`; `kit/k3-entry.js` + `kmotion kit-bundle` rebuild the bundle.
- `structural_twin.py` v0.2: 3D space trusses, NumPy solve with eigenvalue singularity gate.
- Fixes: Playwright-cache browser discovery (env route C → A here), two-pass loudness, esbuild native binary on
  Linux, `kmotion` prints a failing command's message.

## Measured here (4 cores, software WebGL / SwiftShader, 1080×1920)
| What | Result |
|---|---|
| 60 frames of `projects/bunny_twin`, v1.2 `film.py` (sequential, PNG decode) | 151.2 s |
| same, v1.3, 1 page (fast capture) | 112.5 s |
| same, v1.3, 2 pages | 99.2 s (1.52×) |
| same, v1.3, 4 pages | 108.2 s (software GL already saturates the cores) |
| full film, 150 frames, `--blur 2`, auto (2 pages) | 421 s |
| bunny sculpt in the page (274,184 triangles) | ≈ 4 s once per page |
| final film gate (`inspect`) | ok: H.264 yuv420p, no black/frozen, −14.5 LUFS, true peak −3.4 dBTP |
| speed gate | 1 frame over 80 px/f (t = 4.13 s, the HUD caption/panel change), peak 86.6 px/f |
| tests | 29/29 (18 original + 5 space truss + 4 shape kit + 2 fast render) |

## Not measured / limits
- No hardware GPU here: the parallel speed-up with a real GPU is expected to be larger but was not measured.
- The bunny truss values are chosen illustrative numbers, not measurements of a toy; the film says so on screen.
- shape-kit meshes once per page load; very high `cells` values cost seconds per part.
