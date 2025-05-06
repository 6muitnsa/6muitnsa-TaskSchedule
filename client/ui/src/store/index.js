import { defineStore } from 'pinia'
import api from '../api'

// 任务状态管理
export const useTaskStore = defineStore('task', {
  state: () => ({
    tasks: [],
    currentTask: null,
    loading: false,
    error: null
  }),
  
  getters: {
    // 获取未完成任务
    incompleteTasks: (state) => {
      return state.tasks.filter(task => task.status !== 'completed')
    },
    
    // 获取已完成任务
    completedTasks: (state) => {
      return state.tasks.filter(task => task.status === 'completed')
    },
    
    // 获取进行中任务
    inProgressTasks: (state) => {
      return state.tasks.filter(task => task.status === 'in_progress')
    }
  },
  
  actions: {
    // 获取任务列表
    async fetchTasks(params) {
      this.loading = true
      this.error = null
      try {
        const response = await api.task.getTasks(params)
        this.tasks = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 获取任务详情
    async fetchTask(id) {
      this.loading = true
      this.error = null
      try {
        const response = await api.task.getTask(id)
        this.currentTask = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 创建任务
    async createTask(taskData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.task.createTask(taskData)
        this.tasks.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 更新任务
    async updateTask(id, taskData) {
      this.loading = true
      this.error = null
      try {
        const response = await api.task.updateTask(id, taskData)
        const index = this.tasks.findIndex(task => task.id === id)
        if (index !== -1) {
          this.tasks[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 删除任务
    async deleteTask(id) {
      this.loading = true
      this.error = null
      try {
        await api.task.deleteTask(id)
        this.tasks = this.tasks.filter(task => task.id !== id)
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 完成任务
    async completeTask(id) {
      this.loading = true
      this.error = null
      try {
        const response = await api.task.completeTask(id)
        const index = this.tasks.findIndex(task => task.id === id)
        if (index !== -1) {
          this.tasks[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 放弃任务
    async abandonTask(id) {
      this.loading = true
      this.error = null
      try {
        const response = await api.task.abandonTask(id)
        const index = this.tasks.findIndex(task => task.id === id)
        if (index !== -1) {
          this.tasks[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})

// 番茄钟状态管理
export const usePomodoroStore = defineStore('pomodoro', {
  state: () => ({
    settings: {
      focusTime: 25,
      breakTime: 5,
      longBreakTime: 15,
      longBreakInterval: 4
    },
    stats: {
      completedPomodoros: 0,
      focusTime: 0,
      breakTime: 0
    },
    loading: false,
    error: null
  }),
  
  actions: {
    // 获取番茄钟设置
    async fetchSettings() {
      this.loading = true
      this.error = null
      try {
        const response = await api.pomodoro.getSettings()
        this.settings = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 更新番茄钟设置
    async updateSettings(settings) {
      this.loading = true
      this.error = null
      try {
        const response = await api.pomodoro.updateSettings(settings)
        this.settings = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 获取番茄钟统计
    async fetchStats(params) {
      this.loading = true
      this.error = null
      try {
        const response = await api.pomodoro.getStats(params)
        this.stats = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
})

// 系统设置状态管理
export const useSettingsStore = defineStore('settings', {
  state: () => ({
    settings: {
      theme: 'light',
      language: 'zh-CN',
      timezone: 'Asia/Shanghai',
      notifications: {
        taskReminder: true,
        methods: ['desktop', 'browser'],
        reminderTime: '15',
        quietHours: {
          start: null,
          end: null
        }
      },
      data: {
        autoBackup: true,
        backupFrequency: 'daily'
      }
    },
    loading: false,
    error: null
  }),
  
  actions: {
    // 获取系统设置
    async fetchSettings() {
      this.loading = true
      this.error = null
      try {
        const response = await api.settings.getSettings()
        this.settings = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    // 更新系统设置
    async updateSettings(settings) {
      this.loading = true
      this.error = null
      try {
        const response = await api.settings.updateSettings(settings)
        this.settings = response.data
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 备份数据
    async backupData() {
      this.loading = true
      this.error = null
      try {
        await api.settings.backupData()
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 恢复数据
    async restoreData() {
      this.loading = true
      this.error = null
      try {
        await api.settings.restoreData()
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 导出数据
    async exportData() {
      this.loading = true
      this.error = null
      try {
        const response = await api.settings.exportData()
        const url = window.URL.createObjectURL(new Blob([response]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'task-schedule-data.json')
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },
    
    // 清理数据
    async clearData() {
      this.loading = true
      this.error = null
      try {
        await api.settings.clearData()
      } catch (error) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 