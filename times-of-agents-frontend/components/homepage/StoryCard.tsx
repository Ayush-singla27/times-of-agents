import Link from 'next/link'
import { Article } from '@/lib/types/article'

interface StoryCardProps {
  article: Article
}

export default function StoryCard({ article }: StoryCardProps) {
  return (
    <Link href={`/article/${article.slug}`} className="block group">
      <div className="bg-card-white rounded-xl overflow-hidden shadow-[0_2px_8px_rgba(0,0,0,0.06)] hover:shadow-[0_8px_28px_rgba(0,0,0,0.12)] hover:-translate-y-0.5 transition-all duration-200 h-full flex flex-col">
        {/* Amber accent bar */}
        <div className="h-[3px] bg-insight-amber w-full flex-shrink-0" />

        <div className="p-4 flex flex-col flex-1">
          {/* Tags */}
          <div className="flex items-center gap-2 flex-wrap">
            <span className="bg-off-white text-muted font-inter font-semibold text-[10px] uppercase tracking-wider px-2.5 py-0.5 rounded-full">
              {article.category}
            </span>
            {article.isLatest && (
              <span className="bg-conflict-red text-white font-inter font-bold text-[9px] uppercase tracking-wider px-2 py-0.5 rounded-full">
                Latest
              </span>
            )}
          </div>

          {/* Headline */}
          <h3 className="font-playfair font-bold text-[15px] leading-snug text-charcoal mt-2 group-hover:text-analytical-blue transition-colors duration-150">
            {article.headline}
          </h3>

          {/* Summary snippet */}
          {article.summary.length > 0 && (
            <p className="font-inter text-[12px] text-muted leading-relaxed mt-1.5 line-clamp-2">
              {article.summary[0]}
            </p>
          )}

          {/* Footer */}
          <div className="mt-auto pt-3 border-t border-ap-border flex items-center justify-between">
            <span className="font-inter text-[11px] text-muted">{article.sources[0]}</span>
            <span className="font-inter text-[11px] font-semibold text-analytical-blue">
              Read →
            </span>
          </div>
        </div>
      </div>
    </Link>
  )
}
