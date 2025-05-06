<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">任务列表</div>
    </div>
    
    <div class="task-toolbar">
      <el-button type="primary" @click="handleAddTask">
        <el-icon><Plus /></el-icon>新建任务
      </el-button>
      <el-input
        v-model="searchQuery"
        placeholder="搜索任务"
        class="search-input"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <el-tabs v-model="activeTab" class="task-tabs">
      <el-tab-pane label="列表视图" name="list">
        <el-table :data="filteredTasks" style="width: 100%">
          <el-table-column prop="name" label="任务名称" min-width="200" />
          <el-table-column prop="priority" label="优先级" width="120">
            <template #default="{ row }">
              <el-tag :type="getPriorityType(row.priority)">
                {{ getPriorityLabel(row.priority) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="startTime" label="开始时间" width="180" />
          <el-table-column prop="endTime" label="结束时间" width="180" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button size="small" @click="handleEditTask(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="handleDeleteTask(row)">删除</el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="月度视图" name="month">
        <div class="calendar-container">
          <!-- 日历组件将在这里实现 -->
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 任务表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新建任务' : '编辑任务'"
      width="600px"
    >
      <el-form
        ref="taskForm"
        :model="taskForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称" />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="taskForm.priority" placeholder="请选择优先级">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" prop="startTime">
          <el-date-picker
            v-model="taskForm.startTime"
            type="datetime"
            placeholder="选择开始时间"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="endTime">
          <el-date-picker
            v-model="taskForm.endTime"
            type="datetime"
            placeholder="选择结束时间"
          />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入任务描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitTask">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Plus, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 状态
const activeTab = ref('list')
const searchQuery = ref('')
const dialogVisible = ref(false)
const dialogType = ref('add')
const taskForm = ref({
  name: '',
  priority: 'medium',
  startTime: '',
  endTime: '',
  description: ''
})

// 模拟数据
const tasks = ref([
  {
    id: 1,
    name: '完成项目文档',
    priority: 'high',
    startTime: '2024-03-20 09:00',
    endTime: '2024-03-20 18:00',
    status: 'pending',
    description: '编写项目需求文档和设计文档'
  },
  {
    id: 2,
    name: '代码审查',
    priority: 'medium',
    startTime: '2024-03-21 14:00',
    endTime: '2024-03-21 16:00',
    status: 'in_progress',
    description: '审查团队成员的代码提交'
  }
])

// 计算属性
const filteredTasks = computed(() => {
  if (!searchQuery.value) return tasks.value
  return tasks.value.filter(task =>
    task.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 方法
const getPriorityType = (priority) => {
  const types = {
    low: 'info',
    medium: 'warning',
    high: 'danger'
  }
  return types[priority] || 'info'
}

const getPriorityLabel = (priority) => {
  const labels = {
    low: '低',
    medium: '中',
    high: '高'
  }
  return labels[priority] || '未知'
}

const getStatusType = (status) => {
  const types = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success'
  }
  return types[status] || 'info'
}

const getStatusLabel = (status) => {
  const labels = {
    pending: '待开始',
    in_progress: '进行中',
    completed: '已完成'
  }
  return labels[status] || '未知'
}

const handleAddTask = () => {
  dialogType.value = 'add'
  taskForm.value = {
    name: '',
    priority: 'medium',
    startTime: '',
    endTime: '',
    description: ''
  }
  dialogVisible.value = true
}

const handleEditTask = (task) => {
  dialogType.value = 'edit'
  taskForm.value = { ...task }
  dialogVisible.value = true
}

const handleDeleteTask = (task) => {
  ElMessageBox.confirm(
    '确定要删除这个任务吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    tasks.value = tasks.value.filter(t => t.id !== task.id)
    ElMessage.success('删除成功')
  })
}

const handleSubmitTask = () => {
  // 这里应该添加表单验证
  if (dialogType.value === 'add') {
    const newTask = {
      id: tasks.value.length + 1,
      ...taskForm.value,
      status: 'pending'
    }
    tasks.value.push(newTask)
  } else {
    const index = tasks.value.findIndex(t => t.id === taskForm.value.id)
    if (index !== -1) {
      tasks.value[index] = { ...taskForm.value }
    }
  }
  dialogVisible.value = false
  ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
}
</script>

<style lang="scss" scoped>
.task-toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  
  .search-input {
    width: 300px;
  }
}

.task-tabs {
  margin-top: 20px;
}

.calendar-container {
  min-height: 500px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 20px;
}
</style> 