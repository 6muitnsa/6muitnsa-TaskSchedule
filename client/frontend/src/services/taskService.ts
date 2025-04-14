import axios from 'axios'
import type { Task } from '@/types/task'
import { ElMessage } from 'element-plus'

const API_BASE_URL = '/api/tasks'

export const taskService = {
  async getTasks(): Promise<Task[]> {
    const response = await axios.get(API_BASE_URL)
    return response.data
  },

  async getTaskById(id: string): Promise<Task> {
    const response = await axios.get(`${API_BASE_URL}/${id}`)
    return response.data
  },

  async createTask(task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Promise<Task> {
    const response = await axios.post(API_BASE_URL, task)
    return response.data
  },

  async updateTask(id: string, task: Partial<Task>): Promise<Task> {
    const response = await axios.put(`${API_BASE_URL}/${id}`, task)
    return response.data
  },

  async deleteTask(id: string): Promise<void> {
    await axios.delete(`${API_BASE_URL}/${id}`)
  },

  async updateTaskStatus(taskId: string, status: string): Promise<Task> {
    try {
      const response = await axios.patch(`${API_BASE_URL}/${taskId}/status`, { status })
      return response.data
    } catch (error) {
      console.error('更新任务状态失败:', error)
      ElMessage.error('更新任务状态失败')
      throw error
    }
  }
} 