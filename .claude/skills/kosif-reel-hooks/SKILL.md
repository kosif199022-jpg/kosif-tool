---
name: kosif-reel-hooks
description: >-
  Write an Instagram Reel or short video script from one raw idea, in Egyptian
  Arabic, MSA or English - three hooks off the Arabic hook library, scored by a
  local tool, the spoken script, the on-screen cards and a timed beat sheet,
  then a humanizer pass before the user sees it. Use when the user wants a
  Reel, a hook, «اكتبلي ريل عن», «هوك», «سكريبت فيديو قصير», «أقول إيه في
  الفيديو», a voiceover, or is about to record without a first line.
---

# KOSIF Reel Hooks - من فكرة لريل حد يكمّله

One idea in, one Reel script out: scored hook, script, on-screen cards and a
timed beat sheet. The tools are stdlib Python, offline, no keys, and they read
Arabic (Egyptian and MSA), English and mixed lines, Arabic-Indic digits
included.

```bash
T=.claude/skills/kosif-reel-hooks/scripts/reel_tools.py
python3 $T hook hooks.txt                       # rank hooks, one per line
python3 $T hook --hook "سطر واحد" --screen "كارت الشاشة"
python3 $T beats script.txt --target 30         # timed beat sheet
python3 $T clean draft.txt --fix --out clean.txt   # humanizer pass
```

Add `--json` to any command for machine output. Run from the repo root.

## Before you write

1. **Voice.** If the user has a voice file (`out/voice.md` or one they point
   to), read it. If not, ask for two or three of their own reels or captions
   and infer how they talk. A script in the wrong voice is useless because they
   have to say it out loud.
2. **The one true thing.** A Reel needs one specific, true fact: what happened,
   to whom, what it cost or returned. If the idea is thin, ask one batched
   question for it. Never pad.
3. **The library.** Read `data/hooks_ar.json`: 16 Egyptian hook formulas, each
   with a template, an example, the on-screen card, what it is for and the trap
   that ruins it.
4. **Evidence beats defaults.** If the user ran `kosif-instagram-discovery` or
   `kosif-instagram-video-research` for this niche, use the formulas that show
   up in those references over the library order.

## The shape

```
0:00 - 0:03   الهوك     the claim. Spoken line and card written separately; motion in frame 1.
0:03 - 0:07   الرهان    why the viewer should care. One line.
0:07 - ...    الجسم     one idea per beat; the frame changes every beat.
آخر 3 ثواني   التسليم   deliver what the hook promised, then one ask.
آخر جملة      اللوب     repeat a word from the hook so the replay lands clean.
```

Working length is 15 to 45 seconds.

## The loop

1. **Three hooks, three formulas.** Pick three formulas that fit the idea and
   write the spoken line and the card for each. Not three rewrites of one.
2. **Score them** with `hook`. Show the ranking. If the top one is under 50,
   there is no hook yet; editing words will not fix it, find the specific fact.
3. **Write the script** on the winner, the way the user talks: short lines,
   spoken dialect, nothing they would need to rehearse.
4. **Time it** with `beats --target <seconds>`. Fix every flag: hook past 3 s,
   a beat over 4 s, three beats in a row with nothing concrete, no loop, length
   off target by more than 20%. Re-run until clean. Arabic defaults to 140
   words a minute, English to 165; pass `--wpm` once the user has timed
   themselves.
5. **Humanize** with `clean --fix`. It strips hidden characters and long dashes
   and lists the written-Arabic tells («في عالم اليوم»، «لا شك أن»، «دعونا»،
   «رحلة»، «ليس فقط... بل») for you to rewrite by hand.
6. **Print the block:** the script in a fenced block, the cards as a separate
   list with timings, then:

```
الريل جاهز
الهوك:     #1 اعتراف بالتكلفة، 84 STRONG
المدة:     28 ثانية، 11 بيت، 140 كلمة/دقيقة
الشاشة:    6 كروت
البشرية:   2 اتشالوا، 92 PASS
```

7. **Never publish.** This skill writes. The user shoots and posts.

## On-screen cards

- Six words or fewer per card (`--screen` checks it).
- The hook card is up at frame 1.
- Safe zone on 1080x1920: nothing above y=230 or below y=1440, keep the right
  230 px clear. The caption, action rail and audio strip sit on top of the rest.
- Burn in captions for the body; most people watch muted first. For Arabic
  text follow `playbooks/arabic-typography.md`.

## Rules

- One idea per Reel. Two ideas means two Reels; say so.
- Numbers over adjectives. «٤٠٠٠ جنيه» beats «فلوس كتير».
- No intro: no greeting, no «في الفيديو ده», no name, no logo sting.
- One ask at the end: a comment keyword, a save, or a follow.
- **Never fabricate** metrics, clients, revenue or results under the user's
  name. If a number is needed and unknown, leave `{{رقمك}}` and flag it.

## What the score is and is not

It measures five text properties: length, a concrete marker, something at
stake, the heavy word near the front, and a viewer addressed. It catches
greetings, preambles, vague hooks and long hooks. It does not predict views:
the face, the edit, the audio and the feed decide that. Trust the retention
graph over the number.

## Credit

The method (scored hook panel, beat sheet, humanizer pass, safe zone) is
adapted from Jake Schincariol's MIT-licensed
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
Its scripts read Latin letters only, so an Arabic hook scores zero there. The
code, lexicons and hook library here are new and Arabic-first; no upstream code
or text is copied. See `THIRD_PARTY_NOTICES.md`.
