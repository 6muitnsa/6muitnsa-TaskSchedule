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
        rewrite: (path) => {
          const newPath = path.replace(/^(\/api)+/, '/api')
          console.log('代理请求:', {
            originalPath: path,
            newPath: newPath,
            target: `http://${config.app.host}:${config.app.port}`,
            config: config
          })
          return newPath
        },
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.error('代理错误:', err)
            console.error('请求信息:', {
              url: req.url,
              method: req.method,
              headers: req.headers
            })
          })
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('发送代理请求:', {
              method: req.method,
              url: req.url,
              headers: req.headers,
              body: req.body
            })
          })
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('收到代理响应:', {
              statusCode: proxyRes.statusCode,
              url: req.url,
              headers: proxyRes.headers
            })
          })
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