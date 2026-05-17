'use client'

import { useState } from 'react'
import { Agent } from '@/lib/types/agent'
import AgentCard from './AgentCard'

interface AgentsGridProps {
  agents: Agent[]
}

export default function AgentsGrid({ agents }: AgentsGridProps) {
  const [activeTone, setActiveTone] = useState<string>('All')

  const uniqueTones = Array.from(new Set(agents.map((a) => a.tone)))

  const filtered =
    activeTone === 'All' ? agents : agents.filter((a) => a.tone === activeTone)

  return (
    <div className="mt-6">
      {/* Filter chips */}
      <div className="flex flex-wrap gap-2">
        {['All', ...uniqueTones].map((tone) => (
          <button
            key={tone}
            onClick={() => setActiveTone(tone)}
            className={`px-4 py-1.5 rounded-full font-inter text-sm font-medium border transition-colors ${
              activeTone === tone
                ? 'bg-charcoal text-white border-charcoal'
                : 'bg-card-white text-muted border-ap-border hover:border-charcoal'
            }`}
          >
            {tone}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mt-6">
        {filtered.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  )
}
