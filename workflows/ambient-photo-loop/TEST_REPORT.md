# Test report — ambient photo loop (2026-10-23)

Input: 941×1672 PNG (sha256 `a60ed1f2bf1217abe61a12634d82798a46ab0ca6843a13edc0b510285ae54f90`, not committed).

| check | result |
|---|---|
| container | H.264, 1080×1920, 30 fps, 7200 frames, 240.000 s, no audio |
| size | 108.7 MB (sha256 `6c5fbdb46bf4ca93cf95637449698274f7af868cc230ad45f4866f86f6122a2c`) |
| render time | 8 min 41 s for the 24 s loop (720 frames, 4 cores); concat to 240 s by stream copy |
| person unchanged | mean abs diff vs source inside the protected mask: 2.37 / 2.36 / 2.37 / 2.37 / 2.36 at t = 0, 23.967, 24, 120, 239.9 s, the same at every t, so it comes only from H.264/yuv420; before encoding the person pixels are copied from the source |
| loop seam | background diff 3.79 at t = 23.967 vs 3.80 at t = 24 and t = 0: no visible jump |
| script parity | `ambient_loop.py test` stills vs the first ad-hoc render: max diff 7/255, mean 0.04 |
