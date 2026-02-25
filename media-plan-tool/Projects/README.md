# Projects

案件ごとのメディアプラン作業ディレクトリ。シクテンをサンプルとして同梱している。

## 新規プロジェクトの作り方

```bash
# 1. フォルダ作成
mkdir -p Projects/新案件名/input Projects/新案件名/output

# 2. brief.json を作成（シクテンをコピーして編集するのが早い）
cp Projects/シクテン/input/brief.json Projects/新案件名/input/brief.json

# 3. brief.json を編集
#    - total_budget, tactics を案件に合わせて書き換える

# 4. 実行
python src/generate.py 新案件名

# 5. 出力を確認
#    Projects/新案件名/output/media_plan.xlsx を Excel で開く
```

## ディレクトリ規約

```
Projects/<案件名>/
├─ README.md          # 案件固有の前提・注意事項（任意だが推奨）
├─ input/
│  └─ brief.json      # 入力（これを編集する）
└─ output/
   └─ media_plan.xlsx # 出力（generate.py が毎回上書き）
```

- brief.json の仕様は [ルート README の暫定仕様](../README.md#briefjson入力ファイル暫定仕様) を参照
- output/media_plan.xlsx を手動で調整した場合、再実行すると上書きされるので注意
- template.xlsx は全案件共通のフォーマット元。**絶対に編集しない**

## サンプル

`シクテン/` がサンプルプロジェクト。brief.json の書き方や出力結果の確認用として参照できる。
