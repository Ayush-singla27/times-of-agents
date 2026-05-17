import { Debate } from '@/lib/types/article'
import { Agent } from '@/lib/types/agent'
import AgentAvatar from '@/components/ui/AgentAvatar'
import SectionLabel from '@/components/ui/SectionLabel'

interface DebateThreadProps {
  debate: Debate
  agents: Agent[]
}

function formatTime(timestamp: string): string {
  const date = new Date(timestamp)
  if (isNaN(date.getTime())) return timestamp
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })
}

export default function DebateThread({ debate, agents }: DebateThreadProps) {
  return (
    <div className="bg-card-white rounded-xl border border-ap-border p-5">
      {/* Header */}
      <SectionLabel>AGENT DEBATE</SectionLabel>

      {/* Messages */}
      <div className="mt-4 flex flex-col gap-4">
        {debate.messages.map((message, index) => {
          const agent = agents.find(a => a.id === message.agentId)
          const isLeft = index % 2 === 0

          if (isLeft) {
            return (
              <div key={index} className="flex gap-3 items-start">
                {agent && (
                  <AgentAvatar
                    size="sm"
                    avatar={agent.avatar}
                    avatarBg={agent.avatarBg}
                    accentColor={agent.accentColor}
                    name={agent.name}
                  />
                )}
                <div>
                  <div className="flex items-baseline">
                    <span className="font-inter text-xs font-bold text-charcoal">
                      {agent?.name ?? message.agentId}
                    </span>
                    <span className="font-inter text-[10px] text-muted ml-2">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                  <div className="mt-1 bg-off-white rounded-2xl rounded-tl-none px-4 py-3">
                    <p className="font-inter text-sm text-charcoal leading-relaxed">
                      {message.content}
                    </p>
                  </div>
                </div>
              </div>
            )
          } else {
            return (
              <div key={index} className="flex flex-row-reverse gap-3 items-start">
                {agent && (
                  <AgentAvatar
                    size="sm"
                    avatar={agent.avatar}
                    avatarBg={agent.avatarBg}
                    accentColor={agent.accentColor}
                    name={agent.name}
                  />
                )}
                <div>
                  <div className="flex flex-row-reverse items-baseline">
                    <span className="font-inter text-xs font-bold text-charcoal">
                      {agent?.name ?? message.agentId}
                    </span>
                    <span className="font-inter text-[10px] text-muted mr-2">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                  <div className="mt-1 bg-charcoal/5 rounded-2xl rounded-tr-none px-4 py-3">
                    <p className="font-inter text-sm text-charcoal leading-relaxed">
                      {message.content}
                    </p>
                  </div>
                </div>
              </div>
            )
          }
        })}
      </div>
    </div>
  )
}
