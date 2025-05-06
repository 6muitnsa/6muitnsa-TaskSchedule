<template>
  <el-container class="app-wrapper">
    <el-aside width="200px">
      <el-menu
        :router="true"
        class="el-menu-vertical"
        :default-active="route.path"
      >
        <el-menu-item index="/">
          <el-icon><Calendar /></el-icon>
          <span>任务列表</span>
        </el-menu-item>
        <el-menu-item index="/schedule">
          <el-icon><Timer /></el-icon>
          <span>任务调度</span>
        </el-menu-item>
        <el-menu-item index="/statistics">
          <el-icon><DataLine /></el-icon>
          <span>任务统计</span>
        </el-menu-item>
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header height="60px">
        <div class="header-title">智能时间管理优化系统</div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { Calendar, Timer, DataLine, Setting } from '@element-plus/icons-vue'

const route = useRoute()
</script>

<style lang="scss">
.app-wrapper {
  height: 100vh;
  
  .el-aside {
    background-color: #304156;
    
    .el-menu {
      border-right: none;
      background-color: transparent;
    }
  }
  
  .el-header {
    background-color: #fff;
    border-bottom: 1px solid #dcdfe6;
    display: flex;
    align-items: center;
    
    .header-title {
      font-size: 20px;
      font-weight: bold;
      color: #303133;
    }
  }
  
  .el-main {
    background-color: #f0f2f5;
    padding: 20px;
  }
}
</style> 