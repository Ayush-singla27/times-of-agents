import { agents } from '@/lib/data/agents'
import { Agent } from '@/lib/types/agent'

export function useAgents(): { agents: Agent[]; isLoading: boolean; error: null } {
  return { agents, isLoading: false, error: null }
}

export function useAgent(id: string): { agent: Agent | null; isLoading: boolean; error: null } {
  const agent = agents.find(a => a.id === id) ?? null
  return { agent, isLoading: false, error: null }
}
