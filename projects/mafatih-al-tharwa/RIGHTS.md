# RIGHTS.md — footage provenance

All b-roll comes from films that archive.org lists under **Public Domain** (`licenseurl: http://creativecommons.org/licenses/publicdomain/`), mostly from the Prelinger Archives collection. The license field was read from each item's metadata API (`https://archive.org/metadata/<id>`) on 2026-10-18. Shots were re-graded, upscaled and cropped to fill the 9:16 frame; no audio from these films is used.

| archive.org item | title | year | clips used | seconds on screen | SHA-256 of downloaded file |
|---|---|---|---|---|---|
| [SteelASy1936](https://archive.org/details/SteelASy1936) | Steel: A Symphony of Industry | 1936 | 9 | 35.6 | `976b3b6620f7f9170b913970942a8be68d157acbc6e78c6dbff6ebd0076d4e19` |
| [DynamicA1956](https://archive.org/details/DynamicA1956) | The Dynamic American City | 1956 | 35 | 135.9 | `8172f870b4201142b4a8748215907a6794789f9d0e7a50ec82e2b6394ca0e4ef` |
| [Usingthe1947](https://archive.org/details/Usingthe1947) | Using the Bank | 1947 | 32 | 137.5 | `0968e5aad15f7a5b2704fd1e51c2765fb1945a77276361c6f21faa10c261905f` |
| [WhatIsMo1947](https://archive.org/details/WhatIsMo1947) | What Is Money? | 1947 | 12 | 54.5 | `f76fc9cb8063fd8d65d5e6ced8f0d6fcd25f8095637919687b2d1b1e6bda8a42` |
| [Successi1928](https://archive.org/details/Successi1928) | Success in Business | 1928 | 52 | 185.2 | `749aa6483109a9c6c1f94249ed84d30c3be424aff9e37f39a5045b80055aa9d3` |
| [MakingBo1947](https://archive.org/details/MakingBo1947) | Making Books | 1947 | 26 | 84.9 | `04485da7d81f7d1fc96b362db812ccb28dacc51cbcb822ea60d0db80d531c332` |
| [copper_mining_and_smelting](https://archive.org/details/copper_mining_and_smelting) | Copper Mining and Smelting | n.d. | 2 | 6.6 | `1f82b813edb9084d8678d33672b83cdbb0f54a7a9274c634a80e0d54f4eff857` |

Fonts (OFL 1.1, licences in `src/fonts/`): Reem Kufi, Cairo, Amiri.

Voice: the user's own recording, muxed unaltered (AAC stream copied as-is).

Shot-level cut list (source film, source in-point, timeline in/out): `data/cuts.json`. Fade/dissolve trims per shot: `data/shot_trims.json`.
