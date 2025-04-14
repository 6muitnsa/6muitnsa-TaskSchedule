<template>
  <div class="task-list">
    <el-card class="task-card">
      <template #header>
        <div class="card-header">
          <span>任务列表</span>
          <el-button type="primary" @click="showCreateDialog">新建任务</el-button>
        </div>
      </template>
      
      <el-table :data="tasks" style="width: 100%">
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="scope">
            <el-tag :type="getPriorityType(scope.row.priority)">
              {{ getPriorityText(scope.row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="timeStatus" label="时间状态" width="120">
          <template #default="scope">
            <el-tag :type="getTimeStatusType(scope.row.timeStatus)">
              {{ getTimeStatusText(scope.row.timeStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="count" label="计数" width="80">
          <template #default="scope">
            {{ scope.row.count }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 任务表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '新建任务' : '编辑任务'"
      width="50%"
    >
      <el-form :model="taskForm" label-width="100px">
        <el-form-item label="任务名称" required>
          <el-input v-model="taskForm.name" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="taskForm.description" type="textarea" maxlength="500" show-word-limit />
        </el-form-item>
        <el-form-item label="优先级" required>
          <el-select v-model="taskForm.priority">
            <el-option label="高" :value="Priority.HIGH" />
            <el-option label="中" :value="Priority.MEDIUM" />
            <el-option label="低" :value="Priority.LOW" />
          </el-select>
        </el-form-item>
        <el-form-item label="预计时间">
          <el-input-number v-model="taskForm.estimatedTime" :min="0" :max="1440" :step="15" />
          <span class="unit">分钟</span>
        </el-form-item>
        <el-form-item label="开始时间">
          <el-date-picker
            v-model="taskForm.startTime"
            type="datetime"
            placeholder="选择开始时间"
          />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-date-picker
            v-model="taskForm.endTime"
            type="datetime"
            placeholder="选择结束时间"
          />
        </el-form-item>
        <el-form-item label="计数">
          <el-input-number v-model="taskForm.count" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { TaskStatus, TimeStatus, Priority, TaskStatusText, TimeStatusText, PriorityText } from '../types/task'
import type { Task, TaskFormData } from '../types/task'
import { taskService } from '../services/taskService'

const tasks = ref<Task[]>([])
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const currentTaskId = ref<string>('')
const taskForm = ref<TaskFormData>({
  name: '',
  priority: Priority.MEDIUM,
  estimatedTime: 30,
  status: TaskStatus.PENDING,
  timeStatus: TimeStatus.NOT_STARTED,
  count: 0,
  isLocked: false
})

const getPriorityType = (priority: Priority) => {
  switch (priority) {
    case Priority.HIGH:
      return 'danger'
    case Priority.MEDIUM:
      return 'warning'
    case Priority.LOW:
      return 'info'
    default:
      return ''
  }
}

const getStatusType = (status: TaskStatus) => {
  switch (status) {
    case TaskStatus.COMPLETED:
      return 'success'
    case TaskStatus.CANCELLED:
      return 'info'
    case TaskStatus.FOLLOW_UP:
      return 'warning'
    case TaskStatus.PENDING:
      return ''
    default:
      return ''
  }
}

const getTimeStatusType = (timeStatus: TimeStatus) => {
  switch (timeStatus) {
    case TimeStatus.COMPLETED:
      return 'success'
    case TimeStatus.OVERDUE:
      return 'danger'
    case TimeStatus.IN_PROGRESS:
      return 'warning'
    case TimeStatus.NOT_STARTED:
      return ''
    default:
      return ''
  }
}

const getStatusText = (status: TaskStatus): string => {
  return TaskStatusText[status]
}

const getTimeStatusText = (timeStatus: TimeStatus): string => {
  return TimeStatusText[timeStatus]
}

const getPriorityText = (priority: Priority): string => {
  return PriorityText[priority]
}

const fetchTasks = async () => {
  try {
    tasks.value = await taskService.getTasks()
  } catch (error) {
    console.error('获取任务列表失败:', error)
    ElMessage.error('获取任务列表失败')
  }
}

const showCreateDialog = () => {
  dialogType.value = 'create'
  currentTaskId.value = ''
  taskForm.value = {
    name: '',
    priority: Priority.MEDIUM,
    estimatedTime: 30,
    status: TaskStatus.PENDING,
    timeStatus: TimeStatus.NOT_STARTED,
    count: 0,
    isLocked: false
  }
  dialogVisible.value = true
}

const handleEdit = (task: Task) => {
  dialogType.value = 'edit'
  currentTaskId.value = task.id
  taskForm.value = {
    name: task.name,
    description: task.description,
    priority: task.priority,
    startTime: task.startTime,
    endTime: task.endTime,
    type: task.type,
    cycle: task.cycle,
    estimatedTime: task.estimatedTime,
    status: task.status,
    timeStatus: task.timeStatus,
    count: task.count,
    isLocked: task.isLocked
  }
  dialogVisible.value = true
}

const handleDelete = async (task: Task) => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await taskService.deleteTask(task.id)
    ElMessage.success('删除成功')
    fetchTasks()
  } catch (error) {
    if (error === 'cancel') {
      return
    }
    console.error('删除任务失败:', error)
    ElMessage.error('删除任务失败')
  }
}

const handleSubmit = async () => {
  try {
    if (!taskForm.value.name) {
      ElMessage.warning('请输入任务名称')
      return
    }
    if (taskForm.value.name.length > 100) {
      ElMessage.warning('任务名称不能超过100个字符')
      return
    }
    if (taskForm.value.description && taskForm.value.description.length > 500) {
      ElMessage.warning('任务描述不能超过500个字符')
      return
    }
    if (taskForm.value.estimatedTime && (taskForm.value.estimatedTime < 0 || taskForm.value.estimatedTime > 1440)) {
      ElMessage.warning('预计时间必须在0-1440分钟之间')
      return
    }
    if (taskForm.value.count < 0) {
      ElMessage.warning('计数不能为负数')
      return
    }
    if (taskForm.value.startTime && taskForm.value.endTime && taskForm.value.startTime > taskForm.value.endTime) {
      ElMessage.warning('结束时间必须晚于开始时间')
      return
    }
    if (dialogType.value === 'create') {
      await taskService.createTask(taskForm.value)
      ElMessage.success('创建成功')
    } else {
      await taskService.updateTask(currentTaskId.value, taskForm.value)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    fetchTasks()
  } catch (error) {
    console.error('保存任务失败:', error)
    ElMessage.error('保存任务失败')
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.unit {
  margin-left: 10px;
  color: #666;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 