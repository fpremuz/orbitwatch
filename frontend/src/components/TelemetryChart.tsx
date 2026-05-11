import {
  LineChart,
  Line,
  ResponsiveContainer,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts"

import type { TelemetryPoint } from "../types/telemetry"

interface Props {
  title: string
  data: TelemetryPoint[]
}

function TelemetryChart({
  title,
  data,
}: Props) {

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

      <h2 className="text-xl font-semibold mb-6">
        {title}
      </h2>

      <div className="h-[300px]">

        <ResponsiveContainer width="100%" height="100%">

          <LineChart data={data}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="timestamp"
              tickFormatter={(value) =>
                new Date(value).toLocaleTimeString()
              }
            />

            <YAxis />

            <Tooltip
              labelFormatter={(value) =>
                new Date(value).toLocaleString()
              }
            />

            <Line
              type="monotone"
              dataKey="value"
              stroke="#22d3ee"
              strokeWidth={2}
              dot={false}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  )
}

export default TelemetryChart