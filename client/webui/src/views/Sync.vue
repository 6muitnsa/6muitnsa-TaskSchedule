<template>
  <div class="sync">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>同步状态</span>
            </div>
          </template>
          <div class="sync-status">
            <el-steps :active="syncStep" finish-status="success">
              <el-step title="准备" description="等待同步" />
              <el-step title="同步中" description="正在同步数据" />
              <el-step title="完成" description="同步完成" />
            </el-steps>
          </div>
          <div class="sync-controls">
            <el-button
              type="primary"
              :loading="isSyncing"
              :disabled="isSyncing"
              @click="startSync"
            >
              开始同步
            </el-button>
            <el-button
              type="danger"
              :disabled="!isSyncing"
              @click="stopSync"
            >
              停止同步
            </el-button>
            <el-button
              type="success"
              :disabled="isSyncing"
              @click="pullUpdates"
            >
              拉取更新
            </el-button>
          </div>
          <div class="sync-timeline">
            <h3>同步历史</h3>
            <el-timeline>
              <el-timeline-item
                v-for="record in syncHistory"
                :key="record.timestamp"
                :timestamp="formatDate(record.timestamp)"
                :type="getSyncType(record.status)"
              >
                {{ record.message }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>同步统计</span>
            </div>
          </template>
          <div class="sync-stats">
            <div class="stat-item">
              <span class="label">待同步任务</span>
              <span class="value">{{ pendingTasksCount }}</span>
            </div>
            <div class="stat-item">
              <span class="label">待同步番茄钟</span>
              <span class="value">{{ pendingPomodorosCount }}</span>
            </div>
            <div class="stat-item">
              <span class="label">上次同步时间</span>
              <span class="value">{{ lastSyncTime || '从未同步' }}</span>
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
import dayjs from 'dayjs'

export default {
  name: 'Sync',
  setup() {
    const store = useStore()
    const isSyncing = ref(false)
    const syncStep = ref(0)

    const syncHistory = computed(() => {
      return store.state.syncHistory.sort(
        (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
      )
    })

    const pendingTasksCount = computed(() => {
      return store.state.tasks.filter(t => t.status === 'pending').length
    })

    const pendingPomodorosCount = computed(() => {
      return store.state.pomodoroHistory.filter(p => !p.end_time).length
    })

    const lastSyncTime = computed(() => {
      const lastSync = syncHistory.value[0]
      return lastSync ? formatDate(lastSync.timestamp) : null
    })

    const startSync = async () => {
      isSyncing.value = true
      syncStep.value = 1
      try {
        await store.dispatch('startSync')
        syncStep.value = 2
        ElMessage.success('同步完成')
      } catch (error) {
        console.error('同步失败:', error)
        ElMessage.error('同步失败')
      } finally {
        isSyncing.value = false
        syncStep.value = 0
      }
    }

    const stopSync = async () => {
      try {
        await store.dispatch('stopSync')
        isSyncing.value = false
        syncStep.value = 0
        ElMessage.info('同步已停止')
      } catch (error) {
        console.error('停止同步失败:', error)
        ElMessage.error('停止同步失败')
      }
    }

    const pullUpdates = async () => {
      try {
        await store.dispatch('pullUpdates')
        ElMessage.success('更新已拉取')
      } catch (error) {
        console.error('拉取更新失败:', error)
        ElMessage.error('拉取更新失败')
      }
    }

    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
    }

    const getSyncType = (status) => {
      switch (status) {
        case 'success':
          return 'success'
        case 'error':
          return 'danger'
        default:
          return 'info'
      }
    }

    onMounted(async () => {
      await store.dispatch('fetchSyncHistory')
    })

    return {
      isSyncing,
      syncStep,
      syncHistory,
      pendingTasksCount,
      pendingPomodorosCount,
      lastSyncTime,
      startSync,
      stopSync,
      pullUpdates,
      formatDate,
      getSyncType
    }
  }
}
</script>

<style lang="scss" scoped>
.sync {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .sync-status {
    margin-bottom: 30px;
  }

  .sync-controls {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 30px;
  }

  .sync-timeline {
    h3 {
      margin: 0 0 20px;
      font-size: 16px;
    }
  }

  .sync-stats {
    .stat-item {
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