import schedule
import time
import threading
import requests
from datetime import datetime

def check_reminders():
    """检查并触发提醒"""
    try:
        response = requests.post('http://localhost:5000/api/reminders/check')
        if response.status_code == 200:
            print(f"[{datetime.now()}] 提醒检查完成")
        else:
            print(f"[{datetime.now()}] 提醒检查失败: {response.text}")
    except Exception as e:
        print(f"[{datetime.now()}] 提醒检查出错: {str(e)}")

def run_scheduler():
    """运行调度器"""
    # 每分钟检查一次提醒
    schedule.every(1).minutes.do(check_reminders)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_reminder_checker():
    """启动提醒检查器"""
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()
    print(f"[{datetime.now()}] 提醒检查器已启动") 