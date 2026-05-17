'use client'

import { useState } from 'react'
import { AgentTake } from '@/lib/types/agent'
import { Agent } from '@/lib/types/agent'
import AgentAvatar from '@/components/ui/AgentAvatar'
import ToneBadge from '@/components/ui/ToneBadge'
import { getTopEmotions } from '@/lib/utils/emotions'

interface AgentTakeExpandedProps {
  take: AgentTake
  agent: Agent
}

export default function AgentTakeExpanded({ take, agent }: AgentTakeExpandedProps) {
  const [expanded, setExpanded] = useState(false)
  const topEmotions = getTopEmotions(take.emotionProfile, 4)

  return (
    <div className="bg-card-white rounded-xl border border-ap-border p-5">
      {/* Header */}
      <div className="flex items-center gap-3">
        <AgentAvatar
          size="md"
          avatar={agent.avatar}
          avatarBg={agent.avatarBg}
          accentColor={agent.accentColor}
        />
        <span className="font-inter font-bold text-sm text-charcoal">{agent.name}</span>
        <ToneBadge tone={agent.tone} />
      </div>

      {/* Quote */}
      <div className="mt-3 border-l-[3px] border-insight-amber pl-3">
        <p className="font-playfair italic text-[14px] text-charcoal leading-relaxed">
          {take.quote}
        </p>
      </div>

      {/* Expand toggle */}
      <span
        className="mt-2 font-inter text-xs text-analytical-blue cursor-pointer hover:underline inline-block"
        onClick={() => setExpanded((v) => !v)}
      >
        {expanded ? 'Show less' : 'Read full reasoning'}
      </span>

      {/* Full reasoning (expanded) */}
      {expanded && (
        <p className="font-inter text-sm text-charcoal leading-relaxed mt-2">
          {take.fullReasoning}
        </p>
      )}

      {/* Emotion pills row */}
      <div className="mt-3 flex flex-wrap gap-1">
        {topEmotions.map(({ emotion, color }) => (
          <span
            key={emotion}
            className="flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-inter font-semibold text-white"
            style={{ backgroundColor: color }}
          >
            {emotion}
          </span>
        ))}
      </div>
    </div>
  )
}
