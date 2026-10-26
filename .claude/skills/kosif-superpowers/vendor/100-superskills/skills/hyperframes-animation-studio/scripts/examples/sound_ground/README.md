# sound_ground — "الصوت يرسم الأرض" (10 s, 1080p30)

The score draws the land: the spectrogram is a lava canyon, kicks throw sparks and squash a chrome orb, and the world runs
on the tape clock, so a tape stop freezes it while the camera orbits (bullet time) and the picture turns cold silver.

    python motion.py new sound_ground --3d                      # then copy index.html, src/main.js, assets/score.json here
    python score.py projects/sound_ground/assets/score.wav --spec projects/sound_ground/assets/score.json   # tape stop at 6 s
    python motion.py channels projects/sound_ground/assets/score.wav --out projects/sound_ground/src/channels.json
    copy the spectrogram.png and spectrum_height.png it writes next to channels.json (src/)
    python motion.py bundle projects/sound_ground
    python motion.py render projects/sound_ground --engine studio --blur 4
    python motion.py inspect out/sound_ground.mp4 --allow 6.6-7.3
