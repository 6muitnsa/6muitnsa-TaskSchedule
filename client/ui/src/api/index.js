import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('没有权限访问该资源')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error(error.response.data.message || '请求失败')
      }
    } else {
      ElMessage.error('网络错误，请检查您的网络连接')
    }
    return Promise.reject(error)
  }
)

// 任务相关API
export const taskApi = {
  // 获取任务列表
  getTasks: (params) => {
    return api.get('/tasks', { params })
  },
  
  // 获取任务详情
  getTask: (id) => {
    return api.get(`/tasks/${id}`)
  },
  
  // 创建任务
  createTask: (data) => {
    return api.post('/tasks', data)
  },
  
  // 更新任务
  updateTask: (id, data) => {
    return api.put(`/tasks/${id}`, data)
  },
  
  // 删除任务
  deleteTask: (id) => {
    return api.delete(`/tasks/${id}`)
  },
  
  // 完成任务
  completeTask: (id) => {
    return api.post(`/tasks/${id}/complete`)
  },
  
  // 放弃任务
  abandonTask: (id) => {
    return api.post(`/tasks/${id}/abandon`)
  }
}

// 番茄钟相关API
export const pomodoroApi = {
  // 获取番茄钟设置
  getSettings: () => {
    return api.get('/pomodoro/settings')
  },
  
  // 更新番茄钟设置
  updateSettings: (data) => {
    return api.put('/pomodoro/settings', data)
  },
  
  // 获取番茄钟统计
  getStats: (params) => {
    return api.get('/pomodoro/stats', { params })
  }
}

// 系统设置相关API
export const settingsApi = {
  // 获取系统设置
  getSettings: () => {
    return api.get('/settings')
  },
  
  // 更新系统设置
  updateSettings: (data) => {
    return api.put('/settings', data)
  },
  
  // 备份数据
  backupData: () => {
    return api.post('/settings/backup')
  },
  
  // 恢复数据
  restoreData: () => {
    return api.post('/settings/restore')
  },
  
  // 导出数据
  exportData: () => {
    return api.get('/settings/export', { responseType: 'blob' })
  },
  
  // 清理数据
  clearData: () => {
    return api.post('/settings/clear')
  }
}

// 同步相关API
export const syncApi = {
  // 启动同步
  startSync: () => {
    return api.post('/sync/start')
  },
  
  // 停止同步
  stopSync: () => {
    return api.post('/sync/stop')
  },
  
  // 获取同步状态
  getSyncStatus: () => {
    return api.get('/sync/status')
  }
}

export default {
  task: taskApi,
  pomodoro: pomodoroApi,
  settings: settingsApi
} 