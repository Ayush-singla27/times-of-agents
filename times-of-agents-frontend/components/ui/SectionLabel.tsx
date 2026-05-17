import React from 'react'

interface SectionLabelProps {
  children: React.ReactNode
  className?: string
}

export default function SectionLabel({ children, className = '' }: SectionLabelProps) {
  return (
    <p
      className={`font-inter font-bold text-[10px] uppercase tracking-[0.12em] text-muted ${className}`}
    >
      {children}
    </p>
  )
}
