import { InsightChain, ChainNode } from '@/lib/types/chain'

interface InsightChainVerticalProps {
  chain: InsightChain
}

function ChainNodeCard({ node, isLast }: { node: ChainNode; isLast: boolean }) {
  return (
    <div className={`relative flex gap-4 ${isLast ? 'pb-0' : 'pb-6'}`}>
      {/* Left spine */}
      <div className="flex flex-col items-center w-8 flex-shrink-0">
        <div
          className={`w-8 h-8 rounded-full border-2 bg-card-white flex items-center justify-center text-base flex-shrink-0 ${
            isLast ? 'border-conflict-red' : 'border-insight-amber'
          }`}
        >
          {node.icon}
        </div>
        {!isLast && (
          <div className="flex-1 w-0.5 bg-gradient-to-b from-insight-amber to-ap-border mt-1" />
        )}
      </div>

      {/* Card */}
      <div className="flex-1 min-w-0">
        <div
          className={`rounded-xl border p-4 ${
            isLast ? 'border-conflict-red bg-red-50' : 'bg-card-white border-ap-border'
          }`}
        >
          <span
            className={`text-[9px] font-bold uppercase rounded px-1.5 py-0.5 font-inter ${
              isLast ? 'bg-red-100 text-conflict-red' : 'bg-amber-100 text-insight-amber'
            }`}
          >
            {node.step}
          </span>
          <p className="font-playfair font-bold text-[15px] text-charcoal mt-1.5">
            {node.title}
          </p>
          <p className="font-inter text-sm text-muted leading-relaxed mt-2">
            {node.description}
          </p>
        </div>
      </div>
    </div>
  )
}

export default function InsightChainVertical({ chain }: InsightChainVerticalProps) {
  return (
    <div className="relative">
      <div className="mb-6">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-insight-amber" />
          <span className="font-inter font-bold text-sm text-charcoal">{chain.label}</span>
        </div>
        <p className="font-inter text-xs text-muted mt-1">{chain.title}</p>
      </div>

      {chain.nodes.map((node, i) => (
        <ChainNodeCard key={i} node={node} isLast={i === chain.nodes.length - 1} />
      ))}
    </div>
  )
}
