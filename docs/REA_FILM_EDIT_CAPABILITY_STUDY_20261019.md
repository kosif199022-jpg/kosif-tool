# REA Evidence-Based Video Capability Study — 2026-10-19

## Scope and important limitations

This investigation used **REA v6.7.0** on the user's authorized Windows computer. It is a **read-only, static study** of selected local installer artifacts plus **source-level analysis of KOSIF's own JavaScript**. No installer, patch, crack, or untrusted executable was launched. The evidence below DOES NOT establish access to proprietary editor source code, proof of implementation of commercial product features, or a license to reproduce protected code.

**REA package:** https://github.com/morluto/rea (MIT). Node v24.21.0 was verified compatible; rea CLI v6.7.0. The REA CLI was installed in an isolated user-tools directory, with lifecycle install scripts disabled; CLI artifact inspection and JS analysis were executed successfully. The REA MCP setup was *not* registered with Claude Code; REA reports missing agent registrations. Only report the CLI as tested.

### REA evidence from local folder "تجربة"

| Local artifact label | REA operation | SHA-256 | Proven scope |
| --- | --- | --- | --- |
| CapCut installer .exe | `inspect-artifact` | `7e7c5beded462beb4711b04cd506ccc24673d0a637dd1cb80a562b3870e40a79` | Recognized PE artifact, hashed, bounded static inspection |
| Canva installer .exe | `inspect-artifact` | `20530653cef67f160d623e0586f8955c2f9114538c35517007293173599caba6` | Recognized PE artifact, hashed, bounded static inspection |
| Premiere-labelled installer .exe | `inspect-artifact` | `25565eeb1cca35eb873b3ac939b79d3535f8ede1049b049b1e8a271762f63297` | Recognized PE artifact, hashed, bounded static inspection |
| Adobe Animate labelled setup .exe | `inspect-artifact` | `37bafe751e9307c119b84d7247f7c1d6b5c63810f4ad67dfc8c1a6d1479bf4b2` | Recognized PE artifact, hashed, bounded static inspection |
| Houdini-labelled setup .exe | `inspect-artifact` | `a9a380148688902bc6b193e7a7785b47f3fef26e9af7fdce1aa0707be48c664e` | Recognized PE artifact, hashed, bounded static inspection |
| FontLab-labelled setup .exe | `inspect-artifact` | `adcbdf56b023286e24112ab68c1f477e849fed2fb8f82a3761a187a7ec6e058f` | Recognized PE artifact, hashed, bounded static inspection |
| KOSIF first-party web directory | `analyze-javascript-application` | `7ee00ca107269d16511fe3652a0212642a34bcd326ee3058ca2cdabe44f2b753` | Four JS files parsed, 10,882 AST nodes visited, 35 findings, no parse failures |

**KOSIF REA Evidence ID:** `ev_2ef8285b6eda5c6dcdba9444ca99cadac366b8af3b829ee02843477eff2e0c04`.

Source analysis limitations: static application module relationships are **not** verified runtime behavior. REA reported no Electron windows or IPC operations in these four web scripts. This is expected for a conventional browser app, not proof that such functionality does not exist elsewhere.

**Local-only evidence files:** kept outside the repository under the laptop's separate `KOSIF-REA-STUDY-20261019/analysis` workspace. Evidence contains sensitive absolute local paths; it is intentionally **not committed or published**.

Other folder entries were inventoried but not deeply analyzed as executing applications: ACDSee, Capture One, DxO PhotoLab, Lightroom, Affinity Designer, Xara, JPEGmini, Dreamweaver, TikPlayer, virtualcam, and various installers/archives. Existence on disk does not prove installed or licensed functionality. Several folders contain patch/key-generator files, which are excluded. Do not execute or redistribute them.

## International editor feature benchmarking

The following are **documented industry reference capabilities** independently drawn from **official product documentation**. We do not copy proprietary source code, visual identity, fonts or effects:

| Feature family | Product reference / official source | KOSIF action | Current status |
| --- | --- | --- | --- |
| Transcript-based navigation and editing | Descript https://www.descript.com/features | Map `words.json` to navigation, markers, EDL operations; preserve narration in master | Planned UI; input word map supported by new script |
| Auto-captions and smart search | CapCut https://www.capcut.com/tools/desktop-ai-power | Semantic footage retrieval + Arabic captions; optional local OCR review | Planned; input-side matching implemented |
| Reframe, keyframes and graph motion | CapCut https://www.capcut.com/resource/pc-professional-video-editor | Deterministic camera moves, crop-aware vertical planner | Shot-level camera metadata implemented; render remains separate |
| Object masks and AI-assisted rotoscoping | Premiere https://www.adobe.com/products/premiere/ai-video-editing.html | Optional OpenCV/SAM2-type mask adapter, manual review | Proposed only; no engine installed/tested here |
| Track and animate 2D/3D titles | DaVinci Fusion https://www.blackmagicdesign.com/sa/products/davinciresolve/fusion | Node-style visual composition, tracked Arabic infographics | Proposed integration |
| Professional color-matching | Final Cut Pro https://www.apple.com/newsroom/2026/06/apple-creator-studio-gets-smarter-faster-and-more-connected/ | Shot-to-shot exposure/white balance matching | Proposed integration |
| Smart object isolation | Final Cut https://support.apple.com/en-sa/guide/final-cut-pro/ver1d67e3a53/mac | Privacy-preserving mask extraction and tracking | Proposed integration |
| Procedural particles and dynamics | Houdini https://www.sidefx.com/industries/motion-graphics/ | Seeded particle DSL for rain/dust/wind/grain, composited over REAL footage | Proposed integration |
| Vector symbols, motion tweens | Adobe Animate https://helpx.adobe.com/uk/animate/desktop/using/Tweens.html | Reusable vector motions / interpolation timeline | Proposed integration |
| Variable Arabic font inspection | FontLab https://help.fontlab.com/fontlab/8/ | Font profiling, installed-face matching, RTL shaping validation | Proposed enhancement to current font tools |
| Scene-specific prompt video editing | Runway https://runway.com/product/ai-video-editor | Local deterministic edit operations and reference previews, no paid generation | Proposed; remote Runway model **not** integrated |
| Source-locked filmmaking and QC | KOSIF https://github.com/kosif199022-jpg/kosif-tool | Provenance, rights gate, phrase splitting, word triggers, shot camera plan | **Implemented here** in `scripts/cinematic_cut_planner.py` |

## Actually added to KOSIF in this change

**Original source file:** `.claude/skills/kosif-superpowers/scripts/cinematic_cut_planner.py`.

It exposes a reproducible, local, dependency-free command accepting:
- corrected `words.json` with times;
- an inspected real-footage manifest with asset IDs, duration, actual video dimensions, license verification and manual review flags;
- immutable source audio duration and requested FPS.

It produces a JSON **edit decision list**, with:
- frame-exact timeline coverage via rational frame indices;
- phrase segmentation on speech pauses;
- simple bilingual tag-based candidate ranking;
- fail-closed rejection when provenance, 3-frame review, no-original-text or excluded-person flags are not explicitly verified;
- explicit unmatched-shot blockers rather than fake available footage;
- word-triggered hero graphic cues for important words/numbers;
- shot-by-shot deterministic camera motion parameters;
- an explicit unaltered-audio policy.

It does **not** perform transcription, access private websites, download source video, inspect a media frame, detect people, change audio, render the final film, or install third-party packages. Connect to the existing KOSIF/FFmpeg/media-source modules for those stages and verify the finished MP4.

### Usage

```bash
python .claude/skills/kosif-superpowers/scripts/cinematic_cut_planner.py \
  --words project/words.json \
  --clips project/verified_footage.json \
  --duration 48.5 --fps 30 \
  --out project/EDIT_DECISION_LIST.json

python -m unittest discover -s tests -p test_cinematic_cut_planner.py -v
```

Manifest example (flags must come from real checks):

```json
[{
  "id": "approved_shot_001", "path": "assets/shot_001.mp4",
  "duration": 9.6, "width": 3840, "height": 2160,
  "license_verified": true, "reviewed_frames": 3,
  "contains_text": false, "contains_excluded_people": false,
  "is_moving_video": true, "tags": ["مدينة", "مسجد", "sunrise"]
}]
```

## Next implementation priorities

1. Build a frame reviewer that sets text/person flags from observed video with manual confirmation.
2. Add downloadable legally sourced clips via existing KOSIF media tools and durable license evidence.
3. Integrate shot plan with a real frame renderer and FFmpeg preserving the audio master stream.
4. Add tracking-based camera crops, easing interpolation and subject-centering with artifact checks.
5. Add professionally reviewed Arabic motion typography and word-accurate visual event scheduling.
6. Test a complete footage-first film in 9:16. No success claim before a real MP4 passes visual/audio QA.

## Rights and analysis policy

REA is used only on owned or authorized targets. Locally present installers may have unverified provenance. **Do not run or patch them, bypass commercial licenses, intercept external services, copy closed-source algorithms or assets, or upload private binary analysis dumps into a public repository.** All added code in KOSIF must be independently authored or from a compatible open-source dependency with preserved license notices.
