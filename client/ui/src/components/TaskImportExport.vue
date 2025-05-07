<template>
  <div class="task-import-export">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>任务导入导出</span>
        </div>
      </template>

      <div class="import-export-actions">
        <!-- 导出部分 -->
        <div class="export-section">
          <h3>导出任务</h3>
          <div class="export-buttons">
            <el-button type="primary" @click="handleExportJson">
              <el-icon><Download /></el-icon>
              导出为JSON
            </el-button>
            <el-button type="primary" @click="handleExportCsv">
              <el-icon><Download /></el-icon>
              导出为CSV
            </el-button>
          </div>
        </div>

        <!-- 导入部分 -->
        <div class="import-section">
          <h3>导入任务</h3>
          <div class="import-buttons">
            <el-upload
              class="upload-demo"
              action="#"
              :auto-upload="false"
              :on-change="handleJsonFileChange"
              :show-file-list="false"
            >
              <el-button type="primary">
                <el-icon><Upload /></el-icon>
                从JSON导入
              </el-button>
            </el-upload>
            <el-upload
              class="upload-demo"
              action="#"
              :auto-upload="false"
              :on-change="handleCsvFileChange"
              :show-file-list="false"
            >
              <el-button type="primary">
                <el-icon><Upload /></el-icon>
                从CSV导入
              </el-button>
            </el-upload>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, Upload } from '@element-plus/icons-vue'
import { importExportApi } from '../api'

// 导出为JSON
const handleExportJson = async () => {
  try {
    const response = await importExportApi.exportToJson()
    const blob = new Blob([response.data], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'tasks.json'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

// 导出为CSV
const handleExportCsv = async () => {
  try {
    const response = await importExportApi.exportToCsv()
    const blob = new Blob([response.data], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'tasks.csv'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

// 处理JSON文件选择
const handleJsonFileChange = async (file) => {
  try {
    if (!file.raw) {
      ElMessage.warning('请选择文件')
      return
    }

    if (!file.raw.name.endsWith('.json')) {
      ElMessage.warning('请选择JSON文件')
      return
    }

    const response = await importExportApi.importFromJson(file.raw)
    ElMessage.success(response.message)
  } catch (error) {
    console.error('导入失败:', error)
    ElMessage.error('导入失败')
  }
}

// 处理CSV文件选择
const handleCsvFileChange = async (file) => {
  try {
    if (!file.raw) {
      ElMessage.warning('请选择文件')
      return
    }

    if (!file.raw.name.endsWith('.csv')) {
      ElMessage.warning('请选择CSV文件')
      return
    }

    const response = await importExportApi.importFromCsv(file.raw)
    ElMessage.success(response.message)
  } catch (error) {
    console.error('导入失败:', error)
    ElMessage.error('导入失败')
  }
}
</script>

<style lang="scss" scoped>
.task-import-export {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .import-export-actions {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .export-section,
    .import-section {
      h3 {
        margin-bottom: 16px;
        font-size: 16px;
        color: #303133;
      }

      .export-buttons,
      .import-buttons {
        display: flex;
        gap: 16px;
      }
    }
  }
}
</style> 