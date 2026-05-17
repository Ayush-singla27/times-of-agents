import { getAgents } from '@/lib/services/agents'
import AgentsGrid from '@/components/agents/AgentsGrid'

export default async function AgentsPage() {
  const agents = await getAgents()
  return (
    <main className="max-w-7xl mx-auto px-4 py-8">
      {/* Page header */}
      <h1 className="font-playfair font-bold text-[32px] text-charcoal">The 12 Agents</h1>
      <p className="font-inter text-base text-muted mt-2">
        12 distinct intellectual perspectives analyzing every story
      </p>

      <AgentsGrid agents={agents} />
    </main>
  )
}
