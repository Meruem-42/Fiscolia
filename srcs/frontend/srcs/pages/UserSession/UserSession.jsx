import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

export default function UserSession() {
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

  const handleLogout = async () => {
    try {
      const response = await fetch("/api/auth-logout", {
        method: "POST",
        credentials: "include",
      });
      console.log("Logout response:", response.status);
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      navigate("/");
    }
  };

  const handleUpload = () => {
    navigate("/upload");
  };

  if (loading) {
    return <p style={{ textAlign: "center", marginTop: "2rem" }}>Loading...</p>;
  }

  // Only show if user is authenticated
  if (!user) {
    return null; // Will redirect via useEffect
  }

  return (
    <div style={{ textAlign: "center", marginTop: "3rem" }}>
      <h1 style={{ color: "#000091" }}>Welcome {user.email}</h1>
      <p style={{ marginBottom: "2rem", fontSize: "1.1rem" }}>You are authenticated ✓</p>

      <div style={{ display: "flex", justifyContent: "center", gap: "1.5rem", marginBottom: "2rem" }}>
        <button
          type="button"
          onClick={handleUpload}
          style={{
            padding: "0.75rem 1.5rem",
            fontSize: "1rem",
            backgroundColor: "#000091",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Upload File
        </button>

        <button
          type="button"
          onClick={handleLogout}
          style={{
            padding: "0.75rem 1.5rem",
            fontSize: "1rem",
            backgroundColor: "#dc3545",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
}

