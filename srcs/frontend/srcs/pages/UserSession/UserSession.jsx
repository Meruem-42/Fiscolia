import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { handleLogout } from '../Utils/Logout.jsx';
import { ChatBotEmoji } from './ChatBotEmoji.jsx';
import './UserSession.css'

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
     
        <SessionHeader user={ user } />
        <div className="session-body">
          <div className="left-block">
            <h1 className="session-h1">Mes informations personnelles</h1>
            <h2 className="session-h2">Mon identite</h2>
            <div className="session-separator"></div>
            <div className="key-value">
              <p class="session-p">Prénom</p>
              <p class="session-p value">{user.firstname}</p>
            </div>
            <div className="key-value">
              <p class="session-p">Nom</p>
              <p class="session-p value">{user.lastname}</p>
            </div>
            <div className="key-value">
              <p class="session-p">Date de naissance</p>
              <p class="session-p value">non spécifié</p>
            </div>
            <div className="key-value">
              <p class="session-p">Lieu de naissance</p>
              <p class="session-p value">non spécifié</p>
            </div>

            <h2 className="session-h2">Mon mot de passe</h2>
            <div className="session-separator"></div>
            <p class="session-p">*********</p>

            <h2 className="session-h2">Mes moyens de contact</h2>
            <div className="session-separator"></div>
            <p class="session-p">Adresse électronique: {user.email}</p>

            <div className="session-button-position">
              <button className="auth-button">Modifier</button>
            </div>
          </div>
          <details className="right-block" open>
              <summary className="session-h2">La description de l'utilisateur</summary>
              <br />
              <p>Information1</p>
              <p>Information2</p>
              <p>Information3</p>
              <p>Information4</p>
          </details>
          <div className="chat-box-container">
            <div>
              <ChatBotEmoji />
            </div>
            <div className="text-under-emoji">
              Besoin d'aide?
            </div>
          </div>
        </div>
    </div>
  );
}

export function SessionHeader ({ user }) {

  return (
    <div className="session-header">
      <p className="session-header-text-bold">{user.firstname} {user.lastname}</p>
      <p className="session-header-text">Numero fiscal: 9334012429019</p>
    </div>
  )
}