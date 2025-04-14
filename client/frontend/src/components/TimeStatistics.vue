<template>
  <div class="statistics-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="overview-card">
          <template #header>
            <div class="card-header">
              <h2>时间统计概览</h2>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-statistic title="总任务数" :value="statistics.totalTasks" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="已完成任务" :value="statistics.completedTasks" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="总时间(小时)" :value="(statistics.totalTimeSpent / 60).toFixed(1)" />
            </el-col>
            <el-col :span="6">
              <el-statistic title="效率评分" :value="statistics.productivityScore" />
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>每日任务完成情况</h3>
            </div>
          </template>
          <div class="chart-container">
            <!-- 这里可以集成echarts或其他图表库 -->
            <div class="placeholder-chart">图表区域</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>任务类型分布</h3>
            </div>
          </template>
          <div class="chart-container">
            <!-- 这里可以集成echarts或其他图表库 -->
            <div class="placeholder-chart">图表区域</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="table-row">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>详细统计</h3>
            </div>
          </template>
          <el-table :data="statistics.dailyStatistics" style="width: 100%">
            <el-table-column prop="date" label="日期" />
            <el-table-column prop="completedTasks" label="完成任务数" />
            <el-table-column prop="totalTime" label="总时间(小时)" />
            <el-table-column prop="efficiency" label="效率评分" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { statisticsService } from '../services/statisticsService'

interface DailyStat {
  date: string
  completedTasks: number
  totalTime: number
  efficiency: number
}

interface Statistics {
  totalTasks: number
  completedTasks: number
  totalTimeSpent: number
  productivityScore: number
  dailyStatistics: DailyStat[]
}

const statistics = ref<Statistics>({
  totalTasks: 0,
  completedTasks: 0,
  totalTimeSpent: 0,
  productivityScore: 0,
  dailyStatistics: []
})

onMounted(async () => {
  try {
    const data = await statisticsService.getStatistics()
    statistics.value = data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style scoped>
.statistics-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-row {
  margin-top: 20px;
}

.table-row {
  margin-top: 20px;
}

.chart-container {
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.placeholder-chart {
  width: 100%;
  height: 100%;
  background-color: #f5f7fa;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #909399;
}
</style> 