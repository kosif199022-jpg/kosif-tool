# KOSIF Full Body Animator

Independent 2D renderer reusing KOSIF Paint and two-bone IK.

Actions: walk, run, wave, smile, blink, nod. Input: JSON with schema kosif.fullbody.v1, a character and ordered actions. Each action has a duration and either a time or a word cue. Walk/run do not overlap. Word cues require timestamps from an externally verified word-alignment JSON; the bundled word data is synthetic for testing.

Supported outputs: PNG, SVG (five editable layers), GIF, MP4 (H.264). Optional AAC input for MP4 is stream copied; packet hashes are checked after export.

From repository root:
python .claude/skills/kosif-superpowers/scripts/character_fullbody.py doctor
python .claude/skills/kosif-superpowers/scripts/character_fullbody.py render --scene .claude/skills/kosif-superpowers/templates/fullbody-demo.json --words .claude/skills/kosif-superpowers/templates/fullbody-demo-words.json --fps 24 --output fullbody.mp4

Run tests with:
python -m unittest discover -s .claude/skills/kosif-superpowers/evals -p test_character_fullbody.py -v

Limits: 128-1280 pixels, 30 seconds, 100 actions and 600 frames. Walking uses approximate contact, not true foot locking. No 3D mocap, speech recognition, accurate lip-sync or editor timeline yet.

Local Windows result October 19 2026: 14 tests passed.
