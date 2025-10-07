# DLsite Classification Manager

Languages: [English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

A high-performance DLsite work classification and management tool with a modern Web UI and complete API.

## 🌟 Features

- High-Performance Processing: async/await for efficient crawling and file processing
- Smart Code Extraction: auto-detects DLsite codes (RJ, BJ, VJ, RE, BE, VE)
- Complete Metadata: titles, circles, genres, images, descriptions, etc.
- Modern Web Interface: Nuxt.js-based responsive frontend
- Powerful API: RESTful API for search, filtering, sorting
- User Collections: personal ratings and collection categories
- Multiple Views: grid and list modes
- Intelligent Search: multi-field search with advanced filters

## 🛠️ Requirements

- Python 3.8+
- Node.js 16+
- Yarn or npm

## 📦 Installation

1) Clone
```
git clone https://github.com/your-username/dlsite-classification.git
cd dlsite-classification
```

2) Backend deps
```
pip install -r requirements.txt
```

3) Frontend deps
```
cd dlsite_classification_web
yarn install
# or npm install
```

## 🚀 Usage

### Start backend

1. CLI classifier (interactive)
```
python main.py
```

2. Web API server (port 8001)
```
# Default
python server.py

# Specify data path
python server.py --data-path /path/to/your/dlsite/data

# Custom host/port
python server.py --data-path ./test_game_info --port 8080 --host 127.0.0.1

# With environment variable
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

### Start frontend

```
cd dlsite_classification_web

# Dev
yarn dev

# Prod
yarn build
yarn preview
```

Open `http://localhost:3000` or `http://localhost:3001`.

## 🎯 How-To

### Basic flow

1) Prepare data folders
2) Run `python main.py` and choose options
3) Use the web UI to browse results

### Web UI features

- Search by keyword
- Filter by circle, genre, collection, etc.
- Toggle grid/list views
- View work details
- Set ratings and collections

## 📊 Data Format

```
[CircleName]_[CircleID]/
├── [WorkID]_[CircleName]_[CircleID] Work Title/
│   ├── [WorkID]_info/
│   │   ├── [WorkID]_img_main.jpg     # Main image
│   │   ├── [WorkID]_img_smp1.jpg     # Sample image
│   │   ├── code.tag                  # Work code
│   │   ├── title.tag                 # Work title
│   │   ├── company.tag               # Circle info
│   │   └── ... other tag files
```

## 🔧 Configuration

### Data path

Priority order:

1) Command line
```
python server.py --data-path /path/to/your/dlsite/data
```

2) Environment variable
```
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

3) Defaults (checked in order)
- `./test_game_info`
- `/mnt/d/R18/DLsite`
- `./data`

### Server

```
# Port
python server.py --port 8080

# Host
python server.py --host 127.0.0.1

# Full config
python server.py --data-path ./data --port 8080 --host 0.0.0.0
```

### CLI arguments

- `--data-path, -d`: Data folder path
- `--port, -p`: Server port (default 8001)
- `--host`: Server host (default 0.0.0.0)
- `--help`: Show help

## 📡 API Endpoints

- `GET /works`
- `GET /work/{code}`
- `GET /companies`
- `GET /genres`
- `POST /work/{code}/user-data`
- `GET /image?path=<path>`

## 🔗 Links

- Project Home: https://github.com/your-username/dlsite-classification
- Issues: https://github.com/your-username/dlsite-classification/issues
- License: LICENSE

## 🤝 Contributing

Pull Requests and Issues are welcome!

## 📄 License

MIT License — see `LICENSE`.
