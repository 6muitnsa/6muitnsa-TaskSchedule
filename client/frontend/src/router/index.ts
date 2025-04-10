import { createRouter, createWebHistory } from 'vue-router'
import TaskList from '../components/TaskList.vue'
import TaskDetail from '../components/TaskDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: TaskList
    },
    {
      path: '/tasks/:id',
      name: 'task-detail',
      component: TaskDetail
    }
  ]
})

export default router 