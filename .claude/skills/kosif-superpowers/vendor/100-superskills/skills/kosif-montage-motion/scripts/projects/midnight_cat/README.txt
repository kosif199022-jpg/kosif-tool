MIDNIGHT / KOSIF MOTION

A hand-authored, silent, 12-second cinematic vector short.
1280 x 720, 24 fps, H.264 / yuv420p.
No paid generation, external images, fonts, packages, or network requests.

Open midnight-cat.html in a browser. It contains the complete SVG scene and
animation JavaScript. Play/pause, replay, seek and reduced-motion support
are included. Put midnight-cat.mp4 beside it to enable the download link.
window.render(seconds) renders a deterministic frame; window.setPlaying(bool)
controls playback. The animation stops at 12 seconds. It is not a seamless loop.

Story: A tabby follows a luminous butterfly through a rain-soaked neon city,
anticipates a puddle, leaps, lands with a splash, and looks back toward us.

Scene: Multiple parallax layers, camera track and push-in, detailed city
facades, fire escapes, utility wires, awnings, neon signs, ambient halos,
wet reflections, raindrops, expanding puddle ripples, splash particles,
four individually articulated legs, breathing, ear/head motion, eye blinks,
swaying striped tail, collar pendant and flapping butterfly.

Rebuild: node build.cjs
Validate: node test.cjs && node player-test.cjs
Render: XDG_CACHE_HOME=$PWD/.cache python3 render.py
Encode: ffmpeg -framerate 24 -i frames/%04d.png -c:v libx264 -preset slow \
  -crf 18 -pix_fmt yuv420p -movflags +faststart midnight-cat.mp4
Rendering requires installed librsvg, Cairo and ffmpeg. JavaScript requires
Node only for rebuilding; the HTML is standalone.

This is stylized 2.5D vector artwork, not photorealistic 3D, and has no audio.
The video was decoded for frame inspection. Player interactions were tested
with a deterministic JavaScript harness; a browser launch was unavailable.
