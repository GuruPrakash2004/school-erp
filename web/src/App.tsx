import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { TOKEN_KEY } from './api'
import Login from './pages/Login'
import Marks from './pages/Marks'

function RequireLogin({ children }: { children: React.ReactNode }) {
  return localStorage.getItem(TOKEN_KEY) ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/marks"
          element={
            <RequireLogin>
              <Marks />
            </RequireLogin>
          }
        />
        <Route path="*" element={<Navigate to="/marks" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
