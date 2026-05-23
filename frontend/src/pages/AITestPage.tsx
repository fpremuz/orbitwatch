import { useState } from "react"
import axios from "axios"

export default function AITestPage() {
  const [prompt, setPrompt] = useState("")
  const [result, setResult] = useState("")
  const [loading, setLoading] = useState(false)

  const testAI = async () => {
    setLoading(true)
    setResult("")

    try {
      const res = await axios.post("http://localhost:8000/ai/test", {
        prompt,
      })

      setResult(res.data.result)
    } catch (err) {
      setResult("Error calling AI")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
      <div className="w-full max-w-xl space-y-4">

        <h1 className="text-3xl font-bold">
          AI Test Page
        </h1>

        <textarea
          className="w-full p-3 rounded-lg bg-slate-900 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={5}
          placeholder="Write your prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />

        <button
          onClick={testAI}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Test AI"}
        </button>

        {result && (
          <div className="p-4 rounded-lg bg-slate-900 border border-slate-700">
            <pre className="whitespace-pre-wrap">{result}</pre>
          </div>
        )}
      </div>
    </div>
  )
}