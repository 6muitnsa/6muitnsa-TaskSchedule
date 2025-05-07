import json
import csv
from datetime import datetime
from typing import List, Dict, Any
from models.task import TaskCreate
from services.task_service import TaskService

class ImportExportService:
    def __init__(self, db_path):
        self.task_service = TaskService(db_path)

    def export_tasks_to_json(self) -> str:
        """导出任务到JSON文件"""
        tasks = self.task_service.get_tasks()
        return json.dumps([task.model_dump() for task in tasks], ensure_ascii=False, indent=2)

    def export_tasks_to_csv(self) -> str:
        """导出任务到CSV文件"""
        tasks = self.task_service.get_tasks()
        
        # 准备CSV数据
        fieldnames = [
            'id', 'name', 'description', 'priority', 'status',
            'deadline', 'estimated_time', 'actual_time',
            'location', 'tags', 'created_at', 'updated_at'
        ]
        
        # 创建CSV字符串
        output = []
        output.append(','.join(fieldnames))
        
        for task in tasks:
            task_dict = task.model_dump()
            # 处理特殊字段
            task_dict['tags'] = '|'.join(task_dict['tags'])
            task_dict['deadline'] = task_dict['deadline'].isoformat() if task_dict['deadline'] else ''
            task_dict['created_at'] = task_dict['created_at'].isoformat()
            task_dict['updated_at'] = task_dict['updated_at'].isoformat()
            
            # 转义字段中的逗号
            row = []
            for field in fieldnames:
                value = str(task_dict.get(field, ''))
                if ',' in value:
                    value = f'"{value}"'
                row.append(value)
            
            output.append(','.join(row))
        
        return '\n'.join(output)

    def import_tasks_from_json(self, json_data: str) -> List[Dict[str, Any]]:
        """从JSON文件导入任务"""
        try:
            tasks_data = json.loads(json_data)
            results = []
            
            for task_data in tasks_data:
                # 移除不需要的字段
                task_data.pop('id', None)
                task_data.pop('created_at', None)
                task_data.pop('updated_at', None)
                
                # 创建任务
                task = TaskCreate(**task_data)
                created_task = self.task_service.create_task(task)
                results.append(created_task.model_dump())
            
            return results
        except Exception as e:
            raise ValueError(f"导入JSON数据失败: {str(e)}")

    def import_tasks_from_csv(self, csv_data: str) -> List[Dict[str, Any]]:
        """从CSV文件导入任务"""
        try:
            # 解析CSV数据
            lines = csv_data.strip().split('\n')
            if not lines:
                raise ValueError("CSV数据为空")
            
            # 获取字段名
            fieldnames = lines[0].split(',')
            results = []
            
            # 处理每一行数据
            for line in lines[1:]:
                # 处理引号内的逗号
                values = []
                in_quotes = False
                current_value = []
                
                for char in line:
                    if char == '"':
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        values.append(''.join(current_value))
                        current_value = []
                    else:
                        current_value.append(char)
                
                values.append(''.join(current_value))
                
                # 创建任务数据字典
                task_data = dict(zip(fieldnames, values))
                
                # 处理特殊字段
                if task_data.get('tags'):
                    task_data['tags'] = task_data['tags'].split('|')
                else:
                    task_data['tags'] = []
                
                if task_data.get('deadline'):
                    task_data['deadline'] = datetime.fromisoformat(task_data['deadline'])
                else:
                    task_data['deadline'] = None
                
                # 移除不需要的字段
                task_data.pop('id', None)
                task_data.pop('created_at', None)
                task_data.pop('updated_at', None)
                
                # 创建任务
                task = TaskCreate(**task_data)
                created_task = self.task_service.create_task(task)
                results.append(created_task.model_dump())
            
            return results
        except Exception as e:
            raise ValueError(f"导入CSV数据失败: {str(e)}") 