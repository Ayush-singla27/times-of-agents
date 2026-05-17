import { Debate, AgentWar } from '@/lib/types/article'
import { debates as mockDebates, agentWars as mockAgentWars } from '@/lib/data/debates'

const API_BASE = process.env.API_BASE_URL

// Standalone debate/war list endpoints are not yet implemented on the backend.
// Debates are fetched per-article inside lib/services/articles.ts.
// These functions are used by the /api/debates Next.js route; they fall back
// to mock data until the backend exposes dedicated endpoints.

export async function getDebates(): Promise<Debate[]> {
  if (!API_BASE) return mockDebates
  try {
    const res = await fetch(`${API_BASE}/debates`, { next: { revalidate: 60 } })
    if (!res.ok) return mockDebates
    return res.json()
  } catch {
    return mockDebates
  }
}

export async function getAgentWars(): Promise<AgentWar[]> {
  if (!API_BASE) return mockAgentWars
  try {
    const res = await fetch(`${API_BASE}/debates/wars`, { next: { revalidate: 60 } })
    if (!res.ok) return mockAgentWars
    return res.json()
  } catch {
    return mockAgentWars
  }
}
