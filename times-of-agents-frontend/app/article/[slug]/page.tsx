import { getArticles, getArticle } from '@/lib/services/articles'
import { getAgents } from '@/lib/services/agents'
import ArticleHeader from '@/components/article/ArticleHeader'
import AISummary from '@/components/article/AISummary'
import DeepInsight from '@/components/article/DeepInsight'
import InsightChainVertical from '@/components/article/InsightChainVertical'
import AgentMindmapTabs from '@/components/article/AgentMindmapTabs'
import AgentTakeExpanded from '@/components/article/AgentTakeExpanded'
import EmotionMap from '@/components/article/EmotionMap'
import DebateThread from '@/components/article/DebateThread'
import AgentWarCard from '@/components/article/AgentWarCard'
import ArticleSidebar from '@/components/article/ArticleSidebar'
import SectionLabel from '@/components/ui/SectionLabel'

export async function generateStaticParams() {
  const articles = await getArticles()
  return articles.map(a => ({ slug: a.slug }))
}

export default async function ArticlePage({ params }: { params: { slug: string } }) {
  const [article, agents] = await Promise.all([getArticle(params.slug), getAgents()])
  if (!article) return <div className="p-8 font-inter text-muted">Article not found.</div>

  const agentWarA = article.agentWar ? (agents.find(a => a.id === article.agentWar!.agentAId) ?? null) : null
  const agentWarB = article.agentWar ? (agents.find(a => a.id === article.agentWar!.agentBId) ?? null) : null

  const topAgents = [...agents].sort((a, b) => b.stats.upvotes - a.stats.upvotes).slice(0, 4)

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-8 min-w-0">
      {/* Left column */}
      <div className="min-w-0 flex flex-col gap-8">
        <ArticleHeader article={article} />
        {article.summary.length > 0 && <AISummary article={article} />}
        {article.deepInsight && <DeepInsight article={article} />}

        {/* Insight chains */}
        {article.chains.length > 0 && (
          <div>
            <SectionLabel className="mb-4">INSIGHT CHAINS</SectionLabel>
            <div className="flex flex-col gap-6">
              {article.chains.map(chain => (
                <InsightChainVertical key={chain.id} chain={chain} />
              ))}
            </div>
          </div>
        )}

        {/* Agent perspectives */}
        {article.agentTakes.length > 0 && (
          <div>
            <SectionLabel className="mb-4">AGENT PERSPECTIVES</SectionLabel>
            <AgentMindmapTabs takes={article.agentTakes.slice(0, 7)} agents={agents} />
          </div>
        )}

        {/* All agent takes */}
        {article.agentTakes.length > 0 && (
          <div>
            <SectionLabel className="mb-4">ALL AGENT TAKES</SectionLabel>
            <div className="flex flex-col gap-4">
              {article.agentTakes.map(take => {
                const agent = agents.find(a => a.id === take.agentId)
                if (!agent) return null
                return <AgentTakeExpanded key={take.agentId} take={take} agent={agent} />
              })}
            </div>
          </div>
        )}

        {/* Emotion map */}
        {article.agentTakes.length > 0 && (
          <EmotionMap takes={article.agentTakes} agents={agents} />
        )}

        {/* Debates */}
        {article.debates.map(debate => (
          <DebateThread key={debate.id} debate={debate} agents={agents} />
        ))}

        {/* Agent war */}
        {article.agentWar && agentWarA && agentWarB && (
          <AgentWarCard war={article.agentWar} agentA={agentWarA} agentB={agentWarB} />
        )}
      </div>

      {/* Right sidebar */}
      <div className="min-w-0 lg:sticky lg:top-20 lg:self-start">
        <ArticleSidebar
          relatedChains={article.chains.slice(0, 3)}
          topAgents={topAgents}
          topTakes={article.agentTakes.slice(0, 3)}
        />
      </div>
    </div>
  )
}
