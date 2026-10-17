# KOSIF Tool branch reconciliation — 18 October 2026

## Policy
- Every source PR branch head is recorded as a parent in the integration history. No force pushes, branch deletion, or discarded historical commits.
- Where a source branch modifies an older copy of a file already changed in `main`, the reconciliation keeps the current main implementation to protect already-integrated capabilities. All source-specific code files, docs and tests for these 12 PR branches are already present in the main Git tree (verified against their head trees).
- PR #18 adds six previously missing reference catalog and inspection files, with an HTTP(S)-only, public-network-only, bounded-download, local-ffmpeg-protocol patch and fresh regression tests.
- PR #33 was merged separately after adding four new motion runtime files, retaining existing motion implementation routes.
- This record is an ancestry reconciliation, not a claim that every historical source version supersedes the present implementation. Verify the integration PR CI before promoting.

## Integrated history
| PR | Feature | Source head |
| --- | --- | --- |
| #18 | Reference catalog and inspector, hardened | `9b4e23542244eaff67cfe348e164ca4a978155c9` |
| #33 | Motion runtime (merged separately) | `4d6cdde5de52cc991634ef968a11cf81c54566f0` |
| #22 | creative quality gates | `f52be8ce57602028974da776a71b77cb9bfa00de` |
| #23 | music rhythm reactive reference motion | `1b5abd3d3ff3867d7371aab17fb7cf01d91238b7` |
| #24 | Katana reference edit execution | `c4842100f33c7d99d55c1f2700a3989d7b10c169` |
| #25 | capability runtime router | `4deb0e00f25856f99fe535939f119df8ecf4c88c` |
| #26 | REA evidence bridge | `255ae95e1b07df170a2019829d1cb86f3784e5cf` |
| #27 | skill packaging workflow | `054286da4b0ae6393a01d2d3e5ca651a657b65bf` |
| #29 | creative CI and thinking core | `302712bde01a6c58915f22d5003121e53c292a59` |
| #30 | code drawing master | `1dbc40b0eb773f5d6c15d80ad6bf423792ed817c` |
| #31 | community sources scout | `6f96d78e471991de6f71e7be654feab30c987b7d` |
| #32 | creative motion powers | `403919086874a0aa937ab3a64c0f111817c9ea6e` |
| #34 | portable motion | `365aea48cf9714dd7fc4c5912062e9a4fc254d8d` |
| #35 | system design and Python readiness | `79cb118a2dd25aa4c88a1d94ae276467c5c57094` |

## Validation
- Main workflows: `.github/workflows/ci.yml` and `.github/workflows/skill-package.yml` are retained instead of rolling back their accumulated tests.
- Run the CI workflow plus the added `tests/test_reference_fetch_security.py` through Python unittest discovery.
- After successful CI and merge to main, cross-check GitHub PR states to verify integration detection.
