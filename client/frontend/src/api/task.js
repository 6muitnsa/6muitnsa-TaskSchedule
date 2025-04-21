import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 5000
})

// 添加响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // 处理422错误
      if (error.response.status === 422) {
        const errors = error.response.data.detail
        if (Array.isArray(errors)) {
          const errorMessage = errors.map(err => err.msg).join(', ')
          return Promise.reject(new Error(errorMessage))
        }
      }
      // 处理其他错误
      return Promise.reject(new Error(error.response.data.detail || '请求失败'))
    }
    return Promise.reject(error)
  }
)

export const taskApi = {
  // 获取任务列表
  getTasks(params) {
    return api.get('/tasks/', { params })
  },

  // 获取单个任务
  getTask(id) {
    return api.get(`/tasks/${id}`)
  },

  // 创建任务
  createTask(data) {
    return api.post('/tasks/', data)
  },

  // 更新任务
  updateTask(id, data) {
    return api.put(`/tasks/${id}`, data)
  },

  // 删除任务
  deleteTask(id) {
    return api.delete(`/tasks/${id}`)
  },

  // 更新任务状态
  updateTaskStatus(id, status) {
    return api.patch(`/tasks/${id}/status`, { status })
  },

  // 更新任务优先级
  updateTaskPriority(id, priority) {
    return api.patch(`/tasks/${id}/priority`, { priority })
  }
} 