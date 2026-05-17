import { ChainNode } from '@/lib/types/chain'

interface InsightChainNodeProps {
  node: ChainNode
  isOutcome?: boolean
}

export default function InsightChainNode({ node, isOutcome = false }: InsightChainNodeProps) {
  const containerBase =
    'min-w-[200px] max-w-[240px] rounded-xl border border-ap-border bg-card-white p-3'
  const containerOutcome = 'border-conflict-red bg-red-50'
  const containerDefault = 'hover:border-insight-amber hover:bg-amber-50 transition-colors duration-150'

  return (
    <div className={`${containerBase} ${isOutcome ? containerOutcome : containerDefault}`}>
      <div className="flex items-center justify-between gap-1">
        <span className="bg-amber-100 text-insight-amber text-[9px] font-bold uppercase rounded px-1.5 py-0.5 font-inter">
          {node.step}
        </span>
        <span className="text-base">{node.icon}</span>
      </div>
      <p className="font-playfair font-bold text-[13px] text-charcoal mt-1.5 leading-snug">
        {node.title}
      </p>
      <p className="font-inter text-[11px] text-muted leading-relaxed mt-1">
        {node.description}
      </p>
    </div>
  )
}
