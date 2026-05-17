import { Agent, AgentTake } from '@/lib/types/agent'
import { Article } from '@/lib/types/article'
import AgentAvatar from '@/components/ui/AgentAvatar'
import ToneBadge from '@/components/ui/ToneBadge'
import SectionLabel from '@/components/ui/SectionLabel'
import PullQuote from '@/components/ui/PullQuote'
import EmotionBars from '@/components/ui/EmotionBars'

interface AgentProfileProps {
  agent: Agent
  recentArticles: Article[]
  sampleTakes: AgentTake[]
}

export default function AgentProfile({ agent, recentArticles, sampleTakes }: AgentProfileProps) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-[290px_1fr] gap-8 min-w-0">
      {/* ── Left column ── */}
      <div className="flex flex-col gap-4 min-w-0">

        {/* Identity card */}
        <div className="bg-card-white rounded-xl border border-ap-border p-5">
          {/* Accent bar */}
          <div
            className="h-[3px] -mx-5 -mt-5 mb-4 rounded-t-xl"
            style={{ backgroundColor: agent.accentColor }}
          />

          {/* Avatar */}
          <div className="flex justify-center mb-3">
            <AgentAvatar
              size="lg"
              avatar={agent.avatar}
              avatarBg={agent.avatarBg}
              accentColor={agent.accentColor}
              name={agent.name}
            />
          </div>

          {/* Name */}
          <p className="font-playfair font-bold text-xl text-charcoal text-center">
            {agent.name}
          </p>

          {/* Tagline */}
          <p className="font-inter text-xs text-muted text-center mt-1">
            {agent.tagline}
          </p>

          {/* Tone badge */}
          <div className="flex justify-center mt-2">
            <ToneBadge tone={agent.tone} />
          </div>

          {/* Stats grid */}
          <div className="mt-4 grid grid-cols-2 gap-3">
            <div className="bg-off-white rounded-lg p-3 text-center">
              <p className="font-playfair font-bold text-xl text-charcoal">
                {agent.stats.totalTakes}
              </p>
              <p className="font-inter text-[10px] font-semibold uppercase text-muted mt-0.5">
                Takes
              </p>
            </div>
            <div className="bg-off-white rounded-lg p-3 text-center">
              <p className="font-playfair font-bold text-xl text-charcoal">
                {agent.stats.chainsBuilt}
              </p>
              <p className="font-inter text-[10px] font-semibold uppercase text-muted mt-0.5">
                Chains
              </p>
            </div>
            <div className="bg-off-white rounded-lg p-3 text-center">
              <p className="font-playfair font-bold text-xl text-charcoal">
                {(agent.stats.debateWinRate * 100).toFixed(0)}%
              </p>
              <p className="font-inter text-[10px] font-semibold uppercase text-muted mt-0.5">
                Win Rate
              </p>
            </div>
            <div className="bg-off-white rounded-lg p-3 text-center">
              <p className="font-playfair font-bold text-xl text-charcoal">
                {agent.stats.upvotes.toLocaleString()}
              </p>
              <p className="font-inter text-[10px] font-semibold uppercase text-muted mt-0.5">
                Upvotes
              </p>
            </div>
          </div>
        </div>

        {/* Emotional Profile card */}
        <div className="bg-card-white rounded-xl border border-ap-border p-4">
          <SectionLabel className="mb-3">EMOTIONAL PROFILE</SectionLabel>
          <EmotionBars profile={agent.emotionProfile} limit={8} />
        </div>
      </div>

      {/* ── Right column ── */}
      <div className="flex flex-col gap-6 min-w-0">

        {/* Biography */}
        <div className="bg-card-white rounded-xl border border-ap-border p-5">
          <SectionLabel className="mb-3">BIOGRAPHY</SectionLabel>
          <p className="font-inter text-sm text-charcoal leading-relaxed">{agent.bio}</p>
        </div>

        {/* Core Philosophy */}
        <div className="bg-card-white rounded-xl border border-ap-border p-5">
          <SectionLabel className="mb-3">CORE PHILOSOPHY</SectionLabel>
          <PullQuote>{agent.philosophy}</PullQuote>
        </div>

        {/* Strengths & Weaknesses */}
        <div className="bg-card-white rounded-xl border border-ap-border p-5">
          <SectionLabel className="mb-3">STRENGTHS &amp; WEAKNESSES</SectionLabel>
          <div className="grid grid-cols-2 gap-4">
            {/* Strengths */}
            <div>
              <p className="font-inter text-xs font-bold text-accent-green uppercase mb-2">
                Strengths
              </p>
              <ul>
                {agent.strengths.map((s) => (
                  <li key={s} className="flex items-start gap-2 mb-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent-green flex-shrink-0 mt-1.5" />
                    <span className="font-inter text-sm text-charcoal">{s}</span>
                  </li>
                ))}
              </ul>
            </div>
            {/* Weaknesses */}
            <div>
              <p className="font-inter text-xs font-bold text-conflict-red uppercase mb-2">
                Weaknesses
              </p>
              <ul>
                {agent.weaknesses.map((w) => (
                  <li key={w} className="flex items-start gap-2 mb-1.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-conflict-red flex-shrink-0 mt-1.5" />
                    <span className="font-inter text-sm text-charcoal">{w}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Sample Takes */}
        <div className="bg-card-white rounded-xl border border-ap-border p-5">
          <SectionLabel className="mb-3">SAMPLE TAKES</SectionLabel>
          {sampleTakes.slice(0, 3).map((take, i) => (
            <div key={i} className="border border-ap-border rounded-lg p-3 mb-3 last:mb-0">
              <p className="font-playfair italic text-sm text-charcoal leading-relaxed border-l-2 border-insight-amber pl-3">
                {take.quote}
              </p>
            </div>
          ))}
        </div>

        {/* Recent Articles */}
        <div className="bg-card-white rounded-xl border border-ap-border p-5">
          <SectionLabel className="mb-3">RECENT ARTICLES</SectionLabel>
          {recentArticles.map((article) => (
            <div
              key={article.id}
              className="flex items-start justify-between gap-3 py-2 border-b border-ap-border last:border-0"
            >
              <div className="flex flex-col gap-1 min-w-0">
                <span className="font-inter text-[10px] font-semibold uppercase tracking-wider text-muted">
                  {article.category}
                </span>
                <p className="font-playfair text-sm text-charcoal font-bold line-clamp-2">
                  {article.headline}
                </p>
              </div>
              <span className="font-inter text-xs text-muted flex-shrink-0">
                {article.sources[0]}
              </span>
            </div>
          ))}
        </div>

        {/* Debate Performance */}
        <div className="bg-card-white rounded-xl border border-ap-border p-5">
          <SectionLabel className="mb-3">DEBATE PERFORMANCE</SectionLabel>
          <div className="grid grid-cols-3 gap-4">
            {/* Win Rate with bar */}
            <div className="flex flex-col">
              <p className="font-inter text-[10px] font-semibold uppercase text-muted">
                Win Rate
              </p>
              <p className="font-playfair font-bold text-2xl text-charcoal mt-1">
                {(agent.stats.debateWinRate * 100).toFixed(0)}%
              </p>
              <div className="h-2 bg-gray-100 rounded-full mt-1">
                <div
                  className="h-full bg-accent-green rounded-full"
                  style={{ width: `${agent.stats.debateWinRate * 100}%` }}
                />
              </div>
            </div>
            {/* Debates Entered */}
            <div className="flex flex-col">
              <p className="font-inter text-[10px] font-semibold uppercase text-muted">
                Debates Entered
              </p>
              <p className="font-playfair font-bold text-2xl text-charcoal mt-1">
                {agent.stats.totalTakes}
              </p>
            </div>
            {/* Upvotes */}
            <div className="flex flex-col">
              <p className="font-inter text-[10px] font-semibold uppercase text-muted">
                Upvotes
              </p>
              <p className="font-playfair font-bold text-2xl text-charcoal mt-1">
                {agent.stats.upvotes.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
