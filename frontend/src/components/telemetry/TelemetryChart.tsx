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

  // -----------------------------------
  // Normalize + sanitize chart data
  // -----------------------------------
  const normalizedData = [...data]

    // remove invalid entries
    .filter((point) => {

      return (
        point.timestamp &&
        point.value !== undefined &&
        point.value !== null
      )
    })

    // normalize timestamp/value
    .map((point) => {

      return {

        ...point,

        timestamp: new Date(
          point.timestamp
        ).toISOString(),

        value: Number(point.value),
      }
    })

    // sort chronologically
    .sort((a, b) => {

      return (
        new Date(a.timestamp).getTime()
        -
        new Date(b.timestamp).getTime()
      )
    })

    // optional:
    // keep latest 30 points only
    .slice(-30)

  return (

    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

      <h2 className="text-xl font-semibold mb-6">
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
              bottom: 10,
            }}
          >

            <CartesianGrid
              strokeDasharray="3 3"
            />

            <XAxis
              dataKey="timestamp"

              minTickGap={40}

              tickFormatter={(value) => {

                return new Date(value)
                  .toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                  })
              }}
            />

            <YAxis
              domain={["auto", "auto"]}
            />

            <Tooltip

              labelFormatter={(value) => {

                return new Date(value)
                  .toLocaleString()
              }}

              formatter={(value) => [

                Number(value).toFixed(2),

                "Value",
              ]}
            />

            <Line
              type="monotone"

              dataKey="value"

              stroke="#22d3ee"

              strokeWidth={2}

              dot={false}

              isAnimationActive={false}

              connectNulls
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  )
}

export default TelemetryChart