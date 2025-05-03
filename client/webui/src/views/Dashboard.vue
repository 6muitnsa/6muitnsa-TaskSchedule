<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>待办任务</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-value">{{ pendingTasksCount }}</div>
            <div class="stat-label">个任务待完成</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>已完成任务</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-value">{{ completedTasksCount }}</div>
            <div class="stat-label">个任务已完成</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>今日番茄钟</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-value">{{ todayPomodorosCount }}</div>
            <div class="stat-label">个番茄钟</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>本周番茄钟</span>
            </div>
          </template>
          <div class="stat-content">
            <div class="stat-value">{{ weekPomodorosCount }}</div>
            <div class="stat-label">个番茄钟</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>今日任务</span>
            </div>
          </template>
          <el-table
            :data="todayTasks"
            style="width: 100%"
          >
            <el-table-column
              prop="title"
              label="任务名称"
              min-width="200"
            />
            <el-table-column
              prop="priority"
              label="优先级"
              width="100"
            >
              <template #default="{ row }">
                <el-tag :type="getPriorityType(row.priority)">
                  {{ row.priority }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              prop="status"
              label="状态"
              width="100"
            >
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>番茄钟统计</span>
            </div>
          </template>
          <div ref="pomodoroChart" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>任务完成趋势</span>
            </div>
          </template>
          <div ref="taskTrendChart" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>日程安排</span>
            </div>
          </template>
          <el-calendar v-model="currentDate">
            <template #dateCell="{ data }">
              <div class="calendar-cell">
                <p>{{ data.day.split('-').slice(2).join('') }}</p>
                <div class="schedule-items">
                  <div
                    v-for="schedule in getSchedulesForDate(data.day)"
                    :key="schedule.schedule_id"
                    class="schedule-item"
                    :class="getScheduleTypeClass(schedule.type)"
                  >
                    {{ schedule.title }}
                  </div>
                </div>
              </div>
            </template>
          </el-calendar>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import * as echarts from 'echarts'
import dayjs from 'dayjs'

export default {
  name: 'Dashboard',
  setup() {
    const store = useStore()
    const currentDate = ref(new Date())
    const pomodoroChart = ref(null)
    const taskTrendChart = ref(null)

    const pendingTasksCount = computed(() => {
      return store.state.tasks.filter(t => t.status === 'pending').length
    })

    const completedTasksCount = computed(() => {
      return store.state.tasks.filter(t => t.status === 'completed').length
    })

    const todayTasks = computed(() => {
      const today = dayjs().format('YYYY-MM-DD')
      return store.state.tasks.filter(task => {
        const taskDate = dayjs(task.due_date).format('YYYY-MM-DD')
        return taskDate === today
      })
    })

    const todayPomodorosCount = computed(() => {
      const today = dayjs().format('YYYY-MM-DD')
      return store.state.pomodoroHistory.filter(p => {
        const pomodoroDate = dayjs(p.start_time).format('YYYY-MM-DD')
        return pomodoroDate === today
      }).length
    })

    const weekPomodorosCount = computed(() => {
      const weekStart = dayjs().startOf('week')
      const weekEnd = dayjs().endOf('week')
      return store.state.pomodoroHistory.filter(p => {
        const pomodoroDate = dayjs(p.start_time)
        return pomodoroDate.isAfter(weekStart) && pomodoroDate.isBefore(weekEnd)
      }).length
    })

    const getSchedulesForDate = (date) => {
      return store.state.schedules.filter(schedule => {
        const scheduleDate = dayjs(schedule.start_time).format('YYYY-MM-DD')
        return scheduleDate === date
      })
    }

    const getPriorityType = (priority) => {
      if (priority >= 8) return 'danger'
      if (priority >= 5) return 'warning'
      return 'info'
    }

    const getStatusType = (status) => {
      switch (status) {
        case 'completed':
          return 'success'
        case 'in_progress':
          return 'primary'
        default:
          return 'info'
      }
    }

    const getStatusText = (status) => {
      switch (status) {
        case 'completed':
          return '已完成'
        case 'in_progress':
          return '进行中'
        default:
          return '待办'
      }
    }

    const getScheduleTypeClass = (type) => {
      switch (type) {
        case 'work':
          return 'work'
        case 'study':
          return 'study'
        case 'rest':
          return 'rest'
        default:
          return 'other'
      }
    }

    const initPomodoroChart = () => {
      const chart = echarts.init(pomodoroChart.value)
      const option = {
        title: {
          text: '本周番茄钟分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '番茄钟类型',
            type: 'pie',
            radius: '50%',
            data: [
              { value: 10, name: '专注' },
              { value: 5, name: '休息' }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      chart.setOption(option)
    }

    const initTaskTrendChart = () => {
      const chart = echarts.init(taskTrendChart.value)
      const option = {
        title: {
          text: '任务完成趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '完成任务',
            type: 'line',
            data: [5, 8, 6, 7, 9, 4, 3]
          }
        ]
      }
      chart.setOption(option)
    }

    onMounted(async () => {
      await store.dispatch('fetchTasks')
      await store.dispatch('fetchPomodoroHistory')
      await store.dispatch('fetchSchedules')
      initPomodoroChart()
      initTaskTrendChart()
    })

    return {
      currentDate,
      pomodoroChart,
      taskTrendChart,
      pendingTasksCount,
      completedTasksCount,
      todayTasks,
      todayPomodorosCount,
      weekPomodorosCount,
      getSchedulesForDate,
      getPriorityType,
      getStatusType,
      getStatusText,
      getScheduleTypeClass
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  .mt-20 {
    margin-top: 20px;
  }

  .stat-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .stat-content {
      text-align: center;
      padding: 20px 0;

      .stat-value {
        font-size: 36px;
        font-weight: bold;
        color: #409EFF;
      }

      .stat-label {
        margin-top: 10px;
        color: #666;
      }
    }
  }

  .chart {
    height: 300px;
  }

  .calendar-cell {
    height: 100%;
    padding: 4px;

    p {
      margin: 0;
      font-size: 14px;
      color: #666;
    }

    .schedule-items {
      margin-top: 4px;
    }

    .schedule-item {
      margin: 2px 0;
      padding: 2px 4px;
      border-radius: 2px;
      font-size: 12px;
      color: white;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;

      &.work {
        background-color: #409EFF;
      }

      &.study {
        background-color: #67C23A;
      }

      &.rest {
        background-color: #E6A23C;
      }

      &.other {
        background-color: #909399;
      }
    }
  }
}
</style> 