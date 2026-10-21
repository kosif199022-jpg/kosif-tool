# TEST REPORT — «خلّي ولي مدير ٢» كرتون (Plan B «كرتون العربية»)

| Check | Target | Measured | Result |
|---|---|---|---|
| Frame | 1080×1920, 9:16 | 1080×1920 | ✅ |
| fps / frames | 30 | 30 fps, 1,772 frames | ✅ |
| Duration | = audio (59 s) | video 59.067 s / audio 59.000 s | ✅ |
| Audio | original, untouched | stream copy, MD5 `cd64337a…` source = output | ✅ |
| Real footage | none | 100% drawn on canvas (characters, car, street) | ✅ |
| Lip-sync | mouth follows the voice | mouth opening driven by the 30 fps loudness envelope of the active singer | ✅ |
| Who sings | matches the source | boss 0–8.82 s (checked on source frames), young man 8.82–59 s | ✅ |
| Beat | head bob and notes on the beat | 105.5 BPM grid from spectral flux | ✅ |
| Lyrics | readable, synced | faster-whisper large-v3 + manual clean-up of the pidgin dialect; words pop in on onset | ⚠️ some words in the dialect are best-effort |
| Visual QA | frames checked | 8-frame preview, 3 gesture sheets, 10 frames from the delivered MP4 | ✅ |

## Credits and licences
- Sound: «خلّي ولي مدير ٢» by @mo7moneam (Mohamed Moneam), used under TikTok's sound-reuse permission as stated by the user; credited on screen.
- Characters: original caricatures drawn for this film, inspired by the two personas.
- Fonts (SIL OFL 1.1): Lalezar, Marhey, Reem Kufi. Emoji: Noto Color Emoji (OFL).
