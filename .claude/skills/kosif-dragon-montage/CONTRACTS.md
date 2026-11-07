# Dragon Montage — shared contracts (v1)

Every station reads and writes plain JSON files inside one job folder. A station
never reaches into another station's internals; it only reads the files below.
All files carry `"schema"` and are validated by `scripts/dm_common.py`.

Job folder layout (`out/dragon-montage/<job>/`):

```
job.json            kosif.dm.job.v1       inputs, task text, options, station status
analysis.json       kosif.dm.analysis.v1  station 1 (العين الأولى)
brief.json          kosif.dm.brief.v1     station 2 (يفهم المطلوب)
concepts.json       kosif.dm.concepts.v1  station 3 (يفكر بإبداع)
look.json           kosif.dm.look.v1      station 4 (يختار الذوق)
edl.json            kosif.dm.edl.v1       station 5 (يكتب المونتاج)
render/             station 6 outputs: final.mp4, captions.srt, project.fcpxml …
render.json         kosif.dm.render.v1    station 6 receipt
review.json         kosif.dm.review.v1    station 7 (يتفرج وينقد)
receipts.jsonl      one line per tool call: {station, tool, argv, rc, sha256_out, seconds}
report.md           human report (Egyptian Arabic), honest counts
```

Times are seconds (float, 3 decimals). Clip ids are `c01`, `c02` … in input order.
Shot ids are `<clip>-s001`. Paths inside JSON are relative to the job folder when
they point inside it, absolute otherwise.

## kosif.dm.analysis.v1
```json
{"schema":"kosif.dm.analysis.v1",
 "clips":[{"id":"c01","path":"/abs/in.mp4","duration":62.4,"width":1920,"height":1080,
   "fps":29.97,"has_audio":true,"loudness_lufs":-19.2,
   "shots":[{"id":"c01-s001","start":0.0,"end":4.2,
     "quality":{"sharpness":0.71,"exposure":0.55,"shake":0.12,"score":0.68},
     "faces":1,"motion_energy":0.33,"color":{"mean_rgb":[0.41,0.38,0.33],"saturation":0.42},
     "thumb":"analysis/c01-s001.jpg"}],
   "words":[{"w":"اهلا","start":0.32,"end":0.61,"conf":0.93}],
   "silences":[{"start":12.0,"end":13.4}],
   "energy":[{"t":0.0,"rms":0.12}]}],
 "music":{"path":null,"bpm":null,"beats":[],"downbeats":[]},
 "contact_sheet":"analysis/contact.jpg",
 "tools_used":["ffprobe","cinema_lab.scenes","faster-whisper"],
 "missing":["librosa"]}
```
Missing optional tools never crash a station: the field is empty and the tool is
listed in `missing`.

## kosif.dm.brief.v1
```json
{"schema":"kosif.dm.brief.v1","task":"<owner text>","one_truth":"…","audience":"…",
 "platform":"reel|story|youtube|square|landscape","aspect":"9:16","target_seconds":45,
 "feeling":"tense|warm|epic|playful|calm|inspiring|sad|funny","energy":0.0-1.0,
 "language":"ar-eg","content_type":"talking-head|travel|product|interview|event|montage",
 "must_keep":["…"],"avoid":["…"],
 "frameworks":[{"id":"first-principles","source":"dragon-mind","output":"…"}]}
```

## kosif.dm.concepts.v1
```json
{"schema":"kosif.dm.concepts.v1",
 "concepts":[{"id":"A","title":"…","logline":"…","arc":["hook","setup","turn","payoff","cta"],
   "hook":{"text":"…","formula":"hooks_ar#7","score":0.82,"first_seconds":3},
   "rhythm":"on-beat|speech-led|slow-burn","style_hint":"…","risks":["…"]}],
 "decision":{"chosen":"B","matrix":[{"id":"A","scores":{"hook":4,"clarity":3,"novelty":5,"fit":4},"total":16}],
   "why":"…","council":{"used":"llm_council","verdict":"…"}},
 "premortem":["…"]}
```
Rule: the three concepts must differ in arc or rhythm, not only in wording.

## kosif.dm.look.v1
```json
{"schema":"kosif.dm.look.v1","style_id":"neon-tech","style_source":"catalog|library500|atlas86|kmx",
 "grade":{"id":"cinematic","engine":"look_pipeline","lut":null},
 "transitions":[{"id":"cut"},{"id":"xfade-fade","seconds":0.25}],
 "camera":[{"id":"punch-in","scale":1.08}],
 "captions":{"style":"karaoke|punchy|clean|none","font":"Cairo","position":"lower|center"},
 "music":{"mood":"tense","bpm_range":[90,120]},
 "why":"…"}
```
Transition ids map to ffmpeg xfade names (`fade`, `wipeleft`, `slideup`, `circleopen`, …) or `cut`.

## kosif.dm.edl.v1 (the one canonical edit decision list)
```json
{"schema":"kosif.dm.edl.v1","width":1080,"height":1920,"fps":30,
 "events":[{"id":"e001","clip":"c01","src_in":12.30,"src_out":15.10,"rec_in":0.0,
   "speed":1.0,"transition_in":{"id":"cut"},"camera":{"id":"punch-in","scale":1.08},
   "reason":"hook: strongest line, face visible, quality 0.81","shot":"c01-s004"}],
 "audio":{"music":{"path":null,"gain_db":-18,"duck_under_speech_db":-10},"voice_from":"events",
   "target_lufs":-14},
 "captions":{"enabled":true,"style":"karaoke","words_from":"analysis"},
 "grade":{"id":"cinematic"},
 "duration":44.8}
```
Every event has a `reason`. Converters to/from `kosif.timeline.v1`,
`kosif.edl.v1` (cinematic_cut_planner), pro-video-editor EDL JSON and
`nle_export.py` live in `scripts/dm_edl.py`.

## kosif.dm.render.v1
```json
{"schema":"kosif.dm.render.v1","final":"render/final.mp4","extra":["render/final_1x1.mp4"],
 "captions":"render/captions.srt","project":"render/project.fcpxml",
 "verify":{"tool":"verify_video","pass":true,"lufs":-14.1,"true_peak":-1.2},
 "events_out":[{"id":"e001","out_in":0.0,"out_out":2.5}],"muted":["e004"],"warnings":["…"]}
```
Timing has one source of truth: `dm_edl.reflow`. The render snaps each event to whole frames around its
reflowed `rec_in`, and `events_out` gives the exact span of each event in final.mp4, in seconds. A crossfade
makes neighbouring spans overlap. Review maps video times to events with this field. A `src_out` past the
clip's end is clamped, or the event is dropped, and a line is added to `warnings`. Per event, `mute` gives
silence and `grade` replaces the global grade. `audio.limiter_tp` sets the true-peak ceiling.

## kosif.dm.review.v1
```json
{"schema":"kosif.dm.review.v1","round":1,
 "checks":[{"id":"hook-in-3s","pass":true,"evidence":"…"},
   {"id":"dead-air","pass":false,"at":[21.3,23.0],"evidence":"silence 1.7s"},
   {"id":"cuts-on-beat","pass":true,"ratio":0.82}],
 "fixes":[{"event":"e007","action":"trim|drop|swap|retime|regrade","detail":"…"}],
 "frames":["review/r1_f01.jpg"],"verdict":"ship|fix","score":0.0-1.0}
```
`fixes` are applied by `dm_direct.py --apply-review` then re-rendered (max 3 rounds).
Actions: `trim|drop|swap|retime|regrade|extend|add`. `extend` grows one event (`seconds`; b-roll inside its
shot, speech to the next word gap); `add` is global (`"event":"*"`, `"target":"timeline"`, `seconds`) and
re-fills the cut toward `brief.target_seconds` — a duration-under-target fix is never a trim. After every
apply-review the director re-fills to within 8% under target from unused candidates (never what a review
dropped: `edl.meta.dropped_ranges`). Speech events are judged by phrase pacing
(`editor_mind.pacing_by_kind.speech`, 1.5–9 s, cut only between words), b-roll by the feeling/energy pace.
Hook-capable opening roles live in `editor_mind.hook_roles` (think, direct and review read the same list);
a hook swap on talking content picks a spoken line. Caption safe band: `caption_styles.json → safe_area`.

## Honest counting
Report three numbers: `consulted` (cards/frameworks read), `ran_on_your_video`
(tool calls in receipts.jsonl whose inputs are the owner's media), `missing`
(tools not installed). Never call a consulted card "executed".
