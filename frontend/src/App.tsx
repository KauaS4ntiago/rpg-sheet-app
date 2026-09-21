import { Route, Routes } from 'react-router'
import './App.css'
import Welcome from './pages/welcome/Welcome'
import Login from './pages/auth/login/Login'
import Register from './pages/auth/register/Register'

function App() {

  return (
    <Routes>
      <Route path="/" element={<Welcome />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    </Routes>
  )
}

export default App
