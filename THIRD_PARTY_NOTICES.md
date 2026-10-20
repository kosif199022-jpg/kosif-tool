# Third-party notices — إشعارات الطرف الثالث

KOSIF TOOL's own code and text are under the MIT license in [LICENSE](LICENSE). The material below keeps its own license; nothing third-party is vendored beyond what this table lists, and the tool catalog in `.claude/skills/kosif-superpowers/repos.json` only links and credits.

| Material | Where | License | Notes |
|---|---|---|---|
| FFmpeg `vf_xfade.c` transition formulas (NumPy port) | `.claude/skills/kosif-superpowers/scripts/mimic/mm_transitions.py` | LGPL-2.1-or-later | Keep the file separable in any product build; notice at the top of the file. Other mimic modules are MIT with the repo. |
| Amiri (Khaled Hosny), Aref Ruqaa, Cairo, Lalezar, Reem Kufi, Tajawal | `.claude/skills/kosif-superpowers/proofs/_shared/fonts/` | SIL OFL 1.1 | Unmodified Google Fonts releases. |
| Amiri + Bodoni Moda (subset, instanced and merged as "KOSIF Jumuah") | `fonts/kosif-jumuah/` | SIL OFL 1.1 | Derived font; reserved font names respected, see its README and LICENSE. |
| Google Fonts Arabic families fetched on demand | `scripts/mimic/mm_fonts_lib.py` cache | SIL OFL 1.1 per family | Downloaded by the user at run time; never committed. |
| Tesseract `ara.traineddata` | optional `assets/tessdata/` cache | Apache-2.0 (tesseract-ocr/tessdata) | Fetched on demand; never committed. |
| REA (`rea-agents`) | not vendored; installed by the user with npm | MIT (© 2026 morluto); bring-your-own engines keep their own terms | Catalogued as powers REA-001…REA-153. |
| Owner-uploaded skill packages (KOSIF SEE, cinematic kits, mimic, Higgsfield motion skills, film project) | distilled in `references/*.md` in the owner's own words | owner's material (no LICENSE file in the uploads) | Ported scripts rest on the owner's upload as consent; third-party quotes inside them stay reference-only. |
| MagicPath agent skills (MagicPathAI/agent-skills, a1ced96) and MagicPath public documentation | method ideas only, rewritten in KOSIF's words: APPX-120…APPX-139, `.claude/skills/kosif-superpowers/references/app-studies/magicpath.md` | agent-skills: MIT as declared in its plugin manifests (© MagicPathAI); documentation: proprietary, nothing copied | No MagicPath text, code, scripts or images are in the repo; the exported public scripts of the study stay outside it. |
| Third-party videos, prompts and media named in `styles/` and `references/` | links only | their authors' terms | Credited, never copied. |

العربية: كود KOSIF ونصوصه بترخيص MIT؛ ما في الجدول أعلاه يحتفظ بترخيصه، ولا يُضمَّن في المستودع إلا ما ذُكر.
