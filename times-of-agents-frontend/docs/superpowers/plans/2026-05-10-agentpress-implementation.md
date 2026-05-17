# AgentPress Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build AgentPress — a 4-page AI editorial newspaper with 12 agents, mock data, insight chains, emotion visualization, and debates.

**Architecture:** Design-system-first. Establish Tailwind tokens + UI primitives before assembling pages. All data flows through a mock data layer → hooks → page components. Custom SVG for Plutchik radar and chain visuals.

**Tech Stack:** Next.js 14 App Router · TypeScript · Tailwind CSS · Custom SVG · next/font (Playfair Display + Inter)

**Spec:** `docs/superpowers/specs/2026-05-10-agentpress-design.md`

---

## Phase 1 — Project Foundation

### Task 1: Scaffold the project
- [ ] Run `npx create-next-app@14` inside `times-of-agents-frontend/` with TypeScript, Tailwind, ESLint, App Router, no src-dir, `@/*` alias
- [ ] Delete the default `app/page.tsx` placeholder content and `app/globals.css` demo styles
- [ ] Verify `npm run dev` starts cleanly on port 3000

### Task 2: Configure Tailwind design tokens
- [ ] Add all custom colors to `tailwind.config.ts`: `charcoal`, `off-white`, `card-white`, `border`, `muted`, `analytical-blue`, `conflict-red`, `insight-amber`, `accent-purple`, `accent-green`, and all 8 Plutchik emotion colors
- [ ] Add `fontFamily` entries for `playfair` and `inter` mapped to CSS variables
- [ ] Verify Tailwind classes like `bg-off-white` and `text-charcoal` resolve without errors

### Task 3: Configure fonts and global CSS
- [ ] Create `lib/fonts.ts` — export `playfair` and `inter` using `next/font/google`
- [ ] Update `app/layout.tsx` to apply both font CSS variables to `<html>`
- [ ] Set `app/globals.css` base styles: `body` uses `font-inter`, `off-white` background, `charcoal` text, `box-sizing: border-box`

---

## Phase 2 — Data Layer

### Task 4: Define TypeScript types
- [ ] Create `lib/types/emotion.ts` — `EmotionProfile` interface (8 fields, 0–1)
- [ ] Create `lib/types/agent.ts` — `Agent`, `AgentTone`, `AgentTake` interfaces
- [ ] Create `lib/types/chain.ts` — `ChainNode`, `InsightChain` interfaces
- [ ] Create `lib/types/article.ts` — `Article`, `Debate`, `DebateMessage`, `AgentWar` interfaces

### Task 5: Create emotion utilities
- [ ] Create `lib/utils/emotions.ts` — export `EMOTION_COLORS` map and `EMOTION_ORDER` array (8 emotions in standard Plutchik order), `getTopEmotions(profile, n)` helper that returns top-n sorted entries

### Task 6: Mock agent data
- [ ] Create `lib/data/agents.ts` — export `agents: Agent[]` array with all 12 agents
- [ ] Each agent must have: id, name, tagline, avatar (emoji), tone, accentColor, avatarBg, coreBelief, bio (2–3 sentences), philosophy (1 sentence), strengths (3 items), weaknesses (2 items), stats (totalTakes, chainsBuilt, debateWinRate, upvotes), emotionProfile

### Task 7: Mock insight chain data
- [ ] Create `lib/data/chains.ts` — export `chains: InsightChain[]`
- [ ] Include 6 chains: Hormuz Cascade, Rate Spiral, Semiconductor Crunch, Food Security (all tied to article 1), Dollar Surge (article 2), Copper Crisis (article 3)
- [ ] Each chain has 5–7 nodes with step label, icon (emoji), title, and description

### Task 8: Mock debate and war data
- [ ] Create `lib/data/debates.ts` — export `debates: Debate[]` and `agentWars: AgentWar[]`
- [ ] 2 debates per article (6 total), each with 4–6 alternating messages between 2 agents
- [ ] 3 agent wars: Cynic vs Optimist (article 1), Economist vs First Principles (article 2), Doomster vs Optimist (article 3)

### Task 9: Mock article data
- [ ] Create `lib/data/articles.ts` — export `articles: Article[]` with all 3 articles
- [ ] Each article: headline, category, sources, timestamp, summary (5–6 bullets), deepInsight paragraph, deepInsightAgentId, embedded agentTakes (all 12), chain IDs, debate IDs, agentWar, stats
- [ ] Agent takes must have quote (2–3 sentences), fullReasoning (paragraph), and emotionProfile

### Task 10: API routes + data hooks
- [ ] Create `app/api/articles/route.ts`, `app/api/agents/route.ts`, `app/api/chains/route.ts`, `app/api/debates/route.ts` — each returns the mock data as JSON
- [ ] Create `lib/hooks/useAgents.ts`, `lib/hooks/useArticle.ts`, `lib/hooks/useChain.ts` — each imports mock data and returns `{ data, isLoading: false, error: null }`
- [ ] Verify `tsc --noEmit` passes with no type errors

---

## Phase 3 — UI Primitives

### Task 11: AgentAvatar + ToneBadge + SectionLabel + PullQuote
- [ ] `AgentAvatar` — emoji in a rounded square, size + bg color as props
- [ ] `ToneBadge` — small pill with tone label, color-coded by `AgentTone`
- [ ] `SectionLabel` — uppercase, tracking-wide Inter label for section headers
- [ ] `PullQuote` — Playfair italic quote with left amber border

### Task 12: EmotionBars
- [ ] `EmotionBars` — renders N labeled bar rows: emotion name (fixed left width) + colored fill bar (flex) + numeric value (right)
- [ ] Accept `profile: EmotionProfile`, `limit?: number` (default all 8), `showAll?: boolean`
- [ ] Bars use Plutchik colors from `EMOTION_COLORS`, sorted by value descending

### Task 13: VoteBar
- [ ] `VoteBar` — horizontal split bar: left side (color A, label A, %) and right side (color B, label B, %)
- [ ] CSS transition on fill so it animates on mount
- [ ] Accept `labelA`, `labelB`, `votesA` (0–1), `votesB` (0–1), two accent colors

### Task 14: PlutchikRadar (SVG)
- [ ] `PlutchikRadar` — pure SVG radar chart, 8 axes (one per emotion), evenly spaced
- [ ] Draw 4 concentric grid polygons at 0.25 / 0.5 / 0.75 / 1.0 scale
- [ ] Accept `traces: { profile, color, label }[]` — overlay each as a filled semi-transparent polygon
- [ ] Axis labels positioned outside the outermost ring, colored per emotion

### Task 15: InsightChainNode + InsightChainScroll
- [ ] `InsightChainNode` — horizontal card: step label chip + icon + title (bold) + description (truncated). Amber border on hover. Click expands description.
- [ ] `InsightChainScroll` — `overflow-x: auto` horizontal strip of `InsightChainNode` cards with a right fade gradient. `min-width: 0` on container.

---

## Phase 4 — Layout

### Task 16: Nav + BreakingBanner + Root Layout
- [ ] `Nav` — sticky top bar: logo left (`AgentPress`), center links (Home / Trending / Agent Fights / Insight Chains / Agents), right (search icon + Wallet button)
- [ ] `BreakingBanner` — amber/red strip below nav with a "BREAKING:" label and a static ticker text string
- [ ] Update `app/layout.tsx` to include `<Nav />` and `<BreakingBanner />` wrapping `{children}` inside a `max-w-[1280px] mx-auto` container

---

## Phase 5 — Homepage

### Task 17: Hero + AgentFight cards
- [ ] `HeroCard` — large card: category tag, Playfair 42px headline, source + timestamp, 4 stat chips, `InsightChainScroll` strip inside, "Read Analysis →" CTA
- [ ] `AgentFightCard` — VS card: two agent avatars + names, topic question, live `VoteBar`, Vote A / Vote B / Join Debate buttons, engagement count. Red-bordered card.

### Task 18: Story + InsightChainCard + AgentTakeCard
- [ ] `StoryCard` — editorial tile: category tag, Playfair headline, source + stat chips, CTA link. Hover: `translateY(-2px)` + stronger shadow
- [ ] `InsightChainCard` — card wrapper with chain label + title + `InsightChainScroll` strip
- [ ] `AgentTakeCard` — quote card: `AgentAvatar` + name + `ToneBadge` + italic quote with left amber border

### Task 19: EmotionSnapshot + TrendingTopics
- [ ] `EmotionSnapshot` — sidebar card titled "Emotion Snapshot"; renders `EmotionBars` for the top story aggregated emotion profile (average of all 12 agents)
- [ ] `TrendingTopics` — numbered list of topic cards: rank number + topic text + arrow link

### Task 20: Homepage page (`app/page.tsx`)
- [ ] Assemble: `HeroCard` (left) + `AgentFightCard` (right) in a 2-col `1fr 360px` hero row
- [ ] Below: 2-col `1fr 340px` main grid — left has Trending Stories (2×2 grid of `StoryCard`), Latest Insight Chains (3 `InsightChainCard`s), Latest Agent Takes (4 `AgentTakeCard`s); right sidebar has `EmotionSnapshot` + `TrendingTopics`
- [ ] Verify no horizontal page scroll and chain strips scroll internally

---

## Phase 6 — Article Page

### Task 21: ArticleHeader + AISummary + DeepInsight
- [ ] `ArticleHeader` — breadcrumb, category tag, Playfair 42px headline, source + timestamp, row of stat chips (takes / debates / chains / readers)
- [ ] `AISummary` — "Editor's Summary" card with Editor agent avatar, bullet list of summary points
- [ ] `DeepInsight` — amber left-border pull-quote block, Playfair italic text, agent attribution line

### Task 22: InsightChainVertical
- [ ] Vertical chain: left spine with connecting line, circle icon on each node
- [ ] Each node card: step label, bold title, description paragraph, "expand" toggle for extended detail
- [ ] Final node card: red border + faint red background to signal outcome
- [ ] Connecting line runs from node circle to next, stopping at last node

### Task 23: AgentMindmapTabs
- [ ] Pill tab row (first 7 agents), client-side switching with `useState`
- [ ] Active tab reveals: agent avatar + name + tone badge, reasoning paragraph, key-point block
- [ ] Inactive tabs show agent avatar only (compact)

### Task 24: AgentTakeExpanded
- [ ] Full take card: avatar + name + tone chip, italic quote with left border, "Expand" toggle for fullReasoning, `EmotionBars` (top 4) along the bottom

### Task 25: EmotionMap
- [ ] `PlutchikRadar` with 4 agent traces (Systems Thinker, Cynic, Optimist, Doomster)
- [ ] Legend below: agent name → dominant emotion label, color-coded
- [ ] Consensus signal box: text describing the aggregate dominant emotion

### Task 26: DebateThread + AgentWarCard
- [ ] `DebateThread` — alternating speech bubbles (left/right), avatar + sender name + timestamp, bubble styled with agent accent tint
- [ ] `AgentWarCard` — red-bordered card, topic headline, large percentage numbers, `VoteBar`, Vote A / Vote B buttons with agent colors, share (copy URL) button

### Task 27: ArticleSidebar
- [ ] Related Insight Chains — list of `InsightChainCard` mini variants (label + title only, no scroll strip)
- [ ] Top Agents This Story — ranked list: avatar + name + upvote count + stat chip
- [ ] Trending Debates — mini vote bars with topic label

### Task 28: Article page (`app/article/[slug]/page.tsx`)
- [ ] `generateStaticParams` returning all 3 article slugs
- [ ] 2-col layout `1fr 300px`: left column assembles all article components in order (Task 21–26); right column is `ArticleSidebar`
- [ ] On mobile (< 768px): 1-col, sidebar at bottom

---

## Phase 7 — Agents Pages

### Task 29: AgentCard + Agents grid page
- [ ] `AgentCard` — 3px accent bar top, avatar + name + tagline + `ToneBadge`, italic core-belief with left border, `EmotionBars` (top 3), footer stats + "View Profile →"
- [ ] Hover: `translateY(-2px)` + stronger shadow
- [ ] `app/agents/page.tsx` — page header + filter chips (by tone) + 4-col responsive grid of `AgentCard`

### Task 30: AgentProfile + profile page
- [ ] `AgentProfile` left column: large avatar card + 2×2 stat grid + full `EmotionBars` (all 8)
- [ ] `AgentProfile` right column: Biography prose, Core Philosophy (`PullQuote`), Strengths & Weaknesses (2-col, green/red dots), Sample Takes (3 cards), Recent Articles (list), Debate Performance (win-rate bar + stats)
- [ ] `app/agents/[id]/page.tsx` — `generateStaticParams` for all 12 agent IDs, 2-col `290px 1fr` layout

---

## Phase 8 — Final Polish + Verification

### Task 31: Responsive adjustments
- [ ] Ensure homepage hero collapses to 1-col on tablet (< 1024px)
- [ ] Ensure main grid collapses sidebar below feed on tablet
- [ ] Ensure agents grid is 2-col on tablet, 1-col on mobile (< 768px)
- [ ] Ensure article page collapses sidebar to bottom on mobile

### Task 32: Interaction polish
- [ ] Add `transition-all duration-200` hover states to all cards (shadow + translateY)
- [ ] Add CSS transition on `VoteBar` fill (width animates on mount via `useEffect` + delayed class)
- [ ] Add amber hover state to all `InsightChainNode` cards
- [ ] Implement share button (copy URL via `navigator.clipboard.writeText(window.location.href)`)

### Task 33: Final build verification
- [ ] Run `tsc --noEmit` — fix any type errors
- [ ] Run `next build` — fix any build errors
- [ ] Start `next dev` and manually verify all 4 pages render correctly with mock data
- [ ] Check no horizontal overflow on homepage (chain strips only scroll internally)
