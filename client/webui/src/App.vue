<template>
  <el-container class="app-container">
    <el-header>
      <h1>TaskSchedule</h1>
      <el-menu mode="horizontal" :router="true">
        <el-menu-item index="/">仪表盘</el-menu-item>
        <el-menu-item index="/tasks">任务管理</el-menu-item>
        <el-menu-item index="/pomodoro">番茄钟</el-menu-item>
        <el-menu-item index="/schedule">日程安排</el-menu-item>
        <el-menu-item index="/sync">同步</el-menu-item>
        <el-menu-item index="/settings">设置</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="scss">
.app-container {
  height: 100vh;
  
  .el-header {
    background-color: #409EFF;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    
    h1 {
      margin: 0;
    }
  }
  
  .el-main {
    padding: 20px;
  }
}
</style> 