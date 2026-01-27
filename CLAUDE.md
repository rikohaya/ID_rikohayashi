# AP - ビジネスクラスインサイト分析プロジェクト

## プロジェクト概要

北米・欧州ビジネスクラスのインサイト調査・分析を行うWebアプリケーション。

## 技術スタック

- **Backend**: FastAPI (Python 3.x)
- **Frontend**: HTML/CSS/JavaScript（バニラ）
- **AI**: Google Generative AI (Gemini)
- **Database**: SQLite (aiosqlite)

## フォルダ構成

```
AP/
├── backend/          # FastAPI バックエンド
│   ├── main.py       # エントリーポイント
│   ├── database.py   # DB接続・操作
│   ├── models.py     # Pydantic モデル
│   ├── config.py     # 設定
│   ├── routers/      # APIルーター
│   └── services/     # ビジネスロジック
├── frontend/         # フロントエンド
│   ├── index.html
│   ├── script.js
│   └── style.css
├── data/             # データファイル格納
├── Project/          # 分析プロジェクト
│   └── Ana/          # 分析スクリプト・結果
│       ├── analysis.py
│       ├── results/
│       └── webapp/
├── .env              # 環境変数（API キー等）
└── requirements.txt  # Python依存関係
```

## 環境変数

`.env` ファイルに設定:
- Google Generative AI API キー（推定）

## 開発コマンド

```bash
# バックエンド起動
uvicorn backend.main:app --reload

# 依存関係インストール
pip install -r requirements.txt
```

## 更新履歴

- 2026-01-27: 初版作成、プロジェクト構造記録
