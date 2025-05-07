import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',  // 使用环境变量
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
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
    // 统一错误处理
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 任务相关API
export const taskApi = {
  // 获取任务列表
  getTasks(params) {
    return api.get('/tasks', { params })
  },

  // 获取单个任务
  getTask(id) {
    return api.get(`/tasks/${id}`)
  },

  // 创建任务
  createTask(data) {
    return api.post('/tasks', data)
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
  },

  // 更新任务标签
  updateTaskTags(id, tags) {
    return api.patch(`/tasks/${id}/tags`, { tags })
  },

  // 更新任务时间信息
  updateTaskTimeInfo(id, timeInfo) {
    return api.patch(`/tasks/${id}/time-info`, timeInfo)
  },

  // 更新任务复杂信息
  updateTaskComplexInfo(id, complexInfo) {
    return api.patch(`/tasks/${id}/complex-info`, complexInfo)
  },

  // 完成任务
  completeTask(id, data = {}) {
    return api.post(`/tasks/${id}/complete`, data)
  },

  // 放弃任务
  abandonTask(id) {
    return api.post(`/tasks/${id}/abandon`)
  },

  // 批量完成任务
  batchComplete(taskIds) {
    return api.post('/batch/complete', { task_ids: taskIds })
  },

  // 批量放弃任务
  batchAbandon(taskIds) {
    return api.post('/batch/abandon', { task_ids: taskIds })
  },

  // 批量更新标签
  batchUpdateTags(taskIds, tagIds) {
    return api.post('/batch/tags', { task_ids: taskIds, tag_ids: tagIds })
  },

  // 批量更新位置
  batchUpdateLocation(taskIds, locationId) {
    return api.post('/batch/locations', { task_ids: taskIds, location_id: locationId })
  },

  // 批量删除任务
  batchDelete(taskIds) {
    return api.post('/batch/delete', { task_ids: taskIds })
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
  },

  // 创建番茄钟记录
  createPomodoro: (data) => {
    const pomodoroData = {
      pomodoro_id: data.pomodoro_id,
      task_id: data.task_id,
      focus_time: data.focus_time,
      rest_time: data.rest_time,
      start_time: data.start_time,
      end_time: data.end_time,
      status: data.status || '专注中'
    }
    return api.post('/pomodoros', pomodoroData)
  },

  // 更新番茄钟记录
  updatePomodoro: (id, data) => {
    return api.put(`/pomodoros/${id}`, data)
  },

  // 获取番茄钟记录
  getPomodoro: (id) => {
    return api.get(`/pomodoros/${id}`)
  },

  // 获取任务的番茄钟记录
  getTaskPomodoros: (taskId) => {
    return api.get(`/tasks/${taskId}/pomodoros`)
  }
}

// 系统设置相关API
export const settingsApi = {
  // 获取设置
  getSettings: () => {
    return api.get('/settings')
  },
  
  // 更新设置
  updateSettings: (data) => {
    return api.put('/settings', data)
  },
  
  // 获取验证规则
  getValidationRules: () => {
    return api.get('/settings/validation-rules')
  },
  
  // 获取配置文件路径
  getConfigPath: () => {
    return api.get('/settings/path')
  },
  
  // 加载设置
  loadSettings: (path) => {
    return api.post('/settings/load', { path })
  },
  
  // 备份数据
  backupData: () => {
    return api.post('/settings/backup')
  },
  
  // 恢复数据
  restoreData: (data) => {
    return api.post('/settings/restore', data)
  },
  
  // 导出数据
  exportData: () => {
    return api.get('/settings/export')
  },
  
  // 清除数据
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
  },

  // 同步任务
  syncTasks: (data) => {
    const syncData = {
      sync_id: data.sync_id,
      direction: data.direction,
      tasks: data.tasks,
      pomodoros: data.pomodoros,
      timestamp: new Date().toISOString()
    }
    return api.post('/sync/tasks', syncData)
  },

  // 获取同步历史
  getSyncHistory: () => {
    return api.get('/sync/history')
  }
}

// 提醒相关API
export const reminderApi = {
  // 获取提醒列表
  getReminders(params) {
    return api.get('/reminders', { params })
  },

  // 获取单个提醒
  getReminder(id) {
    return api.get(`/reminders/${id}`)
  },

  // 创建提醒
  createReminder(data) {
    return api.post('/reminders', data)
  },

  // 更新提醒
  updateReminder(id, data) {
    return api.put(`/reminders/${id}`, data)
  },

  // 删除提醒
  deleteReminder(id) {
    return api.delete(`/reminders/${id}`)
  },

  // 检查提醒
  checkReminders() {
    return api.post('/reminders/check')
  }
}

// 导入导出相关API
export const importExportApi = {
  // 导出为JSON
  exportToJson() {
    return api.get('/import-export/export/json', {
      responseType: 'blob'
    })
  },

  // 导出为CSV
  exportToCsv() {
    return api.get('/import-export/export/csv', {
      responseType: 'blob'
    })
  },

  // 从JSON导入
  importFromJson(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import-export/import/json', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 从CSV导入
  importFromCsv(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/import-export/import/csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }
}

// 导出所有 API
export * from './statistics'

export { api } 