<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>今日任务</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-number">{{ stats.todayTasks }}</div>
            <div class="stat-label">个任务待完成</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>本周完成</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-number">{{ stats.weekCompleted }}</div>
            <div class="stat-label">个任务已完成</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>番茄钟</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-number">{{ stats.pomodoroCount }}</div>
            <div class="stat-label">个番茄钟已完成</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="dashboard-row">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近任务</span>
              <el-button type="primary" link @click="viewAllTasks">
                查看全部
              </el-button>
            </div>
          </template>
          <el-table :data="recentTasks" style="width: 100%">
            <el-table-column prop="name" label="任务名称" />
            <el-table-column prop="priority" label="优先级">
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)">
                  {{ getPriorityText(row.priority) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="estimated_time" label="预计时间">
              <template #default="{ row }">
                {{ row.estimated_time }}分钟
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button-group>
                  <el-button size="small" @click="editTask(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteTask(row)">
                    删除
                  </el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>快速工具</span>
            </div>
          </template>
          <div class="quick-tools">
            <el-button type="primary" @click="startPomodoro">
              启动番茄钟
            </el-button>
            <el-button @click="createTask">创建任务</el-button>
            <el-button @click="viewCalendar">查看日历</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '../store/task'

const router = useRouter()
const taskStore = useTaskStore()

const stats = ref({
  todayTasks: 0,
  weekCompleted: 0,
  pomodoroCount: 0
})

const recentTasks = ref([])

onMounted(async () => {
  await taskStore.fetchTasks()
  // TODO: 获取统计数据
  // TODO: 获取最近任务
})

const getPriorityType = (priority) => {
  if (priority >= 2001) return 'danger'
  if (priority >= 1001) return 'warning'
  return 'info'
}

const getPriorityText = (priority) => {
  if (priority >= 2001) return '高'
  if (priority >= 1001) return '中'
  return '低'
}

const viewAllTasks = () => {
  router.push('/tasks')
}

const editTask = (task) => {
  router.push(`/tasks/${task.id}`)
}

const deleteTask = async (task) => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
      type: 'warning'
    })
    await taskStore.deleteTask(task.id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消删除
  }
}

const startPomodoro = () => {
  router.push('/pomodoro')
}

const createTask = () => {
  router.push('/tasks/new')
}

const viewCalendar = () => {
  router.push('/calendar')
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.dashboard-row {
  margin-top: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 20px 0;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  margin-top: 10px;
  color: #666;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quick-tools {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style> 