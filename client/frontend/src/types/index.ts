export interface Task {
    id: string;
    name: string;
    description?: string;
    priority: number;
    startTime?: Date;
    endTime?: Date;
    status: TaskStatus;
    timeStatus: TimeStatus;
    type?: TaskType;
    cycle?: TaskCycle;
    count: number;
    isLocked: boolean;
    estimatedTime?: number;
    createTime: Date;
    updateTime: Date;
}

export enum TaskStatus {
    PENDING = '待完成',
    COMPLETED = '已完成',
    FOLLOW_UP = '待跟进',
    CANCELLED = '已取消'
}

export enum TimeStatus {
    NOT_STARTED = '未开始',
    IN_PROGRESS = '进行中',
    OVERDUE = '已超时',
    COMPLETED = '已完成'
}

export enum TaskType {
    WORK = '工作',
    STUDY = '学习',
    LIFE = '生活',
    OTHER = '其他'
}

export enum TaskCycle {
    DAILY = '每日',
    WEEKLY = '每周',
    MONTHLY = '每月',
    ONCE = '一次性'
}

export interface PomodoroTimer {
    id: string;
    taskId: string;
    duration: number;
    breakDuration: number;
    status: PomodoroStatus;
    startTime: Date;
    endTime: Date;
    completedCycles: number;
}

export enum PomodoroStatus {
    RUNNING = '运行中',
    PAUSED = '已暂停',
    COMPLETED = '已完成',
    BREAK = '休息中'
}

export interface TimeStatistics {
    totalTasks: number;
    completedTasks: number;
    totalTimeSpent: number;
    averageTaskDuration: number;
    productivityScore: number;
    dailyStatistics: DailyStat[];
    weeklyStatistics: WeeklyStat[];
    monthlyStatistics: MonthlyStat[];
}

export interface DailyStat {
    date: Date;
    completedTasks: number;
    totalTimeSpent: number;
    productivityScore: number;
}

export interface WeeklyStat {
    week: number;
    year: number;
    completedTasks: number;
    totalTimeSpent: number;
    productivityScore: number;
}

export interface MonthlyStat {
    month: number;
    year: number;
    completedTasks: number;
    totalTimeSpent: number;
    productivityScore: number;
}

export interface TimeAllocation {
    taskId: string;
    recommendedDuration: number;
    optimalTimeSlots: TimeSlot[];
    priorityScore: number;
}

export interface TimeSlot {
    startTime: Date;
    endTime: Date;
    score: number;
} 