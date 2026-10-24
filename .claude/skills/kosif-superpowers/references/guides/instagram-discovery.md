# Instagram reference discovery and causal transfer

The owner registered **@asirgokerr** and **@brkn.land** as reference sources. They are **unreviewed**; no individual reels or visual effects are asserted.

## CLI — run from repository root

```bash
IG=.claude/skills/kosif-superpowers/scripts/instagram_reference_bridge.py
python3 "$IG" sources
python3 "$IG" plan "3d object transforms into hand-drawn sketch"
python3 "$IG" plan "جسيمات مضيئة" --handle brkn.land
python3 "$IG" add https://www.instagram.com/reel/REALCODE/ --topic "Light particles" --state link_only
python3 "$IG" add https://www.instagram.com/reel/REALCODE/ --topic "Light particles" --state frames_reviewed --evidence-uri out/observations.json --motion particles --visual light
python3 "$IG" search "جسيمات ضوء"
python3 "$IG" propose https://www.instagram.com/reel/REALCODE/ --catalog .claude/skills/kosif-infinite-matrices/data/86_style_research_database.json --out out/ideas/reference.json
python3 "$IG" doctor
python3 -m unittest .claude/skills/kosif-superpowers/evals/test_instagram_reference_bridge.py -v
```

`plan` generates public Google/Bing searches. It does not call either provider or Instagram. Due to indexing limitations, queries are not exhaustive. Search actual public results using a separately available research tool and note observed titles/links. `add` writes metadata to `out/kosif-instagram/catalog.sqlite3`, not to the repository's shared tracked source registry; avoid sharing private notes. It only accepts canonical HTTPS Instagram reel/post/TV URLs, drops query/tracking parameters, and refuses unsupported attribution. `import-json` accepts a local array of reviewed metadata records.

`propose` returns `kosif.instagram.to-matrices.v1`: the claimed observations, provenance, candidate 86-style operators by tag overlap, and all six causal bricks **as research prompts**. The suggestion is **not** a valid KMX recipe until a human or agent translates it to typed parents, laws, conditions, simulation and tests.

## Evidence ladder
- `link_only`: only URL observed, all motion/style descriptions are *user labels*, not verified by video inspection.
- `metadata_verified`: metadata/caption checked; provide notes/caption/evidence. Still cannot infer movement from images not viewed.
- `frames_reviewed`: reviewer supplies evidence URI for genuinely viewed authorized frames, with scope and timestamps. Tool enforces presence of URI but **does not verify its content**.

No source proceeds to `PRODUCTION_READY` without KMX's independent controlled render, counterfactual tests and human assessment. No direct Instagram scraping, credential capture, API bypass, download, training or clip republication. An official Meta API integration needs account type, app permissions, and limitations reviewed separately.
