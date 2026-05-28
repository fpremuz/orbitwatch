interface Props {

  healthScore: number

}


function SatelliteStatusBadge({
  healthScore,
}: Props) {

  let badgeColor =
    "bg-green-500/20 text-green-400"

  let label = "NOMINAL"


  if (healthScore < 90) {

    badgeColor =
      "bg-yellow-500/20 text-yellow-400"

    label = "WARNING"

  }


  if (healthScore < 70) {

    badgeColor =
      "bg-red-500/20 text-red-400"

    label = "CRITICAL"

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