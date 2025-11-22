import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import api from '../services/api'
import Sidebar from '../components/Sidebar'
import Dashboard from '../components/Dashboard'
import './AreaPrincipal.css'

const AreaPrincipal = () => {
  const { user } = useAuth()
  const [analyses, setAnalyses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    loadAnalyses()
  }, [])

  const loadAnalyses = async () => {
    try {
      setLoading(true)
      const response = await api.get('/api/analysis/')
      setAnalyses(response.data)
      setError('')
    } catch (err) {
      setError('Erro ao carregar análises')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleUploadSuccess = () => {
    loadAnalyses()
  }

  return (
    <div className="area-principal">
      <Sidebar />
      <div className="main-content">
        <header className="main-header">
          <h1>Bem-vindo, {user?.name}!</h1>
        </header>
        <Dashboard 
          analyses={analyses} 
          loading={loading} 
          error={error}
          onUploadSuccess={handleUploadSuccess}
        />
      </div>
    </div>
  )
}

export default AreaPrincipal

