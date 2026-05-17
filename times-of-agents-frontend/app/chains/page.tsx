import { getChains } from '@/lib/services/chains'
import { getArticles } from '@/lib/services/articles'
import InsightChainCard from '@/components/homepage/InsightChainCard'
import Link from 'next/link'

export default async function ChainsPage() {
  const [chains, articles] = await Promise.all([getChains(), getArticles()])

  // Map articleId → headline for display
  const articleMap = new Map(articles.map(a => [a.id, a]))

  return (
    <div>
      {/* Page header */}
      <div className="mb-6">
        <h1 className="font-playfair font-extrabold text-[32px] text-charcoal leading-tight">
          Insight Chains
        </h1>
        <p className="font-inter text-sm text-muted mt-1">
          {chains.length} causal {chains.length === 1 ? 'chain' : 'chains'} built by our analysis agents
        </p>
      </div>

      {chains.length === 0 ? (
        <div className="flex items-center justify-center py-24">
          <p className="font-inter text-muted text-base">No insight chains yet. Check back after the next pipeline run.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-5">
          {chains.map(chain => {
            const article = chain.articleId ? articleMap.get(chain.articleId) : null
            return (
              <div key={chain.id}>
                {article && (
                  <div className="flex items-center gap-2 mb-2">
                    <span className="bg-off-white text-muted font-inter font-semibold text-[10px] uppercase tracking-wider px-2.5 py-0.5 rounded-full">
                      {article.category}
                    </span>
                    <Link
                      href={`/article/${article.slug}`}
                      className="font-inter font-semibold text-xs text-charcoal hover:text-analytical-blue transition-colors line-clamp-1"
                    >
                      {article.headline}
                    </Link>
                  </div>
                )}
                <InsightChainCard chain={chain} />
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
