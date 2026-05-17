import { AgentTake } from '@/lib/types/agent'
import { Agent } from '@/lib/types/agent'
import AgentAvatar from '@/components/ui/AgentAvatar'
import ToneBadge from '@/components/ui/ToneBadge'

interface AgentTakeCardProps {
  take: AgentTake
  agent: Agent
}

export default function AgentTakeCard({ take, agent }: AgentTakeCardProps) {
  return (
    <div className="bg-card-white rounded-xl p-4 shadow-[0_2px_8px_rgba(0,0,0,0.06)]">
      {/* Header row */}
      <div className="flex items-center gap-3">
        <AgentAvatar
          size="sm"
          avatar={agent.avatar}
          avatarBg={agent.avatarBg}
          accentColor={agent.accentColor}
        />
        <span className="font-inter font-bold text-sm text-charcoal">{agent.name}</span>
        <ToneBadge tone={agent.tone} size="sm" />
      </div>

      {/* Quote */}
      <blockquote className="mt-3 border-l-2 border-insight-amber pl-3 font-playfair italic text-[13px] text-charcoal leading-relaxed">
        {take.quote}
      </blockquote>
    </div>
  )
}
