import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { handleLogout } from '../Utils/Logout.jsx';
import { ChatBotEmoji } from './ChatBotEmoji.jsx';

export default function UserSession({ setIsAuthenticated }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch user info if authenticated
    const fetchUser = async () => {
      try {
        const response = await fetch("/api/me", {
          method: "GET",
          credentials: "include",
          headers: { 
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache'
          }
        });

        console.log("GET /api/me status:", response.status);

        // Handle 304 Not Modified or other non-200/non-401 responses
        if (response.status === 304) {
          // 304 means cached, try again without cache
          console.log("Got 304, retrying without cache...");
          const retryResponse = await fetch("/api/me", {
            method: "GET",
            credentials: "include",
            headers: { 
              'Content-Type': 'application/json',
              'Cache-Control': 'no-cache, no-store, must-revalidate'
            }
          });
          if (retryResponse.ok) {
            const userData = await retryResponse.json();
            console.log("Retry user data fetched:", userData);
            setUser(userData);
            setLoading(false);
            return;
          }
        }

        if (!response.ok) {
          console.error("Not authenticated, redirecting to login. Status:", response.status);
          setLoading(false);
          navigate("/login");
          return;
        }

        const responseText = await response.text();
        console.log("Response text:", responseText);
        
        const userData = JSON.parse(responseText);
        console.log("Parsed user data:", userData);
        setUser(userData);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching user:", err);
        setLoading(false);
        navigate("/login");
      }
    };

    fetchUser();
  }, [navigate]);



  const handleUpload = () => {
    navigate("/upload");
  };

  if (loading) {
    return <p className="auth-field-name">Loading...</p>;
  }

  // Only show if user is authenticated
  if (!user) {
    return null; // Will redirect via useEffect
  }

  return (
    <div className="main-body-style">
      <h1 className="auth-page-title">Bienvenue, {user.firstname}</h1>
      <p className="auth-field-name">Vous etes connectes ✓</p>
      <div>
        <button className="auth-button" type="button" onClick={ () => handleLogout(navigate, setIsAuthenticated) }>
          Se deconnecter
        </button>
      </div>
      <div className="chat-box-container">
        <div>
          <ChatBotEmoji />
        </div>
        <div className="text-under-emoji">
          Besoin d'aide?
        </div>
      </div>
    </div>
  );
}