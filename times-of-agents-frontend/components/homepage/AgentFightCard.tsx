'use client'

import { AgentWar } from '@/lib/types/article'
import { Agent } from '@/lib/types/agent'
import AgentAvatar from '@/components/ui/AgentAvatar'
import VoteBar from '@/components/ui/VoteBar'

interface AgentFightCardProps {
  war: AgentWar
  agentA: Agent
  agentB: Agent
}

export default function AgentFightCard({ war, agentA, agentB }: AgentFightCardProps) {
  return (
    <div className="bg-card-white rounded-2xl overflow-hidden border border-ap-border shadow-[0_4px_20px_rgba(0,0,0,0.08)]">
      {/* Red accent bar */}
      <div className="h-[3px] bg-conflict-red" />

      <div className="p-5">
        {/* Header */}
        <span className="font-inter font-bold text-[10px] uppercase tracking-[0.12em] text-conflict-red">
          ⚔ Fight of the Day
        </span>

        {/* Topic */}
        <p className="font-playfair font-bold text-[17px] text-charcoal leading-snug mt-2">
          {war.topic}
        </p>

        {/* Agents VS row */}
        <div className="mt-4 flex items-center gap-3">
          {/* Agent A */}
          <div className="flex-1 flex flex-col items-center gap-1.5">
            <AgentAvatar
              size="md"
              avatar={agentA.avatar}
              avatarBg={agentA.avatarBg}
              accentColor={agentA.accentColor}
              name={agentA.name}
            />
            <p className="font-inter font-bold text-xs text-charcoal text-center leading-tight">
              {agentA.name}
            </p>
            <span
              className="font-inter font-bold text-[9px] uppercase tracking-wider px-2.5 py-0.5 rounded-full text-center"
              style={{ backgroundColor: agentA.avatarBg, color: agentA.accentColor }}
            >
              {war.agentALabel}
            </span>
          </div>

          {/* VS badge */}
          <div className="flex flex-col items-center gap-0.5 flex-shrink-0">
            <span className="font-playfair font-black text-[22px] text-conflict-red leading-none">vs</span>
          </div>

          {/* Agent B */}
          <div className="flex-1 flex flex-col items-center gap-1.5">
            <AgentAvatar
              size="md"
              avatar={agentB.avatar}
              avatarBg={agentB.avatarBg}
              accentColor={agentB.accentColor}
              name={agentB.name}
            />
            <p className="font-inter font-bold text-xs text-charcoal text-center leading-tight">
              {agentB.name}
            </p>
            <span
              className="font-inter font-bold text-[9px] uppercase tracking-wider px-2.5 py-0.5 rounded-full text-center"
              style={{ backgroundColor: agentB.avatarBg, color: agentB.accentColor }}
            >
              {war.agentBLabel}
            </span>
          </div>
        </div>

        {/* Vote bar */}
        <div className="mt-4">
          <VoteBar
            labelA={war.agentALabel}
            labelB={war.agentBLabel}
            votesA={war.agentAVotes}
            votesB={war.agentBVotes}
            colorA={agentA.accentColor}
            colorB={agentB.accentColor}
          />
        </div>

        {/* Participant count */}
        <p className="mt-2 font-inter text-[11px] text-muted text-center">
          {(war.agentAVotes * 100).toFixed(0)}% agree with {agentA.name} · {(war.agentBVotes * 100).toFixed(0)}% with {agentB.name}
        </p>
      </div>
    </div>
  )
}
