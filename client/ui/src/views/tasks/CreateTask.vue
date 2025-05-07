<template>
  <div class="create-task container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>创建新任务</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="task-form"
      >
        <!-- 任务ID -->
        <el-form-item label="任务ID">
          <el-input v-model="form.id" disabled />
        </el-form-item>

        <!-- 任务名称 -->
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="form.name" placeholder="选填，为空时与任务ID一致" />
        </el-form-item>

        <!-- 任务描述 -->
        <el-form-item label="任务描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="选填"
          />
        </el-form-item>

        <!-- 任务优先级 -->
        <el-form-item label="任务优先级" prop="priority">
          <el-radio-group v-model="priorityType">
            <el-radio label="range">区间选择</el-radio>
            <el-radio label="relative">相对选择</el-radio>
            <el-radio label="number">数字填入</el-radio>
          </el-radio-group>

          <!-- 区间选择 -->
          <div v-if="priorityType === 'range'" class="priority-range">
            <el-select v-model="form.priorityRange" placeholder="选择优先级区间">
              <el-option
                v-for="range in priorityRanges"
                :key="range.value"
                :label="range.label"
                :value="range.value"
              />
            </el-select>
          </div>

          <!-- 相对选择 -->
          <div v-if="priorityType === 'relative'" class="priority-relative">
            <el-select v-model="form.relativeTask" placeholder="选择已有任务">
              <el-option
                v-for="task in existingTasks"
                :key="task.id"
                :label="task.name"
                :value="task.id"
              />
            </el-select>
            <el-radio-group v-model="form.relativePosition">
              <el-radio label="before">优先</el-radio>
              <el-radio label="after">落后</el-radio>
            </el-radio-group>
          </div>

          <!-- 数字填入 -->
          <div v-if="priorityType === 'number'" class="priority-number">
            <el-input-number
              v-model="form.priorityNumber"
              :min="1"
              :max="5000"
              placeholder="输入优先级数字"
            />
          </div>
        </el-form-item>

        <!-- 任务标签 -->
        <el-form-item label="任务标签" prop="tags">
          <el-radio-group v-model="tagType">
            <el-radio label="select">选择已有标签</el-radio>
            <el-radio label="create">添加新标签</el-radio>
          </el-radio-group>

          <div v-if="tagType === 'select'" class="tag-select">
            <el-select
              v-model="form.tags"
              multiple
              filterable
              placeholder="请选择标签"
            >
              <el-option
                v-for="tag in availableTags"
                :key="tag"
                :label="tag"
                :value="tag"
              />
            </el-select>
          </div>

          <div v-else class="tag-create">
            <el-input
              v-model="newTag"
              placeholder="输入新标签"
              @keyup.enter="addNewTag"
            >
              <template #append>
                <el-button @click="addNewTag">添加</el-button>
              </template>
            </el-input>
          </div>
        </el-form-item>

        <!-- 时间设置 -->
        <el-form-item label="开始时间" prop="startTime">
          <el-date-picker
            v-model="form.startTime"
            type="datetime"
            placeholder="选填，默认为当前时间"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm"
          />
        </el-form-item>

        <el-form-item label="结束时间" prop="endTime">
          <el-date-picker
            v-model="form.endTime"
            type="datetime"
            placeholder="选填，不填则为无时限任务"
            format="YYYY-MM-DD HH:mm"
            value-format="YYYY-MM-DD HH:mm"
          />
        </el-form-item>

        <el-form-item label="预计完成时间" prop="estimatedTime">
          <el-input-number
            v-model="form.estimatedTime"
            :min="1"
            :max="480"
            placeholder="选填，默认60分钟"
          >
            <template #append>分钟</template>
          </el-input-number>
        </el-form-item>

        <!-- 地点设置 -->
        <el-form-item label="地点" prop="location">
          <el-radio-group v-model="locationType">
            <el-radio label="select">选择已有地点</el-radio>
            <el-radio label="create">添加新地点</el-radio>
          </el-radio-group>

          <div v-if="locationType === 'select'" class="location-select">
            <el-select
              v-model="form.location"
              filterable
              placeholder="请选择地点"
            >
              <el-option
                v-for="location in availableLocations"
                :key="location"
                :label="location"
                :value="location"
              />
            </el-select>
          </div>

          <div v-else class="location-create">
            <el-input
              v-model="newLocation"
              placeholder="输入新地点"
              @keyup.enter="addNewLocation"
            >
              <template #append>
                <el-button @click="addNewLocation">添加</el-button>
              </template>
            </el-input>
          </div>
        </el-form-item>

        <!-- 休息时间 -->
        <el-form-item label="休息时间" prop="restTime">
          <el-input-number
            v-model="form.restTime"
            :min="1"
            :max="60"
            placeholder="长任务切片时的休息时间"
          >
            <template #append>分钟</template>
          </el-input-number>
        </el-form-item>

        <!-- 高级设定 -->
        <el-form-item label="高级设定">
          <el-switch v-model="showAdvanced" />
        </el-form-item>

        <template v-if="showAdvanced">
          <!-- 周期设置 -->
          <el-form-item label="周期" prop="cycle">
            <el-radio-group v-model="cycleType">
              <el-radio label="none">与起止时间一致</el-radio>
              <el-radio label="simple">独立周期</el-radio>
              <el-radio label="complex">复合周期</el-radio>
            </el-radio-group>

            <!-- 独立周期 -->
            <div v-if="cycleType === 'simple'" class="cycle-simple">
              <span>每</span>
              <el-input-number v-model="form.cycleNumber" :min="1" />
              <el-select v-model="form.cycleUnit">
                <el-option label="分钟" value="minute" />
                <el-option label="小时" value="hour" />
                <el-option label="天" value="day" />
                <el-option label="周" value="week" />
                <el-option label="月" value="month" />
              </el-select>
            </div>

            <!-- 复合周期 -->
            <div v-if="cycleType === 'complex'" class="cycle-complex">
              <el-select v-model="form.cycleComplexType">
                <el-option label="星期" value="weekday" />
                <el-option label="日期" value="date" />
                <el-option label="月份" value="month" />
              </el-select>
              <el-select
                v-model="form.cycleComplexValues"
                multiple
                placeholder="选择具体时间点"
              >
                <el-option
                  v-for="option in cycleComplexOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>
            </div>
          </el-form-item>

          <!-- 任务时间段 -->
          <el-form-item label="任务时间段" prop="timeRange">
            <el-time-picker
              v-model="form.timeRange"
              is-range
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              format="HH:mm"
            />
          </el-form-item>

          <!-- 完成次数 -->
          <el-form-item label="完成次数" prop="completionCount">
            <el-radio-group v-model="completionType">
              <el-radio label="fixed">定次</el-radio>
              <el-radio label="unlimited">不定次</el-radio>
            </el-radio-group>

            <div v-if="completionType === 'fixed'" class="completion-fixed">
              <el-input-number
                v-model="form.completionCount"
                :min="1"
                placeholder="输入完成次数"
              />
            </div>
          </el-form-item>
        </template>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">创建任务</el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { taskApi } from '@/api'

const router = useRouter()
const formRef = ref(null)

// 表单数据
const form = reactive({
  id: generateTaskId(),
  name: '',
  description: '',
  priorityRange: '',
  relativeTask: '',
  relativePosition: 'before',
  priorityNumber: 1,
  tags: [],
  startTime: '',
  endTime: '',
  estimatedTime: 60,
  location: '',
  restTime: 5,
  cycleNumber: 1,
  cycleUnit: 'day',
  cycleComplexType: 'weekday',
  cycleComplexValues: [],
  timeRange: [],
  completionCount: 1
})

// 视图控制
const priorityType = ref('range')
const tagType = ref('select')
const locationType = ref('select')
const showAdvanced = ref(false)
const cycleType = ref('none')
const completionType = ref('fixed')

// 新标签和地点
const newTag = ref('')
const newLocation = ref('')

// 可选的标签和地点
const availableTags = ref([])
const availableLocations = ref([])

// 优先级区间
const priorityRanges = [
  { label: '高优先级', value: 'high' },
  { label: '中优先级', value: 'medium' },
  { label: '低优先级', value: 'low' }
]

// 现有任务
const existingTasks = ref([])

// 复合周期选项
const cycleComplexOptions = computed(() => {
  switch (form.cycleComplexType) {
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

// 生成任务ID
function generateTaskId() {
  return 'TASK-' + Date.now().toString(36).toUpperCase()
}

// 添加新标签
function addNewTag() {
  if (newTag.value && !availableTags.value.includes(newTag.value)) {
    availableTags.value.push(newTag.value)
    form.tags.push(newTag.value)
    newTag.value = ''
  }
}

// 添加新地点
function addNewLocation() {
  if (newLocation.value && !availableLocations.value.includes(newLocation.value)) {
    availableLocations.value.push(newLocation.value)
    form.location = newLocation.value
    newLocation.value = ''
  }
}

// 获取标签和地点列表
const getTagsAndLocations = async () => {
  try {
    const response = await taskApi.getTagsAndLocations()
    availableTags.value = response.data.tags
    availableLocations.value = response.data.locations
  } catch (err) {
    console.error('获取标签和地点列表失败:', err)
    ElMessage.error('获取标签和地点列表失败')
  }
}

// 获取现有任务列表
const getExistingTasks = async () => {
  try {
    const response = await taskApi.getTasks()
    existingTasks.value = response.data
  } catch (err) {
    console.error('获取现有任务列表失败:', err)
    ElMessage.error('获取现有任务列表失败')
  }
}

// 初始化数据
onMounted(async () => {
  await Promise.all([
    getTagsAndLocations(),
    getExistingTasks()
  ])
})

// 表单验证规则
const rules = {
  name: [
    { max: 50, message: '长度不能超过50个字符', trigger: 'blur' }
  ],
  priorityRange: [
    { required: true, message: '请选择优先级区间', trigger: 'change' }
  ],
  relativeTask: [
    { required: true, message: '请选择参考任务', trigger: 'change' }
  ],
  priorityNumber: [
    { required: true, message: '请输入优先级数字', trigger: 'change' }
  ]
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 构建任务数据
    const taskData = {
      name: form.name || form.id,
      description: form.description,
      priority: form.priorityRange,
      tags: form.tags,
      startTime: form.startTime,
      endTime: form.endTime,
      timeInfo: {
        estimatedDuration: form.estimatedTime,
        commuteTime: 0,
        restTime: form.restTime
      },
      complexInfo: {
        period: {
          type: cycleType.value === 'none' ? null : cycleType.value,
          value: cycleType.value === 'simple' ? {
            number: form.cycleNumber,
            unit: form.cycleUnit
          } : cycleType.value === 'complex' ? {
            type: form.cycleComplexType,
            values: form.cycleComplexValues
          } : null
        },
        completionTimes: {
          type: completionType.value,
          value: completionType.value === 'fixed' ? form.completionCount : null
        },
        timeSlot: form.timeRange.length === 2 ? {
          start: form.timeRange[0],
          end: form.timeRange[1]
        } : null
      }
    }
    
    // 调用API创建任务
    await taskApi.createTask(taskData)
    
    ElMessage.success('任务创建成功')
    router.push('/tasks')
  } catch (error) {
    console.error('创建任务失败:', error)
    ElMessage.error('创建任务失败：' + (error.response?.data?.message || error.message))
  }
}

// 取消创建
const handleCancel = () => {
  router.back()
}
</script>

<style lang="scss" scoped>
.create-task {
  padding: var(--spacing-medium);
  max-width: 800px;
  margin: 0 auto;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h2 {
      margin: 0;
      color: var(--text-primary);
    }
  }
  
  .task-form {
    margin-top: var(--spacing-medium);

    .el-radio-group {
      margin-bottom: var(--spacing-small);
    }

    .priority-range,
    .priority-relative,
    .priority-number,
    .tag-select,
    .tag-create,
    .location-select,
    .location-create,
    .cycle-simple,
    .cycle-complex,
    .completion-fixed {
      margin-top: var(--spacing-small);
      display: flex;
      gap: var(--spacing-small);
      align-items: center;
    }

    .cycle-simple {
      span {
        color: var(--text-regular);
      }
    }

    .el-input-number {
      width: 180px;
    }
  }
}

// 响应式布局
@media (max-width: 768px) {
  .create-task {
    .task-form {
      .el-form-item {
        margin-bottom: var(--spacing-medium);
      }

      .priority-range,
      .priority-relative,
      .priority-number,
      .tag-select,
      .tag-create,
      .location-select,
      .location-create,
      .cycle-simple,
      .cycle-complex,
      .completion-fixed {
        flex-direction: column;
        align-items: stretch;

        .el-input-number,
        .el-select {
          width: 100%;
        }
      }
    }
  }
}
</style> 