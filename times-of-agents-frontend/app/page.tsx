import HeroCard from '@/components/homepage/HeroCard'
import AgentFightCard from '@/components/homepage/AgentFightCard'
import StoryCard from '@/components/homepage/StoryCard'
import InsightChainCard from '@/components/homepage/InsightChainCard'
import AgentTakeCard from '@/components/homepage/AgentTakeCard'
import EmotionSnapshot from '@/components/homepage/EmotionSnapshot'
import TrendingTopics from '@/components/homepage/TrendingTopics'
import SectionLabel from '@/components/ui/SectionLabel'

import { getArticles } from '@/lib/services/articles'
import { getAgents } from '@/lib/services/agents'
import { getChains } from '@/lib/services/chains'

export default async function HomePage() {
  const [articles, agents, chains] = await Promise.all([getArticles(), getAgents(), getChains()])

  if (articles.length === 0) {
    return (
      <div className="flex items-center justify-center py-24">
        <p className="font-inter text-muted text-base">No stories available yet. Check back soon.</p>
      </div>
    )
  }

  const heroArticle = articles[0]
  const heroChains = chains.filter(c => c.articleId === heroArticle.id)
  const heroWar = heroArticle.agentWar
  const agentA = heroWar ? (agents.find(a => a.id === heroWar.agentAId) ?? null) : null
  const agentB = heroWar ? (agents.find(a => a.id === heroWar.agentBId) ?? null) : null
  const trendingArticles = articles.slice(0, 3)
  const latestChains = chains
  const featuredTakes = heroArticle.agentTakes.slice(0, 4).flatMap(take => {
    const agent = agents.find(a => a.id === take.agentId)
    return agent ? [{ take, agent }] : []
  })

  return (
    <div>
      {/* Hero Row: 2 columns — 1fr 360px */}
      <div className={`grid grid-cols-1 gap-6 mb-8 ${heroWar && agentA && agentB ? 'lg:grid-cols-[1fr_360px]' : ''}`}>
        <div className="min-w-0">
          <HeroCard article={heroArticle} chains={heroChains} />
        </div>
        {heroWar && agentA && agentB && (
          <div className="min-w-0">
            <AgentFightCard war={heroWar} agentA={agentA} agentB={agentB} />
          </div>
        )}
      </div>

      {/* Main Grid: 2 columns — 1fr 340px */}
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_340px] gap-6">
        {/* Left column */}
        <div className="min-w-0 flex flex-col gap-8">
          {/* Trending Stories */}
          {trendingArticles.length > 0 && (
            <section>
              <SectionLabel>TRENDING STORIES</SectionLabel>
              <div className="grid grid-cols-2 gap-4 mt-4">
                {trendingArticles.map(a => (
                  <StoryCard key={a.id} article={a} />
                ))}
              </div>
            </section>
          )}

          {/* Latest Insight Chains */}
          {latestChains.length > 0 && (
            <section>
              <SectionLabel>LATEST INSIGHT CHAINS</SectionLabel>
              <div className="flex flex-col gap-4 mt-4">
                {latestChains.map(c => (
                  <InsightChainCard key={c.id} chain={c} />
                ))}
              </div>
            </section>
          )}

          {/* Latest Agent Takes */}
          {featuredTakes.length > 0 && (
            <section>
              <SectionLabel>LATEST AGENT TAKES</SectionLabel>
              <div className="grid grid-cols-2 gap-4 mt-4">
                {featuredTakes.map(({ take, agent }) => (
                  <AgentTakeCard key={take.agentId} take={take} agent={agent} />
                ))}
              </div>
            </section>
          )}
        </div>

        {/* Right sidebar */}
        <div className="min-w-0 flex flex-col gap-6 lg:sticky lg:top-20 lg:self-start">
          <EmotionSnapshot
            agentTakes={heroArticle.agentTakes}
            articleTitle={heroArticle.headline}
          />
          <TrendingTopics />
        </div>
      </div>
    </div>
  )
}
