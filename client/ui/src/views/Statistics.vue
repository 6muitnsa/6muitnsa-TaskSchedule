<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">任务统计</div>
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
                <el-select v-model="efficiencyMetric" size="small" style="width: 120px" @change="updateEfficiencyChart">
                  <el-option label="完成率" value="completion" />
                  <el-option label="准时率" value="punctuality" />
                  <el-option label="满意度" value="satisfaction" />
                </el-select>
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
import { ref, computed } from 'vue'
import {
  Calendar,
  Timer,
  Check,
  Star
} from '@element-plus/icons-vue'
import ECharts from '../components/ECharts.vue'

// 统计卡片数据
const statCards = [
  {
    title: '总任务数',
    value: '128',
    icon: 'Calendar',
    color: '#409EFF'
  },
  {
    title: '已完成',
    value: '98',
    icon: 'Check',
    color: '#67C23A'
  },
  {
    title: '平均用时',
    value: '2.5h',
    icon: 'Timer',
    color: '#E6A23C'
  },
  {
    title: '满意度',
    value: '4.8',
    icon: 'Star',
    color: '#F56C6C'
  }
]

// 图表相关数据
const trendTimeRange = ref('week')
const efficiencyMetric = ref('completion')

// 任务完成趋势图表配置
const trendChartOptions = computed(() => ({
  tooltip: {
    trigger: 'axis'
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
      data: [10, 15, 8, 12, 9, 5, 7]
    },
    {
      name: '进行中',
      type: 'line',
      stack: 'Total',
      data: [5, 7, 3, 4, 6, 2, 3]
    },
    {
      name: '待开始',
      type: 'line',
      stack: 'Total',
      data: [3, 4, 2, 5, 3, 1, 2]
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
      data: [
        { value: 35, name: '工作' },
        { value: 25, name: '学习' },
        { value: 20, name: '生活' },
        { value: 15, name: '娱乐' },
        { value: 5, name: '其他' }
      ],
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
      data: [85, 92, 78, 88, 95, 82, 90]
    }
  ]
}))

// 更新趋势图表
const updateTrendChart = () => {
  // TODO: 根据时间范围更新数据
}

// 更新效率图表
const updateEfficiencyChart = () => {
  // TODO: 根据指标类型更新数据
}
</script>

<style lang="scss" scoped>
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
        .stat-title {
          font-size: 14px;
          color: #909399;
          margin-bottom: 8px;
        }
        
        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: #303133;
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
    }
    
    .chart-container {
      height: 300px;
    }
  }
}
</style> 