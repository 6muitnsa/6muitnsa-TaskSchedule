<template>
  <div class="task-detail">
    <el-form :model="task" label-width="100px">
      <el-form-item label="任务名称">
        <el-input v-model="task.name" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="task.description" type="textarea" />
      </el-form-item>
      <el-form-item label="优先级">
        <el-input-number v-model="task.priority" :min="1" :max="10" />
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="task.status">
          <el-option label="待完成" value="待完成" />
          <el-option label="进行中" value="进行中" />
          <el-option label="已完成" value="已完成" />
        </el-select>
      </el-form-item>
      <el-form-item label="时间状态">
        <el-select v-model="task.time_status">
          <el-option label="未开始" value="未开始" />
          <el-option label="进行中" value="进行中" />
          <el-option label="已结束" value="已结束" />
        </el-select>
      </el-form-item>
      <el-form-item label="锁定状态">
        <el-switch v-model="task.is_locked" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSave">保存</el-button>
        <el-button @click="$router.back()">返回</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

interface Task {
  id: string
  name: string
  description: string
  priority: number
  status: string
  time_status: string
  is_locked: boolean
  create_time: string
  update_time: string
}

const route = useRoute()
const router = useRouter()
const task = ref<Task>({
  id: '',
  name: '',
  description: '',
  priority: 1,
  status: '待完成',
  time_status: '未开始',
  is_locked: false,
  create_time: '',
  update_time: ''
})

const fetchTask = async () => {
  try {
    const response = await axios.get(`/api/tasks/${route.params.id}`)
    task.value = response.data
  } catch (error) {
    console.error('获取任务详情失败:', error)
    ElMessage.error('获取任务详情失败')
  }
}

const handleSave = async () => {
  try {
    await axios.put(`/api/tasks/${task.value.id}`, task.value)
    ElMessage.success('任务更新成功')
    router.back()
  } catch (error) {
    console.error('更新任务失败:', error)
    ElMessage.error('更新任务失败')
  }
}

onMounted(() => {
  fetchTask()
})
</script>

<style scoped>
.task-detail {
  padding: 20px;
}
</style> 