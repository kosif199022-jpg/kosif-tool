# مصادر «تحريك الشخصيات 2D» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## 9525-animate (2460-pixel-art)

- الترخيص: **MIT**  ·  الأصل: https://github.com/melodic-software/claude-code-plugins/tree/c8fa858c9059d3183cfc08f646e4a97f44b33973/plugins/pixel-art
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2460-pixel-art/9525-animate
- الوصف: Animate pixel-art sprites: idle, walk, run, attack, jump, hurt, death and custom cycles in 1, 4 or 8 directions, exported as sprite sheets laid out for the target engine (RPG Maker MZ, Godot, PICO-8, plain strips) with Aseprite-shaped frame data and looping GIF previews, with no external tools. The model authors pose-parameterised frames, the bundled stdlib renderer writes sheet, frame data and GI

```markdown
# Animate

Turn a character (an existing spec, or one described in the request) into animation cycles laid
out the way the target engine expects, and show them moving.

## 1. Brief

Follow [`brief.md`](${CLAUDE_PLUGIN_ROOT}/reference/brief.md) the same way `/pixel-art:sprite`
does, including the `brief.md` file, the one-line defaults, and the presence-gated
`/planning:interview` offer. Then add:

- **Cycles** and their purpose: player-controlled actions need responsiveness; enemies and
  cutscene actors can afford anticipation.
- **Directions**: 1 (side-scroller), 4, 8, or isometric.
- **Target layout**: sets frame size, frame count per cycle, direction order, and sheet columns.
  RPG Maker MZ characters, for example, fix 3 patterns x 4 directions at 48x48. Read
  [`engine-layouts.md`](${CLAUDE_PLUGIN_ROOT}/reference/engine-layouts.md).

When the character is an existing spec that already has `brief.md` beside it, read that file and
extend it with cycles, directions, and layout. Do not re-ask fields it already answers. Write the
extended brief beside this spec before the first render.

## 2. Plan the cycles

From [`craft-animation.md`](${CLAUDE_PLUGIN_ROOT}/reference/craft-animation.md) choose, per cycle,
the key poses, frame count, per-frame duration, and loop direction. Write the plan as a short table
before drawing: it is the review rubric later. Engine layouts override craft defaults (MZ walk is
3 patterns played 0-1-2-1).

## 3. Author

Use a procedural generator for anything past a couple of frames: one `draw(direction, pose)`
function whose parameters (limb angles, step phase, body bob, arm swing, squash) produce each
frame, so every frame stays on-model and a fix lands in every frame at once. For a humanoid
walker, start from `${CLAUDE_PLUGIN_ROOT}/scripts/kit.py` and adapt it: a proportion preset
(`chibi`, `standard`, `tall`), a head shape, a hair shape, material ramps, and an `extra`
callback for clothing or props. `${CLAUDE_PLUGIN_ROOT}/examples/walker/blacksmith.py` is a
4-direction walker built that way. `${CLAUDE_PLUGIN_ROOT}/examples/campfire/hero_mz.py` is an
earlier hand-written MZ sheet; copy either example into the working directory before running it, with `kit.py` beside `blacksmith.py`.
Draw one side view and mirror it for the other only when the design is symmetric; the kit shades
after the mirror so the light stays top-left.

A PNG from another backend is snapped with `render.py --snap` before its rows enter the spec
([`backends.md`](${CLAUDE_PLUGIN_ROOT}/reference/backends.md)). Palette presets and project palette
files are the same strings `sprite` uses ([`palettes/README.md`](${CLAUDE_PLUGIN_ROOT}/palettes/README.md)).

Name frames `<cycle>_<direction><index>` or the engine's own names, list them in `sheet.order` in
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

## sprite-pipeline (2696-game-studio)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/game-studio
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2696-game-studio/10368-sprite-pipeline
- الوصف: Generate and normalize 2D sprite animations. Use when the user asks for full-strip generation from approved source frames, consistent anchor and scale normalization, or preview assets for browser-game animation.

```markdown
# Sprite Pipeline

## Overview

Use this skill for 2D sprite generation and normalization. This workflow is intentionally anchored around one approved frame and a whole-strip generation pass because frame-by-frame generation drifts too easily.

This skill is 2D-specific. If the request is for 3D characters, meshes, or materials, route back through `../game-studio/SKILL.md`.

## Core Workflow

1. Start from an approved in-game seed frame.
   - The seed frame should already reflect the right silhouette, palette, costume, and proportions.
2. Build a larger transparent reference canvas around that frame.
   - Use `../../scripts/build_sprite_edit_canvas.py`.
3. Ask for the full animation strip in one edit request.
   - Do not generate each frame independently unless the user explicitly accepts lower consistency.
4. Normalize the result into fixed-size game frames.
   - Use `../../scripts/normalize_sprite_strip.py`.
   - Use one shared scale across the whole strip.
   - Align frames with one shared anchor, typically bottom-center.
5. Optionally lock frame 01 back to the shipped seed frame.
   - Do this when the animation should begin from the exact idle or base pose already in game.
6. Render a preview sheet and inspect the animation in-engine before approving it.
   - Use `../../scripts/render_sprite_preview_sheet.py`.

## Prompting Rules

Always preserve these invariants in the prompt:

- same character
- same facing direction
- same palette family
- same silhouette family
- same readable face or key features
- same outfit proportions
- transparent background
- exact frame count and slot layout

Always ask for:

- one strip at once
- a transparent canvas
- no scenery, labels, or poster composition
- crisp pixel-art clusters for pixel work
- production asset tone, not concept art

## Using Image Generation

For live asset generation or edits, use the installed `imagegen` skill in this workspace. This skill defines the game-specific process; `imagegen` handles the API-backed generation or edit execution.

## Script Recipes

Create a reference canvas:

```bash
python3 scripts/build_sprite_edit_canvas.py \
  --seed output/sprites/idle-01.png \
  --out output/sprites/hurt-edit-canvas.png \
  --frames 4 \
  --slot-size 256 \
  --canvas-size 1024
```

Normalize a raw strip:

```bash
python3 scripts/normalize_sprite_strip.py \
  --input output/sprites/hurt-raw.png \
  --out-dir output/sprites/hurt \
  --frames 4 \
  --frame-size 64 \
  --anchor output/sprites/idle-01.png \
  --lock-frame1
```

Render a preview sheet:

```bash
python3 scripts/render_sprite_preview_sheet.py \
  --frames-dir output/sprites/hurt \
  --out output/sprites/hurt-preview.png \
  --columns 4
```

## Quality Gates

- proportions stay stable across frames
```

## akbun-draw-cartoon-b (1094-akbun-draw)

- الترخيص: **MIT**  ·  الأصل: https://github.com/choisungwook/akbun-aitools/tree/b592650776c4ed1723087911010466d0b537fc6b/plugins/akbun-draw
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1094-akbun-draw/2417-akbun-draw-cartoon-b
- الوصف: 아무 소재(주제·글·이미지·상황)를 "이슈 카드뉴스 낙서 스타일"로 그리는 결과물을 만든다. 이 스타일은 회색 그라데이션 배경 + 얇은 베이지 테두리 액자 + 어린아이 낙서 같은 검정 잉크 라인의 단순한 고래 캐릭터 + 딱 하나의 올리브 그린 포인트 + 왼쪽 아래에 쌓은 굵은 고딕 헤드라인으로 이뤄진, 안전·경고성 카드뉴스 한 장의 그림체다. 이 skill이 고정하는 건 그림체·색감·레이아웃(스타일)이고, 무엇을 그릴지 (소재·구도)는 입력에 맞춰 자유롭게 정한다. 산출물은 두 가지다: 이미지 생성 모델(GPT image, nano-banana 등) AI agent에 그대로 넣을 영어 프롬프트와, Figma/Canva로 가져와 편집할 수 있는 편집 가능 텍스트 SVG 파일. Trigger on: "카드뉴스 

```markdown
# 이슈 카드뉴스 낙서 스타일 프롬프트 + SVG 생성

## 이 skill이 하는 일

아무 소재를 **하나의 정해진 카드뉴스 그림 스타일**로 그린 결과물을 만든다. 그 스타일은 참고 카드
한 장에서 뽑아낸 것이다: 위에서 아래로 밝아졌다 어두워지는 회색 그라데이션 배경, 그 위를 감싸는
얇은 베이지 테두리 액자, 어린아이가 그린 듯한 단순한 검정 잉크 라인의 고래 캐릭터, 화면에서 가장
중요한 사물 **딱 하나에만** 칠한 올리브 그린 포인트, 그리고 왼쪽 아래에 굵은 고딕으로 쌓아 놓은
경고성 헤드라인. 뉴스·SNS에서 보는 안전 이슈 카드뉴스 같은 느낌이다.

**이 skill이 고정하는 것은 "그림체·색감·레이아웃"뿐이다.** 무엇을 그리는지(소재·구도)는 매번 입력에
맞게 자유롭게 정한다. 참고 카드가 "긴 우산을 든 상황"이었다고 해서 그 장면을 재현하는 게 아니다.
그 카드에서 읽어낸 **선·색·배치 처리 방식**을 다른 소재에 그대로 입힌다.

산출물은 그림이 아니라 두 가지다.

1. **영어 이미지 생성 프롬프트** — GPT image나 nano-banana 같은 이미지 생성 AI agent에 그대로 붙여넣는다.
2. **SVG 파일** — 같은 카드를 이 스타일의 벡터로 그린 파일. Figma나 Canva로 가져와 색·문구를 편집한다.

정해진 비주얼 스타일로 카드/포스터 프롬프트와 SVG를 만드는 skill이다. 특정 장면이 아니라
**카드뉴스 스타일 자체**를 재사용한다.

## 캐릭터 (고정 — 고래)

이 카드뉴스는 사람을 그리지 않고 **akbun 마스코트 고래를 낙서풍으로 그린 캐릭터**만 쓴다. 기본
외형(콩 모양 몸통, 흰 배, 작은 지느러미, 점 눈, 곡선 입)은 `akbun-mascot-whale` skill의 캐릭터
스펙을 따르고, 이 skill에서는 어린아이 낙서 같은 잉크 라인으로 렌더링한다. 아래 정의 문장을
프롬프트에 **글자 그대로** 복사한다. 이미지 모델은 문장이 다르면 캐릭터가 달라지므로 표현을 바꾸지
않는다. 사용자가 다른 동작·소품을 지정해도 고래 캐릭터는 유지한다.

고래 캐릭터의 영어 CHARACTER 문장:

```text
a simple naive-doodle rendering of the akbun whale mascot standing upright on its small flat
tail, drawn with a childlike hand-drawn black ink outline: a chubby bean-shaped whale body,
white belly, two small stubby side fins, two black dot eyes and a small curved smile, no other
facial features
```

- **여러 캐릭터가 나오면 채움으로 대비한다.** 행동의 주체인 고래는 **속이 빈 흰색(검정 외곽선만)**
  으로, 그 상황에 당하거나 반응하는 상대 고래는 **꽉 찬 중간 회색 실루엣**으로 그린다. 참고 카드에서
  한 인물은 윤곽선만, 다른 인물은 회색 실루엣이었던 대비를 고래에 그대로 옮긴 것이다.
- **한 마리만 나오면** 흰색(검정 외곽선) 고래로 그린다.

## 스타일 정의 (고정 — 절대 바꾸지 않는다)

무엇을 그리든 아래 그림체·색감·레이아웃은 그대로 유지한다.

- **매체**: 어린아이 낙서 같은 단순한 손그림. 균일한 검정 잉크 아웃라인(`#1A1A1A`)으로 형태만
  그리고, 면은 플랫하게만 칠한다. 그라데이션·질감·해칭·사진 음영 없음(배경 그라데이션은 예외).
- **배경**: 세로 회색 그라데이션. 위 `#EDEDED`(밝은 회색) → 아래 `#8C8C8C`(중간 회색). 배경에
  잡다한 소품을 넣지 않는다.
- **테두리 액자**: 캔버스 안쪽으로 살짝 들여 그린 **얇은 따뜻한 베이지 테두리**(`#CBB994`, 두께 3~5).
  네 변을 감싸는 단순한 사각 액자다.
- **잉크 라인**: `#1A1A1A`, 둥근 모서리·둥근 끝(round join/cap). 손으로 삐뚤빼뚤 그린 듯 단순하다.
- **채움**: 흰색(`#FFFFFF`)과 중간 회색(`#8C8C8C`) 두 톤. 바닥·계단 같은 환경선은 검정 라인만 쓴다.
- **올리브 그린 포인트 (핵심 규칙)**: 머스터드빛 올리브 그린 `#A8B43C` **하나만** 쓴다. 카드가
  말하려는 **핵심 사물 하나**에만 칠한다(예: 위험한 물건, 문제의 대상). 그 외 전부 무채색이다.
- **헤드라인 글씨**: 굵은 고딕. 카드 아래쪽에 왼쪽 정렬로 2~3줄 쌓는다. 색은 진한 회색/검정.
- **분위기**: 안전·경고·목격담 톤의 이슈 카드뉴스. 단순하지만 메시지가 또렷하다.

## 레이아웃·간격 규칙 (참고 카드의 비율을 따른다)

캔버스는 **세로형 카드**다. 기본 `1080×1350`(4:5, 인스타그램 세로형). 요소를 억지로 고정 좌표에 두지
않되, 참고 카드의 **상하좌우 간격 비율**을 지킨다.

- **테두리 액자**: 사방 가장자리에서 약 2%(≈ 22px) 안쪽으로 들여 그린다.
- **그림 영역**: 위 약 3%부터 아래 약 62% 높이까지. 캐릭터와 핵심 사물을 여기 둔다.
- **바닥/지지선**: 캐릭터가 서 있는 계단·바닥·연석 같은 단순한 검정 라인을 화면 중하단(약 45~62% 높이)에
  둔다. 참고 카드처럼 캐릭터에 높이차를 주고 싶으면 계단형으로 그린다.
- **헤드라인 블록**: **왼쪽 아래**. 왼쪽 여백 약 7%(≈ 76px)에서 시작해 왼쪽 정렬로 쌓는다. 첫 줄은
  약 70% 높이, 마지막 줄은 약 93% 높이까지 3줄이 넉넉한 줄간격으로 내려온다.
```

## animate (388-animation-helper)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/animation-helper
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/388-animation-helper/1417-animate
- الوصف: Generate CSS/Framer Motion animations

```markdown
# animation-helper

Generate CSS/Framer Motion animations.

## Tools Available

- **Read** — Read files from the filesystem
- **Write** — Write files to the filesystem
- **Edit** — Make targeted edits to existing files
- **Bash** — Execute shell commands
- **Grep** — Search file contents with regex
- **Glob** — Find files by pattern matching

## Usage

Invoke the `animate` skill to Generate CSS/Framer Motion animations. The skill will analyze the relevant codebase context and generate appropriate output.
```

## klingai-image-to-video (1874-klingai-pack)

- الترخيص: **MIT**  ·  الأصل: https://github.com/jeremylongshore/tons-of-skills-marketplace/tree/b520cf9/plugins/saas-packs/klingai-pack
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/1874-klingai-pack/6075-klingai-image-to-video
- الوصف: Animate static images into video using Kling AI. Use when converting

```markdown
# Kling AI Image-to-Video

## Overview

Animate static images using the `/v1/videos/image2video` endpoint. Supports motion prompts, camera control, dynamic masks (motion brush), static masks, and tail images for start-to-end transitions.

**Endpoint:** `POST https://api.klingai.com/v1/videos/image2video`

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_name` | string | Yes | `kling-v1-5`, `kling-v2-1`, `kling-v2-master`, etc. |
| `image` | string | Yes | URL of the source image (JPG, PNG, WebP) |
| `prompt` | string | No | Motion description for the animation |
| `negative_prompt` | string | No | What to exclude |
| `duration` | string | Yes | `"5"` or `"10"` seconds |
| `aspect_ratio` | string | No | `"16:9"` default |
| `mode` | string | No | `"standard"` or `"professional"` |
| `cfg_scale` | float | No | Prompt adherence (0.0-1.0) |
| `image_tail` | string | No | End-frame image URL (mutually exclusive with masks/camera) |
| `camera_control` | object | No | Camera movement (mutually exclusive with masks/image_tail) |
| `static_mask` | string | No | Mask image URL for fixed regions |
| `dynamic_masks` | array | No | Motion brush trajectories |
| `callback_url` | string | No | Webhook for completion |

## Basic Image-to-Video

```python
import jwt, time, os, requests

BASE = "https://api.klingai.com/v1"

def get_headers():
    ak, sk = os.environ["KLING_ACCESS_KEY"], os.environ["KLING_SECRET_KEY"]
    token = jwt.encode(
        {"iss": ak, "exp": int(time.time()) + 1800, "nbf": int(time.time()) - 5},
        sk, algorithm="HS256", headers={"alg": "HS256", "typ": "JWT"}
    )
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Animate a landscape photo
response = requests.post(f"{BASE}/videos/image2video", headers=get_headers(), json={
    "model_name": "kling-v2-1",
    "image": "https://example.com/landscape.jpg",
    "prompt": "Clouds slowly drifting across the sky, gentle wind rustling through trees",
    "negative_prompt": "static, frozen, blurry",
    "duration": "5",
    "mode": "standard",
})

task_id = response.json()["data"]["task_id"]

# Poll for result
while True:
    time.sleep(15)
    result = requests.get(
        f"{BASE}/videos/image2video/{task_id}", headers=get_headers()
    ).json()
    if result["data"]["task_status"] == "succeed":
        print(f"Video: {result['data']['task_result']['videos'][0]['url']}")
        break
    elif result["data"]["task_status"] == "failed":
        raise RuntimeError(result["data"]["task_status_msg"])
```

## Start-to-End Transition (image_tail)

Use `image_tail` to specify both the first and last frame. Kling interpolates the motion between them.

```python
```
