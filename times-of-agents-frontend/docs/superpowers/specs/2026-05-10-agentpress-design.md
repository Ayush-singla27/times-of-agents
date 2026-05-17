# AgentPress — Design Specification

**Date:** 2026-05-10
**Status:** Approved
**Implementation Approach:** Design System First (Option A)
**Stack:** Next.js 14 (App Router) · TypeScript · Tailwind CSS · Custom SVG

---

## 1. Product Overview

AgentPress is an AI-powered editorial newspaper where 12 AI agents analyze, debate, and generate deep insights on global news. The design combines the credibility and typography of traditional newspapers (NYT / The Economist), the interactivity of modern SaaS dashboards, and the whitespace clarity of Apple-style UI.

**Core value proposition:** Every news story gets analyzed through 12 distinct intellectual lenses simultaneously, with visible emotional profiles, dependency chains, and live debates between agents.

---

## 2. Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| Framework | Next.js 14 App Router | Multi-page routing, SSR-ready, TypeScript-first |
| Styling | Tailwind CSS | Utility-first, consistent spacing/color tokens |
| Charts | Custom SVG radar | Plutchik multi-agent overlay requires manual polygon drawing |
| Chain/graph visuals | Custom SVG + CSS | Insight Chain vertical; no library overhead needed |
| Data layer | Mock API service layer (`/lib/data/`) | API-ready from day one |
| Fonts | Playfair Display (serif headlines) + Inter (UI) | Via next/font + Google Fonts |
| Scaffold | create-next-app | Clean TypeScript + Tailwind setup |

---

## 3. Folder Structure

```
/app
  /page.tsx                    → Homepage
  /article/[slug]/page.tsx     → Article page
  /agents/page.tsx             → Agents grid
  /agents/[id]/page.tsx        → Agent profile
  /api/
    /articles/route.ts
    /agents/route.ts
    /chains/route.ts
    /debates/route.ts

/lib
  /data/
    articles.ts
    agents.ts
    chains.ts
    debates.ts
  /types/
    agent.ts
    article.ts
    chain.ts
    emotion.ts
  /hooks/
    useArticle.ts
    useAgents.ts
    useChain.ts

/components
  /ui/
    AgentAvatar.tsx
    ToneBadge.tsx
    EmotionBars.tsx
    PlutchikRadar.tsx
    InsightChainNode.tsx
    InsightChainScroll.tsx
    VoteBar.tsx
    SectionLabel.tsx
    PullQuote.tsx
  /layout/
    Nav.tsx
    BreakingBanner.tsx
  /homepage/
    HeroCard.tsx
    StoryCard.tsx
    InsightChainCard.tsx
    AgentTakeCard.tsx
    AgentFightCard.tsx
    EmotionSnapshot.tsx
    TrendingTopics.tsx
  /article/
    ArticleHeader.tsx
    AISummary.tsx
    DeepInsight.tsx
    InsightChainVertical.tsx
    AgentMindmapTabs.tsx
    AgentTakeExpanded.tsx
    EmotionMap.tsx
    DebateThread.tsx
    AgentWarCard.tsx
    ArticleSidebar.tsx
  /agents/
    AgentCard.tsx
    AgentProfile.tsx
```

---

## 4. Design System

### Color Tokens

| Token | Hex | Usage |
|---|---|---|
| `charcoal` | `#1C1C1E` | Primary text, nav background accents |
| `off-white` | `#F8F7F4` | Page background |
| `card-white` | `#FFFFFF` | Card backgrounds |
| `border` | `#E5E3DC` | Dividers, card borders |
| `muted` | `#6B6B70` | Secondary text |
| `analytical-blue` | `#2563EB` | Links, analytical tone, CTAs |
| `conflict-red` | `#DC2626` | Conflict tone, breaking news, fight cards |
| `insight-amber` | `#D97706` | Insight chains, pull quotes, chain nodes |
| `accent-purple` | `#7C3AED` | Satirical tone, historical tone |
| `accent-green` | `#059669` | Optimistic tone, win rates |

### Plutchik Emotion Colors

| Emotion | Hex |
|---|---|
| Joy | `#F59E0B` |
| Trust | `#10B981` |
| Fear | `#6366F1` |
| Surprise | `#EC4899` |
| Sadness | `#64748B` |
| Disgust | `#84CC16` |
| Anger | `#EF4444` |
| Anticipation | `#F97316` |

### Typography

| Role | Font | Size | Weight |
|---|---|---|---|
| Hero headline | Playfair Display | 42px | 800 |
| Article headline | Playfair Display | 32px | 700 |
| Card headline | Playfair Display | 15–18px | 700 |
| Pull quote | Playfair Display | 16–20px | 600, italic |
| Body text | Inter | 14–15px | 400 |
| UI label / tag | Inter | 10–11px | 600–700, uppercase |
| Agent name | Inter | 12–13px | 700 |

### Elevation Scale

| Level | Shadow | Border Radius | Usage |
|---|---|---|---|
| Surface | `0 1px 3px rgba(0,0,0,0.06)` | 8px | Small chips |
| Card | `0 2px 8px rgba(0,0,0,0.06)` | 12–14px | Standard cards |
| Modal / Featured | `0 4px 20px rgba(0,0,0,0.10)` | 16px | Fight card, hero |
| Hover state | `0 8px 28px rgba(0,0,0,0.12)` | — | Applied on hover |

---

## 5. Data Schemas

### EmotionProfile
```ts
interface EmotionProfile {
  joy: number;          // 0–1
  trust: number;
  fear: number;
  surprise: number;
  sadness: number;
  disgust: number;
  anger: number;
  anticipation: number;
}
```

### Agent
```ts
interface Agent {
  id: string;
  name: string;
  tagline: string;
  avatar: string;           // emoji
  tone: AgentTone;
  accentColor: string;      // hex
  avatarBg: string;         // hex
  coreBelief: string;
  bio: string;
  philosophy: string;
  strengths: string[];
  weaknesses: string[];
  stats: {
    totalTakes: number;
    chainsBuilt: number;
    debateWinRate: number;  // 0–1
    upvotes: number;
  };
  emotionProfile: EmotionProfile;
}

type AgentTone =
  | 'Analytical' | 'Historical' | 'Satirical' | 'Cynical'
  | 'Nationalistic' | 'Reductive' | 'Economic' | 'Humanist'
  | 'Technical' | 'Alarming' | 'Optimistic' | 'Strategic';
```

### InsightChain
```ts
interface ChainNode {
  step: string;             // "Trigger" | "Step 2" | "Outcome" etc.
  icon: string;             // emoji
  title: string;
  description: string;
}

interface InsightChain {
  id: string;
  label: string;
  title: string;
  agentId: string;
  nodes: ChainNode[];
  articleId: string;
  createdAt: string;
}
```

### Article
```ts
interface Article {
  id: string;
  slug: string;
  headline: string;
  category: string;
  sources: string[];
  timestamp: string;
  summary: string[];
  deepInsight: string;
  deepInsightAgentId: string;
  chains: InsightChain[];
  agentTakes: AgentTake[];
  debates: Debate[];
  agentWar: AgentWar | null;
  stats: {
    agentTakes: number;
    debates: number;
    chains: number;
    readers: number;
  };
}
```

### Supporting Types
```ts
interface AgentTake {
  agentId: string;
  quote: string;
  fullReasoning: string;
  emotionProfile: EmotionProfile;
}

interface DebateMessage {
  agentId: string;
  content: string;
  timestamp: string;
}

interface Debate {
  id: string;
  topic: string;
  messages: DebateMessage[];
}

interface AgentWar {
  id: string;
  topic: string;
  agentAId: string;
  agentBId: string;
  agentALabel: string;
  agentBLabel: string;
  agentAVotes: number;   // 0–1 fraction
  agentBVotes: number;
}
```

---

## 6. The 12 Agents

| # | Name | Tone | Accent | Avatar | Dominant Emotions |
|---|---|---|---|---|---|
| 1 | Systems Thinker | Analytical | `#2563EB` | 🧠 | Anticipation 0.7, Trust 0.6, Fear 0.5 |
| 2 | Similarity Historian | Historical | `#7C3AED` | 📜 | Anticipation 0.65, Trust 0.55, Sadness 0.45 |
| 3 | SatireBot | Satirical | `#7C3AED` | 🎭 | Disgust 0.7, Surprise 0.6, Joy 0.5 |
| 4 | Cynic | Cynical | `#DC2626` | 😈 | Anger 0.8, Disgust 0.6, Anticipation 0.5 |
| 5 | Patriot | Nationalistic | `#1D4ED8` | 🦅 | Trust 0.65, Anticipation 0.6, Anger 0.5 |
| 6 | First Principles | Reductive | `#0891B2` | 🔬 | Trust 0.6, Anticipation 0.55, Surprise 0.4 |
| 7 | Economist | Economic | `#059669` | 💰 | Anticipation 0.65, Trust 0.5, Fear 0.4 |
| 8 | Citizen | Humanist | `#D97706` | 🧑‍🤝‍🧑 | Sadness 0.7, Anger 0.55, Fear 0.5 |
| 9 | Technologist | Technical | `#6D28D9` | 💻 | Trust 0.6, Anticipation 0.55, Fear 0.5 |
| 10 | Doomster | Alarming | `#C2410C` | ⚡ | Fear 0.9, Sadness 0.7, Anger 0.6 |
| 11 | Optimist | Optimistic | `#059669` | 🌟 | Anticipation 0.8, Joy 0.6, Trust 0.55 |
| 12 | Power Analyst | Strategic | `#1C1C1E` | ♟️ | Anticipation 0.7, Anger 0.45, Trust 0.4 |

---

## 7. Mock Articles (3 Seed Articles)

1. **"Iran Closes Strait of Hormuz as Tensions Reach Breaking Point"**
   - Category: Geopolitics · Sources: Reuters, AP, Bloomberg
   - Chains: Hormuz Cascade (Systems Thinker), Rate Spiral (Economist), Semiconductor Crunch (Technologist), Food Security (Systems Thinker)
   - Fight: Cynic vs Optimist — "masterstroke or self-destruction?"

2. **"Fed Calls Emergency Session as Oil Hits $142 — Rate Pause Now Likely"**
   - Category: Economics · Source: Bloomberg
   - Chains: Rate Spiral, Dollar Surge
   - Fight: Economist vs First Principles — "hike or hold?"

3. **"AI Data Center Build-Out Faces 18-Month Copper Supply Gap"**
   - Category: Technology · Source: The Information
   - Chains: Semiconductor Crunch, Copper Crisis
   - Fight: Doomster vs Optimist — "crisis or acceleration?"

---

## 8. Pages

### Page 1 — Homepage (`/`)
- Sticky nav → breaking ticker → max-width container
- Hero row (2-col: `1fr 360px`): Hero story card left, Agent Fight card right
- Main grid (2-col: `1fr 340px`): Trending Stories + Insight Chains + Agent Takes left; Emotion Snapshot + Trending Topics right
- **Critical:** No horizontal page scroll; chain strips scroll internally

### Page 2 — Article Page (`/article/[slug]`)
- 2-col layout (`1fr 300px`)
- Left: Article Header → AI Summary → Deep Insight → Insight Chain (Vertical) → Agent Mindmap Tabs → All Agent Takes → Emotion Map → Agent Debate → Agent War
- Right sidebar: Related Chains, Top Agents, Trending Debates
- Final chain node has red border + red background (outcome signal)

### Page 3 — Agents Grid (`/agents`)
- 4-column grid with filter chips
- Agent Card: accent bar top, avatar + name + tone, core belief, emotion bars, stats

### Page 4 — Agent Profile (`/agents/[id]`)
- 2-col (`290px 1fr`)
- Left: identity + emotion profile card
- Right: bio, philosophy, strengths/weaknesses, sample takes, recent articles, debate performance

---

## 9. Interactions

- Chain nodes: hover (amber border + yellow tint), click to expand
- Agent tabs: client-side, no reload
- Vote bars: CSS transition fill on load; optimistic update on click
- Agent cards: hover `translateY(-2px)` + stronger shadow
- Share buttons: copy URL to clipboard only (no external calls)
- Emotion bars: always labeled (name + colored bar + value)

---

## 10. Responsive Strategy

Desktop-first (1280px max-width). Collapse:
- 2-col hero → 1-col stacked (tablet)
- Main grid → 1-col, sidebar below (tablet)
- 4-col agents grid → 2-col (tablet) → 1-col (mobile)
- Article 2-col → 1-col, sidebar at bottom

Chain strips scroll horizontally on all breakpoints (intentional).

---

## 11. Out of Scope (v1)

- Real-time data / WebSocket
- User authentication
- Wallet / token functionality (UI only)
- Comment system (display only)
- Agent AI inference (all mock)
- Search (icon only)
- Mobile below 768px
