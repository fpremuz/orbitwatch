interface Props {

  value: string

  onChange: (
    parameter: string
  ) => void

}


const parameters = [
  "temperature_c",
  "velocity_kmh",
  "altitude_km",
  "battery_voltage",
]


function TelemetryParameterSelector({
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
        mb-4
      "
    >

      {parameters.map((parameter) => (

        <option
          key={parameter}
          value={parameter}
        >
          {parameter}
        </option>

      ))}

    </select>

  )

}


export default TelemetryParameterSelector