import './Logo.css'
import logoImage from '../images/Nexus-logo.png'

const Logo = ({ size = 'medium' }) => {
  const sizeClass = `logo-${size}`
  
  return (
    <div className={`logo-container ${sizeClass}`}>
      <img 
        src={logoImage} 
        alt="Nexus Education Logo" 
        className="logo-image"
      />
    </div>
  )
}

export default Logo

