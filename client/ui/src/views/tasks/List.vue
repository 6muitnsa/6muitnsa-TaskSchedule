<template>
  <div class="task-list-container">
    <!-- 视图切换按钮 -->
    <div class="view-switcher">
      <el-radio-group v-model="currentView">
        <el-radio-button label="list">列表视图</el-radio-button>
        <el-radio-button label="monthly">月度视图</el-radio-button>
        <el-radio-button label="priority">优先级视图</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索任务..."
        clearable
        @clear="handleSearch"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select v-model="tagFilter" placeholder="标签" clearable @change="handleSearch">
        <el-option
          v-for="tag in availableTags"
          :key="tag"
          :label="tag"
          :value="tag"
        />
      </el-select>

      <el-select v-model="locationFilter" placeholder="地点" clearable @change="handleSearch">
        <el-option
          v-for="location in availableLocations"
          :key="location"
          :label="location"
          :value="location"
        />
      </el-select>

      <el-select v-model="statusFilter" placeholder="状态" clearable @change="handleSearch">
        <el-option label="未开始" value="pending" />
        <el-option label="进行中" value="in_progress" />
        <el-option label="已完成" value="completed" />
        <el-option label="已放弃" value="abandoned" />
      </el-select>
    </div>

    <!-- 列表视图 -->
    <div v-if="currentView === 'list'" class="list-view">
      <el-card v-for="task in filteredTasks" :key="task.id" class="task-card">
        <div class="task-header">
          <div class="task-title">
            <h3>{{ task.name }}</h3>
            <el-tag :type="getPriorityType(task.priority)">
              {{ getPriorityText(task.priority) }}
            </el-tag>
          </div>
          <div class="task-tags">
            <el-tag
              v-for="tag in task.tags"
              :key="tag"
              size="small"
              class="task-tag"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>

        <div class="task-info">
          <div class="task-time">
            <span>开始：{{ formatTime(task.start_time) }}</span>
            <span>结束：{{ formatTime(task.end_time) }}</span>
          </div>
          <div class="task-location" v-if="task.location">
            <el-icon><Location /></el-icon>
            <span>{{ task.location }}</span>
          </div>
        </div>

        <div class="task-description" v-if="task.description">
          {{ task.description }}
        </div>

        <div class="task-actions">
          <el-button-group>
            <el-button 
              type="primary" 
              size="small"
              @click="handleComplete(task)"
              :disabled="task.status === 'completed'"
            >
              完成
            </el-button>
            <el-button 
              type="danger" 
              size="small"
              @click="handleAbandon(task)"
              :disabled="task.status === 'abandoned'"
            >
              放弃
            </el-button>
          </el-button-group>
        </div>
      </el-card>
    </div>

    <!-- 月度视图 -->
    <div v-else-if="currentView === 'monthly'" class="monthly-view">
      <el-calendar v-model="currentDate">
        <template #dateCell="{ data }">
          <div class="calendar-cell">
            <p>{{ data.day.split('-').slice(2).join('') }}</p>
            <div class="task-dots">
              <el-tooltip
                v-for="task in getTasksForDate(data.day)"
                :key="task.id"
                :content="task.name"
                placement="top"
              >
                <div 
                  class="task-dot"
                  :style="{ backgroundColor: getPriorityColor(task.priority) }"
                ></div>
              </el-tooltip>
            </div>
          </div>
        </template>
      </el-calendar>
    </div>

    <!-- 优先级视图 -->
    <div v-else class="priority-view">
      <el-timeline>
        <el-timeline-item
          v-for="task in sortedByPriorityTasks"
          :key="task.id"
          :type="getPriorityType(task.priority)"
          :timestamp="formatTime(task.start_time)"
        >
          <el-card class="priority-task-card">
            <h4>{{ task.name }}</h4>
            <p>优先级：{{ task.priority }}</p>
            <p>状态：{{ getStatusText(task.status) }}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Location } from '@element-plus/icons-vue'
import { api } from '@/api'

// 状态
const currentView = ref('list')
const searchQuery = ref('')
const tagFilter = ref('')
const locationFilter = ref('')
const statusFilter = ref('')
const currentDate = ref(new Date())
const tasks = ref([])
const availableTags = ref([])
const availableLocations = ref([])

// 获取任务列表
const fetchTasks = async () => {
  try {
    const response = await api.get('/tasks')
    tasks.value = response.data
    // 提取所有标签和地点
    availableTags.value = [...new Set(tasks.value.flatMap(task => task.tags || []))]
    availableLocations.value = [...new Set(tasks.value.map(task => task.location).filter(Boolean))]
  } catch (error) {
    ElMessage.error('获取任务列表失败')
    console.error(error)
  }
}

// 过滤任务
const filteredTasks = computed(() => {
  let result = tasks.value

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(task => 
      task.name.toLowerCase().includes(query) ||
      task.description?.toLowerCase().includes(query)
    )
  }

  // 标签过滤
  if (tagFilter.value) {
    result = result.filter(task => task.tags?.includes(tagFilter.value))
  }

  // 地点过滤
  if (locationFilter.value) {
    result = result.filter(task => task.location === locationFilter.value)
  }

  // 状态过滤
  if (statusFilter.value) {
    result = result.filter(task => task.status === statusFilter.value)
  }

  return result
})

// 按优先级排序的任务
const sortedByPriorityTasks = computed(() => {
  return [...filteredTasks.value].sort((a, b) => b.priority - a.priority)
})

// 获取指定日期的任务
const getTasksForDate = (date) => {
  return filteredTasks.value.filter(task => {
    const taskDate = new Date(task.start_time).toISOString().split('T')[0]
    return taskDate === date
  })
}

// 工具函数
const formatTime = (time) => {
  if (!time) return '未设置'
  return new Date(time).toLocaleString()
}

const getPriorityType = (priority) => {
  if (priority >= 3000) return 'danger'
  if (priority >= 2000) return 'warning'
  return 'info'
}

const getPriorityText = (priority) => {
  if (priority >= 3000) return '高'
  if (priority >= 2000) return '中'
  return '低'
}

const getPriorityColor = (priority) => {
  if (priority >= 3000) return '#F56C6C'
  if (priority >= 2000) return '#E6A23C'
  return '#909399'
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '未开始',
    in_progress: '进行中',
    completed: '已完成',
    abandoned: '已放弃'
  }
  return statusMap[status] || status
}

// 事件处理
const handleSearch = () => {
  // 搜索逻辑已通过计算属性实现
}

const handleComplete = async (task) => {
  try {
    await api.post(`/tasks/${task.id}/complete`)
    ElMessage.success('任务已完成')
    await fetchTasks()
  } catch (error) {
    ElMessage.error('操作失败')
    console.error(error)
  }
}

const handleAbandon = async (task) => {
  try {
    await api.post(`/tasks/${task.id}/abandon`)
    ElMessage.success('任务已放弃')
    await fetchTasks()
  } catch (error) {
    ElMessage.error('操作失败')
    console.error(error)
  }
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.task-list-container {
  padding: 20px;
}

.view-switcher {
  margin-bottom: 20px;
  text-align: center;
}

.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.task-card {
  margin-bottom: 15px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.task-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.task-title h3 {
  margin: 0;
}

.task-tags {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.task-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  color: #666;
}

.task-time {
  display: flex;
  gap: 20px;
}

.task-location {
  display: flex;
  align-items: center;
  gap: 5px;
}

.task-description {
  margin-bottom: 10px;
  color: #666;
}

.task-actions {
  display: flex;
  justify-content: flex-end;
}

.calendar-cell {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.task-dots {
  display: flex;
  gap: 2px;
  margin-top: 5px;
}

.task-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.priority-task-card {
  margin-bottom: 10px;
}

.priority-task-card h4 {
  margin: 0 0 10px 0;
}

.priority-task-card p {
  margin: 5px 0;
  color: #666;
}
</style> 