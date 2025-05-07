<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <h3>基本设置</h3>
        </div>
      </template>
      
      <el-form :model="form" label-width="120px">
        <el-form-item label="系统名称">
          <el-input v-model="form.systemName" placeholder="请输入系统名称" />
        </el-form-item>
        
        <!-- 远程访问设置 -->
        <el-form-item label="远程访问">
          <el-button type="primary" @click="startRemoteAccess">启动远程访问</el-button>
          <span class="form-tip">允许通过手机访问本机服务</span>
        </el-form-item>
        
        <!-- 远程访问状态显示 -->
        <template v-if="remoteStatus.show">
          <el-alert
            :title="remoteStatus.message"
            :type="remoteStatus.type"
            :closable="false"
            show-icon
          />
          
          <!-- 远程访问URL和二维码 -->
          <div v-if="remoteStatus.url" class="remote-info">
            <div class="remote-url">
              <span>访问地址：</span>
              <el-input v-model="remoteStatus.url" readonly>
                <template #append>
                  <el-button @click="copyRemoteUrl">复制</el-button>
                </template>
              </el-input>
            </div>
            
            <div class="remote-qrcode">
              <span>扫描二维码访问：</span>
              <div class="qrcode-container">
                <img v-if="remoteStatus.qrcode" :src="'data:image/png;base64,' + remoteStatus.qrcode" alt="访问二维码" />
                <div v-else class="qrcode-placeholder">
                  二维码将显示在这里
                </div>
              </div>
            </div>
            
            <div class="remote-actions">
              <el-button type="danger" @click="stopRemoteAccess">停止远程访问</el-button>
            </div>
          </div>
        </template>
        
        <!-- 数据同步设置 -->
        <el-form-item label="数据同步">
          <el-button type="primary" @click="startSync">同步数据</el-button>
          <span class="form-tip">使用 cloudflared 进行安全的数据同步</span>
        </el-form-item>
        
        <!-- 同步状态显示 -->
        <template v-if="syncStatus.show">
          <el-alert
            :title="syncStatus.message"
            :type="syncStatus.type"
            :closable="false"
            show-icon
          />
          
          <!-- 同步URL和二维码 -->
          <div v-if="syncStatus.url" class="sync-info">
            <div class="sync-url">
              <span>同步地址：</span>
              <el-input v-model="syncStatus.url" readonly>
                <template #append>
                  <el-button @click="copyUrl">复制</el-button>
                </template>
              </el-input>
            </div>
            
            <div class="sync-qrcode">
              <span>扫描二维码同步：</span>
              <div class="qrcode-container">
                <img v-if="syncStatus.qrcode" :src="'data:image/png;base64,' + syncStatus.qrcode" alt="同步二维码" />
                <div v-else class="qrcode-placeholder">
                  二维码将显示在这里
                </div>
              </div>
            </div>
            
            <!-- 同步方向选择 -->
            <div class="sync-direction">
              <el-radio-group v-model="syncStatus.direction">
                <el-radio label="client">客户端同步到手机</el-radio>
                <el-radio label="mobile">手机同步到客户端</el-radio>
              </el-radio-group>
            </div>
            
            <div class="sync-actions">
              <el-button type="primary" @click="confirmSync">确认同步</el-button>
              <el-button @click="cancelSync">取消</el-button>
            </div>
          </div>
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
import axios from 'axios'

const form = reactive({
  systemName: 'TaskSchedule'
})

const remoteStatus = reactive({
  show: false,
  message: '',
  type: 'info',
  url: '',
  qrcode: ''
})

const syncStatus = reactive({
  show: false,
  message: '',
  type: 'info',
  url: '',
  qrcode: '',
  direction: 'client'
})

const startRemoteAccess = async () => {
  try {
    remoteStatus.show = true
    remoteStatus.message = '正在启动远程访问服务...'
    remoteStatus.type = 'info'
    
    const { data } = await axios.post('/api/remote/start')
    remoteStatus.url = data.url
    remoteStatus.qrcode = data.qrcode
    remoteStatus.message = '远程访问服务已启动，请扫描二维码或使用URL访问'
    remoteStatus.type = 'success'
  } catch (error) {
    remoteStatus.message = '启动远程访问服务失败：' + error.message
    remoteStatus.type = 'error'
  }
}

const stopRemoteAccess = async () => {
  try {
    await axios.post('/api/remote/stop')
    remoteStatus.show = false
    remoteStatus.url = ''
    ElMessage.success('远程访问服务已停止')
  } catch (error) {
    ElMessage.error('停止远程访问服务失败：' + error.message)
  }
}

const copyRemoteUrl = () => {
  navigator.clipboard.writeText(remoteStatus.url)
  ElMessage.success('URL已复制到剪贴板')
}

const startSync = async () => {
  try {
    syncStatus.show = true
    syncStatus.message = '正在启动同步服务...'
    syncStatus.type = 'info'
    
    const { data } = await axios.post('/api/sync/start')
    syncStatus.url = data.url
    syncStatus.qrcode = data.qrcode
    syncStatus.message = '同步服务已启动，请扫描二维码或使用URL进行同步'
    syncStatus.type = 'success'
  } catch (error) {
    syncStatus.message = '启动同步服务失败：' + error.message
    syncStatus.type = 'error'
  }
}

const copyUrl = () => {
  navigator.clipboard.writeText(syncStatus.url)
  ElMessage.success('URL已复制到剪贴板')
}

const confirmSync = async () => {
  try {
    await axios.post('/api/sync/confirm', { direction: syncStatus.direction })
    ElMessage.success('同步成功')
    cancelSync()
  } catch (error) {
    ElMessage.error('同步失败：' + error.message)
  }
}

const cancelSync = async () => {
  try {
    await axios.post('/api/sync/stop')
    syncStatus.show = false
    syncStatus.url = ''
    syncStatus.direction = 'client'
  } catch (error) {
    ElMessage.error('停止同步服务失败：' + error.message)
  }
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

.remote-info,
.sync-info {
  margin: 20px 0;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.remote-url,
.sync-url {
  margin-bottom: 20px;
}

.remote-qrcode,
.sync-qrcode {
  margin-bottom: 20px;
}

.qrcode-container {
  margin-top: 10px;
  width: 200px;
  height: 200px;
  border: 1px dashed #dcdfe6;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.qrcode-container img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.qrcode-placeholder {
  color: #909399;
  text-align: center;
  padding: 10px;
}

.sync-direction {
  margin-bottom: 20px;
}

.remote-actions,
.sync-actions {
  display: flex;
  gap: 10px;
}
</style> 