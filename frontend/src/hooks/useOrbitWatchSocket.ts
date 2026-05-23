import {
  useEffect,
  useRef,
  useState,
} from "react"

import type {
  TelemetryEvent,
} from "../types/telemetry"


function useOrbitWatchSocket() {

  const socketRef =
    useRef<WebSocket | null>(null)

  const reconnectTimeoutRef =
    useRef<number | null>(null)

  const [connected, setConnected] =
    useState(false)

  const [events, setEvents] =
    useState<TelemetryEvent[]>([])


  useEffect(() => {

    function connect() {

      const socket =
        new WebSocket(
          "ws://localhost:8000/ws/telemetry"
        )

      socketRef.current = socket

      socket.onopen = () => {

        console.log(
          "Connected to OrbitWatch socket"
        )

        setConnected(true)

      }

      socket.onclose = () => {

        console.log(
          "Disconnected from OrbitWatch socket"
        )

        setConnected(false)

        reconnectTimeoutRef.current =
          window.setTimeout(() => {

            connect()

          }, 3000)

      }

      socket.onerror = (error) => {

        console.error(
          "WebSocket error",
          error
        )

        socket.close()

      }

      socket.onmessage = (event) => {

        try {

          const parsed =
            JSON.parse(event.data)

          if (
            parsed.type !==
            "telemetry_processed"
          ) {
            return
          }

          setEvents((prev) => {

            const updated = [
              ...prev,
              ...parsed.events,
            ]

            return updated.slice(-50)

          })

        } catch (error) {

          console.error(
            "Failed to parse websocket message",
            error
          )

        }

      }

    }

    connect()

    return () => {

      if (reconnectTimeoutRef.current) {

        clearTimeout(
          reconnectTimeoutRef.current
        )

      }

      socketRef.current?.close()

    }

  }, [])


  return {
    connected,
    events,
  }

}


export default useOrbitWatchSocket