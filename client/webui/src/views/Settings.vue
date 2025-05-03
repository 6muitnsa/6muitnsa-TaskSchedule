<template>
  <div class="settings">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>基本设置</span>
            </div>
          </template>
          <el-form
            :model="settingsForm"
            label-width="120px"
          >
            <el-form-item label="主题">
              <el-radio-group v-model="settingsForm.theme">
                <el-radio label="light">浅色</el-radio>
                <el-radio label="dark">深色</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="语言">
              <el-select v-model="settingsForm.language">
                <el-option label="简体中文" value="zh-CN" />
                <el-option label="English" value="en" />
              </el-select>
            </el-form-item>
            <el-form-item label="通知">
              <el-switch v-model="settingsForm.notifications" />
            </el-form-item>
            <el-form-item label="声音提醒">
              <el-switch v-model="settingsForm.soundAlerts" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>番茄钟设置</span>
            </div>
          </template>
          <el-form
            :model="settingsForm"
            label-width="120px"
          >
            <el-form-item label="专注时长">
              <el-input-number
                v-model="settingsForm.focusDuration"
                :min="5"
                :max="60"
                :step="5"
              />
              <span class="unit">分钟</span>
            </el-form-item>
            <el-form-item label="休息时长">
              <el-input-number
                v-model="settingsForm.restDuration"
                :min="1"
                :max="30"
                :step="1"
              />
              <span class="unit">分钟</span>
            </el-form-item>
            <el-form-item label="长休息时长">
              <el-input-number
                v-model="settingsForm.longRestDuration"
                :min="10"
                :max="60"
                :step="5"
              />
              <span class="unit">分钟</span>
            </el-form-item>
            <el-form-item label="长休息间隔">
              <el-input-number
                v-model="settingsForm.longRestInterval"
                :min="2"
                :max="10"
                :step="1"
              />
              <span class="unit">个番茄钟</span>
            </el-form-item>
            <el-form-item label="自动开始休息">
              <el-switch v-model="settingsForm.autoStartRest" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" class="mt-20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>同步设置</span>
            </div>
          </template>
          <el-form
            :model="settingsForm"
            label-width="120px"
          >
            <el-form-item label="自动同步">
              <el-switch v-model="settingsForm.autoSync" />
            </el-form-item>
            <el-form-item
              label="同步间隔"
              :disabled="!settingsForm.autoSync"
            >
              <el-input-number
                v-model="settingsForm.syncInterval"
                :min="5"
                :max="60"
                :step="5"
                :disabled="!settingsForm.autoSync"
              />
              <span class="unit">分钟</span>
            </el-form-item>
            <el-form-item label="同步历史">
              <el-switch v-model="settingsForm.syncHistory" />
            </el-form-item>
            <el-form-item label="同步统计">
              <el-switch v-model="settingsForm.syncStatistics" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>数据管理</span>
            </div>
          </template>
          <div class="data-management">
            <el-button type="primary" @click="exportData">
              导出数据
            </el-button>
            <el-button type="success" @click="importData">
              导入数据
            </el-button>
            <el-button type="danger" @click="clearData">
              清除数据
            </el-button>
          </div>
          <div class="storage-info">
            <h3>存储信息</h3>
            <div class="info-item">
              <span class="label">任务数量</span>
              <span class="value">{{ storageInfo.tasks }}</span>
            </div>
            <div class="info-item">
              <span class="label">番茄钟记录</span>
              <span class="value">{{ storageInfo.pomodoros }}</span>
            </div>
            <div class="info-item">
              <span class="label">日程安排</span>
              <span class="value">{{ storageInfo.schedules }}</span>
            </div>
            <div class="info-item">
              <span class="label">存储大小</span>
              <span class="value">{{ storageInfo.size }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Settings',
  setup() {
    const store = useStore()

    const settingsForm = ref({
      theme: 'light',
      language: 'zh-CN',
      notifications: true,
      soundAlerts: true,
      focusDuration: 25,
      restDuration: 5,
      longRestDuration: 15,
      longRestInterval: 4,
      autoStartRest: true,
      autoSync: true,
      syncInterval: 15,
      syncHistory: true,
      syncStatistics: true
    })

    const storageInfo = computed(() => {
      return {
        tasks: store.state.tasks.length,
        pomodoros: store.state.pomodoroHistory.length,
        schedules: store.state.schedules.length,
        size: '0.5 MB' // 这里应该计算实际存储大小
      }
    })

    const exportData = async () => {
      try {
        await store.dispatch('exportData')
        ElMessage.success('数据导出成功')
      } catch (error) {
        console.error('导出数据失败:', error)
        ElMessage.error('导出数据失败')
      }
    }

    const importData = async () => {
      try {
        await store.dispatch('importData')
        ElMessage.success('数据导入成功')
      } catch (error) {
        console.error('导入数据失败:', error)
        ElMessage.error('导入数据失败')
      }
    }

    const clearData = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要清除所有数据吗？此操作不可恢复！',
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        await store.dispatch('clearData')
        ElMessage.success('数据已清除')
      } catch (error) {
        if (error !== 'cancel') {
          console.error('清除数据失败:', error)
          ElMessage.error('清除数据失败')
        }
      }
    }

    onMounted(async () => {
      await store.dispatch('fetchSettings')
      const settings = store.state.settings
      if (settings) {
        settingsForm.value = { ...settings }
      }
    })

    return {
      settingsForm,
      storageInfo,
      exportData,
      importData,
      clearData
    }
  }
}
</script>

<style lang="scss" scoped>
.settings {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .mt-20 {
    margin-top: 20px;
  }

  .unit {
    margin-left: 10px;
    color: #666;
  }

  .data-management {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 30px;
  }

  .storage-info {
    h3 {
      margin: 0 0 20px;
      font-size: 16px;
    }

    .info-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;
      border-bottom: 1px solid #eee;

      &:last-child {
        border-bottom: none;
      }

      .label {
        color: #666;
      }

      .value {
        font-weight: bold;
      }
    }
  }
}
</style> 