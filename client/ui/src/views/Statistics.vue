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
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
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
      data: [10, 15, 8, 12, 9, 5, 7]
    },
    {
      name: '进行中',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: [5, 7, 3, 4, 6, 2, 3]
    },
    {
      name: '待开始',
      type: 'line',
      stack: 'Total',
      areaStyle: {},
      emphasis: {
        focus: 'series'
      },
      data: [3, 4, 2, 5, 3, 1, 2]
    }
  ]
}))

// 任务类型分布图表配置
const typeChartOptions = computed(() => ({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left',
    data: ['工作', '学习', '生活', '娱乐', '其他']
  },
  series: [
    {
      name: '任务类型',
      type: 'pie',
      radius: ['50%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '20',
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 35, name: '工作' },
        { value: 25, name: '学习' },
        { value: 20, name: '生活' },
        { value: 15, name: '娱乐' },
        { value: 5, name: '其他' }
      ]
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
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  },
  yAxis: {
    type: 'value',
    max: 100,
    axisLabel: {
      formatter: '{value}%'
    }
  },
  series: [
    {
      name: efficiencyMetric.value === 'completion' ? '完成率' :
            efficiencyMetric.value === 'punctuality' ? '准时率' : '满意度',
      type: 'bar',
      barWidth: '60%',
      data: [85, 92, 78, 88, 95, 82, 90],
      itemStyle: {
        borderRadius: [4, 4, 0, 0]
      }
    }
  ]
}))

// 更新趋势图表
const updateTrendChart = async () => {
  try {
    const response = await axios.get(`/api/statistics/trend?range=${trendTimeRange.value}`)
    // TODO: 更新图表数据
  } catch (error) {
    ElMessage.error('获取趋势数据失败：' + error.message)
  }
}

// 更新类型图表
const updateTypeChart = async () => {
  try {
    const response = await axios.get(`/api/statistics/type?view=${typeChartView.value}`)
    // TODO: 更新图表数据
  } catch (error) {
    ElMessage.error('获取类型数据失败：' + error.message)
  }
}

// 更新效率图表
const updateEfficiencyChart = async () => {
  try {
    const response = await axios.get(`/api/statistics/efficiency?metric=${efficiencyMetric.value}&range=${efficiencyTimeRange.value}`)
    // TODO: 更新图表数据
  } catch (error) {
    ElMessage.error('获取效率数据失败：' + error.message)
  }
}

// 刷新所有数据
const refreshData = async () => {
  try {
    const response = await axios.get('/api/statistics/overview')
    statCards.value = response.data.cards
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
  refreshData()
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