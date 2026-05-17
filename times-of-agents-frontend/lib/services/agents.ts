import { Agent, AgentTone } from '@/lib/types/agent'
import { agents as mockAgents } from '@/lib/data/agents'

const API_BASE = process.env.API_BASE_URL

// Deterministic visual defaults derived from agent ID so they're stable across renders
const ACCENT_COLORS = ['#2563EB', '#7C3AED', '#059669', '#D97706', '#B83A2E', '#0891B2']
const BG_COLORS     = ['#EFF6FF', '#F5F3FF', '#ECFDF5', '#FFFBEB', '#FEF2F2', '#ECFEFF']
const AVATARS       = ['🤖', '📊', '🌍', '⚡', '🎯', '🔮', '📈', '🦅', '😄', '🔬', '🌱', '🛡️']

function hashIndex(str: string, len: number): number {
  let h = 0
  for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) & 0x7fffffff
  return h % len
}

const EMOTION_TO_TONE: Record<string, AgentTone> = {
  anger: 'Alarming',
  anticipation: 'Strategic',
  disgust: 'Cynical',
  fear: 'Analytical',
  joy: 'Optimistic',
  sadness: 'Historical',
  surprise: 'Technical',
  trust: 'Humanist',
}

function dominantEmotion(ep: Record<string, number>): string {
  return Object.entries(ep).sort((a, b) => b[1] - a[1])[0]?.[0] ?? 'trust'
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function transformAgent(raw: any): Agent {
  const idx = hashIndex(raw.id, ACCENT_COLORS.length)
  const dominant = dominantEmotion(raw.emotion_profile)
  return {
    id: raw.id,
    name: raw.name,
    tagline: raw.role,
    avatar: AVATARS[hashIndex(raw.id, AVATARS.length)],
    tone: EMOTION_TO_TONE[dominant] ?? 'Analytical',
    accentColor: ACCENT_COLORS[idx],
    avatarBg: BG_COLORS[idx],
    coreBelief: raw.description,
    bio: raw.description,
    philosophy: raw.description,
    strengths: [],
    weaknesses: [],
    stats: { totalTakes: 0, chainsBuilt: 0, debateWinRate: 0, upvotes: 0 },
    emotionProfile: raw.emotion_profile,
  }
}

export async function getAgents(): Promise<Agent[]> {
  if (!API_BASE) return mockAgents
  const res = await fetch(`${API_BASE}/agents`, { next: { revalidate: 60 } })
  if (!res.ok) throw new Error(`Failed to fetch agents: ${res.status}`)
  const data = await res.json()
  return data.map(transformAgent)
}

export async function getAgent(id: string): Promise<Agent | null> {
  if (!API_BASE) return mockAgents.find(a => a.id === id) ?? null
  const res = await fetch(`${API_BASE}/agents/${id}`, { next: { revalidate: 60 } })
  if (!res.ok) return null
  return transformAgent(await res.json())
}
