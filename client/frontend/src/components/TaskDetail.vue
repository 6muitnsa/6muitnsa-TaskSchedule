<template>
  <div class="task-detail">
    <el-descriptions :column="1" border>
      <el-descriptions-item label="任务名称">
        {{ task.name }}
      </el-descriptions-item>
      <el-descriptions-item label="任务描述">
        {{ task.description }}
      </el-descriptions-item>
      <el-descriptions-item label="优先级">
        <el-tag :type="getPriorityType(task.priority)">
          {{ getPriorityText(task.priority) }}
        </el-tag>
      </el-descriptions-item>
      <el-descriptions-item label="预计时间">
        {{ task.estimated_time }}分钟
      </el-descriptions-item>
      <el-descriptions-item label="周期类型">
        {{ getPeriodTypeText(task.period_type) }}
      </el-descriptions-item>
      <el-descriptions-item label="完成次数">
        {{ task.times }}
      </el-descriptions-item>
      <el-descriptions-item label="时间类型">
        {{ getTimeTypeText(task.time_type) }}
      </el-descriptions-item>
      <el-descriptions-item
        v-if="task.time_type === 'fixed'"
        label="具体时间"
      >
        {{ formatTime(task.specific_time) }}
      </el-descriptions-item>
      <el-descriptions-item label="地点">
        {{ getLocationName(task.location_id) }}
      </el-descriptions-item>
      <el-descriptions-item label="创建时间">
        {{ formatDateTime(task.created_at) }}
      </el-descriptions-item>
      <el-descriptions-item label="最后更新时间">
        {{ formatDateTime(task.updated_at) }}
      </el-descriptions-item>
    </el-descriptions>

    <div class="task-actions">
      <el-button type="primary" @click="editTask">编辑</el-button>
      <el-button type="danger" @click="deleteTask">删除</el-button>
      <el-button @click="$emit('close')">关闭</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'

const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete', 'close'])

const locations = ref([])

onMounted(async () => {
  // TODO: 获取地点列表
})

const getPriorityType = (priority) => {
  if (priority >= 2001) return 'danger'
  if (priority >= 1001) return 'warning'
  return 'info'
}

const getPriorityText = (priority) => {
  if (priority >= 2001) return '高'
  if (priority >= 1001) return '中'
  return '低'
}

const getPeriodTypeText = (type) => {
  const map = {
    once: '一次性',
    daily: '每日',
    weekly: '每周',
    monthly: '每月'
  }
  return map[type] || type
}

const getTimeTypeText = (type) => {
  const map = {
    fixed: '固定时间',
    flexible: '灵活时间'
  }
  return map[type] || type
}

const formatTime = (time) => {
  if (!time) return ''
  return format(new Date(time), 'HH:mm')
}

const formatDateTime = (datetime) => {
  if (!datetime) return ''
  return format(new Date(datetime), 'yyyy-MM-dd HH:mm:ss', { locale: zhCN })
}

const getLocationName = (id) => {
  const location = locations.value.find(l => l.id === id)
  return location ? location.name : '未知地点'
}

const editTask = () => {
  emit('edit', props.task)
  emit('close')
}

const deleteTask = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
      type: 'warning'
    })
    emit('delete', props.task)
    emit('close')
  } catch {
    // 用户取消删除
  }
}
</script>

<style scoped>
.task-detail {
  padding: 20px;
}

.task-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 