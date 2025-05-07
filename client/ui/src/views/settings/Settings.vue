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
        :model="form"
        label-width="200px"
        class="settings-form"
      >
        <!-- 配置0：启用调度 -->
        <el-form-item label="启用调度">
          <el-switch v-model="form.enableScheduling" />
        </el-form-item>

        <template v-if="form.enableScheduling">
          <!-- 配置0.1：调度算法选择 -->
          <el-form-item label="调度算法选择">
            <el-radio-group v-model="form.schedulingAlgorithm">
              <el-radio label="fcfs">先来先服务</el-radio>
              <el-radio label="sjf">短任务优先</el-radio>
              <el-radio label="rr">时间片轮转调度</el-radio>
              <el-radio label="priority">优先级调度</el-radio>
              <el-radio label="custom">自定义</el-radio>
              <el-radio label="ai">AI调度</el-radio>
            </el-radio-group>

            <!-- 配置0.1.1：自定义算法 -->
            <div v-if="form.schedulingAlgorithm === 'custom'" class="custom-algorithm">
              <el-alert
                title="自定义算法说明"
                type="info"
                :closable="false"
                show-icon
              >
                <p>自定义算法将会接收的输入内容及格式：</p>
                <pre>{{ algorithmInputFormat }}</pre>
                <p>自定义算法需要返回的输出内容及格式：</p>
                <pre>{{ algorithmOutputFormat }}</pre>
              </el-alert>
              
              <el-radio-group v-model="customAlgorithmType">
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
                  v-model="form.customAlgorithmCode"
                  type="textarea"
                  :rows="10"
                  placeholder="请输入Python代码"
                />
              </div>
            </div>

            <!-- AI调度 -->
            <div v-if="form.schedulingAlgorithm === 'ai'" class="ai-scheduling">
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
              <el-switch v-model="form.enableAIScheduling" />
            </div>
          </el-form-item>

          <!-- 配置0.2：任务密度偏好 -->
          <el-form-item label="任务密度偏好">
            <el-radio-group v-model="form.taskDensityPreference">
              <el-radio label="none">无偏好</el-radio>
              <el-radio label="dense">偏好紧密的任务安排</el-radio>
              <el-radio label="sparse">偏好稀疏的任务安排</el-radio>
            </el-radio-group>

            <!-- 无偏好 -->
            <div v-if="form.taskDensityPreference === 'none'" class="density-none">
              <el-input-number
                v-model="form.dailyTaskLimit"
                :min="1"
                :max="24"
                :default-value="6"
                placeholder="每日任务时常上限"
              />
              <span class="unit">小时</span>
            </div>

            <!-- 偏好紧密 -->
            <div v-if="form.taskDensityPreference === 'dense'" class="density-dense">
              <el-radio-group v-model="form.densePreferenceType">
                <el-radio label="early">尽早完成</el-radio>
                <el-radio label="late">最迟完成</el-radio>
              </el-radio-group>
              <el-alert
                v-if="form.densePreferenceType === 'late'"
                title="不建议选择最迟完成"
                type="warning"
                :closable="false"
                show-icon
              />
            </div>

            <!-- 偏好稀疏 -->
            <div v-if="form.taskDensityPreference === 'sparse'" class="density-sparse">
              <el-checkbox v-model="form.enableTaskSlicing">单次长时间任务切片</el-checkbox>
              <div v-if="form.enableTaskSlicing" class="slicing-settings">
                <span>切片偏好：</span>
                <el-input-number
                  v-model="form.sliceDuration"
                  :min="1"
                  :max="60"
                  :default-value="25"
                  placeholder="切片时长"
                />
                <span class="unit">分钟</span>
                <el-checkbox v-model="form.syncWithPomodoro">与番茄钟相关记录联动</el-checkbox>
              </div>
            </div>
          </el-form-item>
        </template>

        <!-- 配置1：优先级相关 -->
        <el-form-item label="优先级相关">
          <!-- 配置1.1：数字优先级总大小 -->
          <el-form-item label="数字优先级总大小">
            <el-input-number
              v-model="form.priorityTotalSize"
              :min="1000"
              :max="10000"
              :step="100"
              :default-value="5000"
            />
          </el-form-item>

          <!-- 配置1.2：优先级区间的个数 -->
          <el-form-item label="优先级区间的个数">
            <el-input-number
              v-model="form.priorityRangeCount"
              :min="2"
              :max="10"
              :default-value="3"
              @change="handlePriorityRangeCountChange"
            />
          </el-form-item>

          <!-- 配置1.2.1：优先级区间设置 -->
          <el-form-item label="优先级区间设置">
            <div
              v-for="(range, index) in form.priorityRanges"
              :key="index"
              class="priority-range-item"
            >
              <span>区间{{ index + 1 }}</span>
              <el-input v-model="range.name" placeholder="区间命名" />
              <el-input-number
                v-model="range.min"
                :min="1"
                :max="form.priorityTotalSize"
                placeholder="最小值"
              />
              <el-input-number
                v-model="range.max"
                :min="1"
                :max="form.priorityTotalSize"
                placeholder="最大值"
              />
            </div>
          </el-form-item>

          <!-- 配置1.3：同区间任务分配优先级时的步长 -->
          <el-form-item label="同区间任务分配优先级时的步长">
            <el-input-number
              v-model="form.priorityStep"
              :min="1"
              :max="100"
              :default-value="50"
            />
          </el-form-item>
        </el-form-item>

        <!-- 远程访问设置 -->
        <el-divider>远程访问设置</el-divider>
        <el-form-item label="远程访问">
          <el-button 
            type="primary" 
            @click="handleRemoteAccess"
            :loading="remoteLoading"
          >
            {{ isRemoteRunning ? '停止远程访问' : '启动远程访问' }}
          </el-button>
        </el-form-item>

        <template v-if="remoteUrl">
          <el-form-item label="访问地址">
            <el-input v-model="remoteUrl" readonly>
              <template #append>
                <el-button @click="copyRemoteUrl">复制</el-button>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="二维码">
            <div class="qrcode-container">
              <img :src="'data:image/png;base64,' + remoteQrcode" alt="访问二维码" />
            </div>
          </el-form-item>
        </template>

        <!-- 配置2：时间预测 -->
        <el-form-item label="时间预测">
          <el-switch v-model="form.enableTimePrediction" />
        </el-form-item>

        <template v-if="form.enableTimePrediction">
          <!-- 配置2.1：通勤时间预测 -->
          <el-form-item label="通勤时间预测">
            <el-switch v-model="form.enableCommutePrediction" />
          </el-form-item>

          <template v-if="form.enableCommutePrediction">
            <el-form-item label="默认通勤时间">
              <el-input-number
                v-model="form.defaultCommuteTime"
                :min="1"
                :max="120"
                :default-value="15"
                placeholder="默认通勤时间"
              />
              <span class="unit">分钟</span>
            </el-form-item>

            <el-form-item label="地点路由表">
              <el-switch v-model="form.enableRouteTable" />
            </el-form-item>

            <template v-if="form.enableRouteTable">
              <el-form-item>
                <el-button type="primary" @click="showAddRouteDialog">手动添加</el-button>
              </el-form-item>

              <el-table :data="form.routeTable" style="width: 100%">
                <el-table-column prop="start" label="地点1" />
                <el-table-column prop="end" label="地点2" />
                <el-table-column prop="time" label="时间" />
                <el-table-column label="操作">
                  <template #default="{ row, $index }">
                    <el-button type="primary" link @click="editRoute(row, $index)">
                      修改
                    </el-button>
                    <el-button type="danger" link @click="deleteRoute($index)">
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </template>
          </template>
        </template>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">保存设置</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 添加/编辑路由对话框 -->
    <el-dialog
      v-model="routeDialogVisible"
      :title="isEditingRoute ? '修改路由' : '添加路由'"
      width="500px"
    >
      <el-form :model="routeForm" label-width="100px">
        <el-form-item label="地点1">
          <el-input v-model="routeForm.start" placeholder="请输入地点1" />
        </el-form-item>
        <el-form-item label="地点2">
          <el-input v-model="routeForm.end" placeholder="请输入地点2" />
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
          <el-button @click="routeDialogVisible = false">取消</el-button>
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

const settingsStore = useSettingsStore()
const formRef = ref(null)

// 表单数据
const form = reactive({
  enableScheduling: true,
  schedulingAlgorithm: 'fcfs',
  enableAIScheduling: false,
  customAlgorithmCode: '',
  taskDensityPreference: 'none',
  dailyTaskLimit: 6,
  densePreferenceType: 'early',
  enableTaskSlicing: false,
  sliceDuration: 25,
  syncWithPomodoro: false,
  priorityTotalSize: 5000,
  priorityRangeCount: 3,
  priorityRanges: [],
  priorityStep: 50,
  enableTimePrediction: false,
  enableCommutePrediction: false,
  defaultCommuteTime: 15,
  enableRouteTable: false,
  routeTable: []
})

// 自定义算法相关
const customAlgorithmType = ref('file')
const algorithmInputFormat = `{
  "tasks": [
    {
      "id": "string",
      "name": "string",
      "startTime": "string",
      "endTime": "string",
      "priority": number,
      "estimatedTime": number
    }
  ]
}`
const algorithmOutputFormat = `{
  "schedule": [
    {
      "taskId": "string",
      "startTime": "string",
      "endTime": "string"
    }
  ]
}`

// 路由表相关
const routeDialogVisible = ref(false)
const isEditingRoute = ref(false)
const editingRouteIndex = ref(-1)
const routeForm = reactive({
  start: '',
  end: '',
  time: 15
})

// 远程访问相关
const remoteLoading = ref(false)
const isRemoteRunning = ref(false)
const remoteUrl = ref('')
const remoteQrcode = ref('')

// 处理优先级区间数量变化
const handlePriorityRangeCountChange = (value) => {
  const currentLength = form.priorityRanges.length
  if (value > currentLength) {
    // 添加新的区间
    for (let i = currentLength; i < value; i++) {
      form.priorityRanges.push({
        name: `区间${i + 1}`,
        min: 1,
        max: form.priorityTotalSize
      })
    }
  } else {
    // 删除多余的区间
    form.priorityRanges = form.priorityRanges.slice(0, value)
  }
}

// 处理算法文件选择
const handleAlgorithmFileChange = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    form.customAlgorithmCode = e.target.result
  }
  reader.readAsText(file.raw)
}

// 显示添加路由对话框
const showAddRouteDialog = () => {
  isEditingRoute.value = false
  editingRouteIndex.value = -1
  routeForm.start = ''
  routeForm.end = ''
  routeForm.time = 15
  routeDialogVisible.value = true
}

// 编辑路由
const editRoute = (row, index) => {
  isEditingRoute.value = true
  editingRouteIndex.value = index
  routeForm.start = row.start
  routeForm.end = row.end
  routeForm.time = row.time
  routeDialogVisible.value = true
}

// 删除路由
const deleteRoute = (index) => {
  form.routeTable.splice(index, 1)
}

// 保存路由
const saveRoute = () => {
  if (!routeForm.start || !routeForm.end || !routeForm.time) {
    ElMessage.warning('请填写完整信息')
    return
  }

  const routeData = {
    start: routeForm.start,
    end: routeForm.end,
    time: routeForm.time
  }

  if (isEditingRoute.value) {
    form.routeTable[editingRouteIndex.value] = routeData
  } else {
    form.routeTable.push(routeData)
  }

  routeDialogVisible.value = false
}

// 处理远程访问
const handleRemoteAccess = async () => {
  try {
    remoteLoading.value = true
    if (isRemoteRunning.value) {
      // 停止远程访问
      const response = await fetch('/api/remote/stop', {
        method: 'POST'
      })
      const data = await response.json()
      if (data.success) {
        isRemoteRunning.value = false
        remoteUrl.value = ''
        remoteQrcode.value = ''
        ElMessage.success('远程访问已停止')
      }
    } else {
      // 启动远程访问
      const response = await fetch('/api/remote/start', {
        method: 'POST'
      })
      const data = await response.json()
      if (data.success) {
        isRemoteRunning.value = true
        remoteUrl.value = data.url
        remoteQrcode.value = data.qrcode
        ElMessage.success('远程访问已启动')
      }
    }
  } catch (error) {
    ElMessage.error('操作失败：' + error.message)
  } finally {
    remoteLoading.value = false
  }
}

// 复制远程访问地址
const copyRemoteUrl = () => {
  navigator.clipboard.writeText(remoteUrl.value)
    .then(() => ElMessage.success('地址已复制'))
    .catch(() => ElMessage.error('复制失败'))
}

// 检查远程访问状态
const checkRemoteStatus = async () => {
  try {
    const response = await fetch('/api/remote/status')
    const data = await response.json()
    if (data.success) {
      isRemoteRunning.value = data.is_running
      if (data.is_running) {
        remoteUrl.value = data.url
        remoteQrcode.value = data.qrcode
      }
    }
  } catch (error) {
    console.error('获取远程访问状态失败：', error)
  }
}

// 获取设置
onMounted(async () => {
  try {
    const settings = await settingsStore.fetchSettings()
    Object.assign(form, settings)
    await checkRemoteStatus()
  } catch (error) {
    console.error('获取设置失败:', error)
  }
})

// 提交表单
const handleSubmit = async () => {
  try {
    await settingsStore.updateSettings(form)
    ElMessage.success('设置保存成功')
  } catch (error) {
    console.error('保存设置失败:', error)
  }
}

// 重置表单
const handleReset = async () => {
  try {
    const settings = await settingsStore.fetchSettings()
    Object.assign(form, settings)
    ElMessage.success('设置已重置')
  } catch (error) {
    console.error('重置设置失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.settings {
  max-width: 1000px;
  margin: 0 auto;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h2 {
      margin: 0;
    }
  }
  
  .settings-form {
    margin-top: 20px;
    
    .custom-algorithm,
    .ai-scheduling,
    .density-none,
    .density-dense,
    .density-sparse,
    .slicing-settings {
      margin-top: 10px;
      padding: 10px;
      border: 1px solid #dcdfe6;
      border-radius: 4px;
    }
    
    .priority-range-item {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
      
      span {
        min-width: 60px;
      }
    }
    
    .unit {
      margin-left: 5px;
      color: #606266;
    }
    
    pre {
      background-color: #f5f7fa;
      padding: 10px;
      border-radius: 4px;
      margin: 10px 0;
    }
  }

  .qrcode-container {
    display: flex;
    justify-content: center;
    margin: 20px 0;
    
    img {
      max-width: 200px;
      height: auto;
    }
  }
}
</style> 