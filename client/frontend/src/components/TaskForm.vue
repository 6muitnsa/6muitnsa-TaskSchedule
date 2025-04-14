<template>
  <div class="task-form">
    <el-form :model="form" label-width="120px">
      <el-form-item label="任务名称">
        <el-input v-model="form.title" placeholder="请输入任务名称" />
      </el-form-item>
      <el-form-item label="任务描述">
        <el-input
          v-model="form.description"
          type="textarea"
          placeholder="请输入任务描述"
        />
      </el-form-item>
      <el-form-item label="优先级">
        <el-select v-model="form.priority" placeholder="请选择优先级">
          <el-option label="低" value="low" />
          <el-option label="中" value="medium" />
          <el-option label="高" value="high" />
        </el-select>
      </el-form-item>
      <el-form-item label="预计时长">
        <el-input-number v-model="form.estimatedDuration" :min="0" :step="30" />
        <span class="unit">分钟</span>
      </el-form-item>
      <el-form-item label="截止日期">
        <el-date-picker
          v-model="form.deadline"
          type="datetime"
          placeholder="选择截止日期"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
        <el-button @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { Task } from '@/types/task'
import { useTaskStore } from '@/stores/task'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()

const form = ref<Partial<Task>>({
  title: '',
  description: '',
  priority: 'medium',
  estimatedDuration: 60,
  deadline: new Date(),
  status: 'pending'
})

const isEdit = ref(false)

onMounted(async () => {
  const taskId = route.params.id
  if (taskId) {
    isEdit.value = true
    const task = await taskStore.getTaskById(taskId as string)
    if (task) {
      form.value = { ...task }
    }
  }
})

const handleSubmit = async () => {
  try {
    if (isEdit.value) {
      await taskStore.updateTask(route.params.id as string, form.value as Task)
      ElMessage.success('任务更新成功')
    } else {
      await taskStore.createTask(form.value as Task)
      ElMessage.success('任务创建成功')
    }
    router.push('/tasks')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}
</script>

<style scoped>
.task-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.unit {
  margin-left: 10px;
  color: #666;
}
</style> 