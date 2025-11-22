import { useState } from 'react'
import './AnalysisTable.css'

const AnalysisTable = ({ analyses, loading, error }) => {
  const [selectedAnalysis, setSelectedAnalysis] = useState(null)

  if (loading) {
    return (
      <div className="analysis-table-card">
        <h2>📋 Histórico de Análises</h2>
        <div className="loading">Carregando análises...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="analysis-table-card">
        <h2>📋 Histórico de Análises</h2>
        <div className="error">{error}</div>
      </div>
    )
  }

  if (analyses.length === 0) {
    return (
      <div className="analysis-table-card">
        <h2>📋 Histórico de Análises</h2>
        <div className="empty-state">
          Nenhuma análise encontrada. Envie uma ementa para começar!
        </div>
      </div>
    )
  }

  return (
    <>
      <div className="analysis-table-card">
        <h2>📋 Histórico de Análises</h2>
        <div className="table-wrapper">
          <table className="analysis-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nome do Aluno</th>
                <th>Data</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {analyses.map((analysis) => (
                <tr key={analysis.id}>
                  <td className="id-cell">{analysis.id.substring(0, 8)}...</td>
                  <td>{analysis.student_name}</td>
                  <td>
                    {new Date(analysis.created_at).toLocaleDateString('pt-BR')}
                  </td>
                  <td>
                    <button
                      className="view-button"
                      onClick={() => setSelectedAnalysis(analysis)}
                    >
                      Ver Detalhes
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {selectedAnalysis && (
        <div className="modal-overlay" onClick={() => setSelectedAnalysis(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Análise - {selectedAnalysis.student_name}</h3>
              <button
                className="close-button"
                onClick={() => setSelectedAnalysis(null)}
              >
                ×
              </button>
            </div>
            <div className="modal-body">
              <div className="analysis-detail">
                {selectedAnalysis.analysis_detail.split('\n').map((line, idx) => (
                  <p key={idx}>{line}</p>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default AnalysisTable

