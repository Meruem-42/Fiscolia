import React from 'react';
import {
  BrowserRouter, Routes, Route,
} from 'react-router-dom';
import Home from './pages/Homepage';
import Test_back_end from './pages/Test_back_end';
import Login from './pages/Login';
import Register from './pages/Register';
import Chatbot from './pages/Chatbot';

function App() {
	return (
	  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/backend" element={<Test_back_end />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
	  <Route path="/chatbot" element={<Chatbot />} />
    </Routes>
  </BrowserRouter>
	)
}


export default App;
