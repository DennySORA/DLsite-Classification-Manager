# DLsite Classification Manager

言語 Languages: [English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

高性能な DLsite 作品の分類・管理ツール。FastAPI バックエンドと Nuxt 3 Web UI を提供します。

## 🌟 機能特徴

- 非同期クローラーとファイル処理
- インタラクティブ CLI フロー：分類、更新、検証、アーカイブ
- FastAPI REST API：検索、フィルタ、ページング、メタデータ
- Nuxt 3 UI：閲覧、評価、コレクション
- 会社 ARCHIVE ツール：全作品メタデータの取得
- `.tag` ファイルで保存し、DB 不要

## 🛠️ システム要件

- Python 3.10+
- Node.js 18+
- uv
- Yarn（または npm/pnpm）

## 📦 インストール

### バックエンド

```
uv venv
source .venv/bin/activate
uv sync
```

### フロントエンド

```
cd dlsite_classification_web
yarn install
```

## 🚀 使い方

### CLI（インタラクティブ）

```
uv run python main.py
```

### API サーバー

```
uv run python server.py
```

データパス / ホスト / ポートの指定：

```
uv run python server.py --data-path /path/to/your/dlsite/data --host 0.0.0.0 --port 8001
```

環境変数でデータパスを指定：

```
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
```

### フロントエンド

```
cd dlsite_classification_web
yarn dev
```

`http://localhost:3000`（3000 が使用中の場合は `http://localhost:3001`）にアクセス。
フロントエンドは `http://localhost:8001` API を想定しています。

## 🔧 データパス優先順位

1) `--data-path`
2) `DLSITE_DATA_PATH`
3) デフォルト（存在するものを優先）
   - `./test_game_info`
   - `/mnt/d/R18/DLsite`
   - `./data`

## 📡 API エンドポイント

- `GET /` / `GET /status`
- `GET /works`（検索、フィルタ、ソート、ページング）
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

## 📊 データ形式

```
[サークル名]_[サークルID]/
├── [作品ID]_[サークル名]_[サークルID] 作品タイトル/
│   └── [作品ID]_info/
│       ├── [作品ID]_img_main.jpg
│       ├── [作品ID]_img_smp1.jpg
│       ├── code.tag
│       ├── title.tag
│       ├── company.tag
│       └── ... その他のタグファイル
└── ARCHIVE/
    └── RJ123456_info/
        ├── title.tag
        └── ... アーカイブ情報
```

## 🧪 開発

```
uv run ruff check --fix .
uv run ruff format .
uv run mypy .
./run_tests.sh
```

WSL で "bad interpreter" が出る場合：

```
sed -i 's/\r$//' run_tests.sh && chmod +x run_tests.sh
```

## 📸 Web UI プレビュー

![Web Demo 1](doc/1.png)
![Web Demo 2](doc/2.png)
![Web Demo 3](doc/3.png)
![Web Demo 4](doc/4.png)

## 🔗 リンク

- プロジェクトホーム：https://github.com/DennySORA/DLsite-Classification-Manager
- 問題報告：https://github.com/DennySORA/DLsite-Classification-Manager/issues
- ライセンス：LICENSE
