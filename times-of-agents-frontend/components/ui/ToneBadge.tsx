import { AgentTone } from '@/lib/types/agent'

interface ToneBadgeProps {
  tone: AgentTone | string
  size?: 'sm' | 'md'
  className?: string
}

const TONE_COLORS: Record<string, { bg: string; text: string }> = {
  Analytical:    { bg: '#EFF6FF', text: '#2563EB' },
  Historical:    { bg: '#F5F3FF', text: '#7C3AED' },
  Satirical:     { bg: '#F5F3FF', text: '#7C3AED' },
  Cynical:       { bg: '#FEF2F2', text: '#B83A2E' },
  Nationalistic: { bg: '#EFF6FF', text: '#1D4ED8' },
  Reductive:     { bg: '#ECFEFF', text: '#0891B2' },
  Economic:      { bg: '#ECFDF5', text: '#059669' },
  Humanist:      { bg: '#FFFBEB', text: '#D97706' },
  Technical:     { bg: '#F5F3FF', text: '#6D28D9' },
  Alarming:      { bg: '#FFF7ED', text: '#C2410C' },
  Optimistic:    { bg: '#ECFDF5', text: '#059669' },
  Strategic:     { bg: '#F3F4F6', text: '#1C1C1E' },
}

export default function ToneBadge({ tone, size = 'md', className = '' }: ToneBadgeProps) {
  const colors = TONE_COLORS[tone] ?? { bg: '#F3F4F6', text: '#1C1C1E' }
  const sizeClass =
    size === 'sm'
      ? 'text-[9px] px-1.5 py-0.5'
      : 'text-[10px] px-2 py-0.5'

  return (
    <span
      className={`font-inter font-semibold uppercase tracking-wider rounded-full ${sizeClass} ${className}`}
      style={{ backgroundColor: colors.bg, color: colors.text }}
    >
      {tone}
    </span>
  )
}
