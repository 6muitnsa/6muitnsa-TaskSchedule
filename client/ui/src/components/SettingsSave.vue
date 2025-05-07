<template>
  <div class="settings-save">
    <el-button
      type="primary"
      :loading="saving"
      @click="handleSave"
    >
      {{ saving ? '保存中...' : '保存设置' }}
    </el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { settingsApi } from '@/api'

const props = defineProps({
  settings: {
    type: Object,
    required: true
  }
})

const saving = ref(false)

const handleSave = async () => {
  try {
    saving.value = true
    await settingsApi.updateSettings(props.settings)
    ElMessage.success('设置保存成功')
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败：' + (error.message || '未知错误'))
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.settings-save {
  margin-top: 20px;
  text-align: center;
}
</style> 