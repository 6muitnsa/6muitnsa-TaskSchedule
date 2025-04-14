<template>
  <div class="algorithm-selection">
    <h2>选择调度算法</h2>
    <el-form :model="form" label-width="120px">
      <el-form-item label="算法类型">
        <el-select v-model="form.algorithm" placeholder="请选择算法">
          <el-option
            v-for="item in algorithms"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">开始调度</el-button>
        <el-button @click="$router.back()">返回</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useSchedulerStore } from '@/stores/scheduler'

const router = useRouter()
const schedulerStore = useSchedulerStore()

const algorithms = [
  { label: '最早截止时间优先', value: 'EDF' },
  { label: '最短处理时间优先', value: 'SPT' },
  { label: '最高优先级优先', value: 'HPF' },
  { label: '轮转调度', value: 'RR' }
]

const form = ref({
  algorithm: 'EDF'
})

const handleSubmit = async () => {
  try {
    await schedulerStore.setAlgorithm(form.value.algorithm)
    ElMessage.success('算法设置成功')
    router.push('/schedule')
  } catch (error) {
    ElMessage.error('设置失败')
  }
}
</script>

<style scoped>
.algorithm-selection {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  margin-bottom: 30px;
  text-align: center;
}
</style> 