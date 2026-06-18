import { useState, useEffect } from "react";
import axios from "axios";

type Message = {
  role: "user" | "ai";
  content: string;
};

type Conversation = {
  id: string;
  title: string | null;
  created_at: string;
};

export default function AITestPage() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [conversationId, setConversationId] =
    useState<string | null>(null);

  const [conversations, setConversations] =
    useState<Conversation[]>([]);

  useEffect(() => {
    const initialize = async () => {
      await loadConversations();

      const savedConversation =
        localStorage.getItem(
          "orbitwatch_conversation"
        );

      if (savedConversation) {
        await loadConversation(
          savedConversation
        );
      }
    };

    initialize();
  }, []);

  const loadConversations = async () => {
    try {
      const res = await axios.get(
        "http://localhost:8000/chat/conversations"
      );

      setConversations(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const loadConversation = async (
    id: string
  ) => {
    try {
      const res = await axios.get(
        `http://localhost:8000/chat/conversations/${id}`
      );

      const loadedMessages: Message[] =
        res.data.messages.map(
          (m: any) => ({
            role:
              m.role === "assistant"
                ? "ai"
                : "user",
            content: m.content,
          })
        );

      setMessages(loadedMessages);

      setConversationId(id);

      localStorage.setItem(
        "orbitwatch_conversation",
        id
      );

      console.log(
        "Loaded conversation:",
        id
      );
    } catch (err) {
      console.error(err);
    }
  };

  const startNewChat = () => {
    setConversationId(null);
    setMessages([]);

    localStorage.removeItem(
      "orbitwatch_conversation"
    );
  };

  const sendPrompt = async () => {
    if (!prompt.trim()) return;

    const userMessage: Message = {
      role: "user",
      content: prompt,
    };

    setMessages((prev) => [
      ...prev,
      userMessage,
    ]);

    setPrompt("");
    setLoading(true);

    try {
      const res = await axios.post(
        "http://localhost:8000/ai/chat",
        {
          question: prompt,
          conversation_id:
            conversationId,
        }
      );

      const answer =
        res.data?.answer;

      const newConversationId =
        res.data.conversation_id;

      if (newConversationId) {
        setConversationId(
          newConversationId
        );

        localStorage.setItem(
          "orbitwatch_conversation",
          newConversationId
        );
      }

      await loadConversations();

      if (!answer) {
        throw new Error(
          "Invalid API response: missing answer"
        );
      }

      const aiMessage: Message = {
        role: "ai",
        content: answer,
      };

      setMessages((prev) => [
        ...prev,
        aiMessage,
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content:
            "Error calling AI: " +
            err.message,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex">

      {/* SIDEBAR */}

      <div className="w-72 border-r border-slate-700 p-4">

        <button
          onClick={startNewChat}
          className="
            w-full
            mb-4
            p-2
            rounded
            bg-blue-600
            hover:bg-blue-700
            transition
          "
        >
          + New Chat
        </button>

        <h2 className="font-bold mb-4">
          Conversations
        </h2>

        <div className="space-y-2">

          {[...conversations]
            .sort(
              (a, b) =>
                new Date(
                  b.created_at
                ).getTime() -
                new Date(
                  a.created_at
                ).getTime()
            )
            .map((c) => (

              <button
                key={c.id}
                onClick={() =>
                  loadConversation(c.id)
                }
                className={`
                  w-full
                  text-left
                  p-2
                  rounded
                  transition
                  ${
                    conversationId === c.id ? "bg-blue-600" : "bg-slate-800 hover:bg-slate-700"
                  }
                `}
              >
                <div className="font-medium truncate">
                  {c.title ?? "Untitled"}
                </div>

                <div className="text-xs text-slate-400">
                  {c.id.slice(0, 8)}
                </div>
              </button>

            ))}

        </div>

      </div>

      {/* CHAT AREA */}

      <div className="flex-1 flex flex-col">

        {/* HEADER */}

        <div className="p-4 border-b border-slate-700">

          <h1 className="text-xl font-bold">
            AI Test Page
          </h1>

          <p className="text-sm text-slate-400">
            OrbitWatch AI Assistant
          </p>

          {conversationId && (
            <p className="text-xs text-green-400 mt-2">
              Conversation:
              {" "}
              {conversationId}
            </p>
          )}

        </div>

        {/* MESSAGES */}

        <div className="flex-1 p-4 space-y-4 overflow-y-auto">

          {messages.map(
            (msg, i) => (
              <div
                key={i}
                className={`flex ${
                  msg.role ===
                  "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                <div
                  className={`
                    max-w-[75%]
                    px-4
                    py-3
                    rounded-lg
                    whitespace-pre-line
                    ${
                      msg.role ===
                      "user"
                        ? "bg-blue-600"
                        : "bg-slate-700"
                    }
                  `}
                >
                  {msg.content}
                </div>
              </div>
            )
          )}

          {loading && (
            <div className="text-slate-400">
              AI is thinking...
            </div>
          )}

        </div>

        {/* INPUT */}

        <div className="p-4 border-t border-slate-700 flex gap-2">

          <input
            className="
              flex-1
              p-3
              rounded
              bg-slate-800
              border
              border-slate-600
              outline-none
              focus:border-blue-500
            "
            value={prompt}
            onChange={(e) =>
              setPrompt(
                e.target.value
              )
            }
            placeholder="Ask OrbitWatch..."
            onKeyDown={(e) => {
              if (
                e.key === "Enter"
              ) {
                sendPrompt();
              }
            }}
          />

          <button
            onClick={sendPrompt}
            className="
              px-4
              py-2
              bg-blue-600
              rounded
              hover:bg-blue-700
            "
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}