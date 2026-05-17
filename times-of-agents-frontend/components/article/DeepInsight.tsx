import { Article } from '@/lib/types/article'
import SectionLabel from '@/components/ui/SectionLabel'

interface DeepInsightProps {
  article: Article
}

export default function DeepInsight({ article }: DeepInsightProps) {
  return (
    <div className="bg-amber-50 border-l-4 border-insight-amber rounded-r-xl p-5">
      <div className="flex items-center gap-2 mb-3">
        <SectionLabel>DEEP INSIGHT</SectionLabel>
        <span className="text-base">🔬</span>
        <span className="font-inter text-xs font-bold text-charcoal">Insight Analyst</span>
      </div>
      <p className="font-playfair italic text-[17px] text-charcoal leading-relaxed">
        {article.deepInsight}
      </p>
    </div>
  )
}
