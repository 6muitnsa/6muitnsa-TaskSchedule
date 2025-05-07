<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <h3>优先级设置</h3>
        </div>
      </template>
      
      <el-form :model="form" label-width="120px">
        <!-- 配置1.1：数字优先级总大小 -->
        <el-form-item label="优先级总大小">
          <el-input-number v-model="form.totalPriority" :min="100" :max="10000" :step="100" />
          <span class="form-tip">默认值5000</span>
        </el-form-item>
        
        <!-- 配置1.2：优先级区间个数 -->
        <el-form-item label="优先级区间个数">
          <el-input-number v-model="form.intervalCount" :min="1" :max="10" />
          <span class="form-tip">默认值3</span>
        </el-form-item>
        
        <!-- 配置1.2.1：优先级区间设置 -->
        <template v-if="form.intervalCount > 0">
          <div class="interval-settings">
            <h4>优先级区间设置</h4>
            <div v-for="(interval, index) in form.intervals" :key="index" class="interval-item">
              <el-form-item :label="`区间${index + 1}`">
                <el-input v-model="interval.name" placeholder="区间命名" />
                <el-input-number v-model="interval.min" :min="0" :max="form.totalPriority" placeholder="最小值" />
                <span class="interval-separator">-</span>
                <el-input-number v-model="interval.max" :min="0" :max="form.totalPriority" placeholder="最大值" />
              </el-form-item>
            </div>
          </div>
        </template>
        
        <!-- 配置1.3：同区间任务分配优先级时的步长 -->
        <el-form-item label="优先级步长">
          <el-input-number v-model="form.priorityStep" :min="1" :max="100" />
          <span class="form-tip">默认值50</span>
        </el-form-item>
      </el-form>
    </el-card>
    <settings-save :settings="settings" />
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import SettingsSave from '@/components/SettingsSave.vue'
import { settingsApi } from '@/api'

const settings = ref({
  priority: {
    totalPriority: 5000,
    intervalCount: 3,
    intervals: [
      { name: '高优先级', min: 0, max: 1666 },
      { name: '中优先级', min: 1667, max: 3333 },
      { name: '低优先级', min: 3334, max: 5000 }
    ],
    priorityStep: 50
  }
})

const form = reactive({
  totalPriority: 5000,
  intervalCount: 3,
  intervals: [
    { name: '高优先级', min: 0, max: 1666 },
    { name: '中优先级', min: 1667, max: 3333 },
    { name: '低优先级', min: 3334, max: 5000 }
  ],
  priorityStep: 50
})

// 监听表单变化，更新 settings
watch(form, (newForm) => {
  settings.value.priority = {
    totalPriority: newForm.totalPriority,
    intervalCount: newForm.intervalCount,
    intervals: newForm.intervals,
    priorityStep: newForm.priorityStep
  }
}, { deep: true })

// 监听区间个数变化，动态调整区间数组
watch(() => form.intervalCount, (newCount) => {
  const oldCount = form.intervals.length
  if (newCount > oldCount) {
    // 添加新区间
    for (let i = oldCount; i < newCount; i++) {
      const step = Math.floor(form.totalPriority / newCount)
      form.intervals.push({
        name: `区间${i + 1}`,
        min: i * step,
        max: (i + 1) * step
      })
    }
  } else if (newCount < oldCount) {
    // 删除多余区间
    form.intervals.splice(newCount)
  }
})

// 监听总优先级变化，重新计算区间范围
watch(() => form.totalPriority, () => {
  const step = Math.floor(form.totalPriority / form.intervalCount)
  form.intervals.forEach((interval, index) => {
    interval.min = index * step
    interval.max = (index + 1) * step
  })
})

const saveSettings = async () => {
  try {
    await settingsApi.updateSettings(settings.value)
    ElMessage.success('设置保存成功')
  } catch (error) {
    ElMessage.error('设置保存失败')
  }
}

const resetSettings = () => {
  // TODO: 重置为默认设置
  ElMessage.info('设置已重置')
}
</script>

<style scoped>
.settings-container {
  max-width: 800px;
  margin: 0 auto;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-tip {
  margin-left: 10px;
  color: #909399;
  font-size: 14px;
}

.interval-settings {
  margin: 20px 0;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.interval-settings h4 {
  margin: 0 0 20px 0;
  color: #606266;
}

.interval-item {
  margin-bottom: 15px;
}

.interval-separator {
  margin: 0 10px;
  color: #909399;
}
</style> 