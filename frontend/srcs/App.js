import { useState } from 'react'
import './App.css'

function App() {
  const [message, setMessage] = useState("En attente du clic...")
  const [loading, setLoading] = useState(false)

  const callApi = async () => {
    setLoading(true)
    try {
      // Note: On utilise /api/ car Nginx fera la redirection
      const response = await fetch('/api/auth')
      const data = await response.json()
      setMessage(data.message)
      console.error(message)
    } catch (error) {
      setMessage("Erreur : Le backend ne répond pas (encore) !")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ textAlign: 'center', marginTop: '50px', fontFamily: 'sans-serif' }}>
      <h1>Test Docker Major 🚀</h1>
      <div style={{ margin: '20px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
        <p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{message}</p>
      </div>
      <button 
        onClick={callApi}
        disabled={loading}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          cursor: loading ? 'not-allowed' : 'pointer',
          backgroundColor: '#646cff',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}
      >
        {loading ? 'Appel en cours...' : 'Dis Salut au Backend'}
      </button>
    </div>
  )
}

export default App