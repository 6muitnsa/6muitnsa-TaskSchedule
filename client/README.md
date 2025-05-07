# TaskSchedule 客户端

## 项目简介
TaskSchedule 是一个任务调度系统客户端，提供 Web 界面来管理和监控任务。系统采用前后端分离架构，支持任务配置和监控。通过 Cloudflare Tunnel 提供安全的远程访问能力。

## 功能特性
- 任务管理：创建、编辑、删除和监控任务
- 远程控制：支持远程命令执行和状态监控
- 系统设置：系统配置管理
- 数据同步：任务状态和配置同步
- 远程访问：通过 Cloudflare Tunnel 提供安全的远程访问

## 技术栈
- 前端：Vue.js + Vite
- 后端：Flask + SQLite
- 远程访问：cloudflared

**没有TypeScript部分！！没有TS部分！！**

## 项目结构
```
client/
├── api/             # 后端程序（可独立运行，就是说import路径里不要出现“api.”或者“..”之类前缀，api就是根目录了）
│   ├── models/      # 数据模型
│   ├── routes/      # API路由
│   ├── services/    # 业务逻辑
│   └── data/        # SQLite数据库
├── config/          # 配置文件（前后端统一配置文件，Flask配置，数据库配置，用户设置等等需要持久化的文件或配置）
├── logs/            # 日志文件（前后端统一日志文件，存放各种log。分文件夹存放前后端以及cloudflared的重定向输出文件）
├── ui/              # Vue.js前端代码（可部分独立运行，ui即前端部分根目录）
├── utils/           # 工具软件（cloudflared）
├── serve.py         # 一键启动脚本，用于读取全局配置，指定端口等（外部脚本，并非前或后端的一部分。client为根目录）
└── requirements.txt # Python依赖
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 14+
- npm 6+
- cloudflared（用于远程访问）

### 安装步骤
1. 安装后端依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 安装前端依赖：
   ```bash
   cd ui
   npm install
   ```
3. 安装 cloudflared：
   - Windows: 从 [Cloudflare 官网](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/) 下载安装
   - Linux: 
     ```bash
     curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
     sudo dpkg -i cloudflared.deb
     ```

### 启动服务
```bash
python serve.py
```

### 配置说明
- 环境变量配置：`.env` 文件
- 系统配置：`config/` 目录
- Cloudflare Tunnel 配置：参考 [Cloudflare 文档](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

## 开发说明
- 前端开发：`cd ui && npm run dev`
- 后端开发：`python app.py --debug`

## 开源声明
本项目使用以下开源组件：
- [Cloudflare Tunnel](https://github.com/cloudflare/cloudflared) - Apache License 2.0
- [Flask](https://github.com/pallets/flask) - BSD License
- [Vue.js](https://github.com/vuejs/vue) - MIT License
- [schedule](https://github.com/dbader/schedule) - MIT License

## 许可证
MIT License