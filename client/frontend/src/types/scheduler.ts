import { Task } from './task'

export enum SchedulerType {
    FCFS = 'FCFS',
    SJF = 'SJF',
    RR = 'RR'
}

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

export interface SchedulerConfig {
    type: SchedulerType
    timeSlice?: number  // 用于RR算法的时间片大小
}

export interface Scheduler {
    schedule(tasks: Task[]): ScheduleResult[];
    evaluate(tasks: Task[]): ScheduleEvaluation;
} 