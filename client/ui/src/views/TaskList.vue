<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">任务列表</div>
      <div class="page-actions">
        <el-button type="primary" @click="handleCreateTask">
          <el-icon><Plus /></el-icon>创建任务
        </el-button>
      </div>
    </div>

    <div class="task-toolbar">
      <el-form :inline="true" :model="filterForm">
        <el-form-item>
          <el-input
            v-model="filterForm.search"
            placeholder="搜索任务"
            clearable
            @clear="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filterForm.view" placeholder="视图" @change="handleViewChange">
            <el-option label="列表视图" value="list" />
            <el-option label="月度视图" value="month" />
            <el-option label="优先级视图" value="priority" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filterForm.tags" multiple placeholder="标签" clearable>
            <el-option
              v-for="tag in availableTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filterForm.location" placeholder="地点" clearable>
            <el-option
              v-for="location in availableLocations"
              :key="location"
              :label="location"
              :value="location"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filterForm.status" placeholder="状态" clearable>
            <el-option label="未开始" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 列表视图 -->
    <div v-if="filterForm.view === 'list'" class="task-list">
      <el-table :data="tasks" style="width: 100%">
        <el-table-column prop="title" label="任务名称" min-width="200">
          <template #default="{ row }">
            <div class="task-title" @click="handleTaskClick(row)">
              {{ row.title }}
              <el-tag
                v-for="tag in row.tags"
                :key="tag"
                size="small"
                class="task-tag"
              >
                {{ tag }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.start_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="end_time" label="结束时间" width="180">
          <template #default="{ row }">
            <template v-if="row.isUnlimited">
              完成次数：{{ row.completionCount }}/{{ row.requiredCount }}
            </template>
            <template v-else>
              {{ formatDateTime(row.end_time) }}
            </template>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="120">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)">
              {{ row.priority }}
            </el-tag>
          </template>
        </el-table-column>
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
              <el-button type="primary" link @click="handleEdit(row)">
                编辑
              </el-button>
              <el-button type="success" link @click="handleComplete(row)">
                完成
              </el-button>
              <el-button type="danger" link @click="handleAbandon(row)">
                放弃
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 月度视图 -->
    <div v-else-if="filterForm.view === 'month'" class="task-month">
      <el-calendar v-model="currentDate">
        <template #dateCell="{ data }">
          <div class="calendar-cell">
            <p>{{ data.day.split('-').slice(2).join('') }}</p>
            <div class="task-list">
              <div
                v-for="task in getTasksByDate(data.day)"
                :key="task.id"
                class="task-item"
                :class="getTaskStatusClass(task)"
                @click="handleTaskClick(task)"
              >
                {{ task.title }}
              </div>
            </div>
          </div>
        </template>
      </el-calendar>
    </div>

    <!-- 优先级视图 -->
    <div v-else class="task-priority">
      <div v-for="priority in priorityRanges" :key="priority.name" class="priority-group">
        <div class="priority-header">
          <h3>{{ priority.name }}</h3>
          <span class="priority-range">{{ priority.min }} - {{ priority.max }}</span>
        </div>
        <div class="task-list">
          <div
            v-for="task in getTasksByPriority(priority.min, priority.max)"
            :key="task.id"
            class="task-item"
            :class="getTaskStatusClass(task)"
            @click="handleTaskClick(task)"
          >
            <div class="task-info">
              <span class="task-title">{{ task.title }}</span>
              <span class="task-priority">{{ task.priority }}</span>
            </div>
            <div class="task-time">
              <template v-if="task.isUnlimited">
                完成次数：{{ task.completionCount }}/{{ task.requiredCount }}
              </template>
              <template v-else>
                {{ formatDateTime(task.start_time) }} - {{ formatDateTime(task.end_time) }}
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务详情对话框 -->
    <el-dialog
      v-model="taskDialogVisible"
      :title="selectedTask?.title"
      width="500px"
    >
      <div v-if="selectedTask" class="task-detail">
        <div class="detail-item">
          <span class="label">开始时间：</span>
          <span class="value">{{ formatDateTime(selectedTask.start_time) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">结束时间：</span>
          <span class="value">{{ selectedTask.isUnlimited ? '无时间限制' : formatDateTime(selectedTask.end_time) }}</span>
        </div>
        <div class="detail-item">
          <span class="label">优先级：</span>
          <span class="value">{{ selectedTask.priority }}</span>
        </div>
        <div class="detail-item">
          <span class="label">状态：</span>
          <el-tag :type="getStatusType(selectedTask.status)">
            {{ getStatusLabel(selectedTask.status) }}
          </el-tag>
        </div>
        <div class="detail-item" v-if="selectedTask.isUnlimited">
          <span class="label">完成次数：</span>
          <span class="value">{{ selectedTask.completionCount }}/{{ selectedTask.requiredCount }}</span>
        </div>
        <div class="detail-item">
          <span class="label">描述：</span>
          <span class="value">{{ selectedTask.description || '无' }}</span>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="taskDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleEdit(selectedTask)">编辑</el-button>
          <el-button type="success" @click="handleComplete(selectedTask)">完成</el-button>
          <el-button type="danger" @click="handleAbandon(selectedTask)">放弃</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import axios from 'axios'

// 过滤表单
const filterForm = ref({
  search: '',
  view: 'list',
  tags: [],
  location: '',
  status: ''
})

// 任务数据
const tasks = ref([])
const availableTags = ref([])
const availableLocations = ref([])
const currentDate = ref(new Date())

// 任务对话框
const taskDialogVisible = ref(false)
const selectedTask = ref(null)

// 优先级区间
const priorityRanges = ref([
  { name: '高优先级', min: 4000, max: 5000 },
  { name: '中优先级', min: 2000, max: 3999 },
  { name: '低优先级', min: 0, max: 1999 }
])

// 格式化日期时间
const formatDateTime = (datetime) => {
  if (!datetime) return '未设置'
  return new Date(datetime).toLocaleString()
}

// 获取优先级类型
const getPriorityType = (priority) => {
  if (priority >= 4000) return 'danger'
  if (priority >= 2000) return 'warning'
  return 'info'
}

// 获取状态标签
const getStatusLabel = (status) => {
  const labels = {
    pending: '未开始',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return labels[status] || '未知'
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

// 获取任务状态类名
const getTaskStatusClass = (task) => {
  return {
    'task-completed': task.status === 'completed',
    'task-cancelled': task.status === 'cancelled',
    'task-in-progress': task.status === 'in_progress'
  }
}

// 获取指定日期的任务
const getTasksByDate = (date) => {
  return tasks.value.filter(task => {
    const taskDate = new Date(task.start_time).toISOString().split('T')[0]
    return taskDate === date
  })
}

// 获取指定优先级范围的任务
const getTasksByPriority = (min, max) => {
  return tasks.value.filter(task => task.priority >= min && task.priority <= max)
}

// 处理视图切换
const handleViewChange = (value) => {
  filterForm.value.view = value
  loadTasks()
}

// 处理搜索
const handleSearch = () => {
  loadTasks()
}

// 处理重置
const handleReset = () => {
  filterForm.value = {
    search: '',
    view: 'list',
    tags: [],
    location: '',
    status: ''
  }
  loadTasks()
}

// 加载任务
const loadTasks = async () => {
  try {
    const response = await axios.get('/api/tasks', { params: filterForm.value })
    tasks.value = response.data.tasks
    availableTags.value = response.data.tags
    availableLocations.value = response.data.locations
  } catch (error) {
    ElMessage.error('加载任务失败：' + error.message)
  }
}

// 处理任务点击
const handleTaskClick = (task) => {
  selectedTask.value = task
  taskDialogVisible.value = true
}

// 处理创建任务
const handleCreateTask = () => {
  // TODO: 跳转到创建任务页面
}

// 处理编辑任务
const handleEdit = (task) => {
  // TODO: 跳转到编辑任务页面
}

// 处理完成任务
const handleComplete = async (task) => {
  try {
    if (task.isUnlimited) {
      const { value: count } = await ElMessageBox.prompt(
        '请输入完成次数',
        '完成任务',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^[1-9]\d*$/,
          inputErrorMessage: '请输入有效的完成次数'
        }
      )
      await axios.post(`/api/tasks/${task.id}/complete`, { count: parseInt(count) })
    } else {
      await axios.post(`/api/tasks/${task.id}/complete`)
    }
    ElMessage.success('任务已完成')
    loadTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败：' + error.message)
    }
  }
}

// 处理放弃任务
const handleAbandon = async (task) => {
  try {
    await ElMessageBox.confirm(
      '确定要放弃此任务吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await axios.post(`/api/tasks/${task.id}/abandon`)
    ElMessage.success('任务已放弃')
    loadTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败：' + error.message)
    }
  }
}

// 初始化
onMounted(() => {
  loadTasks()
})
</script>

<style lang="scss" scoped>
.page-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.task-toolbar {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
}

.task-list {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;

  .task-title {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;

    .task-tag {
      margin-left: 8px;
    }
  }
}

.task-month {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;

  .calendar-cell {
    height: 100%;
    min-height: 100px;

    .task-list {
      margin-top: 8px;
    }

    .task-item {
      padding: 4px 8px;
      margin-bottom: 4px;
      border-radius: 4px;
      background-color: #f5f7fa;
      cursor: pointer;
      font-size: 12px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;

      &.task-completed {
        background-color: #f0f9eb;
        color: #67c23a;
      }

      &.task-cancelled {
        background-color: #fef0f0;
        color: #f56c6c;
      }

      &.task-in-progress {
        background-color: #fdf6ec;
        color: #e6a23c;
      }
    }
  }
}

.task-priority {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;

  .priority-group {
    margin-bottom: 20px;

    .priority-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      padding-bottom: 10px;
      border-bottom: 1px solid #ebeef5;

      h3 {
        margin: 0;
      }

      .priority-range {
        color: #909399;
        font-size: 14px;
      }
    }

    .task-list {
      .task-item {
        padding: 12px;
        margin-bottom: 8px;
        border-radius: 4px;
        background-color: #f5f7fa;
        cursor: pointer;

        .task-info {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;

          .task-title {
            font-weight: bold;
          }

          .task-priority {
            color: #909399;
          }
        }

        .task-time {
          font-size: 12px;
          color: #606266;
        }

        &.task-completed {
          background-color: #f0f9eb;
        }

        &.task-cancelled {
          background-color: #fef0f0;
        }

        &.task-in-progress {
          background-color: #fdf6ec;
        }
      }
    }
  }
}

.task-detail {
  .detail-item {
    margin-bottom: 16px;

    .label {
      color: #606266;
      margin-right: 8px;
    }

    .value {
      color: #303133;
    }
  }
}
</style> 