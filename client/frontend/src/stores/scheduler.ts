import { defineStore } from 'pinia'
import { ref } from 'vue'
import { schedulerService } from '@/services/schedulerService'

export const useSchedulerStore = defineStore('scheduler', () => {
  const algorithm = ref('EDF')
  const loading = ref(false)
  const error = ref<string | null>(null)

  const setAlgorithm = async (newAlgorithm: string) => {
    try {
      loading.value = true
      error.value = null
      await schedulerService.setAlgorithm(newAlgorithm)
      algorithm.value = newAlgorithm
    } catch (e) {
      error.value = '设置算法失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  const generateSchedule = async () => {
    try {
      loading.value = true
      error.value = null
      return await schedulerService.generateSchedule()
    } catch (e) {
      error.value = '生成调度失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    algorithm,
    loading,
    error,
    setAlgorithm,
    generateSchedule
  }
}) 