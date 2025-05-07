<template>
  <div class="task-reminder">
    <el-button type="primary" @click="showReminderDialog">
      <el-icon><Bell /></el-icon>
      设置提醒
    </el-button>

    <!-- 提醒列表 -->
    <div v-if="reminders.length > 0" class="reminder-list">
      <div v-for="reminder in reminders" :key="reminder.id" class="reminder-item">
        <div class="reminder-info">
          <el-tag :type="getReminderTypeTag(reminder.type)">
            {{ getReminderTypeText(reminder.type) }}
          </el-tag>
          <span class="reminder-time">{{ formatDateTime(reminder.time) }}</span>
        </div>
        <div class="reminder-actions">
          <el-switch
            v-model="reminder.is_active"
            @change="handleReminderStatusChange(reminder)"
          />
          <el-button type="danger" link @click="handleDeleteReminder(reminder)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 创建提醒对话框 -->
    <el-dialog
      v-model="showDialog"
      title="设置提醒"
      width="500px"
    >
      <el-form :model="reminderForm" label-width="100px">
        <el-form-item label="提醒类型">
          <el-select v-model="reminderForm.type" placeholder="请选择提醒类型">
            <el-option label="单次提醒" value="once" />
            <el-option label="每天提醒" value="daily" />
            <el-option label="每周提醒" value="weekly" />
            <el-option label="每月提醒" value="monthly" />
          </el-select>
        </el-form-item>
        <el-form-item label="提醒时间">
          <el-date-picker
            v-model="reminderForm.time"
            type="datetime"
            placeholder="请选择提醒时间"
            :disabled-date="disabledDate"
            :disabled-time="disabledTime"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDialog = false">取消</el-button>
          <el-button type="primary" @click="handleCreateReminder">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Bell, Delete } from '@element-plus/icons-vue'
import { reminderApi } from '../api'
import dayjs from 'dayjs'

const props = defineProps({
  taskId: {
    type: Number,
    required: true
  }
})

// 提醒列表
const reminders = ref([])

// 对话框控制
const showDialog = ref(false)

// 提醒表单
const reminderForm = ref({
  type: 'once',
  time: null
})

// 获取提醒列表
const getReminders = async () => {
  try {
    const response = await reminderApi.getReminders({ task_id: props.taskId })
    reminders.value = response.data
  } catch (error) {
    console.error('获取提醒列表失败:', error)
    ElMessage.error('获取提醒列表失败')
  }
}

// 显示创建提醒对话框
const showReminderDialog = () => {
  reminderForm.value = {
    type: 'once',
    time: null
  }
  showDialog.value = true
}

// 创建提醒
const handleCreateReminder = async () => {
  try {
    if (!reminderForm.value.time) {
      ElMessage.warning('请选择提醒时间')
      return
    }

    await reminderApi.createReminder({
      task_id: props.taskId,
      type: reminderForm.value.type,
      time: reminderForm.value.time
    })

    ElMessage.success('创建提醒成功')
    showDialog.value = false
    getReminders()
  } catch (error) {
    console.error('创建提醒失败:', error)
    ElMessage.error('创建提醒失败')
  }
}

// 更新提醒状态
const handleReminderStatusChange = async (reminder) => {
  try {
    await reminderApi.updateReminder(reminder.id, {
      is_active: reminder.is_active
    })
    ElMessage.success('更新提醒状态成功')
  } catch (error) {
    console.error('更新提醒状态失败:', error)
    ElMessage.error('更新提醒状态失败')
    reminder.is_active = !reminder.is_active // 恢复状态
  }
}

// 删除提醒
const handleDeleteReminder = async (reminder) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个提醒吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await reminderApi.deleteReminder(reminder.id)
    ElMessage.success('删除提醒成功')
    getReminders()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除提醒失败:', error)
      ElMessage.error('删除提醒失败')
    }
  }
}

// 获取提醒类型标签样式
const getReminderTypeTag = (type) => {
  const types = {
    once: 'info',
    daily: 'success',
    weekly: 'warning',
    monthly: 'danger'
  }
  return types[type] || 'info'
}

// 获取提醒类型文本
const getReminderTypeText = (type) => {
  const types = {
    once: '单次提醒',
    daily: '每天提醒',
    weekly: '每周提醒',
    monthly: '每月提醒'
  }
  return types[type] || '未知类型'
}

// 格式化日期时间
const formatDateTime = (datetime) => {
  return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 禁用过去的日期
const disabledDate = (time) => {
  return time.getTime() < Date.now() - 8.64e7
}

// 禁用过去的时间
const disabledTime = (date) => {
  if (date && date.getTime() < Date.now()) {
    return {
      disabledHours: () => Array.from({ length: 24 }, (_, i) => i),
      disabledMinutes: () => Array.from({ length: 60 }, (_, i) => i),
      disabledSeconds: () => Array.from({ length: 60 }, (_, i) => i)
    }
  }
  return {}
}

// 初始化
onMounted(() => {
  getReminders()
})
</script>

<style lang="scss" scoped>
.task-reminder {
  .reminder-list {
    margin-top: 16px;

    .reminder-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px;
      border-bottom: 1px solid #EBEEF5;

      &:last-child {
        border-bottom: none;
      }

      .reminder-info {
        display: flex;
        align-items: center;
        gap: 8px;

        .reminder-time {
          color: #606266;
          font-size: 14px;
        }
      }

      .reminder-actions {
        display: flex;
        align-items: center;
        gap: 8px;
      }
    }
  }
}
</style> 