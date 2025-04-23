<template>
  <div class="task-list">
    <div class="task-header">
      <h2>任务列表</h2>
      <el-button type="primary" @click="createTask">创建任务</el-button>
    </div>

    <el-table :data="tasks" style="width: 100%">
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
      <el-table-column prop="period_type" label="周期类型">
        <template #default="{ row }">
          {{ getPeriodTypeText(row.period_type) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
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

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑任务' : '创建任务'"
      width="50%"
    >
      <task-form
        v-if="dialogVisible"
        :task="selectedTask"
        @submit="handleSubmit"
        @cancel="dialogVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '../store/task'
import TaskForm from './TaskForm.vue'

const router = useRouter()
const taskStore = useTaskStore()

const tasks = ref([])
const dialogVisible = ref(false)
const selectedTask = ref(null)
const isEdit = ref(false)

onMounted(async () => {
  await taskStore.fetchTasks()
  tasks.value = taskStore.getTasks
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

const getPeriodTypeText = (type) => {
  const map = {
    once: '一次性',
    daily: '每日',
    weekly: '每周',
    monthly: '每月'
  }
  return map[type] || type
}

const createTask = () => {
  isEdit.value = false
  selectedTask.value = null
  dialogVisible.value = true
}

const editTask = (task) => {
  isEdit.value = true
  selectedTask.value = task
  dialogVisible.value = true
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

const handleSubmit = async (taskData) => {
  try {
    if (isEdit.value) {
      await taskStore.updateTask(selectedTask.value.id, taskData)
      ElMessage.success('更新成功')
    } else {
      await taskStore.createTask(taskData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await taskStore.fetchTasks()
    tasks.value = taskStore.getTasks
  } catch (error) {
    ElMessage.error(error.message || '操作失败')
  }
}
</script>

<style scoped>
.task-list {
  padding: 20px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 