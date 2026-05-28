import {
  LineChart,
  Line,
  ResponsiveContainer,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts"

import type { TelemetryPoint } from "../../types/telemetry"

interface Props {
  title: string
  data: TelemetryPoint[]
}

function TelemetryChart({
  title,
  data,
}: Props) {

  const normalizedData = data.map((point) => {

    console.log(
      "RAW TIMESTAMP:",
      point.timestamp
    )

    console.log(
      "PARSED DATE:",
      new Date(point.timestamp)
    )

    console.log(
      "TIMESTAMP MS:",
      new Date(point.timestamp).getTime()
    )

    return {
      ...point,

      timestampMs: new Date(
        point.timestamp
      ).getTime(),
    }

  })

  return (

    <div className="
      bg-slate-900
      border
      border-slate-800
      rounded-2xl
      p-6
    ">

      <h2 className="
        text-xl
        font-semibold
        mb-6
      ">
        {title}
      </h2>

      <div className="h-[300px]">

        <ResponsiveContainer
          width="100%"
          height="100%"
        >

          <LineChart
            data={normalizedData}
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
          >

            <CartesianGrid
              strokeDasharray="3 3"
            />

            <XAxis
              type="number"
              dataKey="timestampMs"
              domain={[
                Date.now() - 120000,
                Date.now(),
              ]}

              tickFormatter={(value) => {

                return new Date(value)
                  .toLocaleTimeString(
                    [],
                    {
                      hour: "2-digit",
                      minute: "2-digit",
                      second: "2-digit",
                      fractionalSecondDigits: 3,
                    }
                  )

              }}
            />

            <YAxis />

            <Tooltip
              labelFormatter={(value) => {

                return new Date(
                  Number(value)
                ).toLocaleString()

              }}
            />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#22d3ee"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>

  )

}

export default TelemetryChart