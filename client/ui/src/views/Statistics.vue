<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">任务统计</div>
      <div class="page-actions">
        <el-button type="primary" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>

    <div class="statistics-content">
      <el-row :gutter="20">
        <el-col :span="6" v-for="card in statCards" :key="card.title">
          <el-card class="stat-card" :body-style="{ padding: '20px' }">
            <div class="stat-card-content">
              <div class="stat-icon" :style="{ backgroundColor: card.color }">
                <el-icon><component :is="card.icon" /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-title">{{ card.title }}</div>
                <div class="stat-value">{{ card.value }}</div>
                <div class="stat-trend" v-if="card.trend">
                  <span :class="['trend-value', card.trend > 0 ? 'up' : 'down']">
                    {{ card.trend > 0 ? '+' : '' }}{{ card.trend }}%
                  </span>
                  <span class="trend-label">较上周</span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="chart-row">
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>任务完成趋势</span>
                <el-radio-group v-model="trendTimeRange" size="small" @change="updateTrendChart">
                  <el-radio-button label="week">本周</el-radio-button>
                  <el-radio-button label="month">本月</el-radio-button>
                  <el-radio-button label="year">本年</el-radio-button>
                </el-radio-group>
              </div>
            </template>
            <div class="chart-container">
              <ECharts :options="trendChartOptions" />
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>任务类型分布</span>
                <el-select v-model="typeChartView" size="small" style="width: 120px" @change="updateTypeChart">
                  <el-option label="数量" value="count" />
                  <el-option label="时长" value="duration" />
                </el-select>
              </div>
            </template>
            <div class="chart-container">
              <ECharts :options="typeChartOptions" />
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="chart-row">
        <el-col :span="24">
          <el-card class="chart-card">
            <template #header>
              <div class="card-header">
                <span>任务效率分析</span>
                <div class="header-actions">
                  <el-select v-model="efficiencyMetric" size="small" style="width: 120px" @change="updateEfficiencyChart">
                    <el-option label="完成率" value="completion" />
                    <el-option label="准时率" value="punctuality" />
                    <el-option label="满意度" value="satisfaction" />
                  </el-select>
                  <el-select v-model="efficiencyTimeRange" size="small" style="width: 120px; margin-left: 8px" @change="updateEfficiencyChart">
                    <el-option label="最近7天" value="7days" />
                    <el-option label="最近30天" value="30days" />
                    <el-option label="最近90天" value="90days" />
                  </el-select>
                </div>
              </div>
            </template>
            <div class="chart-container">
              <ECharts :options="efficiencyChartOptions" />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  Calendar,
  Timer,
  Check,
  Star,
  Refresh
} from '@element-plus/icons-vue'
import ECharts from '../components/ECharts.vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { statisticsApi } from '../api'

// 统计卡片数据
const statCards = ref([
  {
    title: '总任务数',
    value: '0',
    icon: 'Calendar',
    color: '#409EFF',
    trend: 0
  },
  {
    title: '已完成',
    value: '0',
    icon: 'Check',
    color: '#67C23A',
    trend: 0
  },
  {
    title: '平均用时',
    value: '0h',
    icon: 'Timer',
    color: '#E6A23C',
    trend: 0
  },
  {
    title: '满意度',
    value: '0',
    icon: 'Star',
    color: '#F56C6C',
    trend: 0
  }
])

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

// 任务效率分析图表配置
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

// 获取统计数据
const getStatistics = async () => {
  try {
    const response = await statisticsApi.getOverview()
    const data = response.data
    
    // 更新统计卡片
    statCards.value[0].value = data.total_tasks.toString()
    statCards.value[1].value = data.completed_tasks.toString()
    statCards.value[2].value = `${Math.round(data.completion_rate)}%`
    statCards.value[3].value = data.pending_tasks.toString()
    
    // 更新趋势图数据
    const dates = Object.keys(data.daily_completion).sort()
    trendChartOptions.value.xAxis.data = dates
    trendChartOptions.value.series[0].data = dates.map(date => data.daily_completion[date])
    trendChartOptions.value.series[1].data = dates.map(() => 0) // 进行中的任务数
    trendChartOptions.value.series[2].data = dates.map(() => 0) // 待开始的任务数
    
    // 更新类型分布图数据
    typeChartOptions.value.series[0].data = Object.entries(data.priority_distribution).map(([name, value]) => ({
      name,
      value
    }))
    
    // 更新效率分析图数据
    efficiencyChartOptions.value.xAxis.data = dates
    efficiencyChartOptions.value.series[0].data = dates.map(date => data.daily_completion[date])
  } catch (err) {
    console.error('获取统计数据失败:', err)
  }
}

// 更新趋势图表
const updateTrendChart = async () => {
  try {
    const response = await statisticsApi.getTrend(trendTimeRange.value)
    // TODO: 更新图表数据
  } catch (error) {
    ElMessage.error('获取趋势数据失败：' + error.message)
  }
}

// 更新类型图表
const updateTypeChart = async () => {
  try {
    const response = await statisticsApi.getTypeStats(typeChartView.value)
    // TODO: 更新图表数据
  } catch (error) {
    ElMessage.error('获取类型数据失败：' + error.message)
  }
}

// 更新效率图表
const updateEfficiencyChart = async () => {
  try {
    const response = await statisticsApi.getEfficiency(efficiencyMetric.value, efficiencyTimeRange.value)
    // TODO: 更新图表数据
  } catch (error) {
    ElMessage.error('获取效率数据失败：' + error.message)
  }
}

// 刷新所有数据
const refreshData = async () => {
  try {
    await getStatistics()
    await Promise.all([
      updateTrendChart(),
      updateTypeChart(),
      updateEfficiencyChart()
    ])
    ElMessage.success('数据已更新')
  } catch (error) {
    ElMessage.error('刷新数据失败：' + error.message)
  }
}

// 初始化
onMounted(() => {
  getStatistics()
})
</script>

<style lang="scss" scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.statistics-content {
  .stat-card {
    margin-bottom: 20px;
    
    .stat-card-content {
      display: flex;
      align-items: center;
      
      .stat-icon {
        width: 48px;
        height: 48px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;
        
        .el-icon {
          font-size: 24px;
          color: #fff;
        }
      }
      
      .stat-info {
        flex: 1;
        
        .stat-title {
          font-size: 14px;
          color: #909399;
          margin-bottom: 8px;
        }
        
        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: #303133;
          margin-bottom: 4px;
        }
        
        .stat-trend {
          font-size: 12px;
          
          .trend-value {
            &.up {
              color: #67C23A;
            }
            
            &.down {
              color: #F56C6C;
            }
          }
          
          .trend-label {
            color: #909399;
            margin-left: 4px;
          }
        }
      }
    }
  }
  
  .chart-row {
    margin-bottom: 20px;
  }
  
  .chart-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .header-actions {
        display: flex;
        align-items: center;
      }
    }
    
    .chart-container {
      height: 300px;
    }
  }
}
</style> 