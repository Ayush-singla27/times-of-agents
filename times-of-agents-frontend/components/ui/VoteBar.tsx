'use client'

import { useState, useEffect } from 'react'

interface VoteBarProps {
  labelA: string
  labelB: string
  votesA: number
  votesB: number
  colorA: string
  colorB: string
}

export default function VoteBar({ labelA, labelB, votesA, votesB, colorA, colorB }: VoteBarProps) {
  const [widthA, setWidthA] = useState(0.5)
  const [widthB, setWidthB] = useState(0.5)

  useEffect(() => {
    const timer = setTimeout(() => {
      setWidthA(votesA)
      setWidthB(votesB)
    }, 300)
    return () => clearTimeout(timer)
  }, [votesA, votesB])

  const showLabelA = votesA >= 0.2
  const showLabelB = votesB >= 0.2

  return (
    <div className="w-full">
      <div className="relative h-10 rounded-full overflow-hidden flex">
        {/* Left segment */}
        <div
          className="flex items-center px-3 transition-all duration-700 ease-out"
          style={{ width: `${widthA * 100}%`, backgroundColor: colorA }}
        >
          <span
            className={`font-inter text-xs font-bold text-white truncate ${showLabelA ? '' : 'hidden'}`}
          >
            {labelA}
          </span>
        </div>
        {/* Right segment */}
        <div
          className="flex items-center justify-end px-3 transition-all duration-700 ease-out"
          style={{ width: `${widthB * 100}%`, backgroundColor: colorB }}
        >
          <span
            className={`font-inter text-xs font-bold text-white truncate ${showLabelB ? '' : 'hidden'}`}
          >
            {labelB}
          </span>
        </div>
      </div>

      <div className="flex justify-between mt-1">
        <span className="font-inter text-xs font-bold" style={{ color: colorA }}>
          {Math.round(votesA * 100)}%
        </span>
        <span className="font-inter text-xs font-bold text-right" style={{ color: colorB }}>
          {Math.round(votesB * 100)}%
        </span>
      </div>
    </div>
  )
}
