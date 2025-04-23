import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref([])
  const loading = ref(false)
  const error = ref(null)

  const getTasks = computed(() => tasks.value)
  const getLoading = computed(() => loading.value)
  const getError = computed(() => error.value)

  const fetchTasks = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get('/api/tasks')
      tasks.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('获取任务列表失败:', err)
    } finally {
      loading.value = false
    }
  }

  const createTask = async (taskData) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post('/api/tasks', taskData)
      tasks.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('创建任务失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateTask = async (taskId, taskData) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.put(`/api/tasks/${taskId}`, taskData)
      const index = tasks.value.findIndex(task => task.id === taskId)
      if (index !== -1) {
        tasks.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('更新任务失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteTask = async (taskId) => {
    loading.value = true
    error.value = null
    try {
      await axios.delete(`/api/tasks/${taskId}`)
      const index = tasks.value.findIndex(task => task.id === taskId)
      if (index !== -1) {
        tasks.value.splice(index, 1)
      }
    } catch (err) {
      error.value = err.message
      console.error('删除任务失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const getTaskById = (taskId) => {
    return tasks.value.find(task => task.id === taskId)
  }

  return {
    tasks,
    loading,
    error,
    getTasks,
    getLoading,
    getError,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    getTaskById
  }
}) 