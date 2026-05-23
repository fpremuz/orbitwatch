import { useState } from "react";
import axios from "axios";

export default function AITestPage() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const testAI = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post("http://localhost:8000/ai/test", {
        prompt,
      });

      setResult(res.data);
    } catch (err: any) {
      setResult({ error: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-2xl font-bold mb-4">AI Test Page</h1>

      <textarea
        className="w-full p-3 rounded bg-slate-800 border border-slate-600"
        rows={4}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter prompt..."
      />

      <button
        className="mt-3 px-4 py-2 bg-blue-600 rounded hover:bg-blue-700"
        onClick={testAI}
      >
        {loading ? "Thinking..." : "Test AI"}
      </button>

      {result && (
        <pre className="mt-6 bg-slate-800 p-4 rounded overflow-auto">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}