import { Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import AuthenticationTransition from './components/AuthenticationTransition'
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
        <Route path="/" element={<AuthenticationTransition><Welcome /></AuthenticationTransition>} />
        <Route path="/login" element={<AuthenticationTransition><Login /></AuthenticationTransition>} />
        <Route path="/register" element={<AuthenticationTransition><Register /></AuthenticationTransition>} />
        <Route path="/forgot-password" element={<AuthenticationTransition><ForgotPassword /></AuthenticationTransition>} />
      </Routes>
    </AnimatePresence>
  )
}

export default App