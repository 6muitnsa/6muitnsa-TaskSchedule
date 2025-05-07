from flask import Blueprint, request, jsonify
from database import get_db
from datetime import datetime

bp = Blueprint('pomodoros', __name__)

@bp.route('/', methods=['GET'])
def get_pomodoros():
    db = get_db()
    task_id = request.args.get('taskId')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    
    query = 'SELECT * FROM pomodoros WHERE 1=1'
    params = []
    
    if task_id:
        query += ' AND task_id = ?'
        params.append(task_id)
    if start_date:
        query += ' AND start_time >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND end_time <= ?'
        params.append(end_date)
    
    pomodoros = db.execute(query, params).fetchall()
    return jsonify({
        'code': 200,
        'data': [dict(pomodoro) for pomodoro in pomodoros],
        'message': '获取番茄钟记录成功'
    })

@bp.route('/', methods=['POST'])
def create_pomodoro():
    data = request.get_json()
    db = get_db()
    
    cursor = db.execute('''
        INSERT INTO pomodoros (
            task_id, focus_time, rest_time,
            start_time, end_time, status
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['taskId'],
        data['focusTime'],
        data['restTime'],
        data['startTime'],
        data['endTime'],
        data['status']
    ))
    db.commit()
    
    return jsonify({
        'code': 200,
        'data': {
            'id': cursor.lastrowid,
            'status': data['status']
        },
        'message': '创建番茄钟记录成功'
    })

@bp.route('/<int:pomodoro_id>', methods=['DELETE'])
def delete_pomodoro(pomodoro_id):
    db = get_db()
    db.execute('DELETE FROM pomodoros WHERE id = ?', (pomodoro_id,))
    db.commit()
    
    return jsonify({
        'code': 200,
        'data': {
            'id': pomodoro_id,
            'status': 'deleted'
        },
        'message': '删除番茄钟记录成功'
    }) 