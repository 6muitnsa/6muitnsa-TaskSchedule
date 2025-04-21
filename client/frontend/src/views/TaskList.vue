<template>
  <div class="task-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务列表</span>
          <el-button type="primary" @click="$router.push('/create')">
            <el-icon><Plus /></el-icon>新建任务
          </el-button>
        </div>
      </template>

      <!-- 视图切换 -->
      <div class="view-switch">
        <el-radio-group v-model="viewMode">
          <el-radio-button label="list">列表视图</el-radio-button>
          <el-radio-button label="month">月视图</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 任务统计 -->
      <el-card class="statistics" shadow="never">
        <div class="stat-container">
          <div class="stat-item">
            <span class="label">总任务数</span>
            <span class="value">{{ totalTasks }}</span>
          </div>
          <div class="stat-item">
            <span class="label">完成率</span>
            <span class="value">{{ completionRate }}%</span>
          </div>
          <div class="stat-item">
            <span class="label">平均满意度</span>
            <span class="value">{{ averageSatisfaction }}</span>
          </div>
        </div>
      </el-card>

      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="状态">
          <el-select v-model="filterForm.status" placeholder="选择状态" clearable>
            <el-option label="待完成" value="pending" />
            <el-option label="已完成" value="completed" />
            <el-option label="待跟进" value="follow_up" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间状态">
          <el-select v-model="filterForm.time_status" placeholder="选择时间状态" clearable>
            <el-option label="未开始" value="not_started" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已超时" value="overdue" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间段">
          <el-select v-model="filterForm.time_slot" placeholder="选择时间段" clearable>
            <el-option label="固定时间" value="fixed" />
            <el-option label="灵活时间" value="flexible" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">筛选</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 列表视图 -->
      <template v-if="viewMode === 'list'">
        <el-table :data="tasks" style="width: 100%" v-loading="loading">
          <el-table-column prop="name" label="任务名称" />
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="priority" label="优先级" sortable />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="time_status" label="时间状态">
            <template #default="{ row }">
              <el-tag :type="getTimeStatusType(row.time_status)">
                {{ getTimeStatusText(row.time_status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="time_slot" label="时间段">
            <template #default="{ row }">
              <el-tag :type="row.time_slot === 'fixed' ? 'danger' : 'success'">
                {{ row.time_slot === 'fixed' ? '固定时间' : '灵活时间' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button-group>
                <el-button type="primary" size="small" @click="handleEdit(row)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click="handleDelete(row)">
                  删除
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </template>

      <!-- 月视图 -->
      <template v-else>
        <div class="calendar-container">
          <el-calendar v-model="currentDate">
            <template #dateCell="{ data }">
              <div class="calendar-cell">
                <div class="date">{{ data.day.split('-').slice(2).join('-') }}</div>
                <div class="tasks">
                  <div 
                    v-for="task in getTasksForDate(data.day)" 
                    :key="task.id" 
                    class="task-item"
                    :class="{
                      'fixed-time': task.time_slot === 'fixed',
                      'flexible-time': task.time_slot === 'flexible',
                      'locked': task.is_locked
                    }"
                  >
                    <div class="task-time">{{ formatTime(task.start_time) }}</div>
                    <div class="task-name">{{ task.name }}</div>
                    <div class="task-status" :class="getStatusClass(task.status)">
                      {{ getStatusText(task.status) }}
                    </div>
                    <div class="task-priority">优先级: {{ task.priority }}</div>
                  </div>
                </div>
              </div>
            </template>
          </el-calendar>
        </div>
      </template>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { taskApi } from '../api/task'

const router = useRouter()
const loading = ref(false)
const tasks = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const viewMode = ref('list')
const currentDate = ref(new Date())

const filterForm = ref({
  status: '',
  time_status: '',
  time_slot: ''
})

// 统计相关
const totalTasks = computed(() => tasks.value.length)
const completionRate = computed(() => {
  const completed = tasks.value.filter(t => t.status === 'completed').length
  return totalTasks.value ? Math.round((completed / totalTasks.value) * 100) : 0
})
const averageSatisfaction = computed(() => {
  const tasksWithFeedback = tasks.value.filter(t => t.feedback)
  return tasksWithFeedback.length
    ? (tasksWithFeedback.reduce((sum, t) => sum + t.feedback, 0) / tasksWithFeedback.length).toFixed(1)
    : '暂无'
})

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    completed: 'success',
    follow_up: 'info',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待完成',
    completed: '已完成',
    follow_up: '待跟进',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const getTimeStatusType = (status) => {
  const types = {
    not_started: 'info',
    in_progress: 'primary',
    overdue: 'danger',
    completed: 'success'
  }
  return types[status] || 'info'
}

const getTimeStatusText = (status) => {
  const texts = {
    not_started: '未开始',
    in_progress: '进行中',
    overdue: '已超时',
    completed: '已完成'
  }
  return texts[status] || status
}

const getStatusClass = (status) => {
  return `status-${status}`
}

// 获取指定日期的任务
const getTasksForDate = (date) => {
  return tasks.value.filter(task => {
    const taskDate = new Date(task.start_time).toISOString().split('T')[0]
    return taskDate === date
  })
}

const formatTime = (datetime) => {
  if (!datetime) return '未设置'
  return new Date(datetime).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchTasks = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }
    
    if (filterForm.value.status) {
      params.status = filterForm.value.status
    }
    
    if (filterForm.value.time_status) {
      params.time_status = filterForm.value.time_status
    }

    if (filterForm.value.time_slot) {
      params.time_slot = filterForm.value.time_slot
    }
    
    const response = await taskApi.getTasks(params)
    tasks.value = response.data
    total.value = response.headers['x-total-count'] || 0
  } catch (error) {
    ElMessage.error('获取任务列表失败')
    console.error('Error fetching tasks:', error)
  } finally {
    loading.value = false
  }
}

const handleFilter = () => {
  currentPage.value = 1
  fetchTasks()
}

const resetFilter = () => {
  filterForm.value = {
    status: '',
    time_status: '',
    time_slot: ''
  }
  handleFilter()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchTasks()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchTasks()
}

const handleEdit = (row) => {
  router.push(`/task/${row.id}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
      type: 'warning'
    })
    await taskApi.deleteTask(row.id)
    ElMessage.success('删除成功')
    fetchTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
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

.view-switch {
  margin-bottom: 20px;
}

.statistics {
  margin-bottom: 20px;
}

.stat-container {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  text-align: center;
}

.stat-item .label {
  display: block;
  color: #909399;
  font-size: 14px;
  margin-bottom: 5px;
}

.stat-item .value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.filter-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.calendar-container {
  margin-top: 20px;
}

.calendar-cell {
  height: 100%;
  padding: 4px;
}

.calendar-cell .date {
  font-weight: bold;
  margin-bottom: 4px;
}

.calendar-cell .tasks {
  max-height: 100px;
  overflow-y: auto;
}

.task-item {
  font-size: 12px;
  padding: 4px;
  margin-bottom: 4px;
  border-radius: 4px;
  border-left: 3px solid;
}

.fixed-time {
  background-color: #fef0f0;
  border-left-color: #f56c6c;
}

.flexible-time {
  background-color: #f0f9eb;
  border-left-color: #67c23a;
}

.locked {
  background-color: #f4f4f5;
  border-left-color: #909399;
}

.task-time {
  font-weight: bold;
  margin-bottom: 2px;
}

.task-name {
  margin-bottom: 2px;
}

.task-status {
  display: inline-block;
  padding: 0 4px;
  border-radius: 2px;
  font-size: 10px;
  margin-bottom: 2px;
}

.task-priority {
  font-size: 10px;
  color: #909399;
}

.status-pending {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.status-completed {
  background-color: #f0f9eb;
  color: #67c23a;
}

.status-follow_up {
  background-color: #f4f4f5;
  color: #909399;
}

.status-cancelled {
  background-color: #fef0f0;
  color: #f56c6c;
}
</style> 