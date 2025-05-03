<template>
  <div class="task-detail">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>任务详情</span>
              <div>
                <el-button type="primary" @click="editTask">编辑</el-button>
                <el-button type="danger" @click="deleteTask">删除</el-button>
              </div>
            </div>
          </template>
          <div class="task-info">
            <h2>{{ task.title }}</h2>
            <div class="task-meta">
              <el-tag :type="getPriorityType(task.priority)">
                优先级: {{ task.priority }}
              </el-tag>
              <el-tag :type="getStatusType(task.status)">
                {{ getStatusText(task.status) }}
              </el-tag>
              <el-tag v-if="task.due_date">
                截止日期: {{ formatDate(task.due_date) }}
              </el-tag>
            </div>
            <div class="task-tags">
              <el-tag
                v-for="tag in task.tags"
                :key="tag"
                class="tag"
              >
                {{ tag }}
              </el-tag>
            </div>
            <div class="task-description">
              <h3>描述</h3>
              <p>{{ task.description || '暂无描述' }}</p>
            </div>
            <div class="task-timeline">
              <h3>时间线</h3>
              <el-timeline>
                <el-timeline-item
                  v-for="event in taskEvents"
                  :key="event.time"
                  :timestamp="formatDate(event.time)"
                  :type="event.type"
                >
                  {{ event.content }}
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>相关番茄钟</span>
            </div>
          </template>
          <el-table
            :data="relatedPomodoros"
            style="width: 100%"
          >
            <el-table-column
              prop="type"
              label="类型"
              width="100"
            >
              <template #default="{ row }">
                <el-tag :type="row.type === 'focus' ? 'success' : 'info'">
                  {{ row.type === 'focus' ? '专注' : '休息' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              prop="start_time"
              label="开始时间"
              width="180"
            >
              <template #default="{ row }">
                {{ formatDate(row.start_time) }}
              </template>
            </el-table-column>
            <el-table-column
              prop="end_time"
              label="结束时间"
              width="180"
            >
              <template #default="{ row }">
                {{ row.end_time ? formatDate(row.end_time) : '进行中' }}
              </template>
            </el-table-column>
            <el-table-column
              prop="duration"
              label="时长"
              width="100"
            >
              <template #default="{ row }">
                {{ formatDuration(row.duration) }}
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import dayjs from 'dayjs'

export default {
  name: 'TaskDetail',
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const taskId = route.params.id

    const task = computed(() => {
      return store.state.tasks.find(t => t.task_id === taskId)
    })

    const taskEvents = computed(() => {
      if (!task.value) return []
      const events = []
      events.push({
        time: task.value.created_at,
        type: 'primary',
        content: '任务创建'
      })
      if (task.value.updated_at) {
        events.push({
          time: task.value.updated_at,
          type: 'info',
          content: '任务更新'
        })
      }
      if (task.value.completed_at) {
        events.push({
          time: task.value.completed_at,
          type: 'success',
          content: '任务完成'
        })
      }
      return events.sort((a, b) => new Date(b.time) - new Date(a.time))
    })

    const relatedPomodoros = computed(() => {
      return store.state.pomodoroHistory.filter(
        p => p.task_id === taskId
      ).sort((a, b) => new Date(b.start_time) - new Date(a.start_time))
    })

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

    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }

    const formatDuration = (duration) => {
      const minutes = Math.floor(duration / 60)
      const seconds = duration % 60
      return `${minutes}分${seconds}秒`
    }

    const editTask = () => {
      router.push(`/tasks/${taskId}/edit`)
    }

    const deleteTask = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要删除这个任务吗？',
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        await store.dispatch('deleteTask', taskId)
        ElMessage.success('任务删除成功')
        router.push('/tasks')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除任务失败:', error)
        }
      }
    }

    onMounted(async () => {
      await store.dispatch('fetchTasks')
      if (!task.value) {
        ElMessage.error('任务不存在')
        router.push('/tasks')
      }
    })

    return {
      task,
      taskEvents,
      relatedPomodoros,
      getPriorityType,
      getStatusType,
      getStatusText,
      formatDate,
      formatDuration,
      editTask,
      deleteTask
    }
  }
}
</script>

<style lang="scss" scoped>
.task-detail {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .task-info {
    h2 {
      margin: 0 0 20px;
    }

    .task-meta {
      margin-bottom: 20px;
      .el-tag {
        margin-right: 10px;
      }
    }

    .task-tags {
      margin-bottom: 20px;
      .tag {
        margin-right: 10px;
        margin-bottom: 10px;
      }
    }

    .task-description {
      margin-bottom: 30px;
      h3 {
        margin: 0 0 10px;
        font-size: 16px;
      }
      p {
        margin: 0;
        color: #666;
      }
    }

    .task-timeline {
      h3 {
        margin: 0 0 20px;
        font-size: 16px;
      }
    }
  }
}
</style> 