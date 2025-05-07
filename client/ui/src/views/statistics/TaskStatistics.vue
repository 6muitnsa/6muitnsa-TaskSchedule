<template>
  <div class="task-statistics">
    <!-- 日期范围选择 -->
    <el-card class="filter-card" v-loading="loading">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :shortcuts="dateShortcuts"
            @change="handleDateRangeChange"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 统计概览 -->
    <el-row :gutter="20" class="statistics-overview" v-loading="loading">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>总任务数</span>
            </div>
          </template>
          <div class="statistic-value">{{ statistics.total_tasks }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>已完成任务</span>
            </div>
          </template>
          <div class="statistic-value">{{ statistics.completed_tasks }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>进行中任务</span>
            </div>
          </template>
          <div class="statistic-value">{{ statistics.in_progress_tasks }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>完成率</span>
            </div>
          </template>
          <div class="statistic-value">{{ statistics.completion_rate }}%</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表展示 -->
    <el-row :gutter="20" class="statistics-charts" v-loading="loading">
      <!-- 任务趋势图 -->
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>任务趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="trendChartOption" autoresize />
          </div>
        </el-card>
      </el-col>

      <!-- 优先级分布图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>优先级分布</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="priorityChartOption" autoresize />
          </div>
        </el-card>
      </el-col>

      <!-- 标签分布图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>标签分布</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="tagChartOption" autoresize />
          </div>
        </el-card>
      </el-col>

      <!-- 地点分布图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>地点分布</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="locationChartOption" autoresize />
          </div>
        </el-card>
      </el-col>

      <!-- 完成时间分布图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>完成时间分布</span>
            </div>
          </template>
          <div class="chart-container">
            <v-chart :option="timeDistributionChartOption" autoresize />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart, BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { getTaskStatistics, getTaskTrends, getTaskAnalysis } from '../../api/statistics'
import { ElMessage } from 'element-plus'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  LineChart,
  PieChart,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
])

// 日期范围选择
const filterForm = ref({
  dateRange: []
})

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    }
  }
]

// 统计数据
const statistics = ref({
  total_tasks: 0,
  completed_tasks: 0,
  in_progress_tasks: 0,
  completion_rate: 0,
  priority_stats: {},
  tag_stats: {},
  location_stats: {},
  daily_stats: {}
})

// 趋势数据
const trends = ref({
  dates: [],
  created_tasks: [],
  completed_tasks: [],
  abandoned_tasks: []
})

// 分析数据
const analysis = ref({
  time_distribution: {},
  most_used_tags: {},
  most_used_locations: {},
  completion_trends: []
})

// 图表配置
const trendChartOption = computed(() => ({
  title: {
    text: '任务趋势'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['创建任务', '完成任务', '放弃任务']
  },
  xAxis: {
    type: 'category',
    data: trends.value.dates
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '创建任务',
      type: 'line',
      data: trends.value.created_tasks
    },
    {
      name: '完成任务',
      type: 'line',
      data: trends.value.completed_tasks
    },
    {
      name: '放弃任务',
      type: 'line',
      data: trends.value.abandoned_tasks
    }
  ]
}))

const priorityChartOption = computed(() => ({
  title: {
    text: '优先级分布'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      type: 'pie',
      radius: '50%',
      data: Object.entries(statistics.value.priority_stats).map(([name, value]) => ({
        name,
        value
      }))
    }
  ]
}))

const tagChartOption = computed(() => ({
  title: {
    text: '标签分布'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      type: 'pie',
      radius: '50%',
      data: Object.entries(statistics.value.tag_stats).map(([name, value]) => ({
        name,
        value
      }))
    }
  ]
}))

const locationChartOption = computed(() => ({
  title: {
    text: '地点分布'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      type: 'pie',
      radius: '50%',
      data: Object.entries(statistics.value.location_stats).map(([name, value]) => ({
        name,
        value
      }))
    }
  ]
}))

const timeDistributionChartOption = computed(() => ({
  title: {
    text: '完成时间分布'
  },
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: Object.keys(analysis.value.time_distribution)
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      type: 'bar',
      data: Object.values(analysis.value.time_distribution)
    }
  ]
}))

// 加载状态
const loading = ref(false)

// 处理日期范围变化
const handleDateRangeChange = (val) => {
  if (val) {
    filterForm.value.dateRange = val
  }
}

// 处理查询
const handleFilter = async () => {
  try {
    loading.value = true
    const [startDate, endDate] = filterForm.value.dateRange
    const params = {
      start_date: startDate.toISOString(),
      end_date: endDate.toISOString()
    }
    
    // 获取统计数据
    const [statisticsRes, trendsRes, analysisRes] = await Promise.all([
      getTaskStatistics(params),
      getTaskTrends({ days: Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) }),
      getTaskAnalysis()
    ])
    
    if (statisticsRes.code === 200 && trendsRes.code === 200 && analysisRes.code === 200) {
      statistics.value = statisticsRes.data
      trends.value = trendsRes.data
      analysis.value = analysisRes.data
    } else {
      throw new Error('获取数据失败')
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error(error.message || '获取统计数据失败')
  } finally {
    loading.value = false
  }
}

// 重置筛选条件
const resetFilter = () => {
  filterForm.value.dateRange = []
  handleFilter()
}

// 初始化
onMounted(() => {
  handleFilter()
})
</script>

<style lang="scss" scoped>
.task-statistics {
  padding: 20px;

  .filter-card {
    margin-bottom: 20px;
  }

  .statistics-overview {
    margin-bottom: 20px;

    .statistic-value {
      font-size: 24px;
      font-weight: bold;
      text-align: center;
      color: #409EFF;
    }
  }

  .statistics-charts {
    .chart-card {
      margin-bottom: 20px;

      .chart-container {
        height: 400px;
      }
    }
  }
}
</style> 