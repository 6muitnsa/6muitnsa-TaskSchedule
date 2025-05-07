import os
import time
import tempfile
import subprocess
from pathlib import Path
import logging
import psutil
import yaml

# 读取配置文件
config_path = Path(__file__).parent.parent.parent / 'config' / 'config.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(config['logging']['level'])

class CloudflaredManager:
    def __init__(self):
        self.tunnels = {}  # 存储活动的隧道信息
        self.cloudflared_path = self._get_cloudflared_path()
    
    def _get_cloudflared_path(self):
        """获取 cloudflared 可执行文件路径"""
        base_path = Path(__file__).parent.parent.parent
        cloudflared_path = base_path / config['remote']['cloudflared_path']
        if not cloudflared_path.exists():
            raise FileNotFoundError(f"找不到 cloudflared 可执行文件: {cloudflared_path}")
        return str(cloudflared_path)
    
    def start_tunnel(self, tunnel_id, port):
        """启动 cloudflared 隧道"""
        if tunnel_id in self.tunnels:
            raise ValueError(f"隧道 {tunnel_id} 已经在运行")
        
        # 创建临时文件用于重定向输出
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=config['remote']['temp_file_suffix']
        )
        temp_file.close()
        
        try:
            # 使用简单的 cloudflared 命令
            cmd = f'"{self.cloudflared_path}" tunnel --url http://localhost:{port} > "{temp_file.name}" 2>&1'
            
            # 启动进程
            process = subprocess.Popen(cmd, shell=True)
            
            # 等待隧道启动
            time.sleep(config['remote']['tunnel_wait_time'])
            
            # 读取输出文件
            with open(temp_file.name, 'r', encoding='utf-8') as f:
                output = f.read()
            
            # 解析 URL
            import re
            url_match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', output)
            if not url_match:
                raise ValueError("无法获取 cloudflared URL")
            
            url = url_match.group(0)
            
            # 保存隧道信息
            self.tunnels[tunnel_id] = {
                'process': process,
                'temp_file': temp_file.name,
                'url': url,
                'pid': process.pid
            }
            
            return url
            
        except Exception as e:
            # 清理临时文件
            if os.path.exists(temp_file.name):
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            raise e
    
    def stop_tunnel(self, tunnel_id):
        """停止 cloudflared 隧道"""
        if tunnel_id not in self.tunnels:
            logger.warning(f"尝试停止不存在的隧道 {tunnel_id}")
            return
        
        tunnel = self.tunnels[tunnel_id]
        logger.info(f"正在停止隧道 {tunnel_id}")
        
        try:
            # 使用 psutil 终止进程及其子进程
            try:
                parent = psutil.Process(tunnel['pid'])
                children = parent.children(recursive=True)
                
                # 先终止子进程
                for child in children:
                    try:
                        child.terminate()
                        logger.debug(f"已终止子进程 {child.pid}")
                    except psutil.NoSuchProcess:
                        pass
                
                # 等待子进程终止
                gone, alive = psutil.wait_procs(children, timeout=3)
                for p in alive:
                    try:
                        p.kill()
                        logger.debug(f"已强制终止子进程 {p.pid}")
                    except psutil.NoSuchProcess:
                        pass
                
                # 终止父进程
                try:
                    parent.terminate()
                    logger.debug(f"已终止父进程 {parent.pid}")
                except psutil.NoSuchProcess:
                    pass
                
                # 等待父进程终止
                gone, alive = psutil.wait_procs([parent], timeout=3)
                for p in alive:
                    try:
                        p.kill()
                        logger.debug(f"已强制终止父进程 {p.pid}")
                    except psutil.NoSuchProcess:
                        pass
                        
            except psutil.NoSuchProcess:
                logger.warning(f"进程 {tunnel['pid']} 不存在")
            
            # 清理临时文件
            if os.path.exists(tunnel['temp_file']):
                try:
                    os.unlink(tunnel['temp_file'])
                    logger.debug(f"已删除临时文件 {tunnel['temp_file']}")
                except Exception as e:
                    logger.warning(f"删除临时文件失败: {e}")
            
            # 移除隧道信息
            del self.tunnels[tunnel_id]
            logger.info(f"隧道 {tunnel_id} 已停止")
            
        except Exception as e:
            logger.error(f"停止隧道 {tunnel_id} 时出错: {e}")
            raise
    
    def get_tunnel_url(self, tunnel_id):
        """获取隧道 URL"""
        if tunnel_id not in self.tunnels:
            raise ValueError(f"找不到隧道 {tunnel_id}")
        return self.tunnels[tunnel_id]['url']
    
    def __del__(self):
        """清理所有隧道"""
        for tunnel_id in list(self.tunnels.keys()):
            try:
                self.stop_tunnel(tunnel_id)
            except Exception as e:
                logger.error(f"清理隧道 {tunnel_id} 时出错: {e}") 