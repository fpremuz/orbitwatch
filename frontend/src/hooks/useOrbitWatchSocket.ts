import { useEffect, useState } from "react"

export interface TelemetryEvent {

  satellite_id: string

  timestamp: string

  parameters: {
    name: string
    value: number
  }[]

}

interface SocketMessage {

  type: string

  events?: TelemetryEvent[]

}

function useOrbitWatchSocket() {

  const [connected, setConnected] =
    useState(false)

  const [events, setEvents] =
    useState<TelemetryEvent[]>([])

  useEffect(() => {

    const socket =
      new WebSocket(
        "ws://localhost:8000/ws/telemetry"
      )

    socket.onopen = () => {

      console.log(
        "Connected to OrbitWatch socket"
      )

      setConnected(true)

    }

    socket.onmessage = (event) => {

      const data: SocketMessage =
        JSON.parse(event.data)

      console.log(
        "Socket message:",
        data
      )

      if (
        data.type ===
        "telemetry_processed"
        &&
        data.events
      ) {

        setEvents((prev) =>
          [...prev, ...data.events!]
            .sort(
              (a, b) =>
                new Date(a.timestamp).getTime() -
                new Date(b.timestamp).getTime()
            )
            .slice(-50)
        )

      }

    }

    socket.onclose = () => {

      console.log(
        "Socket disconnected"
      )

      setConnected(false)

    }

    return () => {

      socket.close()

    }

  }, [])

  return {
    connected,
    events,
  }

}

export default useOrbitWatchSocket