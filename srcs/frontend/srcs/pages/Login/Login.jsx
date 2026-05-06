import { Link, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';


function Login() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const [checkingSession, setCheckingSession] = useState(true);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await fetch('/api/me', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
          },
        });

        if (response.ok) {
          navigate('/session', { replace: true });
          return;
        }
      } catch (error) {
        // Ignore network errors here and keep login form available.
      } finally {
        setCheckingSession(false);
      }
    };

    checkSession();
  }, [navigate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("/api/auth-login", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Important: send cookies
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        setMessage(errorData.detail || "Email or password incorrect");
        return;
      }

      const data = await response.json();
      setMessage(data.message);
      
      // Redirect to UserSession dashboard after successful login
      setTimeout(() => navigate("/session"), 500);
    } catch (error) {
      setMessage("ERROR: " + error.message);
    }
  };

  if (checkingSession) {
    return <p style={{ textAlign: 'center', marginTop: '2rem' }}>Loading...</p>;
  }

  return (
    <div style={{ textAlign: "center", alignContent: "center" }}>
      <h1 style={{ color:"#000091"}}>LOGIN</h1>
      <form onSubmit={handleSubmit}>
        <p>Email</p>
        <input type="text" name="email" value={formData.email} onChange={handleChange} placeholder="Email" />
        <p>Mot de passe</p>
        <input type="password" name="password" value={formData.password} onChange={handleChange} placeholder="Password" />
		<p>{message}</p>
        <button type="submit">Connect</button>
      </form>
      <div>
        <Link to="/">
          <button>Return to the home Page</button>
        </Link>
      </div>
    </div>
  );
}

export default Login