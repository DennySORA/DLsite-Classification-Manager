# DLsite Classification Manager

言語 Languages: [English](README.md) | [繁體中文](README.zh-TW.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

高性能な DLsite 作品の分類・管理ツール。モダンな Web UI と完全な API を提供します。

## 🌟 機能特徴

- 高効率処理：async/await による高性能クローラーとファイル処理
- スマートコード抽出：DLsite 作品コード（RJ, BJ, VJ, RE, BE, VE）を自動識別・抽出
- 完全なメタデータ：タイトル、サークル、ジャンル、画像、紹介文など
- モダンな Web インターフェース：Nuxt.js ベースのレスポンシブ UI
- 強力な API：検索・フィルタリング・ソート対応の RESTful API
- ユーザーコレクション：個人評価とコレクション分類
- 複数のビューモード：グリッド / リスト表示
- インテリジェント検索：マルチフィールド検索と高度なフィルタリング

## 🛠️ システム要件

- Python 3.8+
- Node.js 16+
- Yarn または npm

## 📦 インストール

### 1. リポジトリをクローン
```
git clone https://github.com/your-username/dlsite-classification.git
cd dlsite-classification
```

### 2. バックエンド依存関係をインストール
```
pip install -r requirements.txt
```

### 3. フロントエンド依存関係をインストール
```
cd dlsite_classification_web
yarn install
# または npm install
```

## 🚀 使い方

### バックエンドサービスを起動

1) コマンドライン分類ツール（インタラクティブ CLI）
```
python main.py
```

2) Web API サーバー（ポート 8001）
```
# デフォルト設定
python server.py

# データフォルダを指定
python server.py --data-path /path/to/your/dlsite/data

# カスタムホスト / ポート
python server.py --data-path ./test_game_info --port 8080 --host 127.0.0.1

# 環境変数を使用
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

### フロントエンドを起動

```
cd dlsite_classification_web

# 開発モード
yarn dev

# 本番モード
yarn build
yarn preview
```

`http://localhost:3000` または `http://localhost:3001` にアクセス。

## 🎯 チュートリアル

### 基本フロー

1) データ準備：DLsite 作品フォルダを指定ディレクトリに配置
2) 分類実行：`python main.py` を実行してオプションを選択
3) 結果確認：Web UI で分類結果を閲覧

### Web インターフェース機能

- 検索：キーワードで作品を検索
- フィルタリング：サークル、ジャンル、コレクションなど
- ビュー切替：グリッド / リスト
- 作品詳細：カードをクリックして詳細表示
- 評価・コレクション：詳細画面で設定

## 📊 データ形式

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

## 🔧 設定

### データパス（優先順位）

1) コマンドライン引数
```
python server.py --data-path /path/to/your/dlsite/data
```

2) 環境変数
```
export DLSITE_DATA_PATH=/path/to/your/dlsite/data
python server.py
```

3) デフォルトパス（順に検査）
- `./test_game_info`
- `/mnt/d/R18/DLsite`
- `./data`

### サーバー

```
# ポート
python server.py --port 8080

# ホスト
python server.py --host 127.0.0.1

# 完全設定
python server.py --data-path ./data --port 8080 --host 0.0.0.0
```

### コマンドライン引数

- `--data-path, -d`：データフォルダパス
- `--port, -p`：サーバーポート（デフォルト 8001）
- `--host`：サーバーホスト（デフォルト 0.0.0.0）
- `--help`：ヘルプ

## 📡 API エンドポイント

- `GET /works`
- `GET /work/{code}`
- `GET /companies`
- `GET /genres`
- `POST /work/{code}/user-data`
- `GET /image?path=<path>`

## 🔗 リンク

- プロジェクトホーム：https://github.com/your-username/dlsite-classification
- 問題報告：https://github.com/your-username/dlsite-classification/issues
- ライセンス：LICENSE

## 🤝 貢献

Pull Request と Issue を歓迎します！

## 📄 ライセンス

MIT License — `LICENSE` を参照。

