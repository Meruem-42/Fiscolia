import React from 'react';
import {
  BrowserRouter, Routes, Route,
} from 'react-router-dom';
import Home from './pages/Homepage/Homepage.jsx';
import Test_back_end from './pages/Test_back_end';
import Login from './pages/Login/Login.jsx';
import Register from './pages/Register/Register.jsx';
import Upload from './pages/Upload/Upload.jsx';
import UserSession from './pages/UserSession/UserSession.jsx';

function App() {
	return (
	  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/backend" element={<Test_back_end />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
	  <Route path="/upload" element={<Upload />} />
	  <Route path="/session" element={<UserSession />} />
    </Routes>
  </BrowserRouter>
	)
}


export default App;
