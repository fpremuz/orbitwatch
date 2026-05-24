interface Props {

  severity: string | null

}


function SatelliteStatusBadge({
  severity,
}: Props) {

  let badgeColor =
    "bg-green-500/20 text-green-400"

  let label = "NOMINAL"


  if (severity === "WARNING") {

    badgeColor =
      "bg-yellow-500/20 text-yellow-400"

    label = "WARNING"

  }


  if (
    severity === "CRITICAL"
    || severity === "ANOMALY"
  ) {

    badgeColor =
      "bg-red-500/20 text-red-400"

    label = severity

  }


  return (

    <div className={`
      px-3
      py-1
      rounded-full
      text-xs
      font-semibold
      border
      border-current
      ${badgeColor}
    `}>

      {label}

    </div>

  )

}


export default SatelliteStatusBadge