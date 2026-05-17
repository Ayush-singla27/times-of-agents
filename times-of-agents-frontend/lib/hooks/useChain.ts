import { chains } from '@/lib/data/chains'
import { InsightChain } from '@/lib/types/chain'

export function useChains(): { chains: InsightChain[]; isLoading: boolean; error: null } {
  return { chains, isLoading: false, error: null }
}

export function useChainsByArticle(articleId: string): { chains: InsightChain[]; isLoading: boolean; error: null } {
  const filtered = chains.filter(c => c.articleId === articleId)
  return { chains: filtered, isLoading: false, error: null }
}
