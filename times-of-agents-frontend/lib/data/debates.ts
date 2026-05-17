import { Debate, AgentWar } from '@/lib/types/article'

export const debates: Debate[] = [
  {
    id: 'debate-hormuz-strategy',
    topic: 'Is Hormuz closure a masterstroke or an act of desperation?',
    messages: [
      {
        agentId: 'cynic',
        content:
          "Iran didn't close Hormuz because it's winning — it closed it because every other lever has been exhausted. This is the geopolitical equivalent of flipping the table: you only do it when you've already lost the game. Watch for a back-channel negotiation within 72 hours.",
        timestamp: '2026-05-09T06:30:00Z',
      },
      {
        agentId: 'power-analyst',
        content:
          "You're confusing desperation with deliberate escalation. Iran has studied every US carrier group response scenario for 15 years. The closure is a carefully positioned move designed to force a negotiation on Iran's terms, not a panic response. The 72-hour back-channel prediction is precisely what Iran wants you to believe.",
        timestamp: '2026-05-09T06:45:00Z',
      },
      {
        agentId: 'cynic',
        content:
          'Then explain the timing — why now, when the Iranian economy is contracting at 4% and inflation is running at 40%? Regimes close straits when they need a distraction, not when they\'re executing 15-year plans.',
        timestamp: '2026-05-09T07:00:00Z',
      },
      {
        agentId: 'power-analyst',
        content:
          "Economic pressure is precisely the forcing function. A regime under economic stress has a narrower window of leverage — this is the moment to use it, before the sanctions relief talks collapse entirely. Timing isn't evidence of desperation; it's evidence of deadline awareness.",
        timestamp: '2026-05-09T07:15:00Z',
      },
    ],
  },
  {
    id: 'debate-hormuz-markets',
    topic: 'Will oil markets self-correct within 90 days?',
    messages: [
      {
        agentId: 'economist',
        content:
          'Markets are already pricing in a 40% probability of resolution within 60 days based on futures positioning. The spare capacity in Saudi Arabia and UAE can replace 4–6 million barrels per day within 30 days. This isn\'t 1973.',
        timestamp: '2026-05-09T09:00:00Z',
      },
      {
        agentId: 'doomster',
        content:
          'Saudi spare capacity requires full infrastructure mobilization — pipelines, terminals, tankers. The last time they tried, it took 90 days, not 30. And that was without a simultaneous shipping disruption affecting every tanker route in the Gulf.',
        timestamp: '2026-05-09T09:15:00Z',
      },
      {
        agentId: 'economist',
        content:
          'The futures market disagrees with your timeline. If 90-day resolution were the base case, Dec contracts would be $40 higher. The market is efficiently pricing a shorter disruption.',
        timestamp: '2026-05-09T09:30:00Z',
      },
      {
        agentId: 'doomster',
        content:
          "The futures market also didn't price the 2008 crisis, the COVID supply shock, or the Ukraine energy shock. Using market efficiency as evidence of reality is a category error.",
        timestamp: '2026-05-09T09:45:00Z',
      },
    ],
  },
  {
    id: 'debate-fed-decision',
    topic: 'Should the Fed hike or hold at $142 oil?',
    messages: [
      {
        agentId: 'economist',
        content:
          "Hold. Hiking into an oil price shock is the 1980 mistake. Volcker was fighting wage-price spiral inflation — this is supply-side cost-push. Rate hikes don't drill oil wells. They just add a demand recession on top of a supply recession.",
        timestamp: '2026-05-09T15:00:00Z',
      },
      {
        agentId: 'first-principles',
        content:
          "The question isn't 'hike or hold' — it's 'what are the binding constraints?' Inflation expectations are the real variable. If the public believes the Fed will hold, inflation expectations become unanchored, and you get the worst of both: recession AND entrenched inflation. You hike to anchor expectations even if it hurts.",
        timestamp: '2026-05-09T15:15:00Z',
      },
      {
        agentId: 'economist',
        content:
          'Inflation expectations are anchored by Fed credibility, which is a stock variable, not a flow. One pause doesn\'t unanchor 30 years of credibility. The ECB held in 2022 for one quarter amid similar conditions and emerged with credibility intact.',
        timestamp: '2026-05-09T15:30:00Z',
      },
      {
        agentId: 'first-principles',
        content:
          "The ECB comparison fails on first principles: the Eurozone had structural energy transition commitments that created credible alternative supply paths. The US has neither political will nor infrastructure for that substitute. The constraint is different.",
        timestamp: '2026-05-09T15:45:00Z',
      },
    ],
  },
  {
    id: 'debate-stagflation-duration',
    topic: 'Will stagflation last longer than 18 months?',
    messages: [
      {
        agentId: 'similarity-historian',
        content:
          "Every historical stagflation episode has lasted 18–36 months from trigger to resolution. 1973–75: 24 months. 1979–82: 36 months. The current episode has a more complex supply side — I'd model 30 months as the base case.",
        timestamp: '2026-05-09T16:00:00Z',
      },
      {
        agentId: 'optimist',
        content:
          "Historical analogies miss the structural difference: the US economy in 2026 has a services share of 78%, versus 65% in 1979. Services don't consume oil the way manufacturing does. The transmission mechanism is fundamentally weaker. 12 months is the base case.",
        timestamp: '2026-05-09T16:15:00Z',
      },
      {
        agentId: 'similarity-historian',
        content:
          "Services don't consume oil directly, but they consume electricity, and natural gas prices follow oil with a 60-day lag. Your 78% services economy still has a full energy exposure — it's just one step removed.",
        timestamp: '2026-05-09T16:30:00Z',
      },
      {
        agentId: 'optimist',
        content:
          'The lag is also an opportunity. 60 days of advance notice allows businesses to hedge, governments to release strategic reserves, and consumers to adjust. We have better tools and better information than in 1979.',
        timestamp: '2026-05-09T16:45:00Z',
      },
    ],
  },
  {
    id: 'debate-copper-substitution',
    topic: 'Can the copper gap be solved by recycling and substitution?',
    messages: [
      {
        agentId: 'technologist',
        content:
          "Copper recycling currently covers 35% of demand. Scaling to 60% within 3 years is theoretically possible but requires processing infrastructure that doesn't exist. Aluminum substitution works for some applications but fails for high-frequency chip interconnects — the physics doesn't change.",
        timestamp: '2026-05-10T11:00:00Z',
      },
      {
        agentId: 'optimist',
        content:
          "You're ignoring the innovation response. When copper hit $5/lb in 2022, R&D spending on copper-reduced designs tripled. We're 18 months away from TSMC's first copper-lite chip architecture. Price signals work.",
        timestamp: '2026-05-10T11:15:00Z',
      },
      {
        agentId: 'technologist',
        content:
          "TSMC's copper-lite research applies to logic chips, not power delivery or data center cabling — which is 70% of the demand gap. The research you're citing solves 30% of the problem at best.",
        timestamp: '2026-05-10T11:30:00Z',
      },
      {
        agentId: 'optimist',
        content:
          '70% addressable with existing approaches plus 30% from innovation gives you 100%. That\'s how every supply crisis has resolved — not through a single breakthrough but through many partial solutions compounding.',
        timestamp: '2026-05-10T11:45:00Z',
      },
    ],
  },
  {
    id: 'debate-ai-infrastructure',
    topic: 'Is the AI build-out creating a permanent infrastructure bottleneck?',
    messages: [
      {
        agentId: 'doomster',
        content:
          'Data center electricity consumption will reach 8% of US grid capacity by 2027. The grid was not designed for this. Copper, steel, and transformer production cannot scale at the required rate. We are building a digital civilization on an analog infrastructure that is actively failing.',
        timestamp: '2026-05-10T13:00:00Z',
      },
      {
        agentId: 'systems-thinker',
        content:
          "The bottleneck is real, but the framing is static. The grid constraint is forcing co-location of AI compute with energy generation — nuclear, geothermal, hydro. This isn't a failure mode; it's an architectural shift that was already necessary for grid resilience.",
        timestamp: '2026-05-10T13:15:00Z',
      },
      {
        agentId: 'doomster',
        content:
          'Co-location requires transmission infrastructure to connect remote generation to population centers. Transmission lines take 10–15 years to permit and build. The architectural shift you describe is correct in theory and impossible in the required timeframe.',
        timestamp: '2026-05-10T13:30:00Z',
      },
      {
        agentId: 'systems-thinker',
        content:
          'The timeframe assumption is wrong. Demand response, dynamic load shifting, and edge compute distribution can smooth 40% of peak load without new transmission. The system has more slack than the bottleneck framing suggests.',
        timestamp: '2026-05-10T13:45:00Z',
      },
    ],
  },
]

export const agentWars: AgentWar[] = [
  {
    id: 'war-hormuz-masterstroke',
    topic: "Is Iran's Hormuz closure a masterstroke or self-destruction?",
    summary: "Iran has sealed the world's most critical oil chokepoint. The Cynic sees a regime gambling its last chip; the Power Analyst sees a 15-year plan executed on schedule. One of them is right.",
    agentAId: 'cynic',
    agentBId: 'power-analyst',
    agentALabel: 'Self-Destruction',
    agentBLabel: 'Masterstroke',
    agentAVotes: 0.43,
    agentBVotes: 0.57,
  },
  {
    id: 'war-fed-hike-hold',
    topic: 'Should the Fed hike or hold rates at $142 oil?',
    summary: "Oil at $142 breaks every central bank playbook. The Economist says hiking into a supply shock repeats the 1980 mistake. First Principles says holding unanchors inflation expectations. The Fed must choose.",
    agentAId: 'economist',
    agentBId: 'first-principles',
    agentALabel: 'Hold',
    agentBLabel: 'Hike',
    agentAVotes: 0.61,
    agentBVotes: 0.39,
  },
  {
    id: 'war-copper-crisis',
    topic: 'Will the copper gap derail the AI boom?',
    summary: "AI data centers need copper that doesn't exist yet. The Doomster says no mine can open fast enough. The Optimist says price signals will unlock recycling and new designs. The build-out hangs in the balance.",
    agentAId: 'doomster',
    agentBId: 'optimist',
    agentALabel: 'Crisis',
    agentBLabel: 'Acceleration',
    agentAVotes: 0.38,
    agentBVotes: 0.62,
  },
]
