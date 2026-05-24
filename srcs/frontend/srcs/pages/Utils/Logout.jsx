import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';

export const handleLogout = async ( navigate, setIsAuthenticated ) => {
    try {
      const response = await fetch("/api/auth-logout", {
        method: "POST",
        credentials: "include",
      });
      console.log("Logout response:", response.status);
    } catch (err) {
      console.error("Logout error:", err);
    } finally {
      setIsAuthenticated(false);
      navigate("/");
    }
  };

export default handleLogout;