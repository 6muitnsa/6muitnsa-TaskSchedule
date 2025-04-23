<template>
  <div class="settings">
    <h2>系统设置</h2>
    
    <el-form :model="settings" label-width="120px">
      <el-form-item label="调度算法">
        <el-select v-model="settings.scheduler">
          <el-option label="先来先服务" value="fcfs" />
          <el-option label="短作业优先" value="sjf" />
          <el-option label="轮转调度" value="rr" />
        </el-select>
      </el-form-item>

      <el-form-item label="时间粒度(分钟)">
        <el-input-number v-model="settings.timeGranularity" :min="15" :max="60" :step="15" />
      </el-form-item>

      <el-form-item label="默认任务时间">
        <el-input-number v-model="settings.defaultTaskTime" :min="15" :max="480" :step="15" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="saveSettings">保存设置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

const settings = reactive({
  scheduler: 'fcfs',
  timeGranularity: 30,
  defaultTaskTime: 60
})

const saveSettings = () => {
  // TODO: 调用API保存设置
  ElMessage.success('设置已保存')
}
</script>

<style scoped>
.settings {
  padding: 20px;
}
</style> 