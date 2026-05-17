export interface ChainNode {
  step: string        // "Trigger" | "Step 2" | ... | "Outcome"
  icon: string        // emoji
  title: string
  description: string
}

export interface InsightChain {
  id: string
  label: string       // short label e.g. "Hormuz Cascade"
  title: string       // full thesis sentence
  agentId: string
  nodes: ChainNode[]
  articleId: string
  createdAt: string
}
