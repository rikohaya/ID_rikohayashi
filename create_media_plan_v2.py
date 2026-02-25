#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "辛い麺 5000万"

# スタイル定義
header_font = Font(bold=True, size=10)
header_fill = PatternFill(start_color="FFE4B5", end_color="FFE4B5", fill_type="solid")
phase1_fill = PatternFill(start_color="E6F3FF", end_color="E6F3FF", fill_type="solid")
phase2_fill = PatternFill(start_color="FFF0E6", end_color="FFF0E6", fill_type="solid")
phase3_fill = PatternFill(start_color="E6FFE6", end_color="E6FFE6", fill_type="solid")
ad_fill = PatternFill(start_color="F5F5F5", end_color="F5F5F5", fill_type="solid")
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# 列幅設定
widths = [12, 18, 22, 28, 8, 10, 12, 10, 14, 12, 10, 12]
for i, width in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = width

# ヘッダー行
headers = ["フェーズ", "目的", "項目", "小項目", "Media", "配信有無", "フォロワー規模", "Allocation\nDetail", "Budget(¥)", "KPI", "FW単価", "合計Fw数"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=2, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = thin_border
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

# データ
# 予算合計セル参照用
total_row = 40  # 合計行の位置

data = [
    # Phase 1: 発売前
    ["Phase1", "辛いもの\nイノベーター", "メガKOLギフティング", "YouTube/IG/X複合 世界観訴求", "YT/IG/X", "無し", "Mega", "", 2500000, "総リーチ数", 5.0, ""],
    ["", "", "ミドルKOLギフティング", "辛いものイノベーター層", "TT/IG", "無し", "Middle", "", 2000000, "リーチ数", 4.0, ""],
    ["", "", "商品・SPECIAL BOX", "30名分制作・発送", "-", "-", "-", "", 1000000, "発送数", "", ""],
    ["", "広告配信", "広告配信", "ティザー・解禁情報拡散", "X", "", "-", "", 2000000, "imp数", "", ""],
    ["", "", "広告配信", "ギフティング投稿ブースト", "TT", "", "-", "", 1000000, "imp数", "", ""],

    # Phase 2: 発売期
    ["Phase2", "辛いもの/韓国好き\n（発売盛り上げ）", "メガKOL モッパン", "モッパン系コンテンツ", "TT", "有り", "Mega", "", 3500000, "再生数", 4.0, ""],
    ["", "", "ミドルKOL モッパン", "新発売HOOK+モッパン", "TT", "有り", "Middle", "", 3200000, "再生数", 4.0, ""],
    ["", "", "商品費", "モッパン系用", "-", "-", "-", "", 800000, "-", "", ""],
    ["", "辛い麺顧客獲得\nトライブハック①", "メガKOL", "限界OL/主婦系\n金曜夜・ワンオペ・チートデイ", "TT", "有り", "Mega", "", 3000000, "再生数", 4.0, ""],
    ["", "", "ミドルKOL", "各シーン担当", "TT", "有り", "Middle", "", 2400000, "再生数", 4.0, ""],
    ["", "", "マイクロKOL", "サブ投稿", "TT", "有り", "Nano", "", 100000, "再生数", 5.0, ""],
    ["", "新規顧客獲得\nトライブハック②", "ミドルKOL", "推し活疲れ/生理前/二日酔い/一人時間", "TT", "有り", "Middle", "", 3600000, "再生数", 4.0, ""],
    ["", "", "マイクロKOL", "サブ投稿", "TT", "有り", "Nano", "", 600000, "再生数", 5.0, ""],
    ["", "", "商品費", "トライブハック用", "-", "-", "-", "", 800000, "-", "", ""],
    ["", "グルメ系", "グルメ系ミドルKOL", "TikTok/Instagram", "TT/IG", "有り", "Middle", "", 3500000, "リーチ数", 4.0, ""],
    ["", "広告配信", "広告配信", "KOL投稿ブースト・リーチ最大化", "TT", "", "-", "", 5000000, "imp数", "", ""],
    ["", "", "広告配信", "トレンド入り狙い・話題拡散", "X", "", "-", "", 2000000, "imp数", "", ""],

    # Phase 3: 発売後
    ["Phase3", "SNSトレンド好き\n（UGC醸成）", "ミドルKOL アレンジ", "チーズ/卵/〆ご飯等", "TT", "有り", "Middle", "", 2100000, "再生数", 4.0, ""],
    ["", "", "マイクロKOL アレンジ", "バリエーション展開", "TT", "有り", "Nano", "", 400000, "再生数", 5.0, ""],
    ["", "", "ミドルKOL アレンジ", "アレンジ投稿", "X", "無し", "Middle", "", 300000, "imp数", 2.0, ""],
    ["", "SNS話題HOOK", "ミドルKOL", "○○見ながら訴求", "TT", "有り", "Middle", "", 1400000, "再生数", 4.0, ""],
    ["", "", "マイクロKOL", "サブ投稿", "TT", "有り", "Nano", "", 600000, "再生数", 5.0, ""],
    ["", "ミーム系チャレンジ", "ペイドKOL", "チャレンジ火付け役", "TT", "有り", "Middle", "", 2000000, "参加数", 4.0, ""],
    ["", "", "チャレンジ運用費", "ハッシュタグ管理等", "-", "-", "-", "", 700000, "-", "", ""],
    ["", "広告配信", "広告配信", "アレンジ・ミーム拡散", "TT", "", "-", "", 2500000, "imp数", "", ""],
    ["", "", "広告配信", "Reelsリターゲティング", "IG", "", "-", "", 1500000, "imp数", "", ""],

    # 予備費
    ["予備費", "", "追加ブースト対応", "", "-", "-", "-", "", 800000, "-", "", ""],
    ["", "", "緊急対応・リスク管理", "", "-", "-", "-", "", 700000, "-", "", ""],
]

# データ入力
start_row = 3
for row_idx, row_data in enumerate(data):
    current_row = start_row + row_idx

    # フェーズに応じた色分け
    if row_data[0] == "Phase1" or (row_idx < 5):
        fill = phase1_fill
    elif row_data[0] == "Phase2" or (5 <= row_idx < 17):
        fill = phase2_fill
    elif row_data[0] == "Phase3" or (17 <= row_idx < 27):
        fill = phase3_fill
    else:
        fill = None

    # 広告配信行は別色
    if "広告配信" in str(row_data[1]) or "広告配信" in str(row_data[2]):
        fill = ad_fill

    for col_idx, value in enumerate(row_data):
        cell = ws.cell(row=current_row, column=col_idx + 1, value=value)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        if fill:
            cell.fill = fill

        # Budget列は数値フォーマット
        if col_idx == 8 and isinstance(value, (int, float)) and value > 0:
            cell.number_format = '#,##0'

# Allocation Detail の数式を設定（Budget / 合計Budget）
total_budget_cell = f"I{start_row + len(data)}"
for row_idx in range(len(data)):
    current_row = start_row + row_idx
    budget_value = ws.cell(row=current_row, column=9).value
    if isinstance(budget_value, (int, float)) and budget_value > 0:
        ws.cell(row=current_row, column=8, value=f"=I{current_row}/${total_budget_cell}")
        ws.cell(row=current_row, column=8).number_format = '0%'
        ws.cell(row=current_row, column=8).alignment = Alignment(horizontal='center', vertical='center')

# 合計Fw数の計算（Budget / FW単価）
for row_idx in range(len(data)):
    current_row = start_row + row_idx
    fw_unit = ws.cell(row=current_row, column=11).value
    if isinstance(fw_unit, (int, float)) and fw_unit > 0:
        ws.cell(row=current_row, column=12, value=f"=I{current_row}/K{current_row}")
        ws.cell(row=current_row, column=12).number_format = '#,##0'

# 合計行
total_row = start_row + len(data)
ws.cell(row=total_row, column=7, value="合計").font = Font(bold=True)
ws.cell(row=total_row, column=8, value=f"=SUM(H{start_row}:H{total_row-1})")
ws.cell(row=total_row, column=8).number_format = '0%'
ws.cell(row=total_row, column=9, value=f"=SUM(I{start_row}:I{total_row-1})")
ws.cell(row=total_row, column=9).number_format = '#,##0'
ws.cell(row=total_row, column=9).font = Font(bold=True)

for col in range(1, 13):
    ws.cell(row=total_row, column=col).border = thin_border

# 下部にサマリーテーブル追加
summary_start = total_row + 3

ws.cell(row=summary_start, column=2, value="月").font = Font(bold=True)
ws.cell(row=summary_start, column=3, value="フェーズ").font = Font(bold=True)
ws.cell(row=summary_start, column=4, value="費用").font = Font(bold=True)

summary_data = [
    ["発売前", "Phase1: 話題化", f"=SUM(I{start_row}:I{start_row+4})"],
    ["発売期", "Phase2: 盛り上げ", f"=SUM(I{start_row+5}:I{start_row+16})"],
    ["発売後", "Phase3: UGC醸成", f"=SUM(I{start_row+17}:I{start_row+25})"],
    ["", "予備費", f"=SUM(I{start_row+26}:I{start_row+27})"],
    ["合計", "", f"=I{total_row}"],
]

for idx, (month, phase, cost) in enumerate(summary_data):
    row = summary_start + 1 + idx
    ws.cell(row=row, column=2, value=month)
    ws.cell(row=row, column=3, value=phase)
    ws.cell(row=row, column=4, value=cost)
    ws.cell(row=row, column=4).number_format = '#,##0'
    if idx == len(summary_data) - 1:
        ws.cell(row=row, column=4).font = Font(bold=True)

# KOLサマリー
kol_start = summary_start + 8
ws.cell(row=kol_start, column=2, value="KOLサマリー").font = Font(bold=True, size=11)
ws.cell(row=kol_start+1, column=2, value="カテゴリ")
ws.cell(row=kol_start+1, column=3, value="人数")
ws.cell(row=kol_start+1, column=4, value="金額")

kol_data = [
    ["メガKOL（100万↑）", "3名", 9000000],
    ["ミドルKOL（10-50万）", "25名", 18500000],
    ["マイクロKOL（1-10万）", "6名", 1500000],
    ["合計", "34名", 29000000],
]

for idx, (cat, num, cost) in enumerate(kol_data):
    row = kol_start + 2 + idx
    ws.cell(row=row, column=2, value=cat)
    ws.cell(row=row, column=3, value=num)
    ws.cell(row=row, column=4, value=cost)
    ws.cell(row=row, column=4).number_format = '#,##0'
    if idx == len(kol_data) - 1:
        ws.cell(row=row, column=2).font = Font(bold=True)
        ws.cell(row=row, column=4).font = Font(bold=True)

# 広告配信サマリー
ad_start = kol_start + 8
ws.cell(row=ad_start, column=2, value="広告配信サマリー").font = Font(bold=True, size=11)
ws.cell(row=ad_start+1, column=2, value="媒体")
ws.cell(row=ad_start+1, column=3, value="金額")

ad_data = [
    ["TikTok", 8500000],
    ["X", 4000000],
    ["Instagram", 1500000],
    ["合計", 14000000],
]

for idx, (media, cost) in enumerate(ad_data):
    row = ad_start + 2 + idx
    ws.cell(row=row, column=2, value=media)
    ws.cell(row=row, column=3, value=cost)
    ws.cell(row=row, column=3).number_format = '#,##0'
    if idx == len(ad_data) - 1:
        ws.cell(row=row, column=2).font = Font(bold=True)
        ws.cell(row=row, column=3).font = Font(bold=True)

# ファイル保存
output_path = "/Users/rikohayashi/Downloads/AP/辛い麺_メディアプラン_5000万_v2.xlsx"
wb.save(output_path)
print(f"Excel file created: {output_path}")
