import { Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Welcome from './pages/welcome/Welcome'
import ForgotPassword from './pages/forgot_password/ForgotPassword'
import Login from './pages/auth/login/Login'
import Register from './pages/auth/register/Register'
import './App.css'
import Characters from './pages/characters/Characters'
import Layout from './layouts/Layout'
import Profile from './pages/profile/Profile'

function App() {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Welcome />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route element={<Layout />}>
          <Route path="/characters" element={<Characters />} />
          <Route path="/campaigns" element={<h1>Campaigns Page</h1>} />
          <Route path="/master" element={<h1>Master Page</h1>} />
          <Route path="/profile" element={<Profile />} /> 
        </Route>
        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>
    </AnimatePresence>
  )
}

export default App