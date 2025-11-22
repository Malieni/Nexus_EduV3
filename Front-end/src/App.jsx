import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import AreaPrincipal from './pages/AreaPrincipal'
import PrivateRoute from './components/PrivateRoute'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/area-principal"
            element={
              <PrivateRoute>
                <AreaPrincipal />
              </PrivateRoute>
            }
          />
          <Route path="/" element={<Navigate to="/area-principal" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App

