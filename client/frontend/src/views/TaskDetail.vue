<template>
  <div class="task-detail">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务详情</span>
          <el-button-group>
            <el-button type="primary" @click="handleEdit">编辑</el-button>
            <el-button type="danger" @click="handleDelete">删除</el-button>
          </el-button-group>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="任务名称">{{ task.name }}</el-descriptions-item>
        <el-descriptions-item label="任务类型">{{ getTaskTypeText(task.task_type) }}</el-descriptions-item>
        <el-descriptions-item label="优先级">{{ task.priority }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(task.status)">
            {{ getStatusText(task.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="时间状态">
          <el-tag :type="getTimeStatusType(task.time_status)">
            {{ getTimeStatusText(task.time_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="是否锁定">
          <el-tag :type="task.is_locked ? 'danger' : 'success'">
            {{ task.is_locked ? '已锁定' : '未锁定' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="开始时间">{{ formatDateTime(task.start_time) }}</el-descriptions-item>
        <el-descriptions-item label="结束时间">{{ formatDateTime(task.end_time) }}</el-descriptions-item>
        <el-descriptions-item label="预计时间">{{ task.estimated_time }}分钟</el-descriptions-item>
        <el-descriptions-item label="地点">{{ task.location || '无' }}</el-descriptions-item>
        <el-descriptions-item label="通勤时间">{{ task.commute_time }}分钟</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ task.description }}</el-descriptions-item>
      </el-descriptions>

      <!-- 周期性任务信息 -->
      <template v-if="task.is_periodic">
        <el-divider>周期性任务信息</el-divider>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="周期类型">{{ getPeriodTypeText(task.period_type) }}</el-descriptions-item>
          <el-descriptions-item label="周期值">{{ task.period_value }}</el-descriptions-item>
          <el-descriptions-item label="周期天数" v-if="task.period_type === 'weekly'">
            {{ formatPeriodDays(task.period_days) }}
          </el-descriptions-item>
          <el-descriptions-item label="总次数">{{ task.total_count }}</el-descriptions-item>
          <el-descriptions-item label="已完成次数">{{ task.completed_count }}</el-descriptions-item>
        </el-descriptions>
      </template>

      <!-- 任务反馈 -->
      <el-divider>任务反馈</el-divider>
      <el-form :model="feedbackForm" label-width="120px">
        <el-form-item label="任务满意度">
          <el-rate v-model="feedbackForm.satisfaction" :max="5" />
        </el-form-item>
        <el-form-item label="反馈意见">
          <el-input
            v-model="feedbackForm.comment"
            type="textarea"
            :rows="3"
            placeholder="请输入对任务的反馈意见"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitFeedback">提交反馈</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { taskApi } from '../api/task'

const route = useRoute()
const router = useRouter()
const task = ref({})
const feedbackForm = ref({
  satisfaction: 0,
  comment: ''
})

const getTaskTypeText = (type) => {
  const types = {
    work: '工作',
    study: '学习',
    life: '生活',
    other: '其他'
  }
  return types[type] || type
}

const getStatusType = (status) => {
  const types = {
    pending: 'warning',
    completed: 'success',
    follow_up: 'info',
    cancelled: 'danger'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待完成',
    completed: '已完成',
    follow_up: '待跟进',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const getTimeStatusType = (status) => {
  const types = {
    not_started: 'info',
    in_progress: 'primary',
    overdue: 'danger',
    completed: 'success'
  }
  return types[status] || 'info'
}

const getTimeStatusText = (status) => {
  const texts = {
    not_started: '未开始',
    in_progress: '进行中',
    overdue: '已超时',
    completed: '已完成'
  }
  return texts[status] || status
}

const getPeriodTypeText = (type) => {
  const types = {
    daily: '每天',
    weekly: '每周',
    monthly: '每月'
  }
  return types[type] || type
}

const formatDateTime = (datetime) => {
  if (!datetime) return '无'
  return new Date(datetime).toLocaleString()
}

const formatPeriodDays = (days) => {
  if (!days) return '无'
  const dayMap = {
    '1': '周一',
    '2': '周二',
    '3': '周三',
    '4': '周四',
    '5': '周五',
    '6': '周六',
    '7': '周日'
  }
  return days.split(',').map(day => dayMap[day]).join('、')
}

const fetchTask = async () => {
  try {
    const response = await taskApi.getTask(route.params.id)
    task.value = response.data
  } catch (error) {
    ElMessage.error('获取任务详情失败')
    console.error('Error fetching task:', error)
  }
}

const handleEdit = () => {
  router.push(`/task/${route.params.id}/edit`)
}

const handleDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
      type: 'warning'
    })
    await taskApi.deleteTask(route.params.id)
    ElMessage.success('删除成功')
    router.push('/')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const submitFeedback = async () => {
  try {
    await taskApi.updateTask(route.params.id, {
      feedback: feedbackForm.value.satisfaction,
      feedback_comment: feedbackForm.value.comment
    })
    ElMessage.success('反馈提交成功')
    fetchTask()
  } catch (error) {
    ElMessage.error('反馈提交失败')
    console.error('Error submitting feedback:', error)
  }
}

onMounted(() => {
  fetchTask()
})
</script>

<style scoped>
.task-detail {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-divider {
  margin: 20px 0;
}
</style> 