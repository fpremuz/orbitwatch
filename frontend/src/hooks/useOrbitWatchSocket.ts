import { useEffect } from "react"


interface Props {

  onTelemetryProcessed: () => void

}


function useOrbitWatchSocket({
  onTelemetryProcessed,
}: Props) {

  useEffect(() => {

    const socket =
      new WebSocket(
        "ws://localhost:8000/ws"
      )

    socket.onopen = () => {

      console.log(
        "Connected to OrbitWatch socket"
      )

    }

    socket.onmessage = (event) => {

      const data =
        JSON.parse(event.data)

      console.log(
        "Socket message:",
        data
      )

      if (
        data.type ===
        "telemetry_processed"
      ) {

        onTelemetryProcessed()

      }

    }

    socket.onclose = () => {

      console.log(
        "Socket disconnected"
      )

    }

    return () => {

      socket.close()

    }

  }, [onTelemetryProcessed])

}


export default useOrbitWatchSocket