# Handoff Starter Kit

Claude Code でセッション間の引き継ぎを行うためのスキルセット。

## 機能

| コマンド | 用途 |
|----------|------|
| `/handoff` | セッション終了時に進捗を HANDOFF.md に保存 |
| `/resume` | セッション再開時に前回の状態を読み込み |

## インストール

### 1. スキルファイルをコピー

```bash
# ~/.claude/commands/ フォルダがない場合は作成
mkdir -p ~/.claude/commands

# スキルファイルをコピー
cp commands/handoff.md ~/.claude/commands/
cp commands/resume.md ~/.claude/commands/
```

### 2. プロジェクトに HANDOFF.md を配置

```bash
# プロジェクトルートに HANDOFF.md をコピー
cp templates/HANDOFF.md /path/to/your/project/
```

## 使い方

### セッション終了時

```
/handoff
```

以下が自動で行われます：
- 完了タスク・作業中タスクの記録
- 次のアクションの整理
- git status / git log の記録
- セッション履歴の追記

### セッション再開時

```
/resume
```

以下が表示されます：
- 前回の完了/作業中タスク
- 次のアクション（優先順位付き）
- 未解決の問題
- 未コミット変更の有無

## ファイル構成

```
handoffStarter/
├── README.md                # このファイル
├── commands/
│   ├── handoff.md          # /handoff スキル定義
│   └── resume.md           # /resume スキル定義
└── templates/
    └── HANDOFF.md          # プロジェクト用テンプレート
```

## 運用ルール

- **HANDOFF.md は追記型** - 既存の完了タスク・履歴を削除しない
- **セッション履歴は新しい順** - 最新を先頭に追加
- **永続的な知識は CLAUDE.md へ** - プロジェクト固有設定に反映

## 日常のワークフロー

```
朝:    /resume     → 前回の状態を確認
作業:  タスクを進める
終了:  /handoff    → 進捗を保存
```
