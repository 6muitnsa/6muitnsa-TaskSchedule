<template>
  <div class="pomodoro">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>番茄钟</span>
            </div>
          </template>
          <div class="timer-container">
            <div class="timer-display">
              {{ formatTime(remainingTime) }}
            </div>
            <div class="timer-controls">
              <el-button
                type="primary"
                :disabled="isRunning"
                @click="startPomodoro"
              >
                开始专注
              </el-button>
              <el-button
                type="success"
                :disabled="!isRunning || isResting"
                @click="startRest"
              >
                开始休息
              </el-button>
              <el-button
                type="warning"
                :disabled="!isRunning"
                @click="extendTime"
              >
                延长5分钟
              </el-button>
              <el-button
                type="danger"
                :disabled="!isRunning"
                @click="endPomodoro"
              >
                结束
              </el-button>
            </div>
          </div>
          <div class="current-task" v-if="currentTask">
            <h3>当前任务</h3>
            <el-card shadow="hover">
              <div class="task-info">
                <h4>{{ currentTask.title }}</h4>
                <p>{{ currentTask.description }}</p>
                <div class="task-meta">
                  <el-tag :type="getPriorityType(currentTask.priority)">
                    优先级: {{ currentTask.priority }}
                  </el-tag>
                  <el-tag :type="getStatusType(currentTask.status)">
                    {{ getStatusText(currentTask.status) }}
                  </el-tag>
                </div>
              </div>
            </el-card>
          </div>
          <div class="task-select" v-else>
            <h3>选择任务</h3>
            <el-select
              v-model="selectedTaskId"
              placeholder="请选择任务"
              style="width: 100%"
            >
              <el-option
                v-for="task in pendingTasks"
                :key="task.task_id"
                :label="task.title"
                :value="task.task_id"
              />
            </el-select>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>历史记录</span>
            </div>
          </template>
          <el-table
            :data="pomodoroHistory"
            style="width: 100%"
          >
            <el-table-column
              prop="type"
              label="类型"
              width="100"
            >
              <template #default="{ row }">
                <el-tag :type="row.type === 'focus' ? 'success' : 'info'">
                  {{ row.type === 'focus' ? '专注' : '休息' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              prop="start_time"
              label="开始时间"
              width="180"
            >
              <template #default="{ row }">
                {{ formatDate(row.start_time) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="end_time"
              label="结束时间"
              width="180"
            >
              <template #default="{ row }">
                {{ row.end_time ? formatDate(row.end_time) : '进行中' }}
              </template>
            </el-table-column>
            <el-table-column
              prop="duration"
              label="时长"
              width="100"
            >
              <template #default="{ row }">
                {{ formatDuration(row.duration) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import dayjs from 'dayjs'

export default {
  name: 'Pomodoro',
  setup() {
    const store = useStore()
    const selectedTaskId = ref(null)
    const timer = ref(null)
    const remainingTime = ref(25 * 60) // 25 minutes in seconds
    const isRunning = ref(false)
    const isResting = ref(false)

    const currentTask = computed(() => {
      if (!selectedTaskId.value) return null
      return store.state.tasks.find(t => t.task_id === selectedTaskId.value)
    })

    const pendingTasks = computed(() => {
      return store.state.tasks.filter(t => t.status !== 'completed')
    })

    const pomodoroHistory = computed(() => {
      return store.state.pomodoroHistory.sort(
        (a, b) => new Date(b.start_time) - new Date(a.start_time)
      )
    })

    const startPomodoro = async () => {
      if (!selectedTaskId.value) {
        ElMessage.warning('请先选择任务')
        return
      }

      isRunning.value = true
      isResting.value = false
      remainingTime.value = 25 * 60 // 25 minutes
      timer.value = setInterval(() => {
        if (remainingTime.value > 0) {
          remainingTime.value--
        } else {
          endPomodoro()
          ElMessage.success('专注时间结束！')
        }
      }, 1000)

      await store.dispatch('startPomodoro', {
        taskId: selectedTaskId.value,
        type: 'focus'
      })
    }

    const startRest = async () => {
      isResting.value = true
      remainingTime.value = 5 * 60 // 5 minutes
      clearInterval(timer.value)
      timer.value = setInterval(() => {
        if (remainingTime.value > 0) {
          remainingTime.value--
        } else {
          endPomodoro()
          ElMessage.success('休息时间结束！')
        }
      }, 1000)

      await store.dispatch('startPomodoro', {
        taskId: selectedTaskId.value,
        type: 'rest'
      })
    }

    const extendTime = () => {
      remainingTime.value += 5 * 60 // Add 5 minutes
    }

    const endPomodoro = async () => {
      clearInterval(timer.value)
      isRunning.value = false
      isResting.value = false
      remainingTime.value = 25 * 60

      if (selectedTaskId.value) {
        await store.dispatch('endPomodoro', {
          taskId: selectedTaskId.value,
          type: isResting.value ? 'rest' : 'focus'
        })
      }
    }

    const formatTime = (seconds) => {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
    }

    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }

    const formatDuration = (duration) => {
      const minutes = Math.floor(duration / 60)
      const seconds = duration % 60
      return `${minutes}分${seconds}秒`
    }

    const getPriorityType = (priority) => {
      if (priority >= 8) return 'danger'
      if (priority >= 5) return 'warning'
      return 'info'
    }

    const getStatusType = (status) => {
      switch (status) {
        case 'completed':
          return 'success'
        case 'in_progress':
          return 'primary'
        default:
          return 'info'
      }
    }

    const getStatusText = (status) => {
      switch (status) {
        case 'completed':
          return '已完成'
        case 'in_progress':
          return '进行中'
        default:
          return '待办'
      }
    }

    onMounted(async () => {
      await store.dispatch('fetchTasks')
    })

    onUnmounted(() => {
      if (timer.value) {
        clearInterval(timer.value)
      }
    })

    return {
      selectedTaskId,
      remainingTime,
      isRunning,
      isResting,
      currentTask,
      pendingTasks,
      pomodoroHistory,
      startPomodoro,
      startRest,
      extendTime,
      endPomodoro,
      formatTime,
      formatDate,
      formatDuration,
      getPriorityType,
      getStatusType,
      getStatusText
    }
  }
}
</script>

<style lang="scss" scoped>
.pomodoro {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .timer-container {
    text-align: center;
    margin-bottom: 30px;

    .timer-display {
      font-size: 48px;
      font-weight: bold;
      margin-bottom: 20px;
    }

    .timer-controls {
      display: flex;
      justify-content: center;
      gap: 10px;
    }
  }

  .current-task,
  .task-select {
    margin-top: 20px;

    h3 {
      margin: 0 0 10px;
      font-size: 16px;
    }

    .task-info {
      h4 {
        margin: 0 0 10px;
      }

      p {
        margin: 0 0 10px;
        color: #666;
      }

      .task-meta {
        .el-tag {
          margin-right: 10px;
        }
      }
    }
  }
}
</style> 