import React from 'react'

interface PullQuoteProps {
  children: React.ReactNode
  attribution?: string
  className?: string
}

export default function PullQuote({ children, attribution, className = '' }: PullQuoteProps) {
  return (
    <blockquote className={`border-l-4 border-insight-amber pl-4 ${className}`}>
      <p className="font-playfair italic text-charcoal leading-relaxed">{children}</p>
      {attribution && (
        <p className="font-inter text-sm text-muted mt-2 not-italic">{attribution}</p>
      )}
    </blockquote>
  )
}
