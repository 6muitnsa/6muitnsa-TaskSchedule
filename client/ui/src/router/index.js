import { createRouter, createWebHistory } from 'vue-router'

// 路由路径常量
export const ROUTE_PATHS = {
  DASHBOARD: '/',
  SETTINGS: '/settings',
  SETTINGS_GENERAL: '/settings/general',
  SETTINGS_SCHEDULER: '/settings/scheduler',
  SETTINGS_PRIORITY: '/settings/priority',
  SETTINGS_TIME: '/settings/time',
  STATISTICS: '/statistics',
  POMODORO: '/pomodoro',
  SCHEDULER: '/scheduler',
  TASKS: '/tasks',
  TASK_LIST: '/tasks/list',
  TASK_MANAGE: '/tasks/manage',
  TASK_CREATE: '/tasks/create',
  TASK_EDIT: '/tasks/edit/:id',
  TASK_DETAIL: '/tasks/:id',
  STATISTICS_DETAIL: '/statistics/:id'
}

const routes = [
  {
    path: ROUTE_PATHS.DASHBOARD,
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { title: '仪表盘' }
  },
  {
    path: ROUTE_PATHS.SETTINGS,
    redirect: ROUTE_PATHS.SETTINGS_GENERAL
  },
  {
    path: ROUTE_PATHS.SETTINGS_GENERAL,
    name: 'SettingsGeneral',
    component: () => import('../views/settings/GeneralSettings.vue'),
    meta: { title: '基本设置' }
  },
  {
    path: ROUTE_PATHS.SETTINGS_SCHEDULER,
    name: 'SettingsScheduler',
    component: () => import('../views/settings/SchedulerSettings.vue'),
    meta: { title: '调度设置' }
  },
  {
    path: ROUTE_PATHS.SETTINGS_PRIORITY,
    name: 'SettingsPriority',
    component: () => import('../views/settings/PrioritySettings.vue'),
    meta: { title: '优先级设置' }
  },
  {
    path: ROUTE_PATHS.SETTINGS_TIME,
    name: 'SettingsTime',
    component: () => import('../views/settings/TimeSettings.vue'),
    meta: { title: '时间设置' }
  },
  {
    path: ROUTE_PATHS.STATISTICS,
    name: 'Statistics',
    component: () => import('../views/Statistics.vue'),
    meta: { title: '统计' }
  },
  {
    path: ROUTE_PATHS.POMODORO,
    name: 'Pomodoro',
    component: () => import('../views/Pomodoro.vue'),
    meta: { title: '番茄钟' }
  },
  {
    path: ROUTE_PATHS.SCHEDULER,
    name: 'Scheduler',
    component: () => import('../views/SchedulerView.vue'),
    meta: { title: '调度器' }
  },
  {
    path: ROUTE_PATHS.TASKS,
    redirect: ROUTE_PATHS.TASK_LIST
  },
  {
    path: ROUTE_PATHS.TASK_LIST,
    name: 'TaskList',
    component: () => import('../views/tasks/TaskList.vue'),
    meta: { title: '任务列表' }
  },
  {
    path: ROUTE_PATHS.TASK_MANAGE,
    name: 'TaskManagement',
    component: () => import('../views/tasks/TaskManagement.vue'),
    meta: { title: '任务管理' }
  },
  {
    path: ROUTE_PATHS.TASK_CREATE,
    name: 'TaskCreate',
    component: () => import('../views/tasks/CreateTask.vue'),
    meta: { title: '创建任务' }
  },
  {
    path: ROUTE_PATHS.TASK_EDIT,
    name: 'TaskEdit',
    component: () => import('../views/tasks/EditTask.vue'),
    meta: { title: '编辑任务' }
  },
  {
    path: ROUTE_PATHS.TASK_DETAIL,
    name: 'TaskDetail',
    component: () => import('../views/tasks/TaskDetail.vue'),
    meta: { title: '任务详情' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '404' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - TaskSchedule` : 'TaskSchedule'
  next()
})

export default router 