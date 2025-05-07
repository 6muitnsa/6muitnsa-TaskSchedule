<template>
  <div class="task-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>任务详情</span>
          <div class="header-actions">
            <el-button type="primary" @click="editTask">编辑</el-button>
            <el-button @click="goBack">返回</el-button>
          </div>
        </div>
      </template>

      <div v-if="error" class="error-message">
        <el-alert :title="error" type="error" show-icon />
      </div>

      <div v-else-if="task" class="task-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="任务名称" :span="2">
            {{ task.name }}
          </el-descriptions-item>
          <el-descriptions-item label="优先级">
            <el-tag :type="getPriorityType(task.priority)">
              {{ getPriorityText(task.priority) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(task.status)">
              {{ getStatusText(task.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ task.description || '无' }}
          </el-descriptions-item>
          <el-descriptions-item label="标签" :span="2">
            <el-tag
              v-for="tag in task.tags"
              :key="tag"
              class="mx-1"
              size="small"
            >
              {{ tag }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ formatDate(task.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="截止时间">
            {{ formatDate(task.deadline) }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="task-actions mt-20">
          <el-button
            v-if="task.status === 'pending'"
            type="primary"
            @click="startTask"
          >
            开始任务
          </el-button>
          <el-button
            v-if="task.status === 'in_progress'"
            type="success"
            @click="completeTask"
          >
            完成任务
          </el-button>
          <el-button
            v-if="['pending', 'in_progress'].includes(task.status)"
            type="danger"
            @click="abandonTask"
          >
            放弃任务
          </el-button>
        </div>
      </div>

      <!-- 任务提醒 -->
      <el-card class="task-card">
        <template #header>
          <div class="card-header">
            <span>任务提醒</span>
          </div>
        </template>
        <task-reminder :task-id="task.id" />
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import TaskReminder from '../../components/TaskReminder.vue'
import { taskApi } from '../../api'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)
const task = ref(null)

// 获取任务详情
const getTaskDetail = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await taskApi.getTask(route.params.id)
    task.value = response.data
  } catch (err) {
    console.error('获取任务详情失败:', err)
    error.value = '获取任务详情失败，请重试'
  } finally {
    loading.value = false
  }
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    abandoned: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    pending: '待开始',
    in_progress: '进行中',
    completed: '已完成',
    abandoned: '已放弃'
  }
  return texts[status] || status
}

// 获取优先级类型
const getPriorityType = (priority) => {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[priority] || 'info'
}

// 获取优先级文本
const getPriorityText = (priority) => {
  const texts = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return texts[priority] || priority
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '无'
  return new Date(date).toLocaleString()
}

// 编辑任务
const editTask = () => {
  router.push({
    name: 'EditTask',
    params: { id: task.value.id }
  })
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 开始任务
const startTask = async () => {
  try {
    await taskApi.startTask(task.value.id)
    ElMessage.success('任务已开始')
    await getTaskDetail()
  } catch (err) {
    console.error('开始任务失败:', err)
    ElMessage.error('开始任务失败，请重试')
  }
}

// 完成任务
const completeTask = async () => {
  try {
    await ElMessageBox.confirm('确定要完成任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await taskApi.completeTask(task.value.id)
    ElMessage.success('任务已完成')
    await getTaskDetail()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('完成任务失败:', err)
      ElMessage.error('完成任务失败，请重试')
    }
  }
}

// 放弃任务
const abandonTask = async () => {
  try {
    await ElMessageBox.confirm('确定要放弃任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await taskApi.abandonTask(task.value.id)
    ElMessage.success('任务已放弃')
    await getTaskDetail()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('放弃任务失败:', err)
      ElMessage.error('放弃任务失败，请重试')
    }
  }
}

onMounted(() => {
  getTaskDetail()
})
</script>

<style lang="scss" scoped>
.task-detail {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-actions {
      display: flex;
      gap: 10px;
    }
  }

  .task-content {
    .el-tag {
      margin-right: 5px;
    }
  }

  .mt-20 {
    margin-top: 20px;
  }

  .task-actions {
    display: flex;
    gap: 10px;
    justify-content: center;
  }
}
</style> 