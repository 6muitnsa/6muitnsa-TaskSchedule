<template>
  <div class="batch-operations">
    <el-button-group>
      <el-button
        type="primary"
        :disabled="!selectedTasks.length"
        @click="showBatchDialog('complete')"
      >
        批量完成
      </el-button>
      <el-button
        type="danger"
        :disabled="!selectedTasks.length"
        @click="showBatchDialog('abandon')"
      >
        批量放弃
      </el-button>
      <el-button
        type="warning"
        :disabled="!selectedTasks.length"
        @click="showBatchDialog('tags')"
      >
        批量更新标签
      </el-button>
      <el-button
        type="info"
        :disabled="!selectedTasks.length"
        @click="showBatchDialog('location')"
      >
        批量更新位置
      </el-button>
      <el-button
        type="danger"
        :disabled="!selectedTasks.length"
        @click="showBatchDialog('delete')"
      >
        批量删除
      </el-button>
    </el-button-group>

    <!-- 批量操作对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="30%"
    >
      <div class="dialog-content">
        <p>已选择 {{ selectedTasks.length }} 个任务</p>
        
        <!-- 标签选择 -->
        <div v-if="currentOperation === 'tags'" class="operation-content">
          <el-select
            v-model="selectedTags"
            multiple
            placeholder="选择标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </div>

        <!-- 位置选择 -->
        <div v-if="currentOperation === 'location'" class="operation-content">
          <el-select
            v-model="selectedLocation"
            placeholder="选择位置"
            style="width: 100%"
          >
            <el-option
              v-for="location in availableLocations"
              :key="location"
              :label="location"
              :value="location"
            />
          </el-select>
        </div>

        <!-- 确认信息 -->
        <div v-if="['complete', 'abandon', 'delete'].includes(currentOperation)" class="operation-content">
          <p>确定要{{ operationText }}选中的任务吗？</p>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleBatchOperation">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { taskApi } from '../api'

const props = defineProps({
  selectedTasks: {
    type: Array,
    required: true
  },
  availableTags: {
    type: Array,
    required: true
  },
  availableLocations: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['operation-complete'])

// 对话框控制
const dialogVisible = ref(false)
const currentOperation = ref('')
const selectedTags = ref([])
const selectedLocation = ref('')

// 计算属性
const dialogTitle = computed(() => {
  const titles = {
    complete: '批量完成任务',
    abandon: '批量放弃任务',
    tags: '批量更新标签',
    location: '批量更新位置',
    delete: '批量删除任务'
  }
  return titles[currentOperation.value] || ''
})

const operationText = computed(() => {
  const texts = {
    complete: '完成',
    abandon: '放弃',
    delete: '删除'
  }
  return texts[currentOperation.value] || ''
})

// 方法
const showBatchDialog = (operation) => {
  currentOperation.value = operation
  dialogVisible.value = true
}

const handleBatchOperation = async () => {
  try {
    const taskIds = props.selectedTasks.map(task => task.id)
    let response

    switch (currentOperation.value) {
      case 'complete':
        response = await taskApi.batchComplete(taskIds)
        break
      case 'abandon':
        response = await taskApi.batchAbandon(taskIds)
        break
      case 'tags':
        response = await taskApi.batchUpdateTags(taskIds, selectedTags.value)
        break
      case 'location':
        response = await taskApi.batchUpdateLocation(taskIds, selectedLocation.value)
        break
      case 'delete':
        response = await taskApi.batchDelete(taskIds)
        break
    }

    if (response.data.success) {
      ElMessage.success('批量操作成功')
      emit('operation-complete')
    } else {
      ElMessage.error('批量操作失败')
    }
  } catch (error) {
    console.error('批量操作失败:', error)
    ElMessage.error('批量操作失败')
  } finally {
    dialogVisible.value = false
  }
}
</script>

<style lang="scss" scoped>
.batch-operations {
  margin-bottom: 20px;
}

.dialog-content {
  .operation-content {
    margin-top: 20px;
  }
}
</style> 