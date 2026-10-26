# blue_hour — "الطريق في الساعة الزرقاء" (8 s, 1080p30, a 1 s long exposure per frame)

The book lessons in one shot: ridges of the same rock at 0.7/1.4/2.6/4.5 km turned blue and pale by air alone (Gurney's
aerial perspective, fog colour = horizon sky), sodium lamps against blue hour, upfacing shadows cool and downfacing warm
(skyBounce), cars as light trails and stars as arcs (Night Photography: lighten-stacked long exposure), a slow push-in at
road height (Veo shot language), AgX tone curve so lamp and taillight hues survive the highlights.

    python motion.py new blue_hour --3d --seconds 8                      # then copy index.html and src/main.js here
    python ambience.py projects/blue_hour/assets/ambience.wav --seconds 8 --chords 0:D,4:A --whoosh 2.2,5.6 --sea 0
    python motion.py bundle projects/blue_hour
    python motion.py render projects/blue_hour --engine studio --blur 16 --shutter 30 --stack lighten
    python motion.py inspect out/blue_hour.mp4
