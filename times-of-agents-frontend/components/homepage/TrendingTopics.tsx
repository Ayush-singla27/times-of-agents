import SectionLabel from '@/components/ui/SectionLabel'

const DEFAULT_TOPICS = [
  'Strait of Hormuz',
  'Fed Rate Decision',
  'AI Copper Gap',
  'Oil Markets',
  'Stagflation Risk',
  'Semiconductor Supply',
]

interface TrendingTopicsProps {
  topics?: string[]
}

export default function TrendingTopics({ topics = DEFAULT_TOPICS }: TrendingTopicsProps) {
  return (
    <div className="bg-card-white rounded-xl p-4 border border-ap-border shadow-[0_2px_8px_rgba(0,0,0,0.06)]">
      <SectionLabel>TRENDING TOPICS</SectionLabel>

      <div className="mt-3 flex flex-col gap-2">
        {topics.map((topic, index) => (
          <div
            key={topic}
            className="flex items-center justify-between py-2 border-b border-ap-border last:border-0"
          >
            <div className="flex items-center">
              <span className="font-inter font-black text-sm text-muted w-6">{index + 1}</span>
              <span className="font-inter text-sm text-charcoal font-medium ml-2">{topic}</span>
            </div>
            <span className="font-inter text-muted text-sm">→</span>
          </div>
        ))}
      </div>
    </div>
  )
}
