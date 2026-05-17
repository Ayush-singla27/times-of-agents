interface AgentAvatarProps {
  avatar: string
  avatarBg: string
  accentColor: string
  size?: 'sm' | 'md' | 'lg'
  name?: string
}

const sizeMap = {
  sm: { container: 32, fontSize: 17 },
  md: { container: 48, fontSize: 26 },
  lg: { container: 72, fontSize: 38 },
}

export default function AgentAvatar({
  avatar,
  avatarBg,
  accentColor,
  size = 'md',
  name,
}: AgentAvatarProps) {
  const { container, fontSize } = sizeMap[size]
  return (
    <div
      title={name}
      aria-label={name}
      className="rounded-xl flex items-center justify-center flex-shrink-0 select-none"
      style={{
        width: container,
        height: container,
        minWidth: container,
        backgroundColor: avatarBg,
        border: `2px solid ${accentColor}`,
        fontSize,
        lineHeight: 1,
      }}
    >
      {avatar}
    </div>
  )
}
