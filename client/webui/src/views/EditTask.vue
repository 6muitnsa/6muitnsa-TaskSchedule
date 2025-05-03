<template>
  <div class="edit-task">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>编辑任务</span>
        </div>
      </template>
      <el-form
        :model="taskForm"
        :rules="rules"
        ref="taskFormRef"
        label-width="100px"
      >
        <el-form-item label="任务名称" prop="title">
          <el-input v-model="taskForm.title" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            :rows="4"
          />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-slider
            v-model="taskForm.priority"
            :min="0"
            :max="10"
            :marks="priorityMarks"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="taskForm.status">
            <el-option label="待办" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item label="截止日期" prop="due_date">
          <el-date-picker
            v-model="taskForm.due_date"
            type="datetime"
            placeholder="选择截止日期"
          />
        </el-form-item>
        <el-form-item label="标签" prop="tags">
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
        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="cancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'EditTask',
  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const taskFormRef = ref(null)
    const taskId = route.params.id

    const taskForm = ref({
      title: '',
      description: '',
      priority: 0,
      status: 'pending',
      due_date: null,
      tags: []
    })

    const rules = {
      title: [
        { required: true, message: '请输入任务名称', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
      ],
      description: [
        { max: 500, message: '描述不能超过 500 个字符', trigger: 'blur' }
      ],
      priority: [
        { required: true, message: '请选择优先级', trigger: 'change' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ],
      due_date: [
        { required: true, message: '请选择截止日期', trigger: 'change' }
      ]
    }

    const priorityMarks = {
      0: '低',
      5: '中',
      10: '高'
    }

    const availableTags = computed(() => {
      const tags = new Set()
      store.state.tasks.forEach(task => {
        task.tags.forEach(tag => tags.add(tag))
      })
      return Array.from(tags)
    })

    const submitForm = async () => {
      if (!taskFormRef.value) return
      
      try {
        await taskFormRef.value.validate()
        await store.dispatch('updateTask', {
          taskId,
          taskData: taskForm.value
        })
        ElMessage.success('任务更新成功')
        router.push(`/tasks/${taskId}`)
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }

    const cancel = () => {
      router.push(`/tasks/${taskId}`)
    }

    onMounted(async () => {
      await store.dispatch('fetchTasks')
      const task = store.state.tasks.find(t => t.task_id === taskId)
      if (task) {
        taskForm.value = { ...task }
      } else {
        ElMessage.error('任务不存在')
        router.push('/tasks')
      }
    })

    return {
      taskForm,
      taskFormRef,
      rules,
      priorityMarks,
      availableTags,
      submitForm,
      cancel
    }
  }
}
</script>

<style lang="scss" scoped>
.edit-task {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style> 