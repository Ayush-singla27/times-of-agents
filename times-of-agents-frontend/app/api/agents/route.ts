import { NextResponse } from 'next/server'
import { getAgents } from '@/lib/services/agents'

export async function GET() {
  const agents = await getAgents()
  return NextResponse.json(agents)
}
