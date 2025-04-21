<template>
  <div class="task-create">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>创建新任务</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="task-form"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入任务名称" />
        </el-form-item>

        <el-form-item label="任务描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入任务描述"
          />
        </el-form-item>

        <el-form-item label="优先级" prop="priority">
          <el-radio-group v-model="priorityMode" class="priority-mode">
            <el-radio label="fuzzy">模糊选择</el-radio>
            <el-radio label="compare">比较选择</el-radio>
            <el-radio label="exact">精确数值</el-radio>
          </el-radio-group>
          
          <!-- 模糊选择 -->
          <template v-if="priorityMode === 'fuzzy'">
            <el-select v-model="fuzzyPriority" class="priority-select">
              <el-option label="低" value="low" />
              <el-option label="中" value="medium" />
              <el-option label="高" value="high" />
            </el-select>
            <span class="tip">系统将根据创建顺序自动分配具体优先级</span>
          </template>
          
          <!-- 比较选择 -->
          <template v-if="priorityMode === 'compare'">
            <el-select v-model="compareTask" placeholder="选择参考任务" class="priority-select">
              <el-option v-for="task in existingTasks" :key="task.id" :label="task.name" :value="task.id" />
            </el-select>
            <el-radio-group v-model="compareType" class="compare-type">
              <el-radio label="higher">更高</el-radio>
              <el-radio label="lower">更低</el-radio>
            </el-radio-group>
            <span class="tip">系统将在参考任务优先级基础上加减step值</span>
          </template>
          
          <!-- 精确数值 -->
          <el-input-number v-if="priorityMode === 'exact'" v-model="exactPriority" :min="0" :max="3000" :step="60" class="priority-select" />
        </el-form-item>

        <el-form-item label="任务类型" prop="task_type">
          <el-select v-model="form.task_type" placeholder="请选择任务类型">
            <el-option label="工作" value="work" />
            <el-option label="学习" value="study" />
            <el-option label="生活" value="life" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>

        <el-form-item label="时间段" prop="time_slot">
          <el-radio-group v-model="form.time_slot">
            <el-radio label="fixed">固定时间（不可调度）</el-radio>
            <el-radio label="flexible">灵活时间（可调度）</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="form.start_time"
            type="datetime"
            placeholder="选择开始时间"
            :disabled="form.time_slot === 'flexible'"
          />
        </el-form-item>

        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="form.end_time"
            type="datetime"
            placeholder="选择结束时间"
            :disabled="form.time_slot === 'flexible'"
          />
        </el-form-item>

        <el-form-item label="预计时间(分钟)" prop="estimated_time">
          <el-input-number
            v-model="form.estimated_time"
            :min="0"
            :step="15"
          />
        </el-form-item>

        <el-form-item label="地点" prop="location">
          <el-input v-model="form.location" placeholder="请输入地点" />
        </el-form-item>

        <el-form-item label="通勤时间(分钟)" prop="commute_time">
          <el-input-number
            v-model="form.commute_time"
            :min="0"
            :step="5"
            :disabled="!form.location"
          />
          <span class="tip" v-if="!form.commute_time && form.location">
            系统将根据不同任务地点添加一定通勤时间
          </span>
        </el-form-item>

        <el-form-item label="是否周期性" prop="is_periodic">
          <el-switch v-model="form.is_periodic" />
        </el-form-item>

        <template v-if="form.is_periodic">
          <el-form-item label="周期类型" prop="period_type">
            <el-select v-model="form.period_type" placeholder="请选择周期类型">
              <el-option label="每天" value="daily" />
              <el-option label="每周" value="weekly" />
              <el-option label="每月" value="monthly" />
            </el-select>
          </el-form-item>

          <el-form-item label="周期值" prop="period_value">
            <el-input-number
              v-model="form.period_value"
              :min="1"
              :step="1"
            />
          </el-form-item>

          <el-form-item label="周期天数" prop="period_days" v-if="form.period_type === 'weekly'">
            <el-select
              v-model="form.period_days"
              multiple
              placeholder="请选择周期天数"
            >
              <el-option label="周一" value="1" />
              <el-option label="周二" value="2" />
              <el-option label="周三" value="3" />
              <el-option label="周四" value="4" />
              <el-option label="周五" value="5" />
              <el-option label="周六" value="6" />
              <el-option label="周日" value="7" />
            </el-select>
          </el-form-item>

          <el-form-item label="总次数" prop="total_count">
            <el-input-number
              v-model="form.total_count"
              :min="1"
              :step="1"
            />
          </el-form-item>
        </template>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">创建</el-button>
          <el-button @click="$router.push('/')">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { taskApi } from '../api/task'

const router = useRouter()
const formRef = ref(null)

// 优先级选择相关
const priorityMode = ref('fuzzy')
const fuzzyPriority = ref('medium')
const compareTask = ref(null)
const compareType = ref('higher')
const exactPriority = ref(1500)
const existingTasks = ref([])
const PRIORITY_STEP = 60 // 优先级步长

const form = reactive({
  name: '',
  description: '',
  priority: 1500,
  task_type: 'work',
  time_slot: 'flexible',
  start_time: '',
  end_time: '',
  estimated_time: 60,
  location: '',
  commute_time: 0,
  is_locked: false,
  is_periodic: false,
  period_type: 'weekly',
  period_value: 1,
  period_days: [],
  total_count: 1
})

const rules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入任务描述', trigger: 'blur' }
  ],
  priority: [
    { required: true, message: '请设置优先级', trigger: 'blur' }
  ],
  task_type: [
    { required: true, message: '请选择任务类型', trigger: 'change' }
  ],
  time_slot: [
    { required: true, message: '请选择时间段类型', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ]
}

// 获取现有任务列表
const fetchExistingTasks = async () => {
  try {
    const response = await taskApi.getTasks({ limit: 100 })
    existingTasks.value = response.data
  } catch (error) {
    console.error('Error fetching existing tasks:', error)
  }
}

// 计算最终优先级
const calculatePriority = () => {
  if (priorityMode.value === 'fuzzy') {
    const basePriorities = {
      low: 0,
      medium: 1500,
      high: 3000
    }
    const basePriority = basePriorities[fuzzyPriority.value]
    const existingTasksInRange = existingTasks.value.filter(
      t => Math.abs(t.priority - basePriority) < PRIORITY_STEP
    )
    return basePriority - (existingTasksInRange.length * PRIORITY_STEP)
  } else if (priorityMode.value === 'compare') {
    if (!compareTask.value) return 1500
    const referenceTask = existingTasks.value.find(t => t.id === compareTask.value)
    if (!referenceTask) return 1500
    return compareType.value === 'higher' 
      ? referenceTask.priority + PRIORITY_STEP 
      : referenceTask.priority - PRIORITY_STEP
  } else {
    return exactPriority.value
  }
}

// 计算通勤时间
const calculateCommuteTime = (prevLocation, currentLocation) => {
  if (!prevLocation || !currentLocation) return 5 // 默认5分钟
  return prevLocation !== currentLocation ? 30 : 5 // 地点不同30分钟，相同5分钟
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 如果未设置通勤时间但有地点，自动计算通勤时间
    if (!form.commute_time && form.location) {
      const lastTask = existingTasks.value[existingTasks.value.length - 1]
      form.commute_time = calculateCommuteTime(lastTask?.location, form.location)
    }

    const data = {
      ...form,
      priority: calculatePriority(),
      period_days: form.period_days.join(',')
    }
    await taskApi.createTask(data)
    ElMessage.success('创建成功')
    router.push('/')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('创建失败')
    }
  }
}

onMounted(() => {
  fetchExistingTasks()
})
</script>

<style scoped>
.task-create {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-form {
  max-width: 800px;
  margin: 0 auto;
}

.priority-mode {
  margin-bottom: 10px;
}

.priority-select {
  width: 200px;
  margin-right: 10px;
}

.compare-type {
  margin-left: 10px;
}

.tip {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}
</style> 