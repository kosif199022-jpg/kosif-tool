# سجل تشغيلات سابقة — Earlier-session run log

What this gives: a shipped record of runs that an earlier session on 2026-10-16 measured in its own scratch folder, so power records do not depend on files that never ship. Each row says whether it was re-run for this note. Facts here are per-machine leases: re-run before relying on them (`python3 scripts/probe_env.py`).

| Power | What ran | Result | Re-run for this note? |
|---|---|---|---|
| WEB-08 | `curl -sSL https://huggingface.co/gpt2/resolve/main/config.json` and `…/hf-internal-testing/tiny-random-bert/resolve/main/pytorch_model.bin` through the agent proxy | config 200, 665 B, 0.74 s, valid JSON (`model_type` gpt2); weights 200, 540,217 B, 0.79 s (earlier run: 0.49 s and 1.0 s). The LFS redirect avoids the blocked cdn-lfs host | yes, 2026-10-16 |
| SELF-28 | `pip install torch --index-url https://download.pytorch.org/whl/cpu` in a venv, then a tensor inverse | 21 s, 769 MB, torch 2.14.1+cpu ran (see also `references/arsenal-general.md` row `torch`) | no (earlier session) |
| SELF-28 | Hugging Face small downloads | as WEB-08 | yes |
| GRAPH-05 | `graphify update .` after adding a 3-line function to a sample copy | 1.18 s; rebuilt 250 nodes, 592 edges, 9 communities; the new docstring became a rationale node. `graphify hook install` was **not** run | no (earlier session) |
| GRAPH-09 | `graphify install --project` in a sandbox HOME and project; then fake PreToolUse JSON piped to `graphify hook-guard search` | wrote `.claude/skills/graphify/`, `./CLAUDE.md` block and `.claude/settings.json` hooks (Bash\|Grep → hook-guard search, Read\|Glob → hook-guard read, timeout 10); first grep got an additionalContext nudge, the identical second call printed nothing; 0.09–0.12 s per call; fails open. `graphify claude install`, `claude uninstall` and `uninstall` were **not** run | no (earlier session) |

Graphify: https://github.com/Graphify-Labs/graphify (Apache-2.0; earlier contributions MIT). This note is original to kosif-superpowers.
