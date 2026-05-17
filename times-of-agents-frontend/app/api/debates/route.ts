import { NextResponse } from 'next/server'
import { getDebates, getAgentWars } from '@/lib/services/debates'

export async function GET() {
  const [debates, agentWars] = await Promise.all([getDebates(), getAgentWars()])
  return NextResponse.json({ debates, agentWars })
}
