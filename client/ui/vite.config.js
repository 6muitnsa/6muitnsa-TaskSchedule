import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import yaml from 'js-yaml'
import fs from 'fs'

// 读取配置文件
const configPath = path.resolve(__dirname, '../config/config.yaml')
const config = yaml.load(fs.readFileSync(configPath, 'utf8'))

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    host: config.frontend.host,
    port: config.frontend.port,
    proxy: {
      '/api': {
        target: `http://${config.app.host}:${config.app.port}`,
        changeOrigin: true,
        secure: false,
        ws: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Sending Request to the Target:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
          });
        }
      },
    },
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '.trycloudflare.com'
    ],
    hmr: {
      protocol: 'ws',
      host: config.frontend.host,
      port: config.frontend.port
    }
  }
}) 