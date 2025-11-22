import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import Logo from './Logo'
import Configuracoes from './Configuracoes'
import PoliticasPrivacidade from './PoliticasPrivacidade'
import './Sidebar.css'

const Sidebar = () => {
  const [showConfig, setShowConfig] = useState(false)
  const [showPoliticas, setShowPoliticas] = useState(false)
  const { logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <>
      <aside className="sidebar">
        <div className="sidebar-header">
          <Logo size="small" />
        </div>
        
        <nav className="sidebar-nav">
          <button 
            className="nav-item"
            onClick={() => setShowConfig(true)}
          >
            ⚙️ Configurações
          </button>
          
          <button 
            className="nav-item"
            onClick={() => setShowPoliticas(true)}
          >
            🔒 Políticas de Privacidade
          </button>
          
          <button 
            className="nav-item logout"
            onClick={handleLogout}
          >
            🚪 Logout
          </button>
        </nav>
      </aside>

      {showConfig && (
        <Configuracoes onClose={() => setShowConfig(false)} />
      )}

      {showPoliticas && (
        <PoliticasPrivacidade onClose={() => setShowPoliticas(false)} />
      )}
    </>
  )
}

export default Sidebar

