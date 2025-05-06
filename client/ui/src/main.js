import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router'
import './styles/global.scss'
import './styles/main.scss'

const app = createApp(App)

// 注册 Pinia
const pinia = createPinia()
app.use(pinia)

// 注册 Element Plus
app.use(ElementPlus, {
  locale: zhCn
})

// 注册路由
app.use(router)

// 挂载应用
app.mount('#app') 