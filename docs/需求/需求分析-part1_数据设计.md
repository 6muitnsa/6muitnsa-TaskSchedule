# 数据设计

## 前后端数据交互

### 1. 任务数据格式
```json
{
    "task_id": "string",  // 任务唯一标识符
    "name": "string",     // 任务名称
    "description": "string", // 任务描述
    "priority": number,   // 任务优先级数值
    "tags": ["string"],   // 任务标签列表
    "time_info": {
        "start_time": "datetime",  // 开始时间
        "end_time": "datetime",    // 结束时间
        "estimated_duration": number, // 预计完成时间（分钟）
        "location": "string",      // 地点
        "commute_time": number,    // 通勤时间（分钟）
        "rest_time": number        // 休息时间（分钟）
    },
    "complex_info": {
        "period": {
            "type": "string",      // 周期类型：null/"independent"/"composite"
            "value": "string"      // 周期值：如"3d"/"1m"/"wed,thu"
        },
        "completion_times": {
            "type": "string",      // 完成次数类型："once"/"fixed"/"unlimited"
            "value": number        // 完成次数值
        },
        "time_slot": {
            "start": "time",       // 时间段开始
            "end": "time"          // 时间段结束
        }
    },
    "status": "string",   // 任务状态：未开始/进行中/已完成/已放弃
    "created_at": "datetime",  // 创建时间
    "updated_at": "datetime"   // 更新时间
}
```

### 2. 番茄钟数据格式
```json
{
    "pomodoro_id": "string",  // 番茄钟记录ID
    "task_id": "string",      // 关联的任务ID
    "focus_time": number,     // 专注时长（分钟）
    "rest_time": number,      // 休息时长（分钟）
    "start_time": "datetime", // 开始时间
    "end_time": "datetime",   // 结束时间
    "status": "string"        // 状态：专注中/休息中/已完成
}
```

### 3. 同步数据格式
```json
{
    "sync_id": "string",      // 同步会话ID
    "direction": "string",    // 同步方向：client_to_mobile/mobile_to_client
    "tasks": ["task_id"],     // 同步的任务ID列表
    "pomodoros": ["pomodoro_id"], // 同步的番茄钟记录ID列表
    "timestamp": "datetime"   // 同步时间
}
```

## 配置文件存储(custom.yaml)

### 1. 调度配置
```yaml
scheduler:
  enabled: true
  algorithm: "priority"  # 可选：fcfs/sjf/rr/priority/custom/ai
  custom_algorithm: ""   # 自定义算法文件路径或代码
  task_density: "none"   # 可选：none/tight/loose
  daily_task_limit: 6    # 每日任务时长上限（小时）
  task_slice_preference: 25  # 任务切片时长（分钟）
```

### 2. 优先级配置
```yaml
priority:
  total_range: 5000      # 数字优先级总大小
  interval_count: 3      # 优先级区间个数
  step_size: 50         # 同区间任务优先级步长
  intervals:            # 优先级区间设置
    - name: "低"
      range: [0, 1000]
    - name: "中"
      range: [1001, 2000]
    - name: "高"
      range: [2001, 3000]
```

### 3. 时间预测配置
```yaml
time_prediction:
  enabled: false
  commute:
    enabled: false
    default_time: 15    # 默认通勤时间（分钟）
    location_routes:    # 地点路由表
      - from: "地点1"
        to: "地点2"
        time: 30        # 通勤时间（分钟）
```

## 数据库存储(.db)

### 1. 任务表(tasks)
```sql
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    priority INTEGER NOT NULL,
    start_time DATETIME,
    end_time DATETIME,
    estimated_duration INTEGER DEFAULT 60,
    location TEXT,
    commute_time INTEGER,
    rest_time INTEGER DEFAULT 5,
    period_type TEXT,
    period_value TEXT,
    completion_type TEXT,
    completion_value INTEGER,
    time_slot_start TIME,
    time_slot_end TIME,
    status TEXT DEFAULT '未开始',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 2. 任务标签关联表(task_tags)
```sql
CREATE TABLE task_tags (
    task_id TEXT,
    tag TEXT,
    PRIMARY KEY (task_id, tag),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);
```

### 3. 番茄钟记录表(pomodoros)
```sql
CREATE TABLE pomodoros (
    pomodoro_id TEXT PRIMARY KEY,
    task_id TEXT,
    focus_time INTEGER,
    rest_time INTEGER,
    start_time DATETIME,
    end_time DATETIME,
    status TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);
```

### 4. 同步记录表(sync_records)
```sql
CREATE TABLE sync_records (
    sync_id TEXT PRIMARY KEY,
    direction TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5. 同步任务关联表(sync_tasks)
```sql
CREATE TABLE sync_tasks (
    sync_id TEXT,
    task_id TEXT,
    PRIMARY KEY (sync_id, task_id),
    FOREIGN KEY (sync_id) REFERENCES sync_records(sync_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);
```

### 6. 同步番茄钟关联表(sync_pomodoros)
```sql
CREATE TABLE sync_pomodoros (
    sync_id TEXT,
    pomodoro_id TEXT,
    PRIMARY KEY (sync_id, pomodoro_id),
    FOREIGN KEY (sync_id) REFERENCES sync_records(sync_id),
    FOREIGN KEY (pomodoro_id) REFERENCES pomodoros(pomodoro_id)
);
```