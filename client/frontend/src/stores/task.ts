import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Task } from '@/types/task'
import { taskService } from '@/services/taskService'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchTasks = async () => {
    try {
      loading.value = true
      error.value = null
      tasks.value = await taskService.getTasks()
    } catch (e) {
      error.value = '获取任务列表失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  const getTaskById = async (id: string) => {
    try {
      loading.value = true
      error.value = null
      return await taskService.getTaskById(id)
    } catch (e) {
      error.value = '获取任务详情失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  const createTask = async (task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      loading.value = true
      error.value = null
      const newTask = await taskService.createTask(task)
      tasks.value.push(newTask)
      return newTask
    } catch (e) {
      error.value = '创建任务失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  const updateTask = async (id: string, task: Partial<Task>) => {
    try {
      loading.value = true
      error.value = null
      const updatedTask = await taskService.updateTask(id, task)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = updatedTask
      }
      return updatedTask
    } catch (e) {
      error.value = '更新任务失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  const deleteTask = async (id: string) => {
    try {
      loading.value = true
      error.value = null
      await taskService.deleteTask(id)
      tasks.value = tasks.value.filter(t => t.id !== id)
    } catch (e) {
      error.value = '删除任务失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    getTaskById,
    createTask,
    updateTask,
    deleteTask
  }
}) 