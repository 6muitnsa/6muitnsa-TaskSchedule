<template>
  <div class="pomodoro-timer">
    <div class="timer-display">
      <div class="time">{{ formattedTime }}</div>
      <div class="status">{{ statusText }}</div>
    </div>

    <div class="timer-controls">
      <el-button-group>
        <el-button
          type="primary"
          :disabled="isRunning"
          @click="startTimer"
        >
          开始
        </el-button>
        <el-button
          type="danger"
          :disabled="!isRunning"
          @click="stopTimer"
        >
          停止
        </el-button>
        <el-button
          :disabled="!isRunning"
          @click="resetTimer"
        >
          重置
        </el-button>
      </el-button-group>
    </div>

    <div class="timer-settings">
      <el-form :model="settings" label-width="120px">
        <el-form-item label="工作时间">
          <el-input-number
            v-model="settings.workTime"
            :min="5"
            :max="60"
            :step="5"
          />
          <span class="unit">分钟</span>
        </el-form-item>
        <el-form-item label="休息时间">
          <el-input-number
            v-model="settings.breakTime"
            :min="1"
            :max="30"
            :step="1"
          />
          <span class="unit">分钟</span>
        </el-form-item>
        <el-form-item label="长休息时间">
          <el-input-number
            v-model="settings.longBreakTime"
            :min="5"
            :max="60"
            :step="5"
          />
          <span class="unit">分钟</span>
        </el-form-item>
        <el-form-item label="长休息间隔">
          <el-input-number
            v-model="settings.longBreakInterval"
            :min="2"
            :max="8"
            :step="1"
          />
          <span class="unit">个番茄钟</span>
        </el-form-item>
      </el-form>
    </div>

    <div class="timer-stats">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="今日完成">
          {{ stats.today }} 个
        </el-descriptions-item>
        <el-descriptions-item label="本周完成">
          {{ stats.week }} 个
        </el-descriptions-item>
        <el-descriptions-item label="本月完成">
          {{ stats.month }} 个
        </el-descriptions-item>
        <el-descriptions-item label="总计完成">
          {{ stats.total }} 个
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'

const timer = ref(null)
const timeLeft = ref(0)
const isRunning = ref(false)
const isBreak = ref(false)
const pomodoroCount = ref(0)

const settings = reactive({
  workTime: 25,
  breakTime: 5,
  longBreakTime: 15,
  longBreakInterval: 4
})

const stats = reactive({
  today: 0,
  week: 0,
  month: 0,
  total: 0
})

const formattedTime = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60)
  const seconds = timeLeft.value % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

const statusText = computed(() => {
  if (!isRunning.value) return '准备就绪'
  return isBreak.value ? '休息时间' : '工作时间'
})

const startTimer = () => {
  if (isRunning.value) return
  
  isRunning.value = true
  timer.value = setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      clearInterval(timer.value)
      handleTimerComplete()
    }
  }, 1000)
}

const stopTimer = () => {
  if (!isRunning.value) return
  
  clearInterval(timer.value)
  isRunning.value = false
}

const resetTimer = () => {
  stopTimer()
  timeLeft.value = isBreak.value ? settings.breakTime * 60 : settings.workTime * 60
}

const handleTimerComplete = () => {
  if (!isBreak.value) {
    pomodoroCount.value++
    // TODO: 更新统计数据
  }
  
  isBreak.value = !isBreak.value
  timeLeft.value = isBreak.value ? settings.breakTime * 60 : settings.workTime * 60
  
  if (isRunning.value) {
    startTimer()
  }
}

onMounted(() => {
  timeLeft.value = settings.workTime * 60
  // TODO: 加载统计数据
})

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
</script>

<style scoped>
.pomodoro-timer {
  padding: 20px;
  text-align: center;
}

.timer-display {
  margin-bottom: 30px;
}

.time {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 10px;
}

.status {
  font-size: 18px;
  color: #666;
}

.timer-controls {
  margin-bottom: 30px;
}

.timer-settings {
  margin-bottom: 30px;
}

.unit {
  margin-left: 10px;
  color: #666;
}

.timer-stats {
  margin-top: 30px;
}
</style> 