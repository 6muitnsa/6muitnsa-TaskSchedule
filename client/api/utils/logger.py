import logging
import os
from datetime import datetime

def setup_logger(name):
    """设置指定名称的日志记录器"""
    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 配置日志格式
    log_format = '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # 获取或创建指定名称的日志记录器
    logger = logging.getLogger(name)
    
    # 如果已经有处理器，说明已经配置过，直接返回
    if logger.handlers:
        return logger
        
    # 设置日志级别
    logger.setLevel(logging.DEBUG)
    
    # 创建文件处理器
    file_handler = logging.FileHandler(
        f'logs/{name}_{datetime.now().strftime("%Y%m%d")}.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    file_handler.setLevel(logging.DEBUG)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    console_handler.setLevel(logging.INFO)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name):
    """获取指定名称的日志记录器"""
    return setup_logger(name) 