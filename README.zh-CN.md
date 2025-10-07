# DLsite Classification Manager

语言 Languages: [English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

一款高性能的 DLsite 作品分类与管理工具，提供现代化 Web 界面与完整 API。

## 🌟 功能特性

- 高效处理：基于 async/await 的高性能爬虫与文件处理
- 智能代码提取：自动识别提取 DLsite 作品代码（RJ, BJ, VJ, RE, BE, VE）
- 完整元数据：自动获取标题、社团、类型、图片、简介等信息
- 现代化 Web 界面：基于 Nuxt.js 的响应式前端
- 强大 API：RESTful API 支持搜索、筛选、排序等
- 用户收藏系统：支持个人评分与收藏分类
- 多种视图模式：网格与列表浏览
- 智能搜索：多字段搜索与高级筛选

## 🛠️ 系统要求

- Python 3.8+
- Node.js 16+
- Yarn 或 npm

## 📦 安装步骤

### 1. 克隆项目
```
git clone https://github.com/your-username/dlsite-classification.git
cd dlsite-classification
```

### 2. 安装后端依赖
```
pip install -r requirements.txt
```

### 3. 安装前端依赖
```
cd dlsite_classification_web
yarn install
# 或 npm install
```

## 🚀 使用方法

### 启动后端服务

1) 命令行分类工具（交互式 CLI）
```
python main.py
```

2) Web API 服务器（端口 8001）
```
# 默认设置
python server.py

# 指定数据目录
python server.py --data-path /path/to/your/dlsite/data

# 自定义主机与端口
python server.py --data-path ./test_game_info --port 8080 --host 127.0.0.1

# 使用环境变量
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

### 启动前端界面

```
cd dlsite_classification_web

# 开发模式
yarn dev

# 生产模式
yarn build
yarn preview
```

访问 `http://localhost:3000` 或 `http://localhost:3001` 查看 Web 界面。

## 🎯 使用教程

### 基本分类流程

1) 准备数据：将 DLsite 作品文件夹放入指定目录
2) 运行分类：执行 `python main.py` 并选择分类选项
3) 查看结果：通过 Web 界面浏览分类结果

### Web 界面功能

- 搜索：在搜索框输入关键字查找作品
- 筛选：按社团、类型、收藏等条件筛选
- 视图切换：切换网格/列表视图
- 作品详情：点击卡片查看详细信息
- 评分收藏：在详情页设置个人评分与收藏分类

## 📸 Web 界面预览

![Web Demo 1](doc/1.png)
![Web Demo 2](doc/2.png)
![Web Demo 3](doc/3.png)
![Web Demo 4](doc/4.png)

## 📊 数据格式

```
[社团名称]_[社团ID]/
├── [作品ID]_[社团名称]_[社团ID] 作品标题/
│   ├── [作品ID]_info/
│   │   ├── [作品ID]_img_main.jpg     # 主图
│   │   ├── [作品ID]_img_smp1.jpg     # 示例图
│   │   ├── code.tag                  # 作品代码
│   │   ├── title.tag                 # 作品标题
│   │   ├── company.tag               # 社团信息
│   │   └── ... 其他标签文件
```

## 🔧 配置选项

### 数据路径配置（优先级）

1) 命令行参数（最高）
```
python server.py --data-path /path/to/your/dlsite/data
```

2) 环境变量
```
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

3) 默认路径（依次检查）
- `./test_game_info`
- `/mnt/d/R18/DLsite`
- `./data`

### 服务器配置

```
# 自定义端口
python server.py --port 8080

# 自定义主机
python server.py --host 127.0.0.1

# 完整配置
python server.py --data-path ./data --port 8080 --host 0.0.0.0
```

### 命令行参数

- `--data-path, -d`：数据目录
- `--port, -p`：服务器端口（默认 8001）
- `--host`：服务器主机（默认 0.0.0.0）
- `--help`：帮助

## 📡 API 端点

- `GET /works`
- `GET /work/{code}`
- `GET /companies`
- `GET /genres`
- `POST /work/{code}/user-data`
- `GET /image?path=<path>`

## 🔗 链接

- 项目主页：https://github.com/your-username/dlsite-classification
- 问题反馈：https://github.com/your-username/dlsite-classification/issues
- 许可证：LICENSE

## 🤝 贡献

欢迎提交 Pull Request 与 Issue！

## 📄 许可证

MIT License — 详见 `LICENSE`。

