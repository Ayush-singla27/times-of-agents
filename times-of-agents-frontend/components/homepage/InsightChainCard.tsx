import { InsightChain } from '@/lib/types/chain'
import InsightChainScroll from '@/components/ui/InsightChainScroll'

interface InsightChainCardProps {
  chain: InsightChain
}

export default function InsightChainCard({ chain }: InsightChainCardProps) {
  return (
    <div className="bg-card-white rounded-xl p-4 shadow-[0_2px_8px_rgba(0,0,0,0.06)]">
      {/* Header row */}
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 rounded-full bg-insight-amber flex-shrink-0" />
        <span className="font-inter font-bold text-sm text-charcoal">{chain.label}</span>
      </div>

      {/* Chain title */}
      <p className="font-inter text-xs text-muted mt-1 line-clamp-2">{chain.title}</p>

      {/* Chain scroll */}
      <div className="mt-3">
        <InsightChainScroll nodes={chain.nodes} />
      </div>
    </div>
  )
}
