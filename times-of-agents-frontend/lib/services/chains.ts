import { InsightChain } from '@/lib/types/chain'
import { chains as mockChains } from '@/lib/data/chains'

const API_BASE = process.env.API_BASE_URL

export async function getChains(): Promise<InsightChain[]> {
  if (!API_BASE) return mockChains
  try {
    const res = await fetch(`${API_BASE}/chains`, { next: { revalidate: 60 } })
    if (!res.ok) return mockChains
    return res.json()
  } catch {
    return mockChains
  }
}

export async function getChainsByArticle(articleId: string): Promise<InsightChain[]> {
  if (!API_BASE) return mockChains.filter(c => c.articleId === articleId)
  try {
    const res = await fetch(`${API_BASE}/chains?articleId=${articleId}`, { next: { revalidate: 60 } })
    if (!res.ok) return []
    return res.json()
  } catch {
    return []
  }
}
