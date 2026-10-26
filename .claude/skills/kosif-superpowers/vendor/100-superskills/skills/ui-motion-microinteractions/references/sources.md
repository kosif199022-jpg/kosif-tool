# مصادر «موشن الواجهات والتفاعلات الدقيقة» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## scroll-blur-manifesto (100-ui-motion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/ui-motion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/100-ui-motion/210-scroll-blur-manifesto
- الوصف: Design or implement quiet editorial manifesto sections where large text resolves from blurred ghost layers into sharp copy on scroll. Use when the user asks for scroll blur, blur-to-sharp transitions, Lenis/GSAP ScrollTrigger word reveals, or a warm editorial manifesto section.

```markdown
# Scroll Blur Manifesto

Use this skill for the section after a loud hero: the moment where the argument comes into focus as the user scrolls.

The target feeling is quiet, precise, editorial, and inevitable. It should contrast with kinetic hero energy rather than compete with it.

## Core Direction

Build a restrained manifesto section with:

- warm near-white canvas
- black text at varying opacity
- compact bordered mono chip
- hairline rules when useful
- generous but controlled spacing
- one large left-aligned paragraph
- selected words highlighted as filled pills

This is not a feature grid, screenshot gallery, or card stack. It is a narrative transition.

## Recommended Tools

For implementation, prefer:

- Lenis for smooth scroll
- GSAP + ScrollTrigger for scrub-linked progress
- two text layers: one sharp, one statically pre-blurred
- opacity crossfades between layers for performance
- `prefers-reduced-motion` fallback with readable static text

Do not animate `filter: blur(...)` independently on dozens of words during scroll. That commonly janks. Pre-blur the ghost layer once, then animate opacity.

## Layout Pattern

The typical structure:

1. A small mono chip above the text, for example `Introducing Zine`.
2. A visually hidden complete sentence for crawlers and screen readers.
3. A sharp visible text layer split into word spans.
4. A matching ghost text layer in the same position with `filter: blur(6px-10px)`.
5. ScrollTrigger timeline that reveals ghost words first, then crossfades to sharp words.

Keep the paragraph measure broad but controlled, around `max-width: 960px-1080px` for desktop. Use `text-wrap: pretty` or `balance` where supported.

## Motion Choreography

The scroll behavior should be reversible and scrubbed:

- as the section enters, side labels/chips settle in from slight blur/opacity
- each word appears first as a blurred ghost
- the ghost state holds briefly so the blur is visibly felt
- the sharp layer rises as the ghost layer fades at the same position
- highlighted pill words participate in the same reveal
- when scrolling past, sharp words dissolve back through ghost blur and then out
- the final footnote or source line can be the last element standing

A useful ScrollTrigger shape:

```text
trigger: manifesto block
start: top 65%
end: bottom 30%
scrub: 1
```

Tune these values to the page rhythm.

## Zine-Style Manifesto Copy

For an AI-search growth product, this section can use:

```text
```

## spring-profile-config-overlay-dedupe (3359-spring-profile-config-overlay-dedupe)

- الترخيص: **MIT**  ·  الأصل: https://github.com/voitta-ai/skillz/tree/feb9ceb0539f8f65355406ff1d5789c28c17a512/plugins/spring-profile-config-overlay-dedupe
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3359-spring-profile-config-overlay-dedupe/13874-spring-profile-config-overlay-dedupe
- الوصف: Strip an `application-<profile>.yml` down to the values that actually differ from `application.yml`, and prove the change altered nothing. Use when: (1) a Spring Boot or Grails repo has profile configs that are near-copies of the base config and you cannot tell which lines are real overrides, (2) you are about to change a value in the base config and need to know which profiles silently inherit it

```markdown
# De-duplicate Spring profile configs, and prove the strip changed nothing

## Problem

Spring Boot loads `application.yml` first, then layers `application-<profile>.yml` on top,
merging **per property key** rather than per YAML node. Any key in a profile file whose value
equals the base value is therefore inert — it does nothing except make the file longer and
create a second place to edit.

Left alone this rots in a specific way: someone updates a value in one file, the other copy
keeps the old value, and now two environments disagree for reasons nobody can see by reading
either file. Real numbers from one Grails service: the staging profile carried 128 keys of
which **118 were byte-identical to the base**, and production carried 142 of which 55 were.

The reason people don't clean it up is that a config file is scary to delete from — the
failure mode is a service that starts and then behaves subtly wrong. The fix is to make the
change *verifiable* rather than to eyeball it.

## Context / Trigger Conditions

- `application.yml` plus `application-staging.yml` / `application-production.yml` (or any
  profile names) that look like near-copies.
- You are about to change a base value and want to know who inherits it.
- Two environments differ and neither file explains why.

## Solution

### 1. Confirm the files really are layered

Do not assume. Spring's overlay behaviour depends on the profile actually being activated, and
some deployments pass an explicit config location that replaces rather than supplements the
base. Find the activation and read it:

```bash
grep -rn "SPRING_PROFILES_ACTIVE\|spring.profiles.active\|spring.config" \
  deploy/ .deploy/ helm/ k8s/ Dockerfile* 2>/dev/null
```

You want something like `SPRING_PROFILES_ACTIVE: staging` per environment. If instead you find
`--spring.config.location=...` pointing at a single file, the base is **not** merged and none
of this applies.

Grails note: separate `application-<env>.yml` files mean Spring profile loading, not the
classic Grails `environments:` block inside one file. Both can appear in the same codebase.

### 2. List what is actually inert

Flatten each file to dotted keys and compare:

```bash
python3 - <<'PY'
import yaml, io

def flat(d, p=''):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(flat(v, f"{p}.{k}" if p else str(k)))
    else:
        out[p] = d
    return out

def load(path):
    m = {}
    for doc in yaml.safe_load_all(open(path)):   # multi-document files are common
        if doc:
            m.update(flat(doc))
    return m

base = load('src/main/resources/application.yml')
for prof in ['staging', 'production']:
    d = load(f'src/main/resources/application-{prof}.yml')
```

## spring (613-java-spring)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/java-spring
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/613-java-spring/1642-spring
- الوصف: Generate Spring Boot project scaffolding

```markdown
# spring

Generate Spring Boot project scaffolding.

## Tools

This skill uses the following tools:

- **Read** - Read files from the filesystem
- **Write** - Write files to the filesystem
- **Edit** - Edit existing files with precise replacements
- **Bash** - Execute shell commands
- **Grep** - Search file contents with regex patterns
- **Glob** - Find files by name patterns
```

## create-spring-boot-java-project (2911-java-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/pleaseai/claude-code-plugins/tree/42ce3f976dd3aad0754ca683c1118b0d54faa36a/plugins/java-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2911-java-development/12089-create-spring-boot-java-project
- الوصف: Create Spring Boot Java Project Skeleton

```markdown
# Create Spring Boot Java project prompt

- Please make sure you have the following software installed on your system:

  - Java 21
  - Docker
  - Docker Compose

- If you need to custom the project name, please change the `artifactId` and the `packageName` in [download-spring-boot-project-template](#download-spring-boot-project-template)

- If you need to update the Spring Boot version, please change the `bootVersion` in [download-spring-boot-project-template](#download-spring-boot-project-template)

## Check Java version

- Run following command in terminal and check the version of Java

```shell
java -version
```

## Download Spring Boot project template

- Run following command in terminal to download a Spring Boot project template

```shell
curl https://start.spring.io/starter.zip \
  -d artifactId=${input:projectName:demo-java} \
  -d bootVersion=3.4.5 \
  -d dependencies=lombok,configuration-processor,web,data-jpa,postgresql,data-redis,data-mongodb,validation,cache,testcontainers \
  -d javaVersion=21 \
  -d packageName=com.example \
  -d packaging=jar \
  -d type=maven-project \
  -o starter.zip
```

## Unzip the downloaded file

- Run following command in terminal to unzip the downloaded file

```shell
unzip starter.zip -d ./${input:projectName:demo-java}
```

## Remove the downloaded zip file

- Run following command in terminal to delete the downloaded zip file

```shell
rm -f starter.zip
```

## Change directory to the project root

- Run following command in terminal to change directory to the project root

```shell
cd ${input:projectName:demo-java}
```

## Add additional dependencies

- Insert `springdoc-openapi-starter-webmvc-ui` and `archunit-junit5` dependency into `pom.xml` file

```xml
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
  <version>2.8.6</version>
</dependency>
<dependency>
  <groupId>com.tngtech.archunit</groupId>
  <artifactId>archunit-junit5</artifactId>
  <version>1.2.1</version>
  <scope>test</scope>
</dependency>
```

## Add SpringDoc, Redis, JPA and MongoDB configurations

- Insert SpringDoc configurations into `application.properties` file

```properties
# SpringDoc configurations
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha
```

- Insert Redis configurations into `application.properties` file

```properties
# Redis configurations
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.data.redis.password=rootroot
```

- Insert JPA configurations into `application.properties` file

```properties
# JPA configurations
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost:5432/postgres
```

## enterprise-spring-xml (1545-dasel)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jamie-bitflight/claude_skills/tree/19292fc0d4c92a86e09a7aaaf7f4f375a1bf1ec1/plugins/dasel
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1545-dasel/4244-enterprise-spring-xml
- الوصف: Dasel v3 selectors for Spring bean factory XML — use when querying any Spring ApplicationContext XML for bean discovery, dependency wiring, JMS destination mapping, property injection extraction, or cross-bean reference tracing. Load this skill before writing dasel selectors against Spring bean XML files (applicationContext.xml, *_beans.xml, spring-*.xml).

```markdown
# Spring Bean Factory XML — Dasel v3 Query Patterns

<when_to_use>

Load this skill when querying any Spring bean XML file — `applicationContext.xml`, `*_beans.xml`, `spring-context.xml`, or any Spring ApplicationContext XML — for bean discovery, dependency analysis, JMS wiring, property injection auditing, or cross-bean reference tracing.

</when_to_use>

Dasel v3 selector patterns for Spring bean factory XML. Always pass `-i xml` explicitly.

**Attribute prefix rule:** Dasel friendly mode (default) prefixes XML attributes with `-`. The `id` attribute is `-id`, `class` is `-class`. Text content is `#text`.

## Bean Discovery

```bash
# All bean IDs
cat chaosrouter_beans.xml | dasel -i xml 'beans.bean.filter(has("-id")).map("-id")'

# All bean classes
cat chaosrouter_beans.xml | dasel -i xml 'beans.bean.filter(has("-class")).map("-class")'

# Map -class across every bean (includes beans without -id)
cat chaosrouter_beans.xml | dasel -i xml 'beans.bean.map("-class")'
```

## Class Pattern Matching

Filter beans by class name via regex on `-class`.

```bash
# Beans whose class contains JmsTemplate
cat chaosrouter_beans.xml | dasel -i xml 'beans.bean.filter(-class ~ ".*JmsTemplate.*").map("-id")'

# Count beans matching a class pattern
cat beans.xml | dasel -i xml 'len(beans.bean.filter(-class ~ ".*Jms.*"))'
```

## Dependency Wiring Analysis

Find beans referencing other beans via the `-ref` attribute on `property` child elements.

**Pattern:** `parentCollection.filter(childElement.filter(condition).len($this) > 0)` — filters the parent by testing whether a matching child exists (length > 0).

```bash
# Beans that reference a specific bean ID via ref attribute
cat chaosrouter_beans.xml | dasel -i xml 'beans.bean.filter(property.filter(-ref == "targetBeanId").len($this) > 0).map("-id")'
```

## JMS Destination Mapping

Find which beans consume which JMS destinations via `property` child elements.

```bash
# Beans wired to a specific destination property
cat integrationpoint_beans.xml | dasel -i xml 'beans.bean.filter(property.filter(-name == "destination").len($this) > 0).map("-id")'
```

## Property Injection Extraction

Extract externalized `${...}` placeholder values from bean definitions.

```bash
# All property values using ${...} placeholders
cat storage_beans.xml | dasel -i xml 'beans.bean.property.filter(-value ~ ".*\\$\\{.*\\}.*").map("-value")'
```

## Attribute and Text Content Access

```bash
# <bean id="myBean" class="com.example.Foo">some text</bean>
cat beans.xml | dasel -i xml 'beans.bean[0].-id'       # myBean
cat beans.xml | dasel -i xml 'beans.bean[0].-class'    # com.example.Foo
cat beans.xml | dasel -i xml 'beans.bean[0].#text'     # some text

# Discover all keys (attributes + child elements) on first bean
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
