import { articles } from '@/lib/data/articles'
import { Article } from '@/lib/types/article'

export function useArticles(): { articles: Article[]; isLoading: boolean; error: null } {
  return { articles, isLoading: false, error: null }
}

export function useArticle(slug: string): { article: Article | null; isLoading: boolean; error: null } {
  const article = articles.find(a => a.slug === slug) ?? null
  return { article, isLoading: false, error: null }
}
