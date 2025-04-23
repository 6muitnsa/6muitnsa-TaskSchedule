import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import TaskList from '../views/TaskList.vue'
import CalendarView from '../views/CalendarView.vue'
import Settings from '../views/Settings.vue'
import PomodoroTimer from '../components/PomodoroTimer.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/tasks',
    name: 'TaskList',
    component: TaskList
  },
  {
    path: '/calendar',
    name: 'CalendarView',
    component: CalendarView
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/pomodoro',
    name: 'PomodoroTimer',
    component: PomodoroTimer
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 