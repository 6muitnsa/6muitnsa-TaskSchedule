<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <!-- 移动端菜单按钮 -->
      <div class="mobile-menu-button show-on-mobile" @click="toggleMobileMenu">
        <el-icon><Menu /></el-icon>
      </div>
      
      <el-container>
        <!-- 侧边栏 -->
        <el-aside :width="isMobile ? '100%' : '200px'" :class="{ 'mobile-aside': isMobile, 'show': showMobileMenu }">
          <div class="logo">
            <h1>任务计划</h1>
          </div>
          <el-menu
            :router="true"
            :default-active="route.path"
            class="el-menu-vertical"
            background-color="#304156"
            text-color="#bfcbd9"
            active-text-color="#409EFF"
            @select="handleMenuSelect"
          >
            <el-menu-item index="/">
              <el-icon><DataLine /></el-icon>
              <span>仪表盘</span>
            </el-menu-item>
            <el-menu-item index="/tasks/list">
              <el-icon><List /></el-icon>
              <span>任务列表</span>
            </el-menu-item>
            <el-menu-item index="/tasks/manage">
              <el-icon><Operation /></el-icon>
              <span>任务管理</span>
            </el-menu-item>
            <el-menu-item index="/scheduler">
              <el-icon><Monitor /></el-icon>
              <span>调度控制台</span>
            </el-menu-item>
            <el-menu-item index="/pomodoro">
              <el-icon><Timer /></el-icon>
              <span>番茄钟</span>
            </el-menu-item>
            <el-menu-item index="/statistics">
              <el-icon><TrendCharts /></el-icon>
              <span>统计分析</span>
            </el-menu-item>
            <el-sub-menu index="/settings">
              <template #title>
                <el-icon><Setting /></el-icon>
                <span>设置</span>
              </template>
              <el-menu-item index="/settings/general">基本设置</el-menu-item>
              <el-menu-item index="/settings/scheduler">调度设置</el-menu-item>
              <el-menu-item index="/settings/priority">优先级设置</el-menu-item>
              <el-menu-item index="/settings/time">时间设置</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-aside>

        <el-container>
          <el-header>
            <div class="header-content">
              <h2>{{ route.meta.title || '任务计划' }}</h2>
              <div class="header-actions">
                <el-button type="primary" @click="createTask">
                  <el-icon><Plus /></el-icon>
                  <span class="hide-on-mobile">新建任务</span>
                </el-button>
              </div>
            </div>
          </el-header>
          <el-main>
            <router-view v-slot="{ Component }">
              <transition name="fade" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </el-main>
        </el-container>
      </el-container>
    </div>
  </el-config-provider>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { ROUTE_PATHS } from '@/router'
import {
  DataLine,
  List,
  Operation,
  Monitor,
  Timer,
  Setting,
  Plus,
  TrendCharts,
  Menu
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 移动端相关状态
const isMobile = ref(false)
const showMobileMenu = ref(false)

// 检查是否为移动设备
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

// 切换移动端菜单
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

// 处理菜单选择
const handleMenuSelect = () => {
  if (isMobile.value) {
    showMobileMenu.value = false
  }
}

// 创建任务
const createTask = () => {
  router.push({ name: 'TaskCreate' })
}

// 监听窗口大小变化
onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<style lang="scss">
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

#app {
  height: 100%;
}

.app-container {
  height: 100vh;
  
  .el-container {
    height: 100%;
  }
  
  // 移动端菜单按钮
  .mobile-menu-button {
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 1000;
    padding: 0.5rem;
    background: #304156;
    color: #fff;
    border-radius: 4px;
    cursor: pointer;
  }
  
  // 移动端侧边栏
  .mobile-aside {
    position: fixed;
    top: 0;
    left: -100%;
    z-index: 999;
    transition: left 0.3s ease;
    
    &.show {
      left: 0;
    }
  }
  
  .el-aside {
    background-color: #304156;
    color: #fff;
    transition: width 0.3s ease;
    
    .logo {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #263445;
      
      h1 {
        color: #fff;
        font-size: 18px;
        margin: 0;
      }
    }
    
    .el-menu {
      border-right: none;
      background-color: transparent;
      
      .el-menu-item {
        color: #bfcbd9;
        
        &:hover, &.is-active {
          color: #409eff;
          background-color: #263445;
        }
        
        .el-icon {
          margin-right: 8px;
        }
      }
    }
  }
  
  .el-header {
    background-color: #fff;
    border-bottom: 1px solid #dcdfe6;
    padding: 0 20px;
    box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
    
    .header-content {
      height: 60px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      
      h2 {
        margin: 0;
        font-size: 20px;
        color: #303133;
      }
      
      .header-actions {
        display: flex;
        gap: 12px;
      }
    }
  }
  
  .el-main {
    background-color: #f0f2f5;
    padding: 20px;
    overflow-y: auto;
  }
}

// 移动端适配
@media screen and (max-width: 768px) {
  .app-container {
    .el-header {
      padding: 0 10px;
      
      .header-content {
        h2 {
          font-size: 16px;
        }
      }
    }
    
    .el-main {
      padding: 10px;
    }
  }
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 滚动条样式
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
  
  &:hover {
    background: #a8a8a8;
  }
}
</style> 