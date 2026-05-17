interface BreakingBannerProps {
  text?: string
}

export default function BreakingBanner({
  text = 'BREAKING: Iran closes Strait of Hormuz — oil hits $142 — Fed emergency session called — EU energy ministers convene',
}: BreakingBannerProps) {
  return (
    <div className="bg-charcoal border-b border-charcoal">
      <div className="max-w-[1280px] mx-auto px-6 py-2 flex items-center gap-3">
        <span className="bg-insight-amber text-charcoal font-inter font-black text-[10px] uppercase tracking-wider px-2 py-0.5 rounded flex-shrink-0">
          BREAKING
        </span>
        <span className="font-inter text-xs text-white/75 font-medium">
          {text}
        </span>
      </div>
    </div>
  )
}
