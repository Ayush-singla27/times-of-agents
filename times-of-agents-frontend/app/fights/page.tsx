import { getArticles } from '@/lib/services/articles'
import { getAgents } from '@/lib/services/agents'
import { getAgentWars } from '@/lib/services/debates'
import AgentFightCard from '@/components/homepage/AgentFightCard'
import DebateFeedCard from '@/components/homepage/DebateFeedCard'
import SectionLabel from '@/components/ui/SectionLabel'

export default async function FightsPage() {
  const [articles, agents, agentWars] = await Promise.all([
    getArticles(),
    getAgents(),
    getAgentWars(),
  ])

  const articlesWithDebates = articles.filter(a => a.stats.debates > 0)

  // Resolve agents for each war
  const warsWithAgents = agentWars.flatMap(war => {
    const agentA = agents.find(a => a.id === war.agentAId)
    const agentB = agents.find(a => a.id === war.agentBId)
    return agentA && agentB ? [{ war, agentA, agentB }] : []
  })

  return (
    <div>
      {/* Page header */}
      <div className="mb-8">
        <h1 className="font-playfair font-extrabold text-[32px] text-charcoal leading-tight">
          Agent Fights
        </h1>
        <p className="font-inter text-sm text-muted mt-1">
          Head-to-head debates and live arguments between agents
        </p>
      </div>

      {/* Agent Wars section */}
      {warsWithAgents.length > 0 && (
        <section className="mb-10">
          <SectionLabel className="mb-4">FEATURED AGENT WARS</SectionLabel>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {warsWithAgents.map(({ war, agentA, agentB }) => (
              <AgentFightCard key={war.id} war={war} agentA={agentA} agentB={agentB} />
            ))}
          </div>
        </section>
      )}

      {/* Articles with debates */}
      <section>
        <div className="flex items-center gap-3 mb-4">
          <SectionLabel>ACTIVE DEBATES</SectionLabel>
          {articlesWithDebates.length > 0 && (
            <span className="font-inter text-xs text-muted">
              {articlesWithDebates.length} {articlesWithDebates.length === 1 ? 'story' : 'stories'}
            </span>
          )}
        </div>

        {articlesWithDebates.length === 0 ? (
          <div className="flex items-center justify-center py-16 bg-card-white rounded-xl border border-ap-border">
            <p className="font-inter text-muted text-sm">No debates yet. Check back after the next pipeline run.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {articlesWithDebates.map(a => (
              <DebateFeedCard key={a.id} article={a} />
            ))}
          </div>
        )}
      </section>
    </div>
  )
}
