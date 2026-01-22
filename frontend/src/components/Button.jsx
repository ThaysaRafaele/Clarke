export default function Button({ 
  onClick, 
  children, 
  disabled = false, 
  variant = 'primary' 
}) {
  const styles = {
    primary: {
      padding: '12px 24px',
      backgroundColor: disabled ? '#ccc' : '#00a86b',
      color: 'white',
      border: 'none',
      borderRadius: '8px',
      fontSize: '16px',
      fontWeight: '600',
      cursor: disabled ? 'not-allowed' : 'pointer',
      transition: 'all 0.3s ease',
      opacity: disabled ? 0.6 : 1,
    },
    secondary: {
      padding: '10px 20px',
      backgroundColor: 'transparent',
      color: '#00a86b',
      border: '2px solid #00a86b',
      borderRadius: '8px',
      fontSize: '14px',
      cursor: disabled ? 'not-allowed' : 'pointer',
    }
  }

  return (
    <button 
      onClick={onClick}
      disabled={disabled}
      style={styles[variant]}
      onMouseOver={(e) => {
        if (!disabled && variant === 'primary') {
          e.target.style.backgroundColor = '#008c59'
        }
      }}
      onMouseOut={(e) => {
        if (!disabled && variant === 'primary') {
          e.target.style.backgroundColor = '#00a86b'
        }
      }}
    >
      {children}
    </button>
  )
}