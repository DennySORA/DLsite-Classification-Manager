# DLsite Classification Manager

语言 Languages: [English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

一款高性能的 DLsite 作品分类与管理工具，提供 FastAPI 后端与 Nuxt 3 Web UI。

## 🌟 功能特性

- 异步爬虫与文件处理
- 交互式 CLI 流程：分类、更新、校验、归档
- FastAPI REST API：搜索、筛选、分页与完整元数据
- Nuxt 3 UI：浏览、评分、收藏
- 公司 ARCHIVE 工具：抓取公司全量作品元数据
- 以 `.tag` 文件存储，无需数据库

## 🛠️ 系统要求

- Python 3.10+
- Node.js 18+
- uv
- Yarn（或 npm/pnpm）

## 📦 安装

### 后端

```
uv venv
source .venv/bin/activate
uv sync
```

### 前端

```
cd dlsite_classification_web
yarn install
```

## 🚀 使用方法

### CLI（交互式）

```
uv run python main.py
```

### API 服务器

```
uv run python server.py
```

自定义数据路径 / 主机 / 端口：

```
uv run python server.py --data-path /path/to/your/dlsite/data --host 0.0.0.0 --port 8001
```

也可通过环境变量指定数据路径：

```
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
```

### 前端

```
cd dlsite_classification_web
yarn dev
```

访问 `http://localhost:3000`（若 3000 被占用则为 `http://localhost:3001`）。
前端默认连接 `http://localhost:8001` API。

## 🔧 数据路径优先级

1) `--data-path`
2) `DLSITE_DATA_PATH`
3) 默认路径（依次检查）
   - `./test_game_info`
   - `/mnt/d/R18/DLsite`
   - `./data`

## 📡 API 端点

- `GET /` / `GET /status`
- `GET /works`（搜索、筛选、排序、分页）
- `GET /work/{code}`
- `GET /companies` / `GET /companies/list`
- `GET /company/{company_id}/works-status`
- `POST /company/{company_id}/archive`
- `GET /company/{company_id}/archive-info`
- `GET /genres` / `GET /work-formats` / `GET /file-formats`
- `GET /collections`
- `POST /work/{code}/user-data`
- `GET /image?path=<url-encoded-path>`
- `GET /scan`

Swagger UI：`http://localhost:8001/docs`

## 📊 数据格式

```
[社团名称]_[社团ID]/
├── [作品ID]_[社团名称]_[社团ID] 作品标题/
│   └── [作品ID]_info/
│       ├── [作品ID]_img_main.jpg
│       ├── [作品ID]_img_smp1.jpg
│       ├── code.tag
│       ├── title.tag
│       ├── company.tag
│       └── ... 其他标签文件
└── ARCHIVE/
    └── RJ123456_info/
        ├── title.tag
        └── ... 归档信息
```

## 🧪 开发

```
uv run ruff check --fix .
uv run ruff format .
uv run mypy .
./run_tests.sh
```

若在 WSL 出现 "bad interpreter"：

```
sed -i 's/\r$//' run_tests.sh && chmod +x run_tests.sh
```

## 📸 Web 界面预览

![Web Demo 1](doc/1.png)
![Web Demo 2](doc/2.png)
![Web Demo 3](doc/3.png)
![Web Demo 4](doc/4.png)

## 🔗 链接

- 项目主页：https://github.com/DennySORA/DLsite-Classification-Manager
- 问题反馈：https://github.com/DennySORA/DLsite-Classification-Manager/issues
- 许可证：LICENSE
