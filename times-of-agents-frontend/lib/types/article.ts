import { AgentTake } from './agent'
import { InsightChain } from './chain'

export interface DebateMessage {
  agentId: string
  content: string
  timestamp: string
}

export interface Debate {
  id: string
  topic: string
  messages: DebateMessage[]
}

export interface AgentWar {
  id: string
  topic: string
  summary?: string
  agentAId: string
  agentBId: string
  agentALabel: string
  agentBLabel: string
  agentAVotes: number  // 0–1 fraction
  agentBVotes: number
}

export interface Article {
  id: string
  slug: string
  headline: string
  category: string
  sources: string[]
  timestamp: string
  isLatest: boolean
  summary: string[]
  deepInsight: string
  deepInsightAgentId: string
  chains: InsightChain[]
  agentTakes: AgentTake[]
  debates: Debate[]
  agentWar: AgentWar | null
  stats: {
    agentTakes: number
    debates: number
    chains: number
    readers: number
  }
}
