import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import App from './App.vue'
import router from './router'
import './styles/global.scss'
import './styles/main.scss'

console.log('Vue 应用开始初始化')

const app = createApp(App)

console.log('Vue 应用实例已创建')

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 注册 Pinia
const pinia = createPinia()
app.use(pinia)

// 注册 Element Plus
app.use(ElementPlus, {
  locale: zhCn,
  size: 'default'
})

// 注册路由
app.use(router)

console.log('Vue 插件已加载')

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('全局错误:', err)
  console.error('错误信息:', info)
}

// 挂载应用
app.mount('#app')

console.log('Vue 应用已挂载') 