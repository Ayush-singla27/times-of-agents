import { getArticles } from '@/lib/services/articles'
import StoryCard from '@/components/homepage/StoryCard'

export default async function TrendingPage() {
  const articles = await getArticles()

  return (
    <div>
      {/* Page header */}
      <div className="mb-6">
        <h1 className="font-playfair font-extrabold text-[32px] text-charcoal leading-tight">
          Trending Stories
        </h1>
        <p className="font-inter text-sm text-muted mt-1">
          {articles.length} {articles.length === 1 ? 'story' : 'stories'} analysed by our agents today
        </p>
      </div>

      {articles.length === 0 ? (
        <div className="flex items-center justify-center py-24">
          <p className="font-inter text-muted text-base">No stories available yet. Check back soon.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {articles.map(a => (
            <StoryCard key={a.id} article={a} />
          ))}
        </div>
      )}
    </div>
  )
}
