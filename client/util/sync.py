import os
import re
import subprocess
import qrcode
import base64
from io import BytesIO
from typing import Optional, Tuple

class SyncManager:
    def __init__(self, cloudflared_path: str, port: int = 3000):
        self.cloudflared_path = cloudflared_path
        self.port = port
        self.process: Optional[subprocess.Popen] = None
        self.url: Optional[str] = None
        self.qrcode: Optional[str] = None

    def start(self) -> Tuple[str, str]:
        """启动同步服务"""
        if self.process is not None:
            return self.url, self.qrcode

        # 启动 cloudflared
        cmd = f'"{self.cloudflared_path}" tunnel --url http://localhost:{self.port}'
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        # 等待并获取 URL
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            
            # 使用正则表达式匹配 URL
            match = re.search(r'https?://[a-z0-9-]+\.trycloudflare\.com(?=\s|$)', line)
            if match:
                self.url = match.group(0)
                # 生成二维码
                self.qrcode = self._generate_qrcode(self.url)
                break

        if not self.url:
            self.stop()
            raise Exception("无法获取同步地址")

        return self.url, self.qrcode

    def stop(self):
        """停止同步服务"""
        if self.process is not None:
            self.process.terminate()
            self.process = None
            self.url = None
            self.qrcode = None

    def get_status(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """获取同步状态"""
        is_running = self.process is not None and self.process.poll() is None
        return is_running, self.url, self.qrcode

    def _generate_qrcode(self, url: str) -> str:
        """生成二维码并转换为 base64 图片"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

# 创建全局同步管理器实例
sync_manager = SyncManager(
    cloudflared_path=os.path.join(os.path.dirname(__file__), 'Cloudflared', 'cloudflared-windows-386.exe')
) 