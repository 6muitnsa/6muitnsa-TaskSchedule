<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <el-container>
        <el-aside width="200px">
          <el-menu
            :router="true"
            :default-active="route.path"
            class="el-menu-vertical"
          >
            <el-menu-item index="/dashboard">
              <el-icon><DataLine /></el-icon>
              <span>仪表盘</span>
            </el-menu-item>
            <el-menu-item index="/tasks">
              <el-icon><List /></el-icon>
              <span>任务列表</span>
            </el-menu-item>
            <el-menu-item index="/tasks/manage">
              <el-icon><Operation /></el-icon>
              <span>任务管理</span>
            </el-menu-item>
            <el-menu-item index="/pomodoro">
              <el-icon><Timer /></el-icon>
              <span>番茄钟</span>
            </el-menu-item>
            <el-menu-item index="/settings">
              <el-icon><Setting /></el-icon>
              <span>设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <el-header>
            <div class="header-content">
              <h2>任务计划</h2>
              <div class="header-actions">
                <el-button type="primary" @click="createTask">
                  <el-icon><Plus /></el-icon>
                  新建任务
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
import { useRoute, useRouter } from 'vue-router'
import { DataLine, List, Timer, Setting, Plus, Operation } from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const route = useRoute()
const router = useRouter()

const createTask = () => {
  router.push('/tasks/create')
}
</script>

<style lang="scss" scoped>
.app-container {
  height: 100vh;
  
  .el-container {
    height: 100%;
  }
  
  .el-aside {
    background-color: #304156;
    
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
    border-bottom: 1px solid #e6e6e6;
    padding: 0 20px;
    
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
</style> 