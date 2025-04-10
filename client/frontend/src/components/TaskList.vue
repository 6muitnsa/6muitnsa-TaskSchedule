<template>
  <div class="task-list">
    <el-table :data="tasks" style="width: 100%">
      <el-table-column prop="name" label="任务名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="priority" label="优先级" />
      <el-table-column prop="status" label="状态" />
      <el-table-column prop="time_status" label="时间状态" />
      <el-table-column prop="create_time" label="创建时间" />
      <el-table-column prop="update_time" label="更新时间" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-button type="primary" @click="showCreateDialog = true">新建任务</el-button>

    <el-dialog v-model="showCreateDialog" title="新建任务">
      <el-form :model="newTask" label-width="80px">
        <el-form-item label="任务名称">
          <el-input v-model="newTask.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="newTask.description" type="textarea" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-input-number v-model="newTask.priority" :min="1" :max="10" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="handleCreate">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

interface Task {
  id: string
  name: string
  description: string
  priority: number
  status: string
  time_status: string
  create_time: string
  update_time: string
}

const router = useRouter()
const tasks = ref<Task[]>([])
const showCreateDialog = ref(false)
const newTask = ref({
  name: '',
  description: '',
  priority: 1,
  status: '待完成',
  time_status: '未开始'
})

const fetchTasks = async () => {
  try {
    const response = await axios.get('/api/tasks/')
    tasks.value = response.data.map((task: any) => ({
      ...task,
      create_time: new Date(task.create_time).toLocaleString(),
      update_time: new Date(task.update_time).toLocaleString()
    }))
  } catch (error) {
    console.error('获取任务列表失败:', error)
    ElMessage.error('获取任务列表失败')
  }
}

const handleCreate = async () => {
  try {
    await axios.post('/api/tasks/', newTask.value)
    showCreateDialog.value = false
    newTask.value = {
      name: '',
      description: '',
      priority: 1,
      status: '待完成',
      time_status: '未开始'
    }
    ElMessage.success('任务创建成功')
    fetchTasks()
  } catch (error) {
    console.error('创建任务失败:', error)
    ElMessage.error('创建任务失败')
  }
}

const handleEdit = (task: Task) => {
  router.push(`/tasks/${task.id}`)
}

const handleDelete = async (task: Task) => {
  try {
    await axios.delete(`/api/tasks/${task.id}`)
    ElMessage.success('任务删除成功')
    fetchTasks()
  } catch (error) {
    console.error('删除任务失败:', error)
    ElMessage.error('删除任务失败')
  }
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.task-list {
  padding: 20px;
}
</style> 