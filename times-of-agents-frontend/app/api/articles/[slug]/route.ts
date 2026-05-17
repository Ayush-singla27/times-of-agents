import { NextResponse } from 'next/server'
import { getArticle } from '@/lib/services/articles'

export async function GET(_req: Request, { params }: { params: { slug: string } }) {
  const article = await getArticle(params.slug)
  if (!article) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json(article)
}
