import { NextResponse } from 'next/server'
import { getArticles } from '@/lib/services/articles'

export async function GET() {
  const articles = await getArticles()
  return NextResponse.json(articles)
}
