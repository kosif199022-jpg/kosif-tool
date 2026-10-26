# مصادر «تطبيق واجهة React» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## react-state-management (3096-frontend-mobile-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/smartwatermelon/claude-code-workflows-agents/tree/2a305d553313a8279ce1c2a58b032516366b6093/plugins/frontend-mobile-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3096-frontend-mobile-development/13266-react-state-management
- الوصف: Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or choosing between state management solutions.

```markdown
# React State Management

Comprehensive guide to modern React state management patterns, from local component state to global stores and server state synchronization.

## When to Use This Skill

- Setting up global state management in a React app
- Choosing between Redux Toolkit, Zustand, or Jotai
- Managing server state with React Query or SWR
- Implementing optimistic updates
- Debugging state-related issues
- Migrating from legacy Redux to modern patterns

## Core Concepts

### 1. State Categories

| Type             | Description                  | Solutions                     |
| ---------------- | ---------------------------- | ----------------------------- |
| **Local State**  | Component-specific, UI state | useState, useReducer          |
| **Global State** | Shared across components     | Redux Toolkit, Zustand, Jotai |
| **Server State** | Remote data, caching         | React Query, SWR, RTK Query   |
| **URL State**    | Route parameters, search     | React Router, nuqs            |
| **Form State**   | Input values, validation     | React Hook Form, Formik       |

### 2. Selection Criteria

```
Small app, simple state → Zustand or Jotai
Large app, complex state → Redux Toolkit
Heavy server interaction → React Query + light client state
Atomic/granular updates → Jotai
```

## Quick Start

### Zustand (Simplest)

```typescript
// store/useStore.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface AppState {
  user: User | null
  theme: 'light' | 'dark'
  setUser: (user: User | null) => void
  toggleTheme: () => void
}

export const useStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        theme: 'light',
        setUser: (user) => set({ user }),
        toggleTheme: () => set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light'
        })),
      }),
      { name: 'app-storage' }
    )
  )
)

// Usage in component
function Header() {
  const { user, theme, toggleTheme } = useStore()
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  )
}
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Colocate state** - Keep state as close to where it's used as possible
- **Use selectors** - Prevent unnecessary re-renders with selective subscriptions
- **Normalize data** - Flatten nested structures for easier updates
- **Type everything** - Full TypeScript coverage prevents runtime errors
- **Separate concerns** - Server state (React Query) vs client state (Zustand)

### Don'ts
```

## react-state-management (3486-frontend-mobile-development)

- الترخيص: **MIT**  ·  الأصل: https://github.com/wshobson/agents/tree/156b7a5/plugins/frontend-mobile-development
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/3486-frontend-mobile-development/14210-react-state-management
- الوصف: Master modern React state management with Redux Toolkit, Zustand, Jotai, and React Query. Use when setting up global state, managing server state, or choosing between state management solutions.

```markdown
# React State Management

Comprehensive guide to modern React state management patterns, from local component state to global stores and server state synchronization.

## When to Use This Skill

- Setting up global state management in a React app
- Choosing between Redux Toolkit, Zustand, or Jotai
- Managing server state with React Query or SWR
- Implementing optimistic updates
- Debugging state-related issues
- Migrating from legacy Redux to modern patterns

## Core Concepts

### 1. State Categories

| Type             | Description                  | Solutions                     |
| ---------------- | ---------------------------- | ----------------------------- |
| **Local State**  | Component-specific, UI state | useState, useReducer          |
| **Global State** | Shared across components     | Redux Toolkit, Zustand, Jotai |
| **Server State** | Remote data, caching         | React Query, SWR, RTK Query   |
| **URL State**    | Route parameters, search     | React Router, nuqs            |
| **Form State**   | Input values, validation     | React Hook Form, Formik       |

### 2. Selection Criteria

```
Small app, simple state → Zustand or Jotai
Large app, complex state → Redux Toolkit
Heavy server interaction → React Query + light client state
Atomic/granular updates → Jotai
```

## Quick Start

### Zustand (Simplest)

```typescript
// store/useStore.ts
import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'

interface AppState {
  user: User | null
  theme: 'light' | 'dark'
  setUser: (user: User | null) => void
  toggleTheme: () => void
}

export const useStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        theme: 'light',
        setUser: (user) => set({ user }),
        toggleTheme: () => set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light'
        })),
      }),
      { name: 'app-storage' }
    )
  )
)

// Usage in component
function Header() {
  const { user, theme, toggleTheme } = useStore()
  return (
    <header className={theme}>
      {user?.name}
      <button onClick={toggleTheme}>Toggle Theme</button>
    </header>
  )
}
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Colocate state** - Keep state as close to where it's used as possible
- **Use selectors** - Prevent unnecessary re-renders with selective subscriptions
- **Normalize data** - Flatten nested structures for easier updates
- **Type everything** - Full TypeScript coverage prevents runtime errors
- **Separate concerns** - Server state (React Query) vs client state (Zustand)

### Don'ts
```

## react-component (2111-frontend-dev-kit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/ksarelto/dev-ai-plugins/tree/aa2a58815f38800a8ab6d98f80ca032aa1c2fa18/frontend-dev-kit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2111-frontend-dev-kit/7516-react-component
- الوصف: Scaffold a standalone React component folder with the mandatory files — kebab-case name.tsx (button.tsx, custom-button.tsx), styles.ts (required, no exceptions), index.ts, types.ts — following FSD layer conventions. Use when adding a single component outside a full feature slice or wrapping a shadcn primitive.

```markdown
# React Component

## When to use

- Adding a single component to `shared/ui/` (generic, business-agnostic) or a feature's `ui/` folder (business-specific)
- Wrapping a shadcn/ui primitive in a reusable wrapper
- User asks to "create a component" or "scaffold a component"

For a full feature (api hooks + components + types), use the `react-feature` skill instead.

## Where it lives

| Component is... | Goes in |
|-----------------|---------|
| Generic, reused across features, no business meaning (`Button`, `DataTable`, `EmptyState`) | `src/shared/ui/{name}/` |
| Specific to one feature (`UserAvatar`, `OrderStatusBadge`) | `src/features/{feature}/ui/{name}/` |
| A route-level composition of feature components | Not this skill — belongs in `pages/`, thin, no folder of its own |

`{name}` is kebab-case of the PascalCase export: `Button` → `button/`, `CustomButton` → `custom-button/`, `OrderStatusBadge` → `order-status-badge/`.

If a component built inside a feature turns out to be needed by a second feature, promote it to `shared/ui/` rather than importing across features.

## Component folder structure (mandatory)

Every component lives in its own kebab-case folder. This is the required layout — no exceptions, including one-liners:

```
{TargetPath}/{name}/
├── index.ts                  — re-exports the component; a type or constant only if an outside file imports it
├── {name}.tsx                — JSX implementation (button.tsx, custom-button.tsx)
├── styles.ts                 — ALL Tailwind classes; never inline in JSX
├── types.ts                  — {Name}Props interface (optional but common)
├── constants.ts              — closed-set values and key maps (only when needed)
└── {name}.test.tsx           — colocated behavior test, written in the same change
```

Stories are not part of this folder. A `shared/ui` primitive also gets `{name}.stories.tsx` in that folder. A feature gets one story at `features/<slice>/<slice>.stories.tsx` for the public entry. Entity and widget folders do not get stories.

## Instructions

1. Determine the PascalCase export and kebab-case file stem (`CustomButton` / `custom-button`) and target path from the table above
2. Read rules: `component-structure`, `react`, `styling`, `shadcn`, `i18n`, `testing`, `accessibility`. For FSD placement (`shared/ui` vs feature `ui/`), load `architecture-audit`.
3. Create the component folder with the core files (`index.ts`, `{name}.tsx`, `styles.ts`, `types.ts`) **and** `{name}.test.tsx` in the same change.
4. Every visible string is `t(key)` from the slice's `locales/` or `commonKeys` (`i18n` skill). Server data renders as-is.
5. Handlers are named (`handleX`) and declared above the return; JSX only passes the reference.
```

## react-component-craft (2302-frontend-engineering)

- الترخيص: **MIT**  ·  الأصل: https://github.com/mcorbett51090/ravenclaude/tree/300e672ec81d25d7d6a07345aa7783f7c89d5db7/plugins/frontend-engineering
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2302-frontend-engineering/8835-react-component-craft
- الوصف: Build composable, accessible React components: small components with clear props (composition over a flag-laden mega-component), correct hooks (complete deps, no stale closures, effects only for external sync), controlled validated forms, and accessibility in the markup.

```markdown
# React Component Craft

## Compose
Small components, clear props; shared logic in custom hooks. Refactor the thirty-flag god-component.

## Hooks correctly
Complete `useEffect`/`useMemo` **deps**; no stale closures; effects only to **sync with the outside**, not to derive state. Most 'React is weird' bugs are dependency bugs.

## Accessibility in markup
Semantic elements first (`button`/`nav`/`label`), ARIA only to fill gaps, keyboard-operable, focus managed. (Audit -> web-design.)

## Forms & testability
Controlled, validated, accessible errors; stable `data-testid`/roles for `qa-test-automation`.
```

## create-react-component (2106-feature-dev-kit)

- الترخيص: **MIT**  ·  الأصل: https://github.com/ksarelto/dev-ai-plugins/tree/aa2a58815f38800a8ab6d98f80ca032aa1c2fa18/app-dev-kit/feature-dev-kit
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2106-feature-dev-kit/7491-create-react-component
- الوصف: Scaffold a React component in the correct FSD layer — presentational (entities/ui, shared/ui) or smart container (features/ui, widgets/ui) — with matching styles, tests, and index export. Uses real app patterns.

```markdown
# Create React Component

FSD placement only. Procedures live in **frontend-dev-kit**. Load them; do not restate them.

| Need | Skill |
|------|--------|
| Folder, files, export | `frontend-dev-kit:react-component` |
| Classes | `frontend-dev-kit:tailwind-styles` |
| Labels, focus, live regions | `frontend-dev-kit:accessibility` |
| Colocated test | `frontend-dev-kit:testing` |

## Where it goes

| Type | Path |
|------|------|
| Presentational | `entities/<domain>/ui/`, `shared/ui/`, `features/<slice>/ui/` |
| Container | `features/<slice>/ui/`, `widgets/<name>/ui/` |
| Hook reused by two components | `features/<slice>/model/` or `widgets/<name>/model/` |

Export through the slice `index.ts` only what a file outside the folder already imports. Four states: `rules/ui-quality.mdc` (attached by glob).

One kebab-case folder per component (`profile-card/profile-card.tsx`, `styles.ts`, `types.ts` when there are props, `index.ts`, `profile-card.test.tsx`). Never a flat `ProfileCard.tsx`.

If the piece is a shadcn/Radix primitive (button, dialog, drawer, and the rest) and `shared/ui/<name>` is missing, stop and hand it to `shared-engineer`. Do not author a second copy. Compose `@/shared/ui/<name>` in the part order of its registry demo.

Every component follows `{KIT_DIR}/skills/feature-dev/references/ui-build-contract.md` §§ 1–3: `t()` for every visible string, classes in `styles.ts`, named handlers, no JSX ternaries, closed-set constants, no comments, a colocated test.

## What this skill does NOT do

- Does not define TypeScript, Tailwind, a11y, or test recipes.
- Does not create the slice (`create-slice`) or the route (`add-route`).
```

## react-component-convention (2654-web-tasuke)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/ncaq/konoka/tree/3711ff8dfed1585b79a9e6d4336825513d83c264/plugins/web-tasuke
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2654-web-tasuke/10085-react-component-convention
- الوصف: React component file conventions covering structure ordering, one-component-per-file, and splitting bloated components. Use when writing or reviewing React components.

```markdown
# Reactコンポーネントの規約

## ファイル内の構造順序を守る

すべてのコンポーネントファイルは、上から順に次の流れで構成します。

1. デザイン定義 — `sva`/`cva`/`css`などのstyled-system呼び出し
2. props定義 — `type Props = ...`や`interface Props { ... }`
3. Functional Component定義 — `export const Foo: React.FC<Props> = ...`や`export function Foo(props: Props): React.ReactElement { ... }`

import群は当然この前に置きます。
純粋な振る舞いだけのコンポーネントならデザイン定義は省略可能ですが、
それ以外で順序の入れ替えは認めません。

理由: 「見た目」「インターフェース」「振る舞い」の責務分離をファイル内の縦方向で表現することで、
コンポーネントを読むときの認知の階段を一定に保つため。

## 1ファイル1コンポーネント

1つのファイルの中にexport/非exportを問わずコンポーネントを2つ以上書かないでください。

ファイル内で再利用される小さなコンポーネントが必要になった場合は、必ず別ファイルに切り出します。
切り出した先のファイル名はIDEのQuick Openで識別しやすい名前にし、
`index.tsx`や`index.ts`といった汎用名を新規作成しないでください。
既存の`index.tsx`を大幅に書き換える場合も、
リファクタリングの一環として適切なファイル名にリネームします。

例外として、他のコンポーネントのrender propに渡すためのごく小さなコンポーネントは、
その場で定義することを許容します。
`<DataGrid renderRow={...} />`や`columns[i].render`、
`react-hook-form`の`Controller`の`render`などが該当します。
ただし次の条件をすべて満たすこと。

- 呼び出し元のrender関数の引数型にそのまま当てはめられる、数行〜十数行程度の軽量なものに限る
- ファイル内で1度しか使われない。使い回される可能性が出てきた時点で別ファイルに切り出す
- どのrender propに渡すために定義しているのかを説明するコメントを直前に付ける

例:

```tsx
// DataGridのrenderRowに渡すための行コンポーネント。このファイル内でしか使わない
const DeviceRow: React.FC<{ device: Device }> = ({ device }) => (
  <tr>
    <td>{device.id}</td>
    <td>{device.name}</td>
  </tr>
);
```

ファイル内で複数回使う場合、それなりの行数がある場合、
呼び出し側から渡される関数でなく通常のJSXの一部として使っている場合などは、
必ず別ファイルに切り出してください。

## コンポーネントが肥大化してきたら分割する

「関数の始まりからJSXが登場するまでに30行程度かかっている」状態は、
コンポーネントが過剰な責務を持っている兆候です。
次のいずれかの方法で責務を逃します。

- ロジックをカスタムフックに切り出す。state、副作用、メモ化、ハンドラの寄せ集めはほぼ必ずフック化できます
- 表示の塊を子コンポーネントに切り出す
- 算出値をモジュールスコープの純粋関数に切り出す

ただし、JSX自体が長くなることは必ずしも悪ではありません。
判定すべきは「行数」ではなく「認知負荷」です。
次のような状態は危険信号として扱ってください。

- 同一の構造が縦に並んでいるが、わずかな差異があってループに落とせていない
- 条件分岐ごとにJSXの枝が派生しており、どの枝が描画されるかを脳内でトラッキングする必要がある
- 1つの要素のクラス名/propsを組み立てるために手前で何段ものローカル変数を準備している
- 同じblock内でユーザー情報・支払い情報・通知設定のように複数のドメイン概念を扱っている

逆に、整然と並んだ単純な要素列が長いだけであれば、無理に分割する必要はありません。
「他人がこのコンポーネントを上から下まで一気に読めるか」を基準にしてください。
```
