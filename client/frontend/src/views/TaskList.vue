<template>
  <div class="task-list">
    <div class="task-header">
      <h2>任务列表</h2>
      <div class="header-actions">
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
        <el-button type="primary" @click="showCreateDialog">
          <el-icon><Plus /></el-icon>
          创建任务
        </el-button>
      </div>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="优先级">
          <el-select v-model="filterForm.priority" placeholder="选择优先级" clearable>
            <el-option label="高" :value="3000" />
            <el-option label="中" :value="2000" />
            <el-option label="低" :value="1000" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="选择状态" clearable>
            <el-option label="待完成" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间类型">
          <el-select v-model="filterForm.time_type" placeholder="选择时间类型" clearable>
            <el-option label="固定时间" value="fixed" />
            <el-option label="灵活时间" value="flexible" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="applyFilters">筛选</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-loading="loading">
      <template v-if="filteredTasks.length > 0">
        <el-table :data="filteredTasks" style="width: 100%">
          <el-table-column prop="name" label="任务名称" min-width="200">
            <template #default="{ row }">
              <el-link type="primary" @click="viewTaskDetail(row)">
                {{ row.name }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column prop="priority" label="优先级" width="100">
            <template #default="{ row }">
              <el-tag :type="getPriorityType(row.priority)">
                {{ getPriorityText(row.priority) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="estimated_time" label="预计时间" width="120">
            <template #default="{ row }">
              {{ row.estimated_time }}分钟
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="time_type" label="时间类型" width="120">
            <template #default="{ row }">
              {{ getTimeTypeText(row.time_type) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button
                  size="small"
                  type="primary"
                  @click="startPomodoro(row)"
                  :disabled="row.status === 'completed'"
                >
                  番茄钟
                </el-button>
                <el-button
                  size="small"
                  @click="editTask(row)"
                  :disabled="row.status === 'completed'"
                >
                  编辑
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="deleteTask(row)"
                >
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="totalTasks"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </template>
      <el-empty v-else description="暂无任务" />
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '创建任务' : '编辑任务'"
      width="50%"
    >
      <TaskForm
        v-if="dialogVisible"
        :task="currentTask"
        @submit="handleSubmit"
        @cancel="dialogVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import axios from 'axios'
import TaskForm from '../components/TaskForm.vue'

const router = useRouter()
const loading = ref(false)
const tasks = ref([])
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogType = ref('create')
const currentTask = ref(null)

const filterForm = ref({
  priority: null,
  status: null,
  time_type: null
})

const filteredTasks = computed(() => {
  let result = tasks.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(task => 
      task.name.toLowerCase().includes(query) ||
      task.description.toLowerCase().includes(query)
    )
  }

  if (filterForm.value.priority) {
    result = result.filter(task => task.priority === filterForm.value.priority)
  }

  if (filterForm.value.status) {
    result = result.filter(task => task.status === filterForm.value.status)
  }

  if (filterForm.value.time_type) {
    result = result.filter(task => task.time_type === filterForm.value.time_type)
  }

  return result
})

const totalTasks = computed(() => filteredTasks.value.length)

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

const getStatusType = (status) => {
  switch (status) {
    case 'completed':
      return 'success'
    case 'in_progress':
      return 'warning'
    default:
      return 'info'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'completed':
      return '已完成'
    case 'in_progress':
      return '进行中'
    default:
      return '待完成'
  }
}

const getTimeTypeText = (timeType) => {
  return timeType === 'fixed' ? '固定时间' : '灵活时间'
}

const showCreateDialog = () => {
  dialogType.value = 'create'
  currentTask.value = null
  dialogVisible.value = true
}

const editTask = (task) => {
  dialogType.value = 'edit'
  currentTask.value = task
  dialogVisible.value = true
}

const viewTaskDetail = (task) => {
  router.push(`/tasks/${task.id}`)
}

const deleteTask = async (task) => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
      type: 'warning'
    })
    await axios.delete(`/api/tasks/${task.id}`)
    ElMessage.success('删除成功')
    loadTasks()
  } catch {
    // 用户取消删除
  }
}

const startPomodoro = (task) => {
  router.push(`/pomodoro?taskId=${task.id}`)
}

const handleSubmit = async (taskData) => {
  try {
    if (dialogType.value === 'create') {
      await axios.post('/api/tasks', taskData)
      ElMessage.success('创建成功')
    } else {
      await axios.put(`/api/tasks/${taskData.id}`, taskData)
      ElMessage.success('编辑成功')
    }
    dialogVisible.value = false
    loadTasks()
  } catch (error) {
    ElMessage.error('操作失败，请重试')
  }
}

const applyFilters = () => {
  currentPage.value = 1
  loadTasks()
}

const resetFilters = () => {
  filterForm.value = {
    priority: null,
    status: null,
    time_type: null
  }
  currentPage.value = 1
  loadTasks()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  loadTasks()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  loadTasks()
}

const loadTasks = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/tasks', {
      params: {
        page: currentPage.value,
        page_size: pageSize.value,
        ...filterForm.value
      }
    })
    tasks.value = response.data
  } catch (error) {
    ElMessage.error('加载任务列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTasks()
})
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

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-input {
  width: 300px;
}

.filter-card {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 