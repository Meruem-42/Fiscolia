import { Link, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import '../../index.css'

function RegisterSuccess() {
 
 return (
    <div className="main-body-style">
     
        <h1 className="auth-page-title">Inscription reussie</h1>
        <div className="auth-field-container">
          <p className="auth-field-name">Vous pouvez vous connecter maintenant</p>
        </div>
        <div>
            <Link to="/login">
              <button className="auth-button" type="submit">Se connecter</button>
            </Link>
        </div>
     
      <div>
        <Link to="/">
          <button className="auth-button">Retourner a la page d'accueil</button>
        </Link>
      </div>
    </div>
  )
}

export default RegisterSuccess