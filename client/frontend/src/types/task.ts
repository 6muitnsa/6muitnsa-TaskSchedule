export enum TaskStatus {
    PENDING = 'PENDING',
    COMPLETED = 'COMPLETED',
    FOLLOW_UP = 'FOLLOW_UP',
    CANCELLED = 'CANCELLED'
}

export const TaskStatusText = {
    [TaskStatus.PENDING]: '待完成',
    [TaskStatus.COMPLETED]: '已完成',
    [TaskStatus.FOLLOW_UP]: '待跟进',
    [TaskStatus.CANCELLED]: '已取消'
}

export enum TimeStatus {
    NOT_STARTED = 'NOT_STARTED',
    IN_PROGRESS = 'IN_PROGRESS',
    OVERDUE = 'OVERDUE',
    COMPLETED = 'COMPLETED'
}

export const TimeStatusText = {
    [TimeStatus.NOT_STARTED]: '未开始',
    [TimeStatus.IN_PROGRESS]: '进行中',
    [TimeStatus.OVERDUE]: '已超时',
    [TimeStatus.COMPLETED]: '已完成'
}

export enum Priority {
    LOW = 1,
    MEDIUM = 2,
    HIGH = 3
}

export const PriorityText = {
    [Priority.LOW]: '低',
    [Priority.MEDIUM]: '中',
    [Priority.HIGH]: '高'
}

export interface Task {
    id: string;                    // 任务ID
    title: string;                  // 任务名称
    description: string;            // 任务描述
    priority: 'low' | 'medium' | 'high';  // 优先级
    estimatedDuration: number;      // 预计时间（分钟）
    deadline: Date;                 // 截止时间
    status: 'pending' | 'inProgress' | 'completed';  // 任务状态
    createdAt: Date;                // 创建时间
    updatedAt: Date;                // 更新时间
}

export type TaskPriority = Task['priority']
export type TaskStatus = Task['status']

export interface TaskFormData {
    name: string;
    description?: string;
    priority: Priority;
    startTime?: Date;
    endTime?: Date;
    status: TaskStatus;
    timeStatus: TimeStatus;
    type?: string;
    cycle?: string;
    estimatedTime?: number;
} 