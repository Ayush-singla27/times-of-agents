'use client'

import { useState } from 'react'
import { AgentTake } from '@/lib/types/agent'
import { Agent } from '@/lib/types/agent'
import AgentAvatar from '@/components/ui/AgentAvatar'
import ToneBadge from '@/components/ui/ToneBadge'

interface AgentMindmapTabsProps {
  takes: AgentTake[]
  agents: Agent[]
}

export default function AgentMindmapTabs({ takes, agents }: AgentMindmapTabsProps) {
  const visibleTakes = takes.slice(0, 7)
  const [activeIndex, setActiveIndex] = useState(0)

  const activeTake = visibleTakes[activeIndex]
  const activeAgent = agents.find((a) => a.id === activeTake?.agentId)

  if (!activeTake || !activeAgent) return null

  return (
    <div className="bg-card-white rounded-xl border border-ap-border overflow-hidden">
      {/* Tab strip */}
      <div className="flex gap-2 p-4 border-b border-ap-border overflow-x-auto">
        {visibleTakes.map((take, i) => {
          const agent = agents.find((a) => a.id === take.agentId)
          if (!agent) return null
          const isActive = i === activeIndex
          return (
            <button
              key={i}
              onClick={() => setActiveIndex(i)}
              className={`flex items-center gap-2 px-3 py-2 rounded-full cursor-pointer transition-all duration-150 flex-shrink-0 ${
                isActive ? 'text-white' : 'bg-off-white hover:bg-gray-100'
              }`}
              style={isActive ? { backgroundColor: agent.accentColor } : undefined}
            >
              <AgentAvatar
                size="sm"
                avatar={agent.avatar}
                avatarBg={isActive ? 'rgba(255,255,255,0.2)' : agent.avatarBg}
                accentColor={isActive ? 'rgba(255,255,255,0.5)' : agent.accentColor}
              />
              <span className="font-inter text-xs font-bold">{agent.name}</span>
            </button>
          )
        })}
      </div>

      {/* Active tab content panel */}
      <div className="p-5">
        {/* Agent header row */}
        <div className="flex items-center gap-3 mb-4">
          <AgentAvatar
            size="md"
            avatar={activeAgent.avatar}
            avatarBg={activeAgent.avatarBg}
            accentColor={activeAgent.accentColor}
          />
          <span className="font-inter font-bold text-base text-charcoal">{activeAgent.name}</span>
          <ToneBadge tone={activeAgent.tone} />
        </div>

        {/* Reasoning paragraph */}
        <p className="font-inter text-sm text-charcoal leading-relaxed">
          {activeTake.fullReasoning}
        </p>

        {/* Key point block */}
        <div className="mt-4 bg-off-white rounded-lg p-3">
          <p className="font-inter text-[10px] font-bold uppercase tracking-wider text-muted mb-1">
            KEY INSIGHT
          </p>
          <p className="font-inter text-sm text-charcoal font-medium">{activeTake.quote}</p>
        </div>
      </div>
    </div>
  )
}
