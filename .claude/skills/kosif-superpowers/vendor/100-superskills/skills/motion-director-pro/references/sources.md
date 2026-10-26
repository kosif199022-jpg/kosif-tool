# مصادر «مخرج الموشن المحترف (فيلم لا شرائح)» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## remotion-best-practices (2712-remotion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/remotion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2712-remotion/10430-remotion-best-practices
- الوصف: Router for all Remotion skills

```markdown
## Creating a video

If the user asks to make, create, or build a new video or composition, load [Create a new Remotion video](./remotion-create/REFERENCE.md), whether or not a Remotion project already exists.

## New project setup

If no Remotion project currently exists, load [Create a new Remotion project](./remotion-create/REFERENCE.md)

## React Markup Best Practices

If you are writing Remotion React Markup, load [Remotion Markup Best Practices](./remotion-markup/REFERENCE.md)

## Maps

For static maps, animated routes and markers, geographic explainers, Mapbox, MapLibre, MapTiler, GeoJSON, or 3D geographic flyovers, load [Remotion Maps](./remotion-maps/REFERENCE.md).

## Multimedia

For achieving multimedia tasks in the browser, such as trimming, cropping videos, or getting metadata from them, load [Remotion Multimedia](./remotion-multimedia/REFERENCE.md)

## Improving Interactivity

By structuring the Remotion markup well, we can allow users to interactively change things in the Studio and write back to code. If relevant: [Interactivity Best Practices](./remotion-interactivity/REFERENCE.md)

## Rendering

For advanced rendering beyond simple `npx remotion render`, see: [Rendering Best Practices](./remotion-render/REFERENCE.md)

## Opening Remotion Studio

To launch a project in Remotion Studio, open its exact local URL, or configure Studio CLI flags, load [Remotion Studio](./remotion-studio/REFERENCE.md).

## Captions

When working with Captions, load [Remotion Captions](./remotion-captions/REFERENCE.md).

## Creating a SaaS, automation or application

Use the [Remotion SaaS skill](./remotion-saas/REFERENCE.md) for knowledge about Remotion-powered SaaS apps, such as `<Player>`, rendering on Lambda, Vercel, Cloudflare, via Express.js, client-side rendering, or for finding the right SaaS template.

## Looking up Remotion APIs and documentation

To find and read current Remotion documentation, load [Remotion Docs](./remotion-docs/REFERENCE.md).

## Upgrading

To upgrade Remotion, related packages, compatible Mediabunny packages, and installed Remotion Agent Skills, load [Remotion Upgrade](./remotion-upgrade/REFERENCE.md).


## Codex troubleshooting

When running inside Codex, first try starting the Remotion Studio without opening the system browser:

```bash
npx remotion studio --no-open
```

Only if that fails with file watcher limits such as `EMFILE: too many open files, watch`, retry with polling and without opening a browser from Codex:

```bash
npx remotion studio --no-open --webpack-poll 1000
```
```

## remotion-create (2712-remotion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/remotion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2712-remotion/10432-remotion-create
- الوصف: Create a new Remotion video

```markdown
These are instructions for making a new Remotion project and composition.
If this is not the next task, see [Remotion Best Practices](../remotion-best-practices/SKILL.md)

## Scaffold a project

If a project already exists, skip this.
Ensure Node.js and Git is installed, and the current folder is appropriate for starting a new project.

Scaffold one using:

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
cd my-video
npm i
```

Replace `my-video` with a suitable project name.

## Designing a video

Keep the scaffold and add React Markup.
Follow [Remotion React Markup Best Practices](../remotion-markup/SKILL.md) and [Video Layout Rules](video-layout.md) for video-first layout and text sizing guidance.

## Is this a multi-scene video?

If this is a video with multiple subsequence videos, follow guidance at [Multi-scene videos](../remotion-markup/multi-scene-video.md).

## Interactivity Best Practices

By structuring the React Markup following [Remotion Interactivity Best Practices](../remotion-interactivity/SKILL.md), you allow the user to make edits in the Studio which write back to code.

## TailwindCSS

If Tailwind is requested, see [tailwind.md](tailwind.md) for using TailwindCSS in Remotion.

## Open the preview

After creating or updating the video, start the preview server by default:

```bash
npx remotion studio --no-open
```

This will start a long-running process and print the server URL for the preview.
If the server is already started, it will print the URL.
Open the exact URL in the Codex in-app browser. If no browser tool is available yet, use `tool_search` for the in-app browser control tool, then navigate to the local URL.
You can visit a specific composition by navigating to `/[composition-id]`, for example `http://localhost:3000/MapAnimation`.

## Render the video

Only render if the user explicitly asks for it.

```
npx remotion render
```

For more options, see [Rendering](../remotion-render/SKILL.md).

## Follow-up

The video creation process has finished.
For follow-up prompts, use [Remotion Best Practices](../remotion-best-practices/SKILL.md)
```

## remotion-video-builder (3198-remotion)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/tim-osterhus/codex-remotion-plugin
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3198-remotion/13555-remotion-video-builder
- الوصف: Use when building, reviewing, or refactoring a Remotion project, especially parameterized launch or demo videos with shared props schemas, calculateMetadata, Sequence and Series timing, multiple aspect ratios, terminal or footage layers, and render scripts. Prefer official Remotion docs or MCP for API details because package behavior may change.

```markdown
# Remotion Video Builder

Your Remotion knowledge may be stale. When exact API behavior matters, prefer the official `remotion-documentation` MCP server or the docs at [remotion.dev](https://www.remotion.dev/).

## Start Here

- If the project does not exist yet, scaffold it with `npx create-video@latest` and prefer the blank template.
- Keep every `remotion` and `@remotion/*` package on the exact same version and avoid caret ranges.
- Standard entry shape:
  - `src/index.ts` calls `registerRoot()`
  - `src/Root.tsx` registers all videos with `<Composition>` or `<Still>`

## Build Order

1. Model the input contract first:
   - top-level props schema
   - timeline or event data
   - render profile
2. Define shared props with `zod` and pass the schema to each `<Composition>`.
3. Use `calculateMetadata` to derive `durationInFrames`, `width`, `height`, transformed props, and `defaultOutName`.
4. Build the scene structure with `<Series>` for narrative order and `<Sequence>` for overlays, entrances, footage windows, and callouts.
5. In Remotion v4.x projects, explicitly set `premountFor` on `<Sequence>` elements that need assets loaded before they appear.
6. Add sample data and render scripts before polishing animation.

## Defaults And Rules

- Default to `fps={30}` and `1920x1080` for landscape unless the brief says otherwise.
- Use `AbsoluteFill` for layering.
- Use `staticFile()` for anything coming from `public/`.
- Use `useCurrentFrame()` and `useVideoConfig()` for frame-based logic.
- Prefer subtle motion:
  - `spring()` with high damping
  - `interpolate()` with clamping
- Do not use `Math.random()`. Use `random(seed)` from `remotion`.
- Keep text animation simple and legible.
- Keep landscape and vertical outputs on the same business logic unless the brief truly requires divergence.

## Parameterized Video Checklist

- One shared top-level `z.object()` schema
- `defaultProps` matching the component prop shape
- `calculateMetadata` returning dynamic duration or dimensions when inputs require it
- Sample JSON or TypeScript data for local preview
- Render scripts for every target output

## Footage Strategy

Support at least these modes when footage is optional:

- `none`
- `placeholder`
- `real`

The timeline and overlays should still render when no real footage exists.

## Millrace Launch Video

If the request is about Millrace or the launch video pipeline, read [references/millrace-launch-video.md](references/millrace-launch-video.md) before implementing.

## References

- [references/remotion-core.md](references/remotion-core.md)
- [references/millrace-launch-video.md](references/millrace-launch-video.md)
```

## kinetic-inflated-hero (100-ui-motion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/ui-motion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/100-ui-motion/209-kinetic-inflated-hero
- الوصف: Design or implement full-viewport kinetic typography heroes using inflated physical letterforms, Matter.js-style motion, Pretext-inspired type behavior, and SVG goo/blur effects. Use when the user asks for a memorable animated hero, kinetic brand object, inflated type, soft-body letters, or a Zine-style "invisible" AI-search hero.

```markdown
# Kinetic Inflated Hero

Use this skill when designing or building a homepage hero whose main visual is kinetic typography, not a screenshot, card, dashboard mockup, or conventional centered H1.

The target feeling is a full-viewport brand object: loud, physical, electric, and memorable from a single screenshot.

## Core Direction

Create a full-viewport hero with a strict, high-contrast palette. The reference pattern is Zine's electric-blue hero: saturated blue background, oversized inflated white typography, restrained overlay copy, and compact glass/white CTAs.

The letterforms should feel physical and alive:

- inflated, soft, pressurized, and tactile
- drifting, colliding, stretching, squashing, and settling
- deflecting around support copy, navigation, and CTAs
- more like kinetic type or an interactive brand installation than a SaaS hero

Use Pretext-inspired kinetic typography as a directional reference, but do not default to ASCII/noise aesthetics unless the user asks. The default visual surface is inflated white type on a saturated field.

## Recommended Tools

For implementation, prefer:

- React / Next.js for the component surface
- Matter.js or equivalent physics for collision and obstacle behavior
- opentype.js when deforming real font outlines into soft-body glyphs
- SVG filters for goo, dilation, blur, and deformation
- CSS keyframes for small repeatable letter effects
- requestAnimationFrame only when needed for physics/render loops
- pointer and scroll inputs as optional forces, not mandatory gimmicks

If a project already has motion infrastructure, adapt to it instead of adding dependencies automatically.

## Hero Composition

A good composition usually has:

- a full-bleed hero section, height `100svh`
- a floating nav over the field, usually glass or translucent white
- one compact support-copy block near the lower center
- two compact CTAs below the support copy
- kinetic letterforms occupying the whole canvas, including edge/corner positions
- overlay text and buttons treated as obstacles that type flows around or avoids

For a Zine-style AI-search hero, use this content model:

```text
Your site is invisible to ChatGPT, Claude, Gemini, Perplexity, Grok.
```

Do not render this as a normal static headline. Embed it in the kinetic type system. Let the active AI model name rotate, swap, inflate, or collide into place.

Support copy:

```text
Zine is your always-on growth marketing engine. Agents that write, optimize, and watch your competitors across every channel, so you show up where your customers are looking.
```

CTAs:

```text
Start free
See how it works
```

## Signature Invisible-Word Effect

When the concept includes the word "invisible," make it the signature interaction.
```

## gsap (2702-hyperframes)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/hyperframes
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2702-hyperframes/10377-gsap
- الوصف: GSAP animation reference for HyperFrames. Covers gsap.to(), from(), fromTo(), easing, stagger, defaults, timelines (gsap.timeline(), position parameter, labels, nesting, playback), and performance (transforms, will-change, quickTo). Use when writing GSAP animations in HyperFrames compositions.

```markdown
# GSAP

## Core Tween Methods

- **gsap.to(targets, vars)** — animate from current state to `vars`. Most common.
- **gsap.from(targets, vars)** — animate from `vars` to current state (entrances).
- **gsap.fromTo(targets, fromVars, toVars)** — explicit start and end.
- **gsap.set(targets, vars)** — apply immediately (duration 0).

Always use **camelCase** property names (e.g. `backgroundColor`, `rotationX`).

## Common vars

- **duration** — seconds (default 0.5).
- **delay** — seconds before start.
- **ease** — `"power1.out"` (default), `"power3.inOut"`, `"back.out(1.7)"`, `"elastic.out(1, 0.3)"`, `"none"`.
- **stagger** — number `0.1` or object: `{ amount: 0.3, from: "center" }`, `{ each: 0.1, from: "random" }`.
- **overwrite** — `false` (default), `true`, or `"auto"`.
- **repeat** — number or `-1` for infinite. **yoyo** — alternates direction with repeat.
- **onComplete**, **onStart**, **onUpdate** — callbacks.
- **immediateRender** — default `true` for from()/fromTo(). Set `false` on later tweens targeting the same property+element to avoid overwrite.

## Transforms and CSS

Prefer GSAP's **transform aliases** over raw `transform` string:

| GSAP property               | Equivalent          |
| --------------------------- | ------------------- |
| `x`, `y`, `z`               | translateX/Y/Z (px) |
| `xPercent`, `yPercent`      | translateX/Y in %   |
| `scale`, `scaleX`, `scaleY` | scale               |
| `rotation`                  | rotate (deg)        |
| `rotationX`, `rotationY`    | 3D rotate           |
| `skewX`, `skewY`            | skew                |
| `transformOrigin`           | transform-origin    |

- **autoAlpha** — prefer over `opacity`. At 0: also sets `visibility: hidden`.
- **CSS variables** — `"--hue": 180`.
- **svgOrigin** _(SVG only)_ — global SVG coordinate space origin. Don't combine with `transformOrigin`.
- **Directional rotation** — `"360_cw"`, `"-170_short"`, `"90_ccw"`.
- **clearProps** — `"all"` or comma-separated; removes inline styles on complete.
- **Relative values** — `"+=20"`, `"-=10"`, `"*=2"`.

## Function-Based Values

```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  stagger: 0.1,
});
```

## Easing

Built-in eases: `power1`–`power4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine`. Each has `.in`, `.out`, `.inOut`.

## Defaults

```javascript
gsap.defaults({ duration: 0.6, ease: "power2.out" });
```

## Controlling Tweens

```javascript
const tween = gsap.to(".box", { x: 100 });
tween.pause();
tween.play();
tween.reverse();
tween.kill();
tween.progress(0.5);
tween.time(0.2);
```

## gsap.matchMedia() (Responsive + Accessibility)

Runs setup only when a media query matches; auto-reverts when it stops matching.

```javascript
let mm = gsap.matchMedia();
mm.add(
  {
```

## brand-film (101-video-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/video-skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/101-video-skills/212-brand-film
- الوصف: Plan and make a narrative product brand film that moves from a human problem to a product reveal. Use for launch films, cinematic teasers, and campaign videos where story matters more than a step-by-step demo.

```markdown
# Brand film

A brand film earns the reveal. It makes the audience recognize a problem, turns that problem into a visual idea, then shows the real product as a credible answer.

## Shape the story

Plan a small number of beats: problem, escalation, turn, reveal, proof, and landing. The opening should give the viewer a human reason to care before showing the product. Let a physical or visual metaphor carry the problem, but do not let it replace evidence of what the product actually does.

Write one claim per beat. The proof beat should show the outcome in the real product or a faithful rendering of its UI. Check every capability and privacy statement against current product behavior.

## Keep one visual language

Read the brand's source materials: colors, typography, mark, materials, motion, sound, and examples. Use a limited set of recurring shapes and transitions so the film feels like one world. Change from the problem world to the product world with a motivated visual transition when possible. Keep text short enough to read in its allotted time.

Do not redraw a logo or end tag from memory if the actual asset exists. Use owned or licensed footage, music, and graphics. A metaphor may be invented; the product UI and claimed outcome must be accurate.

## Review before delivery

Storyboard the major frames and transitions. Watch a rough cut for story clarity before polishing. Then check final exports for timing, readable claims, audio mix, brand consistency, and aspect-ratio composition. The film should still make sense when viewed muted, unless the user specifically wants an audio-led piece.
```
