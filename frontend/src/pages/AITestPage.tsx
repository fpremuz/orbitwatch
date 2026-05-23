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

      const aiMessage: Message = {
        role: "ai",
        content: res.data.output,
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
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 space-y-4 overflow-auto">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[70%] px-4 py-2 rounded-lg ${
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
          <div className="text-slate-400">AI is thinking...</div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-slate-700 flex gap-2">
        <input
          className="flex-1 p-3 rounded bg-slate-800 border border-slate-600"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your message..."
          onKeyDown={(e) => {
            if (e.key === "Enter") sendPrompt();
          }}
        />

        <button
          onClick={sendPrompt}
          className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}