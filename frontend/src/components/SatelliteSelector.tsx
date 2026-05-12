import type { SatelliteOverview }
from "../types/satelliteOverview"

interface Props {

  satellites: SatelliteOverview[]

  value: string

  onChange: (
    value: string
  ) => void

}


function SatelliteSelector({
  satellites,
  value,
  onChange,
}: Props) {

  return (

    <select
      value={value}
      onChange={(e) =>
        onChange(e.target.value)
      }
      className="
        bg-slate-900
        border
        border-slate-700
        rounded-xl
        px-4
        py-2
        text-white
      "
    >

      {satellites.map((satellite) => (

        <option
          key={satellite.id}
          value={satellite.id}
        >
          {satellite.name}
        </option>

      ))}

    </select>

  )

}


export default SatelliteSelector