import React from 'react';
import { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Header, Footer } from './Components_of_site.jsx'
import './index.css';
import Home from './pages/Homepage/Homepage.jsx';
import Test_back_end from './pages/Test_back_end';
import Login from './pages/Login/Login.jsx';
import Register from './pages/Register/Register.jsx';
import RegisterSuccess from './pages/Register/RegisterSuccess.jsx';
import Upload from './pages/Upload/Upload.jsx';
import UserSession from './pages/UserSession/UserSession.jsx';
import PrivacyPolicy from './pages/TermsAndPolicies/PrivacyPolicy.jsx'
import TermsOfService from './pages/TermsAndPolicies/TermsOfService.jsx'

function App() {

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  useEffect(() => {
    fetch("/api/me", {
        credentials: "include"
    })
    .then(res => {
        if (res.ok) {
            setIsAuthenticated(true);
        }
    });
  }, []);

	return (
	  <BrowserRouter>
		  <div className="page">

        <Header isAuthenticated={isAuthenticated}/>

        <div className="default-background">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/backend" element={<Test_back_end />} />
            <Route path="/login" element={<Login
              setIsAuthenticated={setIsAuthenticated}
            />} />
            <Route path="/register" element={<Register />} />
  	        <Route path="/upload" element={<Upload />} />
  	        <Route path="/session" element={<UserSession />} />
            <Route path="/privacy_policy" element={<PrivacyPolicy />} />
            <Route path="/terms_of_service" element={<TermsOfService />} />
            <Route path="/register-success" element={<RegisterSuccess />} />
          </Routes>
        </div>

        <Footer />
        
      </div>
   </BrowserRouter>
	)

}

export default App;
