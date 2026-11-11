# Black Dragon — Instagram Reel 12 Video Tools

**Source:** https://www.instagram.com/reel/Dfmun_Fjap1/ (description posted 2026-11-11; descriptions/caption read, audio playback not independently verified).

This integration is **a real installable dependency workspace and executable CLI bridge**, not a claim that GitHub hosts all installed software, or that all 12 packages have rendered a video. Existing Black Dragon seven-stage production protocol stays authoritative.

| Production line | Installed packages / executable |
| --- | --- |
| Render | \`remotion\`, \`@remotion/cli\`; \`hyperframes\`; \`@motion-canvas/core\`, \`@motion-canvas/2d\` |
| Design | \`three\`, Python \`manim\`, \`roughjs\` |
| Animation | \`gsap\`, \`animejs\`, \`@mojs/core\` |
| Sound/output | Python \`whisperx\`, \`auto-editor\`, \`ffmpeg\` + \`ffprobe\` (system or bundled npm binaries) |

## Get started (at the **worker** where videos will render)

Node.js/npm, Python 3.10+ (check current individual tool constraints) and internet access are prerequisites. For Manim, system packages such as Cairo/Pango may also be needed. WhisperX can be large, may download speech models at first use, and may need GPU/CUDA; model licences are separate.

From the repository root:

\`\`\`bash
T=.claude/skills/kosif-black-dragon/integrations/instagram-video-12/toolchain.py
python3 "$T" doctor --json
python3 "$T" plan "ريل سينمائي 9:16 بالعربي مع ترجمة متزامنة"
python3 "$T" install --all --dry-run
python3 "$T" install --all --yes  # downloads and installs, only on the machine executing it
python3 "$T" doctor
python3 "$T" run ffmpeg -- -version
python3 "$T" run hyperframes -- --help
python3 "$T" run remotion -- --help
\`\`\`

On Windows use \`py -3\` instead of \`python3\` if needed. npm binaries remain in this subfolder's \`node_modules\`; Python libraries remain in \`.venv\`. Both are untracked workspace assets. \`ffmpeg\` / \`ffprobe\` are resolved from PATH first, then their platform-specific npm installers.

### How the fusion is executed

1. Run \`plan\` to choose the production libraries; all 12 are tracked in \`registry.json\` and not blindly invoked in every video.
2. Run \`doctor\`. A **READY** status means dependency resolution only; it is *not* an actual rendering/test result. Install any missing tools *with explicit consent*.
3. Produce actual HTML/Three/GSAP/Anime/Mo.js/Rough.js animations via HyperFrames; JSX compositions via Remotion; timeline drawing via Motion Canvas; math via Manim. Packages provide **libraries**, not a uniform universal CLI.
4. Where required, invoke installed command-line tools via \`toolchain.py run <name> -- <args>\` and preserve their real outputs. Python \`whisperx\` does speech/transcription/alignment; \`auto-editor\` can cut silence, but a natural pause margin and human review are required.
5. Use the existing \`video_protocol.py\` for \`brief → concept → color-design → shots → produce → qa-color → deliver\`. Store existing CORE receipts and run its final \`check\` gate. These 12 packages **do not replace** its QA and artistic review.

All operations are local and opt-in; packages are not vendored into this repository. The command \`install --all --yes\` may take substantial disk space and needs a network and the worker's platform prerequisites. Do not present a dry-run, dependency check, or unexecuted plan as completed installation.

### License and security notes

- Remotion is **source-available / license-restricted**, free for eligible individuals and teams up to three; production services and larger organizations must check the current terms: https://www.remotion.dev/docs/license/pricing
- HyperFrames is Apache-2.0: https://github.com/heygen-com/hyperframes
- GSAP is free to use but its terms still apply: https://gsap.com/
- FFmpeg build licensing varies by linked codecs/build options; check your distribution.
- JS/Python dependencies are third-party code with installation scripts; inspect releases and generate/commit lockfiles after first verified install. Do not automatically grant external API keys, download third-party video footage, or run an unknown repo's installation scripts silently.

### Verification

\`\`\`bash
python3 -m unittest discover -s .claude/skills/kosif-black-dragon/integrations/instagram-video-12/tests -v
\`\`\`

This suite tests **registry, route selection, non-mutating dry-run, and doctor behavior** without downloading any packages. Full render, audio alignment, on-device load, and package version compatibility need an additional real worker test and receipt.
