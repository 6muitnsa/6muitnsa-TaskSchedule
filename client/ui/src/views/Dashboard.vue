<template>
  <div class="dashboard container">
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>任务完成个数</span>
          </div>
        </template>
        <div class="card-content">
          <h2>{{ stats.completedTasks }}</h2>
        </div>
      </el-card>

      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>平均专注时长</span>
          </div>
        </template>
        <div class="card-content">
          <h2>{{ stats.avgFocusTime }}分钟</h2>
        </div>
      </el-card>

      <el-card class="stat-card">
        <template #header>
          <div class="card-header">
            <span>平均休息时长</span>
          </div>
        </template>
        <div class="card-content">
          <h2>{{ stats.avgRestTime }}分钟</h2>
        </div>
      </el-card>
    </div>

    <!-- 图表区域 -->
    <div class="charts-grid">
      <!-- 任务完成趋势 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>任务完成趋势</span>
            <el-radio-group v-model="trendTimeRange" size="small">
              <el-radio-button label="week">周</el-radio-button>
              <el-radio-button label="month">月</el-radio-button>
              <el-radio-button label="year">年</el-radio-button>
            </el-radio-group>
          </div>
        </template>
        <div ref="trendChartRef" class="chart-container"></div>
      </el-card>

      <!-- 任务类型分布 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>任务类型分布</span>
          </div>
        </template>
        <div ref="typeChartRef" class="chart-container"></div>
      </el-card>

      <!-- 专注时间分布 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>专注时间分布</span>
          </div>
        </template>
        <div ref="focusTimeChartRef" class="chart-container"></div>
      </el-card>

      <!-- 任务完成率 -->
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>任务完成率</span>
          </div>
        </template>
        <div ref="completionRateChartRef" class="chart-container"></div>
      </el-card>
    </div>

    <!-- 快捷操作按钮 -->
    <div class="action-buttons">
      <el-button type="primary" @click="$router.push('/tasks/create')">
        <el-icon><Plus /></el-icon>
        创建任务
      </el-button>
      <el-button type="success" @click="$router.push('/pomodoro')">
        <el-icon><Timer /></el-icon>
        番茄钟
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Plus, Timer } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 统计数据
const stats = ref({
  completedTasks: 0,
  avgFocusTime: 0,
  avgRestTime: 0
})

// 图表引用
const trendChartRef = ref(null)
const typeChartRef = ref(null)
const focusTimeChartRef = ref(null)
const completionRateChartRef = ref(null)

// 图表实例
let trendChart = null
let typeChart = null
let focusTimeChart = null
let completionRateChart = null

// 时间范围选择
const trendTimeRange = ref('week')

// 初始化统计数据
onMounted(() => {
  // 模拟数据
  stats.value = {
    completedTasks: 25,
    avgFocusTime: 45,
    avgRestTime: 10
  }

  // 初始化图表
  initCharts()
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

// 销毁图表实例
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  trendChart?.dispose()
  typeChart?.dispose()
  focusTimeChart?.dispose()
  completionRateChart?.dispose()
})

// 处理窗口大小变化
const handleResize = () => {
  trendChart?.resize()
  typeChart?.resize()
  focusTimeChart?.resize()
  completionRateChart?.resize()
}

// 初始化所有图表
const initCharts = () => {
  initTrendChart()
  initTypeChart()
  initFocusTimeChart()
  initCompletionRateChart()
}

// 初始化任务完成趋势图表
const initTrendChart = () => {
  trendChart = echarts.init(trendChartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '完成任务数',
        type: 'line',
        smooth: true,
        data: [5, 7, 3, 8, 6, 4, 9],
        areaStyle: {
          opacity: 0.1
        }
      }
    ]
  }
  trendChart.setOption(option)
}

// 初始化任务类型分布图表
const initTypeChart = () => {
  typeChart = echarts.init(typeChartRef.value)
  const option = {
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
          { value: 20, name: '阅读' },
          { value: 15, name: '写作' },
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
  }
  typeChart.setOption(option)
}

// 初始化专注时间分布图表
const initFocusTimeChart = () => {
  focusTimeChart = echarts.init(focusTimeChartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: ['0-30分钟', '30-60分钟', '60-90分钟', '90-120分钟', '120分钟以上']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '任务数量',
        type: 'bar',
        data: [10, 15, 8, 5, 3],
        itemStyle: {
          borderRadius: [4, 4, 0, 0]
        }
      }
    ]
  }
  focusTimeChart.setOption(option)
}

// 初始化任务完成率图表
const initCompletionRateChart = () => {
  completionRateChart = echarts.init(completionRateChartRef.value)
  const option = {
    tooltip: {
      formatter: '{a} <br/>{b} : {c}%'
    },
    series: [
      {
        name: '完成率',
        type: 'gauge',
        progress: {
          show: true,
          width: 18
        },
        axisLine: {
          lineStyle: {
            width: 18
          }
        },
        axisTick: {
          show: false
        },
        splitLine: {
          length: 15,
          lineStyle: {
            width: 2,
            color: '#999'
          }
        },
        axisLabel: {
          distance: 25,
          color: '#999',
          fontSize: 14
        },
        anchor: {
          show: true,
          showAbove: true,
          size: 25,
          itemStyle: {
            borderWidth: 10
          }
        },
        title: {
          show: false
        },
        detail: {
          valueAnimation: true,
          fontSize: 30,
          offsetCenter: [0, '70%']
        },
        data: [
          {
            value: 85,
            name: '完成率'
          }
        ]
      }
    ]
  }
  completionRateChart.setOption(option)
}
</script>

<style lang="scss" scoped>
.dashboard {
  padding: var(--spacing-medium);

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-medium);
    margin-bottom: var(--spacing-large);
  }

  .charts-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-medium);
    margin-bottom: var(--spacing-large);
  }

  .stat-card,
  .chart-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--text-primary);
    }
    
    .card-content {
      text-align: center;
      padding: var(--spacing-medium) 0;
      
      h2 {
        margin: 0;
        font-size: var(--font-size-extra-large);
        color: var(--primary-color);
      }
    }

    .chart-container {
      height: 300px;
    }
  }

  .action-buttons {
    display: flex;
    gap: var(--spacing-medium);
    justify-content: center;
    margin-top: var(--spacing-large);

    .el-button {
      display: flex;
      align-items: center;
      gap: var(--spacing-small);
      padding: var(--spacing-medium) var(--spacing-large);
      font-size: var(--font-size-medium);

      .el-icon {
        font-size: var(--font-size-large);
      }
    }
  }
}

// 响应式布局
@media (max-width: 768px) {
  .dashboard {
    .stats-grid {
      grid-template-columns: 1fr;
    }

    .charts-grid {
      grid-template-columns: 1fr;
    }

    .action-buttons {
      flex-direction: column;
      
      .el-button {
        width: 100%;
      }
    }
  }
}
</style> 