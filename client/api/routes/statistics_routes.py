from flask import Blueprint, request, jsonify
from database import get_db
from datetime import datetime, timedelta
import json
from utils.response import success_response, error_response

bp = Blueprint('statistics', __name__)

def init_routes(statistics_service):
    """初始化路由，注入依赖"""
    @bp.route('/', methods=['GET'])
    def get_statistics():
        time_range = request.args.get('timeRange', 'week')
        metric = request.args.get('metric', 'completion')
        
        db = get_db()
        now = datetime.now()
        
        # 计算时间范围
        if time_range == 'week':
            start_date = (now - timedelta(days=7)).isoformat()
        elif time_range == 'month':
            start_date = (now - timedelta(days=30)).isoformat()
        else:  # year
            start_date = (now - timedelta(days=365)).isoformat()
        
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
        
        # 获取任务分布统计
        priority_dist = db.execute('''
            SELECT 
                priority,
                COUNT(*) as count
            FROM tasks
            WHERE created_at >= ?
            GROUP BY priority
        ''', (start_date,)).fetchall()
        
        tag_dist = db.execute('''
            SELECT 
                tags,
                COUNT(*) as count
            FROM tasks
            WHERE created_at >= ?
            GROUP BY tags
        ''', (start_date,)).fetchall()
        
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
        
        # 构建响应数据
        result = {
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
            },
            'taskDistribution': {
                'byPriority': {
                    row['priority']: row['count']
                    for row in priority_dist
                },
                'byTag': {
                    json.loads(row['tags'])[0] if row['tags'] else '无标签': row['count']
                    for row in tag_dist
                }
            }
        }
        
        return jsonify({
            'code': 200,
            'data': result,
            'message': '获取统计信息成功'
        })

    @bp.route('/overview', methods=['GET'])
    def get_overview():
        """获取统计概览数据"""
        try:
            overview = statistics_service.get_overview()
            return success_response(data=overview, message='获取统计概览成功')
        except Exception as e:
            return error_response(message=f'获取统计概览失败: {str(e)}')

    @bp.route('/tasks', methods=['GET'])
    def get_task_statistics():
        """获取任务统计信息"""
        try:
            # 获取日期范围参数
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            # 转换日期字符串为datetime对象
            if start_date:
                start_date = datetime.fromisoformat(start_date)
            if end_date:
                end_date = datetime.fromisoformat(end_date)
            
            # 获取统计信息
            statistics = statistics_service.get_task_statistics(start_date, end_date)
            return success_response(data=statistics, message='获取任务统计成功')
        except ValueError as e:
            return error_response(message=f'日期格式错误: {str(e)}')
        except Exception as e:
            return error_response(message=f'获取任务统计失败: {str(e)}')

    @bp.route('/trends', methods=['GET'])
    def get_task_trends():
        """获取任务趋势数据"""
        try:
            # 获取天数参数
            days = request.args.get('days', default=30, type=int)
            if days <= 0:
                return error_response(message='天数必须大于0')
            
            # 获取趋势数据
            trends = statistics_service.get_task_trends(days)
            return success_response(data=trends, message='获取任务趋势成功')
        except ValueError as e:
            return error_response(message=f'参数错误: {str(e)}')
        except Exception as e:
            return error_response(message=f'获取任务趋势失败: {str(e)}')

    @bp.route('/analysis', methods=['GET'])
    def get_task_analysis():
        """获取任务分析报告"""
        try:
            # 获取分析报告
            analysis = statistics_service.get_task_analysis()
            return success_response(data=analysis, message='获取任务分析成功')
        except Exception as e:
            return error_response(message=f'获取任务分析失败: {str(e)}') 