<template>
  <div class="scheduler-config">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
    >
      <el-form-item label="调度算法" prop="algorithm">
        <el-select v-model="form.algorithm">
          <el-option label="先来先服务" value="fcfs" />
          <el-option label="短作业优先" value="sjf" />
          <el-option label="轮转调度" value="rr" />
        </el-select>
      </el-form-item>

      <el-form-item label="时间粒度" prop="time_granularity">
        <el-input-number
          v-model="form.time_granularity"
          :min="15"
          :step="15"
        />
        <span class="unit">分钟</span>
      </el-form-item>

      <el-form-item label="默认任务时间" prop="default_task_time">
        <el-input-number
          v-model="form.default_task_time"
          :min="15"
          :step="15"
        />
        <span class="unit">分钟</span>
      </el-form-item>

      <el-form-item label="通勤时间计算" prop="commute_calculation">
        <el-switch v-model="form.commute_calculation" />
      </el-form-item>

      <el-form-item label="自动调度" prop="auto_schedule">
        <el-switch v-model="form.auto_schedule" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm">保存</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>

    <div class="algorithm-description">
      <h3>算法说明</h3>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="先来先服务">
          按照任务创建时间顺序进行调度，适合任务时间相近的情况
        </el-descriptions-item>
        <el-descriptions-item label="短作业优先">
          优先调度预计时间短的任务，适合任务时间差异较大的情况
        </el-descriptions-item>
        <el-descriptions-item label="轮转调度">
          按照优先级轮转分配时间片，适合需要平衡任务执行的情况
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const formRef = ref(null)

const form = reactive({
  algorithm: 'fcfs',
  time_granularity: 30,
  default_task_time: 60,
  commute_calculation: true,
  auto_schedule: true
})

const rules = {
  algorithm: [
    { required: true, message: '请选择调度算法', trigger: 'change' }
  ],
  time_granularity: [
    { required: true, message: '请输入时间粒度', trigger: 'blur' }
  ],
  default_task_time: [
    { required: true, message: '请输入默认任务时间', trigger: 'blur' }
  ]
}

onMounted(async () => {
  // TODO: 获取当前配置
})

const submitForm = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    // TODO: 保存配置
    ElMessage.success('配置已保存')
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
}
</script>

<style scoped>
.scheduler-config {
  padding: 20px;
}

.unit {
  margin-left: 10px;
  color: #666;
}

.algorithm-description {
  margin-top: 40px;
}

.algorithm-description h3 {
  margin-bottom: 20px;
}
</style> 