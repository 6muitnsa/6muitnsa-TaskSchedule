import { createRouter, createWebHistory } from 'vue-router'
import TaskList from '@/components/TaskList.vue'
import PomodoroTimer from '@/components/PomodoroTimer.vue'
import TimeStatistics from '@/components/TimeStatistics.vue'
import ScheduleView from '@/components/ScheduleView.vue'
import TaskDetail from '@/components/TaskDetail.vue'
import TaskForm from '@/components/TaskForm.vue'
import AlgorithmSelection from '@/components/AlgorithmSelection.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/tasks'
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: TaskList
    },
    {
      path: '/tasks/create',
      name: 'taskCreate',
      component: TaskForm
    },
    {
      path: '/tasks/:id',
      name: 'taskDetail',
      component: TaskDetail
    },
    {
      path: '/tasks/:id/edit',
      name: 'taskEdit',
      component: TaskForm
    },
    {
      path: '/pomodoro',
      name: 'pomodoro',
      component: PomodoroTimer
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: TimeStatistics
    },
    {
      path: '/schedule',
      name: 'schedule',
      component: ScheduleView
    },
    {
      path: '/schedule/algorithms',
      name: 'algorithmSelection',
      component: AlgorithmSelection
    }
  ]
})

export default router 