---
name: kosif-social
description: "KOSIF Social — the social-media layer for every video and campaign, Arabic-first and measured: a post pack per platform (caption, hashtags, YouTube title/description, CTA, first comment, cover text, alt text) linted against each platform's limits; Instagram/TikTok/LinkedIn carousels rendered as PNG + PDF with correct Arabic shaping; a content calendar (CSV, Excel, Markdown, calendar .ics) built from content pillars; the best posting time computed from the account's OWN analytics export; A/B tests planned with the sample size they need and read with a significance test. Never posts, schedules on a platform or signs in. Use after any reel/video for 'caption', 'hashtags', 'post', 'carousel', 'content plan', 'posting schedule', 'best time to post', 'A/B'. Arabic: كابشن، وصف، هاشتاجات، بوست، كاروسيل، سلايدات انستا، خطة محتوى، جدول نشر، أحسن وقت للنشر، تجربة نسختين، سوشيال ميديا."
argument-hint: "[الفيديو أو الموضوع + المنصات]"
---

# KOSIF Social — طبقة السوشيال لكل فيديو وحملة

Talk to the user in plain Egyptian/Gulf Arabic like the rest of KOSIF. Every number comes from the tool, not from
memory. **Nothing is ever posted or scheduled on a platform from here** — the user publishes; we prepare and check.

Engine: `python ~/.claude/skills/kosif-social/scripts/social.py <command>` (PC) — on claude.ai run it from the
uploaded skill folder. Needs Python 3.10+; Pillow + arabic-reshaper + python-bidi for carousels; openpyxl for the
Excel calendar (CSV/MD/ICS work without it); fontTools improves font fallback.

## 1. Post pack — after every video (the default job)
```bash
python social.py pack FILM.mp4 --platforms tiktok,reels,shorts --topic "…" --out outputs/NAME.post.json
# fill every post in the JSON (rules for each platform are inside it under _rules) — then:
python social.py check outputs/NAME.post.json        # exit 0 = ready; exit 1 = errors listed per platform
```
- `pack` probes the real file and lists what does not fit each platform (length, ratio, resolution) under `_fit` —
  fix those with `kmotion platforms FILM --to …` / `kmotion trim` before writing captions.
- Write each platform its own text — never one caption pasted everywhere. Follow `references/copy-guide.md`
  (hook in the first line, one CTA, hashtag mix, Arabic hashtag rules, per-platform tone).
- `check` enforces: caption/description length (X weighted: emoji 2, URL 23), YouTube title ≤ 100 (warns > 70),
  hashtag maximum (Instagram 5, YouTube > 60 voids all, Threads 1), hashtag form (no spaces, symbols, diacritics,
  digits-only), duplicates after Arabic normalisation (أ/ا، ة/ه، ى/ي، تشكيل), hook cut before "more", dead links on
  TikTok/Instagram, missing CTA, Instagram alt text, and the video's fit.
- Deliver the pack as a readable Arabic block per platform (copy-ready) + the JSON path. Say the limits are as of
  `AS_OF` and must be checked before a major launch.

## 2. Carousel
```bash
python social.py carousel spec.json --out outputs/NAME_carousel      # slide_01.png … + carousel.pdf + contact_sheet.jpg
```
spec: `{"platform": "instagram", "size": "1080x1350", "brand": {"bg","fg","accent","handle","font","font_bold"},
"slides": [{"title","body","kicker"?, "image"?}], "swipe"?}` — example `examples/carousel.json`.
- Arabic is wrapped in reading order, then shaped; a line with Latin/@handle falls back to a font that has it.
- Titles shrink to ≤ 4 lines, bodies to fit; overflow, too many slides (Instagram 20, TikTok photo 35, X 4) and
  missing images are reported in `warnings` — fix them, don't ship them.
- LinkedIn takes the PDF as a document post. Instagram 3:4 grid: `"size": "1080x1440"`.
- Always LOOK at `contact_sheet.jpg` (and one full slide) before delivering.
- Story for the slides: `super:arabic-copywriting` / `super:storytelling-scripts`; for designed covers and
  thumbnails beyond text slides: `super:thumbnail-social-graphics`.

## 3. Content calendar
```bash
python social.py calendar plan.json --out outputs/calendar      # calendar.csv/.xlsx/.md/.ics
```
plan: `{"start": "YYYY-MM-DD", "weeks": 4, "days_off": ["fri"], "platforms": {"tiktok": 4, "reels": 3},
"pillars": [{"name", "weight"}], "formats": {platform: [...]}, "slots": {platform: "HH:MM" | [..]}, "ideas": [...]}`.
- Pillars are spread by weight (smooth round-robin), posts spread evenly across the allowed days, deterministic.
- Without `slots` the times are labelled as a starting assumption. With the account's export, run `besttime`
  first and pass its hours as `slots`.
- The `.ics` imports into Google/Outlook calendar as reminders — it does not publish anything.
- Ideas: `super:ideation-100-ideas`, `super:reels-shorts-factory` (pillars → hooks → scripts),
  `super:youtube-channel-strategy` (YouTube), `super:market-competitor-research` (what competitors post).

## 4. Best time to post — from the account's own data only
```bash
python social.py besttime export.csv [--metric views] [--date-col "Post time"] [--block 3]
```
The user exports their analytics (TikTok Studio, YouTube Studio, Meta Business Suite → CSV) and attaches it; we
never sign in to fetch it. Median per weekday × 3-hour block (≥ 2 posts per cell), vs the overall median. Fewer
than 8 posts → it says so and keeps the default slots. Report it as a correlation to test, not a law.

## 5. A/B (hooks, covers, titles)
```bash
python social.py abplan ab.json --out outputs/ab      # impressions needed per variant + ab_results.csv to fill
python social.py abread outputs/ab/ab_results.csv --need N
```
One variable at a time, same time slot, alternate order; no verdict before each variant reaches the sample size
(peeking fakes winners). `abread` gives rates, lift, 95 % CI of the difference, z and p. Deeper design:
`super:ab-testing-experiments`.

## 6. How it joins the rest of KOSIF
- `/kosif-video` and `kosif-one` end every social video with §1 (post pack + check) when the video is for a platform.
- `kosif-one` route `social_content` = this skill + the 100 Super Skills playbooks above.
- Platform files (re-encoded per platform) still come from `kmotion platforms`; this skill writes the words around them.

## Limits of this skill — say them plainly
- No posting, scheduling on platforms, DMs or comment replies (outward actions need the user, every time).
- No live analytics or live trends: only what the user exports or pastes.
- Platform limits change; `limits` prints the table with its date.
