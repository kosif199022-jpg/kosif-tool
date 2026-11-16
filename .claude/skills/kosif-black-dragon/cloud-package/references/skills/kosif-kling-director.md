---
name: kosif-kling-director
description: >-
  Kling 4.0 short-film director's prompt pack from one story line: split the
  film into generation blocks of 30 s or less (20 s for Flash), write a master
  prompt per block in the 15-header director order with a shot clock that adds
  up exactly, a 3x3 storyboard prompt per block, and plan.json with the
  settings box and takes plan, then lint every block before any credit is
  spent. Text only, never generates. Use for «فيلم قصير بكلينج», «برومبت كلينج»,
  «ستوري بورد ٣×٣», «قسّم الفيلم لبلوكات», Kling prompt, short film prompts.
---

# KOSIF Kling Director — مخرج أفلام كلينج القصيرة

بالعربي: المهارة دي بتاخد سطر القصة وتطلع لك حزمة البرومبتات كاملة لكلينج 4: تقسيم الفيلم لبلوكات (كل بلوك ٣٠ ثانية أو أقل)، برومبت رئيسي لكل بلوك بالترتيب الصحيح للعناوين وتوقيت لقطات بيتجمع بالظبط على مدة البلوك، وبرومبت ستوري بورد ٣×٣، وملف `plan.json` فيه الإعدادات وخطة اللقطات (takes). وبعدين بتفحص كل بلوك بالـ lint قبل ما تصرف أي كريدت. **مش بتولّد فيديو ولا صور ومش بتصرف كريدت.**

## The method lives in one place

The full director method (Story Engine, acting task, fight beats, anamorphic look, Nano Banana templates A–G, master prompt template H, weak points) is [`living-site/references/level-2-kling-director.md`](../living-site/references/level-2-kling-director.md). Read it for Steps 0–1 (opening questions, 10 ideas) and to fill the `[bracketed]` slots this tool leaves. This skill adds the program for Steps 2, 4 and 5; it does not copy the method, so the two never drift.

## Front door

```bash
K=.claude/skills/kosif-kling-director/scripts/kling_director.py
python3 $K plan 90                                         # block 1: 0-30 s, block 2: 30-60 s, block 3: 60-90 s
python3 $K build --task "<the chosen idea, in the user's words>" --seconds 60 --ratio 21:9 --out out/<job>/kling
python3 $K check out/<job>/kling/block_01.txt              # after you fill the slots: must print PASS
python3 $K --self-test                                     # known answers + 4 planted mistakes caught
```

`build` writes `block_NN.txt` (master prompt), `storyboard_NN.txt` (3x3 grid, 9 panels on the block's clock) and `plan.json`. Exit 0 = every block passes, 1 = a block fails (for example the story line itself says "8K" or names a camera brand: rewrite it), 2 = usage error. `check` is the living-site gate `tools/kling_lint.py` (duration, headers, touching time ranges, reference roles, Omni/Keyframes limits, polish words, brand names, mood-camera words, Arabic dialogue, 24 mm on a face; warnings for negatives, >2 moves, shots over 6 s, missing head-count lock).

## Rules

1. Fill every `[slot]` from the method, then run `check` on each block again: a filled prompt is a new prompt.
2. Kling 4.0 has no Arabic lip sync: Arabic dialogue goes in as a voice-over in the edit; the AUDIO block stays English or silent.
3. Generating is a paid step. Show the prompts and the quote (takes x blocks) and wait for the user's yes; log each paid job with `living-site/tools/ledger.py`. In a KOSIF session the generation itself goes through the Higgsfield MCP mapping in the method file, never through this script.
4. Credit the method's authors when it shapes a delivered film (see [ORIGIN.md](ORIGIN.md)).
