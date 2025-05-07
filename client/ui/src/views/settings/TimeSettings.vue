<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <h3>时间预测设置</h3>
        </div>
      </template>
      
      <el-form :model="form" label-width="120px">
        <!-- 配置2：时间预测 -->
        <el-form-item label="启用时间预测">
          <el-switch v-model="form.timePredictionEnabled" />
          <span class="form-tip">启用后系统将预测任务所需时间</span>
        </el-form-item>
        
        <template v-if="form.timePredictionEnabled">
          <!-- 配置2.1：通勤时间预测 -->
          <el-form-item label="启用通勤预测">
            <el-switch v-model="form.commutePredictionEnabled" />
            <span class="form-tip">启用后系统将预测任务间的通勤时间</span>
          </el-form-item>
          
          <template v-if="form.commutePredictionEnabled">
            <!-- 默认通勤时间 -->
            <el-form-item label="默认通勤时间">
              <el-input-number v-model="form.defaultCommuteTime" :min="1" :max="120" />
              <span class="form-tip">分钟</span>
            </el-form-item>
            
            <!-- 地点路由表 -->
            <el-form-item label="启用路由表">
              <el-switch v-model="form.routeTableEnabled" />
              <span class="form-tip">启用后可以设置地点间的通勤时间</span>
            </el-form-item>
            
            <template v-if="form.routeTableEnabled">
              <!-- 添加路由 -->
              <div class="route-form">
                <h4>添加路由</h4>
                <el-form-item label="地点1">
                  <el-input v-model="newRoute.location1" placeholder="请输入地点1" />
                </el-form-item>
                <el-form-item label="地点2">
                  <el-input v-model="newRoute.location2" placeholder="请输入地点2" />
                </el-form-item>
                <el-form-item label="通勤时间">
                  <el-input-number v-model="newRoute.time" :min="1" :max="120" />
                  <span class="form-tip">分钟</span>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="addRoute">保存路由</el-button>
                </el-form-item>
              </div>
              
              <!-- 路由列表 -->
              <div class="route-list">
                <h4>路由列表</h4>
                <el-table :data="form.routes" style="width: 100%">
                  <el-table-column prop="location1" label="地点1" />
                  <el-table-column prop="location2" label="地点2" />
                  <el-table-column prop="time" label="通勤时间">
                    <template #default="{ row }">
                      {{ row.time }} 分钟
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="150">
                    <template #default="{ row, $index }">
                      <el-button type="primary" link @click="editRoute($index)">编辑</el-button>
                      <el-button type="danger" link @click="deleteRoute($index)">删除</el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </template>
          </template>
        </template>
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
  timePrediction: {
    enabled: false,
    commutePredictionEnabled: false,
    defaultCommuteTime: 15,
    routeTableEnabled: false,
    routes: []
  }
})

const form = reactive({
  timePredictionEnabled: false,
  commutePredictionEnabled: false,
  defaultCommuteTime: 15,
  routeTableEnabled: false,
  routes: []
})

// 监听表单变化，更新 settings
watch(form, (newForm) => {
  settings.value.timePrediction = {
    enabled: newForm.timePredictionEnabled,
    commutePredictionEnabled: newForm.commutePredictionEnabled,
    defaultCommuteTime: newForm.defaultCommuteTime,
    routeTableEnabled: newForm.routeTableEnabled,
    routes: newForm.routes
  }
}, { deep: true })

const newRoute = reactive({
  location1: '',
  location2: '',
  time: 15
})

const addRoute = () => {
  if (!newRoute.location1 || !newRoute.location2) {
    ElMessage.warning('请填写完整的地点信息')
    return
  }
  
  form.routes.push({
    location1: newRoute.location1,
    location2: newRoute.location2,
    time: newRoute.time
  })
  
  // 清空表单
  newRoute.location1 = ''
  newRoute.location2 = ''
  newRoute.time = 15
  
  ElMessage.success('路由添加成功')
}

const editRoute = (index) => {
  // TODO: 实现编辑功能
  ElMessage.info('编辑功能开发中')
}

const deleteRoute = (index) => {
  form.routes.splice(index, 1)
  ElMessage.success('路由删除成功')
}

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

.route-form {
  margin: 20px 0;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.route-form h4 {
  margin: 0 0 20px 0;
  color: #606266;
}

.route-list {
  margin: 20px 0;
}

.route-list h4 {
  margin: 0 0 20px 0;
  color: #606266;
}
</style> 