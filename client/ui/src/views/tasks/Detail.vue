<template>
  <div class="container">
    <el-card class="task-detail">
      <template #header>
        <div class="card-header">
          <h2>{{ task?.title || '加载中...' }}</h2>
          <div class="actions">
            <el-button type="primary" @click="handleEdit" v-if="task">编辑</el-button>
            <el-button type="danger" @click="handleDelete" v-if="task">删除</el-button>
          </div>
        </div>
      </template>
      
      <div v-if="task" class="task-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(task.status)">{{ getStatusText(task.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="优先级">
            <el-tag :type="getPriorityType(task.priority)">{{ getPriorityText(task.priority) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ task.start_time || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ task.end_time || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ task.created_at }}</el-descriptions-item>
          <el-descriptions-item label="更新时间">{{ task.updated_at }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ task.description || '暂无描述' }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="task-actions" v-if="task.status === 'pending'">
          <el-button type="success" @click="handleComplete">完成任务</el-button>
          <el-button type="warning" @click="handleAbandon">放弃任务</el-button>
        </div>
      </div>
      
      <div v-else class="loading">
        <el-empty description="任务不存在或已被删除" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/api'

const route = useRoute()
const router = useRouter()
const task = ref(null)

// 获取任务详情
const fetchTask = async () => {
  try {
    const response = await api.get(`/tasks/${route.params.id}`)
    task.value = response.data
  } catch (error) {
    ElMessage.error('获取任务详情失败')
    console.error(error)
  }
}

// 状态相关方法
const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    completed: 'success',
    abandoned: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '进行中',
    completed: '已完成',
    abandoned: '已放弃'
  }
  return texts[status] || status
}

// 优先级相关方法
const getPriorityType = (priority) => {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[priority] || 'info'
}

const getPriorityText = (priority) => {
  const texts = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return texts[priority] || priority
}

// 操作处理方法
const handleEdit = () => {
  router.push(`/tasks/edit/${route.params.id}`)
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '警告', {
      type: 'warning'
    })
    await api.delete(`/tasks/${route.params.id}`)
    ElMessage.success('删除成功')
    router.push('/tasks')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
      console.error(error)
    }
  }
}

const handleComplete = async () => {
  try {
    await api.post(`/tasks/${route.params.id}/complete`)
    ElMessage.success('任务已完成')
    await fetchTask()
  } catch (error) {
    ElMessage.error('操作失败')
    console.error(error)
  }
}

const handleAbandon = async () => {
  try {
    await ElMessageBox.confirm('确定要放弃这个任务吗？', '警告', {
      type: 'warning'
    })
    await api.post(`/tasks/${route.params.id}/abandon`)
    ElMessage.success('任务已放弃')
    await fetchTask()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
      console.error(error)
    }
  }
}

onMounted(() => {
  fetchTask()
})
</script>

<style scoped>
.task-detail {
  max-width: 800px;
  margin: 20px auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5em;
}

.task-content {
  margin-top: 20px;
}

.task-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.loading {
  padding: 40px 0;
}
</style> 