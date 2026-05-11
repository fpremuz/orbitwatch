import { useEffect, useState } from "react"

import { orbitwatchApi } from "../api/orbitwatchApi"

import type { Satellite } from "../types/satellite"
import type { Alert } from "../types/alert"

import SatelliteCard from "../components/SatelliteCard"
import AlertsTable from "../components/AlertsTable"


function Dashboard() {

  const [satellites, setSatellites] = useState<
    Satellite[]
  >([])

  const [alerts, setAlerts] = useState<
    Alert[]
  >([])

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState("")


  useEffect(() => {

    Promise.all([
      orbitwatchApi.get("/satellites"),
      orbitwatchApi.get("/alerts"),
    ])
      .then(([satelliteResponse, alertResponse]) => {

        setSatellites(
          satelliteResponse.data
        )

        setAlerts(
          alertResponse.data
        )

      })
      .catch(() => {

        setError(
          "Failed to load dashboard data"
        )

      })
      .finally(() => {

        setLoading(false)

      })

  }, [])


  useEffect(() => {

    const interval = setInterval(() => {

      orbitwatchApi
        .get("/alerts")
        .then((response) => {

          setAlerts(response.data)

        })

    }, 5000)

    return () => clearInterval(interval)

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
          Loading dashboard...
        </p>
      )}

      {error && (
        <p className="text-red-500">
          {error}
        </p>
      )}


      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 mb-10">

        {satellites.map((satellite) => (

          <SatelliteCard
            key={satellite.id}
            satellite={satellite}
          />

        ))}

      </div>


      <AlertsTable alerts={alerts} />

    </div>
  )
}

export default Dashboard