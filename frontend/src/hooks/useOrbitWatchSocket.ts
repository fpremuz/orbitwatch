import { useEffect } from "react"


function useOrbitWatchSocket() {

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

    }

    socket.onclose = () => {

      console.log(
        "Socket disconnected"
      )

    }

    return () => {

      socket.close()

    }

  }, [])

}


export default useOrbitWatchSocket