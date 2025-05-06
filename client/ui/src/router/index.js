import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/Dashboard.vue'),
      meta: {
        title: '仪表板'
      }
    },
    {
      path: '/tasks',
      name: 'TaskList',
      component: () => import('../views/tasks/TaskList.vue'),
      meta: {
        title: '任务列表'
      }
    },
    {
      path: '/tasks/create',
      name: 'CreateTask',
      component: () => import('../views/tasks/CreateTask.vue'),
      meta: {
        title: '创建任务'
      }
    },
    {
      path: '/tasks/edit/:id',
      name: 'EditTask',
      component: () => import('../views/tasks/EditTask.vue'),
      meta: {
        title: '编辑任务'
      }
    },
    {
      path: '/tasks/manage',
      name: 'TaskManagement',
      component: () => import('../views/tasks/TaskManagement.vue'),
      meta: {
        title: '任务管理'
      }
    },
    {
      path: '/pomodoro',
      name: 'Pomodoro',
      component: () => import('../views/Pomodoro.vue'),
      meta: {
        title: '番茄钟'
      }
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('../views/Settings.vue'),
      meta: {
        title: '设置'
      }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title} - 任务调度系统`
  next()
})

export default router 