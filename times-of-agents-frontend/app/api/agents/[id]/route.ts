import { NextResponse } from 'next/server'
import { getAgent } from '@/lib/services/agents'

export async function GET(_req: Request, { params }: { params: { id: string } }) {
  const agent = await getAgent(params.id)
  if (!agent) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json(agent)
}
