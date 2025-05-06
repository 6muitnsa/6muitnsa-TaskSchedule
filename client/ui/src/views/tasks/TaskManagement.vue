<template>
  <div class="task-management container">
    <el-card class="management-card">
      <template #header>
        <div class="card-header">
          <h2>任务管理</h2>
        </div>
      </template>

      <!-- 批量操作 -->
      <div class="batch-actions">
        <el-button type="danger" @click="handleBatchDelete" :disabled="!selectedTasks.length">
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
        <el-button type="primary" @click="handleBatchEdit" :disabled="!selectedTasks.length">
          <el-icon><Edit /></el-icon>
          批量编辑
        </el-button>
      </div>

      <!-- 任务列表 -->
      <el-table
        v-loading="loading"
        :data="tasks"
        @selection-change="handleSelectionChange"
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="任务名称" />
        <el-table-column prop="tags" label="标签">
          <template #default="{ row }">
            <el-tag
              v-for="tag in row.tags"
              :key="tag"
              class="mx-1"
              size="small"
            >
              {{ tag }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="地点" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="handleEdit(row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="handleDelete(row)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 标签管理 -->
    <el-card class="management-card">
      <template #header>
        <div class="card-header">
          <h3>标签管理</h3>
          <el-button type="primary" @click="showTagDialog = true">
            <el-icon><Plus /></el-icon>
            添加标签
          </el-button>
        </div>
      </template>

      <div class="tag-list">
        <el-tag
          v-for="tag in tags"
          :key="tag"
          closable
          @close="handleDeleteTag(tag)"
          class="tag-item"
        >
          {{ tag }}
        </el-tag>
      </div>
    </el-card>

    <!-- 地点管理 -->
    <el-card class="management-card">
      <template #header>
        <div class="card-header">
          <h3>地点管理</h3>
          <el-button type="primary" @click="showLocationDialog = true">
            <el-icon><Plus /></el-icon>
            添加地点
          </el-button>
        </div>
      </template>

      <div class="location-list">
        <el-tag
          v-for="location in locations"
          :key="location"
          closable
          @close="handleDeleteLocation(location)"
          class="location-item"
        >
          {{ location }}
        </el-tag>
      </div>
    </el-card>

    <!-- 数据同步 -->
    <el-card class="management-card">
      <template #header>
        <div class="card-header">
          <h3>数据同步</h3>
        </div>
      </template>

      <div class="sync-info">
        <div class="sync-status">
          <span>同步状态：</span>
          <el-tag :type="syncStatus.type">{{ syncStatus.text }}</el-tag>
          <el-button 
            :type="syncStatus.isRunning ? 'danger' : 'primary'"
            @click="toggleSync"
            :loading="syncLoading"
          >
            {{ syncStatus.isRunning ? '停止同步' : '启动同步' }}
          </el-button>
        </div>
        <div class="sync-url" v-if="syncStatus.isRunning">
          <span>同步地址：</span>
          <el-input v-model="syncUrl" readonly>
            <template #append>
              <el-button @click="copySyncUrl">复制</el-button>
            </template>
          </el-input>
        </div>
        <div class="sync-qrcode" v-if="syncStatus.isRunning">
          <span>同步二维码：</span>
          <div class="qrcode-container">
            <img :src="qrcodeUrl" alt="同步二维码" />
          </div>
        </div>
      </div>
    </el-card>

    <!-- 标签对话框 -->
    <el-dialog
      v-model="showTagDialog"
      title="添加标签"
      width="30%"
    >
      <el-form :model="newTag" label-width="80px">
        <el-form-item label="标签名称">
          <el-input v-model="newTag.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showTagDialog = false">取消</el-button>
          <el-button type="primary" @click="handleAddTag">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 地点对话框 -->
    <el-dialog
      v-model="showLocationDialog"
      title="添加地点"
      width="30%"
    >
      <el-form :model="newLocation" label-width="80px">
        <el-form-item label="地点名称">
          <el-input v-model="newLocation.name" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showLocationDialog = false">取消</el-button>
          <el-button type="primary" @click="handleAddLocation">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete, Edit, Plus } from '@element-plus/icons-vue'
import { syncApi } from '@/api'

// 状态
const loading = ref(false)
const tasks = ref([])
const selectedTasks = ref([])
const tags = ref([])
const locations = ref([])
const syncUrl = ref('')
const qrcodeUrl = ref('')
const syncLoading = ref(false)
const syncStatus = ref({
  isRunning: false,
  type: 'info',
  text: '未启动'
})

// 对话框状态
const showTagDialog = ref(false)
const showLocationDialog = ref(false)
const newTag = ref({ name: '' })
const newLocation = ref({ name: '' })

// 初始化数据
onMounted(() => {
  // 模拟数据
  tasks.value = [
    { id: 1, name: '完成项目文档', tags: ['工作', '文档'], location: '办公室' },
    { id: 2, name: '学习Vue3', tags: ['学习', '编程'], location: '家里' },
    { id: 3, name: '阅读技术书籍', tags: ['阅读', '学习'], location: '图书馆' }
  ]
  tags.value = ['工作', '学习', '阅读', '编程', '文档']
  locations.value = ['办公室', '家里', '图书馆']

  // 初始化时获取同步状态
  getSyncStatus()
})

// 选择变化
const handleSelectionChange = (selection) => {
  selectedTasks.value = selection
}

// 批量删除
const handleBatchDelete = () => {
  ElMessageBox.confirm(
    `确定要删除选中的 ${selectedTasks.value.length} 个任务吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 实现批量删除逻辑
    ElMessage.success('删除成功')
  })
}

// 批量编辑
const handleBatchEdit = () => {
  // TODO: 实现批量编辑逻辑
  ElMessage.info('批量编辑功能开发中')
}

// 编辑单个任务
const handleEdit = (task) => {
  // TODO: 实现编辑逻辑
  ElMessage.info(`编辑任务：${task.name}`)
}

// 删除单个任务
const handleDelete = (task) => {
  ElMessageBox.confirm(
    `确定要删除任务"${task.name}"吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // TODO: 实现删除逻辑
    ElMessage.success('删除成功')
  })
}

// 添加标签
const handleAddTag = () => {
  if (!newTag.value.name) {
    ElMessage.warning('请输入标签名称')
    return
  }
  tags.value.push(newTag.value.name)
  newTag.value.name = ''
  showTagDialog.value = false
  ElMessage.success('添加成功')
}

// 删除标签
const handleDeleteTag = (tag) => {
  ElMessageBox.confirm(
    `确定要删除标签"${tag}"吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    tags.value = tags.value.filter(t => t !== tag)
    ElMessage.success('删除成功')
  })
}

// 添加地点
const handleAddLocation = () => {
  if (!newLocation.value.name) {
    ElMessage.warning('请输入地点名称')
    return
  }
  locations.value.push(newLocation.value.name)
  newLocation.value.name = ''
  showLocationDialog.value = false
  ElMessage.success('添加成功')
}

// 删除地点
const handleDeleteLocation = (location) => {
  ElMessageBox.confirm(
    `确定要删除地点"${location}"吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    locations.value = locations.value.filter(l => l !== location)
    ElMessage.success('删除成功')
  })
}

// 启动/停止同步
const toggleSync = async () => {
  if (syncStatus.value.isRunning) {
    try {
      await syncApi.stopSync()
      syncStatus.value = {
        isRunning: false,
        type: 'info',
        text: '已停止'
      }
      syncUrl.value = ''
      qrcodeUrl.value = ''
      ElMessage.success('同步已停止')
    } catch (error) {
      ElMessage.error('停止同步失败：' + error.message)
    }
  } else {
    syncLoading.value = true
    try {
      const response = await syncApi.startSync()
      syncUrl.value = response.data.url
      qrcodeUrl.value = response.data.qrcode
      syncStatus.value = {
        isRunning: true,
        type: 'success',
        text: '运行中'
      }
      ElMessage.success('同步已启动')
    } catch (error) {
      ElMessage.error('启动同步失败：' + error.message)
    } finally {
      syncLoading.value = false
    }
  }
}

// 复制同步地址
const copySyncUrl = () => {
  navigator.clipboard.writeText(syncUrl.value).then(() => {
    ElMessage.success('复制成功')
  })
}

// 组件卸载时停止同步
onUnmounted(async () => {
  if (syncStatus.value.isRunning) {
    try {
      await syncApi.stopSync()
    } catch (error) {
      console.error('停止同步失败：', error)
    }
  }
})

// 获取同步状态
const getSyncStatus = async () => {
  try {
    const response = await syncApi.getSyncStatus()
    if (response.data.isRunning) {
      syncStatus.value = {
        isRunning: true,
        type: 'success',
        text: '运行中'
      }
      syncUrl.value = response.data.url
      qrcodeUrl.value = response.data.qrcode
    }
  } catch (error) {
    console.error('获取同步状态失败：', error)
  }
}
</script>

<style lang="scss" scoped>
.task-management {
  padding: var(--spacing-medium);

  .management-card {
    margin-bottom: var(--spacing-large);

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h2, h3 {
        margin: 0;
        color: var(--text-primary);
      }
    }
  }

  .batch-actions {
    margin-bottom: var(--spacing-medium);
    display: flex;
    gap: var(--spacing-medium);
  }

  .tag-list,
  .location-list {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-small);

    .tag-item,
    .location-item {
      margin-right: var(--spacing-small);
      margin-bottom: var(--spacing-small);
    }
  }

  .sync-info {
    .sync-status {
      margin-bottom: var(--spacing-medium);
    }

    .sync-url,
    .sync-qrcode {
      margin-bottom: var(--spacing-medium);
    }

    .qrcode-container {
      width: 200px;
      height: 200px;
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: var(--spacing-small);
    }
  }
}

// 响应式布局
@media (max-width: 768px) {
  .task-management {
    .batch-actions {
      flex-direction: column;

      .el-button {
        width: 100%;
      }
    }

    .sync-info {
      .sync-url {
        .el-input-group {
          display: flex;
          flex-direction: column;

          .el-input-group__append {
            margin-left: 0;
            margin-top: var(--spacing-small);
          }
        }
      }
    }
  }
}
</style> 