<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <h1>智能时间管理优化系统</h1>
        <div class="header-actions">
          <el-button type="text" @click="toggleTheme">
            <el-icon><Sunny v-if="isDark" /><Moon v-else /></el-icon>
          </el-button>
        </div>
      </div>
    </el-header>
    <el-container class="main-container">
      <el-aside width="200px" class="app-aside">
        <el-menu
          router
          :default-active="$route.path"
          class="el-menu-vertical"
          :collapse="isCollapse"
        >
          <el-menu-item index="/">
            <el-icon><Menu /></el-icon>
            <template #title>仪表盘</template>
          </el-menu-item>
          <el-menu-item index="/tasks">
            <el-icon><List /></el-icon>
            <template #title>任务管理</template>
          </el-menu-item>
          <el-menu-item index="/calendar">
            <el-icon><Calendar /></el-icon>
            <template #title>月度视图</template>
          </el-menu-item>
          <el-menu-item index="/settings">
            <el-icon><Setting /></el-icon>
            <template #title>系统设置</template>
          </el-menu-item>
        </el-menu>
        <div class="collapse-button" @click="toggleCollapse">
          <el-icon><Expand v-if="isCollapse" /><Fold v-else /></el-icon>
        </div>
      </el-aside>
      <el-main class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { Menu, List, Calendar, Setting, Expand, Fold, Sunny, Moon } from '@element-plus/icons-vue'

const isCollapse = ref(false)
const isDark = ref(false)

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark')
}
</script>

<style>
:root {
  --primary-color: #409EFF;
  --success-color: #67C23A;
  --warning-color: #E6A23C;
  --danger-color: #F56C6C;
  --info-color: #909399;
  --text-color: #303133;
  --border-color: #DCDFE6;
  --background-color: #F5F7FA;
}

.dark {
  --primary-color: #79BBFF;
  --success-color: #85CE61;
  --warning-color: #EBB563;
  --danger-color: #F78989;
  --info-color: #A6A9AD;
  --text-color: #E4E7ED;
  --border-color: #4C4D4F;
  --background-color: #1F1F1F;
}

.app-container {
  height: 100vh;
}

.app-header {
  background-color: var(--primary-color);
  color: white;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  font-size: 20px;
}

.app-aside {
  background-color: var(--background-color);
  border-right: 1px solid var(--border-color);
  transition: width 0.3s;
  position: relative;
}

.el-menu-vertical {
  height: calc(100vh - 60px);
  border-right: none;
}

.collapse-button {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  cursor: pointer;
  padding: 10px;
  border-radius: 4px;
  background-color: var(--background-color);
  border: 1px solid var(--border-color);
}

.app-main {
  background-color: var(--background-color);
  padding: 20px;
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 