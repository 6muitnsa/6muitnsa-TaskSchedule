import os
import sys
import json
import subprocess
import webbrowser
from threading import Thread
import time
from pathlib import Path
import logging
from datetime import datetime
import yaml  # 添加yaml导入

# 配置日志
def setup_logging():
    """配置日志"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f'serve_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def load_config():
    """加载配置文件"""
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config', 'config.yaml')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"配置文件不存在: {config_path}")
        raise

def process_output(process, prefix):
    """处理进程输出"""
    while True:
        try:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                logging.info(f"[{prefix}] {output.strip()}")
        except UnicodeDecodeError:
            # 如果遇到编码错误，尝试使用不同的编码
            try:
                output = process.stdout.buffer.readline().decode('utf-8')
                if output:
                    logging.info(f"[{prefix}] {output.strip()}")
            except Exception as e:
                logging.error(f"[{prefix}] 输出解码错误: {str(e)}")

def process_error(process, prefix):
    """处理进程错误"""
    while True:
        try:
            error = process.stderr.readline()
            if error == '' and process.poll() is not None:
                break
            if error:
                logging.error(f"[{prefix}] {error.strip()}")
        except UnicodeDecodeError:
            # 如果遇到编码错误，尝试使用不同的编码
            try:
                error = process.stderr.buffer.readline().decode('utf-8')
                if error:
                    logging.error(f"[{prefix}] {error.strip()}")
            except Exception as e:
                logging.error(f"[{prefix}] 错误输出解码错误: {str(e)}")

def start_backend():
    """启动后端服务"""
    logging.info("启动后端服务...")
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    api_path = os.path.join(script_dir, 'api', 'app.py')
    
    backend_process = subprocess.Popen(
        [sys.executable, api_path],  # 使用绝对路径
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
        encoding='utf-8'  # 指定编码
    )
    
    # 启动输出处理线程
    Thread(target=process_output, args=(backend_process, "后端"), daemon=True).start()
    Thread(target=process_error, args=(backend_process, "后端"), daemon=True).start()
    
    return backend_process

def start_frontend():
    """启动前端服务"""
    logging.info("启动前端服务...")
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(script_dir, 'ui')
    
    frontend_process = subprocess.Popen(
        f'cd "{ui_path}" && set NODE_OPTIONS=--trace-deprecation && npm run dev',  # 使用绝对路径
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
        shell=True,  # Windows 下需要 shell=True
        encoding='utf-8'  # 指定编码
    )
    
    # 启动输出处理线程
    Thread(target=process_output, args=(frontend_process, "前端"), daemon=True).start()
    Thread(target=process_error, args=(frontend_process, "前端"), daemon=True).start()
    
    return frontend_process

def open_browser():
    """打开浏览器"""
    config = load_config()
    time.sleep(2)  # 等待服务启动
    url = f"http://{config['frontend']['host']}:{config['frontend']['port']}"
    logging.info(f"正在打开浏览器: {url}")
    webbrowser.open(url)

def main():
    """主函数"""
    logger = setup_logging()
    logger.info("服务启动器开始运行")
    
    try:
        # 启动后端
        backend_process = start_backend()
        
        # 启动前端
        frontend_process = start_frontend()
        
        # 打开浏览器
        open_browser()
        
        # 等待进程结束
        while True:
            # 检查后端进程
            if backend_process.poll() is not None:
                logger.error("后端服务已停止")
                break
                
            # 检查前端进程
            if frontend_process.poll() is not None:
                logger.error("前端服务已停止")
                break
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("\n正在停止服务...")
        backend_process.terminate()
        frontend_process.terminate()
        logger.info("服务已停止")
    except Exception as e:
        logger.error(f"发生错误: {str(e)}", exc_info=True)
        if 'backend_process' in locals():
            backend_process.terminate()
        if 'frontend_process' in locals():
            frontend_process.terminate()

if __name__ == '__main__':
    main() 