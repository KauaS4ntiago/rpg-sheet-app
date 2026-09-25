import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter } from 'react-router-dom'
import { NotificationProvider } from './contexts/NotificationContext.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <NotificationProvider>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </NotificationProvider>
  </StrictMode>,
)
