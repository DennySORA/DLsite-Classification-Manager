# DLsite Classification Manager

語言 Languages: [English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

一個高效能的 DLsite 作品分類和管理工具，具備現代化的 Web 界面和完整的 API 功能。

## 🌟 功能特色

- 高效率處理：使用 async/await 異步技術，提供高性能的爬蟲和文件處理
- 智能代碼提取：自動識別和提取 DLsite 作品代碼（RJ, BJ, VJ, RE, BE, VE）
- 完整元數據：自動獲取作品標題、公司、類型、圖片、介紹等完整資訊
- 現代化 Web 界面：基於 Nuxt.js 的響應式前端界面
- 強大的 API：提供 RESTful API 支援搜索、篩選、排序等功能
- 用戶收藏系統：支援個人評分和收藏分類功能
- 多種視圖模式：支援網格和列表兩種瀏覽模式
- 智能搜索：支援多欄位搜索和高級篩選

## 🛠️ 系統要求

- Python 3.8+
- Node.js 16+
- Yarn 或 npm

## 📦 安裝步驟

### 1. 下載專案
```
git clone https://github.com/your-username/dlsite-classification.git
cd dlsite-classification
```

### 2. 安裝後端依賴
```
pip install -r requirements.txt
```

### 3. 安裝前端依賴
```
cd dlsite_classification_web
yarn install
# 或 npm install
```

## 🚀 使用方法

### 啟動後端服務

1) 命令列分類工具（互動式 CLI）
```
python main.py
```

2) Web API 伺服器（port 8001）
```
# 預設設定
python server.py

# 指定資料夾路徑
python server.py --data-path /path/to/your/dlsite/data

# 自訂主機與埠號
python server.py --data-path ./test_game_info --port 8080 --host 127.0.0.1

# 使用環境變數
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

### 啟動前端介面

```
cd dlsite_classification_web

# 開發模式
yarn dev

# 正式模式
yarn build
yarn preview
```

開啟 `http://localhost:3000` 或 `http://localhost:3001` 觀看 Web 介面。

## 🎯 使用教學

### 基本分類流程

1) 準備資料夾：將 DLsite 作品資料夾放入指定目錄
2) 執行分類：執行 `python main.py` 並選擇分類選項
3) 檢視結果：透過 Web 介面瀏覽分類結果

### Web 介面功能

- 搜索：於搜索框輸入關鍵字尋找作品
- 篩選：依公司、類型、收藏等條件篩選
- 視圖切換：切換網格/列表視圖
- 作品詳情：點擊卡片查看詳情
- 評分收藏：於詳情頁設定個人評分與收藏分類

## 📸 Web 介面預覽

![Web Demo 1](doc/1.png)
![Web Demo 2](doc/2.png)
![Web Demo 3](doc/3.png)
![Web Demo 4](doc/4.png)

## 📊 資料格式

```
[公司名稱]_[公司ID]/
├── [作品ID]_[公司名稱]_[公司ID] 作品標題/
│   ├── [作品ID]_info/
│   │   ├── [作品ID]_img_main.jpg     # 主要圖片
│   │   ├── [作品ID]_img_smp1.jpg     # 範例圖片
│   │   ├── code.tag                  # 作品代碼
│   │   ├── title.tag                 # 作品標題
│   │   ├── company.tag               # 公司資訊
│   │   └── ... 其他標籤檔
```

## 🔧 設定選項

### 資料路徑設定（優先序）

1) 命令列參數（最高）
```
python server.py --data-path /path/to/your/dlsite/data
```

2) 環境變數
```
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

3) 預設路徑（依序檢查）
- `./test_game_info`
- `/mnt/d/R18/DLsite`
- `./data`

### 伺服器設定

```
# 自訂埠號
python server.py --port 8080

# 自訂主機
python server.py --host 127.0.0.1

# 完整設定
python server.py --data-path ./data --port 8080 --host 0.0.0.0
```

### 命令列參數

- `--data-path, -d`：資料夾路徑
- `--port, -p`：伺服器埠號（預設 8001）
- `--host`：伺服器主機（預設 0.0.0.0）
- `--help`：說明

## 📡 API 端點

- `GET /works`
- `GET /work/{code}`
- `GET /companies`
- `GET /genres`
- `POST /work/{code}/user-data`
- `GET /image?path=<path>`

## 🔗 連結

- 專案首頁：https://github.com/your-username/dlsite-classification
- 問題回報：https://github.com/your-username/dlsite-classification/issues
- 授權條款：LICENSE

## 🤝 貢獻

歡迎提交 Pull Request 與 Issue！

## 📄 授權

MIT License — 詳見 `LICENSE`。

