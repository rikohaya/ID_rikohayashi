# claudecode-media-plan

template.xlsx のフォーマットに従い、brief.json からメディアプランを自動生成する。

## クイックスタート

```bash
# 1. 案件フォルダに brief.json を作成（Projects/シクテン/input/brief.json が例）
# 2. 実行
python src/generate.py シクテン

# → Projects/シクテン/output/media_plan.xlsx が生成される
```

## ディレクトリ構成

```
claudecode-media-plan/
├─ README.md                # 本ファイル
├─ template.xlsx            # お手本Excel（絶対に編集しない）
├─ src/
│  └─ generate.py           # 実行スクリプト
├─ prompts/
│  └─ generate.md           # Claude への生成ルール
└─ Projects/
   └─ <案件名>/
      ├─ README.md           # 案件ガイド（作業前に必読）
      ├─ input/
      │  └─ brief.json       # 入力（これを編集する）
      └─ output/
         └─ media_plan.xlsx  # 出力（毎回上書き）
```

## 触って良いもの / ダメなもの

| ファイル | 編集 | 備考 |
|---|---|---|
| `Projects/<案件名>/input/brief.json` | **OK** | 案件ごとに自由に編集 |
| `Projects/<案件名>/output/media_plan.xlsx` | OK | 生成後の手動調整も可。再実行で上書きされる |
| `src/generate.py` | 注意 | ロジック修正時のみ |
| `prompts/generate.md` | 注意 | Claude への指示変更時のみ |
| **`template.xlsx`** | **禁止** | 全案件のフォーマット元。壊すと全出力に影響 |

## 実行例

```bash
python src/generate.py シクテン
```

- 入力: `Projects/<案件名>/input/brief.json`
- 出力: `Projects/<案件名>/output/media_plan.xlsx`

常にリポジトリのルートディレクトリで実行する。上記以外の実行方法は使わない。

---

## brief.json（入力ファイル）暫定仕様

> この仕様は暫定。将来フィールドが増減する可能性あり。

### 構造

3層: **project** + **defaults** + **tactics**

### project（必須）

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `total_budget` | number | Yes | 総予算（円） |
| `period` | string | — | 施策期間（例: `"2025-07 ~ 2025-12"`） |
| `memo` | string | — | 補足メモ。Excel のメモ欄に出力される |

> 案件名は CLI 引数（フォルダ名）で決まる。brief.json 内に書く必要はない。

### defaults（任意）

tactics で省略されたときのフォールバック値。

| キー | 型 | 説明 | 参考値 |
|---|---|---|---|
| `follower_unit_price` | number | フォロワー単価（円） | `3` |
| `avg_followers` | number | 平均フォロワー数 | `150000` |
| `imp_rate` | number | imp率（0〜1） | `0.2` |
| `cpm` | number | CPM（円） | `300` |
| `fq` | number | フリクエンシー | `1.1` |

### tactics（必須・1件以上）

**共通フィールド（全 ad_type 共通）:**

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `category` | string | Yes | 施策カテゴリ（`"美容レビュー"` / `"広告配信"` / `"ギフティング"` 等） |
| `detail` | string | Yes | 施策詳細（`"美容まとめ投稿"` 等） |
| `ad_type` | string | Yes | `"配信有"` / `"配信無"` / `"広告配信"` の3値 |
| `target` | string | Yes | ターゲット層（`"美容マス層"` 等） |
| `sns` | string | Yes | 媒体（`"IG Feed"` / `"IG Reel"` / `"TikTok"` / `"X"` / `"YouTube"` / `"@cosme"` 等） |
| `allocation` | number | Yes | 予算配分比率（0〜1。全施策の合計が 1.0 以下になるように） |
| `timing` | string | — | 実施時期 |
| `memo` | string | — | 施策ごとの補足 |

**インフルエンサー施策（ad_type = `"配信有"` / `"配信無"`）:**

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `follower_unit_price` | number | *1 | フォロワー単価（円） |
| `avg_followers` | number | *1 | 平均フォロワー数 |
| `num_influencers` | number | — | 起用人数（指定時: 合計FW = avg_followers x num_influencers） |
| `imp_rate` | number | *1 | imp率 |
| `fq` | number | *1 | FQ |

**広告配信施策（ad_type = `"広告配信"`）:**

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `cpm` | number | *1 | CPM（円） |
| `fq` | number | *1 | FQ |

> *1: defaults にあれば省略可。両方なければ必須。

### 算出ロジック

```
# インフルエンサー施策
予算            = total_budget x allocation
合計フォロワー数 = avg_followers x num_influencers   （指定時）
               = 予算 / follower_unit_price          （省略時）
imp数           = 合計フォロワー数 x imp_rate
リーチ数         = imp数 / fq

# 広告配信施策
予算            = total_budget x allocation
imp数           = 予算 / cpm x 1000
リーチ数         = imp数 / fq
```

### コピペ用サンプル

```json
{
  "project": {
    "total_budget": 150000000,
    "period": "2025-07 ~ 2025-12"
  },
  "defaults": {
    "follower_unit_price": 3,
    "avg_followers": 150000,
    "imp_rate": 0.2,
    "cpm": 300,
    "fq": 1.1
  },
  "tactics": [
    {
      "category": "美容レビュー",
      "detail": "美容まとめ投稿",
      "ad_type": "配信有",
      "target": "美容マス層",
      "sns": "IG Feed",
      "allocation": 0.027,
      "timing": "8月",
      "avg_followers": 100000,
      "num_influencers": 4
    },
    {
      "category": "広告配信",
      "detail": "美容まとめ投稿 / 話題化投稿（AD）",
      "ad_type": "広告配信",
      "target": "美容マス層",
      "sns": "IG Feed",
      "allocation": 0.02,
      "timing": "8月",
      "cpm": 250,
      "fq": 2.5
    },
    {
      "category": "ギフティング",
      "detail": "ギフティング",
      "ad_type": "配信無",
      "target": "美容マス層",
      "sns": "@cosme",
      "allocation": 0.004,
      "timing": "8月",
      "num_influencers": 100
    }
  ]
}
```

### 拡張予定フィールド（未実装）

| キー | 型 | 説明 |
|---|---|---|
| `age_reach_rates` | object | 年代別リーチ率 `{"18-24": 0.2, "25-34": 0.4, "35-44": 0.4}` |
| `visit_rate` | number | 来店率 |
| `purchase_rate` | number | 来店後購入率 |
| `eng_rate` | number | エンゲージメント率 |
| `ctr` | number | クリック率 |
| `cvr` | number | コンバージョン率 |

---

## Claude を使う場合の補足

このリポジトリには、非エンジニア向けの
「そのまま使えるプロンプト」を用意しています。

- `prompts_for_users/01_start_prompt.txt`
- `prompts_for_users/02_make_brief_from_materials.txt`

Claude を使う場合は、上記テキストをそのまま貼り付けて使用してください。
