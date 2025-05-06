<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">创建任务</div>
    </div>

    <el-form
      ref="taskForm"
      :model="taskForm"
      :rules="rules"
      label-width="120px"
      class="task-form"
    >
      <el-form-item label="任务ID" prop="id">
        <el-input v-model="taskForm.id" disabled />
      </el-form-item>

      <el-form-item label="任务名称" prop="title">
        <el-input v-model="taskForm.title" placeholder="选填，为空时与任务ID一致" />
      </el-form-item>

      <el-form-item label="任务描述" prop="description">
        <el-input
          v-model="taskForm.description"
          type="textarea"
          rows="3"
          placeholder="选填"
        />
      </el-form-item>

      <el-form-item label="任务优先级" prop="priorityType">
        <el-radio-group v-model="taskForm.priorityType">
          <el-radio label="range">区间选择</el-radio>
          <el-radio label="relative">相对选择</el-radio>
          <el-radio label="number">数字填入</el-radio>
        </el-radio-group>

        <!-- 区间选择 -->
        <div v-if="taskForm.priorityType === 'range'" class="priority-range">
          <el-select v-model="taskForm.priorityRange" placeholder="选择优先级区间">
            <el-option
              v-for="range in priorityRanges"
              :key="range.name"
              :label="range.name"
              :value="range"
            />
          </el-select>
        </div>

        <!-- 相对选择 -->
        <div v-if="taskForm.priorityType === 'relative'" class="priority-relative">
          <el-select v-model="taskForm.relativeTask" placeholder="选择已有任务">
            <el-option
              v-for="task in existingTasks"
              :key="task.id"
              :label="task.title"
              :value="task"
            />
          </el-select>
          <el-radio-group v-model="taskForm.relativeType">
            <el-radio label="higher">优先</el-radio>
            <el-radio label="lower">落后</el-radio>
          </el-radio-group>
        </div>

        <!-- 数字填入 -->
        <div v-if="taskForm.priorityType === 'number'" class="priority-number">
          <el-input-number
            v-model="taskForm.priorityNumber"
            :min="0"
            :max="priorityTotal"
            :step="priorityStep"
          />
        </div>
      </el-form-item>

      <el-form-item label="任务标签" prop="tags">
        <el-select
          v-model="taskForm.tags"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="选择或创建标签"
        >
          <el-option
            v-for="tag in availableTags"
            :key="tag"
            :label="tag"
            :value="tag"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="时间设置">
        <el-checkbox v-model="taskForm.isUnlimited">无时间限制</el-checkbox>
      </el-form-item>

      <template v-if="!taskForm.isUnlimited">
        <el-form-item label="开始时间" prop="startTime">
          <el-date-picker
            v-model="taskForm.startTime"
            type="datetime"
            placeholder="选填，不填则为任务创建时的时间"
          />
        </el-form-item>

        <el-form-item label="结束时间" prop="endTime">
          <el-date-picker
            v-model="taskForm.endTime"
            type="datetime"
            placeholder="选填，不填则为无时限任务"
          />
        </el-form-item>
      </template>

      <template v-else>
        <el-form-item label="完成次数" prop="requiredCount">
          <el-input-number
            v-model="taskForm.requiredCount"
            :min="1"
            :max="1000"
          />
        </el-form-item>
      </template>

      <el-form-item label="预计完成时间" prop="estimatedDuration">
        <el-input-number
          v-model="taskForm.estimatedDuration"
          :min="1"
          :max="480"
          :step="5"
        />
        <span class="unit">分钟</span>
      </el-form-item>

      <el-form-item label="地点" prop="location">
        <el-radio-group v-model="taskForm.locationType">
          <el-radio label="existing">选择已有地点</el-radio>
          <el-radio label="new">添加新地点</el-radio>
        </el-radio-group>

        <template v-if="taskForm.locationType === 'existing'">
          <div class="location-select">
            <el-select v-model="taskForm.startLocation" placeholder="出发地">
              <el-option
                v-for="location in availableLocations"
                :key="location"
                :label="location"
                :value="location"
              />
            </el-select>
            <el-select v-model="taskForm.endLocation" placeholder="目的地">
              <el-option
                v-for="location in availableLocations"
                :key="location"
                :label="location"
                :value="location"
              />
            </el-select>
          </div>
        </template>

        <template v-else>
          <el-input v-model="taskForm.newLocation" placeholder="输入新地点" />
        </template>
      </el-form-item>

      <el-form-item label="休息时间" prop="breakTime">
        <el-input-number
          v-model="taskForm.breakTime"
          :min="0"
          :max="60"
          :step="5"
        />
        <span class="unit">分钟</span>
      </el-form-item>

      <el-form-item label="高级设定">
        <el-switch v-model="taskForm.showAdvanced" />
      </el-form-item>

      <template v-if="taskForm.showAdvanced">
        <el-form-item label="周期设置">
          <el-radio-group v-model="taskForm.cycleType">
            <el-radio label="none">与起止时间一致</el-radio>
            <el-radio label="interval">独立周期</el-radio>
            <el-radio label="composite">复合周期</el-radio>
          </el-radio-group>

          <!-- 独立周期 -->
          <div v-if="taskForm.cycleType === 'interval'" class="cycle-interval">
            <span>每</span>
            <el-input-number v-model="taskForm.cycleInterval" :min="1" />
            <el-select v-model="taskForm.cycleUnit">
              <el-option label="分钟" value="minute" />
              <el-option label="小时" value="hour" />
              <el-option label="天" value="day" />
              <el-option label="周" value="week" />
              <el-option label="月" value="month" />
            </el-select>
          </div>

          <!-- 复合周期 -->
          <div v-if="taskForm.cycleType === 'composite'" class="cycle-composite">
            <el-select v-model="taskForm.compositeType">
              <el-option label="星期" value="weekday" />
              <el-option label="日期" value="date" />
              <el-option label="月份" value="month" />
            </el-select>
            <el-select
              v-model="taskForm.compositeValues"
              multiple
              :placeholder="getCompositePlaceholder"
            >
              <el-option
                v-for="option in compositeOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </div>
        </el-form-item>

        <el-form-item label="任务时间段">
          <el-time-picker
            v-model="taskForm.timeRange"
            is-range
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="HH:mm"
          />
        </el-form-item>

        <el-form-item label="次数设置">
          <el-radio-group v-model="taskForm.countType">
            <el-radio label="fixed">定次</el-radio>
            <el-radio label="unlimited">不定次</el-radio>
          </el-radio-group>

          <el-input-number
            v-if="taskForm.countType === 'fixed'"
            v-model="taskForm.fixedCount"
            :min="1"
            :max="1000"
          />
        </el-form-item>
      </template>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">创建任务</el-button>
        <el-button @click="handleCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()

// 表单数据
const taskForm = ref({
  id: generateTaskId(),
  title: '',
  description: '',
  priorityType: 'range',
  priorityRange: null,
  relativeTask: null,
  relativeType: 'higher',
  priorityNumber: 0,
  tags: [],
  isUnlimited: false,
  startTime: null,
  endTime: null,
  requiredCount: 1,
  estimatedDuration: 60,
  locationType: 'existing',
  startLocation: '',
  endLocation: '',
  newLocation: '',
  breakTime: 5,
  showAdvanced: false,
  cycleType: 'none',
  cycleInterval: 1,
  cycleUnit: 'day',
  compositeType: 'weekday',
  compositeValues: [],
  timeRange: null,
  countType: 'fixed',
  fixedCount: 1
})

// 表单验证规则
const rules = {
  title: [
    { max: 100, message: '任务名称不能超过100个字符', trigger: 'blur' }
  ],
  description: [
    { max: 500, message: '任务描述不能超过500个字符', trigger: 'blur' }
  ],
  priorityType: [
    { required: true, message: '请选择优先级类型', trigger: 'change' }
  ],
  priorityRange: [
    { required: true, message: '请选择优先级区间', trigger: 'change' }
  ],
  relativeTask: [
    { required: true, message: '请选择参考任务', trigger: 'change' }
  ],
  priorityNumber: [
    { required: true, message: '请输入优先级数值', trigger: 'blur' }
  ],
  tags: [
    { type: 'array', max: 5, message: '最多选择5个标签', trigger: 'change' }
  ],
  startTime: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  endTime: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  requiredCount: [
    { required: true, message: '请输入完成次数', trigger: 'blur' }
  ],
  estimatedDuration: [
    { required: true, message: '请输入预计完成时间', trigger: 'blur' }
  ],
  locationType: [
    { required: true, message: '请选择地点类型', trigger: 'change' }
  ],
  startLocation: [
    { required: true, message: '请选择出发地', trigger: 'change' }
  ],
  endLocation: [
    { required: true, message: '请选择目的地', trigger: 'change' }
  ],
  newLocation: [
    { required: true, message: '请输入新地点', trigger: 'blur' }
  ]
}

// 优先级设置
const priorityRanges = ref([])
const priorityTotal = ref(5000)
const priorityStep = ref(50)
const existingTasks = ref([])

// 标签和地点
const availableTags = ref([])
const availableLocations = ref([])

// 复合周期选项
const compositeOptions = computed(() => {
  switch (taskForm.value.compositeType) {
    case 'weekday':
      return [
        { label: '周一', value: 1 },
        { label: '周二', value: 2 },
        { label: '周三', value: 3 },
        { label: '周四', value: 4 },
        { label: '周五', value: 5 },
        { label: '周六', value: 6 },
        { label: '周日', value: 7 }
      ]
    case 'date':
      return Array.from({ length: 31 }, (_, i) => ({
        label: `${i + 1}号`,
        value: i + 1
      }))
    case 'month':
      return Array.from({ length: 12 }, (_, i) => ({
        label: `${i + 1}月`,
        value: i + 1
      }))
    default:
      return []
  }
})

// 获取复合周期占位符
const getCompositePlaceholder = computed(() => {
  switch (taskForm.value.compositeType) {
    case 'weekday':
      return '选择星期'
    case 'date':
      return '选择日期'
    case 'month':
      return '选择月份'
    default:
      return '请选择'
  }
})

// 生成任务ID
function generateTaskId() {
  return 'TASK' + Date.now().toString(36).toUpperCase()
}

// 加载数据
const loadData = async () => {
  try {
    const [settingsRes, tasksRes, tagsRes, locationsRes] = await Promise.all([
      axios.get('/api/settings'),
      axios.get('/api/tasks'),
      axios.get('/api/tags'),
      axios.get('/api/locations')
    ])

    priorityRanges.value = settingsRes.data.priorityRanges
    priorityTotal.value = settingsRes.data.priorityTotal
    priorityStep.value = settingsRes.data.priorityStep
    existingTasks.value = tasksRes.data.tasks
    availableTags.value = tagsRes.data.tags
    availableLocations.value = locationsRes.data.locations
  } catch (error) {
    ElMessage.error('加载数据失败：' + error.message)
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    const formData = {
      ...taskForm.value,
      priority: calculatePriority()
    }
    await axios.post('/api/tasks', formData)
    ElMessage.success('任务创建成功')
    router.push('/tasks')
  } catch (error) {
    ElMessage.error('创建任务失败：' + error.message)
  }
}

// 计算优先级
const calculatePriority = () => {
  switch (taskForm.value.priorityType) {
    case 'range':
      return taskForm.value.priorityRange.min
    case 'relative':
      const basePriority = taskForm.value.relativeTask.priority
      return taskForm.value.relativeType === 'higher'
        ? basePriority + priorityStep.value
        : basePriority - priorityStep.value
    case 'number':
      return taskForm.value.priorityNumber
    default:
      return 0
  }
}

// 取消创建
const handleCancel = () => {
  router.back()
}

// 初始化
onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.page-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.task-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
}

.priority-range,
.priority-relative,
.priority-number,
.cycle-interval,
.cycle-composite,
.location-select {
  margin-top: 10px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.unit {
  margin-left: 8px;
  color: #909399;
}
</style> 