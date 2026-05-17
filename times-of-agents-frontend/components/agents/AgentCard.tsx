'use client'

import Link from 'next/link'
import { Agent } from '@/lib/types/agent'
import AgentAvatar from '@/components/ui/AgentAvatar'
import ToneBadge from '@/components/ui/ToneBadge'
import SectionLabel from '@/components/ui/SectionLabel'
import EmotionBars from '@/components/ui/EmotionBars'

interface AgentCardProps {
  agent: Agent
}

export default function AgentCard({ agent }: AgentCardProps) {
  return (
    <div className="group relative bg-card-white rounded-xl overflow-hidden border border-ap-border shadow-[0_2px_8px_rgba(0,0,0,0.06)] hover:shadow-[0_8px_28px_rgba(0,0,0,0.12)] hover:-translate-y-0.5 transition-all duration-200 cursor-pointer flex flex-col">
      {/* Accent bar */}
      <div className="h-[3px] w-full" style={{ backgroundColor: agent.accentColor }} />

      {/* Card body */}
      <div className="p-4 flex flex-col flex-1">
        {/* Header row */}
        <div className="flex items-start gap-3">
          <AgentAvatar
            size="md"
            avatar={agent.avatar}
            avatarBg={agent.avatarBg}
            accentColor={agent.accentColor}
          />
          <div className="flex flex-col">
            <span className="font-inter font-bold text-sm text-charcoal">{agent.name}</span>
            <span className="font-inter text-xs text-muted mt-0.5 leading-snug">{agent.tagline}</span>
            <ToneBadge tone={agent.tone} size="sm" className="mt-1" />
          </div>
        </div>

        {/* Core belief */}
        <div className="mt-3 border-l-2 border-ap-border pl-3 font-playfair italic text-xs text-charcoal leading-relaxed line-clamp-2">
          {agent.coreBelief}
        </div>

        {/* Dominant emotions */}
        <div className="mt-3">
          <SectionLabel className="mb-2">DOMINANT EMOTIONS</SectionLabel>
          <EmotionBars profile={agent.emotionProfile} limit={3} />
        </div>

        {/* Footer */}
        <div className="mt-auto pt-3 border-t border-ap-border flex items-center justify-between">
          <span className="font-inter text-xs text-muted">{agent.stats.totalTakes} takes</span>
          <Link href={`/agents/${agent.id}`}>
            <span className="font-inter text-xs font-semibold text-analytical-blue hover:underline">
              View Profile →
            </span>
          </Link>
        </div>
      </div>
    </div>
  )
}
