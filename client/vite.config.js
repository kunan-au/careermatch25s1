import { defineConfig } from 'vite'
import path from 'path'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // 删除 server 配置，让它使用默认的 5173 端口
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')  // 确保这个路径正确
    }
  },
  server: {
    port: 5173,  // 改回默认端口
    strictPort: true,  // 如果端口被占用就报错
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