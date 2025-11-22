import './Logo.css'

const Logo = ({ size = 'medium', showText = true }) => {
  const sizeClass = `logo-${size}`
  
  return (
    <div className={`logo-container ${sizeClass}`}>
      <div className="logo-graphic">
        <div className="logo-circle top"></div>
        <div className="logo-circle middle left"></div>
        <div className="logo-circle middle right"></div>
        <div className="logo-circle bottom left-1"></div>
        <div className="logo-circle bottom left-2"></div>
        <div className="logo-circle bottom right-1"></div>
        <div className="logo-circle bottom right-2"></div>
        <svg className="logo-lines" viewBox="0 0 100 100" preserveAspectRatio="none">
          <line x1="50" y1="20" x2="50" y2="45" className="line-1" />
          <line x1="30" y1="50" x2="50" y2="45" className="line-2" />
          <line x1="70" y1="50" x2="50" y2="45" className="line-3" />
          <line x1="20" y1="80" x2="30" y2="55" className="line-4" />
          <line x1="40" y1="80" x2="30" y2="55" className="line-5" />
          <line x1="60" y1="80" x2="70" y2="55" className="line-6" />
          <line x1="80" y1="80" x2="70" y2="55" className="line-7" />
        </svg>
      </div>
      {showText && (
        <div className="logo-text">
          <div className="logo-text-main">Nexus</div>
          <div className="logo-text-sub">
            <span className="logo-line">
              <span className="logo-dot"></span>
              EDUCATION
              <span className="logo-dot"></span>
            </span>
          </div>
        </div>
      )}
    </div>
  )
}

export default Logo

