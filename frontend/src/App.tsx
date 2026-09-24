import { Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Welcome from './pages/welcome/Welcome'
import ForgotPassword from './pages/forgot_password/ForgotPassword'
import Login from './pages/auth/login/Login'
import Register from './pages/auth/register/Register'
import './App.css'

function App() {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Welcome />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
      </Routes>
    </AnimatePresence>
  )
}

export default App