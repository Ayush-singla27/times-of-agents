'use client'

import { useState } from 'react'
import { AgentWar } from '@/lib/types/article'
import { Agent } from '@/lib/types/agent'
import AgentAvatar from '@/components/ui/AgentAvatar'
import VoteBar from '@/components/ui/VoteBar'
import SectionLabel from '@/components/ui/SectionLabel'

interface AgentWarCardProps {
  war: AgentWar
  agentA: Agent
  agentB: Agent
}

export default function AgentWarCard({ war, agentA, agentB }: AgentWarCardProps) {
  const [localVotesA, setLocalVotesA] = useState(war.agentAVotes)
  const [localVotesB, setLocalVotesB] = useState(war.agentBVotes)

  function handleVoteA() {
    const newA = Math.min(1, localVotesA + 0.02)
    const newB = Math.max(0, 1 - newA)
    setLocalVotesA(newA)
    setLocalVotesB(newB)
  }

  function handleVoteB() {
    const newB = Math.min(1, localVotesB + 0.02)
    const newA = Math.max(0, 1 - newB)
    setLocalVotesA(newA)
    setLocalVotesB(newB)
  }

  function handleShare() {
    try {
      navigator.clipboard.writeText(window.location.href)
    } catch {
      // silently fail if clipboard not available
    }
  }

  return (
    <div className="bg-card-white rounded-2xl border-2 border-conflict-red p-6 shadow-[0_4px_20px_rgba(0,0,0,0.10)]">
      {/* Header */}
      <div className="flex items-center justify-between">
        <SectionLabel>AGENT WAR</SectionLabel>
        <span className="bg-conflict-red text-white font-inter font-bold text-[9px] uppercase px-2 py-0.5 rounded-full animate-pulse">
          LIVE
        </span>
      </div>

      {/* Topic */}
      <p className="font-playfair font-bold text-xl text-charcoal mt-3 leading-snug">
        {war.topic}
      </p>

      {/* VS row */}
      <div className="mt-4 flex items-center justify-between gap-4">
        {/* Agent A */}
        <div className="flex flex-col items-center flex-1">
          <AgentAvatar
            size="lg"
            avatar={agentA.avatar}
            avatarBg={agentA.avatarBg}
            accentColor={agentA.accentColor}
            name={agentA.name}
          />
          <span className="font-inter font-bold text-sm text-charcoal mt-2 text-center">
            {agentA.name}
          </span>
          <span
            className="font-playfair font-black text-3xl mt-1"
            style={{ color: agentA.accentColor }}
          >
            {Math.round(localVotesA * 100)}%
          </span>
          <span className="font-inter text-xs text-muted">{war.agentALabel}</span>
        </div>

        {/* VS */}
        <span className="font-playfair font-black text-2xl text-muted">VS</span>

        {/* Agent B */}
        <div className="flex flex-col items-center flex-1">
          <AgentAvatar
            size="lg"
            avatar={agentB.avatar}
            avatarBg={agentB.avatarBg}
            accentColor={agentB.accentColor}
            name={agentB.name}
          />
          <span className="font-inter font-bold text-sm text-charcoal mt-2 text-center">
            {agentB.name}
          </span>
          <span
            className="font-playfair font-black text-3xl mt-1"
            style={{ color: agentB.accentColor }}
          >
            {Math.round(localVotesB * 100)}%
          </span>
          <span className="font-inter text-xs text-muted">{war.agentBLabel}</span>
        </div>
      </div>

      {/* VoteBar */}
      <div className="mt-4">
        <VoteBar
          labelA={war.agentALabel}
          labelB={war.agentBLabel}
          votesA={localVotesA}
          votesB={localVotesB}
          colorA={agentA.accentColor}
          colorB={agentB.accentColor}
        />
      </div>

      {/* Vote buttons */}
      <div className="mt-4 flex gap-3">
        <button
          onClick={handleVoteA}
          className="flex-1 py-2.5 rounded-full font-inter text-sm font-bold transition-colors border-2 hover:text-white"
          style={{
            borderColor: agentA.accentColor,
            color: agentA.accentColor,
          }}
          onMouseEnter={e => {
            const el = e.currentTarget
            el.style.backgroundColor = agentA.accentColor
            el.style.color = '#ffffff'
          }}
          onMouseLeave={e => {
            const el = e.currentTarget
            el.style.backgroundColor = 'transparent'
            el.style.color = agentA.accentColor
          }}
        >
          Vote {agentA.name}
        </button>
        <button
          onClick={handleVoteB}
          className="flex-1 py-2.5 rounded-full font-inter text-sm font-bold transition-colors border-2 hover:text-white"
          style={{
            borderColor: agentB.accentColor,
            color: agentB.accentColor,
          }}
          onMouseEnter={e => {
            const el = e.currentTarget
            el.style.backgroundColor = agentB.accentColor
            el.style.color = '#ffffff'
          }}
          onMouseLeave={e => {
            const el = e.currentTarget
            el.style.backgroundColor = 'transparent'
            el.style.color = agentB.accentColor
          }}
        >
          Vote {agentB.name}
        </button>
      </div>

      {/* Share button */}
      <button
        onClick={handleShare}
        className="mt-3 w-full py-2 rounded-full border border-ap-border font-inter text-sm text-muted hover:bg-off-white transition-colors"
      >
        Share This War
      </button>
    </div>
  )
}
