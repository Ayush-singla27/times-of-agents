import { EmotionProfile } from './emotion'

export type AgentTone =
  | 'Analytical' | 'Historical' | 'Satirical' | 'Cynical'
  | 'Nationalistic' | 'Reductive' | 'Economic' | 'Humanist'
  | 'Technical' | 'Alarming' | 'Optimistic' | 'Strategic'

export interface Agent {
  id: string
  name: string
  tagline: string
  avatar: string        // emoji
  tone: AgentTone
  accentColor: string   // hex
  avatarBg: string      // hex
  coreBelief: string
  bio: string
  philosophy: string
  strengths: string[]
  weaknesses: string[]
  stats: {
    totalTakes: number
    chainsBuilt: number
    debateWinRate: number  // 0–1
    upvotes: number
  }
  emotionProfile: EmotionProfile
}

export interface AgentTake {
  agentId: string
  quote: string
  fullReasoning: string
  emotionProfile: EmotionProfile
}
