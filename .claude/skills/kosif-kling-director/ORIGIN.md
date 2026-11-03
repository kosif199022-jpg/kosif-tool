# Origin and licence

- **Method:** the "Kling 4 Cinematic Director (v2)" skill by Omar Hasan (`omar-hasan-kling-cinematic-director.skill`, re-uploaded by the owner on 2026-11-03), which merges the official Kling 4.0 user guide and the Higgsfield short-film workflow by @adilinthewildtempo. The upload carries no licence file, so its text is **not** copied here: the KOSIF adaptation already in the repository (`.claude/skills/living-site/references/level-2-kling-director.md`, A41, with the mandatory channel-promo first message removed) is the single reference, and this skill links to it.
- **Lint:** `.claude/skills/living-site/tools/kling_lint.py` (KOSIF, A41), loaded by path and not duplicated.
- **Program:** `scripts/kling_director.py` is original KOSIF code (2026-11-03), stdlib only, same terms as the rest of this repository. It writes text files only: no network, no model call, no credits.
