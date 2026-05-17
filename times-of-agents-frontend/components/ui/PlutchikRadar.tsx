import { EmotionProfile } from '@/lib/types/emotion'
import { EMOTION_ORDER, EMOTION_COLORS } from '@/lib/utils/emotions'

interface RadarTrace {
  profile: EmotionProfile
  color: string
  label: string
}

interface PlutchikRadarProps {
  traces: RadarTrace[]
  size?: number
}

function polarToCartesian(
  cx: number,
  cy: number,
  r: number,
  index: number,
  total: number
): { x: number; y: number } {
  const angle = (index / total) * 2 * Math.PI - Math.PI / 2
  return {
    x: cx + r * Math.cos(angle),
    y: cy + r * Math.sin(angle),
  }
}

function buildPolygonPoints(
  cx: number,
  cy: number,
  r: number,
  scale: number,
  profile?: EmotionProfile
): string {
  return EMOTION_ORDER.map((emotion, i) => {
    const value = profile ? profile[emotion] * scale : scale
    const { x, y } = polarToCartesian(cx, cy, r * value, i, EMOTION_ORDER.length)
    return `${x},${y}`
  }).join(' ')
}

export default function PlutchikRadar({ traces, size = 280 }: PlutchikRadarProps) {
  const cx = size / 2
  const cy = size / 2
  const r = size * 0.36
  const GRID_SCALES = [0.25, 0.5, 0.75, 1.0]

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      {/* Grid polygons */}
      {GRID_SCALES.map((scale) => (
        <polygon
          key={scale}
          points={buildPolygonPoints(cx, cy, r, scale)}
          fill="none"
          stroke="#E5E3DC"
          strokeWidth={1}
        />
      ))}

      {/* Axis lines */}
      {EMOTION_ORDER.map((_, i) => {
        const { x, y } = polarToCartesian(cx, cy, r, i, EMOTION_ORDER.length)
        return (
          <line
            key={i}
            x1={cx}
            y1={cy}
            x2={x}
            y2={y}
            stroke="#E5E3DC"
            strokeWidth={1}
          />
        )
      })}

      {/* Traces */}
      {traces.map((trace, ti) => (
        <polygon
          key={ti}
          points={buildPolygonPoints(cx, cy, r, 1, trace.profile)}
          fill={trace.color}
          fillOpacity={0.18}
          stroke={trace.color}
          strokeWidth={2}
        />
      ))}

      {/* Axis labels */}
      {EMOTION_ORDER.map((emotion, i) => {
        const { x, y } = polarToCartesian(cx, cy, r * 1.28, i, EMOTION_ORDER.length)
        return (
          <text
            key={emotion}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="middle"
            fontSize={10}
            fontFamily="var(--font-inter), system-ui, sans-serif"
            fill={EMOTION_COLORS[emotion]}
            style={{ textTransform: 'capitalize' }}
          >
            {emotion}
          </text>
        )
      })}
    </svg>
  )
}
