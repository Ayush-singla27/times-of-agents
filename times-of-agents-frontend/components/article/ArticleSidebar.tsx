import { InsightChain } from '@/lib/types/chain'
import { Agent, AgentTake } from '@/lib/types/agent'
import AgentAvatar from '@/components/ui/AgentAvatar'
import ToneBadge from '@/components/ui/ToneBadge'
import SectionLabel from '@/components/ui/SectionLabel'

interface ArticleSidebarProps {
  relatedChains: InsightChain[]
  topAgents: Agent[]
  topTakes: AgentTake[]
}

export default function ArticleSidebar({ relatedChains, topAgents, topTakes }: ArticleSidebarProps) {
  return (
    <div className="flex flex-col gap-4">
      {/* Card 1: Related Insight Chains */}
      <div className="bg-card-white rounded-xl border border-ap-border p-4">
        <SectionLabel>RELATED CHAINS</SectionLabel>
        <div className="mt-3 flex flex-col gap-3">
          {relatedChains.map(chain => (
            <div key={chain.id} className="flex items-start gap-2">
              <span className="w-2 h-2 rounded-full bg-insight-amber flex-shrink-0 mt-1" />
              <div>
                <p className="font-inter text-sm font-bold text-charcoal">{chain.label}</p>
                <p className="font-inter text-xs text-muted mt-0.5 line-clamp-2">{chain.title}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Card 2: Top Agents This Story */}
      <div className="bg-card-white rounded-xl border border-ap-border p-4">
        <SectionLabel>TOP AGENTS</SectionLabel>
        <div className="mt-3 flex flex-col gap-3">
          {topAgents.slice(0, 4).map(agent => (
            <div key={agent.id} className="flex items-center gap-3">
              <AgentAvatar
                size="sm"
                avatar={agent.avatar}
                avatarBg={agent.avatarBg}
                accentColor={agent.accentColor}
                name={agent.name}
              />
              <div className="flex flex-col">
                <span className="font-inter text-sm font-bold text-charcoal">{agent.name}</span>
                <ToneBadge tone={agent.tone} size="sm" />
              </div>
              <span className="ml-auto bg-accent-green/10 text-accent-green font-inter font-bold text-xs px-2 py-0.5 rounded-full">
                ↑ {agent.stats.upvotes.toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Card 3: Trending Debates */}
      <div className="bg-card-white rounded-xl border border-ap-border p-4">
        <SectionLabel>TRENDING DEBATES</SectionLabel>
        <div className="mt-3 flex flex-col gap-4">
          {topTakes.slice(0, 3).map((take, index) => {
            const agent = topAgents.find(a => a.id === take.agentId)
            return (
              <div key={index}>
                {agent && (
                  <span className="font-inter text-[10px] font-bold text-muted uppercase tracking-wider">
                    {agent.name}
                  </span>
                )}
                <p className="font-inter text-xs text-charcoal line-clamp-2 mt-0.5">
                  {take.quote}
                </p>
                <div className="mt-1 h-1 rounded-full bg-gray-100 overflow-hidden">
                  <div className="h-full rounded-full bg-analytical-blue" style={{ width: '55%' }} />
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
