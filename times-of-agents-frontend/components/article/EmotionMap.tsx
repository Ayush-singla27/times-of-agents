import { AgentTake, Agent } from '@/lib/types/agent'
import { EmotionProfile } from '@/lib/types/emotion'
import PlutchikRadar from '@/components/ui/PlutchikRadar'
import SectionLabel from '@/components/ui/SectionLabel'

interface EmotionMapProps {
  takes: AgentTake[]
  agents: Agent[]
}

const FEATURED_AGENTS = [
  { id: 'systems-thinker', color: '#2563EB' },
  { id: 'cynic',           color: '#B83A2E' },
  { id: 'optimist',        color: '#059669' },
  { id: 'doomster',        color: '#C2410C' },
]

const EMOTION_DESCRIPTIONS: Record<keyof EmotionProfile, string> = {
  joy:          'optimism and positive outlook',
  trust:        'confidence and credibility',
  fear:         'risk awareness and caution',
  surprise:     'shock and unexpectedness',
  sadness:      'loss and regret',
  disgust:      'rejection and moral alarm',
  anger:        'frustration and resistance',
  anticipation: 'expectation and forward focus',
}

function getDominantEmotion(profile: EmotionProfile): { name: keyof EmotionProfile; value: number } {
  const entries = Object.entries(profile) as [keyof EmotionProfile, number][]
  const [name, value] = entries.reduce((best, curr) => curr[1] > best[1] ? curr : best)
  return { name, value }
}

export default function EmotionMap({ takes, agents }: EmotionMapProps) {
  const traces = FEATURED_AGENTS.flatMap(({ id, color }) => {
    const take = takes.find(t => t.agentId === id)
    const agent = agents.find(a => a.id === id)
    if (!take || !agent) return []
    return [{ profile: take.emotionProfile, color, label: agent.name }]
  })

  // Compute consensus: average each emotion across all traces
  let consensusEmotion: keyof EmotionProfile = 'anticipation'
  if (traces.length > 0) {
    const emotions = Object.keys(traces[0].profile) as (keyof EmotionProfile)[]
    const averages = emotions.map(emotion => ({
      emotion,
      avg: traces.reduce((sum, t) => sum + t.profile[emotion], 0) / traces.length,
    }))
    const top = averages.reduce((best, curr) => curr.avg > best.avg ? curr : best)
    consensusEmotion = top.emotion
  }

  return (
    <div className="bg-card-white rounded-xl border border-ap-border p-5">
      <SectionLabel>EMOTION MAP</SectionLabel>
      <p className="font-inter text-xs text-muted mt-1 mb-4">
        Emotional profiles across 4 agent perspectives
      </p>

      <div className="flex flex-col lg:flex-row gap-6 items-start">
        {/* Radar */}
        <PlutchikRadar traces={traces} size={280} />

        {/* Legend + Consensus */}
        <div className="flex-1">
          <p className="font-inter text-[10px] font-bold uppercase tracking-wider text-muted mb-3">
            AGENT LEGEND
          </p>

          <div className="flex flex-col gap-2">
            {traces.map((trace) => {
              const dominant = getDominantEmotion(trace.profile)
              return (
                <div key={trace.label} className="flex items-center gap-2">
                  <span
                    className="w-3 h-3 rounded-full flex-shrink-0"
                    style={{ backgroundColor: trace.color }}
                  />
                  <span className="font-inter text-sm font-bold text-charcoal">{trace.label}</span>
                  <span className="font-inter text-xs text-muted">
                    → {dominant.name} ({dominant.value.toFixed(2)})
                  </span>
                </div>
              )
            })}
          </div>

          {/* Consensus Signal */}
          <div className="mt-4 bg-off-white rounded-lg p-3">
            <p className="font-inter text-[10px] font-bold uppercase tracking-wider text-muted">
              CONSENSUS SIGNAL
            </p>
            <p className="mt-1 font-inter text-sm text-charcoal">
              Dominant across agents:{' '}
              <span className="font-bold">{consensusEmotion}</span>
              {' '}— reflecting heightened {EMOTION_DESCRIPTIONS[consensusEmotion]}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
