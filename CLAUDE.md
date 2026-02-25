# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

マーケティング業務支援プラットフォーム。複数のサブプロジェクトで構成される。

## 開発コマンド

```bash
# バックエンド起動（プロジェクトルートで実行）
uvicorn backend.main:app --reload

# 依存関係インストール
pip install -r requirements.txt

# 分析ダッシュボード（Next.js）起動
cd Project/Ana/webapp && npm run dev

# メディアプラン生成（media-plan-tool）
python media-plan-tool/src/generate.py <案件名>
```

## アーキテクチャ

### メインアプリ（backend/ + frontend/）

FastAPI アプリケーション。`backend/main.py` が静的ファイルとして `frontend/` をマウントし、SPA として配信。

**データフロー:**
- チャット: `frontend/script.js` → `/api/chat` → `routers/chat.py` → `services/gemini.py`（Gemini 1.5 Flash）→ `database.py`（SQLite に会話保存）
- メディアプラン: `frontend/media-plan.js` → `/api/media-plan/*` → `routers/media_plan.py` → `services/media_calculator.py`（人口統計データ内蔵の計算エンジン）

**主要サービス:**
- `services/gemini.py`: Gemini API ラッパー。チャット応答、会話タイトル生成（20文字以内）、ターゲット人口推定の3機能
- `services/media_calculator.py`: 6年齢層×性別の人口・SNS利用率データを内蔵。CPMベースの通常計算と予算逆算の2モード

**DB構成:** SQLite（`data/chat_history.db`）。テーブルは `conversations` と `messages` の2つ。async（aiosqlite）で操作。

### 分析ダッシュボード（Project/Ana/webapp/）

Next.js + React + Recharts + Tailwind CSS。X（Twitter）投稿データの分析結果を可視化するダッシュボード。`public/data/analysis.json` から静的データを読み込んで表示。

### メディアプラン生成ツール（media-plan-tool/）

brief.json → Excel 出力のCLIツール。`template.xlsx` は全案件共通のフォーマット元なので**編集禁止**。案件データは `media-plan-tool/Projects/<案件名>/input/brief.json` に配置。

### カスタムスラッシュコマンド（.claude/commands/口コミ分析/）

口コミCSVデータを段階的に分析するマーケティング分析ワークフロー（①概要→②ポジネガ→③購買要因→④POX→⑤WHO→⑥CEP→⑦コミュニケーション戦略→⑨ビッグアイディア）。

## 設定

- 環境変数: `.env` に `GEMINI_API_KEY` を設定
- Pydantic Settings（`backend/config.py`）が `.env` を自動読込
