<template>
  <div class="schedule-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>任务调度</h2>
          <el-select v-model="selectedAlgorithm" placeholder="选择调度算法">
            <el-option label="轮转调度" value="round-robin" />
            <el-option label="最短作业优先" value="shortest-job-first" />
            <el-option label="先到先服务" value="first-come-first-serve" />
          </el-select>
        </div>
      </template>

      <el-timeline>
        <el-timeline-item
          v-for="(task, index) in scheduledTasks"
          :key="index"
          :timestamp="formatTime(task.startTime)"
          :type="getTimelineItemType(task)"
        >
          <el-card>
            <h4>{{ task.name }}</h4>
            <p>预计时长: {{ task.estimatedTime }}分钟</p>
            <p>优先级: {{ task.priority }}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>

      <div class="evaluation-section">
        <h3>调度评估</h3>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="总时间">
            {{ evaluation.totalTime }}分钟
          </el-descriptions-item>
          <el-descriptions-item label="平均等待时间">
            {{ evaluation.averageWaitingTime }}分钟
          </el-descriptions-item>
          <el-descriptions-item label="平均周转时间">
            {{ evaluation.averageTurnaroundTime }}分钟
          </el-descriptions-item>
          <el-descriptions-item label="调度效率">
            {{ (evaluation.efficiency * 100).toFixed(2) }}%
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { schedulerService } from '../services/schedulerService'
import { ElMessage } from 'element-plus'

interface ScheduledTask {
  id: string
  name: string
  startTime: Date
  endTime: Date
  estimatedTime: number
  priority: number
}

interface ScheduleEvaluation {
  totalTime: number
  averageWaitingTime: number
  averageTurnaroundTime: number
  efficiency: number
}

const selectedAlgorithm = ref('round-robin')
const scheduledTasks = ref<ScheduledTask[]>([])
const evaluation = ref<ScheduleEvaluation>({
  totalTime: 0,
  averageWaitingTime: 0,
  averageTurnaroundTime: 0,
  efficiency: 0
})

const formatTime = (date: Date) => {
  return new Date(date).toLocaleTimeString()
}

const getTimelineItemType = (task: ScheduledTask) => {
  const now = new Date()
  const startTime = new Date(task.startTime)
  const endTime = new Date(task.endTime)

  if (now < startTime) return 'info'
  if (now >= startTime && now <= endTime) return 'primary'
  return 'success'
}

const loadSchedule = async () => {
  try {
    const result = await schedulerService.scheduleTasks(selectedAlgorithm.value)
    scheduledTasks.value = result.scheduledTasks
    evaluation.value = result.evaluation
  } catch (error) {
    console.error('加载调度结果失败:', error)
    ElMessage.error('加载调度结果失败')
  }
}

watch(selectedAlgorithm, () => {
  loadSchedule()
})

onMounted(() => {
  loadSchedule()
})
</script>

<style scoped>
.schedule-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.evaluation-section {
  margin-top: 20px;
}

.evaluation-section h3 {
  margin-bottom: 15px;
}
</style> 