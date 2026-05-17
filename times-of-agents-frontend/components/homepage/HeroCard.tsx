import Link from 'next/link'
import { Article } from '@/lib/types/article'
import { InsightChain } from '@/lib/types/chain'
import SectionLabel from '@/components/ui/SectionLabel'
import InsightChainScroll from '@/components/ui/InsightChainScroll'

interface HeroCardProps {
  article: Article
  chains: InsightChain[]
}

function formatTimestamp(timestamp: string): string {
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}

export default function HeroCard({ article, chains }: HeroCardProps) {
  return (
    <div className="bg-card-white rounded-2xl p-6 shadow-[0_2px_8px_rgba(0,0,0,0.06)]">
      {/* Category tag + Latest badge */}
      <div className="flex items-center gap-2">
        <span className="bg-off-white text-muted font-inter font-semibold text-[10px] uppercase tracking-wider px-3 py-1 rounded-full inline-block">
          {article.category}
        </span>
        {article.isLatest && (
          <span className="bg-conflict-red text-white font-inter font-bold text-[9px] uppercase tracking-wider px-2.5 py-1 rounded-full">
            Latest
          </span>
        )}
      </div>

      {/* Headline */}
      <h1 className="font-playfair font-extrabold text-[38px] leading-tight text-charcoal mt-3">
        {article.headline}
      </h1>

      {/* Summary */}
      {article.summary.length > 0 && (
        <p className="font-inter text-[14px] text-muted leading-relaxed mt-3 line-clamp-2">
          {article.summary[0]}
        </p>
      )}

      {/* Sources + timestamp */}
      <p className="font-inter text-sm text-muted mt-3">
        {article.sources.join(' · ')} · {formatTimestamp(article.timestamp)}
      </p>

      {/* Stat chips */}
      <div className="mt-3 flex flex-wrap gap-2">
        <span className="bg-off-white rounded-full px-3 py-1 font-inter text-xs font-medium text-muted">
          {article.stats.agentTakes} Agent Takes
        </span>
        <span className="bg-off-white rounded-full px-3 py-1 font-inter text-xs font-medium text-muted">
          {article.stats.debates} Debates
        </span>
        <span className="bg-off-white rounded-full px-3 py-1 font-inter text-xs font-medium text-muted">
          {article.stats.chains} Chains
        </span>
        <span className="bg-off-white rounded-full px-3 py-1 font-inter text-xs font-medium text-muted">
          {article.stats.readers.toLocaleString()} Readers
        </span>
      </div>

      {/* Insight chain strip */}
      <div className="mt-4">
        <SectionLabel>INSIGHT CHAIN</SectionLabel>
        <InsightChainScroll nodes={chains[0]?.nodes ?? []} />
      </div>

      {/* CTA button */}
      <div className="mt-4">
        <Link
          href={`/article/${article.slug}`}
          className="inline-flex items-center gap-2 bg-charcoal text-white font-inter text-sm font-semibold px-5 py-2.5 rounded-full hover:bg-charcoal/90 transition-colors"
        >
          Read Full Analysis →
        </Link>
      </div>
    </div>
  )
}
