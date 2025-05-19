import { defineConfig } from 'vite'
import path from 'path'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Remove server configuration to use default port 5173
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')  // Ensure this path is correct
    }
  },
  server: {
    port: 5173,  // Use default port
    strictPort: true,  // Throw error if port is in use
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('proxy error', err);
          });
        }
      }
    }
  }
}) 