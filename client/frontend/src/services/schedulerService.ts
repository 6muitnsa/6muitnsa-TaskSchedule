import { SchedulerType, SchedulerConfig } from '../types/scheduler'
import { Task } from '../types/task'
import axios from 'axios'

const API_BASE_URL = '/api/scheduler'

export interface ScheduledTask {
  id: string
  name: string
  startTime: Date
  endTime: Date
  estimatedTime: number
  priority: number
}

export interface ScheduleEvaluation {
  totalTime: number
  averageWaitingTime: number
  averageTurnaroundTime: number
  efficiency: number
}

export interface ScheduleResult {
  scheduledTasks: ScheduledTask[]
  evaluation: ScheduleEvaluation
}

class FCFSScheduler {
    schedule(tasks: Task[]): ScheduleResult[] {
        const sortedTasks = [...tasks].sort((a, b) => 
            new Date(a.createTime).getTime() - new Date(b.createTime).getTime()
        )
        
        let currentTime = new Date()
        return sortedTasks.map(task => {
            const startTime = new Date(currentTime)
            const duration = task.estimatedTime || 30 // 默认30分钟
            currentTime = new Date(currentTime.getTime() + duration * 60000)
            
            return {
                taskId: task.id,
                startTime,
                endTime: new Date(currentTime),
                actualDuration: duration
            }
        })
    }

    evaluate(tasks: Task[]): ScheduleEvaluation {
        const scheduleResults = this.schedule(tasks)
        const totalTime = scheduleResults.reduce((sum, result) => 
            sum + result.actualDuration, 0
        )
        
        let totalWaitingTime = 0
        let totalTurnaroundTime = 0
        
        scheduleResults.forEach((result, index) => {
            const task = tasks.find(t => t.id === result.taskId)!
            const waitingTime = (new Date(result.startTime).getTime() - 
                new Date(task.createTime).getTime()) / 60000
            const turnaroundTime = waitingTime + result.actualDuration
            
            totalWaitingTime += waitingTime
            totalTurnaroundTime += turnaroundTime
        })
        
        return {
            totalTime,
            averageWaitingTime: totalWaitingTime / tasks.length,
            averageTurnaroundTime: totalTurnaroundTime / tasks.length,
            efficiency: 1 - (totalWaitingTime / (totalTime * tasks.length))
        }
    }
}

class SJFScheduler {
    schedule(tasks: Task[]): ScheduleResult[] {
        const sortedTasks = [...tasks].sort((a, b) => 
            (a.estimatedTime || 30) - (b.estimatedTime || 30)
        )
        
        let currentTime = new Date()
        return sortedTasks.map(task => {
            const startTime = new Date(currentTime)
            const duration = task.estimatedTime || 30
            currentTime = new Date(currentTime.getTime() + duration * 60000)
            
            return {
                taskId: task.id,
                startTime,
                endTime: new Date(currentTime),
                actualDuration: duration
            }
        })
    }

    evaluate(tasks: Task[]): ScheduleEvaluation {
        const scheduleResults = this.schedule(tasks)
        const totalTime = scheduleResults.reduce((sum, result) => 
            sum + result.actualDuration, 0
        )
        
        let totalWaitingTime = 0
        let totalTurnaroundTime = 0
        
        scheduleResults.forEach((result, index) => {
            const task = tasks.find(t => t.id === result.taskId)!
            const waitingTime = (new Date(result.startTime).getTime() - 
                new Date(task.createTime).getTime()) / 60000
            const turnaroundTime = waitingTime + result.actualDuration
            
            totalWaitingTime += waitingTime
            totalTurnaroundTime += turnaroundTime
        })
        
        return {
            totalTime,
            averageWaitingTime: totalWaitingTime / tasks.length,
            averageTurnaroundTime: totalTurnaroundTime / tasks.length,
            efficiency: 1 - (totalWaitingTime / (totalTime * tasks.length))
        }
    }
}

class RRScheduler {
    private timeSlice: number

    constructor(timeSlice: number = 15) {
        this.timeSlice = timeSlice
    }

    schedule(tasks: Task[]): ScheduleResult[] {
        const results: ScheduleResult[] = []
        const taskQueue = [...tasks]
        const remainingTime = new Map<string, number>(
            tasks.map(task => [task.id, task.estimatedTime || 30])
        )
        
        let currentTime = new Date()
        
        while (taskQueue.length > 0) {
            const task = taskQueue.shift()!
            const remaining = remainingTime.get(task.id)!
            
            if (remaining > 0) {
                const startTime = new Date(currentTime)
                const duration = Math.min(remaining, this.timeSlice)
                currentTime = new Date(currentTime.getTime() + duration * 60000)
                
                results.push({
                    taskId: task.id,
                    startTime,
                    endTime: new Date(currentTime),
                    actualDuration: duration
                })
                
                remainingTime.set(task.id, remaining - duration)
                
                if (remaining - duration > 0) {
                    taskQueue.push(task)
                }
            }
        }
        
        return results
    }

    evaluate(tasks: Task[]): ScheduleEvaluation {
        const scheduleResults = this.schedule(tasks)
        const totalTime = scheduleResults.reduce((sum, result) => 
            sum + result.actualDuration, 0
        )
        
        let totalWaitingTime = 0
        let totalTurnaroundTime = 0
        
        scheduleResults.forEach((result, index) => {
            const task = tasks.find(t => t.id === result.taskId)!
            const waitingTime = (new Date(result.startTime).getTime() - 
                new Date(task.createTime).getTime()) / 60000
            const turnaroundTime = waitingTime + result.actualDuration
            
            totalWaitingTime += waitingTime
            totalTurnaroundTime += turnaroundTime
        })
        
        return {
            totalTime,
            averageWaitingTime: totalWaitingTime / tasks.length,
            averageTurnaroundTime: totalTurnaroundTime / tasks.length,
            efficiency: 1 - (totalWaitingTime / (totalTime * tasks.length))
        }
    }
}

export const schedulerService = {
    createScheduler(config: SchedulerConfig) {
        switch (config.type) {
            case SchedulerType.FCFS:
                return new FCFSScheduler()
            case SchedulerType.SJF:
                return new SJFScheduler()
            case SchedulerType.RR:
                return new RRScheduler(config.timeSlice)
            default:
                throw new Error('不支持的调度算法类型')
        }
    },

    async scheduleTasks(algorithm: string, tasks: Task[]): Promise<ScheduleResult> {
        try {
            const response = await axios.post(`${API_BASE_URL}/schedule`, {
                algorithm,
                tasks: tasks.map(task => ({
                    id: task.id,
                    name: task.name,
                    priority: task.priority,
                    estimatedTime: task.estimatedTime,
                    startTime: task.startTime,
                    endTime: task.endTime
                }))
            })
            return response.data
        } catch (error) {
            console.error('调度任务失败:', error)
            throw error
        }
    },

    async getAvailableAlgorithms(): Promise<string[]> {
        try {
            const response = await axios.get(`${API_BASE_URL}/schedule/algorithms`)
            return response.data
        } catch (error) {
            console.error('获取可用算法失败:', error)
            throw error
        }
    },

    async evaluateSchedule(tasks: ScheduledTask[]): Promise<ScheduleEvaluation> {
        try {
            const response = await axios.post(`${API_BASE_URL}/schedule/evaluate`, {
                tasks
            })
            return response.data
        } catch (error) {
            console.error('评估调度失败:', error)
            throw error
        }
    },

    async setAlgorithm(algorithm: string): Promise<void> {
        await axios.post(`${API_BASE_URL}/algorithm`, { algorithm })
    },

    async generateSchedule(): Promise<any> {
        const response = await axios.post(`${API_BASE_URL}/generate`)
        return response.data
    }
} 