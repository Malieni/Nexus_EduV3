import './Modal.css'

const PoliticasPrivacidade = ({ onClose }) => {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>🔒 Políticas de Privacidade</h3>
          <button className="close-button" onClick={onClose}>
            ×
          </button>
        </div>
        <div className="modal-body">
          <h4>1. Coleta de Informações</h4>
          <p>
            O Nexus Education coleta informações necessárias para fornecer
            serviços de análise de ementas acadêmicas, incluindo dados de
            usuários e documentos enviados.
          </p>

          <h4>2. Uso das Informações</h4>
          <p>
            As informações coletadas são utilizadas exclusivamente para
            fornecer os serviços do sistema, incluindo análise de documentos
            e histórico de análises.
          </p>

          <h4>3. Proteção de Dados</h4>
          <p>
            Todos os dados são armazenados de forma segura e protegidos contra
            acesso não autorizado. Utilizamos criptografia e medidas de
            segurança adequadas.
          </p>

          <h4>4. Compartilhamento</h4>
          <p>
            Não compartilhamos suas informações pessoais com terceiros, exceto
            quando necessário para fornecer os serviços ou quando exigido por lei.
          </p>

          <h4>5. Seus Direitos</h4>
          <p>
            Você tem o direito de acessar, corrigir ou excluir suas informações
            pessoais a qualquer momento através das configurações da conta.
          </p>

          <p style={{ marginTop: '20px', fontSize: '0.9rem', color: '#666' }}>
            Última atualização: {new Date().toLocaleDateString('pt-BR')}
          </p>
        </div>
      </div>
    </div>
  )
}

export default PoliticasPrivacidade

