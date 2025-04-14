<template>
  <div class="app">
    <el-container>
      <el-header>
        <h1>智能时间管理优化系统</h1>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
// import TaskList from './components/TaskList.vue'
</script>

<style>
.app {
  /* font-family: Arial, sans-serif; */
  height: 100vh;
}

.el-header {
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.el-main {
  padding: 20px;
}
</style> 