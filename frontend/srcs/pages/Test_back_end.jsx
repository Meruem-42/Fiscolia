import { useState } from 'react'
import { Link } from 'react-router-dom'

function Test_back_end() {
  const [message, setMessage] = useState("Test back end ...")
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
	<div style={{textAlign: 'center', marginTop: '50px', fontFamily: 'sans-serif' }}>
	  <h1 style={{ color: '#000091', fontFamily: 'cursive'}}>FISCOLIA</h1>
	  <div style={{ margin: '20px', padding: '20px', border: '4px solid #830404(70%)', borderRadius: '8px' }}>
		<p style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{message}</p>
	  </div>
	  <button 
		onClick={callApi}
		disabled={loading}
		style={{
		  padding: '10px 20px',
		  fontSize: '16px',
		  cursor: loading ? 'not-allowed' : 'pointer',
		  backgroundColor: '#000091',
		  color: 'white',
		  border: 'none',
		  borderRadius: '4px'
		}}
	  >
		{loading ? 'Appel en cours...' : 'Dis Salut au Backend'}
	  </button>
	<div>

	<Link to="/">
		<button>HOMEPAGE</button>
	</Link>
	</div>
	</div>
  )
}

export default Test_back_end