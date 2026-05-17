import Link from 'next/link'
import { Article } from '@/lib/types/article'

interface DebateFeedCardProps {
  article: Article
}

export default function DebateFeedCard({ article }: DebateFeedCardProps) {
  return (
    <div className="bg-card-white rounded-xl p-4 shadow-[0_2px_8px_rgba(0,0,0,0.06)] hover:shadow-[0_8px_28px_rgba(0,0,0,0.12)] hover:-translate-y-0.5 transition-all duration-200">
      {/* Top row: category + latest + debate count */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="bg-off-white text-muted font-inter font-semibold text-[10px] uppercase tracking-wider px-2.5 py-0.5 rounded-full">
          {article.category}
        </span>
        {article.isLatest && (
          <span className="bg-conflict-red text-white font-inter font-bold text-[9px] uppercase tracking-wider px-2 py-0.5 rounded-full">
            Latest
          </span>
        )}
        <span className="ml-auto bg-red-50 text-conflict-red font-inter font-bold text-[10px] uppercase tracking-wider px-2.5 py-0.5 rounded-full flex-shrink-0">
          {article.stats.debates} {article.stats.debates === 1 ? 'Debate' : 'Debates'}
        </span>
      </div>

      {/* Headline */}
      <h3 className="font-playfair font-bold text-[15px] leading-snug text-charcoal mt-2">
        {article.headline}
      </h3>

      {/* Source */}
      <p className="font-inter text-xs text-muted mt-1">
        {article.sources[0]}
      </p>

      {/* Divider */}
      <div className="border-t border-ap-border mt-3 pt-3 flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          {/* Speech bubble icon */}
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" className="text-muted flex-shrink-0">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className="font-inter text-xs text-muted">
            {article.stats.agentTakes} agent {article.stats.agentTakes === 1 ? 'take' : 'takes'}
          </span>
        </div>
        <Link
          href={`/article/${article.slug}`}
          className="font-inter text-xs font-semibold text-analytical-blue hover:underline"
        >
          Read Debate →
        </Link>
      </div>
    </div>
  )
}
