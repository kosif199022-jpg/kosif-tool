# KOSIF Blender and Smart Draw Evidence (2026-10-19)

## Verified local read-only inventories

- REA 6.7.0 and Ghidra 12.1.4 inspected Blender 5.2.2 BlendThumb.dll:
  9 segments, 557 defined procedures, 237 defined strings. SHA256:
  7230681cc83424fbdcd67438019a5af64068f073d98c15b3a58e37d0717d2fc4.
  This DLL is thumbnail shell integration, NOT Blender's complete 3D engine.
- blender_api_audit.py AST-parsed 810 of 810 bundled Python scripts:
  66 bpy.types.Operator class definitions, 31 PropertyGroups, 24 Panels,
  10 Menus. Filename-topic matches: animation 150, video 104,
  materials 84, geometry 36, drawing 15 (nonexclusive). This is static source
  evidence, not execution or C/C++ source understanding.
- Desktop folder تجربة: 2,109 files, 18,530,811,455 bytes, zero unreadable;
  30 binary candidates, 1,232 text/source candidates, 137 archives.
  Static triage is NOT an exhaustive reverse engineering audit.
- First GitHub account: 24 repositories (19 public, 5 private) inventoried at
  metadata level only. Other accounts/branches/source are not all included.

Private evidence remains off GitHub in KOSIF_RESEARCH_PRIVATE_20261019:
REA_BLENDER_THUMB_20261019.json,
BLENDER_PYTHON_API_AUDIT_20261019.json,
TAJRIBA_CURRENT_LOCAL_AUDIT_20261019.json,
GITHUB_REPO_METADATA_20261019.json.

## Independently executable drawing tool

smart_draw.py takes strokes as constrained JSON, recognizes rectangles, circles
(as ellipses), lines and freehand geometrically, with pen/marker/highlighter,
layer separation, PNG and SVG outputs. Uses KOSIF Creative Paint. It is NOT
machine-learning object prediction and does not embed third-party artwork.

    python scripts/smart_draw.py doctor
    python scripts/smart_draw.py analyze --scene templates/smart-draw-demo.json
    python scripts/smart_draw.py render --scene templates/smart-draw-demo.json --output sketch.svg

## Official sources and limits

AutoDraw https://www.autodraw.com uses ML guesses with artist drawings;
its model and graphics are not imported into KOSIF.
Canva Draw https://www.canva.com/draw/ describes pens, highlighters, Shape Assist,
editability and team collaboration; KOSIF implements a smaller original subset,
not the collaborative app, eraser or template library.
Blender API https://developer.blender.org/docs/release_notes/5.2/python_api/
provides legal reference for Blender Python interface. native_3d.py works
without Blender but supports a much smaller set of 3D features.
Further reviews should trace actual selected source behaviors, test outputs,
verify third-party scripts/licenses, and label missing pieces explicitly.
