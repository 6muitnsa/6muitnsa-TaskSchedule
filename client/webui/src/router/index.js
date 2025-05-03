import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: () => import('../views/Tasks.vue')
  },
  {
    path: '/tasks/create',
    name: 'CreateTask',
    component: () => import('../views/CreateTask.vue')
  },
  {
    path: '/tasks/:id',
    name: 'TaskDetail',
    component: () => import('../views/TaskDetail.vue')
  },
  {
    path: '/pomodoro',
    name: 'Pomodoro',
    component: () => import('../views/Pomodoro.vue')
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: () => import('../views/Schedule.vue')
  },
  {
    path: '/sync',
    name: 'Sync',
    component: () => import('../views/Sync.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router 