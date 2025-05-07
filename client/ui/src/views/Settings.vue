<template>
  <div class="settings">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>系统设置</h2>
      </div>
      </template>

          <el-form
        ref="formRef"
        :model="settings"
        :rules="rules"
            label-width="120px"
            class="settings-form"
          >
        <!-- 调度设置 -->
        <el-form-item label="启用调度">
          <el-switch v-model="settings.scheduler.enabled" />
            </el-form-item>

        <template v-if="settings.scheduler.enabled">
          <!-- 调度算法 -->
          <el-form-item label="调度算法">
            <el-radio-group v-model="settings.scheduler.algorithm">
              <el-radio label="fcfs">先来先服务</el-radio>
              <el-radio label="sjf">短任务优先</el-radio>
              <el-radio label="rr">时间片轮转调度</el-radio>
              <el-radio label="priority">优先级调度</el-radio>
              <el-radio label="custom">自定义</el-radio>
              <el-radio label="ai">AI调度</el-radio>
            </el-radio-group>

            <!-- 自定义算法 -->
            <div v-if="settings.scheduler.algorithm === 'custom'" class="custom-algorithm">
              <el-alert
                title="自定义算法说明"
                type="info"
                :closable="false"
                show-icon
              >
                <p>自定义算法将会接收的输入内容及格式</p>
                <p>自定义算法需要返回的输出内容及格式</p>
              </el-alert>

              <el-radio-group v-model="customAlgorithmType" class="mt-4">
                <el-radio label="file">文件选择</el-radio>
                <el-radio label="code">直接输入代码</el-radio>
              </el-radio-group>

              <div v-if="customAlgorithmType === 'file'" class="file-upload">
                <el-upload
                  action="#"
                  :auto-upload="false"
                  :on-change="handleAlgorithmFileChange"
                >
                  <el-button type="primary">选择Python文件</el-button>
                </el-upload>
              </div>

              <div v-if="customAlgorithmType === 'code'" class="code-input">
                <el-input
                  v-model="settings.scheduler.custom_algorithm"
                  type="textarea"
                  :rows="10"
                  placeholder="请输入Python代码"
                />
              </div>
            </div>

            <!-- AI调度 -->
            <div v-if="settings.scheduler.algorithm === 'ai'" class="ai-scheduling">
              <el-alert
                title="AI调度说明"
                type="warning"
                :closable="false"
                show-icon
              >
                <p>云端功能，需联网</p>
                <p>AI算法调度，难以尽如人意</p>
                <p>使用AI调度会将已有任务数据去除个人信息偏好等后上传</p>
              </el-alert>
            </div>
            </el-form-item>

          <!-- 任务密度偏好 -->
          <el-form-item label="任务密度偏好">
            <el-radio-group v-model="settings.scheduler.task_density">
              <el-radio label="none">无偏好</el-radio>
              <el-radio label="tight">偏好紧密的任务安排</el-radio>
              <el-radio label="loose">偏好稀疏的任务安排</el-radio>
            </el-radio-group>

            <!-- 无偏好 -->
            <div v-if="settings.scheduler.task_density === 'none'" class="density-none">
              <el-input-number
                v-model="settings.scheduler.daily_task_limit"
                :min="1"
                :max="24"
                :default-value="6"
                placeholder="每日任务时常上限"
              />
              <span class="unit">小时</span>
                      </div>

            <!-- 偏好稀疏 -->
            <div v-if="settings.scheduler.task_density === 'loose'" class="density-sparse">
              <el-checkbox v-model="settings.scheduler.enable_task_slicing">单次长时间任务切片</el-checkbox>
              <div v-if="settings.scheduler.enable_task_slicing" class="slicing-settings">
                <span>切片偏好：</span>
                <el-input-number
                  v-model="settings.scheduler.task_slice_preference"
                  :min="1"
                  :max="60"
                  :default-value="25"
                  placeholder="切片时长"
                />
                <span class="unit">分钟</span>
              </div>
            </div>
              </el-form-item>
        </template>

        <!-- 优先级设置 -->
        <el-divider>优先级设置</el-divider>
        <el-form-item label="优先级总大小">
                <el-input-number
            v-model="settings.priority.total_range"
            :min="1000"
            :max="10000"
            :default-value="5000"
          />
              </el-form-item>

        <el-form-item label="优先级区间个数">
                <el-input-number
            v-model="settings.priority.interval_count"
                  :min="1"
            :max="10"
            :default-value="3"
            @change="handlePriorityRangeCountChange"
                />
              </el-form-item>

        <div class="priority-ranges">
          <div v-for="(range, index) in settings.priority.intervals" :key="index" class="priority-range">
            <h4>区间 {{ index + 1 }}</h4>
            <el-form-item label="区间命名">
              <el-input v-model="range.name" />
            </el-form-item>
            <el-form-item label="区间范围">
              <el-input-number
                v-model="range.range[0]"
                :min="0"
                :max="settings.priority.total_range"
                :step="settings.priority.step_size"
              />
              <span class="separator">-</span>
              <el-input-number
                v-model="range.range[1]"
                :min="0"
                :max="settings.priority.total_range"
                :step="settings.priority.step_size"
              />
            </el-form-item>
          </div>
        </div>

        <el-form-item label="优先级步长">
          <el-input-number
            v-model="settings.priority.step_size"
            :min="1"
            :max="100"
            :default-value="50"
          />
        </el-form-item>

        <!-- 时间预测设置 -->
        <el-divider>时间预测设置</el-divider>
        <el-form-item label="启用时间预测">
          <el-switch v-model="settings.time_prediction.enabled" />
        </el-form-item>

        <template v-if="settings.time_prediction.enabled">
          <el-form-item label="启用通勤预测">
            <el-switch v-model="settings.time_prediction.commute.enabled" />
            </el-form-item>

          <template v-if="settings.time_prediction.commute.enabled">
            <el-form-item label="默认通勤时间">
              <el-input-number
                v-model="settings.time_prediction.commute.default_time"
                :min="1"
                :max="120"
                :default-value="15"
              />
              <span class="unit">分钟</span>
            </el-form-item>

            <div class="route-table">
              <el-button type="primary" @click="showRouteDialog = true">
                添加路由
              </el-button>

              <el-table :data="settings.time_prediction.commute.location_routes" style="width: 100%">
                <el-table-column prop="from" label="地点1" />
                <el-table-column prop="to" label="地点2" />
                <el-table-column prop="time" label="通勤时间">
                  <template #default="{ row }">
                    {{ row.time }} 分钟
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="200">
                  <template #default="{ row, $index }">
                    <el-button-group>
                      <el-button size="small" @click="handleEditRoute(row, $index)">
                        编辑
                      </el-button>
                      <el-button size="small" type="danger" @click="handleDeleteRoute($index)">
                        删除
              </el-button>
                    </el-button-group>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </template>
        </template>

        <el-form-item>
          <el-button type="primary" @click="handleSave">保存设置</el-button>
          <el-button @click="handleReset">重置</el-button>
            </el-form-item>
      </el-form>
    </el-card>

    <!-- 路由对话框 -->
    <el-dialog
      v-model="showRouteDialog"
      :title="isEditingRoute ? '修改路由' : '添加路由'"
      width="500px"
    >
      <el-form :model="routeForm" label-width="100px">
        <el-form-item label="地点1">
          <el-input v-model="routeForm.from" placeholder="请输入地点1" />
            </el-form-item>
        <el-form-item label="地点2">
          <el-input v-model="routeForm.to" placeholder="请输入地点2" />
            </el-form-item>
        <el-form-item label="通勤时间">
          <el-input-number
            v-model="routeForm.time"
            :min="1"
            :max="120"
            placeholder="请输入通勤时间"
          />
          <span class="unit">分钟</span>
            </el-form-item>
          </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showRouteDialog = false">取消</el-button>
          <el-button type="primary" @click="saveRoute">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useSettingsStore } from '@/store'
import { settingsApi } from '@/api'

const settingsStore = useSettingsStore()
const formRef = ref(null)

// 表单数据
const settings = reactive({
  scheduler: {
    enabled: true,
    algorithm: 'priority',
    custom_algorithm: '',
    task_density: 'none',
    daily_task_limit: 6,
    task_slice_preference: 25,
    enable_task_slicing: false
  },
  priority: {
    total_range: 5000,
    interval_count: 3,
    step_size: 50,
    intervals: [
      {
        name: '低',
        range: [0, 1000]
      },
      {
        name: '中',
        range: [1001, 2000]
      },
      {
        name: '高',
        range: [2001, 3000]
      }
    ]
  },
  time_prediction: {
    enabled: false,
    commute: {
      enabled: false,
      default_time: 15,
      location_routes: []
    }
  }
})

// 自定义算法相关
const customAlgorithmType = ref('file')

// 路由相关
const showRouteDialog = ref(false)
const isEditingRoute = ref(false)
const editingRouteIndex = ref(-1)
const routeForm = reactive({
  from: '',
  to: '',
  time: 15
})

// 初始化优先级区间
const initPriorityRanges = () => {
  if (!settings.priority.interval_count || settings.priority.interval_count < 1) {
    settings.priority.interval_count = 3
  }
  const rangeSize = Math.floor(settings.priority.total_range / settings.priority.interval_count)
  settings.priority.intervals = Array(settings.priority.interval_count).fill(null).map((_, index) => ({
    name: `区间${index + 1}`,
    range: [
      Math.floor(rangeSize * index),
      Math.floor(rangeSize * (index + 1))
    ]
  }))
}

// 处理优先级区间数量变化
const handlePriorityRangeCountChange = () => {
  initPriorityRanges()
}

// 处理算法文件上传
const handleAlgorithmFileChange = (file) => {
  // TODO: 实现文件上传逻辑
  ElMessage.success('文件上传成功')
}

// 保存路由
const saveRoute = () => {
  if (!routeForm.from || !routeForm.to) {
    ElMessage.warning('请填写完整的地点信息')
    return
  }

  if (isEditingRoute.value) {
    settings.time_prediction.commute.location_routes[editingRouteIndex.value] = { ...routeForm }
  } else {
    settings.time_prediction.commute.location_routes.push({ ...routeForm })
  }

  showRouteDialog.value = false
  isEditingRoute.value = false
  editingRouteIndex.value = -1
  Object.assign(routeForm, { from: '', to: '', time: 15 })
}

// 编辑路由
const handleEditRoute = (route, index) => {
  isEditingRoute.value = true
  editingRouteIndex.value = index
  Object.assign(routeForm, route)
  showRouteDialog.value = true
}

// 删除路由
const handleDeleteRoute = (index) => {
  settings.time_prediction.commute.location_routes.splice(index, 1)
}

// 保存设置
const handleSave = async () => {
  try {
    // 获取验证规则
    const validationRules = await settingsApi.getValidationRules()
    
    // 验证设置
    const isValid = validateSettings(settings, validationRules.data)
    if (!isValid) {
      ElMessage.error('设置验证失败，请检查输入')
      return
    }

    // 更新设置
    await settingsApi.updateSettings(settings)
    ElMessage.success('设置保存成功')
  } catch (error) {
    ElMessage.error('设置保存失败：' + error.message)
  }
}

// 重置设置
const handleReset = async () => {
  try {
    const response = await settingsApi.getSettings()
    Object.assign(settings, response.data)
    ElMessage.success('设置已重置')
  } catch (error) {
    ElMessage.error('重置设置失败：' + error.message)
  }
}

// 验证设置
const validateSettings = (settings, rules) => {
  if (!settings || !rules) return false
  
  // 验证调度配置
  if (settings.scheduler) {
    if (!rules.scheduler?.algorithm?.includes(settings.scheduler.algorithm)) {
      return false
    }
    if (!rules.scheduler?.task_density?.includes(settings.scheduler.task_density)) {
      return false
    }
    if (settings.scheduler.daily_task_limit < (rules.scheduler?.daily_task_limit?.min ?? 1) ||
        settings.scheduler.daily_task_limit > (rules.scheduler?.daily_task_limit?.max ?? 24)) {
      return false
    }
    if (settings.scheduler.task_slice_preference < (rules.scheduler?.task_slice_preference?.min ?? 1) ||
        settings.scheduler.task_slice_preference > (rules.scheduler?.task_slice_preference?.max ?? 60)) {
      return false
    }
  }

  // 验证优先级配置
  if (settings.priority) {
    if (settings.priority.total_range < (rules.priority?.total_range?.min ?? 1000) ||
        settings.priority.total_range > (rules.priority?.total_range?.max ?? 10000)) {
      return false
    }
    if (settings.priority.interval_count < (rules.priority?.interval_count?.min ?? 1) ||
        settings.priority.interval_count > (rules.priority?.interval_count?.max ?? 10)) {
      return false
    }
    if (settings.priority.step_size < (rules.priority?.step_size?.min ?? 1) ||
        settings.priority.step_size > (rules.priority?.step_size?.max ?? 100)) {
      return false
    }
  }

  // 验证时间预测配置
  if (settings.time_prediction?.commute) {
    if (settings.time_prediction.commute.default_time < (rules.time_prediction?.commute?.default_time?.min ?? 1) ||
        settings.time_prediction.commute.default_time > (rules.time_prediction?.commute?.default_time?.max ?? 120)) {
      return false
    }
  }

  return true
}

// 获取设置
onMounted(async () => {
  try {
    // 获取配置文件路径
    const response = await settingsApi.getConfigPath()
    const configPath = response.data
    
    // 读取配置文件
    const settingsResponse = await settingsApi.loadSettings(configPath)
    const loadedSettings = settingsResponse.data
    
    // 更新设置
    if (loadedSettings) {
      Object.assign(settings, loadedSettings)
    }
    
    initPriorityRanges()
  } catch (error) {
    ElMessage.error('获取设置失败：' + error.message)
  }
})
</script>

<style lang="scss" scoped>
.settings {
  padding: var(--spacing-medium);
  
  .settings-form {
    max-width: 800px;
    margin: 0 auto;
  }

  .custom-algorithm,
  .ai-scheduling,
  .density-none,
  .density-dense,
  .density-sparse {
    margin-top: var(--spacing-medium);
    padding: var(--spacing-medium);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
  }

  .priority-ranges {
    margin: var(--spacing-medium) 0;

    .priority-range {
      margin-bottom: var(--spacing-medium);
      padding: var(--spacing-medium);
      border: 1px solid var(--border-color);
      border-radius: var(--border-radius);

      h4 {
        margin: 0 0 var(--spacing-medium) 0;
        color: var(--text-primary);
      }
    }
  }

  .route-table {
    margin-top: var(--spacing-medium);
  }

  .unit {
    margin-left: var(--spacing-small);
    color: var(--text-secondary);
  }
  
  .separator {
    margin: 0 var(--spacing-small);
    color: var(--text-secondary);
  }

  .mt-4 {
    margin-top: var(--spacing-medium);
  }
}

// 响应式布局
@media (max-width: 768px) {
  .settings {
    .settings-form {
      padding: 0;
    }

    .priority-ranges {
      .priority-range {
        padding: var(--spacing-small);
      }
    }
  }
}
</style> 