<template>
  <div class="calendar-view">
    <div class="calendar-header">
      <h2>月度视图</h2>
      <div class="calendar-controls">
        <el-button-group>
          <el-button @click="prevMonth">上个月</el-button>
          <el-button @click="nextMonth">下个月</el-button>
        </el-button-group>
        <el-button @click="today">今天</el-button>
      </div>
    </div>

    <el-calendar v-model="currentDate">
      <template #dateCell="{ data }">
        <div class="calendar-cell">
          <p>{{ data.day.split('-').slice(2).join('') }}</p>
          <div class="task-list">
            <div v-for="task in getTasksForDate(data.day)" :key="task.id" class="task-item">
              {{ task.name }}
            </div>
          </div>
        </div>
      </template>
    </el-calendar>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const currentDate = ref(new Date())

const prevMonth = () => {
  const date = new Date(currentDate.value)
  date.setMonth(date.getMonth() - 1)
  currentDate.value = date
}

const nextMonth = () => {
  const date = new Date(currentDate.value)
  date.setMonth(date.getMonth() + 1)
  currentDate.value = date
}

const today = () => {
  currentDate.value = new Date()
}

const getTasksForDate = (date) => {
  // TODO: 从API获取该日期的任务
  return []
}
</script>

<style scoped>
.calendar-view {
  padding: 20px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-controls {
  display: flex;
  gap: 10px;
}

.calendar-cell {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.calendar-cell p {
  margin: 0;
  font-weight: bold;
}

.task-list {
  flex: 1;
  overflow-y: auto;
}

.task-item {
  font-size: 12px;
  padding: 2px 4px;
  margin: 2px 0;
  background-color: #f0f9ff;
  border-radius: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style> 