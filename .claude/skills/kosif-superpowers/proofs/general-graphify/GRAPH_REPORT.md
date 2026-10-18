# Graph Report - sample  (2026-10-16)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 244 nodes · 586 edges · 8 communities
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 35 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7

## God Nodes (most connected - your core abstractions)
1. `Atlas` - 25 edges
2. `main()` - 24 edges
3. `build_prompt()` - 16 edges
4. `run()` - 14 edges
5. `CliError` - 12 edges
6. `doc_variables()` - 12 edges
7. `main()` - 12 edges
8. `cmd_list()` - 11 edges
9. `cmd_scaffold()` - 10 edges
10. `main()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `aspect_resolution()` --calls--> `resolve()`  [EXTRACTED]
  tools/kosif.py → tools/aspects.py
- `_aspect_arg()` --calls--> `resolve()`  [EXTRACTED]
  tools/kosif.py → tools/aspects.py
- `main()` --calls--> `ratio_of()`  [EXTRACTED]
  tools/verify_video.py → tools/aspects.py
- `problems()` --calls--> `is_valid()`  [EXTRACTED]
  tools/import_briefs.py → tools/aspects.py

## Import Cycles
- None detected.

## Communities (8 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (37): ASPECT_NAMES, ASPECT_PRESETS, aspectSize(), BEGIN_FRAME_FLAGS, checkFrameSize(), COMMON_FLAGS, composeContactSheet(), DEFAULTS (+29 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (27): aspect_resolution(), Atlas, build_prompt(), CliError, cmd_list(), cmd_prompt(), cmd_scaffold(), cmd_search() (+19 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (19): load_json(), main(), playbook_meta(), skill_md(), brief_text(), main(), shared_runs(), words() (+11 more)

### Community 3 - "Community 3"
Cohesion: 0.17
Nodes (15): attempt(), doctor(), download(), edit_safe(), find_ytdlp(), impersonation(), info_for(), main() (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.15
Nodes (9): is_https(), iso_date_ok(), label_ratio(), looks_like_media(), main(), ratio_label(), read_json(), Report (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (11): _even(), is_valid(), _label(), ratio_of(), resolution(), resolve(), bullets(), main() (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.20
Nodes (11): aspect_label(), base_records(), canonical_categories(), fetch(), load_categories(), log(), main(), grab() (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.27
Nodes (15): cmd_family(), cmd_search(), cmd_show(), cmd_stats(), cmd_styles(), cmd_suggest(), expand(), filtered() (+7 more)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run()` connect `Community 4` to `Community 2`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.06748911465892599 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.10431372549019607 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `Community 4` be split into smaller, more focused modules?**
  _Cohesion score 0.14855072463768115 - nodes in this community are weakly interconnected._
- **Should `Community 5` be split into smaller, more focused modules?**
  _Cohesion score 0.14761904761904762 - nodes in this community are weakly interconnected._