# TaskSchedule API 文档

## 基础信息

- 基础URL: `http://localhost:8000`
- API版本: v1
- 文档地址: `http://localhost:8000/docs`

## 任务管理接口

### 1. 创建任务

- **URL**: `/api/tasks/`
- **方法**: POST
- **描述**: 创建一个新的任务
- **请求体**:
```json
{
    "name": "任务名称",
    "description": "任务描述",
    "priority": 1500,
    "start_time": "2024-04-19T10:00:00",
    "end_time": "2024-04-19T12:00:00",
    "task_type": "work",
    "is_locked": false,
    "estimated_time": 120,
    "location": "办公室",
    "commute_time": 30,
    "is_periodic": false,
    "period_type": "weekly",
    "period_value": 1,
    "period_days": "1,3,5",
    "total_count": 1
}
```

### 2. 获取任务列表

- **URL**: `/api/tasks/`
- **方法**: GET
- **描述**: 获取任务列表，支持分页和过滤
- **查询参数**:
  - `skip`: 跳过的记录数（默认：0）
  - `limit`: 每页记录数（默认：100，最大：100）
  - `status`: 任务状态过滤（可选值：pending, completed, follow_up, cancelled）
  - `time_status`: 时间状态过滤（可选值：not_started, in_progress, overdue, completed）

### 3. 获取单个任务

- **URL**: `/api/tasks/{task_id}`
- **方法**: GET
- **描述**: 获取指定ID的任务详情
- **路径参数**:
  - `task_id`: 任务ID

### 4. 更新任务

- **URL**: `/api/tasks/{task_id}`
- **方法**: PUT
- **描述**: 更新指定ID的任务信息
- **路径参数**:
  - `task_id`: 任务ID
- **请求体**: 同创建任务，所有字段可选

### 5. 删除任务

- **URL**: `/api/tasks/{task_id}`
- **方法**: DELETE
- **描述**: 删除指定ID的任务
- **路径参数**:
  - `task_id`: 任务ID

### 6. 更新任务状态

- **URL**: `/api/tasks/{task_id}/status`
- **方法**: PATCH
- **描述**: 更新指定ID的任务状态
- **路径参数**:
  - `task_id`: 任务ID
- **请求体**:
```json
{
    "status": "completed"
}
```

### 7. 更新任务优先级

- **URL**: `/api/tasks/{task_id}/priority`
- **方法**: PATCH
- **描述**: 更新指定ID的任务优先级
- **路径参数**:
  - `task_id`: 任务ID
- **请求体**:
```json
{
    "priority": 2000
}
```

## 数据模型

### 任务状态（TaskStatus）
- `pending`: 待完成
- `completed`: 已完成
- `follow_up`: 待跟进
- `cancelled`: 已取消

### 时间状态（TimeStatus）
- `not_started`: 未开始
- `in_progress`: 进行中
- `overdue`: 已超时
- `completed`: 已完成

### 任务类型（TaskType）
- `work`: 工作
- `study`: 学习
- `life`: 生活
- `other`: 其他

## 响应格式

### 成功响应
```json
{
    "id": 1,
    "name": "任务名称",
    "description": "任务描述",
    "priority": 1500,
    "status": "pending",
    "time_status": "not_started",
    "created_at": "2024-04-19T10:00:00",
    "updated_at": "2024-04-19T10:00:00"
}
```

### 错误响应
```json
{
    "detail": "错误信息"
}
```

## 状态码
- 200: 请求成功
- 201: 创建成功
- 400: 请求参数错误
- 404: 资源不存在
- 500: 服务器内部错误
