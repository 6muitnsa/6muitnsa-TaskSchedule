<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <h3>调度设置</h3>
        </div>
      </template>
      
      <el-form :model="form" label-width="120px">
        <!-- 配置0：启用调度 -->
        <el-form-item label="启用调度">
          <el-switch v-model="form.schedulerEnabled" />
          <span class="form-tip">启用后系统将自动调度任务</span>
        </el-form-item>
        
        <template v-if="form.schedulerEnabled">
          <!-- 配置0.1：调度算法选择 -->
          <el-form-item label="调度算法">
            <el-radio-group v-model="form.algorithm">
              <el-radio label="fcfs">先来先服务</el-radio>
              <el-radio label="sjf">短任务优先</el-radio>
              <el-radio label="round-robin">时间片轮转调度</el-radio>
              <el-radio label="priority">优先级调度</el-radio>
              <el-radio label="custom">自定义</el-radio>
              <el-radio label="ai">AI调度</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <!-- 自定义算法配置 -->
          <template v-if="form.algorithm === 'custom'">
            <el-form-item label="自定义算法">
              <el-radio-group v-model="form.customType">
                <el-radio label="file">选择Python文件</el-radio>
                <el-radio label="code">直接输入代码</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item v-if="form.customType === 'file'">
              <el-upload
                action="#"
                :auto-upload="false"
                :on-change="handleFileChange"
                accept=".py"
              >
                <el-button type="primary">选择Python文件</el-button>
              </el-upload>
            </el-form-item>
            
            <el-form-item v-if="form.customType === 'code'">
              <el-input
                type="textarea"
                v-model="form.customCode"
                :rows="10"
                placeholder="请输入Python代码"
              />
            </el-form-item>
          </template>
          
          <!-- AI调度说明 -->
          <template v-if="form.algorithm === 'ai'">
            <el-alert
              title="云端功能，需联网"
              type="info"
              :closable="false"
              show-icon
            />
            <el-alert
              title="AI算法调度，难以尽如人意"
              type="warning"
              :closable="false"
              show-icon
            />
            <el-alert
              title="使用AI调度会将已有任务数据去除个人信息偏好等后上传"
              type="warning"
              :closable="false"
              show-icon
            />
          </template>
          
          <!-- 配置0.2：任务密度偏好 -->
          <el-form-item label="任务密度偏好">
            <el-radio-group v-model="form.densityPreference">
              <el-radio label="none">无偏好</el-radio>
              <el-radio label="dense">偏好紧密的任务安排</el-radio>
              <el-radio label="sparse">偏好稀疏的任务安排</el-radio>
            </el-radio-group>
          </el-form-item>
          
          <!-- 无偏好设置 -->
          <template v-if="form.densityPreference === 'none'">
            <el-form-item label="每日任务时长上限">
              <el-input-number v-model="form.dailyTaskLimit" :min="1" :max="24" />
              <span class="form-tip">小时</span>
            </el-form-item>
          </template>
          
          <!-- 紧密安排设置 -->
          <template v-if="form.densityPreference === 'dense'">
            <el-form-item label="完成偏好">
              <el-radio-group v-model="form.completionPreference">
                <el-radio label="early">尽早完成</el-radio>
                <el-radio label="late">最迟完成</el-radio>
              </el-radio-group>
            </el-form-item>
          </template>
          
          <!-- 稀疏安排设置 -->
          <template v-if="form.densityPreference === 'sparse'">
            <el-form-item label="单次长时间任务切片">
              <el-input-number v-model="form.sliceDuration" :min="5" :max="120" />
              <span class="form-tip">分钟</span>
            </el-form-item>
            <el-form-item>
              <el-checkbox v-model="form.syncWithPomodoro">与番茄钟记录联动</el-checkbox>
            </el-form-item>
          </template>
        </template>
        
        <el-form-item>
          <el-button type="primary" @click="saveSettings">保存设置</el-button>
          <el-button @click="resetSettings">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
  schedulerEnabled: true,
  algorithm: 'priority',
  customType: 'file',
  customCode: '',
  densityPreference: 'none',
  dailyTaskLimit: 6,
  completionPreference: 'early',
  sliceDuration: 25,
  syncWithPomodoro: false
})

const handleFileChange = (file) => {
  // TODO: 处理文件上传
  console.log('File changed:', file)
}

const saveSettings = async () => {
  try {
    // TODO: 调用API保存设置
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

.el-alert {
  margin-bottom: 10px;
}
</style> 