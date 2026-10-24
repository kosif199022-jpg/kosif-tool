# Practical examples

All commands from the repo root. `K=.claude/skills/kosif-infinite-matrices/scripts/kmx.py`.

## 1. Re-run the first experiment without touching the shared memory

```bash
python3 $K experiment --recipe .claude/skills/kosif-infinite-matrices/recipes/glass-remembers-light.json \
  --out out/kmx/glass --render --mp4
# -> out/kmx/glass/{report.json, report.md, scene.html, stills/*.jpg, glass-remembers-light.mp4}
```

Open `scene.html` in a browser: the bar has play, scrub, a view selector (A | B | C, or one condition full frame) and sound. `?storyboard=1` shows the five key beats.

## 2. Log a replication on another machine

```bash
python3 $K experiment --recipe .../glass-remembers-light.json --out out/kmx/glass-rep --record --replication --sources SRC-001,SRC-003
python3 $K ledger verify
```

## 3. Rate the result (human review)

```bash
python3 $K rate --experiment EXP-0001 --score 4 --by "king" --notes "trace reads clearly; glow could be warmer"
python3 $K ledger stats          # operator_scores now include structure:tessellate, dynamics:integrate, finish:accumulate
```

## 4. A counterfactual variant: what if the glass forgets faster?

Copy the recipe, change only the physics, and run it. A changed field gives a new recipe hash, so it records as a new experiment:

```bash
mkdir -p out/kmx && python3 - <<'EOF'
import json; p='.claude/skills/kosif-infinite-matrices/recipes/glass-remembers-light.json'
r=json.load(open(p)); r['id']='KMX-R-0002'; r['slug']='glass-forgets-fast'; r['title_en']='Glass that forgets light fast'
r['title_ar']='الزجاج اللي بينسى الضوء بسرعة'; r['memory']['decay']=0.6
json.dump(r, open('out/kmx/glass-forgets-fast.json','w'), ensure_ascii=False, indent=1)
EOF
python3 $K experiment --recipe out/kmx/glass-forgets-fast.json --out out/kmx/forgets
```

Measured here: with `decay` raised from 0.035 to 0.6 the A−C gain drops from +0.340 to +0.117 and A−B from +0.515 to +0.191 (8/8 seeds still positive), so the verdict becomes `NOT_CONFIRMED` against the 0.15 margin. Fast forgetting makes persistent memory behave like no memory, which is the prediction; a negative result like this is worth recording too.

## 5. Ask for new ideas that build on saved results

```bash
python3 $K ideate --count 5 --seed 7          # look first
python3 $K ideate --count 5 --seed 7 --record # then save them as PROPOSED ideas
```

Each idea names three parents from three families with no shared code lineage and a signature that is new. The next step for any idea is a recipe and an experiment.

## 6. Inspect why a style was chosen as a parent

```bash
python3 $K bricks show flow-field     # its six bricks, REA counts, code-lineage neighbours
python3 $K bricks summary             # corpus-level findings
```

## 7. Move one of the 283 seeds forward

```bash
python3 $K hypotheses show KMX-SEED-001
# after writing and running a recipe for it:
python3 $K hypotheses mark KMX-SEED-001 --status NUMERIC_TESTED --evidence out/kmx/seed001/report.json --note "recipe KMX-R-0003"
```

## 8. From KOSIF Superpowers

```bash
python3 .claude/skills/kosif-superpowers/scripts/hub.py find "اعمل أسلوب جديد بذاكرة ضوء وقارن مع وبدون"
python3 .claude/skills/kosif-superpowers/scripts/hub.py tool infinite-matrices
```
