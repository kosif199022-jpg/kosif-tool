# مصادر «تطوير الألعاب للويب» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

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

## rust-bracket-game-loop (2199-lvtd-skills)

- الترخيص: **MIT**  ·  الأصل: https://github.com/hashgraph-online/awesome-codex-plugins/tree/9cc4f3e/plugins/LVTD-LLC/skills
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2199-lvtd-skills/8153-rust-bracket-game-loop
- الوصف: Build and review bracket-lib style Rust 2D game loops, state structs, game modes, input handling, rendering calls, and restart flow. Use when creating a small Rust game with bracket-lib, porting a tutorial loop, or debugging tick/update/render state behavior.

```markdown
# Rust Bracket Game Loop

Use this skill to create or review a small Rust game loop, especially one built
with `bracket-lib` and an explicit game state. Keep `tick` as a coordinator:
read input, advance state, render, and dispatch to small helper functions.

## Core Workflow

1. Inspect the target project's `Cargo.toml`, edition, engine, and existing
   architecture before changing dependencies.
2. Create one state object that contains data preserved between frames.
3. Implement the engine trait or callback required by the project.
4. Route modes through an enum rather than scattered booleans.
5. Keep rendering and state mutation ordered and easy to trace.
6. Add a restart/reset path before adding many gameplay states.

## Read Next

Read `references/game-loop-patterns.md` for setup patterns, code skeletons,
mode routing, and review checks.

## Source Notes

Guidance is transformed and paraphrased from *Hands-On Rust* Chapter 3 and
the official companion source repository. Current crate context was checked
against `bracket-lib` documentation on docs.rs and the bracket-lib example
repository. Verify the target project's dependency versions before copying API
details.
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

## unity-ecs-patterns (3490-game-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/game-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3490-game-development/14213-unity-ecs-patterns
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
