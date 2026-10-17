# KOSIF Reference Visual Intelligence — executable camera and color measurement

**This is original executable KOSIF code**, not a Katana clone or bookmark list. It extends the Reference Edit Engine from measured shot cuts to actual low-resolution palette, exposure, frame change, and coarse displacement candidates, applied to new user-owned Remotion compositions.

## Real capabilities, requirements and states

| Capability | Tool | Truth boundary |
|---|---|---|
| Read video duration and dimensions | motion_reference_probe.py | ffprobe + authorized local media |
| Detect candidate edit cuts | motion_reference_probe.py --cuts | ffmpeg, heuristic review required |
| Measure palette, brightness, contrast | reference_visual_fingerprint.py | 64×36 local frames at 2 fps |
| Coarse displacement and change candidates | reference_visual_fingerprint.py | Pixel statistics, NOT object/camera tracking |
| Generate fresh editable shot colors | reference_edit_engine.py --visual | Validated aggregate fingerprint applied to original graphics |
| Preserve source audio timeline | audio_cue_mapper.py | Valid existing or externally aligned words |
| Build MP4 | Remotion local install and QA | Not guaranteed by Python code or a generated React project |
| Semantic understanding, original effect reconstruction | External reviewed tools | Not in this module |
| Higgsfield Katana API | Authorized external service | Not bundled or accessed here |

### Step-by-step executable workflow

Set the skill path inside the full kosif-tool repository:

    SKILL_DIR=.claude/skills/kosif-superpowers

Measure cuts and visual fingerprints from an authorized video:

    python3 "$SKILL_DIR/scripts/motion_reference_probe.py" ./reference.mp4 --cuts --out ./cuts.json
    python3 "$SKILL_DIR/scripts/reference_visual_fingerprint.py" ./reference.mp4 --probe ./cuts.json --out ./reference-look.json

Optionally generate cues from actual audio (word timestamps need a genuine aligner and corrected lyrics):

    python3 "$SKILL_DIR/scripts/audio_cue_mapper.py" ./voice.wav --aligned-words ./words.json --out ./cues.json

Produce a NEW editable Remotion composition with measured per-shot palette, no copied source frames:

    python3 "$SKILL_DIR/scripts/reference_edit_engine.py" --probe ./cuts.json --visual ./reference-look.json --cues ./cues.json --fps 30 --out ./new-edit

Omit the --cues argument entirely if no audio cue JSON is available. For user-owned replacement media use the engine's existing --manifest and --assets-dir flags only after checking that the content is owned/licensed.

Inspect the generated files: new-edit/src/plan.json, new-edit/src/Video.jsx, and decision-report.json. With user approval and a separately installed licensed Remotion version, preview, render and inspect the final MP4's image and original audio. Never announce completion just because HTML/React source was generated.

### Technical and evidence constraints

- The frame decoder is a bounded local ffmpeg subprocess; the reference file remains unchanged. Maximum 120 seconds and 1 GB media input, sampling every half second at 64x36 RGB.
- Color histograms, luminance proxy, local contrast and adjacent-frame changes are observations, not accurate calibrated color grading, semantic emotion recognition, film director intent or verified camera movements.
- The script estimates possible 2D translation through sparse pixel matching. Objects and lighting changes can imitate translation; this is NOT a CoTracker or SAM 2 substitute.
- The user retains the right to decide how much of a reference's visual style or editing choices to reuse. No original video pixels, full frames, source soundtrack, characters, or third-party artwork are copied into the new project by this module.
- The editable video engine accepts only validated six-digit hex palette data, contiguous segments and a duration matching its original reference cut report. Untrusted JSON cannot inject scripts into React style props.
- The output states are separated: source present; ffmpeg environment available; measured visual stats; storyboard/project created; rendered MP4; visually checked output. Only evidence of each step may promote it.
- Permissions are never auto-granted: verify read_user_media, media_usage_rights and write_new_files; installing packages, uploading customer media or spending generation credits requires distinct approval.
- No model weights or third-party library source code is bundled in this addition.

### Ecosystems studied: implement rather than blindly copy

The concept draws on [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) for shot boundaries, [CoTracker](https://github.com/facebookresearch/co-tracker) for point-motion research, [Remotion](https://github.com/remotion-dev/remotion) for frame-indexed React output, [Motion Starter Kit](https://github.com/motalim-ai/motion-starter-kit) for preview/approval patterns, and [Higgsfield Skills](https://github.com/higgsfield-ai/skills) for authorized external generation workflows. These are separate projects. Higgsfield Skills are NOT Katana source code; CoTracker would require its own compute and weights. Check runtime and commercial rights per component before installing.

### Regression commands

    python3 -m unittest discover -s "$SKILL_DIR/evals" -p 'test_reference_visual*.py' -v
    python3 "$SKILL_DIR/scripts/capability_runtime_router.py" --id reference-visual-style --json

The tests cover RGB means and palette, low-detail motion, sample segmentation, unsafe value rejection, remapped shot styles, real original React project generation and actual decoded synthetic ffmpeg input on hosts with ffmpeg/ffprobe. Mock-based source tests do not prove any particular user video or artistic fidelity.

### Still not implemented

High-accuracy foreground tracking; independent camera reconstruction; 3D face/pose inference; exact transitions from proprietary video; full clone of Katana; paid Higgsfield generation; automatic legal/media rights verification. Use authorized external tools and a separate measurable acceptance test to add each in the future.
