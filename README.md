# DLsite Classification Manager

Languages: [English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

A high-performance DLsite works classifier and collection manager with a FastAPI
backend and a Nuxt 3 web UI.

## 🌟 Features

- Async crawler and file processing
- Interactive CLI workflows: classify, update, validate, archive
- FastAPI REST API with search, filters, pagination, and metadata
- Nuxt 3 UI for browsing, ratings, and collections
- Company archive tools to fetch full catalogs
- Tag-file storage (`*.tag`) with no database requirement

## 🛠️ Requirements

- Python 3.10+
- Node.js 18+
- uv
- Yarn (or npm/pnpm)

## 📦 Installation

### Backend

```
uv venv
source .venv/bin/activate
uv sync
```

### Frontend

```
cd dlsite_classification_web
yarn install
```

## 🚀 Usage

### CLI (interactive)

```
uv run python main.py
```

### API server

```
uv run python server.py
```

Custom data path / host / port:

```
uv run python server.py --data-path /path/to/your/dlsite/data --host 0.0.0.0 --port 8001
```

Set `DLSITE_DATA_PATH` to pin the data directory:

```
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
```

### Frontend

```
cd dlsite_classification_web
yarn dev
```

Open `http://localhost:3000` (or `http://localhost:3001` if 3000 is taken).
The UI expects the API at `http://localhost:8001`.

## 🔧 Data Path Priority

1) `--data-path`
2) `DLSITE_DATA_PATH`
3) Defaults (first existing):
   - `./test_game_info`
   - `/mnt/d/R18/DLsite`
   - `./data`

## 📡 API Endpoints

- `GET /` / `GET /status`
- `GET /works` (search, filter, sort, paginate)
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

Swagger UI: `http://localhost:8001/docs`

## 📊 Data Format

```
[CompanyName]_[CompanyID]/
├── [WorkID]_[CompanyName]_[CompanyID] Work Title/
│   └── [WorkID]_info/
│       ├── [WorkID]_img_main.jpg
│       ├── [WorkID]_img_smp1.jpg
│       ├── code.tag
│       ├── title.tag
│       ├── company.tag
│       └── ... other tag files
└── ARCHIVE/
    └── RJ123456_info/
        ├── title.tag
        └── ... archived metadata
```

## 🧪 Development

```
uv run ruff check --fix .
uv run ruff format .
uv run mypy .
./run_tests.sh
```

If you see a WSL "bad interpreter" error:

```
sed -i 's/\r$//' run_tests.sh && chmod +x run_tests.sh
```

## 📸 Web UI Preview

![Web Demo 1](doc/1.png)
![Web Demo 2](doc/2.png)
![Web Demo 3](doc/3.png)
![Web Demo 4](doc/4.png)

## 🔗 Links

- Project Home: https://github.com/DennySORA/DLsite-Classification-Manager
- Issues: https://github.com/DennySORA/DLsite-Classification-Manager/issues
- License: LICENSE
