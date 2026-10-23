# KOSIF Atlas: vendored skills

Whole skill folders copied verbatim from the [KOSIF Atlas](https://github.com/kosif199022-jpg/kosif-atlas) at commit `99bb108d`, with the owner's approval (2026-10-23).

Each folder sits beside the KOSIF power card that cites it (`atlas.vendored` in `data/powers/atlas-*.json`). The card gives the method in our own words; this folder keeps the original text so nothing is lost.

- Only skills that pass the safe rule are copied: verdict `READ_ONLY_OK`, a permissive license (MIT or Apache-2.0 so far) and no risk flags. Copyleft skills are linked, never copied.
- Text files only. Nothing here is executed by KOSIF.
- Each plugin folder keeps its `SOURCE.md` (upstream repository, commit and license) and its `LICENSE` when the plugin shipped one. All rights stay with the original authors.
- `KOSIF_INTEGRATION.json` lists every copied file with its SHA-256; `evals/test_atlas_vendor.py` checks them.

To use one skill directly, copy its folder into your skills directory. The card's `install` field has the exact command, for example:

```bash
mkdir -p ~/.claude/skills && cp -r .claude/skills/kosif-superpowers/vendor/kosif-atlas/skills/3104-llm-finetuning/13286-checkpoint-promotion ~/.claude/skills/checkpoint-promotion
```

The packaged claude.ai skill leaves `vendor/` out, like the other vendored set in `vendor/obra-superpowers-v7`.
