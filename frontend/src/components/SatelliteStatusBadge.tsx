interface Props {

  level: string | null

}


function SatelliteStatusBadge({
  level,
}: Props) {

  let badgeColor =
    "bg-green-500/20 text-green-400"

  let label = "NOMINAL"


  if (level === "WARNING") {

    badgeColor =
      "bg-yellow-500/20 text-yellow-400"

    label = "WARNING"

  }


  if (
    level === "CRITICAL"
    || level === "ANOMALY"
  ) {

    badgeColor =
      "bg-red-500/20 text-red-400"

    label = level

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