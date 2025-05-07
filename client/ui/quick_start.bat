@echo off
chcp 65001

echo 正在启动开发服务器...
set NODE_ENV=development
set VITE_MODE=development
call npm run dev
if errorlevel 1 (
    echo 开发服务器启动失败！
    pause
    exit /b 1
) 