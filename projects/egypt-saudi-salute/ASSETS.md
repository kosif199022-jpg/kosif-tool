# ASSETS.md

| Path | Source | Licence / rights | Modifications |
|---|---|---|---|
| assets/photo.png | Supplied by the user | User's own | none |
| assets/song.mp3 | Supplied by the user (metadata: melkosif57, made with Suno) | User's own | none — muxed unaltered in timing (AAC encode for MP4) |
| assets/photo@2x.jpg | Derived from photo.png | — | EDSR ×2 super-resolution (model: Saafke/EDSR_Tensorflow) |
| assets/fg.png | Derived | — | BiRefNet-portrait segmentation via rembg |
| assets/bg.jpg, plate@2x.jpg | Derived | — | People and flags removed (OpenCV inpaint + sky fill) |
| assets/flagmask.png, flagfill@2x.png | Derived | — | Colour mask; flags extended behind heads |
| assets/fonts/ArefRuqaa-*.ttf, Cairo.ttf, Amiri-Bold.ttf, ReemKufi.ttf | github.com/google/fonts | SIL Open Font License 1.1 | renamed only |
| Icons, map, ornaments, wave, end card | Drawn in code for this film | Original | — |

No third-party footage, music or prompts were used. Nothing was downloaded beyond fonts and model weights.
