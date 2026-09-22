import { Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import PageTransition from './components/PageTransition'
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
        <Route path="/" element={<PageTransition><Welcome /></PageTransition>} />
        <Route path="/login" element={<PageTransition><Login /></PageTransition>} />
        <Route path="/register" element={<PageTransition><Register /></PageTransition>} />
        <Route path="/forgot-password" element={<PageTransition><ForgotPassword /></PageTransition>}
      </Routes>
    </AnimatePresence>
  )
}

export default App