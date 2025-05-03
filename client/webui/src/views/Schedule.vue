<template>
  <div class="schedule">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>日程安排</span>
              <el-button type="primary" @click="showCreateDialog">
                创建日程
              </el-button>
            </div>
          </template>
          <el-calendar v-model="currentDate">
            <template #dateCell="{ data }">
              <div class="calendar-cell">
                <p>{{ data.day.split('-').slice(2).join('') }}</p>
                <div class="schedule-items">
                  <div
                    v-for="schedule in getSchedulesForDate(data.day)"
                    :key="schedule.schedule_id"
                    class="schedule-item"
                    :class="getScheduleTypeClass(schedule.type)"
                    @click="showScheduleDetail(schedule)"
                  >
                    {{ schedule.title }}
                  </div>
                </div>
              </div>
            </template>
          </el-calendar>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑日程' : '创建日程'"
      width="500px"
    >
      <el-form
        :model="scheduleForm"
        :rules="rules"
        ref="scheduleFormRef"
        label-width="100px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="scheduleForm.title" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="scheduleForm.description"
            type="textarea"
            :rows="4"
          />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="scheduleForm.type">
            <el-option label="工作" value="work" />
            <el-option label="学习" value="study" />
            <el-option label="休息" value="rest" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker
            v-model="scheduleForm.start_time"
            type="datetime"
            placeholder="选择开始时间"
          />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker
            v-model="scheduleForm.end_time"
            type="datetime"
            placeholder="选择结束时间"
          />
        </el-form-item>
        <el-form-item label="重复" prop="repeat">
          <el-select v-model="scheduleForm.repeat">
            <el-option label="不重复" value="none" />
            <el-option label="每天" value="daily" />
            <el-option label="每周" value="weekly" />
            <el-option label="每月" value="monthly" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveSchedule">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="detailDialogVisible"
      title="日程详情"
      width="500px"
    >
      <div v-if="selectedSchedule" class="schedule-detail">
        <h3>{{ selectedSchedule.title }}</h3>
        <p class="description">{{ selectedSchedule.description }}</p>
        <div class="meta">
          <el-tag :type="getScheduleTypeClass(selectedSchedule.type)">
            {{ getScheduleTypeText(selectedSchedule.type) }}
          </el-tag>
          <span class="time">
            {{ formatDate(selectedSchedule.start_time) }} -
            {{ formatDate(selectedSchedule.end_time) }}
          </span>
        </div>
        <div class="repeat" v-if="selectedSchedule.repeat !== 'none'">
          <span>重复: {{ getRepeatText(selectedSchedule.repeat) }}</span>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="danger" @click="deleteSchedule">删除</el-button>
          <el-button @click="editSchedule">编辑</el-button>
          <el-button type="primary" @click="detailDialogVisible = false">
            关闭
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import dayjs from 'dayjs'

export default {
  name: 'Schedule',
  setup() {
    const store = useStore()
    const currentDate = ref(new Date())
    const dialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const isEdit = ref(false)
    const selectedSchedule = ref(null)
    const scheduleFormRef = ref(null)

    const scheduleForm = ref({
      title: '',
      description: '',
      type: 'work',
      start_time: null,
      end_time: null,
      repeat: 'none'
    })

    const rules = {
      title: [
        { required: true, message: '请输入标题', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
      ],
      type: [
        { required: true, message: '请选择类型', trigger: 'change' }
      ],
      start_time: [
        { required: true, message: '请选择开始时间', trigger: 'change' }
      ],
      end_time: [
        { required: true, message: '请选择结束时间', trigger: 'change' }
      ]
    }

    const getSchedulesForDate = (date) => {
      return store.state.schedules.filter(schedule => {
        const scheduleDate = dayjs(schedule.start_time).format('YYYY-MM-DD')
        return scheduleDate === date
      })
    }

    const getScheduleTypeClass = (type) => {
      switch (type) {
        case 'work':
          return 'work'
        case 'study':
          return 'study'
        case 'rest':
          return 'rest'
        default:
          return 'other'
      }
    }

    const getScheduleTypeText = (type) => {
      switch (type) {
        case 'work':
          return '工作'
        case 'study':
          return '学习'
        case 'rest':
          return '休息'
        default:
          return '其他'
      }
    }

    const getRepeatText = (repeat) => {
      switch (repeat) {
        case 'daily':
          return '每天'
        case 'weekly':
          return '每周'
        case 'monthly':
          return '每月'
        default:
          return '不重复'
      }
    }

    const formatDate = (date) => {
      return dayjs(date).format('YYYY-MM-DD HH:mm')
    }

    const showCreateDialog = () => {
      isEdit.value = false
      scheduleForm.value = {
        title: '',
        description: '',
        type: 'work',
        start_time: null,
        end_time: null,
        repeat: 'none'
      }
      dialogVisible.value = true
    }

    const showScheduleDetail = (schedule) => {
      selectedSchedule.value = schedule
      detailDialogVisible.value = true
    }

    const editSchedule = () => {
      isEdit.value = true
      scheduleForm.value = { ...selectedSchedule.value }
      dialogVisible.value = true
      detailDialogVisible.value = false
    }

    const saveSchedule = async () => {
      if (!scheduleFormRef.value) return
      
      try {
        await scheduleFormRef.value.validate()
        if (isEdit.value) {
          await store.dispatch('updateSchedule', {
            scheduleId: selectedSchedule.value.schedule_id,
            scheduleData: scheduleForm.value
          })
          ElMessage.success('日程更新成功')
        } else {
          await store.dispatch('createSchedule', scheduleForm.value)
          ElMessage.success('日程创建成功')
        }
        dialogVisible.value = false
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }

    const deleteSchedule = async () => {
      try {
        await ElMessageBox.confirm(
          '确定要删除这个日程吗？',
          '警告',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        await store.dispatch('deleteSchedule', selectedSchedule.value.schedule_id)
        ElMessage.success('日程删除成功')
        detailDialogVisible.value = false
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除日程失败:', error)
          ElMessage.error('删除日程失败')
        }
      }
    }

    return {
      currentDate,
      dialogVisible,
      detailDialogVisible,
      isEdit,
      selectedSchedule,
      scheduleForm,
      scheduleFormRef,
      rules,
      getSchedulesForDate,
      getScheduleTypeClass,
      getScheduleTypeText,
      getRepeatText,
      formatDate,
      showCreateDialog,
      showScheduleDetail,
      editSchedule,
      saveSchedule,
      deleteSchedule
    }
  }
}
</script>

<style lang="scss" scoped>
.schedule {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .calendar-cell {
    height: 100%;
    padding: 4px;

    p {
      margin: 0;
      font-size: 14px;
      color: #666;
    }

    .schedule-items {
      margin-top: 4px;
    }

    .schedule-item {
      margin: 2px 0;
      padding: 2px 4px;
      border-radius: 2px;
      font-size: 12px;
      color: white;
      cursor: pointer;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;

      &.work {
        background-color: #409EFF;
      }

      &.study {
        background-color: #67C23A;
      }

      &.rest {
        background-color: #E6A23C;
      }

      &.other {
        background-color: #909399;
      }
    }
  }

  .schedule-detail {
    h3 {
      margin: 0 0 10px;
    }

    .description {
      margin: 0 0 10px;
      color: #666;
    }

    .meta {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;

      .time {
        color: #666;
      }
    }

    .repeat {
      color: #666;
    }
  }
}
</style> 