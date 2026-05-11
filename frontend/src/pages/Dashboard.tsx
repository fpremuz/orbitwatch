import { useEffect, useState } from "react"

import { orbitwatchApi } from "../api/orbitwatchApi"

import type { Satellite } from "../types/satellite"

import SatelliteCard from "../components/SatelliteCard"


function Dashboard() {

  const [satellites, setSatellites] = useState<
    Satellite[]
  >([])

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState("")


  useEffect(() => {

    orbitwatchApi
      .get("/satellites")
      .then((response) => {

        setSatellites(response.data)

      })
      .catch(() => {

        setError(
          "Failed to load satellites"
        )

      })
      .finally(() => {

        setLoading(false)

      })

  }, [])


  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <div className="mb-10">

        <h1 className="text-4xl font-bold mb-2">
          OrbitWatch Mission Control
        </h1>

        <p className="text-slate-400">
          Telemetry and satellite operations dashboard
        </p>

      </div>


      {loading && (
        <p className="text-slate-400">
          Loading satellites...
        </p>
      )}

      {error && (
        <p className="text-red-500">
          {error}
        </p>
      )}


      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

        {satellites.map((satellite) => (

          <SatelliteCard
            key={satellite.id}
            satellite={satellite}
          />

        ))}

      </div>

    </div>
  )
}

export default Dashboard