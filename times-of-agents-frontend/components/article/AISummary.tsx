import { Article } from '@/lib/types/article'

interface AISummaryProps {
  article: Article
}

export default function AISummary({ article }: AISummaryProps) {
  return (
    <div className="bg-off-white rounded-xl p-5 border border-ap-border">
      <div className="flex items-center gap-3">
        <span className="text-base">🤖</span>
        <span className="font-inter font-bold text-sm text-charcoal">AI Summary</span>
        <span className="font-inter text-xs text-muted ml-auto">Pipeline · Search Summary</span>
      </div>
      <div className="mt-4 flex flex-col gap-2">
        {article.summary.map((point, i) => (
          <div key={i} className="flex items-start gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-analytical-blue flex-shrink-0 mt-1.5" />
            <p className="font-inter text-sm text-charcoal leading-relaxed">{point}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
