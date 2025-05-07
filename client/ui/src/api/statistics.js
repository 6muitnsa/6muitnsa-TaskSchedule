import { api } from './index'

export const statisticsApi = {
  // 获取概览数据
  getOverview() {
    return api.get('/statistics/overview')
  },

  // 获取趋势数据
  getTrend(params) {
    return api.get('/statistics/trend', { params })
  },

  // 获取类型统计
  getTypeStats() {
    return api.get('/statistics/type')
  },

  // 获取效率数据
  getEfficiency() {
    return api.get('/statistics/efficiency')
  }
}

// 获取任务统计信息
export const getTaskStatistics = (params) => {
  return api.get('/statistics/tasks', { params })
}

// 获取任务趋势数据
export const getTaskTrends = (params) => {
  return api.get('/statistics/trends', { params })
}

// 获取任务分析报告
export const getTaskAnalysis = () => {
  return api.get('/statistics/analysis')
} 