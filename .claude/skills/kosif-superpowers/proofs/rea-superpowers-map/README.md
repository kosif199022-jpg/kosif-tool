# REA receipt for the superpowers map

`receipt.json` is the trimmed output of `rea import-reference-source` (REA 6.7.0, MIT) run on this skill folder: counts, languages, manifests, exclusions, REA's limitations, the JavaScript require/import edges, and the graph and root SHA-256 that identify REA's full graph of the tree at `vcs_head`. REA read the tree as historical reference only and executed nothing.

Refresh it with the commands in [maintain.md](../../references/guides/maintain.md#mapping-the-skill-the-rea-way); `scripts/rea_superpowers_map.py ingest-rea` refuses any JSON that is not a REA HistoricalSourceSummary/HistoricalSourceGraph.
