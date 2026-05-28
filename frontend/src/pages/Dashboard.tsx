import {
  useEffect,
  useState,
  useCallback,
} from "react"

import { orbitwatchApi } from "../api/orbitwatchApi"

import type { Alert } from "../types/alert"

import type {
  TelemetryPoint,
  TelemetryEvent,
} from "../types/telemetry"

import type {
  SatelliteOverview,
} from "../types/satelliteOverview"

import SatelliteOverviewCard from "../components/SatelliteOverviewCard"

import AlertsTable from "../components/AlertsTable"

import TelemetryChart from "../components/telemetry/TelemetryChart"

import TelemetryParameterSelector from "../components/telemetry/TelemetryParameterSelector"

import SatelliteSelector from "../components/SatelliteSelector"

import useOrbitWatchSocket from "../hooks/useOrbitWatchSocket"

import ConnectionStatus from "../components/telemetry/ConnectionStatus"


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
    useState("temperature_c")

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState("")


  const {
    connected,
    events,
  } = useOrbitWatchSocket()


  const loadTelemetry = useCallback(
    async (
      satelliteId: string,
      parameter: string
    ) => {

      try {

        const response =
          await orbitwatchApi.get(
            `/telemetry/history/${satelliteId}?parameter=${parameter}`
          )

        const formatted =
          response.data.map(
            (point: TelemetryPoint) => ({
              ...point,
              timestampMs:
                new Date(
                  point.timestamp
                ).getTime(),
            })
          )

        formatted.sort(
          (a: TelemetryPoint, b: TelemetryPoint) =>
            a.timestampMs - b.timestampMs
        )

        setTelemetryData(
          formatted
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


  useEffect(() => {

    async function initialize() {

      try {

        setLoading(true)

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
          satellitesData.length > 0
        ) {

          const firstSatelliteId =
            satellitesData[0].id

          setSelectedSatelliteId(
            firstSatelliteId
          )

          const alertResponse =
            await orbitwatchApi.get(
              `/alerts/?satellite_id=${firstSatelliteId}`
            )

          setAlerts(
            alertResponse.data
          )

          await loadTelemetry(
            firstSatelliteId,
            selectedParameter
          )

        }

        setError("")

      } catch (error) {

        console.error(
          "Dashboard initialization failed",
          error
        )

        setError(
          "Failed to load dashboard data"
        )

      } finally {

        setLoading(false)

      }

    }

    initialize()

  }, [
    loadTelemetry,
    selectedParameter,
  ])


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


  useEffect(() => {

    if (!events.length) {
      return
    }

    const matchingEvents =
      events.filter(
        (
          event: TelemetryEvent
        ) =>
          event.satellite_id ===
          selectedSatelliteId
      )

    if (!matchingEvents.length) {
      return
    }

    const newPoints: TelemetryPoint[] = []

    matchingEvents.forEach(
      (
        event: TelemetryEvent
      ) => {

        const parameter =
          event.parameters.find(
            (parameter) =>
              parameter.name ===
              selectedParameter
          )

        if (!parameter) {
          return
        }

        newPoints.push({

          timestamp:
            event.timestamp,

          timestampMs:
            new Date(
              event.timestamp
            ).getTime(),

          value:
            parameter.value,

        })

      }
    )

    if (!newPoints.length) {
      return
    }

    setTelemetryData((prev) => {

      const updated = [
        ...prev,
        ...newPoints,
      ]

      updated.sort(
        (a, b) =>
          a.timestampMs - b.timestampMs
      )

      return updated.slice(-200)

    })

  }, [
    events,
    selectedSatelliteId,
    selectedParameter,
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

        <div className="
          flex
          flex-col
          gap-4
          mb-8
        ">

          <ConnectionStatus
            connected={connected}
          />

        </div>

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