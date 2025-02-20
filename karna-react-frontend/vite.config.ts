import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: `http://${process.env.HOST || 'localhost'}:8000`,
        changeOrigin: true,
      }
    },
    host: true, // Listen on all local IPs
    port: 5173
  }
})
