# KMX-R-0001 — Glass that remembers light

**الزجاج اللي بيتذكر الضوء** · CONFIRMED_IN_MODEL

Causal inside this numerical model only: same stimulus, same seed, one factor changed per condition. Not a claim about real glass physics or global novelty.

## Six bricks

- **state:** Glass memory field M[x,y] in 0..1.5 on a 48x27 grid; tile id and absorption per cell; particle positions p_i and velocities v_i in grid units; light L[x,y,t].
- **operation:** write (L into M), leak (decay), diffuse inside a tile, sample gradient (bilinear central difference), integrate particles (semi-implicit Euler with drag), render (glow + motes + lead lines).
- **law:** M(t+dt) = clamp(M + dt*(absorb_tile*write*L - decay*M) + dt*diffusion*lap_tile(M), 0, 1.5);  v(t+dt) = (1-drag)*v + dt*(gain*grad M(p) + flow + jitter);  p(t+dt) = reflect(p + dt*v)
- **time:** 30 steps per second, 1 step per frame, 10 s; beam ON from 0.0 to 4.0 s and OFF afterwards, so every effect seen after 4.0 s comes from history, not from the live stimulus.
- **memory:** Material memory = M (physical history inside the run). Research memory = the experiment ledger (memory/ledger.jsonl) that stores verdicts across runs.
- **feedback:** Particles read M (state -> dynamics). They do not write back to M in v1, so the causal chain is one-directional and testable: light -> M -> motion.

## Parents (one role each, three families)

- structure → `stained-glass` (Painterly), operator `tessellate`: Voronoi glass tiles set where memory can spread (lead lines block diffusion) and how strongly each tile absorbs light.
- dynamics → `flow-field` (Data & Information), operator `integrate`: Particles are integrated through a vector field; here the field is the gradient of stored light.
- finish → `light-painting` (Light & Imaging), operator `accumulate`: Long-exposure accumulation becomes a physical material state instead of a camera effect.

## Conditions (same stimulus, same seed, one factor changed)

| condition | change | motes on trace after beam off | memory after off | same memory as A |
|---|---|---|---|---|
| A_full | `{}` | 77.2% | 158.93 | — |
| B_no_coupling | `{"coupling.gain": 0.0}` | 28.6% | 158.93 | True |
| C_no_memory | `{"memory.mode": "instant"}` | 49.5% | 0.00 | False |

Chance level (share of the pane that is on the trace): 23.4%.

## Replication over 8 seeds

| A minus | mean | sd | min | positive | sign test p |
|---|---|---|---|---|---|
| B_no_coupling | +0.515 | 0.060 | +0.428 | 8/8 | 0.003906 |
| C_no_memory | +0.340 | 0.040 | +0.271 | 8/8 | 0.003906 |

## Dose-response (coupling gain × factor)

| factor | capture A |
|---|---|
| 0.00 | 28.6% |
| 0.25 | 61.6% |
| 0.50 | 70.5% |
| 1.00 | 77.2% |
| 1.50 | 80.6% |

Spearman ρ = 1.000.

## Checks

- ✅ B_same_memory_as_A
- ✅ C_has_no_memory_after_off
- ✅ A_beats_B_every_seed
- ✅ A_beats_C_every_seed
- ✅ dose_response_monotone

## Render evidence

- deterministic (same t → same pixels): True
- page errors: 0
- t=2.40s: A vs B changed pixels 2.4%, A vs C 45.7%
- t=3.90s: A vs B changed pixels 4.0%, A vs C 68.9%
- t=6.00s: A vs B changed pixels 3.9%, A vs C 73.8%
- t=9.90s: A vs B changed pixels 3.8%, A vs C 76.2%
- video: glass-remembers-light.mp4

## Limits

- The causal claim holds inside this numerical model; it says nothing about real glass optics.
- Particles read memory but do not write it (one-directional chain, v1).
- Visual quality and meaning still need a human rating (`kmx.py rate`).
- Not a claim of global novelty; parents come from a third-party reference atlas analysed locally.
