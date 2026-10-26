# v5.1 static audit and verification scope

## Baseline selection

Five supplied archives were materialized and inspected without running their scripts. ZIP members were checked for traversal, absolute paths, symlinks, duplicate normalized names and bounded extracted size. Ultra uses Windows separators; these were normalized before safe extraction. Original archives were preserved.

- **kosif-montage-motion.zip:** internally v5; 131 entries, 4,099,185 uncompressed bytes. Selected baseline. Combines v4 workflow utilities and Pro v1.3 shapes/space-truss work; adds `direct.py`, `verse.py`, their HTML templates and director tests.
- **KOSIF-Montage-Motion-Pro-v1.3-3D.zip:** 151 entries, 4,923,809 bytes. Includes shape kit, 3D structural examples, font assets and tests, but lacks v5 directors, lab template and everyday tools.py utility integration.
- **kosif-montage-motion-v4.zip:** 115 entries, 2,336,278 bytes. Includes fast/local rendering, lab kit and edit utilities; lacks v5 directors and Pro shape/font additions.
- **KOSIF-Motion.zip:** 55 entries, 1,155,292 bytes. Windows standalone package with install/menu BAT files, requirements.txt and a JavaScript lockfile; no SKILL.md.
- **ultra-motion-montage.zip:** 44 entries, 9,759,937 bytes. Older 2D/3D animator, beat detector, montage and QA tools, with generated demos and one bytecode cache. Narrower, Windows-oriented capture; not chosen as primary baseline.

All 99 Python files across the five expanded archives passed AST syntax parsing. This is not execution, dependency verification, an end-to-end test, or a security certification.

## Interfaces and dependencies

The existing composition interface is `index.html`, root data-composition-id/data-width/data-height/data-duration metadata, ready state `window.__ready`, and deterministic rendering through `window.render(t)` or kit-managed timelines/seek. Existing workflows also use transcript word arrays and loosely structured edit/verse JSON; there is no single existing scene-manifest schema.

`proplan.py` already emits `kosif.proplan.v1`; the Site uses that planning shape but explicitly labels its route `remote_planning_only`. The new manifest is distinct and does not become a direct legacy renderer input.

Actual local work needs FFmpeg/ffprobe; Python packages include numpy, Pillow, OpenCV, Playwright and optional faster-whisper/whisper, psutil, arabic-reshaper and python-bidi. Audio synthesis uses numpy. Voice narration invokes Windows PowerShell and OneCore. JavaScript package.json declares three, gsap, hyperframes and esbuild with floating ranges; v5 has no lockfile or complete Python dependency manifest. Copying the old standalone lockfile would not prove reproducibility of v5.

Ordinary Cloudflare Workers cannot spawn this Python/FFmpeg/Chromium subprocess pipeline: Node child_process is exposed as a nonfunctional stub. A Worker is suitable for bounded JSON planning/validation, templates and HTTP APIs; real rendering needs a separate execution environment. WebAssembly or external rendering services would be distinct additional implementations, not an automatic port.

Sources checked for runtime constraints:
- https://developers.cloudflare.com/workers/runtime-apis/nodejs/
- https://developers.cloudflare.com/workers/platform/limits/

## Preserved legacy limitations

These issues are observed in the supplied baseline and are not silently fixed or certified by the new bridge:

1. `motion.new`, `direct` and `verse` concatenate a caller project name with project roots without containment checks. Use a simple safe slug only. Do not expose these functions directly as a network service.
2. Title substitution in templates uses raw string replacement without HTML escaping. Do not insert untrusted titles directly.
3. `direct.apply_fixes` accepts an empty source phrase; its replacement loop can fail to progress or grow indefinitely. Do not use empty correction keys.
4. `film.Encoder.close` waits for FFmpeg without checking its return code. Verify the actual output through ffprobe and QA before claiming success.
5. `film.py drawing` imports external `studio.py`, which is absent from these skill archives. That mode is not self-contained.
6. Browser capture enables file access and disables the GPU sandbox; do not render arbitrary untrusted HTML in a privileged or sensitive environment.
7. Many legacy media commands have no explicit duration/resource caps. Transcript JSON lacks centralized schema validation and several empty-input cases are unguarded.
8. proplan's structural scope wording still says 2D-only, while the bundled structural solver implements 2D and 3D pin-jointed axial trusses. Neither is certified engineering analysis; bending, buckling and material nonlinearities are outside its scope. The Site deliberately does not expose that solver.
9. The package declares an ISC license, but no top-level license text establishes licensing for all original code. Three.js bundle retains MIT attribution; GSAP names its separate standard license; font OFL files are included. Preserve notices and verify rights before wider redistribution or incorporation into a hosted proprietary product. No blanket ISC relicensing is implied.
10. Documentation makes quality and completeness claims beyond what static inspection verifies. Treat measured local render/QA output as evidence, not promotional text.

## v5.1 changes and tests

The upgrade preserves bundled rendering source, examples and tests. It adds a new stdlib-only, exact-origin, private-Site bridge with consent gates; no legacy modules are imported by the new client. It updates the entrypoint and Arabic README, retaining earlier local documentation in LEGACY_WORKFLOWS.md.

The bridge's mocked HTTP tests cover operation allowlisting, consent before network use, missing/invalid access, exact authentication header and origin, refusal of redirects, bounded request/response sizes, content-type rejection, safe error messages, suppression of credential echo, finite JSON and exclusive nonsymlink project creation. Live Site access and MP4 rendering require separate verification. A freshly saved HTML file is still code to review before executing in a browser.
