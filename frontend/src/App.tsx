import { BrowserRouter, Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import AITestPage from "./pages/AITestPage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/ai/test" element={<AITestPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App