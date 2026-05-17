import { NextResponse } from 'next/server'
import { NextRequest } from 'next/server'
import { getChains, getChainsByArticle } from '@/lib/services/chains'

export async function GET(request: NextRequest) {
  const articleId = request.nextUrl.searchParams.get('articleId')
  const chains = articleId ? await getChainsByArticle(articleId) : await getChains()
  return NextResponse.json(chains)
}
