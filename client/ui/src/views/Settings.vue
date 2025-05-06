<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">系统设置</div>
    </div>

    <div class="settings-content">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本设置" name="basic">
          <el-form
            ref="basicForm"
            :model="basicSettings"
            label-width="120px"
            class="settings-form"
          >
            <el-form-item label="默认优先级">
              <el-select v-model="basicSettings.defaultPriority">
                <el-option label="低" value="low" />
                <el-option label="中" value="medium" />
                <el-option label="高" value="high" />
              </el-select>
            </el-form-item>
            <el-form-item label="默认任务时长">
              <el-input-number
                v-model="basicSettings.defaultDuration"
                :min="15"
                :max="480"
                :step="15"
              />
              <span class="unit">分钟</span>
            </el-form-item>
            <el-form-item label="休息时间">
              <el-input-number
                v-model="basicSettings.breakTime"
                :min="5"
                :max="60"
                :step="5"
              />
              <span class="unit">分钟</span>
            </el-form-item>
            <el-form-item label="工作时间">
              <el-time-picker
                v-model="basicSettings.workStartTime"
                format="HH:mm"
                placeholder="开始时间"
              />
              <span class="separator">至</span>
              <el-time-picker
                v-model="basicSettings.workEndTime"
                format="HH:mm"
                placeholder="结束时间"
              />
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="调度设置" name="schedule">
          <el-form
            ref="scheduleForm"
            :model="scheduleSettings"
            label-width="120px"
            class="settings-form"
          >
            <el-form-item label="默认调度算法">
              <el-select v-model="scheduleSettings.defaultAlgorithm">
                <el-option label="先来先服务" value="FCFS" />
                <el-option label="短作业优先" value="SJF" />
                <el-option label="优先级调度" value="Priority" />
                <el-option label="轮转调度" value="RR" />
              </el-select>
            </el-form-item>
            <el-form-item label="时间片长度">
              <el-input-number
                v-model="scheduleSettings.timeSlice"
                :min="15"
                :max="120"
                :step="15"
              />
              <span class="unit">分钟</span>
            </el-form-item>
            <el-form-item label="自动调度">
              <el-switch v-model="scheduleSettings.autoSchedule" />
            </el-form-item>
            <el-form-item label="调度间隔">
              <el-input-number
                v-model="scheduleSettings.scheduleInterval"
                :min="1"
                :max="24"
                :step="1"
              />
              <span class="unit">小时</span>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="通知设置" name="notification">
          <el-form
            ref="notificationForm"
            :model="notificationSettings"
            label-width="120px"
            class="settings-form"
          >
            <el-form-item label="任务提醒">
              <el-switch v-model="notificationSettings.taskReminder" />
            </el-form-item>
            <el-form-item label="提醒时间">
              <el-input-number
                v-model="notificationSettings.reminderTime"
                :min="5"
                :max="60"
                :step="5"
              />
              <span class="unit">分钟前</span>
            </el-form-item>
            <el-form-item label="声音提醒">
              <el-switch v-model="notificationSettings.soundReminder" />
            </el-form-item>
            <el-form-item label="桌面通知">
              <el-switch v-model="notificationSettings.desktopNotification" />
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="数据管理" name="data">
          <el-form
            ref="dataForm"
            :model="dataSettings"
            label-width="120px"
            class="settings-form"
          >
            <el-form-item label="数据备份">
              <el-button type="primary" @click="handleBackup">立即备份</el-button>
              <el-button @click="handleRestore">恢复数据</el-button>
            </el-form-item>
            <el-form-item label="自动备份">
              <el-switch v-model="dataSettings.autoBackup" />
            </el-form-item>
            <el-form-item label="备份频率">
              <el-select v-model="dataSettings.backupFrequency">
                <el-option label="每天" value="daily" />
                <el-option label="每周" value="weekly" />
                <el-option label="每月" value="monthly" />
              </el-select>
            </el-form-item>
            <el-form-item label="数据清理">
              <el-button type="danger" @click="handleClearData">清理历史数据</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>

      <div class="settings-footer">
        <el-button type="primary" @click="handleSave">保存设置</el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 当前激活的标签页
const activeTab = ref('basic')

// 基本设置
const basicSettings = ref({
  defaultPriority: 'medium',
  defaultDuration: 60,
  breakTime: 15,
  workStartTime: '09:00',
  workEndTime: '18:00'
})

// 调度设置
const scheduleSettings = ref({
  defaultAlgorithm: 'Priority',
  timeSlice: 30,
  autoSchedule: true,
  scheduleInterval: 4
})

// 通知设置
const notificationSettings = ref({
  taskReminder: true,
  reminderTime: 15,
  soundReminder: true,
  desktopNotification: true
})

// 数据设置
const dataSettings = ref({
  autoBackup: true,
  backupFrequency: 'daily'
})

// 保存设置
const handleSave = () => {
  // TODO: 调用API保存设置
  ElMessage.success('设置已保存')
}

// 重置设置
const handleReset = () => {
  ElMessageBox.confirm(
    '确定要重置所有设置吗？',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 重置所有设置
    ElMessage.success('设置已重置')
  })
}

// 备份数据
const handleBackup = () => {
  // TODO: 实现数据备份
  ElMessage.success('数据备份成功')
}

// 恢复数据
const handleRestore = () => {
  // TODO: 实现数据恢复
  ElMessage.success('数据恢复成功')
}

// 清理数据
const handleClearData = () => {
  ElMessageBox.confirm(
    '确定要清理历史数据吗？此操作不可恢复！',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 实现数据清理
    ElMessage.success('历史数据已清理')
  })
}
</script>

<style lang="scss" scoped>
.settings-content {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
  
  .settings-form {
    max-width: 600px;
    margin: 20px 0;
    
    .unit {
      margin-left: 8px;
      color: #909399;
    }
    
    .separator {
      margin: 0 8px;
      color: #909399;
    }
  }
  
  .settings-footer {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #dcdfe6;
    text-align: center;
  }
}
</style> 