# Atlas core-work pass — 2026-11-07

تمريرة على الأطلس (14,793 مهارة) مركّزة على شغل المالك: المونتاج والريلز والموشن، الكتابة العربية والهوكس، التفكير، التنين الأسود، والمواقع الحية. ثمانية مسارات متوازية قرأت كل SKILL.md كنص خامل، ودمجت المنهج بكلامنا: ترقية كارت موجود أولًا، وكارت جديد فقط لفجوة حقيقية. لا كود اتنسخ أو اتشغّل، ولا ملفات اتنسخت في vendor.

| المسار | قُرئ بالكامل | كروت جديدة | ترقيات | مُستبعد بعد القراءة |
|---|---|---|---|---|
| المواقع الحية والواجهات (frontend) | 48 | 2 | 17 | 23 |
| الصور والمخططات (image) | 47 | 2 | 12 | 22 |
| التسويق والنمو (marketing) | 40 | 12 | 10 | 6 |
| التنين الأسود والتحقق (orchestration) | 46 | 9 | 13 | 7 |
| صناعة المهارات (skillcraft) | 64 | 4 | 11 | 18 |
| التفكير والتخطيط (thinking) | 78 | 15 | 16 | 10 |
| الفيديو والصوت (video) | 56 | 1 | 3 | 47 |
| الكتابة والهوكس (writing) | 57 | 8 | 9 | 17 |
| **المجموع** | **436** | **53** | **91** | **150** |

Ledger: covered 2,675 → 2,960 · pending 1,535 → 1,439 · excluded-review 8,020 → 7,794 (Markdown only was read for those; scripts never opened).

## New cards

| ID | Card | Track | Why it matters |
|---|---|---|---|
| ABUILD-61 | One motion language per page, with binding bans | frontend | Gives living-site and kosif-web-film builds one coherent motion grammar with checkable bans instead of an effect pile, and a reduced-motion path that is designed rather than broken. |
| ABUILD-62 | Weighted 10-point site craft scorecard, signature moment first | frontend | Turns 'is this living site good enough?' into a stated number with named gaps, and forces the one memorable moment that a web film or launch page is remembered by. |
| AMEDIA-31 | Cohesive batch photo look and portrait retouch: same values on every image, a downscaled preview gate, no generative edits on people | image | Image design and montage: stills from mixed phones/sources become one coherent set before they enter a reel, with a safety gate and no identity-altering edits. |
| ADOCS-61 | Chart and infographic critique gate before render: claim title, strongest encoding for the key comparison, still-frame test, a stated job for every motion and particle | image | Data-in-motion and explainer films: one gate that stops pretty-but-empty or misleading chart scenes before an expensive render. |
| ASTRAT-109 | Short-form channel growth plan: pillars tied to metrics, a cadence you can hold for a year, owned-audience funnel | marketing | Gives the owner a defensible plan for growing his own reels/motion channel and his clients' accounts, sized to real production capacity. |
| ASTRAT-110 | Social video performance readout: validated formulas, decision vs vanity metrics, top/bottom-3 review | marketing | Lets the owner explain to clients (and himself) why a reel worked, with numbers that survive checking. |
| ASTRAT-111 | Grounded ad-creative batch: evidence corpus, 3-5 angles, generation waves, spec gate, iteration log | marketing | Turns the owner's motion/video ad production into a repeatable, evidence-based batch process clients can approve fast. |
| ASTRAT-112 | Creative test journal: one-variable hypotheses, honest results, learnings only from patterns | marketing | Makes the owner's hook and thumbnail experiments compound into real rules instead of gut feel. |
| ASTRAT-113 | Brand-deal pricing: value-based base fee, usage/exclusivity line items, walk-away floor, disclosure | marketing | Protects the owner's income and reputation when brands pay for his reels or when he hires creators for client campaigns. |
| ASTRAT-114 | Creative-project proposal: buyer's words first, scope with exclusions, distinct options, mutual next steps | marketing | Directly helps the owner win and scope paid video/motion work without scope creep. |
| ASTRAT-115 | Client objection and stalled-deal diagnosis: real concern, own proof, one forward question | marketing | Gives the owner calm, evidence-based replies when clients push back on his video/motion prices. |
| ASTRAT-116 | Launch campaign plan with preflight gates: objective→audience→message→channel→measure, backward schedule, ordered go-live | marketing | Wraps the owner's launch films and trailers in a launch plan that actually ships on time with working links. |
| ASTRAT-117 | One-goal lock: judge every idea ON / PARTIAL / OFF and always return a sharper version | marketing | Keeps the owner's many content and product ideas pointed at the one result that matters this quarter. |
| ASTRAT-118 | Signal mining and listening digest: angles you have standing to make, plus an explicit dropped list | marketing | Helps the owner ride trends only where his voice adds something, and report audience sentiment honestly. |
| ASTRAT-119 | Bullseye channel choice: one strategy per channel, three cheap tests, then focus on one | marketing | Gives the owner a disciplined way to choose how his studio/products find paying clients. |
| ASTRAT-120 | Honest service/portfolio page: positioning sentence, one job per section, no invented proof, client handoff | marketing | Supports the owner's cinematic web films and studio site with an honest conversion structure. |
| AMIND-83 | Council verdict synthesizer: dedupe, weight, arbitrate, classify — never re-review | orchestration | Gives the Black Dragon / council one honest final verdict over many parallel reviewers, with an audit trail instead of a majority vote. |
| AMIND-84 | Ensemble rule review: overlapping rule slices across rigid parallel workers, corroboration-weighted merge | orchestration | Lets the 370+ QA checks for reels, posters and Arabic type run in parallel without silently dropping items. |
| AMIND-85 | Independent re-derivation verifier: GIVEN is not DERIVED; withhold the author's numbers and reasoning | orchestration | Makes Black Dragon 'executed/verified' tiers mean something: the checker never inherits the maker's numbers. |
| AMIND-86 | Verify the premise before dispatching a wave of parallel agents | orchestration | Stops the orchestrator from launching eight agents on a wrong count or a capability a tool does not have. |
| AMIND-87 | Cold-reader gate and fresh-walker loop for anything a stranger must act on | orchestration | Checks client briefs, captions, Arabic hooks and KOSIF tool docs with a reader who has none of the session's context. |
| AMIND-88 | Human sign-off gate with structured, countable feedback | orchestration | Turns the owner's approval of a film or poster into a gate the agent cannot mark as passed by itself. |
| AMIND-89 | Unknown-coverage review: is there evidence each risk class was even investigated | orchestration | Adds the missing 'what did we never check' line to Black Dragon's evidence tiers and delivery reports. |
| AMIND-90 | Second-opinion pipeline with an honest delta — never counterfeit a validation | orchestration | Keeps council and Black Dragon reports from showing 'verified' badges for checks that never ran. |
| AMIND-91 | Agent-session review rubric: fixed categories, verbatim quoted evidence, unclassified bucket | orchestration | Lets the owner improve Black Dragon and the skills from what runs actually did, with quotes, not impressions. |
| ACRAFT-27 | Match the instruction form to the failure, then micro-test the wording | skillcraft | Makes every rule the owner adds to kosif-superpowers or a Black Dragon brief actually change behaviour instead of adding sediment. |
| ACRAFT-28 | Design a skill's shape: invocation mode, step typing, completion criteria, growing gotchas | skillcraft | Gives kosif-superpowers families and new owner skills a repeatable structure that loads cheaply and is followed step by step. |
| ACRAFT-29 | Refactor a large skill without losing behaviour: invariant ledger, single source of truth, earned labels | skillcraft | kosif-superpowers has 5,800+ cards and many chapters; this keeps it shrinking safely instead of accumulating contradictions. |
| ACRAFT-30 | Skillify a finished session into a reusable workflow skill | skillcraft | Turns the owner's recurring reel/montage/prompt-pack sessions into reusable skills instead of re-explaining them each time. |
| AMIND-92 | Hard call with no good option: reversibility test, 10/10/10, outsider test and the pre-announcement draft | thinking | Gives the Dragon Mind a humane procedure for killing a direction, a scene or a collaboration instead of drifting. |
| AMIND-93 | Brain dump to a plan with zero loss: tag every fragment, keep the owner's voice, find the spine, park the asides | thinking | The owner thinks in bursts and voice notes; this turns them into a plan without flattening his Arabic voice. |
| AMIND-94 | Problem-first one-page brief: a condition not a solution, minimal reading, explicit Not-Doing list and a human checkpoint | thinking | Every video, film or design job starts from a brief; this makes the brief bound the work before credits and hours are spent. |
| AMIND-95 | Evidence-based retrospective: audit last time's promises, rank waste by cost, turn each lesson into repeat/change/stop | thinking | Makes the Black Dragon's after-run receipts produce changes that actually fire next time. |
| AMIND-96 | Second-brain method: atomic claim-titled notes, maps of content, PARA buckets and progressive summarisation | thinking | Gives the owner's ideas, references and lessons a home that grows into reusable creative and research capital. |
| AMIND-97 | Digest a long source into durable highlights: by theme not order, keep specifics and disagreements, claim nothing unsaid | thinking | Feeds research for scripts, hooks and explainer films with faithful, specific notes instead of vague summaries. |
| AMIND-98 | Audience feedback round: collect every response before revising, then sort convergent, divergent, single-reader and declined-with-reason | thinking | Client and audience notes on cuts and designs become one calm revision plan instead of whiplash edits. |
| AMIND-99 | Plan drift check: reopen the plan, quote its gate, park off-scope finds in a later list or a deferred-decision record | thinking | Keeps Black Dragon's long multi-step runs pointed at the owner's brief instead of attractive side quests. |
| AMIND-100 | Question scoreboard: never stall on a question — log it in one line, resolve by measurement or bypass, keep working | thinking | Lets long autonomous production runs keep moving while the owner is away, without silent guesses or unsafe publishes. |
| AMIND-101 | Cut to focus: full inventory, a grid on two real axes, a cut list that names each loss, one-sentence survivors | thinking | Cutting scenes, series ideas and deliverables is half of editing; this makes the cut explicit and honest. |
| AMIND-102 | Rehearse a difficult conversation: labelled simulation, one counterpart turn at a time, out-of-character debrief and a real plan | thinking | Prepares the owner for pricing, revision-limit and deadline conversations with clients. |
| AMIND-103 | Questionnaire for the person who knows: interview the send, not the subject | thinking | A clean client intake for film, design and ad jobs, so briefs start from the client's real knowledge. |
| AMIND-104 | Decision memo shaped like a decision: trigger and a number, the decision in one sentence, alternatives killed for specific reasons, all consequences | thinking | Owner-facing recommendations from the Dragon Mind read as decisions with costs, not balanced surveys. |
| AMIND-105 | Standalone editor brief: feel statement, chapter timeline with pacing, cut/audio/graphics rules, thumbnail and short pulls, delivery spec with QC | thinking | Directly serves the owner's montage and reel work: briefs that let him or any editor or agent cut without back-and-forth. |
| AMIND-106 | Opportunity–solution tree: one outcome, evidence-backed opportunities, three solutions each, cheap experiments | thinking | Turns 'what should I make next' for the owner's channels and products into tested bets. |
| AMEDIA-32 | Long-form tutorial outline with demo-prep checklist | video | Gives the owner a filming-ready plan for long Arabic/English tutorials so demos never stall mid-recording. |
| ACRAFT-31 | Owner voice file: measurable, quote-backed, grows from edits | writing | kosif-reel-hooks requires out/voice.md but no card says how to build it; scripts he must say aloud fail in the wrong voice. |
| ACRAFT-32 | Discourse-level rewrite with an isolated cold reader | writing | Owner's Arabic explainers and voiceovers often pass the word scan yet still lose viewers; this targets why. |
| ACRAFT-33 | Arabic translationese repair after translation or localization | writing | Owner localizes scripts, subtitles and tool UI to Arabic; existing cards cover AI tells and dialect but not translation calques. |
| ACRAFT-34 | Story bank interview: numbers, turning points, positions | writing | Feeds kosif-reel-hooks' 'one true thing' and {{رقمك}} placeholders with real, owner-approved specifics. |
| ACRAFT-35 | From spark to filmable premise: what-ifs, logline tests, stakes | writing | Strengthens the concept stage of his cinematic films (e.g. Egypt 2120) before expensive boards. |
| ACRAFT-36 | Dialogue scene craft: subtext, late entry, visible-only action | writing | Fills a gap: no card teaches dialogue/scene writing for his character-driven films and ads. |
| ACRAFT-37 | From fragments to a script: explore, then exploit | writing | Gives a repeatable path from his voice notes to explainer/voiceover scripts. |
| ACRAFT-38 | Seven-sweep copy review with revalidation | writing | Gives his Arabic captions and ad copy a disciplined edit pass beyond AI-tell removal. |

## Upgraded cards

| ID | Track | What it adds |
|---|---|---|
| APP-17 | frontend | Lets the owner choose glow, radius or timing values for films and sites by eye from real renders instead of prose. |
| ABUILD-22 | frontend | Makes every living-site or HTML-film page delivery carry the same six proofs instead of 'it builds'. |
| ABUILD-35 | frontend | Gives the critic pass on sites and UI frames a fixed, severity-ranked format the owner can act on. |
| UI-07 | frontend | Product UI rebuilt inside films and saas-animation scenes reads as a real shipped app rather than a template. |
| UI-89 | frontend | Living sites ship fast, RTL-correct and crawlable by default instead of being rescued after a Lighthouse run. |
| DOC-06 | frontend | Black Dragon receipts and project reports export to clean PDFs without half-drawn charts or split cards. |
| UI-80 | frontend | Glass cards and Apple-style UI in films stay readable over moving footage. |
| UI-69 | frontend | HUD and callout overlays in 3D and product films never smother the hero subject. |
| SHAPE-79 | frontend | Icons and logo reveals in draw-on scenes read early and stay legible at small sizes. |
| QA-136 | frontend | Strengthens the mimic/rotoscope pipeline with a repeatable measure-fit-review loop instead of ad-hoc tweaks. |
| ENG-58 | frontend | Fast batch covers without a browser, with a guard that keeps Arabic titles correct. |
| DRAW-25 | frontend | Hand-drawn warmth in films reads as craft, not as a broken render. |
| UI-04 | frontend | Real-feature product films show the app as it truly renders, numbers included. |
| ABUILD-36 | frontend | Lets the owner tidy arbitrary spacing/type/colour in existing kits without a redesign or lost changes. |
| CAM-62 | frontend | Scroll-story living sites keep their message for every viewer, including reduced-motion and keyboard users. |
| ABUILD-45 | frontend | Launch pages for the owner's products get a defensible structure before any GSAP polish. |
| APP-16 | frontend | Keeps UI demos and living sites from over-animating the controls viewers see most. |
| AMIND-41 | image | Deep thinking and explainer scripts: a mind map that is memorable and directly animatable rather than a wall of phrases. |
| ADOCS-20 | image | Explainer and code-to-video diagrams that teach real specifics and survive a render-and-look loop. |
| EXPL-10 | image | Diagram scenes that fail loudly on clipped labels or floating arrows instead of shipping them. |
| EXPL-13 | image | Boards that later become animated camera-tour films start clean and readable. |
| DATA-99 | image | Cinematic web films and scroll stories where each beat proves something and survives as a still. |
| DATA-96 | image | Chart frames that look designed rather than library-default and composite cleanly over footage. |
| ENG-381 | image | Dense particle and data fields in browser films stay crisp and fast without jumping to WebGL too early. |
| MAP-10 | image | Documentary map scenes where motion encodes something true and globes do not drift off their coordinates. |
| GEN-32 | image | Reverse-prompting and reference study stay factual, so recreated shots are based on what is really in the frame. |
| BRAND-12 | image | Brand and logo work for clients ends with a defensible pick and a complete, licence-clean suite. |
| FMT-50 | image | Covers and banners for the owner's channels and sites go out at the right size and weight, with share previews that work. |
| GEN-86 | image | Paid image generation stays reproducible and honest about what exists. |
| STORY-83 | marketing | Makes the owner's publishing calendar realistic and campaign-aware. |
| FMT-57 | marketing | Turns each long edit the owner makes into a week of native short-form posts. |
| AMEDIA-25 | marketing | Gives every long video the owner publishes a complete, consistent discovery package. |
| ASTRAT-19 | marketing | Helps the owner decide which revenue lines (client work, templates, sponsorships, courses) to build first. |
| ADOCS-45 | marketing | Strengthens the owner's Arabic↔English campaign versions so they feel native, not translated. |
| FMT-09 | marketing | Adds quality gates to every social graphic and cover the owner exports. |
| FMT-33 | marketing | Makes the post pack robust when the owner adapts one caption to many platforms and languages. |
| ASTRAT-86 | marketing | Lets the owner write hooks and offers for a specific viewer or client instead of everyone. |
| FMT-47 | marketing | Stops one lucky thumbnail swap from becoming a false rule. |
| STORY-17 | marketing | Tightens the owner's reel openings and structures with a concrete checklist. |
| AGENT-02 | orchestration | Black Dragon can grade every subagent result off disk instead of trusting its prose. |
| AGENT-14 | orchestration | Keeps red-team passes on films/plans from flooding the owner with invented objections. |
| AGENT-13 | orchestration | Revision loops on scripts and films stop at a real pause condition instead of polishing forever. |
| CHECK-11 | orchestration | Every green QA check on a render states what it cannot see. |
| CHECK-31 | orchestration | Black Dragon receipts cannot be satisfied by stale or tampered evidence. |
| CHECK-10 | orchestration | Status lines in owner reports carry their evidence and grade inline. |
| QA-254 | orchestration | Choosing among Higgsfield/image variants becomes a logged, reproducible decision instead of 'the prettiest one'. |
| QA-253 | orchestration | Visual regression on motion/web films is judged on honest matched pairs. |
| AMIND-55 | orchestration | Arabic hooks and captions never ship an invented statistic. |
| AMIND-66 | orchestration | Transcript mining yields countable, verifiable findings. |
| AMIND-08 | orchestration | Long multi-session film projects resume without redoing or silently dropping work. |
| CHECK-24 | orchestration | Self-evolution of kosif-superpowers cannot 'improve' by gaming its own metric. |
| AGENT-23 | orchestration | Fits the Black Dragon rule that no capability is left unused by a lazy 'not possible'. |
| CHECK-21 | skillcraft | Makes the skill's with/without evidence trustworthy instead of contaminated by the session's own context. |
| PROMPT-22 | skillcraft | The owner's skill descriptions carry Arabic+English triggers; this gives a measured way to tune them. |
| AGENT-27 | skillcraft | Lets CHECK-24's self-evolution loop for kosif-superpowers run without accepting lucky or regressive edits. |
| AMIND-79 | skillcraft | Keeps the owner's large skill library routable and cheap in context. |
| PROMPT-38 | skillcraft | Cheap structured way to tune recurring prompts (captions, hooks, generator briefs). |
| PROMPT-15 | skillcraft | Stops 'B feels better' claims on owner prompt changes. |
| PROMPT-08 | skillcraft | Directly fits the Black Dragon orchestrator handing whole jobs to fresh sessions. |
| GEN-84 | skillcraft | Sharper rule for when generated stills may carry text vs when Arabic/type goes in the overlay. |
| PROMPT-10 | skillcraft | Cuts paid regeneration on owner image/video campaigns. |
| GEN-49 | skillcraft | Avoids picking Kling/Seedance versions from memory. |
| AGENT-31 | skillcraft | Long Black Dragon runs survive compaction without losing conventions. |
| MODEL-24 | thinking | Pre-mortems on productions and launches end with dated kill switches instead of generic risks. |
| AMIND-76 | thinking | Stress-tests a production plan or concept fast, with recommended answers so the owner just confirms. |
| THINK-25 | thinking | Fewer, sharper questions to the owner; more momentum on creative jobs. |
| IDEA-01 | thinking | Concept rounds for films and campaigns yield three defended directions instead of a pile of ideas. |
| IDEA-15 | thinking | Lets the Dragon Mind compare real alternative cuts or concepts before committing credits. |
| THINK-28 | thinking | Battle-tests big production plans before money is committed. |
| PROD-06 | thinking | Closes the loop on the owner's big calls so judgement improves over time. |
| ADOCS-30 | thinking | A research and lessons wiki the owner can trust, with every figure traceable. |
| ASTRAT-92 | thinking | Testing a series idea or product with real viewers yields evidence, not polite compliments. |
| PLAN-06 | thinking | Big films and pipelines start with one finished scene that proves the pipeline before scaling. |
| PLAN-08 | thinking | Pilot projects and free samples for clients get agreed exit criteria up front. |
| ASTRAT-12 | thinking | Honest go/no-go on the owner's product and channel bets. |
| AMIND-81 | thinking | Naming the owner's products, series and channels with checked availability. |
| IDEA-18 | thinking | Style and layout choices for designs and films are picked by seeing, not by reading. |
| ASTRAT-06 | thinking | Huge foggy projects (a full film universe, a product line) get charted before planning. |
| THINK-22 | thinking | Keeps the owner's tools lean: reuse powers before building new ones. |
| FOOT-14 | video | Lets the owner copy a viral reel's editing style as portable rules without copying its content. |
| VOICE-21 | video | Strengthens the owner's narration and voice work for long Arabic voiceovers and audio episodes. |
| GEN-86 | video | Prevents costly re-rolls and continuity errors in the owner's AI-generated reels and cinematic films. |
| WRITE-06 | writing | Stops humanizer passes from flattening or rewriting his own drafts. |
| WRITE-16 | writing | Respects his ownership of drafts he only wants critiqued. |
| WRITE-22 | writing | Makes his VO scripts read cleanly aloud and time correctly. |
| STORY-17 | writing | Directly sharpens kosif-reel-hooks choices and A/B testing. |
| FMT-57 | writing | Turns each of his long videos into a week of native shorts and posts. |
| BEAT-X06 | writing | Raises his Arabic song/lyric film writing quality and stops endless regenerate loops. |
| ACODE-260 | writing | Keeps kosif-tool Arabic UI from shipping broken strings. |
| ADOCS-45 | writing | Consistent Arabic terminology across long translated material. |
| STORY-46 | writing | Keeps his product reels honest and defensible. |

Receipts per track: `.claude/skills/kosif-superpowers/data/atlas-pass-20261107-<track>.json` (SKILL.md sha256 per source, skipped ids with reasons).
