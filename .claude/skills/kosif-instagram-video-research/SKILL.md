---
name: kosif-instagram-video-research
description: Search public Instagram Reel references by content/topic and known creator, expand Arabic-to-English queries, optionally ingest public search index via Brave Search API, and keep a ranked evidence-labelled SQLite library. No Instagram scraping or rights bypass.
---

# KOSIF Instagram Video Research — بحث ريلز إنستجرام بالموضوع

**Part of KOSIF Superpowers + reference input for KOSIF Infinite Matrices.**

## Registered references
Use `data/creator_registry.json` as the ground-truth source registry:
- [@asirgokerr](https://www.instagram.com/asirgokerr/) — added from user-provided URL; nature/travel themes mentioned in independent public credits. Direct profile/video inspection **not verified**.
- [@brkn.land](https://www.instagram.com/brkn.land/) — added from user-provided URL; indexed captions mention clouds, dreamscapes, flowers, coastal scenery, sunsets and night skies. Style/technical production methods **not verified**.

## User intent
Respond to prompts such as «ابحث عن فيديوهات شلال وسط الغابة», «عايز ريلز غيوم من brkn.land», «اختار مرجع سينمائي عند الغروب». The goal is **content discovery and visual inspiration**, not downloading or copying third-party content.

## Executable workflow
```bash
python .claude/skills/kosif-instagram-video-research/instagram_research.py sources
python .claude/skills/kosif-instagram-video-research/instagram_research.py plan 'غروب وسط السحاب'
python .claude/skills/kosif-instagram-video-research/instagram_research.py search 'غيوم' --accounts-only
BRAVE_SEARCH_API_KEY=... python .claude/skills/kosif-instagram-video-research/instagram_research.py search 'سماء ليلية'
python .claude/skills/kosif-instagram-video-research/instagram_research.py import results.json
python .claude/skills/kosif-instagram-video-research/instagram_research.py find 'غروب'
```

A search without `BRAVE_SEARCH_API_KEY` returns clickable web search and in-app Instagram search URLs **only**. This is NOT a list of confirmed videos. Optional API calls use Brave's documented public-web-index API, not undocumented Instagram internal endpoints.

## Evidence hierarchy
- `search_links_not_verified_hits`: only suggested query URLs.
- `public_search_index_unverified`: found in a public search result; video, author and runtime availability unverified.
- `url_only_unverified`: manually supplied media link without video-frame analysis.
- `verified_by_authorized_review`: future level only if the reviewer actually opens source content or receives licensed frames.

Do not claim direct account access, creator ownership, video accessibility, generation method, or music from text snippets.

## Search design
1. Parse scene attributes: subject, place, light, camera motion, aesthetic, time period.
2. Generate multilingual variants (Arabic + English) and scoped queries (all public Reels or selected creators).
3. Search via public index or return browser links; prefer direct original Reel URLs.
4. Canonicalize and deduplicate safe Instagram links, preserving source and evidence.
5. Rank indexed metadata; disclose that ranking is lexical and content incomplete.
6. Optionally, with lawful access/permission, analyse user-provided frames/audio and record verified S/O/F/t/M mechanisms for Infinite Matrices. Never infer mechanisms from a caption alone.

## Safety and portability
No login automation, account cookies, private-account access, arbitrary scraping, DRM circumvention, media downloader or mass mirror. API quotas/fees belong to service provider. Keep keys in environment; never commit tokens. Static references do not prove active connectivity.


## Update 2026-10-24 — evidence-based creative mechanism mining

The two creator profiles are already registered in the existing `data/creator_registry.json` (canonical source of truth). Do not create a duplicate registry. The user supplied these handles for discovery; no claims about their unseen Reels are warranted.

**Multilingual creative research:** `expand()` supports Arabic terms for whiteboard, motion, 3D, compositing, particles, cinematic media, video editing, and corresponding English/Turkish terms. Compound topics such as `موشن سبورة` retain both concepts in the translated query.

**Controlled provenance bridge to Infinite Matrices:** A Reel surfaced via public web index is **not** reviewed. A human reviewer can add observed mechanisms only after inspecting the actual video through authorized means:

```bash
# First index a real public Reel URL found through the profile, search result or user.
python .claude/skills/kosif-instagram-video-research/instagram_research.py add \
 "https://www.instagram.com/reel/REAL_SHORTCODE/" \
 --title "Actual verified title" --author "asirgokerr"

# A real reviewer explicitly attests to mechanism observations:
python .claude/skills/kosif-instagram-video-research/instagram_research.py review \
 "https://www.instagram.com/reel/REAL_SHORTCODE/" \
 --reviewer "researcher" \
 --tags "motion,cinematic" \
 --mechanisms "path reveal,parallax" \
 --observations "Describe the actually observed shots, timing, causal relationships and evidence."

# Search now includes observed mechanism tags, not just captions:
python .claude/skills/kosif-instagram-video-research/instagram_research.py find "parallax"

# Machine-readable evidence input for KOSIF Infinite Matrices:
python .claude/skills/kosif-instagram-video-research/instagram_research.py export-reviewed \
 "/tmp/kosif-reviewed-reel-references.json"

python -m unittest discover -s .claude/skills/kosif-instagram-video-research/tests -v
```

The `reviewed_reels` SQLite table is separate from low-confidence public snippets, preserving human annotations on re-index. These exported observations become **research inputs**, not instantly validated renderer primitives; a proposed mechanism still requires independent reconstruction and A/B evaluation. Never auto-upgrade verification from search snippets or creator names. No automated login, video downloading, DRM bypass, bulk mirroring, copying others' creative works or unsolicited credentials.

**Status / verification:** the Python changes and offline regression tests are committed. Live Instagram access, Brave-key presence, human video inspection, and successful visual reconstruction have not been demonstrated by the code alone.
