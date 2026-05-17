import { getAgents, getAgent } from '@/lib/services/agents'
import { getArticles } from '@/lib/services/articles'
import AgentProfile from '@/components/agents/AgentProfile'

export async function generateStaticParams() {
  const agents = await getAgents()
  return agents.map(a => ({ id: a.id }))
}

export default async function AgentProfilePage({ params }: { params: { id: string } }) {
  const [agent, articles] = await Promise.all([getAgent(params.id), getArticles()])
  if (!agent) return <div className="p-8 font-inter text-muted">Agent not found.</div>

  const recentArticles = articles.filter(article =>
    article.agentTakes.some(t => t.agentId === agent.id)
  )

  const sampleTakes = recentArticles
    .map(a => a.agentTakes.find(t => t.agentId === agent.id)!)
    .filter(Boolean)
    .slice(0, 3)

  return (
    <main className="max-w-7xl mx-auto px-4 py-8">
      <AgentProfile agent={agent} recentArticles={recentArticles} sampleTakes={sampleTakes} />
    </main>
  )
}
