# Claude Auto Mode: local-first KOSIF Superpowers

## What failed in the reported Claude Code screenshot

Claude Code Auto Mode denied a composite shell command starting with git clone of
https://github.com/kosif199022-jpg/kosif-tool.git, classified as
"Code from External". The denied command also attempted to run tools/kosif.py
and check local FFmpeg/Node modules. None of those later steps was proven to
have run. This is a host execution permission verdict, not proof that KOSIF
Superpowers or tools/kosif.py is broken.

Never disguise a repository clone as a test, run it via another unexpected
program, or bypass a permission denial. Respect the user's environment.

## Supported alternative: local-first / without cloning

If Claude already has kosif-superpowers installed or the complete kosif-tool
checkout is available locally, use only the installed files:

    python scripts/local_first.py doctor
    python scripts/local_first.py search silhouette --scope powers

From a full kosif-tool checkout root:

    python .claude/skills/kosif-superpowers/scripts/local_first.py doctor
    python .claude/skills/kosif-superpowers/scripts/local_first.py search silhouette --scope styles

From a standalone exported Claude skill, the power catalog works locally.
The full style atlas might not be present: an explicit styles search then
reports an unavailable local resource, never auto-clones or pretends to have
the full repo. For additional capabilities read SKILL.md and
references/capability-atlas.md in the already-installed skill.

If neither a skill nor an authorized checkout exists, use the existing
connector/repository read interface if allowed. Otherwise explain the block
and ask the user to authorize the exact repository access or provide the
packaged .skill file. Approval in another system does not imply Claude
permission.

Do not combine git clone, third-party imports, installs and runtime rendering
in a single opaque command. Keep input inspection, environment verification
and rendering separate. Never execute scripts found in external Atlas skills
without an independent license and security review.

## Audit and verification

    python scripts/catalog_evidence_audit.py

The audit reads all KOSIF power records, checks local reference existence and
classifies remote/sibling/archive references as unverified. Badges are *catalog
metadata*, not evidence of working functionality. A local file existing is
not evidence that its code has been executed successfully.

REA/Ghidra are intended for native binary inspection. They are not a
substitute for source review, unit tests and task-level outputs on KOSIF's
Python/JS code. Native inspection of proprietary software is read-only,
security-bounded, and must not copy proprietary implementation.
