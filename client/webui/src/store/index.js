import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    tasks: [],
    currentTask: null,
    schedule: [],
    pomodoroStatus: null,
    syncStatus: 'idle'
  },
  mutations: {
    SET_TASKS(state, tasks) {
      state.tasks = tasks
    },
    SET_CURRENT_TASK(state, task) {
      state.currentTask = task
    },
    SET_SCHEDULE(state, schedule) {
      state.schedule = schedule
    },
    SET_POMODORO_STATUS(state, status) {
      state.pomodoroStatus = status
    },
    SET_SYNC_STATUS(state, status) {
      state.syncStatus = status
    }
  },
  actions: {
    async fetchTasks({ commit }) {
      try {
        const response = await axios.get('/tasks/')
        commit('SET_TASKS', response.data)
      } catch (error) {
        console.error('Error fetching tasks:', error)
      }
    },
    async createTask({ dispatch }, taskData) {
      try {
        await axios.post('/tasks/', taskData)
        dispatch('fetchTasks')
      } catch (error) {
        console.error('Error creating task:', error)
      }
    },
    async updateTask({ dispatch }, { taskId, taskData }) {
      try {
        await axios.put(`/tasks/${taskId}`, taskData)
        dispatch('fetchTasks')
      } catch (error) {
        console.error('Error updating task:', error)
      }
    },
    async deleteTask({ dispatch }, taskId) {
      try {
        await axios.delete(`/tasks/${taskId}`)
        dispatch('fetchTasks')
      } catch (error) {
        console.error('Error deleting task:', error)
      }
    },
    async startPomodoro({ commit }, taskId) {
      try {
        const response = await axios.post(`/pomodoros/start/${taskId}`)
        commit('SET_POMODORO_STATUS', response.data)
      } catch (error) {
        console.error('Error starting pomodoro:', error)
      }
    },
    async startRest({ commit }) {
      try {
        const response = await axios.post('/pomodoros/rest/')
        commit('SET_POMODORO_STATUS', response.data)
      } catch (error) {
        console.error('Error starting rest:', error)
      }
    },
    async endPomodoro({ commit }) {
      try {
        const response = await axios.post('/pomodoros/end/')
        commit('SET_POMODORO_STATUS', null)
      } catch (error) {
        console.error('Error ending pomodoro:', error)
      }
    },
    async startSync({ commit }) {
      try {
        const response = await axios.post('/sync/start/')
        commit('SET_SYNC_STATUS', 'syncing')
      } catch (error) {
        console.error('Error starting sync:', error)
      }
    },
    async stopSync({ commit }) {
      try {
        await axios.post('/sync/stop/')
        commit('SET_SYNC_STATUS', 'idle')
      } catch (error) {
        console.error('Error stopping sync:', error)
      }
    },
    async pullChanges({ dispatch }) {
      try {
        await axios.post('/sync/pull/')
        dispatch('fetchTasks')
      } catch (error) {
        console.error('Error pulling changes:', error)
      }
    }
  },
  getters: {
    pendingTasks: state => state.tasks.filter(task => task.status === 'pending'),
    completedTasks: state => state.tasks.filter(task => task.status === 'completed'),
    highPriorityTasks: state => state.tasks.filter(task => task.priority > 7),
    tasksByTag: state => tag => state.tasks.filter(task => task.tags.includes(tag))
  }
}) 