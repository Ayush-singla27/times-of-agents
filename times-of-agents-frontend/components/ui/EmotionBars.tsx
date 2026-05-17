import { EmotionProfile } from '@/lib/types/emotion'
import { getTopEmotions } from '@/lib/utils/emotions'

interface EmotionBarsProps {
  profile: EmotionProfile
  limit?: number
  className?: string
}

export default function EmotionBars({ profile, limit = 8, className = '' }: EmotionBarsProps) {
  const topEmotions = getTopEmotions(profile, limit)

  return (
    <div className={`flex flex-col gap-y-2 ${className}`}>
      {topEmotions.map(({ emotion, value, color }) => (
        <div key={emotion} className="flex items-center gap-2">
          <span
            className="font-inter text-[11px] text-muted capitalize"
            style={{ minWidth: 88 }}
          >
            {emotion}
          </span>
          <div className="flex-1 bg-gray-100 rounded-full h-1.5 overflow-hidden">
            <div
              className="h-1.5 rounded-full"
              style={{ width: `${value * 100}%`, backgroundColor: color }}
            />
          </div>
          <span
            className="font-inter text-[10px] text-muted text-right"
            style={{ minWidth: 32 }}
          >
            {(value * 100).toFixed(0)}%
          </span>
        </div>
      ))}
    </div>
  )
}
