# DLsite Classification Manager

一個高效能的 DLsite 作品分類和管理工具，具備現代化的 Web 界面和完整的 API 功能。

## 📋 目錄 / 目次 / Table of Contents

- [中文說明](#中文說明)
- [日本語の説明](#日本語の説明)
- [English Documentation](#english-documentation)

---

## 中文說明

### 🌟 功能特色

- **高效率處理**: 使用 async/await 異步技術，提供高性能的爬蟲和文件處理
- **智能代碼提取**: 自動識別和提取 DLsite 作品代碼 (RJ, BJ, VJ, RE, BE, VE)
- **完整元數據**: 自動獲取作品標題、公司、類型、圖片、介紹等完整信息
- **現代化 Web 界面**: 基於 Nuxt.js 的響應式前端界面
- **強大的 API**: 提供 RESTful API 支持搜索、篩選、排序等功能
- **用戶收藏系統**: 支持個人評分和收藏分類功能
- **多種視圖模式**: 支持網格和列表兩種瀏覽模式
- **智能搜索**: 支持多字段搜索和高級篩選

### 🛠️ 系統要求

- Python 3.8+
- Node.js 16+
- Yarn 或 npm

### 📦 安裝步驟

#### 1. 克隆項目
```bash
git clone https://github.com/your-username/dlsite-classification.git
cd dlsite-classification
```

#### 2. 安裝 Python 依賴
```bash
pip install -r requirements.txt
```

#### 3. 安裝前端依賴
```bash
cd dlsite_classification_web
yarn install
# 或使用 npm install
```

### 🚀 使用方法

#### 啟動後端服務

1. **命令行分類工具**（互動式 CLI）
```bash
python main.py
```

2. **Web API 服務器**（port 8001）
```bash
# 使用預設設定
python server.py

# 指定資料夾路徑
python server.py --data-path /path/to/your/dlsite/data

# 自定義端口和主機
python server.py --data-path ./test_game_info --port 8080 --host 127.0.0.1

# 使用環境變數
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

#### 啟動前端界面

```bash
cd dlsite_classification_web

# 開發模式
yarn dev

# 生產模式
yarn build
yarn preview
```

訪問 `http://localhost:3000` 或 `http://localhost:3001` 查看 Web 界面。

### 🎯 使用教學

#### 基本分類流程

1. **準備數據**: 將 DLsite 作品文件夾放置在指定目錄
2. **運行分類**: 執行 `python main.py` 選擇相應的分類選項
3. **查看結果**: 使用 Web 界面瀏覽分類結果

#### Web 界面功能

- **搜索**: 在搜索框中輸入關鍵詞搜索作品
- **篩選**: 使用側邊欄按公司、類型、收藏等條件篩選
- **視圖切換**: 點擊右上角圖標切換網格/列表視圖
- **作品詳情**: 點擊作品卡片查看詳細信息
- **評分收藏**: 在作品詳情中設置個人評分和收藏分類

### 📊 數據格式

項目使用標準化的數據格式存儲作品信息：

```
[公司名稱]_[公司ID]/
├── [作品ID]_[公司名稱]_[公司ID] 作品標題/
│   ├── [作品ID]_info/
│   │   ├── [作品ID]_img_main.jpg     # 主要圖片
│   │   ├── [作品ID]_img_smp1.jpg     # 範例圖片
│   │   ├── code.tag                  # 作品代碼
│   │   ├── title.tag                 # 作品標題
│   │   ├── company.tag               # 公司資訊
│   │   └── ... 其他標籤文件
```

### 🔧 配置選項

#### 資料路徑設定

系統支持多種方式設定資料路徑，優先級如下：

1. **命令行參數**（優先級最高）
```bash
python server.py --data-path /path/to/your/dlsite/data
```

2. **環境變數**
```bash
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

3. **預設路徑**（按順序檢查）
   - `./test_game_info` - 測試數據
   - `/mnt/d/R18/DLsite` - 原始預設路徑
   - `./data` - 通用數據路徑

#### 伺服器設定

```bash
# 自定義端口
python server.py --port 8080

# 自定義主機
python server.py --host 127.0.0.1

# 完整配置
python server.py --data-path ./data --port 8080 --host 0.0.0.0
```

#### 命令行參數說明

- `--data-path, -d`: 指定資料夾路徑
- `--port, -p`: 指定伺服器端口（預設 8001）
- `--host`: 指定伺服器主機（預設 0.0.0.0）
- `--help`: 顯示說明

### 📡 API 端點

- `GET /works` - 獲取作品列表，支持搜索和篩選
- `GET /work/{code}` - 獲取特定作品詳情
- `GET /companies` - 獲取公司列表
- `GET /genres` - 獲取類型標籤
- `POST /work/{code}/user-data` - 更新用戶評分和收藏
- `GET /image?path=<path>` - 獲取圖片資源

### 🆘 常見問題

**Q: 分類後找不到作品？**
A: 確認數據路徑設置正確，並檢查文件夾命名是否包含正確的作品代碼。

**Q: Web 界面無法加載圖片？**
A: 確認後端服務已啟動，並檢查圖片文件路徑是否正確。

**Q: 如何添加新的作品？**
A: 將新作品按照標準格式放置在數據目錄中，然後運行重新掃描。

---

## 日本語の説明

### 🌟 機能特徴

- **高効率処理**: async/await非同期技術により、高性能なクローラーとファイル処理を提供
- **スマートコード抽出**: DLsite作品コード（RJ, BJ, VJ, RE, BE, VE）の自動識別・抽出
- **完全なメタデータ**: 作品タイトル、サークル、ジャンル、画像、紹介文などの完全な情報を自動取得
- **モダンなWebインターフェース**: Nuxt.jsベースのレスポンシブフロントエンドUI
- **強力なAPI**: 検索、フィルタリング、ソート機能をサポートするRESTful API
- **ユーザーコレクションシステム**: 個人評価とコレクション分類機能をサポート
- **複数のビューモード**: グリッドとリストの2つの表示モードをサポート
- **インテリジェント検索**: マルチフィールド検索と高度なフィルタリング

### 🛠️ システム要件

- Python 3.8+
- Node.js 16+
- Yarn または npm

### 📦 インストール手順

#### 1. プロジェクトのクローン
```bash
git clone https://github.com/your-username/dlsite-classification.git
cd dlsite-classification
```

#### 2. Python依存関係のインストール
```bash
pip install -r requirements.txt
```

#### 3. フロントエンド依存関係のインストール
```bash
cd dlsite_classification_web
yarn install
# または npm install
```

### 🚀 使用方法

#### バックエンドサービスの起動

1. **コマンドライン分類ツール**（インタラクティブCLI）
```bash
python main.py
```

2. **Web APIサーバー**（ポート8001）
```bash
# デフォルト設定を使用
python server.py

# データフォルダパスを指定
python server.py --data-path /path/to/your/dlsite/data

# カスタムポートとホスト
python server.py --data-path ./test_game_info --port 8080 --host 127.0.0.1

# 環境変数を使用
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

#### フロントエンドインターフェースの起動

```bash
cd dlsite_classification_web

# 開発モード
yarn dev

# 本番モード
yarn build
yarn preview
```

`http://localhost:3000` または `http://localhost:3001` でWebインターフェースにアクセス。

### 🎯 使用チュートリアル

#### 基本的な分類フロー

1. **データ準備**: DLsite作品フォルダを指定ディレクトリに配置
2. **分類実行**: `python main.py` を実行し、適切な分類オプションを選択
3. **結果確認**: Webインターフェースで分類結果を閲覧

#### Webインターフェース機能

- **検索**: 検索ボックスにキーワードを入力して作品を検索
- **フィルタリング**: サイドバーでサークル、ジャンル、コレクションなどの条件でフィルタリング
- **ビュー切り替え**: 右上のアイコンでグリッド/リストビューを切り替え
- **作品詳細**: 作品カードをクリックして詳細情報を表示
- **評価・コレクション**: 作品詳細で個人評価とコレクション分類を設定

### 📊 データ形式

プロジェクトは標準化されたデータ形式で作品情報を保存：

```
[サークル名]_[サークルID]/
├── [作品ID]_[サークル名]_[サークルID] 作品タイトル/
│   ├── [作品ID]_info/
│   │   ├── [作品ID]_img_main.jpg     # メイン画像
│   │   ├── [作品ID]_img_smp1.jpg     # サンプル画像
│   │   ├── code.tag                  # 作品コード
│   │   ├── title.tag                 # 作品タイトル
│   │   ├── company.tag               # サークル情報
│   │   └── ... その他のタグファイル
```

### 🔧 設定オプション

#### データパス設定

システムは複数の方法でデータパスを設定でき、優先順位は以下の通り：

1. **コマンドライン引数**（最高優先度）
```bash
python server.py --data-path /path/to/your/dlsite/data
```

2. **環境変数**
```bash
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

3. **デフォルトパス**（順番にチェック）
   - `./test_game_info` - テストデータ
   - `/mnt/d/R18/DLsite` - 元のデフォルトパス
   - `./data` - 一般的なデータパス

#### サーバー設定

```bash
# カスタムポート
python server.py --port 8080

# カスタムホスト
python server.py --host 127.0.0.1

# 完全な設定
python server.py --data-path ./data --port 8080 --host 0.0.0.0
```

#### コマンドライン引数説明

- `--data-path, -d`: データフォルダパスを指定
- `--port, -p`: サーバーポートを指定（デフォルト 8001）
- `--host`: サーバーホストを指定（デフォルト 0.0.0.0）
- `--help`: ヘルプを表示

### 📡 APIエンドポイント

- `GET /works` - 作品リストの取得、検索・フィルタリング対応
- `GET /work/{code}` - 特定作品の詳細取得
- `GET /companies` - サークルリスト取得
- `GET /genres` - ジャンルタグ取得
- `POST /work/{code}/user-data` - ユーザー評価・コレクション更新
- `GET /image?path=<path>` - 画像リソース取得

### 🆘 よくある質問

**Q: 分類後に作品が見つからない？**
A: データパスの設定が正しいか確認し、フォルダ名に正しい作品コードが含まれているかチェックしてください。

**Q: Webインターフェースで画像が読み込まれない？**
A: バックエンドサービスが起動していることを確認し、画像ファイルパスが正しいかチェックしてください。

**Q: 新しい作品を追加するには？**
A: 新しい作品を標準形式でデータディレクトリに配置し、再スキャンを実行してください。

---

## English Documentation

### 🌟 Features

- **High-Performance Processing**: Utilizes async/await technology for efficient crawling and file processing
- **Smart Code Extraction**: Automatically identifies and extracts DLsite work codes (RJ, BJ, VJ, RE, BE, VE)
- **Complete Metadata**: Automatically fetches work titles, companies, genres, images, descriptions, and more
- **Modern Web Interface**: Responsive frontend UI based on Nuxt.js
- **Powerful API**: RESTful API supporting search, filtering, sorting, and more
- **User Collection System**: Personal rating and collection categorization features
- **Multiple View Modes**: Grid and list view modes for browsing
- **Intelligent Search**: Multi-field search with advanced filtering capabilities

### 🛠️ System Requirements

- Python 3.8+
- Node.js 16+
- Yarn or npm

### 📦 Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/dlsite-classification.git
cd dlsite-classification
```

#### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Install Frontend Dependencies
```bash
cd dlsite_classification_web
yarn install
# or npm install
```

### 🚀 Usage

#### Start Backend Services

1. **Command Line Classification Tool** (Interactive CLI)
```bash
python main.py
```

2. **Web API Server** (port 8001)
```bash
# Use default settings
python server.py

# Specify data folder path
python server.py --data-path /path/to/your/dlsite/data

# Custom port and host
python server.py --data-path ./test_game_info --port 8080 --host 127.0.0.1

# Use environment variable
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

#### Start Frontend Interface

```bash
cd dlsite_classification_web

# Development mode
yarn dev

# Production mode
yarn build
yarn preview
```

Access the web interface at `http://localhost:3000` or `http://localhost:3001`.

### 🎯 Usage Tutorial

#### Basic Classification Workflow

1. **Prepare Data**: Place DLsite work folders in the designated directory
2. **Run Classification**: Execute `python main.py` and choose appropriate classification options
3. **View Results**: Browse classification results using the web interface

#### Web Interface Features

- **Search**: Enter keywords in the search box to find works
- **Filtering**: Use sidebar to filter by company, genre, collection, etc.
- **View Toggle**: Click the top-right icon to switch between grid/list views
- **Work Details**: Click work cards to view detailed information
- **Rating & Collection**: Set personal ratings and collection categories in work details

### 📊 Data Format

The project uses a standardized data format to store work information:

```
[Company Name]_[Company ID]/
├── [Work ID]_[Company Name]_[Company ID] Work Title/
│   ├── [Work ID]_info/
│   │   ├── [Work ID]_img_main.jpg     # Main image
│   │   ├── [Work ID]_img_smp1.jpg     # Sample image
│   │   ├── code.tag                   # Work code
│   │   ├── title.tag                  # Work title
│   │   ├── company.tag                # Company info
│   │   └── ... Other tag files
```

### 🔧 Configuration

#### Data Path Configuration

The system supports multiple ways to set the data path, with the following priority order:

1. **Command Line Arguments** (Highest Priority)
```bash
python server.py --data-path /path/to/your/dlsite/data
```

2. **Environment Variables**
```bash
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

3. **Default Paths** (Checked in order)
   - `./test_game_info` - Test data
   - `/mnt/d/R18/DLsite` - Original default path
   - `./data` - Common data path

#### Server Configuration

```bash
# Custom port
python server.py --port 8080

# Custom host
python server.py --host 127.0.0.1

# Complete configuration
python server.py --data-path ./data --port 8080 --host 0.0.0.0
```

#### Command Line Arguments

- `--data-path, -d`: Specify data folder path
- `--port, -p`: Specify server port (default 8001)
- `--host`: Specify server host (default 0.0.0.0)
- `--help`: Show help message

### 📡 API Endpoints

- `GET /works` - Get works list with search and filtering support
- `GET /work/{code}` - Get specific work details
- `GET /companies` - Get company list
- `GET /genres` - Get genre tags
- `POST /work/{code}/user-data` - Update user ratings and collections
- `GET /image?path=<path>` - Get image resources

### 🆘 FAQ

**Q: Can't find works after classification?**
A: Verify that the data path is set correctly and check that folder names contain the correct work codes.

**Q: Web interface can't load images?**
A: Ensure the backend service is running and check that image file paths are correct.

**Q: How to add new works?**
A: Place new works in the data directory following the standard format, then run a rescan.

---

## 🔗 Links

- [項目首頁 / プロジェクトホーム / Project Home](https://github.com/your-username/dlsite-classification)
- [問題回報 / 問題報告 / Issue Report](https://github.com/your-username/dlsite-classification/issues)
- [使用許可 / ライセンス / License](LICENSE)

## 🤝 貢獻 / 貢献 / Contributing

歡迎提交 Pull Request 和 Issue！
Pull RequestとIssueの投稿を歓迎します！
Pull Requests and Issues are welcome!

## 📄 許可證 / ライセンス / License

本項目採用 MIT 許可證 - 查看 [LICENSE](LICENSE) 文件了解詳情。
このプロジェクトはMITライセンスの下で公開されています - 詳細は[LICENSE](LICENSE)ファイルをご覧ください。
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.