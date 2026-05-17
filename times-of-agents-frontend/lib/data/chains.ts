import { InsightChain } from '@/lib/types/chain'

export const chains: InsightChain[] = [
  {
    id: 'hormuz-cascade',
    label: 'Hormuz Cascade',
    title: 'How closing a 33-mile strait triggers a global semiconductor shortage',
    agentId: 'systems-thinker',
    articleId: 'hormuz-closure',
    createdAt: '2026-05-09T07:00:00Z',
    nodes: [
      {
        step: 'Trigger',
        icon: '🚢',
        title: 'Hormuz Closure',
        description:
          'Iran seals the world\'s most critical oil chokepoint. 21 million barrels per day — 20% of global supply — suddenly cannot move.',
      },
      {
        step: 'Step 2',
        icon: '🛢️',
        title: 'Oil Refining Halts',
        description:
          'Gulf refineries dependent on Iranian crude go offline. Sulfur, a mandatory refinery byproduct, stops being produced as a side effect.',
      },
      {
        step: 'Step 3',
        icon: '⚗️',
        title: 'Sulfur Scarcity',
        description:
          'Sulfuric acid production — derived from refinery sulfur — drops 35%. This acid is irreplaceable in phosphate fertilizer manufacturing.',
      },
      {
        step: 'Step 4',
        icon: '🌾',
        title: 'Fertilizer Shortage',
        description:
          'Phosphate fertilizer prices spike 60%. Farmers in India, Brazil, and Sub-Saharan Africa cut planted acreage by 15–20%.',
      },
      {
        step: 'Step 5',
        icon: '⚙️',
        title: 'Copper Supply Disruption',
        description:
          'The same shipping lanes that carry oil also carry copper ore from Chilean ports. Freight costs make copper extraction uneconomic for marginal mines.',
      },
      {
        step: 'Step 6',
        icon: '💻',
        title: 'Semiconductor Fab Delays',
        description:
          'Copper is the primary conductor in chip manufacturing. TSMC and Samsung face a 6-month supply gap, halting next-gen GPU production.',
      },
      {
        step: 'Outcome',
        icon: '⚡',
        title: 'Three Simultaneous Supply Shocks',
        description:
          'Oil, food, and semiconductor crises converge simultaneously — a synchronized shock that no central bank policy can address in isolation.',
      },
    ],
  },
  {
    id: 'rate-spiral',
    label: 'Rate Spiral',
    title: 'How $142 oil breaks every central bank model and triggers a stagflation trap',
    agentId: 'economist',
    articleId: 'fed-oil-142',
    createdAt: '2026-05-09T14:00:00Z',
    nodes: [
      {
        step: 'Trigger',
        icon: '💰',
        title: 'Oil Hits $142',
        description:
          'Brent crude crosses $142 per barrel — the highest since 2008. Energy feeds into every CPI component with a 6–8 week lag.',
      },
      {
        step: 'Step 2',
        icon: '📈',
        title: 'CPI Surge',
        description:
          'Headline inflation jumps 1.8 percentage points within 60 days. Transportation, food, and manufacturing costs all reprice simultaneously.',
      },
      {
        step: 'Step 3',
        icon: '🏦',
        title: 'Fed Emergency Session',
        description:
          'The Fed faces an impossible choice: hike into a demand shock or hold and let inflation become entrenched. Political pressure favors a pause.',
      },
      {
        step: 'Step 4',
        icon: '💵',
        title: 'Dollar Uncertainty',
        description:
          'Markets price in a rate pause, weakening the dollar. Commodity prices denominated in dollars surge further, compounding the inflation spiral.',
      },
      {
        step: 'Step 5',
        icon: '🌍',
        title: 'EM Debt Stress',
        description:
          'Dollar-denominated emerging market debt becomes harder to service. Three sovereign credit rating downgrades occur within 30 days.',
      },
      {
        step: 'Outcome',
        icon: '📉',
        title: 'Stagflation Trap',
        description:
          'Growth slows as energy costs crush margins; inflation rises as supply chains reprice. The Fed has no tool that addresses both simultaneously.',
      },
    ],
  },
  {
    id: 'semiconductor-crunch',
    label: 'Semiconductor Crunch',
    title: 'How the AI compute boom collides with an 18-month copper supply gap',
    agentId: 'technologist',
    articleId: 'ai-copper-gap',
    createdAt: '2026-05-10T09:00:00Z',
    nodes: [
      {
        step: 'Trigger',
        icon: '🤖',
        title: 'AI Build-Out Demand',
        description:
          'The top 6 hyperscalers collectively order 340% of their normal annual copper volume to wire new AI data centers across three continents.',
      },
      {
        step: 'Step 2',
        icon: '⛏️',
        title: 'Mine Capacity Maxed',
        description:
          'The world\'s top 10 copper mines are already running at 97% capacity. There is no spare capacity to absorb the demand surge.',
      },
      {
        step: 'Step 3',
        icon: '🚢',
        title: 'Shipping Disruption',
        description:
          'Hormuz closure adds 15 days and 40% cost to Chilean copper shipments. Marginal mines become uneconomic overnight.',
      },
      {
        step: 'Step 4',
        icon: '🏗️',
        title: 'Data Center Construction Halts',
        description:
          '47 planned hyperscale facilities pause construction. Copper delivery timelines extend from 8 weeks to 18+ months.',
      },
      {
        step: 'Step 5',
        icon: '💻',
        title: 'GPU Production Bottleneck',
        description:
          'TSMC and NVIDIA both cite copper interconnect availability as the binding constraint on H200 and next-gen chip production.',
      },
      {
        step: 'Outcome',
        icon: '📊',
        title: '18-Month AI Deployment Delay',
        description:
          'Major AI model deployments planned for 2026 slip to 2027–2028. Clean energy (EVs, solar) competes for the same constrained copper supply.',
      },
    ],
  },
  {
    id: 'food-security',
    label: 'Food Security',
    title: 'How an oil closure triggers a food emergency affecting 260 million people',
    agentId: 'systems-thinker',
    articleId: 'hormuz-closure',
    createdAt: '2026-05-09T08:30:00Z',
    nodes: [
      {
        step: 'Trigger',
        icon: '🛢️',
        title: 'Oil Price Shock',
        description:
          'Energy is the input cost multiplier for all agriculture — from tractor fuel to refrigerated transport. A 60% oil spike translates to a 25–40% farm cost increase.',
      },
      {
        step: 'Step 2',
        icon: '🚜',
        title: 'Fertilizer Cost +60%',
        description:
          'Natural gas (used in ammonia synthesis) and sulfuric acid (phosphate production) both spike simultaneously. Fertilizer becomes unaffordable for smallholder farmers.',
      },
      {
        step: 'Step 3',
        icon: '🌾',
        title: 'Crop Yield Reduction',
        description:
          'Farmers in the top 15 food-producing nations reduce planted acreage 12–18%. Early harvest forecasts revised down 8% globally.',
      },
      {
        step: 'Step 4',
        icon: '🚢',
        title: 'Export Restrictions',
        description:
          'India halts rice exports. China restricts corn and soybean flows. Both cite domestic food security. The global grain market loses 340 million tonnes of supply.',
      },
      {
        step: 'Step 5',
        icon: '🆘',
        title: 'WFP Funding Gap',
        description:
          'The World Food Programme faces a $4.2B funding shortfall as donor nations redirect budgets to energy security. 67 active operations face suspension.',
      },
      {
        step: 'Outcome',
        icon: '🌍',
        title: '260M People at Acute Risk',
        description:
          'UN projects 260 million people reach acute food insecurity within 6 months — the largest food emergency since World War II.',
      },
    ],
  },
  {
    id: 'dollar-surge',
    label: 'Dollar Surge',
    title: 'How a Fed rate pause triggers a dollar collapse and EM debt spiral',
    agentId: 'economist',
    articleId: 'fed-oil-142',
    createdAt: '2026-05-09T16:00:00Z',
    nodes: [
      {
        step: 'Trigger',
        icon: '🏦',
        title: 'Fed Pause Signal',
        description:
          'Fed chair signals a rate pause amid oil-driven economic shock, ending the tightening cycle prematurely. Real rates go negative.',
      },
      {
        step: 'Step 2',
        icon: '💵',
        title: 'Dollar Weakens 8%',
        description:
          'The trade-weighted dollar index drops 8% in 6 trading days — the fastest decline since 2020. Foreign holders reduce Treasury positions.',
      },
      {
        step: 'Step 3',
        icon: '📈',
        title: 'Commodity Super-Spike',
        description:
          'Dollar-denominated commodities surge as the dollar falls. Oil, copper, wheat, and lithium all hit multi-year highs simultaneously.',
      },
      {
        step: 'Step 4',
        icon: '🏦',
        title: 'Bank Stress Emerges',
        description:
          'Energy sector loan books deteriorate. Three regional banks with high energy exposure face margin calls. Fed issues emergency liquidity notice.',
      },
      {
        step: 'Outcome',
        icon: '💥',
        title: 'Credit Crunch in Energy Sector',
        description:
          'Lending to energy projects freezes as banks reassess exposure. Planned refinery expansions cancel. The supply shock becomes self-reinforcing.',
      },
    ],
  },
  {
    id: 'copper-crisis',
    label: 'Copper Crisis',
    title: 'Why AI\'s appetite for copper is incompatible with current mining capacity',
    agentId: 'doomster',
    articleId: 'ai-copper-gap',
    createdAt: '2026-05-10T10:00:00Z',
    nodes: [
      {
        step: 'Trigger',
        icon: '⚡',
        title: 'AI Demand Explosion',
        description:
          'A single large-scale AI data center requires 30,000 tons of copper — equivalent to a mid-sized mine\'s annual output. 200+ centers are planned for 2026.',
      },
      {
        step: 'Step 2',
        icon: '⛏️',
        title: 'Supply Cannot Scale',
        description:
          'Opening a new copper mine takes 16–20 years from discovery to production. The pipeline of mines that can open by 2027 is fixed and insufficient.',
      },
      {
        step: 'Step 3',
        icon: '🔋',
        title: 'Three-Way Demand Collision',
        description:
          'AI data centers, EV manufacturing, and solar grid infrastructure all hit peak copper demand simultaneously — the first time in history.',
      },
      {
        step: 'Step 4',
        icon: '🏗️',
        title: 'Construction Delays Cascade',
        description:
          'Data center build costs rise 35% as copper prices spike. Hyperscalers delay, cancel, or relocate 40% of planned capacity.',
      },
      {
        step: 'Step 5',
        icon: '🌍',
        title: 'Clean Energy Delayed',
        description:
          'EV and solar projects lose copper allocations to higher-margin AI buyers. Clean energy transition timelines extend by 3–5 years.',
      },
      {
        step: 'Outcome',
        icon: '📉',
        title: 'Structural Supply Deficit for a Decade',
        description:
          'Copper enters a structural deficit that cannot be resolved before 2034 regardless of price. The green and digital transitions compete for a resource neither can share.',
      },
    ],
  },
]
