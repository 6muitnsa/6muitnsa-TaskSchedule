import axios from 'axios'

const API_BASE_URL = '/api'

export interface DailyStat {
  date: string
  completedTasks: number
  totalTime: number
  efficiency: number
}

export interface Statistics {
  totalTasks: number
  completedTasks: number
  totalTimeSpent: number
  productivityScore: number
  dailyStatistics: DailyStat[]
}

export const statisticsService = {
  async getStatistics(): Promise<Statistics> {
    const response = await axios.get(`${API_BASE_URL}/statistics`)
    return response.data
  },

  async getDailyStatistics(startDate: string, endDate: string): Promise<DailyStat[]> {
    const response = await axios.get(`${API_BASE_URL}/statistics/daily`, {
      params: { startDate, endDate }
    })
    return response.data
  },

  async getTaskTypeDistribution(): Promise<{ type: string; count: number }[]> {
    const response = await axios.get(`${API_BASE_URL}/statistics/task-types`)
    return response.data
  }
} 