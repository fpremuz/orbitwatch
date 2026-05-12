import {
  useEffect,
  useState,
  useCallback,
} from "react"

import { orbitwatchApi } from "../api/orbitwatchApi"

import type { Alert } from "../types/alert"
import type { TelemetryPoint } from "../types/telemetry"
import type { SatelliteOverview } from "../types/satelliteOverview"

import SatelliteOverviewCard from "../components/SatelliteOverviewCard"
import AlertsTable from "../components/AlertsTable"
import TelemetryChart from "../components/TelemetryChart"
import TelemetryParameterSelector from "../components/TelemetryParameterSelector"
import SatelliteSelector from "../components/SatelliteSelector"

import useOrbitWatchSocket from "../hooks/useOrbitWatchSocket"


function Dashboard() {

  const [satellites, setSatellites] =
    useState<SatelliteOverview[]>([])

  const [selectedSatelliteId, setSelectedSatelliteId] =
    useState("")

  const [alerts, setAlerts] =
    useState<Alert[]>([])

  const [telemetryData, setTelemetryData] =
    useState<TelemetryPoint[]>([])

  const [selectedParameter, setSelectedParameter] =
    useState("temperature")

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState("")


  const loadTelemetry = useCallback(
    async (
      satelliteId: string,
      parameter: string
    ) => {

      try {

        const telemetryResponse =
          await orbitwatchApi.get(
            `/telemetry/history/${satelliteId}?parameter=${parameter}`
          )

        setTelemetryData(
          telemetryResponse.data
        )

      } catch (error) {

        console.error(
          "Failed to load telemetry",
          error
        )

      }

    },
    []
  )


  const refreshDashboard = useCallback(
    async () => {

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

        if (
          satellitesData.length > 0 &&
          !selectedSatelliteId
        ) {

          setSelectedSatelliteId(
            satellitesData[0].id
          )

        }

        const satelliteId =
          selectedSatelliteId ||
          satellitesData[0]?.id

        const alertResponse =
          await orbitwatchApi.get(
            `/alerts?satellite_id=${satelliteId}`
          )

        setAlerts(
          alertResponse.data
        )

        if (satelliteId) {

          await loadTelemetry(
            satelliteId,
            selectedParameter
          )

        }

      } catch (error) {

        console.error(
          "Dashboard refresh failed",
          error
        )

      }

    },
    [
      loadTelemetry,
      selectedParameter,
      selectedSatelliteId,
    ]
  )


  useOrbitWatchSocket({
    onTelemetryProcessed:
      refreshDashboard,
  })


  useEffect(() => {

    async function initialize() {

      try {

        await refreshDashboard()

      } catch (error) {

        console.error(error)

        setError(
          "Failed to load dashboard data"
        )

      } finally {

        setLoading(false)

      }

    }

    initialize()

  }, [refreshDashboard])


  useEffect(() => {

    if (!selectedSatelliteId) {
      return
    }

    loadTelemetry(
      selectedSatelliteId,
      selectedParameter
    )

  }, [
    selectedSatelliteId,
    selectedParameter,
    loadTelemetry,
  ])


  return (

    <div className="
      min-h-screen
      bg-slate-950
      text-white
      p-8
    ">

      <div className="mb-10">

        <h1 className="
          text-4xl
          font-bold
          mb-2
        ">
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


      <div className="mb-6">

        <SatelliteSelector
          satellites={satellites}
          value={selectedSatelliteId}
          onChange={setSelectedSatelliteId}
        />

      </div>


      <div className="mb-10">

        <TelemetryParameterSelector
          value={selectedParameter}
          onChange={setSelectedParameter}
        />

        <TelemetryChart
          title={`${selectedParameter} Telemetry`}
          data={telemetryData}
        />

      </div>


      <AlertsTable
        alerts={alerts}
      />

    </div>

  )

}


export default Dashboard