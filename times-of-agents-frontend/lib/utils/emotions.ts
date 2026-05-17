import { EmotionProfile } from '@/lib/types/emotion'

export const EMOTION_COLORS: Record<keyof EmotionProfile, string> = {
  joy: '#F59E0B',
  trust: '#10B981',
  fear: '#6366F1',
  surprise: '#EC4899',
  sadness: '#64748B',
  disgust: '#84CC16',
  anger: '#EF4444',
  anticipation: '#F97316',
}

export const EMOTION_ORDER: (keyof EmotionProfile)[] = [
  'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation',
]

export function getTopEmotions(
  profile: EmotionProfile,
  n: number = 8
): { emotion: keyof EmotionProfile; value: number; color: string }[] {
  return EMOTION_ORDER
    .map(emotion => ({ emotion, value: profile[emotion], color: EMOTION_COLORS[emotion] }))
    .sort((a, b) => b.value - a.value)
    .slice(0, n)
}
