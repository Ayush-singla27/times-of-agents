import { Article, Debate, DebateMessage } from '@/lib/types/article'
import { InsightChain } from '@/lib/types/chain'
import { articles as mockArticles } from '@/lib/data/articles'

const API_BASE = process.env.API_BASE_URL

function parseSummaryPoints(searchSummary: string, description: string): string[] {
  const text = (searchSummary || description || '').trim()
  if (!text) return []

  // Split on double newlines first (well-structured prose)
  const byParagraph = text.split(/\n\n+/).map(p => p.trim()).filter(p => p.length > 40)
  if (byParagraph.length >= 3) return byParagraph.slice(0, 5)

  // Fall back to splitting on sentence boundaries and grouping pairs
  const sentences = text.match(/[^.!?]+[.!?]+(?:\s|$)/g) ?? []
  const points: string[] = []
  for (let i = 0; i < sentences.length && points.length < 5; i += 2) {
    const point = ((sentences[i] ?? '') + (sentences[i + 1] ?? '')).trim()
    if (point.length > 20) points.push(point)
  }
  return points.length > 0 ? points : [text]
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function transformDebate(articleId: string, raw: any): Debate {
  const messages: DebateMessage[] = (raw.transcript ?? []).map(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (msg: any): DebateMessage => ({
      agentId: msg.agent_id,
      content: msg.content,
      timestamp: msg.created_at,
    })
  )
  return { id: articleId, topic: raw.topic ?? '', messages }
}

// Used for list responses — no debate fetch needed
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function transformArticleSummary(raw: any): Article {
  return {
    id: raw.topic_id,
    slug: raw.topic_id,
    headline: raw.title,
    category: 'News',
    sources: raw.source ? [raw.source] : [],
    timestamp: raw.run_date ? new Date(raw.run_date).toISOString() : new Date().toISOString(),
    isLatest: raw.is_latest ?? false,
    summary: parseSummaryPoints(raw.search_summary, raw.description),
    deepInsight: raw.search_summary ?? '',
    deepInsightAgentId: '',
    chains: [],
    agentTakes: [],
    debates: [],
    agentWar: null,
    stats: {
      agentTakes: 0,
      debates: raw.has_discussion ? 1 : 0,
      chains: 0,
      readers: 0,
    },
  }
}

// Used for single-article responses — includes fetched debate, insight chain, and deep insight
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function transformArticleDetail(
  raw: any,
  debate: Debate | null,
  insightChain: InsightChain | null,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  deepInsightRaw: any | null,
): Article {
  return {
    id: raw.topic_id,
    slug: raw.topic_id,
    headline: raw.title,
    category: 'News',
    sources: raw.source ? [raw.source] : [],
    timestamp: raw.run_date ? new Date(raw.run_date).toISOString() : new Date().toISOString(),
    isLatest: raw.is_latest ?? false,
    summary: parseSummaryPoints(raw.search_summary, raw.description),
    deepInsight: deepInsightRaw?.conclusion ?? raw.search_summary ?? '',
    deepInsightAgentId: deepInsightRaw?.agent_id ?? '',
    chains: insightChain ? [insightChain] : [],
    agentTakes: [],
    debates: debate ? [debate] : [],
    agentWar: null,
    stats: {
      agentTakes: 0,
      debates: debate ? 1 : 0,
      chains: insightChain ? 1 : 0,
      readers: 0,
    },
  }
}

export async function getArticles(): Promise<Article[]> {
  if (!API_BASE) return mockArticles
  const res = await fetch(`${API_BASE}/articles`, { next: { revalidate: 60 } })
  if (!res.ok) throw new Error(`Failed to fetch articles: ${res.status}`)
  const data = await res.json()
  return data.map(transformArticleSummary)
}

export async function getArticle(slug: string): Promise<Article | null> {
  if (!API_BASE) return mockArticles.find(a => a.slug === slug) ?? null

  const [articleRes, debateRes, insightRes, deepInsightRes] = await Promise.allSettled([
    fetch(`${API_BASE}/articles/${slug}`, { next: { revalidate: 60 } }),
    fetch(`${API_BASE}/articles/${slug}/debate`, { next: { revalidate: 60 } }),
    fetch(`${API_BASE}/articles/${slug}/insight`, { next: { revalidate: 60 } }),
    fetch(`${API_BASE}/articles/${slug}/deep_insight`, { next: { revalidate: 60 } }),
  ])

  if (articleRes.status === 'rejected' || !articleRes.value.ok) return null
  const raw = await articleRes.value.json()

  let debate: Debate | null = null
  if (debateRes.status === 'fulfilled' && debateRes.value.ok)
    debate = transformDebate(raw.topic_id, await debateRes.value.json())

  let insightChain: InsightChain | null = null
  if (insightRes.status === 'fulfilled' && insightRes.value.ok)
    insightChain = await insightRes.value.json()

  let deepInsightRaw: unknown | null = null
  if (deepInsightRes.status === 'fulfilled' && deepInsightRes.value.ok)
    deepInsightRaw = await deepInsightRes.value.json()

  return transformArticleDetail(raw, debate, insightChain, deepInsightRaw)
}
