<template>
  <div class="scheduler-view">
    <el-card class="scheduler-card">
      <template #header>
        <div class="card-header">
          <span>任务调度控制台</span>
        </div>
      </template>
      
      <div class="control-panel">
        <el-button type="primary" @click="runScheduler" :loading="running">
          运行调度
        </el-button>
        <el-button type="info" @click="refreshResults">
          刷新结果
        </el-button>
      </div>

      <div class="results-panel">
        <h3>调度结果</h3>
        <el-table
          v-loading="loading"
          :data="schedulerResults"
          style="width: 100%"
          border
        >
          <el-table-column prop="timestamp" label="执行时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.timestamp) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
                {{ scope.row.status === 'success' ? '成功' : '失败' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="详细信息" />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '../api'

const running = ref(false)
const loading = ref(false)
const schedulerResults = ref([])

const runScheduler = async () => {
  try {
    running.value = true
    const response = await api.post('/api/scheduler/run')
    if (response.data.code === 200) {
      ElMessage.success('调度任务已启动')
      await refreshResults()
    } else {
      ElMessage.error(response.data.message || '启动调度任务失败')
    }
  } catch (error) {
    ElMessage.error('启动调度任务失败：' + (error.response?.data?.message || error.message))
  } finally {
    running.value = false
  }
}

const refreshResults = async () => {
  try {
    loading.value = true
    const response = await api.get('/api/scheduler/results')
    if (response.data.code === 200) {
      schedulerResults.value = response.data.data
    } else {
      ElMessage.error(response.data.message || '获取调度结果失败')
      schedulerResults.value = []
    }
  } catch (error) {
    ElMessage.error('获取调度结果失败：' + (error.response?.data?.message || error.message))
    schedulerResults.value = []
  } finally {
    loading.value = false
  }
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

onMounted(() => {
  refreshResults()
})
</script>

<style scoped>
.scheduler-view {
  padding: 20px;
}

.scheduler-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.control-panel {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.results-panel {
  margin-top: 20px;
}

h3 {
  margin-bottom: 15px;
  color: #606266;
}
</style> 