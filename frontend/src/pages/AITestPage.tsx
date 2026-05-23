import { useState } from "react";
import axios from "axios";

type Message = {
  role: "user" | "ai";
  content: string;
};

export default function AITestPage() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const sendPrompt = async () => {
    if (!prompt.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: prompt,
    };

    setMessages((prev) => [...prev, userMessage]);
    setPrompt("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/ai/test", {
        prompt,
      });

      // backend now returns:
      // { status: "ok", data: { summary, severity, recommendation } }

      const data = res.data?.data;

      if (!data) {
        throw new Error("Invalid API response: missing data field");
      }

      const aiMessage: Message = {
        role: "ai",
        content: `🧠 Summary: ${data.summary}

⚠️ Severity: ${data.severity}

💡 Recommendation: ${data.recommendation}`,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "Error calling AI: " + err.message,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-slate-700">
        <h1 className="text-xl font-bold">AI Test Page</h1>
        <p className="text-sm text-slate-400">
          Orbitwatch AI analysis endpoint test
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 space-y-4 overflow-y-auto">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[75%] px-4 py-3 rounded-lg whitespace-pre-line ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-700 text-white"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-slate-400 text-sm">
            AI is analyzing telemetry...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-slate-700 flex gap-2">
        <input
          className="flex-1 p-3 rounded bg-slate-800 border border-slate-600 outline-none focus:border-blue-500"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter satellite data or prompt..."
          onKeyDown={(e) => {
            if (e.key === "Enter") sendPrompt();
          }}
        />

        <button
          onClick={sendPrompt}
          className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}