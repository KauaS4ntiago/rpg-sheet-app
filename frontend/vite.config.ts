import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    allowedHosts: true,
    proxy: {
      '/auth': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/users': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/characters': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/attributes': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/skills': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      },
      '/abilities': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
        }
      }
})