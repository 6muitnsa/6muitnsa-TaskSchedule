<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-width="120px"
  >
    <el-form-item label="任务名称" prop="name">
      <el-input v-model="form.name" />
    </el-form-item>

    <el-form-item label="任务描述" prop="description">
      <el-input
        v-model="form.description"
        type="textarea"
        :rows="3"
      />
    </el-form-item>

    <el-form-item label="优先级" prop="priority">
      <el-radio-group v-model="priorityType" class="priority-selector">
        <el-radio-button label="fuzzy">模糊选择</el-radio-button>
        <el-radio-button label="compare">比较选择</el-radio-button>
        <el-radio-button label="exact">精确数值</el-radio-button>
      </el-radio-group>

      <!-- 模糊选择 -->
      <div v-if="priorityType === 'fuzzy'" class="priority-options">
        <el-radio-group v-model="form.priority">
          <el-radio :label="1000">低</el-radio>
          <el-radio :label="2000">中</el-radio>
          <el-radio :label="3000">高</el-radio>
        </el-radio-group>
      </div>

      <!-- 比较选择 -->
      <div v-if="priorityType === 'compare'" class="priority-options">
        <el-select v-model="compareTask" placeholder="选择参考任务" class="compare-select">
          <el-option
            v-for="task in otherTasks"
            :key="task.id"
            :label="task.name"
            :value="task.id"
          />
        </el-select>
        <el-radio-group v-model="compareType" class="compare-type">
          <el-radio label="higher">更高优先级</el-radio>
          <el-radio label="lower">更低优先级</el-radio>
        </el-radio-group>
      </div>

      <!-- 精确数值 -->
      <div v-if="priorityType === 'exact'" class="priority-options">
        <el-input-number
          v-model="form.priority"
          :min="0"
          :max="3000"
          :step="1"
        />
      </div>
    </el-form-item>

    <el-form-item label="预计时间" prop="estimated_time">
      <el-input-number
        v-model="form.estimated_time"
        :min="15"
        :step="15"
      />
      <span class="unit">分钟</span>
    </el-form-item>

    <el-form-item label="周期类型" prop="period_type">
      <el-select v-model="form.period_type">
        <el-option label="一次性" value="once" />
        <el-option label="每日" value="daily" />
        <el-option label="每周" value="weekly" />
        <el-option label="每月" value="monthly" />
      </el-select>
    </el-form-item>

    <el-form-item label="完成次数" prop="times">
      <el-input-number
        v-model="form.times"
        :min="1"
        :disabled="form.period_type === 'once'"
      />
    </el-form-item>

    <el-form-item label="时间类型" prop="time_type">
      <el-radio-group v-model="form.time_type">
        <el-radio label="fixed">固定时间</el-radio>
        <el-radio label="flexible">灵活时间</el-radio>
      </el-radio-group>
    </el-form-item>

    <el-form-item
      v-if="form.time_type === 'fixed'"
      label="具体时间"
      prop="specific_time"
    >
      <el-time-picker
        v-model="form.specific_time"
        format="HH:mm"
      />
    </el-form-item>

    <el-form-item label="开始时间" prop="start_time">
      <el-date-picker
        v-model="form.start_time"
        type="datetime"
        placeholder="选择开始时间"
      />
    </el-form-item>

    <el-form-item label="结束时间" prop="end_time">
      <el-date-picker
        v-model="form.end_time"
        type="datetime"
        placeholder="选择结束时间"
      />
    </el-form-item>

    <el-form-item label="地点" prop="location_id">
      <el-select v-model="form.location_id">
        <el-option
          v-for="location in locations"
          :key="location.id"
          :label="location.name"
          :value="location.id"
        />
      </el-select>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submitForm">提交</el-button>
      <el-button @click="$emit('cancel')">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  task: {
    type: Object,
    default: () => null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const formRef = ref(null)
const locations = ref([])
const otherTasks = ref([])
const priorityType = ref('fuzzy')
const compareTask = ref(null)
const compareType = ref('higher')

const form = reactive({
  name: '',
  description: '',
  priority: 2000,
  estimated_time: 60,
  period_type: 'once',
  times: 1,
  time_type: 'flexible',
  specific_time: null,
  start_time: null,
  end_time: null,
  location_id: null
})

const rules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' }
  ],
  estimated_time: [
    { required: true, message: '请输入预计时间', trigger: 'blur' }
  ],
  period_type: [
    { required: true, message: '请选择周期类型', trigger: 'change' }
  ],
  times: [
    { required: true, message: '请输入完成次数', trigger: 'blur' }
  ],
  time_type: [
    { required: true, message: '请选择时间类型', trigger: 'change' }
  ],
  specific_time: [
    { required: true, message: '请选择具体时间', trigger: 'change' }
  ],
  start_time: [
    { required: true, message: '请选择开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择结束时间', trigger: 'change' }
  ],
  location_id: [
    { required: true, message: '请选择地点', trigger: 'change' }
  ]
}

// 监听比较选择的变化
watch([compareTask, compareType], async ([taskId, type]) => {
  if (taskId && type) {
    try {
      const response = await axios.get(`/api/tasks/${taskId}`)
      const task = response.data
      if (type === 'higher') {
        form.priority = task.priority + 1
      } else {
        form.priority = task.priority - 1
      }
    } catch (error) {
      console.error('获取任务信息失败:', error)
    }
  }
})

onMounted(async () => {
  if (props.task) {
    Object.assign(form, props.task)
  }
  
  // 获取地点列表
  try {
    const response = await axios.get('/api/locations')
    locations.value = response.data
  } catch (error) {
    console.error('获取地点列表失败:', error)
  }

  // 获取其他任务列表（用于比较优先级）
  try {
    const response = await axios.get('/api/tasks')
    otherTasks.value = response.data.filter(task => task.id !== props.task?.id)
  } catch (error) {
    console.error('获取任务列表失败:', error)
  }
})

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    emit('submit', form)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.priority-selector {
  margin-bottom: 20px;
}

.priority-options {
  margin-top: 10px;
}

.compare-select {
  width: 100%;
  margin-bottom: 10px;
}

.compare-type {
  display: flex;
  gap: 20px;
}

.unit {
  margin-left: 10px;
  color: #666;
}
</style> 