# أرنب وأسد — KOSIF LAB 01 (sources only)

```bash
export KOSIF_MOTION_HOME=$PWD/work
python scripts/kmotion.py new lab_rabbit_lion --lab --seconds 20 --fps 24 --size 960x540 --title "أرنب وأسد"   # then copy this folder's index.html + src/main.js over it
python scripts/kmotion.py score work/projects/lab_rabbit_lion/assets/score.wav --spec assets/score.json --cues assets/cues.json
python scripts/kmotion.py frames projects/lab_rabbit_lion --times 1,4.5,8,11,14.5,17,19.5
python scripts/kmotion.py render projects/lab_rabbit_lion --engine studio --workers 2
python scripts/kmotion.py inspect work/out/lab_rabbit_lion.mp4
```
Six beats on the HUD: SHAPE (wire → plush) · JOINT (pivot rings, the ear, the eye) · LOAD (the mane) · BREAK (the far side, ears flop) · SWAP (the tail becomes a tuft) · RANK (the wide).
