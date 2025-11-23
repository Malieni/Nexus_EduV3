import axios from 'axios'

// Debug: Verificar URL da API
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
console.log('🔌 API URL configurada:', apiUrl)

const api = axios.create({
  baseURL: apiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos de timeout
})

// Interceptor para debug de erros
api.interceptors.request.use(
  (config) => {
    console.log('📤 Requisição:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    console.error('❌ Erro na requisição:', error)
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    console.log('✅ Resposta:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('❌ Erro na resposta:', error.message)
    if (error.code === 'ECONNABORTED') {
      console.error('⏱️ Timeout: O servidor demorou muito para responder')
    } else if (error.code === 'ERR_NETWORK') {
      console.error('🌐 Erro de rede: Não foi possível conectar ao servidor')
      console.error('🔗 Verifique se a URL está correta:', apiUrl)
    }
    return Promise.reject(error)
  }
)

export default api

