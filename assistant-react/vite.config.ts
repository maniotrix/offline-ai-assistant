import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Update target to match Flask server port
        changeOrigin: true,
        rewrite: (path) => path // No need to strip "/api" if Flask routes are defined with it
      }
    }
  }
});
