<template>
  <div class="pomodoro-container">
    <el-card class="pomodoro-card">
      <template #header>
        <div class="card-header">
          <h2>番茄钟</h2>
        </div>
      </template>
      
      <div class="timer-display">
        <span class="time">{{ formattedTime }}</span>
      </div>
      
      <div class="timer-controls">
        <el-button 
          type="primary" 
          @click="startTimer" 
          :disabled="isRunning"
        >
          开始
        </el-button>
        <el-button 
          type="warning" 
          @click="pauseTimer" 
          :disabled="!isRunning || isPaused"
        >
          暂停
        </el-button>
        <el-button 
          type="danger" 
          @click="stopTimer" 
          :disabled="!isRunning && !isPaused"
        >
          停止
        </el-button>
      </div>
      
      <div class="settings">
        <el-form :model="settings" label-width="120px">
          <el-form-item label="专注时长(分钟)">
            <el-input-number 
              v-model="settings.workDuration" 
              :min="1" 
              :max="60"
            />
          </el-form-item>
          <el-form-item label="休息时长(分钟)">
            <el-input-number 
              v-model="settings.breakDuration" 
              :min="1" 
              :max="30"
            />
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'

const settings = ref({
  workDuration: 25,
  breakDuration: 5
})

const timeLeft = ref(0)
const isRunning = ref(false)
const isPaused = ref(false)
const timer = ref<number | null>(null)
const isBreak = ref(false)

const formattedTime = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60)
  const seconds = timeLeft.value % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

const startTimer = () => {
  if (!isRunning.value) {
    timeLeft.value = (isBreak.value ? settings.value.breakDuration : settings.value.workDuration) * 60
    isRunning.value = true
    isPaused.value = false
    timer.value = window.setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--
      } else {
        clearInterval(timer.value!)
        isRunning.value = false
        isBreak.value = !isBreak.value
        ElMessage.success(isBreak.value ? '休息时间到！' : '专注时间到！')
      }
    }, 1000)
  }
}

const pauseTimer = () => {
  if (isRunning.value && !isPaused.value) {
    clearInterval(timer.value!)
    isPaused.value = true
  }
}

const stopTimer = () => {
  clearInterval(timer.value!)
  isRunning.value = false
  isPaused.value = false
  isBreak.value = false
  timeLeft.value = 0
}

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
</script>

<style scoped>
.pomodoro-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.pomodoro-card {
  text-align: center;
}

.timer-display {
  font-size: 4rem;
  margin: 20px 0;
}

.timer-controls {
  margin: 20px 0;
}

.settings {
  margin-top: 20px;
}
</style> 