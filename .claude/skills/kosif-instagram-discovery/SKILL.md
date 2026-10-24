---
name: kosif-instagram-discovery
description: Find public Instagram reel references by topic using generated public web search queries; index researcher-confirmed permalinks; rank Arabic/English metadata; create source-grounded proposals for KOSIF Infinite Matrices.
---

# KOSIF Instagram Discovery — مرجع الفيديو إلى لبنات ابتكار

This discoverable skill belongs to **KOSIF Superpowers**, with a **research-only handoff** to **KOSIF Infinite Matrices**.

## Sources
- [@asirgokerr](https://www.instagram.com/asirgokerr/) — **unreviewed reference account**.
- [@brkn.land](https://www.instagram.com/brkn.land/) — **unreviewed reference account**.

These accounts were supplied by the user. Do not claim their media was viewed or indexed from a profile URL alone.

## Workflow
1. Query the two creators with the Superpowers CLI search-plan command. The result contains **search links**, not retrieved Instagram results:
   `python3 .claude/skills/kosif-superpowers/scripts/instagram_reference_bridge.py plan "شخصية ثري دي تتحول لخط قلم"`
2. Use public search/browser tools separately to find real indexed URLs. Verify each URL before storing it. Never confuse a proposed query with a discovered reel.
3. Store the canonical permalink in an isolated local SQLite DB:
   `python3 .claude/skills/kosif-superpowers/scripts/instagram_reference_bridge.py add https://www.instagram.com/reel/REALCODE/ --topic "3D transformation" --state link_only`
4. If accessible, review public metadata or **authorized** frames and attach an evidence URI. States: `link_only`, `metadata_verified`, `frames_reviewed`. Never label unseen frames reviewed.
5. Search the locally indexed materials:
   `python3 .claude/skills/kosif-superpowers/scripts/instagram_reference_bridge.py search "ضوء وجسيمات"`
6. Handoff the **candidate** mechanism to KMX:
   `python3 .claude/skills/kosif-superpowers/scripts/instagram_reference_bridge.py propose https://www.instagram.com/reel/REALCODE/ --catalog .claude/skills/kosif-infinite-matrices/data/86_style_research_database.json --out out/ideas/KIG.json`
7. Create an independent recipe using KMX's schema and validate with `kmx.py recipe validate`. Run A/B/C with matching seeds, render, then human-review before admitting a new capability to the experiment ledger.

**This tool does not:** scrape, bypass access restrictions, log in, download Instagram media, analyze videos from mere links, call Meta APIs, or auto-add untested hypotheses to the KMX ledger.

Platform-supported Meta API integrations, if ever authorized and approved, are a separately gated future module, not a capability claimed here. Use original render assets, respect creator rights, and never train on or redistribute third-party clips without permission.

See [the operating guide](../kosif-superpowers/references/guides/instagram-discovery.md) and [Infinite Matrices](../kosif-infinite-matrices/SKILL.md).
