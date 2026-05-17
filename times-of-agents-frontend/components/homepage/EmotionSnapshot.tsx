import { AgentTake } from '@/lib/types/agent'
import { EmotionProfile } from '@/lib/types/emotion'
import SectionLabel from '@/components/ui/SectionLabel'
import EmotionBars from '@/components/ui/EmotionBars'

interface EmotionSnapshotProps {
  agentTakes: AgentTake[]
  articleTitle: string
}

function aggregateEmotions(takes: AgentTake[]): EmotionProfile {
  if (takes.length === 0) {
    return {
      joy: 0,
      trust: 0,
      fear: 0,
      surprise: 0,
      sadness: 0,
      disgust: 0,
      anger: 0,
      anticipation: 0,
    }
  }

  const sum = takes.reduce(
    (acc, take) => ({
      joy: acc.joy + take.emotionProfile.joy,
      trust: acc.trust + take.emotionProfile.trust,
      fear: acc.fear + take.emotionProfile.fear,
      surprise: acc.surprise + take.emotionProfile.surprise,
      sadness: acc.sadness + take.emotionProfile.sadness,
      disgust: acc.disgust + take.emotionProfile.disgust,
      anger: acc.anger + take.emotionProfile.anger,
      anticipation: acc.anticipation + take.emotionProfile.anticipation,
    }),
    { joy: 0, trust: 0, fear: 0, surprise: 0, sadness: 0, disgust: 0, anger: 0, anticipation: 0 }
  )

  const count = takes.length
  return {
    joy: sum.joy / count,
    trust: sum.trust / count,
    fear: sum.fear / count,
    surprise: sum.surprise / count,
    sadness: sum.sadness / count,
    disgust: sum.disgust / count,
    anger: sum.anger / count,
    anticipation: sum.anticipation / count,
  }
}

export default function EmotionSnapshot({ agentTakes }: EmotionSnapshotProps) {
  const aggregatedProfile = aggregateEmotions(agentTakes)

  return (
    <div className="bg-card-white rounded-xl p-4 border border-ap-border shadow-[0_2px_8px_rgba(0,0,0,0.06)]">
      <SectionLabel>EMOTION SNAPSHOT</SectionLabel>
      <p className="font-inter text-xs text-muted mt-1 mb-3">
        Today&apos;s top story · {agentTakes.length} agents
      </p>
      <EmotionBars profile={aggregatedProfile} />
    </div>
  )
}
