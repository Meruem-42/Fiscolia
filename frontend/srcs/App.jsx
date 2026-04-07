import React from 'react';

import {
  BrowserRouter, Routes, Route,
} from 'react-router-dom';
import Home from './pages/Homepage';
import Test_back_end from './pages/Test_back_end';
import Login from './pages/Login';

function App() {
	return (
	  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/backend" element={<Test_back_end />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  </BrowserRouter>
	)
}





export default App;
