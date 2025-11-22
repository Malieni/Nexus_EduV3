import { useState } from 'react'
import api from '../services/api'
import AnalysisTable from './AnalysisTable'
import UploadForm from './UploadForm'
import './Dashboard.css'

const Dashboard = ({ analyses, loading, error, onUploadSuccess }) => {
  const [uploadLoading, setUploadLoading] = useState(false)
  const [uploadError, setUploadError] = useState('')

  const handleUpload = async (studentName, file) => {
    setUploadError('')
    setUploadLoading(true)

    try {
      const formData = new FormData()
      formData.append('student_name', studentName)
      formData.append('pdf_file', file)

      await api.post('/api/analysis/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onUploadSuccess()
      setUploadError('')
    } catch (err) {
      setUploadError(
        err.response?.data?.detail || 'Erro ao fazer upload do arquivo'
      )
    } finally {
      setUploadLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <div className="dashboard-card">
        <h2>📊 Dashboard</h2>
        <div className="stats">
          <div className="stat-item">
            <div className="stat-value">{analyses.length}</div>
            <div className="stat-label">Total de Análises</div>
          </div>
        </div>
      </div>

      <UploadForm 
        onUpload={handleUpload} 
        loading={uploadLoading}
        error={uploadError}
      />

      <AnalysisTable analyses={analyses} loading={loading} error={error} />
    </div>
  )
}

export default Dashboard

