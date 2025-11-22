import { useState } from 'react'
import './UploadForm.css'

const UploadForm = ({ onUpload, loading, error }) => {
  const [studentName, setStudentName] = useState('')
  const [file, setFile] = useState(null)
  const [fileName, setFileName] = useState('')

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      if (selectedFile.type !== 'application/pdf') {
        alert('Apenas arquivos PDF são aceitos')
        return
      }
      setFile(selectedFile)
      setFileName(selectedFile.name)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (!studentName.trim()) {
      alert('Por favor, informe o nome do aluno')
      return
    }

    if (!file) {
      alert('Por favor, selecione um arquivo PDF')
      return
    }

    onUpload(studentName, file)
    
    // Reset form
    setStudentName('')
    setFile(null)
    setFileName('')
    e.target.reset()
  }

  return (
    <div className="upload-form-card">
      <h2>📄 Enviar Ementa (PDF)</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="studentName">Nome do Aluno</label>
          <input
            type="text"
            id="studentName"
            value={studentName}
            onChange={(e) => setStudentName(e.target.value)}
            required
            placeholder="Nome completo do aluno"
          />
        </div>

        <div className="form-group">
          <label htmlFor="pdfFile">Arquivo PDF</label>
          <div className="file-input-wrapper">
            <input
              type="file"
              id="pdfFile"
              accept=".pdf"
              onChange={handleFileChange}
              required
              className="file-input"
            />
            <label htmlFor="pdfFile" className="file-label">
              {fileName || 'Selecionar arquivo PDF'}
            </label>
          </div>
        </div>

        <button type="submit" disabled={loading} className="submit-button">
          {loading ? 'Enviando e analisando...' : 'Enviar e Analisar'}
        </button>
      </form>
    </div>
  )
}

export default UploadForm

