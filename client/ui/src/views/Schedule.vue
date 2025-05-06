<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">任务调度</div>
    </div>

    <div class="schedule-toolbar">
      <el-form :inline="true" :model="scheduleForm">
        <el-form-item label="调度算法">
          <el-select v-model="scheduleForm.algorithm" placeholder="请选择调度算法">
            <el-option label="先来先服务" value="FCFS" />
            <el-option label="短作业优先" value="SJF" />
            <el-option label="优先级调度" value="Priority" />
            <el-option label="轮转调度" value="RR" />
            <el-option label="自定义算法" value="custom">
              <template #default>
                <div class="custom-algorithm-option">
                  <span>自定义算法</span>
                  <el-radio-group v-model="scheduleForm.customAlgorithmType" size="small">
                    <el-radio label="file">文件上传</el-radio>
                    <el-radio label="code">代码输入</el-radio>
                  </el-radio-group>
                </div>
              </template>
            </el-option>
            <el-option label="AI调度" value="ai">
              <template #default>
                <div class="ai-algorithm-option">
                  <span>AI调度</span>
                  <el-tooltip content="云端功能，需联网" placement="top">
                    <el-icon><InfoFilled /></el-icon>
                  </el-tooltip>
                </div>
              </template>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="任务密度">
          <el-radio-group v-model="scheduleForm.density">
            <el-radio label="none">无偏好</el-radio>
            <el-radio label="dense">偏好紧密</el-radio>
            <el-radio label="sparse">偏好稀疏</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="scheduleForm.density === 'dense'">
          <el-radio-group v-model="scheduleForm.densePreference">
            <el-radio label="early">尽早完成</el-radio>
            <el-radio label="late">最迟完成</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="scheduleForm.density === 'sparse'">
          <el-checkbox v-model="scheduleForm.sliceLongTasks">单次长时间任务切片</el-checkbox>
          <el-input-number
            v-if="scheduleForm.sliceLongTasks"
            v-model="scheduleForm.sliceDuration"
            :min="15"
            :max="120"
            :step="5"
            placeholder="切片时长"
          />
          <span class="unit">分钟</span>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="scheduleForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :shortcuts="dateShortcuts"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSchedule" :loading="loading">
            {{ loading ? '调度中...' : '开始调度' }}
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="schedule-content">
      <el-row :gutter="20">
        <el-col :span="16">
          <div class="schedule-timeline">
            <div class="timeline-header">
              <div class="time-slots">
                <div v-for="hour in 24" :key="hour" class="time-slot">
                  {{ hour - 1 }}:00
                </div>
              </div>
            </div>
            <div class="timeline-body">
              <div v-for="day in scheduleDays" :key="day.date" class="timeline-day">
                <div class="day-header">{{ day.label }}</div>
                <div class="day-content">
                  <div
                    v-for="task in day.tasks"
                    :key="task.id"
                    class="task-block"
                    :style="getTaskStyle(task)"
                    :title="getTaskTooltip(task)"
                    @click="handleTaskClick(task)"
                  >
                    <el-tooltip
                      :content="getTaskTooltip(task)"
                      placement="top"
                      :show-after="500"
                    >
                      <div class="task-content">
                        <span class="task-title">{{ task.title }}</span>
                        <span class="task-time">{{ formatTaskTime(task) }}</span>
                      </div>
                    </el-tooltip>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="schedule-stats">
            <el-card class="stats-card">
              <template #header>
                <div class="card-header">
                  <span>调度统计</span>
                  <el-button type="text" @click="refreshStats">
                    <el-icon><Refresh /></el-icon>
                  </el-button>
                </div>
              </template>
              <div class="stats-content">
                <div class="stat-item">
                  <span class="label">总任务数：</span>
                  <span class="value">{{ stats.totalTasks }}</span>
                </div>
                <div class="stat-item">
                  <span class="label">已完成：</span>
                  <span class="value">{{ stats.completedTasks }}</span>
                </div>
                <div class="stat-item">
                  <span class="label">待调度：</span>
                  <span class="value">{{ stats.pendingTasks }}</span>
                </div>
                <div class="stat-item">
                  <span class="label">平均等待时间：</span>
                  <span class="value">{{ stats.avgWaitTime }}分钟</span>
                </div>
              </div>
            </el-card>

            <el-card class="stats-card">
              <template #header>
                <div class="card-header">
                  <span>调度日志</span>
                  <el-button type="text" @click="clearLogs">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
              </template>
              <div class="log-content" ref="logContent">
                <div v-for="(log, index) in scheduleLogs" :key="index" class="log-item">
                  <span class="log-time">{{ formatLogTime(log.time) }}</span>
                  <span class="log-message">{{ log.message }}</span>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 任务详情对话框 -->
    <el-dialog
      v-model="taskDialogVisible"
      :title="selectedTask?.title"
      width="500px"
    >
      <div v-if="selectedTask" class="task-detail">
        <div class="detail-item">
          <span class="label">开始时间：</span>
          <span class="value">{{ formatDateTime(selectedTask.start_time) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">结束时间：</span>
          <span class="value">{{ selectedTask.isUnlimited ? '无时间限制' : formatDateTime(selectedTask.end_time) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">优先级：</span>
          <span class="value">{{ selectedTask.priority }}</span>
        </div>
        <div class="detail-item">
          <span class="label">状态：</span>
          <el-tag :type="getStatusType(selectedTask.status)">
            {{ getStatusLabel(selectedTask.status) }}
          </el-tag>
        </div>
        <div class="detail-item" v-if="selectedTask.isUnlimited">
          <span class="label">完成次数：</span>
          <span class="value">{{ selectedTask.completionCount }}/{{ selectedTask.requiredCount }}</span>
        </div>
        <div class="detail-item">
          <span class="label">描述：</span>
          <span class="value">{{ selectedTask.description || '无' }}</span>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="taskDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleTaskEdit">编辑</el-button>
          <el-button type="success" @click="handleTaskComplete(selectedTask)">完成</el-button>
          <el-button type="danger" @click="handleTaskAbandon(selectedTask)">放弃</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh, Delete, InfoFilled } from '@element-plus/icons-vue'
import axios from 'axios'

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  }
]

// 调度表单
const scheduleForm = ref({
  algorithm: 'Priority',
  dateRange: [],
  density: 'none',
  densePreference: 'early',
  sliceLongTasks: false,
  sliceDuration: 25,
  customAlgorithmType: 'file',
  customAlgorithmCode: ''
})

// 加载状态
const loading = ref(false)

// 调度数据
const scheduleDays = ref([])
const stats = ref({
  totalTasks: 0,
  completedTasks: 0,
  pendingTasks: 0,
  avgWaitTime: 0
})

// 调度日志
const scheduleLogs = ref([])
const logContent = ref(null)

// 任务对话框
const taskDialogVisible = ref(false)
const selectedTask = ref(null)

// 格式化日期时间
const formatDateTime = (datetime) => {
  if (!datetime) return '未设置'
  return new Date(datetime).toLocaleString()
}

// 格式化日志时间
const formatLogTime = (time) => {
  return new Date(time).toLocaleTimeString()
}

// 格式化任务时间
const formatTaskTime = (task) => {
  if (task.isUnlimited) {
    return `完成次数：${task.completionCount}/${task.requiredCount}`
  }
  return `${task.startTime} - ${task.endTime}`
}

// 获取任务样式
const getTaskStyle = (task) => {
  const startHour = parseInt(task.startTime.split(':')[0])
  const endHour = parseInt(task.endTime.split(':')[0])
  const duration = endHour - startHour
  
  return {
    left: `${(startHour / 24) * 100}%`,
    width: `${(duration / 24) * 100}%`,
    backgroundColor: getPriorityColor(task.priority),
    borderLeft: `4px solid ${getPriorityColor(task.priority)}`
  }
}

// 获取任务提示
const getTaskTooltip = (task) => {
  const lines = [
    task.title,
    `开始时间：${task.startTime}`,
    `结束时间：${task.endTime}`,
    `优先级：${task.priority}`,
    `状态：${getStatusLabel(task.status)}`
  ]
  if (task.description) {
    lines.push(`描述：${task.description}`)
  }
  return lines.join('\n')
}

// 获取优先级标签
const getPriorityLabel = (priority) => {
  return `优先级: ${priority}`
}

// 获取优先级类型
const getPriorityType = (priority) => {
  if (priority >= 4000) return 'danger'
  if (priority >= 2000) return 'warning'
  return 'info'
}

// 获取优先级颜色
const getPriorityColor = (priority) => {
  // 根据优先级数值返回颜色
  const colors = {
    high: '#f56c6c',
    medium: '#e6a23c',
    low: '#909399'
  }
  return colors[priority] || '#909399'
}

// 获取状态标签
const getStatusLabel = (status) => {
  const labels = {
    pending: '未开始',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labels[status] || '未知'
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 处理算法文件上传
const handleAlgorithmUpload = (response) => {
  if (response.success) {
    ElMessage.success('算法文件上传成功')
  } else {
    ElMessage.error('算法文件上传失败：' + response.message)
  }
}

// 上传前验证
const beforeAlgorithmUpload = (file) => {
  const isPython = file.name.endsWith('.py')
  if (!isPython) {
    ElMessage.error('只能上传Python文件！')
    return false
  }
  return true
}

// 处理文件超出限制
const handleExceed = () => {
  ElMessage.warning('只能上传一个算法文件')
}

// 处理调度
const handleSchedule = async () => {
  if (!scheduleForm.value.algorithm) {
    ElMessage.warning('请选择调度算法')
    return
  }
  if (!scheduleForm.value.dateRange || scheduleForm.value.dateRange.length !== 2) {
    ElMessage.warning('请选择时间范围')
    return
  }
  
  if (scheduleForm.value.algorithm === 'custom') {
    if (scheduleForm.value.customAlgorithmType === 'code' && !scheduleForm.value.customAlgorithmCode) {
      ElMessage.warning('请输入算法代码')
      return
    }
  }
  
  if (scheduleForm.value.algorithm === 'ai') {
    ElMessageBox.confirm(
      '使用AI调度会将任务数据上传至云端，是否继续？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    ).then(() => {
      performSchedule()
    })
  } else {
    performSchedule()
  }
}

// 执行调度
const performSchedule = async () => {
  loading.value = true
  try {
    const formData = {
      algorithm: scheduleForm.value.algorithm,
      start_date: scheduleForm.value.dateRange[0].toISOString(),
      end_date: scheduleForm.value.dateRange[1].toISOString(),
      density: scheduleForm.value.density,
      densePreference: scheduleForm.value.densePreference,
      sliceLongTasks: scheduleForm.value.sliceLongTasks,
      sliceDuration: scheduleForm.value.sliceDuration
    }

    if (scheduleForm.value.algorithm === 'custom') {
      if (scheduleForm.value.customAlgorithmType === 'code') {
        formData.algorithm_code = scheduleForm.value.customAlgorithmCode
      }
    }

    const response = await axios.post('/api/schedule', formData)
    
    scheduleDays.value = response.data.schedule
    addLog('开始调度任务')
    ElMessage.success('调度完成')
  } catch (error) {
    ElMessage.error('调度失败：' + error.message)
  } finally {
    loading.value = false
  }
}

// 重置表单
const handleReset = () => {
  scheduleForm.value = {
    algorithm: 'Priority',
    dateRange: [],
    density: 'none',
    densePreference: 'early',
    sliceLongTasks: false,
    sliceDuration: 25,
    customAlgorithmType: 'file',
    customAlgorithmCode: ''
  }
}

// 刷新统计数据
const refreshStats = async () => {
  try {
    const response = await axios.get('/api/tasks/statistics')
    stats.value = response.data
  } catch (error) {
    ElMessage.error('获取统计数据失败：' + error.message)
  }
}

// 添加日志
const addLog = (message) => {
  scheduleLogs.value.unshift({
    time: new Date().toISOString(),
    message
  })
  nextTick(() => {
    if (logContent.value) {
      logContent.value.scrollTop = 0
    }
  })
}

// 清空日志
const clearLogs = () => {
  scheduleLogs.value = []
}

// 处理任务点击
const handleTaskClick = (task) => {
  selectedTask.value = task
  taskDialogVisible.value = true
}

// 处理任务编辑
const handleTaskEdit = () => {
  // TODO: 实现任务编辑功能
  taskDialogVisible.value = false
}

// 处理任务完成
const handleTaskComplete = async (task) => {
  try {
    if (task.isUnlimited) {
      // 显示完成次数选择对话框
      const { value: count } = await ElMessageBox.prompt(
        '请输入完成次数',
        '完成任务',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^[1-9]\d*$/,
          inputErrorMessage: '请输入有效的完成次数'
        }
      )
      await axios.post(`/api/tasks/${task.id}/complete`, { count: parseInt(count) })
    } else {
      await axios.post(`/api/tasks/${task.id}/complete`)
    }
    ElMessage.success('任务已完成')
    refreshStats()
  } catch (error) {
    ElMessage.error('操作失败：' + error.message)
  }
}

// 处理任务放弃
const handleTaskAbandon = async (task) => {
  try {
    await ElMessageBox.confirm(
      '确定要放弃此任务吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await axios.post(`/api/tasks/${task.id}/abandon`)
    ElMessage.success('任务已放弃')
    refreshStats()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败：' + error.message)
    }
  }
}

// 初始化
onMounted(() => {
  refreshStats()
})
</script>

<style lang="scss" scoped>
.schedule-toolbar {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
}

.schedule-content {
  .schedule-timeline {
    background-color: #fff;
    border-radius: 4px;
    padding: 20px;
    
    .timeline-header {
      .time-slots {
        display: flex;
        border-bottom: 1px solid #dcdfe6;
        
        .time-slot {
          flex: 1;
          text-align: center;
          padding: 8px 0;
          font-size: 12px;
          color: #909399;
        }
      }
    }
    
    .timeline-body {
      .timeline-day {
        display: flex;
        border-bottom: 1px solid #ebeef5;
        
        .day-header {
          width: 100px;
          padding: 10px;
          font-weight: bold;
          background-color: #f5f7fa;
        }
        
        .day-content {
          flex: 1;
          position: relative;
          height: 60px;
          
          .task-block {
            position: absolute;
            height: 40px;
            margin: 10px 0;
            padding: 0 10px;
            line-height: 40px;
            color: #fff;
            border-radius: 4px;
            cursor: pointer;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            transition: all 0.3s;
            
            &:hover {
              transform: scale(1.02);
              box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
            }
            
            .task-content {
              display: flex;
              flex-direction: column;
              justify-content: center;
              height: 100%;
              
              .task-title {
                font-size: 14px;
                font-weight: bold;
              }
              
              .task-time {
                font-size: 12px;
                opacity: 0.8;
              }
            }
          }
        }
      }
    }
  }
  
  .schedule-stats {
    .stats-card {
      margin-bottom: 20px;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
      }
      
      .stats-content {
        .stat-item {
          margin-bottom: 10px;
          
          .label {
            color: #606266;
          }
          
          .value {
            font-weight: bold;
            color: #303133;
          }
        }
      }
      
      .log-content {
        height: 300px;
        overflow-y: auto;
        
        .log-item {
          padding: 8px 0;
          border-bottom: 1px solid #ebeef5;
          font-size: 12px;
          color: #606266;
          
          .log-time {
            color: #909399;
            margin-right: 8px;
          }
        }
      }
    }
  }
}

.task-detail {
  .detail-item {
    margin-bottom: 16px;
    
    .label {
      color: #606266;
      margin-right: 8px;
    }
    
    .value {
      color: #303133;
    }
  }
}

.custom-algorithm-option {
  display: flex;
  align-items: center;
  gap: 10px;
}

.algorithm-upload {
  margin-top: 10px;
}

.code-tips {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 12px;
  color: #606266;

  p {
    margin: 0 0 5px 0;
    font-weight: bold;
  }

  ul {
    margin: 0;
    padding-left: 20px;
  }
}
</style> 