from database import get_db
from datetime import datetime, timedelta
from models.task import Task
from models.sync_record import SyncRecord
from typing import Dict, List, Any
from services.task_service import TaskService
from sqlite3 import Error as SQLiteError
import os
import json
from .scheduler_service import SchedulerService

class StatisticsService:
    def __init__(self, db_path):
        self.task_service = TaskService(db_path)
        self.scheduler_service = SchedulerService()
        self.stats_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'statistics.json')
        self._ensure_stats_file()

    def _ensure_stats_file(self):
        """确保统计文件存在"""
        os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
        if not os.path.exists(self.stats_file):
            self._save_stats({
                'daily_stats': {},
                'weekly_stats': {},
                'monthly_stats': {},
                'last_updated': datetime.now().isoformat()
            })

    def _load_stats(self) -> Dict:
        """加载统计数据"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'daily_stats': {},
                'weekly_stats': {},
                'monthly_stats': {},
                'last_updated': datetime.now().isoformat()
            }

    def _save_stats(self, stats: Dict):
        """保存统计数据"""
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    def get_overview(self):
        """获取统计概览"""
        try:
            tasks = self.task_service.get_all_tasks()
            
            # 计算基本统计信息
            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t['status'] == 'completed'])
            pending_tasks = len([t for t in tasks if t['status'] == 'pending'])
            
            # 计算完成率
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            # 计算优先级分布
            priority_distribution = {
                'high': len([t for t in tasks if t['priority'] == 'high']),
                'medium': len([t for t in tasks if t['priority'] == 'medium']),
                'low': len([t for t in tasks if t['priority'] == 'low'])
            }
            
            # 计算最近7天的任务完成情况
            today = datetime.now().date()
            daily_completion = {}
            for i in range(7):
                date = today - timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                daily_completion[date_str] = len([
                    t for t in tasks 
                    if t['status'] == 'completed' 
                    and datetime.strptime(t['updated_at'], '%Y-%m-%d %H:%M:%S').date() == date
                ])
            
            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'completion_rate': round(completion_rate, 2),
                'priority_distribution': priority_distribution,
                'daily_completion': daily_completion
            }
        except Exception as e:
            print(f"获取统计概览失败: {str(e)}")
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'pending_tasks': 0,
                'completion_rate': 0,
                'priority_distribution': {'high': 0, 'medium': 0, 'low': 0},
                'daily_completion': {}
            }

    def _get_recent_completions(self, days: int) -> List[Dict[str, Any]]:
        """获取最近几天的任务完成情况"""
        tasks = self.task_service.get_all_tasks()
        today = datetime.now().date()
        completions = []
        
        for i in range(days):
            date = today - timedelta(days=i)
            date_str = date.isoformat()
            completed_count = sum(1 for task in tasks 
                                if task.get('status') == 'completed' 
                                and task.get('completed_at', '').startswith(date_str))
            
            completions.append({
                'date': date_str,
                'count': completed_count
            })
        
        return completions

    def update_task_statistics(self, task_id: str, status: str, completion_time: float = None):
        """更新任务统计信息"""
        stats = self._load_stats()
        today = datetime.now().date().isoformat()
        
        # 更新每日统计
        if today not in stats['daily_stats']:
            stats['daily_stats'][today] = {
                'total_tasks': 0,
                'completed_tasks': 0,
                'total_completion_time': 0
            }
        
        daily_stats = stats['daily_stats'][today]
        if status == 'completed':
            daily_stats['completed_tasks'] += 1
            if completion_time:
                daily_stats['total_completion_time'] += completion_time
        
        daily_stats['total_tasks'] += 1
        
        # 更新最后更新时间
        stats['last_updated'] = datetime.now().isoformat()
        
        self._save_stats(stats)

    def get_daily_statistics(self, date: str = None) -> Dict:
        """获取每日统计信息"""
        stats = self._load_stats()
        if not date:
            date = datetime.now().date().isoformat()
        return stats['daily_stats'].get(date, {
            'total_tasks': 0,
            'completed_tasks': 0,
            'total_completion_time': 0
        })

    def get_weekly_statistics(self) -> Dict:
        """获取每周统计信息"""
        stats = self._load_stats()
        return stats['weekly_stats']

    def get_monthly_statistics(self) -> Dict:
        """获取每月统计信息"""
        stats = self._load_stats()
        return stats['monthly_stats']

    def get_overview_old(self):
        """获取统计概览"""
        db = get_db()
        now = datetime.now()
        start_date = (now - timedelta(days=7)).isoformat()  # 默认显示一周数据
        
        # 获取任务完成统计
        task_stats = db.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN status = 'abandoned' THEN 1 ELSE 0 END) as abandoned
            FROM tasks
            WHERE created_at >= ?
        ''', (start_date,)).fetchone()
        
        # 获取专注时间统计
        focus_stats = db.execute('''
            SELECT 
                AVG(focus_time) as average,
                SUM(focus_time) as total
            FROM pomodoros
            WHERE start_time >= ?
        ''', (start_date,)).fetchone()
        
        # 获取休息时间统计
        rest_stats = db.execute('''
            SELECT 
                AVG(rest_time) as average,
                SUM(rest_time) as total
            FROM pomodoros
            WHERE start_time >= ?
        ''', (start_date,)).fetchone()
        
        # 计算趋势（与上一个时间段比较）
        prev_start_date = (datetime.fromisoformat(start_date) - timedelta(days=7)).isoformat()
        prev_focus_stats = db.execute('''
            SELECT AVG(focus_time) as average
            FROM pomodoros
            WHERE start_time >= ? AND start_time < ?
        ''', (prev_start_date, start_date)).fetchone()
        
        prev_rest_stats = db.execute('''
            SELECT AVG(rest_time) as average
            FROM pomodoros
            WHERE start_time >= ? AND start_time < ?
        ''', (prev_start_date, start_date)).fetchone()
        
        # 计算趋势百分比
        focus_trend = 0
        if prev_focus_stats['average']:
            focus_trend = ((focus_stats['average'] or 0) - prev_focus_stats['average']) / prev_focus_stats['average'] * 100
        
        rest_trend = 0
        if prev_rest_stats['average']:
            rest_trend = ((rest_stats['average'] or 0) - prev_rest_stats['average']) / prev_rest_stats['average'] * 100
        
        return {
            'taskCompletion': {
                'total': task_stats['total'] or 0,
                'completed': task_stats['completed'] or 0,
                'inProgress': task_stats['in_progress'] or 0,
                'abandoned': task_stats['abandoned'] or 0
            },
            'focusTime': {
                'average': focus_stats['average'] or 0,
                'total': focus_stats['total'] or 0,
                'trend': focus_trend
            },
            'restTime': {
                'average': rest_stats['average'] or 0,
                'total': rest_stats['total'] or 0,
                'trend': rest_trend
            }
        }

    def get_task_statistics(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """获取任务统计信息"""
        try:
            tasks = self.task_service.get_tasks()
            
            # 如果没有指定日期范围，默认使用最近30天
            if not start_date:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
            
            # 过滤日期范围内的任务
            filtered_tasks = [
                task for task in tasks
                if start_date <= task.created_at <= end_date
            ]
            
            # 计算基本统计信息
            total_tasks = len(filtered_tasks)
            completed_tasks = len([t for t in filtered_tasks if t.status == 'completed'])
            abandoned_tasks = len([t for t in filtered_tasks if t.status == 'abandoned'])
            in_progress_tasks = len([t for t in filtered_tasks if t.status == 'in_progress'])
            
            # 计算完成率
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            # 计算平均完成时间
            completed_tasks_with_time = [
                t for t in filtered_tasks
                if t.status == 'completed' and t.actual_time
            ]
            avg_completion_time = sum(t.actual_time for t in completed_tasks_with_time) / len(completed_tasks_with_time) if completed_tasks_with_time else 0
            
            # 按优先级统计
            priority_stats = {
                '高': len([t for t in filtered_tasks if t.priority == '高']),
                '中': len([t for t in filtered_tasks if t.priority == '中']),
                '低': len([t for t in filtered_tasks if t.priority == '低'])
            }
            
            # 按标签统计
            tag_stats = {}
            for task in filtered_tasks:
                for tag in task.tags:
                    tag_stats[tag] = tag_stats.get(tag, 0) + 1
            
            # 按地点统计
            location_stats = {}
            for task in filtered_tasks:
                if task.location:
                    location_stats[task.location] = location_stats.get(task.location, 0) + 1
            
            # 按日期统计
            daily_stats = {}
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                daily_tasks = [
                    t for t in filtered_tasks
                    if t.created_at.strftime('%Y-%m-%d') == date_str
                ]
                daily_stats[date_str] = {
                    'total': len(daily_tasks),
                    'completed': len([t for t in daily_tasks if t.status == 'completed']),
                    'abandoned': len([t for t in daily_tasks if t.status == 'abandoned']),
                    'in_progress': len([t for t in daily_tasks if t.status == 'in_progress'])
                }
                current_date += timedelta(days=1)
            
            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'abandoned_tasks': abandoned_tasks,
                'in_progress_tasks': in_progress_tasks,
                'completion_rate': round(completion_rate, 2),
                'avg_completion_time': round(avg_completion_time, 2),
                'priority_stats': priority_stats,
                'tag_stats': tag_stats,
                'location_stats': location_stats,
                'daily_stats': daily_stats
            }
        except Exception as e:
            raise Exception(f"获取任务统计失败: {str(e)}")

    def get_task_trends(self, days: int = 30) -> Dict[str, List[Any]]:
        """获取任务趋势数据"""
        try:
            if days <= 0:
                raise ValueError("天数必须大于0")
                
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            tasks = self.task_service.get_tasks()
            filtered_tasks = [
                task for task in tasks
                if start_date <= task.created_at <= end_date
            ]
            
            # 准备趋势数据
            dates = []
            created_tasks = []
            completed_tasks = []
            abandoned_tasks = []
            
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                dates.append(date_str)
                
                daily_tasks = [
                    t for t in filtered_tasks
                    if t.created_at.strftime('%Y-%m-%d') == date_str
                ]
                
                created_tasks.append(len(daily_tasks))
                completed_tasks.append(len([t for t in daily_tasks if t.status == 'completed']))
                abandoned_tasks.append(len([t for t in daily_tasks if t.status == 'abandoned']))
                
                current_date += timedelta(days=1)
            
            return {
                'dates': dates,
                'created_tasks': created_tasks,
                'completed_tasks': completed_tasks,
                'abandoned_tasks': abandoned_tasks
            }
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"获取任务趋势失败: {str(e)}")

    def get_task_analysis(self) -> Dict[str, Any]:
        """获取任务分析报告"""
        try:
            tasks = self.task_service.get_tasks()
            
            # 计算任务完成时间分布
            completion_times = [
                t.actual_time for t in tasks
                if t.status == 'completed' and t.actual_time
            ]
            
            time_distribution = {
                '0-30分钟': len([t for t in completion_times if t <= 30]),
                '30-60分钟': len([t for t in completion_times if 30 < t <= 60]),
                '1-2小时': len([t for t in completion_times if 60 < t <= 120]),
                '2-4小时': len([t for t in completion_times if 120 < t <= 240]),
                '4小时以上': len([t for t in completion_times if t > 240])
            }
            
            # 计算最常使用的标签
            tag_usage = {}
            for task in tasks:
                for tag in task.tags:
                    tag_usage[tag] = tag_usage.get(tag, 0) + 1
            
            most_used_tags = dict(sorted(
                tag_usage.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5])
            
            # 计算最常使用的地点
            location_usage = {}
            for task in tasks:
                if task.location:
                    location_usage[task.location] = location_usage.get(task.location, 0) + 1
            
            most_used_locations = dict(sorted(
                location_usage.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5])
            
            # 计算任务完成率趋势
            completion_trends = []
            current_date = datetime.now() - timedelta(days=30)
            while current_date <= datetime.now():
                date_str = current_date.strftime('%Y-%m-%d')
                daily_tasks = [
                    t for t in tasks
                    if t.created_at.strftime('%Y-%m-%d') == date_str
                ]
                
                if daily_tasks:
                    completion_rate = len([t for t in daily_tasks if t.status == 'completed']) / len(daily_tasks) * 100
                    completion_trends.append({
                        'date': date_str,
                        'rate': round(completion_rate, 2)
                    })
                
                current_date += timedelta(days=1)
            
            return {
                'time_distribution': time_distribution,
                'most_used_tags': most_used_tags,
                'most_used_locations': most_used_locations,
                'completion_trends': completion_trends
            }
        except Exception as e:
            raise Exception(f"获取任务分析失败: {str(e)}") 