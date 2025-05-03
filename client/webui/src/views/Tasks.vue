<template>
  <div class="tasks">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>任务列表</span>
              <el-button type="primary" @click="showCreateDialog">新建任务</el-button>
            </div>
          </template>
          <el-table :data="tasks" style="width: 100%">
            <el-table-column prop="title" label="任务名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="priority" label="优先级" width="100">
              <template #default="scope">
                <el-tag :type="getPriorityType(scope.row.priority)">
                  {{ scope.row.priority }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="due_date" label="截止日期" width="150">
              <template #default="scope">
                {{ formatDate(scope.row.due_date) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="scope">
                <el-button size="small" @click="editTask(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteTask(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 创建/编辑任务对话框 -->
    <el-dialog
      :title="dialogTitle"
      v-model="dialogVisible"
      width="50%"
    >
      <el-form :model="taskForm" label-width="100px">
        <el-form-item label="任务名称">
          <el-input v-model="taskForm.title" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="taskForm.description" type="textarea" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-slider v-model="taskForm.priority" :min="0" :max="10" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="taskForm.status">
            <el-option label="待办" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item label="截止日期">
          <el-date-picker
            v-model="taskForm.due_date"
            type="datetime"
            placeholder="选择截止日期"
          />
        </el-form-item>
        <el-form-item label="标签">
          <el-select
            v-model="taskForm.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="请选择标签"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveTask">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import dayjs from 'dayjs'

export default {
  name: 'Tasks',
  setup() {
    const store = useStore()
    const dialogVisible = ref(false)
    const dialogTitle = ref('新建任务')
    const taskForm = ref({
      title: '',
      description: '',
      priority: 0,
      status: 'pending',
      due_date: null,
      tags: []
    })
    const editingTaskId = ref(null)

    const tasks = computed(() => store.state.tasks)
    const availableTags = computed(() => {
      const tags = new Set()
      store.state.tasks.forEach(task => {
        task.tags.forEach(tag => tags.add(tag))
      })
      return Array.from(tags)
    })

    const getPriorityType = (priority) => {
      if (priority > 7) return 'danger'
      if (priority > 4) return 'warning'
      return 'info'
    }

    const getStatusType = (status) => {
      switch (status) {
        case 'completed': return 'success'
        case 'in_progress': return 'warning'
        default: return 'info'
      }
    }

    const formatDate = (date) => {
      return date ? dayjs(date).format('YYYY-MM-DD HH:mm') : ''
    }

    const showCreateDialog = () => {
      dialogTitle.value = '新建任务'
      taskForm.value = {
        title: '',
        description: '',
        priority: 0,
        status: 'pending',
        due_date: null,
        tags: []
      }
      editingTaskId.value = null
      dialogVisible.value = true
    }

    const editTask = (task) => {
      dialogTitle.value = '编辑任务'
      taskForm.value = { ...task }
      editingTaskId.value = task.task_id
      dialogVisible.value = true
    }

    const saveTask = async () => {
      if (editingTaskId.value) {
        await store.dispatch('updateTask', {
          taskId: editingTaskId.value,
          taskData: taskForm.value
        })
      } else {
        await store.dispatch('createTask', taskForm.value)
      }
      dialogVisible.value = false
    }

    const deleteTask = async (task) => {
      await store.dispatch('deleteTask', task.task_id)
    }

    onMounted(() => {
      store.dispatch('fetchTasks')
    })

    return {
      tasks,
      availableTags,
      dialogVisible,
      dialogTitle,
      taskForm,
      getPriorityType,
      getStatusType,
      formatDate,
      showCreateDialog,
      editTask,
      saveTask,
      deleteTask
    }
  }
}
</script>

<style lang="scss" scoped>
.tasks {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 