# REA receipt for the whole KOSIF Atlas

`receipt.json` is the trimmed output of two `rea import-reference-source` runs (REA 6.7.0, MIT) on [kosif-atlas](https://github.com/kosif199022-jpg/kosif-atlas) at `vcs_head`:

- a `--detail summary` run on the repository root
- a full graph run on `skills/`

It records counts, languages, limitations and the manifest, graph and root SHA-256. It also has a digest over the REA SHA-256 of all 14,793 SKILL.md files, so a re-run can prove that the same files were read.

REA read the Atlas as historical reference only, and nothing in it was executed. The per-skill review status built on this read is `data/atlas_ledger.json.gz` (`scripts/atlas_ledger.py`). The pass is described in [atlas-ledger-20261023.md](../../references/atlas-ledger-20261023.md).
