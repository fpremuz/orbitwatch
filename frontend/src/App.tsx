import { useEffect, useState } from "react"
import axios from "axios"

function App() {

  const [health, setHealth] = useState("loading")

  useEffect(() => {

    axios
      .get("http://localhost:8000/health/live")
      .then((response) => {
        setHealth(response.data.status)
      })
      .catch(() => {
        setHealth("offline")
      })

  }, [])

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <h1 className="text-4xl font-bold mb-6">
        OrbitWatch Mission Control
      </h1>

      <div className="bg-slate-900 rounded-2xl p-6 border border-slate-800">

        <h2 className="text-xl font-semibold mb-4">
          Backend Status
        </h2>

        <p className="text-slate-300">
          API Status: {health}
        </p>

      </div>

    </div>
  )
}

export default App