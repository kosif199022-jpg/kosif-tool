# mcp-for-blender (ahujasid/blender-mcp) - dissection

Commit 2e4b0bc294694b1570d76ed01be657c22e6d02a0. About 33.8k stars. License MIT (LICENSE) plus a separate
TERMS_AND_CONDITIONS.md (read, see below).

## What it really is
A two-part bridge: `addon.py` (7264 lines) is a Blender addon that opens a local TCP socket inside a GUI Blender
and executes JSON commands on the main thread; `src/blender_mcp/server.py` (2288 lines, FastMCP) exposes MCP tools
and forwards them to the addon. Everything depends on a LIVE Blender GUI with the addon running. The Dragon runs
`blender -b` headless, so the socket/addon layer is not reusable; only the ideas and the asset APIs are.

## Terms and conditions (TERMS_AND_CONDITIONS.md)
Not a use restriction on the code. It is a privacy/telemetry policy: content telemetry (prompts, code, screenshots,
scene metadata, manual edits) is opt-in and off by default; a minimal anonymous usage record is sent unless
`DISABLE_TELEMETRY=true`. Opted-in data may be used for AI training and open datasets. Verdict: the Dragon should not
install the addon/server (telemetry.py, trajectory.py, consent_prompt.py); we only take ideas, so the policy does not
apply. If anyone ever runs the server: set DISABLE_TELEMETRY=true and never tick the consent box.

## Architecture (hand-read)
- Tools in server.py: get_addon_status (452), get_scene_info (609), execute_blender_code (793), look (1564),
  search_assets (1882) / import_asset (1952) over Poly Haven, Sketchfab, Poly Pizza; generate_3d (1759) over Tripo,
  Hunyuan3D, Hyper3D Rodin, Meshy (generation.py:32); viewport app (2121+); record_trajectory_feedback (1485).
- blender_scripts.py: observation scripts sent through execute_code (SCENE_SUMMARY, LOOK).
- guides/*.md (7 files, 21 KB): short Blender craft guides (scene, materials, rigging, retopology, animation, level design, bpy).
- Poly Haven API base: addon.py:336; Poly Pizza: addon.py:220.

## Dragon already has
blender-pro: headless `blender -b`, 139 ops, recipes, raw bpy exec, `inspect` (objects/materials/frames), `thumb`
render. media-hunter already covers Poly Haven HDRI/texture search at media level.

## New vs the Dragon
1. Scene audit with spatial judgement: real size from evaluated bounds, ground contact (on ground / floating / below)
   (blender_scripts.py `bounds`/`line`). Dragon `inspect` has dimensions but no judgement.
2. Mesh topology health: quads/tris/ngons, non-manifold, boundary, loose verts, poles (blender_scripts.py `topology`).
3. Armature weight check (`weights`).
4. Poly Haven search ranked by downloads with real-world dimensions (server.py:889), file resolution by res/format.
5. Post-import normalisation recipe (guides/scene.md): scale from bbox, drop to ground, face -Y.
6. Asset-source decision guide (guides/scene.md): generate hero, PolyHaven surfaces/HDRIs, Sketchfab named things, Poly Pizza low-poly.
7. Sketchfab / Poly Pizza / Meshy / Tripo / Hyper3D / Hunyuan3D integrations: keys required, paid or rate-limited; source-linked only.
8. `look` multi-angle sheets from the offscreen GPU viewport: needs GUI GPU, not portable to -b. Source-linked.
9. guides/*.md could be condensed into blender-pro references.

## Native implementation
`native_blender_audit.py`: `audit <file.blend>` (items 1-3 plus missing textures, unapplied/negative scale, default
names, no UV/material/camera/light, huge/tiny), `polyhaven search|files` (item 4, stdlib urllib, retries), `self-test`.
Written from scratch, no copied code. Runs `blender -b FILE --python self -- args`; result via a marker line.

Self-test (python -I native_blender_audit.py self-test, Blender 5.2.3 LTS, real run):
```
{
  "ok": true,
  "self_test": "PASS",
  "blender": "5.2.3 LTS",
  "objects": 6,
  "issues": 15,
  "totals": {
    "warn": 4,
    "info": 11
  },
  "polyhaven": {
    "hdri_hits": 225,
    "first": "lilienstein",
    "files_1k_hdr": 1
  }
}
```
It builds a broken scene (floating cube, sunk scaled cube, 2000 m plane, default-named plane, 3-face fin edge),
asserts each finding, and does a live Poly Haven HDRI search plus file resolve.

## Caveats
- Poly Haven /assets listing sometimes truncates mid-read (seen once); helper retries 4 times.
- Audit uses evaluated object bound boxes (object-level), ground = world Z=0.
- Generation providers need API keys and spend credits; not implemented.

## REA evidence log
REA tools run: none productively. `inspect_artifact` was loaded but takes no path (needs an already opened target),
and this is plain Python source plus one HTML viewer, so per REA's own guidance it was read by hand (Read/Grep).
No Evidence ids. Nothing opened, nothing to close.
