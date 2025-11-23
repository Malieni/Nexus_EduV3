import { createContext, useState, useEffect, useContext } from 'react'
import api from '../services/api'

const AuthContext = createContext({})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('token'))

  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
      loadUser()
    } else {
      setLoading(false)
    }
  }, [token])

  const loadUser = async () => {
    try {
      const response = await api.get('/api/auth/me')
      setUser(response.data)
    } catch (error) {
      console.error('Erro ao carregar usuário:', error)
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await api.post('/api/auth/login', { email, password })
      const { access_token, user } = response.data
      
      localStorage.setItem('token', access_token)
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      setToken(access_token)
      setUser(user)
      
      return { success: true }
    } catch (error) {
      console.error('Erro ao fazer login:', error)
      console.error('Resposta do servidor:', error.response)
      
      // Extrai mensagem de erro mais detalhada
      let errorMessage = 'Erro ao fazer login'
      
      if (error.response) {
        errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage
      } else if (error.request) {
        errorMessage = 'Não foi possível conectar ao servidor. Verifique sua conexão.'
      } else {
        errorMessage = error.message || errorMessage
      }
      
      return {
        success: false,
        error: errorMessage
      }
    }
  }

  const register = async (name, email, password) => {
    try {
      const response = await api.post('/api/auth/register', {
        name,
        email,
        password
      })
      const { access_token, user } = response.data
      
      localStorage.setItem('token', access_token)
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      setToken(access_token)
      setUser(user)
      
      return { success: true }
    } catch (error) {
      console.error('Erro ao cadastrar:', error)
      console.error('Resposta do servidor:', error.response)
      
      // Extrai mensagem de erro mais detalhada
      let errorMessage = 'Erro ao cadastrar'
      
      if (error.response) {
        // Erro com resposta do servidor
        errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage
      } else if (error.request) {
        // Requisição feita mas sem resposta
        errorMessage = 'Não foi possível conectar ao servidor. Verifique sua conexão.'
      } else {
        // Erro ao configurar a requisição
        errorMessage = error.message || errorMessage
      }
      
      return {
        success: false,
        error: errorMessage
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    delete api.defaults.headers.common['Authorization']
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

