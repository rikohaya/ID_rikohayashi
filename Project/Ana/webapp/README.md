# 界隈分析ダッシュボード

北米ビジネスクラスX発話の界隈分析結果を可視化するWebダッシュボードです。

## セットアップ

### 1. 依存関係のインストール

```bash
cd webapp
npm install
```

### 2. 分析データの生成

親ディレクトリで分析スクリプトを実行し、JSONデータを生成します。

```bash
cd ..
python analysis.py
```

生成された `results/analysis.json` を `webapp/public/data/` にコピーします。

```bash
cp results/analysis.json webapp/public/data/
```

### 3. ローカル開発サーバーの起動

```bash
cd webapp
npm run dev
```

ブラウザで http://localhost:3000 を開いてダッシュボードを確認できます。

## Vercelへのデプロイ

### 方法1: Vercel CLIを使用

```bash
npm i -g vercel
vercel
```

### 方法2: GitHubリポジトリ経由

1. このプロジェクトをGitHubにプッシュ
2. [Vercel](https://vercel.com)でGitHubリポジトリを連携
3. 自動デプロイが開始されます

## 機能

- **エグゼクティブサマリー**: 主要な発見事項をカード形式で表示
- **界隈別チャート**: 各界隈の投稿数を横棒グラフで可視化
- **航空会社別チャート**: 航空会社の言及数を可視化
- **クロス分析ヒートマップ**: 航空会社×界隈の関係をヒートマップで表示
- **注目トピック**: バイラルトピックや炎上リスクを表示
- **界隈別インサイト**: 各界隈の詳細情報とビジネスインサイト
- **総合提言**: 航空会社向け・SNS戦略の提言

## 技術スタック

- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Recharts
