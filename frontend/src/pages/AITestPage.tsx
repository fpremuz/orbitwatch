import { useState } from "react"

export default function AITestPage() {
  const [prompt, setPrompt] = useState("")
  const [result, setResult] = useState("")
  const [loading, setLoading] = useState(false)

  async function handleTest() {
    setLoading(true)

    const res = await fetch("http://localhost:8000/ai/test", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    })

    const data = await res.json()

    setResult(data.result)
    setLoading(false)
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Test Page</h1>

      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter prompt..."
        rows={5}
        style={{ width: "100%" }}
      />

      <button onClick={handleTest} disabled={loading}>
        {loading ? "Running..." : "Test AI"}
      </button>

      <pre style={{ marginTop: 20 }}>
        {result}
      </pre>
    </div>
  )
}