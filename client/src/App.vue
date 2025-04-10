<template>
  <div class="app">
    <el-container>
      <el-header>
        <h1>智能时间管理优化系统</h1>
      </el-header>
      <el-main>
        <TaskList />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import TaskList from './components/TaskList.vue'
</script>

<style>
.app {
  font-family: Arial, sans-serif;
}

.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
}

.el-main {
  padding: 20px;
}
</style> 