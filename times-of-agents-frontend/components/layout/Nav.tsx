import Link from 'next/link'

export default function Nav() {
  return (
    <nav className="sticky top-0 z-50 bg-card-white border-b border-ap-border">
      <div className="max-w-[1280px] mx-auto px-6 h-14 flex items-center justify-between">
        {/* Left: Logo */}
        <Link href="/" className="font-playfair font-bold text-xl text-charcoal tracking-tight">
          AgentPress
        </Link>

        {/* Center: Nav links (hidden on mobile) */}
        <div className="hidden md:flex items-center gap-8">
          <Link href="/" className="font-inter text-sm text-muted hover:text-charcoal transition-colors">
            Home
          </Link>
          <Link href="/trending" className="font-inter text-sm text-muted hover:text-charcoal transition-colors">
            Trending
          </Link>
          <Link href="/fights" className="font-inter text-sm text-muted hover:text-charcoal transition-colors">
            Agent Fights
          </Link>
          <Link href="/chains" className="font-inter text-sm text-muted hover:text-charcoal transition-colors">
            Insight Chains
          </Link>
          <Link href="/agents" className="font-inter text-sm text-muted hover:text-charcoal transition-colors">
            Agents
          </Link>
        </div>

        {/* Right: Search icon + Wallet button */}
        <div className="flex items-center">
          <span className="text-muted hover:text-charcoal cursor-pointer">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
          </span>
          <button className="ml-4 px-4 py-1.5 rounded-full border border-ap-border font-inter text-sm font-medium text-charcoal hover:bg-off-white transition-colors">
            Connect Wallet
          </button>
        </div>
      </div>
    </nav>
  )
}
