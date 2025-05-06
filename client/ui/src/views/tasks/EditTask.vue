<template>
  <div class="edit-task">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>{{ isEdit ? '编辑任务' : '创建任务' }}</h2>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="task-form"
      >
        <!-- 任务ID（自动生成） -->
        <el-form-item label="任务ID">
          <el-input v-model="form.id" disabled />
        </el-form-item>

        <!-- 任务名称（选填，为空时与任务ID一致） -->
        <el-form-item label="任务名称">
          <el-input v-model="form.name" placeholder="选填，为空时与任务ID一致" />
        </el-form-item>

        <!-- 任务描述（选填） -->
        <el-form-item label="任务描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="选填"
          />
        </el-form-item>

        <!-- 任务优先级（必填，三选一） -->
        <el-form-item label="任务优先级" prop="priority" required>
          <el-radio-group v-model="priorityType">
            <el-radio label="range">区间选择</el-radio>
            <el-radio label="relative">相对选择</el-radio>
            <el-radio label="number">数字填入</el-radio>
          </el-radio-group>

          <!-- 1. 区间选择 -->
          <div v-if="priorityType === 'range'" class="priority-range">
            <el-select v-model="form.priorityRange" placeholder="选择优先级区间">
              <el-option
                v-for="range in priorityRanges"
                :key="range.name"
                :label="range.name"
                :value="range.name"
              />
            </el-select>
          </div>

          <!-- 2. 相对选择 -->
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

          <!-- 3. 数字填入 -->
          <div v-if="priorityType === 'number'" class="priority-number">
            <el-input-number
              v-model="form.priorityNumber"
              :min="1"
              :max="priorityTotalSize"
              placeholder="输入优先级数字"
            />
          </div>
        </el-form-item>

        <!-- 任务tag（选填，支持多个任务tag） -->
        <el-form-item label="任务标签">
          <el-radio-group v-model="tagType" class="mb-2">
            <el-radio label="existing">选择已有tag</el-radio>
            <el-radio label="new">添加新的tag</el-radio>
          </el-radio-group>

          <div v-if="tagType === 'existing'">
            <el-select
              v-model="form.tags"
              multiple
              placeholder="选择已有标签"
            >
              <el-option
                v-for="tag in existingTags"
                :key="tag"
                :label="tag"
                :value="tag"
              />
            </el-select>
          </div>

          <div v-if="tagType === 'new'">
            <el-input
              v-model="newTag"
              placeholder="输入新标签"
              class="mb-2"
            >
              <template #append>
                <el-button @click="addNewTag">添加</el-button>
              </template>
            </el-input>
            <el-tag
              v-for="tag in form.tags"
              :key="tag"
              closable
              class="mr-2"
              @close="removeTag(tag)"
            >
              {{ tag }}
            </el-tag>
          </div>
        </el-form-item>

        <!-- 时间输入 -->
        <el-form-item label="时间设置">
          <el-form-item label="开始时间">
            <el-date-picker
              v-model="form.startTime"
              type="datetime"
              placeholder="选填，不填则为任务创建时的时间"
            />
          </el-form-item>

          <el-form-item label="结束时间">
            <el-date-picker
              v-model="form.endTime"
              type="datetime"
              placeholder="选填，不填则为无时限任务"
            />
          </el-form-item>

          <el-form-item label="预计完成时间">
            <el-input-number
              v-model="form.estimatedTime"
              :min="1"
              placeholder="选填，不填时为60分钟"
            />
            <span class="unit">分钟</span>
          </el-form-item>
        </el-form-item>

        <!-- 地点输入 -->
        <el-form-item label="地点">
          <el-radio-group v-model="locationType" class="mb-2">
            <el-radio label="single">选择已有地点</el-radio>
            <el-radio label="route">选择出发地和目的地</el-radio>
            <el-radio label="new">添加新的地点</el-radio>
          </el-radio-group>

          <!-- 选择已有地点 -->
          <div v-if="locationType === 'single'">
            <el-select v-model="form.location" placeholder="选择地点">
              <el-option
                v-for="loc in existingLocations"
                :key="loc"
                :label="loc"
                :value="loc"
              />
            </el-select>
          </div>

          <!-- 选择出发地和目的地 -->
          <div v-if="locationType === 'route'" class="route-selection">
            <el-select v-model="form.startLocation" placeholder="选择出发地">
              <el-option
                v-for="loc in existingLocations"
                :key="loc"
                :label="loc"
                :value="loc"
              />
            </el-select>
            <el-select v-model="form.endLocation" placeholder="选择目的地">
              <el-option
                v-for="loc in existingLocations"
                :key="loc"
                :label="loc"
                :value="loc"
              />
            </el-select>
          </div>

          <!-- 添加新的地点 -->
          <div v-if="locationType === 'new'">
            <el-input
              v-model="newLocation"
              placeholder="输入新地点"
            >
              <template #append>
                <el-button @click="addNewLocation">添加</el-button>
              </template>
            </el-input>
          </div>
        </el-form-item>

        <!-- 休息时间 -->
        <el-form-item label="休息时间">
          <el-input-number
            v-model="form.breakTime"
            :min="1"
            placeholder="休息时间"
          />
          <span class="unit">分钟</span>
        </el-form-item>

        <!-- 高级设定 -->
        <el-form-item>
          <el-switch
            v-model="showAdvanced"
            active-text="高级设定"
          />
        </el-form-item>

        <template v-if="showAdvanced">
          <!-- 周期设置 -->
          <el-form-item label="周期">
            <el-radio-group v-model="cycleType">
              <el-radio label="none">与起止时间一致</el-radio>
              <el-radio label="independent">独立周期</el-radio>
              <el-radio label="composite">复合周期</el-radio>
            </el-radio-group>

            <!-- 独立周期 -->
            <div v-if="cycleType === 'independent'" class="cycle-independent">
              <span>每</span>
              <el-input-number
                v-model="form.cycleValue"
                :min="1"
                controls-position="right"
              />
              <el-select v-model="form.cycleUnit">
                <el-option label="分钟" value="minute" />
                <el-option label="小时" value="hour" />
                <el-option label="天" value="day" />
                <el-option label="周" value="week" />
                <el-option label="月" value="month" />
              </el-select>
            </div>

            <!-- 复合周期 -->
            <div v-if="cycleType === 'composite'" class="cycle-composite">
              <el-checkbox-group v-model="form.weekDays">
                <el-checkbox label="1">周一</el-checkbox>
                <el-checkbox label="2">周二</el-checkbox>
                <el-checkbox label="3">周三</el-checkbox>
                <el-checkbox label="4">周四</el-checkbox>
                <el-checkbox label="5">周五</el-checkbox>
                <el-checkbox label="6">周六</el-checkbox>
                <el-checkbox label="0">周日</el-checkbox>
              </el-checkbox-group>
              <el-checkbox-group v-model="form.monthDays">
                <el-checkbox
                  v-for="day in 31"
                  :key="day"
                  :label="day"
                >
                  {{ day }}号
                </el-checkbox>
              </el-checkbox-group>
              <el-checkbox-group v-model="form.months">
                <el-checkbox
                  v-for="month in 12"
                  :key="month"
                  :label="month"
                >
                  {{ month }}月
                </el-checkbox>
              </el-checkbox-group>
            </div>
          </el-form-item>

          <!-- 任务时间段 -->
          <el-form-item label="任务时间段">
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
          <el-form-item label="完成次数">
            <el-radio-group v-model="form.completionType">
              <el-radio label="fixed">定次</el-radio>
              <el-radio label="unlimited">不定次</el-radio>
            </el-radio-group>

            <template v-if="form.completionType === 'fixed'">
              <el-input-number
                v-model="form.completionCount"
                :min="1"
                :default-value="1"
                controls-position="right"
              />
              <span>次</span>
            </template>
          </el-form-item>
        </template>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '创建任务' }}
          </el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useTaskStore, useSettingsStore } from '@/store'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()
const settingsStore = useSettingsStore()
const formRef = ref(null)

// 是否为编辑模式
const isEdit = computed(() => !!route.params.id)

// 表单数据
const form = reactive({
  id: '',
  name: '',
  description: '',
  priorityRange: '',
  priorityNumber: null,
  relativeTask: '',
  relativePosition: 'before',
  tags: [],
  startTime: '',
  endTime: '',
  estimatedTime: 60,
  location: '',
  startLocation: '',
  endLocation: '',
  breakTime: 5,
  cycleType: 'none',
  cycleValue: 1,
  cycleUnit: 'day',
  weekDays: [],
  monthDays: [],
  months: [],
  timeRange: [],
  completionType: 'fixed',
  completionCount: 1
})

// 控制显示
const priorityType = ref('range')
const tagType = ref('existing')
const locationType = ref('single')
const showAdvanced = ref(false)
const cycleType = ref('none')

// 新增标签和地点
const newTag = ref('')
const newLocation = ref('')

// 从设置中获取的数据
const priorityRanges = ref([])
const priorityTotalSize = ref(5000)

// 已有数据
const existingTags = ref([])
const existingLocations = ref([])
const existingTasks = ref([])

// 表单验证规则
const rules = {
  priority: [
    { required: true, message: '请设置任务优先级', trigger: 'change' }
  ],
  completionCount: [
    { required: true, message: '请设置完成次数', trigger: 'change' }
  ]
}

// 获取必要数据
const fetchData = async () => {
  try {
    // 获取设置
    const settings = await settingsStore.fetchSettings()
    priorityRanges.value = settings.priorityRanges
    priorityTotalSize.value = settings.priorityTotalSize

    // 获取已有标签
    const tags = await taskStore.fetchTags()
    existingTags.value = tags

    // 获取已有地点
    const locations = await taskStore.fetchLocations()
    existingLocations.value = locations

    // 获取任务列表（用于相对优先级）
    const tasks = await taskStore.fetchTasks()
    existingTasks.value = tasks

    // 如果是编辑模式，获取任务数据
    if (isEdit.value) {
      const taskData = await taskStore.fetchTask(route.params.id)
      if (taskData) {
        Object.assign(form, taskData)
        // 设置相关控制状态
        if (taskData.priorityNumber) {
          priorityType.value = 'number'
        } else if (taskData.relativeTask) {
          priorityType.value = 'relative'
        }
        
        if (taskData.startLocation || taskData.endLocation) {
          locationType.value = 'route'
        }
        
        if (taskData.cycleValue || taskData.weekDays?.length) {
          showAdvanced.value = true
          cycleType.value = taskData.cycleType
        }
      }
    }
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  }
}

// 添加新标签
const addNewTag = () => {
  if (newTag.value && !form.tags.includes(newTag.value)) {
    form.tags.push(newTag.value)
    newTag.value = ''
  }
}

// 移除标签
const removeTag = (tag) => {
  const index = form.tags.indexOf(tag)
  if (index > -1) {
    form.tags.splice(index, 1)
  }
}

// 添加新地点
const addNewLocation = () => {
  if (newLocation.value && !existingLocations.value.includes(newLocation.value)) {
    existingLocations.value.push(newLocation.value)
    form.location = newLocation.value
    newLocation.value = ''
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    // 处理优先级
    let priority
    if (priorityType.value === 'range') {
      priority = form.priorityRange
    } else if (priorityType.value === 'number') {
      priority = form.priorityNumber
    } else {
      priority = {
        taskId: form.relativeTask,
        position: form.relativePosition
      }
    }
    
    // 处理地点
    let location
    if (locationType.value === 'route') {
      location = {
        start: form.startLocation,
        end: form.endLocation
      }
    } else {
      location = form.location
    }
    
    const taskData = {
      ...form,
      priority,
      location
    }
    
    if (isEdit.value) {
      await taskStore.updateTask(route.params.id, taskData)
      ElMessage.success('任务更新成功')
    } else {
      await taskStore.createTask(taskData)
      ElMessage.success('任务创建成功')
    }
    
    router.push('/tasks')
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  }
}

// 取消
const handleCancel = () => {
  router.back()
}

onMounted(fetchData)
</script>

<style lang="scss" scoped>
.edit-task {
  max-width: 800px;
  margin: 0 auto;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h2 {
      margin: 0;
    }
  }
  
  .task-form {
    margin-top: 20px;
    
    .mb-2 {
      margin-bottom: 8px;
    }
    
    .mr-2 {
      margin-right: 8px;
    }
    
    .unit {
      margin-left: 5px;
      color: #606266;
    }
    
    .priority-range,
    .priority-relative,
    .priority-number,
    .route-selection,
    .cycle-independent,
    .cycle-composite {
      margin-top: 10px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    
    .cycle-composite {
      flex-direction: column;
      align-items: flex-start;
      
      .el-checkbox-group {
        margin-bottom: 10px;
      }
    }
  }
}
</style> 