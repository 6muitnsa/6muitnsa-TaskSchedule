from flask import jsonify

def success_response(data=None, message='success', code=200):
    """成功响应"""
    return jsonify({
        'code': code,
        'data': data,
        'message': message
    })

def error_response(message='error', code=400):
    """错误响应"""
    return jsonify({
        'code': code,
        'message': message
    }), code 