interface Props {
  level: string
}

function AlertLevelBadge({ level }: Props) {

  const styles: Record<string, string> = {
    INFO: "bg-blue-500/20 text-blue-400",
    WARNING: "bg-yellow-500/20 text-yellow-400",
    CRITICAL: "bg-red-500/20 text-red-400",
  }

  return (
    <span
      className={`
        px-3 py-1 rounded-full text-xs font-semibold
        ${styles[level] || "bg-slate-700 text-slate-300"}
      `}
    >
      {level}
    </span>
  )
}

export default AlertLevelBadge