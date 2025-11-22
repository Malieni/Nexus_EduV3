import './Modal.css'

const Configuracoes = ({ onClose }) => {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>⚙️ Configurações</h3>
          <button className="close-button" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="modal-body">
          <p>Funcionalidade de configurações em desenvolvimento.</p>
          <p>Em breve você poderá personalizar as preferências do sistema aqui.</p>
        </div>
      </div>
    </div>
  )
}

export default Configuracoes

