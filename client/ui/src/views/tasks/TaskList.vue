<template>
  <div class="task-list container">
    <!-- 视图切换和搜索筛选 -->
    <div class="view-controls">
      <el-radio-group v-model="currentView" @change="handleViewChange">
        <el-radio-button label="list">列表视图</el-radio-button>
        <el-radio-button label="month">月度视图</el-radio-button>
        <el-radio-button label="priority">优先级视图</el-radio-button>
      </el-radio-group>

      <div class="search-filter">
        <el-input
          v-model="searchQuery"
          placeholder="搜索任务"
          prefix-icon="Search"
          clearable
          @clear="handleSearch"
          @input="handleSearch"
        />
        <el-select v-model="filterTag" placeholder="标签筛选" clearable @change="handleFilter">
          <el-option
            v-for="tag in tags"
            :key="tag"
            :label="tag"
            :value="tag"
          />
        </el-select>
        <el-select v-model="filterLocation" placeholder="地点筛选" clearable @change="handleFilter">
          <el-option
            v-for="location in locations"
            :key="location"
            :label="location"
            :value="location"
          />
        </el-select>
        <el-select v-model="filterStatus" placeholder="状态筛选" clearable @change="handleFilter">
          <el-option label="未开始" value="not_started" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已完成" value="completed" />
          <el-option label="已放弃" value="abandoned" />
        </el-select>
      </div>
    </div>

    <!-- 列表视图 -->
    <div v-if="currentView === 'list'" class="list-view">
      <el-table :data="filteredTasks" style="width: 100%">
        <el-table-column prop="name" label="任务名称" min-width="200">
          <template #default="{ row }">
            <div class="task-name">
              <span>{{ row.name }}</span>
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
        <el-table-column prop="startTime" label="开始时间" width="180" />
        <el-table-column prop="endTime" label="结束时间" width="180">
          <template #default="{ row }">
            <span v-if="row.endTime">{{ row.endTime }}</span>
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
          v-for="task in sortedTasks"
          :key="task.id"
          :type="getPriorityType(task.priority)"
          :timestamp="task.startTime"
        >
          <el-card>
            <div class="task-header">
              <h4>{{ task.name }}</h4>
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
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 视图控制
const currentView = ref('list')
const currentDate = ref(new Date())

// 搜索和筛选
const searchQuery = ref('')
const filterTag = ref('')
const filterLocation = ref('')
const filterStatus = ref('')

// 模拟数据
const tasks = ref([
  {
    id: 1,
    name: '完成项目文档',
    startTime: '2024-03-20 09:00',
    endTime: '2024-03-20 12:00',
    status: 'in_progress',
    priority: '高',
    tags: ['工作', '文档'],
    location: '办公室'
  },
  {
    id: 2,
    name: '每日阅读',
    startTime: '2024-03-20 14:00',
    endTime: null,
    status: 'not_started',
    priority: '中',
    tags: ['学习', '阅读'],
    location: '图书馆',
    completionCount: 2,
    requiredCount: 5
  }
])

const tags = ref(['工作', '学习', '生活', '文档', '阅读'])
const locations = ref(['办公室', '家', '图书馆'])

// 计算属性
const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    const matchesSearch = task.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesTag = !filterTag.value || task.tags.includes(filterTag.value)
    const matchesLocation = !filterLocation.value || task.location === filterLocation.value
    const matchesStatus = !filterStatus.value || task.status === filterStatus.value
    return matchesSearch && matchesTag && matchesLocation && matchesStatus
  })
})

const sortedTasks = computed(() => {
  return [...filteredTasks.value].sort((a, b) => {
    const priorityOrder = { '高': 3, '中': 2, '低': 1 }
    return priorityOrder[b.priority] - priorityOrder[a.priority]
  })
})

// 方法
const handleViewChange = (view) => {
  currentView.value = view
}

const handleSearch = () => {
  // 实现搜索逻辑
}

const handleFilter = () => {
  // 实现筛选逻辑
}

const getStatusType = (status) => {
  const types = {
    not_started: 'info',
    in_progress: 'warning',
    completed: 'success',
    abandoned: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    not_started: '未开始',
    in_progress: '进行中',
    completed: '已完成',
    abandoned: '已放弃'
  }
  return texts[status] || status
}

const getPriorityType = (priority) => {
  const types = {
    '高': 'danger',
    '中': 'warning',
    '低': 'info'
  }
  return types[priority] || 'info'
}

const getPriorityColor = (priority) => {
  const colors = {
    '高': '#F56C6C',
    '中': '#E6A23C',
    '低': '#909399'
  }
  return colors[priority] || '#909399'
}

const getTasksForDate = (date) => {
  return tasks.value.filter(task => {
    const taskDate = task.startTime.split(' ')[0]
    return taskDate === date
  })
}

const handleEdit = (task) => {
  router.push(`/tasks/edit/${task.id}`)
}

const handleComplete = async (task) => {
  try {
    if (task.endTime) {
      await ElMessageBox.confirm('确认完成该任务？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
      // 实现完成任务逻辑
      ElMessage.success('任务已完成')
    } else {
      // 对于需要完成次数的任务，显示次数选择对话框
      const { value: count } = await ElMessageBox.prompt(
        '请输入完成次数',
        '完成次数',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputPattern: /^[1-9]\d*$/,
          inputErrorMessage: '请输入有效的完成次数'
        }
      )
      if (count) {
        // 实现更新完成次数逻辑
        ElMessage.success(`已更新完成次数为 ${count}`)
      }
    }
  } catch {
    // 用户取消操作
  }
}

const handleAbandon = async (task) => {
  try {
    await ElMessageBox.confirm('确认放弃该任务？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    // 实现放弃任务逻辑
    ElMessage.success('任务已放弃')
  } catch {
    // 用户取消操作
  }
}
</script>

<style lang="scss" scoped>
.task-list {
  padding: var(--spacing-medium);

  .view-controls {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-medium);
    margin-bottom: var(--spacing-large);

    .search-filter {
      display: flex;
      gap: var(--spacing-medium);
      flex-wrap: wrap;

      .el-input,
      .el-select {
        width: 200px;
      }
    }
  }

  .list-view {
    .task-name {
      display: flex;
      align-items: center;
      gap: var(--spacing-small);

      .task-tag {
        margin-left: var(--spacing-small);
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
      align-items: flex-start;
      margin-bottom: var(--spacing-small);

      h4 {
        margin: 0;
        color: var(--text-primary);
      }

      .task-tags {
        display: flex;
        gap: var(--spacing-small);
      }
    }

    .task-info {
      margin: var(--spacing-small) 0;
      color: var(--text-regular);
    }

    .task-actions {
      margin-top: var(--spacing-small);
    }
  }
}

// 响应式布局
@media (max-width: 768px) {
  .task-list {
    .view-controls {
      .search-filter {
        .el-input,
        .el-select {
          width: 100%;
        }
      }
    }
  }
}
</style> 