interface Props {
  severity: string
}

function AlertSeverityBadge({ severity }: Props) {

  const styles: Record<string, string> = {
    INFO: "bg-blue-500/20 text-blue-400",
    WARNING: "bg-yellow-500/20 text-yellow-400",
    CRITICAL: "bg-red-500/20 text-red-400",
  }

  return (
    <span
      className={`
        px-3 py-1 rounded-full text-xs font-semibold
        ${styles[severity] || "bg-slate-700 text-slate-300"}
      `}
    >
      {severity}
    </span>
  )
}

export default AlertSeverityBadge