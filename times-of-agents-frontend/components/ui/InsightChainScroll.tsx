import { ChainNode } from '@/lib/types/chain'
import InsightChainNode from './InsightChainNode'

interface InsightChainScrollProps {
  nodes: ChainNode[]
  className?: string
}

export default function InsightChainScroll({ nodes, className = '' }: InsightChainScrollProps) {
  return (
    <div
      className={`overflow-x-auto [&::-webkit-scrollbar]:hidden ${className}`}
      style={{ scrollbarWidth: 'none' }}
    >
      <div className="flex items-center w-max pb-2">
        {nodes.map((node, i) => (
          <div key={i} className="flex items-center flex-shrink-0">
            <InsightChainNode node={node} isOutcome={i === nodes.length - 1} />
            {i < nodes.length - 1 && (
              <div className="flex items-center justify-center w-8 flex-shrink-0">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" className="text-insight-amber">
                  <path d="M5 12h14M13 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
