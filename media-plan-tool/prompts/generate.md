# generate.md — メディアプラン生成ルール

## 実行方法（固定）

**常にリポジトリのルートディレクトリで実行する。**

```bash
cd /path/to/claudecode-media-plan   # ← ここがルート
python src/generate.py <project_name>
```

- 入力: `Projects/<project_name>/input/brief.json`
- 出力: `Projects/<project_name>/output/media_plan.xlsx`

これ以外の実行方法は使わない。
`src/` や `Projects/` の中に移動してからの相対パス実行、任意パス引数の指定は行わない。

## 絶対ルール

1. **template.xlsx の構造・書式・数式を壊さない**
   - FMT タブの列順（C〜R）、ヘッダー行（4行目）、合計行の SUM 数式は変更禁止
   - セルの書式（通貨 ¥, %, #,##0 等）はテンプレートのものを維持する
2. **推測しない**
   - brief.json に書かれていない値は Excel 上で空欄にする
   - 「ありそうな値」を勝手に埋めない
3. **入力にない情報は空欄**
   - defaults にもtactics にも無いフィールドは、セルに何も書き込まない
   - 数式は残すが、参照先が空なら Excel 側で 0 や #DIV/0! になるのが正しい挙動

## template.xlsx の構造（FMT タブ）

```
行4  : ヘッダー（C〜R: 施策/詳細/広告配信有無/ターゲット/SNS/アロケーション/予算/フォロワー単価/合計フォロワー数/起用人数/平均フォロワー数/imp率/imp数/CPM/FQ/リーチ数）
行5〜 : データ行（施策ごとに1行）
合計行: "合計" ラベル + SUM 数式 + 総予算の直接入力
メモ行: 合計の2行下
```

列と数式のパターン:

| 列 | インフルエンサー（配信有/配信無） | 広告配信 |
|---|---|---|
| H: アロケーション | 入力値 | 入力値 |
| I: 予算 | `=$I$合計行*H{r}` | `=$I$合計行*H{r}` |
| J: フォロワー単価 | 入力値 | — |
| K: 合計FW | `=I/J` or `=L*M` | — |
| L: 起用人数 | `=ROUND(K/M,0)` or 入力値 | — |
| M: 平均FW | 入力値 | — |
| N: imp率 | 入力値 | — |
| O: imp数 | `=K*N` | `=I/P*1000` |
| P: CPM | `=I*1000/O`（参考値） | 入力値 |
| Q: FQ | 入力値 | 入力値 |
| R: リーチ数 | `=O/Q` | `=O/Q` |

## brief.json の仕様（暫定）

### 構造

```json
{
  "project":  { "total_budget": 数値, ... },
  "defaults": { "follower_unit_price": 3, "cpm": 300, ... },
  "tactics":  [ { "category": "...", "ad_type": "...", ... }, ... ]
}
```

### project（必須）

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `total_budget` | number | Yes | 総予算（円） |
| `period` | string | — | 施策期間 |
| `memo` | string | — | メモ欄に出力 |

> 案件名は CLI 引数（フォルダ名）で決まる。brief.json には不要。

### defaults（任意）

| キー | 型 | 説明 |
|---|---|---|
| `follower_unit_price` | number | フォロワー単価（円） |
| `avg_followers` | number | 平均フォロワー数 |
| `imp_rate` | number | imp率（0〜1） |
| `cpm` | number | CPM（円） |
| `fq` | number | FQ |

### tactics 共通フィールド

| キー | 型 | 必須 | 説明 |
|---|---|---|---|
| `category` | string | Yes | 施策カテゴリ |
| `detail` | string | Yes | 施策詳細 |
| `ad_type` | string | Yes | `"配信有"` / `"配信無"` / `"広告配信"` |
| `target` | string | Yes | ターゲット層 |
| `sns` | string | Yes | 媒体 |
| `allocation` | number | Yes | 予算配分比率（0〜1） |
| `timing` | string | — | 実施時期 |

### ad_type 別の追加フィールド

**配信有 / 配信無（インフルエンサー）:**
`follower_unit_price`, `avg_followers`, `num_influencers`, `imp_rate`, `fq`
（defaults にあれば省略可）

**広告配信:**
`cpm`, `fq`
（defaults にあれば省略可）

## 行数の増減ルール

- tactics の数 > テンプレートのデータ行数 → 合計行の直前に行を挿入
- tactics の数 < テンプレートのデータ行数 → 末尾の不要行を削除
- 挿入した行にはテンプレート行のスタイルをコピーする
- 合計行の SUM 範囲は実際のデータ行に合わせて更新する
