# 任务调度系统 API 文档

## 基础信息
- 基础URL: `/api`
- 所有请求和响应都使用JSON格式
- 时间格式: ISO 8601 (例如: "2024-04-14T10:00:00Z")

## 任务管理接口

### 1. 创建任务
- **URL**: `/tasks/`
- **方法**: POST
- **描述**: 创建新任务
- **请求体**:
```json
{
    "name": "任务名称",  // 必填，最大100字符
    "description": "任务描述",  // 可选，最大500字符
    "priority": 1,  // 必填，整数
    "startTime": "2024-04-14T10:00:00Z",  // 可选
    "endTime": "2024-04-14T11:00:00Z",  // 可选
    "status": "PENDING",  // 必填，可选值: PENDING, COMPLETED, FOLLOW_UP, CANCELLED
    "timeStatus": "NOT_STARTED",  // 必填，可选值: NOT_STARTED, IN_PROGRESS, OVERDUE, COMPLETED
    "type": "类型",  // 可选
    "cycle": "周期",  // 可选
    "estimatedTime": 60  // 可选，整数（分钟）
}
```
- **响应**: 返回创建的任务对象

### 2. 获取任务列表
- **URL**: `/tasks/`
- **方法**: GET
- **描述**: 获取任务列表
- **查询参数**:
  - `skip`: 跳过的记录数（默认0）
  - `limit`: 返回的最大记录数（默认100，最大1000）
- **响应**: 返回任务列表数组

### 3. 获取单个任务
- **URL**: `/tasks/{task_id}`
- **方法**: GET
- **描述**: 获取指定ID的任务
- **响应**: 返回任务对象

### 4. 更新任务
- **URL**: `/tasks/{task_id}`
- **方法**: PUT
- **描述**: 更新指定ID的任务
- **请求体**: 同创建任务
- **响应**: 返回更新后的任务对象

### 5. 删除任务
- **URL**: `/tasks/{task_id}`
- **方法**: DELETE
- **描述**: 删除指定ID的任务
- **响应**: 
```json
{
    "message": "Task deleted successfully"
}
```

### 6. 更新任务状态
- **URL**: `/tasks/{task_id}/status`
- **方法**: PATCH
- **描述**: 更新任务状态
- **请求参数**:
  - `status`: 新状态（PENDING, COMPLETED, FOLLOW_UP, CANCELLED）
- **响应**: 返回更新后的任务对象

## 调度器接口

### 1. 调度任务
- **URL**: `/schedule`
- **方法**: POST
- **描述**: 根据指定算法调度任务
- **请求体**:
```json
{
    "algorithm": "算法名称",
    "tasks": [
        {
            "id": "任务ID",
            "name": "任务名称",
            "priority": 1,
            "estimatedTime": 60,
            "startTime": "2024-04-14T10:00:00Z",
            "endTime": "2024-04-14T11:00:00Z"
        }
    ]
}
```
- **响应**:
```json
{
    "scheduled_tasks": [
        {
            "id": "任务ID",
            "name": "任务名称",
            "start_time": "2024-04-14T10:00:00Z",
            "end_time": "2024-04-14T11:00:00Z",
            "estimated_time": 60,
            "priority": 1
        }
    ],
    "evaluation": {
        "total_time": 120.5,
        "average_waiting_time": 30.2,
        "average_turnaround_time": 90.3,
        "efficiency": 0.85
    }
}
```

### 2. 获取可用算法
- **URL**: `/schedule/algorithms`
- **方法**: GET
- **描述**: 获取可用的调度算法列表
- **响应**: 返回算法名称数组

### 3. 评估调度
- **URL**: `/schedule/evaluate`
- **方法**: POST
- **描述**: 评估任务调度方案
- **请求体**: 同调度任务
- **响应**: 返回调度评估结果

## 错误响应
所有接口在发生错误时都会返回以下格式的响应：
```json
{
    "detail": "错误信息"
}
```

常见HTTP状态码：
- 200: 成功
- 400: 请求参数错误
- 404: 资源未找到
- 500: 服务器内部错误 