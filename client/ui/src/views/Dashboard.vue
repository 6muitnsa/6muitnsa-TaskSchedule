<template>
  <div class="dashboard">
    <!-- 错误提示 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      :closable="false"
      class="mb-4"
    />

    <!-- 加载状态 -->
    <div v-loading="loading">
      <!-- 顶部统计卡片 -->
      <el-row :gutter="20" class="mb-4">
        <el-col :span="6" v-for="card in statCards" :key="card.title">
          <el-card class="stat-card" :body-style="{ padding: '20px' }">
            <div class="stat-card-content">
              <div class="stat-card-icon" :style="{ backgroundColor: card.color }">
                <el-icon><component :is="card.icon" /></el-icon>
              </div>
              <div class="stat-card-info">
                <div class="stat-card-title">{{ card.title }}</div>
                <div class="stat-card-value">{{ card.value }}</div>
                <div class="stat-card-trend" :class="{ 'up': card.trend > 0, 'down': card.trend < 0 }">
                  <el-icon v-if="card.trend !== 0">
                    <component :is="card.trend > 0 ? 'ArrowUp' : 'ArrowDown'" />
                  </el-icon>
                  <span>{{ Math.abs(card.trend) }}%</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 图表区域 -->
      <el-row :gutter="20" class="mb-4">
        <el-col :span="16">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>任务完成趋势</span>
                <el-radio-group v-model="trendTimeRange" size="small">
                  <el-radio-button label="week">本周</el-radio-button>
                  <el-radio-button label="month">本月</el-radio-button>
                  <el-radio-button label="year">全年</el-radio-button>
                </el-radio-group>
              </div>
            </template>
            <div class="chart-container">
              <v-chart class="chart" :option="trendChartOptions" autoresize />
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>任务类型分布</span>
                <el-radio-group v-model="typeChartView" size="small">
                  <el-radio-button label="count">数量</el-radio-button>
                  <el-radio-button label="time">时间</el-radio-button>
                </el-radio-group>
              </div>
            </template>
            <div class="chart-container">
              <v-chart class="chart" :option="typeChartOptions" autoresize />
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 效率分析 -->
      <el-row :gutter="20" class="mb-4">
        <el-col :span="24">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>效率分析</span>
                <div class="header-actions">
                  <el-select v-model="efficiencyMetric" size="small" class="mr-2">
                    <el-option label="完成率" value="completion" />
                    <el-option label="专注时长" value="focus" />
                    <el-option label="休息时长" value="rest" />
                  </el-select>
                  <el-select v-model="efficiencyTimeRange" size="small">
                    <el-option label="最近7天" value="7days" />
                    <el-option label="最近30天" value="30days" />
                    <el-option label="最近90天" value="90days" />
                  </el-select>
                </div>
              </div>
            </template>
            <div class="chart-container">
              <v-chart class="chart" :option="efficiencyChartOptions" autoresize />
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 最近任务和待办事项 -->
      <el-row :gutter="20">
        <el-col :span="16">
          <el-card class="task-card">
            <template #header>
              <div class="card-header">
                <span>最近任务</span>
                <el-button type="primary" link @click="viewAllTasks">
                  查看全部
                </el-button>
              </div>
            </template>
            <el-table :data="recentTasks" style="width: 100%">
              <el-table-column prop="title" label="任务名称" min-width="200" />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)">
                    {{ getStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="priority" label="优先级" width="100">
                <template #default="{ row }">
                  <el-tag :type="getPriorityType(row.priority)">
                    {{ getPriorityText(row.priority) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="deadline" label="截止时间" width="150" />
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" link @click="viewTask(row)">
                    查看
                  </el-button>
                  <el-button type="primary" link @click="editTask(row)">
                    编辑
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="todo-card">
            <template #header>
              <div class="card-header">
                <span>待办事项</span>
                <el-button type="primary" link @click="createTask">
                  新建任务
                </el-button>
              </div>
            </template>
            <div class="todo-list">
              <div v-for="todo in todoList" :key="todo.id" class="todo-item">
                <el-checkbox v-model="todo.completed" @change="handleTodoStatusChange(todo)">
                  <span :class="{ 'completed': todo.completed }">{{ todo.title }}</span>
                </el-checkbox>
                <div class="todo-info">
                  <el-tag size="small" :type="getPriorityType(todo.priority)">
                    {{ getPriorityText(todo.priority) }}
                  </el-tag>
                  <span class="todo-deadline">{{ todo.deadline }}</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, provide } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
} from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'
import {
  Calendar,
  Check,
  Timer,
  Star,
  ArrowUp,
  ArrowDown
} from '@element-plus/icons-vue'
import { statisticsApi, taskApi } from '../api'

// 注册 ECharts 组件
echarts.use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
])

// 提供主题
provide(THEME_KEY, 'light')

const router = useRouter()

// 加载状态
const loading = ref(true)
const error = ref(null)

// 统计数据
const statistics = ref({
  task_stats: {
    total: 0,
    completed: 0,
    in_progress: 0,
    abandoned: 0
  },
  focus_stats: {
    average: 0,
    total: 0,
    trend: 0
  },
  rest_stats: {
    average: 0,
    total: 0,
    trend: 0
  }
})

// 统计卡片数据
const statCards = computed(() => {
  const taskStats = statistics.value?.task_stats || {
    total: 0,
    completed: 0,
    in_progress: 0,
    abandoned: 0
  }
  const focusStats = statistics.value?.focus_stats || {
    average: 0,
    total: 0,
    trend: 0
  }
  const restStats = statistics.value?.rest_stats || {
    average: 0,
    total: 0,
    trend: 0
  }

  return [
    {
      title: '总任务数',
      value: taskStats.total.toString(),
      icon: 'Calendar',
      color: '#409EFF',
      trend: 0
    },
    {
      title: '已完成',
      value: taskStats.completed.toString(),
      icon: 'Check',
      color: '#67C23A',
      trend: 0
    },
    {
      title: '平均用时',
      value: `${Math.round(focusStats.average)}h`,
      icon: 'Timer',
      color: '#E6A23C',
      trend: focusStats.trend
    },
    {
      title: '休息时间',
      value: `${Math.round(restStats.average)}h`,
      icon: 'Star',
      color: '#F56C6C',
      trend: restStats.trend
    }
  ]
})

// 图表相关数据
const trendTimeRange = ref('week')
const typeChartView = ref('count')
const efficiencyMetric = ref('completion')
const efficiencyTimeRange = ref('7days')

// 任务完成趋势图表配置
const trendChartOptions = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross',
      label: {
        backgroundColor: '#6a7985'
      }
    }
  },
  legend: {
    data: ['已完成', '进行中', '待开始']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: []
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '已完成',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: []
    },
    {
      name: '进行中',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: []
    },
    {
      name: '待开始',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: []
    }
  ]
}))

// 任务类型分布图表配置
const typeChartOptions = computed(() => ({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '任务类型',
      type: 'pie',
      radius: '50%',
      data: [],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
}))

// 效率分析图表配置
const efficiencyChartOptions = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: []
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '效率值',
      type: 'bar',
      data: [],
      itemStyle: {
        color: '#409EFF'
      }
    }
  ]
}))

// 最近任务
const recentTasks = ref([])

// 待办事项列表
const todoList = ref([])

// 获取统计数据
const getStatistics = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await statisticsApi.getOverview()
    if (response && response.data) {
      statistics.value = response.data
    }
  } catch (err) {
    console.error('获取统计数据失败:', err)
    error.value = '获取统计数据失败，请检查网络连接'
    // 保持默认值
  } finally {
    loading.value = false
  }
}

// 获取最近任务
const getRecentTasks = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await taskApi.getRecentTasks()
    if (response && response.data) {
      recentTasks.value = response.data
    }
  } catch (err) {
    console.error('获取最近任务失败:', err)
    error.value = '获取最近任务失败，请检查网络连接'
    recentTasks.value = []
  } finally {
    loading.value = false
  }
}

// 获取待办事项
const getTodoList = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await taskApi.getTasks({
      status: 'not_started',
      limit: 10,
      sort: 'priority:desc,created_at:desc'
    })
    if (response && response.data) {
      todoList.value = response.data
    }
  } catch (err) {
    console.error('获取待办事项失败:', err)
    error.value = '获取待办事项失败，请检查网络连接'
    todoList.value = []
  } finally {
    loading.value = false
  }
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    abandoned: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    pending: '待开始',
    in_progress: '进行中',
    completed: '已完成',
    abandoned: '已放弃'
  }
  return texts[status] || status
}

// 获取优先级类型
const getPriorityType = (priority) => {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[priority] || 'info'
}

// 获取优先级文本
const getPriorityText = (priority) => {
  const texts = {
    high: '高',
    medium: '中',
    low: '低'
  }
  return texts[priority] || priority
}

// 查看任务
const viewTask = (task) => {
  try {
    router.push({
      name: 'taskDetail',
      params: { id: task.id }
    })
  } catch (err) {
    console.error('跳转到任务详情页失败:', err)
    ElMessage.error('跳转失败，请重试')
  }
}

// 编辑任务
const editTask = (task) => {
  try {
    router.push({
      name: 'editTask',
      params: { id: task.id }
    })
  } catch (err) {
    console.error('跳转到任务编辑页失败:', err)
    ElMessage.error('跳转失败，请重试')
  }
}

// 查看全部任务
const viewAllTasks = () => {
  try {
    router.push({ name: 'taskList' })
  } catch (err) {
    console.error('跳转到任务列表页失败:', err)
    ElMessage.error('跳转失败，请重试')
  }
}

// 创建任务
const createTask = () => {
  try {
    router.push({ name: 'createTask' })
  } catch (err) {
    console.error('跳转到创建任务页失败:', err)
    ElMessage.error('跳转失败，请重试')
  }
}

// 处理待办事项状态变化
const handleTodoStatusChange = async (todo) => {
  try {
    await taskApi.updateTaskStatus(todo.id, todo.completed ? 'completed' : 'not_started')
    ElMessage.success('更新成功')
    await getTodoList()
  } catch (err) {
    console.error('更新待办事项状态失败:', err)
    ElMessage.error('更新失败')
    todo.completed = !todo.completed // 恢复状态
  }
}

// 初始化数据
onMounted(async () => {
  try {
    await Promise.all([
      getStatistics(),
      getRecentTasks(),
      getTodoList()
    ])
  } catch (err) {
    console.error('初始化数据失败:', err)
    error.value = '加载数据失败，请刷新页面重试'
  }
})
</script>

<style lang="scss" scoped>
.dashboard {
  .mb-4 {
    margin-bottom: 16px;
  }

  .mr-2 {
    margin-right: 8px;
  }

  .stat-card {
    .stat-card-content {
      display: flex;
      align-items: center;
      gap: 16px;

      .stat-card-icon {
        width: 48px;
        height: 48px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
      }

      .stat-card-info {
        flex: 1;

        .stat-card-title {
          font-size: 14px;
          color: #909399;
          margin-bottom: 4px;
        }

        .stat-card-value {
          font-size: 24px;
          font-weight: bold;
          color: #303133;
          margin-bottom: 4px;
        }

        .stat-card-trend {
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 4px;

          &.up {
            color: #67C23A;
          }

          &.down {
            color: #F56C6C;
          }
        }
      }
    }
  }

  .chart-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .chart-container {
      height: 300px;

      .chart {
        height: 100%;
      }
    }
  }

  .task-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }

  .todo-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .todo-list {
      .todo-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid #EBEEF5;

        &:last-child {
          border-bottom: none;
        }

        .completed {
          text-decoration: line-through;
          color: #909399;
        }

        .todo-info {
          display: flex;
          align-items: center;
          gap: 8px;

          .todo-deadline {
            font-size: 12px;
            color: #909399;
          }
        }
      }
    }
  }
}
</style> 