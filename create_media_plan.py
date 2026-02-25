#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

wb = Workbook()

# スタイル定義
header_font = Font(bold=True, size=11)
header_fill = PatternFill(start_color="FFD700", end_color="FFD700", fill_type="solid")
phase1_fill = PatternFill(start_color="E6F3FF", end_color="E6F3FF", fill_type="solid")
phase2_fill = PatternFill(start_color="FFF0E6", end_color="FFF0E6", fill_type="solid")
phase3_fill = PatternFill(start_color="E6FFE6", end_color="E6FFE6", fill_type="solid")
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

def set_column_widths(ws, widths):
    for i, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = width

def add_header_row(ws, row, values, fill=None):
    for col, val in enumerate(values, 1):
        cell = ws.cell(row=row, column=col, value=val)
        cell.font = header_font
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center')
        if fill:
            cell.fill = fill

def add_data_row(ws, row, values, fill=None):
    for col, val in enumerate(values, 1):
        cell = ws.cell(row=row, column=col, value=val)
        cell.border = thin_border
        cell.alignment = Alignment(horizontal='center', vertical='center')
        if fill:
            cell.fill = fill

# =====================================
# Sheet 1: 全体サマリー
# =====================================
ws1 = wb.active
ws1.title = "全体サマリー"
set_column_widths(ws1, [20, 15, 15])

ws1.cell(row=1, column=1, value="辛い麺 新商品発売アクティベーション メディアプラン").font = Font(bold=True, size=14)
ws1.cell(row=2, column=1, value="予算総額：5,000万円").font = Font(bold=True, size=12)

row = 4
add_header_row(ws1, row, ["項目", "金額", "配分比率"], header_fill)
data = [
    ["KOL費用", "2,900万円", "58%"],
    ["広告配信", "1,500万円", "30%"],
    ["商品・制作・運用費", "450万円", "9%"],
    ["予備費", "150万円", "3%"],
    ["合計", "5,000万円", "100%"],
]
for d in data:
    row += 1
    add_data_row(ws1, row, d)

row += 2
ws1.cell(row=row, column=1, value="フェーズ別予算配分").font = Font(bold=True, size=12)
row += 1
add_header_row(ws1, row, ["フェーズ", "金額", "配分比率"], header_fill)
phase_data = [
    ["Phase1：発売前（話題化）", "850万円", "17%"],
    ["Phase2：発売期（盛り上げ）", "2,850万円", "57%"],
    ["Phase3：発売後（UGC醸成）", "1,150万円", "23%"],
    ["予備費", "150万円", "3%"],
]
for d in phase_data:
    row += 1
    add_data_row(ws1, row, d)

# =====================================
# Sheet 2: Phase1 発売前
# =====================================
ws2 = wb.create_sheet("Phase1_発売前")
set_column_widths(ws2, [25, 25, 10, 12, 12])

ws2.cell(row=1, column=1, value="Phase 1：発売前（話題化）【850万円】").font = Font(bold=True, size=14)
ws2.cell(row=2, column=1, value="目的：新商品発売情報ざわつかせ").font = Font(size=11)

row = 4
ws2.cell(row=row, column=1, value="■ KOL施策【550万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws2, row, ["施策", "内容", "人数", "単価", "金額"], header_fill)
kol_data = [
    ["メガKOLギフティング", "YouTube/IG/X複合", "1名", "250万円", "250万円"],
    ["ミドルKOLギフティング", "辛いものイノベーター層", "4名", "50万円", "200万円"],
    ["商品・SPECIAL BOX制作", "30名分", "-", "-", "100万円"],
    ["小計", "", "", "", "550万円"],
]
for d in kol_data:
    row += 1
    add_data_row(ws2, row, d, phase1_fill)

row += 2
ws2.cell(row=row, column=1, value="■ 広告配信【300万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws2, row, ["媒体", "金額", "用途", "", ""], header_fill)
ad_data = [
    ["X", "200万円", "ティザー・解禁情報拡散", "", ""],
    ["TikTok", "100万円", "ギフティング投稿ブースト", "", ""],
    ["小計", "300万円", "", "", ""],
]
for d in ad_data:
    row += 1
    add_data_row(ws2, row, d, phase1_fill)

# =====================================
# Sheet 3: Phase2 発売期
# =====================================
ws3 = wb.create_sheet("Phase2_発売期")
set_column_widths(ws3, [25, 30, 10, 12, 12])

ws3.cell(row=1, column=1, value="Phase 2：発売期（盛り上げ）【2,850万円】").font = Font(bold=True, size=14)
ws3.cell(row=2, column=1, value="目的：発売期の盛り上げ・バズ創出").font = Font(size=11)

row = 4
ws3.cell(row=row, column=1, value="■ 2-1. 新商品発売HOOK × モッパン【750万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws3, row, ["施策", "内容", "人数", "単価", "金額"], header_fill)
data_2_1 = [
    ["メガKOL（TikTok）", "モッパン系", "1名", "350万円", "350万円"],
    ["ミドルKOL（TikTok）", "新発売HOOK+モッパン", "4名", "80万円", "320万円"],
    ["商品費", "-", "-", "-", "80万円"],
    ["小計", "", "", "", "750万円"],
]
for d in data_2_1:
    row += 1
    add_data_row(ws3, row, d, phase2_fill)

row += 2
ws3.cell(row=row, column=1, value="■ 2-2. トライブハック①：辛い麺顧客獲得【550万円】").font = Font(bold=True, size=11)
ws3.cell(row=row+1, column=1, value="シーン：金曜夜の疲れ / ワンオペ育児後 / チートデイ").font = Font(size=10, italic=True)
row += 2
add_header_row(ws3, row, ["施策", "内容", "人数", "単価", "金額"], header_fill)
data_2_2 = [
    ["メガKOL（TikTok）", "限界OL/主婦系", "1名", "300万円", "300万円"],
    ["ミドルKOL（TikTok）", "各シーン担当", "4名", "60万円", "240万円"],
    ["マイクロKOL", "サブ投稿", "1名", "10万円", "10万円"],
    ["小計", "", "", "", "550万円"],
]
for d in data_2_2:
    row += 1
    add_data_row(ws3, row, d, phase2_fill)

row += 2
ws3.cell(row=row, column=1, value="■ 2-3. トライブハック②：新規顧客獲得【500万円】").font = Font(bold=True, size=11)
ws3.cell(row=row+1, column=1, value="シーン：推し活疲れ / 生理前爆食 / 二日酔い / 一人時間").font = Font(size=10, italic=True)
row += 2
add_header_row(ws3, row, ["施策", "内容", "人数", "単価", "金額"], header_fill)
data_2_3 = [
    ["ミドルKOL（TikTok）", "各シーン担当", "6名", "60万円", "360万円"],
    ["マイクロKOL", "サブ投稿", "4名", "15万円", "60万円"],
    ["商品費", "-", "-", "-", "80万円"],
    ["小計", "", "", "", "500万円"],
]
for d in data_2_3:
    row += 1
    add_data_row(ws3, row, d, phase2_fill)

row += 2
ws3.cell(row=row, column=1, value="■ 2-4. グルメ系ギフティング【350万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws3, row, ["施策", "内容", "人数", "単価", "金額"], header_fill)
data_2_4 = [
    ["グルメ系ミドルKOL", "TikTok/Instagram", "5名", "70万円", "350万円"],
]
for d in data_2_4:
    row += 1
    add_data_row(ws3, row, d, phase2_fill)

row += 2
ws3.cell(row=row, column=1, value="■ 発売期 広告配信【700万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws3, row, ["媒体", "金額", "用途", "", ""], header_fill)
ad_data_2 = [
    ["TikTok Spark Ads", "500万円", "KOL投稿ブースト・リーチ最大化", "", ""],
    ["X", "200万円", "トレンド入り狙い・話題拡散", "", ""],
    ["小計", "700万円", "", "", ""],
]
for d in ad_data_2:
    row += 1
    add_data_row(ws3, row, d, phase2_fill)

# =====================================
# Sheet 4: Phase3 発売後
# =====================================
ws4 = wb.create_sheet("Phase3_発売後")
set_column_widths(ws4, [25, 30, 10, 12, 12])

ws4.cell(row=1, column=1, value="Phase 3：発売後（UGC醸成）【1,150万円】").font = Font(bold=True, size=14)
ws4.cell(row=2, column=1, value="目的：UGCの醸成・継続的な話題化").font = Font(size=11)

row = 4
ws4.cell(row=row, column=1, value="■ 3-1. アレンジ系コンテンツ【280万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws4, row, ["施策", "内容", "人数", "単価", "金額"], header_fill)
data_3_1 = [
    ["ミドルKOL（TikTok）", "チーズ/卵/〆ご飯等", "3名", "70万円", "210万円"],
    ["マイクロKOL（TikTok）", "バリエーション展開", "2名", "20万円", "40万円"],
    ["X ミドルKOL", "アレンジ投稿", "1名", "30万円", "30万円"],
    ["小計", "", "", "", "280万円"],
]
for d in data_3_1:
    row += 1
    add_data_row(ws4, row, d, phase3_fill)

row += 2
ws4.cell(row=row, column=1, value="■ 3-2. SNSで話題のHOOK【200万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws4, row, ["施策", "内容", "人数", "単価", "金額"], header_fill)
data_3_2 = [
    ["ミドルKOL（TikTok）", "○○見ながら訴求", "2名", "70万円", "140万円"],
    ["マイクロKOL", "サブ投稿", "3名", "20万円", "60万円"],
    ["小計", "", "", "", "200万円"],
]
for d in data_3_2:
    row += 1
    add_data_row(ws4, row, d, phase3_fill)

row += 2
ws4.cell(row=row, column=1, value="■ 3-3. ミーム系チャレンジ【270万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws4, row, ["施策", "内容", "人数", "単価", "金額"], header_fill)
data_3_3 = [
    ["ペイドKOL", "チャレンジ火付け役", "4名", "50万円", "200万円"],
    ["チャレンジ運用費", "ハッシュタグ管理等", "-", "-", "70万円"],
    ["小計", "", "", "", "270万円"],
]
for d in data_3_3:
    row += 1
    add_data_row(ws4, row, d, phase3_fill)

row += 2
ws4.cell(row=row, column=1, value="■ 発売後 広告配信【400万円】").font = Font(bold=True, size=11)
row += 1
add_header_row(ws4, row, ["媒体", "金額", "用途", "", ""], header_fill)
ad_data_3 = [
    ["TikTok", "250万円", "アレンジ・ミーム拡散", "", ""],
    ["Instagram", "150万円", "Reelsリターゲティング", "", ""],
    ["小計", "400万円", "", "", ""],
]
for d in ad_data_3:
    row += 1
    add_data_row(ws4, row, d, phase3_fill)

# =====================================
# Sheet 5: KOLサマリー
# =====================================
ws5 = wb.create_sheet("KOLサマリー")
set_column_widths(ws5, [20, 10, 15])

ws5.cell(row=1, column=1, value="KOL起用サマリー【34名・2,900万円】").font = Font(bold=True, size=14)

row = 3
add_header_row(ws5, row, ["カテゴリ", "人数", "金額"], header_fill)
kol_summary = [
    ["メガKOL（100万↑）", "3名", "900万円"],
    ["ミドルKOL（10-50万）", "25名", "1,850万円"],
    ["マイクロKOL（1-10万）", "6名", "150万円"],
    ["合計", "34名", "2,900万円"],
]
for d in kol_summary:
    row += 1
    add_data_row(ws5, row, d)

# =====================================
# Sheet 6: 広告配信サマリー
# =====================================
ws6 = wb.create_sheet("広告配信サマリー")
set_column_widths(ws6, [15, 12, 12, 12, 12])

ws6.cell(row=1, column=1, value="広告配信サマリー【1,500万円】").font = Font(bold=True, size=14)

row = 3
add_header_row(ws6, row, ["フェーズ", "TikTok", "X", "Instagram", "計"], header_fill)
ad_summary = [
    ["発売前", "100万円", "200万円", "-", "300万円"],
    ["発売期", "500万円", "200万円", "-", "700万円"],
    ["発売後", "250万円", "-", "150万円", "400万円"],
    ["合計", "850万円", "400万円", "150万円", "1,500万円"],
]
for d in ad_summary:
    row += 1
    add_data_row(ws6, row, d)

# =====================================
# Sheet 7: KPI
# =====================================
ws7 = wb.create_sheet("想定KPI")
set_column_widths(ws7, [15, 25, 15])

ws7.cell(row=1, column=1, value="想定KPI").font = Font(bold=True, size=14)

row = 3
add_header_row(ws7, row, ["フェーズ", "指標", "目標値"], header_fill)
kpi_data = [
    ["発売前", "総リーチ", "800万imp"],
    ["発売前", "X関連投稿数", "1,500件"],
    ["発売期", "TikTok総再生数", "5,000万再生"],
    ["発売期", "エンゲージメント率", "5%以上"],
    ["発売後", "UGC投稿数", "8,000件"],
    ["発売後", "チャレンジ参加数", "800件"],
]
for d in kpi_data:
    row += 1
    add_data_row(ws7, row, d)

# ファイル保存
output_path = "/Users/rikohayashi/Downloads/AP/辛い麺_メディアプラン_5000万.xlsx"
wb.save(output_path)
print(f"Excel file created: {output_path}")
