<template>
  <div class="calendar-view">
    <div class="calendar-header">
      <el-button-group>
        <el-button @click="prevMonth">上个月</el-button>
        <el-button @click="nextMonth">下个月</el-button>
      </el-button-group>
      <h2>{{ currentMonthText }}</h2>
    </div>

    <el-calendar v-model="currentDate">
      <template #dateCell="{ data }">
        <div class="calendar-cell">
          <div class="date">{{ data.day.split('-').slice(2).join('') }}</div>
          <div class="tasks">
            <div
              v-for="task in getTasksForDate(data.day)"
              :key="task.id"
              class="task-item"
              :class="getTaskPriorityClass(task)"
              @click="showTaskDetail(task)"
            >
              {{ task.name }}
            </div>
          </div>
        </div>
      </template>
    </el-calendar>

    <el-dialog
      v-model="taskDetailVisible"
      title="任务详情"
      width="50%"
    >
      <task-detail
        v-if="selectedTask"
        :task="selectedTask"
        @close="taskDetailVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'
import TaskDetail from './TaskDetail.vue'

const currentDate = ref(new Date())
const tasks = ref([])
const taskDetailVisible = ref(false)
const selectedTask = ref(null)

const currentMonthText = computed(() => {
  return format(currentDate.value, 'yyyy年MM月', { locale: zhCN })
})

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

const getTasksForDate = (date) => {
  return tasks.value.filter(task => {
    const taskDate = new Date(task.start_time)
    return format(taskDate, 'yyyy-MM-dd') === date
  })
}

const getTaskPriorityClass = (task) => {
  if (task.priority >= 2001) return 'high-priority'
  if (task.priority >= 1001) return 'medium-priority'
  return 'low-priority'
}

const showTaskDetail = (task) => {
  selectedTask.value = task
  taskDetailVisible.value = true
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

.calendar-cell {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.date {
  font-weight: bold;
  margin-bottom: 5px;
}

.tasks {
  flex: 1;
  overflow-y: auto;
}

.task-item {
  padding: 2px 5px;
  margin: 2px 0;
  border-radius: 3px;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.high-priority {
  background-color: #fef0f0;
  color: #f56c6c;
}

.medium-priority {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.low-priority {
  background-color: #f0f9eb;
  color: #67c23a;
}
</style> 