# مصادر «بكسل آرت وأصول الألعاب» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## 9528-tileset (2460-pixel-art)

- الترخيص: **MIT**  ·  الأصل: https://github.com/melodic-software/claude-code-plugins/tree/c8fa858c9059d3183cfc08f646e4a97f44b33973/plugins/pixel-art
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2460-pixel-art/9528-tileset
- الوصف: Create pixel-art tilesets with no external tools: terrain, autotiles (RPG Maker MZ A1-A5 and B-E, blob-47, 16-tile corner sets), seamless backgrounds, and parallax layers, laid out as the target engine's sheet. The model authors a palette-locked spec or a procedural generator, the bundled stdlib renderer writes the sheet, and a render-review loop iterates until the seams read. Use when: 'tileset',

```markdown
# Tileset

Produce a tileset or parallax layer the target engine can load, and show it.

## 1. Brief

Follow [`brief.md`](${CLAUDE_PLUGIN_ROOT}/reference/brief.md) the same way `/pixel-art:sprite`
does, including the `brief.md` file, the one-line defaults, and the presence-gated
`/planning:interview` offer. Then add:

- **Set**: seamless single tile, blob-47, 16-tile corner, RPG Maker quarter-tile block, or parallax layers.
- **Tile size and sheet**: the engine cell and which file (A2, B, a Godot atlas, a plain strip). Read
  [`engine-layouts.md`](${CLAUDE_PLUGIN_ROOT}/reference/engine-layouts.md) and
  [`craft-tiles.md`](${CLAUDE_PLUGIN_ROOT}/reference/craft-tiles.md). Do not restate their tables.

## 2. Choose the backend

Same rule as `/pixel-art:sprite`: read [`backends.md`](${CLAUDE_PLUGIN_ROOT}/reference/backends.md).
`native` is the default and always available. Honor `${user_config.backend}` when it names another
backend (`native` or `aseprite`). Stay on native unless the request or that setting names Aseprite.

## 3. Author

Draw the set `craft-tiles.md` names for that engine. Quarter-tile targets are the source block (the
engine composes the final shapes), not a hand-drawn tile for every composed shape, unless the brief
asks for that proof. Blob and corner sets are the full tiles the engine samples. Parallax layers
follow the depth rules in `craft-tiles.md`: slower, darker, and less detailed as they recede, and
the scroll step divides the loop width.

Prefer a short procedural generator when the sheet is larger than a few tiles. A worked A2 ground
sheet is `${CLAUDE_PLUGIN_ROOT}/examples/tileset/a2_ground.py`. Keep the palette locked in the spec.

## 4. Render

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/backends.py" <spec.json> --out <dir> --scale 4
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/gallery.py" <dir>
```

`backends.py` writes the same files `render.py` does. Pass `--backend <name>` when this request
names one; otherwise pass `--backend ${user_config.backend}` when that option is set, rather than
relying on the environment to carry it.

Output location resolves as in `/pixel-art:sprite`. Keep the spec and the generator beside the output.

## 5. Review loop

Read `preview.png` and critique it against the brief and `craft-tiles.md`: seams on a repeat (the
generator or a 3x3 preview), edge-band thickness on an autotile, a center that does not shout the
grid, and a blank top-left cell when the target sheet requires one. Fix the spec or generator,
re-render, re-read. Stop when it reads at 1x or after the user's direction says so; typically 2 to
4 rounds. Name the remaining weaknesses honestly.

## 6. Deliver

Report `sheet.png` at 1x under the filename the engine expects, `sheet.json`, the preview, and the
```

## phaser-2d-game (2696-game-studio)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/game-studio
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2696-game-studio/10366-phaser-2d-game
- الوصف: Implement 2D browser games with Phaser. Use when the user wants a Phaser, TypeScript, and Vite stack for scenes, gameplay systems, cameras, sprite animation, and DOM-overlay HUD patterns.

```markdown
# Phaser 2D Game

## Overview

Use this skill for the main execution path in this plugin. Phaser is the default stack for 2D browser games here because it handles rendering, timing, sprites, cameras, and scene orchestration well without forcing gameplay rules into the framework.

Preferred stack:

- Phaser
- TypeScript
- Vite
- DOM-based HUD or menus layered over the game canvas

## Architecture

1. Keep gameplay state outside Phaser scenes.
   - Systems own rules, turn order, movement, combat, inventory, objectives, and progression.
   - Phaser scenes adapt system state into sprites, camera motion, animation playback, and effects.
2. Make scenes thin.
   - Boot and asset preload
   - Menu or shell scene
   - Gameplay scene
   - Optional overlay or debug scene
3. Keep renderer-facing objects disposable.
   - Sprite containers, emitters, tweens, and camera rigs are view state, not source of truth.
4. Favor stable asset manifest keys over direct file-path references throughout gameplay code.

## Implementation Guidance

- Use one integration boundary where the scene reads simulation state and emits input actions back.
- Prefer deterministic system updates over scene-local mutation.
- Treat HUD and menus as DOM when text, status density, or responsiveness matter.
- Keep animation state derived from gameplay state rather than ad hoc sprite flags.

## 2D Modes Covered Well

- Turn-based grids and tactics
- Top-down exploration
- Side-view action platformers
- Character-action combat with sprite animation
- Lightweight management or deck-driven battle scenes

## Camera and Presentation

- Choose the camera model early: locked, follow, room-based, or tactical-pan.
- Keep camera logic separate from game rules.
- Use restrained screen shake, hit-stop, and parallax. Effects should improve readability, not obscure it.

## UI Integration

- Use DOM overlays for HUD, command menus, settings, and narrative panels.
- Keep the canvas responsible for the world, combat readability, and motion.
- Avoid shoving dense text or complex settings UIs into Phaser unless the project explicitly needs an in-canvas presentation.

## Asset Organization

- `characters/`
- `environment/`
- `ui/`
- `fx/`
- `audio/`
- `data/`

Keep manifest keys human-readable and stable.

## Default Directory Shape

See `../../references/phaser-architecture.md` for a concrete module split.

## Anti-Patterns

- Game rules inside `update()` loops without a system boundary
- Scene-to-scene state passed through mutable global objects
- HUD text rendered in the game canvas just because it is convenient
- Asset paths embedded everywhere instead of a manifest layer
- Overusing generic React dashboard patterns for game UI

## References

- Shared architecture: `../web-game-foundations/SKILL.md`
```

## 9527-sprite (2460-pixel-art)

- الترخيص: **MIT**  ·  الأصل: https://github.com/melodic-software/claude-code-plugins/tree/c8fa858c9059d3183cfc08f646e4a97f44b33973/plugins/pixel-art
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2460-pixel-art/9527-sprite
- الوصف: Create static pixel-art sprites (characters, items, icons, portraits, faces, battlers, props) as engine-ready PNG sheets with no external tools: the model authors a palette-locked spec or a procedural generator, the bundled stdlib renderer writes the files, and a render-review loop iterates until the sprite reads. Use when: 'make a sprite', 'pixel art of X', 'draw a 32x32 icon', 'character portrai

```markdown
# Sprite

Produce a static sprite the user can drop into a game or project, and show it to them.

## 1. Brief

Follow [`brief.md`](${CLAUDE_PLUGIN_ROOT}/reference/brief.md). That file is the only copy of the
fields: subject, style references, proportions, size, palette, view, mood, target, and 2 to 6 done
criteria. Ask only what changes the output. State every unspecified field as a default in one line.

Write `brief.md` beside the spec before the first render. A later run that finds it there reads it
and does not ask again.

When the request is vague or high-stakes, offer `/planning:interview` (if the planning plugin is
installed). Planning owns a numbered-question brief. If planning is not installed, or the user does
not accept, continue with the in-skill brief, which is the default and works alone. Do not start
the interview unless the user accepts.

## 2. Choose the backend

Read [`backends.md`](${CLAUDE_PLUGIN_ROOT}/reference/backends.md). `native` is the default and
always available. Honor `${user_config.backend}` when it names another backend. `${CLAUDE_PLUGIN_ROOT}/scripts/backends.py`
detects that backend, uses it when it is present, and otherwise prints one line and renders with
`native`. The backend is `native` (default) or `aseprite`. Both honor the same artifact contract:
the spec and the files in step 4.

## 3. Author

Write the spec that `render.py` reads (its docstring is the format). Two authoring modes:

- **Hand-authored grid**: small sprites (up to about 24x24), icons, faces. Write rows directly.
- **Procedural generator**: larger sprites or families of variants. Write a short Python script
  that draws with primitives (rects, ellipses, lines) onto a material grid, then applies shading
  and outlining passes and emits the spec JSON. Materials map to color ramps (highlight, base,
  shadow, line), which keeps the palette locked and makes recolors one-line edits.
  For a full-body humanoid character, adapt `${CLAUDE_PLUGIN_ROOT}/scripts/kit.py` instead of
  writing that machinery: it draws down, left, and up and mirrors for right, and one `down` frame
  is a static character. Portraits and faces stay hand-authored grids.

The spec `palette` may be an inline object, a bundled preset name, or a path to a project palette
file ([`palettes/README.md`](${CLAUDE_PLUGIN_ROOT}/palettes/README.md)). When the project has
`pixel-art-palette.json` (or another path its `CLAUDE.md` names), use that path instead of
inventing colors. Do not retype a preset by hand. Images from another backend are snapped with
`render.py --snap` (see [`backends.md`](${CLAUDE_PLUGIN_ROOT}/reference/backends.md)), not by eye.

Apply [`craft-static.md`](${CLAUDE_PLUGIN_ROOT}/reference/craft-static.md): readable silhouette
```

## godot-gdscript-patterns (3098-game-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/game-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3098-game-development/13268-godot-gdscript-patterns
- الوصف: Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization. Use when building Godot games, implementing game systems, or learning GDScript best practices.

```markdown
# Godot GDScript Patterns

Production patterns for Godot 4.x game development with GDScript, covering architecture, signals, scenes, and optimization.

## When to Use This Skill

- Building games with Godot 4
- Implementing game systems in GDScript
- Designing scene architecture
- Managing game state
- Optimizing GDScript performance
- Learning Godot best practices

## Core Concepts

### 1. Godot Architecture

```
Node: Base building block
├── Scene: Reusable node tree (saved as .tscn)
├── Resource: Data container (saved as .tres)
├── Signal: Event communication
└── Group: Node categorization
```

### 2. GDScript Basics

```gdscript
class_name Player
extends CharacterBody2D

# Signals
signal health_changed(new_health: int)
signal died

# Exports (Inspector-editable)
@export var speed: float = 200.0
@export var max_health: int = 100
@export_range(0, 1) var damage_reduction: float = 0.0
@export_group("Combat")
@export var attack_damage: int = 10
@export var attack_cooldown: float = 0.5

# Onready (initialized when ready)
@onready var sprite: Sprite2D = $Sprite2D
@onready var animation: AnimationPlayer = $AnimationPlayer
@onready var hitbox: Area2D = $Hitbox

# Private variables (convention: underscore prefix)
var _health: int
var _can_attack: bool = true

func _ready() -> void:
    _health = max_health

func _physics_process(delta: float) -> void:
    var direction := Input.get_vector("left", "right", "up", "down")
    velocity = direction * speed
    move_and_slide()

func take_damage(amount: int) -> void:
    var actual_damage := int(amount * (1.0 - damage_reduction))
    _health = max(_health - actual_damage, 0)
    health_changed.emit(_health)

    if _health <= 0:
        died.emit()
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.
```

## unity-ecs-patterns (3098-game-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/game-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3098-game-development/13269-unity-ecs-patterns
- الوصف: Master Unity ECS (Entity Component System) with DOTS, Jobs, and Burst for high-performance game development. Use when building data-oriented games, optimizing performance, or working with large entity counts.

```markdown
# Unity ECS Patterns

Production patterns for Unity's Data-Oriented Technology Stack (DOTS) including Entity Component System, Job System, and Burst Compiler.

## When to Use This Skill

- Building high-performance Unity games
- Managing thousands of entities efficiently
- Implementing data-oriented game systems
- Optimizing CPU-bound game logic
- Converting OOP game code to ECS
- Using Jobs and Burst for parallelization

## Core Concepts

### 1. ECS vs OOP

| Aspect      | Traditional OOP   | ECS/DOTS        |
| ----------- | ----------------- | --------------- |
| Data layout | Object-oriented   | Data-oriented   |
| Memory      | Scattered         | Contiguous      |
| Processing  | Per-object        | Batched         |
| Scaling     | Poor with count   | Linear scaling  |
| Best for    | Complex behaviors | Mass simulation |

### 2. DOTS Components

```
Entity: Lightweight ID (no data)
Component: Pure data (no behavior)
System: Logic that processes components
World: Container for entities
Archetype: Unique combination of components
Chunk: Memory block for same-archetype entities
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Use ISystem over SystemBase** - Better performance
- **Burst compile everything** - Massive speedup
- **Batch structural changes** - Use ECB
- **Profile with Profiler** - Identify bottlenecks
- **Use Aspects** - Clean component grouping

### Don'ts

- **Don't use managed types** - Breaks Burst
- **Don't structural change in jobs** - Use ECB
- **Don't over-architect** - Start simple
- **Don't ignore chunk utilization** - Group similar entities
- **Don't forget disposal** - Native collections leak
```

## godot-gdscript-patterns (3490-game-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/game-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3490-game-development/14212-godot-gdscript-patterns
- الوصف: Master Godot 4 GDScript patterns including signals, scenes, state machines, and optimization. Use when building Godot games, implementing game systems, or learning GDScript best practices.

```markdown
# Godot GDScript Patterns

Production patterns for Godot 4.x game development with GDScript, covering architecture, signals, scenes, and optimization.

## When to Use This Skill

- Building games with Godot 4
- Implementing game systems in GDScript
- Designing scene architecture
- Managing game state
- Optimizing GDScript performance
- Learning Godot best practices

## Core Concepts

### 1. Godot Architecture

```
Node: Base building block
├── Scene: Reusable node tree (saved as .tscn)
├── Resource: Data container (saved as .tres)
├── Signal: Event communication
└── Group: Node categorization
```

### 2. GDScript Basics

```gdscript
class_name Player
extends CharacterBody2D

# Signals
signal health_changed(new_health: int)
signal died

# Exports (Inspector-editable)
@export var speed: float = 200.0
@export var max_health: int = 100
@export_range(0, 1) var damage_reduction: float = 0.0
@export_group("Combat")
@export var attack_damage: int = 10
@export var attack_cooldown: float = 0.5

# Onready (initialized when ready)
@onready var sprite: Sprite2D = $Sprite2D
@onready var animation: AnimationPlayer = $AnimationPlayer
@onready var hitbox: Area2D = $Hitbox

# Private variables (convention: underscore prefix)
var _health: int
var _can_attack: bool = true

func _ready() -> void:
    _health = max_health

func _physics_process(delta: float) -> void:
    var direction := Input.get_vector("left", "right", "up", "down")
    velocity = direction * speed
    move_and_slide()

func take_damage(amount: int) -> void:
    var actual_damage := int(amount * (1.0 - damage_reduction))
    _health = max(_health - actual_damage, 0)
    health_changed.emit(_health)

    if _health <= 0:
        died.emit()
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.
```
