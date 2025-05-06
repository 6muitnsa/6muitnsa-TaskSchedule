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
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="scheduleForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSchedule">开始调度</el-button>
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
                  >
                    {{ task.name }}
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
                </div>
              </template>
              <div class="log-content">
                <div v-for="(log, index) in scheduleLogs" :key="index" class="log-item">
                  {{ log }}
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// 调度表单
const scheduleForm = ref({
  algorithm: 'Priority',
  dateRange: []
})

// 模拟数据
const scheduleDays = ref([
  {
    date: '2024-03-20',
    label: '3月20日',
    tasks: [
      {
        id: 1,
        name: '项目文档',
        startTime: '09:00',
        endTime: '12:00',
        priority: 'high'
      },
      {
        id: 2,
        name: '代码审查',
        startTime: '14:00',
        endTime: '16:00',
        priority: 'medium'
      }
    ]
  },
  {
    date: '2024-03-21',
    label: '3月21日',
    tasks: [
      {
        id: 3,
        name: '团队会议',
        startTime: '10:00',
        endTime: '11:00',
        priority: 'high'
      }
    ]
  }
])

// 统计数据
const stats = ref({
  totalTasks: 3,
  completedTasks: 1,
  pendingTasks: 2,
  avgWaitTime: 45
})

// 调度日志
const scheduleLogs = ref([
  '2024-03-20 09:00:00 开始调度任务：项目文档',
  '2024-03-20 12:00:00 完成任务：项目文档',
  '2024-03-20 14:00:00 开始调度任务：代码审查'
])

// 计算任务样式
const getTaskStyle = (task) => {
  const startHour = parseInt(task.startTime.split(':')[0])
  const endHour = parseInt(task.endTime.split(':')[0])
  const duration = endHour - startHour
  
  return {
    left: `${(startHour / 24) * 100}%`,
    width: `${(duration / 24) * 100}%`,
    backgroundColor: task.priority === 'high' ? '#f56c6c' : '#e6a23c'
  }
}

// 获取任务提示
const getTaskTooltip = (task) => {
  return `${task.name}\n${task.startTime} - ${task.endTime}\n优先级：${task.priority}`
}

// 处理调度
const handleSchedule = () => {
  if (!scheduleForm.value.algorithm) {
    ElMessage.warning('请选择调度算法')
    return
  }
  if (!scheduleForm.value.dateRange || scheduleForm.value.dateRange.length !== 2) {
    ElMessage.warning('请选择时间范围')
    return
  }
  
  // TODO: 调用后端API进行调度
  ElMessage.success('开始调度任务')
}

// 重置表单
const handleReset = () => {
  scheduleForm.value = {
    algorithm: 'Priority',
    dateRange: []
  }
}
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
          }
        }
      }
    }
  }
  
  .schedule-stats {
    .stats-card {
      margin-bottom: 20px;
      
      .card-header {
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
        }
      }
    }
  }
}
</style> 