import type { Satellite } from "../types/satellite"

interface Props {
  satellite: Satellite
}

function SatelliteCard({ satellite }: Props) {

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-cyan-500 transition-all">

      <div className="flex items-center justify-between mb-4">

        <h2 className="text-xl font-semibold text-white">
          {satellite.name}
        </h2>

        <div className="w-3 h-3 rounded-full bg-green-500" />

      </div>

      <div className="space-y-2 text-sm text-slate-400">

        <p>
          NORAD ID: {satellite.norad_id}
        </p>

        <p>
          Satellite ID: {satellite.id}
        </p>

        <p>
          Registered:{" "}
          {new Date(
            satellite.created_at
          ).toLocaleString()}
        </p>

      </div>

    </div>
  )
}

export default SatelliteCard