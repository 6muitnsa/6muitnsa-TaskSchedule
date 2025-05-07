<template>
  <div class="task-management-container">
    <h1>任务管理</h1>

    <!-- 批量操作 -->
    <el-card class="batch-actions">
      <template #header>
        <div class="card-header">
          <span>批量操作</span>
          <el-button-group>
            <el-button type="danger" :disabled="!selectedTasks.length" @click="handleBatchDelete">批量删除</el-button>
            <el-button type="primary" :disabled="!selectedTasks.length" @click="handleBatchComplete">批量完成</el-button>
          </el-button-group>
        </div>
      </template>
      <div class="batch-content">
        <el-table
          :data="tasks"
          style="width: 100%"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="title" label="任务名称" min-width="200">
            <template #default="{ row }">
              <div class="task-name">
                <span>{{ row.title }}</span>
                <el-tag
                  v-for="tag in row.tags"
                  :key="tag"
                  size="small"
                  class="task-tag"
                >
                  {{ tag }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="priority" label="优先级" width="100">
            <template #default="{ row }">
              <el-tag :type="getPriorityType(row.priority)">{{ row.priority }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 标签管理 -->
    <el-card class="tag-management">
      <template #header>
        <div class="card-header">
          <span>标签管理</span>
          <el-button type="primary" @click="handleAddTag">添加标签</el-button>
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
    <el-card class="location-management">
      <template #header>
        <div class="card-header">
          <span>地点管理</span>
          <el-button type="primary" @click="handleAddLocation">添加地点</el-button>
        </div>
      </template>
      <el-table :data="locations" style="width: 100%">
        <el-table-column prop="name" label="地点名称" />
        <el-table-column prop="commute_time" label="通勤时间">
          <template #default="{ row }">
            {{ row.commute_time }} 分钟
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="handleEditLocation(row)">编辑</el-button>
              <el-button 
                size="small" 
                type="danger" 
                @click="handleDeleteLocation(row)"
              >删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 标签添加对话框 -->
    <el-dialog
      v-model="tagDialogVisible"
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
          <el-button @click="tagDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitNewTag">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 地点添加/编辑对话框 -->
    <el-dialog
      v-model="locationDialogVisible"
      :title="isEditingLocation ? '编辑地点' : '添加地点'"
      width="30%"
    >
      <el-form :model="locationForm" label-width="80px">
        <el-form-item label="地点名称">
          <el-input v-model="locationForm.name" />
        </el-form-item>
        <el-form-item label="通勤时间">
          <el-input-number 
            v-model="locationForm.commute_time" 
            :min="1" 
            :max="120"
          >
            <template #append>分钟</template>
          </el-input-number>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="locationDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitLocation">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { api } from '@/api'

// 状态
const tags = ref([])
const locations = ref([])
const tasks = ref([])
const selectedTasks = ref([])
const tagDialogVisible = ref(false)
const locationDialogVisible = ref(false)
const isEditingLocation = ref(false)
const newTag = ref({ name: '' })
const locationForm = ref({
  name: '',
  commute_time: 30
})

// 获取数据
const fetchData = async () => {
  try {
    // 获取标签
    const tagsResponse = await api.get('/tags')
    tags.value = tagsResponse.data

    // 获取地点
    const locationsResponse = await api.get('/locations')
    locations.value = locationsResponse.data

    // 获取任务列表
    const tasksResponse = await api.get('/tasks')
    tasks.value = tasksResponse.data
  } catch (error) {
    ElMessage.error('获取数据失败')
    console.error(error)
  }
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    'not_started': 'info',
    'in_progress': 'warning',
    'completed': 'success',
    'abandoned': 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    'not_started': '未开始',
    'in_progress': '进行中',
    'completed': '已完成',
    'abandoned': '已放弃'
  }
  return texts[status] || status
}

// 获取优先级类型
const getPriorityType = (priority) => {
  const types = {
    'high': 'danger',
    'medium': 'warning',
    'low': 'success'
  }
  return types[priority] || 'info'
}

// 处理选择变化
const handleSelectionChange = (selection) => {
  selectedTasks.value = selection
}

// 标签相关方法
const handleAddTag = () => {
  newTag.value = { name: '' }
  tagDialogVisible.value = true
}

const submitNewTag = async () => {
  try {
    await api.post('/tags', newTag.value)
    ElMessage.success('添加标签成功')
    tagDialogVisible.value = false
    await fetchData()
  } catch (error) {
    ElMessage.error('添加标签失败')
    console.error(error)
  }
}

const handleDeleteTag = async (tag) => {
  try {
    await ElMessageBox.confirm('确定要删除这个标签吗？', '警告', {
      type: 'warning'
    })
    await api.delete(`/tags/${tag}`)
    ElMessage.success('删除标签成功')
    await fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除标签失败')
      console.error(error)
    }
  }
}

// 地点相关方法
const handleAddLocation = () => {
  isEditingLocation.value = false
  locationForm.value = {
    name: '',
    commute_time: 30
  }
  locationDialogVisible.value = true
}

const handleEditLocation = (location) => {
  isEditingLocation.value = true
  locationForm.value = { ...location }
  locationDialogVisible.value = true
}

const submitLocation = async () => {
  try {
    if (isEditingLocation.value) {
      await api.put(`/locations/${locationForm.value.id}`, locationForm.value)
      ElMessage.success('更新地点成功')
    } else {
      await api.post('/locations', locationForm.value)
      ElMessage.success('添加地点成功')
    }
    locationDialogVisible.value = false
    await fetchData()
  } catch (error) {
    ElMessage.error(isEditingLocation.value ? '更新地点失败' : '添加地点失败')
    console.error(error)
  }
}

const handleDeleteLocation = async (location) => {
  try {
    await ElMessageBox.confirm('确定要删除这个地点吗？', '警告', {
      type: 'warning'
    })
    await api.delete(`/locations/${location.id}`)
    ElMessage.success('删除地点成功')
    await fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除地点失败')
      console.error(error)
    }
  }
}

// 批量操作方法
const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm('确定要删除选中的任务吗？', '警告', {
      type: 'warning'
    })
    const taskIds = selectedTasks.value.map(task => task.id)
    await api.post('/tasks/batch-delete', { task_ids: taskIds })
    ElMessage.success('批量删除成功')
    await fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
      console.error(error)
    }
  }
}

const handleBatchComplete = async () => {
  try {
    const taskIds = selectedTasks.value.map(task => task.id)
    await api.post('/tasks/batch-complete', { task_ids: taskIds })
    ElMessage.success('批量完成成功')
    await fetchData()
  } catch (error) {
    ElMessage.error('批量完成失败')
    console.error(error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.task-management-container {
  padding: 20px;
}

.task-management-container h1 {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-actions {
  margin-bottom: 20px;
}

.tag-management {
  margin-bottom: 20px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-item {
  margin-right: 10px;
  margin-bottom: 10px;
}

.location-management {
  margin-bottom: 20px;
}

.batch-content {
  margin-top: 20px;
}

.task-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.task-tag {
  margin-left: 4px;
}
</style> 