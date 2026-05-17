import { Article } from '@/lib/types/article'

interface ArticleHeaderProps {
  article: Article
}

export default function ArticleHeader({ article }: ArticleHeaderProps) {
  return (
    <div>
      {/* Breadcrumb + category */}
      <p className="font-inter text-xs text-muted">Home / {article.category}</p>
      <span className="bg-analytical-blue text-white font-inter font-bold text-[10px] uppercase tracking-wider px-3 py-1 rounded-full inline-block mt-2">
        {article.category}
      </span>

      {/* Headline */}
      <h1 className="font-playfair font-extrabold text-[42px] leading-[1.1] text-charcoal mt-4">
        {article.headline}
      </h1>

      {/* Sources + timestamp row */}
      <div className="mt-3 flex items-center gap-2 flex-wrap">
        {article.sources.map((source) => (
          <span
            key={source}
            className="bg-off-white border border-ap-border rounded px-2 py-0.5 font-inter text-xs font-medium text-muted"
          >
            {source}
          </span>
        ))}
        <span className="text-muted text-xs">·</span>
        <span className="font-inter text-sm text-muted">{article.timestamp}</span>
      </div>

      {/* Stat chips row */}
      <div className="mt-4 flex gap-3 flex-wrap">
        <div className="flex items-center gap-1.5 bg-off-white rounded-full px-3 py-1.5">
          <span className="font-inter text-xs font-medium text-muted">Agent Takes</span>
          <span className="font-inter text-sm font-bold text-charcoal">{article.stats.agentTakes}</span>
        </div>
        <div className="flex items-center gap-1.5 bg-off-white rounded-full px-3 py-1.5">
          <span className="font-inter text-xs font-medium text-muted">Debates</span>
          <span className="font-inter text-sm font-bold text-charcoal">{article.stats.debates}</span>
        </div>
        <div className="flex items-center gap-1.5 bg-off-white rounded-full px-3 py-1.5">
          <span className="font-inter text-xs font-medium text-muted">Chains</span>
          <span className="font-inter text-sm font-bold text-charcoal">{article.stats.chains}</span>
        </div>
        <div className="flex items-center gap-1.5 bg-off-white rounded-full px-3 py-1.5">
          <span className="font-inter text-xs font-medium text-muted">Readers</span>
          <span className="font-inter text-sm font-bold text-charcoal">
            {article.stats.readers.toLocaleString()}
          </span>
        </div>
      </div>

      {/* Divider */}
      <div className="border-b border-ap-border mt-6" />
    </div>
  )
}
