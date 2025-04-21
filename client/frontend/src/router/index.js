import { createRouter, createWebHistory } from 'vue-router'
import TaskList from '../views/TaskList.vue'
import TaskCreate from '../views/TaskCreate.vue'
import TaskDetail from '../views/TaskDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'task-list',
      component: TaskList
    },
    {
      path: '/create',
      name: 'task-create',
      component: TaskCreate
    },
    {
      path: '/task/:id',
      name: 'task-detail',
      component: TaskDetail
    }
  ]
})

export default router 