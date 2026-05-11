import { useEffect, useState } from "react"

import { orbitwatchApi } from "../api/orbitwatchApi"

import type { Alert } from "../types/alert"
import type { TelemetryPoint } from "../types/telemetry"
import type { SatelliteOverview } from "../types/satelliteOverview"

import SatelliteOverviewCard from "../components/SatelliteOverviewCard"
import AlertsTable from "../components/AlertsTable"
import TelemetryChart from "../components/TelemetryChart"
import useOrbitWatchSocket from "../hooks/useOrbitWatchSocket"


function Dashboard() {

  useOrbitWatchSocket()

  const [satellites, setSatellites] = useState<
    SatelliteOverview[]
  >([])

  const [alerts, setAlerts] = useState<
    Alert[]
  >([])

  const [temperatureData, setTemperatureData] =
    useState<TelemetryPoint[]>([])

  const [loading, setLoading] = useState(true)

  const [error, setError] = useState("")


  async function loadTelemetry(
    satelliteId: string
  ) {

    const telemetryResponse =
      await orbitwatchApi.get(
        `/telemetry/history/${satelliteId}?parameter=temperature`
      )

    setTemperatureData(
      telemetryResponse.data
    )

  }


  async function loadDashboard() {

    try {

      const satelliteResponse =
        await orbitwatchApi.get(
          "/satellites/overview"
        )

      const satellitesData =
        satelliteResponse.data

      setSatellites(
        satellitesData
      )

      const alertResponse =
        await orbitwatchApi.get(
          "/alerts"
        )

      setAlerts(
        alertResponse.data
      )

      if (satellitesData.length > 0) {

        await loadTelemetry(
          satellitesData[0].id
        )

      }

    } catch (error) {

      console.error(error)

      setError(
        "Failed to load dashboard data"
      )

    } finally {

      setLoading(false)

    }

  }


  useEffect(() => {

    loadDashboard()

  }, [])


  useEffect(() => {

    if (satellites.length === 0) {
      return
    }

    const interval = setInterval(
      async () => {

        try {

          const alertResponse =
            await orbitwatchApi.get(
              "/alerts"
            )

          setAlerts(
            alertResponse.data
          )

          await loadTelemetry(
            satellites[0].id
          )

        } catch (error) {

          console.error(
            "Polling failed",
            error
          )

        }

      },
      5000
    )

    return () => clearInterval(interval)

  }, [satellites])


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


      <div className="
        grid
        grid-cols-1
        md:grid-cols-2
        xl:grid-cols-3
        gap-6
        mb-10
      ">

        {satellites.map((satellite) => (

          <SatelliteOverviewCard
            key={satellite.id}
            satellite={satellite}
          />

        ))}

      </div>


      <div className="mb-10">

        <TelemetryChart
          title="Temperature Telemetry"
          data={temperatureData}
        />

      </div>


      <AlertsTable
        alerts={alerts}
      />

    </div>

  )

}

export default Dashboard