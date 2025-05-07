<template>
  <div class="task-list container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务列表</span>
          <div class="header-actions">
            <task-import-export />
            <el-button type="primary" @click="showCreateDialog">
              <el-icon><Plus /></el-icon>
              新建任务
            </el-button>
          </div>
        </div>
      </template>

      <!-- 视图切换和搜索筛选 -->
      <div class="filter-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索任务"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>

        <el-select v-model="filterStatus" placeholder="状态" clearable>
          <el-option label="待处理" value="pending" />
          <el-option label="未开始" value="not_started" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已完成" value="completed" />
          <el-option label="已放弃" value="abandoned" />
        </el-select>

        <el-select v-model="filterPriority" placeholder="优先级" clearable>
          <el-option label="高" value="high" />
          <el-option label="中" value="medium" />
          <el-option label="低" value="low" />
        </el-select>

        <el-select v-model="filterTag" placeholder="标签" clearable>
          <el-option
            v-for="tag in tags"
            :key="tag"
            :label="tag"
            :value="tag"
          />
        </el-select>

        <el-select v-model="filterLocation" placeholder="位置" clearable>
          <el-option
            v-for="location in locations"
            :key="location"
            :label="location"
            :value="location"
          />
        </el-select>

        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button @click="resetFilters">重置</el-button>
      </div>

      <div class="view-switcher">
        <el-radio-group v-model="currentView" size="large">
          <el-radio-button label="list">列表视图</el-radio-button>
          <el-radio-button label="priority">优先级视图</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 批量操作 -->
      <batch-operations
        :selected-tasks="selectedTasks"
        :available-tags="tags"
        :available-locations="locations"
        @operation-complete="handleOperationComplete"
      />

      <!-- 列表视图 -->
      <div v-if="currentView === 'list'" class="list-view">
        <el-table
          :data="filteredTasks"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="title" label="任务名称" min-width="200">
            <template #default="{ row }">
              <div class="task-name">
                <span>{{ row.title }}</span>
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
          <el-table-column prop="created_at" label="创建时间" width="180" />
          <el-table-column prop="due_date" label="截止时间" width="180">
            <template #default="{ row }">
              <span v-if="row.due_date">{{ row.due_date }}</span>
              <span v-else>完成次数: {{ row.completionCount }}/{{ row.requiredCount }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button-group>
                <el-button size="small" @click="handleEdit(row)">编辑</el-button>
                <el-button size="small" type="success" @click="handleComplete(row)">完成</el-button>
                <el-button size="small" type="danger" @click="handleAbandon(row)">放弃</el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 月度视图 -->
      <div v-else-if="currentView === 'month'" class="month-view">
        <el-calendar v-model="currentDate">
          <template #dateCell="{ data }">
            <div class="calendar-cell">
              <p>{{ data.day.split('-').slice(2).join('') }}</p>
              <div class="task-dots">
                <el-tooltip
                  v-for="task in getTasksForDate(data.day)"
                  :key="task.id"
                  :content="task.title"
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
            v-for="task in sortedTasks"
            :key="task.id"
            :type="getPriorityType(task.priority)"
            :timestamp="task.created_at"
          >
            <el-card>
              <div class="task-header">
                <h4>{{ task.title }}</h4>
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
                <p>创建时间: {{ task.created_at }}</p>
                <p>开始时间: {{ task.startTime }}</p>
                <p v-if="task.endTime">结束时间: {{ task.endTime }}</p>
                <p v-else>完成次数: {{ task.completionCount }}/{{ task.requiredCount }}</p>
                <p>状态: {{ getStatusText(task.status) }}</p>
              </div>
              <div class="task-actions">
                <el-button-group>
                  <el-button size="small" @click="handleEdit(task)">编辑</el-button>
                  <el-button size="small" type="success" @click="handleComplete(task)">完成</el-button>
                  <el-button size="small" type="danger" @click="handleAbandon(task)">放弃</el-button>
                </el-button-group>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import BatchOperations from '../../components/BatchOperations.vue'
import TaskImportExport from '../../components/TaskImportExport.vue'
import { taskApi } from '../../api'

const router = useRouter()

// 状态变量
const loading = ref(false)
const error = ref(null)

// 视图控制
const currentView = ref('list')
const currentDate = ref(new Date())

// 搜索和筛选
const searchQuery = ref('')
const filterTag = ref('')
const filterLocation = ref('')
const filterStatus = ref('')
const filterPriority = ref('')

// 选中的任务
const selectedTasks = ref([])

// 标签和地点列表
const tags = ref([])
const locations = ref([])

// 任务列表
const tasks = ref([])

// 计算属性：过滤后的任务列表
const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesTag = !filterTag.value || task.tags.includes(filterTag.value)
    const matchesLocation = !filterLocation.value || task.location === filterLocation.value
    const matchesStatus = !filterStatus.value || task.status === filterStatus.value
    return matchesSearch && matchesTag && matchesLocation && matchesStatus
  })
})

// 计算属性：按优先级排序的任务列表
const sortedTasks = computed(() => {
  const priorityOrder = { '高': 0, '中': 1, '低': 2 }
  return [...filteredTasks.value].sort((a, b) => {
    return priorityOrder[a.priority] - priorityOrder[b.priority]
  })
})

// 获取指定日期的任务
const getTasksForDate = (date) => {
  return filteredTasks.value.filter(task => {
    const taskDate = task.created_at.split(' ')[0]
    return taskDate === date
  })
}

// 获取优先级颜色
const getPriorityColor = (priority) => {
  const colors = {
    '高': '#F56C6C',
    '中': '#E6A23C',
    '低': '#67C23A'
  }
  return colors[priority] || '#909399'
}

// 获取优先级类型
const getPriorityType = (priority) => {
  const types = {
    '高': 'danger',
    '中': 'warning',
    '低': 'success'
  }
  return types[priority] || 'info'
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    'pending': 'info',
    'not_started': 'info',
    'in_progress': 'warning',
    'completed': 'success',
    'abandoned': 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    'pending': '待处理',
    'not_started': '未开始',
    'in_progress': '进行中',
    'completed': '已完成',
    'abandoned': '已放弃'
  }
  return texts[status] || status
}

// 处理视图切换
const handleViewChange = (view) => {
  currentView.value = view
}

// 处理搜索
const handleSearch = () => {
  // 实现搜索逻辑
}

// 处理筛选
const handleFilter = () => {
  // 实现筛选逻辑
}

// 处理选择变化
const handleSelectionChange = (selection) => {
  selectedTasks.value = selection
}

// 处理批量操作完成
const handleOperationComplete = () => {
  // 刷新任务列表
  getTasks()
}

// 显示创建对话框
const showCreateDialog = () => {
  router.push('/tasks/create')
}

// 处理编辑
const handleEdit = (task) => {
  router.push(`/tasks/${task.id}/edit`)
}

// 处理完成
const handleComplete = async (task) => {
  try {
    await ElMessageBox.confirm('确定要完成任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await taskApi.completeTask(task.id)
    ElMessage.success('任务已完成')
    getTasks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('完成任务失败:', error)
      ElMessage.error('完成任务失败')
    }
  }
}

// 处理放弃
const handleAbandon = async (task) => {
  try {
    await ElMessageBox.confirm('确定要放弃任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await taskApi.abandonTask(task.id)
    ElMessage.success('任务已放弃')
    getTasks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('放弃任务失败:', error)
      ElMessage.error('放弃任务失败')
    }
  }
}

// 获取任务列表
const getTasks = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await taskApi.getTasks()
    tasks.value = response.data
  } catch (err) {
    console.error('获取任务列表失败:', err)
    error.value = '获取任务列表失败，请检查网络连接'
    tasks.value = []
  } finally {
    loading.value = false
  }
}

// 获取标签和地点列表
const getTagsAndLocations = async () => {
  try {
    const response = await taskApi.getTagsAndLocations()
    tags.value = response.data.tags
    locations.value = response.data.locations
  } catch (err) {
    console.error('获取标签和地点列表失败:', err)
    tags.value = []
    locations.value = []
  }
}

// 初始化数据
onMounted(async () => {
  await Promise.all([
    getTasks(),
    getTagsAndLocations()
  ])
})
</script>

<style lang="scss" scoped>
.task-list {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-actions {
      display: flex;
      gap: 16px;
      align-items: center;
    }
  }

  .filter-bar {
    margin-bottom: 20px;
    display: flex;
    gap: 16px;
  }

  .view-switcher {
    margin-bottom: 20px;
  }

  .list-view {
    .task-name {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;

      .task-tag {
        margin: 2px 4px;
        white-space: nowrap;
        display: inline-block;
      }
    }
  }

  .month-view {
    .calendar-cell {
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;

      .task-dots {
        display: flex;
        gap: 4px;
        flex-wrap: wrap;

        .task-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
        }
      }
    }
  }

  .priority-view {
    .task-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      .task-tags {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;

        .task-tag {
          margin: 2px 4px;
          white-space: nowrap;
          display: inline-block;
        }
      }
    }

    .task-info {
      margin-bottom: 16px;
    }
  }
}
</style> 