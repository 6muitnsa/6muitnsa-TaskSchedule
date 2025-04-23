import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref({
    algorithm: 'fcfs',
    time_granularity: 30,
    default_task_time: 60,
    commute_calculation: true,
    auto_schedule: true
  })

  const loading = ref(false)
  const error = ref(null)

  const getSettings = computed(() => settings.value)
  const getLoading = computed(() => loading.value)
  const getError = computed(() => error.value)

  const fetchSettings = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get('/api/settings')
      settings.value = response.data
    } catch (err) {
      error.value = err.message
      console.error('获取设置失败:', err)
    } finally {
      loading.value = false
    }
  }

  const updateSettings = async (newSettings) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.put('/api/settings', newSettings)
      settings.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('更新设置失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const resetSettings = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post('/api/settings/reset')
      settings.value = response.data
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('重置设置失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    settings,
    loading,
    error,
    getSettings,
    getLoading,
    getError,
    fetchSettings,
    updateSettings,
    resetSettings
  }
}) 