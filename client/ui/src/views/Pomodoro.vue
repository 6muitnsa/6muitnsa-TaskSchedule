<template>
  <div class="pomodoro container">
    <el-card class="timer-card">
      <template #header>
        <div class="card-header">
          <h2>番茄钟</h2>
        </div>
      </template>

      <!-- 专注时间 -->
      <div v-if="currentMode === 'focus'" class="timer-section">
        <div class="timer-display">
          <div class="time">{{ formatTime(timeLeft) }}</div>
          <div class="mode">专注时间</div>
          <div class="elapsed-time">已专注：{{ formatTime(elapsedTime) }}</div>
        </div>

        <div class="timer-controls">
          <el-button
            type="primary"
            size="large"
            :icon="isRunning ? 'Pause' : 'VideoPlay'"
            @click="toggleTimer"
          >
            {{ isRunning ? '暂停专注' : '开始专注' }}
          </el-button>
          <el-button
            type="warning"
            size="large"
            icon="Plus"
            @click="extendTime(5)"
          >
            延长5分钟
          </el-button>
          <el-button
            type="info"
            size="large"
            icon="Switch"
            @click="switchToBreak"
          >
            提前休息
          </el-button>
        </div>
      </div>

      <!-- 休息时间 -->
      <div v-else class="timer-section">
        <div class="timer-display">
          <div class="time">{{ formatTime(timeLeft) }}</div>
          <div class="mode">休息时间</div>
          <div class="elapsed-time">已休息：{{ formatTime(elapsedTime) }}</div>
        </div>

        <div class="timer-controls">
          <el-button
            type="success"
            size="large"
            :icon="isRunning ? 'Pause' : 'VideoPlay'"
            @click="toggleTimer"
          >
            {{ isRunning ? '暂停休息' : '开始休息' }}
          </el-button>
          <el-button
            type="warning"
            size="large"
            icon="Plus"
            @click="extendTime(5)"
          >
            延长5分钟
          </el-button>
          <el-button
            type="info"
            size="large"
            icon="Switch"
            @click="switchToFocus"
          >
            提前专注
          </el-button>
        </div>
      </div>

      <!-- 状态提示 -->
      <div v-if="showStatusTip" class="status-tip">
        <el-alert
          title="此次专注时长远超平均值，状态极好"
          type="success"
          :closable="false"
          show-icon
        >
          <template #default>
            <div class="status-tip-content">
              <p>此次任务类型是？</p>
              <el-select
                v-model="selectedTaskType"
                placeholder="选择任务类型"
                @change="handleTaskTypeSelect"
              >
                <el-option
                  v-for="type in taskTypes"
                  :key="type"
                  :label="type"
                  :value="type"
                />
              </el-select>
              <el-button @click="skipStatusTip">跳过</el-button>
            </div>
          </template>
        </el-alert>
      </div>
    </el-card>

    <!-- 历史记录 -->
    <el-card class="history-card">
      <template #header>
        <div class="card-header">
          <h3>番茄钟历史记录</h3>
        </div>
      </template>

      <div class="history-list">
        <div
          v-for="(record, index) in historyRecords"
          :key="index"
          class="history-item"
        >
          <div class="history-info">
            <div class="history-mode">
              <el-tag :type="record.mode === 'focus' ? 'primary' : 'success'">
                {{ record.mode === 'focus' ? '专注' : '休息' }}
              </el-tag>
            </div>
            <div class="history-time">
              <span>时长：{{ record.duration }}分钟</span>
              <span>时间：{{ record.time }}</span>
            </div>
          </div>
          <el-button
            type="danger"
            size="small"
            icon="Delete"
            @click="deleteRecord(index)"
          >
            删除
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'

// 状态
const isRunning = ref(false)
const timeLeft = ref(25 * 60) // 默认25分钟
const elapsedTime = ref(0) // 已用时间
const currentMode = ref('focus')
const timer = ref(null)
const showStatusTip = ref(false)
const selectedTaskType = ref('')

// 历史记录
const historyRecords = ref([])

// 任务类型
const taskTypes = ref(['工作', '学习', '阅读', '写作', '其他'])

// 格式化时间
const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 切换计时器状态
const toggleTimer = () => {
  if (isRunning.value) {
    clearInterval(timer.value)
    // 记录当前时间
    addHistoryRecord()
  } else {
    timer.value = setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--
        elapsedTime.value++
      } else {
        handleTimerComplete()
      }
    }, 1000)
  }
  isRunning.value = !isRunning.value
}

// 延长时间
const extendTime = (minutes) => {
  timeLeft.value += minutes * 60
}

// 切换到休息模式
const switchToBreak = () => {
  // 记录当前状态并切换到休息模式
  addHistoryRecord()
  currentMode.value = 'break'
  timeLeft.value = 5 * 60 // 默认5分钟休息
  elapsedTime.value = 0
  isRunning.value = true
  clearInterval(timer.value)
  timer.value = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
      elapsedTime.value++
    } else {
      handleTimerComplete()
    }
  }, 1000)
}

// 切换到专注模式
const switchToFocus = () => {
  // 记录当前状态并切换到专注模式
  addHistoryRecord()
  currentMode.value = 'focus'
  timeLeft.value = 25 * 60 // 默认25分钟专注
  elapsedTime.value = 0
  isRunning.value = true
  clearInterval(timer.value)
  timer.value = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
      elapsedTime.value++
    } else {
      handleTimerComplete()
    }
  }, 1000)
}

// 处理计时器完成
const handleTimerComplete = () => {
  clearInterval(timer.value)
  isRunning.value = false
  addHistoryRecord()

  if (currentMode.value === 'focus') {
    // 检查是否需要显示状态提示
    const focusDuration = elapsedTime.value / 60
    if (focusDuration > 30) { // 假设30分钟是平均值
      showStatusTip.value = true
    }
    currentMode.value = 'break'
    timeLeft.value = 5 * 60 // 默认5分钟休息
    elapsedTime.value = 0
  } else {
    currentMode.value = 'focus'
    timeLeft.value = 25 * 60 // 默认25分钟专注
    elapsedTime.value = 0
  }
}

// 添加历史记录
const addHistoryRecord = () => {
  const now = new Date()
  const duration = Math.round(elapsedTime.value / 60)
  
  historyRecords.value.unshift({
    mode: currentMode.value,
    duration: duration,
    time: now.toLocaleTimeString()
  })
}

// 删除历史记录
const deleteRecord = (index) => {
  historyRecords.value.splice(index, 1)
}

// 处理任务类型选择
const handleTaskTypeSelect = (type) => {
  // TODO: 实现任务类型选择逻辑
  ElMessage.success(`已记录任务类型：${type}`)
  showStatusTip.value = false
  selectedTaskType.value = ''
}

// 跳过状态提示
const skipStatusTip = () => {
  showStatusTip.value = false
  selectedTaskType.value = ''
}

// 生命周期钩子
onMounted(() => {
  // 初始化
})

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
</script>

<style lang="scss" scoped>
.pomodoro {
  padding: var(--spacing-medium);
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-large);
  max-width: 1200px;
  margin: 0 auto;

  .timer-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h2 {
        margin: 0;
        color: var(--text-primary);
      }
    }

    .timer-section {
      text-align: center;
      padding: var(--spacing-large) 0;

      .timer-display {
        margin-bottom: var(--spacing-large);

        .time {
          font-size: 48px;
          font-weight: bold;
          color: var(--text-primary);
          margin-bottom: var(--spacing-small);
        }

        .mode {
          font-size: var(--font-size-large);
          color: var(--text-regular);
          margin-bottom: var(--spacing-small);
        }

        .elapsed-time {
          font-size: var(--font-size-medium);
          color: var(--text-secondary);
        }
      }

      .timer-controls {
        display: flex;
        gap: var(--spacing-medium);
        justify-content: center;

        .el-button {
          min-width: 120px;
        }
      }
    }

    .status-tip {
      margin-top: var(--spacing-medium);

      .status-tip-content {
        display: flex;
        gap: var(--spacing-medium);
        align-items: center;
        margin-top: var(--spacing-small);

        p {
          margin: 0;
          color: var(--text-regular);
        }
      }
    }
  }

  .history-card {
    .card-header {
      h3 {
        margin: 0;
        color: var(--text-primary);
      }
    }

    .history-list {
      .history-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--spacing-small) 0;
        border-bottom: 1px solid var(--border-color-light);

        &:last-child {
          border-bottom: none;
        }

        .history-info {
          display: flex;
          gap: var(--spacing-medium);
          align-items: center;

          .history-time {
            display: flex;
            gap: var(--spacing-medium);
            color: var(--text-regular);
          }
        }
      }
    }
  }
}

// 响应式布局
@media (max-width: 768px) {
  .pomodoro {
    grid-template-columns: 1fr;

    .timer-card {
      .timer-section {
        .timer-controls {
          flex-direction: column;

          .el-button {
            width: 100%;
          }
        }
      }

      .status-tip {
        .status-tip-content {
          flex-direction: column;
          align-items: stretch;

          .el-select {
            width: 100%;
          }
        }
      }
    }
  }
}
</style> 